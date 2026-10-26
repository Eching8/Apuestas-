"""Proyección diaria completa: una sola simulación por partido para todos los mercados.

Devuelve las filas de los jugadores probables y un diccionario de simulaciones (jugadores x simulaciones)
con todas las estadísticas, sus periodos (1.er cuarto y 1.ª mitad) y, aparte, las probabilidades de primer
anotador. Los mercados combinados, doble-doble, triple-doble, duelos y máximo anotador se calculan sobre
estas mismas simulaciones (ver estadisticas.valor_mercado y comparativos).
"""
from __future__ import annotations

import logging
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from ..config import RAIZ
from ..features import periodos as fper
from . import estadisticas as me
from . import primer_anotador as pa
from .simulacion import simular

log = logging.getLogger(__name__)


def modelo_produccion(con, cfg: dict, forzar: bool = False) -> tuple[me.ModeloProduccion, dict]:
    """Modelo de todas las estadísticas y concentraciones de periodo (reentrenado cada `reentrenar_cada_dias`)."""
    from ..features import produccion as fp
    ruta = RAIZ / cfg.get("produccion", {}).get("modelo", "data/modelos/produccion.joblib")
    dias = cfg.get("puntos", {}).get("reentrenar_cada_dias", 7)
    if ruta.exists() and not forzar:
        if (pd.Timestamp.now() - pd.Timestamp(ruta.stat().st_mtime, unit="s")).days < dias:
            return joblib.load(ruta)
    log.info("Entrenando los modelos de producción (todas las estadísticas)")
    df = fp.construir(con)
    m = me.entrenar(df)
    df = fper.fracciones(con, df)
    conc = fper.estimar_concentraciones(df[df["season"] >= df["season"].max() - 1])
    ruta.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump((m, conc), ruta)
    return m, conc


def proyectar(con, cfg: dict, fecha: str, n_sims: int = 10_000, semilla: int = 2026) -> dict:
    from . import puntos as mp
    filas = mp.filas_dia(con, cfg, fecha)                   # features (y minutos) de los jugadores de hoy
    if filas.empty:
        return {}
    m, conc = modelo_produccion(con, cfg)
    # Fracciones por periodo de los partidos de hoy (con todo el historial anterior).
    from ..features import produccion as fp
    hist = fp.construir(con)
    hist = pd.concat([hist, filas[[c for c in filas.columns if c in hist.columns]]], ignore_index=True)
    fr = fper.fracciones(con, hist)
    fr = fr[fr["game_id"].isin(filas["game_id"]) & fr["minutes"].isna()]
    cols_fr = [c for c in fr.columns if c.startswith("frac_")]
    filas = filas.merge(fr[["game_id", "player_id"] + cols_fr], on=["game_id", "player_id"], how="left")
    sims = simular(me.entrada(m, filas), me.disp_completa(m), n_sims=n_sims, semilla=semilla)
    sims["reb"] = me.valor_mercado(sims, "reb")
    rng = np.random.default_rng(semilla + 1)
    for st in fper.STATS_PERIODO:
        f1h = filas[f"frac_{st}_1h"].fillna(0.5).to_numpy()
        f1q = filas[f"frac_{st}_1q"].fillna(0.25).to_numpy()
        sims[f"{st}_1q"], sims[f"{st}_1h"] = fper.simular_periodos(rng, sims[st], f1h, f1q, *conc[st])
    mp.guardar_resumen(con, filas, sims["pts"], fecha)
    # Primer anotador con los titulares probables (los 5 con más titularidades recientes).
    primer = primer_anotador_dia(con, filas)
    return {"filas": filas, "sims": sims, "primer": primer, "modelo": m}


def primer_anotador_dia(con, filas: pd.DataFrame) -> pd.DataFrame:
    est = pa.Estado()
    for r in pa.cargar(con).itertuples():
        est.actualizar(r)
    peso = pa.peso_tiro_hasta(con, filas["start_utc"].min())
    salida = []
    for gid, g in filas.groupby("game_id"):
        equipos = con.execute("SELECT home_id, away_id FROM games WHERE game_id = ?", [gid]).fetchone()
        tits = {}
        for t in equipos:
            gg = g[g["team_id"] == t].sort_values(["titular_ewm", "min_si_juega"], ascending=False)
            tits[t] = list(gg["player_id"].head(5))
        if any(len(v) < 5 for v in tits.values()):
            continue
        p = pa.predecir_partido(est, equipos[0], equipos[1], tits[equipos[0]], tits[equipos[1]], peso)
        salida.append(p.assign(game_id=gid))
    return pd.concat(salida, ignore_index=True) if salida else pd.DataFrame()


def valor(sims: dict, mercado: str, periodo: str = "game") -> np.ndarray:
    """Valor del mercado en cada simulación, para el partido completo o un periodo."""
    if periodo == "game":
        return me.valor_mercado(sims, mercado)
    componentes = {"pts": ["pts"], "reb": ["reb"], "ast": ["ast"], "pr": ["pts", "reb"], "pa": ["pts", "ast"],
                   "ra": ["reb", "ast"], "pra": ["pts", "reb", "ast"]}[mercado]
    return sum(sims[f"{c}_{periodo}"] for c in componentes)


MERCADOS_PERIODO = {"pts", "reb", "ast", "pr", "pa", "ra", "pra"}


def guardar_sims(salida: dict, fecha: str) -> Path:
    """Guarda las simulaciones del día (para combinadas y duelos sin volver a simular)."""
    ruta = RAIZ / "data" / "cache" / f"sims_{fecha}.npz"
    ruta.parent.mkdir(parents=True, exist_ok=True)
    claves = {k: v.astype(np.int16) if v.dtype.kind in "iu" else v.astype(np.float32) for k, v in salida["sims"].items()}
    np.savez_compressed(ruta, **claves)
    salida["filas"][["game_id", "player_id", "name", "team_id"]].to_parquet(ruta.with_suffix(".filas.parquet"))
    return ruta


def cargar_sims(fecha: str) -> tuple[pd.DataFrame, dict]:
    ruta = RAIZ / "data" / "cache" / f"sims_{fecha}.npz"
    z = np.load(ruta)
    return pd.read_parquet(ruta.with_suffix(".filas.parquet")), {k: z[k] for k in z.files}
