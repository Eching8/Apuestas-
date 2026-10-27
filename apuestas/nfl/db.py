"""Tablas de la NFL dentro de la misma base SQLite (prefijo nfl_).

- nfl_games: calendario con resultado, línea de cierre (spread/total), techo, superficie, clima y QB titular.
- nfl_player_games: una fila por jugador y partido con todas las estadísticas de nflverse.
- nfl_player_pbp: lo que sale del jugada a jugada (zona roja, dentro de la 10 y la 5, envíos a la zona de
  anotación, carreras diseñadas de QB frente a scrambles, jugada más larga).
- nfl_team_games: el partido de cada equipo visto como ataque (jugadas, ritmo, EPA, éxito, explosivas, zona roja).
  Lo que concede una defensa es la fila de su rival en el mismo partido.
- nfl_rosters / nfl_movimientos: equipo actual de cada jugador y los cambios de equipo (traspasos, cortes).
- nfl_injuries / nfl_transactions: parte de lesiones (oficial y de ESPN) y movimientos de plantilla.
- nfl_lineas: cada línea de cada casa cada vez que se descarga (para ver cómo se mueve el mercado).
- nfl_picks: selecciones recomendadas, su liquidación y el rendimiento real.
"""
from __future__ import annotations

import sqlite3

from ..db import now_iso

STATS_JUGADOR = (
    "completions", "attempts", "passing_yards", "passing_tds", "passing_interceptions", "sacks_suffered",
    "passing_air_yards", "passing_yards_after_catch", "passing_first_downs", "passing_epa", "passing_cpoe",
    "passing_2pt_conversions", "carries", "rushing_yards", "rushing_tds", "rushing_fumbles_lost",
    "rushing_first_downs", "rushing_epa", "rushing_2pt_conversions", "receptions", "targets", "receiving_yards",
    "receiving_tds", "receiving_fumbles_lost", "receiving_air_yards", "receiving_yards_after_catch",
    "receiving_first_downs", "receiving_epa", "receiving_2pt_conversions", "target_share", "air_yards_share",
    "wopr", "racr", "pacr", "special_teams_tds", "def_tackles_solo", "def_tackle_assists", "def_sacks",
    "def_interceptions", "def_pass_defended", "fg_made", "fg_att", "pat_made", "fantasy_points_ppr",
)

SCHEMA = f"""
CREATE TABLE IF NOT EXISTS nfl_games (
    game_id TEXT PRIMARY KEY,
    season INTEGER NOT NULL,
    game_type TEXT,
    week INTEGER,
    gameday TEXT NOT NULL,
    gametime TEXT,
    home_team TEXT NOT NULL,
    away_team TEXT NOT NULL,
    home_score INTEGER,
    away_score INTEGER,
    spread_line REAL,          -- ventaja esperada del local (positivo = local favorito)
    total_line REAL,
    home_moneyline REAL,
    away_moneyline REAL,
    roof TEXT, surface TEXT, temp REAL, wind REAL,
    div_game INTEGER,
    home_rest INTEGER, away_rest INTEGER,
    home_qb_id TEXT, away_qb_id TEXT,
    espn_id TEXT,
    updated_at TEXT
);
CREATE INDEX IF NOT EXISTS ix_nfl_games_day ON nfl_games(gameday);

CREATE TABLE IF NOT EXISTS nfl_player_games (
    game_id TEXT NOT NULL,
    player_id TEXT NOT NULL,
    season INTEGER NOT NULL,
    week INTEGER NOT NULL,
    season_type TEXT,
    team TEXT NOT NULL,
    opp TEXT NOT NULL,
    name TEXT,
    position TEXT,
    {", ".join(f"{c} REAL" for c in STATS_JUGADOR)},
    PRIMARY KEY (game_id, player_id)
);
CREATE INDEX IF NOT EXISTS ix_nfl_pg_player ON nfl_player_games(player_id);
CREATE INDEX IF NOT EXISTS ix_nfl_pg_opp ON nfl_player_games(opp);

CREATE TABLE IF NOT EXISTS nfl_player_pbp (
    game_id TEXT NOT NULL,
    player_id TEXT NOT NULL,
    rz_carries INTEGER, i10_carries INTEGER, i5_carries INTEGER,
    rz_targets INTEGER, i10_targets INTEGER, ez_targets INTEGER,
    rz_rec INTEGER, rz_rec_tds INTEGER, rz_rush_tds INTEGER, ez_rec INTEGER,
    designed_runs INTEGER, scrambles INTEGER,
    long_rush REAL, long_rec REAL, long_pass REAL,
    rush_success INTEGER, rec_success INTEGER,
    PRIMARY KEY (game_id, player_id)
);

CREATE TABLE IF NOT EXISTS nfl_primer_td (
    game_id TEXT PRIMARY KEY,
    player_id TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS nfl_snaps (
    game_id TEXT NOT NULL,
    player_id TEXT NOT NULL,
    offense_snaps INTEGER,
    offense_pct REAL,
    PRIMARY KEY (game_id, player_id)
);

CREATE TABLE IF NOT EXISTS nfl_team_games (
    game_id TEXT NOT NULL,
    team TEXT NOT NULL,
    opp TEXT NOT NULL,
    season INTEGER, week INTEGER, is_home INTEGER,
    points INTEGER, opp_points INTEGER,
    plays INTEGER, dropbacks INTEGER, pass_att INTEGER, carries INTEGER, designed_runs INTEGER, targets INTEGER,
    pass_yds REAL, rush_yds REAL, yards REAL,
    epa REAL, pass_epa REAL, rush_epa REAL, success INTEGER,
    explosive_pass INTEGER, explosive_rush INTEGER,
    sacks INTEGER, turnovers INTEGER,
    rz_trips INTEGER, rz_tds INTEGER,
    pass_tds INTEGER, rush_tds INTEGER,
    third_att INTEGER, third_conv INTEGER,
    proe REAL,
    qb_rush_yds REAL, qb_rush_att INTEGER,
    drives INTEGER, punts INTEGER, fga INTEGER, fgm INTEGER,
    PRIMARY KEY (game_id, team)
);

-- Cada cambio en el marcador (TD, FG, extra, 2 puntos, safety), en orden: liquida los mercados de partido.
CREATE TABLE IF NOT EXISTS nfl_anotaciones (
    game_id TEXT NOT NULL,
    play_id REAL NOT NULL,
    qtr INTEGER,
    team TEXT,
    puntos INTEGER,
    tipo TEXT,
    home_score INTEGER,
    away_score INTEGER,
    player_id TEXT,
    distancia REAL,
    PRIMARY KEY (game_id, play_id)
);

-- Estadísticas de cada jugador por cuarto (props de 1.er cuarto, 1.ª mitad...).
CREATE TABLE IF NOT EXISTS nfl_player_quarter (
    game_id TEXT NOT NULL,
    player_id TEXT NOT NULL,
    qtr INTEGER NOT NULL,
    attempts REAL, completions REAL, passing_yards REAL, passing_tds REAL, passing_interceptions REAL,
    carries REAL, rushing_yards REAL, rushing_tds REAL,
    targets REAL, receptions REAL, receiving_yards REAL, receiving_tds REAL,
    PRIMARY KEY (game_id, player_id, qtr)
);

CREATE TABLE IF NOT EXISTS nfl_rosters (
    player_id TEXT PRIMARY KEY,
    name TEXT,
    position TEXT,
    team TEXT,
    status TEXT,
    season INTEGER,
    week INTEGER,
    espn_id TEXT,
    pfr_id TEXT,
    depth_position TEXT,
    years_exp INTEGER,
    updated_at TEXT
);
CREATE INDEX IF NOT EXISTS ix_nfl_rosters_espn ON nfl_rosters(espn_id);

CREATE TABLE IF NOT EXISTS nfl_movimientos (
    player_id TEXT NOT NULL,
    season INTEGER NOT NULL,
    week INTEGER NOT NULL,
    from_team TEXT,
    to_team TEXT NOT NULL,
    fuente TEXT,
    detected_at TEXT,
    PRIMARY KEY (player_id, season, week, to_team)
);

CREATE TABLE IF NOT EXISTS nfl_injuries (
    player_id TEXT NOT NULL,
    fuente TEXT NOT NULL,      -- 'nfl' (parte oficial de la semana) o 'espn' (al momento)
    name TEXT,
    team TEXT,
    position TEXT,
    status TEXT,
    detail TEXT,
    comment TEXT,
    season INTEGER,
    week INTEGER,
    fecha TEXT,
    updated_at TEXT,
    PRIMARY KEY (player_id, fuente)
);

CREATE TABLE IF NOT EXISTS nfl_transactions (
    fecha TEXT NOT NULL,
    team TEXT NOT NULL,
    description TEXT NOT NULL,
    PRIMARY KEY (fecha, team, description)
);

CREATE TABLE IF NOT EXISTS nfl_lineas (
    captured_at TEXT NOT NULL,
    event_id TEXT NOT NULL,
    game_id TEXT,
    player_id TEXT,            -- id de nflverse; NULL en mercados de equipo
    sgo_player_id TEXT,
    entidad TEXT NOT NULL,     -- jugador o 'home' / 'away' / 'all'
    stat TEXT NOT NULL,
    lado TEXT NOT NULL,        -- 'más' / 'menos' / 'sí'
    book TEXT NOT NULL,        -- casa o 'consenso'
    line REAL,
    odd REAL,
    open_line REAL,
    open_odd REAL,
    PRIMARY KEY (captured_at, event_id, entidad, stat, lado, book, line)
);
CREATE INDEX IF NOT EXISTS ix_nfl_lineas_game ON nfl_lineas(game_id, player_id);

CREATE TABLE IF NOT EXISTS nfl_picks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT NOT NULL,
    fecha TEXT NOT NULL,
    game_id TEXT NOT NULL,
    player_id TEXT NOT NULL,
    name TEXT,
    team TEXT,
    stat TEXT NOT NULL,
    line REAL NOT NULL,
    lado TEXT NOT NULL,
    prob REAL NOT NULL,
    prob_modelo REAL,
    prob_casa REAL,
    odd REAL,
    book TEXT,
    ev REAL,
    origen TEXT,               -- 'informe' o 'validar'
    razones TEXT,              -- JSON
    resultado REAL,
    acierto INTEGER,           -- 1 acierto, 0 fallo, NULL pendiente o nula (no jugó)
    settled_at TEXT,
    UNIQUE (fecha, game_id, player_id, stat, line, lado, origen)
);

CREATE TABLE IF NOT EXISTS nfl_descargas (
    url TEXT PRIMARY KEY,
    etag TEXT,
    updated_at TEXT
);

-- Lo que cada defensa concede a cada posición, partido a partido.
CREATE VIEW IF NOT EXISTS nfl_def_pos AS
SELECT pg.game_id, pg.opp AS defensa, pg.team AS ataque, pg.season, pg.week, pg.position,
       SUM(pg.attempts) AS attempts, SUM(pg.completions) AS completions, SUM(pg.passing_yards) AS passing_yards,
       SUM(pg.passing_tds) AS passing_tds, SUM(pg.passing_interceptions) AS ints, SUM(pg.sacks_suffered) AS sacks,
       SUM(pg.carries) AS carries, SUM(pg.rushing_yards) AS rushing_yards, SUM(pg.rushing_tds) AS rushing_tds,
       SUM(pg.targets) AS targets, SUM(pg.receptions) AS receptions, SUM(pg.receiving_yards) AS receiving_yards,
       SUM(pg.receiving_tds) AS receiving_tds,
       SUM(COALESCE(pp.rz_carries, 0)) AS rz_carries, SUM(COALESCE(pp.rz_targets, 0)) AS rz_targets,
       SUM(COALESCE(pp.designed_runs, 0)) AS designed_runs, SUM(COALESCE(pp.scrambles, 0)) AS scrambles
FROM nfl_player_games pg
LEFT JOIN nfl_player_pbp pp ON pp.game_id = pg.game_id AND pp.player_id = pg.player_id
WHERE pg.position IN ('QB', 'RB', 'FB', 'WR', 'TE')
GROUP BY pg.game_id, pg.opp, pg.position;
"""

ESTADOS_FUERA = ("out", "injured reserve", "doubtful", "suspension", "physically unable to perform", "pup",
                 "reserve", "non-football injury", "ir")
ESTADOS_DUDA = ("questionable",)
ROSTER_FUERA = ("RES", "CUT", "INA", "RET", "DEV", "UFA", "TRD", "EXE", "NWT", "SUS")


def estado_fuera(status: str | None) -> bool:
    s = (status or "").lower()
    return any(s.startswith(e) for e in ESTADOS_FUERA)


def estado_duda(status: str | None) -> bool:
    return (status or "").lower().startswith(ESTADOS_DUDA)


class NflDB:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn
        self.conn.executescript(SCHEMA)
        self._migrar()

    def _migrar(self) -> None:
        """Columnas añadidas después de crear la base (las bases viejas no las tienen)."""
        nuevas = {"nfl_team_games": ("drives INTEGER", "punts INTEGER", "fga INTEGER", "fgm INTEGER"),
                  "nfl_player_pbp": ("rz_rec INTEGER", "rz_rec_tds INTEGER", "rz_rush_tds INTEGER", "ez_rec INTEGER")}
        for tabla, columnas in nuevas.items():
            existentes = {r[1] for r in self.conn.execute(f"PRAGMA table_info({tabla})")}
            for col in columnas:
                if col.split()[0] not in existentes:
                    self.conn.execute(f"ALTER TABLE {tabla} ADD COLUMN {col}")

    def commit(self) -> None:
        self.conn.commit()

    # --- Descargas condicionales ------------------------------------------------------

    def etag(self, url: str) -> str | None:
        r = self.conn.execute("SELECT etag FROM nfl_descargas WHERE url = ?", (url,)).fetchone()
        return r[0] if r else None

    def guardar_etag(self, url: str, etag: str | None) -> None:
        self.conn.execute("INSERT OR REPLACE INTO nfl_descargas(url, etag, updated_at) VALUES (?, ?, ?)",
                          (url, etag, now_iso()))

    # --- Escritura ----------------------------------------------------------------------

    def upsert_games(self, filas: list[dict]) -> int:
        cols = ("game_id", "season", "game_type", "week", "gameday", "gametime", "home_team", "away_team",
                "home_score", "away_score", "spread_line", "total_line", "home_moneyline", "away_moneyline",
                "roof", "surface", "temp", "wind", "div_game", "home_rest", "away_rest", "home_qb_id", "away_qb_id",
                "espn_id")
        self.conn.executemany(
            f"INSERT OR REPLACE INTO nfl_games({', '.join(cols)}, updated_at) "
            f"VALUES ({', '.join('?' * len(cols))}, ?)",
            [tuple(f.get(c) for c in cols) + (now_iso(),) for f in filas])
        return len(filas)

    def reemplazar_player_games(self, season: int, filas: list[dict]) -> int:
        cols = ("game_id", "player_id", "season", "week", "season_type", "team", "opp", "name", "position") \
            + STATS_JUGADOR
        self.conn.execute("DELETE FROM nfl_player_games WHERE season = ?", (season,))
        self.conn.executemany(
            f"INSERT OR REPLACE INTO nfl_player_games({', '.join(cols)}) VALUES ({', '.join('?' * len(cols))})",
            [tuple(f.get(c) for c in cols) for f in filas])
        return len(filas)

    def reemplazar_pbp(self, season: int, resumen) -> None:
        """Guarda un ResumenPbp (ver fuentes.agregar_pbp) de una temporada."""
        like = f"{season}_%"
        jugadores, equipos = resumen.jugadores, resumen.equipos
        self.conn.executemany("INSERT OR REPLACE INTO nfl_primer_td(game_id, player_id) VALUES (?, ?)",
                              list(resumen.primeros.items()))
        for tabla, filas in (("nfl_anotaciones", resumen.anotaciones), ("nfl_player_quarter", resumen.cuartos)):
            self.conn.execute(f"DELETE FROM {tabla} WHERE game_id LIKE ?", (like,))
            for f in filas:
                cols = list(f)
                self.conn.execute(f"INSERT OR REPLACE INTO {tabla}({', '.join(cols)}) "
                                  f"VALUES ({', '.join('?' * len(cols))})", tuple(f[c] for c in cols))
        self.conn.execute("DELETE FROM nfl_player_pbp WHERE game_id LIKE ?", (like,))
        self.conn.execute("DELETE FROM nfl_team_games WHERE game_id LIKE ?", (like,))
        if jugadores:
            cols = list(jugadores[0])
            self.conn.executemany(
                f"INSERT OR REPLACE INTO nfl_player_pbp({', '.join(cols)}) VALUES ({', '.join('?' * len(cols))})",
                [tuple(f[c] for c in cols) for f in jugadores])
        if equipos:
            cols = list(equipos[0])
            self.conn.executemany(
                f"INSERT OR REPLACE INTO nfl_team_games({', '.join(cols)}) VALUES ({', '.join('?' * len(cols))})",
                [tuple(f[c] for c in cols) for f in equipos])
        # Los puntos salen del calendario (el jugada a jugada no trae el marcador final de forma fiable).
        self.conn.execute(
            "UPDATE nfl_team_games SET "
            "points = (SELECT CASE WHEN g.home_team = nfl_team_games.team THEN g.home_score ELSE g.away_score END "
            "          FROM nfl_games g WHERE g.game_id = nfl_team_games.game_id), "
            "opp_points = (SELECT CASE WHEN g.home_team = nfl_team_games.team THEN g.away_score ELSE g.home_score END "
            "              FROM nfl_games g WHERE g.game_id = nfl_team_games.game_id) "
            "WHERE game_id LIKE ?", (like,))

    def reemplazar_snaps(self, season: int, filas: list[dict]) -> None:
        self.conn.execute("DELETE FROM nfl_snaps WHERE game_id LIKE ?", (f"{season}_%",))
        self.conn.executemany(
            "INSERT OR REPLACE INTO nfl_snaps(game_id, player_id, offense_snaps, offense_pct) VALUES (?, ?, ?, ?)",
            [(f["game_id"], f["player_id"], f["offense_snaps"], f["offense_pct"]) for f in filas])

    def actualizar_roster(self, filas: list[dict]) -> list[dict]:
        """Guarda el equipo más reciente de cada jugador y devuelve los cambios de equipo detectados."""
        cambios = []
        for f in filas:
            prev = self.conn.execute("SELECT team, season, week FROM nfl_rosters WHERE player_id = ?",
                                     (f["player_id"],)).fetchone()
            if prev and (prev["season"], prev["week"]) > (f["season"], f["week"]):
                continue  # ya hay un dato más reciente
            if prev and prev["team"] and f["team"] and prev["team"] != f["team"]:
                cambios.append({"player_id": f["player_id"], "name": f.get("name"), "season": f["season"],
                                "prev_season": prev["season"], "week": f["week"], "from_team": prev["team"],
                                "to_team": f["team"]})
            self.conn.execute(
                "INSERT INTO nfl_rosters(player_id, name, position, team, status, season, week, espn_id, pfr_id, "
                "depth_position, years_exp, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) "
                "ON CONFLICT(player_id) DO UPDATE SET name = excluded.name, position = excluded.position, "
                "team = excluded.team, status = excluded.status, season = excluded.season, week = excluded.week, "
                "espn_id = COALESCE(excluded.espn_id, nfl_rosters.espn_id), "
                "pfr_id = COALESCE(excluded.pfr_id, nfl_rosters.pfr_id), depth_position = excluded.depth_position, "
                "years_exp = excluded.years_exp, updated_at = excluded.updated_at",
                (f["player_id"], f.get("name"), f.get("position"), f.get("team"), f.get("status"), f["season"],
                 f["week"], f.get("espn_id"), f.get("pfr_id"), f.get("depth_position"), f.get("years_exp"),
                 now_iso()))
        return cambios

    def guardar_movimiento(self, player_id: str, season: int, week: int, from_team: str | None, to_team: str,
                           fuente: str) -> None:
        """week 0 = cambio entre temporadas (agencia libre, traspaso de la pretemporada)."""
        self.conn.execute(
            "INSERT OR IGNORE INTO nfl_movimientos(player_id, season, week, from_team, to_team, fuente, detected_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)", (player_id, season, week, from_team, to_team, fuente, now_iso()))

    def guardar_lesiones(self, filas: list[dict], fuente: str) -> int:
        self.conn.execute("DELETE FROM nfl_injuries WHERE fuente = ?", (fuente,))
        self.conn.executemany(
            "INSERT OR REPLACE INTO nfl_injuries(player_id, fuente, name, team, position, status, detail, comment, "
            "season, week, fecha, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [(f["player_id"], fuente, f.get("name"), f.get("team"), f.get("position"), f.get("status"),
              f.get("detail"), f.get("comment"), f.get("season"), f.get("week"), f.get("fecha"), now_iso())
             for f in filas])
        return len(filas)

    def guardar_transacciones(self, filas: list[dict]) -> int:
        antes = self.conn.total_changes
        self.conn.executemany("INSERT OR IGNORE INTO nfl_transactions(fecha, team, description) VALUES (?, ?, ?)",
                              [(f["fecha"], f["team"], f["description"]) for f in filas])
        return self.conn.total_changes - antes

    def guardar_lineas(self, filas: list[dict]) -> int:
        cols = ("captured_at", "event_id", "game_id", "player_id", "sgo_player_id", "entidad", "stat", "lado",
                "book", "line", "odd", "open_line", "open_odd")
        self.conn.executemany(
            f"INSERT OR REPLACE INTO nfl_lineas({', '.join(cols)}) VALUES ({', '.join('?' * len(cols))})",
            [tuple(f.get(c) for c in cols) for f in filas])
        return len(filas)

    # --- Lectura ------------------------------------------------------------------------

    def proximos_partidos(self, desde: str, hasta: str) -> list[sqlite3.Row]:
        return self.conn.execute(
            "SELECT * FROM nfl_games WHERE gameday >= ? AND gameday <= ? ORDER BY gameday, gametime, game_id",
            (desde, hasta)).fetchall()

    def lesiones(self) -> dict[str, dict]:
        """La información más reciente de cada jugador (ESPN manda sobre el parte oficial de la semana)."""
        out: dict[str, dict] = {}
        for r in self.conn.execute("SELECT * FROM nfl_injuries ORDER BY CASE fuente WHEN 'espn' THEN 1 ELSE 0 END"):
            out[r["player_id"]] = dict(r)
        return out

    def historial_lineas(self, game_id: str, player_id: str | None, stat: str) -> list[sqlite3.Row]:
        return self.conn.execute(
            "SELECT * FROM nfl_lineas WHERE game_id = ? AND player_id IS ? AND stat = ? AND book = 'consenso' "
            "ORDER BY captured_at", (game_id, player_id, stat)).fetchall()
