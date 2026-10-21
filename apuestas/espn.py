"""Fuente ESPN: el API público (sin clave ni cuota) que usa la propia web de ESPN.

No está documentado oficialmente: puede cambiar sin aviso, así que se usa con mesura (una petición
por segundo como mucho, tope por ejecución) y se para al primer bloqueo (403/429).

`EspnApi` imita la interfaz de `ApiFootball` y devuelve las respuestas ya convertidas al formato de
API-Football, así el recolector, el modelo y el chequeo de alineaciones funcionan igual con
cualquiera de las dos fuentes. Lo que da ESPN:

- partidos por liga y fecha (scoreboard) y el historial de cada equipo en TODAS sus competiciones;
- por partido (summary): córners, tarjetas, remates, tiros a puerta, atajadas, faltas, posesión;
  alineaciones con titulares; estadísticas por jugador; cuotas de DraftKings (1X2 y total de goles).

Los ids de ESPN se desplazan en `OFFSET` para no chocar nunca con los de API-Football en la base.
"""
from __future__ import annotations

import logging
import os
import time
from datetime import date, timedelta
from typing import Any

import requests

from .api_football import ApiError, PresupuestoAgotado

log = logging.getLogger(__name__)

BASE_URL = "https://site.api.espn.com/apis/site/v2/sports/soccer"
OFFSET = 1_000_000_000
MIN_INTERVALO = float(os.environ.get("APUESTAS_INTERVALO_ESPN", 1.0))

# id de liga (API-Football, el que usa la configuración) -> slug de ESPN.
LIGAS_ESPN = {
    2: "uefa.champions", 3: "uefa.europa", 848: "uefa.europa.conf", 531: "uefa.super_cup",
    39: "eng.1", 140: "esp.1", 78: "ger.1", 135: "ita.1", 61: "fra.1", 71: "bra.1",
    13: "conmebol.libertadores", 11: "conmebol.sudamericana", 16: "concacaf.champions", 15: "fifa.cwc",
    239: "col.1", 262: "mex.1", 128: "arg.1", 40: "eng.2", 88: "ned.1", 94: "por.1",
}
SLUG_A_LIGA = {v: k for k, v in LIGAS_ESPN.items()}

ESTADISTICAS = {
    "wonCorners": "Corner Kicks", "yellowCards": "Yellow Cards", "redCards": "Red Cards",
    "shotsOnTarget": "Shots on Goal", "totalShots": "Total Shots", "foulsCommitted": "Fouls",
    "possessionPct": "Ball Possession", "saves": "Goalkeeper Saves",
}


def _id(valor) -> int:
    return OFFSET + int(valor)


def _estado(status: dict) -> str:
    t = status.get("type") or {}
    nombre, estado = t.get("name", ""), t.get("state", "")
    if "POSTPONED" in nombre:
        return "PST"
    if "CANCEL" in nombre:
        return "CANC"
    if "ABANDON" in nombre or "SUSPENDED" in nombre:
        return "ABD"
    if estado == "pre":
        return "NS"
    if estado == "in":
        return "LIVE"
    if estado == "post":
        if "PEN" in nombre:
            return "PEN"
        if "AET" in nombre or "EXTRA" in nombre:
            return "AET"
        return "FT" if t.get("completed", True) else "ABD"
    return "TBD"


def _marcador(c: dict) -> int | None:
    s = c.get("score")
    if isinstance(s, dict):
        s = s.get("value", s.get("displayValue"))
    try:
        return int(float(s))
    except (TypeError, ValueError):
        return None


def evento_a_fixture(ev: dict, slug: str | None = None, temporada: int | None = None,
                     nombre_liga: str | None = None) -> dict:
    """Evento de scoreboard o de calendario de equipo -> item de /fixtures de API-Football."""
    comp = (ev.get("competitions") or [{}])[0]
    equipos = {c.get("homeAway"): c for c in comp.get("competitors") or []}
    slug = slug or (ev.get("league") or {}).get("slug")
    liga = ev.get("league") or {}
    status = comp.get("status") or ev.get("status") or {}
    final = _estado(status) in ("FT", "AET", "PEN")

    def equipo(lado: str) -> dict:
        t = (equipos.get(lado) or {}).get("team") or {}
        return {"id": _id(t["id"]), "name": t.get("displayName") or t.get("name")}

    return {
        "fixture": {"id": _id(ev["id"]), "date": ev.get("date") or comp.get("date"),
                    "status": {"short": _estado(status)}, "referee": None},
        "league": {"id": SLUG_A_LIGA.get(slug), "season": temporada or (ev.get("season") or {}).get("year"),
                   "name": nombre_liga or liga.get("name") or slug, "country": None},
        "teams": {"home": equipo("home"), "away": equipo("away")},
        "goals": {"home": _marcador(equipos.get("home") or {}) if final else None,
                  "away": _marcador(equipos.get("away") or {}) if final else None},
    }


def resumen_a_estadisticas(resumen: dict) -> list[dict]:
    out = []
    for t in (resumen.get("boxscore") or {}).get("teams") or []:
        valores = {s.get("name"): s.get("displayValue") for s in t.get("statistics") or []}
        if not valores:
            continue
        stats = []
        for clave, tipo in ESTADISTICAS.items():
            if clave in valores:
                v = valores[clave]
                stats.append({"type": tipo, "value": f"{v}%" if clave == "possessionPct" else v})
        out.append({"team": {"id": _id(t["team"]["id"])}, "statistics": stats})
    return out


def _minuto(jugada: dict) -> int | None:
    texto = str((jugada.get("clock") or {}).get("displayValue", "")).split("'")[0].split("+")[0]
    return int(texto) if texto.isdigit() else None


def _minutos_jugados(p: dict) -> int:
    cambio = next((_minuto(j) for j in p.get("plays") or [] if j.get("substitution")), None)
    if p.get("starter"):
        return cambio if p.get("subbedOut") and cambio else 90
    if p.get("subbedIn"):
        return max(1, 90 - (cambio or 70))
    return 0


def _posicion(p: dict) -> str | None:
    abrev = (p.get("position") or {}).get("abbreviation") or ""
    return "G" if abrev == "G" else (abrev[:1] if abrev and abrev != "SUB" else None)


def resumen_a_jugadores(resumen: dict) -> list[dict]:
    out = []
    for t in resumen.get("rosters") or []:
        jugadores = []
        for p in t.get("roster") or []:
            st = {s.get("name"): s.get("value", s.get("displayValue")) for s in p.get("stats") or []}
            num = lambda k: int(float(st.get(k) or 0))
            minutos = _minutos_jugados(p)
            jugadores.append({
                "player": {"id": _id(p["athlete"]["id"]), "name": p["athlete"].get("displayName")},
                "statistics": [{"games": {"minutes": minutos or None, "position": _posicion(p)},
                                "shots": {"total": num("totalShots"), "on": num("shotsOnTarget")},
                                "goals": {"total": num("totalGoals"), "assists": num("goalAssists")},
                                "cards": {"yellow": num("yellowCards"), "red": num("redCards")}}],
            })
        out.append({"team": {"id": _id(t["team"]["id"])}, "players": jugadores})
    return out


def resumen_a_alineaciones(resumen: dict) -> list[dict]:
    out = []
    for t in resumen.get("rosters") or []:
        xi = [{"player": {"id": _id(p["athlete"]["id"]), "name": p["athlete"].get("displayName"), "pos": _posicion(p)}}
              for p in t.get("roster") or [] if p.get("starter")]
        if xi:
            out.append({"team": {"id": _id(t["team"]["id"])}, "formation": t.get("formation"), "startXI": xi})
    return out


def americana_a_decimal(valor) -> float | None:
    try:
        v = float(valor)
    except (TypeError, ValueError):
        return None
    if v >= 100:
        return round(1 + v / 100, 3)
    if v <= -100:
        return round(1 + 100 / abs(v), 3)
    return None


def resumen_a_cuotas(resumen: dict) -> list[dict]:
    """pickcenter de ESPN -> respuesta de /odds de API-Football (1X2 y total de goles)."""
    casas = []
    for p in resumen.get("pickcenter") or []:
        apuestas = []
        ml = [("Home", (p.get("homeTeamOdds") or {}).get("moneyLine")), ("Draw", (p.get("drawOdds") or {}).get("moneyLine")),
              ("Away", (p.get("awayTeamOdds") or {}).get("moneyLine"))]
        valores = [{"value": v, "odd": str(americana_a_decimal(o))} for v, o in ml if americana_a_decimal(o)]
        if len(valores) == 3:
            apuestas.append({"name": "Match Winner", "values": valores})
        linea, over, under = p.get("overUnder"), americana_a_decimal(p.get("overOdds")), americana_a_decimal(p.get("underOdds"))
        if linea is not None and over and under:
            apuestas.append({"name": "Goals Over/Under", "values": [{"value": f"Over {linea}", "odd": str(over)},
                                                                   {"value": f"Under {linea}", "odd": str(under)}]})
        if apuestas:
            casas.append({"name": (p.get("provider") or {}).get("name", "ESPN"), "bets": apuestas})
    return [{"bookmakers": casas}] if casas else []


class EspnApi:
    """Misma interfaz que ApiFootball (lo que usan Collector y chequeo), con datos de ESPN."""

    def __init__(self, ligas: list[int], presupuesto: int = 400, session: requests.Session | None = None,
                 base_url: str = BASE_URL):
        self.ligas = [l for l in ligas if l in LIGAS_ESPN] or list(LIGAS_ESPN)
        self.session = session or requests.Session()
        self.base_url = base_url
        self.presupuesto = presupuesto
        self.peticiones = 0
        self.restantes_hoy = None          # ESPN no tiene cuota diaria
        self._ultima = 0.0
        self._resumenes: dict[int, dict] = {}

    def _get(self, path: str, **params: Any) -> dict:
        if self.peticiones >= self.presupuesto:
            raise PresupuestoAgotado(f"Presupuesto de {self.presupuesto} peticiones a ESPN agotado")
        espera = MIN_INTERVALO - (time.monotonic() - self._ultima)
        if espera > 0:
            time.sleep(espera)
        self._ultima = time.monotonic()
        self.peticiones += 1
        resp = self.session.get(f"{self.base_url}{path}", params=params, timeout=30)
        if resp.status_code in (403, 429):
            # Señal de bloqueo: no insistir.
            self.presupuesto = self.peticiones
            raise PresupuestoAgotado(f"ESPN respondió {resp.status_code}; se para para no ser bloqueados")
        if resp.status_code == 404:
            return {}
        resp.raise_for_status()
        return resp.json()

    # --- Interfaz de ApiFootball ----------------------------------------------------

    def partidos_por_fecha(self, fecha: str, zona_horaria: str) -> list[dict]:
        d = date.fromisoformat(fecha)
        # ESPN agrupa por su propio día (y no acepta rangos): se piden ese día y el siguiente, porque
        # los partidos de la noche americana caen en el día siguiente en UTC. El recolector filtra.
        out, vistos = [], set()
        for liga in self.ligas:
            slug = LIGAS_ESPN[liga]
            for dia in (d, d + timedelta(days=1)):
                data = self._get(f"/{slug}/scoreboard", dates=f"{dia:%Y%m%d}", limit=200)
                info = (data.get("leagues") or [{}])[0]
                temporada = (info.get("season") or {}).get("year")
                for ev in data.get("events") or []:
                    if ev["id"] not in vistos:
                        vistos.add(ev["id"])
                        out.append(evento_a_fixture(ev, slug, temporada, info.get("name")))
        return out

    def ultimos_partidos(self, team_id: int, n: int) -> list[dict]:
        espn_id = team_id - OFFSET
        eventos = []
        data = self._get(f"/all/teams/{espn_id}/schedule")
        eventos += data.get("events") or []
        jugados = [e for e in eventos if _estado((e.get("competitions") or [{}])[0].get("status") or {}) in
                   ("FT", "AET", "PEN")]
        if len(jugados) < n:
            # Principio de temporada: completar con la anterior.
            anterior = ((data.get("season") or {}).get("year") or date.today().year) - 1
            previos = self._get(f"/all/teams/{espn_id}/schedule", season=anterior).get("events") or []
            jugados += [e for e in previos if _estado((e.get("competitions") or [{}])[0].get("status") or {}) in
                        ("FT", "AET", "PEN")]
        jugados.sort(key=lambda e: e.get("date", ""), reverse=True)
        return [evento_a_fixture(e) for e in jugados[:n]]

    def _resumen(self, fixture_id: int) -> dict:
        if fixture_id not in self._resumenes:
            self._resumenes[fixture_id] = self._get("/all/summary", event=fixture_id - OFFSET)
        return self._resumenes[fixture_id]

    def partido(self, fixture_id: int) -> dict | None:
        r = self._resumen(fixture_id)
        comp = ((r.get("header") or {}).get("competitions") or [None])[0]
        if comp is None:
            return None
        ev = {"id": fixture_id - OFFSET, "date": comp.get("date"), "competitions": [comp],
              "league": (r.get("header") or {}).get("league") or {}}
        return evento_a_fixture(ev, temporada=((r.get("header") or {}).get("season") or {}).get("year"))

    def estadisticas_partido(self, fixture_id: int) -> list[dict]:
        return resumen_a_estadisticas(self._resumen(fixture_id))

    def jugadores_partido(self, fixture_id: int) -> list[dict]:
        return resumen_a_jugadores(self._resumen(fixture_id))

    def alineaciones(self, fixture_id: int) -> list[dict]:
        return resumen_a_alineaciones(self._resumen(fixture_id))

    def cuotas(self, fixture_id: int) -> list[dict]:
        return resumen_a_cuotas(self._resumen(fixture_id))

    def disponible(self) -> str:
        data = self._get("/eng.1/scoreboard")
        if "events" not in data:
            raise ApiError("ESPN no devolvió partidos")
        return f"OK ({len(data['events'])} partidos de Premier en su jornada actual)"
