"""Liquidación de predicciones y combinadas con los resultados reales (seguimiento de aciertos/ROI)."""
from __future__ import annotations

import json
import re

from .db import Database
from .markets import LABEL

_STAT_BY_LABEL = {v: k for k, v in LABEL.items()}


def _team_value(row, stat: str) -> float | None:
    if row is None:
        return None
    if stat == "cards":
        return None if row["yellow"] is None else row["yellow"] + (row["red"] or 0)
    return row[stat]


def settle_pick(db: Database, fixture_id: int, market: str, selection: str) -> int | None:
    m = db.q("SELECT * FROM matches WHERE fixture_id=?", (fixture_id,))
    if not m or m[0]["status"] not in ("FT", "AET", "PEN") or m[0]["home_goals"] is None:
        return None
    m = m[0]
    hg, ag = m["home_goals"], m["away_goals"]
    if market == "1X2":
        return int({"1": hg > ag, "X": hg == ag, "2": hg < ag}[selection])
    if market == "Doble oportunidad":
        return int({"1X": hg >= ag, "X2": hg <= ag, "12": hg != ag}[selection])
    if market == "Ambos marcan":
        both = hg > 0 and ag > 0
        return int(both if selection == "Sí" else not both)

    ou = re.match(r"(Más de|Menos de) ([\d.]+)", selection)
    if not ou:
        return None
    line = float(ou.group(2))

    def decide(value: float | None) -> int | None:
        if value is None:
            return None
        return int(value > line) if ou.group(1) == "Más de" else int(value < line)

    if "jugador:" in market:
        label, name = market.split(" jugador: ", 1)
        col = "shots" if label == "Remates" else "shots_on"
        row = db.q(f"SELECT {col} AS v, minutes FROM player_match_stats WHERE fixture_id=? AND name=?", (fixture_id, name))
        if not row:
            return None  # sin datos del jugador (no jugó o no se descargó)
        return decide(row[0]["v"])

    label, scope = market.rsplit(" ", 1)
    stat = _STAT_BY_LABEL.get(label)
    if stat is None:
        return None
    if stat == "goals":
        value = {"totales": hg + ag, "local": hg, "visitante": ag}[scope]
        return decide(value)
    rows = {r["team_id"]: r for r in db.q("SELECT * FROM team_match_stats WHERE fixture_id=?", (fixture_id,))}
    h, a = _team_value(rows.get(m["home_id"]), stat), _team_value(rows.get(m["away_id"]), stat)
    if scope == "totales":
        return decide(None if h is None or a is None else h + a)
    return decide(h if scope == "local" else a)


def settle_pending(db: Database) -> dict:
    settled = 0
    for p in db.q("SELECT fixture_id, market, selection FROM predictions WHERE result IS NULL"):
        res = settle_pick(db, p["fixture_id"], p["market"], p["selection"])
        if res is not None:
            db.conn.execute("UPDATE predictions SET result=? WHERE fixture_id=? AND market=? AND selection=?",
                            (res, p["fixture_id"], p["market"], p["selection"]))
            settled += 1
    for c in db.q("SELECT id, legs FROM combos WHERE result IS NULL"):
        results = [settle_pick(db, leg["fixture_id"], leg["market"], leg["selection"]) for leg in json.loads(c["legs"])]
        if 0 in results:
            db.conn.execute("UPDATE combos SET result=0 WHERE id=?", (c["id"],))
        elif results and all(r == 1 for r in results):
            db.conn.execute("UPDATE combos SET result=1 WHERE id=?", (c["id"],))
    db.conn.commit()
    return {"settled": settled}


def performance(db: Database) -> dict:
    """Rendimiento histórico de los picks publicados (solo los que tenían cuota real)."""
    rows = db.q("SELECT prob, odds, result FROM predictions WHERE result IS NOT NULL AND odds IS NOT NULL")
    combos = db.q("SELECT odds, result, kind FROM combos WHERE result IS NOT NULL")
    n = len(rows)
    profit = sum((r["odds"] - 1) if r["result"] else -1 for r in rows)
    brier = sum((r["prob"] - r["result"]) ** 2 for r in rows) / n if n else None
    cprofit = sum((c["odds"] - 1) if c["result"] else -1 for c in combos)
    return {
        "picks": n, "aciertos": sum(r["result"] for r in rows),
        "roi_picks": profit / n if n else None, "brier": brier,
        "combinadas": len(combos), "combinadas_ganadas": sum(c["result"] for c in combos),
        "roi_combinadas": cprofit / len(combos) if combos else None,
    }
