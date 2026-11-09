"""Las apuestas de la NHL que arma el usuario se siguen como las combinadas del sistema.

Cada día va en apuestas_usuario/nhl/AAAA-MM-DD.json (mismo formato que la NBA):

    {"fecha": "2026-11-08", "apuestas": [
        {"nombre": "Segura cuota 2", "cuota": 2.10, "prob": 0.50, "real": false,
         "patas": [{"jugador": "Nathan MacKinnon", "stat": "shots", "lado": "más", "linea": 3.5}, ...]}]}

stat: shots, points, goals, assists, blocked, hits o saves. "linea" es la de la casa: "4+" es más de 3.5. Las de
dinero real llevan "real": true y, si se quiere, "apostado" y "moneda". Se registran como combinadas de tipo
"usuario:<nombre>" en cuanto los partidos están en la base y se liquidan solas con las demás.
"""
from __future__ import annotations

import json
import logging
from pathlib import Path

from ..config import ROOT
from ..db import now_iso
from ..nba.sgo import clave_nombre
from .db import NhlDB
from .modelo import COMPONENTES

log = logging.getLogger("apuestas")
DIR = ROOT / "apuestas_usuario" / "nhl"
PREFIJO = "usuario:"


def _jugadores(db: NhlDB, fecha: str) -> dict[str, tuple[str, str, str]]:
    out: dict[str, tuple[str, str, str]] = {}
    for tabla in ("nhl_player_games", "nhl_goalie_games"):
        for r in db.conn.execute(
                f"""SELECT t.player_id, t.team_id, t.name FROM {tabla} t JOIN nhl_games g ON g.id = t.game_id
                    WHERE g.fecha <= ? ORDER BY g.fecha DESC""", (fecha,)):
            out.setdefault(clave_nombre(r["name"]), (r["player_id"], r["team_id"], r["name"]))
    return out


def registrar(db: NhlDB, carpeta: Path = DIR) -> int:
    n = 0
    if not carpeta.exists():
        return 0
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
            if db.conn.execute("SELECT 1 FROM nhl_combinadas WHERE fecha = ? AND tipo = ?", (fecha, tipo)).fetchone():
                continue
            patas = []
            for p in ap["patas"]:
                info = jugadores.get(clave_nombre(p["jugador"]))
                if info is None or info[1] not in juegos or p["stat"] not in COMPONENTES:
                    log.warning("NHL %s, %s: no encuentro %s (%s) en los partidos del día", fecha, ap["nombre"],
                                p["jugador"], p["stat"])
                    break
                game_id, titulo = juegos[info[1]]
                patas.append({"game_id": game_id, "partido": titulo, "player_id": info[0], "nombre": info[2],
                              "stat": p["stat"], "line": float(p["linea"]), "side": p["lado"], "prob": p.get("prob"),
                              "odd": None})
            else:
                db.conn.execute("""INSERT INTO nhl_combinadas(fecha, tipo, patas, prob, cuota, created_at)
                                   VALUES (?, ?, ?, ?, ?, ?)""",
                                (fecha, tipo, json.dumps(patas, ensure_ascii=False), ap.get("prob") or 0.0,
                                 ap.get("cuota"), now_iso()))
                n += 1
    db.commit()
    return n
