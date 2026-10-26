"""Cuotas -> probabilidad implícita -> probabilidad justa (sin margen), edge y valor esperado.

Métodos para quitar el margen (overround) de un mercado de n resultados con cuotas decimales o_i:
- multiplicativo: p_i = (1/o_i) / sum(1/o_j). Reparte el margen en proporción a cada probabilidad.
- power: p_i = (1/o_i)^k con k tal que sum(p_i) = 1. Carga más margen en los resultados improbables
  (corrige en parte el sesgo favorito-sorpresa).
- shin: modelo de Shin (1993) con una fracción z de apostadores con información privilegiada; también
  carga más margen en los resultados improbables. Útil en mercados de muchos resultados (primer anotador).
"""
from __future__ import annotations

import numpy as np
from scipy.optimize import brentq


def implicitas(cuotas) -> np.ndarray:
    return 1.0 / np.asarray(cuotas, dtype=float)


def margen(cuotas) -> float:
    """Overround: suma de probabilidades implícitas - 1."""
    return float(implicitas(cuotas).sum() - 1.0)


def multiplicativo(cuotas) -> np.ndarray:
    q = implicitas(cuotas)
    return q / q.sum()


def power(cuotas) -> np.ndarray:
    q = implicitas(cuotas)
    if abs(q.sum() - 1) < 1e-12:
        return q
    k = brentq(lambda k: (q ** k).sum() - 1.0, 1e-6, 50.0)
    return q ** k


def shin(cuotas) -> np.ndarray:
    q = implicitas(cuotas)
    s = q.sum()
    if abs(s - 1) < 1e-12:
        return q

    def probs(z):
        return (np.sqrt(z ** 2 + 4 * (1 - z) * q ** 2 / s) - z) / (2 * (1 - z))

    z = brentq(lambda z: probs(z).sum() - 1.0, 0.0, 0.999)
    return probs(z)


METODOS = {"multiplicativo": multiplicativo, "power": power, "shin": shin}


def justa(cuotas, metodo: str = "multiplicativo") -> np.ndarray:
    return METODOS[metodo](cuotas)


def justa_dos_lados(cuota_a, cuota_b, metodo: str = "multiplicativo") -> np.ndarray:
    """Probabilidad justa del lado A en mercados de dos resultados (vectorizado)."""
    a, b = np.asarray(cuota_a, dtype=float), np.asarray(cuota_b, dtype=float)
    if metodo == "multiplicativo":
        qa, qb = 1 / a, 1 / b
        return qa / (qa + qb)
    return np.array([METODOS[metodo]([x, y])[0] for x, y in zip(a, b)])


def ev(p, cuota):
    """Valor esperado por unidad apostada: p * cuota - 1."""
    return np.asarray(p) * np.asarray(cuota) - 1.0


def edge(p, p_justa):
    """Ventaja en probabilidad frente al mercado sin margen."""
    return np.asarray(p) - np.asarray(p_justa)


def cuota_justa(p):
    return 1.0 / np.asarray(p)
