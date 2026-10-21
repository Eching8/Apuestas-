"""Modelo estadístico.

Para cada estadística (goles, córners, tarjetas, remates, tiros al arco) se calcula un índice de
ataque ("a favor") y de defensa ("en contra") por equipo, relativo a la media de la liga y con
encogimiento bayesiano hacia 1.0 cuando hay pocos partidos. El valor esperado del partido es:

    λ_local     = media_liga_local     × ataque_local     × defensa_visitante
    λ_visitante = media_liga_visitante × ataque_visitante × defensa_local

Goles: Poisson bivariado con corrección Dixon-Coles para marcadores bajos.
Córners/tarjetas/remates: Binomial negativa (capturan la sobredispersión real de estos conteos).
Tarjetas: se ajustan además por el promedio histórico del árbitro.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

from .config import SETTINGS
from .db import Database

STATS = {
    # nombre: (columna a favor, columna en contra)
    "goals": ("goals", "goals_against"),
    "corners": ("corners", "corners_against"),
    "cards": ("cards", "cards_against"),
    "shots": ("shots", "shots_against"),
    "shots_on": ("shots_on", "shots_on_against"),
}
MAX_N = 40
BASELINE_PRIOR = 30  # partidos virtuales con la media global al estimar la media de una liga
MARKET_GOALS_WEIGHT = 0.5  # peso de los goles implícitos en las cuotas frente al modelo


# ------------------------------------------------------------------ distribuciones
def poisson_pmf(k: int, lam: float) -> float:
    if lam <= 0:
        return 1.0 if k == 0 else 0.0
    return math.exp(k * math.log(lam) - lam - math.lgamma(k + 1))


def nbinom_pmf(k: int, mean: float, disp: float | None) -> float:
    """Binomial negativa parametrizada por media y dispersión k (var = μ + μ²/k). disp=None -> Poisson."""
    if disp is None or disp <= 0 or disp > 1e4:
        return poisson_pmf(k, mean)
    p = disp / (disp + mean)
    return math.exp(math.lgamma(k + disp) - math.lgamma(disp) - math.lgamma(k + 1)
                    + disp * math.log(p) + k * math.log1p(-p))


def dist(mean: float, disp: float | None, n: int = MAX_N) -> list[float]:
    probs = [nbinom_pmf(k, mean, disp) for k in range(n)]
    tail = max(0.0, 1.0 - sum(probs))
    probs[-1] += tail
    return probs


def prob_over(probs: list[float], line: float) -> float:
    return sum(p for k, p in enumerate(probs) if k > line)


def convolve(a: list[float], b: list[float]) -> list[float]:
    out = [0.0] * (len(a) + len(b) - 1)
    for i, pa in enumerate(a):
        if pa < 1e-12:
            continue
        for j, pb in enumerate(b):
            out[i + j] += pa * pb
    return out


def dispersion(values: list[float]) -> float | None:
    """Estima k por método de momentos; None si no hay sobredispersión (=> Poisson)."""
    if len(values) < 10:
        return None
    m = sum(values) / len(values)
    var = sum((v - m) ** 2 for v in values) / (len(values) - 1)
    if var <= m * 1.02 or m <= 0:
        return None
    return m * m / (var - m)


def score_matrix(lh: float, la: float, rho: float = -0.08, n: int = 11) -> list[list[float]]:
    """Matriz de marcadores con corrección Dixon-Coles."""
    m = [[poisson_pmf(i, lh) * poisson_pmf(j, la) for j in range(n)] for i in range(n)]
    m[0][0] *= max(0.0, 1 - lh * la * rho)
    m[0][1] *= max(0.0, 1 + lh * rho)
    m[1][0] *= max(0.0, 1 + la * rho)
    m[1][1] *= max(0.0, 1 - rho)
    total = sum(map(sum, m))
    return [[v / total for v in row] for row in m]


def market_implied_goals(odds: dict) -> tuple[float, float] | None:
    """Goles esperados (local, visitante) que mejor reproducen las cuotas sin margen de 1X2 y total."""
    try:
        o1, ox, o2 = odds[("1X2", "1")], odds[("1X2", "X")], odds[("1X2", "2")]
    except KeyError:
        return None
    s = 1 / o1 + 1 / ox + 1 / o2
    target = [1 / o1 / s, 1 / ox / s, 1 / o2 / s]
    ou = None
    for (market, sel), over in odds.items():
        if market == "Goles totales" and sel.startswith("Más de"):
            under = odds.get((market, sel.replace("Más de", "Menos de")))
            if under:
                ou = (float(sel.split()[-1]), (1 / over) / (1 / over + 1 / under))
    best, best_err = None, float("inf")
    grid = [0.2 + 0.05 * i for i in range(77)]
    pm = {lam: [poisson_pmf(k, lam) for k in range(11)] for lam in grid}
    for lh in grid:
        for la in grid:
            if ou and abs((lh + la) - ou[0]) > 2.0:
                continue
            ph, pa = pm[lh], pm[la]
            p1 = px = 0.0
            for i in range(11):
                px += ph[i] * pa[i]
                p1 += ph[i] * sum(pa[:i])
            p2 = 1 - p1 - px
            err = (p1 - target[0]) ** 2 + (px - target[1]) ** 2 + (p2 - target[2]) ** 2
            if ou:
                tot = [0.0] * 21
                for i in range(11):
                    for j in range(11):
                        tot[i + j] += ph[i] * pa[j]
                err += (sum(tot[int(ou[0]) + 1:]) - ou[1]) ** 2
            if err < best_err:
                best, best_err = (lh, la), err
    return best


def blend_with_market(proj: "MatchProjection", odds: dict) -> None:
    implied = market_implied_goals(odds)
    if not implied:
        return
    w = MARKET_GOALS_WEIGHT
    proj.exp_home["goals"] = (1 - w) * proj.exp_home["goals"] + w * implied[0]
    proj.exp_away["goals"] = (1 - w) * proj.exp_away["goals"] + w * implied[1]
    proj.scores = score_matrix(proj.exp_home["goals"], proj.exp_away["goals"])
    proj.market_goals = implied


# ------------------------------------------------------------------ ratings
def _row_value(row, col: str) -> float | None:
    if col == "cards":
        y, r = row["yellow"], row["red"]
        return None if y is None else y + (r or 0)
    if col == "cards_against":
        y, r = row["yellow_against"], row["red_against"]
        return None if y is None else y + (r or 0)
    return row[col]


@dataclass
class LeagueBaseline:
    mean_home: dict[str, float]
    mean_away: dict[str, float]
    disp: dict[str, float | None]
    sample: int


def league_baseline(db: Database, league_id: int, before: str) -> LeagueBaseline:
    rows = db.league_averages(league_id, before)
    fallback = {"goals": (1.50, 1.20), "corners": (5.4, 4.4), "cards": (2.0, 2.3),
                "shots": (13.5, 11.0), "shots_on": (4.8, 3.9)}
    glob = db.all_averages(before)
    mean_home, mean_away, disp = {}, {}, {}
    k = BASELINE_PRIOR
    for stat, (col_for, _) in STATS.items():
        home = [v for r in rows if r["is_home"] and (v := _row_value(r, col_for)) is not None]
        away = [v for r in rows if not r["is_home"] and (v := _row_value(r, col_for)) is not None]
        g_home = [v for r in glob if r["is_home"] and (v := _row_value(r, col_for)) is not None]
        g_away = [v for r in glob if not r["is_home"] and (v := _row_value(r, col_for)) is not None]
        prior_h = sum(g_home) / len(g_home) if len(g_home) >= 40 else fallback[stat][0]
        prior_a = sum(g_away) / len(g_away) if len(g_away) >= 40 else fallback[stat][1]
        # media de la liga suavizada hacia la media global (k partidos "virtuales")
        mean_home[stat] = (sum(home) + k * prior_h) / (len(home) + k)
        mean_away[stat] = (sum(away) + k * prior_a) / (len(away) + k)
        disp[stat] = None if stat == "goals" else dispersion(home + away)
    return LeagueBaseline(mean_home, mean_away, disp, len(rows) // 2)


@dataclass
class TeamRating:
    team_id: int
    attack: dict[str, float] = field(default_factory=dict)
    defense: dict[str, float] = field(default_factory=dict)
    sample: int = 0
    form: str = ""  # últimos resultados, ej. "WWDLW"


# Partidos entre equipos de ligas distintas (copas europeas, amistosos): los índices se calcularon
# contra rivales de otro nivel, así que se atenúan hacia 1.0 (índice ** CROSS_LEAGUE_DAMPING).
CROSS_LEAGUE_DAMPING = 0.6
_baseline_cache: dict[tuple, LeagueBaseline] = {}


def cached_baseline(db: Database, league_id: int, before: str) -> LeagueBaseline:
    key = (id(db), league_id, before)
    if key not in _baseline_cache:
        _baseline_cache[key] = league_baseline(db, league_id, before)
    return _baseline_cache[key]


def main_league(hist) -> int | None:
    counts: dict[int, int] = {}
    for r in hist:
        if r["league_id"] is not None:
            counts[r["league_id"]] = counts.get(r["league_id"], 0) + 1
    return max(counts, key=counts.get) if counts else None


def team_rating(db: Database, team_id: int, before: str, base: LeagueBaseline,
                target_league: int | None = None) -> TeamRating:
    hist = db.team_history(team_id, before, SETTINGS.history_window)
    rating = TeamRating(team_id, sample=len(hist))
    rating.form = "".join(
        "W" if r["goals"] > r["goals_against"] else "D" if r["goals"] == r["goals_against"] else "L"
        for r in hist[:5] if r["goals"] is not None
    )
    # cada partido del historial se compara con la media de SU propia competición
    bases = {r["league_id"]: cached_baseline(db, r["league_id"], before) for r in hist}
    for stat, (col_for, col_against) in STATS.items():
        att_num = def_num = 0.0
        att_w = def_w = 0.0
        for i, r in enumerate(hist):
            w = SETTINGS.decay ** i
            b = bases.get(r["league_id"], base)
            exp_for = b.mean_home[stat] if r["is_home"] else b.mean_away[stat]
            exp_against = b.mean_away[stat] if r["is_home"] else b.mean_home[stat]
            vf, va = _row_value(r, col_for), _row_value(r, col_against)
            if vf is not None and exp_for > 0:
                att_num += w * vf / exp_for
                att_w += w
            if va is not None and exp_against > 0:
                def_num += w * va / exp_against
                def_w += w
        k = SETTINGS.prior_weight
        rating.attack[stat] = (att_num + k) / (att_w + k)
        rating.defense[stat] = (def_num + k) / (def_w + k)
    if target_league is not None and main_league(hist) not in (None, target_league):
        for d in (rating.attack, rating.defense):
            for stat in d:
                d[stat] = d[stat] ** CROSS_LEAGUE_DAMPING
    return rating


def referee_factor(db: Database, referee: str | None, before: str, base: LeagueBaseline) -> float:
    if not referee:
        return 1.0
    rows = db.referee_history(referee, before)
    if not rows:
        return 1.0
    league_cards = base.mean_home["cards"] + base.mean_away["cards"]
    avg = sum((r["yellow"] or 0) + (r["red"] or 0) for r in rows) / len(rows)
    k = 6.0  # encogimiento: un árbitro con 6 partidos pesa la mitad
    return (avg / league_cards * len(rows) + k) / (len(rows) + k)


# ------------------------------------------------------------------ proyección de partido
@dataclass
class MatchProjection:
    fixture_id: int
    home_id: int
    away_id: int
    exp_home: dict[str, float]
    exp_away: dict[str, float]
    disp: dict[str, float | None]
    scores: list[list[float]]
    home_rating: TeamRating
    away_rating: TeamRating
    referee_factor: float = 1.0
    players: list[dict] = field(default_factory=list)
    market_goals: tuple[float, float] | None = None

    def team_dist(self, stat: str, side: str) -> list[float]:
        mean = (self.exp_home if side == "home" else self.exp_away)[stat]
        return dist(mean, self.disp.get(stat))

    def total_dist(self, stat: str) -> list[float]:
        return convolve(self.team_dist(stat, "home"), self.team_dist(stat, "away"))[:MAX_N * 2]

    @property
    def data_quality(self) -> float:
        """0-1 según partidos de historial disponibles."""
        n = min(self.home_rating.sample, self.away_rating.sample)
        return min(1.0, n / 10)


def project_match(db: Database, match: dict) -> MatchProjection:
    before = match["date"]
    _baseline_cache.clear()  # la base de datos crece durante la ejecución
    base = cached_baseline(db, match["league_id"], before)
    h = team_rating(db, match["home_id"], before, base, match["league_id"])
    a = team_rating(db, match["away_id"], before, base, match["league_id"])
    ref = referee_factor(db, match.get("referee"), before, base)
    exp_h, exp_a = {}, {}
    for stat in STATS:
        exp_h[stat] = base.mean_home[stat] * h.attack[stat] * a.defense[stat]
        exp_a[stat] = base.mean_away[stat] * a.attack[stat] * h.defense[stat]
    exp_h["cards"] *= ref
    exp_a["cards"] *= ref
    proj = MatchProjection(match["fixture_id"], match["home_id"], match["away_id"], exp_h, exp_a,
                           base.disp, score_matrix(exp_h["goals"], exp_a["goals"]), h, a, ref)
    proj.players = player_projections(db, match["home_id"], before, exp_h["shots"]) + \
        player_projections(db, match["away_id"], before, exp_a["shots"])
    return proj


def player_projections(db: Database, team_id: int, before: str, team_exp_shots: float) -> list[dict]:
    """Remates y tiros al arco esperados por jugador (últimos 10 partidos del equipo)."""
    rows = db.player_history(team_id, before, matches=10)
    if not rows:
        return []
    team_matches = len({r["fixture_id"] for r in rows})
    team_shots_avg = sum(r["shots"] for r in rows) / max(team_matches, 1)
    pace = team_exp_shots / team_shots_avg if team_shots_avg > 0 else 1.0
    by_player: dict[int, dict] = {}
    for r in rows:
        p = by_player.setdefault(r["player_id"], {"player_id": r["player_id"], "name": r["name"],
                                                  "team_id": team_id, "position": r["position"],
                                                  "apps": 0, "starts": 0, "minutes": 0, "shots": 0, "shots_on": 0})
        if r["minutes"] and r["minutes"] > 0:
            p["apps"] += 1
            p["starts"] += int(r["minutes"] >= 60)
            p["minutes"] += r["minutes"]
            p["shots"] += r["shots"]
            p["shots_on"] += r["shots_on"]
    out = []
    for p in by_player.values():
        if p["apps"] < 3 or p["minutes"] < 180:
            continue
        p_play = p["starts"] / team_matches  # probabilidad aproximada de ser titular
        exp_min = p["minutes"] / p["apps"]
        p["exp_shots"] = p["shots"] / p["minutes"] * exp_min * pace
        p["exp_shots_on"] = p["shots_on"] / p["minutes"] * exp_min * pace
        p["p_play"] = min(1.0, p_play)
        out.append(p)
    return sorted(out, key=lambda x: -x["exp_shots"])[:6]
