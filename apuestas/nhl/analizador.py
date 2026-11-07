"""Une calendario, lesiones, porteros probables, líneas y modelo: evalúa cada prop del día y liquida las anteriores.

Sin líneas de la casa (The Odds API solo con ODDS_API_NHL=1, para no gastar los créditos de la NBA), cada jugador
de papel principal se evalúa a la línea que pondría la casa (`modelo.linea_estimada`) y la combinada sale con cuota
estimada: el usuario manda las cuotas de Betano y se evalúan esas exactas.
"""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from datetime import date, timedelta

from ..db import now_iso
from ..nba.sgo import clave_nombre
from .db import NhlDB
from .modelo import (ESTADOS_FUERA, PESO_MERCADO, PROB_SEGURA, Contexto, Evaluacion, Jugador, Segura,
                     construir_contexto, evaluar, linea_estimada, predecir, preparar_jugador, preparar_portero,
                     seguras, valor)

log = logging.getLogger(__name__)

STATS_ESTIMADAS = ("shots", "points", "assists", "blocked")
# Margen típico de Betano en props de la NHL: con una línea estimada, la cuota estimada es la justa / MARGEN_CASA.
MARGEN_CASA = 1.08


@dataclass
class Partido:
    game: dict
    lesiones: list[dict] = field(default_factory=list)
    jugadores: dict[str, Jugador] = field(default_factory=dict)
    evaluaciones: list[Evaluacion] = field(default_factory=list)
    sin_datos: list[str] = field(default_factory=list)
    seguras: list[Segura] = field(default_factory=list)

    @property
    def titulo(self) -> str:
        return f"{self.game['away_name']} @ {self.game['home_name']}"


def fuera(estado: str) -> bool:
    estado = (estado or "").lower()
    return any(e in estado for e in ESTADOS_FUERA)


def _es_equipo(clave: str, nombre: str, apodo: str) -> bool:
    n, a = clave_nombre(nombre), clave_nombre(apodo)
    return bool(clave) and (clave in (n, a) or clave.endswith("_" + a))


def emparejar_props(db: NhlDB, fecha: str, eventos: list[dict], ctx: Contexto) -> tuple[int, list[str]]:
    """Eventos ya normalizados ({"equipos": [(local, visitante)], "props": [...]}) -> líneas por jugador de ESPN."""
    juegos = db.games_on(fecha)
    filas, sin_emparejar = [], []
    for ev in eventos:
        g = next((g for local, visita in ev["equipos"] for g in juegos
                  if _es_equipo(local, g["home_name"], g["home_nick"])
                  and _es_equipo(visita, g["away_name"], g["away_nick"])), None)
        if g is None:
            sin_emparejar.append(" vs ".join(ev["equipos"][0]))
            continue
        por_nombre: dict[str, str] = {}
        for pid, ps in list(ctx.por_jugador.items()) + list(ctx.porteros.items()):
            if ps[0]["team_id"] in (g["home_id"], g["away_id"]):
                por_nombre.setdefault(clave_nombre(ps[0]["name"]), pid)
        for p in ev["props"]:
            pid = por_nombre.get(clave_nombre(p["name"]))
            if pid is None:
                sin_emparejar.append(p["name"])
                continue
            filas.append({**p, "game_id": g["id"], "player_id": pid})
    db.save_props(fecha, filas)
    db.commit()
    return len(filas), sorted(set(sin_emparejar))


def analizar(db: NhlDB, fecha: str, min_partidos: int = 8, min_minutos: float = 10.0,
             peso_mercado: float = PESO_MERCADO, prob_segura: float = PROB_SEGURA) -> tuple[list[Partido], Contexto]:
    ctx = construir_contexto(db.conn, fecha)
    lesiones = [dict(r) for r in db.injuries(fecha)]
    props_por_juego: dict[str, list[dict]] = {}
    for r in db.props(fecha):
        props_por_juego.setdefault(r["game_id"], []).append(dict(r))
    partidos = []
    hace_3_semanas = (date.fromisoformat(fecha) - timedelta(days=21)).isoformat()
    for g in db.games_on(fecha):
        g = dict(g)
        part = Partido(g, [l for l in lesiones if l["team_id"] in (g["home_id"], g["away_id"])])
        estado = {l["player_id"]: l["status"] for l in part.lesiones}

        def jugador(pid: str) -> Jugador | None:
            if pid in part.jugadores:
                return part.jugadores[pid]
            if pid in part.sin_datos or fuera(estado.get(pid, "")):
                return None
            portero = pid in ctx.porteros and pid not in ctx.por_jugador
            hist = (ctx.porteros if portero else ctx.por_jugador).get(pid, [])
            if not hist:
                part.sin_datos.append(pid)
                return None
            team = hist[0]["team_id"] if hist[0]["team_id"] in (g["home_id"], g["away_id"]) else g["home_id"]
            opp = g["away_id"] if team == g["home_id"] else g["home_id"]
            if portero:
                j = preparar_portero(ctx, pid, hist[0]["name"], team, opp)
            else:
                ausentes = [l["player_id"] for l in part.lesiones if l["team_id"] == team and fuera(l["status"])]
                fuera_rival = [l["player_id"] for l in part.lesiones if l["team_id"] == opp and fuera(l["status"])]
                j = preparar_jugador(ctx, pid, hist[0]["name"], team, opp, ausentes, fuera_rival)
            if j is None:
                part.sin_datos.append(pid)
                return None
            if estado.get(pid):
                j.notas.insert(0, f"en el parte de lesiones: {estado[pid].lower()}")
            if j.n < min_partidos or (not j.es_portero and j.minutos < min_minutos):
                part.sin_datos.append(pid)
                return None
            part.jugadores[pid] = j
            return j

        con_linea = set()
        for prop in props_por_juego.get(g["id"], []):
            j = jugador(prop["player_id"])
            if j is not None and (prop["stat"] == "saves") == j.es_portero:
                part.evaluaciones.append(evaluar(ctx, j, prop["stat"], prop["line"], prop["over_odd"],
                                                 prop["under_odd"], peso_mercado))
                con_linea.add((prop["player_id"], prop["stat"]))
        for pid, hist in ctx.por_jugador.items():
            if (hist[0]["team_id"] in (g["home_id"], g["away_id"]) and hist[0]["season"] == ctx.temporada
                    and hist[0]["fecha"] >= hace_3_semanas):
                jugador(pid)
        # Porteros: solo el titular probable de hoy (ESPN).
        for team in (g["home_id"], g["away_id"]):
            pid = ctx.portero_hoy.get(team)
            if pid and pid in ctx.porteros:
                jugador(pid)
        # Sin línea de la casa: la que pondría la casa, para los de papel principal.
        for j in part.jugadores.values():
            for stat in (("saves",) if j.es_portero else STATS_ESTIMADAS):
                if (j.player_id, stat) in con_linea:
                    continue
                if stat == "blocked" and j.grupo != "D":
                    continue
                pred = predecir(ctx, j, stat)
                line = linea_estimada(j, stat, pred.mu)
                part.evaluaciones.append(evaluar(ctx, j, stat, line, peso_mercado=peso_mercado, estimada=True))
        part.evaluaciones.sort(key=lambda e: e.prob, reverse=True)
        principales = {(e.player_id, e.stat): e.line for e in part.evaluaciones if not e.estimada}
        for j in part.jugadores.values():
            part.seguras += seguras(ctx, j, prob_segura, principales)
        part.seguras.sort(key=lambda s: (s.prob, s.line), reverse=True)
        partidos.append(part)
    return partidos, ctx


def cuota(e: Evaluacion) -> float:
    """La de la casa o, con línea estimada, la justa menos el margen típico de Betano."""
    return e.odd if e.odd else 1 / e.prob / MARGEN_CASA


# "Menos" de producción (tiros, puntos, goles, asistencias): exigencia de la NBA hasta medirlos con líneas reales.
STATS_ANOTACION = {"shots", "points", "goals", "assists"}
MENOS_ANOTACION_PROB = 0.75
MENOS_ANOTACION_ACIERTOS = 8


def menos_aceptable(e: Evaluacion) -> bool:
    if e.lado != "menos" or e.stat not in STATS_ANOTACION:
        return True
    return e.prob >= MENOS_ANOTACION_PROB and e.acierto_10[0] >= MENOS_ANOTACION_ACIERTOS


def candidatas_seguras(partidos: list[Partido], cuota_min: float = 1.30, prob_min: float = 0.62,
                       min_aciertos: int = 7) -> list[tuple[Partido, Evaluacion]]:
    """Props ordenadas por probabilidad, solo de jugadores constantes: papel principal con tiempo en hielo estable,
    sin cambio de línea ni de unidad de PP, traspaso ni lesión, que la pasaron en 7+ de sus últimos 10 y en el 60 %+
    de esta temporada, cada una con 62 %+."""
    out = []
    for p in partidos:
        for e in p.evaluaciones:
            if e.alertas or cuota(e) < cuota_min or e.prob < prob_min:
                continue
            hits, n = e.acierto_10
            if n < 8 or hits < min_aciertos:
                continue
            hits_t, n_t = e.acierto_temporada
            if n_t >= 2 and hits_t / n_t < 0.6:
                continue
            if not menos_aceptable(e):
                continue
            out.append((p, e))
    return sorted(out, key=lambda x: (x[1].prob, x[1].acierto_10[0]), reverse=True)


def combinada_segura(candidatas: list[tuple[Partido, Evaluacion]], n: int = 4) -> list[tuple[Partido, Evaluacion]]:
    elegidas, usados = [], set()
    for p, e in candidatas:
        if p.game["id"] not in usados:
            usados.add(p.game["id"])
            elegidas.append((p, e))
            if len(elegidas) == n:
                break
    return elegidas


def mejores(partidos: list[Partido], prob_min: float) -> list[tuple[Partido, Evaluacion]]:
    out = [(p, e) for p in partidos for e in p.evaluaciones if e.prob >= prob_min]
    return sorted(out, key=lambda x: x[1].prob, reverse=True)


def guardar_picks(db: NhlDB, fecha: str, picks: list[tuple[Partido, Evaluacion]],
                  partidos: list[Partido] = ()) -> None:
    db.conn.execute("DELETE FROM nhl_picks WHERE fecha = ? AND result IS NULL", (fecha,))
    sql = """INSERT OR REPLACE INTO nhl_picks(fecha, game_id, player_id, name, stat, line, side, prob, mu, odd,
                 tipo, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    db.conn.executemany(sql, [(fecha, p.game["id"], e.player_id, e.nombre, e.stat, e.line, e.lado, e.prob, e.mu,
                               e.odd, "estimada" if e.estimada else "prop", now_iso()) for p, e in picks])
    db.conn.executemany(sql, [(fecha, p.game["id"], s.player_id, s.nombre, s.stat, s.line, "más", s.prob, s.mu,
                               None, "segura", now_iso()) for p in partidos for s in p.seguras])
    db.commit()


def guardar_analisis(db: NhlDB, fecha: str, partidos: list[Partido]) -> None:
    db.conn.execute("DELETE FROM nhl_analisis WHERE fecha = ?", (fecha,))
    filas = []
    for p in partidos:
        for e in p.evaluaciones:
            detalle = {"factores": e.factores, "acierto_10": e.acierto_10, "acierto_temporada": e.acierto_temporada,
                       "vs_rival": e.vs_rival, "argumentos": e.argumentos, "alertas": e.alertas,
                       "notas": p.jugadores[e.player_id].notas if e.player_id in p.jugadores else []}
            filas.append((fecha, p.game["id"], e.player_id, e.nombre, e.stat, e.line, e.lado, e.prob, e.prob_modelo,
                          e.prob_mercado, e.mu, e.sd, e.odd, int(e.estimada), json.dumps(detalle, ensure_ascii=False),
                          now_iso()))
    db.conn.executemany(
        """INSERT OR REPLACE INTO nhl_analisis(fecha, game_id, player_id, name, stat, line, side, prob, prob_modelo,
               prob_mercado, mu, sd, odd, estimada, detalle, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", filas)
    db.commit()


# --- Liquidación y rendimiento --------------------------------------------------------

def fila_jugador(db: NhlDB, game_id: str, player_id: str, stat: str) -> dict | None:
    tabla = "nhl_goalie_games" if stat == "saves" else "nhl_player_games"
    r = db.conn.execute(f"SELECT * FROM {tabla} WHERE game_id = ? AND player_id = ?", (game_id, player_id)).fetchone()
    return dict(r) if r else None


def resultado(db: NhlDB, game_id: str, player_id: str, stat: str, line: float, side: str) -> tuple[float | None, int]:
    """(valor real, 1 acierto / 0 fallo / 2 anulada: no jugó o empate exacto)."""
    fila = fila_jugador(db, game_id, player_id, stat)
    if fila is None:
        return None, 2
    actual = valor(fila, stat)
    if actual == line:
        return actual, 2
    return actual, int((actual > line) == (side == "más"))


def liquidar(db: NhlDB) -> int:
    n = 0
    for pk in db.conn.execute(
            """SELECT p.* FROM nhl_picks p JOIN nhl_games g ON g.id = p.game_id
               WHERE p.result IS NULL AND g.box_ok = 1""").fetchall():
        actual, res = resultado(db, pk["game_id"], pk["player_id"], pk["stat"], pk["line"], pk["side"])
        db.conn.execute("UPDATE nhl_picks SET actual = ?, result = ? WHERE id = ?", (actual, res, pk["id"]))
        n += 1
    db.commit()
    return n


TRAMOS = ((0.0, 0.65), (0.65, 0.70), (0.70, 0.75), (0.75, 0.80), (0.80, 0.85), (0.85, 1.01))


def rendimiento(db: NhlDB) -> dict:
    filas = db.conn.execute("SELECT * FROM nhl_picks WHERE result IN (0, 1)").fetchall()

    def resumen(grupo):
        n = len(grupo)
        con_cuota = [r for r in grupo if r["odd"]]
        return {"n": n, "acierto": sum(r["result"] for r in grupo) / n,
                "prob_media": sum(r["prob"] for r in grupo) / n,
                "beneficio": sum((r["odd"] - 1) if r["result"] else -1 for r in con_cuota) if con_cuota else None,
                "con_cuota": len(con_cuota)}

    tramos = []
    for lo, hi in TRAMOS:
        g = [r for r in filas if lo <= r["prob"] < hi]
        if g:
            tramos.append({"tramo": f"{lo * 100:.0f}-{min(hi, 1) * 100:.0f}%", **resumen(g)})
    por_stat, por_tipo = {}, {}
    for r in filas:
        por_stat.setdefault(r["stat"], []).append(r)
        por_tipo.setdefault(r["tipo"] or "prop", []).append(r)
    return {"total": resumen(filas) if filas else None, "tramos": tramos,
            "tipos": [{"tipo": k, **resumen(v)} for k, v in sorted(por_tipo.items())],
            "stats": sorted(({"stat": k, **resumen(v)} for k, v in por_stat.items()), key=lambda x: -x["n"])}
