"""Fuente principal: API-Football v3 (api-sports.io).

Endpoints usados:
  /fixtures?date=YYYY-MM-DD&timezone=...      partidos del día
  /fixtures?team=ID&last=N                    últimos partidos de un equipo (historial)
  /fixtures/statistics?fixture=ID             córners, tarjetas, tiros, remates, posesión, xG
  /fixtures/players?fixture=ID                remates y tiros al arco por jugador, minutos, tarjetas
  /odds?fixture=ID&bookmaker=ID               cuotas de mercados (1X2, goles, córners, tarjetas, BTTS...)
"""
from __future__ import annotations

import logging
import re
from typing import Any

from ..config import SETTINGS
from ..db import Database, now_iso
from .http import CachedClient

log = logging.getLogger(__name__)

FINISHED = {"FT", "AET", "PEN"}

# Nombre de estadística en API-Football -> columna propia
STAT_MAP = {
    "Corner Kicks": "corners",
    "Yellow Cards": "yellow",
    "Red Cards": "red",
    "Total Shots": "shots",
    "Shots on Goal": "shots_on",
    "Fouls": "fouls",
    "Ball Possession": "possession",
    "expected_goals": "xg",
}


def _num(value: Any) -> float | None:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    m = re.search(r"-?\d+(\.\d+)?", str(value))
    return float(m.group()) if m else None


class ApiFootball:
    def __init__(self, db: Database, key: str | None = None):
        key = key or SETTINGS.api_football_key
        if not key:
            raise RuntimeError("Falta API_FOOTBALL_KEY (ver .env.example)")
        self.db = db
        self.client = CachedClient(db, "https://v3.football.api-sports.io",
                                   headers={"x-apisports-key": key},
                                   budget=SETTINGS.request_budget,
                                   min_interval=SETTINGS.api_football_interval)

    def _get(self, path: str, params: dict, ttl: float = 3600) -> list[dict]:
        body = self.client.get(path, params, ttl)
        if body.get("errors"):
            log.warning("API-Football %s %s -> %s", path, params, body["errors"])
        return body.get("response", []) or []

    # ---------- fixtures ----------
    def fixtures_by_date(self, day: str, ttl: float = 900) -> list[dict]:
        return self._get("/fixtures", {"date": day, "timezone": SETTINGS.timezone}, ttl)

    def team_last_fixtures(self, team_id: int, last: int) -> list[dict]:
        return self._get("/fixtures", {"team": team_id, "last": last, "timezone": SETTINGS.timezone}, ttl=6 * 3600)

    def fixture_statistics(self, fixture_id: int) -> list[dict]:
        return self._get("/fixtures/statistics", {"fixture": fixture_id}, ttl=-1)

    def fixture_players(self, fixture_id: int) -> list[dict]:
        return self._get("/fixtures/players", {"fixture": fixture_id}, ttl=-1)

    def odds(self, fixture_id: int) -> list[dict]:
        return self._get("/odds", {"fixture": fixture_id, "bookmaker": SETTINGS.bookmaker_id}, ttl=1800)

    # ---------- persistencia ----------
    def store_fixture(self, fx: dict) -> dict:
        f, lg, t, g = fx["fixture"], fx["league"], fx["teams"], fx["goals"]
        row = {
            "fixture_id": f["id"],
            "date": f["date"][:10],
            "kickoff_utc": f.get("date"),
            "league_id": lg["id"],
            "league_name": lg.get("name"),
            "season": lg.get("season"),
            "round": lg.get("round"),
            "home_id": t["home"]["id"],
            "away_id": t["away"]["id"],
            "status": f["status"]["short"],
            "home_goals": g.get("home"),
            "away_goals": g.get("away"),
            "referee": (f.get("referee") or "").split(",")[0].strip() or None,
            "venue": (f.get("venue") or {}).get("name"),
        }
        existing = self.db.q("SELECT espn_id, validated, validation_notes FROM matches WHERE fixture_id=?", (f["id"],))
        if existing:
            row.update({k: existing[0][k] for k in ("espn_id", "validated", "validation_notes")})
        row["updated_at"] = now_iso()
        self.db.upsert("matches", row)
        for side in ("home", "away"):
            self.db.conn.execute(
                "INSERT OR IGNORE INTO teams (id, name, league_id, country, updated_at) VALUES (?,?,?,?,?)",
                (t[side]["id"], t[side]["name"], lg["id"], lg.get("country"), now_iso()),
            )
            self.db.conn.execute("UPDATE teams SET name=?, updated_at=? WHERE id=?",
                                 (t[side]["name"], now_iso(), t[side]["id"]))
        return row

    def parse_statistics(self, stats: list[dict]) -> dict[int, dict]:
        """-> {team_id: {corners, yellow, red, shots, shots_on, fouls, possession, xg}}"""
        out: dict[int, dict] = {}
        for block in stats:
            vals = {col: None for col in STAT_MAP.values()}
            for item in block.get("statistics", []):
                col = STAT_MAP.get(item.get("type"))
                if col:
                    vals[col] = _num(item.get("value"))
            # API-Football devuelve null en lugar de 0 cuando no hubo tarjetas/córners
            for col in ("corners", "yellow", "red", "shots", "shots_on", "fouls"):
                if vals[col] is None and block.get("statistics"):
                    vals[col] = 0.0
            out[block["team"]["id"]] = vals
        return out

    def store_finished_match(self, fx: dict, with_players: bool = True) -> bool:
        """Guarda resultado + estadísticas de equipo (y jugadores) de un partido terminado."""
        match = self.store_fixture(fx)
        if match["status"] not in FINISHED:
            return False
        fid = match["fixture_id"]
        stats = self.parse_statistics(self.fixture_statistics(fid))
        if len(stats) != 2:
            log.info("Partido %s sin estadísticas completas", fid)
            self.db.conn.commit()
            return False
        h, a = match["home_id"], match["away_id"]
        for team, opp, is_home in ((h, a, 1), (a, h, 0)):
            s, o = stats.get(team, {}), stats.get(opp, {})
            self.db.upsert("team_match_stats", {
                "fixture_id": fid, "team_id": team, "is_home": is_home,
                "goals": match["home_goals"] if is_home else match["away_goals"],
                "goals_against": match["away_goals"] if is_home else match["home_goals"],
                "corners": s.get("corners"), "corners_against": o.get("corners"),
                "yellow": s.get("yellow"), "red": s.get("red"),
                "yellow_against": o.get("yellow"), "red_against": o.get("red"),
                "shots": s.get("shots"), "shots_against": o.get("shots"),
                "shots_on": s.get("shots_on"), "shots_on_against": o.get("shots_on"),
                "fouls": s.get("fouls"), "possession": s.get("possession"), "xg": s.get("xg"),
            })
        if with_players:
            self.store_players(fid)
        self.db.conn.commit()
        return True

    def store_players(self, fixture_id: int) -> None:
        for team_block in self.fixture_players(fixture_id):
            team_id = team_block["team"]["id"]
            for p in team_block.get("players", []):
                st = (p.get("statistics") or [{}])[0]
                games, shots = st.get("games", {}) or {}, st.get("shots", {}) or {}
                goals, cards = st.get("goals", {}) or {}, st.get("cards", {}) or {}
                self.db.upsert("player_match_stats", {
                    "fixture_id": fixture_id, "player_id": p["player"]["id"], "team_id": team_id,
                    "name": p["player"]["name"], "position": games.get("position"),
                    "minutes": games.get("minutes") or 0,
                    "shots": shots.get("total") or 0, "shots_on": shots.get("on") or 0,
                    "goals": goals.get("total") or 0, "assists": goals.get("assists") or 0,
                    "yellow": cards.get("yellow") or 0, "red": cards.get("red") or 0,
                })

    # ---------- cuotas ----------
    def parse_odds(self, response: list[dict]) -> dict[tuple[str, str], float]:
        """Normaliza cuotas al formato (mercado, selección) que usa markets.py."""
        out: dict[tuple[str, str], float] = {}
        if not response:
            return out
        for bm in response[0].get("bookmakers", []):
            for bet in bm.get("bets", []):
                name = bet.get("name", "")
                for v in bet.get("values", []):
                    key = _map_odd(name, str(v.get("value")))
                    if key:
                        out.setdefault(key, float(v["odd"]))
        return out


def player_key(label: str, name: str) -> str:
    """Clave de cuota de jugador independiente de acentos/formato del nombre entre fuentes."""
    from ..validation import norm_name
    return f"{label} jugador#{norm_name(name)}"


def _map_odd(bet: str, value: str) -> tuple[str, str] | None:
    """Traduce nombres de mercado de API-Football a claves internas."""
    player_bets = {"Home Player Shots": "Remates", "Away Player Shots": "Remates",
                   "Home Player Shots On Target Total": "Tiros al arco",
                   "Away Player Shots On Target Total": "Tiros al arco"}
    if bet in player_bets:
        # valor "Nombre - N" = N o más; sin número = 1 o más
        m = re.match(r"(.+?)(?:\s+-\s+(\d+))?\s*$", value)
        n = int(m.group(2) or 1)
        return (player_key(player_bets[bet], m.group(1)), f"Más de {n - 0.5}")
    ou = re.match(r"(Over|Under)\s+([\d.]+)", value)
    if bet == "Match Winner":
        return ("1X2", {"Home": "1", "Draw": "X", "Away": "2"}.get(value, value))
    if bet == "Double Chance":
        return ("Doble oportunidad", {"Home/Draw": "1X", "Home/Away": "12", "Draw/Away": "X2"}.get(value, value))
    if bet == "Both Teams Score":
        return ("Ambos marcan", {"Yes": "Sí", "No": "No"}.get(value, value))
    if not ou:
        return None
    side = "Más de" if ou.group(1) == "Over" else "Menos de"
    sel = f"{side} {ou.group(2)}"
    mapping = {
        "Goals Over/Under": "Goles totales",
        "Total - Home": "Goles local",
        "Total - Away": "Goles visitante",
        "Corners Over Under": "Córners totales",
        "Home Corners Over/Under": "Córners local",
        "Away Corners Over/Under": "Córners visitante",
        "Cards Over/Under": "Tarjetas totales",
        "Home Team Total Cards": "Tarjetas local",
        "Away Team Total Cards": "Tarjetas visitante",
        "Total ShotOnGoal": "Tiros al arco totales",
        "Home Team Total ShotOnGoal": "Tiros al arco local",
        "Away Team Total ShotOnGoal": "Tiros al arco visitante",
        "Total Shots": "Remates totales",
    }
    market = mapping.get(bet)
    return (market, sel) if market else None
