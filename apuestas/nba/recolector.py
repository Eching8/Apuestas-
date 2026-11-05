"""Descarga de partidos de ESPN a la base: box score y tiros de los terminados, lesiones de los pendientes."""
from __future__ import annotations

import logging
from datetime import date, timedelta

from ..api_football import ApiError
from .db import NbaDB
from . import jugadas
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
                jugadas.guardar(db.conn, g["id"], jugadas.parse_jugadas(resumen))
                jugadas.guardar_tipos(db.conn, g["id"], jugadas.parse_tipos(resumen))
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


def completar_jugadas(espn: Espn, db: NbaDB, desde: str, limite: int = 600) -> int:
    """Pide de nuevo el resumen de los partidos ya guardados sin jugada a jugada procesada (desde una fecha)."""
    jugadas.preparar(db.conn)
    db.conn.executescript(jugadas.SCHEMA_TIPOS)
    faltan = [r[0] for r in db.conn.execute(
        """SELECT g.id FROM nba_games g WHERE g.box_ok = 1 AND g.fecha >= ? AND g.season_type IN (2, 3)
           AND (NOT EXISTS (SELECT 1 FROM nba_jugadas j WHERE j.game_id = g.id AND j.comp_fga IS NOT NULL)
                OR NOT EXISTS (SELECT 1 FROM nba_tiros_tipo t WHERE t.game_id = g.id))
           ORDER BY g.fecha DESC""", (desde,))]
    hechos = 0
    for gid in faltan[:limite]:
        try:
            resumen = espn.resumen(gid)
            filas = jugadas.parse_jugadas(resumen)
            tipos = jugadas.parse_tipos(resumen)
        except Exception as e:   # un partido sin jugada a jugada no frena el resto
            log.warning("jugadas de %s: %s", gid, e)
            continue
        jugadas.guardar(db.conn, gid, filas or [])
        jugadas.guardar_tipos(db.conn, gid, tipos or [])
        hechos += 1
        if hechos % 50 == 0:
            db.commit()
            log.info("jugada a jugada: %d de %d", hechos, min(limite, len(faltan)))
    db.commit()
    return hechos
