"""Las apuestas que arma el usuario (de prueba o reales) se siguen como las combinadas del sistema.

Cada día va en apuestas_usuario/AAAA-MM-DD.json:

    {"fecha": "2026-10-29", "apuestas": [
        {"nombre": "Doble de bet builders", "cuota": 8.54, "prob": 0.165, "real": false,
         "patas": [{"jugador": "Jaylen Wells", "stat": "points", "lado": "más", "linea": 9.5}, ...]}]}

"linea" es la de la casa: "10+" es más de 9.5. "prob" es la que daba el modelo al armarla. Se registran como
combinadas de tipo "usuario:<nombre>" la primera vez que los partidos están en la base (si un jugador no se
encuentra, se reintenta al día siguiente) y se liquidan solas con las demás.
"""
from __future__ import annotations

import json
import logging
from pathlib import Path

from ..config import ROOT
from ..db import now_iso
from .db import NbaDB
from .modelo import COMPONENTES
from .sgo import clave_nombre

log = logging.getLogger("apuestas")
DIR = ROOT / "apuestas_usuario"
PREFIJO = "usuario:"


def _jugadores(db: NbaDB, fecha: str) -> dict[str, tuple[str, str, str]]:
    """Nombre normalizado -> (player_id, equipo de su último partido, nombre en ESPN)."""
    out: dict[str, tuple[str, str, str]] = {}
    for r in db.conn.execute(
            """SELECT pg.player_id, pg.team_id, pg.name FROM nba_player_games pg JOIN nba_games g ON g.id = pg.game_id
               WHERE g.fecha <= ? ORDER BY g.fecha DESC""", (fecha,)):
        out.setdefault(clave_nombre(r["name"]), (r["player_id"], r["team_id"], r["name"]))
    return out


def registrar(db: NbaDB, carpeta: Path = DIR) -> int:
    n = 0
    for fichero in sorted(carpeta.glob("*.json")):
        datos = json.loads(fichero.read_text(encoding="utf-8"))
        fecha = datos["fecha"]
        juegos = {}
        for g in db.games_on(fecha):
            titulo = f"{g['away_name']} @ {g['home_name']}"
            juegos[g["home_id"]] = juegos[g["away_id"]] = (g["id"], titulo)
        if not juegos:
            continue
        jugadores = _jugadores(db, fecha)
        for ap in datos["apuestas"]:
            tipo = PREFIJO + ap["nombre"]
            if db.conn.execute("SELECT 1 FROM nba_combinadas WHERE fecha = ? AND tipo = ?", (fecha, tipo)).fetchone():
                continue
            patas = []
            for p in ap["patas"]:
                info = jugadores.get(clave_nombre(p["jugador"]))
                if info is None or info[1] not in juegos or p["stat"] not in COMPONENTES:
                    log.warning("%s, %s: no encuentro %s (%s) en los partidos del día", fecha, ap["nombre"],
                                p["jugador"], p["stat"])
                    break
                game_id, titulo = juegos[info[1]]
                patas.append({"game_id": game_id, "partido": titulo, "player_id": info[0], "nombre": info[2],
                              "stat": p["stat"], "line": float(p["linea"]), "side": p["lado"], "prob": p.get("prob"),
                              "odd": None})
            else:
                db.conn.execute("""INSERT INTO nba_combinadas(fecha, tipo, patas, prob, cuota, created_at)
                                   VALUES (?, ?, ?, ?, ?, ?)""",
                                (fecha, tipo, json.dumps(patas, ensure_ascii=False), ap["prob"], ap.get("cuota"),
                                 now_iso()))
                n += 1
    db.commit()
    return n
