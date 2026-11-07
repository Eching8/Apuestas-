"""Líneas de props de la NHL con The Odds API, solo con ODDS_API_NHL=1.

El plan gratuito (500 créditos al mes) lo comparte con la NBA: con la NHL activada, la ración diaria (créditos que
quedan entre los días que faltan del mes, `nba.theodds.partidos_hoy`) se reparte y la NHL se queda con
ODDS_API_NHL_PARTE (0.3 por defecto, máximo 0.5); la NBA, con el resto. Cada partido cuesta un crédito por mercado:
por defecto solo tiros a puerta y puntos; ODDS_API_NHL_EXTRA=1 añade asistencias, tiros bloqueados y paradas (más
créditos). Si no alcanza para todos, se piden primero los partidos más parejos.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime

import requests

from ..api_football import ApiError
from ..nba.sgo import clave_nombre
from ..nba.theodds import BASE_URL, _iso, parte_nhl, partidos_hoy
from ..nba import theodds as nba_theodds

log = logging.getLogger(__name__)

DEPORTE = "icehockey_nhl"
MERCADOS = {"player_shots_on_goal": "shots", "player_points": "points"}
MERCADOS_EXTRA = {"player_assists": "assists", "player_blocked_shots": "blocked", "player_total_saves": "saves"}


def activada() -> bool:
    return os.environ.get("ODDS_API_NHL") == "1"


class TheOddsApiNhl:
    def __init__(self, api_key: str, session: requests.Session | None = None, base_url: str = BASE_URL,
                 regiones: str = "us", extra: bool | None = None):
        self.api_key = api_key
        extra = os.environ.get("ODDS_API_NHL_EXTRA") == "1" if extra is None else extra
        self.mercados = {**MERCADOS, **(MERCADOS_EXTRA if extra else {})}
        self.session = session or requests.Session()
        self.base_url = base_url
        self.regiones = regiones
        self.peticiones = 0
        self.restantes: str | None = None
        self.recortados = False

    def _get(self, ruta: str, **params):
        resp = self.session.get(f"{self.base_url}{ruta}", params={"apiKey": self.api_key, **params}, timeout=30)
        self.peticiones += 1
        self.restantes = resp.headers.get("x-requests-remaining", self.restantes)
        if resp.status_code == 401:
            raise ApiError("The Odds API rechazó la clave: revisa ODDS_API_KEY")
        if resp.status_code != 200:
            raise ApiError(f"The Odds API {ruta}: HTTP {resp.status_code} {resp.text[:200]}")
        return resp.json()

    def eventos(self, inicio: datetime, fin: datetime, prioridad: dict | None = None) -> list[dict]:
        lista = self._get(f"/sports/{DEPORTE}/events", commenceTimeFrom=_iso(inicio), commenceTimeTo=_iso(fin))
        maximo = partidos_hoy(self.restantes, inicio, len(self.mercados), parte_nhl())
        if maximo is not None and maximo < len(lista):
            prioridad = prioridad or {}
            lista = sorted(lista, key=lambda ev: prioridad.get((clave_nombre(ev["home_team"]),
                                                                clave_nombre(ev["away_team"])), 99.0))[:maximo]
            self.recortados = True
        out = []
        for ev in lista:
            odds = self._get(f"/sports/{DEPORTE}/events/{ev['id']}/odds", regions=self.regiones,
                             markets=",".join(self.mercados), oddsFormat="decimal")
            out.append({"equipos": [(clave_nombre(ev["home_team"]), clave_nombre(ev["away_team"]))],
                        "props": parse_props(odds)})
        log.info("The Odds API (NHL): %d partidos, %s créditos restantes", len(out), self.restantes)
        return out


def parse_props(evento: dict) -> list[dict]:
    """Igual que la NBA (la línea que más casas ofrecen y la mediana de sus cuotas), con los mercados de la NHL."""
    return nba_theodds.parse_props(evento, {**MERCADOS, **MERCADOS_EXTRA})
