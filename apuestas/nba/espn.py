"""Cliente de la API pública de ESPN (sin clave): calendario, box score, tiros con coordenadas y lesiones.

- scoreboard: partidos de un día (https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard)
- summary: un partido con box score por jugador, jugada a jugada (cada tiro con su posición) y lesiones.
"""
from __future__ import annotations

import logging
import os
import re
import time
from typing import Any

import requests

from ..api_football import ApiError
from .zonas import distancia, zona

log = logging.getLogger(__name__)

BASE_URL = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba"
# Pausa entre consultas: la API es gratuita y sin clave, no hay que abusar de ella.
MIN_INTERVALO = float(os.environ.get("APUESTAS_NBA_INTERVALO", 0.4))
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


def parse_scoreboard(data: dict) -> list[dict]:
    out = []
    for e in data.get("events", []):
        comp = e["competitions"][0]
        lados = {c["homeAway"]: c for c in comp["competitors"]}
        if "home" not in lados or "away" not in lados:
            continue
        season = e.get("season", {})
        out.append({
            "id": str(e["id"]),
            "date_utc": e["date"],
            "season": season.get("year"),
            "season_type": season.get("type"),
            "status": e["status"]["type"]["name"],
            "home": _team(lados["home"]["team"]),
            "away": _team(lados["away"]["team"]),
            "home_pts": _int(lados["home"].get("score")),
            "away_pts": _int(lados["away"].get("score")),
        })
    return out


def _int(v) -> int | None:
    try:
        return int(v)
    except (TypeError, ValueError):
        return None


def _minutos(v: str) -> float:
    """'34', '34:12' o marcas de no jugó ('-', '--', 'DNP')."""
    try:
        if v and ":" in v:
            m, s = v.split(":", 1)
            return int(m) + int(s) / 60
        return float(v)
    except (TypeError, ValueError):
        return 0.0


def _hecho_intentado(v: str) -> tuple[int, int]:
    m = re.match(r"(\d+)-(\d+)", v or "")
    return (int(m.group(1)), int(m.group(2))) if m else (0, 0)


def grupo_posicion(pos: str | None) -> str:
    """G (base/escolta), F (alero/ala-pívot) o C (pívot)."""
    pos = (pos or "").upper()
    if pos.startswith("C"):
        return "C"
    if pos.startswith("PF") or pos.startswith("SF") or pos.startswith("F"):
        return "F"
    return "G"


def parse_box(summary: dict) -> list[dict]:
    """Una fila por jugador que jugó (minutos > 0)."""
    equipos = summary.get("boxscore", {}).get("players", [])
    ids = [str(t["team"]["id"]) for t in equipos]
    rows = []
    for t in equipos:
        team_id = str(t["team"]["id"])
        opp_id = next((i for i in ids if i != team_id), None)
        for bloque in t.get("statistics", []):
            labels = bloque.get("labels") or bloque.get("names") or []
            for a in bloque.get("athletes", []):
                if a.get("didNotPlay") or not a.get("stats"):
                    continue
                s = dict(zip(labels, a["stats"]))
                minutos = _minutos(s.get("MIN"))
                if minutos <= 0:
                    continue
                fgm, fga = _hecho_intentado(s.get("FG"))
                tpm, tpa = _hecho_intentado(s.get("3PT"))
                ftm, fta = _hecho_intentado(s.get("FT"))
                ath = a["athlete"]
                rows.append({
                    "player_id": str(ath["id"]), "team_id": team_id, "opp_id": opp_id,
                    "name": ath.get("displayName"),
                    "position": (ath.get("position") or {}).get("abbreviation"),
                    "starter": int(bool(a.get("starter"))), "minutes": round(minutos, 2),
                    "pts": _int(s.get("PTS")) or 0, "fgm": fgm, "fga": fga, "tpm": tpm, "tpa": tpa,
                    "ftm": ftm, "fta": fta, "reb": _int(s.get("REB")) or 0, "oreb": _int(s.get("OREB")) or 0,
                    "dreb": _int(s.get("DREB")) or 0, "ast": _int(s.get("AST")) or 0, "stl": _int(s.get("STL")) or 0,
                    "blk": _int(s.get("BLK")) or 0, "tov": _int(s.get("TO")) or 0, "pf": _int(s.get("PF")) or 0,
                })
    return rows


def parse_shots(summary: dict) -> list[dict]:
    """Tiros de campo con zona. El primer participante es el tirador; el segundo, quien asiste o tapona."""
    ids = [str(t["team"]["id"]) for t in summary.get("boxscore", {}).get("players", [])]
    rows = []
    for p in summary.get("plays", []):
        if not p.get("shootingPlay") or "free throw" in (p.get("type", {}).get("text", "") + p.get("text", "")).lower():
            continue
        c, part = p.get("coordinate") or {}, p.get("participants") or []
        x, y, valor = c.get("x"), c.get("y"), p.get("pointsAttempted")
        if x is None or y is None or valor not in (2, 3) or abs(x) > 100 or abs(y) > 100 or not part:
            continue
        z = zona(x, y, valor)
        if z is None:
            continue
        team_id = str((p.get("team") or {}).get("id"))
        texto = p.get("text", "").lower()
        rows.append({
            "seq": int(p.get("sequenceNumber") or p["id"][-6:]),
            "player_id": str(part[0]["athlete"]["id"]), "team_id": team_id,
            "opp_id": next((i for i in ids if i != team_id), None),
            "period": (p.get("period") or {}).get("number"),
            "x": x, "y": y, "dist": round(distancia(x, y), 1), "zone": z, "value": valor,
            "made": int(bool(p.get("scoringPlay"))), "assisted": int("assist" in texto),
        })
    return rows


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
