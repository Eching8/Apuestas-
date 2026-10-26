"""Validación de la proyección de minutos: walk-forward mensual, métricas por segmento y bootstrap."""
from __future__ import annotations

import logging
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd

from ..features import minutos as fm
from ..models import minutos as mm
from .walkforward import walk_forward

log = logging.getLogger(__name__)

PREDICTORES = {
    "base (media exp.)": "min_base",
    "base normalizada a 240": "min_norm",
    "LightGBM": "min_pred_bruta",
    "LightGBM + reparto": "min_pred",
}


def segmentos(d: pd.DataFrame) -> dict[str, pd.Series]:
    return {
        "todos": pd.Series(True, index=d.index),
        "con prop de puntos": d["con_prop"],
        "rotación (base >= 15 min)": d["min_base"] >= 15,
        "compañeros fuera (>= 15 min libres)": d["libres"] >= 15,
        "back-to-back": d["b2b"] == 1,
        "posible paliza (|spread| >= 12)": d["spread_abs"] >= 12,
        "vuelve tras >= 10 días": d["dias_desde"] >= 10,
        "inicio de temporada (< 5 partidos)": d["n_temp"] < 5,
        "cambio de equipo reciente (< 5 partidos)": d["n_equipo"] < 5,
        "playoffs": d["playoffs"] == 1,
    }


def tabla_errores(d: pd.DataFrame) -> pd.DataFrame:
    filas = []
    for seg, mask in segmentos(d).items():
        s = d[mask]
        if len(s) < 50:
            continue
        fila = {"segmento": seg, "n": len(s)}
        for nombre, col in PREDICTORES.items():
            fila[f"MAE {nombre}"] = (s[col] - s["minutes"]).abs().mean()
        fila["sesgo LGB+reparto"] = (s["min_pred"] - s["minutes"]).mean()
        filas.append(fila)
    return pd.DataFrame(filas)


def tabla_temporadas(d: pd.DataFrame) -> pd.DataFrame:
    return (d.assign(e_base=(d["min_base"] - d["minutes"]).abs(), e_norm=(d["min_norm"] - d["minutes"]).abs(),
                     e_lgb=(d["min_pred"] - d["minutes"]).abs(), e2=(d["min_pred"] - d["minutes"]) ** 2)
            .groupby("season").agg(n=("minutes", "size"), mae_base=("e_base", "mean"), mae_norm=("e_norm", "mean"),
                                    mae_lgb=("e_lgb", "mean"), rmse_lgb=("e2", lambda x: np.sqrt(x.mean())))
            .reset_index())


def tabla_cuantiles(d: pd.DataFrame) -> pd.DataFrame:
    """Cobertura real de los cuantiles si juega (debería parecerse a la nominal) y error de la media si juega."""
    filas = []
    j = d[d["minutes"] > 0]
    for seg, s in (("jugaron", j), ("jugaron, con prop de puntos", j[j["con_prop"]])):
        y = s["minutes"]
        filas.append({"segmento": seg, "n": len(s), "MAE media si juega": (s["min_si_juega"] - y).abs().mean(),
                      "P(y <= q10)": (y <= s["min_q10"]).mean(),
                      "P(y <= q50)": (y <= s["min_q50"]).mean(), "P(y <= q90)": (y <= s["min_q90"]).mean(),
                      "ancho medio q10-q90": (s["min_q90"] - s["min_q10"]).mean()})
    return pd.DataFrame(filas)


def tabla_dnp(d: pd.DataFrame) -> pd.DataFrame:
    """Calibración de P(no juega | vestido)."""
    y = (d["minutes"] == 0).astype(float)
    base = d["dnp_ewm"].fillna(y.mean()).clip(0.001, 0.999)
    p = d["p_dnp"].clip(0.001, 0.999)
    resumen = pd.DataFrame([
        {"modelo": "tasa reciente del jugador", "brier": ((base - y) ** 2).mean(),
         "log loss": -(y * np.log(base) + (1 - y) * np.log(1 - base)).mean()},
        {"modelo": "LightGBM", "brier": ((p - y) ** 2).mean(),
         "log loss": -(y * np.log(p) + (1 - y) * np.log(1 - p)).mean()}])
    tramos = pd.cut(p, [0, 0.02, 0.05, 0.1, 0.2, 0.4, 0.6, 1.0])
    calib = (pd.DataFrame({"tramo": tramos, "p": p, "y": y}).groupby("tramo", observed=True)
             .agg(n=("y", "size"), p_media=("p", "mean"), frecuencia_real=("y", "mean")).reset_index())
    calib["tramo"] = calib["tramo"].astype(str)
    return resumen, calib


def bootstrap_diferencia(d: pd.DataFrame, col_a: str, col_b: str, n: int = 1000, semilla: int = 7) -> dict:
    """IC 95 % de MAE(a) - MAE(b) remuestreando PARTIDOS (las filas de un partido no son independientes)."""
    e = (d[col_a] - d["minutes"]).abs() - (d[col_b] - d["minutes"]).abs()
    por_partido = e.groupby(d["game_id"]).agg(["sum", "size"])
    s, c = por_partido["sum"].to_numpy(), por_partido["size"].to_numpy()
    rng = np.random.default_rng(semilla)
    idx = rng.integers(0, len(s), size=(n, len(s)))
    difs = s[idx].sum(axis=1) / c[idx].sum(axis=1)
    return {"diferencia": s.sum() / c.sum(), "ic95": (np.quantile(difs, 0.025), np.quantile(difs, 0.975)),
            "p_valor_aprox": float((difs >= 0).mean())}


def validar(con: duckdb.DuckDBPyConnection, desde: str = "2023-10-01", hasta: str | None = None) -> dict:
    df = fm.dataset(con)
    con_prop = con.execute("""SELECT DISTINCT game_id, player_id FROM prop_odds
                              WHERE market = 'pts' AND period = 'game' AND player_id IS NOT NULL""").df()
    df = df.merge(con_prop.assign(con_prop=True), on=["game_id", "player_id"], how="left")
    df["con_prop"] = df["con_prop"].fillna(False).astype(bool)
    res = walk_forward(df, mm.entrenar, mm.predecir, desde, hasta, log=log)
    resumen_dnp, calib_dnp = tabla_dnp(res)
    return {
        "predicciones": res,
        "errores": tabla_errores(res),
        "temporadas": tabla_temporadas(res),
        "cuantiles": tabla_cuantiles(res),
        "dnp": resumen_dnp, "dnp_calibracion": calib_dnp,
        "bootstrap_vs_norm": bootstrap_diferencia(res, "min_pred", "min_norm"),
        "bootstrap_vs_norm_props": bootstrap_diferencia(res[res["con_prop"]], "min_pred", "min_norm"),
        "importancia": mm.importancia(mm.entrenar(df)),
    }


def informe(r: dict) -> str:
    f = lambda t: t.to_markdown(index=False, floatfmt=".3f")  # noqa: E731
    b, bp = r["bootstrap_vs_norm"], r["bootstrap_vs_norm_props"]
    return "\n\n".join([
        "# Fase 2: proyección de minutos (validación walk-forward mensual)",
        f"Filas evaluadas fuera de muestra: {len(r['predicciones']):,} (bloques {r['predicciones']['bloque'].min()} "
        f"a {r['predicciones']['bloque'].max()}). Cada mes se predice con un modelo entrenado solo con meses anteriores.",
        "## Error absoluto medio (minutos) por segmento", f(r["errores"]),
        "## Por temporada", f(r["temporadas"]),
        "## Bootstrap (remuestreo por partido): MAE(LightGBM + reparto) - MAE(base normalizada)",
        f"- Todos: {b['diferencia']:+.3f} min, IC 95 % [{b['ic95'][0]:+.3f}, {b['ic95'][1]:+.3f}]\n"
        f"- Jugadores con prop: {bp['diferencia']:+.3f} min, IC 95 % [{bp['ic95'][0]:+.3f}, {bp['ic95'][1]:+.3f}]",
        "## Distribución si juega: cobertura real de los cuantiles (nominal 10 / 50 / 90 %)", f(r["cuantiles"]),
        "## Probabilidad de no jugar estando disponible (DNP técnico)", f(r["dnp"]), f(r["dnp_calibracion"]),
        "## Importancia de las variables (ganancia, modelo final)", f(r["importancia"].head(15)),
    ])


def guardar_informe(r: dict, ruta: Path) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(informe(r), encoding="utf-8")
