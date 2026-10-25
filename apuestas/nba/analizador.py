"""Une calendario, lesiones, líneas y modelo: evalúa cada prop del día y liquida las de días anteriores."""
from __future__ import annotations

import logging
from dataclasses import dataclass, field

from ..db import now_iso
from .db import NbaDB
from .modelo import (ESTADOS_FUERA, PESO_MERCADO, Contexto, Evaluacion, Jugador, construir_contexto, evaluar, mejor_contra,
                     preparar_jugador, valor)
from .sgo import clave_nombre, equipos_evento, parse_props

log = logging.getLogger(__name__)


@dataclass
class Partido:
    game: dict
    lesiones: list[dict] = field(default_factory=list)
    jugadores: dict[str, Jugador] = field(default_factory=dict)
    evaluaciones: list[Evaluacion] = field(default_factory=list)
    sin_datos: list[str] = field(default_factory=list)

    @property
    def titulo(self) -> str:
        return f"{self.game['away_name']} @ {self.game['home_name']}"


def emparejar_props(db: NbaDB, fecha: str, eventos: list[dict], ctx: Contexto) -> tuple[int, list[str]]:
    """Asigna cada evento de SportsGameOdds a su partido de ESPN y cada jugador a su id de ESPN."""
    juegos = {}
    for g in db.games_on(fecha):
        juegos[(clave_nombre(g["home_name"]), clave_nombre(g["away_name"]))] = g
        # Respaldo por apodo: ESPN dice "LA Clippers" y SportsGameOdds "Los Angeles Clippers".
        juegos[(clave_nombre(g["home_nick"]), clave_nombre(g["away_nick"]))] = g
    filas, sin_emparejar = [], []
    for ev in eventos:
        g = juegos.get(equipos_evento(ev)) or juegos.get(equipos_evento(ev, "medium"))
        if g is None:
            sin_emparejar.append(" vs ".join(equipos_evento(ev)))
            continue
        # Jugadores de los dos equipos según su último partido, por nombre normalizado.
        por_nombre: dict[str, str] = {}
        for pid, ps in ctx.por_jugador.items():
            if ps[0]["team_id"] in (g["home_id"], g["away_id"]):
                por_nombre.setdefault(clave_nombre(ps[0]["name"]), pid)
        for p in parse_props(ev):
            pid = por_nombre.get(clave_nombre(p["name"]))
            if pid is None:
                pid = _por_apellido(por_nombre, p["name"])
            if pid is None:
                sin_emparejar.append(p["name"])
                continue
            filas.append({**p, "game_id": g["id"], "player_id": pid})
    db.save_props(fecha, filas)
    db.commit()
    return len(filas), sorted(set(sin_emparejar))


def _por_apellido(por_nombre: dict[str, str], nombre: str) -> str | None:
    """Respaldo: misma inicial y mismo apellido (sin sufijos), si es único."""
    partes = [x for x in clave_nombre(nombre).split("_") if x not in ("JR", "SR", "II", "III", "IV")]
    if len(partes) < 2:
        return None
    hits = [pid for k, pid in por_nombre.items()
            if (q := [x for x in k.split("_") if x not in ("JR", "SR", "II", "III", "IV")])
            and q[-1] == partes[-1] and q[0][:1] == partes[0][:1]]
    return hits[0] if len(hits) == 1 else None


def analizar(db: NbaDB, fecha: str, min_partidos: int = 8, min_minutos: float = 12.0,
             peso_mercado: float = PESO_MERCADO) -> tuple[list[Partido], Contexto]:
    ctx = construir_contexto(db.conn, fecha)
    lesiones = [dict(r) for r in db.injuries(fecha)]
    props_por_juego: dict[str, list[dict]] = {}
    for r in db.props(fecha):
        props_por_juego.setdefault(r["game_id"], []).append(dict(r))
    partidos = []
    for g in db.games_on(fecha):
        g = dict(g)
        part = Partido(g, [l for l in lesiones if l["team_id"] in (g["home_id"], g["away_id"])])
        estado = {l["player_id"]: l["status"].lower() for l in part.lesiones}
        for prop in props_por_juego.get(g["id"], []):
            pid = prop["player_id"]
            if estado.get(pid, "") in ESTADOS_FUERA:
                continue
            j = part.jugadores.get(pid)
            if j is None and pid not in part.sin_datos:
                hist = ctx.por_jugador.get(pid, [])
                if not hist:
                    part.sin_datos.append(pid)
                    continue
                team = hist[0]["team_id"] if hist[0]["team_id"] in (g["home_id"], g["away_id"]) else None
                team = team or g["home_id"]
                opp = g["away_id"] if team == g["home_id"] else g["home_id"]
                ausentes = [(l["player_id"], l["name"]) for l in part.lesiones
                            if l["team_id"] == team and l["status"].lower() in ESTADOS_FUERA]
                j = preparar_jugador(ctx, pid, hist[0]["name"], team, opp, ausentes)
                if estado.get(pid):
                    j.notas.insert(0, f"en el parte de lesiones: {estado[pid]}")
                if j.n < min_partidos or j.minutos < min_minutos:
                    part.sin_datos.append(pid)
                    continue
                part.jugadores[pid] = j
            if j is None:
                continue
            part.evaluaciones.append(evaluar(ctx, j, prop["stat"], prop["line"], prop["over_odd"],
                                                   prop["under_odd"], peso_mercado))
        part.evaluaciones.sort(key=lambda e: e.prob, reverse=True)
        partidos.append(part)
    return partidos, ctx


def mejores(partidos: list[Partido], prob_min: float) -> list[tuple[Partido, Evaluacion]]:
    out = [(p, e) for p in partidos for e in p.evaluaciones if e.prob >= prob_min]
    return sorted(out, key=lambda x: x[1].prob, reverse=True)


def guardar_picks(db: NbaDB, fecha: str, picks: list[tuple[Partido, Evaluacion]]) -> None:
    db.conn.execute("DELETE FROM nba_picks WHERE fecha = ? AND result IS NULL", (fecha,))
    db.conn.executemany(
        """INSERT OR REPLACE INTO nba_picks(fecha, game_id, player_id, name, stat, line, side, prob, mu, odd,
               created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        [(fecha, p.game["id"], e.player_id, e.nombre, e.stat, e.line, e.lado, e.prob, e.mu, e.odd, now_iso())
         for p, e in picks],
    )
    db.commit()


# --- Liquidación y rendimiento --------------------------------------------------------

def liquidar(db: NbaDB) -> int:
    """result: 1 acierto, 0 fallo, 2 anulada (no jugó o empate exacto con la línea)."""
    n = 0
    pendientes = db.conn.execute(
        """SELECT p.* FROM nba_picks p JOIN nba_games g ON g.id = p.game_id
           WHERE p.result IS NULL AND g.box_ok = 1""").fetchall()
    for pk in pendientes:
        fila = db.conn.execute("SELECT * FROM nba_player_games WHERE game_id = ? AND player_id = ?",
                               (pk["game_id"], pk["player_id"])).fetchone()
        if fila is None:
            actual, res = None, 2
        else:
            actual = valor(dict(fila), pk["stat"])
            if actual == pk["line"]:
                res = 2
            else:
                res = int((actual > pk["line"]) == (pk["side"] == "más"))
        db.conn.execute("UPDATE nba_picks SET actual = ?, result = ? WHERE id = ?", (actual, res, pk["id"]))
        n += 1
    db.commit()
    return n


TRAMOS = ((0.0, 0.65), (0.65, 0.70), (0.70, 0.75), (0.75, 0.80), (0.80, 0.85), (0.85, 1.01))


def rendimiento(db: NbaDB) -> dict:
    filas = db.conn.execute("SELECT * FROM nba_picks WHERE result IN (0, 1)").fetchall()

    def resumen(grupo):
        n = len(grupo)
        con_cuota = [r for r in grupo if r["odd"]]
        return {
            "n": n, "acierto": sum(r["result"] for r in grupo) / n, "prob_media": sum(r["prob"] for r in grupo) / n,
            "beneficio": sum((r["odd"] - 1) if r["result"] else -1 for r in con_cuota) if con_cuota else None,
            "con_cuota": len(con_cuota),
        }

    tramos = []
    for lo, hi in TRAMOS:
        g = [r for r in filas if lo <= r["prob"] < hi]
        if g:
            tramos.append({"tramo": f"{lo * 100:.0f}-{min(hi, 1) * 100:.0f}%", **resumen(g)})
    por_stat = {}
    for r in filas:
        por_stat.setdefault(r["stat"], []).append(r)
    return {"total": resumen(filas) if filas else None, "tramos": tramos,
            "stats": sorted(({"stat": k, **resumen(v)} for k, v in por_stat.items()), key=lambda x: -x["n"])}
