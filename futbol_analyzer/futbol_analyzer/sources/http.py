"""Cliente HTTP con reintentos, caché en SQLite y control de presupuesto de peticiones."""
from __future__ import annotations

import json
import logging
import time
from typing import Any

import requests

from ..db import Database

log = logging.getLogger(__name__)


class BudgetExceeded(RuntimeError):
    pass


class CachedClient:
    def __init__(self, db: Database, base_url: str, headers: dict[str, str] | None = None,
                 budget: int | None = None, min_interval: float = 0.0):
        self.db = db
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update(headers or {})
        self.session.headers.setdefault("User-Agent", "futbol-analyzer/1.0")
        self.budget = budget
        self.used = 0
        self.min_interval = min_interval
        self._last = 0.0

    def get(self, path: str, params: dict[str, Any] | None = None, ttl: float = 3600) -> Any:
        """ttl en segundos; ttl=-1 = caché permanente (datos de partidos ya terminados)."""
        params = params or {}
        key = f"{self.base_url}{path}?{json.dumps(params, sort_keys=True)}"
        cached = self.db.cache_get(key, ttl)
        if cached is not None:
            return cached
        if self.budget is not None and self.used >= self.budget:
            raise BudgetExceeded(f"Presupuesto de peticiones agotado ({self.budget}) para {self.base_url}")

        for attempt in range(4):
            wait = self.min_interval - (time.time() - self._last)
            if wait > 0:
                time.sleep(wait)
            self._last = time.time()
            try:
                resp = self.session.get(f"{self.base_url}{path}", params=params, timeout=20)
            except requests.RequestException as exc:
                log.warning("Error de red %s (intento %d): %s", path, attempt + 1, exc)
                time.sleep(2 ** attempt)
                continue
            self.used += 1
            if resp.status_code == 429:  # límite por minuto
                log.warning("Límite por minuto alcanzado en %s; esperando 60 s", self.base_url)
                time.sleep(60)
                continue
            resp.raise_for_status()
            body = resp.json()
            errors = body.get("errors") if isinstance(body, dict) else None
            if errors and "rateLimit" in str(errors):  # API-Football avisa del límite con HTTP 200
                log.warning("Límite por minuto alcanzado en %s; esperando 60 s", self.base_url)
                time.sleep(60)
                continue
            if not errors:  # no guardar en caché respuestas de error
                self.db.cache_put(key, body)
            return body
        raise RuntimeError(f"No se pudo obtener {path} tras varios intentos")
