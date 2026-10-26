"""Informe de cobertura y calidad de la base (python -m nbaev datos estado)."""
from __future__ import annotations

import duckdb
import pandas as pd


def _tabla(df: pd.DataFrame) -> str:
    if df.empty:
        return "(vacío)\n"
    return df.to_markdown(index=False, floatfmt=".3f") + "\n"


def informe(con: duckdb.DuckDBPyConnection) -> str:
    out = ["# Estado de los datos\n"]
    tipos = "CASE season_type WHEN 2 THEN 'regular' WHEN 3 THEN 'playoffs' WHEN 5 THEN 'play-in' END"
    out.append("## Partidos por temporada\n")
    out.append(_tabla(con.execute(f"""
        SELECT season || '-' || lpad(CAST((season + 1) % 100 AS VARCHAR), 2, '0') AS temporada, {tipos} AS tipo,
               count(*) AS partidos, sum(CAST(status = 'STATUS_FINAL' AS INT)) AS terminados,
               sum(CAST(box_ok AS INT)) AS con_box, sum(CAST(pbp_ok AS INT)) AS con_jugadas,
               min(fecha) AS desde, max(fecha) AS hasta
        FROM games GROUP BY ALL ORDER BY 1, 2""").df()))

    out.append("## Jugada a jugada frente al box score\n")
    out.append("Fracción de jugadores cuya suma por cuartos coincide exactamente con el box score, y error de "
               "los minutos reconstruidos con los cambios (el box de ESPN redondea los minutos al entero).\n\n")
    out.append(_tabla(con.execute("""
        SELECT g.season AS temporada, count(*) AS partidos, avg(ok_pts) AS pts, avg(ok_oreb) AS oreb,
               avg(ok_dreb) AS dreb, avg(ok_ast) AS ast, avg(ok_fg3m) AS fg3m, avg(ok_stl) AS stl,
               avg(ok_blk) AS blk, avg(ok_tov) AS tov, avg(ok_ftm) AS ftm, avg(mae_min) AS mae_minutos,
               quantile_cont(max_err_min, 0.99) AS p99_err_max_min
        FROM pbp_quality q JOIN games g USING (game_id) GROUP BY 1 ORDER BY 1""").df()))

    out.append("## Primer anotador y salto inicial\n")
    out.append(_tabla(con.execute("""
        SELECT g.season AS temporada, count(*) AS partidos,
               avg(CAST(jump_winner_team IS NOT NULL AS INT)) AS con_salto,
               avg(CAST(first_fg_player IS NOT NULL AS INT)) AS con_primera_canasta,
               avg(CAST(len(home_starters) = 5 AND len(away_starters) = 5 AS INT)) AS con_titulares,
               avg(CAST(first_fg_team = jump_winner_team AS INT)) AS gana_salto_anota_primero
        FROM game_starts s JOIN games g USING (game_id) GROUP BY 1 ORDER BY 1""").df()))

    out.append("## Líneas del partido (spread y total)\n")
    out.append(_tabla(con.execute("""
        SELECT g.season AS temporada, l.source AS fuente, l.kind AS tipo, count(*) AS partidos,
               avg(CAST(l.total IS NOT NULL AS INT)) AS con_total, avg(CAST(l.spread_home IS NOT NULL AS INT)) AS con_spread
        FROM game_lines l JOIN games g USING (game_id) GROUP BY ALL ORDER BY 1, 2, 3""").df()))

    out.append("## Cuotas de props\n")
    out.append(_tabla(con.execute("""
        SELECT source AS fuente, kind AS tipo, book AS casa, count(DISTINCT game_id) AS partidos,
               count(*) AS cuotas, avg(CAST(player_id IS NOT NULL AS INT)) AS jugador_emparejado,
               min(start_utc)::DATE AS desde, max(start_utc)::DATE AS hasta
        FROM prop_odds GROUP BY ALL ORDER BY 1, 2, 3""").df()))

    out.append("## Catálogo de mercados\n")
    out.append(_tabla(con.execute("""
        SELECT source AS fuente, stat_id, period AS periodo, bet_type AS tipo, market AS mercado, modelado,
               estado, veces FROM market_catalog ORDER BY modelado DESC, veces DESC""").df()))

    out.append("## Otras fuentes\n")
    out.append(_tabla(con.execute("""
        SELECT 'lesiones (capturas)' AS dato, count(DISTINCT snapshot_at) AS n, max(snapshot_at)::VARCHAR AS ultima FROM injuries
        UNION ALL SELECT 'alineaciones (capturas)', count(DISTINCT snapshot_at), max(snapshot_at)::VARCHAR FROM lineups
        UNION ALL SELECT 'ausencias en box score', count(*), NULL FROM player_absences
        UNION ALL SELECT 'stats.nba.com (filas)', count(*), max(fetched_at)::VARCHAR FROM nba_stats
        UNION ALL SELECT 'tiros con zona', count(*), NULL FROM shots
        UNION ALL SELECT 'tramos de quinteto', count(*), NULL FROM stints""").df()))

    errores = con.execute("SELECT source, key, detail FROM ingest_log WHERE status = 'error' LIMIT 20").df()
    if not errores.empty:
        out.append("## Errores de descarga\n")
        out.append(_tabla(errores))
    return "\n".join(out)
