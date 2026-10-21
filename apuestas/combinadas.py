"""Construcción de combinadas a partir de las selecciones candidatas.

Se usa como máximo una selección por partido: dos selecciones del mismo partido (p. ej. "más
de 2.5 goles" y "ambos marcan") están correlacionadas y multiplicar sus probabilidades
sobrestimaría la de la combinada.
"""
from __future__ import annotations

import itertools
import math
from dataclasses import dataclass

from .model import Market

POOL_MAX = 24        # selecciones que entran en la búsqueda
POR_PARTIDO = 3      # mejores selecciones por partido que se consideran


@dataclass
class Leg:
    fixture_id: int
    partido: str
    market: Market

    @property
    def prob(self) -> float:
        return self.market.final_prob if self.market.final_prob is not None else self.market.prob

    @property
    def odd(self) -> float:
        # Sin cuota real se usa la cuota justa: la combinada solo vale si la casa paga más que eso.
        return self.market.odd or self.market.fair_odd


@dataclass
class Combo:
    perfil: str
    legs: list[Leg]

    @property
    def prob(self) -> float:
        return math.prod(l.prob for l in self.legs)

    @property
    def odd(self) -> float:
        return math.prod(l.odd for l in self.legs)

    @property
    def con_cuotas(self) -> bool:
        return all(l.market.odd for l in self.legs)

    @property
    def ev(self) -> float:
        return self.prob * self.odd - 1

    @property
    def kelly(self) -> float:
        """Fracción de Kelly al 25 %, con tope del 2 % del bankroll."""
        if not self.con_cuotas or self.odd <= 1:
            return 0.0
        f = (self.prob * self.odd - 1) / (self.odd - 1)
        return max(0.0, min(0.02, f / 4))


def _pool(legs: list[Leg], score) -> list[Leg]:
    by_fx: dict[int, list[Leg]] = {}
    for l in sorted(legs, key=score, reverse=True):
        by_fx.setdefault(l.fixture_id, [])
        if len(by_fx[l.fixture_id]) < POR_PARTIDO:
            by_fx[l.fixture_id].append(l)
    return sorted((l for ls in by_fx.values() for l in ls), key=score, reverse=True)[:POOL_MAX]


def _enumerate(pool: list[Leg], max_size: int):
    for size in range(2, max_size + 1):
        for combo in itertools.combinations(pool, size):
            if len({l.fixture_id for l in combo}) == size:
                yield list(combo)


def _top(combos: list[Combo], key, n: int) -> list[Combo]:
    """Las n mejores combinadas que no repiten exactamente los mismos partidos."""
    out, seen = [], set()
    for c in sorted(combos, key=key, reverse=True):
        firma = frozenset(l.fixture_id for l in c.legs)
        if firma in seen:
            continue
        seen.add(firma)
        out.append(c)
        if len(out) == n:
            break
    return out


def build_combos(legs: list[Leg], prob_min: float, max_size: int = 4, cuota_min: float = 2.0,
                 n: int = 3) -> dict[str, list[Combo]]:
    """Devuelve combinadas por perfil:

    - alta_probabilidad: la mayor probabilidad conjunta con cuota total >= cuota_min.
    - valor: el mayor valor esperado (EV) con probabilidad conjunta >= prob_min.
    """
    if len({l.fixture_id for l in legs}) < 2:
        return {"alta_probabilidad": [], "valor": []}

    seguras = [Combo("alta_probabilidad", c) for c in _enumerate(_pool(legs, lambda l: l.prob), max_size)]
    seguras = [c for c in seguras if c.odd >= cuota_min]

    valor_pool = _pool(legs, lambda l: l.prob * l.odd)
    valor = [Combo("valor", c) for c in _enumerate(valor_pool, max_size)]
    valor = [c for c in valor if c.prob >= prob_min and c.con_cuotas and c.ev > 0]

    return {
        "alta_probabilidad": _top(seguras, lambda c: c.prob, n),
        "valor": _top(valor, lambda c: c.ev, n),
    }
