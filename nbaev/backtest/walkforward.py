"""Validación walk-forward por fechas: se entrena con todo lo anterior a cada bloque y se predice el bloque.
Nunca hay división aleatoria: un bloque de prueba es siempre posterior a todos sus datos de entrenamiento."""
from __future__ import annotations

from collections.abc import Callable, Iterator

import pandas as pd


def bloques_mensuales(fechas: pd.Series, desde: str, hasta: str | None = None) -> Iterator[tuple[pd.Timestamp, pd.Timestamp]]:
    """(inicio, fin) de cada mes con partidos entre `desde` y `hasta`."""
    f = pd.to_datetime(fechas)
    meses = sorted(f[(f >= pd.Timestamp(desde)) & ((f <= pd.Timestamp(hasta)) if hasta else True)].dt.to_period("M").unique())
    for mes in meses:
        yield mes.start_time, (mes + 1).start_time


def walk_forward(df: pd.DataFrame, entrenar: Callable[[pd.DataFrame], object],
                 predecir: Callable[[object, pd.DataFrame], pd.DataFrame], desde: str, hasta: str | None = None,
                 col_fecha: str = "start_utc", log=None) -> pd.DataFrame:
    """Devuelve las filas de prueba con sus predicciones fuera de muestra."""
    salidas = []
    for ini, fin in bloques_mensuales(df[col_fecha], desde, hasta):
        train = df[df[col_fecha] < ini]
        test = df[(df[col_fecha] >= ini) & (df[col_fecha] < fin)]
        if test.empty or train.empty:
            continue
        modelo = entrenar(train)
        pred = predecir(modelo, test)
        salidas.append(pd.concat([test, pred], axis=1).assign(bloque=ini.strftime("%Y-%m")))
        if log:
            log.info("Bloque %s: entrenado con %d filas, %d de prueba", ini.strftime("%Y-%m"), len(train), len(test))
    return pd.concat(salidas, ignore_index=True) if salidas else pd.DataFrame()
