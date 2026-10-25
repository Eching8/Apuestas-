"""Cliente de stats.nba.com: quién defendió a quién (boxscorematchupsv3) y estadísticas avanzadas.

stats.nba.com no responde a servidores en la nube (las peticiones se quedan colgadas): hay que
ejecutarlo desde una conexión de casa (tu computadora o un runner de GitHub Actions instalado en ella).
Los ids de jugador y partido de la NBA no son los de ESPN: se emparejan por fecha, apodo del equipo
y nombre normalizado.
"""
from __future__ import annotations

import logging
import os
import time
from typing import Any

import requests

from ..api_football import ApiError

log = logging.getLogger(__name__)

BASE_URL = "https://stats.nba.com/stats"
MIN_INTERVALO = float(os.environ.get("APUESTAS_NBA_STATS_INTERVALO", 0.8))
CABECERAS = {
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/124.0 Safari/537.36"),
    "Referer": "https://www.nba.com/", "Origin": "https://www.nba.com",
    "Accept": "application/json, text/plain, */*", "Accept-Language": "en-US,en;q=0.9",
    "x-nba-stats-origin": "stats", "x-nba-stats-token": "true",
}
TIPOS = {2: "Regular Season", 3: "Playoffs"}


def temporada_nba(season_espn: int) -> str:
    """ESPN llama 2026 a la temporada 2025-26."""
    return f"{season_espn - 1}-{str(season_espn)[-2:]}"


class NbaStats:
    def __init__(self, session: requests.Session | None = None, base_url: str = BASE_URL, timeout: float = 40):
        self.base_url = base_url
        self.session = session or requests.Session()
        self.session.headers.update(CABECERAS)
        self.timeout = timeout
        self.peticiones = 0
        self._ultima = 0.0

    def _get(self, path: str, **params: Any) -> dict:
        for intento in range(4):
            espera = MIN_INTERVALO - (time.monotonic() - self._ultima)
            if espera > 0:
                time.sleep(espera)
            self._ultima = time.monotonic()
            try:
                resp = self.session.get(f"{self.base_url}/{path}", params=params, timeout=self.timeout)
            except requests.RequestException as e:
                log.warning("stats.nba.com %s: %s (reintento %d)", path, e, intento + 1)
                time.sleep(5 * (intento + 1))
                continue
            self.peticiones += 1
            if resp.status_code in (429, 500, 502, 503, 504):
                time.sleep(10 * (intento + 1))
                continue
            if resp.status_code != 200:
                raise ApiError(f"stats.nba.com {path} {params}: HTTP {resp.status_code}")
            return resp.json()
        raise ApiError(f"stats.nba.com {path}: sin respuesta. Si estás en un servidor en la nube, la NBA lo "
                       "bloquea: ejecútalo desde tu computadora.")

    def partidos(self, season_espn: int, season_type: int) -> list[dict]:
        """Una fila por equipo y partido: GAME_ID, GAME_DATE, TEAM_NAME, MATCHUP..."""
        data = self._get("leaguegamelog", Counter=0, Direction="ASC", LeagueID="00", PlayerOrTeam="T",
                         Season=temporada_nba(season_espn), SeasonType=TIPOS[season_type], Sorter="DATE",
                         DateFrom="", DateTo="")
        return _filas(data)

    def enfrentamientos(self, game_id: str) -> dict:
        return self._get("boxscorematchupsv3", GameID=game_id, LeagueID="00", startPeriod=0, endPeriod=0)

    def avanzadas(self, season_espn: int, season_type: int) -> list[dict]:
        vacios = ("College", "Conference", "Country", "DateFrom", "DateTo", "Division", "DraftPick", "DraftYear",
                  "GameScope", "GameSegment", "Height", "Location", "Outcome", "PlayerExperience", "PlayerPosition",
                  "SeasonSegment", "ShotClockRange", "StarterBench", "VsConference", "VsDivision", "Weight")
        data = self._get("leaguedashplayerstats", MeasureType="Advanced", PerMode="PerGame", LeagueID="00",
                         Season=temporada_nba(season_espn), SeasonType=TIPOS[season_type], LastNGames=0, Month=0,
                         OpponentTeamID=0, PORound=0, PaceAdjust="N", PlusMinus="N", Rank="N", Period=0, TeamID=0,
                         TwoWay=0, **{k: "" for k in vacios})
        return _filas(data)


def _filas(data: dict) -> list[dict]:
    sets = data.get("resultSets") or data.get("resultSet") or []
    if isinstance(sets, dict):
        sets = [sets]
    if not sets:
        return []
    return [dict(zip(sets[0]["headers"], r)) for r in sets[0]["rowSet"]]


def _minutos(v) -> float:
    if isinstance(v, (int, float)):
        return float(v)
    if v and ":" in str(v):
        m, s = str(v).split(":", 1)
        return int(m) + float(s) / 60
    return float(v or 0)


def parse_enfrentamientos(data: dict) -> list[dict]:
    """Una fila por atacante y defensor. En boxscorematchupsv3 cada jugador de un equipo es el atacante
    y sus "matchups" son los defensores rivales que lo marcaron."""
    caja = data.get("boxScoreMatchups") or {}
    filas = []
    for lado in ("homeTeam", "awayTeam"):
        equipo = caja.get(lado) or {}
        for jug in equipo.get("players", []):
            for m in jug.get("matchups", []):
                st = m.get("statistics") or {}
                filas.append({
                    "nba_game_id": caja.get("gameId"), "team_nick": equipo.get("teamName"),
                    "off_nba_id": jug.get("personId"),
                    "off_name": f"{jug.get('firstName', '')} {jug.get('familyName', '')}".strip(),
                    "off_pos": jug.get("position") or "",
                    "def_nba_id": m.get("personId"),
                    "def_name": f"{m.get('firstName', '')} {m.get('familyName', '')}".strip(),
                    "minutos": _minutos(st.get("matchupMinutes")),
                    "posesiones": float(st.get("partialPossessions") or 0),
                    "pts": float(st.get("playerPoints") or 0),
                    "fgm": int(st.get("matchupFieldGoalsMade") or 0),
                    "fga": int(st.get("matchupFieldGoalsAttempted") or 0),
                    "tpm": int(st.get("matchupThreePointersMade") or 0),
                    "tpa": int(st.get("matchupThreePointersAttempted") or 0),
                    "ftm": int(st.get("matchupFreeThrowsMade") or 0),
                    "ast": int(st.get("matchupAssists") or 0),
                    "tov": int(st.get("matchupTurnovers") or 0),
                    "blk": int(st.get("matchupBlocks") or 0),
                })
    return filas
