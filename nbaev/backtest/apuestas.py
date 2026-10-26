"""Backtest de apuestas con cuotas reales: selección, liquidación, ROI, drawdown, CLV y bootstrap.

Genérico para cualquier mercado de dos lados (over/under, sí/no). Entrada: una fila por línea y tipo
(apertura/cierre) con cuotas de ambos lados, probabilidad justa del mercado, probabilidades del modelo
(fuera de muestra) y el resultado.

Reglas (fijadas antes de mirar resultados):
- Se apuesta a la cuota de APERTURA (la última disponible antes del partido sería más realista para quien
  apuesta tarde; la apertura es lo que permite medir CLV).
- Probabilidad de decisión: mezcla modelo + mercado ajustada walk-forward (solo meses anteriores).
- Se apuesta el lado con mayor EV si edge >= umbral y EV > 0; máximo 1 apuesta por jugador y partido y
  `max_por_partido` por partido (las de mayor EV).
- CLV: con la misma línea al cierre, CLV = cuota apostada x probabilidad justa del cierre - 1. Si la línea
  se movió, cuenta si se movió a favor ("batir el cierre").
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from ..betting import banca

# Muestra mínima y condición para validar un mercado (sección 1 de los requisitos).
MIN_APUESTAS = 300


@dataclass
class Estrategia:
    nombre: str
    col_p: str                 # columna de probabilidad (lado over / sí)
    edge_min: float = 0.04
    max_por_partido: int = 3
    lado_fijo: str | None = None   # controles: apostar siempre a 'over' o 'under'


def _logit(p):
    p = np.clip(p, 1e-3, 1 - 1e-3)
    return np.log(p / (1 - p))


def mezclar_oos(d: pd.DataFrame, col: str, min_train: int = 1500) -> pd.Series:
    """Probabilidad mezcla de mercado y modelo: regresión logística sobre logit(p_mercado) y logit(modelo),
    reentrenada en cada bloque con los bloques anteriores. NaN donde aún no hay datos suficientes."""
    from sklearn.linear_model import LogisticRegression
    out = pd.Series(np.nan, index=d.index)
    for b in sorted(d["bloque"].unique()):
        tr, te = d[d["bloque"] < b], d["bloque"] == b
        if len(tr) < min_train:
            continue
        m = LogisticRegression(C=1e3).fit(np.column_stack([_logit(tr["p_mercado"]), _logit(tr[col])]), tr["y"])
        out[te] = m.predict_proba(np.column_stack([_logit(d.loc[te, "p_mercado"]), _logit(d.loc[te, col])]))[:, 1]
    return out


def preparar(lin: pd.DataFrame, cols_modelo: list[str], kind: str = "apertura") -> pd.DataFrame:
    """Líneas de `kind` (a esa cuota se apuesta) con su cierre (si lo hay) y la mezcla de cada modelo.
    Con kind = 'cierre' se apuesta a la cuota de cierre (el CLV es 0 por definición)."""
    ap = lin[lin["kind"] == kind].copy()
    ci = (lin[lin["kind"] == "cierre"][["game_id", "player_id", "line", "cuota_over", "cuota_under", "p_mercado"]]
          .rename(columns={"line": "linea_cierre", "cuota_over": "co_cierre", "cuota_under": "cu_cierre",
                           "p_mercado": "p_mercado_cierre"}))
    ap = ap.merge(ci.drop_duplicates(["game_id", "player_id"]), on=["game_id", "player_id"], how="left")
    for c in cols_modelo:
        ap[f"{c}_mezcla"] = mezclar_oos(ap, c)
    return ap


def seleccionar(d: pd.DataFrame, e: Estrategia) -> pd.DataFrame:
    p_over = d[e.col_p] if e.col_p in d else pd.Series(np.nan, index=d.index)
    lados = []
    for lado, p, cuota, justa in (("over", p_over, d["cuota_over"], d["p_mercado"]),
                                  ("under", 1 - p_over, d["cuota_under"], 1 - d["p_mercado"])):
        lados.append(d.assign(lado=lado, p=p, cuota=cuota, p_justa=justa, ev=p * cuota - 1, edge=p - justa))
    x = pd.concat(lados, ignore_index=True)
    if e.lado_fijo:
        x = x[x["lado"] == e.lado_fijo].copy()
        x["p"] = x["p_justa"]
    else:
        x = x[x["p"].notna() & (x["edge"] >= e.edge_min) & (x["ev"] > 0)]
    x = x.sort_values("ev", ascending=False)
    x = x.drop_duplicates(["game_id", "player_id"])                       # 1 por jugador y partido
    x = x.groupby("game_id", group_keys=False).head(e.max_por_partido)     # tope por partido
    return liquidar(x)


def sd_puntos(linea):
    """Desviación típica aproximada de los puntos de un jugador según su línea (ajustada con los residuos
    de la fase 3: 4,8 con media 7; 6,2 con 12; 7,4 con 22; 8,0 con 32)."""
    return 2.6 + np.sqrt(np.maximum(linea, 0.5))


def liquidar(x: pd.DataFrame, sd_linea=sd_puntos) -> pd.DataFrame:
    from scipy.stats import norm
    x = x.copy()
    gana = np.where(x["lado"] == "over", x["y"] == 1, x["y"] == 0)
    x["resultado"] = gana.astype(float)
    x["ganancia"] = np.where(gana, x["cuota"] - 1, -1.0)
    # CLV frente al cierre.
    misma = x["linea_cierre"].notna() & (x["linea_cierre"] == x["line"])
    p_cierre_lado = np.where(x["lado"] == "over", x["p_mercado_cierre"], 1 - x["p_mercado_cierre"])
    x["clv"] = np.where(misma, x["cuota"] * p_cierre_lado - 1, np.nan)
    a_favor = np.where(x["lado"] == "over", x["linea_cierre"] > x["line"], x["linea_cierre"] < x["line"])
    en_contra = np.where(x["lado"] == "over", x["linea_cierre"] < x["line"], x["linea_cierre"] > x["line"])
    precio_a_favor = misma & (p_cierre_lado > x["p_justa"])
    x["bate_cierre"] = np.where(x["linea_cierre"].isna(), np.nan,
                                np.where(a_favor | precio_a_favor, 1.0, np.where(en_contra | misma, 0.0, np.nan)))
    # CLV ajustado por línea: la probabilidad justa del cierre trasladada a NUESTRA línea con una normal
    # centrada en la media que implica el cierre (permite medir CLV aunque la línea se haya movido).
    sd = sd_linea(x["linea_cierre"])
    media_cierre = x["linea_cierre"] + norm.ppf(np.clip(x["p_mercado_cierre"], 0.01, 0.99)) * sd
    p_over_nuestra = 1 - norm.cdf((x["line"] - media_cierre) / sd)
    p_lado = np.where(x["lado"] == "over", p_over_nuestra, 1 - p_over_nuestra)
    x["clv_ajustado"] = np.where(x["linea_cierre"].notna(), x["cuota"] * p_lado - 1, np.nan)
    return x


def maximo_drawdown(ganancias: pd.Series) -> float:
    """Máxima caída de la ganancia acumulada (en unidades) apostando 1 unidad fija."""
    acum = ganancias.cumsum()
    return float((acum.cummax().clip(lower=0) - acum).max()) if len(acum) else 0.0


def bootstrap_roi(x: pd.DataFrame, n: int = 2000, semilla: int = 5) -> tuple[float, float, float]:
    """IC 95 % del ROI y p-valor de ROI <= 0, remuestreando partidos (apuestas del mismo partido no son
    independientes)."""
    if x.empty:
        return np.nan, np.nan, np.nan
    g = x.groupby("game_id")["ganancia"].agg(["sum", "size"])
    s, c = g["sum"].to_numpy(), g["size"].to_numpy()
    idx = np.random.default_rng(semilla).integers(0, len(s), size=(n, len(s)))
    roi = s[idx].sum(1) / c[idx].sum(1)
    return float(np.quantile(roi, 0.025)), float(np.quantile(roi, 0.975)), float((roi <= 0).mean())


def metricas(x: pd.DataFrame) -> dict:
    x = x.sort_values(["fecha", "game_id"])
    lo, hi, p = bootstrap_roi(x)
    return {"apuestas": len(x), "partidos": x["game_id"].nunique(), "acierto": x["resultado"].mean(),
            "p_media": x["p"].mean(), "cuota_media": x["cuota"].mean(), "edge_medio": x["edge"].mean(),
            "ev_medio": x["ev"].mean(), "ganancia_u": x["ganancia"].sum(), "roi": x["ganancia"].mean(),
            "roi_ic_inf": lo, "roi_ic_sup": hi, "p_valor": p, "max_drawdown_u": maximo_drawdown(x["ganancia"]),
            "clv_medio": x["clv"].mean(), "con_clv": int(x["clv"].notna().sum()),
            "clv_ajustado": x["clv_ajustado"].mean(), "bate_cierre": x["bate_cierre"].mean()}


def holm(pvalores: pd.Series) -> pd.Series:
    """p-valores ajustados por Holm-Bonferroni (comparaciones múltiples entre estrategias)."""
    p = pvalores.fillna(1.0)
    orden = p.sort_values().index
    m = len(p)
    ajust = pd.Series(index=p.index, dtype=float)
    acum = 0.0
    for i, k in enumerate(orden):
        acum = max(acum, min(1.0, (m - i) * p[k]))
        ajust[k] = acum
    return ajust


def evaluar(d: pd.DataFrame, estrategias: list[Estrategia]) -> tuple[pd.DataFrame, dict[str, pd.DataFrame]]:
    filas, apuestas = [], {}
    for e in estrategias:
        x = seleccionar(d, e)
        apuestas[e.nombre] = x
        filas.append({"estrategia": e.nombre, **metricas(x)})
    t = pd.DataFrame(filas)
    t["p_valor_holm"] = holm(t["p_valor"]).to_numpy()
    return t, apuestas


def estado_mercado(m_apertura: dict, m_cierre: dict | None = None) -> str:
    """validado: muestra mínima, CLV ajustado positivo y bate el cierre más de la mitad de las veces y,
    si se da el backtest a la cuota de cierre (momento en que se conoce toda la información que usa el
    modelo), su ROI también es positivo con IC 95 % por encima de 0."""
    if m_apertura["apuestas"] < MIN_APUESTAS:
        return "sin validar"
    clv_ok = (m_apertura.get("clv_ajustado") or -1) > 0 and (m_apertura.get("bate_cierre") or 0) > 0.5
    cierre_ok = m_cierre is None or (m_cierre["apuestas"] >= MIN_APUESTAS and (m_cierre["roi_ic_inf"] or -1) > 0)
    return "validado" if clv_ok and cierre_ok else "desactivado"


def calibracion_apuestas(x: pd.DataFrame) -> pd.DataFrame:
    tr = pd.cut(x["p"], [0, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 1.0])
    t = (x.assign(tramo=tr).groupby("tramo", observed=True)
         .agg(apuestas=("resultado", "size"), p_media=("p", "mean"), acierto_real=("resultado", "mean"),
              roi=("ganancia", "mean")).reset_index())
    t["tramo"] = t["tramo"].astype(str)
    return t


def banca_kelly(x: pd.DataFrame, reglas: banca.ReglasBanca = banca.ReglasBanca()) -> dict:
    h = banca.simular_banca(x[["fecha", "p", "cuota", "resultado"]], reglas)
    if h.empty:
        return {}
    return {"banca_final": float(h["banca"].iloc[-1]), "max_drawdown_pct": float(h["drawdown"].max()),
            "dias": len(h), "riesgo_medio_dia_pct": float((h["riesgo"] / h["banca"].shift(1).fillna(100)).mean())}
