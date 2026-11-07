"""Subcomandos de la NHL.

    python -m apuestas nhl historial                      # ESPN: desde el último día guardado (o 2025-26 entera)
    python -m apuestas nhl analizar                       # props de hoy: picks, combinadas, bet builders, informe
    python -m apuestas nhl actualizar                     # resultados de ayer + liquidación
    python -m apuestas nhl rendimiento                    # ¿aciertan lo que prometen?
    python -m apuestas nhl backtest --desde 2025-11-01 --hasta 2026-04-16
    python -m apuestas nhl correlaciones                  # correlaciones entre jugadores del mismo partido
"""
from __future__ import annotations

import logging
import math
from collections import defaultdict
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from ..config import Config
from ..db import Database
from ..nba.sgo import clave_nombre, ventana_dia
from ..report import AVISO
from . import builder, combinadas, theodds, usuario
from .analizador import (analizar, candidatas_seguras, emparejar_props, guardar_analisis, guardar_picks, liquidar,
                         mejores, rendimiento)
from .backtest import ajustar_calibracion, backtest, picks_constantes, resumen
from .db import NhlDB
from .espn import Espn
from .informe import escribir, etiqueta
from .modelo import NOMBRES, construir_contexto
from .recolector import descargar_dia, descargar_rango

log = logging.getLogger("apuestas")
HISTORIAL_INICIO = date(2025, 10, 7)


def _hoy(cfg: Config) -> date:
    return datetime.now(ZoneInfo(cfg.zona_horaria)).date()


def _fecha(value: str | None, cfg: Config, offset: int = 0) -> date:
    return date.fromisoformat(value) if value else _hoy(cfg) + timedelta(days=offset)


def cmd_historial(args, cfg: Config, db: Database) -> int:
    nhl = NhlDB(db.conn)
    hasta = _fecha(args.hasta, cfg, offset=-1)
    if args.desde:
        desde = date.fromisoformat(args.desde)
    else:
        ultimo = nhl.conn.execute("SELECT MAX(fecha) FROM nhl_games WHERE box_ok = 1").fetchone()[0]
        desde = date.fromisoformat(ultimo) - timedelta(days=1) if ultimo else HISTORIAL_INICIO
    espn = Espn()
    n = descargar_rango(espn, nhl, desde, hasta)
    print(f"{n} partidos nuevos de la NHL guardados ({espn.peticiones} consultas a ESPN).")
    return 0


def cmd_actualizar(args, cfg: Config, db: Database) -> int:
    nhl = NhlDB(db.conn)
    fecha = _fecha(args.fecha, cfg, offset=-1)
    n = descargar_dia(Espn(), nhl, fecha.isoformat())
    print(f"{fecha}: {n['nuevos']} partidos guardados; {liquidar(nhl)} props y {combinadas.liquidar(nhl)} "
          "combinadas liquidadas.")
    return 0


def _parejos(nhl: NhlDB, fecha: str) -> dict:
    out = {}
    for r in nhl.conn.execute(
            """SELECT h.name, a.name, g.margen_esperado FROM nhl_games g JOIN nhl_teams h ON h.id = g.home_id
               JOIN nhl_teams a ON a.id = g.away_id WHERE g.fecha = ?""", (fecha,)):
        out[(clave_nombre(r[0]), clave_nombre(r[1]))] = abs(r[2]) if r[2] is not None else 99.0
    return out


def cmd_analizar(args, cfg: Config, db: Database) -> int:
    nhl = NhlDB(db.conn)
    fecha = _fecha(args.fecha, cfg).isoformat()
    avisos: list[str] = []
    if not args.sin_descarga:
        espn = Espn()
        ayer = (date.fromisoformat(fecha) - timedelta(days=1)).isoformat()
        descargar_dia(espn, nhl, ayer)
        liquidar(nhl)
        print(f"{usuario.registrar(nhl)} apuestas tuyas de la NHL registradas para seguirlas.")
        combinadas.liquidar(nhl)
        n = descargar_dia(espn, nhl, fecha, lesiones=True)
        print(f"{n['partidos']} partidos el {fecha}; {n['lesiones']} jugadores en el parte de lesiones.")
        if theodds.activada() and cfg.odds_api_key:
            try:
                api = theodds.TheOddsApiNhl(cfg.odds_api_key)
                eventos = api.eventos(*ventana_dia(fecha, cfg.zona_horaria), prioridad=_parejos(nhl, fecha))
                if eventos:
                    ctx = construir_contexto(nhl.conn, fecha)
                    props, sin = emparejar_props(nhl, fecha, eventos, ctx)
                    avisos.append(f"Líneas de The Odds API: {len(eventos)} partidos, {props} props"
                                  + (f" (solo los más parejos para no quitarle créditos a la NBA; {api.restantes} "
                                     "créditos restantes)" if api.recortados else ""))
                    if sin:
                        avisos.append("Sin emparejar con ESPN: " + ", ".join(sin[:20]))
            except Exception as exc:
                log.warning("The Odds API (NHL) no respondió (%s)", exc)
                avisos.append(f"Sin líneas de la casa: The Odds API no respondió ({str(exc)[:100]})")
        else:
            avisos.append("Sin líneas de la casa (ODDS_API_NHL no está activada, para no gastar los créditos de la "
                          "NBA): picks a líneas estimadas y cuotas estimadas. Mándame las líneas y cuotas de Betano "
                          "y evalúo esas exactas.")
    partidos, ctx = analizar(nhl, fecha, cfg.nhl_min_partidos, peso_mercado=cfg.nhl_peso_mercado,
                             prob_segura=cfg.nhl_prob_segura)
    picks = mejores(partidos, cfg.nhl_prob_min)
    guardar_picks(nhl, fecha, [(p, e) for p, e in picks if e.titular and not e.alertas], partidos)
    guardar_analisis(nhl, fecha, partidos)
    candidatas = candidatas_seguras(partidos, cfg.nhl_cuota_min)
    builders = builder.del_dia(ctx, partidos)
    combis = combinadas.del_dia(partidos, candidatas) + combinadas.de_builders(builders)
    combinadas.guardar(nhl, fecha, combis)
    ayer_fecha = (date.fromisoformat(fecha) - timedelta(days=1)).isoformat()
    md, js = escribir(cfg.reportes_dir, fecha, ctx, partidos, picks, avisos, candidatas, combis, builders,
                      (ayer_fecha, combinadas.detalle(nhl, ayer_fecha)), combinadas.resumen(nhl))
    print(f"{sum(len(p.evaluaciones) for p in partidos)} props evaluadas; {len(candidatas)} de jugadores constantes.")
    for p, e in candidatas[:args.top]:
        print(f"  {e.prob * 100:4.0f}%  {etiqueta(e):<50} esperado {e.mu:5.1f}  últ.10 {e.acierto_10[0]}/"
              f"{e.acierto_10[1]}  ({p.titulo}){' [línea estimada]' if e.estimada else ''}")
    for c in combis:
        print(f"{combinadas.nombre_tipo(c.tipo)}: {c.prob * 100:.0f}%"
              + (f", cuota {'~' if c.estimada else ''}{c.cuota:.2f}" if c.cuota else f", justa {1 / c.prob:.2f}")
              + " — " + "; ".join(combinadas.etiqueta_pata(x) for x in c.patas))
    print(f"Informe: {md}\nDatos: {js}\n")
    print(AVISO.replace("> ", "").replace("**", ""))
    return 0


def cmd_rendimiento(args, cfg: Config, db: Database) -> int:
    nhl = NhlDB(db.conn)
    r = rendimiento(nhl)
    if not r["total"]:
        print("Aún no hay props de la NHL liquidadas.")
    else:
        def linea(nombre, x):
            ben = "" if x["beneficio"] is None else f"  {x['beneficio']:+.2f} u en {x['con_cuota']} con cuota"
            return (f"  {nombre:<22} n={x['n']:<5} acierto {x['acierto'] * 100:5.1f}%  "
                    f"prob. media {x['prob_media'] * 100:5.1f}%{ben}")
        print(linea("Total", r["total"]))
        for t in r["tipos"]:
            print(linea(t["tipo"], t))
        for t in r["tramos"]:
            print(linea(t["tramo"], t))
        for s in r["stats"]:
            print(linea(NOMBRES.get(s["stat"], s["stat"]), s))
    for c in combinadas.resumen(nhl):
        print(f"  {combinadas.nombre_tipo(c['tipo']):<30} n={c['n']:<4} ganadas {c['ganadas']}  "
              f"prob. media {c['prob_media'] * 100:5.1f}%")
    return 0


def _linea_bt(nombre, x):
    return (f"  {nombre:<22} n={x['n']:<6} acierto {x['acierto'] * 100:5.1f}%  prob. media "
            f"{x['prob_media'] * 100:5.1f}%  Brier {x['brier']:.4f}  log-loss {x['logloss']:.4f}")


def cmd_backtest(args, cfg: Config, db: Database) -> int:
    filas = backtest(db.conn, date.fromisoformat(args.desde), date.fromisoformat(args.hasta),
                     sin_calibrar=args.sin_calibrar)
    if not filas:
        print("Sin partidos en ese rango (descárgalos antes con 'nhl historial').")
        return 0
    r = resumen(filas)
    print("Líneas de referencia: tiros, bloqueados, hits y paradas, la mediana de sus últimos 10 (.5); puntos, goles "
          "y asistencias, 0.5.")
    print(_linea_bt("Total", r["total"]))
    print("Por tramo de probabilidad:")
    for t in r["tramos"]:
        print(_linea_bt(t["tramo"], t))
    print("Por estadística:")
    for s, x in sorted(r["stats"].items()):
        print(_linea_bt(NOMBRES[s], x))
    sel = picks_constantes(filas)
    if sel:
        rs = resumen(sel)
        print("Lo que propondría el sistema (jugadores constantes, 62 %+, 7+ de 10, 60 %+ de la temporada):")
        print(_linea_bt("Total", rs["total"]))
        for t in rs["tramos"]:
            print(_linea_bt(t["tramo"], t))
        for s, x in sorted(rs["stats"].items()):
            for lado in ("más", "menos"):
                g = [f for f in sel if f["stat"] == s and f["lado"] == lado]
                if len(g) >= 20:
                    print(_linea_bt(f"{NOMBRES[s]} ({lado})", resumen(g)["total"]))
    if args.sin_calibrar:
        print("Calibración por estadística que minimiza el log-loss:", ajustar_calibracion(filas))
    return 0


def cmd_correlaciones(args, cfg: Config, db: Database) -> int:
    """Correlación de los desvíos (real − media de sus últimos 10) entre jugadores del mismo partido."""
    filas = db.conn.execute(
        """SELECT pg.game_id, pg.player_id, pg.team_id, pg.toi, pg.sog, pg.g, pg.a, pg.bs, g.fecha
           FROM nhl_player_games pg JOIN nhl_games g ON g.id = pg.game_id
           WHERE g.season_type = 2 AND g.fecha >= ? ORDER BY g.fecha""", (args.desde,)).fetchall()
    hist: dict[str, list] = defaultdict(list)
    desvios: dict[str, list] = defaultdict(list)
    for r in filas:
        h = hist[r["player_id"]]
        vals = {"shots": r["sog"], "points": r["g"] + r["a"], "assists": r["a"], "blocked": r["bs"]}
        if len(h) >= 10 and r["toi"] >= 14:
            ult = h[-10:]
            d = {s: vals[s] - sum(x[s] for x in ult) / 10 for s in vals}
            desvios[r["game_id"]].append((r["team_id"], d))
        h.append(vals)
    for s1, s2 in (("shots", "shots"), ("points", "points"), ("assists", "assists"), ("blocked", "blocked"),
                   ("shots", "points"), ("points", "blocked"), ("shots", "blocked")):
        for mismo in (True, False):
            xs, ys = [], []
            for jug in desvios.values():
                for i, (t1, d1) in enumerate(jug):
                    for t2, d2 in jug[i + 1:]:
                        if (t1 == t2) == mismo:
                            xs.append(d1[s1])
                            ys.append(d2[s2])
                            if s1 != s2:
                                xs.append(d2[s1])
                                ys.append(d1[s2])
            n = len(xs)
            mx, my = sum(xs) / n, sum(ys) / n
            cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / n
            sx = math.sqrt(sum((x - mx) ** 2 for x in xs) / n)
            sy = math.sqrt(sum((y - my) ** 2 for y in ys) / n)
            print(f"  {s1:<8} ↔ {s2:<8} {'compañeros' if mismo else 'rivales':<11} r = {cov / sx / sy:+.3f}  (n = {n})")
    return 0


def registrar(sub) -> None:
    nhl = sub.add_parser("nhl", help="props de jugadores de la NHL")
    s = nhl.add_subparsers(dest="nhl_cmd", required=True)

    h = s.add_parser("historial", help="descarga partidos jugados de ESPN a la base")
    h.add_argument("--desde", help="AAAA-MM-DD (por defecto, desde el último día guardado o el 2025-10-07)")
    h.add_argument("--hasta", help="AAAA-MM-DD (por defecto, ayer)")
    h.set_defaults(func=cmd_historial)

    a = s.add_parser("analizar", help="evalúa las props del día")
    a.add_argument("--fecha", help="AAAA-MM-DD (por defecto, hoy)")
    a.add_argument("--sin-descarga", action="store_true", help="usar solo lo que ya está en la base")
    a.add_argument("--top", type=int, default=15)
    a.set_defaults(func=cmd_analizar)

    u = s.add_parser("actualizar", help="guarda los resultados de un día y liquida")
    u.add_argument("--fecha", help="AAAA-MM-DD (por defecto, ayer)")
    u.set_defaults(func=cmd_actualizar)

    r = s.add_parser("rendimiento", help="acierto real frente a la probabilidad estimada")
    r.set_defaults(func=cmd_rendimiento)

    b = s.add_parser("backtest", help="calibración del modelo sobre partidos ya jugados")
    b.add_argument("--desde", required=True)
    b.add_argument("--hasta", required=True)
    b.add_argument("--sin-calibrar", action="store_true", help="sin la calibración, y propone la que mejor ajusta")
    b.set_defaults(func=cmd_backtest)

    c = s.add_parser("correlaciones", help="correlaciones entre jugadores del mismo partido (bet builders)")
    c.add_argument("--desde", default="2025-10-07")
    c.set_defaults(func=cmd_correlaciones)
