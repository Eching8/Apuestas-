"""Fuente Bzzoiro Sports Data (BSD): https://sports.bzzoiro.com — gratis con registro.

Plan gratuito: 7.500 peticiones al día por cuenta (se reinicia a las 00:00 UTC) y 10 por segundo.
Lo que se usa de ella, porque ESPN no lo da:

- **cuotas de consenso** de ~14 casas (1X2, más/menos 1.5/2.5/3.5 y ambos marcan) y el **árbitro**
  de cada partido: una sola llamada a la lista de partidos del día (`/api/events/`, v1);
- **alineaciones** confirmadas (o previstas) y bajas, para el chequeo previo si ESPN aún no las tiene
  (`/api/v2/events/{id}/lineups/`).

La clave va en `BZZOIRO_TOKEN` o, en la nube, como *network secret* para `sports.bzzoiro.com`
(cabecera `Authorization`, prefijo `Token`). Como con cualquier fuente, se lleva un registro propio
del consumo y nunca se pasa de `BZZOIRO_MAX_DIA` peticiones al día.
"""
from __future__ import annotations

import logging
import os
import time
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import requests

from .api_football import ApiError, PresupuestoAgotado
from .registro import Registro

log = logging.getLogger(__name__)

BASE_URL = "https://sports.bzzoiro.com"
MAX_DIA = int(os.environ.get("BZZOIRO_MAX_DIA", 1000))       # muy por debajo de las 7.500 del plan
MIN_INTERVALO = 0.5

# Mercado de BSD -> (bet, value) con los nombres de API-Football que entiende odds.attach_odds.
CUOTAS = {
    "odds_home": ("Match Winner", "Home"), "odds_draw": ("Match Winner", "Draw"), "odds_away": ("Match Winner", "Away"),
    "odds_over_15": ("Goals Over/Under", "Over 1.5"), "odds_under_15": ("Goals Over/Under", "Under 1.5"),
    "odds_over_25": ("Goals Over/Under", "Over 2.5"), "odds_under_25": ("Goals Over/Under", "Under 2.5"),
    "odds_over_35": ("Goals Over/Under", "Over 3.5"), "odds_under_35": ("Goals Over/Under", "Under 3.5"),
    "odds_btts_yes": ("Both Teams Score", "Yes"), "odds_btts_no": ("Both Teams Score", "No"),
}


def _nombre(valor) -> str:
    if isinstance(valor, dict):
        return valor.get("name") or valor.get("short_name") or ""
    return valor or ""


def evento_basico(ev: dict) -> dict:
    """Lo que interesa de un partido de /api/events/ (v1): equipos, hora, árbitro y cuotas."""
    arbitro = ev.get("referee")
    return {
        "id": ev.get("id"),
        "local": _nombre(ev.get("home_team_obj")) or _nombre(ev.get("home_team")),
        "visitante": _nombre(ev.get("away_team_obj")) or _nombre(ev.get("away_team")),
        "inicio": ev.get("event_date"),
        "liga": _nombre(ev.get("league")),
        "arbitro": _nombre(arbitro) if arbitro else None,
        "cuotas": [(bet, value, float(ev[k])) for k, (bet, value) in CUOTAS.items()
                   if ev.get(k) not in (None, "") and float(ev[k]) > 1],
    }


def alineacion_basica(data: dict) -> dict | None:
    """/lineups/ -> {"estado", "local": [(nombre, posición)], "visitante": [...], "bajas": [...]}."""
    if not data or not data.get("lineups"):
        return None
    lados = data["lineups"]
    jugadores = lambda lado: [(p.get("name"), p.get("position")) for p in (lados.get(lado) or {}).get("players") or []]
    bajas = []
    for lado in ("home", "away"):
        for p in ((data.get("unavailable_players") or {}).get(lado) or []):
            bajas.append(p.get("name") if isinstance(p, dict) else str(p))
    return {"estado": data.get("lineup_status"), "local": jugadores("home"), "visitante": jugadores("away"),
            "bajas": bajas}


class Bzzoiro:
    def __init__(self, token: str = "", session: requests.Session | None = None, registro: Registro | None = None,
                 max_dia: int = MAX_DIA, base_url: str = BASE_URL):
        self.session = session or requests.Session()
        if token:
            self.session.headers.update({"Authorization": f"Token {token}"})
        self.base_url = base_url
        self.registro = registro
        self.max_dia = max_dia
        self.peticiones = 0
        self._ultima = 0.0

    def _get(self, path: str, **params) -> dict:
        usadas = self.registro.usadas() if self.registro else self.peticiones
        if usadas >= self.max_dia:
            raise PresupuestoAgotado(f"Bzzoiro: tope diario propio de {self.max_dia} peticiones alcanzado")
        espera = MIN_INTERVALO - (time.monotonic() - self._ultima)
        if espera > 0:
            time.sleep(espera)
        self._ultima = time.monotonic()
        self.peticiones += 1
        if self.registro:
            self.registro.sumar()
        resp = self.session.get(f"{self.base_url}{path}", params=params, timeout=30)
        if resp.status_code in (401, 403):
            raise ApiError("Bzzoiro rechaza la clave: falta BZZOIRO_TOKEN o el network secret de sports.bzzoiro.com")
        if resp.status_code == 429:
            raise PresupuestoAgotado(f"Bzzoiro: límite alcanzado ({resp.text[:120]})")
        resp.raise_for_status()
        restantes = resp.headers.get("RateLimit", "")
        if "r=" in restantes and self.registro:
            try:
                self.registro.anotar_restantes(int(restantes.split("r=")[1].split(";")[0]))
            except ValueError:
                pass
        return resp.json()

    def disponible(self) -> str:
        data = self._get("/api/v2/leagues/", limit=1)
        return f"OK ({data.get('count', '?')} ligas)"

    def partidos(self, desde: date, hasta: date) -> list[dict]:
        out, pagina = [], 1
        while True:
            data = self._get("/api/events/", date_from=desde.isoformat(), date_to=hasta.isoformat(), page=pagina)
            out += [evento_basico(e) for e in data.get("results") or []]
            if not data.get("next") or pagina >= 10:
                return out
            pagina += 1

    def alineacion(self, evento_id: int) -> dict | None:
        return alineacion_basica(self._get(f"/api/v2/events/{evento_id}/lineups/"))


def inicio_utc(texto: str | None) -> datetime | None:
    if not texto:
        return None
    try:
        dt = datetime.fromisoformat(texto.replace("Z", "+00:00"))
    except ValueError:
        return None
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def buscar(eventos: list[dict], local: str, visitante: str, inicio: datetime, tolerancia=timedelta(hours=3)) -> dict | None:
    """El partido de otra fuente que corresponde a uno nuestro: misma hora (± 3 h) y nombres parecidos."""
    from .football_data import _similar
    mejor, puntos = None, 0.0
    for ev in eventos:
        t = inicio_utc(ev.get("inicio"))
        if t is None or abs(t - inicio) > tolerancia:
            continue
        p = min(_similar(local, ev["local"]), _similar(visitante, ev["visitante"]))
        if p > puntos:
            mejor, puntos = ev, p
    return mejor if puntos >= 0.6 else None


def registro_por_defecto(nombre: str) -> Path:
    return Path(os.environ.get("APUESTAS_DATOS", Path(__file__).resolve().parent.parent / "data")) / nombre
