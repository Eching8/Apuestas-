"""Respaldo de líneas de player props: The Odds API (https://the-odds-api.com), cuando SportsGameOdds no responde.

Plan gratuito: 500 créditos al mes. Listar los partidos no gasta; las cuotas de un partido cuestan un crédito por
mercado y región, así que con los cuatro mercados de MERCADOS y una región son ~40 créditos en un día de 10
partidos. Por cada jugador y estadística se guarda la línea que más casas ofrecen y la mediana de sus cuotas.
"""
from __future__ import annotations

import logging
from collections import defaultdict
from datetime import datetime
from statistics import median

import requests

from ..api_football import ApiError
from .sgo import clave_nombre

log = logging.getLogger(__name__)

BASE_URL = "https://api.the-odds-api.com/v4"
DEPORTE = "basketball_nba"
# Mercado de The Odds API -> estadística interna. Los combinados (player_points_rebounds_assists...) también existen,
# pero cada uno cuesta un crédito más por partido.
MERCADOS = {"player_points": "points", "player_rebounds": "rebounds", "player_assists": "assists",
            "player_threes": "threes"}
# Defensivas y pérdidas: cuestan un crédito más por partido cada una, así que solo se piden con
# ODDS_API_DEFENSIVAS=1 (con el plan gratuito de 500 créditos no alcanza ni para los cuatro de arriba todo el mes).
MERCADOS_DEFENSIVOS = {"player_steals": "steals", "player_blocks": "blocks", "player_blocks_steals": "stocks",
                       "player_turnovers": "turnovers"}


def _iso(t: datetime) -> str:
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


class TheOddsApi:
    def __init__(self, api_key: str, session: requests.Session | None = None, base_url: str = BASE_URL,
                 regiones: str = "us", defensivas: bool = False):
        self.api_key = api_key
        self.mercados = {**MERCADOS, **(MERCADOS_DEFENSIVOS if defensivas else {})}
        self.session = session or requests.Session()
        self.base_url = base_url
        self.regiones = regiones
        self.peticiones = 0
        self.restantes: str | None = None

    def _get(self, ruta: str, **params) -> list | dict:
        resp = self.session.get(f"{self.base_url}{ruta}", params={"apiKey": self.api_key, **params}, timeout=30)
        self.peticiones += 1
        self.restantes = resp.headers.get("x-requests-remaining", self.restantes)
        if resp.status_code == 401:
            raise ApiError("The Odds API rechazó la clave: revisa ODDS_API_KEY")
        if resp.status_code != 200:
            raise ApiError(f"The Odds API {ruta}: HTTP {resp.status_code} {resp.text[:200]}")
        return resp.json()

    def eventos(self, inicio: datetime, fin: datetime) -> list[dict]:
        """Partidos de la NBA entre inicio y fin (UTC) con sus props, en el formato que lee emparejar_props."""
        out = []
        for ev in self._get(f"/sports/{DEPORTE}/events", commenceTimeFrom=_iso(inicio), commenceTimeTo=_iso(fin)):
            odds = self._get(f"/sports/{DEPORTE}/events/{ev['id']}/odds", regions=self.regiones,
                             markets=",".join(self.mercados), oddsFormat="decimal")
            out.append({"equipos": [(clave_nombre(ev["home_team"]), clave_nombre(ev["away_team"]))],
                        "props": parse_props(odds)})
        log.info("The Odds API: %d partidos, %s créditos restantes", len(out), self.restantes)
        return out


def parse_props(evento: dict) -> list[dict]:
    """Una fila por jugador y estadística: la línea que ofrecen más casas, con la mediana de sus cuotas."""
    lineas: dict[tuple[str, str], dict[float, dict]] = defaultdict(
        lambda: defaultdict(lambda: {"over": [], "under": [], "casas": set()}))
    for casa in evento.get("bookmakers", []):
        for mercado in casa.get("markets", []):
            stat = MERCADOS.get(mercado.get("key")) or MERCADOS_DEFENSIVOS.get(mercado.get("key"))
            if not stat:
                continue
            for o in mercado.get("outcomes", []):
                lado, jugador, punto = (o.get("name") or "").lower(), o.get("description"), o.get("point")
                if lado not in ("over", "under") or not jugador or punto is None or not o.get("price"):
                    continue
                celda = lineas[(jugador, stat)][float(punto)]
                celda[lado].append(float(o["price"]))
                celda["casas"].add(casa.get("key"))
    filas = []
    for (jugador, stat), por_linea in lineas.items():
        centro = median(por_linea)
        linea, celda = max(por_linea.items(), key=lambda kv: (len(kv[1]["casas"]), -abs(kv[0] - centro)))
        filas.append({"sgo_player_id": None, "name": jugador, "sgo_team_id": None, "stat": stat, "line": linea,
                      "over_odd": round(median(celda["over"]), 3) if celda["over"] else None,
                      "under_odd": round(median(celda["under"]), 3) if celda["under"] else None,
                      "books": len(celda["casas"])})
    return filas
