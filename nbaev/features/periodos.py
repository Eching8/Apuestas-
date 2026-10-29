"""Reparto de la producción por periodo (props de 1.er cuarto y 1.ª mitad).

Para cada jugador y partido, con partidos anteriores: qué fracción de sus puntos, rebotes y asistencias
produce en el 1.er cuarto y en la 1.ª mitad (media exponencial de las sumas, encogida hacia la fracción
media de su grupo -titular o suplente- en temporadas anteriores). La simulación reparte el valor del
partido simulado con una beta-binomial (1.er cuarto <= 1.ª mitad <= partido, siempre coherente).
"""
from __future__ import annotations

import duckdb
import numpy as np
import pandas as pd

PERIODOS = {"1q": (1,), "1h": (1, 2)}
STATS_PERIODO = {"pts": ["pts"], "reb": ["oreb", "dreb"], "ast": ["ast"]}
K = {"pts": 60.0, "reb": 25.0, "ast": 15.0}        # peso del prior (en unidades de la estadística)
VIDA = 20


def cargar_periodos(con: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    """Por jugador y partido: estadística total y en cada periodo."""
    return con.execute("""
        SELECT p.game_id, p.player_id,
               sum(CASE WHEN p.period = 1 THEN p.pts END) AS pts_1q, sum(CASE WHEN p.period <= 2 THEN p.pts END) AS pts_1h,
               sum(CASE WHEN p.period = 1 THEN p.oreb + p.dreb END) AS reb_1q,
               sum(CASE WHEN p.period <= 2 THEN p.oreb + p.dreb END) AS reb_1h,
               sum(CASE WHEN p.period = 1 THEN p.ast END) AS ast_1q, sum(CASE WHEN p.period <= 2 THEN p.ast END) AS ast_1h,
               sum(p.pts) AS pts_g, sum(p.oreb + p.dreb) AS reb_g, sum(p.ast) AS ast_g
        FROM player_periods p GROUP BY 1, 2""").df()


def fracciones(con: duckdb.DuckDBPyConnection, df: pd.DataFrame) -> pd.DataFrame:
    """Añade frac_{stat}_{periodo} a `df` (filas jugador-partido ordenables por start_utc)."""
    per = cargar_periodos(con)
    d = df.merge(per, on=["game_id", "player_id"], how="left").sort_values(["player_id", "start_utc"])
    d = d.reset_index(drop=True)
    grupo = np.where(d["titular_ewm"].fillna(0) >= 0.5, "titular", "suplente")
    n_prev = d.groupby("player_id").cumcount()
    n_eff = np.minimum(n_prev, 1.44 * VIDA)
    for st in STATS_PERIODO:
        tot = _ewm(d[f"{st}_g"], d["player_id"]) * n_eff
        for p in PERIODOS:
            parc = _ewm(d[f"{st}_{p}"], d["player_id"]) * n_eff
            # Prior: fracción media de su grupo en la temporada anterior (la primera usa la suya).
            prior = (d.assign(g=grupo).groupby(["season", "g"]).apply(
                lambda x: x[f"{st}_{p}"].sum() / max(x[f"{st}_g"].sum(), 1), include_groups=False)
                .rename("prior").reset_index())
            prior_sig = prior.assign(season=prior["season"] + 1)
            prior = pd.concat([prior[prior["season"] == prior["season"].min()], prior_sig]).drop_duplicates(
                ["season", "g"], keep="last")
            pr = d.assign(g=grupo)[["season", "g"]].merge(prior, on=["season", "g"], how="left")["prior"].to_numpy()
            d[f"frac_{st}_{p}"] = (parc.fillna(0) + K[st] * pr) / (tot.fillna(0) + K[st])
    return d


def _ewm(x: pd.Series, grupos: pd.Series) -> pd.Series:
    return x.astype(float).groupby(grupos).transform(lambda s: s.shift(1).ewm(halflife=VIDA, min_periods=1).mean())


def _conc(n, y, f) -> float:
    m = n >= 2
    n, y, f = n[m], y[m], np.clip(f[m], 0.02, 0.98)
    if len(n) < 100:
        return 50.0
    exceso = ((((y - n * f) ** 2) / (n * f * (1 - f))) - 1).mean() / (n - 1).mean()
    return float(np.clip(1 / max(exceso, 1e-3) - 1, 2, 500))


def estimar_concentraciones(d: pd.DataFrame) -> dict[str, tuple[float, float]]:
    """Por estadística: (concentración de la 1.ª mitad sobre el partido, del 1.er cuarto sobre la 1.ª mitad)."""
    out = {}
    for st in STATS_PERIODO:
        x = d.dropna(subset=[f"{st}_g", f"{st}_1h", f"{st}_1q", f"frac_{st}_1h", f"frac_{st}_1q"])
        c_h = _conc(x[f"{st}_g"].to_numpy(), x[f"{st}_1h"].to_numpy(), x[f"frac_{st}_1h"].to_numpy())
        f_qh = (x[f"frac_{st}_1q"] / x[f"frac_{st}_1h"].clip(lower=1e-3)).to_numpy()
        c_q = _conc(x[f"{st}_1h"].to_numpy(), x[f"{st}_1q"].to_numpy(), f_qh)
        out[st] = (c_h, c_q)
    return out


def simular_periodos(rng, total: np.ndarray, frac_1h: np.ndarray, frac_1q: np.ndarray, conc_1h: float,
                     conc_q_de_h: float) -> tuple[np.ndarray, np.ndarray]:
    """Reparte el total simulado: 1.ª mitad ~ BetaBin(total, frac_1h); 1.er cuarto ~ BetaBin(1.ª mitad, frac_1q/frac_1h)."""
    def bb(n, p, c):
        p = np.clip(np.broadcast_to(p, n.shape), 1e-3, 1 - 1e-3)
        return rng.binomial(n, rng.beta(p * c, (1 - p) * c))
    h1 = bb(total, frac_1h[:, None], conc_1h)
    q1 = bb(h1, np.clip(frac_1q / np.maximum(frac_1h, 1e-3), 0, 1)[:, None], conc_q_de_h)
    return q1, h1
