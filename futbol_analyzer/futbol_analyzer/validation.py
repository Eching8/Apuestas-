"""Validación cruzada API-Football vs ESPN: confirma que resultados y estadísticas coinciden."""
from __future__ import annotations

import logging
import re
import unicodedata
from difflib import SequenceMatcher

from .config import LEAGUES, SETTINGS
from .db import Database, now_iso
from .sources.espn import Espn

log = logging.getLogger(__name__)

_STOP = {"fc", "cf", "sc", "ac", "afc", "club", "de", "cd", "ud", "sd", "ca", "fk", "sk", "as", "ss", "us", "1."}


def norm_name(name: str) -> str:
    name = unicodedata.normalize("NFKD", name or "").encode("ascii", "ignore").decode().lower()
    words = [w for w in re.split(r"[^a-z0-9.]+", name) if w and w not in _STOP]
    return " ".join(words)


def name_similarity(a: str, b: str) -> float:
    na, nb = norm_name(a), norm_name(b)
    if not na or not nb:
        return 0.0
    if na in nb or nb in na:
        return 0.95
    whole = SequenceMatcher(None, na, nb).ratio()
    # cada palabra del nombre más corto debe parecerse a alguna del otro
    # ("manchester city" vs "manchester united" comparte una palabra pero no la que los distingue)
    ta, tb = sorted((na.split(), nb.split()), key=len)
    worst = min(max(SequenceMatcher(None, x, y).ratio() for y in tb) for x in ta)
    return 0.4 * whole + 0.6 * worst


def find_espn_event(events: list[dict], home: str, away: str, threshold: float = 0.6) -> dict | None:
    best, best_score = None, 0.0
    for ev in events:
        score = (name_similarity(home, ev["home"]) + name_similarity(away, ev["away"])) / 2
        if score > best_score:
            best, best_score = ev, score
    return best if best_score >= threshold else None


class Validator:
    def __init__(self, db: Database, espn: Espn | None = None):
        self.db = db
        self.espn = espn or Espn(db)
        self._boards: dict[tuple[str, str], list[dict]] = {}

    def _events(self, code: str, day: str) -> list[dict]:
        if (code, day) not in self._boards:
            try:
                self._boards[(code, day)] = self.espn.scoreboard(code, day)
            except Exception as exc:  # la fuente secundaria nunca debe tumbar el pipeline
                log.warning("ESPN no disponible para %s %s: %s", code, day, exc)
                self._boards[(code, day)] = []
        return self._boards[(code, day)]

    def link_fixture(self, fixture_id: int) -> tuple[str, str] | None:
        """Asocia un partido de API-Football con su evento ESPN. Devuelve (código liga, id evento)."""
        m = self.db.q(
            """SELECT m.*, h.name AS home, a.name AS away FROM matches m
               JOIN teams h ON h.id=m.home_id JOIN teams a ON a.id=m.away_id WHERE fixture_id=?""",
            (fixture_id,),
        )
        if not m:
            return None
        m = m[0]
        code = LEAGUES.get(m["league_id"], (None, None))[1]
        if not code:
            return None
        if m["espn_id"]:
            return code, m["espn_id"]
        ev = find_espn_event(self._events(code, m["date"]), m["home"], m["away"])
        if not ev:
            return None
        self.db.conn.execute("UPDATE matches SET espn_id=? WHERE fixture_id=?", (ev["id"], fixture_id))
        self.db.conn.commit()
        return code, ev["id"]

    def validate_fixture(self, fixture_id: int) -> int:
        """Compara goles, córners, tarjetas y tiros. 1 = válido, -1 = discrepancia, 0 = sin datos."""
        link = self.link_fixture(fixture_id)
        if not link:
            return 0
        code, event_id = link
        try:
            espn = self.espn.match_stats(code, event_id)
        except Exception as exc:
            log.warning("No se pudo validar %s: %s", fixture_id, exc)
            return 0
        m = self.db.q("SELECT * FROM matches WHERE fixture_id=?", (fixture_id,))[0]
        tol = SETTINGS.validation_tolerance
        problems, checks = [], 0
        for side, team_id in (("home", m["home_id"]), ("away", m["away_id"])):
            row = self.db.q("SELECT * FROM team_match_stats WHERE fixture_id=? AND team_id=?", (fixture_id, team_id))
            if not row or side not in espn:
                continue
            row = row[0]
            for stat in ("corners", "yellow", "red", "shots_on", "shots"):
                a, b = row[stat], espn[side].get(stat)
                if a is None or b is None:
                    continue
                ok = abs(a - b) <= tol[stat]
                checks += 1
                self.db.upsert("validations", {
                    "fixture_id": fixture_id, "stat": stat, "team_side": side,
                    "primary_value": a, "secondary_value": b, "ok": int(ok), "checked_at": now_iso(),
                })
                if not ok:
                    problems.append(f"{stat}-{side}: {a:g} vs {b:g}")
        # Goles desde el marcador de ESPN
        ev = next((e for e in self._events(code, m["date"]) if e["id"] == event_id), None)
        if ev and ev["completed"] and m["home_goals"] is not None:
            checks += 1
            if (ev["home_goals"], ev["away_goals"]) != (m["home_goals"], m["away_goals"]):
                problems.append(f"marcador {m['home_goals']}-{m['away_goals']} vs ESPN {ev['home_goals']}-{ev['away_goals']}")
        status = 0 if checks == 0 else (-1 if problems else 1)
        self.db.conn.execute("UPDATE matches SET validated=?, validation_notes=? WHERE fixture_id=?",
                             (status, "; ".join(problems) or None, fixture_id))
        self.db.conn.commit()
        return status
