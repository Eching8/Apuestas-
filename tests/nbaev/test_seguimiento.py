"""Pruebas del seguimiento de props (valor real de cada tipo de mercado)."""
from __future__ import annotations

from datetime import datetime

import numpy as np
import pandas as pd

from nbaev import seguimiento
from nbaev.data import db


def test_valores_reales_por_mercado():
    con = db.conectar(":memory:")
    db.upsert(con, "games", [{"game_id": "g", "season": 2026, "season_type": 2, "start_utc": datetime(2026, 10, 27),
                              "fecha": datetime(2026, 10, 26).date(), "home_id": "A", "away_id": "B",
                              "status": "STATUS_FINAL", "box_ok": True}])
    db.insertar(con, "player_games", [{"game_id": "g", "player_id": "p", "team_id": "A", "minutes": 34, "pts": 22,
                                       "reb": 11, "oreb": 3, "dreb": 8, "ast": 4, "stl": 1, "blk": 0, "tov": 2,
                                       "fg3m": 2, "fgm": 8, "ftm": 4}])
    db.insertar(con, "player_periods", [{"game_id": "g", "player_id": "p", "team_id": "A", "period": q, "pts": v,
                                         "oreb": 0, "dreb": 2, "ast": 1} for q, v in ((1, 7), (2, 5), (3, 6), (4, 4))])
    db.insertar(con, "game_starts", [{"game_id": "g", "first_fg_player": "p"}])
    pred = pd.DataFrame({"game_id": ["g"] * 6 + ["g"], "player_id": ["p"] * 6 + ["x"],
                         "market": ["pts", "pra", "doble_doble", "pts", "primera_canasta", "triple_doble", "pts"],
                         "period": ["game", "game", "game", "1q", "game", "game", "game"],
                         "line": [20.5, 37.5, -1, 6.5, -1, -1, 10.5]})
    v = seguimiento.valores_reales(con, pred)
    assert list(v[:6]) == [22.0, 37.0, 1.0, 7.0, 1.0, 0.0]
    assert np.isnan(v.iloc[6])                 # no jugó: nula
