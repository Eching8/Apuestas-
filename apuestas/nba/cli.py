"""Subcomandos de la NBA.

    python -m apuestas nba historial --desde 2025-10-21   # descarga el historial de ESPN (una vez)
    python -m apuestas nba enfrentamientos               # stats.nba.com: quién defendió a quién (desde casa)
    python -m apuestas nba analizar                      # props de hoy
    python -m apuestas nba actualizar                    # resultados de ayer + liquidación
    python -m apuestas nba rendimiento                   # calibración: ¿aciertan lo que dicen?
    python -m apuestas nba backtest --desde 2026-03-01 --hasta 2026-03-31
"""
from __future__ import annotations

import argparse
import logging
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from ..config import Config
from ..db import Database
from ..report import AVISO
from .analizador import (analizar, candidatas_seguras, combinada_segura, emparejar_props, guardar_analisis,
                         guardar_picks, liquidar, mejores,
                         rendimiento)
from . import combinadas
from .backtest import backtest, resumen
from .db import NbaDB
from .enfrentamientos import descargar_avanzadas, descargar_temporada
from .espn import Espn
from .informe import escribir, etiqueta
from .modelo import NOMBRES, construir_contexto
from .nbastats import TIPOS, NbaStats, temporada_nba
from .recolector import descargar_alturas, descargar_dia, descargar_rango
from .sgo import SportsGameOdds, ventana_dia

log = logging.getLogger("apuestas")
HISTORIAL_INICIO = date(2025, 10, 21)


def _hoy(cfg: Config) -> date:
    return datetime.now(ZoneInfo(cfg.zona_horaria)).date()


def _fecha(value: str | None, cfg: Config, offset: int = 0) -> date:
    return date.fromisoformat(value) if value else _hoy(cfg) + timedelta(days=offset)


def cmd_historial(args, cfg: Config, db: Database) -> int:
    nba = NbaDB(db.conn)
    hasta = _fecha(args.hasta, cfg, offset=-1)
    if args.desde:
        desde = date.fromisoformat(args.desde)
    else:
        # Sin --desde: continúa desde el último día guardado (o la temporada 2025-26 si la base está vacía).
        ultimo = nba.conn.execute("SELECT MAX(fecha) FROM nba_games WHERE box_ok = 1").fetchone()[0]
        desde = date.fromisoformat(ultimo) - timedelta(days=1) if ultimo else HISTORIAL_INICIO
    espn = Espn()
    n = descargar_rango(espn, nba, desde, hasta)
    print(f"{n} partidos nuevos guardados ({espn.peticiones} consultas a ESPN).")
    return 0


def cmd_enfrentamientos(args, cfg: Config, db: Database) -> int:
    nba = NbaDB(db.conn)
    temporadas = [args.temporada] if args.temporada else [
        r[0] for r in nba.conn.execute("SELECT DISTINCT season FROM nba_games WHERE box_ok = 1 ORDER BY season")]
    if not temporadas:
        print("La base no tiene partidos de ESPN: ejecuta antes 'nba historial'.")
        return 2
    ns = NbaStats()
    for season in temporadas:
        for tipo in args.tipos:
            n = descargar_temporada(ns, nba, season, tipo, maximo=args.maximo)
            print(f"Temporada {temporada_nba(season)} ({TIPOS[tipo]}): {n['partidos']} partidos en stats.nba.com, "
                  f"{n['nuevos']} nuevos con enfrentamientos, {n['sin_espn']} sin partido de ESPN, "
                  f"{n['sin_datos']} sin datos, {n['jugadores_sin_emparejar']} filas sin emparejar.")
            if not args.sin_avanzadas:
                print(f"  Estadísticas avanzadas: {descargar_avanzadas(ns, nba, season, tipo)} jugadores.")
    print(f"{ns.peticiones} consultas a stats.nba.com.")
    return 0


def cmd_actualizar(args, cfg: Config, db: Database) -> int:
    nba = NbaDB(db.conn)
    fecha = _fecha(args.fecha, cfg, offset=-1)
    espn = Espn()
    n = descargar_dia(espn, nba, fecha.isoformat())
    liquidadas = liquidar(nba)
    combis = combinadas.liquidar(nba)
    print(f"{fecha}: {n['nuevos']} partidos terminados guardados; {liquidadas} props y {combis} combinadas "
          "liquidadas.")
    return 0


def cmd_analizar(args, cfg: Config, db: Database) -> int:
    nba = NbaDB(db.conn)
    fecha = _fecha(args.fecha, cfg).isoformat()
    sin_emparejar: list[str] = []
    if not args.sin_descarga:
        espn = Espn()
        ayer = (date.fromisoformat(fecha) - timedelta(days=1)).isoformat()
        descargar_dia(espn, nba, ayer)
        liquidar(nba)
        combinadas.liquidar(nba)
        n = descargar_dia(espn, nba, fecha, lesiones=True)
        print(f"{descargar_alturas(espn, nba)} jugadores con estatura (plantillas de ESPN).")
        print(f"{n['partidos']} partidos el {fecha}; {n['lesiones']} jugadores en el parte de lesiones.")
        eventos = SportsGameOdds(cfg.sgo_key).eventos(*ventana_dia(fecha, cfg.zona_horaria))
        ctx = construir_contexto(nba.conn, fecha)
        props, sin_emparejar = emparejar_props(nba, fecha, eventos, ctx)
        print(f"{len(eventos)} partidos con líneas en SportsGameOdds; {props} props emparejadas.")
    partidos, ctx = analizar(nba, fecha, cfg.nba_min_partidos, peso_mercado=cfg.nba_peso_mercado,
                             prob_segura=cfg.nba_prob_segura)
    picks = mejores(partidos, cfg.nba_prob_min)
    guardar_picks(nba, fecha, picks, partidos)
    guardar_analisis(nba, fecha, partidos)
    candidatas = candidatas_seguras(partidos, cfg.nba_cuota_min)
    combis = combinadas.del_dia(partidos, candidatas)
    combinadas.guardar(nba, fecha, combis)
    md, js = escribir(cfg.reportes_dir, fecha, ctx, partidos, picks, sin_emparejar, args.por_partido, candidatas,
                      combis, combinadas.listo(nba))
    print(f"{sum(len(p.evaluaciones) for p in partidos)} props evaluadas; {len(picks)} con probabilidad "
          f">= {cfg.nba_prob_min * 100:.0f}%.")
    for p, e in picks[:args.top]:
        print(f"  {e.prob * 100:4.0f}%  {etiqueta(e):<55} esperado {e.mu:5.1f}  últ.10 {e.acierto_10[0]}/{e.acierto_10[1]}"
              f"  ({p.titulo})")
    combi = combinada_segura(candidatas)
    if combi:
        prob = cuota = 1.0
        print("Combinada segura del día (la más probable de cada partido, jugadores constantes):")
        for p, e in combi:
            prob *= e.prob
            cuota *= e.odd
            print(f"  {e.prob * 100:4.0f}%  {etiqueta(e):<55} cuota {e.odd:.2f}  últ.10 "
                  f"{e.acierto_10[0]}/{e.acierto_10[1]}  ({p.titulo})")
        print(f"  Todas: {prob * 100:.0f}% de probabilidad, cuota {cuota:.2f}")
    seguras = sorted(((p, s) for p in partidos for s in p.seguras), key=lambda x: -x[1].prob)
    if seguras:
        print(f"{len(seguras)} picks seguros de titulares estables (línea baja al {cfg.nba_prob_segura * 100:.0f}%+):")
        for p, s in seguras[:args.top]:
            print(f"  {s.prob * 100:4.0f}%  {s.nombre}: más de {s.line:g} {NOMBRES[s.stat]:<14} "
                  f"cuota mínima {s.cuota_minima:.2f}  ({p.titulo})")
    print(f"Informe: {md}\nDatos: {js}\n")
    print(AVISO.replace("> ", "").replace("**", ""))
    return 0


def cmd_rendimiento(args, cfg: Config, db: Database) -> int:
    nba = NbaDB(db.conn)
    r = rendimiento(nba)
    imprimir_listo(nba)
    if not r["total"]:
        print("Aún no hay props liquidadas. Ejecuta 'nba actualizar' después de los partidos.")
        return 0

    def linea(nombre, x):
        ben = "" if x["beneficio"] is None else f"  {x['beneficio']:+.2f} u en {x['con_cuota']} con cuota"
        return (f"  {nombre:<22} n={x['n']:<5} acierto {x['acierto'] * 100:5.1f}%  "
                f"prob. media {x['prob_media'] * 100:5.1f}%{ben}")

    print(linea("Total", r["total"]))
    for t in r["tipos"]:
        print(linea({"prop": "Props (línea normal)", "segura": "Seguras (titulares)"}.get(t["tipo"], t["tipo"]), t))
    print("Por tramo de probabilidad (si el acierto queda por debajo del tramo, el modelo es optimista):")
    for t in r["tramos"]:
        print(linea(t["tramo"], t))
    print("Por estadística:")
    for s in r["stats"]:
        print(linea(NOMBRES.get(s["stat"], s["stat"]), s))
    combis = combinadas.resumen(nba)
    if combis:
        print("Combinadas (de prueba):")
        for c in combis:
            ben = "" if c["beneficio"] is None else f"  {c['beneficio']:+.2f} u en {c['con_cuota']} con cuota"
            print(f"  {c['tipo']:<22} n={c['n']:<5} ganadas {c['ganadas']} ({c['ganadas'] / c['n'] * 100:.0f}%)  "
                  f"prob. media {c['prob_media'] * 100:5.1f}%{ben}")
    return 0


def imprimir_listo(nba: NbaDB) -> None:
    criterios = combinadas.listo(nba)
    cumplidos = sum(ok for _, ok, _ in criterios)
    estado = "LISTO para dinero real" if cumplidos == len(criterios) else "en calibración: picks de prueba"
    print(f"¿Listo para apostar dinero real? {estado} ({cumplidos}/{len(criterios)} criterios)")
    for nombre, ok, detalle in criterios:
        print(f"  [{'x' if ok else ' '}] {nombre}: {detalle}")
    print()


def cmd_backtest(args, cfg: Config, db: Database) -> int:
    filas = backtest(db.conn, date.fromisoformat(args.desde), date.fromisoformat(args.hasta))
    if not filas:
        print("Sin partidos en ese rango (descárgalos antes con 'nba historial').")
        return 0
    r = resumen(filas)

    def linea(nombre, x):
        return (f"  {nombre:<22} n={x['n']:<6} acierto {x['acierto'] * 100:5.1f}%  "
                f"prob. media {x['prob_media'] * 100:5.1f}%  Brier {x['brier']:.3f}")

    print("Línea de referencia: mediana de los últimos 10 partidos del jugador (.5).")
    print(linea("Total", r["total"]))
    print("Por tramo de probabilidad:")
    for t in r["tramos"]:
        print(linea(t["tramo"], t))
    print("Por estadística:")
    for s, x in sorted(r["stats"].items(), key=lambda kv: kv[1]["brier"]):
        print(linea(NOMBRES[s], x))
    return 0


def registrar(sub) -> None:
    nba = sub.add_parser("nba", help="props de jugadores de la NBA")
    s = nba.add_subparsers(dest="nba_cmd", required=True)

    h = s.add_parser("historial", help="descarga partidos jugados de ESPN a la base")
    h.add_argument("--desde", help="AAAA-MM-DD, p. ej. 2025-10-21 (por defecto, desde el último día guardado)")
    h.add_argument("--hasta", help="AAAA-MM-DD (por defecto, ayer)")
    h.set_defaults(func=cmd_historial)

    e = s.add_parser("enfrentamientos",
                     help="descarga de stats.nba.com quién defendió a quién (solo desde una conexión de casa)")
    e.add_argument("--temporada", type=int, help="año de ESPN: 2026 = 2025-26 (por defecto, las de la base)")
    e.add_argument("--tipos", type=int, nargs="+", default=[2, 3], help="2 = temporada regular, 3 = playoffs")
    e.add_argument("--maximo", type=int, help="máximo de partidos nuevos por temporada (para probar)")
    e.add_argument("--sin-avanzadas", action="store_true", help="no descargar uso, %% de rebotes, etc.")
    e.set_defaults(func=cmd_enfrentamientos)

    a = s.add_parser("analizar", help="evalúa las props del día")
    a.add_argument("--fecha", help="AAAA-MM-DD (por defecto, hoy)")
    a.add_argument("--sin-descarga", action="store_true", help="usar solo lo que ya está en la base")
    a.add_argument("--top", type=int, default=15, help="cuántas props mostrar en pantalla")
    a.add_argument("--por-partido", type=int, default=8, help="props por partido en el informe")
    a.set_defaults(func=cmd_analizar)

    u = s.add_parser("actualizar", help="guarda los resultados de un día y liquida las props")
    u.add_argument("--fecha", help="AAAA-MM-DD (por defecto, ayer)")
    u.set_defaults(func=cmd_actualizar)

    b = s.add_parser("backtest", help="calibración del modelo sobre partidos ya jugados")
    b.add_argument("--desde", required=True)
    b.add_argument("--hasta", required=True)
    b.set_defaults(func=cmd_backtest)

    r = s.add_parser("rendimiento", help="acierto real frente a la probabilidad estimada")
    r.set_defaults(func=cmd_rendimiento)
