"""Simulación de partidos completos para combinar selecciones del mismo partido ("crea tu apuesta").

Multiplicar probabilidades de un mismo partido es un error: "gana el local" y "más de 2.5 goles"
o "más de 8.5 tiros a puerta" y "más de 5.5 atajadas" van de la mano. Aquí se simula el partido
entero, respetando los vínculos más fuertes:

- marcador desde la matriz de Dixon-Coles;
- tiros a puerta = goles + atajadas del portero rival (por definición);
- remates totales = tiros a puerta + remates fuera (binomial negativa);
- córners y tarjetas: binomial negativa por equipo, independientes del marcador (su relación con
  el resultado es débil; es la parte más aproximada).

La probabilidad de una combinación es la fracción de simulaciones en las que se cumplen todas.
"""
from __future__ import annotations

import numpy as np

from .model import Market, MatchExpectation, score_grid

N_SIMULACIONES = 20_000


def _negbin(rng: np.random.Generator, mu: float, ratio: float, n: int) -> np.ndarray:
    mu = max(mu, 1e-3)
    if ratio <= 1.0001:
        return rng.poisson(mu, n)
    r = mu / (ratio - 1)
    return rng.negative_binomial(r, r / (r + mu), n)


def simular(e: MatchExpectation, n: int = N_SIMULACIONES, seed: int = 0) -> dict[str, np.ndarray]:
    """Arrays de n partidos simulados: '<stat>_home' y '<stat>_away' para cada estadística disponible."""
    rng = np.random.default_rng(seed)
    grid = np.array(score_grid(e.home["goals"], e.away["goals"], e.rho))
    idx = rng.choice(grid.size, size=n, p=grid.ravel() / grid.sum())
    sim = {"goals_home": idx // grid.shape[1], "goals_away": idx % grid.shape[1]}
    disp = e.dispersion

    if "shots_on" in e.home:
        for lado, rival in (("home", "away"), ("away", "home")):
            # Atajadas del portero rival = tiros a puerta de este equipo que no fueron gol.
            if "saves" in e.home:
                mu_saves = getattr(e, rival)["saves"]
            else:
                mu_saves = max(0.1, getattr(e, lado)["shots_on"] - getattr(e, lado)["goals"])
            atajadas = _negbin(rng, mu_saves, disp.get("saves", 1.1), n)
            sim[f"saves_{rival}"] = atajadas
            sim[f"shots_on_{lado}"] = sim[f"goals_{lado}"] + atajadas
            if "shots_total" in e.home:
                fuera = max(0.1, getattr(e, lado)["shots_total"] - getattr(e, lado)["shots_on"])
                sim[f"shots_total_{lado}"] = sim[f"shots_on_{lado}"] + _negbin(rng, fuera, disp["shots_total"], n)
    for stat in ("corners", "cards"):
        if stat in e.home:
            for lado in ("home", "away"):
                sim[f"{stat}_{lado}"] = _negbin(rng, getattr(e, lado)[stat], disp[stat], n)
    return sim


def cumple(sim: dict[str, np.ndarray], m: Market) -> np.ndarray | None:
    """Vector booleano: en qué simulaciones gana la selección. None si no se puede simular."""
    gh, ga = sim["goals_home"], sim["goals_away"]
    tipo = m.key.split(":")[0]
    if tipo == "result":
        return {"1": gh > ga, "X": gh == ga, "2": gh < ga}[m.side]
    if tipo == "dc":
        return {"1X": gh >= ga, "X2": gh <= ga, "12": gh != ga}[m.side]
    if tipo == "btts":
        ambos = (gh > 0) & (ga > 0)
        return ambos if m.side == "yes" else ~ambos
    if m.scope not in ("total", "home", "away") or m.line is None or m.side not in ("over", "under"):
        return None
    h, a = sim.get(f"{m.stat}_home"), sim.get(f"{m.stat}_away")
    if h is None or a is None:
        return None
    valor = {"total": h + a, "home": h, "away": a}[m.scope]
    return valor > m.line if m.side == "over" else valor < m.line


def familia(m: Market) -> str:
    """Selecciones de la misma familia son redundantes entre sí (p. ej. dos líneas de córners totales)."""
    tipo = m.key.split(":")[0]
    if tipo in ("result", "dc"):
        return "resultado"
    if tipo == "btts":
        return "btts"
    return f"{m.stat}:{m.scope}"
