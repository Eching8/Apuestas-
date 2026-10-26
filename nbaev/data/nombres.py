"""Emparejamiento de jugadores de otras fuentes con los ids de ESPN por nombre normalizado."""
from __future__ import annotations

import difflib
import re
import unicodedata
from datetime import datetime

import duckdb

from . import db

SUFIJOS = {"JR", "SR", "II", "III", "IV", "V"}


def clave_nombre(nombre: str) -> str:
    """'Jaren Jackson Jr.' -> 'JAREN_JACKSON_JR'; 'Nikola Jokić' -> 'NIKOLA_JOKIC'."""
    s = unicodedata.normalize("NFKD", nombre or "").encode("ascii", "ignore").decode().upper()
    s = re.sub(r"[.'’]", "", s)
    return re.sub(r"[^A-Z0-9]+", "_", s).strip("_")


def sin_sufijo(clave: str) -> str:
    partes = clave.split("_")
    while len(partes) > 2 and partes[-1] in SUFIJOS:
        partes.pop()
    return "_".join(partes)


def _apellido_inicial(clave: str) -> tuple[str, str] | None:
    partes = sin_sufijo(clave).split("_")
    return (partes[-1], partes[0][:1]) if len(partes) >= 2 else None


def candidatos(con: duckdb.DuckDBPyConnection, equipos: list[str], fecha: datetime) -> dict[str, tuple[str, str]]:
    """clave de nombre -> (player_id, team_id) de los jugadores de esos equipos alrededor de `fecha`
    (box scores y ausencias ±90 días, parte de lesiones y alineaciones). Si un jugador aparece en
    varios equipos se queda el registro más cercano a la fecha (traspasos)."""
    filas = con.execute("""
        WITH cerca AS (
            SELECT p.player_id, p.name, p.team_id, g.start_utc AS t FROM player_games p JOIN games g USING (game_id)
            WHERE g.start_utc BETWEEN ? - INTERVAL 90 DAY AND ? + INTERVAL 90 DAY
            UNION ALL SELECT a.player_id, a.name, a.team_id, g.start_utc FROM player_absences a JOIN games g USING (game_id)
            WHERE g.start_utc BETWEEN ? - INTERVAL 90 DAY AND ? + INTERVAL 90 DAY
            UNION ALL SELECT player_id, name, team_id, snapshot_at FROM injuries
            WHERE snapshot_at BETWEEN ? - INTERVAL 90 DAY AND ? + INTERVAL 1 DAY
            UNION ALL SELECT player_id, name, team_id, snapshot_at FROM lineups
            WHERE snapshot_at BETWEEN ? - INTERVAL 90 DAY AND ? + INTERVAL 1 DAY
        )
        SELECT player_id, arg_min(name, abs(epoch(t) - epoch(?::TIMESTAMP))),
               arg_min(team_id, abs(epoch(t) - epoch(?::TIMESTAMP)))
        FROM cerca GROUP BY player_id""", [fecha] * 10).fetchall()
    out: dict[str, tuple[str, str]] = {}
    for pid, nombre, team in filas:
        if team in equipos:
            out[clave_nombre(nombre)] = (pid, team)
    return out


def emparejar_jugadores(con: duckdb.DuckDBPyConnection, fuente: str, nombres: dict[str, str],
                        equipos: list[str], fecha: datetime) -> dict[str, tuple[str | None, str | None]]:
    """{id de la fuente: nombre} -> {id de la fuente: (player_id de ESPN, team_id)} para un partido en `fecha`."""
    cand = candidatos(con, equipos, fecha)
    por_id = {v[0]: v for v in cand.values()}
    sin_suf = {}
    for k, v in cand.items():
        sin_suf.setdefault(sin_sufijo(k), []).append(v)
    out, nuevos = {}, []
    for sid, nombre in nombres.items():
        previo = con.execute("SELECT player_id FROM player_map WHERE source = ? AND source_player_id = ?",
                             [fuente, sid]).fetchone()
        if previo and previo[0] in por_id:
            out[sid] = por_id[previo[0]]
            continue
        k = clave_nombre(nombre)
        metodo, hallado = None, None
        if k in cand:
            metodo, hallado = "exacto", cand[k]
        elif len(sin_suf.get(sin_sufijo(k), [])) == 1:
            metodo, hallado = "sin_sufijo", sin_suf[sin_sufijo(k)][0]
        else:
            parecidos = difflib.get_close_matches(k, list(cand), n=2, cutoff=0.86)
            if len(parecidos) == 1:
                metodo, hallado = "aproximado", cand[parecidos[0]]
            else:
                # Apodos ("Ron Holland" / "Ronald Holland II"): mismo apellido e inicial, único en el partido.
                firma = _apellido_inicial(k)
                iguales = [v for c, v in cand.items() if _apellido_inicial(c) == firma]
                if firma and len(iguales) == 1:
                    metodo, hallado = "apellido_inicial", iguales[0]
        out[sid] = hallado or (None, None)
        if hallado:
            nuevos.append({"source": fuente, "source_player_id": sid, "player_id": hallado[0], "name": nombre,
                           "metodo": metodo})
    db.upsert(con, "player_map", nuevos)
    return out
