"""Cruza las probabilidades del modelo con las cuotas reales de las casas de apuestas.

Para cada mercado se usa la cuota mediana entre casas (más robusta que la mejor, que a veces
es un error o una línea desactualizada) y se informa también la mejor disponible.
Cuando existe el lado contrario del mercado, se calcula la probabilidad implícita sin margen
y se combina con la del modelo: el mercado suele ser más preciso que cualquier modelo propio,
así que mezclar ambos evita "valor" falso por errores del modelo.
"""
from __future__ import annotations

import re
import unicodedata
from statistics import median

from .model import Market

# Nombres de mercado en API-Football (normalizados: minúsculas, sin espacios ni símbolos).
BETS = {
    ("goals", "total"): ["goalsoverunder"],
    ("goals", "home"): ["totalhome"],
    ("goals", "away"): ["totalaway"],
    ("corners", "total"): ["cornersoverunder", "totalcorners"],
    ("corners", "home"): ["homecornersoverunder", "totalcornershome"],
    ("corners", "away"): ["awaycornersoverunder", "totalcornersaway"],
    ("cards", "total"): ["cardsoverunder", "totalcards"],
    ("cards", "home"): ["hometeamtotalcards", "homecardsoverunder"],
    ("cards", "away"): ["awayteamtotalcards", "awaycardsoverunder"],
    ("shots_on", "total"): ["totalshotongoal", "shotsongoaloverunder", "totalshotsongoal"],
    ("shots_on", "home"): ["homeshotongoal", "homeshotsongoal"],
    ("shots_on", "away"): ["awayshotongoal", "awayshotsongoal"],
    ("shots_total", "total"): ["totalshots", "shotsoverunder"],
}
RESULT_VALUES = {"1": "home", "X": "draw", "2": "away"}
DC_VALUES = {"1X": "homedraw", "X2": "drawaway", "12": "homeaway"}
OPUESTO = {"over": "under", "under": "over", "yes": "no", "no": "yes"}


def _norm(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9.]", "", text.lower())


class OddsBook:
    def __init__(self, rows):
        self.by_key: dict[tuple[str, str], list[float]] = {}
        for r in rows:
            self.by_key.setdefault((_norm(r["bet"]), _norm(r["value"])), []).append(r["odd"])

    def get(self, bets: list[str], value: str) -> list[float]:
        for b in bets:
            odds = self.by_key.get((b, _norm(value)))
            if odds:
                return odds
        return []

    def find(self, bet_contains: str, value_contains: str) -> list[float]:
        bet_contains, value_contains = _norm(bet_contains), _norm(value_contains)
        for (b, v), odds in self.by_key.items():
            if bet_contains in b and value_contains and value_contains == v:
                return odds
        return []


def _base_markets(home: str, away: str) -> list[Market]:
    """Mercados posibles sin modelo, para mirarlos solo con las cuotas."""
    from .model import NOMBRES
    out = [
        Market("result:1", f"Gana {home}", 0, "goals", "match", "1"),
        Market("result:X", "Empate", 0, "goals", "match", "X"),
        Market("result:2", f"Gana {away}", 0, "goals", "match", "2"),
        Market("btts:yes", "Ambos marcan: sí", 0, "goals", "match", "yes"),
        Market("btts:no", "Ambos marcan: no", 0, "goals", "match", "no"),
    ]
    rangos = {"goals": range(0, 6), "corners": range(5, 15), "cards": range(1, 9), "shots_on": range(4, 16),
              "shots_total": range(16, 34)}
    for (stat, scope), _ in BETS.items():
        quien = {"total": "", "home": f"{home} ", "away": f"{away} "}[scope]
        r = rangos[stat] if scope == "total" else range(0, max(1, rangos[stat].stop // 2 + 1))
        for x in r:
            line = x + 0.5
            for side, txt in (("over", "más"), ("under", "menos")):
                label = f"{quien}{txt} de {line} {NOMBRES[stat]}"
                out.append(Market(f"{stat}:{scope}:{side}:{line}", label[0].upper() + label[1:], 0, stat, scope,
                                  side, line))
    return out


def market_only(rows, home: str, away: str) -> list[Market]:
    """Probabilidades implícitas (sin margen) de las casas, para partidos sin historial suficiente.

    No sirven para encontrar valor (por definición la cuota es "justa" según el mercado), solo
    para saber qué resultados ve más probables el mercado.
    """
    book = OddsBook(rows)
    out = []
    result_odds = {s: book.get(["matchwinner"], v) for s, v in RESULT_VALUES.items()}
    for m in _base_markets(home, away):
        odds = _odds_for(book, m)
        if not odds:
            continue
        if m.key.startswith("result:"):
            if not all(result_odds.values()):
                continue
            inv = {s: 1 / median(o) for s, o in result_odds.items()}
            p = inv[m.side] / sum(inv.values())
        else:
            contra = _odds_for(book, m, OPUESTO[m.side])
            if not contra:
                continue
            a, b = 1 / median(odds), 1 / median(contra)
            p = a / (a + b)
        m.prob = m.market_prob = m.final_prob = p
        m.odd, m.best_odd, m.bookmakers = round(median(odds), 3), max(odds), len(odds)
        m.edge = p * m.odd - 1
        out.append(m)
    # Doble oportunidad a partir del 1X2.
    if all(result_odds.values()):
        inv = {s: 1 / median(o) for s, o in result_odds.items()}
        tot = sum(inv.values())
        for side, label in (("1X", f"{home} o empate"), ("X2", f"{away} o empate"), ("12", "No hay empate")):
            m = Market(f"dc:{side}", label, 0, "goals", "match", side)
            odds = _odds_for(book, m)
            if odds:
                p = sum(inv[c] for c in side) / tot
                m.prob = m.market_prob = m.final_prob = p
                m.odd, m.best_odd, m.bookmakers = round(median(odds), 3), max(odds), len(odds)
                m.edge = p * m.odd - 1
                out.append(m)
    return out


def _odds_for(book: OddsBook, m: Market, side: str | None = None) -> list[float]:
    side = side or m.side
    if m.key.startswith("result:"):
        return book.get(["matchwinner"], RESULT_VALUES[side])
    if m.key.startswith("dc:"):
        return book.get(["doublechance"], DC_VALUES[side])
    if m.key.startswith("btts:"):
        return book.get(["bothteamsscore"], side)
    if m.scope == "player":
        if not m.player_name or side != "over":
            return []
        if m.stat == "goals" and m.line == 0.5:
            return book.find("anytimegoalscorer", m.player_name)
        # "Home Player Shots" / "Away Player Shots On Target Total", valores "Nombre - N" = N o más.
        bet = {"shots_total": "playershots", "shots_on": "playershotsontargettotal"}[m.stat]
        valor = f"{m.player_name} - {int(m.line + 0.5)}"
        for prefijo in ("home", "away"):
            odds = book.get([prefijo + bet], valor)
            if odds:
                return odds
        return []
    bets = BETS.get((m.stat, m.scope))
    if not bets or side not in ("over", "under"):
        return []
    return book.get(bets, f"{side} {m.line}")


def attach_odds(markets: list[Market], rows, peso_modelo: float = 0.5) -> None:
    book = OddsBook(rows)
    result_odds = {s: book.get(["matchwinner"], v) for s, v in RESULT_VALUES.items()}
    for m in markets:
        odds = _odds_for(book, m)
        m.final_prob = m.prob
        if not odds:
            continue
        m.odd, m.best_odd, m.bookmakers = round(median(odds), 3), max(odds), len(odds)

        # Probabilidad del mercado sin margen.
        implied = None
        if m.key.startswith("result:") and all(result_odds.values()):
            inv = {s: 1 / median(o) for s, o in result_odds.items()}
            implied = inv[m.side] / sum(inv.values())
        elif m.side in OPUESTO:
            contra = _odds_for(book, m, OPUESTO[m.side])
            if contra:
                a, b = 1 / median(odds), 1 / median(contra)
                implied = a / (a + b)
        if implied is not None:
            m.market_prob = implied
            m.final_prob = peso_modelo * m.prob + (1 - peso_modelo) * implied
        m.edge = m.final_prob * m.odd - 1
