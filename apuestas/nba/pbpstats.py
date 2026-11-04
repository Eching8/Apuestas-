"""pbpstats.com: estadísticas de jugada por jugada que ESPN no da y stats.nba.com no deja bajar desde la nube.

- Rebotes disponibles: qué % de los rebotes defensivos y ofensivos que caen con el jugador en pista se queda
  (DefFGReboundPct, OffFGReboundPct): la "conversión" de sus oportunidades de rebote.
- Transición: posesiones que empiezan tras un robo (StartType=OffLiveBallTurnover). Para cada equipo, los puntos
  que anota así y los que concede (Type=Opponent). Por jugador pbpstats no filtra por cómo empieza la posesión.

Se baja una vez al día (4 peticiones) y se guarda en la tabla nba_pbp. Si pbpstats no responde, el informe sale
igual sin estos datos.
"""
from __future__ import annotations

import json
import logging
import time

import requests

from ..db import now_iso
from .sgo import clave_nombre

log = logging.getLogger(__name__)

URL = "https://api.pbpstats.com/get-totals/nba"
# pbpstats usa las siglas de la NBA; ESPN, algunas distintas.
SIGLAS_ESPN = {"NYK": "NY", "GSW": "GS", "SAS": "SA", "NOP": "NO", "UTA": "UTAH", "WAS": "WSH"}
CONSULTAS = {
    "jugadores": {"Type": "Player"},
    "equipos": {"Type": "Team"},
    "equipos_transicion": {"Type": "Team", "StartType": "OffLiveBallTurnover"},
    "rivales_transicion": {"Type": "Opponent", "StartType": "OffLiveBallTurnover"},
}

SCHEMA = """
CREATE TABLE IF NOT EXISTS nba_pbp (
    clave TEXT,
    temporada INTEGER,
    datos TEXT,
    updated_at TEXT,
    PRIMARY KEY (clave, temporada)
);
"""


def temporada_pbp(season_espn: int) -> str:
    return f"{season_espn - 1}-{str(season_espn)[-2:]}"


def descargar(conn, season_espn: int, session: requests.Session | None = None, timeout: float = 30,
              pausa: float = 2.0) -> int:
    """Baja las consultas de CONSULTAS y las guarda. Devuelve cuántas se guardaron."""
    conn.executescript(SCHEMA)
    s = session or requests.Session()
    n = 0
    for clave, params in CONSULTAS.items():
        filas = []
        for intento in range(3):
            try:
                resp = s.get(URL, params={"Season": temporada_pbp(season_espn), "SeasonType": "Regular Season",
                                          **params}, headers={"User-Agent": "Mozilla/5.0"}, timeout=timeout)
                resp.raise_for_status()
                filas = resp.json().get("multi_row_table_data") or []
                break
            except Exception as exc:   # sin estos datos el análisis sigue
                log.warning("pbpstats %s (intento %d): %s", clave, intento + 1, exc)
                time.sleep(pausa * (intento + 1))
        time.sleep(pausa)
        if not filas:
            continue
        conn.execute("INSERT OR REPLACE INTO nba_pbp (clave, temporada, datos, updated_at) VALUES (?, ?, ?, ?)",
                     (clave, season_espn, json.dumps(filas), now_iso()))
        n += 1
    conn.commit()
    return n


def cargar(conn, season_espn: int) -> dict:
    """{"jugadores": {CLAVE_NOMBRE: fila}, "jugadores_transicion": {...}, "equipos": {SIGLA_ESPN: fila}, ...}."""
    try:
        filas = conn.execute("SELECT clave, datos FROM nba_pbp WHERE temporada = ?", (season_espn,)).fetchall()
    except Exception:
        return {}
    out = {}
    for clave, datos in filas:
        lista = json.loads(datos)
        if clave.startswith("jugadores"):
            out[clave] = {clave_nombre(f.get("Name", "")): f for f in lista}
        else:
            out[clave] = {SIGLAS_ESPN.get(f.get("Name"), f.get("Name")): f for f in lista}
    return out


def por_partido(fila: dict, campo: str, partidos: float | None = None) -> float | None:
    g = partidos or fila.get("GamesPlayed")
    v = fila.get(campo)
    return v / g if v is not None and g else None
