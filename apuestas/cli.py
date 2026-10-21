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
import logging
import sys
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from .analyzer import analyze_fixture, candidates
from .api_football import ApiError, ApiFootball
from .backtest import backtest_liga, render_backtest
from .collector import ANULADOS, Collector
from .combinadas import Leg, build_combos
from .config import FECHA_INICIO, Config, load_config
from .db import Database
from .football_data import FootballData, validate_day
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
        api = ApiFootball(cfg.api_football_key, cfg.presupuesto_peticiones)
        Collector(api, db, cfg).collect_day(fecha, con_jugadores=not args.sin_jugadores,
                                            con_cuotas=not args.sin_cuotas_api)
        log.info("Peticiones usadas: %d (quedan hoy según la API: %s)", api.peticiones, api.restantes_hoy)

    fixtures = [dict(r) for r in db.fixtures_on(fecha) if r["status"] not in ANULADOS]
    if cfg.ligas:
        fixtures = [f for f in fixtures if f["league_id"] in cfg.ligas]
    historico = None
    if cfg.usar_historico:
        historico = ModeloHistorico(Historico(cfg.historico_dir), cfg.ligas_historico, cfg.temporadas_historico,
                                    date.fromisoformat(fecha))
    analyses = [analyze_fixture(db, fx, cfg, con_jugadores=not args.sin_jugadores, historico=historico)
                for fx in fixtures]
    analyses = [a for a in analyses if a.ok] + [a for a in analyses if not a.ok]

    picks, legs = {}, []
    for a in analyses:
        if not a.ok:
            continue
        sel = candidates(a, cfg, sin_cuotas=args.incluir_sin_cuota)
        sel.sort(key=lambda m: ((m.edge or 0), m.final_prob or m.prob), reverse=True)
        picks[a.fixture["id"]] = sel[:SELECCIONES_POR_PARTIDO]
        partido = f"{a.fixture['home_name']} vs {a.fixture['away_name']}"
        legs += [Leg(a.fixture["id"], partido, m) for m in sel]

    combos = build_combos(legs, cfg.prob_min_combinada, cfg.max_selecciones_combinada)
    md, js = write_reports(cfg.reportes_dir, fecha, analyses, picks, combos)
    save_picks(db, fecha, picks, combos)

    analizados = sum(a.ok for a in analyses)
    print(f"{analizados} de {len(analyses)} partidos analizados el {fecha}.")
    for perfil, lista in combos.items():
        for c in lista[:1]:
            legs_txt = " + ".join(f"{l.market.label}" for l in c.legs)
            print(f"  [{perfil}] prob {c.prob * 100:.0f}% cuota {c.odd:.2f}: {legs_txt}")
    print(f"Informe: {md}\nDatos: {js}\n")
    print(AVISO.replace("> ", "").replace("**", ""))
    return 0


def cmd_actualizar(args, cfg: Config, db: Database) -> int:
    fecha = _fecha(args.fecha, cfg, offset=-1)
    api = ApiFootball(cfg.api_football_key, cfg.presupuesto_peticiones)
    n = Collector(api, db, cfg).update_results(fecha, con_jugadores=not args.sin_jugadores)
    liquidadas = settle_pending(db)
    print(f"{n} partidos terminados guardados del {fecha}; {liquidadas} selecciones liquidadas. "
          f"Peticiones usadas: {api.peticiones}.")
    return 0


def cmd_diario(args, cfg: Config, db: Database) -> int:
    args.fecha = None
    if _hoy(cfg) - timedelta(days=1) >= FECHA_INICIO:
        cmd_actualizar(args, cfg, db)
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
    md.write_text(render_backtest(resultados, desde, args.peso, args.valor), encoding="utf-8")
    print(f"Informe completo (apuestas simuladas, CLV y calibración): {md}")
    return 0


def cmd_predecir(args, cfg: Config, db: Database) -> int:
    hoy = _hoy(cfg)
    analyses, picks, combos = predecir(cfg, hoy, args.dias, _ligas_arg(args.ligas, cfg), args.incluir_sin_cuota)
    if not analyses:
        print("football-data.co.uk no publica partidos de esas ligas para los próximos días.")
        return 0
    md, js = write_reports(cfg.reportes_dir, hoy.isoformat(), analyses, picks, combos, prefijo="predicciones-",
                           titulo="Predicciones del modelo histórico")
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
