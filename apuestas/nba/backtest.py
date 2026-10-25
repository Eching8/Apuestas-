"""Backtest de calibración: ¿cuando el modelo dice 70 %, pasa el 70 % de las veces?

Para cada día del rango se reconstruye el contexto solo con partidos anteriores y se evalúa a cada
jugador que jugó contra una línea de referencia: la mediana de sus últimos 10 partidos redondeada
a .5 (las casas suelen poner la línea cerca de ahí). No hay partes de lesiones históricos, así que
el backtest no usa el ajuste por bajas y solo incluye a quien jugó (como si se supiera que juega).
"""
from __future__ import annotations

from datetime import date, timedelta
from statistics import median

from .analizador import TRAMOS
from .modelo import construir_contexto, evaluar, preparar_jugador, valor

STATS_BACKTEST = ("points", "rebounds", "assists", "threes", "pra", "pr", "pa", "ra", "steals", "blocks")


def linea_referencia(partidos: list[dict], stat: str) -> float:
    return int(median(valor(p, stat) for p in partidos[:10])) + 0.5


def backtest(conn, desde: date, hasta: date, min_partidos: int = 10, min_minutos: float = 20.0,
             stats=STATS_BACKTEST) -> list[dict]:
    filas, dia = [], desde
    while dia <= hasta:
        fecha = dia.isoformat()
        jugados = conn.execute(
            """SELECT pg.* FROM nba_player_games pg JOIN nba_games g ON g.id = pg.game_id
               WHERE g.fecha = ? AND g.season_type IN (2, 3)""", (fecha,)).fetchall()
        if jugados:
            ctx = construir_contexto(conn, fecha)
            for r in jugados:
                j = preparar_jugador(ctx, r["player_id"], r["name"], r["team_id"], r["opp_id"])
                if j is None or j.n < min_partidos or j.minutos < min_minutos:
                    continue
                for stat in stats:
                    line = linea_referencia(j.partidos, stat)
                    e = evaluar(ctx, j, stat, line, detalle=False)
                    real = valor(dict(r), stat)
                    filas.append({"fecha": fecha, "stat": stat, "prob": e.prob, "prob_modelo": e.prob_modelo,
                                  "acierto": int((real > line) if e.lado == "más" else (real < line))})
        dia += timedelta(days=1)
    return filas


def resumen(filas: list[dict], clave: str = "prob") -> dict:
    def bloque(g):
        n = len(g)
        return {"n": n, "acierto": sum(f["acierto"] for f in g) / n, "prob_media": sum(f[clave] for f in g) / n,
                "brier": sum((f[clave] - f["acierto"]) ** 2 for f in g) / n}

    tramos = []
    for lo, hi in TRAMOS:
        g = [f for f in filas if lo <= f[clave] < hi]
        if g:
            tramos.append({"tramo": f"{lo * 100:.0f}-{min(hi, 1) * 100:.0f}%", **bloque(g)})
    stats = {}
    for f in filas:
        stats.setdefault(f["stat"], []).append(f)
    return {"total": bloque(filas) if filas else None, "tramos": tramos,
            "stats": {s: bloque(g) for s, g in stats.items()}}
