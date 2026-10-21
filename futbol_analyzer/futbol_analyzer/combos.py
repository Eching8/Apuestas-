"""Constructor de combinadas: alta probabilidad conjunta y valor esperado positivo.

Reglas:
  * Máximo una selección por partido (las selecciones de un mismo partido están correlacionadas
    y las casas suelen penalizarlas o no permitirlas).
  * Cada pata debe tener probabilidad >= combo_leg_min_prob.
  * La probabilidad conjunta se calcula como producto (independencia entre partidos distintos).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from itertools import combinations

from .config import SETTINGS
from .markets import MAX_USEFUL_PROB, Pick


@dataclass
class Combo:
    kind: str
    legs: list[Pick] = field(default_factory=list)

    @property
    def prob(self) -> float:
        r = 1.0
        for leg in self.legs:
            r *= leg.prob
        return r

    @property
    def has_real_odds(self) -> bool:
        return all(leg.odds for leg in self.legs)

    @property
    def odds(self) -> float:
        r = 1.0
        for leg in self.legs:
            r *= leg.odds or leg.min_odds or leg.fair_odds
        return r

    @property
    def ev(self) -> float | None:
        return self.prob * self.odds - 1 if self.has_real_odds else None


def _best_leg_per_match(picks: list[Pick], require_odds: bool) -> list[Pick]:
    """Recibe los picks ya filtrados por select_value_picks."""
    best: dict[int, Pick] = {}
    min_prob = SETTINGS.min_prob_pick if require_odds else SETTINGS.combo_leg_min_prob
    for pk in picks:
        if pk.prob < min_prob or pk.prob > MAX_USEFUL_PROB:
            continue
        if require_odds and (pk.odds is None or pk.ev is None or pk.ev < 0):
            continue
        score = (pk.ev if pk.ev is not None else 0) + pk.prob
        cur = best.get(pk.fixture_id)
        if cur is None or score > (cur.ev if cur.ev is not None else 0) + cur.prob:
            best[pk.fixture_id] = pk
    return sorted(best.values(), key=lambda x: -x.prob)[:20]


def build_combos(picks: list[Pick]) -> list[Combo]:
    combos: list[Combo] = []
    max_legs, min_legs = SETTINGS.combo_max_legs, SETTINGS.combo_min_legs

    # 1) Combinadas de VALOR: solo patas con cuota real y EV positivo; maximiza EV conjunto
    value_legs = _best_leg_per_match(picks, require_odds=True)
    cands = []
    for n in range(min_legs, max_legs + 1):
        for legs in combinations(value_legs, n):
            c = Combo("Valor", list(legs))
            if c.prob >= SETTINGS.combo_min_prob and c.odds >= 1.8:
                cands.append(c)
    combos += _diverse(sorted(cands, key=lambda c: -(c.ev or 0)), SETTINGS.combo_count)

    # 2) Combinadas SEGURAS: máxima probabilidad con cuota total >= 1.70 (con o sin cuota real)
    safe_legs = _best_leg_per_match(picks, require_odds=False)
    cands = []
    for n in range(min_legs, max_legs + 1):
        for legs in combinations(safe_legs, n):
            c = Combo("Alta probabilidad", list(legs))
            if c.odds >= 1.70 and c.prob >= SETTINGS.combo_min_prob:
                cands.append(c)
    combos += _diverse(sorted(cands, key=lambda c: -c.prob), SETTINGS.combo_count)
    return combos


def _diverse(cands: list[Combo], k: int, max_reuse: int = 2) -> list[Combo]:
    """Evita que todas las combinadas repitan las mismas patas."""
    used: dict[tuple, int] = {}
    out = []
    for c in cands:
        keys = [(leg.fixture_id, leg.market, leg.selection) for leg in c.legs]
        if any(used.get(key, 0) >= max_reuse for key in keys):
            continue
        out.append(c)
        for key in keys:
            used[key] = used.get(key, 0) + 1
        if len(out) >= k:
            break
    return out
