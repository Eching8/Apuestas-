"""Respaldo de líneas de player props: The Odds API (https://the-odds-api.com), cuando SportsGameOdds no responde.

Plan gratuito: 500 créditos al mes. Listar los partidos no gasta; las cuotas de un partido cuestan un crédito por
mercado y región, así que con los cuatro mercados de MERCADOS y una región son ~40 créditos en un día de 10
partidos: más de lo que da el plan. Por eso se racionan: cada día se piden solo los partidos que caben en los créditos
restantes repartidos entre los días que faltan del mes, empezando por los más parejos. Por cada jugador y estadística se guarda la línea que más casas ofrecen y la mediana de sus cuotas.
"""
from __future__ import annotations

import logging
import os
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
        self.recortados = False

    def _get(self, ruta: str, **params) -> list | dict:
        resp = self.session.get(f"{self.base_url}{ruta}", params={"apiKey": self.api_key, **params}, timeout=30)
        self.peticiones += 1
        self.restantes = resp.headers.get("x-requests-remaining", self.restantes)
        if resp.status_code == 401:
            raise ApiError("The Odds API rechazó la clave: revisa ODDS_API_KEY")
        if resp.status_code != 200:
            raise ApiError(f"The Odds API {ruta}: HTTP {resp.status_code} {resp.text[:200]}")
        return resp.json()

    def eventos(self, inicio: datetime, fin: datetime, prioridad: dict | None = None) -> list[dict]:
        """Partidos de la NBA entre inicio y fin (UTC) con sus props, en el formato que lee emparejar_props.

        Reparte los créditos que quedan entre los días que faltan del mes (ver partidos_hoy): si no alcanzan para todos
        los partidos, pide primero los de menor valor en `prioridad` ({(clave_local, clave_visita): valor}, p. ej. la
        diferencia esperada: los más parejos, donde los titulares juegan sus minutos)."""
        out = []
        lista = self._get(f"/sports/{DEPORTE}/events", commenceTimeFrom=_iso(inicio), commenceTimeTo=_iso(fin))
        # Con la NHL activada (ODDS_API_NHL=1) los créditos del día se reparten: la NBA se queda con 1 - PARTE_NHL.
        parte = 1 - parte_nhl() if os.environ.get("ODDS_API_NHL") == "1" else 1.0
        maximo = partidos_hoy(self.restantes, inicio, len(self.mercados), parte)
        if maximo is not None and maximo < len(lista):
            prioridad = prioridad or {}
            lista = sorted(lista, key=lambda ev: prioridad.get((clave_nombre(ev["home_team"]),
                                                                clave_nombre(ev["away_team"])), 99.0))[:maximo]
            self.recortados = True
        for ev in lista:
            odds = self._get(f"/sports/{DEPORTE}/events/{ev['id']}/odds", regions=self.regiones,
                             markets=",".join(self.mercados), oddsFormat="decimal")
            out.append({"equipos": [(clave_nombre(ev["home_team"]), clave_nombre(ev["away_team"]))],
                        "props": parse_props(odds)})
        log.info("The Odds API: %d partidos, %s créditos restantes", len(out), self.restantes)
        return out


RESERVA = 8   # créditos que no se tocan (por si hace falta repetir un día)


def parte_nhl() -> float:
    """Parte de la ración diaria de créditos para la NHL cuando ODDS_API_NHL=1 (la NBA se queda con el resto)."""
    try:
        return min(0.5, max(0.0, float(os.environ.get("ODDS_API_NHL_PARTE", "0.3"))))
    except ValueError:
        return 0.3


def partidos_hoy(restantes: str | None, dia: datetime, por_partido: int, parte: float = 1.0) -> int | None:
    """Cuántos partidos se pueden pedir hoy para que los créditos lleguen a fin de mes (None = sin límite conocido).
    `parte`: fracción de la ración del día (la NBA y la NHL comparten los créditos)."""
    try:
        quedan = float(restantes) - RESERVA
    except (TypeError, ValueError):
        return None
    import calendar
    dias = calendar.monthrange(dia.year, dia.month)[1] - dia.day + 1
    return max(0, int(quedan * parte / max(1, dias) / max(1, por_partido)))


def parse_props(evento: dict, mercados: dict[str, str] | None = None) -> list[dict]:
    """Una fila por jugador y estadística: la línea que ofrecen más casas, con la mediana de sus cuotas.
    `mercados`: mercado de The Odds API -> estadística (por defecto, los de la NBA)."""
    mercados = mercados or {**MERCADOS, **MERCADOS_DEFENSIVOS}
    lineas: dict[tuple[str, str], dict[float, dict]] = defaultdict(
        lambda: defaultdict(lambda: {"over": [], "under": [], "casas": set()}))
    for casa in evento.get("bookmakers", []):
        for mercado in casa.get("markets", []):
            stat = mercados.get(mercado.get("key"))
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
