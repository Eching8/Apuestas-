"""Features de producción (etapa B): tasas por minuto, porcentajes de tiro, defensa rival y ritmo.

Para cada jugador y partido, con información solo de partidos anteriores (`shift(1)`):
- Tasas por minuto de cada estadística: media exponencial (ponderada por minutos) con regresión bayesiana
  hacia la media de su grupo de posición en temporadas anteriores. El peso del prior equivale a
  `K_MIN` minutos jugados: con poca muestra la tasa se acerca a la de su posición.
- Porcentajes de tiro (2P, 3P, TL) con el mismo encogimiento, medido en intentos.
- Defensa rival: lo que concede cada equipo por minuto a cada grupo de posición, relativo a la liga.
- Ritmo: posesiones por 48 minutos de ambos equipos y total implícito del partido.
"""
from __future__ import annotations

import duckdb
import numpy as np
import pandas as pd

from .minutos import grupo_posicion

# Estadísticas de conteo con tasa por minuto.
CONTEOS = ["pts", "fga", "fg3a", "fta", "fgm", "fg3m", "ftm", "oreb", "dreb", "ast", "stl", "blk", "tov"]
VIDA_MEDIA = 12        # partidos: vida media de la media exponencial de tasas
K_MIN = 250.0          # minutos equivalentes del prior de posición
K_INTENTOS = {"fg2": 150.0, "fg3": 250.0, "ft": 80.0}
VIDA_MEDIA_EQUIPO = 15  # partidos: defensa y ritmo de cada equipo

FEATURES_PTS = [
    "r_pts", "r_fga", "r_fg3a", "r_fta", "p_fg2", "p_fg3", "p_ft", "r_pts_comp", "usg_ewm", "ts_ewm",
    "r_pts_temp", "n_hist", "min_base", "titular_ewm", "libres", "libres_pos", "fga_libres",
    "def_pos", "def_drtg", "ritmo_esp", "total", "total_implicito", "spread_equipo", "is_home", "b2b",
    "dias_descanso", "playoffs", "pos_g", "pos_f", "pos_c",
]


def cargar(con: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    """Box score de quienes jugaron con contexto del partido y usage."""
    return con.execute("""
        SELECT p.game_id, p.player_id, p.team_id, p.opp_id, p.name, p.position, p.starter, p.minutes,
               p.pts, p.fgm, p.fga, p.fg3m, p.fg3a, p.ftm, p.fta, p.oreb, p.dreb, p.reb, p.ast, p.stl, p.blk,
               p.tov, p.pf, a.usg_pct, a.ts_pct, g.start_utc, g.season, g.season_type,
               c.is_home, c.b2b, c.dias_descanso, c.spread_equipo, c.total, c.total_implicito
        FROM player_games p
        JOIN games g USING (game_id)
        JOIN v_player_adv a ON a.game_id = p.game_id AND a.player_id = p.player_id
        LEFT JOIN team_context c ON c.game_id = p.game_id AND c.team_id = p.team_id
        WHERE g.status = 'STATUS_FINAL' AND p.minutes > 0
        ORDER BY p.player_id, g.start_utc""").df()


def _ewm_prev(x: pd.Series, grupos: pd.Series, vida: float) -> pd.Series:
    return x.groupby(grupos).transform(lambda s: s.shift(1).ewm(halflife=vida, min_periods=1).mean())


def priors_posicion(df: pd.DataFrame) -> pd.DataFrame:
    """Tasa media por minuto y porcentajes de cada grupo de posición en cada temporada, asignados a la
    temporada SIGUIENTE (sin fuga). La primera temporada usa su propia media (solo calienta el modelo)."""
    g = df.groupby(["season", "pos_grupo"])
    suma = g[CONTEOS + ["minutes"]].sum()
    out = pd.DataFrame(index=suma.index)
    for c in CONTEOS:
        out[f"prior_r_{c}"] = suma[c] / suma["minutes"]
    out["prior_p_fg2"] = (suma["fgm"] - suma["fg3m"]) / (suma["fga"] - suma["fg3a"])
    out["prior_p_fg3"] = suma["fg3m"] / suma["fg3a"]
    out["prior_p_ft"] = suma["ftm"] / suma["fta"]
    out = out.reset_index()
    siguiente = out.assign(season=out["season"] + 1)
    primera = out[out["season"] == out["season"].min()]
    return pd.concat([primera, siguiente]).drop_duplicates(["season", "pos_grupo"], keep="first")


def tasas_jugador(df: pd.DataFrame) -> pd.DataFrame:
    """Tasas por minuto y porcentajes encogidos hacia el prior de posición."""
    pid = df["player_id"]
    ewm_min = _ewm_prev(df["minutes"], pid, VIDA_MEDIA)
    n_prev = df.groupby("player_id").cumcount()
    # Minutos efectivos de la media exponencial: media x nº efectivo de partidos (≈ 1,44 x vida media).
    exposicion = ewm_min * np.minimum(n_prev, 1.44 * VIDA_MEDIA)
    df["n_hist"] = n_prev
    for c in CONTEOS:
        r = _ewm_prev(df[c].astype(float), pid, VIDA_MEDIA) / ewm_min.clip(lower=1)
        df[f"r_{c}"] = ((r * exposicion).fillna(0) + df[f"prior_r_{c}"] * K_MIN) / (exposicion.fillna(0) + K_MIN)
    # Porcentajes: intentos y aciertos acumulados con media exponencial (vida media más larga).
    pares = {"fg2": (df["fgm"] - df["fg3m"], df["fga"] - df["fg3a"]), "fg3": (df["fg3m"], df["fg3a"]),
             "ft": (df["ftm"], df["fta"])}
    for k, (hechos, intentos) in pares.items():
        h = _ewm_prev(hechos.astype(float), pid, 30)
        a = _ewm_prev(intentos.astype(float), pid, 30)
        n_eff = np.minimum(n_prev, 1.44 * 30)
        df[f"p_{k}"] = ((h * n_eff).fillna(0) + df[f"prior_p_{k}"] * K_INTENTOS[k]) / (
            (a * n_eff).fillna(0) + K_INTENTOS[k])
    df["r_pts_comp"] = (2 * (df["r_fga"] - df["r_fg3a"]) * df["p_fg2"] + 3 * df["r_fg3a"] * df["p_fg3"]
                        + df["r_fta"] * df["p_ft"])
    df["usg_ewm"] = _ewm_prev(df["usg_pct"].astype(float), pid, VIDA_MEDIA)
    df["ts_ewm"] = _ewm_prev(df["ts_pct"].astype(float), pid, VIDA_MEDIA)
    ps = df["player_id"] + "|" + df["season"].astype(str)
    df["r_pts_temp"] = (df.groupby(ps)["pts"].transform(lambda s: s.shift(1).cumsum())
                        / df.groupby(ps)["minutes"].transform(lambda s: s.shift(1).cumsum()).clip(lower=1))
    return df


def defensa_y_ritmo(con: duckdb.DuckDBPyConnection, df: pd.DataFrame) -> pd.DataFrame:
    """Por equipo y partido (antes de jugarlo): factor de puntos concedidos a cada posición, rating
    defensivo relativo y ritmo, con media exponencial de sus partidos anteriores."""
    # Partidos jugados más los futuros de `df` (sin ritmo real): con shift(1) reciben el último valor conocido.
    eq = con.execute("""SELECT game_id, team_id, opp_id, start_utc, season, pace, drtg FROM v_team_adv""").df()
    futuros = (df.loc[df["minutes"].isna(), ["game_id", "team_id", "opp_id", "start_utc", "season"]]
               .drop_duplicates(["game_id", "team_id"]))
    futuros = futuros[~futuros["game_id"].isin(eq["game_id"])]
    if not futuros.empty:
        rivales = futuros.rename(columns={"team_id": "opp_id", "opp_id": "team_id"})
        eq = pd.concat([eq, futuros, rivales], ignore_index=True).drop_duplicates(["game_id", "team_id"])
    eq = eq.sort_values(["team_id", "start_utc"]).reset_index(drop=True)
    eq["pace_ewm"] = _ewm_prev(eq["pace"], eq["team_id"], VIDA_MEDIA_EQUIPO)
    eq["drtg_ewm"] = _ewm_prev(eq["drtg"], eq["team_id"], VIDA_MEDIA_EQUIPO)
    liga = eq.groupby("season")[["pace", "drtg"]].mean().rename(columns=lambda c: f"liga_{c}")
    liga_prev = liga.shift(1).fillna(liga)   # media de la temporada anterior (la primera usa la suya)
    eq = eq.merge(liga_prev, left_on="season", right_index=True, how="left")

    # Puntos por minuto concedidos a cada grupo de posición (sumando a los rivales que jugaron contra él).
    conc = (df.groupby(["game_id", "opp_id", "pos_grupo"])[["pts", "minutes"]].sum(min_count=1).reset_index()
            .rename(columns={"opp_id": "def_team"}))
    conc = conc.merge(eq[["game_id", "team_id", "start_utc", "season"]].rename(columns={"team_id": "def_team"}),
                      on=["game_id", "def_team"])
    conc = conc.sort_values(["def_team", "pos_grupo", "start_utc"])
    clave = conc["def_team"] + "|" + conc["pos_grupo"]
    conc["pts_ewm"] = _ewm_prev(conc["pts"].astype(float), clave, VIDA_MEDIA_EQUIPO)
    conc["min_ewm"] = _ewm_prev(conc["minutes"], clave, VIDA_MEDIA_EQUIPO)
    liga_pos = conc.groupby(["season", "pos_grupo"]).apply(lambda d: d["pts"].sum() / d["minutes"].sum(),
                                                           include_groups=False).rename("liga_pos").reset_index()
    liga_pos["season"] += 1
    conc = conc.merge(liga_pos, on=["season", "pos_grupo"], how="left")
    conc["def_pos"] = (conc["pts_ewm"] / conc["min_ewm"]) / conc["liga_pos"]

    out = df.merge(conc[["game_id", "def_team", "pos_grupo", "def_pos"]].rename(columns={"def_team": "opp_id"}),
                   on=["game_id", "opp_id", "pos_grupo"], how="left")
    rival = eq[["game_id", "team_id", "pace_ewm", "drtg_ewm", "liga_pace", "liga_drtg"]].rename(
        columns={"team_id": "opp_id", "pace_ewm": "opp_pace", "drtg_ewm": "opp_drtg"})
    # `pace` (real) solo sirve para estimar la varianza del ritmo en entrenamiento; nunca es una feature.
    propio = eq[["game_id", "team_id", "pace_ewm", "pace"]].rename(columns={"pace_ewm": "own_pace"})
    out = out.merge(rival, on=["game_id", "opp_id"], how="left").merge(propio, on=["game_id", "team_id"], how="left")
    out["def_drtg"] = out["opp_drtg"] / out["liga_drtg"]
    out["ritmo_esp"] = (out["own_pace"] + out["opp_pace"]) / (2 * out["liga_pace"])
    return out


def construir(con: duckdb.DuckDBPyConnection, df: pd.DataFrame | None = None,
              minutos: pd.DataFrame | None = None) -> pd.DataFrame:
    """Dataset de producción. `minutos` (opcional) aporta min_base, libres y titular_ewm de la fase 2
    por (game_id, player_id); si no se da, se calculan aquí con las features de minutos."""
    df = cargar(con) if df is None else df
    df["pos_grupo"] = df["position"].map(grupo_posicion)
    df = df.merge(priors_posicion(df), on=["season", "pos_grupo"], how="left")
    df = df.sort_values(["player_id", "start_utc"]).reset_index(drop=True)
    df = tasas_jugador(df)
    df = defensa_y_ritmo(con, df)
    if minutos is None:
        from . import minutos as fm
        minutos = fm.dataset(con)
    cols = ["game_id", "player_id", "min_base", "libres", "libres_pos", "titular_ewm"]
    df = df.merge(minutos[cols], on=["game_id", "player_id"], how="left")
    # Tiros "liberados": intentos habituales de los compañeros que hoy no están (con su tasa por minuto).
    df["fga_base"] = df["r_fga"] * df["min_base"]
    tg = df.groupby(["game_id", "team_id"])["fga_base"].transform("sum")
    eqs = (df.assign(t=tg).groupby(["game_id", "team_id"]).agg(t=("t", "first"), s=("start_utc", "first"))
           .reset_index().sort_values(["team_id", "s"]))
    eqs["habitual"] = eqs.groupby("team_id")["t"].transform(lambda x: x.shift(1).ewm(halflife=5).mean())
    df = df.merge(eqs[["game_id", "team_id", "habitual"]], on=["game_id", "team_id"], how="left")
    df["fga_libres"] = (df["habitual"] - tg).fillna(0)
    # Margen final real (solo para estimar el efecto de las palizas en los minutos; nunca es una feature).
    margen = con.execute("""SELECT a.game_id, a.team_id, a.pts - b.pts AS margen_real FROM team_games a
                            JOIN team_games b ON b.game_id = a.game_id AND b.team_id <> a.team_id""").df()
    df = df.merge(margen, on=["game_id", "team_id"], how="left")
    df["playoffs"] = (df["season_type"] == 3).astype(float)
    df["is_home"] = df["is_home"].astype(float)
    df["b2b"] = df["b2b"].astype(float)
    for g in ("G", "F", "C"):
        df[f"pos_{g.lower()}"] = (df["pos_grupo"] == g).astype(float)
    return df.sort_values(["start_utc", "game_id", "team_id", "player_id"]).reset_index(drop=True)
