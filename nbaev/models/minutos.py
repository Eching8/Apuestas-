"""Modelo de minutos (etapa A): media, cuantiles y probabilidad de no jugar (DNP técnico).

- Baselines: media exponencial de minutos (`min_base`) y la misma normalizada a los 240 minutos que
  reparten los jugadores disponibles del equipo (`min_norm`).
- LightGBM: regresión de la media (L2), regresión cuantílica (10, 50 y 90 %) y clasificador de minutos = 0.
- Reparto por equipo opcional: escala las medias para que cada equipo sume los minutos esperados de un partido.

La salida alimenta la simulación Monte Carlo: P(DNP) y una distribución de minutos si juega.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path

import joblib
import lightgbm as lgb
import numpy as np
import pandas as pd

from ..features.minutos import FEATURES, a_matriz

log = logging.getLogger(__name__)

CUANTILES = (0.1, 0.5, 0.9)
PARAMS = {"learning_rate": 0.05, "num_leaves": 31, "min_data_in_leaf": 100, "feature_fraction": 0.8,
          "bagging_fraction": 0.8, "bagging_freq": 1, "lambda_l2": 1.0, "verbose": -1, "num_threads": 4}
RONDAS = 400


@dataclass
class ModeloMinutos:
    media: lgb.Booster | None = None          # minutos esperados contando el riesgo de no jugar
    media_juega: lgb.Booster | None = None    # minutos esperados si juega (las props se anulan si no juega)
    cuantiles: dict[float, lgb.Booster] = field(default_factory=dict)
    p_cero: lgb.Booster | None = None
    minutos_equipo: float = 241.5      # media real de minutos por equipo y partido (incluye prórrogas)
    entrenado_hasta: pd.Timestamp | None = None

    def guardar(self, ruta: Path) -> None:
        ruta.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self, ruta)

    @staticmethod
    def cargar(ruta: Path) -> "ModeloMinutos":
        return joblib.load(ruta)


def entrenar(df: pd.DataFrame, cuantiles: tuple[float, ...] = CUANTILES, rondas: int = RONDAS) -> ModeloMinutos:
    """Entrena con las filas de `df` que tienen minutos reales."""
    d = df[df["minutes"].notna()]
    X, y = a_matriz(d), d["minutes"].to_numpy()
    m = ModeloMinutos(entrenado_hasta=d["start_utc"].max())
    m.media = lgb.train({**PARAMS, "objective": "regression"}, lgb.Dataset(X, y), rondas)
    juega = y > 0
    Xj, yj = X[juega], y[juega]
    m.media_juega = lgb.train({**PARAMS, "objective": "regression"}, lgb.Dataset(Xj, yj), rondas)
    # Cuantiles condicionados a jugar: es la distribución que importa para una prop (si no juega, se anula).
    for q in cuantiles:
        m.cuantiles[q] = lgb.train({**PARAMS, "objective": "quantile", "alpha": q}, lgb.Dataset(Xj, yj), rondas)
    m.p_cero = lgb.train({**PARAMS, "objective": "binary"}, lgb.Dataset(X, (y == 0).astype(int)), rondas // 2)
    m.minutos_equipo = float(d.groupby(["game_id", "team_id"])["minutes"].sum().mean())
    return m


def predecir(m: ModeloMinutos, df: pd.DataFrame, repartir: bool = True) -> pd.DataFrame:
    """Columnas:
    - min_pred: minutos esperados (con el riesgo de no jugar), repartidos por equipo si `repartir`.
    - p_dnp: probabilidad de no jugar estando disponible.
    - min_si_juega y min_q10/q50/q90: media y cuantiles si juega (escalados con el mismo factor del reparto).
    """
    X = a_matriz(df)
    out = pd.DataFrame(index=df.index)
    out["min_pred_bruta"] = np.clip(m.media.predict(X), 0, 48)
    out["p_dnp"] = m.p_cero.predict(X)
    out["min_pred"] = out["min_pred_bruta"]
    if repartir:
        out["min_pred"] = repartir_equipo(df, out["min_pred_bruta"], m.minutos_equipo)
    factor = (out["min_pred"] / out["min_pred_bruta"].clip(lower=0.5)).clip(0.7, 1.3)
    out["min_si_juega"] = np.clip(m.media_juega.predict(X) * factor, 0, 48)
    for q, b in m.cuantiles.items():
        out[f"min_q{int(q * 100)}"] = np.clip(b.predict(X) * factor, 0, 53)
    return out


def repartir_equipo(df: pd.DataFrame, pred: pd.Series, total: float) -> pd.Series:
    """Escala las predicciones de cada equipo para que sumen `total` minutos, sin pasar de 48 por jugador."""
    grupo = [df["game_id"], df["team_id"]]
    p = pred.astype(float).copy()
    for _ in range(5):  # quien llega al tope se fija en 48 y el resto reparte lo que falta
        tope = p >= 48.0 - 1e-9
        libre = p.where(~tope, 0.0).groupby(grupo).transform("sum").clip(lower=1e-6)
        objetivo = total - 48.0 * tope.groupby(grupo).transform("sum")
        p = pd.Series(np.where(tope, 48.0, np.minimum(p * objetivo / libre, 48.0)), index=p.index)
    return p


def importancia(m: ModeloMinutos) -> pd.DataFrame:
    gan = m.media.feature_importance("gain")
    return (pd.DataFrame({"feature": FEATURES, "ganancia": gan / gan.sum()})
            .sort_values("ganancia", ascending=False).reset_index(drop=True))


# --- Proyección del día ---------------------------------------------------------------------------

def modelo_vigente(con, cfg: dict, ruta: Path, forzar: bool = False) -> ModeloMinutos:
    """Carga el modelo guardado o lo reentrena si no existe o tiene más de `reentrenar_cada_dias`."""
    from ..features import minutos as fm
    dias = cfg["minutos"].get("reentrenar_cada_dias", 7)
    if ruta.exists() and not forzar:
        edad = (pd.Timestamp.now() - pd.Timestamp(ruta.stat().st_mtime, unit="s")).days
        if edad < dias:
            return ModeloMinutos.cargar(ruta)
    log.info("Entrenando el modelo de minutos con todo el histórico")
    m = entrenar(fm.dataset(con))
    m.guardar(ruta)
    return m


def proyectar(con, cfg: dict, fecha: str, ruta_modelo: Path, corte=None) -> pd.DataFrame:
    """Minutos proyectados de los jugadores probables de los partidos (aún no terminados) de `fecha`."""
    from ..data import db
    from ..features import minutos as fm
    ids = [r[0] for r in con.execute("SELECT game_id FROM games WHERE fecha = ? AND status <> 'STATUS_FINAL'",
                                     [fecha]).fetchall()]
    if not ids:
        log.warning("No hay partidos pendientes el %s", fecha)
        return pd.DataFrame()
    corte = corte or db.ahora_utc()
    futuras = fm.filas_futuras(con, ids, corte, cfg["minutos"]["prob_juega"])
    df = fm.construir(pd.concat([fm.cargar(con), futuras], ignore_index=True))
    df = df[df["game_id"].isin(ids) & df["minutes"].isna()].reset_index(drop=True)
    m = modelo_vigente(con, cfg, ruta_modelo)
    out = pd.concat([df, predecir(m, df)], axis=1)
    out["fecha"] = pd.to_datetime(fecha).date()
    out["modelo_hasta"] = m.entrenado_hasta
    out["created_at"] = db.ahora_utc()
    con.execute("DELETE FROM proj_minutos WHERE game_id IN (SELECT unnest(?))", [ids])
    db.upsert(con, "proj_minutos", out)
    return out
