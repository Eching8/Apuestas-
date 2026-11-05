"""Jugada a jugada de ESPN: quién estaba en cancha, oportunidades de rebote y transición, por jugador y partido.

ESPN no da estos datos hechos (stats.nba.com sí, pero no responde desde la nube), así que se calculan:

- En cancha: los titulares del box score y cada cambio ("X enters the game for Y"). Al empezar cada cuarto,
  los cinco de cada equipo son los que aparecen en el cuarto antes de entrar por un cambio, completados con los
  que terminaron el cuarto anterior.
- Oportunidades de rebote: cada tiro de campo fallado deja un rebote. Los cinco que defienden suman una
  oportunidad defensiva y los cinco que atacan, una ofensiva (los libres fallados no cuentan, como en el modelo).
  Con los rebotes de cada jugador sale qué % de sus oportunidades convierte.
- Transición: puntos en los TRANSICION_SEG segundos siguientes a un robo o a un rebote defensivo de su equipo
  (contraataque), por jugador y por equipo, ajustados a los "fast break points" oficiales del box cuando están;
  lo que concede un equipo es la transición del rival.

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
    trans_pts REAL,
    trans_fga INTEGER,
    comp_fga INTEGER,
    comp_fgm INTEGER,
    comp_xfgm REAL,
    pts_favor REAL,
    pts_contra REAL,
    PRIMARY KEY (game_id, player_id)
);
"""
COLUMNAS_NUEVAS = {"comp_fga": "INTEGER", "comp_fgm": "INTEGER", "comp_xfgm": "REAL", "pts_favor": "REAL",
                   "pts_contra": "REAL"}

# Acierto de la liga por tipo de tiro (2025-26 y el inicio de 2026-27, 1.408 partidos): (de 2, de 3).
ACIERTO_TIPO = {"recibe y tira": (0.434, 0.368), "creado": (0.436, 0.332), "penetración": (0.547, 0.216),
                "corte": (0.772, 0.30), "poste": (0.456, 0.219), "palmeo": (0.599, 0.30), "aro": (0.654, 0.30)}



def _segundos(clock: dict | None) -> float:
    v = (clock or {}).get("displayValue", "0") or "0"
    try:
        partes = [float(x) for x in v.split(":")]
    except ValueError:
        return 0.0
    if len(partes) == 3 and partes[0] < 12 and partes[2] == 0:   # "1:39:00" = 1:39
        partes = partes[:2]
    total = 0.0
    for x in partes:
        total = total * 60 + x
    return total


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
                if not a.get("athlete", {}).get("id"):
                    continue   # ESPN a veces manda una ficha vacía
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
                          "oreb_op": 0, "dreb": 0, "oreb": 0, "trans_pts": 0, "trans_fga": 0, "comp_fga": 0,
                          "comp_fgm": 0, "comp_xfgm": 0.0, "pts_favor": 0, "pts_contra": 0}
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
            # Puntos de cada equipo con cada jugador en pista (para su impacto defensivo: con él y sin él).
            if p.get("scoringPlay") and p.get("scoreValue"):
                for pid in en_cancha.get(equipo, []):
                    fila(pid)["pts_favor"] += p["scoreValue"]
                for pid in en_cancha.get(rival[equipo], []):
                    fila(pid)["pts_contra"] += p["scoreValue"]
                fila(f"equipo:{equipo}")["pts_favor"] += p["scoreValue"]
                fila(f"equipo:{rival[equipo]}")["pts_contra"] += p["scoreValue"]
            # Tiros de sus compañeros con él en pista y lo que se esperaba que metieran según el tipo de tiro: la
            # base de sus asistencias "esperadas" (ESPN solo apunta la asistencia si el tiro entra).
            if es_tiro and ids:
                tipo_t = tipo_tiro(p["type"]["text"])
                if tipo_t:
                    triple = (p.get("pointsAttempted") or 0) == 3 or "three point" in texto
                    esperado = ACIERTO_TIPO[tipo_t][1 if triple else 0]
                    for pid in en_cancha.get(equipo, []):
                        if pid != ids[0]:
                            f = fila(pid)
                            f["comp_fga"] += 1
                            f["comp_fgm"] += bool(p.get("scoringPlay"))
                            f["comp_xfgm"] += esperado
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
    # La cuenta de 7 s sigue a los "fast break points" oficiales (correlación 0.84) pero da más puntos según la
    # temporada (2025-26: 22.6 frente a 15.9). Si el box trae la cifra oficial, se usa para el equipo y se reparte
    # entre sus jugadores en proporción a lo que anotó cada uno en esos 7 s.
    for t in summary.get("boxscore", {}).get("teams", []):
        tid = str(t.get("team", {}).get("id", ""))
        oficial = next((x.get("displayValue") for x in t.get("statistics", []) if x.get("name") == "fastBreakPoints"),
                       None)
        eq = filas.get(f"equipo:{tid}")
        if eq is None or oficial in (None, "", "-"):
            continue
        try:
            oficial = float(oficial)
        except ValueError:
            continue
        propio = eq["trans_pts"]
        eq["trans_pts"] = oficial
        for f in filas.values():
            if f["team_id"] == tid and not f["player_id"].startswith("equipo:"):
                f["trans_pts"] = f["trans_pts"] * oficial / propio if propio else 0.0
    return [f for f in filas.values() if f["team_id"]]


def preparar(conn) -> None:
    """Crea la tabla o le añade las columnas nuevas si es de una versión anterior."""
    conn.executescript(SCHEMA)
    tiene = {r[1] for r in conn.execute("PRAGMA table_info(nba_jugadas)")}
    for col, tipo in COLUMNAS_NUEVAS.items():
        if col not in tiene:
            conn.execute(f"ALTER TABLE nba_jugadas ADD COLUMN {col} {tipo}")


def guardar(conn, game_id: str, filas: list[dict]) -> None:
    preparar(conn)
    conn.execute("DELETE FROM nba_jugadas WHERE game_id = ?", (game_id,))
    conn.executemany(
        """INSERT INTO nba_jugadas (game_id, player_id, team_id, segundos, dreb_op, oreb_op, dreb, oreb, trans_pts,
               trans_fga, comp_fga, comp_fgm, comp_xfgm, pts_favor, pts_contra) VALUES (:game_id, :player_id, :team_id,
               :segundos, :dreb_op, :oreb_op, :dreb, :oreb, :trans_pts, :trans_fga, :comp_fga, :comp_fgm, :comp_xfgm,
               :pts_favor, :pts_contra)""",
        [{**f, "game_id": game_id} for f in filas])


# --- Tipos de tiro (parecido a los "play types" de Synergy, desde el tipo de tiro de ESPN) ----------------------
# ESPN describe cada tiro ("Pullup Jump Shot", "Cutting Dunk Shot"...). Se agrupan así:
TIPOS_TIRO = ("recibe y tira", "creado", "penetración", "corte", "poste", "palmeo", "aro")

SCHEMA_TIPOS = """
CREATE TABLE IF NOT EXISTS nba_tiros_tipo (
    game_id TEXT,
    player_id TEXT,
    team_id TEXT,
    tipo TEXT,
    fga INTEGER,
    fgm INTEGER,
    tpa INTEGER,
    tpm INTEGER,
    pts INTEGER,
    asistidos INTEGER,
    PRIMARY KEY (game_id, player_id, tipo)
);
"""


def tipo_tiro(texto: str) -> str | None:
    t = texto.lower()
    if "heave" in t or "no shot" in t:
        return None
    if "putback" in t or "tip " in t or t.startswith("tip"):
        return "palmeo"
    if "alley oop" in t or "cutting" in t:
        return "corte"
    if "driving" in t or ("running" in t and ("layup" in t or "dunk" in t or "finger roll" in t)):
        return "penetración"
    if "turnaround" in t or "hook" in t:
        return "poste"
    if "pullup" in t or "step back" in t or "fade away" in t or "fadeaway" in t:
        return "creado"
    if "floating" in t:
        return "penetración"
    if "jump shot" in t:
        return "recibe y tira"
    if "layup" in t or "dunk" in t or "finger roll" in t:
        return "aro"
    return None


def parse_tipos(summary: dict) -> list[dict]:
    """Tiros de campo de cada jugador por tipo, y los de cada equipo (player_id = "equipo:<id>")."""
    equipo_de = {}
    for t in summary.get("boxscore", {}).get("players", []):
        for g in t.get("statistics", []):
            for a in g.get("athletes", []):
                if a.get("athlete", {}).get("id"):
                    equipo_de[str(a["athlete"]["id"])] = str(t["team"]["id"])
    filas: dict[tuple, dict] = {}
    for p in summary.get("plays") or []:
        if not p.get("shootingPlay") or "free throw" in p["type"]["text"].lower():
            continue
        tipo = tipo_tiro(p["type"]["text"])
        ids = _ids(p)
        if tipo is None or not ids or ids[0] not in equipo_de:
            continue
        triple = (p.get("pointsAttempted") or 0) == 3 or "three point" in (p.get("text") or "").lower()
        anota = bool(p.get("scoringPlay"))
        asistido = anota and "assist" in (p.get("text") or "").lower()
        tid = equipo_de[ids[0]]
        for pid in (ids[0], f"equipo:{tid}"):
            f = filas.setdefault((pid, tipo), {"player_id": pid, "team_id": tid, "tipo": tipo, "fga": 0, "fgm": 0,
                                               "tpa": 0, "tpm": 0, "pts": 0, "asistidos": 0})
            f["fga"] += 1
            f["fgm"] += anota
            f["tpa"] += triple
            f["tpm"] += anota and triple
            f["pts"] += (3 if triple else 2) if anota else 0
            f["asistidos"] += asistido
    return list(filas.values())


def guardar_tipos(conn, game_id: str, filas: list[dict]) -> None:
    conn.executescript(SCHEMA_TIPOS)
    conn.execute("DELETE FROM nba_tiros_tipo WHERE game_id = ?", (game_id,))
    conn.executemany(
        """INSERT INTO nba_tiros_tipo (game_id, player_id, team_id, tipo, fga, fgm, tpa, tpm, pts, asistidos)
           VALUES (:game_id, :player_id, :team_id, :tipo, :fga, :fgm, :tpa, :tpm, :pts, :asistidos)""",
        [{**f, "game_id": game_id} for f in filas])


# --- Árbitros ------------------------------------------------------------------------------------------------
# Se guardan, pero no entran en el modelo: en 2025-26 (1.126 partidos) los equipos arbitrales que más pitan no
# dejaron más tiros libres ni más puntos de lo esperado. Tampoco el impacto defensivo con/sin cada jugador
# (pts_favor / pts_contra) mejoró el ajuste por bajas del rival: con una temporada es demasiado ruidoso.
SCHEMA_ARBITROS = """
CREATE TABLE IF NOT EXISTS nba_arbitros (
    game_id TEXT,
    nombre TEXT,
    PRIMARY KEY (game_id, nombre)
);
"""


def parse_arbitros(summary: dict) -> list[str]:
    return [o.get("displayName") or o.get("fullName") for o in (summary.get("gameInfo") or {}).get("officials") or []
            if o.get("displayName") or o.get("fullName")]


def guardar_arbitros(conn, game_id: str, nombres: list[str]) -> None:
    conn.executescript(SCHEMA_ARBITROS)
    conn.execute("DELETE FROM nba_arbitros WHERE game_id = ?", (game_id,))
    conn.executemany("INSERT OR IGNORE INTO nba_arbitros (game_id, nombre) VALUES (?, ?)", [(game_id, n) for n in nombres])
