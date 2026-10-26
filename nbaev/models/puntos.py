"""Modelo de puntos (etapa B) y entrada de la simulación.

Tres candidatos que se comparan en validación (ver backtest/puntos.py):
1. Baseline: tasa por minuto encogida del jugador (`r_pts_comp`) x minutos proyectados, simulada con sus
   componentes de tiro.
2. LightGBM de tasa: predice puntos por minuto con contexto (defensa rival por posición, ritmo, total
   implícito, compañeros fuera...). Los volúmenes de tiro del jugador se escalan para que la media de la
   simulación coincida con esa tasa (se conserva su perfil: reparto 2/3, libres y acierto).
3. LightGBM cuantílico directo: cuantiles de los puntos (sin simulación), interpolados como CDF.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import lightgbm as lgb
import numpy as np
import pandas as pd

from ..features.produccion import FEATURES_PTS
from .simulacion import Z90, Dispersion, estimar_dispersion

PARAMS = {"learning_rate": 0.03, "num_leaves": 31, "min_data_in_leaf": 200, "feature_fraction": 0.8,
          "bagging_fraction": 0.8, "bagging_freq": 1, "lambda_l2": 5.0, "verbose": -1, "num_threads": 4}
CUANTILES_PTS = (0.05, 0.15, 0.25, 0.35, 0.5, 0.65, 0.75, 0.85, 0.95)
FEATURES_CUANT = FEATURES_PTS + ["min_si_juega", "min_q10", "min_q90"]


@dataclass
class ModeloPuntos:
    tasa: lgb.Booster | None = None
    cuantiles: dict[float, lgb.Booster] = field(default_factory=dict)
    disp: Dispersion = field(default_factory=Dispersion)


def _X(df: pd.DataFrame, cols=FEATURES_PTS) -> pd.DataFrame:
    return df[cols].astype(float).replace([np.inf, -np.inf], np.nan)


def entrenar(df: pd.DataFrame, rondas: int = 500, cuantilico: bool = True) -> ModeloPuntos:
    """`df`: filas de entrenamiento (jugaron) con features de producción. Para el modelo cuantílico se
    necesitan además los minutos proyectados fuera de muestra (min_si_juega, min_q10, min_q90)."""
    m = ModeloPuntos()
    d = df[df["minutes"] >= 3]
    y = d["pts"] / d["minutes"]
    m.tasa = lgb.train({**PARAMS, "objective": "regression"}, lgb.Dataset(_X(d), y, weight=d["minutes"]), rondas)
    m.disp = estimar_dispersion(d)
    if cuantilico and "min_si_juega" in d:
        dq = d[d["min_si_juega"].notna()]
        for q in CUANTILES_PTS:
            m.cuantiles[q] = lgb.train({**PARAMS, "objective": "quantile", "alpha": q},
                                       lgb.Dataset(_X(dq, FEATURES_CUANT), dq["pts"]), rondas // 2)
    return m


def entrada_simulacion(m: ModeloPuntos | None, df: pd.DataFrame, usar_lgb: bool = True) -> pd.DataFrame:
    """Columnas que necesita `simulacion.simular`. Sin LightGBM (o `usar_lgb=False`) es el baseline."""
    out = df[["game_id", "team_id", "player_id", "min_base", "spread_equipo", "is_home", "r_fga", "r_fg3a",
              "r_fta", "p_fg2", "p_fg3", "p_ft"]].copy()
    out["min_media"] = df["min_si_juega"]
    out["min_sd"] = ((df["min_q90"] - df["min_q10"]) / (2 * Z90)).clip(lower=1.0)
    if usar_lgb and m is not None and m.tasa is not None:
        tasa = np.clip(m.tasa.predict(_X(df)), 0.02, 2.0)
        k = tasa / df["r_pts_comp"].clip(lower=0.02)
        # Se escalan los volúmenes (intentos de campo, de triple y libres); el acierto se mantiene.
        for c in ("r_fga", "r_fg3a", "r_fta"):
            out[c] = df[c] * k
        out["tasa_pts"] = tasa
    else:
        out["tasa_pts"] = df["r_pts_comp"]
    return out


def cdf_cuantiles(m: ModeloPuntos, df: pd.DataFrame, lineas: np.ndarray) -> np.ndarray:
    """P(puntos > línea) interpolando linealmente los cuantiles del modelo cuantílico directo."""
    X = _X(df, FEATURES_CUANT)
    qs = np.array(sorted(m.cuantiles))
    vals = np.column_stack([m.cuantiles[q].predict(X) for q in qs])
    vals = np.maximum.accumulate(vals, axis=1)     # cuantiles monótonos
    out = np.empty(len(df))
    for i, (v, l) in enumerate(zip(vals, lineas)):
        # Colas: se extienden con la pendiente del último tramo.
        xs = np.concatenate([[v[0] - (v[1] - v[0]) * qs[0] / (qs[1] - qs[0])], v,
                             [v[-1] + (v[-1] - v[-2]) * (1 - qs[-1]) / (qs[-1] - qs[-2])]])
        ps = np.concatenate([[0.0], qs, [1.0]])
        out[i] = 1 - np.interp(l, xs, ps)
    return np.clip(out, 0.001, 0.999)


# --- Proyección del día ---------------------------------------------------------------------------

def modelo_vigente(con, cfg: dict, ruta, forzar: bool = False) -> ModeloPuntos:
    """Modelo entrenado con todo el histórico (se reentrena si tiene más de `reentrenar_cada_dias`)."""
    import joblib
    from pathlib import Path

    from ..features import produccion as fp
    ruta = Path(ruta)
    dias = cfg.get("puntos", {}).get("reentrenar_cada_dias", 7)
    if ruta.exists() and not forzar:
        if (pd.Timestamp.now() - pd.Timestamp(ruta.stat().st_mtime, unit="s")).days < dias:
            return joblib.load(ruta)
    m = entrenar(fp.construir(con), cuantilico=False)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(m, ruta)
    return m


def proyectar(con, cfg: dict, fecha: str, n_sims: int = 10_000, semilla: int = 2026) -> tuple[pd.DataFrame, dict]:
    """Distribución de puntos de cada jugador probable de `fecha` (usa la proyección de minutos del día).
    Devuelve (resumen por jugador, simulaciones por estadística)."""
    from ..config import RAIZ
    from ..data import db
    from ..features import minutos as fm
    from ..features import produccion as fp
    from . import minutos as mm
    from .simulacion import resumen, simular

    proj = mm.proyectar(con, cfg, fecha, RAIZ / cfg["minutos"]["modelo"])
    if proj.empty:
        return pd.DataFrame(), {}
    ctx = con.execute("SELECT game_id, team_id, total_implicito FROM team_context").df()
    fut = proj[["game_id", "player_id", "team_id", "opp_id", "name", "position", "start_utc", "season",
                "season_type", "is_home", "b2b", "dias_descanso", "spread_equipo", "total"]].copy()
    fut = fut.merge(ctx, on=["game_id", "team_id"], how="left")
    hist = fp.cargar(con)
    for c in hist.columns:
        if c not in fut:
            fut[c] = np.nan
    minutos = pd.concat([fm.dataset(con), proj], ignore_index=True)
    df = fp.construir(con, pd.concat([hist, fut[hist.columns]], ignore_index=True), minutos=minutos)
    df = df[df["minutes"].isna() & df["game_id"].isin(proj["game_id"])].reset_index(drop=True)
    # Proyección de minutos y sus variables (las usan las explicaciones SHAP del modelo de minutos).
    extra = [c for c in fm.FEATURES if c not in df.columns]
    df = df.merge(proj[["game_id", "player_id", "min_si_juega", "min_q10", "min_q90", "p_dnp", "prob_juega",
                        "estado_lesion", "min_pred"] + extra], on=["game_id", "player_id"], how="left")
    m = modelo_vigente(con, cfg, RAIZ / cfg.get("puntos", {}).get("modelo", "data/modelos/puntos.joblib"))
    entrada = entrada_simulacion(m, df)
    sims = simular(entrada, m.disp, n_sims=n_sims, semilla=semilla)
    out = pd.concat([df[["game_id", "player_id", "team_id", "name", "estado_lesion", "prob_juega", "p_dnp",
                         "min_si_juega"]], resumen(sims["pts"]).add_prefix("pts_")], axis=1)
    out["fecha"] = pd.to_datetime(fecha).date()
    out["created_at"] = db.ahora_utc()
    con.execute("DELETE FROM proj_puntos WHERE game_id IN (SELECT unnest(?))", [list(df["game_id"].unique())])
    db.upsert(con, "proj_puntos", out)
    return out, {"filas": df, "sims": sims}


def probabilidades_lineas(con, filas: pd.DataFrame, sims: dict, corte=None) -> pd.DataFrame:
    """P(over), P(under) y P(push) de cada línea de puntos capturada para los jugadores simulados."""
    from ..data import asof, db
    from .simulacion import prob_over
    corte = corte or db.ahora_utc()
    cuotas = asof.cuotas_en(con, corte, list(filas["game_id"].unique()))
    lin = cuotas[(cuotas["market"] == "pts") & (cuotas["period"] == "game") & (cuotas["bet_type"] == "ou")]
    lin = lin[["game_id", "player_id", "line"]].dropna().drop_duplicates()
    pos = filas.reset_index()[["index", "game_id", "player_id"]]
    lin = lin.merge(pos, on=["game_id", "player_id"])
    if lin.empty:
        return lin
    p_over, p_push = prob_over(sims["pts"][lin["index"].to_numpy()], lin["line"].to_numpy())
    lin["p_over"], lin["p_push"] = p_over, p_push
    lin["p_under"] = 1 - p_over - p_push
    lin["market"], lin["period"] = "pts", "game"
    return lin.drop(columns="index")
