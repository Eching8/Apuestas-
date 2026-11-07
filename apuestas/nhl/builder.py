"""Bet builder por partido de la NHL: 2-3 "más de" de jugadores constantes del mismo partido, con el mismo guion.

Cada pierna es la línea .5 más alta (sin bajar de la mínima de la casa) que pasa con al menos PROB_PIERNA y que el
jugador pasó en 2 de cada 3 partidos de esta temporada. La probabilidad de acertar todas tiene en cuenta que los
jugadores de un mismo partido se mueven juntos (cópula normal con un factor del partido y otro del equipo, con las
correlaciones medidas en 2025-26, ver FACTORES). Sin cuota de la casa se da la justa (1 / probabilidad).
"""
from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from statistics import NormalDist

from .analizador import Partido
from .modelo import (NOMBRES, Contexto, Jugador, _aciertos, _prob_jugador, alertas, piso_casa, predecir, prob_lados,
                     valor, vetada)

PROB_PIERNA = 0.72
PIERNAS = 3
PIERNAS_MIN = 2
SIMULACIONES = 20000
MINIMOS = {"shots": 2.0, "points": 0.7, "assists": 0.5, "blocked": 1.5}
ACIERTO_TEMPORADA_MIN = 0.67
# Varianza del factor partido (g) y del factor equipo (t): correlación entre compañeros = g + t, entre rivales = g.
# Medidas en 2025-26 con los desvíos de cada jugador frente a su media (`nhl correlaciones`); ver README.
# 2025-26 (desvíos frente a su media de los últimos 10, jugadores con 14+ min; 183.000 pares de compañeros y 196.000
# de rivales): puntos +0.12 entre compañeros (un gol suma a tres), asistencias +0.05, bloqueados +0.025, tiros +0.02;
# entre rivales, -0.01 a 0 en todo. Entre compañeros de la misma línea la correlación es mayor (ESPN no da las
# líneas): con dos del mismo equipo la probabilidad conjunta queda algo conservadora.
FACTORES = {"shots": (0.0, 0.02), "points": (0.0, 0.12), "assists": (0.0, 0.055), "blocked": (0.0, 0.025)}
# Pares con correlación en contra (otro guion): puntos de un equipo ↔ bloqueados del rival (-0.019) y tiros ↔
# bloqueados del mismo equipo (-0.014). No se combinan en un bet builder.
CONTRARIOS: set[tuple[str, str, bool]] = {("points", "blocked", False), ("shots", "blocked", True),
                                          ("assists", "blocked", False)}   # (stat, stat, mismo equipo)


@dataclass
class Pierna:
    player_id: str
    nombre: str
    team_id: str
    stat: str
    line: float
    prob: float
    mu: float
    acierto_10: tuple[int, int]

    @property
    def etiqueta(self) -> str:
        return f"{self.nombre} {int(self.line + 0.5)}+ {NOMBRES[self.stat]}"


@dataclass
class Builder:
    partido: Partido
    piernas: list[Pierna] = field(default_factory=list)
    prob: float = 0.0

    @property
    def cuota_justa(self) -> float:
        return 1 / self.prob if self.prob else float("inf")


def piernas(ctx: Contexto, j: Jugador, objetivo: float = PROB_PIERNA,
            principales: dict[tuple[str, str], float] | None = None) -> list[Pierna]:
    if j.es_portero or alertas(ctx, j, "shots"):
        return []
    out = []
    ult = j.partidos[:10]
    for stat, minimo in MINIMOS.items():
        if stat == "blocked" and j.grupo != "D":
            continue
        if vetada(j.nombre, stat) or sum(valor(p, stat) for p in ult) / len(ult) < minimo:
            continue
        pred = predecir(ctx, j, stat)
        piso = piso_casa(j, stat, pred.mu, (principales or {}).get((j.player_id, stat)))
        actual = [x for x in j.partidos if x["season"] == ctx.temporada]
        for k in range(int(pred.mu) + 1, -1, -1):
            if k + 0.5 < piso:
                break
            p = _prob_jugador(j, stat, k + 0.5, "más", prob_lados(k + 0.5, pred.mu, pred.var)[0])
            hits_t, n_t = _aciertos(actual, stat, k + 0.5, "más")
            if n_t >= 3 and hits_t < ACIERTO_TEMPORADA_MIN * n_t:
                continue
            if p >= objetivo:
                out.append(Pierna(j.player_id, j.nombre, j.team_id, stat, k + 0.5, p, pred.mu,
                                  _aciertos(ult, stat, k + 0.5, "más")))
                break
    return out


def prob_conjunta(patas: list[Pierna], sims: int = SIMULACIONES, semilla: int = 7) -> float:
    rng = random.Random(semilla)
    normal = NormalDist()
    umbrales = [normal.inv_cdf(min(max(p.prob, 1e-6), 1 - 1e-6)) for p in patas]
    equipos = sorted({p.team_id for p in patas})
    aciertos = 0
    for _ in range(sims):
        g = rng.gauss(0, 1)
        t = {e: rng.gauss(0, 1) for e in equipos}
        ok = True
        for p, u in zip(patas, umbrales):
            vg, vt = FACTORES[p.stat]
            z = math.sqrt(vg) * g + math.sqrt(vt) * t[p.team_id] + math.sqrt(1 - vg - vt) * rng.gauss(0, 1)
            if -z > u:
                ok = False
                break
        aciertos += ok
    return aciertos / sims


def coherente(elegidas: list[Pierna], nueva: Pierna) -> bool:
    for p in elegidas:
        mismo = p.team_id == nueva.team_id
        if (p.stat, nueva.stat, mismo) in CONTRARIOS or (nueva.stat, p.stat, mismo) in CONTRARIOS:
            return False
    return True


def builder(ctx: Contexto, part: Partido, n: int = PIERNAS, objetivo: float = PROB_PIERNA) -> Builder | None:
    principales = {(e.player_id, e.stat): e.line for e in part.evaluaciones if not e.estimada}
    candidatas = []
    for j in part.jugadores.values():
        candidatas += piernas(ctx, j, objetivo, principales)
    elegidas, jugadores = [], set()
    for p in sorted(candidatas, key=lambda x: -x.prob):
        if p.player_id not in jugadores and coherente(elegidas, p):
            jugadores.add(p.player_id)
            elegidas.append(p)
        if len(elegidas) == n:
            break
    if len(elegidas) < PIERNAS_MIN:
        return None
    return Builder(part, elegidas, prob_conjunta(elegidas))


def del_dia(ctx: Contexto, partidos: list[Partido]) -> list[Builder]:
    builders = [b for b in (builder(ctx, p) for p in partidos) if b]
    return sorted(builders, key=lambda b: -b.prob)
