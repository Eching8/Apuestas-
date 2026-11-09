"""Cliente de la API pública de ESPN para la NHL (sin clave).

- scoreboard: partidos de un día, con el portero probable de cada equipo y la línea (moneyline y total) de la casa.
- summary: un partido con box score por jugador (tiempo en hielo total, en power play y en inferioridad, tiros a
  puerta, goles, asistencias, tiros bloqueados, hits...), porteros (tiros recibidos, paradas), jugada a jugada (cada
  tiro con coordenadas, tipo y situación; cada gol con sus asistentes) y lesiones.

Comprobado el 7 nov 2026: en el box, "S" son los tiros a puerta (la suma cuadra con los "shotsTotal" del equipo),
"SM" los tiros fuera y "SOG" los goles en la tanda de penaltis (no los tiros a puerta). ESPN no da las líneas
(quién juega con quién) ni el "titular": el rol se mide con el tiempo en hielo.
"""
from __future__ import annotations

import logging
import math
import os
import re
import time
from typing import Any

import requests

from ..api_football import ApiError

log = logging.getLogger(__name__)

BASE_URL = "https://site.api.espn.com/apis/site/v2/sports/hockey/nhl"
MIN_INTERVALO = float(os.environ.get("APUESTAS_NHL_INTERVALO", 0.4))
TERMINADO = "STATUS_FINAL"


class Espn:
    def __init__(self, session: requests.Session | None = None, base_url: str = BASE_URL):
        self.base_url = base_url
        self.session = session or requests.Session()
        self.session.headers.setdefault("User-Agent", "Mozilla/5.0 (apuestas)")
        self.peticiones = 0
        self._ultima = 0.0

    def _get(self, path: str, **params: Any) -> dict:
        for intento in range(4):
            espera = MIN_INTERVALO - (time.monotonic() - self._ultima)
            if espera > 0:
                time.sleep(espera)
            self._ultima = time.monotonic()
            try:
                resp = self.session.get(f"{self.base_url}{path}", params=params, timeout=30)
            except requests.RequestException as e:
                log.warning("ESPN %s: %s (reintento %d)", path, e, intento + 1)
                time.sleep(2 ** intento)
                continue
            self.peticiones += 1
            if resp.status_code in (429, 500, 502, 503, 504):
                time.sleep(2 ** (intento + 1))
                continue
            if resp.status_code != 200:
                raise ApiError(f"ESPN {path} {params}: HTTP {resp.status_code}")
            return resp.json()
        raise ApiError(f"ESPN {path} {params}: sin respuesta tras varios intentos")

    def partidos(self, fecha: str) -> list[dict]:
        """Partidos de un día (AAAA-MM-DD, calendario de ESPN en hora del este de EE. UU.)."""
        return parse_scoreboard(self._get("/scoreboard", dates=fecha.replace("-", ""), limit=50))

    def resumen(self, game_id: str) -> dict:
        return self._get("/summary", event=game_id)


# --- Parsers --------------------------------------------------------------------------

def _team(t: dict) -> dict:
    return {"id": str(t["id"]), "abbr": t.get("abbreviation"), "name": t.get("displayName"),
            "nickname": t.get("name") or t.get("shortDisplayName")}


def _int(v) -> int | None:
    try:
        return int(v)
    except (TypeError, ValueError):
        return None


def _float(v) -> float | None:
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def americana(v) -> float | None:
    """Cuota americana -> probabilidad implícita (con margen)."""
    v = _float(v)
    if not v:
        return None
    return 100 / (v + 100) if v > 0 else -v / (-v + 100)


def goles_esperados(p_local: float, total: float) -> tuple[float, float]:
    """Goles esperados de local y visitante que cuadran con la probabilidad de que gane el local (moneyline sin
    margen, prórroga incluida: el empate a 60' se reparte a medias) y el total de la casa (Poisson independientes)."""
    def p_gana(d: float) -> float:
        lh, la = max(0.05, (total + d) / 2), max(0.05, (total - d) / 2)
        ph = [math.exp(-lh) * lh ** k / math.factorial(k) for k in range(16)]
        pa = [math.exp(-la) * la ** k / math.factorial(k) for k in range(16)]
        gana = sum(ph[i] * pa[j] for i in range(16) for j in range(i))
        empate = sum(ph[i] * pa[i] for i in range(16))
        return gana + empate / 2
    lo, hi = -total + 0.1, total - 0.1
    for _ in range(40):
        mid = (lo + hi) / 2
        if p_gana(mid) < p_local:
            lo = mid
        else:
            hi = mid
    d = (lo + hi) / 2
    return (total + d) / 2, (total - d) / 2


def _linea_partido(comp: dict) -> dict:
    """Moneyline y total de la casa (ESPN, antes del partido) -> goles esperados de cada equipo."""
    for o in comp.get("odds") or []:
        total = _float(o.get("overUnder"))
        ml = o.get("moneyline") or {}
        ph = americana((o.get("homeTeamOdds") or {}).get("moneyLine")
                       or ((ml.get("home") or {}).get("close") or {}).get("odds"))
        pa = americana((o.get("awayTeamOdds") or {}).get("moneyLine")
                       or ((ml.get("away") or {}).get("close") or {}).get("odds"))
        if total and ph and pa:
            p = ph / (ph + pa)
            gh, ga = goles_esperados(p, total)
            return {"total_esperado": total, "margen_esperado": round(gh - ga, 3)}
        if total:
            return {"total_esperado": total, "margen_esperado": None}
    return {"total_esperado": None, "margen_esperado": None}


def parse_scoreboard(data: dict) -> list[dict]:
    out = []
    for e in data.get("events", []):
        comp = e["competitions"][0]
        lados = {c["homeAway"]: c for c in comp["competitors"]}
        if "home" not in lados or "away" not in lados:
            continue
        season = e.get("season", {})
        probables = {}
        for lado in ("home", "away"):
            for pr in lados[lado].get("probables") or []:
                ath = pr.get("athlete") or {}
                if pr.get("name") == "probableStartingGoalie" and ath.get("id"):
                    probables[lado] = {"player_id": str(ath["id"]), "name": ath.get("displayName")}
        out.append({
            "id": str(e["id"]),
            "date_utc": e["date"],
            "season": season.get("year"),
            "season_type": season.get("type"),
            "status": e["status"]["type"]["name"],
            "home": _team(lados["home"]["team"]),
            "away": _team(lados["away"]["team"]),
            "home_goals": _int(lados["home"].get("score")),
            "away_goals": _int(lados["away"].get("score")),
            "periodos": _int((e.get("status") or {}).get("period")),
            "probables": probables,
            **_linea_partido(comp),
        })
    return out


def toi(v: str | None) -> float:
    """'13:44' -> 13.73 minutos."""
    try:
        if v and ":" in v:
            m, s = v.split(":", 1)
            return int(m) + int(s) / 60
        return float(v or 0)
    except (TypeError, ValueError):
        return 0.0


def grupo_posicion(pos: str | None) -> str:
    """F (delantero: C, LW, RW), D (defensa) o G (portero)."""
    pos = (pos or "").upper()
    if pos.startswith("G"):
        return "G"
    if pos.startswith("D"):
        return "D"
    return "F"


def parse_box(summary: dict) -> tuple[list[dict], list[dict]]:
    """(jugadores de campo, porteros) que jugaron (tiempo en hielo > 0)."""
    equipos = summary.get("boxscore", {}).get("players", [])
    ids = [str(t["team"]["id"]) for t in equipos]
    skaters, goalies = [], []
    for t in equipos:
        team_id = str(t["team"]["id"])
        opp_id = next((i for i in ids if i != team_id), None)
        for bloque in t.get("statistics", []):
            nombre_bloque = bloque.get("name")
            labels = bloque.get("labels") or []
            for a in bloque.get("athletes", []):
                if a.get("didNotPlay") or not a.get("stats"):
                    continue
                s = dict(zip(labels, a["stats"]))
                minutos = toi(s.get("TOI"))
                if minutos <= 0:
                    continue
                ath = a["athlete"]
                base = {"player_id": str(ath["id"]), "team_id": team_id, "opp_id": opp_id,
                        "name": ath.get("displayName"), "position": (ath.get("position") or {}).get("abbreviation")}
                if nombre_bloque == "goalies":
                    goalies.append({**base, "toi": round(minutos, 2), "sa": _int(s.get("SA")) or 0,
                                    "sv": _int(s.get("SV")) or 0, "ga": _int(s.get("GA")) or 0,
                                    "es_sv": _int(s.get("ESSV")) or 0, "pp_sv": _int(s.get("PPSV")) or 0,
                                    "sh_sv": _int(s.get("SHSV")) or 0})
                    continue
                if nombre_bloque not in ("forwards", "defenses", "skaters"):
                    continue
                skaters.append({
                    **base, "grupo": "D" if nombre_bloque == "defenses" else grupo_posicion(base["position"]),
                    "toi": round(minutos, 2), "pptoi": round(toi(s.get("PPTOI")), 2),
                    "shtoi": round(toi(s.get("SHTOI")), 2), "estoi": round(toi(s.get("ESTOI")), 2),
                    "shifts": _int(s.get("SHFT")) or 0, "g": _int(s.get("G")) or 0, "a": _int(s.get("A")) or 0,
                    "sog": _int(s.get("S")) or 0, "missed": _int(s.get("SM")) or 0, "bs": _int(s.get("BS")) or 0,
                    "hits": _int(s.get("HT")) or 0, "tk": _int(s.get("TK")) or 0, "gv": _int(s.get("GV")) or 0,
                    "pm": _int(s.get("+/-")) or 0, "pim": _int(s.get("PIM")) or 0, "fow": _int(s.get("FW")) or 0,
                    "fol": _int(s.get("FL")) or 0,
                })
    # Portero titular: el que más tiempo jugó de su equipo.
    for team_id in {g["team_id"] for g in goalies}:
        suyos = sorted((g for g in goalies if g["team_id"] == team_id), key=lambda g: -g["toi"])
        for k, g in enumerate(suyos):
            g["starter"] = int(k == 0)
    return skaters, goalies


FUERZA = {"even-strength": "ES", "power-play": "PP", "short-handed": "SH"}
RESULTADO = {"Shot": "sog", "Goal": "goal", "Missed": "missed", "Blocked": "blocked"}
TIPOS_TIRO = ("Wrist Shot", "Snap Shot", "Slap Shot", "Backhand", "Tip-In", "Deflected", "Wrap-around", "Poke",
              "Bat", "Between Legs", "Cradle")


def tipo_tiro(texto: str) -> str | None:
    for t in TIPOS_TIRO:
        if t.lower() in texto.lower():
            return t
    return None


def distancia(x: float, y: float) -> float:
    """Distancia a la portería (ESPN: x de -100 a 100, porterías en x = ±89)."""
    return math.hypot(89 - abs(x), y)


def parse_jugadas(summary: dict) -> tuple[list[dict], list[dict], list[dict]]:
    """(tiros, goles con asistentes, penaltis) de la jugada a jugada."""
    ids = [str(t["team"]["id"]) for t in summary.get("boxscore", {}).get("players", [])]
    tiros, goles, penaltis = [], [], []
    for p in summary.get("plays", []):
        tipo = (p.get("type") or {}).get("text", "")
        part = p.get("participants") or []
        team_id = str((p.get("team") or {}).get("id"))
        opp = next((i for i in ids if i != team_id), None)
        periodo = (p.get("period") or {}).get("number")
        fuerza = FUERZA.get((p.get("strength") or {}).get("abbreviation"), "ES")
        seq = _int(p.get("sequenceNumber")) or _int(str(p.get("id", ""))[-6:]) or 0
        if tipo in RESULTADO and part:
            if (periodo or 0) > 4:   # tanda de penaltis: no cuenta en las estadísticas del partido
                continue
            c = p.get("coordinate") or {}
            x, y = c.get("x"), c.get("y")
            portero = next((str(q["athlete"]["id"]) for q in part[1:] if q.get("type") in ("saver", "goalie")), None)
            tiros.append({"seq": seq, "player_id": str(part[0]["athlete"]["id"]), "team_id": team_id, "opp_id": opp,
                          "period": periodo, "x": x, "y": y,
                          "dist": round(distancia(x, y), 1) if x is not None and y is not None else None,
                          "shot_type": tipo_tiro(p.get("text", "")), "result": RESULTADO[tipo], "strength": fuerza,
                          "goalie_id": portero})
            if tipo == "Goal":
                asist = [str(q["athlete"]["id"]) for q in part[1:] if q.get("type") == "assister"]
                goles.append({"seq": seq, "team_id": team_id, "opp_id": opp, "period": periodo, "strength": fuerza,
                              "scorer_id": str(part[0]["athlete"]["id"]),
                              "a1_id": asist[0] if asist else None, "a2_id": asist[1] if len(asist) > 1 else None})
        elif part and _es_penalti(p):
            penaltis.append({"seq": seq, "player_id": str(part[0]["athlete"]["id"]), "team_id": team_id,
                             "opp_id": opp, "period": periodo, "tipo": tipo})
    return tiros, goles, penaltis


NO_PENALTI = {"Face Off", "Hit", "Stoppage", "Giveaway", "Takeaway", "Shot", "Goal", "Missed", "Blocked",
              "Period Start", "Period End", "End of Game", "Shootout", "Game End", "Delayed Penalty", "Challenge",
              "Official Challenge", "Early Intermission Start", "Early Intermission End", "Penalty Shot"}


def _es_penalti(p: dict) -> bool:
    """ESPN pone el nombre de la falta como tipo ('Tripping', 'Hooking'...): todo lo que no es otra jugada."""
    tipo = (p.get("type") or {}).get("text", "")
    return bool(tipo) and tipo not in NO_PENALTI and " against " in (p.get("text") or "")


def parse_injuries(summary: dict) -> list[dict]:
    out = []
    for t in summary.get("injuries", []):
        for i in t.get("injuries", []):
            ath = i.get("athlete") or {}
            if not ath.get("id"):
                continue
            out.append({"team_id": str(t["team"]["id"]), "player_id": str(ath["id"]),
                        "name": ath.get("displayName"), "status": i.get("status") or "",
                        "detail": ((i.get("details") or {}).get("type") or "")})
    return out


def nombre_limpio(texto: str) -> str:
    return re.sub(r"\s+", " ", texto or "").strip()
