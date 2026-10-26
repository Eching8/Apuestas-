"""Gestión de banca: Kelly fraccional con tope por apuesta y tope diario."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass
class ReglasBanca:
    fraccion_kelly: float = 0.25    # 1/4 Kelly
    tope_apuesta: float = 0.02      # máximo 2 % de la banca por apuesta
    tope_diario: float = 0.10       # máximo 10 % de la banca arriesgado en un día
    minimo: float = 0.0             # apuesta mínima (fracción de banca); por debajo no se apuesta


def kelly(p, cuota) -> np.ndarray:
    """Fracción de Kelly completa: (p*o - 1) / (o - 1). Negativa = no apostar."""
    p, o = np.asarray(p, dtype=float), np.asarray(cuota, dtype=float)
    return (p * o - 1.0) / (o - 1.0)


def fraccion(p, cuota, reglas: ReglasBanca = ReglasBanca()) -> np.ndarray:
    """Fracción de la banca a apostar: Kelly fraccional recortado al tope por apuesta."""
    f = np.clip(kelly(p, cuota) * reglas.fraccion_kelly, 0.0, reglas.tope_apuesta)
    return np.where(f < reglas.minimo, 0.0, f)


def aplicar_tope_diario(fracciones: pd.Series, dias: pd.Series, tope: float) -> pd.Series:
    """Si las apuestas de un día suman más que `tope`, se escalan todas en proporción."""
    total = fracciones.groupby(dias).transform("sum")
    factor = np.where(total > tope, tope / total.clip(lower=1e-12), 1.0)
    return fracciones * factor


def simular_banca(apuestas: pd.DataFrame, reglas: ReglasBanca = ReglasBanca(), banca_inicial: float = 100.0
                  ) -> pd.DataFrame:
    """Evolución de la banca apostando cada día con la banca al inicio del día.

    `apuestas` necesita: fecha, p (probabilidad usada), cuota, resultado (1 gana, 0 pierde, 0.5 nulo/push).
    """
    a = apuestas.sort_values("fecha").copy()
    a["f"] = fraccion(a["p"], a["cuota"], reglas)
    a["f"] = aplicar_tope_diario(a["f"], a["fecha"], reglas.tope_diario)
    banca, filas = banca_inicial, []
    for fecha, dia in a.groupby("fecha", sort=True):
        stakes = dia["f"].to_numpy() * banca
        gan = np.where(dia["resultado"] == 1, stakes * (dia["cuota"] - 1),
                       np.where(dia["resultado"] == 0, -stakes, 0.0))
        banca += gan.sum()
        filas.append({"fecha": fecha, "apuestas": len(dia), "riesgo": stakes.sum(), "ganancia": gan.sum(),
                      "banca": banca})
    out = pd.DataFrame(filas)
    if not out.empty:
        out["max_previo"] = out["banca"].cummax().clip(lower=banca_inicial)
        out["drawdown"] = 1 - out["banca"] / out["max_previo"]
    return out
