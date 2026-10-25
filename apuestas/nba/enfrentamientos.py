"""Descarga de stats.nba.com a la base y emparejamiento con los partidos y jugadores de ESPN."""
from __future__ import annotations

import logging
from datetime import date, timedelta

from ..api_football import ApiError
from ..db import now_iso
from .analizador import _por_apellido
from .db import NbaDB
from .nbastats import NbaStats, parse_enfrentamientos
from .sgo import clave_nombre

log = logging.getLogger(__name__)


def _partido_espn(db: NbaDB, fecha: str, equipos: list[str]) -> str | None:
    """Partido de ESPN del mismo día (±1 por husos horarios) con los mismos equipos."""
    claves = {clave_nombre(e) for e in equipos}
    apodos = {clave_nombre(e).split("_")[-1] for e in equipos}
    dia = date.fromisoformat(fecha)
    for f in (dia, dia - timedelta(days=1), dia + timedelta(days=1)):
        for g in db.games_on(f.isoformat()):
            if {clave_nombre(g["home_name"]), clave_nombre(g["away_name"])} == claves:
                return g["id"]
            if {clave_nombre(g["home_nick"]).split("_")[-1], clave_nombre(g["away_nick"]).split("_")[-1]} == apodos:
                return g["id"]
    return None


def _jugadores_partido(db: NbaDB, game_id: str) -> dict[str, tuple[str, str]]:
    """Nombre normalizado -> (id de ESPN, equipo) de quienes jugaron ese partido."""
    return {clave_nombre(r["name"]): (r["player_id"], r["team_id"]) for r in db.conn.execute(
        "SELECT player_id, team_id, name FROM nba_player_games WHERE game_id = ?", (game_id,))}


def emparejar_filas(db: NbaDB, game_id: str | None, filas: list[dict]) -> list[dict]:
    jugadores = _jugadores_partido(db, game_id) if game_id else {}
    por_nombre = {k: v[0] for k, v in jugadores.items()}
    equipo = {pid: team for pid, team in jugadores.values()}
    equipos = set(equipo.values())

    def buscar(nombre: str) -> str | None:
        return por_nombre.get(clave_nombre(nombre)) or _por_apellido(por_nombre, nombre)

    out = []
    for f in filas:
        off, dfn = buscar(f["off_name"]), buscar(f["def_name"])
        off_team = equipo.get(off) if off else None
        def_team = equipo.get(dfn) if dfn else None
        if off_team and not def_team:
            def_team = next((t for t in equipos if t != off_team), None)
        if def_team and not off_team:
            off_team = next((t for t in equipos if t != def_team), None)
        out.append({**f, "game_id": game_id, "off_player_id": off, "def_player_id": dfn,
                    "off_team_id": off_team, "def_team_id": def_team})
    return out


def guardar_enfrentamientos(db: NbaDB, nba_game_id: str, fecha: str, season: int, season_type: int,
                            game_id: str | None, filas: list[dict]) -> None:
    db.conn.execute("DELETE FROM nba_matchups WHERE nba_game_id = ?", (nba_game_id,))
    db.conn.executemany(
        """INSERT OR REPLACE INTO nba_matchups(nba_game_id, game_id, off_nba_id, def_nba_id, off_player_id,
               def_player_id, off_team_id, def_team_id, off_name, def_name, minutos, posesiones, pts, fgm, fga,
               tpm, tpa, ftm, ast, tov, blk)
           VALUES (:nba_game_id, :game_id, :off_nba_id, :def_nba_id, :off_player_id, :def_player_id, :off_team_id,
                   :def_team_id, :off_name, :def_name, :minutos, :posesiones, :pts, :fgm, :fga, :tpm, :tpa, :ftm,
                   :ast, :tov, :blk)""",
        [{**f, "nba_game_id": nba_game_id} for f in filas])
    db.conn.execute(
        """INSERT OR REPLACE INTO nba_stats_games(nba_game_id, fecha, season, season_type, game_id, filas, updated_at)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (nba_game_id, fecha, season, season_type, game_id, len(filas), now_iso()))
    db.commit()


def descargar_temporada(ns: NbaStats, db: NbaDB, season: int, season_type: int = 2,
                        hasta: str | None = None, maximo: int | None = None) -> dict:
    """Descarga los enfrentamientos de los partidos jugados que aún no están en la base."""
    partidos: dict[str, dict] = {}
    for r in ns.partidos(season, season_type):
        g = partidos.setdefault(str(r["GAME_ID"]), {"fecha": str(r["GAME_DATE"])[:10], "equipos": []})
        g["equipos"].append(r["TEAM_NAME"])
    hechos = {r[0] for r in db.conn.execute("SELECT nba_game_id FROM nba_stats_games WHERE filas > 0")}
    pendientes = sorted((gid for gid, g in partidos.items()
                         if gid not in hechos and (not hasta or g["fecha"] <= hasta)),
                        key=lambda gid: partidos[gid]["fecha"])
    if maximo:
        pendientes = pendientes[:maximo]
    n = {"partidos": len(partidos), "nuevos": 0, "sin_espn": 0, "sin_datos": 0, "jugadores_sin_emparejar": 0}
    for i, gid in enumerate(pendientes, 1):
        g = partidos[gid]
        try:
            filas = parse_enfrentamientos(ns.enfrentamientos(gid))
        except ApiError as e:
            log.warning("%s %s: %s", g["fecha"], gid, e)
            n["sin_datos"] += 1
            continue
        game_id = _partido_espn(db, g["fecha"], g["equipos"])
        if not filas:
            n["sin_datos"] += 1
        if game_id is None:
            n["sin_espn"] += 1
        filas = emparejar_filas(db, game_id, filas)
        n["jugadores_sin_emparejar"] += sum(1 for f in filas if not f["off_player_id"] or not f["def_player_id"])
        guardar_enfrentamientos(db, gid, g["fecha"], season, season_type, game_id, filas)
        n["nuevos"] += bool(filas)
        if i % 25 == 0:
            log.info("%d/%d partidos de stats.nba.com (%s)", i, len(pendientes), g["fecha"])
    return n


def descargar_avanzadas(ns: NbaStats, db: NbaDB, season: int, season_type: int = 2) -> int:
    por_nombre = {clave_nombre(r["name"]): r["player_id"]
                  for r in db.conn.execute("SELECT DISTINCT player_id, name FROM nba_player_games")}
    filas = []
    for r in ns.avanzadas(season, season_type):
        filas.append((season, season_type, r["PLAYER_ID"], por_nombre.get(clave_nombre(r["PLAYER_NAME"])),
                      r["PLAYER_NAME"], r.get("TEAM_ABBREVIATION"), r.get("GP"), r.get("MIN"), r.get("USG_PCT"),
                      r.get("TS_PCT"), r.get("AST_PCT"), r.get("OREB_PCT"), r.get("DREB_PCT"), r.get("REB_PCT"),
                      r.get("TM_TOV_PCT"), r.get("PACE"), r.get("PIE")))
    db.conn.executemany(
        """INSERT OR REPLACE INTO nba_avanzadas(season, season_type, nba_id, player_id, name, team_abbr, gp, minutos,
               usg_pct, ts_pct, ast_pct, oreb_pct, dreb_pct, reb_pct, tov_pct, pace, pie)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", filas)
    db.commit()
    return len(filas)
