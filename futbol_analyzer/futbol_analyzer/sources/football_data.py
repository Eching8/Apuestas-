"""football-data.co.uk: CSV gratuitos (sin clave) usados como segunda fuente.

  * Ligas europeas (mmz4281/<temporada>/<código>.csv): marcador, córners, tarjetas, remates, tiros al
    arco, xG, árbitro (Premier) y cuotas de Bet365/Pinnacle/media del mercado.
  * Ligas "extra" (new/<país>.csv): marcador y cuotas 1X2 de cierre (Liga MX, MLS, Argentina, Brasil).
  * fixtures.csv: próximos partidos de las ligas europeas con cuotas (1X2, más/menos 2.5, hándicap asiático).

Se actualiza un par de veces por semana; los datos se guardan en caché 6 horas.
"""
from __future__ import annotations

import csv
import io
import logging
from datetime import date, datetime

import requests

from ..db import Database, now_iso
from ..validation import name_similarity
from .espn_provider import EspnProvider

log = logging.getLogger(__name__)

BASE = "https://www.football-data.co.uk"
# id de liga (API-Football) -> (código en football-data, tipo de archivo)
FD_LEAGUES = {
    39: ("E0", "main"), 140: ("SP1", "main"), 135: ("I1", "main"), 78: ("D1", "main"),
    61: ("F1", "main"), 94: ("P1", "main"), 88: ("N1", "main"),
    262: ("MEX", "new"), 253: ("USA", "new"), 128: ("ARG", "new"), 71: ("BRA", "new"),
}
# Nombres abreviados de football-data -> nombre de ESPN
ALIAS = {
    "Man City": "Manchester City", "Man United": "Manchester United", "Nott'm Forest": "Nottingham Forest",
    "Newcastle": "Newcastle United", "Wolves": "Wolverhampton Wanderers", "Tottenham": "Tottenham Hotspur",
    "West Ham": "West Ham United", "Brighton": "Brighton & Hove Albion", "Leeds": "Leeds United",
    "Ath Bilbao": "Athletic Club", "Ath Madrid": "Atletico Madrid", "Betis": "Real Betis", "Sociedad": "Real Sociedad",
    "Vallecano": "Rayo Vallecano", "Celta": "Celta Vigo", "Espanol": "Espanyol", "Alaves": "Alavés",
    "Inter": "Internazionale", "Milan": "AC Milan", "Roma": "AS Roma",
    "Leverkusen": "Bayer Leverkusen", "M'gladbach": "Borussia Monchengladbach", "Dortmund": "Borussia Dortmund",
    "Ein Frankfurt": "Eintracht Frankfurt", "FC Koln": "1. FC Köln", "Union Berlin": "1. FC Union Berlin",
    "Paris SG": "Paris Saint-Germain", "Sp Lisbon": "Sporting CP", "Sp Braga": "SC Braga",
    "PSV Eindhoven": "PSV Eindhoven", "Feyenoord": "Feyenoord Rotterdam",
    "Club America": "América", "UNAM": "Pumas UNAM", "Atl. San Luis": "Atlético de San Luis",
}


def _season_code(d: date) -> str:
    start = d.year if d.month >= 7 else d.year - 1
    return f"{start % 100:02d}{(start + 1) % 100:02d}"


def _f(v: str | None) -> float | None:
    try:
        return float(v) if v not in (None, "") else None
    except ValueError:
        return None


def _date(s: str) -> date:
    return datetime.strptime(s, "%d/%m/%Y" if len(s) == 10 else "%d/%m/%y").date()


class FootballData:
    def __init__(self, db: Database):
        self.db = db
        self.session = requests.Session()
        self.session.headers["User-Agent"] = "futbol-analyzer/1.0"
        self._rows: dict[str, list[dict]] = {}

    def _csv(self, path: str, ttl: float = 6 * 3600) -> list[dict]:
        if path in self._rows:
            return self._rows[path]
        key = f"{BASE}/{path}"
        text = self.db.cache_get(key, ttl)
        if text is None:
            try:
                resp = self.session.get(key, timeout=30)
                resp.raise_for_status()
                text = resp.content.decode("utf-8-sig", errors="replace")
                self.db.cache_put(key, text)
            except Exception as exc:
                log.warning("football-data no disponible (%s): %s", path, exc)
                text = ""
        rows = list(csv.DictReader(io.StringIO(text))) if text else []
        self._rows[path] = rows
        return rows

    def results(self, league_id: int, day: date) -> list[dict]:
        if league_id not in FD_LEAGUES:
            return []
        code, kind = FD_LEAGUES[league_id]
        if kind == "main":
            return [r for r in self._csv(f"mmz4281/{_season_code(day)}/{code}.csv") if r.get("FTHG")]
        out = []
        for r in self._csv(f"new/{code}.csv"):
            if r.get("HG") and r.get("Date") and abs((_date(r["Date"]) - day).days) <= 3:
                out.append({"Date": r["Date"], "HomeTeam": r["Home"], "AwayTeam": r["Away"],
                            "FTHG": r["HG"], "FTAG": r["AG"], "B365H": r.get("B365CH"),
                            "B365D": r.get("B365CD"), "B365A": r.get("B365CA")})
        return out

    def fixtures(self) -> list[dict]:
        return self._csv("fixtures.csv", ttl=3 * 3600)

    @staticmethod
    def find(rows: list[dict], day: date, home: str, away: str) -> dict | None:
        best, best_score = None, 0.0
        for r in rows:
            try:
                if abs((_date(r["Date"]) - day).days) > 1:
                    continue
            except (KeyError, ValueError):
                continue
            sh = name_similarity(ALIAS.get(r["HomeTeam"], r["HomeTeam"]), home)
            sa = name_similarity(ALIAS.get(r["AwayTeam"], r["AwayTeam"]), away)
            if min(sh, sa) < 0.6:
                continue
            if (sh + sa) / 2 > best_score:
                best, best_score = r, (sh + sa) / 2
        return best if best_score >= 0.7 else None

    @staticmethod
    def odds_from_row(r: dict) -> dict[tuple[str, str], float]:
        """Cuotas Bet365 (o media del mercado si falta) de una fila de football-data."""
        out: dict[tuple[str, str], float] = {}
        pairs = {("1X2", "1"): ("B365H", "AvgH"), ("1X2", "X"): ("B365D", "AvgD"), ("1X2", "2"): ("B365A", "AvgA"),
                 ("Goles totales", "Más de 2.5"): ("B365>2.5", "Avg>2.5"),
                 ("Goles totales", "Menos de 2.5"): ("B365<2.5", "Avg<2.5")}
        for key, cols in pairs.items():
            for c in cols:
                v = _f(r.get(c))
                if v and v > 1:
                    out[key] = v
                    break
        return out


class FootballDataValidator:
    """Valida partidos terminados guardados desde ESPN contra football-data.co.uk (sin coste de peticiones).
    También añade xG y árbitro cuando el CSV los trae."""

    STATS = (("goals", "FTHG", "FTAG"), ("corners", "HC", "AC"), ("yellow", "HY", "AY"),
             ("red", "HR", "AR"), ("shots", "HS", "AS"), ("shots_on", "HST", "AST"))

    def __init__(self, db: Database, fd: FootballData | None = None):
        self.db = db
        self.fd = fd or FootballData(db)

    def validate_fixture(self, fixture_id: int) -> int:
        from ..config import SETTINGS
        m = self.db.q("""SELECT m.*, h.name hn, a.name an FROM matches m JOIN teams h ON h.id=m.home_id
                         JOIN teams a ON a.id=m.away_id WHERE fixture_id=?""", (fixture_id,))
        if not m or m[0]["league_id"] not in FD_LEAGUES:
            return 0
        m = m[0]
        day = date.fromisoformat(m["date"])
        row = self.fd.find(self.fd.results(m["league_id"], day), day, m["hn"], m["an"])
        if not row:
            return 0
        tol = dict(SETTINGS.validation_tolerance)
        problems, checks = [], 0
        for stat, ch, ca in self.STATS:
            for side, team_id, col in (("home", m["home_id"], ch), ("away", m["away_id"], ca)):
                fdv = _f(row.get(col))
                ts = self.db.q("SELECT * FROM team_match_stats WHERE fixture_id=? AND team_id=?", (fixture_id, team_id))
                if fdv is None or not ts or ts[0][stat] is None:
                    continue
                ok = abs(ts[0][stat] - fdv) <= tol.get(stat, 0)
                checks += 1
                self.db.upsert("validations", {"fixture_id": fixture_id, "stat": f"{stat}@football-data",
                                               "team_side": side, "primary_value": ts[0][stat],
                                               "secondary_value": fdv, "ok": int(ok), "checked_at": now_iso()})
                if not ok:
                    problems.append(f"{stat}-{side}: ESPN {ts[0][stat]:g} vs football-data {fdv:g}")
        # enriquecer: xG y árbitro
        for team_id, col in ((m["home_id"], "HxG"), (m["away_id"], "AxG")):
            if _f(row.get(col)) is not None:
                self.db.conn.execute("UPDATE team_match_stats SET xg=? WHERE fixture_id=? AND team_id=?",
                                     (_f(row[col]), fixture_id, team_id))
        status = 0 if checks == 0 else (-1 if problems else 1)
        prev = m["validation_notes"]
        notes = "; ".join(problems) or None
        self.db.conn.execute(
            """UPDATE matches SET validated=?, validation_notes=?, referee=COALESCE(referee, ?) WHERE fixture_id=?""",
            (status if m["validated"] != -1 else -1, "; ".join(x for x in (prev, notes) if x) or None,
             row.get("Referee") or None, fixture_id))
        self.db.conn.commit()
        return status

    def validate_pending(self) -> dict:
        """Valida todo el historial aún sin validar de las ligas cubiertas (no consume peticiones de pago)."""
        ids = [r[0] for r in self.db.q(
            f"""SELECT fixture_id FROM matches WHERE status='FT' AND validated=0
                AND league_id IN ({",".join(str(x) for x in FD_LEAGUES)})""")]
        out = {1: 0, -1: 0, 0: 0}
        for fid in ids:
            out[self.validate_fixture(fid)] += 1
        return {"validados": out[1], "discrepancias": out[-1], "sin_datos": out[0]}


class ChainValidator:
    """Prueba varios validadores en orden y se queda con el primero que tenga datos."""

    def __init__(self, *validators):
        self.validators = validators

    def validate_fixture(self, fixture_id: int) -> int:
        for v in self.validators:
            res = v.validate_fixture(fixture_id)
            if res != 0:
                return res
        return 0

    def validate_pending(self) -> dict:
        out = {}
        for v in self.validators:
            if hasattr(v, "validate_pending"):
                out.update(v.validate_pending())
        return out


class EspnPlusProvider(EspnProvider):
    """ESPN + football-data: añade cuotas Bet365 (1X2 y goles) y el árbitro de los partidos de ligas europeas."""

    def __init__(self, db: Database, fd: FootballData | None = None):
        super().__init__(db)
        self.fd = fd or FootballData(db)
        self._fd_rows: dict[int, dict] = {}

    def fixtures_by_date(self, day: str, ttl: float = 900) -> list[dict]:
        fixtures = super().fixtures_by_date(day, ttl)
        d = date.fromisoformat(day)
        upcoming = self.fd.fixtures()
        for fx in fixtures:
            if fx["league"]["id"] not in FD_LEAGUES:
                continue
            row = self.fd.find(upcoming, d, fx["teams"]["home"]["name"], fx["teams"]["away"]["name"])
            if row:
                self._fd_rows[fx["fixture"]["id"]] = row
                fx["fixture"]["referee"] = fx["fixture"].get("referee") or row.get("Referee") or None
        return fixtures

    def odds(self, fixture_id: int) -> dict:
        return {"espn": super().odds(fixture_id), "fd": self._fd_rows.get(fixture_id)}

    def parse_odds(self, o: dict) -> dict[tuple[str, str], float]:
        out = FootballData.odds_from_row(o["fd"]) if o.get("fd") else {}
        for key, value in super().parse_odds(o.get("espn") or {}).items():
            out.setdefault(key, value)
        return out
