"""Cliente de API-Football v3 (https://www.api-football.com/documentation-v3).

Fuente principal: partidos del día, estadísticas por partido (córners, tarjetas,
tiros), estadísticas de jugadores y cuotas de casas de apuestas.
"""
from __future__ import annotations

import logging
import time
from typing import Any

import requests

log = logging.getLogger(__name__)

BASE_URL = "https://v3.football.api-sports.io"


class ApiError(RuntimeError):
    pass


class PresupuestoAgotado(ApiError):
    """Se alcanzó el tope de peticiones configurado para esta ejecución."""


class ApiFootball:
    def __init__(self, api_key: str, presupuesto: int = 90, session: requests.Session | None = None,
                 base_url: str = BASE_URL):
        if not api_key:
            raise ApiError(
                "Falta API_FOOTBALL_KEY. Crea una cuenta gratis en https://dashboard.api-football.com "
                "y pon la clave en el archivo .env"
            )
        self.base_url = base_url
        self.session = session or requests.Session()
        self.session.headers.update({"x-apisports-key": api_key})
        self.presupuesto = presupuesto
        self.peticiones = 0
        self.restantes_hoy: int | None = None

    def _get(self, path: str, **params: Any) -> list[dict]:
        if self.peticiones >= self.presupuesto:
            raise PresupuestoAgotado(f"Presupuesto de {self.presupuesto} peticiones agotado")
        if self.restantes_hoy is not None and self.restantes_hoy <= 0:
            raise PresupuestoAgotado("La API indica que no quedan peticiones hoy")

        for intento in range(3):
            resp = self.session.get(f"{self.base_url}{path}", params=params, timeout=30)
            self.peticiones += 1
            if resp.status_code == 429:
                time.sleep(61)
                continue
            resp.raise_for_status()
            restantes = resp.headers.get("x-ratelimit-requests-remaining")
            if restantes is not None and restantes.isdigit():
                self.restantes_hoy = int(restantes)
            # Límite por minuto (10 en el plan gratuito): si se agota, esperar a que se renueve.
            por_minuto = resp.headers.get("x-ratelimit-remaining")
            if por_minuto is not None and por_minuto.isdigit() and int(por_minuto) <= 1:
                log.info("Límite por minuto alcanzado, esperando 60 s...")
                time.sleep(61)
            data = resp.json()
            errors = data.get("errors")
            if errors:
                if isinstance(errors, dict) and "rateLimit" in errors:
                    time.sleep(61)
                    continue
                raise ApiError(f"{path} {params}: {errors}")
            return data.get("response", [])
        raise ApiError(f"{path}: límite de peticiones por minuto, reintentos agotados")

    # --- Endpoints -----------------------------------------------------------------

    def partidos_por_fecha(self, fecha: str, zona_horaria: str) -> list[dict]:
        return self._get("/fixtures", date=fecha, timezone=zona_horaria)

    def ultimos_partidos(self, team_id: int, n: int) -> list[dict]:
        return self._get("/fixtures", team=team_id, last=n)

    def partido(self, fixture_id: int) -> dict | None:
        res = self._get("/fixtures", id=fixture_id)
        return res[0] if res else None

    def estadisticas_partido(self, fixture_id: int) -> list[dict]:
        return self._get("/fixtures/statistics", fixture=fixture_id)

    def jugadores_partido(self, fixture_id: int) -> list[dict]:
        return self._get("/fixtures/players", fixture=fixture_id)

    def alineaciones(self, fixture_id: int) -> list[dict]:
        return self._get("/fixtures/lineups", fixture=fixture_id)

    def cuotas(self, fixture_id: int) -> list[dict]:
        return self._get("/odds", fixture=fixture_id)
