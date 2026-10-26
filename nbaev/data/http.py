"""Cliente HTTP con límite de peticiones, reintentos con espera exponencial y respeto de Retry-After."""
from __future__ import annotations

import logging
import time
from collections import deque
from typing import Any

import requests

log = logging.getLogger(__name__)


class ErrorFuente(RuntimeError):
    """La fuente no respondió o rechazó la petición de forma definitiva."""


class Limitador:
    """Pausa mínima entre peticiones y, opcionalmente, máximo de peticiones por minuto."""

    def __init__(self, min_intervalo: float = 0.0, max_por_minuto: int | None = None,
                 reloj=time.monotonic, dormir=time.sleep):
        self.min_intervalo = min_intervalo
        self.max_por_minuto = max_por_minuto
        self._reloj, self._dormir = reloj, dormir
        self._historial: deque[float] = deque()
        self._ultima = float("-inf")

    def esperar(self) -> None:
        ahora = self._reloj()
        espera = self.min_intervalo - (ahora - self._ultima)
        if self.max_por_minuto:
            while self._historial and ahora - self._historial[0] >= 60:
                self._historial.popleft()
            if len(self._historial) >= self.max_por_minuto:
                espera = max(espera, 60 - (ahora - self._historial[0]) + 0.05)
        if espera > 0:
            self._dormir(espera)
        self._ultima = self._reloj()
        if self.max_por_minuto:
            self._historial.append(self._ultima)


class ClienteHttp:
    def __init__(self, base_url: str, limitador: Limitador, reintentos: int = 4, timeout: float = 30,
                 cabeceras: dict | None = None, session: requests.Session | None = None, nombre: str = "http"):
        self.base_url = base_url.rstrip("/")
        self.limitador = limitador
        self.reintentos = reintentos
        self.timeout = timeout
        self.session = session or requests.Session()
        self.session.headers.setdefault("User-Agent", "Mozilla/5.0 (nbaev)")
        self.session.headers.update(cabeceras or {})
        self.nombre = nombre
        self.peticiones = 0

    def get_json(self, path: str, **params: Any) -> Any:
        url = path if path.startswith("http") else f"{self.base_url}/{path.lstrip('/')}"
        ultimo_error = ""
        for intento in range(self.reintentos):
            self.limitador.esperar()
            try:
                resp = self.session.get(url, params=params, timeout=self.timeout)
            except requests.RequestException as e:
                ultimo_error = str(e)
                log.warning("%s %s: %s (intento %d)", self.nombre, path, e, intento + 1)
                time.sleep(min(2 ** intento, 30))
                continue
            self.peticiones += 1
            if resp.status_code == 429 or resp.status_code >= 500:
                ultimo_error = f"HTTP {resp.status_code}"
                espera = _retry_after(resp) or min(2 ** (intento + 1), 60)
                log.warning("%s %s: HTTP %d, espero %.0f s", self.nombre, path, resp.status_code, espera)
                time.sleep(espera)
                continue
            if resp.status_code != 200:
                raise ErrorFuente(f"{self.nombre} {path} {params}: HTTP {resp.status_code} {resp.text[:200]}")
            return resp.json()
        raise ErrorFuente(f"{self.nombre} {path}: sin respuesta tras {self.reintentos} intentos ({ultimo_error})")


def _retry_after(resp: requests.Response) -> float | None:
    try:
        return float(resp.headers.get("Retry-After", ""))
    except ValueError:
        return None
