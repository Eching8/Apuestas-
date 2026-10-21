"""Fuente secundaria (pública, sin clave): ESPN. Se usa para validar resultados y estadísticas.

  /apis/site/v2/sports/soccer/{liga}/scoreboard?dates=YYYYMMDD
  /apis/site/v2/sports/soccer/{liga}/summary?event=ID
"""
from __future__ import annotations

import logging
from typing import Any

from ..db import Database
from .http import CachedClient

log = logging.getLogger(__name__)

ESPN_STAT_MAP = {
    "wonCorners": "corners",
    "yellowCards": "yellow",
    "redCards": "red",
    "totalShots": "shots",
    "shotsOnTarget": "shots_on",
    "foulsCommitted": "fouls",
    "possessionPct": "possession",
}


class Espn:
    def __init__(self, db: Database):
        self.client = CachedClient(db, "https://site.api.espn.com/apis/site/v2/sports/soccer",
                                   min_interval=0.2)

    def scoreboard(self, league_code: str, day: str) -> list[dict]:
        body = self.client.get(f"/{league_code}/scoreboard", {"dates": day.replace("-", "")}, ttl=900)
        events = []
        for ev in body.get("events", []):
            comp = (ev.get("competitions") or [{}])[0]
            teams = {c.get("homeAway"): c for c in comp.get("competitors", [])}
            if "home" not in teams or "away" not in teams:
                continue
            events.append({
                "id": ev["id"],
                "date": ev.get("date"),
                "completed": ev.get("status", {}).get("type", {}).get("completed", False),
                "home": teams["home"]["team"].get("displayName"),
                "away": teams["away"]["team"].get("displayName"),
                "home_goals": _int(teams["home"].get("score")),
                "away_goals": _int(teams["away"].get("score")),
            })
        return events

    def match_stats(self, league_code: str, event_id: str) -> dict[str, dict[str, Any]]:
        """-> {'home': {...}, 'away': {...}} con las mismas columnas que API-Football."""
        body = self.client.get(f"/{league_code}/summary", {"event": event_id}, ttl=-1)
        out: dict[str, dict] = {}
        comp = ((body.get("header") or {}).get("competitions") or [{}])[0]
        side_by_team = {c["team"]["id"]: c.get("homeAway") for c in comp.get("competitors", []) if "team" in c}
        for t in (body.get("boxscore") or {}).get("teams", []):
            side = side_by_team.get(t["team"]["id"]) or t.get("homeAway")
            vals = {}
            for s in t.get("statistics", []):
                col = ESPN_STAT_MAP.get(s.get("name"))
                if col:
                    vals[col] = _float(s.get("displayValue"))
            if side:
                out[side] = vals
        return out


def _int(v: Any) -> int | None:
    try:
        return int(v)
    except (TypeError, ValueError):
        return None


def _float(v: Any) -> float | None:
    try:
        return float(str(v).replace("%", ""))
    except (TypeError, ValueError):
        return None
