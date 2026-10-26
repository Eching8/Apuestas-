"""Pruebas de margen, EV y Kelly."""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from nbaev.betting import banca, margen


@pytest.mark.parametrize("metodo", ["multiplicativo", "power", "shin"])
def test_quitar_margen_suma_uno(metodo):
    for cuotas in ([1.91, 1.91], [1.5, 2.6], [2.2, 3.4, 3.6], [4.0] * 10 + [1.3]):
        p = margen.justa(cuotas, metodo)
        assert p.sum() == pytest.approx(1.0, abs=1e-9)
        assert (p > 0).all()


def test_margen_y_simetria():
    assert margen.margen([1.91, 1.91]) == pytest.approx(2 / 1.91 - 1)
    assert margen.justa([1.91, 1.91]) == pytest.approx([0.5, 0.5])


def test_power_y_shin_cargan_mas_al_improbable():
    cuotas = [1.25, 4.2]
    mult, pw, sh = (margen.justa(cuotas, m) for m in ("multiplicativo", "power", "shin"))
    # El favorito recibe más probabilidad justa (el margen se carga al improbable).
    assert pw[0] > mult[0] and sh[0] > mult[0]


def test_sin_margen_no_cambia():
    cuotas = [2.0, 2.0]
    for m in ("multiplicativo", "power", "shin"):
        assert margen.justa(cuotas, m) == pytest.approx([0.5, 0.5])


def test_dos_lados_vectorizado():
    p = margen.justa_dos_lados([1.8, 2.1], [2.0, 1.75])
    assert p[0] == pytest.approx((1 / 1.8) / (1 / 1.8 + 1 / 2.0))


def test_ev_y_edge():
    assert margen.ev(0.55, 2.0) == pytest.approx(0.10)
    assert margen.ev(0.80, 1.15) < 0          # 80 % de probabilidad pero mala apuesta
    assert margen.edge(0.55, 0.50) == pytest.approx(0.05)


def test_kelly_y_topes():
    assert banca.kelly(0.55, 2.0) == pytest.approx(0.10)
    r = banca.ReglasBanca()
    assert banca.fraccion(0.55, 2.0, r) == pytest.approx(0.02)          # 1/4 Kelly = 2,5 % -> tope 2 %
    assert banca.fraccion(0.52, 2.0, r) == pytest.approx(0.01)
    assert banca.fraccion(0.45, 2.0, r) == 0.0                          # EV negativo: nada


def test_tope_diario():
    f = pd.Series([0.02] * 8 + [0.02])
    d = pd.Series(["a"] * 8 + ["b"])
    out = banca.aplicar_tope_diario(f, d, 0.10)
    assert out[:8].sum() == pytest.approx(0.10) and out.iloc[8] == pytest.approx(0.02)


def test_simular_banca_drawdown():
    a = pd.DataFrame({"fecha": ["d1", "d2", "d3"], "p": [0.6, 0.6, 0.6], "cuota": [2.0, 2.0, 2.0],
                      "resultado": [1, 0, 0]})
    h = banca.simular_banca(a, banca.ReglasBanca(), 100.0)
    assert h["banca"].iloc[0] == pytest.approx(102.0)
    assert h["drawdown"].max() > 0
    assert np.isclose(h["banca"].iloc[-1], 102.0 * 0.98 * 0.98)
