"""Jugada a jugada de ESPN: normalización, producción por cuarto, minutos en pista y primer anotador.

Convenciones de ESPN (comprobadas en 2021-22 y 2025-26):
- Tiro bloqueado: participantes [tirador, taponador], texto "X blocks Y's ...".
- Pérdida con robo: participantes [quien pierde, quien roba], texto "(... steals)".
- Canasta asistida: participantes [anotador, asistente], texto "(... assists)".
- Cambio: participantes [entra, sale], texto "X enters the game for Y".
- Salto: participantes [jugador 1, jugador 2, quien gana la posesión]; team.id = equipo que la gana.
- Rebote sin participante = rebote de equipo (no cuenta para ningún jugador).
"""
from __future__ import annotations

import re
from collections import defaultdict

from .zonas import distancia, zona

DURACION = {"reg": 720.0, "ot": 300.0}
STATS = ("pts", "fgm", "fga", "fg3m", "fg3a", "ftm", "fta", "oreb", "dreb", "ast", "stl", "blk", "tov", "pf")

# Tipos de pérdida que no llevan la palabra "turnover" en el tipo de jugada de ESPN.
PERDIDAS_SIN_PALABRA = {"traveling", "double dribble", "discontinued dribble", "palming", "backcourt",
                        "lane violation", "offensive goaltending", "illegal assist", "3-second",
                        "5-second", "8-second", "jump ball violation", "inbound"}
# Faltas que no cuentan como personales del jugador.
FALTAS_NO_PERSONALES = ("technical", "delay", "too many players", "defensive 3-second", "def 3 sec")

def duracion(periodo: int) -> float:
    return DURACION["reg"] if periodo <= 4 else DURACION["ot"]

def inicio_periodo(periodo: int) -> float:
    """Segundos de juego transcurridos al empezar el periodo."""
    return 720.0 * min(periodo - 1, 4) + 300.0 * max(periodo - 5, 0)

def reloj(v) -> float | None:
    """'11:38' -> 698; '45.2' -> 45.2 (segundos que quedan)."""
    s = str(v or "").strip()
    try:
        if ":" in s:
            m, sec = s.split(":", 1)
            return int(m) * 60 + float(sec)
        return float(s)
    except ValueError:
        return None

def _pid(p: dict, i: int) -> str | None:
    part = p.get("participants") or []
    if len(part) > i:
        return str((part[i].get("athlete") or {}).get("id") or "") or None
    return None

def clasificar(p: dict) -> str:
    tipo = (p.get("type") or {}).get("text", "").lower().replace("\n", " ")
    texto = (p.get("text") or "").lower()
    if tipo == "substitution":
        return "cambio"
    if tipo.startswith("jumpball") or tipo == "jump ball":
        return "salto"
    if tipo in ("end period", "end game", "end of period", "end of game"):
        return "fin_periodo"
    if "free throw" in tipo:
        return "libre"
    if p.get("shootingPlay"):
        return "tiro"
    if tipo == "offensive rebound":
        return "rebote_of"
    if tipo == "defensive rebound":
        return "rebote_def"
    if "turnover" in tipo or any(t in tipo for t in PERDIDAS_SIN_PALABRA) or " turnover" in texto:
        return "perdida"
    if "foul" in tipo or "charge" in tipo:
        return "falta"
    return "otro"

def normalizar(summary: dict) -> list[dict]:
    """Jugadas ordenadas con su tipo, tiempo transcurrido y participantes."""
    game_id = str(summary["header"]["id"])
    filas = []
    for p in summary.get("plays", []):
        periodo = (p.get("period") or {}).get("number") or 0
        if periodo <= 0:
            continue
        queda = reloj((p.get("clock") or {}).get("displayValue"))
        if queda is None:
            queda = 0.0
        evento = clasificar(p)
        texto = p.get("text") or ""
        valor = None
        c = p.get("coordinate") or {}
        x, y = c.get("x"), c.get("y")
        if x is None or y is None or abs(x) > 1000 or abs(y) > 1000:
            x = y = None
        if evento == "tiro":
            valor = valor_tiro(p, texto, x, y)
        elif evento == "libre":
            valor = 1
        try:
            seq = int(p.get("sequenceNumber"))
        except (TypeError, ValueError):
            seq = int(str(p.get("id"))[-7:])
        filas.append({
            "game_id": game_id, "seq": seq, "period": periodo, "clock_s": queda,
            "elapsed_s": inicio_periodo(periodo) + duracion(periodo) - queda,
            "team_id": str((p.get("team") or {}).get("id") or "") or None,
            "type_id": str((p.get("type") or {}).get("id") or ""),
            "type_text": (p.get("type") or {}).get("text", "").replace("\n", " "),
            "text": texto, "event": evento,
            "made": bool(p.get("scoringPlay")) if evento in ("tiro", "libre") else None,
            "points": int(p.get("scoreValue") or 0) if p.get("scoringPlay") else 0,
            "value": valor, "p1": _pid(p, 0), "p2": _pid(p, 1), "p3": _pid(p, 2),
            "home_score": p.get("homeScore"), "away_score": p.get("awayScore"), "x": x, "y": y,
        })
    # ESPN repite a veces un sequenceNumber: se renumera el duplicado al final (el orden real lo da el reloj).
    vistos, siguiente = set(), max((f["seq"] for f in filas), default=0) + 1
    for f in filas:
        if f["seq"] in vistos:
            f["seq"], siguiente = siguiente, siguiente + 1
        vistos.add(f["seq"])
    filas.sort(key=lambda r: (r["period"], -r["clock_s"], r["seq"]))
    return filas

def valor_tiro(p: dict, texto: str, x: float | None, y: float | None) -> int:
    """2 o 3. Hasta 2022 ESPN no rellena pointsAttempted: se usa el valor anotado, el texto
    ("three point") y, en fallos sin esa palabra, la distancia del texto o de las coordenadas."""
    pa = p.get("pointsAttempted") or 0
    if pa in (2, 3):
        return pa
    if p.get("scoringPlay") and int(p.get("scoreValue") or 0) in (2, 3):
        return int(p["scoreValue"])
    t = texto.lower()
    if "three point" in t or "3-pt" in t:
        return 3
    m = re.search(r"(\d+)-foot", t)
    pies = float(m.group(1)) if m else (distancia(x, y) if x is not None else None)
    if pies is None:
        return 2
    esquina = y is not None and y < 9
    return 3 if pies >= 24 or (pies >= 22 and esquina) else 2


def jugadores_por_equipo(box: list[dict]) -> dict[str, str]:
    """player_id -> team_id de los que jugaron."""
    return {r["player_id"]: r["team_id"] for r in box}

# --- Producción por periodo ---------------------------------------------------------------------

def produccion_por_periodo(jugadas: list[dict]) -> dict[tuple[str, int], dict[str, int]]:
    """(player_id, periodo) -> estadísticas acumuladas en ese periodo."""
    acc: dict[tuple[str, int], dict[str, int]] = defaultdict(lambda: dict.fromkeys(STATS, 0))
    for j in jugadas:
        per, ev, texto = j["period"], j["event"], j["text"].lower()
        if ev == "tiro" and j["p1"]:
            s = acc[(j["p1"], per)]
            s["fga"] += 1
            if j["value"] == 3:
                s["fg3a"] += 1
            if j["made"]:
                s["fgm"] += 1
                s["pts"] += j["points"] or j["value"]
                if j["value"] == 3:
                    s["fg3m"] += 1
                if j["p2"] and "assist" in texto:
                    acc[(j["p2"], per)]["ast"] += 1
            elif j["p2"] and "block" in texto:
                acc[(j["p2"], per)]["blk"] += 1
        elif ev == "libre" and j["p1"]:
            s = acc[(j["p1"], per)]
            s["fta"] += 1
            if j["made"]:
                s["ftm"] += 1
                s["pts"] += 1
        elif ev == "rebote_of" and j["p1"]:
            acc[(j["p1"], per)]["oreb"] += 1
        elif ev == "rebote_def" and j["p1"]:
            acc[(j["p1"], per)]["dreb"] += 1
        elif ev == "perdida" and j["p1"] and "team" not in j["type_text"].lower():
            acc[(j["p1"], per)]["tov"] += 1
            if j["p2"] and "steal" in texto:
                acc[(j["p2"], per)]["stl"] += 1
        elif ev == "falta" and j["p1"] and not any(f in j["type_text"].lower() for f in FALTAS_NO_PERSONALES):
            acc[(j["p1"], per)]["pf"] += 1
            if j["p2"] and "double personal" in j["type_text"].lower():
                acc[(j["p2"], per)]["pf"] += 1
    return acc

# --- Quintetos y minutos ------------------------------------------------------------------------

def quintetos(jugadas: list[dict], equipo_de: dict[str, str], titulares: dict[str, list[str]]
              ) -> tuple[list[dict], dict[tuple[str, int], float]]:
    """Reconstruye quién estaba en pista. Devuelve (tramos, segundos por (jugador, periodo)).

    En cada periodo un jugador está en pista al empezar si su primera aparición no es "entra al
    juego" (sale en un cambio o registra una acción antes). El 1.er cuarto usa los titulares del box.
    Si faltan jugadores (alguien jugó el periodo entero sin aparecer), se completan con los que
    terminaron el periodo anterior en pista y no entraron en ningún cambio de este periodo.
    """
    por_periodo: dict[int, list[dict]] = defaultdict(list)
    for j in jugadas:
        por_periodo[j["period"]].append(j)
    equipos = sorted(set(equipo_de.values()))
    tramos, segundos = [], defaultdict(float)
    en_pista_prev: dict[str, list[str]] = {t: list(titulares.get(t, [])) for t in equipos}

    for per in sorted(por_periodo):
        js = por_periodo[per]
        ini = inicio_periodo(per)
        fin = ini + duracion(per)
        en_pista: dict[str, set[str]] = {}
        for t in equipos:
            if per == 1 and len(titulares.get(t, [])) == 5:
                en_pista[t] = set(titulares[t])
                continue
            primera: dict[str, str] = {}
            for j in js:
                if j["event"] == "cambio":
                    for pid, papel in ((j["p1"], "entra"), (j["p2"], "sale")):
                        if pid and equipo_de.get(pid) == t:
                            primera.setdefault(pid, papel)
                elif j["event"] not in ("fin_periodo",):
                    for pid in (j["p1"], j["p2"], j["p3"]):
                        if pid and equipo_de.get(pid) == t and not _es_tecnica(j):
                            primera.setdefault(pid, "accion")
            s = {pid for pid, papel in primera.items() if papel != "entra"}
            if len(s) < 5:
                entran = {pid for pid, papel in primera.items() if papel == "entra"}
                for pid in en_pista_prev.get(t, []):
                    if len(s) >= 5:
                        break
                    if pid not in s and pid not in entran and pid not in primera:
                        s.add(pid)
            en_pista[t] = s

        # Recorrer el periodo aplicando cambios.
        actual = {t: set(en_pista[t]) for t in equipos}
        desde = {t: ini for t in equipos}
        for j in js:
            if j["event"] != "cambio":
                continue
            entra, sale = j["p1"], j["p2"]
            t = equipo_de.get(entra) or equipo_de.get(sale)
            if t is None:
                continue
            ahora = j["elapsed_s"]
            if ahora > desde[t]:
                tramos.append({"team_id": t, "period": per, "start_s": desde[t], "end_s": ahora,
                               "lineup": sorted(actual[t])})
                for pid in actual[t]:
                    segundos[(pid, per)] += ahora - desde[t]
                desde[t] = ahora
            if sale:
                actual[t].discard(sale)
            if entra:
                actual[t].add(entra)
        for t in equipos:
            if fin > desde[t]:
                tramos.append({"team_id": t, "period": per, "start_s": desde[t], "end_s": fin,
                               "lineup": sorted(actual[t])})
                for pid in actual[t]:
                    segundos[(pid, per)] += fin - desde[t]
            en_pista_prev[t] = sorted(actual[t])
    return tramos, dict(segundos)

def _es_tecnica(j: dict) -> bool:
    """Técnicas y libres de técnica pueden ser de jugadores en el banquillo."""
    t = (j["type_text"] + " " + j["text"]).lower()
    return "technical" in t or "ejection" in t

# --- Primer anotador y salto inicial ------------------------------------------------------------

def inicio_partido(jugadas: list[dict], equipo_de: dict[str, str], home_id: str, away_id: str,
                   titulares: dict[str, list[str]]) -> dict:
    out = {"jump_home_player": None, "jump_away_player": None, "jump_winner_team": None,
           "first_fg_player": None, "first_fg_team": None, "first_pts_player": None, "first_pts_team": None,
           "home_first_fg_player": None, "away_first_fg_player": None,
           "home_first_pts_player": None, "away_first_pts_player": None,
           "home_starters": sorted(titulares.get(home_id, [])), "away_starters": sorted(titulares.get(away_id, []))}
    salto = next((j for j in jugadas if j["period"] == 1 and j["event"] == "salto"), None)
    if salto:
        for pid in (salto["p1"], salto["p2"]):
            if equipo_de.get(pid) == home_id:
                out["jump_home_player"] = pid
            elif equipo_de.get(pid) == away_id:
                out["jump_away_player"] = pid
        ganador = salto["team_id"] or equipo_de.get(salto["p3"])
        out["jump_winner_team"] = ganador if ganador in (home_id, away_id) else None
    lado = {home_id: "home", away_id: "away"}
    for j in jugadas:
        if j["event"] not in ("tiro", "libre") or not j["made"] or not j["p1"]:
            continue
        t = equipo_de.get(j["p1"]) or j["team_id"]
        if out["first_pts_player"] is None:
            out["first_pts_player"], out["first_pts_team"] = j["p1"], t
        if t in lado and out[f"{lado[t]}_first_pts_player"] is None:
            out[f"{lado[t]}_first_pts_player"] = j["p1"]
        if j["event"] == "tiro":
            if out["first_fg_player"] is None:
                out["first_fg_player"], out["first_fg_team"] = j["p1"], t
            if t in lado and out[f"{lado[t]}_first_fg_player"] is None:
                out[f"{lado[t]}_first_fg_player"] = j["p1"]
        if all(out[k] for k in ("first_fg_player", "home_first_fg_player", "away_first_fg_player")):
            break
    return out

# --- Tiros con zona -------------------------------------------------------------------------------

def tiros(jugadas: list[dict], equipo_de: dict[str, str]) -> list[dict]:
    """ESPN da coordenadas en pies sobre media cancha: x de 0 a 50 (aro en 25), y desde el aro."""
    equipos = set(equipo_de.values())
    out = []
    for j in jugadas:
        if j["event"] != "tiro" or j["x"] is None or not j["p1"]:
            continue
        if not (0 <= j["x"] <= 50 and -5 <= j["y"] <= 94):
            continue
        z = zona(j["x"], j["y"], j["value"])
        if z is None:
            continue
        t = equipo_de.get(j["p1"]) or j["team_id"]
        out.append({"game_id": j["game_id"], "seq": j["seq"], "player_id": j["p1"], "team_id": t,
                    "opp_id": next((e for e in equipos if e != t), None), "period": j["period"],
                    "x": j["x"], "y": j["y"], "dist": round(distancia(j["x"], j["y"]), 1), "zone": z,
                    "value": j["value"], "made": bool(j["made"]),
                    "assisted": bool(j["made"] and "assist" in j["text"].lower())})
    return out

TEXTO_CAMBIO = re.compile(r"(.+) enters the game for (.+)", re.I)
