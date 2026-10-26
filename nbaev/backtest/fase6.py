"""Fase 6: backtest mercado por mercado e informe de todos los mercados."""
from __future__ import annotations

import logging

import duckdb
import pandas as pd

from ..models import primer_anotador as pa
from . import fase4
from . import mercados as bm

log = logging.getLogger(__name__)


# Ninguna casa real cotiza sin margen: las líneas con margen < 1 % (p. ej. 2,00 / 2,00 en pérdidas) son
# valores de relleno de la fuente y se descartan.
MARGEN_MINIMO = 0.01


def ejecutar(con: duckdb.DuckDBPyConnection, lineas: pd.DataFrame, guardar: bool = True) -> dict:
    resultados, filas = {}, []
    lineas = lineas[lineas["margen"] >= MARGEN_MINIMO]
    for mk, d in lineas.groupby("market"):
        if (d["kind"] == "apertura").sum() < 300:
            log.info("%s: muy pocas líneas de apertura (%d), queda sin validar", mk, (d["kind"] == "apertura").sum())
            continue
        r = fase4.ejecutar(con, d, mercado=mk)
        resultados[mk] = r
        m, mc = r["metricas"], r["metricas_cierre"]
        filas.append({"mercado": mk, "líneas apertura": r["lineas_evaluadas"], "apuestas": m["apuestas"],
                      "ROI apertura": m["roi"], "IC inf": m["roi_ic_inf"], "IC sup": m["roi_ic_sup"],
                      "CLV ajustado": m["clv_ajustado"], "bate cierre": m["bate_cierre"],
                      "apuestas al cierre": mc["apuestas"], "ROI al cierre": mc["roi"],
                      "IC inf cierre": mc["roi_ic_inf"], "IC sup cierre": mc["roi_ic_sup"], "estado": r["estado"]})
        if guardar:
            bet_type = "yn" if mk in bm.MERCADOS_SN else "ou"
            fase4.guardar_validacion(con, r, bet_type=bet_type)
    return {"resumen": pd.DataFrame(filas), "detalle": resultados}


def informe(r: dict, pit: pd.DataFrame, lineas: pd.DataFrame, maximo: pd.DataFrame, primer: pd.DataFrame) -> str:
    f = lambda t: t.to_markdown(index=False, floatfmt=".4f")  # noqa: E731
    res_max, cal_max = bm.tabla_maximo(maximo)
    res_pa, cal_pa = pa.informe(primer)
    partes = [
        "# Fase 6: todos los mercados de jugador",
        "Una sola simulación por partido para todos los mercados (minutos -> tiros -> puntos, triples, tiros de "
        "campo y libres; rebotes ofensivos y defensivos, asistencias, robos, tapones y pérdidas con su propio "
        "LightGBM de tasa y su binomial negativa; reparto por periodos; primer anotador). Validación walk-forward "
        "mensual de la temporada 2025-26 con minutos proyectados fuera de muestra.",
        "## 1. Calibración de cada distribución (PIT aleatorizado; ideal 0,10 en cada decil)",
        "Incluye las props de 1.er cuarto y 1.ª mitad, que no tienen cuotas históricas: es su única validación "
        "hasta acumular capturas diarias.",
        f(bm.tabla_pit(pit)),
        "## 2. Probabilidad frente a las líneas reales de cada mercado (log loss; menor es mejor)",
        f(bm.tabla_probabilidades(lineas)),
        "## 3. Backtest de apuestas por mercado",
        "Mismas reglas que la fase 4: mezcla modelo + mercado ajustada walk-forward, edge >= 4 %, máximo 1 por "
        "jugador y 3 por partido. 'ROI al cierre' es la prueba realista (apostar cuando se conoce lo que usa el "
        "modelo). Validado = >= 300 apuestas, CLV ajustado > 0, bate el cierre > 50 % y ROI al cierre con IC 95 % > 0.",
        f(r["resumen"]),
        "## 4. Máximo anotador del partido (comparativo, sin cuotas históricas)",
        f(res_max), f(cal_max),
        "## 5. Primera canasta (submodelo propio, sin cuotas históricas)",
        "Log loss multiclase de quién anota la primera canasta de campo (titulares + 'un suplente'), partidos desde "
        "octubre de 2024, con información anterior a cada partido y los titulares confirmados.",
        f(res_pa), f(cal_pa),
    ]
    return "\n\n".join(partes)
