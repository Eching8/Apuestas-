"""Mantiene la base al día: partidos, estadísticas, jugada a jugada, plantillas, traspasos y lesiones.

Cada archivo de nflverse se pide con su ETag: si no cambió desde la última vez, no se descarga ni se procesa,
así que ejecutarlo varias veces al día cuesta casi nada. Las temporadas pasadas se descargan una sola vez.
"""
from __future__ import annotations

import logging

from ..nba.sgo import clave_nombre
from .db import STATS_JUGADOR, NflDB
from .fuentes import (EspnNfl, Nflverse, agregar_pbp, cambios_semanales, parse_calendario, parse_lesiones_nflverse,
                      parse_roster_semanal, parse_snaps, parse_stats_jugador, traspasos_en_texto)

log = logging.getLogger(__name__)


# Sube cuando cambia lo que se extrae de los archivos: obliga a procesarlos de nuevo aunque no hayan cambiado.
VERSION_PROCESO = "3"


def _archivo(db: NflDB, nv: Nflverse, ruta: str, forzar: bool = False) -> list[dict] | None:
    url = nv.url(ruta)
    guardado = db.etag(url) or ""
    etag_previo, _, version = guardado.rpartition("#v")
    previo = etag_previo if version == VERSION_PROCESO and not forzar else None
    filas, etag = nv.descargar(ruta, previo)
    if filas is not None:
        db.guardar_etag(url, f"{etag or ''}#v{VERSION_PROCESO}")
    return filas


def actualizar(db: NflDB, nv: Nflverse, temporadas: list[int], espn: EspnNfl | None = None,
               forzar: bool = False) -> dict:
    """Descarga lo que haya cambiado. Devuelve un resumen con lo que se guardó."""
    r = {"partidos": 0, "jugadores": {}, "pbp": [], "traspasos": [], "lesiones": 0, "lesiones_espn": 0,
         "transacciones": 0}
    filas = _archivo(db, nv, "schedules/games.csv", forzar)
    if filas is not None:
        r["partidos"] = db.upsert_games(parse_calendario(filas, set(temporadas)))
        db.commit()
    actual = max(temporadas)
    for season in temporadas:
        filas = _archivo(db, nv, f"stats_player/stats_player_week_{season}.csv", forzar)
        if filas is not None:
            r["jugadores"][season] = db.reemplazar_player_games(season, parse_stats_jugador(filas, STATS_JUGADOR))
            db.commit()
        filas = _archivo(db, nv, f"pbp/play_by_play_{season}.csv.gz", forzar)
        if filas is not None:
            db.reemplazar_pbp(season, agregar_pbp(filas))
            r["pbp"].append(season)
            db.commit()
        filas = _archivo(db, nv, f"weekly_rosters/roster_weekly_{season}.csv", forzar)
        if filas is not None:
            cambios = db.actualizar_roster(parse_roster_semanal(filas))
            en_temporada = cambios_semanales(filas)
            con_semana = {c["player_id"] for c in en_temporada}
            for c in en_temporada:
                db.guardar_movimiento(c["player_id"], season, c["week"], c["from_team"], c["to_team"], "nflverse")
            for c in cambios:
                if c["player_id"] not in con_semana:
                    db.guardar_movimiento(c["player_id"], season, 0 if c["season"] != c.get("prev_season") else
                                          c["week"], c["from_team"], c["to_team"], "nflverse")
            if season == actual:
                r["traspasos"] = en_temporada
            db.commit()
        filas = _archivo(db, nv, f"snap_counts/snap_counts_{season}.csv", forzar)
        if filas is not None:
            pfr = {row[0]: row[1] for row in db.conn.execute(
                "SELECT pfr_id, player_id FROM nfl_rosters WHERE pfr_id IS NOT NULL")}
            db.reemplazar_snaps(season, parse_snaps(filas, pfr))
            db.commit()
    filas = _archivo(db, nv, f"injuries/injuries_{actual}.csv", forzar)
    if filas is not None:
        r["lesiones"] = db.guardar_lesiones(parse_lesiones_nflverse(filas), "nfl")
        db.commit()
    if espn is not None:
        r.update(actualizar_espn(db, espn, actual))
    return r


def actualizar_espn(db: NflDB, espn: EspnNfl, season: int) -> dict:
    """Parte de lesiones al momento y traspasos recientes (más rápido que las plantillas semanales)."""
    por_espn = {row[0]: row[1] for row in db.conn.execute(
        "SELECT espn_id, player_id FROM nfl_rosters WHERE espn_id IS NOT NULL")}
    por_nombre = _indice_nombres(db)
    filas = []
    for les in espn.lesiones():
        pid = por_espn.get(les["espn_id"]) or por_nombre.get((clave_nombre(les["name"]), les["team"]))
        if pid:
            filas.append({**les, "player_id": pid, "season": season})
    n_les = db.guardar_lesiones(filas, "espn")
    trans = espn.transacciones()
    n_trans = db.guardar_transacciones(trans)
    traspasos = []
    por_solo_nombre = {}
    for (nombre, team), pid in por_nombre.items():
        por_solo_nombre.setdefault(nombre, []).append((team, pid))
    for t in traspasos_en_texto(trans):
        candidatos = [pid for team, pid in por_solo_nombre.get(clave_nombre(t["name"]), [])
                      if team in (t["from_team"], t["to_team"])]
        if len(candidatos) != 1:
            continue
        pid = candidatos[0]
        actual = db.conn.execute("SELECT team, week FROM nfl_rosters WHERE player_id = ?", (pid,)).fetchone()
        if actual and actual["team"] != t["to_team"]:
            db.conn.execute("UPDATE nfl_rosters SET team = ?, updated_at = datetime('now') WHERE player_id = ?",
                            (t["to_team"], pid))
            db.conn.execute(
                "INSERT OR IGNORE INTO nfl_movimientos(player_id, season, week, from_team, to_team, fuente, detected_at) "
                "VALUES (?, ?, ?, ?, ?, 'espn', datetime('now'))",
                (pid, season, (actual["week"] or 0) + 1, actual["team"], t["to_team"]))
            traspasos.append({**t, "player_id": pid})
    db.commit()
    return {"lesiones_espn": n_les, "transacciones": n_trans, "traspasos_espn": traspasos}


def _indice_nombres(db: NflDB) -> dict[tuple[str, str], str]:
    return {(clave_nombre(r["name"] or ""), r["team"]): r["player_id"]
            for r in db.conn.execute("SELECT player_id, name, team FROM nfl_rosters")}
