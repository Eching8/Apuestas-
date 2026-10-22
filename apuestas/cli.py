"""Línea de comandos.

    python -m apuestas analizar              # partidos de hoy: descarga, analiza, combinadas, informe
    python -m apuestas actualizar            # resultados de ayer + liquidación de selecciones
    python -m apuestas diario                # actualizar (ayer) + analizar (hoy), para programarlo
    python -m apuestas validar --fecha 2026-10-21
    python -m apuestas rendimiento
    python -m apuestas historico             # descarga el historial de football-data.co.uk
    python -m apuestas backtest              # ¿el modelo histórico le gana a las casas?
    python -m apuestas predecir --dias 3     # próximos partidos solo con el modelo histórico
"""
from __future__ import annotations

import argparse
import json
import logging
import sys
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from .analyzer import analyze_fixture, candidates, combinadas_extra
from .api_football import ApiError
from .api_football import REGISTRO_USO, leer_registro
from .api_football import estado as estado_api
from .backtest import backtest_conteos, backtest_liga, render_backtest, render_conteos
from .collector import ANULADOS, POR_JUGAR, Collector
from .combinadas import Leg, build_combos
from .config import FECHA_INICIO, Config, ligas_filtro, load_config
from .db import Database
from .chequeo import agenda, chequear, render_chequeo
from .football_data import FootballData, validate_day
from .fuentes import cliente_bzzoiro, cliente_partidos, enriquecer, estado_fuentes
from .historico import NOMBRES_LIGA, Historico
from .predicciones import predecir
from .puente import ModeloHistorico
from .report import AVISO, save_picks, write_reports
from .settle import settle_pending, summary

log = logging.getLogger("apuestas")
SELECCIONES_POR_PARTIDO = 8


def _hoy(cfg: Config) -> date:
    return datetime.now(ZoneInfo(cfg.zona_horaria)).date()


def _fecha(value: str | None, cfg: Config, offset: int = 0) -> str:
    if value:
        return date.fromisoformat(value).isoformat()
    return (_hoy(cfg) + timedelta(days=offset)).isoformat()


def cmd_analizar(args, cfg: Config, db: Database) -> int:
    fecha = _fecha(args.fecha, cfg)
    if date.fromisoformat(fecha) < FECHA_INICIO:
        log.error("El seguimiento empieza el %s; usa una fecha igual o posterior.", FECHA_INICIO)
        return 2
    if not args.sin_descarga:
        api = getattr(args, "api", None) or cliente_partidos(cfg)
        listos = Collector(api, db, cfg).collect_day(fecha, con_jugadores=not args.sin_jugadores,
                                                     con_cuotas=not args.sin_cuotas_api)
        log.info("Peticiones usadas: %d (quedan hoy según la API: %s)", api.peticiones, api.restantes_hoy)
        # Árbitro y cuotas de Bzzoiro y SportsGameOdds, solo para los partidos que se van a analizar.
        if not args.sin_cuotas_api:
            for nota in enriquecer(db, cfg, [dict(db.fixture(i)) for i in listos]):
                log.info("%s", nota)

    fixtures = [dict(r) for r in db.fixtures_on(fecha) if r["status"] not in ANULADOS]
    filtro = ligas_filtro(cfg)
    if filtro:
        fixtures = [f for f in fixtures if f["league_id"] in filtro]
    historico = _modelo_historico(cfg, fecha)
    analyses = [analyze_fixture(db, fx, cfg, con_jugadores=not args.sin_jugadores, historico=historico)
                for fx in fixtures]
    analyses = [a for a in analyses if a.ok] + [a for a in analyses if not a.ok]

    # Solo se recomiendan partidos que aún no han empezado (los demás quedan en el informe como referencia).
    por_jugar = [a for a in analyses if a.ok and a.fixture["status"] in POR_JUGAR]
    picks, legs = {}, []
    for a in por_jugar:
        sel = candidates(a, cfg, sin_cuotas=args.incluir_sin_cuota)
        sel.sort(key=lambda m: ((m.edge or 0), m.final_prob or m.prob), reverse=True)
        picks[a.fixture["id"]] = sel[:SELECCIONES_POR_PARTIDO]
        partido = f"{a.fixture['home_name']} vs {a.fixture['away_name']}"
        legs += [Leg(a.fixture["id"], partido, m) for m in sel]

    combos = build_combos(legs, cfg.prob_min_combinada, cfg.max_selecciones_combinada)
    combos["loteria"], builders = combinadas_extra(por_jugar, cfg)
    md, js = write_reports(cfg.reportes_dir, fecha, analyses, picks, combos, builders=builders)
    save_picks(db, fecha, picks, combos)

    analizados = sum(a.ok for a in analyses)
    print(f"{analizados} de {len(analyses)} partidos analizados el {fecha}; {len(por_jugar)} aún por jugar.")
    for perfil, lista in combos.items():
        for c in lista[:1]:
            legs_txt = " + ".join(f"{l.market.label}" for l in c.legs)
            print(f"  [{perfil}] prob {c.prob * 100:.0f}% cuota {c.odd:.2f}: {legs_txt}")
    print(f"Informe: {md}\nDatos: {js}\n")
    print(AVISO.replace("> ", "").replace("**", ""))
    return 0


def cmd_actualizar(args, cfg: Config, db: Database) -> int:
    fecha = _fecha(args.fecha, cfg, offset=-1)
    api = getattr(args, "api", None) or cliente_partidos(cfg)
    n = Collector(api, db, cfg).update_results(fecha, con_jugadores=not args.sin_jugadores)
    liquidadas = settle_pending(db)
    print(f"{n} partidos terminados guardados del {fecha}; {liquidadas} selecciones liquidadas. "
          f"Peticiones usadas: {api.peticiones}.")
    return 0


def cmd_diario(args, cfg: Config, db: Database) -> int:
    args.fecha = None
    # Un solo presupuesto para las dos fases: el resto del día queda para los chequeos de alineación.
    # Los resultados de ayer tienen un tope propio para que no se coman el análisis de hoy.
    args.api = cliente_partidos(cfg)
    total = args.api.presupuesto
    if cfg.fuente == "api-football":
        args.api.presupuesto = min(total, cfg.presupuesto_actualizar)
    if _hoy(cfg) - timedelta(days=1) >= FECHA_INICIO:
        cmd_actualizar(args, cfg, db)
    args.api.presupuesto = total
    args.sin_descarga = False
    return cmd_analizar(args, cfg, db)


def cmd_validar(args, cfg: Config, db: Database) -> int:
    if not cfg.football_data_key:
        log.error("Falta FOOTBALL_DATA_KEY (gratis en https://www.football-data.org/client/register).")
        return 2
    fecha = _fecha(args.fecha, cfg)
    res = validate_day(db, FootballData(cfg.football_data_key), fecha)
    print(f"Validación {fecha} con football-data.org: {res}")
    for r in db.conn.execute(
        """SELECT v.detail, h.name AS home, a.name AS away FROM validations v JOIN fixtures f ON f.id = v.fixture_id
           JOIN teams h ON h.id = f.home_id JOIN teams a ON a.id = f.away_id WHERE f.fecha_local = ? AND v.ok = 0""",
        (fecha,),
    ):
        print(f"  Discrepancia {r['home']} vs {r['away']}: {r['detail']}")
    return 0


def cmd_rendimiento(args, cfg: Config, db: Database) -> int:
    s = summary(db)
    if not s["selecciones"] and not s["combinadas"]:
        print("Aún no hay selecciones liquidadas. Ejecuta 'actualizar' después de los partidos.")
        return 0
    print("Selecciones sueltas por mercado (beneficio apostando 1 unidad a la cuota mediana):")
    for r in s["selecciones"]:
        ben = "-" if r["beneficio"] is None else f"{r['beneficio']:+.2f} u en {r['con_cuota']} con cuota"
        print(f"  {r['tipo']:<12} n={r['n']:<4} acierto {r['acierto'] * 100:5.1f}%  "
              f"prob. media {r['prob_media'] * 100:5.1f}%  {ben}")
    print("Combinadas:")
    for r in s["combinadas"]:
        ben = "-" if r["beneficio"] is None else f"{r['beneficio']:+.2f} u"
        print(f"  {r['perfil']:<18} n={r['n']:<4} acierto {r['acierto'] * 100:5.1f}%  "
              f"prob. media {r['prob_media'] * 100:5.1f}%  {ben}")
    print("\nSi el acierto real queda por debajo de la probabilidad media, el modelo es optimista: "
          "sube APUESTAS_PROB_MIN o baja APUESTAS_PESO_MODELO.")
    return 0


def _modelo_historico(cfg: Config, fecha: str) -> ModeloHistorico | None:
    if not cfg.usar_historico:
        return None
    return ModeloHistorico(Historico(cfg.historico_dir), cfg.ligas_historico, cfg.temporadas_historico,
                           date.fromisoformat(fecha))


def cmd_chequeo(args, cfg: Config, db: Database) -> int:
    fecha = _fecha(args.fecha, cfg)
    api = cliente_partidos(cfg, cfg.presupuesto_chequeo if cfg.fuente == "api-football" else 60)
    resultados = chequear(db, api, cfg, fecha, ventana_min=args.ventana, historico=_modelo_historico(cfg, fecha),
                          forzar=args.forzar, con_cuotas=not args.sin_cuotas_api, bzzoiro=cliente_bzzoiro(cfg))
    if not resultados:
        print(f"Ningún partido con selecciones empieza en los próximos {args.ventana} minutos (o ya están chequeados).")
    for r in resultados:
        print(f"\n{r.partido} ({r.inicio_utc[11:16]} UTC) — {r.estado}")
        for n in r.notas:
            print(f"  · {n}")
        for t in r.confirmadas:
            print(f"  ✅ {t}")
        for t in r.anuladas:
            print(f"  ❌ {t}")
        for t in r.nuevas:
            print(f"  🆕 {t}")
    cfg.reportes_dir.mkdir(parents=True, exist_ok=True)
    md = cfg.reportes_dir / f"{fecha}-chequeo.md"
    md.write_text(render_chequeo(db, fecha), encoding="utf-8")
    print(f"\nPeticiones usadas: {api.peticiones} (quedan hoy según la API: {api.restantes_hoy}). Informe: {md}")
    if any(r.estado == "esperando" for r in resultados):
        print("PENDIENTE: hay alineaciones sin publicar; vuelve a ejecutar 'chequeo' en 10-15 minutos.")
    return 0


def cmd_remates(args, cfg: Config, db: Database) -> int:
    """Mejor pick de remates por jugador en cada partido y combinada de cuota alta por tanda horaria."""
    from .chequeo import alineaciones_bzzoiro, parse_alineaciones
    from .remates import (candidatos_mixtos, combinada, combinada_mixta, picks, proyectar, render,
                          render_mixta)
    fecha = _fecha(args.fecha, cfg)
    ligas = [int(x) for x in args.ligas.split(",")] if args.ligas else ligas_filtro(cfg)
    fixtures = [dict(r) for r in db.fixtures_on(fecha)
                if r["status"] in POR_JUGAR and (not ligas or r["league_id"] in ligas)]
    if not fixtures:
        print(f"No hay partidos pendientes de esas ligas el {fecha} en la base (ejecuta antes 'analizar').")
        return 0
    historico = _modelo_historico(cfg, fecha)
    ahora = datetime.now(ZoneInfo("UTC"))
    api = cliente_partidos(cfg, 60) if args.alineaciones else None
    bz, eventos_bz = (cliente_bzzoiro(cfg), None) if args.alineaciones else (None, None)
    analisis = []
    alineaciones_por_partido: dict[int, dict] = {}
    for fx in fixtures:
        al = None
        inicio = datetime.fromisoformat(fx["date_utc"])
        if api is not None and inicio - ahora <= timedelta(minutes=args.ventana):
            try:
                al = parse_alineaciones(api.alineaciones(fx["id"]))
                if not (fx["home_id"] in al and fx["away_id"] in al) and bz is not None:
                    if eventos_bz is None:
                        eventos_bz = bz.partidos(inicio.date(), inicio.date())
                    al_bz, _, _ = alineaciones_bzzoiro(bz, db, fx, eventos_bz)
                    al = al_bz or al
            except Exception as e:      # una fuente caída no debe tumbar el resto del análisis
                log.warning("Alineación de %s vs %s no disponible: %s", fx["home_name"], fx["away_name"], e)
        if al and fx["home_id"] in al and fx["away_id"] in al:
            alineaciones_por_partido[fx["id"]] = al
        analisis.append(proyectar(db, cfg, fx, historico, al))
    grupos: dict[str, list] = {}
    for hora in sorted({an.fixture["date_utc"][11:16] for an in analisis}):
        mejores = [ps[0] for an in analisis if an.fixture["date_utc"][11:16] == hora and (ps := picks(an))]
        grupos[hora] = combinada(mejores, args.objetivo, args.max_legs)
    texto = render(fecha, analisis, grupos, args.objetivo)
    if args.mixta:
        # Todos los mercados: el análisis completo del partido (ajustado por la alineación si la hay)
        # más el mejor pick de remates de jugador.
        from .chequeo import aplicar_impacto, impacto_alineacion
        mixtos: dict[str, list[list]] = {}
        for an in analisis:
            fx = an.fixture
            factores = {}
            if an.con_alineacion and alineaciones_por_partido.get(fx["id"]):
                al = alineaciones_por_partido[fx["id"]]
                for tid, nombre in ((fx["home_id"], fx["home_name"]), (fx["away_id"], fx["away_name"])):
                    factores[tid] = impacto_alineacion(db, tid, nombre, fx["date_utc"], al[tid]["titulares"]).factor
            a = analyze_fixture(db, fx, cfg, con_jugadores=False, historico=historico,
                                ajuste=lambda e, f=factores, fx=fx: aplicar_impacto(e, f.get(fx["home_id"], 1.0),
                                                                                f.get(fx["away_id"], 1.0)))
            mixtos.setdefault(fx["date_utc"][11:16], []).append(candidatos_mixtos(a, an))
        grupos_mixtos = {h: combinada_mixta(c, args.objetivo, args.max_legs + 2) for h, c in sorted(mixtos.items())}
        texto += "\n\n" + render_mixta(fecha, grupos_mixtos, args.objetivo)
    cfg.reportes_dir.mkdir(parents=True, exist_ok=True)
    md = cfg.reportes_dir / f"remates-{fecha}.md"
    md.write_text(texto, encoding="utf-8")
    print(texto)
    print(f"\nInforme: {md}")
    return 0


def cmd_fuentes(args, cfg: Config, db: Database) -> int:
    print(f"Fuente principal: {cfg.fuente}")
    todo_ok = True
    for nombre, ok, detalle in estado_fuentes(cfg):
        print(f"  {'✅' if ok else '⚠️ '} {nombre}: {detalle}")
        if not ok and nombre.startswith(cfg.fuente.split("-")[0].upper()[:4]):
            todo_ok = False
    return 0 if todo_ok else 1


def cmd_api(args, cfg: Config, db: Database) -> int:
    try:
        r = estado_api(api_key=cfg.api_football_key)
    except (ApiError, OSError) as e:
        print(f"API-Football: NO DISPONIBLE — {e}")
        return 1
    origen = "API_FOOTBALL_KEY" if cfg.api_football_key else "network secret (la añade el proxy)"
    sub_ = r.get("subscription") or {}
    req = r.get("requests") or {}
    propio = leer_registro(REGISTRO_USO)
    print(f"API-Football: OK — clave por {origen}; plan {sub_.get('plan', '?')}; "
          f"peticiones hoy según /status {req.get('current', '?')} de {req.get('limit_day', '?')}; "
          f"según el registro propio {propio.get('peticiones', 0)} (restantes {propio.get('restantes', '?')})")
    return 0


def cmd_agenda(args, cfg: Config, db: Database) -> int:
    fecha = _fecha(args.fecha, cfg)
    momentos = agenda(db, fecha, antelacion_min=args.antelacion)
    if args.json:
        print(json.dumps(momentos, ensure_ascii=False))
        return 0
    if not momentos:
        print(f"No quedan partidos con selecciones por chequear el {fecha}.")
    zona = ZoneInfo(cfg.zona_horaria)
    for m in momentos:
        local = datetime.fromisoformat(m["chequeo_utc"]).astimezone(zona).strftime("%H:%M")
        print(f"Chequeo a las {m['chequeo_utc'][11:16]} UTC ({local} hora local): {', '.join(m['partidos'])}")
    return 0


def _ligas_arg(value: str | None, cfg: Config) -> list[str]:
    ligas = [x.strip().upper() for x in value.split(",")] if value else cfg.ligas_historico
    desconocidas = [l for l in ligas if l not in NOMBRES_LIGA]
    if desconocidas:
        raise SystemExit(f"Ligas desconocidas: {', '.join(desconocidas)}. Disponibles: {', '.join(NOMBRES_LIGA)}")
    return ligas


def cmd_historico(args, cfg: Config, db: Database) -> int:
    ligas = _ligas_arg(args.ligas, cfg)
    partidos = Historico(cfg.historico_dir).partidos(ligas, args.temporadas or cfg.temporadas_historico, _hoy(cfg))
    print(f"{len(partidos)} partidos jugados guardados en {cfg.historico_dir}")
    for liga in ligas:
        ps = [p for p in partidos if p.liga == liga]
        if not ps:
            print(f"  {liga:<4} {NOMBRES_LIGA[liga]:<26} sin datos")
            continue
        con_stats = sum("shots_on" in p.stats for p in ps) / len(ps)
        con_cuotas = sum(bool(p.cuotas_cierre) for p in ps) / len(ps)
        print(f"  {liga:<4} {NOMBRES_LIGA[liga]:<26} {len(ps):>5} partidos  {ps[0].fecha} → {ps[-1].fecha}  "
              f"estadísticas {con_stats:4.0%}  cuotas {con_cuotas:4.0%}")
    return 0


def cmd_backtest(args, cfg: Config, db: Database) -> int:
    ligas = _ligas_arg(args.ligas, cfg)
    desde = date.fromisoformat(args.desde)
    hoy = _hoy(cfg)
    # Temporadas de entrenamiento previas a la primera de prueba, más las de prueba.
    temporadas = (hoy.year - desde.year) + 3
    partidos = Historico(cfg.historico_dir).partidos(ligas, temporadas, hoy)
    resultados = []
    for liga in ligas:
        r = backtest_liga(partidos, liga, desde)
        if not r.predicciones:
            print(f"{liga}: sin datos suficientes")
            continue
        resultados.append(r)
        m = r.metricas(args.peso)["1x2"]
        if m["modelo"]:
            print(f"{NOMBRES_LIGA[liga]:<26} 1X2 log-loss  modelo {m['modelo']['logloss']:.4f}  "
                  f"mezcla {m[f'mezcla_{args.peso:.2f}']['logloss']:.4f}  "
                  f"previas {m['cuotas_previas']['logloss']:.4f}  cierre {m['cuotas_cierre']['logloss']:.4f}  "
                  f"(n={m['modelo']['n']})")
    if not resultados:
        return 1
    cfg.reportes_dir.mkdir(parents=True, exist_ok=True)
    md = cfg.reportes_dir / f"backtest-{hoy.isoformat()}.md"
    texto = render_backtest(resultados, desde, args.peso, args.valor)
    if args.conteos:
        conteos = []
        for r in resultados:
            c = backtest_conteos(partidos, r.liga, desde)
            if any(c.filas.values()):
                conteos.append(c)
                resumen = "  ".join(f"{s} {m['modelo']:.3f}/{m['media_liga']:.3f}" for s, m in c.metricas().items())
                print(f"{NOMBRES_LIGA[r.liga]:<26} conteos (modelo/media liga)  {resumen}")
        texto += "\n" + render_conteos(conteos)
    md.write_text(texto, encoding="utf-8")
    print(f"Informe completo (apuestas simuladas, CLV y calibración): {md}")
    return 0


def cmd_predecir(args, cfg: Config, db: Database) -> int:
    hoy = _hoy(cfg)
    analyses, picks, combos = predecir(cfg, hoy, args.dias, _ligas_arg(args.ligas, cfg), args.incluir_sin_cuota)
    combos["loteria"], builders = combinadas_extra(analyses, cfg)
    if not analyses:
        print("football-data.co.uk no publica partidos de esas ligas para los próximos días.")
        return 0
    md, js = write_reports(cfg.reportes_dir, hoy.isoformat(), analyses, picks, combos, prefijo="predicciones-",
                           titulo="Predicciones del modelo histórico", builders=builders)
    for a in analyses:
        fx = a.fixture
        sel = picks.get(fx["id"], [])
        mejor = f"  → {sel[0].label} ({(sel[0].final_prob or sel[0].prob) * 100:.0f}%, cuota {sel[0].odd or sel[0].fair_odd:.2f})" if sel else ""
        if a.expectation is None:
            print(f"{fx['cuando'][:10]} {fx['league_country']:<4} {fx['home_name']} vs {fx['away_name']}: {'; '.join(a.notas)}")
            continue
        r = {m.key: m.prob for m in a.markets}
        print(f"{fx['cuando'][:10]} {fx['league_country']:<4} {fx['home_name']} vs {fx['away_name']}: "
              f"1 {r['result:1']:.0%}  X {r['result:X']:.0%}  2 {r['result:2']:.0%}  "
              f"+2.5 {r['goals:total:over:2.5']:.0%}  goles {a.expectation.home['goals']:.2f}-{a.expectation.away['goals']:.2f}"
              f"{mejor}")
    print(f"\nInforme: {md}\nDatos: {js}\n")
    print(AVISO.replace("> ", "").replace("**", ""))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="apuestas", description="Analizador diario de partidos y combinadas")
    p.add_argument("-v", "--verbose", action="store_true")
    sub = p.add_subparsers(dest="cmd", required=True)

    def comunes(sp, fecha_help):
        sp.add_argument("--fecha", help=fecha_help)
        sp.add_argument("--sin-jugadores", action="store_true", help="no descargar ni analizar jugadores (ahorra peticiones)")

    a = sub.add_parser("analizar", help="analiza los partidos de un día y genera combinadas")
    comunes(a, "AAAA-MM-DD (por defecto, hoy)")
    a.add_argument("--sin-descarga", action="store_true", help="usar solo lo que ya está en la base")
    a.add_argument("--sin-cuotas-api", action="store_true", help="no descargar cuotas")
    a.add_argument("--incluir-sin-cuota", action="store_true",
                   help="incluir selecciones sin cuota disponible (se usa la cuota justa del modelo)")
    a.set_defaults(func=cmd_analizar)

    u = sub.add_parser("actualizar", help="guarda resultados y estadísticas de un día jugado y liquida")
    comunes(u, "AAAA-MM-DD (por defecto, ayer)")
    u.set_defaults(func=cmd_actualizar)

    d = sub.add_parser("diario", help="actualizar ayer + analizar hoy")
    comunes(d, argparse.SUPPRESS)
    d.add_argument("--sin-cuotas-api", action="store_true")
    d.add_argument("--incluir-sin-cuota", action="store_true")
    d.set_defaults(func=cmd_diario)

    v = sub.add_parser("validar", help="contrasta horarios y marcadores con football-data.org")
    v.add_argument("--fecha")
    v.set_defaults(func=cmd_validar)

    r = sub.add_parser("rendimiento", help="acierto real del modelo con las selecciones liquidadas")
    r.set_defaults(func=cmd_rendimiento)

    ch = sub.add_parser("chequeo", help="alineaciones + cuotas actuales antes del partido -> apuestas finales")
    ch.add_argument("--fecha", help="AAAA-MM-DD (por defecto, hoy)")
    ch.add_argument("--ventana", type=int, default=60, help="minutos hacia delante (por defecto 60)")
    ch.add_argument("--forzar", action="store_true", help="repetir partidos ya chequeados")
    ch.add_argument("--sin-cuotas-api", action="store_true", help="no volver a pedir cuotas (ahorra peticiones)")
    ch.set_defaults(func=cmd_chequeo)

    ap = sub.add_parser("api", help="comprueba la clave y el consumo de API-Football (no gasta peticiones)")
    ap.set_defaults(func=cmd_api)

    re_ = sub.add_parser("remates", help="mejores picks de remates por jugador y combinada de cuota alta")
    re_.add_argument("--fecha", help="AAAA-MM-DD (por defecto, hoy)")
    re_.add_argument("--ligas", help="ids de liga (API-Football) separados por comas; por defecto las prioritarias")
    re_.add_argument("--objetivo", type=float, default=100.0, help="cuota total objetivo de cada combinada")
    re_.add_argument("--max-legs", type=int, default=6, help="máximo de selecciones por combinada")
    re_.add_argument("--alineaciones", action="store_true",
                     help="usar alineaciones confirmadas (ESPN, con Bzzoiro de respaldo) de los partidos cercanos")
    re_.add_argument("--ventana", type=int, default=75, help="minutos antes del inicio para buscar alineación")
    re_.add_argument("--mixta", action="store_true",
                     help="añadir una combinada de cuota alta con todos los mercados (un pick por partido)")
    re_.set_defaults(func=cmd_remates)

    fu = sub.add_parser("fuentes", help="estado y consumo de ESPN, Bzzoiro, SportsGameOdds y API-Football")
    fu.set_defaults(func=cmd_fuentes)

    ag = sub.add_parser("agenda", help="a qué horas ejecutar 'chequeo' hoy")
    ag.add_argument("--fecha", help="AAAA-MM-DD (por defecto, hoy)")
    ag.add_argument("--antelacion", type=int, default=35, help="minutos antes del primer partido de cada grupo")
    ag.add_argument("--json", action="store_true")
    ag.set_defaults(func=cmd_agenda)

    ayuda_ligas = "códigos de football-data.co.uk separados por comas (por defecto APUESTAS_LIGAS_HISTORICO)"
    h = sub.add_parser("historico", help="descarga/actualiza el historial de football-data.co.uk")
    h.add_argument("--ligas", help=ayuda_ligas)
    h.add_argument("--temporadas", type=int, help="temporadas hacia atrás (por defecto APUESTAS_TEMPORADAS)")
    h.set_defaults(func=cmd_historico)

    b = sub.add_parser("backtest", help="evalúa el modelo histórico contra las cuotas reales")
    b.add_argument("--ligas", help=ayuda_ligas)
    b.add_argument("--desde", default="2024-07-01", help="primer día de prueba (AAAA-MM-DD)")
    b.add_argument("--peso", type=float, default=None, help="peso del modelo en la mezcla con el mercado")
    b.add_argument("--valor", type=float, default=None, help="valor mínimo para apostar en la simulación")
    b.add_argument("--conteos", action="store_true",
                   help="evaluar también córners, tarjetas, remates y atajadas (más lento)")
    b.set_defaults(func=cmd_backtest)

    pr = sub.add_parser("predecir", help="predice los próximos partidos con el modelo histórico (sin API)")
    pr.add_argument("--ligas", help=ayuda_ligas)
    pr.add_argument("--dias", type=int, default=3, help="días hacia delante (por defecto 3)")
    pr.add_argument("--incluir-sin-cuota", action="store_true",
                    help="incluir selecciones sin cuota (córners, tarjetas...) con su cuota justa")
    pr.set_defaults(func=cmd_predecir)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO, format="%(levelname)s %(message)s")
    cfg = load_config()
    if getattr(args, "peso", "-") is None:
        args.peso = cfg.peso_modelo
    if getattr(args, "valor", "-") is None:
        args.valor = cfg.valor_min
    db = Database(cfg.db_path)
    try:
        return args.func(args, cfg, db)
    except ApiError as e:
        log.error("%s", e)
        return 1
    finally:
        db.close()


if __name__ == "__main__":
    sys.exit(main())
