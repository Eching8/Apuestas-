"""Tablas de la NBA dentro de la misma base SQLite (prefijo nba_)."""
from __future__ import annotations

import sqlite3

from ..db import now_iso

SCHEMA = """
CREATE TABLE IF NOT EXISTS nba_teams (
    id TEXT PRIMARY KEY,
    abbr TEXT,
    name TEXT,
    nickname TEXT
);

CREATE TABLE IF NOT EXISTS nba_games (
    id TEXT PRIMARY KEY,
    date_utc TEXT NOT NULL,
    fecha TEXT NOT NULL,
    season INTEGER,
    season_type INTEGER,
    home_id TEXT NOT NULL,
    away_id TEXT NOT NULL,
    status TEXT,
    home_pts INTEGER,
    away_pts INTEGER,
    box_ok INTEGER NOT NULL DEFAULT 0,
    updated_at TEXT
);
CREATE INDEX IF NOT EXISTS ix_nba_games_fecha ON nba_games(fecha);

-- Una fila por jugador que jugó en el partido. Quien no aparece no jugó.
CREATE TABLE IF NOT EXISTS nba_player_games (
    game_id TEXT NOT NULL REFERENCES nba_games(id),
    player_id TEXT NOT NULL,
    team_id TEXT NOT NULL,
    opp_id TEXT NOT NULL,
    is_home INTEGER NOT NULL,
    name TEXT,
    position TEXT,
    starter INTEGER,
    minutes REAL NOT NULL,
    pts INTEGER, fgm INTEGER, fga INTEGER, tpm INTEGER, tpa INTEGER, ftm INTEGER, fta INTEGER,
    reb INTEGER, oreb INTEGER, dreb INTEGER, ast INTEGER, stl INTEGER, blk INTEGER, tov INTEGER, pf INTEGER,
    PRIMARY KEY (game_id, player_id)
);
CREATE INDEX IF NOT EXISTS ix_nba_pg_player ON nba_player_games(player_id);
CREATE INDEX IF NOT EXISTS ix_nba_pg_opp ON nba_player_games(opp_id);

CREATE TABLE IF NOT EXISTS nba_shots (
    game_id TEXT NOT NULL REFERENCES nba_games(id),
    seq INTEGER NOT NULL,
    player_id TEXT NOT NULL,
    team_id TEXT NOT NULL,
    opp_id TEXT,
    period INTEGER,
    x REAL, y REAL, dist REAL,
    zone TEXT NOT NULL,
    value INTEGER NOT NULL,
    made INTEGER NOT NULL,
    assisted INTEGER NOT NULL,
    PRIMARY KEY (game_id, seq)
);
CREATE INDEX IF NOT EXISTS ix_nba_shots_player ON nba_shots(player_id);
CREATE INDEX IF NOT EXISTS ix_nba_shots_opp ON nba_shots(opp_id);

CREATE TABLE IF NOT EXISTS nba_injuries (
    fecha TEXT NOT NULL,
    team_id TEXT NOT NULL,
    player_id TEXT NOT NULL,
    name TEXT,
    status TEXT,
    detail TEXT,
    PRIMARY KEY (fecha, player_id)
);

-- Línea de consenso de SportsGameOdds por jugador y estadística (partido completo).
CREATE TABLE IF NOT EXISTS nba_props (
    fecha TEXT NOT NULL,
    game_id TEXT NOT NULL,
    player_id TEXT NOT NULL,
    stat TEXT NOT NULL,
    line REAL NOT NULL,
    over_odd REAL,
    under_odd REAL,
    books INTEGER,
    fetched_at TEXT NOT NULL,
    PRIMARY KEY (fecha, game_id, player_id, stat)
);

-- Totales de cada equipo por partido (suma de sus jugadores): base de los fallos, canastas y pérdidas
-- esperados de cada partido.
CREATE VIEW IF NOT EXISTS nba_team_games AS
SELECT game_id, team_id, opp_id, is_home, SUM(minutes) AS minutes, SUM(pts) AS pts, SUM(fgm) AS fgm,
       SUM(fga) AS fga, SUM(tpm) AS tpm, SUM(tpa) AS tpa, SUM(ftm) AS ftm, SUM(fta) AS fta, SUM(oreb) AS oreb,
       SUM(dreb) AS dreb, SUM(reb) AS reb, SUM(ast) AS ast, SUM(stl) AS stl, SUM(blk) AS blk, SUM(tov) AS tov
FROM nba_player_games GROUP BY game_id, team_id;

-- Cada prop evaluada con todo su análisis: de dónde sale la media (componentes) y las estadísticas
-- relacionadas en sus últimos 5 y 10 partidos, la temporada, la anterior y contra este rival (JSON).
CREATE TABLE IF NOT EXISTS nba_analisis (
    fecha TEXT NOT NULL,
    game_id TEXT NOT NULL,
    player_id TEXT NOT NULL,
    name TEXT,
    stat TEXT NOT NULL,
    line REAL NOT NULL,
    side TEXT NOT NULL,
    prob REAL NOT NULL,
    prob_modelo REAL,
    prob_mercado REAL,
    mu REAL,
    sd REAL,
    odd REAL,
    detalle TEXT NOT NULL,
    created_at TEXT NOT NULL,
    PRIMARY KEY (fecha, game_id, player_id, stat)
);

-- stats.nba.com: quién defendió a quién. Una fila por atacante y defensor en cada partido, con los
-- ids de la NBA y, emparejados por nombre, los de ESPN (player_id) que usa el resto de la base.
CREATE TABLE IF NOT EXISTS nba_matchups (
    nba_game_id TEXT NOT NULL,
    game_id TEXT,
    off_nba_id INTEGER NOT NULL,
    def_nba_id INTEGER NOT NULL,
    off_player_id TEXT,
    def_player_id TEXT,
    off_team_id TEXT,
    def_team_id TEXT,
    off_name TEXT,
    def_name TEXT,
    minutos REAL, posesiones REAL, pts REAL, fgm INTEGER, fga INTEGER, tpm INTEGER, tpa INTEGER, ftm INTEGER,
    ast INTEGER, tov INTEGER, blk INTEGER,
    PRIMARY KEY (nba_game_id, off_nba_id, def_nba_id)
);
CREATE INDEX IF NOT EXISTS ix_nba_matchups_off ON nba_matchups(off_player_id);
CREATE INDEX IF NOT EXISTS ix_nba_matchups_def ON nba_matchups(def_player_id);

-- Partidos de stats.nba.com ya descargados y su partido de ESPN.
CREATE TABLE IF NOT EXISTS nba_stats_games (
    nba_game_id TEXT PRIMARY KEY,
    fecha TEXT NOT NULL,
    season INTEGER,
    season_type INTEGER,
    game_id TEXT,
    filas INTEGER NOT NULL DEFAULT 0,
    updated_at TEXT
);

-- Estadísticas avanzadas de temporada (uso, % de rebotes y asistencias, true shooting...).
CREATE TABLE IF NOT EXISTS nba_avanzadas (
    season INTEGER NOT NULL,
    season_type INTEGER NOT NULL,
    nba_id INTEGER NOT NULL,
    player_id TEXT,
    name TEXT,
    team_abbr TEXT,
    gp INTEGER, minutos REAL, usg_pct REAL, ts_pct REAL, ast_pct REAL, oreb_pct REAL, dreb_pct REAL,
    reb_pct REAL, tov_pct REAL, pace REAL, pie REAL,
    PRIMARY KEY (season, season_type, nba_id)
);

-- Combinadas del día (de prueba hasta que el sistema esté calibrado): patas en JSON.
CREATE TABLE IF NOT EXISTS nba_combinadas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT NOT NULL,
    tipo TEXT NOT NULL,
    patas TEXT NOT NULL,
    prob REAL NOT NULL,
    cuota REAL,
    cuota_final REAL,
    aciertos INTEGER,
    result INTEGER,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS nba_picks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT NOT NULL,
    game_id TEXT NOT NULL,
    player_id TEXT NOT NULL,
    name TEXT,
    stat TEXT NOT NULL,
    line REAL NOT NULL,
    side TEXT NOT NULL,
    prob REAL NOT NULL,
    mu REAL,
    odd REAL,
    actual REAL,
    result INTEGER,
    tipo TEXT NOT NULL DEFAULT 'prop',
    created_at TEXT NOT NULL,
    UNIQUE (fecha, game_id, player_id, stat, side, line)
);
"""


class NbaDB:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn
        self.conn.executescript(SCHEMA)
        # Bases creadas antes de existir la columna (p. ej. la caché de GitHub Actions).
        columnas = {r[1] for r in self.conn.execute("PRAGMA table_info(nba_picks)")}
        if "tipo" not in columnas:
            self.conn.execute("ALTER TABLE nba_picks ADD COLUMN tipo TEXT NOT NULL DEFAULT 'prop'")

    def commit(self) -> None:
        self.conn.commit()

    # --- Escritura ----------------------------------------------------------------

    def upsert_team(self, t: dict) -> None:
        self.conn.execute(
            "INSERT OR REPLACE INTO nba_teams(id, abbr, name, nickname) VALUES (:id, :abbr, :name, :nickname)", t)

    def upsert_game(self, g: dict, fecha: str) -> None:
        self.upsert_team(g["home"])
        self.upsert_team(g["away"])
        self.conn.execute(
            """INSERT INTO nba_games(id, date_utc, fecha, season, season_type, home_id, away_id, status,
                                     home_pts, away_pts, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
               ON CONFLICT(id) DO UPDATE SET date_utc = excluded.date_utc, fecha = excluded.fecha,
                   status = excluded.status, home_pts = excluded.home_pts, away_pts = excluded.away_pts,
                   updated_at = excluded.updated_at""",
            (g["id"], g["date_utc"], fecha, g["season"], g["season_type"], g["home"]["id"], g["away"]["id"],
             g["status"], g["home_pts"], g["away_pts"], now_iso()),
        )

    def save_box(self, game_id: str, home_id: str, players: list[dict], shots: list[dict]) -> None:
        self.conn.execute("DELETE FROM nba_player_games WHERE game_id = ?", (game_id,))
        self.conn.execute("DELETE FROM nba_shots WHERE game_id = ?", (game_id,))
        self.conn.executemany(
            """INSERT INTO nba_player_games(game_id, player_id, team_id, opp_id, is_home, name, position, starter,
                   minutes, pts, fgm, fga, tpm, tpa, ftm, fta, reb, oreb, dreb, ast, stl, blk, tov, pf)
               VALUES (:game_id, :player_id, :team_id, :opp_id, :is_home, :name, :position, :starter, :minutes,
                       :pts, :fgm, :fga, :tpm, :tpa, :ftm, :fta, :reb, :oreb, :dreb, :ast, :stl, :blk, :tov, :pf)""",
            [{**p, "game_id": game_id, "is_home": int(p["team_id"] == home_id)} for p in players],
        )
        self.conn.executemany(
            """INSERT OR REPLACE INTO nba_shots(game_id, seq, player_id, team_id, opp_id, period, x, y, dist, zone,
                   value, made, assisted)
               VALUES (:game_id, :seq, :player_id, :team_id, :opp_id, :period, :x, :y, :dist, :zone, :value,
                       :made, :assisted)""",
            [{**s, "game_id": game_id} for s in shots],
        )
        self.conn.execute("UPDATE nba_games SET box_ok = 1 WHERE id = ?", (game_id,))

    def save_injuries(self, fecha: str, rows: list[dict]) -> None:
        self.conn.executemany(
            """INSERT OR REPLACE INTO nba_injuries(fecha, team_id, player_id, name, status, detail)
               VALUES (:fecha, :team_id, :player_id, :name, :status, :detail)""",
            [{**r, "fecha": fecha} for r in rows],
        )

    def save_props(self, fecha: str, rows: list[dict]) -> None:
        # Cada descarga reemplaza las líneas del día: las que ya no ofrece ninguna casa no deben quedar.
        self.conn.execute("DELETE FROM nba_props WHERE fecha = ?", (fecha,))
        self.conn.executemany(
            """INSERT OR REPLACE INTO nba_props(fecha, game_id, player_id, stat, line, over_odd, under_odd, books,
                   fetched_at)
               VALUES (:fecha, :game_id, :player_id, :stat, :line, :over_odd, :under_odd, :books, :fetched_at)""",
            [{**r, "fecha": fecha, "fetched_at": now_iso()} for r in rows],
        )

    # --- Lectura ------------------------------------------------------------------

    def games_on(self, fecha: str) -> list[sqlite3.Row]:
        return self.conn.execute(
            """SELECT g.*, h.name AS home_name, h.abbr AS home_abbr, h.nickname AS home_nick,
                      a.name AS away_name, a.abbr AS away_abbr, a.nickname AS away_nick
               FROM nba_games g JOIN nba_teams h ON h.id = g.home_id JOIN nba_teams a ON a.id = g.away_id
               WHERE g.fecha = ? ORDER BY g.date_utc""", (fecha,)).fetchall()

    def game_done(self, game_id: str) -> bool:
        r = self.conn.execute("SELECT box_ok FROM nba_games WHERE id = ?", (game_id,)).fetchone()
        return bool(r and r["box_ok"])

    def injuries(self, fecha: str) -> list[sqlite3.Row]:
        return self.conn.execute("SELECT * FROM nba_injuries WHERE fecha = ?", (fecha,)).fetchall()

    def props(self, fecha: str) -> list[sqlite3.Row]:
        return self.conn.execute("SELECT * FROM nba_props WHERE fecha = ?", (fecha,)).fetchall()
