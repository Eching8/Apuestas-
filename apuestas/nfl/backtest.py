"""Backtest: el modelo predice cada partido ya jugado usando solo los datos anteriores a ese día.

Como en las apuestas reales (un jugador que no juega anula la apuesta), solo se evalúan los jugadores que
jugaron, y los que no jugaron se tratan como bajas conocidas antes del partido. Líneas del partido: las de
cierre de nflverse (spread y total). Para las yardas y conteos la línea de referencia es la mediana de los
últimos 8 partidos del jugador (.5), porque no hay histórico de líneas de las casas.
"""
from __future__ import annotations

import math
from collections import defaultdict

from .modelo import (STATS_POR_POSICION, Linea, construir_contexto, entorno, p_al_menos, preparar_equipo,
                     proyectar, valor)
from .modelo_partido import prob_partido, simular

TRAMOS = ((0.0, 0.1), (0.1, 0.2), (0.2, 0.3), (0.3, 0.4), (0.4, 0.5), (0.5, 0.6), (0.6, 0.7), (0.7, 0.8),
          (0.8, 1.01))


def backtest(conn, desde: str, hasta: str, progreso=None, partidos: bool = False,
             n_simulaciones: int = 1000) -> list[dict]:
    """Con partidos=True también simula cada partido y lo compara con las líneas de cierre (spread y total) y
    con el ganador: 'g_spread' (cubre el local), 'g_total' (más del total) y 'g_ml' (gana el local)."""
    dias = [r[0] for r in conn.execute(
        "SELECT DISTINCT gameday FROM nfl_games WHERE gameday >= ? AND gameday <= ? AND home_score IS NOT NULL "
        "ORDER BY gameday", (desde, hasta))]
    filas = []
    for dia in dias:
        ctx = construir_contexto(conn, dia, usar_estado_actual=False)
        juegos = conn.execute("SELECT * FROM nfl_games WHERE gameday = ? AND home_score IS NOT NULL", (dia,)).fetchall()
        for g in juegos:
            reales = {r["player_id"]: dict(r) for r in conn.execute(
                "SELECT pg.*, pp.long_rec, pp.long_rush FROM nfl_player_games pg LEFT JOIN nfl_player_pbp pp "
                "ON pp.game_id = pg.game_id AND pp.player_id = pg.player_id WHERE pg.game_id = ?", (g["game_id"],))}
            if not reales:
                continue
            linea = Linea(total=g["total_line"], spread_home=g["spread_line"])
            if partidos and g["home_team"] in ctx.perfiles and g["away_team"] in ctx.perfiles:
                sim = simular(ctx, g["home_team"], g["away_team"], n=n_simulaciones, viento=g["wind"],
                              techo=g["roof"])
                dif, total = g["home_score"] - g["away_score"], g["home_score"] + g["away_score"]
                if g["spread_line"] is not None and dif != g["spread_line"]:
                    p, _ = prob_partido(sim, "pts", "sp", "game", "home", "home", -g["spread_line"])
                    filas.append({"fecha": dia, "player_id": g["game_id"], "pos": "-", "stat": "g_spread",
                                  "prob": p, "acierto": int(dif > g["spread_line"]), "ingenua": 0.5})
                if g["total_line"] is not None and total != g["total_line"]:
                    p, media = prob_partido(sim, "pts", "ou", "game", "all", "más", g["total_line"])
                    filas.append({"fecha": dia, "player_id": g["game_id"], "pos": "-", "stat": "g_total",
                                  "prob": p, "acierto": int(total > g["total_line"]), "ingenua": 0.5,
                                  "media": media, "real": total})
                if dif != 0:
                    p, _ = prob_partido(sim, "pts", "ml", "game", "home", "home", None)
                    filas.append({"fecha": dia, "player_id": g["game_id"], "pos": "-", "stat": "g_ml",
                                  "prob": p, "acierto": int(dif > 0), "ingenua": 0.5})
            for team, opp, local in ((g["home_team"], g["away_team"], True), (g["away_team"], g["home_team"], False)):
                if team not in ctx.perfiles or opp not in ctx.perfiles:
                    continue
                # Los que no jugaron cuentan como bajas conocidas.
                for pid, partidos in ctx.jugadores.items():
                    if partidos[0]["team"] == team and pid not in reales:
                        ctx.lesiones[pid] = {"status": "Out", "detail": ""}
                ent = entorno(ctx, team, opp, local, linea, g["wind"], g["roof"])
                for j in preparar_equipo(ctx, team):
                    real = reales.get(j.player_id)
                    if real is None or j.n < 3:
                        continue
                    p = proyectar(ctx, j, ent)
                    lam = p.lambdas.get("tds", 0)
                    if lam >= 0.02:
                        tds = valor(real, "tds")
                        hist = [valor(x, "tds") >= 1 for x in j.partidos[:16]]
                        ingenua = (sum(hist) + 1) / (len(hist) + 4)
                        filas.append({"fecha": dia, "player_id": j.player_id, "pos": j.pos, "stat": "tds_1",
                                      "prob": p_al_menos(lam, 1), "acierto": int(tds >= 1), "ingenua": ingenua})
                        filas.append({"fecha": dia, "player_id": j.player_id, "pos": j.pos, "stat": "tds_2",
                                      "prob": p_al_menos(lam, 2), "acierto": int(tds >= 2), "ingenua": None})
                    for stat in STATS_POR_POSICION[j.pos]:
                        if stat == "tds" or stat not in p.medias:
                            continue
                        prev = sorted(valor(x, stat) for x in j.partidos[:8])
                        if len(prev) < 4:
                            continue
                        ref = math.floor(prev[len(prev) // 2]) + 0.5
                        mas, _ = p.prob(stat, ref)
                        hits = sum(v > ref for v in prev)
                        filas.append({"fecha": dia, "player_id": j.player_id, "pos": j.pos, "stat": stat,
                                      "prob": mas, "acierto": int(valor(real, stat) > ref),
                                      "ingenua": (hits + 1) / (len(prev) + 2), "media": p.medias[stat],
                                      "real": valor(real, stat)})
        if progreso:
            progreso(dia, len(filas))
    return filas


def _brier(fs: list[dict], clave: str = "prob") -> float:
    return sum((f[clave] - f["acierto"]) ** 2 for f in fs) / len(fs)


def resumen(filas: list[dict]) -> dict:
    out = {"stats": {}, "tramos_td": [], "tramos": []}
    por_stat = defaultdict(list)
    for f in filas:
        por_stat[f["stat"]].append(f)
    for stat, fs in por_stat.items():
        con_ing = [f for f in fs if f["ingenua"] is not None]
        out["stats"][stat] = {"n": len(fs), "acierto": sum(f["acierto"] for f in fs) / len(fs),
                              "prob_media": sum(f["prob"] for f in fs) / len(fs), "brier": _brier(fs),
                              "brier_ingenua": _brier(con_ing, "ingenua") if con_ing else None}
    for nombre, fs in (("tramos_td", por_stat.get("tds_1", [])),
                       ("tramos", [f for f in filas if not f["stat"].startswith(("tds", "g_"))])):
        for lo, hi in TRAMOS:
            t = [f for f in fs if lo <= f["prob"] < hi]
            if t:
                out[nombre].append({"tramo": f"{lo * 100:.0f}-{min(hi, 1) * 100:.0f}%", "n": len(t),
                                    "prob_media": sum(f["prob"] for f in t) / len(t),
                                    "acierto": sum(f["acierto"] for f in t) / len(t)})
    return out
