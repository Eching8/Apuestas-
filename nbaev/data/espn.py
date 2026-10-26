"""ESPN (API pública, sin clave): calendario, box score, jugada a jugada, líneas de cierre y lesiones.

Es la fuente principal porque responde desde cualquier red (stats.nba.com bloquea servidores en la nube).
- scoreboard: partidos de un día y calendario de la temporada.
- summary: un partido con box score, jugada a jugada (con coordenadas de tiro), líneas (pickcenter).
- injuries: parte de lesiones actual de toda la liga.

Ojo: el bloque `injuries` de un summary es SIEMPRE el parte actual, no el del día del partido. Para
partidos pasados las bajas se toman de los jugadores que no jugaron en el box score.
"""
from __future__ import annotations

import gzip
import json
import logging
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from .http import ClienteHttp, Limitador

log = logging.getLogger(__name__)

ET = ZoneInfo("America/New_York")
FINAL = "STATUS_FINAL"


class Espn:
    def __init__(self, cfg: dict, crudos: Path | None = None, session=None):
        c = cfg["fuentes"]["espn"]
        self.http = ClienteHttp(c["url"], Limitador(c["min_intervalo_s"]), c["reintentos"], c["timeout_s"],
                                session=session, nombre="ESPN")
        self.crudos = crudos

    def scoreboard(self, fecha: str) -> dict:
        """fecha AAAA-MM-DD (calendario de ESPN, hora del este)."""
        return self.http.get_json("/scoreboard", dates=fecha.replace("-", ""), limit=100)

    def summary(self, game_id: str, cache: bool = True) -> dict:
        """Resumen de un partido. Si está terminado se guarda comprimido en crudos/ para reprocesar."""
        archivo = self._archivo(game_id)
        if cache and archivo and archivo.exists():
            with gzip.open(archivo, "rt", encoding="utf-8") as f:
                return json.load(f)
        data = self.http.get_json("/summary", event=game_id)
        if archivo and _estado(data) == FINAL:
            archivo.parent.mkdir(parents=True, exist_ok=True)
            with gzip.open(archivo, "wt", encoding="utf-8") as f:
                json.dump(data, f, separators=(",", ":"))
        return data

    def lesiones(self) -> dict:
        return self.http.get_json("/injuries")

    def _archivo(self, game_id: str) -> Path | None:
        return self.crudos / "espn" / f"{game_id[-2:]}" / f"{game_id}.json.gz" if self.crudos else None


def _estado(summary: dict) -> str | None:
    try:
        return summary["header"]["competitions"][0]["status"]["type"]["name"]
    except (KeyError, IndexError):
        return None


# --- Utilidades ---------------------------------------------------------------------------------

def a_int(v) -> int | None:
    try:
        return int(float(v))
    except (TypeError, ValueError):
        return None


def utc_naive(iso: str) -> datetime:
    """'2021-11-05T23:00Z' -> datetime UTC sin zona."""
    return datetime.fromisoformat(iso.replace("Z", "+00:00")).replace(tzinfo=None)


def fecha_et(iso: str) -> str:
    return datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone(ET).date().isoformat()


def minutos(v) -> float:
    """'34', '34:12' o marcas de no jugó ('-', '--', 'DNP')."""
    try:
        if v and ":" in str(v):
            m, s = str(v).split(":", 1)
            return int(m) + int(s) / 60
        return float(v)
    except (TypeError, ValueError):
        return 0.0


def hecho_intentado(v) -> tuple[int, int]:
    m = re.match(r"(\d+)-(\d+)", str(v or ""))
    return (int(m.group(1)), int(m.group(2))) if m else (0, 0)


def temporada_desde_espn(year: int) -> int:
    """ESPN llama 2022 a la temporada 2021-22; aquí se guarda el año de inicio (2021)."""
    return int(year) - 1


# --- Scoreboard -------------------------------------------------------------------------------

def calendario(scoreboard: dict) -> list[str]:
    """Fechas (AAAA-MM-DD, hora del este) con partidos en la temporada del scoreboard."""
    out = []
    for liga in scoreboard.get("leagues", []):
        for d in liga.get("calendar", []):
            if isinstance(d, str):
                out.append(fecha_et(d) if "T" in d else d[:10])
    return sorted(set(out))


def equipo(t: dict) -> dict:
    return {"team_id": str(t["id"]), "abbr": t.get("abbreviation"), "name": t.get("displayName"),
            "nickname": t.get("name") or t.get("shortDisplayName")}


def parse_scoreboard(data: dict, tipos: tuple[int, ...] = (2, 3, 5)) -> tuple[list[dict], list[dict]]:
    """Partidos del día de los tipos pedidos y equipos. Excluye el All-Star (equipos fuera de la liga)."""
    partidos, equipos = [], {}
    for e in data.get("events", []):
        season = e.get("season", {})
        if season.get("type") not in tipos:
            continue
        comp = e["competitions"][0]
        lados = {c["homeAway"]: c for c in comp["competitors"]}
        if "home" not in lados or "away" not in lados:
            continue
        h, a = lados["home"]["team"], lados["away"]["team"]
        if not h.get("abbreviation") or not a.get("abbreviation") or comp.get("type", {}).get("abbreviation") == "ALLSTAR":
            continue
        for t in (h, a):
            equipos[str(t["id"])] = equipo(t)
        partidos.append({
            "game_id": str(e["id"]),
            "season": temporada_desde_espn(season["year"]),
            "season_type": season["type"],
            "start_utc": utc_naive(e["date"]),
            "fecha": fecha_et(e["date"]),
            "home_id": str(h["id"]), "away_id": str(a["id"]),
            "neutral": bool(comp.get("neutralSite")),
            "status": e["status"]["type"]["name"],
            "home_pts": a_int(lados["home"].get("score")),
            "away_pts": a_int(lados["away"].get("score")),
            "periods": e["status"].get("period"),
        })
    return partidos, list(equipos.values())


# --- Box score ----------------------------------------------------------------------------------

LESION = re.compile(r"INJUR|SPRAIN|STRAIN|SORE|SURGERY|FRACTURE|ILLNESS|CONCUSSION|CONTUSION|TEAR|"
                    r"KNEE|ANKLE|FOOT|BACK|HAMSTRING|HIP|WRIST|HAND|SHOULDER|CALF|GROIN|PROTOCOL|"
                    r"BRUISE|SURGICAL|ACHILLES|RECOVERY|REST|PERSONAL|SUSPEN", re.I)


def tipo_ausencia(reason: str) -> str:
    """Clasifica el motivo de no jugar: 'tecnica' (decisión del entrenador) frente a 'lesion' (o
    cualquier ausencia ajena al rendimiento: descanso, suspensión, motivo personal)."""
    r = (reason or "").upper()
    if "COACH" in r:
        return "tecnica"
    if LESION.search(r) or "NOT WITH TEAM" in r or "G LEAGUE" in r or "INACTIVE" in r:
        return "lesion"
    return "otra"


def parse_box(summary: dict) -> tuple[list[dict], list[dict]]:
    """(jugadores que jugaron, jugadores convocados que no jugaron)."""
    equipos = summary.get("boxscore", {}).get("players", [])
    comp = summary["header"]["competitions"][0]
    casa = next(str(c["team"]["id"]) for c in comp["competitors"] if c["homeAway"] == "home")
    ids = [str(t["team"]["id"]) for t in equipos]
    game_id = str(summary["header"]["id"])
    jugaron, ausentes = [], []
    for t in equipos:
        team_id = str(t["team"]["id"])
        opp_id = next((i for i in ids if i != team_id), None)
        for bloque in t.get("statistics", []):
            labels = bloque.get("labels") or bloque.get("names") or []
            for a in bloque.get("athletes", []):
                ath = a["athlete"]
                pos = (ath.get("position") or {}).get("abbreviation")
                s = dict(zip(labels, a.get("stats") or []))
                mins = minutos(s.get("MIN"))
                if a.get("didNotPlay") or not a.get("stats") or mins <= 0:
                    reason = a.get("reason") or ""
                    ausentes.append({"game_id": game_id, "player_id": str(ath["id"]), "team_id": team_id,
                                     "name": ath.get("displayName"), "position": pos, "reason": reason,
                                     "kind": tipo_ausencia(reason)})
                    continue
                fgm, fga = hecho_intentado(s.get("FG"))
                tpm, tpa = hecho_intentado(s.get("3PT"))
                ftm, fta = hecho_intentado(s.get("FT"))
                jugaron.append({
                    "game_id": game_id, "player_id": str(ath["id"]), "team_id": team_id, "opp_id": opp_id,
                    "is_home": team_id == casa, "name": ath.get("displayName"), "position": pos,
                    "starter": bool(a.get("starter")), "minutes": round(mins, 2),
                    "pts": a_int(s.get("PTS")) or 0, "fgm": fgm, "fga": fga, "fg3m": tpm, "fg3a": tpa,
                    "ftm": ftm, "fta": fta, "oreb": a_int(s.get("OREB")) or 0, "dreb": a_int(s.get("DREB")) or 0,
                    "reb": a_int(s.get("REB")) or 0, "ast": a_int(s.get("AST")) or 0,
                    "stl": a_int(s.get("STL")) or 0, "blk": a_int(s.get("BLK")) or 0,
                    "tov": a_int(s.get("TO")) or 0, "pf": a_int(s.get("PF")) or 0,
                    "plus_minus": a_int(str(s.get("+/-", "")).replace("+", "")),
                })
    return jugaron, ausentes


def parse_team_box(summary: dict) -> list[dict]:
    """Totales de equipo (incluyen rebotes y pérdidas de equipo) y puntos por cuarto."""
    comp = summary["header"]["competitions"][0]
    lados = {str(c["team"]["id"]): c for c in comp["competitors"]}
    game_id = str(summary["header"]["id"])
    filas = []
    for t in summary.get("boxscore", {}).get("teams", []):
        team_id = str(t["team"]["id"])
        opp_id = next((i for i in lados if i != team_id), None)
        st = {}
        for s in t.get("statistics", []):
            st[s.get("abbreviation") or s.get("label")] = s.get("displayValue")
            st[s.get("label")] = s.get("displayValue")
        fgm, fga = hecho_intentado(st.get("FG"))
        tpm, tpa = hecho_intentado(st.get("3PT"))
        ftm, fta = hecho_intentado(st.get("FT"))
        cuartos = [a_int(x.get("displayValue") or x.get("value")) or 0 for x in lados[team_id].get("linescores", [])]
        oreb, dreb = a_int(st.get("OR")) or 0, a_int(st.get("DR")) or 0
        filas.append({
            "game_id": game_id, "team_id": team_id, "opp_id": opp_id,
            "is_home": lados[team_id]["homeAway"] == "home",
            "pts": a_int(lados[team_id].get("score")), "fgm": fgm, "fga": fga, "fg3m": tpm, "fg3a": tpa,
            "ftm": ftm, "fta": fta, "oreb": oreb, "dreb": dreb, "reb": a_int(st.get("REB")) or oreb + dreb,
            "ast": a_int(st.get("AST")) or 0, "stl": a_int(st.get("STL")) or 0, "blk": a_int(st.get("BLK")) or 0,
            "tov": a_int(st.get("ToTO")) if st.get("ToTO") is not None else a_int(st.get("TO")) or 0,
            "pf": a_int(st.get("PF")) or 0,
            "q1": cuartos[0] if len(cuartos) > 0 else None, "q2": cuartos[1] if len(cuartos) > 1 else None,
            "q3": cuartos[2] if len(cuartos) > 2 else None, "q4": cuartos[3] if len(cuartos) > 3 else None,
            "ot": sum(cuartos[4:]) if len(cuartos) > 4 else 0,
        })
    return filas


# --- Líneas del partido -------------------------------------------------------------------------

def _americana(v) -> float | None:
    try:
        return float(str(v).replace("+", ""))
    except (TypeError, ValueError):
        return None


def parse_lineas(summary: dict) -> dict | None:
    """Spread y total del pickcenter de ESPN (la línea previa al partido; en partidos pasados, la de
    cierre). spread_home negativo = local favorito."""
    picks = summary.get("pickcenter") or []
    if not picks:
        return None
    p = sorted(picks, key=lambda x: (x.get("provider") or {}).get("priority", 99))[0]
    comp = summary["header"]["competitions"][0]
    abbr = {c["homeAway"]: c["team"].get("abbreviation") for c in comp["competitors"]}
    spread = None
    m = re.match(r"([A-Z]+)\s+(-?\d+(?:\.\d+)?)", str(p.get("details") or ""))
    if m:
        valor = float(m.group(2))
        spread = valor if m.group(1) == abbr["home"] else -valor if m.group(1) == abbr["away"] else None
    elif str(p.get("details") or "").upper().startswith("EVEN"):
        spread = 0.0
    return {
        "game_id": str(summary["header"]["id"]), "source": f"espn:{(p.get('provider') or {}).get('name', '?')}",
        "kind": "cierre", "snapshot_at": None, "spread_home": spread, "total": p.get("overUnder"),
        "ml_home": _americana((p.get("homeTeamOdds") or {}).get("moneyLine")),
        "ml_away": _americana((p.get("awayTeamOdds") or {}).get("moneyLine")),
    }


# --- Lesiones -----------------------------------------------------------------------------------

def parse_lesiones(data: dict, snapshot_at: datetime) -> list[dict]:
    """Parte de lesiones de toda la liga (endpoint /injuries)."""
    filas = []
    for t in data.get("injuries", []):
        team_id = str(t.get("id") or (t.get("team") or {}).get("id") or "")
        for i in t.get("injuries", []):
            ath = i.get("athlete") or {}
            pid = str(ath.get("id") or "")
            if not pid:
                links = [l.get("href", "") for l in ath.get("links", [])]
                m = next((re.search(r"/id/(\d+)", h) for h in links if "/id/" in h), None)
                pid = m.group(1) if m else ""
            if not pid:
                continue
            det = i.get("details") or {}
            filas.append({
                "snapshot_at": snapshot_at, "source": "espn", "team_id": team_id, "player_id": pid,
                "name": ath.get("displayName"), "status": i.get("status") or "",
                "detail": " ".join(x for x in (det.get("type"), det.get("detail"), det.get("side")) if x)
                          or i.get("shortComment", "")[:120],
                "return_date": det.get("returnDate"),
            })
    return filas
