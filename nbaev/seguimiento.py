"""Seguimiento de las props de un día: cómo salieron y dónde se equivocó el modelo.

    python -m nbaev seguimiento exportar --fecha AAAA-MM-DD   # antes de los partidos: guarda lo evaluado
    python -m nbaev seguimiento evaluar --fecha AAAA-MM-DD    # después: resultados, calibración y errores

`exportar` deja en docs/seguimiento/ la última evaluación de cada línea antes del inicio de su partido
(predicciones), la proyección de minutos y la de puntos, para poder evaluarlas aunque la base local se
pierda. `evaluar` las cruza con los resultados reales (box score, cuartos, primera canasta) y con el cierre.
"""
from __future__ import annotations

import logging
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd

from .betting import margen as mg
from .betting.registro import EXPRESION
from .config import RAIZ

log = logging.getLogger(__name__)
CARPETA = RAIZ / "docs" / "seguimiento"


def exportar(con: duckdb.DuckDBPyConnection, fecha: str, carpeta: Path = CARPETA) -> dict:
    carpeta.mkdir(parents=True, exist_ok=True)
    pred = con.execute("""
        SELECT p.*, g.start_utc FROM predicciones p JOIN games g USING (game_id)
        WHERE p.fecha = ? AND p.snapshot_at < g.start_utc
        QUALIFY row_number() OVER (PARTITION BY p.game_id, p.player_id, p.market, p.period, p.line
                                   ORDER BY p.snapshot_at DESC) = 1""", [fecha]).df()
    minutos = con.execute("SELECT * FROM proj_minutos WHERE fecha = ?", [fecha]).df()
    puntos = con.execute("SELECT * FROM proj_puntos WHERE fecha = ?", [fecha]).df()
    pred.to_csv(carpeta / f"{fecha}_predicciones.csv", index=False)
    minutos.to_csv(carpeta / f"{fecha}_minutos.csv", index=False)
    puntos.to_csv(carpeta / f"{fecha}_puntos.csv", index=False)
    return {"predicciones": len(pred), "picks": int(pred["pick"].sum()), "minutos": len(minutos)}


# --- Resultados reales -------------------------------------------------------------------------------

def valores_reales(con: duckdb.DuckDBPyConnection, pred: pd.DataFrame) -> pd.Series:
    """Valor real de cada línea (NaN si el jugador no jugó o el partido no ha terminado)."""
    ids = list(pred["game_id"].astype(str).unique())
    box = con.execute("SELECT * FROM player_games WHERE game_id IN (SELECT unnest(?))", [ids]).df()
    box = box.set_index(["game_id", "player_id"])
    per = con.execute("""SELECT game_id, player_id,
                            sum(CASE WHEN period = 1 THEN pts END) AS pts_1q, sum(CASE WHEN period <= 2 THEN pts END) AS pts_1h,
                            sum(CASE WHEN period = 1 THEN oreb + dreb END) AS reb_1q,
                            sum(CASE WHEN period <= 2 THEN oreb + dreb END) AS reb_1h,
                            sum(CASE WHEN period = 1 THEN ast END) AS ast_1q, sum(CASE WHEN period <= 2 THEN ast END) AS ast_1h
                         FROM player_periods WHERE game_id IN (SELECT unnest(?)) GROUP BY 1, 2""", [ids]).df()
    per = per.set_index(["game_id", "player_id"])
    primera = dict(con.execute("SELECT game_id, first_fg_player FROM game_starts WHERE game_id IN (SELECT unnest(?))",
                               [ids]).fetchall())
    comp = {"pr": ["pts", "reb"], "pa": ["pts", "ast"], "ra": ["reb", "ast"], "pra": ["pts", "reb", "ast"],
            "pts": ["pts"], "reb": ["reb"], "ast": ["ast"]}
    out = []
    for r in pred.itertuples():
        k = (str(r.game_id), str(r.player_id))
        if r.market == "primera_canasta":
            out.append(float(primera.get(k[0]) == k[1]) if k[0] in primera and k in box.index else np.nan)
            continue
        if k not in box.index:
            out.append(np.nan)          # no jugó (o el partido no ha terminado): apuesta nula
            continue
        b = box.loc[k]
        if r.period != "game":
            if k not in per.index:
                out.append(np.nan)
                continue
            out.append(float(sum(per.loc[k, f"{c}_{r.period}"] for c in comp[r.market])))
        elif r.market in ("doble_doble", "triple_doble"):
            n10 = sum(b[c] >= 10 for c in ("pts", "reb", "ast", "stl", "blk"))
            out.append(float(n10 >= (2 if r.market == "doble_doble" else 3)))
        else:
            out.append(float(eval(EXPRESION[r.market], {}, b.to_dict())))   # expresión fija: "pts + reb"...
    return pd.Series(out, index=pred.index)


def cierres(con: duckdb.DuckDBPyConnection, pred: pd.DataFrame) -> pd.DataFrame:
    """Probabilidad justa de cierre (consenso) del lado elegido, con la misma línea."""
    ids = list(pred["game_id"].astype(str).unique())
    c = con.execute("""SELECT game_id, player_id, market, period, coalesce(line, -1) AS line,
                              max(CASE WHEN side IN ('over', 'yes') THEN odds END) AS co,
                              max(CASE WHEN side IN ('under', 'no') THEN odds END) AS cu
                       FROM prop_odds WHERE kind = 'cierre' AND book = 'consenso' AND game_id IN (SELECT unnest(?))
                       GROUP BY ALL HAVING co IS NOT NULL AND cu IS NOT NULL""", [ids]).df()
    if c.empty:
        return c
    c["margen_cierre"] = 1 / c["co"] + 1 / c["cu"] - 1
    c = c[c["margen_cierre"] >= 0.01]
    c["p_cierre_over"] = mg.justa_dos_lados(c["co"], c["cu"])
    return c[["game_id", "player_id", "market", "period", "line", "p_cierre_over"]]


def evaluar(con: duckdb.DuckDBPyConnection, fecha: str, carpeta: Path = CARPETA) -> dict:
    pred = pd.read_csv(carpeta / f"{fecha}_predicciones.csv", dtype={"game_id": str, "player_id": str})
    pred["valor_real"] = valores_reales(con, pred)
    sobre = pred["lado"].isin(["over", "sí"])
    sin_linea = pred["line"] < 0
    pred["y_over"] = np.where(sin_linea, pred["valor_real"],
                              np.where(pred["valor_real"] > pred["line"], 1.0,
                                       np.where(pred["valor_real"] < pred["line"], 0.0, np.nan)))
    pred.loc[pred["valor_real"].isna(), "y_over"] = np.nan
    pred["gana"] = np.where(sobre, pred["y_over"], 1 - pred["y_over"])
    # Probabilidades del lado over / sí (las predicciones guardan las del lado elegido).
    for c in ("p_modelo", "p_justa", "p_final"):
        pred[f"{c}_over"] = np.where(sobre, pred[c], 1 - pred[c])
    ci = cierres(con, pred)
    if not ci.empty:
        pred = pred.merge(ci, on=["game_id", "player_id", "market", "period", "line"], how="left")
        p_c = np.where(sobre, pred["p_cierre_over"], 1 - pred["p_cierre_over"])
        pred["clv"] = pred["cuota"] * p_c - 1
    else:
        pred["clv"] = np.nan
    ev = pred.dropna(subset=["y_over"])
    return {"pred": pred, "evaluadas": ev, "fecha": fecha, **_minutos(con, carpeta, fecha), **_puntos(con, ev)}


def _minutos(con, carpeta: Path, fecha: str) -> dict:
    ruta = carpeta / f"{fecha}_minutos.csv"
    if not ruta.exists():
        return {}
    m = pd.read_csv(ruta, dtype={"game_id": str, "player_id": str})
    box = con.execute("SELECT game_id, player_id, minutes FROM player_games WHERE game_id IN (SELECT unnest(?))",
                      [list(m["game_id"].unique())]).df()
    jugados = con.execute("SELECT DISTINCT game_id FROM player_games WHERE game_id IN (SELECT unnest(?))",
                          [list(m["game_id"].unique())]).df()["game_id"]
    m = m[m["game_id"].isin(jugados)].merge(box, on=["game_id", "player_id"], how="left")
    m["minutes"] = m["minutes"].fillna(0.0)
    jug = m[m["minutes"] > 0]
    return {"minutos": m, "min_mae": float((jug["min_si_juega"] - jug["minutes"]).abs().mean()) if len(jug) else np.nan,
            "min_sesgo": float((jug["min_si_juega"] - jug["minutes"]).mean()) if len(jug) else np.nan}


def _puntos(con, ev: pd.DataFrame) -> dict:
    p = ev[(ev["market"] == "pts") & (ev["period"] == "game")]
    if p.empty:
        return {}
    return {"pts_mae_modelo": float((p["proyeccion"] - p["valor_real"]).abs().mean()),
            "pts_mae_linea": float((p["line"] - p["valor_real"]).abs().mean()),
            "pts_sesgo_modelo": float((p["proyeccion"] - p["valor_real"]).mean()),
            "pts_sesgo_linea": float((p["line"] - p["valor_real"]).mean())}


# --- Informe -------------------------------------------------------------------------------------------

def _brier(p, y):
    return float(((p - y) ** 2).mean())


def informe(r: dict) -> str:
    f = lambda t: t.to_markdown(index=False, floatfmt=".3f")  # noqa: E731
    ev, pred = r["evaluadas"], r["pred"]
    picks = ev[ev["pick"]]
    partes = [f"# Seguimiento de las props del {r['fecha']}",
              f"Líneas evaluadas antes de los partidos: {len(pred)}; con resultado: {len(ev)} "
              f"(el resto, jugador que no jugó o empate con la línea: nulas)."]
    if not picks.empty:
        gan = picks["gana"].sum()
        roi = (np.where(picks["gana"] == 1, picks["cuota"] - 1, -1.0)).mean()
        partes += ["## Picks (monto 0: ningún mercado validado; ROI simulado con 1 unidad por pick)",
                   f"{int(gan)} ganadas de {len(picks)} ({gan / len(picks):.0%}); ROI {roi:+.1%}; EV medio esperado "
                   f"{picks['ev'].mean():+.1%}; probabilidad media usada {picks['p_final'].mean():.1%}; CLV medio "
                   f"{picks['clv'].mean():+.1%} ({picks['clv'].notna().sum()} con cierre).",
                   f(picks[["jugador", "market", "period", "line", "lado", "cuota", "proyeccion", "valor_real", "p_final",
                            "p_justa", "ev", "gana", "clv"]].sort_values("ev", ascending=False))]
    # Calibración por mercado (lado over / sí).
    filas = []
    for (mk, per), d in ev.groupby(["market", "period"]):
        filas.append({"mercado": mk, "periodo": per, "líneas": len(d), "over real": d["y_over"].mean(),
                      "P(over) mercado": d["p_justa_over"].mean(), "P(over) final": d["p_final_over"].mean(),
                      "P(over) modelo": d["p_modelo_over"].mean(), "Brier mercado": _brier(d["p_justa_over"], d["y_over"]),
                      "Brier final": _brier(d["p_final_over"], d["y_over"]),
                      "Brier modelo": _brier(d["p_modelo_over"], d["y_over"])})
    t = pd.DataFrame(filas)
    tot = {"mercado": "TODOS", "periodo": "", "líneas": len(ev), "over real": ev["y_over"].mean(),
           "P(over) mercado": ev["p_justa_over"].mean(), "P(over) final": ev["p_final_over"].mean(),
           "P(over) modelo": ev["p_modelo_over"].mean(), "Brier mercado": _brier(ev["p_justa_over"], ev["y_over"]),
           "Brier final": _brier(ev["p_final_over"], ev["y_over"]), "Brier modelo": _brier(ev["p_modelo_over"], ev["y_over"])}
    partes += ["## Calibración por mercado (lado over / sí; Brier: menor es mejor)",
               "Si 'over real' queda por encima de 'P(over) modelo', el modelo fue demasiado pesimista (sesgo al under).",
               f(pd.concat([t, pd.DataFrame([tot])], ignore_index=True))]
    if "min_mae" in r:
        m = r["minutos"]
        jug = m[m["minutes"] > 0].assign(error=lambda d: d["min_si_juega"] - d["minutes"])
        partes += ["## Minutos",
                   f"Error medio {r['min_mae']:.2f} min, sesgo {r['min_sesgo']:+.2f} (positivo = se proyectaron de más). "
                   "Mayores errores:",
                   f(jug.reindex(jug["error"].abs().sort_values(ascending=False).index)
                     [["name", "estado_lesion", "min_si_juega", "minutes", "error"]].head(12))]
        no_jugaron = m[(m["minutes"] == 0) & (m["min_si_juega"] >= 15)]
        if not no_jugaron.empty:
            partes += ["Proyectados con 15+ minutos que no jugaron:",
                       f(no_jugaron[["name", "estado_lesion", "prob_juega", "p_dnp", "min_si_juega"]])]
    if "pts_mae_modelo" in r:
        partes += ["## Puntos: proyección del modelo frente a la línea de la casa",
                   f"Error medio: modelo {r['pts_mae_modelo']:.2f}, línea {r['pts_mae_linea']:.2f}. Sesgo (proyección - "
                   f"real): modelo {r['pts_sesgo_modelo']:+.2f}, línea {r['pts_sesgo_linea']:+.2f}."]
    peores = ev.assign(err=(ev["proyeccion"] - ev["valor_real"]).abs())
    peores = peores[peores["period"] == "game"].sort_values("err", ascending=False).drop_duplicates("player_id")
    partes += ["## Mayores fallos de proyección (partido completo)",
               f(peores[["jugador", "market", "line", "proyeccion", "valor_real", "p_modelo_over", "p_justa_over"]].head(12))]
    return "\n\n".join(partes)


def guardar(r: dict, carpeta: Path = CARPETA) -> Path:
    ruta = carpeta / f"{r['fecha']}_resultado.md"
    ruta.write_text(informe(r), encoding="utf-8")
    r["pred"].to_csv(carpeta / f"{r['fecha']}_resultado.csv", index=False)
    return ruta
