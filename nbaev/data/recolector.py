"""Descarga incremental de ESPN a DuckDB: calendario, partidos terminados y parte de lesiones.

Un partido terminado se descarga una sola vez (queda en crudos/ comprimido y en la base), así que
cada actualización diaria solo pide lo nuevo.
"""
from __future__ import annotations

import logging
from datetime import date, datetime, timedelta

import duckdb

from . import db, espn
from .procesar import procesar

log = logging.getLogger(__name__)


def temporada_de(fecha: date) -> int:
    """Año de inicio de la temporada que contiene la fecha (la NBA empieza en octubre)."""
    return fecha.year if fecha.month >= 8 else fecha.year - 1


def fechas_de_temporada(cli: espn.Espn, season: int) -> list[str]:
    """Fechas con partidos de la temporada según el calendario de ESPN."""
    data = cli.scoreboard(f"{season}-12-01")
    return espn.calendario(data)


def actualizar_calendario(con: duckdb.DuckDBPyConnection, cli: espn.Espn, desde: int, hasta: date,
                          tipos: tuple[int, ...] = (2, 3, 5)) -> int:
    """Guarda los partidos (y su estado) de cada fecha del calendario hasta `hasta` inclusive.
    Las fechas cuyos partidos ya están todos terminados en la base no se vuelven a pedir."""
    hechas = {r[0].isoformat() for r in con.execute(
        "SELECT fecha FROM games GROUP BY fecha HAVING bool_and(status = 'STATUS_FINAL')").fetchall()}
    vacias = {r[0] for r in con.execute(
        "SELECT replace(key, 'scoreboard:', '') FROM ingest_log WHERE source = 'espn' AND status = 'vacio'").fetchall()}
    nuevos = 0
    for season in range(desde, temporada_de(hasta) + 1):
        fechas = [f for f in fechas_de_temporada(cli, season) if f <= hasta.isoformat()]
        pendientes = [f for f in fechas if f not in hechas and f not in vacias]
        log.info("Temporada %d-%02d: %d fechas, %d por consultar", season, (season + 1) % 100, len(fechas), len(pendientes))
        for f in pendientes:
            partidos, equipos = espn.parse_scoreboard(cli.scoreboard(f), tipos)
            db.upsert(con, "teams", equipos)
            if not partidos:
                db.registrar(con, "espn", f"scoreboard:{f}", "vacio")
                continue
            # No pisar las marcas de descarga de partidos ya procesados.
            previos = {r[0]: (r[1], r[2]) for r in con.execute(
                "SELECT game_id, box_ok, pbp_ok FROM games WHERE fecha = ?", [f]).fetchall()}
            for p in partidos:
                p["box_ok"], p["pbp_ok"] = previos.get(p["game_id"], (False, False))
                p["updated_at"] = db.ahora_utc()
            nuevos += db.upsert(con, "games", partidos)
    return nuevos


def guardar_partido(con: duckdb.DuckDBPyConnection, summary: dict) -> dict:
    """Procesa un summary y escribe todas sus tablas en una transacción."""
    p = procesar(summary)
    game_id = str(summary["header"]["id"])
    con.execute("BEGIN")
    try:
        for tabla in ("player_games", "player_absences", "team_games", "plays", "player_periods", "stints",
                      "shots", "game_starts"):
            con.execute(f"DELETE FROM {tabla} WHERE game_id = ?", [game_id])
        db.insertar(con, "player_games", p.jugadores)
        db.insertar(con, "player_absences", p.ausencias)
        db.insertar(con, "team_games", p.equipos)
        db.insertar(con, "plays", p.jugadas)
        db.insertar(con, "player_periods", p.periodos)
        db.insertar(con, "stints", p.tramos)
        db.insertar(con, "shots", p.tiros)
        if p.inicio:
            db.insertar(con, "game_starts", [p.inicio])
        if p.lineas:
            db.upsert(con, "game_lines", [p.lineas])
        if p.control:
            db.upsert(con, "pbp_quality", [{"game_id": game_id, **p.control}])
        con.execute("UPDATE games SET box_ok = ?, pbp_ok = ?, updated_at = ? WHERE game_id = ?",
                    [bool(p.jugadores), bool(p.periodos), db.ahora_utc(), game_id])
        con.execute("COMMIT")
    except Exception:
        con.execute("ROLLBACK")
        raise
    return p.control


def descargar_partidos(con: duckdb.DuckDBPyConnection, cli: espn.Espn, limite: int | None = None,
                       reprocesar: bool = False) -> dict:
    """Descarga y procesa los partidos terminados que faltan (o todos con reprocesar=True, desde crudos/)."""
    filtro = "status = 'STATUS_FINAL'" + ("" if reprocesar else " AND NOT box_ok")
    ids = [r[0] for r in con.execute(f"SELECT game_id FROM games WHERE {filtro} ORDER BY start_utc").fetchall()]
    if limite:
        ids = ids[:limite]
    log.info("Partidos por procesar: %d", len(ids))
    ok = fallos = 0
    for i, gid in enumerate(ids, 1):
        try:
            guardar_partido(con, cli.summary(gid))
            db.registrar(con, "espn", f"summary:{gid}", "ok")
            ok += 1
        except Exception as e:  # un partido roto no debe parar la descarga
            fallos += 1
            log.exception("Partido %s: %s", gid, e)
            db.registrar(con, "espn", f"summary:{gid}", "error", str(e))
        if i % 100 == 0:
            log.info("  %d/%d partidos (%d errores)", i, len(ids), fallos)
    return {"ok": ok, "errores": fallos, "peticiones": cli.http.peticiones}


def guardar_lesiones(con: duckdb.DuckDBPyConnection, cli: espn.Espn) -> int:
    """Captura el parte de lesiones actual con la hora (UTC) de la captura."""
    filas = espn.parse_lesiones(cli.lesiones(), db.ahora_utc())
    return db.upsert(con, "injuries", filas)


def guardar_titulares_confirmados(con: duckdb.DuckDBPyConnection, cli: espn.Espn, fecha: str) -> int:
    """Para partidos del día ya empezados o terminados, guarda los titulares reales del box score.
    (Antes del salto ESPN no publica quintetos; ver README: carga manual por CSV.)"""
    filas = []
    ahora = db.ahora_utc()
    for (gid,) in con.execute("SELECT game_id FROM games WHERE fecha = ? AND status <> 'STATUS_SCHEDULED'",
                              [fecha]).fetchall():
        jugadores, _ = espn.parse_box(cli.summary(gid, cache=True))
        filas += [{"snapshot_at": ahora, "source": "espn", "game_id": gid, "team_id": j["team_id"],
                   "player_id": j["player_id"], "name": j["name"], "confirmed": True}
                  for j in jugadores if j["starter"]]
    return db.upsert(con, "lineups", filas)


def hoy_et() -> date:
    return datetime.now(espn.ET).date()


def ayer_et() -> date:
    return hoy_et() - timedelta(days=1)
