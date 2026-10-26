"""Pruebas de la fase 6: mercados derivados, periodos, comparativos, combinadas y primer anotador."""
from __future__ import annotations

from types import SimpleNamespace

import numpy as np
import pandas as pd
import pytest

from nbaev.betting import combinadas as cb
from nbaev.betting import seleccion
from nbaev.features import periodos as fper
from nbaev.models import estadisticas as me
from nbaev.models import primer_anotador as pa
from nbaev.models import simulacion as sim


def sims_juego(n=20000, semilla=1):
    j = pd.DataFrame({
        "game_id": ["g"] * 4, "team_id": ["A", "A", "B", "B"], "player_id": ["a1", "a2", "b1", "b2"],
        "name": ["Ana Uno", "Ana Dos", "Beto Uno", "Beto Dos"], "min_media": [34.0, 30.0, 35.0, 28.0],
        "min_sd": [4.0] * 4, "min_base": [33.0, 29.0, 34.0, 27.0], "spread_equipo": [-3.0, -3.0, 3.0, 3.0],
        "is_home": [1, 1, 0, 0], "r_fga": [0.6, 0.4, 0.55, 0.35], "r_fg3a": [0.2, 0.15, 0.2, 0.1],
        "r_fta": [0.2, 0.1, 0.2, 0.08], "p_fg2": [0.55] * 4, "p_fg3": [0.36] * 4, "p_ft": [0.8] * 4,
        "r_oreb": [0.05, 0.08, 0.04, 0.1], "r_dreb": [0.2, 0.25, 0.18, 0.28], "r_ast": [0.25, 0.1, 0.3, 0.08],
        "r_stl": [0.04] * 4, "r_blk": [0.02, 0.05, 0.01, 0.06], "r_tov": [0.08] * 4})
    d = sim.Dispersion(tam_stats={k: 8.0 for k in ("oreb", "dreb", "ast", "stl", "blk", "tov")})
    s = sim.simular(j, d, n_sims=n, semilla=semilla)
    s["reb"] = me.valor_mercado(s, "reb")
    return j, s


def test_combinados_y_dobles_coherentes():
    _, s = sims_juego()
    pra = me.valor_mercado(s, "pra")
    np.testing.assert_array_equal(pra, s["pts"] + s["oreb"] + s["dreb"] + s["ast"])
    dd, td = me.valor_mercado(s, "doble_doble"), me.valor_mercado(s, "triple_doble")
    assert (td <= dd).all()                       # un triple-doble siempre es doble-doble
    assert dd.mean() > td.mean()


def test_periodos_coherentes():
    _, s = sims_juego()
    rng = np.random.default_rng(3)
    q1, h1 = fper.simular_periodos(rng, s["pts"], np.full(4, 0.52), np.full(4, 0.27), 40.0, 40.0)
    assert (q1 <= h1).all() and (h1 <= s["pts"]).all()
    assert q1.mean() / s["pts"].mean() == pytest.approx(0.27, abs=0.02)


def test_combinada_mismo_partido_correlacionada():
    j, s = sims_juego()
    filas = j[["game_id", "player_id", "name", "team_id"]]
    a = cb.Seleccion("Ana Uno", "pts", 15.5, "over", cuota=1.9, p_justa=0.5)
    b = cb.Seleccion("Ana Uno", "pra", 25.5, "over", cuota=1.9, p_justa=0.5)
    r = cb.combinada(filas, s, [a, b])
    assert r["p_conjunta"] > r["p_si_fueran_independientes"]     # mismo jugador: muy correlacionadas
    assert r["margen_acumulado"] == pytest.approx((1 / 3.61) / 0.25 - 1)


def test_duelo_y_maximo_suman_uno():
    j, s = sims_juego()
    filas = j[["game_id", "player_id", "name", "team_id"]]
    d = cb.duelo(filas, s, "Ana Uno", "Beto Dos")
    assert d["p_a"] + d["p_b"] + d["p_empate"] == pytest.approx(1.0)
    m = cb.maximo(filas, s, "g")
    assert m["p"].sum() == pytest.approx(1.0) and m.iloc[0]["jugador"] in ("Ana Uno", "Beto Uno")


def test_lineas_si_no_y_primera_canasta():
    filas = []
    for pid, o in zip("abcdefghij", [4.5, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 12.0, 14.0, 16.0]):
        filas.append({"source": "sgo", "book": "fanduel", "game_id": "g", "player_id": pid, "player_name": pid,
                      "market": "primera_canasta", "period": "game", "bet_type": "yn", "line": np.nan, "side": "yes",
                      "odds": o})
    filas += [{"source": "sgo", "book": "fanduel", "game_id": "g", "player_id": "a", "player_name": "a",
               "market": "doble_doble", "period": "game", "bet_type": "yn", "line": np.nan, "side": s, "odds": o}
              for s, o in (("yes", 3.0), ("no", 1.36))]
    t = seleccion.lineas_con_lados(pd.DataFrame(filas))
    pc = t[t["market"] == "primera_canasta"]
    assert pc["p_justa_over"].sum() == pytest.approx(1.0)
    dd = t[t["market"] == "doble_doble"].iloc[0]
    assert dd["p_justa_over"] == pytest.approx((1 / 3) / (1 / 3 + 1 / 1.36))


def test_primer_anotador_probabilidades():
    est = pa.Estado()
    r = SimpleNamespace(jump_home_player="c1", jump_away_player="c2", jump_winner_team="H", home_id="H", away_id="A",
                        first_fg_team="H", home_starters=["h1", "h2", "h3", "h4", "c1"],
                        away_starters=["a1", "a2", "a3", "a4", "c2"], home_first_fg_player="h1",
                        away_first_fg_player="a2")
    for _ in range(30):
        est.actualizar(r)
    p = pa.predecir_partido(est, "H", "A", r.home_starters, r.away_starters, {})
    assert p["p_partido"].sum() == pytest.approx(1.0)
    assert p.groupby("team_id")["p_equipo"].sum().round(6).eq(1.0).all()
    assert p.set_index("player_id").loc["h1", "p_partido"] == p["p_partido"].max()   # anota siempre primero
    assert p[p["team_id"] == "H"]["p_gana_salto"].iloc[0] > 0.5                       # su pívot gana los saltos
