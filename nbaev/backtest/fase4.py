"""Fase 4: backtest del mercado de puntos con cuotas reales y decisión de validación del mercado."""
from __future__ import annotations

import logging

import duckdb
import pandas as pd

from ..data import db
from . import apuestas as ap

log = logging.getLogger(__name__)

PRINCIPAL = "Mezcla LightGBM, edge >= 4 % (principal)"
CIERRE = "Mezcla LightGBM a la cuota de cierre, edge >= 4 %"


def diagnostico_origen(x: pd.DataFrame, lineas_oos: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """¿De dónde sale el ROI? Por movimiento de la línea hasta el cierre y por bajas de compañeros."""
    import numpy as np
    mov = np.where(x["lado"] == "over", x["linea_cierre"] - x["line"], x["line"] - x["linea_cierre"])
    cat = pd.cut(pd.Series(mov, index=x.index), [-99, -0.5, 0.49, 99], labels=["en contra", "sin cambio", "a favor"])
    t1 = (x.assign(movimiento=cat.astype(str).where(x["linea_cierre"].notna(), "sin cierre"))
          .groupby("movimiento").agg(apuestas=("ganancia", "size"), acierto=("resultado", "mean"),
                                     roi=("ganancia", "mean")).reset_index())
    t2 = pd.DataFrame()
    if "libres" in x:
        y = x.copy()
        y["minutos_liberados_equipo"] = pd.cut(y["libres"].abs(), [-1, 5, 15, 500], labels=["<= 5", "5-15", "> 15"])
        t2 = (y.groupby("minutos_liberados_equipo", observed=True)
              .agg(apuestas=("ganancia", "size"), roi=("ganancia", "mean")).reset_index())
    return {"movimiento": t1, "bajas": t2}


def estrategias() -> list[ap.Estrategia]:
    return [
        ap.Estrategia(PRINCIPAL, "p_lgb_mezcla", 0.04),
        ap.Estrategia("Mezcla LightGBM, edge >= 2 %", "p_lgb_mezcla", 0.02),
        ap.Estrategia("Mezcla LightGBM, edge >= 6 %", "p_lgb_mezcla", 0.06),
        ap.Estrategia("Mezcla cuantílico, edge >= 4 %", "p_cuant_mezcla", 0.04),
        ap.Estrategia("Mezcla baseline, edge >= 4 %", "p_base_mezcla", 0.04),
        ap.Estrategia("LightGBM puro (sin mercado), edge >= 4 %", "p_lgb", 0.04),
        ap.Estrategia("Baseline puro, edge >= 4 %", "p_base", 0.04),
        ap.Estrategia("Control: todos los over a la apertura", "p_mercado", lado_fijo="over"),
        ap.Estrategia("Control: todos los under a la apertura", "p_mercado", lado_fijo="under"),
    ]


def ejecutar(con: duckdb.DuckDBPyConnection, lineas_oos: pd.DataFrame, mercado: str = "pts") -> dict:
    fechas = con.execute("SELECT game_id, fecha FROM games").df()
    lin = lineas_oos.merge(fechas, on="game_id", how="left")
    d = ap.preparar(lin, ["p_lgb", "p_base", "p_cuant"])
    # Solo se evalúan las aperturas donde ya existe la mezcla (hace falta historial previo para ajustarla).
    d = d[d["p_lgb_mezcla"].notna()].copy()
    tabla, apuestas = ap.evaluar(d, estrategias())
    principal = apuestas[PRINCIPAL]
    m = tabla.set_index("estrategia").loc[PRINCIPAL].to_dict()
    # Mismo modelo apostando a la cuota de CIERRE: es el momento en que de verdad se conoce lo que usa el
    # modelo (quién se viste, spread y total de cierre). Es la prueba realista.
    dc = ap.preparar(lin, ["p_lgb"], kind="cierre")
    dc = dc[dc["p_lgb_mezcla"].notna()].copy()
    tabla_c, apuestas_c = ap.evaluar(dc, [ap.Estrategia(CIERRE, "p_lgb_mezcla", 0.04),
                                          ap.Estrategia("Mezcla LightGBM a la cuota de cierre, edge >= 2 %",
                                                        "p_lgb_mezcla", 0.02),
                                          ap.Estrategia("LightGBM puro a la cuota de cierre, edge >= 4 %",
                                                        "p_lgb", 0.04)])
    m_c = tabla_c.set_index("estrategia").loc[CIERRE].to_dict()
    estado = ap.estado_mercado(m, m_c)
    origen = diagnostico_origen(principal, lineas_oos)
    por_mes = (principal.assign(mes=pd.to_datetime(principal["fecha"]).dt.strftime("%Y-%m")).groupby("mes")
               .agg(apuestas=("ganancia", "size"), roi=("ganancia", "mean"), clv_ajustado=("clv_ajustado", "mean"),
                    bate_cierre=("bate_cierre", "mean")).reset_index())
    por_lado = (principal.groupby("lado").agg(apuestas=("ganancia", "size"), acierto=("resultado", "mean"),
                                              roi=("ganancia", "mean"), clv_ajustado=("clv_ajustado", "mean")).reset_index())
    return {"mercado": mercado, "tabla": tabla, "apuestas": apuestas, "estado": estado, "metricas": m,
            "tabla_cierre": tabla_c, "metricas_cierre": m_c, "origen": origen,
            "por_mes": por_mes, "por_lado": por_lado, "calibracion": ap.calibracion_apuestas(principal),
            "banca": ap.banca_kelly(principal), "lineas_evaluadas": len(d),
            "periodo": (str(d["fecha"].min()), str(d["fecha"].max()))}


def guardar_validacion(con: duckdb.DuckDBPyConnection, r: dict, period: str = "game", bet_type: str = "ou") -> None:
    m, mc = r["metricas"], r["metricas_cierre"]
    motivo = ("ROI a la cuota de cierre negativo: la ventaja a la apertura viene de información que solo se "
              "conoce cerca del partido" if r["estado"] == "desactivado" else "")
    db.upsert(con, "market_validation", [{
        "market": r["mercado"], "period": period, "estrategia": PRINCIPAL, "desde": r["periodo"][0],
        "hasta": r["periodo"][1], "apuestas": m["apuestas"], "roi_apertura": m["roi"], "roi_ic_inf": m["roi_ic_inf"],
        "roi_ic_sup": m["roi_ic_sup"], "clv_ajustado": m["clv_ajustado"], "bate_cierre": m["bate_cierre"],
        "max_drawdown_u": m["max_drawdown_u"], "apuestas_cierre": mc["apuestas"], "roi_cierre": mc["roi"],
        "roi_cierre_ic_inf": mc["roi_ic_inf"], "roi_cierre_ic_sup": mc["roi_ic_sup"], "estado": r["estado"],
        "motivo": motivo, "evaluado_at": db.ahora_utc()}])
    con.execute("UPDATE market_catalog SET estado = ? WHERE market = ? AND period = ? AND bet_type = ?",
                [r["estado"], r["mercado"], period, bet_type])


def informe(r: dict) -> str:
    f = lambda t: t.to_markdown(index=False, floatfmt=".4f")  # noqa: E731
    m, b = r["metricas"], r["banca"]
    cols = ["estrategia", "apuestas", "acierto", "cuota_media", "edge_medio", "roi", "roi_ic_inf", "roi_ic_sup",
            "p_valor", "p_valor_holm", "max_drawdown_u", "clv_ajustado", "bate_cierre"]
    mc = r["metricas_cierre"]
    return "\n\n".join([
        "# Fase 4: backtest del mercado de puntos con cuotas reales",
        f"Líneas de apertura evaluadas: {r['lineas_evaluadas']:,} ({r['periodo'][0]} a {r['periodo'][1]}). "
        "Cuotas de consenso de SportsGameOdds (casas de EE. UU.; bet365 no está en la fuente). Se apuesta a la "
        "cuota de apertura con la probabilidad mezcla modelo + mercado ajustada walk-forward. ROI con apuesta "
        "fija de 1 unidad; IC 95 % y p-valor por bootstrap remuestreando partidos; p-valor de Holm por haber "
        "probado varias estrategias.",
        "## Estrategias", f(r["tabla"][cols]),
        "## ¿De dónde sale el ROI a la apertura?",
        "Por movimiento de la línea entre apertura y cierre (a favor = el mercado se movió hacia la apuesta):",
        f(r["origen"]["movimiento"]),
        "Por minutos habituales liberados en el equipo (bajas de compañeros conocidas solo poco antes del partido):",
        f(r["origen"]["bajas"]) if not r["origen"]["bajas"].empty else "(sin datos)",
        "## Prueba realista: apostar a la cuota de cierre",
        "El modelo usa información que solo se conoce cerca del salto (quién se viste, spread y total de cierre). "
        "Esa información no existía cuando se publicó la apertura, así que el ROI a la apertura no es alcanzable: "
        "quien la tiene ya ve cuotas parecidas al cierre. Esta es la medida honesta de la ventaja del modelo:",
        f(r["tabla_cierre"][cols]),
        f"## Mercado de puntos: **{r['estado'].upper()}**",
        f"- A la apertura: {m['apuestas']:.0f} apuestas, ROI {m['roi']:+.2%} (IC 95 % [{m['roi_ic_inf']:+.2%}, "
        f"{m['roi_ic_sup']:+.2%}]), CLV ajustado por línea {m['clv_ajustado']:+.2%}, bate el cierre en el "
        f"{m['bate_cierre']:.1%}.\n- A la cuota de cierre (realista): {mc['apuestas']:.0f} apuestas, ROI {mc['roi']:+.2%} "
        f"(IC 95 % [{mc['roi_ic_inf']:+.2%}, {mc['roi_ic_sup']:+.2%}]).\n- Máximo drawdown con apuesta fija (apertura): "
        f"{m['max_drawdown_u']:.1f} unidades.\n- Banca con 1/4 Kelly (tope 2 % por apuesta, 10 % por día), "
        f"empezando en 100: termina en {b.get('banca_final', float('nan')):.1f}, máximo drawdown "
        f"{b.get('max_drawdown_pct', float('nan')):.1%} (no alcanzable por lo explicado arriba).\n- Regla de validación: "
        f"al menos {ap.MIN_APUESTAS} apuestas, CLV ajustado positivo, batir el cierre más de la mitad de las veces y ROI "
        "con IC 95 % por encima de 0 al apostar en el momento en que se conoce la información que usa el modelo.",
        "## Por mes (estrategia principal)", f(r["por_mes"]),
        "## Por lado", f(r["por_lado"]),
        "## Calibración de las apuestas (probabilidad usada frente a acierto real)", f(r["calibracion"]),
    ])
