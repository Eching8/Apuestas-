"""Acceso a los datos "tal como se conocían" antes de un instante: la única puerta para construir
features y evaluar. Regla: para predecir un partido que empieza en T solo se usa información
disponible antes de T (o antes de la hora de la predicción, si es anterior).

- Estadísticas de un partido: disponibles desde su inicio + `datos.horas_hasta_disponible`.
- Lesiones, alineaciones y cuotas: desde su `snapshot_at`.
- Cuotas de apertura históricas (sin hora exacta): disponibles antes del partido.
- Cuotas de cierre y resultados de las props: NUNCA como entrada; solo para evaluar (CLV, aciertos).
- stats.nba.com: filas acumuladas con date_to anterior a la fecha del partido.
"""
from __future__ import annotations

from datetime import date, datetime, timedelta

import duckdb
import pandas as pd


class FugaDeDatos(AssertionError):
    """Se intentó usar información posterior al corte."""


def disponible_desde(start_utc: datetime, horas: float) -> datetime:
    return start_utc + timedelta(hours=horas)


def partidos_previos(con: duckdb.DuckDBPyConnection, corte: datetime, horas: float = 3.5) -> pd.DataFrame:
    """Partidos terminados cuyas estadísticas ya se conocían en `corte`."""
    return con.execute("""SELECT * FROM games WHERE status = 'STATUS_FINAL'
                          AND start_utc + to_microseconds(CAST(? * 3600e6 AS BIGINT)) <= ?
                          ORDER BY start_utc""", [horas, corte]).df()


def box_previo(con: duckdb.DuckDBPyConnection, corte: datetime, horas: float = 3.5,
               player_ids: list[str] | None = None) -> pd.DataFrame:
    filtro = "AND p.player_id IN (SELECT unnest(?))" if player_ids else ""
    params = [horas, corte] + ([player_ids] if player_ids else [])
    return con.execute(f"""SELECT p.*, g.start_utc, g.fecha, g.season, g.season_type FROM player_games p
                           JOIN games g USING (game_id)
                           WHERE g.start_utc + to_microseconds(CAST(? * 3600e6 AS BIGINT)) <= ? {filtro}
                           ORDER BY g.start_utc""", params).df()


def lesiones_en(con: duckdb.DuckDBPyConnection, corte: datetime) -> pd.DataFrame:
    """Último estado conocido de cada jugador en el parte de lesiones anterior a `corte`.
    Solo cuenta la última captura: si un jugador ya no aparece en ella, está disponible."""
    ultima = con.execute("SELECT max(snapshot_at) FROM injuries WHERE snapshot_at < ?", [corte]).fetchone()[0]
    if ultima is None:
        return pd.DataFrame(columns=["player_id", "team_id", "name", "status", "detail", "snapshot_at"])
    return con.execute("SELECT * FROM injuries WHERE snapshot_at = ?", [ultima]).df()


def cuotas_en(con: duckdb.DuckDBPyConnection, corte: datetime, game_ids: list[str] | None = None) -> pd.DataFrame:
    """Cuotas conocidas antes de `corte` (última captura de cada casa/jugador/mercado/línea/lado).
    Excluye cierres y resultados."""
    filtro = "AND game_id IN (SELECT unnest(?))" if game_ids else ""
    params = [corte, corte] + ([game_ids] if game_ids else [])
    df = con.execute(f"""
        SELECT * EXCLUDE (result) FROM prop_odds
        WHERE ((kind = 'captura' AND snapshot_at < ?) OR (kind = 'apertura' AND start_utc > ?)) {filtro}
        QUALIFY row_number() OVER (PARTITION BY source, book, game_id, source_player_id, stat_id, period, line, side
                                   ORDER BY kind = 'captura' DESC, snapshot_at DESC NULLS LAST) = 1""", params).df()
    return df


def nba_stats_en(con: duckdb.DuckDBPyConnection, fecha: date) -> pd.DataFrame:
    """Última foto acumulada de stats.nba.com anterior al día del partido."""
    return con.execute("""SELECT * FROM nba_stats WHERE date_to < ?
                          QUALIFY row_number() OVER (PARTITION BY endpoint, measure, nba_player_id
                                                     ORDER BY date_to DESC) = 1""", [fecha]).df()


def verificar(df: pd.DataFrame, columna: str, corte: datetime) -> None:
    """Lanza FugaDeDatos si alguna fila tiene `columna` >= corte."""
    if df.empty or columna not in df.columns:
        return
    maximo = pd.to_datetime(df[columna]).max()
    if pd.notna(maximo) and maximo >= pd.Timestamp(corte):
        raise FugaDeDatos(f"{columna} llega hasta {maximo}, posterior o igual al corte {corte}")
