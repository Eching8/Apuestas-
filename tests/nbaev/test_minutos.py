"""Pruebas de la fase 2 (minutos) con datos sintéticos."""
from __future__ import annotations

from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import pytest

from nbaev.backtest.walkforward import bloques_mensuales, walk_forward
from nbaev.features import minutos as fm
from nbaev.models import minutos as mm


def historial(n_partidos=30, semilla=1):
    """Dos equipos de 8 jugadores con minutos estables; el jugador A1 falta en el último partido."""
    rng = np.random.default_rng(semilla)
    filas = []
    t0 = datetime(2025, 11, 1)
    for k in range(n_partidos):
        gid = f"g{k:03d}"
        for team, opp in (("A", "B"), ("B", "A")):
            for i in range(8):
                pid = f"{team}{i}"
                if pid == "A1" and k == n_partidos - 1:
                    continue  # baja: no está vestido
                base = 36 - 3.5 * i
                filas.append({"game_id": gid, "player_id": pid, "team_id": team, "name": pid, "position": "G",
                              "starter": i < 5, "minutes": max(0.0, base + rng.normal(0, 2)), "pf": 2,
                              "vestido": True, "start_utc": t0 + timedelta(days=2 * k), "fecha": None,
                              "season": 2025, "season_type": 2, "opp_id": opp, "is_home": team == "A",
                              "b2b": False, "dias_descanso": 1, "partidos_4d": 2, "km_viaje": 0.0,
                              "spread_equipo": 0.0, "total": 225.0})
    return pd.DataFrame(filas)


def test_features_sin_fuga():
    """Cambiar los minutos del último partido no puede cambiar sus propias features."""
    df = historial()
    a = fm.construir(df)
    df2 = df.copy()
    ultimo = df2["game_id"] == df2["game_id"].max()
    df2.loc[ultimo, "minutes"] = 0.0
    b = fm.construir(df2)
    cols = [c for c in fm.FEATURES if c not in ("partido_temp",)]
    ka = a[a["game_id"] == df["game_id"].max()].sort_values("player_id")[cols].reset_index(drop=True)
    kb = b[b["game_id"] == df["game_id"].max()].sort_values("player_id")[cols].reset_index(drop=True)
    pd.testing.assert_frame_equal(ka, kb)


def test_minutos_libres_cuando_falta_un_titular():
    f = fm.construir(historial())
    ultimo = f[f["game_id"] == f["game_id"].max()]
    libres_a = ultimo[ultimo["team_id"] == "A"]["libres"].iloc[0]
    libres_b = ultimo[ultimo["team_id"] == "B"]["libres"].iloc[0]
    assert libres_a > 25 and abs(libres_b) < 6      # A1 (~32 min) no está
    # Normalizar a 240 reparte sus minutos entre los demás del equipo A.
    a0 = ultimo[ultimo["player_id"] == "A0"].iloc[0]
    assert a0["min_norm"] > a0["min_base"]


def test_prob_juega_pondera_disponibles():
    df = historial()
    futuro = df[df["game_id"] == df["game_id"].max()].copy()
    futuro["game_id"], futuro["minutes"] = "futuro", np.nan
    futuro["start_utc"] = futuro["start_utc"] + timedelta(days=2)
    futuro["prob_juega"] = np.where(futuro["player_id"] == "A0", 0.5, 1.0)
    f = fm.construir(pd.concat([df, futuro], ignore_index=True))
    fila = f[(f["game_id"] == "futuro") & (f["team_id"] == "A")].iloc[0]
    a0 = f[(f["game_id"] == "futuro") & (f["player_id"] == "A0")].iloc[0]
    assert fila["suma_base"] == pytest.approx(
        f[(f["game_id"] == "futuro") & (f["team_id"] == "A")]["min_base"].sum() - 0.5 * a0["min_base"])


def test_repartir_suma_y_tope():
    df = pd.DataFrame({"game_id": ["g"] * 3, "team_id": ["A"] * 3})
    p = mm.repartir_equipo(df, pd.Series([47.0, 30.0, 20.0]), 120.0)
    assert p.max() <= 48.0 and p.sum() == pytest.approx(120.0, abs=0.5)


def test_prob_juega_tabla():
    tabla = {"Out": 0.0, "Questionable": 0.5, "otro": 0.4}
    assert fm.prob_juega(None, tabla) == 1.0
    assert fm.prob_juega("out", tabla) == 0.0
    assert fm.prob_juega("Raro", tabla) == 0.4


def test_walk_forward_no_mira_el_futuro():
    df = pd.DataFrame({"start_utc": pd.date_range("2025-01-01", periods=120, freq="D"), "y": range(120)})
    vistos = []

    def entrenar(train):
        vistos.append(train["start_utc"].max())
        return train["start_utc"].max()

    def predecir(maximo, test):
        assert maximo < test["start_utc"].min()
        return pd.DataFrame({"pred": 0}, index=test.index)

    res = walk_forward(df, entrenar, predecir, "2025-02-01")
    assert set(res["bloque"]) == {"2025-02", "2025-03", "2025-04"}
    assert len(list(bloques_mensuales(df["start_utc"], "2025-02-01", "2025-03-15"))) == 2


def test_modelo_entrena_y_predice():
    f = fm.construir(historial(60))
    m = mm.entrenar(f[f["game_id"] < "g050"], rondas=30)
    p = mm.predecir(m, f[f["game_id"] >= "g050"])
    assert {"min_pred", "min_si_juega", "min_q10", "min_q90", "p_dnp"} <= set(p.columns)
    assert (p["min_q10"] <= p["min_q90"] + 1e-6).all()
    suma = p.groupby([f.loc[p.index, "game_id"], f.loc[p.index, "team_id"]])["min_pred"].sum()
    assert np.allclose(suma, m.minutos_equipo, atol=1.0)
