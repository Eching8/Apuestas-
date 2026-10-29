"""Fase 6: validación de todos los mercados de jugador con la misma simulación.

Walk-forward mensual (cada mes se entrena con los anteriores; minutos proyectados fuera de muestra):
- PIT aleatorizado de cada estadística y de los periodos (1.er cuarto y 1.ª mitad), con o sin cuotas.
- Probabilidades frente a las líneas reales de cada mercado (over/under y sí/no: doble-doble, triple-doble).
- Máximo anotador del partido (mercado comparativo): log loss frente al resultado real.
Las líneas resultantes alimentan el mismo backtest de apuestas de la fase 4, mercado por mercado.
"""
from __future__ import annotations

import logging

import duckdb
import numpy as np
import pandas as pd

from ..features import periodos as fper
from ..features import produccion as fp
from ..models import estadisticas as me
from ..models import simulacion as sim
from .walkforward import bloques_mensuales

log = logging.getLogger(__name__)

MERCADOS_OU = ["pts", "reb", "ast", "fg3m", "stl", "blk", "tov", "fgm", "ftm", "pr", "pa", "ra", "pra", "stocks"]
MERCADOS_SN = ["doble_doble", "triple_doble"]
REAL = {"pts": "pts", "reb": "reb", "ast": "ast", "fg3m": "fg3m", "stl": "stl", "blk": "blk", "tov": "tov",
        "fgm": "fgm", "ftm": "ftm", "pr": "pts + reb", "pa": "pts + ast", "ra": "reb + ast", "pra": "pts + reb + ast",
        "stocks": "stl + blk"}
PIT_STATS = ["pts", "reb", "ast", "fg3m", "stl", "blk", "tov", "pra"]


def lineas(con: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    """Líneas de consenso (apertura y cierre) de todos los mercados modelados, con ambos lados.
    Un cierre se acepta solo si hay apertura y no se aleja más de max(1, 15 % de la línea) (ver fase 3)."""
    df = con.execute("""
        SELECT game_id, player_id, market, kind, bet_type, line,
               max(CASE WHEN side IN ('over', 'yes') THEN odds END) AS cuota_over,
               max(CASE WHEN side IN ('under', 'no') THEN odds END) AS cuota_under
        FROM prop_odds
        WHERE period = 'game' AND book = 'consenso' AND kind IN ('apertura', 'cierre') AND player_id IS NOT NULL
          AND ((bet_type = 'ou' AND market IN (SELECT unnest(?))) OR (bet_type = 'yn' AND market IN (SELECT unnest(?))))
        GROUP BY ALL HAVING cuota_over IS NOT NULL AND cuota_under IS NOT NULL""", [MERCADOS_OU, MERCADOS_SN]).df()
    ap = (df[df["kind"] == "apertura"].groupby(["game_id", "player_id", "market"])["line"].median()
          .rename("linea_apertura"))
    df = df.merge(ap, on=["game_id", "player_id", "market"], how="left")
    hay_ap = df.set_index(["game_id", "player_id", "market"]).index.isin(ap.index)
    tol = np.maximum(1.0, 0.15 * df["linea_apertura"].fillna(0))
    ok_ou = (df["line"] - df["linea_apertura"]).abs() <= tol
    valido = (df["kind"] == "apertura") | (hay_ap & ((df["bet_type"] == "yn") | ok_ou))
    df = df[valido].copy()
    io, iu = 1 / df["cuota_over"], 1 / df["cuota_under"]
    df["p_mercado"] = io / (io + iu)
    df["margen"] = io + iu - 1
    return df[(df["margen"] >= 0.01) & (df["margen"] < 0.35)]


def _pit(s: np.ndarray, y: np.ndarray, rng) -> np.ndarray:
    y = y[:, None]
    return (s < y).mean(1) + rng.uniform(size=len(y)) * (s == y).mean(1)


def validar(con: duckdb.DuckDBPyConnection, minutos_oos: pd.DataFrame, desde: str = "2025-10-01",
            n_sims: int = 2000, semilla: int = 17) -> dict:
    df = fp.construir(con)
    df = df.merge(minutos_oos[["game_id", "player_id", "min_si_juega", "min_q10", "min_q90"]],
                  on=["game_id", "player_id"], how="left")
    df = fper.fracciones(con, df)
    df["reb"] = df["oreb"] + df["dreb"]
    lin = lineas(con)
    reales = con.execute(f"""SELECT game_id, player_id, {', '.join(f'{v} AS real_{k}' for k, v in REAL.items())}
                             FROM player_games""").df()
    rng = np.random.default_rng(semilla)
    pits, lineas_oos, maximos = [], [], []
    for ini, fin in bloques_mensuales(df["start_utc"], desde):
        train = df[df["start_utc"] < ini]
        test = df[(df["start_utc"] >= ini) & (df["start_utc"] < fin) & df["min_si_juega"].notna()].copy()
        if test.empty:
            continue
        test = test.reset_index(drop=True)
        m = me.entrenar(train)
        disp = me.disp_completa(m)
        conc = fper.estimar_concentraciones(train[train["season"] >= train["season"].max() - 1])
        res = {}
        for nombre, usar in (("lgb", True), ("base", False)):
            res[nombre] = sim.simular(me.entrada(m, test, usar_lgb=usar), disp, n_sims=n_sims, semilla=semilla)
        s = res["lgb"]
        s["reb"] = me.valor_mercado(s, "reb")
        # Periodos (sobre las simulaciones del modelo).
        for st in fper.STATS_PERIODO:
            q1, h1 = fper.simular_periodos(rng, s[st], test[f"frac_{st}_1h"].to_numpy(), test[f"frac_{st}_1q"].to_numpy(),
                                           *conc[st])
            s[f"{st}_1q"], s[f"{st}_1h"] = q1, h1
        # PIT de cada estadística y periodo.
        p = {"bloque": ini.strftime("%Y-%m")}
        for st in PIT_STATS:
            y = (test["pts"] + test["reb"] + test["ast"]) if st == "pra" else test[st]
            p[st] = _pit(me.valor_mercado(s, st), y.to_numpy(), rng)
        for st in fper.STATS_PERIODO:
            for per in fper.PERIODOS:
                y = test[f"{st}_{per}"].to_numpy()
                ok = ~np.isnan(y)
                p[f"{st}_{per}"] = np.where(ok, _pit(s[f"{st}_{per}"], np.nan_to_num(y), rng), np.nan)
        pits.append(pd.DataFrame(p).assign(game_id=test["game_id"].to_numpy(), player_id=test["player_id"].to_numpy()))

        # Máximo anotador del partido.
        maximos.append(maximo_anotador(test, s["pts"]).assign(bloque=ini.strftime("%Y-%m")))

        # Líneas reales.
        lt = lin.merge(test[["game_id", "player_id"]].reset_index(), on=["game_id", "player_id"])
        if not lt.empty:
            lt = lt.merge(reales, on=["game_id", "player_id"], how="left")
            for nombre in ("lgb", "base"):
                r = res[nombre]
                col = np.full(len(lt), np.nan)
                sd = np.full(len(lt), np.nan)
                for mk, g in lt.groupby("market"):
                    v = me.valor_mercado(r, mk)[g["index"].to_numpy()]
                    if mk in MERCADOS_SN:
                        col[g.index] = v.mean(1)
                    else:
                        l = g["line"].to_numpy()[:, None]
                        po, pe = (v > l).mean(1), (v == l).mean(1)
                        col[g.index] = po / np.clip(1 - pe, 1e-9, None)
                        sd[g.index] = v.std(1)
                lt[f"p_{nombre}"] = np.clip(col, 0.001, 0.999)
                if nombre == "lgb":
                    lt["sd_sim"] = sd
            # Resultado real.
            y = np.full(len(lt), np.nan)
            for mk, g in lt.groupby("market"):
                if mk in MERCADOS_SN:
                    dd = test.loc[g["index"], ["pts", "reb", "ast", "stl", "blk"]].ge(10).sum(1).to_numpy()
                    y[g.index] = (dd >= (2 if mk == "doble_doble" else 3)).astype(float)
                else:
                    real = g[f"real_{mk}"].to_numpy()
                    y[g.index] = np.where(real == g["line"].to_numpy(), np.nan, (real > g["line"].to_numpy()).astype(float))
            lt["y"] = y
            lt["bloque"] = ini.strftime("%Y-%m")
            lineas_oos.append(lt.dropna(subset=["y"]))
        log.info("Bloque %s: %d jugadores, %d líneas", ini.strftime("%Y-%m"), len(test), len(lt))
    return {"pit": pd.concat(pits, ignore_index=True), "lineas": pd.concat(lineas_oos, ignore_index=True),
            "maximo": pd.concat(maximos, ignore_index=True)}


def maximo_anotador(test: pd.DataFrame, pts: np.ndarray) -> pd.DataFrame:
    """P(ser el máximo anotador del partido) de cada jugador (empates repartidos) y si lo fue."""
    filas = []
    for gid, g in test.groupby("game_id"):
        s = pts[g.index.to_numpy()]
        mx = s.max(0)
        es = (s == mx)
        p = (es / es.sum(0)).mean(1)
        real = g["pts"].to_numpy()
        fue = (real == real.max()) / (real == real.max()).sum()
        filas.append(pd.DataFrame({"game_id": gid, "player_id": g["player_id"].to_numpy(), "p": p, "y": fue}))
    return pd.concat(filas, ignore_index=True)


# --- Informe ------------------------------------------------------------------------------------------

def tabla_pit(pit: pd.DataFrame) -> pd.DataFrame:
    """Por estadística: fracción en los deciles extremos (ideal 0,10) y desviación máxima de un decil."""
    filas = []
    for c in [c for c in pit.columns if c not in ("bloque", "game_id", "player_id")]:
        v = pit[c].dropna()
        h = np.histogram(v, bins=np.linspace(0, 1, 11))[0] / len(v)
        filas.append({"estadística": c, "n": len(v), "decil 1": h[0], "decil 5": h[4], "decil 10": h[-1],
                      "máx. desviación": float(np.abs(h - 0.1).max())})
    return pd.DataFrame(filas)


def tabla_maximo(mx: pd.DataFrame) -> pd.DataFrame:
    p = mx["p"].clip(1e-4, 1 - 1e-4)
    ll = -(mx["y"] * np.log(p) + (1 - mx["y"]) * np.log(1 - p)).mean()
    n_por = mx.groupby("game_id")["p"].transform("size")
    u = (1 / n_por).clip(1e-4, 1 - 1e-4)
    ll_u = -(mx["y"] * np.log(u) + (1 - mx["y"]) * np.log(1 - u)).mean()
    tr = pd.cut(mx["p"], [0, 0.05, 0.1, 0.2, 0.3, 0.45, 1.0])
    cal = mx.assign(tramo=tr).groupby("tramo", observed=True).agg(n=("y", "size"), p_media=("p", "mean"),
                                                                   frecuencia_real=("y", "mean")).reset_index()
    cal["tramo"] = cal["tramo"].astype(str)
    return pd.DataFrame([{"partidos": mx["game_id"].nunique(), "log loss modelo": ll, "log loss uniforme": ll_u}]), cal


def tabla_probabilidades(lin: pd.DataFrame) -> pd.DataFrame:
    def ll(p, y):
        p = np.clip(p, 1e-4, 1 - 1e-4)
        return float(-(y * np.log(p) + (1 - y) * np.log(1 - p)).mean())
    filas = []
    for (mk, kind), d in lin.groupby(["market", "kind"]):
        filas.append({"mercado": mk, "líneas": kind, "n": len(d), "margen medio": d["margen"].mean(),
                      "log loss mercado": ll(d["p_mercado"], d["y"]), "log loss LightGBM": ll(d["p_lgb"], d["y"]),
                      "log loss baseline": ll(d["p_base"], d["y"])})
    return pd.DataFrame(filas)
