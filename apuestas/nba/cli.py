"""Subcomandos de la NBA.

    python -m apuestas nba historial --desde 2025-10-21   # descarga el historial de ESPN (una vez)
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
from .analizador import (analizar, emparejar_props, guardar_analisis, guardar_picks, liquidar, mejores,
                         rendimiento)
from .backtest import backtest, resumen
from .db import NbaDB
from .espn import Espn
from .informe import escribir, etiqueta
from .modelo import NOMBRES, construir_contexto
from .recolector import descargar_dia, descargar_rango
from .sgo import SportsGameOdds, ventana_dia

log = logging.getLogger("apuestas")


def _hoy(cfg: Config) -> date:
    return datetime.now(ZoneInfo(cfg.zona_horaria)).date()


def _fecha(value: str | None, cfg: Config, offset: int = 0) -> date:
    return date.fromisoformat(value) if value else _hoy(cfg) + timedelta(days=offset)


def cmd_historial(args, cfg: Config, db: Database) -> int:
    nba = NbaDB(db.conn)
    hasta = _fecha(args.hasta, cfg, offset=-1)
    espn = Espn()
    n = descargar_rango(espn, nba, date.fromisoformat(args.desde), hasta)
    print(f"{n} partidos nuevos guardados ({espn.peticiones} consultas a ESPN).")
    return 0


def cmd_actualizar(args, cfg: Config, db: Database) -> int:
    nba = NbaDB(db.conn)
    fecha = _fecha(args.fecha, cfg, offset=-1)
    espn = Espn()
    n = descargar_dia(espn, nba, fecha.isoformat())
    liquidadas = liquidar(nba)
    print(f"{fecha}: {n['nuevos']} partidos terminados guardados; {liquidadas} props liquidadas.")
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
        n = descargar_dia(espn, nba, fecha, lesiones=True)
        print(f"{n['partidos']} partidos el {fecha}; {n['lesiones']} jugadores en el parte de lesiones.")
        eventos = SportsGameOdds(cfg.sgo_key).eventos(*ventana_dia(fecha, cfg.zona_horaria))
        ctx = construir_contexto(nba.conn, fecha)
        props, sin_emparejar = emparejar_props(nba, fecha, eventos, ctx)
        print(f"{len(eventos)} partidos con líneas en SportsGameOdds; {props} props emparejadas.")
    partidos, ctx = analizar(nba, fecha, cfg.nba_min_partidos, peso_mercado=cfg.nba_peso_mercado)
    picks = mejores(partidos, cfg.nba_prob_min)
    guardar_picks(nba, fecha, picks)
    guardar_analisis(nba, fecha, partidos)
    md, js = escribir(cfg.reportes_dir, fecha, ctx, partidos, picks, sin_emparejar)
    print(f"{sum(len(p.evaluaciones) for p in partidos)} props evaluadas; {len(picks)} con probabilidad "
          f">= {cfg.nba_prob_min * 100:.0f}%.")
    for p, e in picks[:args.top]:
        print(f"  {e.prob * 100:4.0f}%  {etiqueta(e):<55} esperado {e.mu:5.1f}  últ.10 {e.acierto_10[0]}/{e.acierto_10[1]}"
              f"  ({p.titulo})")
    print(f"Informe: {md}\nDatos: {js}\n")
    print(AVISO.replace("> ", "").replace("**", ""))
    return 0


def cmd_rendimiento(args, cfg: Config, db: Database) -> int:
    r = rendimiento(NbaDB(db.conn))
    if not r["total"]:
        print("Aún no hay props liquidadas. Ejecuta 'nba actualizar' después de los partidos.")
        return 0

    def linea(nombre, x):
        ben = "" if x["beneficio"] is None else f"  {x['beneficio']:+.2f} u en {x['con_cuota']} con cuota"
        return (f"  {nombre:<22} n={x['n']:<5} acierto {x['acierto'] * 100:5.1f}%  "
                f"prob. media {x['prob_media'] * 100:5.1f}%{ben}")

    print(linea("Total", r["total"]))
    print("Por tramo de probabilidad (si el acierto queda por debajo del tramo, el modelo es optimista):")
    for t in r["tramos"]:
        print(linea(t["tramo"], t))
    print("Por estadística:")
    for s in r["stats"]:
        print(linea(NOMBRES.get(s["stat"], s["stat"]), s))
    return 0


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
    h.add_argument("--desde", required=True, help="AAAA-MM-DD, p. ej. 2025-10-21 (temporada pasada completa)")
    h.add_argument("--hasta", help="AAAA-MM-DD (por defecto, ayer)")
    h.set_defaults(func=cmd_historial)

    a = s.add_parser("analizar", help="evalúa las props del día")
    a.add_argument("--fecha", help="AAAA-MM-DD (por defecto, hoy)")
    a.add_argument("--sin-descarga", action="store_true", help="usar solo lo que ya está en la base")
    a.add_argument("--top", type=int, default=15, help="cuántas props mostrar en pantalla")
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
