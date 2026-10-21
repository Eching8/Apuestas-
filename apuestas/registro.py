"""Registro propio del consumo de cada API, por día o por mes (UTC).

Los contadores de los proveedores se actualizan con retraso o ni siquiera existen; este archivo
(en `data/`, guardado en la rama `datos`) es el que manda para no pasarse nunca del límite.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


class Registro:
    def __init__(self, path: Path, periodo: str = "dia"):
        self.path = Path(path)
        self.periodo = periodo

    def clave(self) -> str:
        hoy = datetime.now(timezone.utc).date().isoformat()
        return hoy if self.periodo == "dia" else hoy[:7]

    def _leer(self) -> dict:
        try:
            return json.loads(self.path.read_text(encoding="utf-8")) if self.path.exists() else {}
        except (OSError, ValueError):
            return {}

    def _actual(self) -> dict:
        return self._leer().get(self.clave(), {})

    def usadas(self) -> int:
        return int(self._actual().get("peticiones") or 0)

    def restantes(self) -> int | None:
        r = self._actual().get("restantes")
        return None if r is None else int(r)

    def _escribir(self, **cambios) -> None:
        datos = self._leer()
        actual = {**datos.get(self.clave(), {}), **cambios}
        # Solo se conservan los últimos periodos.
        datos = {k: v for k, v in sorted(datos.items())[-40:] if k != self.clave()}
        datos[self.clave()] = actual
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(datos, indent=1, sort_keys=True), encoding="utf-8")

    def sumar(self, n: int = 1) -> None:
        self._escribir(peticiones=self.usadas() + n)

    def anotar_restantes(self, restantes: int) -> None:
        self._escribir(restantes=restantes)
