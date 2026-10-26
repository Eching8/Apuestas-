"""Pruebas del motor de backtest de apuestas."""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from nbaev.backtest import apuestas as ap


def lineas():
    """Tres jugadores de un partido y uno de otro; el modelo ve valor en el over de p1 y p2."""
    return pd.DataFrame({
        "game_id": ["g1", "g1", "g1", "g2"], "player_id": ["p1", "p2", "p3", "p4"], "fecha": ["d1"] * 4,
        "line": [20.5, 10.5, 15.5, 8.5], "cuota_over": [1.91] * 4, "cuota_under": [1.91] * 4,
        "p_mercado": [0.5] * 4, "p_modelo": [0.60, 0.57, 0.52, 0.40], "y": [1, 0, 1, 0],
        "linea_cierre": [21.5, 10.5, np.nan, 8.5], "co_cierre": [1.91] * 4, "cu_cierre": [1.91] * 4,
        "p_mercado_cierre": [0.5, 0.45, np.nan, 0.5],
    })


def test_seleccion_por_edge_y_lado():
    x = ap.seleccionar(lineas(), ap.Estrategia("t", "p_modelo", edge_min=0.04))
    elegidas = dict(zip(x["player_id"], x["lado"]))
    assert elegidas == {"p1": "over", "p2": "over", "p4": "under"}       # p3: edge 2 % < 4 %
    assert x.set_index("player_id").loc["p1", "ganancia"] == pytest.approx(0.91)
    assert x.set_index("player_id").loc["p2", "ganancia"] == -1.0


def test_tope_por_partido():
    x = ap.seleccionar(lineas(), ap.Estrategia("t", "p_modelo", edge_min=0.0, max_por_partido=1))
    assert (x.groupby("game_id").size() <= 1).all()
    assert x[x["game_id"] == "g1"]["player_id"].iloc[0] == "p1"           # la de mayor EV


def test_clv_y_batir_cierre():
    x = ap.seleccionar(lineas(), ap.Estrategia("t", "p_modelo", edge_min=0.04)).set_index("player_id")
    assert x.loc["p1", "bate_cierre"] == 1.0                     # over 20,5 y cerró en 21,5
    assert x.loc["p2", "bate_cierre"] == 0.0                     # misma línea, el over se abarató
    assert x.loc["p2", "clv"] == pytest.approx(1.91 * 0.45 - 1)
    assert x.loc["p1", "clv_ajustado"] > x.loc["p2", "clv_ajustado"]


def test_holm():
    adj = ap.holm(pd.Series([0.01, 0.04, 0.03]))
    assert list(adj.round(4)) == [0.03, 0.06, 0.06]


def test_drawdown():
    assert ap.maximo_drawdown(pd.Series([1, -1, -1, -1, 1])) == 3.0


def test_estado_mercado():
    m = {"apuestas": 500, "clv_ajustado": 0.02, "bate_cierre": 0.6}
    assert ap.estado_mercado(m) == "validado"
    assert ap.estado_mercado({**m, "apuestas": 100}) == "sin validar"
    assert ap.estado_mercado(m, {"apuestas": 400, "roi_ic_inf": -0.02}) == "desactivado"
