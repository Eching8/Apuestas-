"""Comparación de las simulaciones con las cuotas del día: probabilidad final, edge, EV, filtros y monto.

Orden de decisión para cada línea (jugador, mercado, periodo, línea, casa):
1. Probabilidad del modelo: P(over), P(under) y P(empate) de la simulación del partido.
2. Probabilidad justa del mercado: se quita el margen de la casa con sus dos lados (o del consenso si la
   casa solo publica un lado).
3. Probabilidad final: mezcla modelo + mercado (ver mezcla.py).
4. EV = p_gana x cuota + p_empate - 1 y edge = p_final - p_justa del lado.
5. Filtros: EV > 0; edge >= mínimo del mercado (más alto en mercados exóticos); minutos proyectados
   mínimos; sin jugadores en duda; Benjamini-Hochberg sobre todas las líneas del día; estado del mercado.
6. Exposición: máximo de apuestas por jugador y por partido (se quedan las de mayor EV).
7. Monto: Kelly fraccional con tope por apuesta y tope diario, solo en mercados VALIDADOS.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from . import banca as bk
from . import margen as mg
from .mezcla import Mezcla, benjamini_hochberg, p_valor_edge

# Mercado -> estadística de la simulación (los demás mercados se añaden en la fase 6).
SIM_DE_MERCADO = {"pts": "pts", "fg3m": "fg3m", "fgm": "fgm", "ftm": "ftm"}
ESTADOS_EN_DUDA = {"questionable", "doubtful", "day-to-day", "game time decision", "gtd"}


def estado_mercados(con) -> dict[tuple[str, str], str]:
    """(mercado, periodo) -> estado. Sin validación registrada: 'sin validar'."""
    try:
        filas = con.execute("SELECT market, period, estado FROM market_validation").fetchall()
    except Exception:
        filas = []
    return {(m, p): e for m, p, e in filas}


def edge_minimo(cfg_ap: dict, mercado: str, periodo: str) -> float:
    pm = cfg_ap.get("edge_min_por_mercado", {})
    base = float(cfg_ap.get("edge_min", 0.04))
    return max(base, float(pm.get(mercado, base)), float(pm.get(f"periodo_{periodo}", base)))


def lineas_con_lados(cuotas: pd.DataFrame) -> pd.DataFrame:
    """Una fila por casa, jugador, mercado, periodo y línea con la cuota de cada lado y la prob. justa."""
    c = cuotas[cuotas["player_id"].notna() & cuotas["market"].isin(SIM_DE_MERCADO) & (cuotas["bet_type"] == "ou")]
    if c.empty:
        return pd.DataFrame()
    claves = ["source", "book", "game_id", "player_id", "player_name", "market", "period", "line"]
    t = c.pivot_table(index=claves, columns="side", values="odds", aggfunc="max").reset_index()
    for lado in ("over", "under"):
        if lado not in t:
            t[lado] = np.nan
    t = t.rename(columns={"over": "cuota_over", "under": "cuota_under"})
    dos = t["cuota_over"].notna() & t["cuota_under"].notna()
    t["p_justa_over"] = np.where(dos, mg.justa_dos_lados(t["cuota_over"].fillna(2), t["cuota_under"].fillna(2)), np.nan)
    t["margen_casa"] = np.where(dos, 1 / t["cuota_over"] + 1 / t["cuota_under"] - 1, np.nan)
    # Casas con un solo lado (p. ej. CSV de bet365): probabilidad justa del consenso en la misma línea.
    cons = t[t["book"] == "consenso"][["game_id", "player_id", "market", "period", "line", "p_justa_over"]]
    t = t.merge(cons.rename(columns={"p_justa_over": "p_justa_consenso"}),
                on=["game_id", "player_id", "market", "period", "line"], how="left")
    t["p_justa_over"] = t["p_justa_over"].fillna(t["p_justa_consenso"])
    return t.drop(columns="p_justa_consenso")


def evaluar(lineas: pd.DataFrame, filas: pd.DataFrame, sims: dict, mezcla: Mezcla, cfg: dict,
            estados: dict, banca_actual: float) -> pd.DataFrame:
    """Tabla con todas las líneas evaluadas (una fila por línea y lado elegido) y la decisión."""
    cfg_ap = cfg.get("apuestas", {})
    if lineas.empty:
        return pd.DataFrame()
    filas = filas.copy()
    pos = filas.reset_index()[["index", "game_id", "player_id"]]
    t = lineas[lineas["period"] == "game"].merge(pos, on=["game_id", "player_id"])
    if t.empty:
        return pd.DataFrame()
    p_over, p_push = np.empty(len(t)), np.empty(len(t))
    for mercado, col in SIM_DE_MERCADO.items():
        m = (t["market"] == mercado).to_numpy()
        if m.any():
            s = sims[col][t.loc[m, "index"].to_numpy()]
            l = t.loc[m, "line"].to_numpy()[:, None]
            p_over[m], p_push[m] = (s > l).mean(1), (s == l).mean(1)
    t["p_modelo_over"] = p_over / np.clip(1 - p_push, 1e-9, None)     # condicionada a que no haya empate
    t["p_empate"] = p_push
    t["p_final_over"] = np.where(t["p_justa_over"].notna(), mezcla.aplicar(t["p_justa_over"], t["p_modelo_over"]),
                                 np.nan)
    lados = []
    for lado in ("over", "under"):
        p_fin = t["p_final_over"] if lado == "over" else 1 - t["p_final_over"]
        p_mod = t["p_modelo_over"] if lado == "over" else 1 - t["p_modelo_over"]
        p_jus = t["p_justa_over"] if lado == "over" else 1 - t["p_justa_over"]
        cuota = t[f"cuota_{lado}"]
        p_gana = p_fin * (1 - t["p_empate"])
        lados.append(t.assign(lado=lado, cuota=cuota, p_modelo=p_mod, p_justa=p_jus, p_final=p_fin, p_gana=p_gana,
                              ev=p_gana * cuota + t["p_empate"] - 1, edge=p_fin - p_jus))
    x = pd.concat(lados, ignore_index=True)
    x = x[x["cuota"].notna()]
    # Mejor casa para cada lado: la principal (bet365) si la hay; si no, la cuota más alta.
    principal = cfg.get("cuotas", {}).get("casa_principal", "bet365")
    x["es_principal"] = x["book"] == principal
    x = x[x["book"] != "consenso"] if (x["book"] != "consenso").any() else x
    x = (x.sort_values(["es_principal", "cuota"], ascending=False)
         .drop_duplicates(["game_id", "player_id", "market", "period", "line", "lado"]))
    # Lado con más EV de cada línea.
    x = x.sort_values("ev", ascending=False).drop_duplicates(["game_id", "player_id", "market", "period", "line"])

    # Contexto del jugador.
    info = filas[["game_id", "player_id", "name", "team_id", "estado_lesion", "min_si_juega", "p_dnp"]]
    x = x.merge(info, on=["game_id", "player_id"], how="left")
    x["proyeccion"] = [float(sims[SIM_DE_MERCADO[m]][i].mean()) for m, i in zip(x["market"], x["index"])]
    x["estado_mercado"] = [estados.get((m, p), "sin validar") for m, p in zip(x["market"], x["period"])]

    # Filtros.
    x["edge_min"] = [edge_minimo(cfg_ap, m, p) for m, p in zip(x["market"], x["period"])]
    x["p_valor"] = p_valor_edge(x["edge"], mezcla.sd_edge)
    candidatas = (x["ev"] > 0) & (x["edge"] >= x["edge_min"])
    x["pasa_bh"] = False
    x.loc[x.index, "pasa_bh"] = benjamini_hochberg(x["p_valor"], cfg_ap.get("fdr", 0.10))
    en_duda = x["estado_lesion"].fillna("").str.lower().isin(ESTADOS_EN_DUDA)
    motivos = []
    for i, r in x.iterrows():
        m = []
        if not candidatas[i]:
            m.append("sin valor" if r["ev"] <= 0 else "edge bajo")
        if not r["pasa_bh"]:
            m.append("no supera comparaciones múltiples")
        if r["min_si_juega"] < cfg_ap.get("min_minutos", 15):
            m.append("pocos minutos")
        if cfg_ap.get("excluir_en_duda", True) and en_duda[i]:
            m.append(f"en duda ({r['estado_lesion']})")
        if pd.isna(r["p_justa"]):
            m.append("sin probabilidad justa")
        motivos.append("; ".join(m))
    x["motivo_descarte"] = motivos
    x["pick"] = x["motivo_descarte"] == ""

    # Exposición: máximo por jugador y por partido entre los picks (mayor EV primero).
    picks = x[x["pick"]].sort_values("ev", ascending=False)
    picks = picks.groupby(["game_id", "player_id"], group_keys=False).head(cfg_ap.get("max_por_jugador", 1))
    picks = picks.groupby("game_id", group_keys=False).head(cfg_ap.get("max_por_partido", 3))
    x.loc[x["pick"] & ~x.index.isin(picks.index), "motivo_descarte"] = "tope de exposición"
    x["pick"] = x.index.isin(picks.index)

    # Monto: solo en mercados validados.
    reglas = bk.ReglasBanca(cfg_ap.get("fraccion_kelly", 0.25), cfg_ap.get("tope_apuesta", 0.02),
                            cfg_ap.get("tope_diario", 0.10))
    f = pd.Series(np.where(x["pick"] & (x["estado_mercado"] == "validado"),
                           bk.fraccion(x["p_gana"].fillna(0), x["cuota"], reglas), 0.0), index=x.index)
    f = bk.aplicar_tope_diario(f, pd.Series("hoy", index=x.index), reglas.tope_diario)
    x["fraccion_banca"] = f
    x["monto"] = (f * banca_actual).round(2)
    return x.sort_values(["pick", "ev"], ascending=False).reset_index(drop=True)
