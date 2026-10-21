"""Fuente SportsGameOdds (https://sportsgameodds.com): cuotas de córners, tarjetas, tiros y más.

Plan gratuito "Amateur": 10 peticiones por minuto y **2.500 objetos al mes** (cada partido devuelto
cuenta como un objeto). En fútbol solo incluye **Champions League** (y MLS): el resto de ligas
responde 400. Se usa para lo que ninguna otra fuente gratuita da —cuotas de córners, tarjetas, tiros
y atajadas de 8 casas— una vez al día y solo si hay partidos de esas ligas. Antes de pedir nada se
consulta el consumo real en `/account/usage` (no gasta objetos) y se corta en `SGO_MAX_MES`.

Clave en `SGO_API_KEY` o, en la nube, como *network secret* para `api.sportsgameodds.com` con la
cabecera `x-api-key` (sin prefijo).

Las cuotas se identifican por oddID = `{statID}-{entidad}-{periodo}-{tipo}-{lado}`. statID de fútbol
vistos (octubre de 2026): points (goles), cornerKicks, weightedCards (tarjetas; la roja puede pesar
más que la amarilla, así que es una aproximación a nuestro "amarillas + rojas"), shots, shots_onGoal,
goalie_saves y bothTeamsScored. Los desconocidos se registran en el log.
"""
from __future__ import annotations

import logging
import os
import re
import time
from datetime import date, datetime, timedelta, timezone

import requests

from .api_football import ApiError, PresupuestoAgotado
from .espn import americana_a_decimal
from .registro import Registro

log = logging.getLogger(__name__)

BASE_URL = "https://api.sportsgameodds.com/v2"
MAX_MES = int(os.environ.get("SGO_MAX_MES", 2000))           # el plan permite 2.500
MIN_INTERVALO = 6.5                                            # 10 por minuto

# Nombre de liga (en minúsculas, fragmentos) -> id de liga de la configuración (API-Football).
LIGAS = {
    39: ("premier league", "epl"), 140: ("la liga", "laliga"), 78: ("bundesliga",), 71: ("brasil", "brazil"),
    2: ("champions league",), 3: ("europa league",), 848: ("conference league",), 13: ("libertadores",),
    11: ("sudamericana",), 239: ("colombia",), 16: ("concacaf",),
}
# statID normalizado (solo letras) -> estadística del modelo. El orden importa: lo más específico antes.
STATS = [
    ("bothteams", "btts"), ("corner", "corners"), ("yellowcard", "cards"), ("card", "cards"), ("booking", "cards"),
    ("shotsongoal", "shots_on"), ("shotsontarget", "shots_on"), ("ontarget", "shots_on"),
    ("save", "saves"), ("shot", "shots_total"),
]
# Estadística -> nombre de la apuesta en API-Football (lo que espera odds.BETS) por ámbito.
APUESTAS = {
    ("goals", "total"): "Goals Over/Under", ("goals", "home"): "Total - Home", ("goals", "away"): "Total - Away",
    ("corners", "total"): "Corners Over Under", ("corners", "home"): "Home Corners Over/Under",
    ("corners", "away"): "Away Corners Over/Under", ("cards", "total"): "Cards Over/Under",
    ("cards", "home"): "Home Cards Over/Under", ("cards", "away"): "Away Cards Over/Under",
    ("shots_on", "total"): "Total ShotOnGoal", ("shots_on", "home"): "Home ShotOnGoal",
    ("shots_on", "away"): "Away ShotOnGoal", ("shots_total", "total"): "Total Shots",
    ("shots_total", "home"): "Home Total Shots", ("shots_total", "away"): "Away Total Shots",
    ("saves", "total"): "Total Goalkeeper Saves", ("saves", "home"): "Home Goalkeeper Saves",
    ("saves", "away"): "Away Goalkeeper Saves",
}
ENTIDAD = {"all": "total", "home": "home", "away": "away"}


def stat_de(stat_id: str) -> str | None:
    s = re.sub(r"[^a-z]", "", stat_id.lower())
    if s == "points":
        return "goals"
    for fragmento, stat in STATS:
        if fragmento in s:
            return stat
    return None


def cuotas_de_evento(ev: dict) -> list[tuple[str, str, str, float]]:
    """Evento de SGO -> filas (casa, apuesta, valor, cuota decimal) en el formato de API-Football."""
    filas, desconocidos = [], set()
    for odd in (ev.get("odds") or {}).values():
        if odd.get("periodID") != "game" or odd.get("playerID"):
            continue
        tipo, lado, stat_id = odd.get("betTypeID"), odd.get("sideID"), odd.get("statID", "")
        stat = stat_de(stat_id)
        for casa, b in (odd.get("byBookmaker") or {}).items():
            if not b.get("available", True):
                continue
            cuota = americana_a_decimal(b.get("odds"))
            if cuota is None:
                continue
            if stat == "goals" and tipo == "ml3way" and lado in ("home", "draw", "away"):
                filas.append((casa, "Match Winner", {"home": "Home", "draw": "Draw", "away": "Away"}[lado], cuota))
            elif stat == "btts" and tipo == "yn" and lado in ("yes", "no"):
                filas.append((casa, "Both Teams Score", lado.capitalize(), cuota))
            elif stat and tipo == "ou" and lado in ("over", "under"):
                apuesta = APUESTAS.get((stat, ENTIDAD.get(odd.get("statEntityID", ""), "")))
                linea = b.get("overUnder") or odd.get("bookOverUnder")
                if apuesta and linea is not None:
                    filas.append((casa, apuesta, f"{lado.capitalize()} {float(linea):g}", cuota))
            elif stat is None:
                desconocidos.add(stat_id)
    if desconocidos:
        log.debug("SportsGameOdds: statID sin usar %s", sorted(desconocidos))
    return filas


def evento_basico(ev: dict) -> dict:
    equipos = ev.get("teams") or {}
    nombre = lambda lado: ((equipos.get(lado) or {}).get("names") or {}).get("long", "")
    return {"id": ev.get("eventID"), "local": nombre("home"), "visitante": nombre("away"),
            "inicio": (ev.get("status") or {}).get("startsAt"), "cuotas": cuotas_de_evento(ev)}


class SportsGameOdds:
    def __init__(self, api_key: str = "", session: requests.Session | None = None, registro: Registro | None = None,
                 max_mes: int = MAX_MES, base_url: str = BASE_URL):
        self.session = session or requests.Session()
        if api_key:
            self.session.headers.update({"x-api-key": api_key})
        self.base_url = base_url
        self.registro = registro
        self.max_mes = max_mes
        self.peticiones = 0
        self._ultima = 0.0

    def uso_servidor(self) -> int | None:
        """Objetos usados este mes según SportsGameOdds (consultarlo no gasta objetos)."""
        resp = self.session.get(f"{self.base_url}/account/usage", timeout=30)
        if resp.status_code in (401, 403):
            raise ApiError("SportsGameOdds rechaza la clave: falta SGO_API_KEY o el network secret")
        resp.raise_for_status()
        mes = (((resp.json().get("data") or {}).get("rateLimits") or {}).get("per-month") or {})
        valor = mes.get("current-entities")
        return int(valor) if isinstance(valor, (int, float)) or str(valor).isdigit() else None

    def _sincronizar(self) -> int:
        """Lo usado este mes: lo más alto entre el registro propio y el contador del servidor."""
        propio = self.registro.usadas() if self.registro else 0
        try:
            servidor = self.uso_servidor()
        except requests.RequestException:
            servidor = None
        if servidor is not None and servidor > propio and self.registro:
            self.registro.sumar(servidor - propio)
            propio = servidor
        return propio

    def _get(self, path: str, coste: int = 1, **params) -> dict:
        usados = self.registro.usadas() if self.registro else 0
        if usados + coste > self.max_mes:
            raise PresupuestoAgotado(f"SportsGameOdds: tope mensual propio de {self.max_mes} objetos alcanzado")
        espera = MIN_INTERVALO - (time.monotonic() - self._ultima)
        if espera > 0:
            time.sleep(espera)
        self._ultima = time.monotonic()
        self.peticiones += 1
        resp = self.session.get(f"{self.base_url}{path}", params=params, timeout=30)
        if resp.status_code in (401, 403):
            raise ApiError("SportsGameOdds rechaza la clave: falta SGO_API_KEY o el network secret")
        if resp.status_code == 429:
            raise PresupuestoAgotado("SportsGameOdds: límite del plan alcanzado")
        resp.raise_for_status()
        data = resp.json()
        if self.registro:
            # Cada objeto devuelto cuenta (mínimo 1 por respuesta).
            self.registro.sumar(max(1, len(data.get("data") or []) if isinstance(data.get("data"), list) else 1))
        return data

    def disponible(self) -> str:
        usados = self._sincronizar()
        return f"OK (plan gratuito: {usados} de 2500 objetos usados este mes; tope propio {self.max_mes})"

    def ligas(self) -> dict[int, str]:
        """id de liga de la configuración -> leagueID de SGO (por nombre)."""
        out = {}
        for liga in self._get("/leagues/", sportID="SOCCER").get("data") or []:
            nombre = (liga.get("name") or liga.get("long") or "").lower() + " " + (liga.get("leagueID") or "").lower()
            for nuestro, claves in LIGAS.items():
                if nuestro not in out and any(c in nombre for c in claves):
                    out[nuestro] = liga["leagueID"]
        return out

    def partidos(self, league_ids: list[str], desde: datetime, hasta: datetime, max_objetos: int = 60) -> list[dict]:
        if not league_ids:
            return []
        self._sincronizar()
        out, cursor = [], None
        while len(out) < max_objetos:
            params = {"leagueID": ",".join(league_ids), "oddsAvailable": "true",
                      "startsAfter": desde.isoformat(), "startsBefore": hasta.isoformat(),
                      "limit": min(25, max_objetos - len(out))}
            if cursor:
                params["cursor"] = cursor
            data = self._get("/events/", coste=params["limit"], **params)
            out += [evento_basico(e) for e in data.get("data") or []]
            cursor = data.get("nextCursor")
            if not cursor:
                break
        return out
