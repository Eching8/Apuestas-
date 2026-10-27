"""Descarga de partidos de ESPN a la base: box score y tiros de los terminados, lesiones de los pendientes."""
from __future__ import annotations

import logging
from datetime import date, timedelta

from ..api_football import ApiError
from .db import NbaDB
from .espn import TERMINADO, Espn, parse_box, parse_injuries, parse_shots

log = logging.getLogger(__name__)


def descargar_dia(espn: Espn, db: NbaDB, fecha: str, lesiones: bool = False) -> dict:
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
            # Algunos partidos (aplazados, exhibiciones) no tienen resumen: no deben frenar el resto.
            log.warning("%s: sin resumen de %s @ %s (%s)", fecha, g["away"]["name"], g["home"]["name"], e)
            continue
        if terminado:
            players = parse_box(resumen)
            if players:
                db.save_box(g["id"], g["home"]["id"], players, parse_shots(resumen))
                n["nuevos"] += 1
        else:
            filas = parse_injuries(resumen)
            db.save_injuries(fecha, filas)
            n["lesiones"] += len(filas)
        db.commit()
    db.commit()
    return n


def descargar_rango(espn: Espn, db: NbaDB, desde: date, hasta: date) -> int:
    nuevos, dia = 0, desde
    while dia <= hasta:
        n = descargar_dia(espn, db, dia.isoformat())
        if n["partidos"]:
            log.info("%s: %d partidos, %d nuevos guardados", dia, n["partidos"], n["nuevos"])
        nuevos += n["nuevos"]
        dia += timedelta(days=1)
    return nuevos


def descargar_alturas(espn: Espn, db: NbaDB) -> int:
    """Estaturas de las plantillas actuales de los 30 equipos (una consulta por equipo)."""
    n = 0
    for (team_id,) in db.conn.execute("SELECT id FROM nba_teams").fetchall():
        try:
            filas = espn.plantilla(team_id)
        except ApiError as e:
            log.warning("plantilla de %s: %s", team_id, e)
            continue
        db.save_alturas(filas)
        n += len(filas)
    db.commit()
    return n
