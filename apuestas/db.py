"""Base de datos SQLite: equipos, partidos, estadísticas por equipo y jugador, cuotas y picks."""
from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS teams (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    country TEXT
);

CREATE TABLE IF NOT EXISTS leagues (
    id INTEGER NOT NULL,
    season INTEGER NOT NULL,
    name TEXT,
    country TEXT,
    PRIMARY KEY (id, season)
);

CREATE TABLE IF NOT EXISTS fixtures (
    id INTEGER PRIMARY KEY,
    date_utc TEXT NOT NULL,
    fecha_local TEXT NOT NULL,
    league_id INTEGER,
    season INTEGER,
    home_id INTEGER NOT NULL REFERENCES teams(id),
    away_id INTEGER NOT NULL REFERENCES teams(id),
    status TEXT,
    home_goals INTEGER,
    away_goals INTEGER,
    stats_ok INTEGER NOT NULL DEFAULT 0,
    players_ok INTEGER NOT NULL DEFAULT 0,
    updated_at TEXT
);
CREATE INDEX IF NOT EXISTS ix_fixtures_fecha ON fixtures(fecha_local);
CREATE INDEX IF NOT EXISTS ix_fixtures_home ON fixtures(home_id);
CREATE INDEX IF NOT EXISTS ix_fixtures_away ON fixtures(away_id);

-- Una fila por equipo y partido: lo que hizo el equipo y lo que recibió.
CREATE TABLE IF NOT EXISTS team_stats (
    fixture_id INTEGER NOT NULL REFERENCES fixtures(id),
    team_id INTEGER NOT NULL REFERENCES teams(id),
    opponent_id INTEGER NOT NULL,
    is_home INTEGER NOT NULL,
    goals INTEGER,
    corners INTEGER,
    yellow INTEGER,
    red INTEGER,
    cards INTEGER,
    shots_on INTEGER,
    shots_total INTEGER,
    fouls INTEGER,
    possession REAL,
    xg REAL,
    PRIMARY KEY (fixture_id, team_id)
);
CREATE INDEX IF NOT EXISTS ix_team_stats_team ON team_stats(team_id);

CREATE TABLE IF NOT EXISTS player_stats (
    fixture_id INTEGER NOT NULL REFERENCES fixtures(id),
    player_id INTEGER NOT NULL,
    team_id INTEGER NOT NULL,
    name TEXT,
    position TEXT,
    minutes INTEGER,
    goals INTEGER,
    assists INTEGER,
    shots_on INTEGER,
    shots_total INTEGER,
    yellow INTEGER,
    red INTEGER,
    PRIMARY KEY (fixture_id, player_id)
);
CREATE INDEX IF NOT EXISTS ix_player_stats_player ON player_stats(player_id);
CREATE INDEX IF NOT EXISTS ix_player_stats_team ON player_stats(team_id);

CREATE TABLE IF NOT EXISTS odds (
    fixture_id INTEGER NOT NULL,
    bookmaker TEXT NOT NULL,
    bet TEXT NOT NULL,
    value TEXT NOT NULL,
    odd REAL NOT NULL,
    fetched_at TEXT NOT NULL,
    PRIMARY KEY (fixture_id, bookmaker, bet, value)
);

CREATE TABLE IF NOT EXISTS combos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT NOT NULL,
    perfil TEXT NOT NULL,
    prob REAL NOT NULL,
    odd REAL,
    ev REAL,
    result INTEGER,
    created_at TEXT NOT NULL
);

-- Selecciones recomendadas (sueltas con combo_id NULL, o parte de una combinada).
CREATE TABLE IF NOT EXISTS picks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT NOT NULL,
    fixture_id INTEGER NOT NULL,
    market_key TEXT NOT NULL,
    label TEXT NOT NULL,
    prob REAL NOT NULL,
    odd REAL,
    edge REAL,
    combo_id INTEGER REFERENCES combos(id),
    result INTEGER,
    created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_picks_fixture ON picks(fixture_id);

CREATE TABLE IF NOT EXISTS validations (
    fixture_id INTEGER NOT NULL,
    source TEXT NOT NULL,
    ok INTEGER NOT NULL,
    detail TEXT,
    checked_at TEXT NOT NULL,
    PRIMARY KEY (fixture_id, source)
);
"""


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class Database:
    def __init__(self, path: Path | str):
        self.path = str(path)
        if self.path != ":memory:":
            Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.path)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.conn.executescript(SCHEMA)

    @contextmanager
    def tx(self):
        try:
            yield self.conn
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise

    def close(self) -> None:
        self.conn.close()

    # --- Escritura ----------------------------------------------------------------

    def upsert_team(self, team_id: int, name: str, country: str | None = None) -> None:
        self.conn.execute(
            "INSERT INTO teams(id, name, country) VALUES (?, ?, ?) "
            "ON CONFLICT(id) DO UPDATE SET name = excluded.name, country = COALESCE(excluded.country, teams.country)",
            (team_id, name, country),
        )

    def upsert_league(self, league_id: int, season: int, name: str, country: str | None) -> None:
        self.conn.execute(
            "INSERT OR REPLACE INTO leagues(id, season, name, country) VALUES (?, ?, ?, ?)",
            (league_id, season, name, country),
        )

    def upsert_fixture(self, f: dict) -> None:
        self.conn.execute(
            """INSERT INTO fixtures(id, date_utc, fecha_local, league_id, season, home_id, away_id, status,
                                    home_goals, away_goals, updated_at)
               VALUES (:id, :date_utc, :fecha_local, :league_id, :season, :home_id, :away_id, :status,
                       :home_goals, :away_goals, :updated_at)
               ON CONFLICT(id) DO UPDATE SET
                   date_utc = excluded.date_utc, fecha_local = excluded.fecha_local, status = excluded.status,
                   home_goals = excluded.home_goals, away_goals = excluded.away_goals,
                   updated_at = excluded.updated_at""",
            {**f, "updated_at": now_iso()},
        )

    def save_team_stats(self, rows: list[dict]) -> None:
        self.conn.executemany(
            """INSERT OR REPLACE INTO team_stats(fixture_id, team_id, opponent_id, is_home, goals, corners, yellow,
                   red, cards, shots_on, shots_total, fouls, possession, xg)
               VALUES (:fixture_id, :team_id, :opponent_id, :is_home, :goals, :corners, :yellow, :red, :cards,
                       :shots_on, :shots_total, :fouls, :possession, :xg)""",
            rows,
        )

    def save_player_stats(self, rows: list[dict]) -> None:
        self.conn.executemany(
            """INSERT OR REPLACE INTO player_stats(fixture_id, player_id, team_id, name, position, minutes, goals,
                   assists, shots_on, shots_total, yellow, red)
               VALUES (:fixture_id, :player_id, :team_id, :name, :position, :minutes, :goals, :assists,
                       :shots_on, :shots_total, :yellow, :red)""",
            rows,
        )

    def mark_fixture(self, fixture_id: int, stats_ok: int | None = None, players_ok: int | None = None) -> None:
        """1 = datos guardados, -1 = la API no tiene cobertura para ese partido."""
        if stats_ok is not None:
            self.conn.execute("UPDATE fixtures SET stats_ok = ? WHERE id = ?", (int(stats_ok), fixture_id))
        if players_ok is not None:
            self.conn.execute("UPDATE fixtures SET players_ok = ? WHERE id = ?", (int(players_ok), fixture_id))

    def save_odds(self, fixture_id: int, rows: list[tuple[str, str, str, float]]) -> None:
        ts = now_iso()
        self.conn.execute("DELETE FROM odds WHERE fixture_id = ?", (fixture_id,))
        self.conn.executemany(
            "INSERT OR REPLACE INTO odds(fixture_id, bookmaker, bet, value, odd, fetched_at) VALUES (?, ?, ?, ?, ?, ?)",
            [(fixture_id, b, bet, v, o, ts) for b, bet, v, o in rows],
        )

    def save_validation(self, fixture_id: int, source: str, ok: bool, detail: str) -> None:
        self.conn.execute(
            "INSERT OR REPLACE INTO validations(fixture_id, source, ok, detail, checked_at) VALUES (?, ?, ?, ?, ?)",
            (fixture_id, source, int(ok), detail, now_iso()),
        )

    # --- Lectura ------------------------------------------------------------------

    def fixture(self, fixture_id: int) -> sqlite3.Row | None:
        return self.conn.execute(
            """SELECT f.*, h.name AS home_name, a.name AS away_name, l.name AS league_name, l.country AS league_country
               FROM fixtures f JOIN teams h ON h.id = f.home_id JOIN teams a ON a.id = f.away_id
               LEFT JOIN leagues l ON l.id = f.league_id AND l.season = f.season
               WHERE f.id = ?""",
            (fixture_id,),
        ).fetchone()

    def fixtures_on(self, fecha_local: str) -> list[sqlite3.Row]:
        return self.conn.execute(
            """SELECT f.*, h.name AS home_name, a.name AS away_name, l.name AS league_name, l.country AS league_country
               FROM fixtures f JOIN teams h ON h.id = f.home_id JOIN teams a ON a.id = f.away_id
               LEFT JOIN leagues l ON l.id = f.league_id AND l.season = f.season
               WHERE f.fecha_local = ? ORDER BY f.date_utc""",
            (fecha_local,),
        ).fetchall()

    def has_stats(self, fixture_id: int) -> tuple[int, int]:
        row = self.conn.execute("SELECT stats_ok, players_ok FROM fixtures WHERE id = ?", (fixture_id,)).fetchone()
        return (row["stats_ok"], row["players_ok"]) if row else (0, 0)

    def team_history(self, team_id: int, before_utc: str, limit: int) -> list[sqlite3.Row]:
        """Partidos terminados del equipo antes de una fecha, con lo hecho y lo recibido."""
        return self.conn.execute(
            """SELECT f.id AS fixture_id, f.date_utc, f.league_id, t.is_home,
                      t.goals, t.corners, t.cards, t.yellow, t.red, t.shots_on, t.shots_total, t.xg,
                      o.goals AS goals_against, o.corners AS corners_against, o.cards AS cards_against,
                      o.shots_on AS shots_on_against, o.shots_total AS shots_total_against
               FROM team_stats t
               JOIN team_stats o ON o.fixture_id = t.fixture_id AND o.team_id = t.opponent_id
               JOIN fixtures f ON f.id = t.fixture_id
               WHERE t.team_id = ? AND f.date_utc < ? AND f.stats_ok = 1
               ORDER BY f.date_utc DESC LIMIT ?""",
            (team_id, before_utc, limit),
        ).fetchall()

    def league_means(self, league_id: int | None, before_utc: str) -> dict[str, float] | None:
        """Promedio por equipo y partido de cada estadística en la liga (o global si no hay liga)."""
        where = "f.stats_ok = 1 AND f.date_utc < ?"
        params: list = [before_utc]
        if league_id is not None:
            where += " AND f.league_id = ?"
            params.append(league_id)
        row = self.conn.execute(
            f"""SELECT COUNT(*) AS n, AVG(t.goals) AS goals, AVG(t.corners) AS corners, AVG(t.cards) AS cards,
                       AVG(t.shots_on) AS shots_on, AVG(t.shots_total) AS shots_total
                FROM team_stats t JOIN fixtures f ON f.id = t.fixture_id WHERE {where}""",
            params,
        ).fetchone()
        if not row or row["n"] < 20:
            return None
        return {k: row[k] for k in ("goals", "corners", "cards", "shots_on", "shots_total") if row[k] is not None}

    def player_history(self, team_id: int, before_utc: str, partidos: int) -> list[sqlite3.Row]:
        """Estadísticas de jugadores del equipo en sus últimos `partidos` partidos con datos."""
        return self.conn.execute(
            """SELECT p.* FROM player_stats p JOIN fixtures f ON f.id = p.fixture_id
               WHERE p.team_id = ? AND f.players_ok = 1 AND f.date_utc < ?
                 AND p.fixture_id IN (
                     SELECT f2.id FROM fixtures f2 JOIN player_stats p2 ON p2.fixture_id = f2.id
                     WHERE p2.team_id = ? AND f2.players_ok = 1 AND f2.date_utc < ?
                     GROUP BY f2.id ORDER BY f2.date_utc DESC LIMIT ?)
               ORDER BY f.date_utc DESC""",
            (team_id, before_utc, team_id, before_utc, partidos),
        ).fetchall()

    def odds_for(self, fixture_id: int) -> list[sqlite3.Row]:
        return self.conn.execute("SELECT * FROM odds WHERE fixture_id = ?", (fixture_id,)).fetchall()

    def match_totals(self, fixture_id: int) -> dict | None:
        rows = self.conn.execute(
            "SELECT t.* FROM team_stats t WHERE t.fixture_id = ? ORDER BY t.is_home DESC", (fixture_id,)
        ).fetchall()
        if len(rows) != 2:
            return None
        return {"home": dict(rows[0]), "away": dict(rows[1])}

    def player_line(self, fixture_id: int, player_id: int) -> sqlite3.Row | None:
        return self.conn.execute(
            "SELECT * FROM player_stats WHERE fixture_id = ? AND player_id = ?", (fixture_id, player_id)
        ).fetchone()
