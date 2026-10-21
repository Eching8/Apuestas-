"""Modo híbrido: ESPN (gratis, sin límite) para partidos, historial y estadísticas; API-Football
(100 peticiones/día en el plan gratis) para lo que ESPN no da:

  * cuotas de Bet365 en córners, tarjetas, tiros, remates, ambos marcan y remates por jugador
  * árbitro de cada partido
  * validación cruzada de los partidos terminados (marcador, córners, tarjetas, tiros)

Gasto típico por día: 1 petición por fecha consultada + 1 por partido para cuotas
+ 1 por partido terminado validado (con tope `validation_budget`).
"""
from __future__ import annotations

import logging
from datetime import date, datetime

from ..config import SETTINGS
from ..db import Database, now_iso
from ..validation import find_espn_event
from .api_football import ApiFootball
from .football_data import EspnPlusProvider

log = logging.getLogger(__name__)


class HybridProvider(EspnPlusProvider):
    def __init__(self, db: Database, af: ApiFootball | None = None):
        super().__init__(db)
        self.af = af or ApiFootball(db)
        self.af_map: dict[int, dict] = {}  # id ESPN -> fixture de API-Football

    def _link_day(self, day: str, fixtures: list[dict]) -> None:
        today = datetime.now(self.tz).date()
        if abs((date.fromisoformat(day) - today).days) > 1:
            return  # el plan gratis solo permite ayer, hoy y mañana
        try:
            af_fixtures = self.af.fixtures_by_date(day, ttl=1800)
        except Exception as exc:
            log.warning("API-Football no disponible para %s: %s", day, exc)
            return
        candidates = [{"home": f["teams"]["home"]["name"], "away": f["teams"]["away"]["name"],
                       "kick": f["fixture"]["date"], "af": f} for f in af_fixtures]
        for fx in fixtures:
            kick = datetime.fromisoformat(fx["fixture"]["date"])
            near = [c for c in candidates
                    if abs((datetime.fromisoformat(c["kick"]) - kick).total_seconds()) <= 3 * 3600]
            match = find_espn_event(near, fx["teams"]["home"]["name"], fx["teams"]["away"]["name"])
            if match:
                af = match["af"]
                self.af_map[fx["fixture"]["id"]] = af
                ref = (af["fixture"].get("referee") or "").split(",")[0].strip() or None
                fx["fixture"]["referee"] = ref

    def fixtures_by_date(self, day: str, ttl: float = 900) -> list[dict]:
        fixtures = super().fixtures_by_date(day, ttl)
        if fixtures:
            self._link_day(day, fixtures)
        return fixtures

    def odds(self, fixture_id: int) -> dict:
        af_resp = []
        af = self.af_map.get(fixture_id)
        if af:
            try:
                af_resp = self.af.odds(af["fixture"]["id"])
            except Exception as exc:
                log.warning("Sin cuotas de API-Football para %s: %s", fixture_id, exc)
        return {"af": af_resp, "base": super().odds(fixture_id)}

    def parse_odds(self, o: dict) -> dict[tuple[str, str], float]:
        """Bet365 vía API-Football primero; football-data y DraftKings (ESPN) completan lo que falte."""
        out = self.af.parse_odds(o.get("af") or [])
        for key, value in super().parse_odds(o.get("base") or {}).items():
            out.setdefault(key, value)
        return out


class ApiFootballValidator:
    """Compara lo guardado desde ESPN con las estadísticas de API-Football del mismo partido."""

    STATS = ("corners", "yellow", "red", "shots_on", "shots")

    def __init__(self, db: Database, provider: HybridProvider):
        self.db = db
        self.provider = provider
        self.used = 0

    def validate_fixture(self, fixture_id: int) -> int:
        af = self.provider.af_map.get(fixture_id)
        if not af or self.used >= SETTINGS.validation_budget:
            return 0
        m = self.db.q("SELECT * FROM matches WHERE fixture_id=?", (fixture_id,))
        if not m:
            return 0
        m = m[0]
        try:
            self.used += 1
            af_stats = self.provider.af.parse_statistics(self.provider.af.fixture_statistics(af["fixture"]["id"]))
        except Exception as exc:
            log.warning("No se pudo validar %s: %s", fixture_id, exc)
            return 0
        tol = SETTINGS.validation_tolerance
        problems, checks = [], 0
        af_goals = (af["goals"]["home"], af["goals"]["away"])
        if None not in af_goals and m["home_goals"] is not None:
            checks += 1
            if af_goals != (m["home_goals"], m["away_goals"]):
                problems.append(f"marcador ESPN {m['home_goals']}-{m['away_goals']} vs API-Football {af_goals[0]}-{af_goals[1]}")
        for side, team_id in (("home", m["home_id"]), ("away", m["away_id"])):
            row = self.db.q("SELECT * FROM team_match_stats WHERE fixture_id=? AND team_id=?", (fixture_id, team_id))
            other = af_stats.get(af["teams"][side]["id"])
            if not row or not other:
                continue
            for stat in self.STATS:
                a, b = row[0][stat], other.get(stat)
                if a is None or b is None:
                    continue
                ok = abs(a - b) <= tol[stat]
                checks += 1
                self.db.upsert("validations", {
                    "fixture_id": fixture_id, "stat": stat, "team_side": side,
                    "primary_value": a, "secondary_value": b, "ok": int(ok), "checked_at": now_iso(),
                })
                if not ok:
                    problems.append(f"{stat}-{side}: ESPN {a:g} vs API-Football {b:g}")
        ref = (af["fixture"].get("referee") or "").split(",")[0].strip()
        status = 0 if checks == 0 else (-1 if problems else 1)
        self.db.conn.execute(
            "UPDATE matches SET validated=?, validation_notes=?, referee=COALESCE(?, referee) WHERE fixture_id=?",
            (status, "; ".join(problems) or None, ref or None, fixture_id))
        self.db.conn.commit()
        return status
