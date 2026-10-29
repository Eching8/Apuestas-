"""Línea de comandos: python -m nbaev <grupo> <comando>."""
from __future__ import annotations

import argparse
import logging
import sys
from datetime import date

from . import config

log = logging.getLogger("nbaev")


def _con(cfg, solo_lectura: bool = False):
    from .data import db
    return db.conectar(config.ruta(cfg, "db"), solo_lectura=solo_lectura)


def _espn(cfg):
    from .data.espn import Espn
    return Espn(cfg, crudos=config.ruta(cfg, "crudos"))


def cmd_historial(cfg, args) -> None:
    """Calendario y partidos terminados desde la temporada configurada hasta ayer."""
    from .data import recolector
    con, cli = _con(cfg), _espn(cfg)
    hasta = date.fromisoformat(args.hasta) if args.hasta else recolector.ayer_et()
    desde = args.desde or cfg["temporadas"]["desde"]
    n = recolector.actualizar_calendario(con, cli, desde, hasta, tuple(cfg["temporadas"]["tipos"]))
    log.info("Partidos en calendario actualizados: %d", n)
    r = recolector.descargar_partidos(con, cli, limite=args.limite)
    log.info("Partidos descargados: %s", r)
    log.info("Líneas rellenadas: %s", recolector.rellenar_lineas(con, cli))
    _contexto(con)


def _contexto(con) -> None:
    from .data import contexto
    log.info("Contexto de partidos (descanso, viajes, total implícito): %d filas", contexto.guardar(con))


def cmd_reprocesar(cfg, args) -> None:
    """Vuelve a procesar los partidos desde crudos/ (tras cambiar un parser), sin descargar."""
    from .data import recolector
    con, cli = _con(cfg), _espn(cfg)
    log.info("Reprocesados: %s", recolector.descargar_partidos(con, cli, reprocesar=True))
    _contexto(con)


def cmd_lesiones(cfg, args) -> None:
    from .data import recolector
    con, cli = _con(cfg), _espn(cfg)
    log.info("Lesiones guardadas: %d", recolector.guardar_lesiones(con, cli))


def cmd_cuotas(cfg, args) -> None:
    """Captura las cuotas de props de hoy (SportsGameOdds) con hora de captura."""
    from .data import cuotas_sgo, recolector
    con = _con(cfg)
    fecha = date.fromisoformat(args.fecha) if args.fecha else recolector.hoy_et()
    log.info("Cuotas: %s", cuotas_sgo.capturar_dia(con, cfg, fecha))


def cmd_cuotas_historicas(cfg, args) -> None:
    """Aperturas y cierres de props de partidos pasados (gasta entidades del plan de SportsGameOdds)."""
    from .data import cuotas_sgo
    con = _con(cfg)
    r = cuotas_sgo.descargar_historico(con, cfg, date.fromisoformat(args.desde), date.fromisoformat(args.hasta),
                                       max_partidos=args.max_partidos)
    log.info("Cuotas históricas: %s", r)


def cmd_importar_csv(cfg, args) -> None:
    from .data import cuotas_csv
    con = _con(cfg)
    log.info("Filas importadas: %s", cuotas_csv.importar(con, args.archivo, kind=args.tipo))


def cmd_nba_api(cfg, args) -> None:
    """Métricas avanzadas y tracking de stats.nba.com (solo desde redes no bloqueadas)."""
    from .data import nba_stats
    con = _con(cfg)
    log.info("stats.nba.com: %s", nba_stats.descargar(con, cfg, args.temporada, args.hasta))


def cmd_diario_datos(cfg, args) -> None:
    """Actualización diaria: partidos de ayer, lesiones, cuotas de hoy y emparejamiento de ids."""
    from .data import cuotas_sgo, recolector
    con, cli = _con(cfg), _espn(cfg)
    hoy = recolector.hoy_et()
    recolector.actualizar_calendario(con, cli, recolector.temporada_de(hoy), hoy, tuple(cfg["temporadas"]["tipos"]))
    log.info("Partidos: %s", recolector.descargar_partidos(con, cli))
    log.info("Líneas rellenadas: %s", recolector.rellenar_lineas(con, cli))
    log.info("Lesiones: %d", recolector.guardar_lesiones(con, cli))
    log.info("Líneas de hoy (ESPN): %d", recolector.capturar_lineas_dia(con, cli, hoy.isoformat()))
    if not args.sin_cuotas:
        try:
            # Cierre y resultado de las props de ayer (para CLV y liquidación) y captura de las de hoy.
            ayer = recolector.ayer_et()
            log.info("Cierres de ayer: %s", cuotas_sgo.descargar_historico(con, cfg, ayer, ayer, respetar_reserva=False))
            log.info("Cuotas de hoy: %s", cuotas_sgo.capturar_dia(con, cfg, hoy))
        except Exception as e:
            log.error("No se pudieron descargar las cuotas: %s", e)
    _contexto(con)
    if cfg["fuentes"]["nba_api"]["modo"] != "no":
        from .data import nba_stats
        log.info("stats.nba.com: %s", nba_stats.descargar(con, cfg, recolector.temporada_de(hoy), None))


def cmd_estado(cfg, args) -> None:
    from .data import calidad
    con = _con(cfg, solo_lectura=True)
    print(calidad.informe(con))


def cmd_minutos_validar(cfg, args) -> None:
    """Walk-forward mensual del modelo de minutos e informe en reportes/fase2_minutos.md."""
    from .backtest import minutos as bm
    con = _con(cfg, solo_lectura=True)
    r = bm.validar(con, desde=args.desde)
    # Predicciones fuera de muestra: entrada de la validación de la fase 3 (puntos).
    cache = config.RAIZ / "data" / "cache" / "minutos_oos.parquet"
    cache.parent.mkdir(parents=True, exist_ok=True)
    r["predicciones"].to_parquet(cache)
    ruta = config.RAIZ / "reportes" / "fase2_minutos.md"
    bm.guardar_informe(r, ruta)
    print(bm.informe(r))
    log.info("Informe guardado en %s", ruta)


def cmd_minutos_entrenar(cfg, args) -> None:
    from .models import minutos as mm
    con = _con(cfg, solo_lectura=True)
    m = mm.modelo_vigente(con, cfg, config.RAIZ / cfg["minutos"]["modelo"], forzar=True)
    print(mm.importancia(m).head(10).to_string(index=False))


def cmd_minutos_proyectar(cfg, args) -> None:
    from .data import recolector
    from .models import minutos as mm
    con = _con(cfg)
    fecha = args.fecha or recolector.hoy_et().isoformat()
    out = mm.proyectar(con, cfg, fecha, config.RAIZ / cfg["minutos"]["modelo"])
    if out.empty:
        return
    cols = ["name", "team_id", "estado_lesion", "min_pred", "min_si_juega", "min_q10", "min_q90", "p_dnp", "libres"]
    for gid, g in out.groupby("game_id"):
        print(f"\n== Partido {gid}")
        print(g.sort_values(["team_id", "min_pred"], ascending=[True, False])[cols].round(1).to_string(index=False))


def cmd_puntos_validar(cfg, args) -> None:
    """Walk-forward del modelo de puntos con minutos fuera de muestra -> reportes/fase3_puntos.md."""
    import pandas as pd
    from .backtest import puntos as bp
    cache = config.RAIZ / "data" / "cache" / "minutos_oos.parquet"
    if not cache.exists():
        raise SystemExit("Falta data/cache/minutos_oos.parquet: ejecuta antes `minutos validar --desde 2022-10-01`")
    con = _con(cfg, solo_lectura=True)
    r = bp.validar(con, pd.read_parquet(cache), desde=args.desde, n_sims=args.sims)
    r["pred"].to_parquet(config.RAIZ / "data" / "cache" / "puntos_oos.parquet")
    r["lineas"].to_parquet(config.RAIZ / "data" / "cache" / "puntos_lineas_oos.parquet")
    bp.guardar(r, config.RAIZ / "reportes")
    print(bp.informe(r))


def cmd_puntos_proyectar(cfg, args) -> None:
    from .data import recolector
    from .models import puntos as mp
    con = _con(cfg)
    fecha = args.fecha or recolector.hoy_et().isoformat()
    out, sim = mp.proyectar(con, cfg, fecha, n_sims=cfg["puntos"]["simulaciones"])
    if out.empty:
        return
    cols = ["name", "estado_lesion", "min_si_juega", "pts_media", "pts_q10", "pts_q50", "pts_q90"]
    for gid, g in out.groupby("game_id"):
        print(f"\n== Partido {gid}")
        print(g.sort_values("pts_media", ascending=False)[cols].head(12).round(1).to_string(index=False))
    lin = mp.probabilidades_lineas(con, sim["filas"], sim["sims"])
    if not lin.empty:
        print("\nLíneas capturadas:")
        print(lin.merge(out[["game_id", "player_id", "name"]], on=["game_id", "player_id"])
              [["name", "line", "p_over", "p_under"]].round(3).to_string(index=False))


def cmd_backtest_puntos(cfg, args) -> None:
    """Fase 4: backtest con cuotas reales del mercado de puntos y estado del mercado en el catálogo."""
    import pandas as pd
    from .backtest import fase4
    cache = config.RAIZ / "data" / "cache"
    lin = pd.read_parquet(cache / "puntos_lineas_oos.parquet")
    lin = lin[lin["margen"] >= 0.01]          # sin margen = cuota de relleno de la fuente
    pred = pd.read_parquet(cache / "puntos_oos.parquet")[["game_id", "player_id", "libres"]]
    lin = lin.merge(pred.drop_duplicates(["game_id", "player_id"]), on=["game_id", "player_id"], how="left")
    con = _con(cfg)
    r = fase4.ejecutar(con, lin)
    fase4.guardar_validacion(con, r)
    texto = fase4.informe(r)
    for carpeta in (config.RAIZ / "reportes", config.RAIZ / "docs" / "resultados"):
        carpeta.mkdir(parents=True, exist_ok=True)
        (carpeta / "fase4_backtest_puntos.md").write_text(texto, encoding="utf-8")
    print(texto)


def cmd_diario(cfg, args) -> None:
    """Todo el flujo del día: datos, proyección, comparación con cuotas, picks, registro y banca."""
    from . import diario
    from .data import recolector
    if not args.sin_actualizar:
        cmd_diario_datos(cfg, args)
    con = _con(cfg)
    fecha = args.fecha or recolector.hoy_et().isoformat()
    r = diario.ejecutar(con, cfg, fecha)
    t = r["tabla"]
    log.info("Apuestas liquidadas: %s. Banca: %s", r.get("liquidadas"), r.get("banca"))
    if t.empty:
        return
    picks = t[t["pick"]]
    print(f"\nLíneas evaluadas: {len(t)}; picks: {len(picks)}; con monto: {(picks['monto'] > 0).sum()}")
    cols = ["name", "partido", "market", "period", "line", "lado", "proyeccion", "cuota", "book", "p_justa", "p_final", "edge",
            "ev", "monto", "estado_mercado"]
    print(t.sort_values("ev", ascending=False)[cols].head(15).round(3).to_string(index=False))
    print(f"\nInforme: reportes/diario/{fecha}.md (también .csv y .json)")


def cmd_apuestas(cfg, args) -> None:
    from .betting import registro
    con = _con(cfg)
    if args.cmd == "confirmar":
        registro.confirmar(con, args.id, args.cuota, args.monto)
    elif args.cmd == "descartar":
        registro.descartar(con, args.id)
    elif args.cmd == "liquidar":
        log.info("Liquidadas: %d", registro.liquidar(con))
    print(con.execute("SELECT id, fecha, jugador, market, line, lado, book, cuota, monto, estado, resultado, ganancia, clv "
                      "FROM apuestas ORDER BY id DESC LIMIT 20").df().to_string(index=False))
    print(registro.resumen(con).to_string(index=False))
    print(f"Banca: {registro.banca_actual(con, cfg['apuestas']['banca_inicial']):,.2f}")


def cmd_mercados_validar(cfg, args) -> None:
    """Fase 6: walk-forward de todos los mercados (simulación completa) con minutos fuera de muestra."""
    import pandas as pd
    from .backtest import mercados as bm
    cache = config.RAIZ / "data" / "cache"
    con = _con(cfg, solo_lectura=True)
    r = bm.validar(con, pd.read_parquet(cache / "minutos_oos.parquet"), desde=args.desde, n_sims=args.sims)
    for k in ("pit", "lineas", "maximo"):
        r[k].to_parquet(cache / f"mercados_{k}_oos.parquet")
    print(bm.tabla_pit(r["pit"]).round(3).to_string(index=False))


def cmd_backtest_mercados(cfg, args) -> None:
    """Fase 6: backtest e informe de todos los mercados (necesita `mercados validar`)."""
    import pandas as pd
    from .backtest import fase6
    from .models import primer_anotador as pa
    cache = config.RAIZ / "data" / "cache"
    lin = pd.read_parquet(cache / "mercados_lineas_oos.parquet")
    con = _con(cfg)
    r = fase6.ejecutar(con, lin)
    primer = pa.validar(con, "2024-10-01")["pred"]
    texto = fase6.informe(r, pd.read_parquet(cache / "mercados_pit_oos.parquet"), lin,
                          pd.read_parquet(cache / "mercados_maximo_oos.parquet"), primer)
    for carpeta in (config.RAIZ / "reportes", config.RAIZ / "docs" / "resultados"):
        carpeta.mkdir(parents=True, exist_ok=True)
        (carpeta / "fase6_mercados.md").write_text(texto, encoding="utf-8")
    # Las mezclas modelo + mercado de cada mercado se regeneran con estas líneas, y el estado de los mercados se
    # versiona en config/ para que un clon nuevo (o GitHub Actions) lo tenga sin repetir la validación.
    from . import diario
    (config.RAIZ / cfg["apuestas"]["mezclas"]).unlink(missing_ok=True)
    diario.mezclas_vigentes(cfg)
    estados = con.execute("SELECT market, period, estado, apuestas, roi_cierre, roi_cierre_ic_inf, clv_ajustado, "
                          "CAST(evaluado_at AS VARCHAR) AS evaluado_at FROM market_validation").df()
    (config.RAIZ / "config" / "estado_mercados.json").write_text(
        estados.to_json(orient="records", force_ascii=False, indent=1), encoding="utf-8")
    print(texto)


def _sims_del_dia(cfg, fecha):
    from .data import recolector
    from .models import proyeccion
    fecha = fecha or recolector.hoy_et().isoformat()
    try:
        return proyeccion.cargar_sims(fecha)
    except FileNotFoundError:
        raise SystemExit(f"No hay simulaciones guardadas del {fecha}: ejecuta antes `python -m nbaev diario`")


def cmd_combinada(cfg, args) -> None:
    """Probabilidad conjunta de una combinada con las simulaciones del día.
    Cada --sel es "jugador|mercado|línea|lado|cuota[|prob_justa][|periodo]" (línea vacía en sí/no)."""
    from .betting import combinadas as cb
    filas, sims = _sims_del_dia(cfg, args.fecha)
    sel = []
    for txt in args.sel:
        p = txt.split("|") + [""] * 7
        sel.append(cb.Seleccion(p[0], p[1], float(p[2]) if p[2] else None, p[3], periodo=p[6] or "game",
                                cuota=float(p[4]) if p[4] else None, p_justa=float(p[5]) if p[5] else None))
    r = cb.combinada(filas, sims, sel)
    for k, v in r.items():
        print(f"{k}: {v}")
    if "ev_combinada" in r:
        print("\nLa combinada acumula el margen de cada selección: solo tiene sentido si su EV supera al de las "
              "simples y el mercado está validado.")


def cmd_comparar(cfg, args) -> None:
    from .betting import combinadas as cb
    filas, sims = _sims_del_dia(cfg, args.fecha)
    if args.cmd == "duelo":
        print(cb.duelo(filas, sims, args.a, args.b, args.mercado))
    else:
        gid = filas.loc[filas["name"].str.contains(args.jugador_de_partido, case=False), "game_id"].iloc[0]
        team = None
        if args.equipo:
            team = filas.loc[filas["name"].str.contains(args.jugador_de_partido, case=False), "team_id"].iloc[0]
        print(cb.maximo(filas, sims, gid, args.mercado, team).round(3).to_string(index=False))


def cmd_props(cfg, args) -> None:
    """Las N mejores props del día (tabla de `diario`): mayor EV entre las que pasan todos los filtros,
    máximo 1 por jugador y `--max-partido` por partido. Indica siempre si el mercado está validado."""
    import pandas as pd
    from .data import recolector
    fecha = args.fecha or recolector.hoy_et().isoformat()
    ruta = config.RAIZ / "reportes" / "diario" / f"{fecha}.csv"
    if not ruta.exists():
        raise SystemExit(f"No hay tabla del {fecha}: ejecuta antes `python -m nbaev diario`")
    t = pd.read_csv(ruta)
    p = t[t["pick"]].sort_values("EV", ascending=False)
    p = p.drop_duplicates("jugador").groupby("partido", group_keys=False).head(args.max_partido).head(args.n)
    if p.empty:
        print("Ninguna línea pasa todos los filtros hoy.")
        return
    validados = (p["estado del mercado"] == "validado").sum()
    print(f"Props del {fecha} ({len(p)}; en mercados validados: {validados}).")
    if validados < len(p):
        print("AVISO: las props de mercados no validados son informativas (monto 0): el backtest no demostró "
              "ventaja en esos mercados.")
    for i, (_, r) in enumerate(p.iterrows(), 1):
        linea = "" if pd.isna(r["línea"]) else f" {r['línea']:g}"
        periodo = "" if r["periodo"] == "game" else f" ({r['periodo']})"
        print(f"\n{i}. {r['jugador']} ({r['partido']}) — {r['mercado']}{periodo} {r['lado']}{linea} @ {r['cuota']:.2f} "
              f"({r['casa']})")
        print(f"   proyección {r['proyección']:.2f} · minutos {r['minutos proyectados']:.0f} · prob. final "
              f"{r['prob. final']:.1%} vs justa {r['prob. justa']:.1%} · edge {r['edge']:+.1%} · EV {r['EV']:+.1%} · "
              f"monto {r['monto sugerido']:.2f} · mercado {r['estado del mercado']}")
        if isinstance(r["razones (SHAP)"], str) and r["razones (SHAP)"]:
            print(f"   razones: {r['razones (SHAP)']}")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="nbaev", description="Props NBA con valor esperado")
    ap.add_argument("--config", help="ruta a un YAML de configuración")
    grupos = ap.add_subparsers(dest="grupo", required=True)

    d = grupos.add_parser("datos", help="descarga y mantenimiento de la base").add_subparsers(dest="cmd", required=True)
    p = d.add_parser("historial", help="calendario y box scores/jugada a jugada hasta ayer")
    p.add_argument("--desde", type=int, help="año de inicio de la primera temporada (2021 = 2021-22)")
    p.add_argument("--hasta", help="AAAA-MM-DD (por defecto ayer)")
    p.add_argument("--limite", type=int, help="máximo de partidos a descargar en esta ejecución")
    p.set_defaults(f=cmd_historial)
    d.add_parser("reprocesar", help="rehace las tablas desde crudos/ sin descargar").set_defaults(f=cmd_reprocesar)
    d.add_parser("lesiones", help="captura el parte de lesiones actual").set_defaults(f=cmd_lesiones)
    p = d.add_parser("cuotas", help="captura las cuotas de props del día")
    p.add_argument("--fecha")
    p.set_defaults(f=cmd_cuotas)
    p = d.add_parser("cuotas-historicas", help="aperturas y cierres de partidos pasados (SportsGameOdds)")
    p.add_argument("--desde", required=True)
    p.add_argument("--hasta", required=True)
    p.add_argument("--max-partidos", type=int, help="tope de partidos (entidades) a gastar")
    p.set_defaults(f=cmd_cuotas_historicas)
    p = d.add_parser("importar-csv", help="importa cuotas cargadas a mano (p. ej. bet365)")
    p.add_argument("archivo")
    p.add_argument("--tipo", default="captura", choices=["captura", "apertura", "cierre"])
    p.set_defaults(f=cmd_importar_csv)
    p = d.add_parser("nba-api", help="métricas avanzadas y tracking de stats.nba.com")
    p.add_argument("--temporada", type=int, required=True)
    p.add_argument("--hasta", help="AAAA-MM-DD: datos acumulados hasta esa fecha (sin fuga)")
    p.set_defaults(f=cmd_nba_api)
    p = d.add_parser("diario", help="actualización diaria de datos (sin proyectar)")
    p.add_argument("--sin-cuotas", action="store_true")
    p.set_defaults(f=cmd_diario_datos)
    d.add_parser("estado", help="cobertura y calidad de los datos").set_defaults(f=cmd_estado)

    mi = grupos.add_parser("minutos", help="fase 2: proyección de minutos").add_subparsers(dest="cmd", required=True)
    p = mi.add_parser("validar", help="validación walk-forward mensual")
    p.add_argument("--desde", default="2023-10-01")
    p.set_defaults(f=cmd_minutos_validar)
    mi.add_parser("entrenar", help="entrena con todo el histórico y guarda el modelo").set_defaults(f=cmd_minutos_entrenar)
    p = mi.add_parser("proyectar", help="minutos de los partidos de una fecha")
    p.add_argument("--fecha", help="AAAA-MM-DD (por defecto hoy, hora del este)")
    p.set_defaults(f=cmd_minutos_proyectar)

    pu = grupos.add_parser("puntos", help="fase 3: modelo de puntos").add_subparsers(dest="cmd", required=True)
    p = pu.add_parser("validar", help="validación walk-forward mensual con líneas reales")
    p.add_argument("--desde", default="2023-10-01")
    p.add_argument("--sims", type=int, default=2000, help="simulaciones por jugador en la validación")
    p.set_defaults(f=cmd_puntos_validar)
    p = pu.add_parser("proyectar", help="distribución de puntos de los partidos de una fecha")
    p.add_argument("--fecha")
    p.set_defaults(f=cmd_puntos_proyectar)

    bt = grupos.add_parser("backtest", help="fase 4: backtest con cuotas reales").add_subparsers(dest="cmd", required=True)
    bt.add_parser("puntos", help="mercado de puntos (necesita `puntos validar`)").set_defaults(f=cmd_backtest_puntos)
    bt.add_parser("mercados", help="todos los mercados (necesita `mercados validar`)").set_defaults(
        f=cmd_backtest_mercados)

    p = grupos.add_parser("diario", help="flujo completo del día: datos, proyección, picks y banca")
    p.add_argument("--fecha")
    p.add_argument("--sin-actualizar", action="store_true", help="no descarga datos ni cuotas")
    p.add_argument("--sin-cuotas", action="store_true", help="actualiza datos pero no captura cuotas")
    p.set_defaults(f=cmd_diario)
    ap_ = grupos.add_parser("apuestas", help="registro de apuestas").add_subparsers(dest="cmd", required=True)
    p = ap_.add_parser("confirmar", help="marcar como hecha una apuesta sugerida")
    p.add_argument("id", type=int)
    p.add_argument("--cuota", type=float)
    p.add_argument("--monto", type=float)
    p.set_defaults(f=cmd_apuestas)
    p = ap_.add_parser("descartar")
    p.add_argument("id", type=int)
    p.set_defaults(f=cmd_apuestas)
    ap_.add_parser("liquidar", help="liquidar con los resultados reales").set_defaults(f=cmd_apuestas)
    ap_.add_parser("ver", help="últimas apuestas y rendimiento").set_defaults(f=cmd_apuestas)

    me_ = grupos.add_parser("mercados", help="fase 6: todos los mercados").add_subparsers(dest="cmd", required=True)
    p = me_.add_parser("validar", help="walk-forward de todos los mercados con líneas reales")
    p.add_argument("--desde", default="2025-10-01")
    p.add_argument("--sims", type=int, default=2000)
    p.set_defaults(f=cmd_mercados_validar)

    p = grupos.add_parser("props", help="las N mejores props del día (de la tabla de `diario`)")
    p.add_argument("--n", type=int, default=8)
    p.add_argument("--max-partido", type=int, default=2)
    p.add_argument("--fecha")
    p.set_defaults(f=cmd_props)
    p = grupos.add_parser("combinada", help="probabilidad conjunta de una combinada (simulaciones del día)")
    p.add_argument("--fecha")
    p.add_argument("--sel", action="append", required=True,
                   help='"jugador|mercado|línea|lado|cuota[|prob_justa][|periodo]"; repetir por selección')
    p.set_defaults(f=cmd_combinada)
    co = grupos.add_parser("comparar", help="duelos y máximo anotador").add_subparsers(dest="cmd", required=True)
    p = co.add_parser("duelo")
    p.add_argument("a")
    p.add_argument("b")
    p.add_argument("--mercado", default="pts")
    p.add_argument("--fecha")
    p.set_defaults(f=cmd_comparar)
    p = co.add_parser("maximo", help="máximo del partido (o de su equipo con --equipo) de un jugador dado")
    p.add_argument("jugador_de_partido")
    p.add_argument("--mercado", default="pts")
    p.add_argument("--equipo", action="store_true")
    p.add_argument("--fecha")
    p.set_defaults(f=cmd_comparar)

    args = ap.parse_args(argv)
    cfg = config.cargar(args.config)
    config.configurar_logs(cfg)
    args.f(cfg, args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
