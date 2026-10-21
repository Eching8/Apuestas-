"""Base de datos SQLite: equipos, partidos, estadísticas por equipo/jugador, predicciones y combinadas."""
from __future__ import annotations

import json
import sqlite3
import time
from contextlib import contextmanager
from typing import Any, Iterable

SCHEMA = """
CREATE TABLE IF NOT EXISTS teams (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    country TEXT,
    league_id INTEGER,
    updated_at TEXT
);
CREATE TABLE IF NOT EXISTS matches (
    fixture_id INTEGER PRIMARY KEY,
    date TEXT NOT NULL,               -- YYYY-MM-DD (zona horaria configurada)
    kickoff_utc TEXT,
    league_id INTEGER,
    league_name TEXT,
    season INTEGER,
    round TEXT,
    home_id INTEGER, away_id INTEGER,
    status TEXT,                      -- NS, FT, AET, PEN, PST, ...
    home_goals INTEGER, away_goals INTEGER,
    referee TEXT,
    venue TEXT,
    espn_id TEXT,
    validated INTEGER DEFAULT 0,      -- 1 = coincide con fuente secundaria, -1 = discrepancia, 0 = sin validar
    validation_notes TEXT,
    updated_at TEXT
);
CREATE INDEX IF NOT EXISTS ix_matches_date ON matches(date);
CREATE INDEX IF NOT EXISTS ix_matches_home ON matches(home_id);
CREATE INDEX IF NOT EXISTS ix_matches_away ON matches(away_id);

CREATE TABLE IF NOT EXISTS team_match_stats (
    fixture_id INTEGER, team_id INTEGER, is_home INTEGER,
    goals INTEGER, goals_against INTEGER,
    corners INTEGER, corners_against INTEGER,
    yellow INTEGER, red INTEGER, yellow_against INTEGER, red_against INTEGER,
    shots INTEGER, shots_against INTEGER,
    shots_on INTEGER, shots_on_against INTEGER,
    fouls INTEGER, possession REAL, xg REAL,
    PRIMARY KEY (fixture_id, team_id)
);
CREATE INDEX IF NOT EXISTS ix_tms_team ON team_match_stats(team_id);

CREATE TABLE IF NOT EXISTS player_match_stats (
    fixture_id INTEGER, player_id INTEGER, team_id INTEGER,
    name TEXT, position TEXT, minutes INTEGER,
    shots INTEGER, shots_on INTEGER, goals INTEGER, assists INTEGER,
    yellow INTEGER, red INTEGER,
    PRIMARY KEY (fixture_id, player_id)
);
CREATE INDEX IF NOT EXISTS ix_pms_team ON player_match_stats(team_id);

CREATE TABLE IF NOT EXISTS validations (
    fixture_id INTEGER, stat TEXT, team_side TEXT,
    primary_value REAL, secondary_value REAL, ok INTEGER,
    checked_at TEXT,
    PRIMARY KEY (fixture_id, stat, team_side)
);

CREATE TABLE IF NOT EXISTS predictions (
    fixture_id INTEGER, date TEXT,
    market TEXT, selection TEXT,
    prob REAL, fair_odds REAL, odds REAL, ev REAL,
    confidence TEXT,
    result INTEGER,                   -- NULL pendiente, 1 ganada, 0 perdida
    created_at TEXT,
    PRIMARY KEY (fixture_id, market, selection)
);

CREATE TABLE IF NOT EXISTS combos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT, kind TEXT,
    legs TEXT,                        -- JSON con las selecciones
    prob REAL, odds REAL, ev REAL,
    result INTEGER,
    created_at TEXT
);

CREATE TABLE IF NOT EXISTS team_ratings (
    date TEXT, team_id INTEGER, stat TEXT,
    attack REAL, defense REAL,        -- índices relativos a la media de la liga (1.0 = promedio)
    avg_for REAL, avg_against REAL,   -- promedios reales de los últimos partidos
    sample INTEGER, form TEXT,
    PRIMARY KEY (date, team_id, stat)
);

CREATE TABLE IF NOT EXISTS api_cache (
    key TEXT PRIMARY KEY, body TEXT, fetched_at REAL
);
"""


def now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S")


class Database:
    def __init__(self, path: str):
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA)
        self.conn.commit()

    @contextmanager
    def tx(self):
        try:
            yield self.conn
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise

    def q(self, sql: str, params: Iterable[Any] = ()) -> list[sqlite3.Row]:
        return self.conn.execute(sql, tuple(params)).fetchall()

    def upsert(self, table: str, row: dict[str, Any]) -> None:
        cols = ", ".join(row)
        marks = ", ".join("?" for _ in row)
        self.conn.execute(f"INSERT OR REPLACE INTO {table} ({cols}) VALUES ({marks})", tuple(row.values()))

    # ---- caché de peticiones HTTP ----
    def cache_get(self, key: str, ttl: float) -> Any | None:
        row = self.conn.execute("SELECT body, fetched_at FROM api_cache WHERE key=?", (key,)).fetchone()
        if row and (ttl < 0 or time.time() - row["fetched_at"] < ttl):
            return json.loads(row["body"])
        return None

    def cache_put(self, key: str, body: Any) -> None:
        self.conn.execute("INSERT OR REPLACE INTO api_cache VALUES (?,?,?)", (key, json.dumps(body), time.time()))
        self.conn.commit()

    # ---- consultas de historial ----
    def team_history(self, team_id: int, before_date: str, limit: int) -> list[sqlite3.Row]:
        return self.q(
            """SELECT s.*, m.date, m.league_id, m.referee FROM team_match_stats s
               JOIN matches m ON m.fixture_id = s.fixture_id
               WHERE s.team_id=? AND m.date < ? AND m.status IN ('FT','AET','PEN')
               ORDER BY m.date DESC LIMIT ?""",
            (team_id, before_date, limit),
        )

    def league_averages(self, league_id: int, before_date: str, limit: int = 400) -> list[sqlite3.Row]:
        return self.q(
            """SELECT s.* FROM team_match_stats s JOIN matches m ON m.fixture_id = s.fixture_id
               WHERE m.league_id=? AND m.date < ? AND m.status IN ('FT','AET','PEN')
               ORDER BY m.date DESC LIMIT ?""",
            (league_id, before_date, limit),
        )

    def all_averages(self, before_date: str, limit: int = 2000) -> list[sqlite3.Row]:
        return self.q(
            """SELECT s.* FROM team_match_stats s JOIN matches m ON m.fixture_id = s.fixture_id
               WHERE m.date < ? AND m.status IN ('FT','AET','PEN') ORDER BY m.date DESC LIMIT ?""",
            (before_date, limit),
        )

    def player_history(self, team_id: int, before_date: str, matches: int = 10) -> list[sqlite3.Row]:
        return self.q(
            """SELECT p.* FROM player_match_stats p JOIN matches m ON m.fixture_id = p.fixture_id
               WHERE p.team_id=? AND m.date < ? AND p.fixture_id IN (
                   SELECT s.fixture_id FROM team_match_stats s JOIN matches mm ON mm.fixture_id=s.fixture_id
                   WHERE s.team_id=? AND mm.date < ? ORDER BY mm.date DESC LIMIT ?)""",
            (team_id, before_date, team_id, before_date, matches),
        )

    def referee_history(self, referee: str, before_date: str, limit: int = 30) -> list[sqlite3.Row]:
        return self.q(
            """SELECT m.fixture_id, SUM(s.yellow) AS yellow, SUM(s.red) AS red FROM matches m
               JOIN team_match_stats s ON s.fixture_id = m.fixture_id
               WHERE m.referee=? AND m.date < ? AND m.status IN ('FT','AET','PEN')
               GROUP BY m.fixture_id ORDER BY m.date DESC LIMIT ?""",
            (referee, before_date, limit),
        )

    def match_count(self, team_id: int) -> int:
        row = self.conn.execute(
            """SELECT COUNT(*) FROM team_match_stats s JOIN matches m ON m.fixture_id=s.fixture_id
               WHERE s.team_id=? AND m.status IN ('FT','AET','PEN') AND s.corners IS NOT NULL""",
            (team_id,),
        ).fetchone()
        return row[0]
