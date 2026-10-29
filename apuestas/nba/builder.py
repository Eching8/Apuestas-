"""Bet builder por partido (varios "más de" de titulares del mismo partido) y dobles de bet builders.

Cada pierna es la línea .5 más alta de un titular estable que pasa con al menos PROB_PIERNA. Descartan
al jugador las alertas de DESCARTA; el cambio de rol no, porque al inicio de temporada lo tiene casi un tercio
de los jugadores (28 oct 2026: 43 de 134) y a menudo es justo lo que explica su buena racha. La probabilidad de acertar todas tiene en cuenta que los jugadores de un mismo partido se
mueven un poco juntos (ritmo, prórroga): correlación de sus desvíos frente a su media, temporada 2025-26,
puntos +0.08 entre compañeros y +0.04 entre rivales; asistencias, rebotes y triples casi nada. Se simula
con una cópula normal con un factor del partido y otro del equipo.

Las casas no publican aquí la cuota de estas líneas alternativas: se da la cuota justa (1 / probabilidad)
para compararla con la del bet builder de la casa.
"""
from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from statistics import NormalDist

from .analizador import Partido
from .modelo import Contexto, Jugador, NOMBRES, _aciertos, _prob_jugador, alertas, predecir, prob_lados, valor

PROB_PIERNA = 0.72
PIERNAS = 4
SIMULACIONES = 20000
# Media mínima en sus últimos 10 para considerar la estadística.
MINIMOS = {"points": 10, "assists": 3, "rebounds": 5, "threes": 1.5}
# Varianza del factor partido (g) y del factor equipo (t) por estadística: correlación entre compañeros
# = g + t y entre rivales = g.
FACTORES = {"points": (0.036, 0.045), "rebounds": (0.026, 0.005), "assists": (0.01, 0.0), "threes": (0.005, 0.0)}


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
    prob: float = 0.0          # de acertar todas, con correlación

    @property
    def cuota_justa(self) -> float:
        return 1 / self.prob if self.prob else float("inf")


def linea_minima_casa(principal: float) -> float:
    """La línea alternativa más baja que suele ofrecer la casa: la principal menos ~10 % (al menos 1).
    27 oct 2026, Betano: Cade 8.5 asistencias -> 8+, Brunson 25.5 puntos -> 24+, Dončić 32.5 -> 30+,
    Reaves 5.5 asistencias -> 5+ (en rebotes y en algunos puntos ofrece incluso algo más bajo)."""
    return principal - max(1, math.floor(0.1 * principal))


# Con 3+ partidos esta temporada, la línea tiene que haberla pasado en al menos 2 de cada 3; si no, se prueba
# una más baja (sin bajar de la mínima de la casa). Backtest 2025-26: inicio (25 oct-20 nov) prometían 50.9 % y
# acertaron 61.0 % (sin el filtro, 48.1 % y 56.4 %); diciembre, 51.6 % y 55.8 % (sin él, 49.3 % y 52.9 %). Dar
# más peso a esta temporada en todo el modelo empeoró el Brier en las dos ventanas, incluso solo para quien
# cambió de rol o de equipo: pocos partidos son ruido para la media, pero sirven para descartar líneas.
ACIERTO_TEMPORADA_MIN = 0.67
DESCARTA = {"suplente", "minutos inestables", "traspaso reciente", "en el parte de lesiones"}


def piernas(ctx: Contexto, j: Jugador, objetivo: float = PROB_PIERNA,
            principales: dict[tuple[str, str], float] | None = None) -> list[Pierna]:
    """Las piernas posibles del jugador. Con la línea principal de la casa, solo líneas que la casa ofrece."""
    if set(alertas(j, "points")) & DESCARTA:
        return []
    out = []
    ult = j.partidos[:10]
    for stat, minimo in MINIMOS.items():
        if sum(valor(p, stat) for p in ult) / len(ult) < minimo:
            continue
        pred = predecir(ctx, j, stat)
        principal = (principales or {}).get((j.player_id, stat))
        piso = linea_minima_casa(principal) if principal is not None else -1
        actual = [x for x in j.partidos if x["season"] == ctx.temporada]
        for k in range(int(pred.mu), -1, -1):
            if k + 0.5 < piso:
                break
            p = _prob_jugador(j, stat, k + 0.5, "más", prob_lados(k + 0.5, pred.mu, pred.var)[0])
            hits_t, n_t = _aciertos(actual, stat, k + 0.5, "más")
            if n_t >= 3 and hits_t < ACIERTO_TEMPORADA_MIN * n_t:
                continue   # esta temporada no la está pasando: probar una línea más baja
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
            # Más de la línea = el desvío del jugador no cae en la cola baja.
            if -z > u:
                ok = False
                break
        aciertos += ok
    return aciertos / sims


def builder(ctx: Contexto, part: Partido, n: int = PIERNAS, objetivo: float = PROB_PIERNA,
            modo: str = "seguro") -> Builder | None:
    """modo "seguro": las piernas más probables. Modo "cuota": las más cercanas al objetivo (por encima),
    que son líneas más altas y pagan más (cuota justa del bet builder de 4 piernas en torno a 3.5-4)."""
    principales = {(e.player_id, e.stat): e.line for e in part.evaluaciones}
    candidatas = []
    for j in part.jugadores.values():
        candidatas += piernas(ctx, j, objetivo, principales)
    if modo == "cuota":
        # Puntos y asistencias primero (las casas los pagan mejor que rebotes de 1.5) y lo más cerca del objetivo.
        orden = sorted(candidatas, key=lambda x: (x.stat not in ("points", "assists"), x.prob))
    else:
        orden = sorted(candidatas, key=lambda x: -x.prob)
    elegidas, jugadores = [], set()
    for p in orden:
        if p.player_id not in jugadores:
            jugadores.add(p.player_id)
            elegidas.append(p)
        if len(elegidas) == n:
            break
    if len(elegidas) < n:
        return None
    return Builder(part, elegidas, prob_conjunta(elegidas))


def del_dia(ctx: Contexto, partidos: list[Partido], modo: str = "seguro"
            ) -> tuple[list[Builder], tuple[Builder, Builder] | None]:
    builders = [b for b in (builder(ctx, p, modo=modo) for p in partidos) if b]
    builders.sort(key=lambda b: -b.prob)
    doble = (builders[0], builders[1]) if len(builders) >= 2 else None
    return builders, doble
