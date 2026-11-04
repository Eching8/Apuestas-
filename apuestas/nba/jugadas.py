"""Jugada a jugada de ESPN: quién estaba en cancha, oportunidades de rebote y transición, por jugador y partido.

ESPN no da estos datos hechos (stats.nba.com sí, pero no responde desde la nube), así que se calculan:

- En cancha: los titulares del box score y cada cambio ("X enters the game for Y"). Al empezar cada cuarto,
  los cinco de cada equipo son los que aparecen en el cuarto antes de entrar por un cambio, completados con los
  que terminaron el cuarto anterior.
- Oportunidades de rebote: cada tiro de campo fallado deja un rebote. Los cinco que defienden suman una
  oportunidad defensiva y los cinco que atacan, una ofensiva (los libres fallados no cuentan, como en el modelo).
  Con los rebotes de cada jugador sale qué % de sus oportunidades convierte.
- Transición: puntos en los TRANSICION_SEG segundos siguientes a un robo o a un rebote defensivo de su equipo
  (contraataque), por jugador y por equipo; lo que concede un equipo es la transición del rival.

Una fila por jugador y partido en nba_jugadas, y una por equipo (player_id = "equipo:<id>") con los totales.
"""
from __future__ import annotations

import logging

log = logging.getLogger(__name__)

TRANSICION_SEG = 7.0   # con 7 s la media coincide con los "fast break points" de ESPN (13.2 frente a 13.3)

SCHEMA = """
CREATE TABLE IF NOT EXISTS nba_jugadas (
    game_id TEXT,
    player_id TEXT,
    team_id TEXT,
    segundos REAL,
    dreb_op INTEGER,
    oreb_op INTEGER,
    dreb INTEGER,
    oreb INTEGER,
    trans_pts INTEGER,
    trans_fga INTEGER,
    PRIMARY KEY (game_id, player_id)
);
"""



def _segundos(clock: dict | None) -> float:
    v = (clock or {}).get("displayValue", "0") or "0"
    if ":" in v:
        m, s = v.split(":", 1)
        return int(m) * 60 + float(s)
    try:
        return float(v)
    except ValueError:
        return 0.0


def _duracion(periodo: int) -> float:
    return 720.0 if periodo <= 4 else 300.0


def _ids(p: dict) -> list[str]:
    return [str(x["athlete"]["id"]) for x in p.get("participants", []) if x.get("athlete", {}).get("id")]


def _cinco_iniciales(plays: list[dict], equipo_de: dict[str, str], equipo: str, anteriores: list[str]) -> list[str]:
    """Los cinco de un equipo al empezar un cuarto."""
    vistos, entraron = [], set()
    for p in plays:
        ids = _ids(p)
        if p["type"]["text"] == "Substitution" and len(ids) >= 2:
            entra, sale = ids[0], ids[1]
            if equipo_de.get(sale) == equipo and sale not in entraron and sale not in vistos:
                vistos.append(sale)
            if equipo_de.get(entra) == equipo:
                entraron.add(entra)
            continue
        for i in ids:
            if equipo_de.get(i) == equipo and i not in entraron and i not in vistos:
                vistos.append(i)
    for i in anteriores:
        if len(vistos) >= 5:
            break
        if i not in vistos and i not in entraron:
            vistos.append(i)
    return vistos[:5]


def parse_jugadas(summary: dict) -> list[dict]:
    plays = summary.get("plays") or []
    equipos = summary.get("boxscore", {}).get("players", [])
    if not plays or len(equipos) != 2:
        return []
    equipo_de, titulares = {}, {}
    for t in equipos:
        tid = str(t["team"]["id"])
        titulares[tid] = []
        for g in t.get("statistics", []):
            for a in g.get("athletes", []):
                pid = str(a["athlete"]["id"])
                equipo_de[pid] = tid
                if a.get("starter"):
                    titulares[tid].append(pid)
    tids = list(titulares)
    rival = {tids[0]: tids[1], tids[1]: tids[0]}
    filas: dict[str, dict] = {}

    def fila(pid: str) -> dict:
        if pid not in filas:
            filas[pid] = {"player_id": pid, "team_id": equipo_de.get(pid, ""), "segundos": 0.0, "dreb_op": 0,
                          "oreb_op": 0, "dreb": 0, "oreb": 0, "trans_pts": 0, "trans_fga": 0}
        return filas[pid]

    for tid in tids:
        fila(f"equipo:{tid}")["team_id"] = tid

    por_periodo: dict[int, list[dict]] = {}
    for p in plays:
        por_periodo.setdefault(int(p.get("period", {}).get("number", 0) or 0), []).append(p)
    en_cancha = {tid: list(titulares[tid][:5]) for tid in tids}
    for periodo in sorted(k for k in por_periodo if k > 0):
        lista = por_periodo[periodo]
        if periodo > 1:
            en_cancha = {tid: _cinco_iniciales(lista, equipo_de, tid, en_cancha[tid]) for tid in tids}
        reloj = _duracion(periodo)
        ventana: dict[str, float] = {}           # equipo -> segundos del reloj al empezar su contraataque
        for p in lista:
            t = _segundos(p.get("clock"))
            transcurrido = max(0.0, reloj - t)
            for tid in tids:
                for pid in en_cancha[tid]:
                    fila(pid)["segundos"] += transcurrido
            reloj = min(reloj, t)
            tipo = p["type"]["text"]
            ids = _ids(p)
            equipo = str((p.get("team") or {}).get("id", "")) or (equipo_de.get(ids[0], "") if ids else "")
            texto = (p.get("text") or "").lower()
            if tipo == "Substitution" and len(ids) >= 2:
                entra, sale = ids[0], ids[1]
                tid = equipo_de.get(entra) or equipo_de.get(sale)
                if tid in en_cancha:
                    if sale in en_cancha[tid]:
                        en_cancha[tid].remove(sale)
                    if entra not in en_cancha[tid]:
                        en_cancha[tid].append(entra)
                continue
            if equipo not in rival:
                continue
            # Se cierra el contraataque del equipo que defiende en cuanto el rival tira o recupera.
            for tid in list(ventana):
                if ventana[tid] - t > TRANSICION_SEG or (tid != equipo and (p.get("shootingPlay") or "rebound" in texto)):
                    del ventana[tid]
            cierra_propio = False
            es_tiro = bool(p.get("shootingPlay")) and "free throw" not in tipo.lower()
            if p.get("shootingPlay") and equipo in ventana:
                if ids and es_tiro:
                    fila(ids[0])["trans_fga"] += 1
                if p.get("scoringPlay"):
                    puntos = int(p.get("scoreValue") or 0)
                    if ids:
                        fila(ids[0])["trans_pts"] += puntos
                    fila(f"equipo:{equipo}")["trans_pts"] += puntos
            # Solo tiros de campo: el modelo multiplica la tasa por los fallos de campo esperados del rival.
            fallo = False
            if es_tiro and not p.get("scoringPlay"):
                fallo = True
                cierra_propio = True
            if fallo:
                for pid in en_cancha.get(rival[equipo], []):
                    fila(pid)["dreb_op"] += 1
                for pid in en_cancha.get(equipo, []):
                    fila(pid)["oreb_op"] += 1
                fila(f"equipo:{rival[equipo]}")["dreb_op"] += 1
                fila(f"equipo:{equipo}")["oreb_op"] += 1
            if cierra_propio:
                ventana.pop(equipo, None)
            # Los rebotes "de equipo" (sin jugador) no cuentan: casi todos son tras un primer libre fallado.
            if tipo == "Defensive Rebound":
                if ids:
                    fila(ids[0])["dreb"] += 1
                    fila(f"equipo:{equipo}")["dreb"] += 1
                ventana[equipo] = t
            elif tipo == "Offensive Rebound" and ids:
                fila(ids[0])["oreb"] += 1
                fila(f"equipo:{equipo}")["oreb"] += 1
            elif "turnover" in tipo.lower() and "steals" in texto and len(ids) >= 2:
                ladron = equipo_de.get(ids[1])
                if ladron in rival:
                    ventana[ladron] = t
    return [f for f in filas.values() if f["team_id"]]


def guardar(conn, game_id: str, filas: list[dict]) -> None:
    conn.executescript(SCHEMA)
    conn.execute("DELETE FROM nba_jugadas WHERE game_id = ?", (game_id,))
    conn.executemany(
        """INSERT INTO nba_jugadas (game_id, player_id, team_id, segundos, dreb_op, oreb_op, dreb, oreb, trans_pts,
               trans_fga) VALUES (:game_id, :player_id, :team_id, :segundos, :dreb_op, :oreb_op, :dreb, :oreb,
               :trans_pts, :trans_fga)""",
        [{**f, "game_id": game_id} for f in filas])
