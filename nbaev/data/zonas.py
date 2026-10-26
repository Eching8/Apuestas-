"""Zonas de tiro a partir de las coordenadas de ESPN.

ESPN da cada tiro en pies sobre media cancha: x de 0 a 50 (el aro está en x = 25) e y como
distancia desde el aro hacia el centro del campo (los triples de esquina tienen y < 9).
"""
from __future__ import annotations

import math

ZONAS = ("aro", "pintura", "media", "esquina3", "triple")
# Más allá de esta distancia es un lanzamiento desesperado (final de cuarto): no describe al tirador.
DISTANCIA_LEJANA = 35.0


def distancia(x: float, y: float) -> float:
    return math.hypot(x - 25.0, y)


def zona(x: float, y: float, valor: int) -> str | None:
    """Zona del tiro, o None si es un lanzamiento desde campo propio."""
    d = distancia(x, y)
    if d >= DISTANCIA_LEJANA:
        return None
    if valor == 3:
        return "esquina3" if y < 9 else "triple"
    if d <= 4:
        return "aro"
    if abs(x - 25) <= 8 and y <= 14:
        return "pintura"
    return "media"
