"""Modelos de tasa por minuto de rebotes, asistencias, robos, tapones y pérdidas, y mercados derivados.

Cada estadística tiene su LightGBM (objetivo: estadística por minuto, ponderado por minutos) con el
historial del jugador, su rol, la defensa rival frente a su posición EN ESA ESTADÍSTICA, el ritmo y el
contexto del partido. En la simulación cada estadística es binomial negativa con media tasa x minutos x
ritmo, con la varianza estimada con datos. Los puntos y los tiros salen del modelo de puntos.

Los mercados combinados (PR, PA, RA, PRA, robos + tapones), doble-doble y triple-doble se calculan sobre
las mismas simulaciones: son coherentes con los mercados simples por construcción.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import lightgbm as lgb
import numpy as np
import pandas as pd

from . import puntos as mp
from .simulacion import Dispersion

STATS = ["oreb", "dreb", "ast", "stl", "blk", "tov"]
COMUNES = ["r_pts", "r_fga", "r_fg3a", "r_fta", "r_oreb", "r_dreb", "r_ast", "r_stl", "r_blk", "r_tov", "usg_ewm",
           "n_hist", "min_base", "titular_ewm", "libres", "libres_pos", "fga_libres", "def_drtg", "ritmo_esp", "total",
           "total_implicito", "spread_equipo", "is_home", "b2b", "dias_descanso", "playoffs", "pos_g", "pos_f", "pos_c"]
PARAMS = {**mp.PARAMS}

# Mercado -> cómo se calcula a partir de las simulaciones.
DERIVADOS = {
    "reb": ("oreb", "dreb"), "pr": ("pts", "oreb", "dreb"), "pa": ("pts", "ast"), "ra": ("oreb", "dreb", "ast"),
    "pra": ("pts", "oreb", "dreb", "ast"), "stocks": ("stl", "blk"),
}
SIMPLES = {"pts", "oreb", "dreb", "ast", "stl", "blk", "tov", "fg3m", "fgm", "ftm"}


def features(stat: str) -> list[str]:
    return COMUNES + [f"def_pos_{stat}"]


@dataclass
class ModeloProduccion:
    puntos: mp.ModeloPuntos = field(default_factory=mp.ModeloPuntos)
    tasas: dict[str, lgb.Booster] = field(default_factory=dict)
    tam: dict[str, float] = field(default_factory=dict)     # tamaño de la binomial negativa de cada estadística


def entrenar(df: pd.DataFrame, rondas: int = 400, cuantilico: bool = False) -> ModeloProduccion:
    m = ModeloProduccion(puntos=mp.entrenar(df, cuantilico=cuantilico))
    d = df[df["minutes"] >= 3]
    v_ritmo = m.puntos.disp.sd_ritmo ** 2
    for st in STATS:
        X = d[features(st)].astype(float)
        m.tasas[st] = lgb.train({**PARAMS, "objective": "regression"},
                                lgb.Dataset(X, d[st] / d["minutes"], weight=d["minutes"]), rondas)
        # Varianza: Var = mu + mu^2 (1/tam + var_ritmo), con la media prevista por la tasa previa del jugador.
        mu = (d[f"r_{st}"] * d["minutes"]).to_numpy()
        y = d[st].to_numpy()
        inv = max(((y - mu) ** 2 - mu).mean() / (mu ** 2).mean() - v_ritmo, 0.005)
        m.tam[st] = float(1 / inv)
    return m


def entrada(m: ModeloProduccion, df: pd.DataFrame, usar_lgb: bool = True) -> pd.DataFrame:
    """Entrada de la simulación con las tasas de todas las estadísticas."""
    out = mp.entrada_simulacion(m.puntos, df, usar_lgb=usar_lgb)
    for st in STATS:
        if usar_lgb and st in m.tasas:
            out[f"r_{st}"] = np.clip(m.tasas[st].predict(df[features(st)].astype(float)), 0.0, 2.0)
        else:
            out[f"r_{st}"] = df[f"r_{st}"].to_numpy()
    return out


def disp_completa(m: ModeloProduccion) -> Dispersion:
    d = m.puntos.disp
    d.tam_stats = dict(m.tam)
    return d


def valor_mercado(sims: dict[str, np.ndarray], mercado: str) -> np.ndarray:
    """Array (jugadores, simulaciones) con el valor del mercado en cada simulación."""
    if mercado in SIMPLES:
        return sims[mercado]
    if mercado in DERIVADOS:
        return sum(sims[c] for c in DERIVADOS[mercado])
    if mercado in ("doble_doble", "triple_doble"):
        cats = [sims["pts"], sims["oreb"] + sims["dreb"], sims["ast"], sims["stl"], sims["blk"]]
        n10 = sum((c >= 10).astype(np.int8) for c in cats)
        return (n10 >= (2 if mercado == "doble_doble" else 3)).astype(np.int8)
    raise KeyError(mercado)
