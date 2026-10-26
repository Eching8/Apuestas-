"""Las 3 razones principales de cada pick, con valores SHAP de los modelos de minutos y de tasa.

Las contribuciones se expresan en unidades de la estadística del mercado (puntos, rebotes...): valor =
tasa x minutos, así que una contribución SHAP a la tasa vale (contribución x minutos proyectados) y una a
los minutos vale (contribución x tasa proyectada). En mercados combinados se suman las de sus componentes.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

NOMBRES = {
    "r_pts": "anotación por minuto reciente", "r_pts_comp": "anotación por minuto (tiros y acierto)",
    "r_pts_temp": "anotación por minuto en la temporada", "r_fga": "tiros por minuto", "r_fg3a": "triples intentados por minuto",
    "r_fta": "tiros libres por minuto", "p_fg2": "% de 2", "p_fg3": "% de 3", "p_ft": "% de libres",
    "usg_ewm": "uso (usage) reciente", "ts_ewm": "true shooting reciente", "n_hist": "partidos de historial",
    "min_base": "minutos habituales", "titular_ewm": "frecuencia como titular", "libres": "minutos libres en el equipo (bajas)",
    "libres_pos": "minutos libres en su posición", "fga_libres": "tiros libres de compañeros ausentes",
    "def_pos": "defensa rival frente a su posición", "def_drtg": "rating defensivo del rival", "ritmo_esp": "ritmo esperado",
    "total": "total del partido", "total_implicito": "puntos esperados de su equipo", "spread_equipo": "spread",
    "is_home": "local", "b2b": "back-to-back", "dias_descanso": "días de descanso", "playoffs": "playoffs",
    "pos_g": "posición base/escolta", "pos_f": "posición alero", "pos_c": "posición pívot",
    "min_ewm3": "minutos últimos partidos", "min_ewm10": "minutos últimos 10", "min_temp": "minutos en la temporada",
    "min_temp_ant": "minutos temporada anterior", "min_ult": "minutos del último partido", "min_max10": "máximo de minutos reciente",
    "min_std10": "variabilidad de minutos", "n_temp": "partidos en la temporada", "n_equipo": "partidos con su equipo",
    "titular_ult": "titular en el último partido", "dnp_ewm": "frecuencia sin jugar", "pf36_ewm": "faltas por 36 min",
    "dias_desde": "días desde su último partido", "cambio_equipo": "cambio de equipo", "min_norm": "minutos normalizados del equipo",
    "rango_equipo": "jerarquía en la rotación", "n_disponibles": "jugadores disponibles", "suma_base": "minutos habituales disponibles",
    "partidos_4d": "partidos en 4 días", "km_viaje": "km de viaje", "spread_abs": "riesgo de paliza", "partido_temp": "jornada",
}


def _shap(booster, X: pd.DataFrame) -> np.ndarray:
    """Valores SHAP (TreeSHAP exacto). Usa la librería shap y, si no está, la implementación de LightGBM."""
    try:
        import shap
        return np.asarray(shap.TreeExplainer(booster).shap_values(X))
    except Exception:
        return booster.predict(X, pred_contrib=True)[:, :-1]


# Componentes de cada mercado con modelo de tasa propio (los tiros salen del modelo de puntos).
COMPONENTES = {"pts": ["pts"], "fg3m": ["pts"], "fgm": ["pts"], "ftm": ["pts"], "oreb": ["oreb"], "dreb": ["dreb"],
               "reb": ["oreb", "dreb"], "ast": ["ast"], "stl": ["stl"], "blk": ["blk"], "tov": ["tov"],
               "pr": ["pts", "oreb", "dreb"], "pa": ["pts", "ast"], "ra": ["oreb", "dreb", "ast"],
               "pra": ["pts", "oreb", "dreb", "ast"], "stocks": ["stl", "blk"],
               "doble_doble": ["pts", "oreb", "dreb", "ast"], "triple_doble": ["pts", "oreb", "dreb", "ast"]}


def contribuciones(m_prod, m_minutos, filas: pd.DataFrame, mercado: str = "pts") -> pd.DataFrame:
    """Contribución (en unidades de la estadística del mercado) de cada variable para cada jugador.
    `m_prod` es un ModeloProduccion (o un ModeloPuntos, solo para puntos)."""
    from ..features.minutos import FEATURES as F_MIN
    from ..features.minutos import a_matriz
    from ..features.produccion import FEATURES_PTS
    from ..models import estadisticas as me
    from ..models.puntos import _X
    m_pts = getattr(m_prod, "puntos", m_prod)
    total = None
    tasa_total = np.zeros(len(filas))
    for c in COMPONENTES.get(mercado, ["pts"]):
        if c == "pts":
            X, booster, cols = _X(filas), m_pts.tasa, FEATURES_PTS
        else:
            cols = me.features(c)
            X, booster = filas[cols].astype(float), m_prod.tasas[c]
        tasa_total += np.clip(booster.predict(X), 0, 2)
        parte = pd.DataFrame(_shap(booster, X) * filas["min_si_juega"].to_numpy()[:, None], columns=cols,
                             index=filas.index)
        total = parte if total is None else total.add(parte, fill_value=0.0)
    c_min = pd.DataFrame(_shap(m_minutos.media_juega, a_matriz(filas)) * tasa_total[:, None], columns=F_MIN,
                         index=filas.index)
    return total.add(c_min, fill_value=0.0)


def razones(contrib: pd.DataFrame, filas: pd.DataFrame, lado: pd.Series, n: int = 3) -> pd.Series:
    """Texto con las `n` variables que más empujan hacia el lado apostado (over: positivas; under: negativas)."""
    out = {}
    for i in contrib.index:
        signo = 1.0 if lado.get(i, "over") in ("over", "yes", "sí") else -1.0
        c = contrib.loc[i] * signo
        top = c[c > 0].sort_values(ascending=False).head(n)
        if len(top) < n:
            top = pd.concat([top, c.drop(top.index).abs().sort_values(ascending=False).head(n - len(top))])
        partes = []
        for f in top.index:
            v = filas.at[i, f] if f in filas.columns else np.nan
            valor = "" if pd.isna(v) else f" ({v:.2f})" if abs(v) < 10 else f" ({v:.0f})"
            partes.append(f"{NOMBRES.get(f, f)}{valor}: {contrib.at[i, f]:+.1f}")
        out[i] = "; ".join(partes)
    return pd.Series(out)
