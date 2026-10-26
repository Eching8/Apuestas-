"""Comparación de las simulaciones con las cuotas del día: probabilidad final, edge, EV, filtros y monto.

Orden de decisión para cada línea (jugador, mercado, periodo, línea, casa):
1. Probabilidad del modelo con la simulación del partido (todas las líneas y mercados salen de la misma).
2. Probabilidad justa del mercado: se quita el margen de la casa con sus dos lados (o del consenso si la
   casa solo publica un lado). Primera canasta: método de Shin sobre todos los jugadores del partido.
3. Probabilidad final: mezcla modelo + mercado propia de cada mercado (ver mezcla.py).
4. EV = p_gana x cuota + p_empate - 1 y edge = p_final - p_justa del lado.
5. Filtros: EV > 0; edge >= mínimo del mercado (más alto en mercados exóticos); minutos proyectados
   mínimos; sin jugadores en duda; Benjamini-Hochberg sobre todas las líneas del día; estado del mercado.
6. Exposición: máximo de apuestas por jugador y por partido (se quedan las de mayor EV).
7. Monto: Kelly fraccional con tope por apuesta y tope diario, solo en mercados VALIDADOS.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from ..models import estadisticas as me
from ..models.proyeccion import MERCADOS_PERIODO, valor
from . import banca as bk
from . import margen as mg
from .mezcla import Mezcla, benjamini_hochberg, p_valor_edge

MERCADOS_OU = me.SIMPLES | set(me.DERIVADOS)
MERCADOS_SN = {"doble_doble", "triple_doble"}
ESTADOS_EN_DUDA = {"questionable", "doubtful", "day-to-day", "game time decision", "gtd"}
CLAVE = ["game_id", "player_id", "market", "period", "line"]


def estado_mercados(con) -> dict[tuple[str, str], str]:
    """(mercado, periodo) -> estado. Si la base no tiene validaciones (clon nuevo, GitHub Actions) se usa el
    resultado versionado en config/estado_mercados.json. Sin validación registrada: 'sin validar'."""
    try:
        filas = con.execute("SELECT market, period, estado FROM market_validation").fetchall()
    except Exception:
        filas = []
    if not filas:
        import json

        from ..config import RAIZ
        ruta = RAIZ / "config" / "estado_mercados.json"
        if ruta.exists():
            filas = [(d["market"], d["period"], d["estado"]) for d in json.loads(ruta.read_text(encoding="utf-8"))]
    return {(m, p): e for m, p, e in filas}


def edge_minimo(cfg_ap: dict, mercado: str, periodo: str) -> float:
    pm = cfg_ap.get("edge_min_por_mercado", {})
    base = float(cfg_ap.get("edge_min", 0.04))
    return max(base, float(pm.get(mercado, base)), float(pm.get(f"periodo_{periodo}", base)))


def modelable(mercado: str, periodo: str, bet_type: str) -> bool:
    if bet_type == "ou":
        return mercado in MERCADOS_OU if periodo == "game" else (periodo in ("1q", "1h") and mercado in MERCADOS_PERIODO)
    return periodo == "game" and (mercado in MERCADOS_SN or mercado == "primera_canasta")


def lineas_con_lados(cuotas: pd.DataFrame) -> pd.DataFrame:
    """Una fila por casa, jugador, mercado, periodo y línea con la cuota de cada lado y la prob. justa
    del lado 'over' / 'sí'."""
    c = cuotas[cuotas["player_id"].notna()].copy()
    if c.empty:
        return pd.DataFrame()
    c = c[[modelable(m, p, b) for m, p, b in zip(c["market"], c["period"], c["bet_type"])]]
    if c.empty:
        return pd.DataFrame()
    c["lado_std"] = c["side"].map({"over": "over", "yes": "over", "under": "under", "no": "under"})
    c["line"] = c["line"].fillna(-1.0)       # sí/no sin línea: marcador para poder agrupar
    claves = ["source", "book", "game_id", "player_id", "player_name", "market", "period", "bet_type", "line"]
    t = c.pivot_table(index=claves, columns="lado_std", values="odds", aggfunc="max").reset_index()
    for lado in ("over", "under"):
        if lado not in t:
            t[lado] = np.nan
    t = t.rename(columns={"over": "cuota_over", "under": "cuota_under"})
    dos = t["cuota_over"].notna() & t["cuota_under"].notna()
    t["p_justa_over"] = np.where(dos, mg.justa_dos_lados(t["cuota_over"].fillna(2), t["cuota_under"].fillna(2)), np.nan)
    # Sin margen no es una cuota real (valores de relleno de la fuente, p. ej. 2,00 / 2,00): se descarta.
    margen_casa = 1 / t["cuota_over"] + 1 / t["cuota_under"] - 1
    t = t[~(dos & (margen_casa < 0.01))].copy()
    # Primera canasta (solo "sí"): Shin sobre todos los jugadores del partido en esa casa.
    pc = t["market"] == "primera_canasta"
    for (_, gid), g in t[pc & t["cuota_over"].notna()].groupby(["book", "game_id"]):
        if len(g) >= 5:
            t.loc[g.index, "p_justa_over"] = mg.justa(g["cuota_over"].to_numpy(), "shin")
    # Casas con un solo lado: probabilidad justa del consenso en la misma línea.
    cons = t[t["book"] == "consenso"][CLAVE + ["p_justa_over"]]
    t = t.merge(cons.rename(columns={"p_justa_over": "p_justa_consenso"}), on=CLAVE, how="left")
    t["p_justa_over"] = t["p_justa_over"].fillna(t["p_justa_consenso"])
    return t.drop(columns="p_justa_consenso")


def prob_modelo(t: pd.DataFrame, filas: pd.DataFrame, sims: dict, primer: pd.DataFrame | None) -> pd.DataFrame:
    """P(over/sí) condicionada a que no haya empate, P(empate) y proyección (media) de cada línea."""
    p_over, p_push, proy = np.full(len(t), np.nan), np.zeros(len(t)), np.full(len(t), np.nan)
    for (mk, per), g in t.groupby(["market", "period"]):
        pos = g.index.to_numpy()
        if mk == "primera_canasta":
            if primer is not None and not primer.empty:
                mp_ = primer[primer["player_id"] != "SUPLENTE"].set_index(["game_id", "player_id"])["p_partido"]
                p_over[pos] = [mp_.get((a, b), np.nan) for a, b in zip(g["game_id"], g["player_id"])]
            continue
        v = valor(sims, mk, per)[g["index"].to_numpy()]
        proy[pos] = v.mean(1)
        if mk in MERCADOS_SN:
            p_over[pos] = v.mean(1)
        else:
            l = g["line"].to_numpy()[:, None]
            po, pe = (v > l).mean(1), (v == l).mean(1)
            p_over[pos], p_push[pos] = po / np.clip(1 - pe, 1e-9, None), pe
    t["p_modelo_over"] = np.clip(p_over, 0.0005, 0.9995)
    t["p_empate"] = p_push
    t["proyeccion"] = proy
    return t


def evaluar(lineas: pd.DataFrame, filas: pd.DataFrame, sims: dict, mezclas: dict[str, Mezcla], cfg: dict,
            estados: dict, banca_actual: float, primer: pd.DataFrame | None = None) -> pd.DataFrame:
    """Tabla con todas las líneas evaluadas (una fila por línea y lado elegido) y la decisión."""
    cfg_ap = cfg.get("apuestas", {})
    if lineas.empty:
        return pd.DataFrame()
    filas = filas.copy()
    pos = filas.reset_index()[["index", "game_id", "player_id"]]
    t = lineas.merge(pos, on=["game_id", "player_id"]).reset_index(drop=True)
    if t.empty:
        return pd.DataFrame()
    t = prob_modelo(t, filas, sims, primer)
    defecto = mezclas.get("_defecto", Mezcla(peso_mercado=0.7, peso_modelo=0.3, sd_edge=0.04))
    t["p_final_over"] = np.nan
    for mk, g in t.groupby("market"):
        mz = mezclas.get(mk, defecto)
        ok = g["p_justa_over"].notna()
        t.loc[g.index[ok], "p_final_over"] = mz.aplicar(g.loc[ok, "p_justa_over"], g.loc[ok, "p_modelo_over"])
        t.loc[g.index, "sd_edge"] = mz.sd_edge
    lados = []
    for lado in ("over", "under"):
        signo = lado == "over"
        p_fin = t["p_final_over"] if signo else 1 - t["p_final_over"]
        p_mod = t["p_modelo_over"] if signo else 1 - t["p_modelo_over"]
        p_jus = t["p_justa_over"] if signo else 1 - t["p_justa_over"]
        cuota = t[f"cuota_{lado}"]
        p_gana = p_fin * (1 - t["p_empate"])
        nombre = np.where(t["bet_type"] == "yn", "sí" if signo else "no", lado)
        lados.append(t.assign(lado=nombre, cuota=cuota, p_modelo=p_mod, p_justa=p_jus, p_final=p_fin, p_gana=p_gana,
                              ev=p_gana * cuota + t["p_empate"] - 1, edge=p_fin - p_jus))
    x = pd.concat(lados, ignore_index=True)
    x = x[x["cuota"].notna()]
    x["line"] = x["line"].where(x["line"] >= 0)          # quita el marcador de los mercados sí/no
    # Mejor casa para cada lado: la principal (bet365) si la hay; si no, la cuota más alta (nunca el consenso).
    principal = cfg.get("cuotas", {}).get("casa_principal", "bet365")
    x["es_principal"] = x["book"] == principal
    if (x["book"] != "consenso").any():
        x = x[x["book"] != "consenso"]
    clave = ["game_id", "player_id", "market", "period", "line"]
    x = (x.sort_values(["es_principal", "cuota"], ascending=False)
         .drop_duplicates(clave + ["lado"], ignore_index=True))
    x = x.sort_values("ev", ascending=False).drop_duplicates(clave, ignore_index=True)

    info = filas[["game_id", "player_id", "name", "team_id", "estado_lesion", "min_si_juega", "p_dnp"]]
    x = x.merge(info, on=["game_id", "player_id"], how="left")
    x["estado_mercado"] = [estados.get((m, p), "sin validar") for m, p in zip(x["market"], x["period"])]

    # Filtros.
    x["edge_min"] = [edge_minimo(cfg_ap, m, p) for m, p in zip(x["market"], x["period"])]
    x["p_valor"] = [float(p_valor_edge(e, s)) for e, s in zip(x["edge"].fillna(-1), x["sd_edge"].fillna(0.04))]
    candidatas = (x["ev"] > 0) & (x["edge"] >= x["edge_min"])
    x["pasa_bh"] = benjamini_hochberg(x["p_valor"], cfg_ap.get("fdr", 0.10))
    en_duda = x["estado_lesion"].fillna("").str.lower().isin(ESTADOS_EN_DUDA)
    motivos = []
    for i, r in x.iterrows():
        m = []
        if not candidatas[i]:
            m.append("sin valor" if not r["ev"] > 0 else "edge bajo")
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
    x["fraccion_banca"] = bk.aplicar_tope_diario(f, pd.Series("hoy", index=x.index), reglas.tope_diario)
    x["monto"] = (x["fraccion_banca"] * banca_actual).round(2)
    return x.sort_values(["pick", "ev"], ascending=False).reset_index(drop=True)
