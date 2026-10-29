"""Pruebas de la simulación y del modelo de puntos (fase 3)."""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from nbaev.models import simulacion as sim


def jugadores(n=3):
    return pd.DataFrame({
        "game_id": ["g1"] * n, "team_id": ["A"] * (n - 1) + ["B"], "player_id": [f"p{i}" for i in range(n)],
        "min_media": [34.0, 20.0, 30.0][:n], "min_sd": [4.0, 5.0, 4.0][:n], "min_base": [33.0, 18.0, 30.0][:n],
        "spread_equipo": [-5.0, -5.0, 5.0][:n], "is_home": [1, 1, 0][:n],
        "r_fga": [0.55, 0.30, 0.45][:n], "r_fg3a": [0.20, 0.15, 0.10][:n], "r_fta": [0.20, 0.05, 0.12][:n],
        "p_fg2": [0.55, 0.50, 0.58][:n], "p_fg3": [0.37, 0.35, 0.30][:n], "p_ft": [0.85, 0.75, 0.70][:n],
    })


def test_coherencia_entre_lineas():
    s = sim.simular(jugadores(), sim.Dispersion(), n_sims=5000, semilla=1)["pts"]
    lineas = np.arange(0.5, 50.5, 1.0)
    for i in range(s.shape[0]):
        p = [sim.prob_over(s[i:i + 1], [l])[0][0] for l in lineas]
        assert all(a >= b for a, b in zip(p, p[1:]))          # P(20+) >= P(25+) siempre


def test_puntos_son_suma_de_componentes():
    r = sim.simular(jugadores(), sim.Dispersion(), n_sims=2000, semilla=2)
    np.testing.assert_array_equal(r["pts"], 2 * (r["fgm"] - r["fg3m"]) + 3 * r["fg3m"] + r["ftm"])
    assert (r["fg3m"] <= r["fg3a"]).all() and (r["fgm"] <= r["fga"]).all() and (r["ftm"] <= r["fta"]).all()


def test_media_cerca_de_tasa_por_minutos():
    j = jugadores()
    r = sim.simular(j, sim.Dispersion(), n_sims=20000, semilla=3)
    tasa = 2 * (j.r_fga - j.r_fg3a) * j.p_fg2 + 3 * j.r_fg3a * j.p_fg3 + j.r_fta * j.p_ft
    esperado = (tasa * j.min_media).to_numpy()
    assert np.allclose(r["pts"].mean(axis=1), esperado, rtol=0.06)


def test_prob_over_con_empate():
    s = np.array([[10, 10, 11, 9]])
    p_over, p_push = sim.prob_over(s, [10])
    assert p_over[0] == 0.25 and p_push[0] == 0.5


def test_ritmo_correlaciona_jugadores_del_mismo_partido():
    j = jugadores()
    d = sim.Dispersion(sd_ritmo=0.10, sd_acierto=0.0)
    r = sim.simular(j, d, n_sims=20000, semilla=4)["fga"]
    assert np.corrcoef(r[0], r[2])[0, 1] > 0.05          # equipos distintos, mismo ritmo


def test_estimar_dispersion_recupera_parametros():
    rng = np.random.default_rng(5)
    n = 40000
    mins = rng.uniform(15, 38, n)
    r_fga, r_fta, r_fg3a = 0.45, 0.15, 0.18
    tam_fga, tam_fta = 15.0, 3.0
    fga = rng.negative_binomial(tam_fga, tam_fga / (tam_fga + r_fga * mins))
    fta = rng.negative_binomial(tam_fta, tam_fta / (tam_fta + r_fta * mins))
    fg3a = rng.binomial(fga, r_fg3a / r_fga)
    p2 = rng.beta(0.53 * 50, 0.47 * 50, n)
    fgm2 = rng.binomial(fga - fg3a, p2)
    fg3m = rng.binomial(fg3a, 0.36)
    ftm = rng.binomial(fta, 0.78)
    df = pd.DataFrame({"minutes": mins, "fga": fga, "fta": fta, "fg3a": fg3a, "fgm": fgm2 + fg3m, "fg3m": fg3m,
                       "ftm": ftm, "r_fga": r_fga, "r_fta": r_fta, "r_fg3a": r_fg3a, "p_fg2": 0.53, "p_fg3": 0.36,
                       "p_ft": 0.78, "game_id": np.arange(n)})
    d = sim.estimar_dispersion(df)
    assert d.tam_fga == pytest.approx(tam_fga, rel=0.25)
    assert d.tam_fta == pytest.approx(tam_fta, rel=0.25)
    assert d.conc_fg2 == pytest.approx(50, rel=0.35)
    assert d.conc_fg3 > 200                                 # sin sobredispersión -> concentración alta
