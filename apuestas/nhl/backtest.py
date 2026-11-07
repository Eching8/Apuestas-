"""Backtest de calibración de la NHL: ¿cuando el modelo dice 70 %, pasa el 70 % de las veces?

Para cada día se reconstruye el contexto solo con partidos anteriores y se evalúa a cada jugador que jugó contra una
línea de referencia: tiros a puerta, bloqueados, hits y paradas, la mediana de sus últimos 10 redondeada a .5; puntos,
goles y asistencias, 0.5 (la línea que la casa pone a casi todos). El portero rival es el que salió de titular (en
el día real se usa el probable de ESPN, que casi siempre acierta). No hay partes de lesiones históricos: solo entra
quien jugó, sin ajuste por bajas. No hay cuotas históricas: es la probabilidad del modelo, sin mezclar con la casa.
"""
from __future__ import annotations

import math
from datetime import date, timedelta
from statistics import median

from . import modelo
from .modelo import (construir_contexto, evaluar, preparar_jugador, preparar_portero, valor)

TRAMOS = ((0.0, 0.62), (0.62, 0.65), (0.65, 0.70), (0.70, 0.75), (0.75, 0.80), (0.80, 0.85), (0.85, 1.01))
STATS_BACKTEST = ("shots", "points", "assists", "goals", "blocked", "hits")


def linea_referencia(partidos: list[dict], stat: str) -> float:
    if stat in ("points", "goals", "assists"):
        return 0.5
    return int(median(valor(p, stat) for p in partidos[:10])) + 0.5


def backtest(conn, desde: date, hasta: date, min_partidos: int = 10, min_minutos: float = 10.0,
             stats=STATS_BACKTEST, porteros: bool = True, sin_calibrar: bool = False) -> list[dict]:
    guardada = dict(modelo.CALIBRACION_STAT), modelo.CALIBRACION
    if sin_calibrar:
        modelo.CALIBRACION_STAT.clear()
        modelo.CALIBRACION = 1.0
    try:
        return _backtest(conn, desde, hasta, min_partidos, min_minutos, stats, porteros)
    finally:
        modelo.CALIBRACION_STAT.clear()
        modelo.CALIBRACION_STAT.update(guardada[0])
        modelo.CALIBRACION = guardada[1]


def _backtest(conn, desde, hasta, min_partidos, min_minutos, stats, porteros) -> list[dict]:
    filas, dia = [], desde
    while dia <= hasta:
        fecha = dia.isoformat()
        jugados = conn.execute(
            """SELECT pg.* FROM nhl_player_games pg JOIN nhl_games g ON g.id = pg.game_id
               WHERE g.fecha = ? AND g.season_type IN (2, 3)""", (fecha,)).fetchall()
        if jugados:
            ctx = construir_contexto(conn, fecha)
            titulares = conn.execute(
                """SELECT gg.* FROM nhl_goalie_games gg JOIN nhl_games g ON g.id = gg.game_id
                   WHERE g.fecha = ? AND gg.starter = 1""", (fecha,)).fetchall()
            ctx.portero_hoy = {r["team_id"]: r["player_id"] for r in titulares}
            for r in jugados:
                j = preparar_jugador(ctx, r["player_id"], r["name"], r["team_id"], r["opp_id"])
                if j is None or j.n < min_partidos or j.minutos < min_minutos:
                    continue
                al = modelo.alertas(ctx, j, "shots")
                for stat in stats:
                    line = linea_referencia(j.partidos, stat)
                    e = evaluar(ctx, j, stat, line, detalle=False)
                    fila = _fila(fecha, stat, line, e, valor(dict(r), stat), j, al, ctx)
                    fila["toi_esperado"], fila["toi"] = j.minutos, r["toi"]
                    filas.append(fila)
            if porteros:
                for r in titulares:
                    if r["toi"] < 40:
                        continue
                    j = preparar_portero(ctx, r["player_id"], r["name"], r["team_id"], r["opp_id"])
                    if j is None or j.n < 8:
                        continue
                    line = linea_referencia(j.partidos, "saves")
                    e = evaluar(ctx, j, "saves", line, detalle=False)
                    filas.append(_fila(fecha, "saves", line, e, r["sv"], j, [], ctx))
        dia += timedelta(days=1)
    return filas


def _fila(fecha, stat, line, e, real, j, al, ctx) -> dict:
    temp = e.acierto_temporada
    return {"fecha": fecha, "stat": stat, "line": line, "lado": e.lado, "prob": e.prob, "mu": e.mu, "real": real,
            "grupo": j.grupo, "acierto": int((real > line) if e.lado == "más" else (real < line)),
            "aciertos_10": e.acierto_10[0], "n_10": e.acierto_10[1],
            "temp": temp[0] / temp[1] if temp[1] else None, "n_temp": temp[1],
            "constante": not al and e.titular, "factores": e.factores, "b2b": j.b2b, "rival_b2b": j.rival_b2b,
            "margen": ctx.margen.get(j.team_id)}


def resumen(filas: list[dict], clave: str = "prob") -> dict:
    def bloque(g):
        n = len(g)
        ll = -sum(math.log(max(1e-6, f[clave] if f["acierto"] else 1 - f[clave])) for f in g) / n
        return {"n": n, "acierto": sum(f["acierto"] for f in g) / n, "prob_media": sum(f[clave] for f in g) / n,
                "brier": sum((f[clave] - f["acierto"]) ** 2 for f in g) / n, "logloss": ll}

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


def ajustar_calibracion(filas: list[dict]) -> dict[str, float]:
    """Factor k por estadística (prob = 0.5 + (p − 0.5) · k) que minimiza el log-loss, con filas sin calibrar."""
    out = {}
    por_stat: dict[str, list] = {}
    for f in filas:
        por_stat.setdefault(f["stat"], []).append(f)
    for s, g in por_stat.items():
        mejor = None
        for k100 in range(50, 131):
            k = k100 / 100
            ll = 0.0
            for f in g:
                p = min(0.999, max(0.001, 0.5 + (f["prob"] - 0.5) * k))
                ll -= math.log(p if f["acierto"] else 1 - p)
            if mejor is None or ll < mejor[0]:
                mejor = (ll, k)
        out[s] = mejor[1]
    return out


def picks_constantes(filas: list[dict], prob_min: float = 0.62) -> list[dict]:
    """Lo que el sistema propondría: jugador constante (papel principal, sin alertas), 7+ de 10, 60 %+ esta
    temporada y prob 62 %+; los "menos" de tiros, puntos, goles y asistencias, 75 %+ y 8+ de 10."""
    out = []
    for f in filas:
        if not f["constante"] or f["prob"] < prob_min or f["n_10"] < 8 or f["aciertos_10"] < 7:
            continue
        if f["n_temp"] >= 2 and (f["temp"] or 0) < 0.6:
            continue
        if f["lado"] == "menos" and f["stat"] in ("shots", "points", "goals", "assists") and (
                f["prob"] < 0.75 or f["aciertos_10"] < 8):
            continue
        out.append(f)
    return out
