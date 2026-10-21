"""Cliente de API-Football v3 (https://www.api-football.com/documentation-v3).

Fuente principal: partidos del día, estadísticas por partido (córners, tarjetas,
tiros), estadísticas de jugadores y cuotas de casas de apuestas.
"""
from __future__ import annotations

import json
import logging
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests

log = logging.getLogger(__name__)

BASE_URL = "https://v3.football.api-sports.io"
# Pausa mínima entre consultas: el plan gratuito permite 10 por minuto.
MIN_INTERVALO = float(os.environ.get("APUESTAS_INTERVALO", 7.0))
# Peticiones del día que nunca se usan (margen de seguridad frente al límite del plan).
RESERVA_DIARIA = int(os.environ.get("APUESTAS_RESERVA", 10))
# Registro propio del consumo por día (UTC, como el contador de API-Football): /status se actualiza
# con retraso, así que no basta para saber cuánto se ha gastado.
REGISTRO_USO = Path(os.environ.get("APUESTAS_USO_API", Path(__file__).resolve().parent.parent / "data" / "uso_api.json"))


def _hoy_utc() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def leer_registro(path: Path | None) -> dict:
    if path is None or not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8")).get(_hoy_utc(), {})
    except (OSError, ValueError):
        return {}


def _guardar_registro(path: Path | None, peticiones: int, restantes: int | None) -> None:
    if path is None:
        return
    try:
        datos = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    except (OSError, ValueError):
        datos = {}
    datos = {k: v for k, v in datos.items() if k >= _hoy_utc()[:8] + "01"}   # solo el mes en curso
    datos[_hoy_utc()] = {"peticiones": peticiones, "restantes": restantes}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(datos, indent=1), encoding="utf-8")


class ApiError(RuntimeError):
    pass


class PresupuestoAgotado(ApiError):
    """Se alcanzó el tope de peticiones configurado para esta ejecución."""


def estado(session: requests.Session | None = None, api_key: str = "", base_url: str = BASE_URL) -> dict:
    """Respuesta de /status (no gasta peticiones del día). Sirve también para saber si la clave llega
    por otra vía: en la nube, un "network secret" la añade el proxy sin que la sesión la vea."""
    session = session or requests.Session()
    headers = {"x-apisports-key": api_key} if api_key else {}
    data = session.get(f"{base_url}/status", headers=headers, timeout=30).json()
    if data.get("errors"):
        raise ApiError(f"API-Football rechaza la clave: {data['errors']}")
    return data.get("response") or {}


class ApiFootball:
    """Cliente con doble tope: `presupuesto` por ejecución y, sobre todo, el consumo real del día.

    Al crearse consulta /status (gratis) para saber cuántas peticiones lleva el día entre TODAS las
    ejecuciones, y nunca pasa de `límite del plan − RESERVA_DIARIA`. Si no puede saberlo, no arranca:
    es preferible no analizar a arriesgar la suspensión de la cuenta.
    """

    def __init__(self, api_key: str, presupuesto: int = 90, session: requests.Session | None = None,
                 base_url: str = BASE_URL, reserva: int = RESERVA_DIARIA, registro: Path | None = REGISTRO_USO):
        self.base_url = base_url
        self.session = session or requests.Session()
        if api_key:
            self.session.headers.update({"x-apisports-key": api_key})
        try:
            info = estado(self.session, base_url=base_url)
        except (ApiError, OSError, ValueError) as e:
            if not api_key:
                raise ApiError(
                    "Falta la clave de API-Football. Crea una cuenta gratis en https://dashboard.api-football.com "
                    "y ponla en el archivo .env (API_FOOTBALL_KEY) o, en la nube, como network secret para "
                    "v3.football.api-sports.io con la cabecera x-apisports-key"
                ) from None
            raise ApiError(f"No se pudo consultar el consumo diario de API-Football ({e}); no se hace nada") from None
        uso = info.get("requests") or {}
        limite, usadas = int(uso.get("limit_day") or 0), int(uso.get("current") or 0)
        if not limite:
            raise ApiError("API-Football no informa del límite diario; no se hace nada para no pasarse")
        # La cifra más pesimista entre /status, el registro propio y la última cabecera de la API.
        self.registro = registro
        previo = leer_registro(registro)
        self.contadas_hoy = int(previo.get("peticiones") or 0)
        usadas = max(usadas, self.contadas_hoy)
        if previo.get("restantes") is not None:
            usadas = max(usadas, limite - int(previo["restantes"]))
        self.reserva = reserva
        self.limite_dia, self.usadas_al_empezar = limite, usadas
        self.restantes_hoy: int | None = limite - usadas
        self.presupuesto = max(0, min(presupuesto, limite - usadas - reserva))
        self.peticiones = 0
        log.info("API-Football: %d de %d peticiones usadas hoy; esta ejecución puede usar %d",
                 usadas, limite, self.presupuesto)
        self._ultima = 0.0

    def _get(self, path: str, **params: Any) -> list[dict]:
        for intento in range(2):
            # Se comprueba antes de cada intento: los reintentos también cuentan en el límite.
            if self.peticiones >= self.presupuesto:
                raise PresupuestoAgotado(f"Presupuesto de {self.presupuesto} peticiones agotado")
            if self.restantes_hoy is not None and self.restantes_hoy <= getattr(self, "reserva", 0):
                raise PresupuestoAgotado("Solo quedan las peticiones de reserva del día; se para aquí")
            espera = MIN_INTERVALO - (time.monotonic() - self._ultima)
            if espera > 0:
                time.sleep(espera)
            self._ultima = time.monotonic()
            resp = self.session.get(f"{self.base_url}{path}", params=params, timeout=30)
            self.peticiones += 1
            self.contadas_hoy = getattr(self, "contadas_hoy", 0) + 1
            if self.restantes_hoy is not None:
                self.restantes_hoy -= 1        # la cabecera de la respuesta, si viene, lo corrige
            if resp.status_code == 429:
                time.sleep(61)
                continue
            resp.raise_for_status()
            restantes = resp.headers.get("x-ratelimit-requests-remaining")
            if restantes is not None and restantes.isdigit():
                self.restantes_hoy = min(int(restantes), self.restantes_hoy or int(restantes))
            _guardar_registro(getattr(self, "registro", None), self.contadas_hoy, self.restantes_hoy)
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
