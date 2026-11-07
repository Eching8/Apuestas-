"""Tablas de la NHL dentro de la misma base SQLite (prefijo nhl_)."""
from __future__ import annotations

import sqlite3

from ..db import now_iso

SCHEMA = """
CREATE TABLE IF NOT EXISTS nhl_teams (
    id TEXT PRIMARY KEY,
    abbr TEXT,
    name TEXT,
    nickname TEXT
);

CREATE TABLE IF NOT EXISTS nhl_games (
    id TEXT PRIMARY KEY,
    date_utc TEXT NOT NULL,
    fecha TEXT NOT NULL,
    season INTEGER,
    season_type INTEGER,
    home_id TEXT NOT NULL,
    away_id TEXT NOT NULL,
    status TEXT,
    home_goals INTEGER,
    away_goals INTEGER,
    periodos INTEGER,               -- 3 = tiempo reglamentario, 4 = prórroga, 5 = penaltis
    box_ok INTEGER NOT NULL DEFAULT 0,
    margen_esperado REAL,           -- goles que se espera que gane el local (moneyline y total de la casa, ESPN)
    total_esperado REAL,            -- total de goles de la casa
    home_goalie_id TEXT,            -- portero probable (ESPN, el día del partido)
    away_goalie_id TEXT,
    updated_at TEXT
);
CREATE INDEX IF NOT EXISTS ix_nhl_games_fecha ON nhl_games(fecha);

-- Una fila por jugador de campo que jugó. Tiempos en minutos.
CREATE TABLE IF NOT EXISTS nhl_player_games (
    game_id TEXT NOT NULL REFERENCES nhl_games(id),
    player_id TEXT NOT NULL,
    team_id TEXT NOT NULL,
    opp_id TEXT NOT NULL,
    is_home INTEGER NOT NULL,
    name TEXT,
    position TEXT,
    grupo TEXT,                     -- F (delantero) o D (defensa)
    toi REAL NOT NULL, pptoi REAL, shtoi REAL, estoi REAL, shifts INTEGER,
    g INTEGER, a INTEGER, sog INTEGER, missed INTEGER, bs INTEGER, hits INTEGER, tk INTEGER, gv INTEGER,
    pm INTEGER, pim INTEGER, fow INTEGER, fol INTEGER,
    ppp INTEGER,                    -- puntos en power play (de la jugada a jugada)
    pp_sog INTEGER,                 -- tiros a puerta en power play
    PRIMARY KEY (game_id, player_id)
);
CREATE INDEX IF NOT EXISTS ix_nhl_pg_player ON nhl_player_games(player_id);

CREATE TABLE IF NOT EXISTS nhl_goalie_games (
    game_id TEXT NOT NULL REFERENCES nhl_games(id),
    player_id TEXT NOT NULL,
    team_id TEXT NOT NULL,
    opp_id TEXT NOT NULL,
    is_home INTEGER NOT NULL,
    name TEXT,
    starter INTEGER,
    toi REAL, sa INTEGER, sv INTEGER, ga INTEGER, es_sv INTEGER, pp_sv INTEGER, sh_sv INTEGER,
    PRIMARY KEY (game_id, player_id)
);
CREATE INDEX IF NOT EXISTS ix_nhl_gg_player ON nhl_goalie_games(player_id);

-- Tiros de la jugada a jugada (a puerta, gol, fuera, bloqueado) con su situación.
CREATE TABLE IF NOT EXISTS nhl_shots (
    game_id TEXT NOT NULL REFERENCES nhl_games(id),
    seq INTEGER NOT NULL,
    player_id TEXT NOT NULL,
    team_id TEXT NOT NULL,
    opp_id TEXT,
    period INTEGER,
    x REAL, y REAL, dist REAL,
    shot_type TEXT,
    result TEXT NOT NULL,           -- sog, goal, missed, blocked
    strength TEXT,                  -- ES, PP, SH
    goalie_id TEXT,
    PRIMARY KEY (game_id, seq)
);
CREATE INDEX IF NOT EXISTS ix_nhl_shots_player ON nhl_shots(player_id);

CREATE TABLE IF NOT EXISTS nhl_goals (
    game_id TEXT NOT NULL REFERENCES nhl_games(id),
    seq INTEGER NOT NULL,
    team_id TEXT NOT NULL,
    opp_id TEXT,
    period INTEGER,
    strength TEXT,
    scorer_id TEXT, a1_id TEXT, a2_id TEXT,
    PRIMARY KEY (game_id, seq)
);

-- Penaltis cometidos (para medir el power play que concede cada equipo).
CREATE TABLE IF NOT EXISTS nhl_penalties (
    game_id TEXT NOT NULL REFERENCES nhl_games(id),
    seq INTEGER NOT NULL,
    player_id TEXT,
    team_id TEXT,
    opp_id TEXT,
    period INTEGER,
    tipo TEXT,
    PRIMARY KEY (game_id, seq)
);

CREATE TABLE IF NOT EXISTS nhl_injuries (
    fecha TEXT NOT NULL,
    team_id TEXT NOT NULL,
    player_id TEXT NOT NULL,
    name TEXT,
    status TEXT,
    detail TEXT,
    PRIMARY KEY (fecha, player_id)
);

-- Líneas de la casa (The Odds API con ODDS_API_NHL=1) por jugador y estadística.
CREATE TABLE IF NOT EXISTS nhl_props (
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

CREATE TABLE IF NOT EXISTS nhl_analisis (
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
    estimada INTEGER,               -- 1 = línea estimada (sin línea de la casa)
    detalle TEXT NOT NULL,
    created_at TEXT NOT NULL,
    PRIMARY KEY (fecha, game_id, player_id, stat)
);

CREATE TABLE IF NOT EXISTS nhl_picks (
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

CREATE TABLE IF NOT EXISTS nhl_combinadas (
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
"""


class NhlDB:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn
        self.conn.executescript(SCHEMA)

    def commit(self) -> None:
        self.conn.commit()

    # --- Escritura ----------------------------------------------------------------

    def upsert_team(self, t: dict) -> None:
        self.conn.execute(
            "INSERT OR REPLACE INTO nhl_teams(id, abbr, name, nickname) VALUES (:id, :abbr, :name, :nickname)", t)

    def upsert_game(self, g: dict, fecha: str) -> None:
        self.upsert_team(g["home"])
        self.upsert_team(g["away"])
        pr = g.get("probables") or {}
        self.conn.execute(
            """INSERT INTO nhl_games(id, date_utc, fecha, season, season_type, home_id, away_id, status, home_goals,
                                     away_goals, periodos, margen_esperado, total_esperado, home_goalie_id,
                                     away_goalie_id, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
               ON CONFLICT(id) DO UPDATE SET date_utc = excluded.date_utc, fecha = excluded.fecha,
                   status = excluded.status, home_goals = excluded.home_goals, away_goals = excluded.away_goals,
                   periodos = COALESCE(excluded.periodos, nhl_games.periodos),
                   margen_esperado = COALESCE(excluded.margen_esperado, nhl_games.margen_esperado),
                   total_esperado = COALESCE(excluded.total_esperado, nhl_games.total_esperado),
                   home_goalie_id = COALESCE(excluded.home_goalie_id, nhl_games.home_goalie_id),
                   away_goalie_id = COALESCE(excluded.away_goalie_id, nhl_games.away_goalie_id),
                   updated_at = excluded.updated_at""",
            (g["id"], g["date_utc"], fecha, g["season"], g["season_type"], g["home"]["id"], g["away"]["id"],
             g["status"], g.get("home_goals"), g.get("away_goals"), g.get("periodos"), g.get("margen_esperado"),
             g.get("total_esperado"), (pr.get("home") or {}).get("player_id"),
             (pr.get("away") or {}).get("player_id"), now_iso()),
        )

    def save_box(self, game_id: str, home_id: str, skaters: list[dict], goalies: list[dict], tiros: list[dict],
                 goles: list[dict], penaltis: list[dict]) -> None:
        for tabla in ("nhl_player_games", "nhl_goalie_games", "nhl_shots", "nhl_goals", "nhl_penalties"):
            self.conn.execute(f"DELETE FROM {tabla} WHERE game_id = ?", (game_id,))
        ppp: dict[str, int] = {}
        for gol in goles:
            if gol["strength"] == "PP":
                for pid in (gol["scorer_id"], gol["a1_id"], gol["a2_id"]):
                    if pid:
                        ppp[pid] = ppp.get(pid, 0) + 1
        pp_sog: dict[str, int] = {}
        for t in tiros:
            if t["strength"] == "PP" and t["result"] in ("sog", "goal"):
                pp_sog[t["player_id"]] = pp_sog.get(t["player_id"], 0) + 1
        self.conn.executemany(
            """INSERT INTO nhl_player_games(game_id, player_id, team_id, opp_id, is_home, name, position, grupo, toi,
                   pptoi, shtoi, estoi, shifts, g, a, sog, missed, bs, hits, tk, gv, pm, pim, fow, fol, ppp, pp_sog)
               VALUES (:game_id, :player_id, :team_id, :opp_id, :is_home, :name, :position, :grupo, :toi, :pptoi,
                       :shtoi, :estoi, :shifts, :g, :a, :sog, :missed, :bs, :hits, :tk, :gv, :pm, :pim, :fow, :fol,
                       :ppp, :pp_sog)""",
            [{**p, "game_id": game_id, "is_home": int(p["team_id"] == home_id), "ppp": ppp.get(p["player_id"], 0),
              "pp_sog": pp_sog.get(p["player_id"], 0)} for p in skaters])
        self.conn.executemany(
            """INSERT INTO nhl_goalie_games(game_id, player_id, team_id, opp_id, is_home, name, starter, toi, sa, sv,
                   ga, es_sv, pp_sv, sh_sv)
               VALUES (:game_id, :player_id, :team_id, :opp_id, :is_home, :name, :starter, :toi, :sa, :sv, :ga,
                       :es_sv, :pp_sv, :sh_sv)""",
            [{**g, "game_id": game_id, "is_home": int(g["team_id"] == home_id)} for g in goalies])
        self.conn.executemany(
            """INSERT OR REPLACE INTO nhl_shots(game_id, seq, player_id, team_id, opp_id, period, x, y, dist,
                   shot_type, result, strength, goalie_id)
               VALUES (:game_id, :seq, :player_id, :team_id, :opp_id, :period, :x, :y, :dist, :shot_type, :result,
                       :strength, :goalie_id)""", [{**t, "game_id": game_id} for t in tiros])
        self.conn.executemany(
            """INSERT OR REPLACE INTO nhl_goals(game_id, seq, team_id, opp_id, period, strength, scorer_id, a1_id,
                   a2_id) VALUES (:game_id, :seq, :team_id, :opp_id, :period, :strength, :scorer_id, :a1_id, :a2_id)""",
            [{**g, "game_id": game_id} for g in goles])
        self.conn.executemany(
            """INSERT OR REPLACE INTO nhl_penalties(game_id, seq, player_id, team_id, opp_id, period, tipo)
               VALUES (:game_id, :seq, :player_id, :team_id, :opp_id, :period, :tipo)""",
            [{**p, "game_id": game_id} for p in penaltis])
        self.conn.execute("UPDATE nhl_games SET box_ok = 1 WHERE id = ?", (game_id,))

    def save_injuries(self, fecha: str, rows: list[dict]) -> None:
        self.conn.executemany(
            """INSERT OR REPLACE INTO nhl_injuries(fecha, team_id, player_id, name, status, detail)
               VALUES (:fecha, :team_id, :player_id, :name, :status, :detail)""",
            [{**r, "fecha": fecha} for r in rows])

    def save_props(self, fecha: str, rows: list[dict]) -> None:
        self.conn.execute("DELETE FROM nhl_props WHERE fecha = ?", (fecha,))
        self.conn.executemany(
            """INSERT OR REPLACE INTO nhl_props(fecha, game_id, player_id, stat, line, over_odd, under_odd, books,
                   fetched_at)
               VALUES (:fecha, :game_id, :player_id, :stat, :line, :over_odd, :under_odd, :books, :fetched_at)""",
            [{**r, "fecha": fecha, "fetched_at": now_iso()} for r in rows])

    # --- Lectura ------------------------------------------------------------------

    def games_on(self, fecha: str) -> list[sqlite3.Row]:
        return self.conn.execute(
            """SELECT g.*, h.name AS home_name, h.abbr AS home_abbr, h.nickname AS home_nick,
                      a.name AS away_name, a.abbr AS away_abbr, a.nickname AS away_nick
               FROM nhl_games g JOIN nhl_teams h ON h.id = g.home_id JOIN nhl_teams a ON a.id = g.away_id
               WHERE g.fecha = ? ORDER BY g.date_utc""", (fecha,)).fetchall()

    def game_done(self, game_id: str) -> bool:
        r = self.conn.execute("SELECT box_ok FROM nhl_games WHERE id = ?", (game_id,)).fetchone()
        return bool(r and r["box_ok"])

    def injuries(self, fecha: str) -> list[sqlite3.Row]:
        return self.conn.execute("SELECT * FROM nhl_injuries WHERE fecha = ?", (fecha,)).fetchall()

    def props(self, fecha: str) -> list[sqlite3.Row]:
        return self.conn.execute("SELECT * FROM nhl_props WHERE fecha = ?", (fecha,)).fetchall()
