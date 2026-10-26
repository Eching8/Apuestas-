"""Base de datos local DuckDB: esquema y utilidades de escritura.

Convenciones:
- `season` es el año de inicio de la temporada (2021 = 2021-22).
- Ids de equipos, jugadores y partidos son los de ESPN (la fuente que funciona desde cualquier red).
  Las demás fuentes se emparejan con ellos en `player_map`.
- Todo lo que llega de una fuente externa en el tiempo (lesiones, cuotas) lleva la hora de captura
  (`snapshot_at`, UTC) para poder reconstruir qué se sabía antes de cada partido.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from pathlib import Path

import duckdb
import pandas as pd

log = logging.getLogger(__name__)

ESQUEMA = """
CREATE TABLE IF NOT EXISTS teams (
    team_id VARCHAR PRIMARY KEY, abbr VARCHAR, name VARCHAR, nickname VARCHAR
);

CREATE TABLE IF NOT EXISTS games (
    game_id VARCHAR PRIMARY KEY,
    season INTEGER NOT NULL,           -- 2021 = 2021-22
    season_type INTEGER NOT NULL,      -- 2 regular, 3 playoffs, 5 play-in
    start_utc TIMESTAMP NOT NULL,
    fecha DATE NOT NULL,               -- fecha del partido en hora del este (como la NBA)
    home_id VARCHAR NOT NULL,
    away_id VARCHAR NOT NULL,
    neutral BOOLEAN,
    status VARCHAR,
    home_pts INTEGER,
    away_pts INTEGER,
    periods INTEGER,
    box_ok BOOLEAN DEFAULT FALSE,
    pbp_ok BOOLEAN DEFAULT FALSE,
    updated_at TIMESTAMP
);

-- Box score: una fila por jugador que jugó (minutos > 0).
CREATE TABLE IF NOT EXISTS player_games (
    game_id VARCHAR, player_id VARCHAR, team_id VARCHAR, opp_id VARCHAR, is_home BOOLEAN,
    name VARCHAR, position VARCHAR, starter BOOLEAN, minutes DOUBLE,
    pts INTEGER, fgm INTEGER, fga INTEGER, fg3m INTEGER, fg3a INTEGER, ftm INTEGER, fta INTEGER,
    oreb INTEGER, dreb INTEGER, reb INTEGER, ast INTEGER, stl INTEGER, blk INTEGER, tov INTEGER,
    pf INTEGER, plus_minus INTEGER,
    PRIMARY KEY (game_id, player_id)
);

-- Jugadores en la convocatoria que no jugaron, con el motivo que da el box score
-- (lesión, decisión técnica, no convocado...). Sirve como parte de bajas histórico.
CREATE TABLE IF NOT EXISTS player_absences (
    game_id VARCHAR, player_id VARCHAR, team_id VARCHAR, name VARCHAR, position VARCHAR,
    reason VARCHAR, kind VARCHAR,      -- lesion | tecnica | otra
    PRIMARY KEY (game_id, player_id)
);

-- Totales de equipo del box score (incluye rebotes de equipo, que no son de ningún jugador).
CREATE TABLE IF NOT EXISTS team_games (
    game_id VARCHAR, team_id VARCHAR, opp_id VARCHAR, is_home BOOLEAN,
    pts INTEGER, fgm INTEGER, fga INTEGER, fg3m INTEGER, fg3a INTEGER, ftm INTEGER, fta INTEGER,
    oreb INTEGER, dreb INTEGER, reb INTEGER, ast INTEGER, stl INTEGER, blk INTEGER, tov INTEGER,
    pf INTEGER, q1 INTEGER, q2 INTEGER, q3 INTEGER, q4 INTEGER, ot INTEGER,
    PRIMARY KEY (game_id, team_id)
);

-- Jugada a jugada normalizado.
CREATE TABLE IF NOT EXISTS plays (
    game_id VARCHAR, seq INTEGER, period INTEGER,
    clock_s DOUBLE,                    -- segundos que quedan en el periodo
    elapsed_s DOUBLE,                  -- segundos de juego transcurridos desde el inicio
    team_id VARCHAR, type_id VARCHAR, type_text VARCHAR, text VARCHAR,
    event VARCHAR,                     -- tiro | libre | rebote_of | rebote_def | perdida | falta | cambio | salto | fin_periodo | otro
    made BOOLEAN, points INTEGER, value INTEGER,
    p1 VARCHAR, p2 VARCHAR, p3 VARCHAR,
    home_score INTEGER, away_score INTEGER, x DOUBLE, y DOUBLE,
    PRIMARY KEY (game_id, seq)
);

-- Producción por jugador y periodo, reconstruida con el jugada a jugada (props de cuarto y mitad).
CREATE TABLE IF NOT EXISTS player_periods (
    game_id VARCHAR, player_id VARCHAR, team_id VARCHAR, period INTEGER, seconds DOUBLE,
    pts INTEGER, fgm INTEGER, fga INTEGER, fg3m INTEGER, fg3a INTEGER, ftm INTEGER, fta INTEGER,
    oreb INTEGER, dreb INTEGER, ast INTEGER, stl INTEGER, blk INTEGER, tov INTEGER, pf INTEGER,
    PRIMARY KEY (game_id, player_id, period)
);

-- Tramos con el mismo quinteto en pista.
CREATE TABLE IF NOT EXISTS stints (
    game_id VARCHAR, team_id VARCHAR, period INTEGER, start_s DOUBLE, end_s DOUBLE,
    lineup VARCHAR[],
    PRIMARY KEY (game_id, team_id, period, start_s)
);

-- Tiros de campo con zona (coordenadas de ESPN).
CREATE TABLE IF NOT EXISTS shots (
    game_id VARCHAR, seq INTEGER, player_id VARCHAR, team_id VARCHAR, opp_id VARCHAR, period INTEGER,
    x DOUBLE, y DOUBLE, dist DOUBLE, zone VARCHAR, value INTEGER, made BOOLEAN, assisted BOOLEAN,
    PRIMARY KEY (game_id, seq)
);

-- Inicio del partido: salto inicial, titulares y primeros anotadores (submodelo de primer anotador).
CREATE TABLE IF NOT EXISTS game_starts (
    game_id VARCHAR PRIMARY KEY,
    jump_home_player VARCHAR, jump_away_player VARCHAR, jump_winner_team VARCHAR,
    first_fg_player VARCHAR, first_fg_team VARCHAR,       -- primera canasta de campo
    first_pts_player VARCHAR, first_pts_team VARCHAR,     -- primeros puntos (incluye libres)
    home_first_fg_player VARCHAR, away_first_fg_player VARCHAR,
    home_first_pts_player VARCHAR, away_first_pts_player VARCHAR,
    home_starters VARCHAR[], away_starters VARCHAR[]
);

-- Líneas del partido (spread y total). spread_home negativo = local favorito.
CREATE TABLE IF NOT EXISTS game_lines (
    game_id VARCHAR, source VARCHAR, kind VARCHAR,        -- kind: cierre | apertura | captura
    snapshot_at TIMESTAMP,
    spread_home DOUBLE, total DOUBLE, ml_home DOUBLE, ml_away DOUBLE,
    PRIMARY KEY (game_id, source, kind)
);

-- Parte de lesiones tal como se conocía en `snapshot_at`.
CREATE TABLE IF NOT EXISTS injuries (
    snapshot_at TIMESTAMP, source VARCHAR, team_id VARCHAR, player_id VARCHAR, name VARCHAR,
    status VARCHAR, detail VARCHAR, return_date VARCHAR,
    PRIMARY KEY (snapshot_at, source, player_id)
);

-- Alineaciones titulares (confirmadas o cargadas a mano) con hora de captura.
CREATE TABLE IF NOT EXISTS lineups (
    snapshot_at TIMESTAMP, source VARCHAR, game_id VARCHAR, team_id VARCHAR, player_id VARCHAR,
    name VARCHAR, confirmed BOOLEAN,
    PRIMARY KEY (snapshot_at, source, game_id, player_id)
);

-- Cuotas de props. Una fila por captura, casa, jugador, mercado, línea y lado.
-- kind: apertura | cierre | captura. snapshot_at es NULL en apertura/cierre históricos si la fuente
-- no da la hora exacta (se sabe que la apertura es anterior y el cierre es el inicio del partido).
CREATE TABLE IF NOT EXISTS prop_odds (
    source VARCHAR, kind VARCHAR, snapshot_at TIMESTAMP, book VARCHAR,
    event_id VARCHAR, game_id VARCHAR, start_utc TIMESTAMP,
    stat_id VARCHAR,                   -- identificador original de la fuente
    market VARCHAR,                    -- mercado normalizado (NULL si aún no se modela)
    period VARCHAR,                    -- game | 1q | 1h ...
    bet_type VARCHAR,                  -- ou | yn
    source_player_id VARCHAR, player_id VARCHAR, player_name VARCHAR, team_id VARCHAR,
    side VARCHAR, line DOUBLE, odds DOUBLE,                -- cuota decimal
    result DOUBLE                      -- valor final de la estadística si la fuente lo da
);
CREATE INDEX IF NOT EXISTS ix_prop_odds_game ON prop_odds(game_id);

-- Catálogo de mercados vistos en las fuentes. Los nuevos entran como "sin validar".
CREATE TABLE IF NOT EXISTS market_catalog (
    source VARCHAR, stat_id VARCHAR, period VARCHAR, bet_type VARCHAR,
    market VARCHAR, modelado BOOLEAN, estado VARCHAR,    -- estado: sin validar | validado | desactivado
    first_seen TIMESTAMP, last_seen TIMESTAMP, veces INTEGER,
    PRIMARY KEY (source, stat_id, period, bet_type)
);

-- Correspondencia de ids de otras fuentes con los de ESPN.
CREATE TABLE IF NOT EXISTS player_map (
    source VARCHAR, source_player_id VARCHAR, player_id VARCHAR, name VARCHAR, metodo VARCHAR,
    PRIMARY KEY (source, source_player_id)
);
CREATE TABLE IF NOT EXISTS event_map (
    source VARCHAR, event_id VARCHAR, game_id VARCHAR, PRIMARY KEY (source, event_id)
);

-- stats.nba.com (nba_api): métricas avanzadas y tracking por jugador y temporada, calculadas hasta
-- `date_to` (inclusive) para que no haya fuga de información. `datos` es la fila original en JSON.
CREATE TABLE IF NOT EXISTS nba_stats (
    endpoint VARCHAR, measure VARCHAR, season INTEGER, date_to DATE, nba_player_id VARCHAR,
    player_name VARCHAR, team_abbr VARCHAR, datos JSON, fetched_at TIMESTAMP,
    PRIMARY KEY (endpoint, measure, season, date_to, nba_player_id)
);

-- Control de calidad de cada partido: % de jugadores cuyo jugada a jugada cuadra con el box score.
CREATE TABLE IF NOT EXISTS pbp_quality (
    game_id VARCHAR PRIMARY KEY, n INTEGER, mae_min DOUBLE, max_err_min DOUBLE,
    ok_pts DOUBLE, ok_fgm DOUBLE, ok_fga DOUBLE, ok_fg3m DOUBLE, ok_fg3a DOUBLE, ok_ftm DOUBLE, ok_fta DOUBLE,
    ok_oreb DOUBLE, ok_dreb DOUBLE, ok_ast DOUBLE, ok_stl DOUBLE, ok_blk DOUBLE, ok_tov DOUBLE, ok_pf DOUBLE
);

-- Proyección de minutos de cada jugador probable (fase 2). Se reescribe en cada ejecución del día.
CREATE TABLE IF NOT EXISTS proj_minutos (
    fecha DATE, game_id VARCHAR, player_id VARCHAR, team_id VARCHAR, name VARCHAR, estado_lesion VARCHAR,
    prob_juega DOUBLE, min_base DOUBLE, min_norm DOUBLE, libres DOUBLE, min_pred DOUBLE, min_si_juega DOUBLE,
    min_q10 DOUBLE, min_q50 DOUBLE, min_q90 DOUBLE, p_dnp DOUBLE, modelo_hasta TIMESTAMP, created_at TIMESTAMP,
    PRIMARY KEY (fecha, game_id, player_id)
);

-- Distribución de puntos simulada de cada jugador probable (fase 3).
CREATE TABLE IF NOT EXISTS proj_puntos (
    fecha DATE, game_id VARCHAR, player_id VARCHAR, team_id VARCHAR, name VARCHAR, estado_lesion VARCHAR,
    prob_juega DOUBLE, p_dnp DOUBLE, min_si_juega DOUBLE, pts_media DOUBLE, pts_q10 DOUBLE, pts_q25 DOUBLE,
    pts_q50 DOUBLE, pts_q75 DOUBLE, pts_q90 DOUBLE, created_at TIMESTAMP,
    PRIMARY KEY (fecha, game_id, player_id)
);

-- Registro de descargas (qué se pidió, cuándo y si falló).
CREATE TABLE IF NOT EXISTS ingest_log (
    source VARCHAR, key VARCHAR, status VARCHAR, detail VARCHAR, logged_at TIMESTAMP,
    PRIMARY KEY (source, key)
);
"""

# Vistas con métricas avanzadas calculadas desde el box score (fórmulas estándar de Basketball-Reference).
VISTAS = """
CREATE OR REPLACE VIEW v_team_games AS
SELECT t.*, g.season, g.season_type, g.fecha, g.start_utc,
       t.fga + 0.44 * t.fta - t.oreb + t.tov AS poss,
       o.pts AS opp_pts, o.fga + 0.44 * o.fta - o.oreb + o.tov AS opp_poss,
       m.minutes AS team_minutes
FROM team_games t
JOIN team_games o ON o.game_id = t.game_id AND o.team_id = t.opp_id
JOIN games g ON g.game_id = t.game_id
JOIN (SELECT game_id, team_id, SUM(minutes) AS minutes FROM player_games GROUP BY 1, 2) m
  ON m.game_id = t.game_id AND m.team_id = t.team_id;

CREATE OR REPLACE VIEW v_team_adv AS
SELECT *, (poss + opp_poss) / 2 AS poss_avg,
       48 * ((poss + opp_poss) / 2) / (team_minutes / 5) AS pace,
       100 * pts / NULLIF((poss + opp_poss) / 2, 0) AS ortg,
       100 * opp_pts / NULLIF((poss + opp_poss) / 2, 0) AS drtg
FROM v_team_games;

CREATE OR REPLACE VIEW v_player_adv AS
SELECT p.*, g.season, g.season_type, g.fecha, g.start_utc,
       100 * ((p.fga + 0.44 * p.fta + p.tov) * (t.team_minutes / 5))
           / NULLIF(p.minutes * (t.fga + 0.44 * t.fta + t.tov), 0) AS usg_pct,
       p.pts / NULLIF(2 * (p.fga + 0.44 * p.fta), 0) AS ts_pct,
       t.pace
FROM player_games p
JOIN v_team_adv t ON t.game_id = p.game_id AND t.team_id = p.team_id
JOIN games g ON g.game_id = p.game_id;
"""


def conectar(ruta: str | Path, solo_lectura: bool = False) -> duckdb.DuckDBPyConnection:
    ruta = Path(ruta)
    if str(ruta) != ":memory:":
        ruta.parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(ruta), read_only=solo_lectura)
    if not solo_lectura:
        con.execute(ESQUEMA)
        con.execute(VISTAS)
    return con


def ahora_utc() -> datetime:
    """Hora actual en UTC sin zona (DuckDB guarda TIMESTAMP sin zona: siempre UTC por convención)."""
    return datetime.now(timezone.utc).replace(tzinfo=None, microsecond=0)


def columnas(con: duckdb.DuckDBPyConnection, tabla: str) -> list[str]:
    return [r[0] for r in con.execute(f"DESCRIBE {tabla}").fetchall()]


def upsert(con: duckdb.DuckDBPyConnection, tabla: str, filas: list[dict] | pd.DataFrame) -> int:
    """Inserta o actualiza filas por clave primaria. En filas que ya existen, las columnas que no vienen
    en `filas` conservan su valor (comportamiento de INSERT OR REPLACE de DuckDB)."""
    df = filas if isinstance(filas, pd.DataFrame) else pd.DataFrame(filas)
    if df.empty:
        return 0
    cols = [c for c in columnas(con, tabla) if c in df.columns]
    con.register("_entrada", df[cols])
    try:
        con.execute(f"INSERT OR REPLACE INTO {tabla} ({', '.join(cols)}) SELECT {', '.join(cols)} FROM _entrada")
    finally:
        con.unregister("_entrada")
    return len(df)


def insertar(con: duckdb.DuckDBPyConnection, tabla: str, filas: list[dict] | pd.DataFrame) -> int:
    """Inserción simple (tablas sin clave primaria, como prop_odds)."""
    df = filas if isinstance(filas, pd.DataFrame) else pd.DataFrame(filas)
    if df.empty:
        return 0
    cols = [c for c in columnas(con, tabla) if c in df.columns]
    con.register("_entrada", df[cols])
    try:
        con.execute(f"INSERT INTO {tabla} ({', '.join(cols)}) SELECT {', '.join(cols)} FROM _entrada")
    finally:
        con.unregister("_entrada")
    return len(df)


def registrar(con: duckdb.DuckDBPyConnection, fuente: str, clave: str, estado: str, detalle: str = "") -> None:
    con.execute("INSERT OR REPLACE INTO ingest_log VALUES (?, ?, ?, ?, ?)",
                [fuente, clave, estado, detalle[:500], ahora_utc()])
