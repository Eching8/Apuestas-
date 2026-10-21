"""Generación de mercados, probabilidades, comparación con cuotas y selección de picks."""
from __future__ import annotations

import math
from dataclasses import asdict, dataclass

from .config import SETTINGS
from .model import MatchProjection, poisson_pmf, prob_over
from .sources.api_football import player_key

LINES = {
    "goals": {"total": [0.5, 1.5, 2.5, 3.5, 4.5], "team": [0.5, 1.5, 2.5]},
    "corners": {"total": [6.5, 7.5, 8.5, 9.5, 10.5, 11.5, 12.5], "team": [2.5, 3.5, 4.5, 5.5, 6.5]},
    "cards": {"total": [1.5, 2.5, 3.5, 4.5, 5.5, 6.5], "team": [0.5, 1.5, 2.5, 3.5]},
    "shots_on": {"total": [5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5], "team": [2.5, 3.5, 4.5, 5.5, 6.5]},
    "shots": {"total": [18.5, 20.5, 22.5, 24.5, 26.5, 28.5], "team": [8.5, 9.5, 10.5, 11.5, 12.5, 13.5, 15.5]},
}
LABEL = {"goals": "Goles", "corners": "Córners", "cards": "Tarjetas",
         "shots_on": "Tiros al arco", "shots": "Remates"}
# Mercados con probabilidad muy alta pagan cuotas inútiles y se descartan de los picks
MAX_USEFUL_PROB = 0.88
# Sin cuota real: rango de probabilidad aceptado y margen mínimo exigido sobre la cuota justa
NO_ODDS_BAND = (0.68, 0.84)
NO_ODDS_EDGE = 1.05
MODEL_WEIGHT = 0.65  # peso del modelo frente a la probabilidad implícita (sin margen) de la casa


@dataclass
class Pick:
    fixture_id: int
    match: str
    market: str
    selection: str
    prob: float           # probabilidad final (modelo, combinada con mercado si hay cuota)
    model_prob: float
    fair_odds: float
    odds: float | None = None
    ev: float | None = None
    confidence: str = "Media"
    stat_group: str = ""  # para evitar combinar mercados correlacionados del mismo partido
    min_odds: float | None = None  # sin cuota real: apostar solo si la casa paga al menos esto

    def to_dict(self) -> dict:
        return asdict(self)


def match_markets(p: MatchProjection) -> list[tuple[str, str, float, str]]:
    """-> [(mercado, selección, probabilidad, grupo)]"""
    out: list[tuple[str, str, float, str]] = []
    m = p.scores
    n = len(m)
    p1 = sum(m[i][j] for i in range(n) for j in range(n) if i > j)
    px = sum(m[i][i] for i in range(n))
    p2 = 1 - p1 - px
    out += [("1X2", "1", p1, "resultado"), ("1X2", "X", px, "resultado"), ("1X2", "2", p2, "resultado"),
            ("Doble oportunidad", "1X", p1 + px, "resultado"), ("Doble oportunidad", "X2", p2 + px, "resultado"),
            ("Doble oportunidad", "12", p1 + p2, "resultado")]
    btts = sum(m[i][j] for i in range(1, n) for j in range(1, n))
    out += [("Ambos marcan", "Sí", btts, "goles"), ("Ambos marcan", "No", 1 - btts, "goles")]

    total_goals = [0.0] * (2 * n)
    home_goals, away_goals = [0.0] * n, [0.0] * n
    for i in range(n):
        for j in range(n):
            total_goals[i + j] += m[i][j]
            home_goals[i] += m[i][j]
            away_goals[j] += m[i][j]

    for stat, lines in LINES.items():
        label = LABEL[stat]
        if stat == "goals":
            tot, hd, ad = total_goals, home_goals, away_goals
        else:
            tot, hd, ad = p.total_dist(stat), p.team_dist(stat, "home"), p.team_dist(stat, "away")
        for line in lines["total"]:
            po = prob_over(tot, line)
            out += [(f"{label} totales", f"Más de {line}", po, stat), (f"{label} totales", f"Menos de {line}", 1 - po, stat)]
        for side, d, name in (("home", hd, "local"), ("away", ad, "visitante")):
            for line in lines["team"]:
                po = prob_over(d, line)
                out += [(f"{label} {name}", f"Más de {line}", po, f"{stat}-{side}"),
                        (f"{label} {name}", f"Menos de {line}", 1 - po, f"{stat}-{side}")]

    for pl in p.players:
        for key, label, lines in (("exp_shots", "Remates", (0.5, 1.5, 2.5)), ("exp_shots_on", "Tiros al arco", (0.5, 1.5))):
            lam = pl[key]
            for line in lines:
                p_over = 1 - sum(poisson_pmf(k, lam) for k in range(int(line) + 1))
                out.append((f"{label} jugador: {pl['name']}", f"Más de {line}", pl["p_play"] * p_over,
                            f"player-{pl['player_id']}"))
    return out


def _no_vig(odds: dict, market: str, selection: str) -> float | None:
    """Probabilidad implícita sin margen usando la selección complementaria."""
    o = odds.get((market, selection))
    if not o:
        return None
    if selection.startswith("Más de"):
        other = odds.get((market, selection.replace("Más de", "Menos de")))
        group = [o, other] if other else None
    elif selection.startswith("Menos de"):
        other = odds.get((market, selection.replace("Menos de", "Más de")))
        group = [o, other] if other else None
    elif market == "1X2":
        group = [odds.get(("1X2", s)) for s in ("1", "X", "2")]
        group = group if all(group) else None
        if group:
            return (1 / o) / sum(1 / g for g in group)
    elif market == "Ambos marcan":
        other = odds.get((market, "No" if selection == "Sí" else "Sí"))
        group = [o, other] if other else None
    else:
        group = None
    if not group:
        return None
    return (1 / group[0]) / sum(1 / g for g in group)


def confidence(p: MatchProjection) -> str:
    q = p.data_quality
    return "Alta" if q >= 0.8 else "Media" if q >= 0.5 else "Baja"


def build_picks(p: MatchProjection, match_label: str, odds: dict | None = None) -> list[Pick]:
    odds = odds or {}
    conf = confidence(p)
    picks = []
    for market, sel, prob, group in match_markets(p):
        if not (0.0 < prob < 1.0):
            continue
        o = odds.get((market, sel))
        if o is None and " jugador: " in market:
            label, name = market.split(" jugador: ", 1)
            o = odds.get((player_key(label, name), sel))
        final = prob
        market_p = _no_vig(odds, market, sel)
        if market_p is not None:
            final = MODEL_WEIGHT * prob + (1 - MODEL_WEIGHT) * market_p
        pick = Pick(p.fixture_id, match_label, market, sel, round(final, 4), round(prob, 4),
                    round(1 / final, 2), o, round(final * o - 1, 4) if o else None, conf, group)
        picks.append(pick)
    return picks


def select_value_picks(picks: list[Pick]) -> list[Pick]:
    """Mercados óptimos.

    Con cuota real: probabilidad >= min_prob_pick, EV >= min_ev y cuota <= max_odds_pick.
    Sin cuota real: probabilidad dentro de NO_ODDS_BAND, una sola línea por mercado (la más
    probable dentro del rango) y una cuota mínima a exigir = cuota justa × NO_ODDS_EDGE.
    """
    with_odds, no_odds = [], {}
    for pk in picks:
        if pk.confidence == "Baja" or pk.prob > MAX_USEFUL_PROB:
            continue
        if pk.odds is not None:
            if pk.prob >= SETTINGS.min_prob_pick and pk.ev >= SETTINGS.min_ev and pk.odds <= SETTINGS.max_odds_pick:
                with_odds.append(pk)
        elif NO_ODDS_BAND[0] <= pk.prob <= NO_ODDS_BAND[1]:
            key = (pk.fixture_id, pk.market)
            if key not in no_odds or pk.prob > no_odds[key].prob:
                no_odds[key] = pk
    for pk in no_odds.values():
        pk.min_odds = round(pk.fair_odds * NO_ODDS_EDGE, 2)
    with_odds.sort(key=lambda x: x.ev, reverse=True)
    rest = sorted(no_odds.values(), key=lambda x: x.prob, reverse=True)
    return with_odds + rest


def kelly(prob: float, odds: float, fraction: float = 0.25) -> float:
    """Stake sugerido (fracción del bank) con Kelly fraccional."""
    b = odds - 1
    if b <= 0:
        return 0.0
    k = (prob * b - (1 - prob)) / b
    return max(0.0, round(k * fraction, 4))


def implied(odds: float) -> float:
    return 1 / odds if odds else math.nan
