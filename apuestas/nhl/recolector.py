"""Descarga de partidos de ESPN a la base: box score y jugada a jugada de los terminados, lesiones de los pendientes."""
from __future__ import annotations

import logging
from datetime import date, timedelta

from ..api_football import ApiError
from .db import NhlDB
from .espn import TERMINADO, Espn, parse_box, parse_injuries, parse_jugadas

log = logging.getLogger(__name__)


def descargar_dia(espn: Espn, db: NhlDB, fecha: str, lesiones: bool = False) -> dict:
    """Guarda los partidos de un día. Un partido ya guardado no se vuelve a pedir."""
    n = {"partidos": 0, "nuevos": 0, "lesiones": 0}
    for g in espn.partidos(fecha):
        db.upsert_game(g, fecha)
        n["partidos"] += 1
        terminado = g["status"] == TERMINADO
        if terminado and db.game_done(g["id"]):
            continue
        if not terminado and not lesiones:
            continue
        try:
            resumen = espn.resumen(g["id"])
        except ApiError as e:
            log.warning("%s: sin resumen de %s @ %s (%s)", fecha, g["away"]["name"], g["home"]["name"], e)
            continue
        if terminado:
            skaters, goalies = parse_box(resumen)
            if skaters:
                db.save_box(g["id"], g["home"]["id"], skaters, goalies, *parse_jugadas(resumen))
                n["nuevos"] += 1
        else:
            filas = parse_injuries(resumen)
            db.save_injuries(fecha, filas)
            n["lesiones"] += len(filas)
        db.commit()
    db.commit()
    return n


def descargar_rango(espn: Espn, db: NhlDB, desde: date, hasta: date) -> int:
    nuevos, dia = 0, desde
    while dia <= hasta:
        n = descargar_dia(espn, db, dia.isoformat())
        if n["partidos"]:
            log.info("%s: %d partidos, %d nuevos guardados", dia, n["partidos"], n["nuevos"])
        nuevos += n["nuevos"]
        dia += timedelta(days=1)
    return nuevos
