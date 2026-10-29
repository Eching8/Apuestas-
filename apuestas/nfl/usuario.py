"""Las apuestas que arma el usuario en su casa (de prueba o reales) se siguen como las combinadas del sistema.

Cada día va en apuestas_usuario/nfl/AAAA-MM-DD.json (aparte de las de la NBA, en apuestas_usuario/):

    {"fecha": "2026-10-29", "apuestas": [
        {"nombre": "Base 5.80", "cuota": 5.80, "prob": 0.20, "real": false,
         "patas": [{"jugador": "Bryce Young", "stat": "rush_yds", "lado": "menos", "linea": 8.5}, ...]}]}

"linea" es la de la casa ("1+" es más de 0.5). "stat" usa los nombres del modelo (rec, rec_yds, rush_yds,
pass_tds...); "equipo" es opcional y desempata nombres repetidos. Las patas pueden ser de cualquier partido de los 7 días desde "fecha" (una combinada armada el
jueves con partidos del domingo y el lunes). Se registran como combinadas "usuario:<nombre>" cuando el partido
está en la base y se liquidan solas con las demás.
"""
from __future__ import annotations

import json
import logging
from datetime import date, timedelta
from pathlib import Path

from ..config import ROOT
from ..db import now_iso
from ..nba.sgo import clave_nombre
from . import equipos
from .db import NflDB
from .modelo import NOMBRES, STATS_POR_POSICION

log = logging.getLogger("apuestas")
DIR = ROOT / "apuestas_usuario" / "nfl"
PREFIJO = "usuario:"
DIAS_VENTANA = 7


def registrar(db: NflDB, carpeta: Path = DIR) -> int:
    n = 0
    if not carpeta.exists():
        return 0
    for fichero in sorted(carpeta.glob("*.json")):
        datos = json.loads(fichero.read_text(encoding="utf-8"))
        fecha = datos["fecha"]
        hasta = (date.fromisoformat(fecha) + timedelta(days=DIAS_VENTANA - 1)).isoformat()
        juegos = {}
        for g in db.conn.execute("SELECT * FROM nfl_games WHERE gameday BETWEEN ? AND ? ORDER BY gameday",
                                 (fecha, hasta)):
            titulo = f"{g['away_team']} @ {g['home_team']}"
            for team in (g["home_team"], g["away_team"]):
                juegos.setdefault(team, (g["game_id"], titulo))      # el primer partido de cada equipo
        if not juegos:
            continue
        nombres: dict[str, list[tuple]] = {}
        for r in db.conn.execute("SELECT player_id, name, team, position FROM nfl_rosters"):
            nombres.setdefault(clave_nombre(r["name"] or ""), []).append(
                (r["player_id"], r["team"], r["name"], r["position"]))
        for ap in datos["apuestas"]:
            tipo = PREFIJO + ap["nombre"]
            if db.conn.execute("SELECT 1 FROM nfl_combinadas WHERE fecha = ? AND tipo = ?", (fecha, tipo)).fetchone():
                continue
            patas = []
            for p in ap["patas"]:
                info = _elegir(nombres.get(clave_nombre(p["jugador"]), []), p, juegos)
                if info is None or info[1] not in juegos or p["stat"] not in NOMBRES:
                    log.warning("%s, %s: no encuentro %s (%s) en los partidos de la semana", fecha, ap["nombre"],
                                p["jugador"], p["stat"])
                    break
                game_id, titulo = juegos[info[1]]
                patas.append({"game_id": game_id, "partido": titulo, "player_id": info[0], "nombre": info[2],
                              "team": info[1], "stat": p["stat"], "line": float(p["linea"]), "side": p["lado"],
                              "prob": p.get("prob"), "odd": None})
            else:
                db.conn.execute("INSERT INTO nfl_combinadas(fecha, tipo, patas, prob, cuota, created_at) "
                                "VALUES (?, ?, ?, ?, ?, ?)",
                                (fecha, tipo, json.dumps(patas, ensure_ascii=False), ap["prob"], ap.get("cuota"),
                                 now_iso()))
                n += 1
    db.commit()
    return n


def _elegir(candidatos: list[tuple], pata: dict, juegos: dict) -> tuple | None:
    """Entre jugadores con el mismo nombre (Justin Jefferson de MIN y el LB de CLE), el del equipo indicado, que
    juegue esa semana y cuya posición tenga la estadística."""
    if pata.get("equipo"):
        candidatos = [c for c in candidatos if c[1] == equipos.por_texto(pata["equipo"])]
    candidatos = [c for c in candidatos if c[1] in juegos]
    return max(candidatos, key=lambda c: pata["stat"] in STATS_POR_POSICION.get(c[3], ()), default=None)
