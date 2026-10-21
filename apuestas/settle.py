"""Liquida las selecciones guardadas con los resultados reales, para medir el acierto del modelo."""
from __future__ import annotations

from .db import Database


def evaluate(key: str, totals: dict, player_row=None) -> bool | None:
    """Resultado de un mercado dado el partido terminado. None si no se puede decidir."""
    h, a = totals["home"], totals["away"]
    parts = key.split(":")
    kind = parts[0]
    if kind == "result":
        diff = h["goals"] - a["goals"]
        return {"1": diff > 0, "X": diff == 0, "2": diff < 0}[parts[1]]
    if kind == "dc":
        diff = h["goals"] - a["goals"]
        return {"1X": diff >= 0, "X2": diff <= 0, "12": diff != 0}[parts[1]]
    if kind == "btts":
        both = h["goals"] > 0 and a["goals"] > 0
        return both if parts[1] == "yes" else not both
    if kind == "player":
        _, _pid, stat, side, line = parts
        if player_row is None:
            return None  # no jugó: la mayoría de casas anulan la apuesta
        value = player_row[stat]
    else:
        stat, scope, side, line = parts
        if h[stat] is None or a[stat] is None:
            return None
        value = {"total": h[stat] + a[stat], "home": h[stat], "away": a[stat]}[scope]
    line = float(line)
    return value > line if side == "over" else value < line


def settle_pending(db: Database) -> int:
    pending = db.conn.execute(
        """SELECT p.id, p.fixture_id, p.market_key FROM picks p JOIN fixtures f ON f.id = p.fixture_id
           WHERE p.result IS NULL AND f.stats_ok = 1"""
    ).fetchall()
    n = 0
    with db.tx():
        for p in pending:
            totals = db.match_totals(p["fixture_id"])
            if not totals:
                continue
            player_row = None
            if p["market_key"].startswith("player:"):
                player_row = db.player_line(p["fixture_id"], int(p["market_key"].split(":")[1]))
            res = evaluate(p["market_key"], totals, player_row)
            if res is not None:
                db.conn.execute("UPDATE picks SET result = ? WHERE id = ?", (int(res), p["id"]))
                n += 1
        # Una combinada se gana si todas sus selecciones se ganan.
        db.conn.execute(
            """UPDATE combos SET result = CASE
                   WHEN EXISTS (SELECT 1 FROM picks WHERE combo_id = combos.id AND result = 0) THEN 0
                   WHEN NOT EXISTS (SELECT 1 FROM picks WHERE combo_id = combos.id AND result IS NULL) THEN 1
               END
               WHERE result IS NULL"""
        )
    return n


def summary(db: Database) -> dict:
    """Acierto y rendimiento (apostando 1 unidad) de las selecciones y combinadas liquidadas."""
    singles = db.conn.execute(
        """SELECT substr(market_key, 1, instr(market_key || ':', ':') - 1) AS tipo, COUNT(*) AS n,
                  AVG(result) AS acierto, AVG(prob) AS prob_media,
                  SUM(CASE WHEN odd IS NOT NULL THEN (CASE WHEN result = 1 THEN odd - 1 ELSE -1 END) END) AS beneficio,
                  SUM(CASE WHEN odd IS NOT NULL THEN 1 ELSE 0 END) AS con_cuota
           FROM picks WHERE combo_id IS NULL AND result IS NOT NULL GROUP BY tipo ORDER BY n DESC"""
    ).fetchall()
    combos = db.conn.execute(
        """SELECT perfil, COUNT(*) AS n, AVG(result) AS acierto, AVG(prob) AS prob_media,
                  SUM(CASE WHEN odd IS NOT NULL THEN (CASE WHEN result = 1 THEN odd - 1 ELSE -1 END) END) AS beneficio
           FROM combos WHERE result IS NOT NULL GROUP BY perfil"""
    ).fetchall()
    return {"selecciones": [dict(r) for r in singles], "combinadas": [dict(r) for r in combos]}
