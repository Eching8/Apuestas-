"""Submodelo de primer anotador (primera canasta de campo del partido y de cada equipo).

P(jugador j anota la primera canasta del partido) = P(su equipo anota primero) x P(j | su equipo anota primero)
- P(su equipo anota primero) = p_salto x q + (1 - p_salto) x (1 - q), con p_salto = P(su equipo gana el salto
  inicial) (Bradley-Terry con la tasa de victorias de cada saltador encogida a 0,5) y q = P(el equipo que gana
  el salto anota primero), estimada con partidos anteriores (~0,63).
- P(j | equipo): cuota de primeras canastas del equipo que hizo j como titular, encogida hacia su peso en el
  volumen de tiro de los titulares; un resto fijo para suplentes.
Todo se calcula partido a partido con información anterior (sin fuga). Los titulares son los confirmados
(este mercado se apuesta con los quintetos publicados, ~30 min antes del salto).
"""
from __future__ import annotations

from collections import defaultdict

import duckdb
import numpy as np
import pandas as pd

K_SALTO = 8.0      # saltos equivalentes del prior (0,5)
K_REPARTO = 15.0   # titularidades equivalentes del prior (peso en el volumen de tiro)


def cargar(con: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    return con.execute("""
        SELECT s.*, g.start_utc, g.season, g.home_id, g.away_id
        FROM game_starts s JOIN games g USING (game_id)
        WHERE g.status = 'STATUS_FINAL' AND len(s.home_starters) = 5 AND len(s.away_starters) = 5
        ORDER BY g.start_utc""").df()


class Estado:
    """Contadores acumulados hasta el partido actual (se actualizan después de predecir cada partido)."""

    def __init__(self):
        self.saltos = defaultdict(lambda: [0.0, 0.0])      # jugador -> [ganados, disputados]
        self.saltador = defaultdict(lambda: defaultdict(int))  # equipo -> jugador -> saltos
        self.primera = defaultdict(lambda: [0.0, 0.0])     # jugador -> [primeras canastas del equipo, titularidades]
        self.q = [0.0, 0.0]                                 # [ganó salto y anotó primero, partidos con salto]
        self.suplentes = [0.0, 0.0]                         # [primera canasta de un suplente, equipos-partido]

    def p_salto(self, a, b) -> float:
        def tasa(j):
            g, n = self.saltos[j]
            return (g + K_SALTO * 0.5) / (n + K_SALTO)
        ta, tb = tasa(a), tasa(b)
        return ta * (1 - tb) / (ta * (1 - tb) + tb * (1 - ta))

    def saltador_probable(self, equipo, titulares) -> str:
        c = self.saltador[equipo]
        return max(titulares, key=lambda j: (c.get(j, 0), j))

    def reparto(self, titulares, peso_tiro: dict) -> dict:
        resto = (self.suplentes[0] + 0.5) / (self.suplentes[1] + 15)
        total_tiro = sum(peso_tiro.get(j, 1.0) for j in titulares)
        w = {}
        for j in titulares:
            prior = peso_tiro.get(j, 1.0) / total_tiro
            f, n = self.primera[j]
            w[j] = (f + K_REPARTO * prior) / (n + K_REPARTO)
        s = sum(w.values())
        return {j: (1 - resto) * v / s for j, v in w.items()}, resto

    def actualizar(self, r):
        if r.jump_home_player and r.jump_away_player and r.jump_winner_team:
            gana_h = r.jump_winner_team == r.home_id
            self.saltos[r.jump_home_player][0] += gana_h
            self.saltos[r.jump_away_player][0] += 1 - gana_h
            self.saltos[r.jump_home_player][1] += 1
            self.saltos[r.jump_away_player][1] += 1
            self.saltador[r.home_id][r.jump_home_player] += 1
            self.saltador[r.away_id][r.jump_away_player] += 1
            if r.first_fg_team:
                self.q[0] += r.first_fg_team == r.jump_winner_team
                self.q[1] += 1
        for lado, equipo in (("home", r.home_id), ("away", r.away_id)):
            tit = list(getattr(r, f"{lado}_starters"))
            primero = getattr(r, f"{lado}_first_fg_player")
            for j in tit:
                self.primera[j][1] += 1
                self.primera[j][0] += primero == j
            if primero:
                self.suplentes[1] += 1
                self.suplentes[0] += primero not in tit

    @property
    def q_salto(self) -> float:
        return (self.q[0] + 0.63 * 50) / (self.q[1] + 50)


def predecir_partido(est: Estado, home_id, away_id, tit_h, tit_a, peso_tiro: dict) -> pd.DataFrame:
    """P(primera canasta del partido) y P(primera canasta de su equipo) de cada titular (+ resto suplentes)."""
    sh, sa = est.saltador_probable(home_id, tit_h), est.saltador_probable(away_id, tit_a)
    p_h = est.p_salto(sh, sa)
    q = est.q_salto
    p_equipo = {home_id: p_h * q + (1 - p_h) * (1 - q)}
    p_equipo[away_id] = 1 - p_equipo[home_id]
    filas = []
    for equipo, tit in ((home_id, tit_h), (away_id, tit_a)):
        rep, resto = est.reparto(tit, peso_tiro)
        for j, p in rep.items():
            filas.append({"team_id": equipo, "player_id": j, "p_equipo": p, "p_partido": p * p_equipo[equipo],
                          "p_gana_salto": p_h if equipo == home_id else 1 - p_h})
        filas.append({"team_id": equipo, "player_id": "SUPLENTE", "p_equipo": resto, "p_partido": resto * p_equipo[equipo],
                      "p_gana_salto": p_h if equipo == home_id else 1 - p_h})
    return pd.DataFrame(filas)


def peso_tiro_hasta(con, antes_de) -> dict:
    """Tiros de campo por partido de cada jugador en sus últimos 20 partidos anteriores (peso del prior)."""
    return dict(con.execute("""
        SELECT player_id, avg(fga) FROM (
            SELECT p.player_id, p.fga, row_number() OVER (PARTITION BY p.player_id ORDER BY g.start_utc DESC) AS k
            FROM player_games p JOIN games g USING (game_id) WHERE g.start_utc < ?) WHERE k <= 20
        GROUP BY 1""", [antes_de]).fetchall())


def validar(con: duckdb.DuckDBPyConnection, desde: str = "2024-10-01") -> dict:
    """Recorre todos los partidos en orden; evalúa desde `desde` (log loss multiclase frente a uniforme y a
    reparto por volumen de tiro) y calibración."""
    partidos = cargar(con)
    fga = con.execute("""SELECT p.player_id, g.start_utc, p.fga FROM player_games p JOIN games g USING (game_id)
                         ORDER BY g.start_utc""").df()
    fga["fga_ewm"] = fga.groupby("player_id")["fga"].transform(lambda s: s.shift(1).ewm(halflife=10).mean())
    ultimo = {}
    filas = []
    est = Estado()
    i_fga = 0
    fga_arr = fga.to_numpy()
    for r in partidos.itertuples():
        while i_fga < len(fga_arr) and fga_arr[i_fga][1] < r.start_utc:
            if not np.isnan(fga_arr[i_fga][3]):
                ultimo[fga_arr[i_fga][0]] = fga_arr[i_fga][3]
            i_fga += 1
        if r.start_utc >= pd.Timestamp(desde) and r.first_fg_player:
            pred = predecir_partido(est, r.home_id, r.away_id, list(r.home_starters), list(r.away_starters), ultimo)
            ganador = r.first_fg_player if pred["player_id"].eq(r.first_fg_player).any() else "SUPLENTE"
            pred = pred.assign(game_id=r.game_id, y=(pred["player_id"] == ganador) & (
                (pred["team_id"] == r.first_fg_team) | (pred["player_id"] != "SUPLENTE")))
            tit = pd.Series({j: ultimo.get(j, 1.0) for j in list(r.home_starters) + list(r.away_starters)})
            pred["p_volumen"] = pred["player_id"].map(tit / tit.sum() * 0.95).fillna(0.025)
            filas.append(pred)
        est.actualizar(r)
    d = pd.concat(filas, ignore_index=True)
    return {"pred": d, "estado": est}


def informe(d: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    gan = d[d["y"]]
    n = gan["game_id"].nunique()
    res = pd.DataFrame([{
        "partidos": n,
        "log loss modelo": float(-np.log(gan["p_partido"].clip(1e-4)).mean()),
        "log loss volumen de tiro": float(-np.log(gan["p_volumen"].clip(1e-4)).mean()),
        "log loss uniforme (1/11)": float(np.log(11)),
        "acierto del salto (equipo que lo gana anota primero)": None,
    }])
    tr = pd.cut(d["p_partido"], [0, 0.05, 0.08, 0.11, 0.14, 0.18, 1.0])
    cal = (d.assign(tramo=tr).groupby("tramo", observed=True)
           .agg(n=("y", "size"), p_media=("p_partido", "mean"), frecuencia_real=("y", "mean")).reset_index())
    cal["tramo"] = cal["tramo"].astype(str)
    return res.drop(columns="acierto del salto (equipo que lo gana anota primero)"), cal
