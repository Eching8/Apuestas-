"""Líneas de player props de SportsGameOdds (https://sportsgameodds.com/docs).

Plan gratuito: 2.500 "entidades" (partidos) al mes, así que solo se piden los partidos del día.
Se guarda la línea de consenso (bookOverUnder) y su cuota; las casas concretas solo se cuentan.
"""
from __future__ import annotations

import logging
import os
import re
import unicodedata
from datetime import datetime, timedelta, timezone

import requests

from ..api_football import ApiError

log = logging.getLogger(__name__)

BASE_URL = "https://api.sportsgameodds.com/v2"
# statID de SportsGameOdds -> estadística interna.
STATS_SGO = {
    "points": "points", "rebounds": "rebounds", "assists": "assists", "threePointersMade": "threes",
    "steals": "steals", "blocks": "blocks", "turnovers": "turnovers", "points+rebounds": "pr",
    "points+assists": "pa", "rebounds+assists": "ra", "points+rebounds+assists": "pra",
    "blocks+steals": "stocks", "fieldGoalsMade": "fgm", "freeThrowsMade": "ftm",
    "freeThrowsAttempted": "fta",
}


def clave_nombre(nombre: str) -> str:
    """'Jaren Jackson Jr.' -> 'JAREN_JACKSON_JR'; 'Nikola Jokić' -> 'NIKOLA_JOKIC'."""
    s = unicodedata.normalize("NFKD", nombre or "").encode("ascii", "ignore").decode().upper()
    s = re.sub(r"[.'’]", "", s)
    return re.sub(r"[^A-Z0-9]+", "_", s).strip("_")


def nombre_de_id(player_id: str) -> str:
    """'CJ_MCCOLLUM_1_NBA' -> 'CJ_MCCOLLUM'. Desde el 29 oct 2026 SportsGameOdds no siempre manda el nombre."""
    return re.sub(r"_\d+_NBA$", "", player_id or "")


def americana_a_decimal(v) -> float | None:
    try:
        a = float(str(v).replace("+", ""))
    except (TypeError, ValueError):
        return None
    if a == 0:
        return None
    return round(1 + (a / 100 if a > 0 else 100 / -a), 3)


class SportsGameOdds:
    def __init__(self, api_key: str = "", session: requests.Session | None = None, base_url: str = BASE_URL):
        self.base_url = base_url
        self.session = session or requests.Session()
        if api_key:
            self.session.headers["X-Api-Key"] = api_key
        self.peticiones = 0

    def eventos(self, inicio: datetime, fin: datetime) -> list[dict]:
        """Partidos de la NBA con cuotas que empiezan entre inicio y fin (UTC)."""
        out, cursor = [], None
        while True:
            params = {"leagueID": "NBA", "oddsAvailable": "true", "limit": 25,
                      "startsAfter": inicio.isoformat(), "startsBefore": fin.isoformat()}
            if cursor:
                params["cursor"] = cursor
            resp = self.session.get(f"{self.base_url}/events", params=params, timeout=30)
            self.peticiones += 1
            if resp.status_code == 401:
                raise ApiError("SportsGameOdds rechazó la clave: revisa SPORTSGAMEODDS_KEY en el .env")
            if resp.status_code != 200:
                raise ApiError(f"SportsGameOdds /events: HTTP {resp.status_code} {resp.text[:200]}")
            data = resp.json()
            out += data.get("data", [])
            cursor = data.get("nextCursor")
            if not cursor or not data.get("data"):
                return out


def ventana_dia(fecha: str, zona: str) -> tuple[datetime, datetime]:
    from zoneinfo import ZoneInfo
    ini = datetime.fromisoformat(fecha).replace(hour=6, tzinfo=ZoneInfo(zona))
    return ini.astimezone(timezone.utc), (ini + timedelta(days=1)).astimezone(timezone.utc)


def parse_props(evento: dict) -> list[dict]:
    """Una fila por jugador y estadística con la línea de consenso del partido completo."""
    jugadores = evento.get("players", {})
    lados: dict[tuple[str, str], dict] = {}
    for o in evento.get("odds", {}).values():
        stat = STATS_SGO.get(o.get("statID"))
        if (not stat or not o.get("playerID") or o.get("periodID") != "game" or o.get("betTypeID") != "ou"
                or o.get("cancelled") or not o.get("bookOddsAvailable")):
            continue
        lados.setdefault((o["playerID"], stat), {})[o["sideID"]] = o
    filas = []
    for (pid, stat), par in lados.items():
        over, under = par.get("over"), par.get("under")
        base = over or under
        try:
            linea = float(base["bookOverUnder"])
        except (TypeError, ValueError, KeyError):
            continue
        casas = len((over or {}).get("byBookmaker") or {}) + len((under or {}).get("byBookmaker") or {})
        if not casas:
            # Sin ninguna casa detrás, SportsGameOdds rellena línea y cuota (+100) con valores que no son
            # apostables: el 26 oct 2026 era un tercio de las props, con líneas lejos de las reales.
            continue
        info = jugadores.get(pid, {})
        filas.append({
            "sgo_player_id": pid, "name": info.get("name") or nombre_de_id(pid), "sgo_team_id": info.get("teamID"),
            "stat": stat, "line": linea,
            # Cada lado vale solo si alguna casa lo ofrece; si no, su cuota es relleno (+100).
            "over_odd": americana_a_decimal(over.get("bookOdds")) if over and over.get("byBookmaker") else None,
            "under_odd": americana_a_decimal(under.get("bookOdds")) if under and under.get("byBookmaker") else None,
            "books": max(len((over or {}).get("byBookmaker") or {}), len((under or {}).get("byBookmaker") or {})),
        })
    return filas


def equipos_evento(evento: dict, nombre: str = "long") -> tuple[str, str]:
    """Claves normalizadas de local y visitante: 'long' ('UTAH_JAZZ') o 'medium' (apodo: 'JAZZ')."""
    t = evento.get("teams", {})
    return tuple(clave_nombre((t.get(lado, {}).get("names") or {}).get(nombre, "")) for lado in ("home", "away"))
