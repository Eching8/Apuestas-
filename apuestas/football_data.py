"""Validación cruzada con football-data.org (fuente independiente de API-Football).

Compara horario y marcador final de los partidos guardados con los de football-data.org.
El plan gratuito cubre las principales ligas europeas, Champions League, Brasileirão y
algunas competiciones más; los partidos fuera de esa cobertura quedan "sin verificar".
"""
from __future__ import annotations

import difflib
import re
import unicodedata
from datetime import datetime

import requests

from .db import Database

BASE_URL = "https://api.football-data.org/v4"
_RUIDO = re.compile(r"\b(fc|cf|ac|sc|afc|cd|ud|sd|rc|rcd|club|de|futbol|calcio|ss|as|sv|vfb|vfl|tsg|1\.)\b")


def _norm(name: str) -> str:
    name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode().lower()
    name = _RUIDO.sub(" ", name)
    return re.sub(r"[^a-z0-9]+", " ", name).strip()


def _similar(a: str, b: str) -> float:
    a, b = _norm(a), _norm(b)
    if a and b and (a in b or b in a):
        return 1.0
    return difflib.SequenceMatcher(None, a, b).ratio()


class FootballData:
    def __init__(self, api_key: str, session: requests.Session | None = None):
        self.session = session or requests.Session()
        self.session.headers.update({"X-Auth-Token": api_key})

    def matches(self, date_from: str, date_to: str) -> list[dict]:
        resp = self.session.get(f"{BASE_URL}/matches", params={"dateFrom": date_from, "dateTo": date_to}, timeout=30)
        resp.raise_for_status()
        return resp.json().get("matches", [])


def _team_names(t: dict) -> list[str]:
    return [n for n in (t.get("name"), t.get("shortName"), t.get("tla")) if n]


def _best_match(fx, candidates: list[dict]) -> tuple[dict | None, float]:
    best, score = None, 0.0
    for m in candidates:
        s = min(max(_similar(fx["home_name"], n) for n in _team_names(m["homeTeam"])),
                max(_similar(fx["away_name"], n) for n in _team_names(m["awayTeam"])))
        if s > score:
            best, score = m, s
    return best, score


def validate_day(db: Database, client: FootballData, fecha: str) -> dict[str, int]:
    """Valida los partidos guardados de un día. Devuelve el conteo de ok / discrepancias / sin cobertura."""
    fixtures = db.fixtures_on(fecha)
    # Un día de margen por la diferencia de zona horaria.
    d = datetime.fromisoformat(fecha).date()
    otros = client.matches((d.fromordinal(d.toordinal() - 1)).isoformat(), (d.fromordinal(d.toordinal() + 1)).isoformat())
    cuenta = {"ok": 0, "discrepancia": 0, "sin_cobertura": 0}
    with db.tx():
        for fx in fixtures:
            m, score = _best_match(fx, otros)
            if m is None or score < 0.75:
                cuenta["sin_cobertura"] += 1
                continue
            problemas = []
            kick_a = datetime.fromisoformat(fx["date_utc"])
            kick_b = datetime.fromisoformat(m["utcDate"].replace("Z", "+00:00"))
            if abs((kick_a - kick_b).total_seconds()) > 3 * 3600:
                problemas.append(f"hora {fx['date_utc']} vs {m['utcDate']}")
            if fx["status"] == "FT" and m.get("status") == "FINISHED":
                ft = (m.get("score") or {}).get("fullTime") or {}
                if (ft.get("home"), ft.get("away")) != (fx["home_goals"], fx["away_goals"]):
                    problemas.append(f"marcador {fx['home_goals']}-{fx['away_goals']} vs {ft.get('home')}-{ft.get('away')}")
            ok = not problemas
            cuenta["ok" if ok else "discrepancia"] += 1
            db.save_validation(fx["id"], "football-data.org", ok, "; ".join(problemas) or "coincide")
    return cuenta
