"""Probabilidad final = mezcla del modelo y del mercado, y control de comparaciones múltiples.

Mezcla: regresión logística y ~ logit(p_mercado) + logit(p_modelo) ajustada con las líneas reales fuera de
muestra de la validación (fase 3/4). Se ajusta con las líneas de CIERRE: a la hora en que se ejecuta el modelo
con el parte de lesiones del día, las cuotas se parecen más al cierre que a la apertura, y es lo conservador
(el peso del modelo frente al cierre es pequeño).

Comparaciones múltiples: cada día se evalúan cientos de líneas y algunas parecerán EV+ por azar. Bajo la
hipótesis "el modelo no sabe nada que el mercado no sepa", la diferencia p_final - p_justa se comporta como
ruido con desviación `sd_edge` (medida en la validación). Cada línea recibe un p-valor y se aplica
Benjamini-Hochberg sobre todas las líneas del día (tasa de falsos descubrimientos `fdr`).
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import norm


@dataclass
class Mezcla:
    mercado: str = "pts"
    intercepto: float = 0.0
    peso_mercado: float = 1.0
    peso_modelo: float = 0.0
    sd_edge: float = 0.03          # dispersión de p_final - p_justa cuando no hay ventaja
    n: int = 0
    ajustada_con: str = "cierre"

    def aplicar(self, p_mercado, p_modelo) -> np.ndarray:
        z = self.intercepto + self.peso_mercado * _logit(p_mercado) + self.peso_modelo * _logit(p_modelo)
        return 1 / (1 + np.exp(-z))

    def guardar(self, ruta: Path) -> None:
        ruta.parent.mkdir(parents=True, exist_ok=True)
        ruta.write_text(json.dumps(asdict(self), indent=2), encoding="utf-8")

    @staticmethod
    def cargar(ruta: Path) -> "Mezcla":
        return Mezcla(**json.loads(Path(ruta).read_text(encoding="utf-8")))


def _logit(p):
    p = np.clip(np.asarray(p, dtype=float), 1e-3, 1 - 1e-3)
    return np.log(p / (1 - p))


def ajustar(lineas_oos: pd.DataFrame, col_modelo: str = "p_lgb", kind: str = "cierre", mercado: str = "pts") -> Mezcla:
    from sklearn.linear_model import LogisticRegression
    d = lineas_oos[lineas_oos["kind"] == kind].dropna(subset=["p_mercado", col_modelo, "y"])
    X = np.column_stack([_logit(d["p_mercado"]), _logit(d[col_modelo])])
    m = LogisticRegression(C=1e3).fit(X, d["y"])
    mz = Mezcla(mercado=mercado, intercepto=float(m.intercept_[0]), peso_mercado=float(m.coef_[0][0]),
                peso_modelo=float(m.coef_[0][1]), n=len(d), ajustada_con=kind)
    mz.sd_edge = float(np.std(mz.aplicar(d["p_mercado"], d[col_modelo]) - d["p_mercado"]))
    return mz


def p_valor_edge(edge, sd_edge: float) -> np.ndarray:
    """P(edge >= observado | sin ventaja), con edge ~ N(0, sd_edge)."""
    return 1 - norm.cdf(np.asarray(edge, dtype=float) / max(sd_edge, 1e-6))


def benjamini_hochberg(p: pd.Series, fdr: float = 0.10) -> pd.Series:
    """True para las líneas que superan Benjamini-Hochberg con la tasa de falsos descubrimientos `fdr`."""
    p = p.fillna(1.0)
    m = len(p)
    if m == 0:
        return pd.Series(dtype=bool)
    orden = p.sort_values()
    umbral = fdr * np.arange(1, m + 1) / m
    pasa = orden.to_numpy() <= umbral
    k = np.max(np.nonzero(pasa)[0]) + 1 if pasa.any() else 0
    out = pd.Series(False, index=p.index)
    out[orden.index[:k]] = True
    return out
