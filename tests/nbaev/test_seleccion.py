"""Pruebas de la comparación con cuotas, la mezcla y el registro de apuestas (fase 5)."""
from __future__ import annotations

from datetime import datetime

import numpy as np
import pandas as pd
import pytest

from nbaev.betting import mezcla, registro, seleccion
from nbaev.data import db

CFG = {"apuestas": {"edge_min": 0.04, "fdr": 1.0, "min_minutos": 15, "excluir_en_duda": True, "max_por_jugador": 1,
                    "max_por_partido": 3, "fraccion_kelly": 0.25, "tope_apuesta": 0.02, "tope_diario": 0.10},
       "cuotas": {"casa_principal": "bet365"}}


def escenario():
    """Dos jugadores: p1 anota ~25 (línea 20,5 a cuota pareja: valor en el over); p2 en duda."""
    rng = np.random.default_rng(0)
    sims = {"pts": np.vstack([rng.poisson(25, 10000), rng.poisson(25, 10000)])}
    for k in ("fg3m", "fgm", "ftm"):
        sims[k] = np.zeros_like(sims["pts"])
    filas = pd.DataFrame({"game_id": ["g1", "g1"], "player_id": ["p1", "p2"], "name": ["Uno", "Dos"],
                          "team_id": ["A", "A"], "estado_lesion": [None, "Questionable"], "min_si_juega": [34.0, 30.0],
                          "p_dnp": [0.0, 0.0]})
    filas_cuotas = []
    for pid in ("p1", "p2"):
        for book, o, u in (("fanduel", 1.91, 1.91), ("bet365", 1.87, 1.95), ("consenso", 1.91, 1.91)):
            for side, odds in (("over", o), ("under", u)):
                filas_cuotas.append({"source": "sgo" if book != "bet365" else "csv", "book": book, "game_id": "g1",
                                     "player_id": pid, "player_name": pid, "market": "pts", "period": "game",
                                     "bet_type": "ou", "line": 20.5, "side": side, "odds": odds})
    return filas, sims, pd.DataFrame(filas_cuotas)


def test_evaluar_elige_principal_y_filtra():
    filas, sims, cuotas = escenario()
    lineas = seleccion.lineas_con_lados(cuotas)
    m = {"pts": mezcla.Mezcla(peso_mercado=0.5, peso_modelo=0.5, sd_edge=0.03)}
    t = seleccion.evaluar(lineas, filas, sims, m, CFG, {("pts", "game"): "validado"}, 1000.0).set_index("player_id")
    assert t.loc["p1", "lado"] == "over" and t.loc["p1", "book"] == "bet365"     # casa principal aunque pague menos
    assert t.loc["p1", "pick"] and t.loc["p1", "monto"] == pytest.approx(20.0)   # tope del 2 % de 1.000
    assert not t.loc["p2", "pick"] and "en duda" in t.loc["p2", "motivo_descarte"]


def test_sin_validar_no_recibe_monto():
    filas, sims, cuotas = escenario()
    lineas = seleccion.lineas_con_lados(cuotas)
    t = seleccion.evaluar(lineas, filas, sims, {"pts": mezcla.Mezcla(peso_mercado=0.5, peso_modelo=0.5)}, CFG, {}, 1000.0)
    assert (t["monto"] == 0).all() and (t["estado_mercado"] == "sin validar").all()


def test_mezcla_y_bh():
    m = mezcla.Mezcla(peso_mercado=1.0, peso_modelo=0.0)
    assert m.aplicar(0.6, 0.9) == pytest.approx(0.6, abs=1e-6)
    p = pd.Series([0.001, 0.02, 0.03, 0.5])
    assert list(mezcla.benjamini_hochberg(p, 0.1)) == [True, True, True, False]
    assert list(mezcla.benjamini_hochberg(p, 0.01)) == [True, False, False, False]


def test_registro_y_liquidacion():
    con = db.conectar(":memory:")
    db.upsert(con, "games", [{"game_id": "g1", "season": 2026, "season_type": 2, "start_utc": datetime(2026, 10, 27),
                              "fecha": datetime(2026, 10, 26).date(), "home_id": "A", "away_id": "B",
                              "status": "STATUS_FINAL", "box_ok": True}])
    db.insertar(con, "player_games", [{"game_id": "g1", "player_id": "p1", "team_id": "A", "minutes": 34, "pts": 27}])
    tabla = pd.DataFrame([{"game_id": "g1", "player_id": "p1", "name": "Uno", "market": "pts", "period": "game",
                           "line": 20.5, "lado": "over", "book": "bet365", "cuota": 1.87, "p_modelo": 0.7, "p_final": 0.6,
                           "edge": 0.08, "ev": 0.12, "monto": 20.0, "pick": True}])
    assert registro.registrar_sugeridas(con, tabla, datetime(2026, 10, 26).date(), {}) == 1
    assert registro.registrar_sugeridas(con, tabla, datetime(2026, 10, 26).date(), {}) == 0     # sin duplicados
    registro.confirmar(con, 1, cuota=1.9)
    db.insertar(con, "prop_odds", [{"game_id": "g1", "player_id": "p1", "market": "pts", "period": "game", "line": 20.5,
                                    "kind": "cierre", "book": "consenso", "side": s, "odds": o}
                                   for s, o in (("over", 1.7), ("under", 2.15))])
    assert registro.liquidar(con) == 1
    r = con.execute("SELECT resultado, ganancia, cuota_cierre, clv FROM apuestas WHERE id = 1").fetchone()
    assert r[0] == "ganada" and r[1] == pytest.approx(18.0) and r[2] == 1.7 and r[3] > 0
    assert registro.banca_actual(con, 1000.0) == pytest.approx(1018.0)
