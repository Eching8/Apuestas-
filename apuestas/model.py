"""Modelo estadístico: convierte el historial de los equipos en probabilidades por mercado.

- Goles: Poisson independiente por equipo (1X2, doble oportunidad, ambos marcan, totales).
- Córners, tarjetas y tiros: binomial negativa (permite más varianza que Poisson, que es lo
  habitual en estas estadísticas), con la dispersión estimada del propio historial.
- Jugadores: tasa por 90 minutos ajustada por los minutos esperados y por el rival.

La fuerza de cada equipo es ataque × defensa del rival / media de la liga, con los partidos
recientes pesando más y una contracción hacia la media cuando hay pocos datos.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from statistics import median

STATS = ("goals", "corners", "cards", "shots_on", "shots_total")
NOMBRES = {
    "goals": "goles", "corners": "córners", "cards": "tarjetas",
    "shots_on": "tiros a puerta", "shots_total": "remates totales",
}
DECAY = 0.85          # peso del partido i-ésimo más antiguo: DECAY**i
SHRINK_K = 3.0        # partidos "virtuales" de media de liga que se suman al historial
# Ventaja de local por estadística (multiplicador local, visitante).
VENTAJA_LOCAL = {
    "goals": (1.08, 0.93), "corners": (1.06, 0.95), "shots_on": (1.06, 0.95),
    "shots_total": (1.06, 0.95), "cards": (0.95, 1.05),
}
# Medias por equipo y partido si la base aún no tiene datos de la liga (referencias europeas típicas).
MEDIAS_POR_DEFECTO = {"goals": 1.35, "corners": 5.0, "cards": 2.1, "shots_on": 4.3, "shots_total": 12.0}


# --- Distribuciones -------------------------------------------------------------------

def poisson_pmf(k: int, lam: float) -> float:
    if lam <= 0:
        return 1.0 if k == 0 else 0.0
    return math.exp(k * math.log(lam) - lam - math.lgamma(k + 1))


def negbin_pmf(k: int, mu: float, var: float) -> float:
    """Binomial negativa parametrizada por media y varianza (si var <= mu, cae en Poisson)."""
    if var <= mu * 1.0001:
        return poisson_pmf(k, mu)
    r = mu * mu / (var - mu)
    p = r / (r + mu)
    return math.exp(math.lgamma(k + r) - math.lgamma(r) - math.lgamma(k + 1) + r * math.log(p) + k * math.log1p(-p))


def prob_over(line: float, mu: float, var: float | None = None) -> float:
    """P(X > line) para líneas .5"""
    var = mu if var is None else var
    k_max = int(math.floor(line))
    return max(0.0, min(1.0, 1.0 - sum(negbin_pmf(k, mu, var) for k in range(k_max + 1))))


# --- Perfiles de equipo ---------------------------------------------------------------

@dataclass
class TeamProfile:
    team_id: int
    n: int
    favor: dict[str, float] = field(default_factory=dict)
    contra: dict[str, float] = field(default_factory=dict)
    totales: dict[str, list[float]] = field(default_factory=dict)


def _weighted_mean(values: list[float]) -> float | None:
    pairs = [(v, DECAY ** i) for i, v in enumerate(values) if v is not None]
    if not pairs:
        return None
    return sum(v * w for v, w in pairs) / sum(w for _, w in pairs)


def team_profile(team_id: int, history: list) -> TeamProfile:
    """`history` son filas de Database.team_history, del más reciente al más antiguo."""
    prof = TeamProfile(team_id=team_id, n=len(history))
    for s in STATS:
        prof.favor[s] = _weighted_mean([h[s] for h in history])
        prof.contra[s] = _weighted_mean([h[f"{s}_against"] for h in history])
        prof.totales[s] = [h[s] + h[f"{s}_against"] for h in history
                           if h[s] is not None and h[f"{s}_against"] is not None]
    return prof


def _shrink(value: float | None, n: int, mean: float) -> float:
    if value is None:
        return mean
    return (n * value + SHRINK_K * mean) / (n + SHRINK_K)


def _dispersion(home: TeamProfile, away: TeamProfile, stat: str) -> float:
    """Ratio varianza/media de los totales por partido de ambos equipos, acotado."""
    vals = home.totales.get(stat, []) + away.totales.get(stat, [])
    if len(vals) < 6:
        return 1.15
    m = sum(vals) / len(vals)
    if m <= 0:
        return 1.0
    v = sum((x - m) ** 2 for x in vals) / (len(vals) - 1)
    return max(1.0, min(2.5, v / m))


@dataclass
class MatchExpectation:
    home: dict[str, float]
    away: dict[str, float]
    dispersion: dict[str, float]
    n_home: int
    n_away: int

    def total(self, stat: str) -> float:
        return self.home[stat] + self.away[stat]


def expect_match(home: TeamProfile, away: TeamProfile, league_means: dict[str, float] | None) -> MatchExpectation:
    exp_h, exp_a, disp = {}, {}, {}
    for s in STATS:
        m = (league_means or {}).get(s) or MEDIAS_POR_DEFECTO[s]
        att_h, def_a = _shrink(home.favor[s], home.n, m), _shrink(away.contra[s], away.n, m)
        att_a, def_h = _shrink(away.favor[s], away.n, m), _shrink(home.contra[s], home.n, m)
        adv_h, adv_a = VENTAJA_LOCAL[s]
        exp_h[s] = max(0.05, att_h * def_a / m * adv_h)
        exp_a[s] = max(0.05, att_a * def_h / m * adv_a)
        disp[s] = 1.0 if s == "goals" else _dispersion(home, away, s)
    return MatchExpectation(exp_h, exp_a, disp, home.n, away.n)


# --- Mercados -------------------------------------------------------------------------

@dataclass
class Market:
    key: str           # identificador estable, p. ej. "corners:total:over:9.5"
    label: str         # texto para el informe
    prob: float        # probabilidad del modelo
    stat: str
    scope: str         # total | home | away | match | player
    side: str          # over | under | yes | no | 1 | X | 2 | 1X | 12 | X2
    line: float | None = None
    player_id: int | None = None
    player_name: str | None = None
    # Lo rellena odds.attach_odds:
    odd: float | None = None
    best_odd: float | None = None
    bookmakers: int = 0
    market_prob: float | None = None
    final_prob: float | None = None
    edge: float | None = None

    @property
    def fair_odd(self) -> float:
        return 1.0 / max(self.prob, 1e-9)


def _lines_around(mu: float, spread: int = 2) -> list[float]:
    base = math.floor(mu)
    return [x + 0.5 for x in range(max(0, base - spread - 1), base + spread + 1)]


def goal_markets(e: MatchExpectation, home: str, away: str) -> list[Market]:
    lh, la = e.home["goals"], e.away["goals"]
    grid = [[poisson_pmf(i, lh) * poisson_pmf(j, la) for j in range(11)] for i in range(11)]
    p1 = sum(grid[i][j] for i in range(11) for j in range(11) if i > j)
    px = sum(grid[i][i] for i in range(11))
    p2 = 1 - p1 - px
    btts = (1 - poisson_pmf(0, lh)) * (1 - poisson_pmf(0, la))
    out = [
        Market("result:1", f"Gana {home}", p1, "goals", "match", "1"),
        Market("result:X", "Empate", px, "goals", "match", "X"),
        Market("result:2", f"Gana {away}", p2, "goals", "match", "2"),
        Market("dc:1X", f"{home} o empate", p1 + px, "goals", "match", "1X"),
        Market("dc:X2", f"{away} o empate", p2 + px, "goals", "match", "X2"),
        Market("dc:12", "No hay empate", p1 + p2, "goals", "match", "12"),
        Market("btts:yes", "Ambos marcan: sí", btts, "goals", "match", "yes"),
        Market("btts:no", "Ambos marcan: no", 1 - btts, "goals", "match", "no"),
    ]
    for line in (0.5, 1.5, 2.5, 3.5, 4.5):
        po = prob_over(line, lh + la)
        out.append(Market(f"goals:total:over:{line}", f"Más de {line} goles", po, "goals", "total", "over", line))
        out.append(Market(f"goals:total:under:{line}", f"Menos de {line} goles", 1 - po, "goals", "total", "under", line))
    for scope, name, lam in (("home", home, lh), ("away", away, la)):
        for line in (0.5, 1.5, 2.5):
            po = prob_over(line, lam)
            out.append(Market(f"goals:{scope}:over:{line}", f"{name} más de {line} goles", po, "goals", scope, "over", line))
            out.append(Market(f"goals:{scope}:under:{line}", f"{name} menos de {line} goles", 1 - po, "goals", scope, "under", line))
    return out


def count_markets(e: MatchExpectation, stat: str, home: str, away: str) -> list[Market]:
    nombre = NOMBRES[stat]
    out = []
    ratio = e.dispersion[stat]
    mu = e.total(stat)
    for line in _lines_around(mu, 3):
        po = prob_over(line, mu, mu * ratio)
        out.append(Market(f"{stat}:total:over:{line}", f"Más de {line} {nombre}", po, stat, "total", "over", line))
        out.append(Market(f"{stat}:total:under:{line}", f"Menos de {line} {nombre}", 1 - po, stat, "total", "under", line))
    for scope, name in (("home", home), ("away", away)):
        mu_t = getattr(e, scope)[stat]
        for line in _lines_around(mu_t, 2):
            po = prob_over(line, mu_t, mu_t * ratio)
            out.append(Market(f"{stat}:{scope}:over:{line}", f"{name} más de {line} {nombre}", po, stat, scope, "over", line))
            out.append(Market(f"{stat}:{scope}:under:{line}", f"{name} menos de {line} {nombre}", 1 - po, stat, scope, "under", line))
    return out


def match_markets(e: MatchExpectation, home: str, away: str) -> list[Market]:
    out = goal_markets(e, home, away)
    for s in ("corners", "cards", "shots_on", "shots_total"):
        out += count_markets(e, s, home, away)
    return out


# --- Jugadores ------------------------------------------------------------------------

def player_markets(rows: list, rival_factor: dict[str, float], min_partidos: int, max_jugadores: int = 6) -> list[Market]:
    """Mercados de jugador a partir de Database.player_history.

    `rival_factor[stat]` = lo que concede el rival / media de liga (1.0 = rival medio).
    Solo se consideran jugadores habituales (titulares en la mayoría de partidos recientes).
    """
    by_player: dict[int, list] = {}
    for r in rows:
        by_player.setdefault(r["player_id"], []).append(r)
    partidos = len({r["fixture_id"] for r in rows})
    out: list[Market] = []
    candidatos = []
    for pid, apps in by_player.items():
        if len(apps) < min_partidos or len(apps) < 0.6 * partidos:
            continue
        minutos = [a["minutes"] for a in apps]
        total_min = sum(minutos)
        if total_min < 60 * min_partidos:
            continue
        exp_min = median(minutos) * len(apps) / partidos   # castiga a los que a veces no juegan
        tasa = {s: sum(a[s] for a in apps) / total_min * 90 for s in ("shots_on", "shots_total", "goals")}
        candidatos.append((tasa["shots_total"], pid, apps[0]["name"], exp_min, tasa))
    candidatos.sort(reverse=True)

    for _, pid, name, exp_min, tasa in candidatos[:max_jugadores]:
        lam_on = tasa["shots_on"] * exp_min / 90 * rival_factor.get("shots_on", 1.0)
        lam_tot = tasa["shots_total"] * exp_min / 90 * rival_factor.get("shots_total", 1.0)
        lam_g = tasa["goals"] * exp_min / 90 * rival_factor.get("goals", 1.0)
        for stat, lam, line, texto in (
            ("shots_on", lam_on, 0.5, "1+ tiro a puerta"),
            ("shots_on", lam_on, 1.5, "2+ tiros a puerta"),
            ("shots_total", lam_tot, 0.5, "1+ remate"),
            ("shots_total", lam_tot, 1.5, "2+ remates"),
            ("shots_total", lam_tot, 2.5, "3+ remates"),
            ("goals", lam_g, 0.5, "marca gol"),
        ):
            # Remates de jugador tienen algo más de varianza que Poisson.
            p = prob_over(line, lam, lam * (1.0 if stat == "goals" else 1.2))
            out.append(Market(f"player:{pid}:{stat}:over:{line}", f"{name}: {texto}", p, stat, "player", "over",
                              line, player_id=pid, player_name=name))
    return out
