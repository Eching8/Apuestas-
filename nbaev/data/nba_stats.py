"""stats.nba.com vía nba_api: métricas avanzadas y tracking (potential assists, rebound chances, touches).

stats.nba.com bloquea las IPs de servidores en la nube (la conexión se queda colgada), así que en modo
"auto" se hace una prueba corta y, si no responde, se omite sin romper el resto del flujo. Desde una
conexión doméstica funciona. Cada descarga es acumulada hasta `date_to` (inclusive): para predecir un
partido del día D se usan solo filas con date_to < D (ver asof.py).
"""
from __future__ import annotations

import json
import logging
import time
from datetime import date, timedelta

import duckdb

from . import db

log = logging.getLogger(__name__)

# (endpoint, medida) -> parámetros de nba_api
CONSULTAS = {
    ("leaguedashplayerstats", "Advanced"): {"measure_type_detailed_defense": "Advanced"},
    ("leaguedashptstats", "Passing"): {"pt_measure_type": "Passing"},
    ("leaguedashptstats", "Rebounding"): {"pt_measure_type": "Rebounding"},
    ("leaguedashptstats", "Possessions"): {"pt_measure_type": "Possessions"},
}

_disponible: bool | None = None


def temporada_nba(season: int) -> str:
    """2021 -> '2021-22'."""
    return f"{season}-{(season + 1) % 100:02d}"


def disponible(cfg: dict) -> bool:
    """Prueba (una vez por ejecución) si stats.nba.com responde desde esta red."""
    global _disponible
    modo = cfg["fuentes"]["nba_api"]["modo"]
    if modo == "no":
        return False
    if _disponible is None:
        try:
            from nba_api.stats.endpoints import leaguegamelog
            leaguegamelog.LeagueGameLog(season="2024-25", timeout=min(cfg["fuentes"]["nba_api"]["timeout_s"], 15))
            _disponible = True
        except Exception as e:  # timeout, conexión cortada, 403...
            log.warning("stats.nba.com no responde desde esta red (%s). Métricas de tracking omitidas.",
                        type(e).__name__)
            _disponible = False
    return _disponible or modo == "si"


def _pedir(endpoint: str, params: dict, season: int, date_to: date | None, timeout: float):
    from nba_api.stats.endpoints import leaguedashplayerstats, leaguedashptstats
    comunes = {"season": temporada_nba(season), "season_type_all_star": "Regular Season", "timeout": timeout,
               "per_mode_simple" if endpoint == "leaguedashptstats" else "per_mode_detailed": "PerGame"}
    if date_to:
        comunes["date_to_nullable"] = date_to.strftime("%m/%d/%Y")
    if endpoint == "leaguedashplayerstats":
        r = leaguedashplayerstats.LeagueDashPlayerStats(**comunes, **params)
    else:
        r = leaguedashptstats.LeagueDashPtStats(player_or_team="Player", **comunes, **params)
    return r.get_data_frames()[0]


def descargar(con: duckdb.DuckDBPyConnection, cfg: dict, season: int, hasta: str | None) -> dict:
    """Descarga las consultas de CONSULTAS acumuladas hasta `hasta` (por defecto ayer)."""
    if not disponible(cfg):
        return {"disponible": False}
    c = cfg["fuentes"]["nba_api"]
    date_to = date.fromisoformat(hasta) if hasta else date.today() - timedelta(days=1)
    ahora, n = db.ahora_utc(), 0
    for (endpoint, medida), params in CONSULTAS.items():
        try:
            df = _pedir(endpoint, params, season, date_to, c["timeout_s"])
        except Exception as e:
            log.error("stats.nba.com %s/%s: %s", endpoint, medida, e)
            db.registrar(con, "nba_api", f"{endpoint}:{medida}:{season}:{date_to}", "error", str(e))
            continue
        filas = [{"endpoint": endpoint, "measure": medida, "season": season, "date_to": date_to,
                  "nba_player_id": str(r["PLAYER_ID"]), "player_name": r.get("PLAYER_NAME"),
                  "team_abbr": r.get("TEAM_ABBREVIATION"), "datos": json.dumps(r, default=str), "fetched_at": ahora}
                 for r in df.to_dict("records")]
        n += db.upsert(con, "nba_stats", filas)
        db.registrar(con, "nba_api", f"{endpoint}:{medida}:{season}:{date_to}", "ok", f"{len(filas)} filas")
        time.sleep(c["min_intervalo_s"])
    return {"disponible": True, "filas": n, "date_to": str(date_to)}
