"""Proveedor completo basado en ESPN (sin clave). Alternativa a API-Football con la misma interfaz:
partidos del día, historial de cada equipo en todas sus competiciones, estadísticas de equipo y
jugador, y cuotas de DraftKings (1X2, doble oportunidad y total de goles).

Los fixtures se devuelven con la misma forma que API-Football para reutilizar el pipeline.
"""
from __future__ import annotations

import logging
import zlib
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from ..config import LEAGUES, SETTINGS
from ..db import Database, now_iso
from .espn import ESPN_STAT_MAP, _float, _int
from .http import CachedClient

log = logging.getLogger(__name__)

FINISHED = {"FT", "AET", "PEN"}
CODE_TO_LEAGUE = {code: (lid, name) for lid, (name, code) in LEAGUES.items()}


def league_id_for(slug: str) -> int:
    """Liga configurada -> su id de API-Football; otra competición -> id negativo estable."""
    if slug in CODE_TO_LEAGUE:
        return CODE_TO_LEAGUE[slug][0]
    return -(zlib.crc32(slug.encode()) % 1_000_000) - 1


def american_to_decimal(odds: str | int | float | None) -> float | None:
    try:
        v = float(str(odds).replace("+", ""))
    except (TypeError, ValueError):
        return None
    if v == 0:
        return None
    return round(1 + v / 100, 3) if v > 0 else round(1 + 100 / abs(v), 3)


class EspnProvider:
    BASE = "https://site.api.espn.com/apis/site/v2/sports/soccer"

    def __init__(self, db: Database):
        self.db = db
        self.client = CachedClient(db, self.BASE, min_interval=0.15)
        self.tz = ZoneInfo(SETTINGS.timezone)
        self._odds: dict[int, dict] = {}

    # ---------- conversión ----------
    def _status(self, comp: dict) -> str:
        t = (comp.get("status") or {}).get("type") or {}
        if t.get("completed"):
            return "FT"
        state = t.get("state")
        if state == "pre":
            return "PST" if "postpon" in (t.get("description") or "").lower() else "NS"
        return "LIVE" if state == "in" else (t.get("name") or "NS")

    def _to_fixture(self, ev: dict, slug: str, league_name: str | None = None) -> dict | None:
        comp = (ev.get("competitions") or [{}])[0]
        teams = {c.get("homeAway"): c for c in comp.get("competitors", [])}
        if "home" not in teams or "away" not in teams:
            return None
        kickoff = datetime.fromisoformat(ev["date"].replace("Z", "+00:00")).astimezone(self.tz)
        status = self._status(comp)

        def score(c):
            s = c.get("score")
            if isinstance(s, dict):
                s = s.get("value", s.get("displayValue"))
            v = _float(s)
            return int(v) if v is not None and status in FINISHED else None

        fid = int(ev["id"])
        if comp.get("odds"):
            self._odds[fid] = comp["odds"][0]
        return {
            "fixture": {"id": fid, "date": kickoff.isoformat(), "referee": None,
                        "status": {"short": status}, "venue": comp.get("venue") or {}},
            "league": {"id": league_id_for(slug), "slug": slug,
                       "name": league_name or CODE_TO_LEAGUE.get(slug, (0, slug))[1],
                       "season": (ev.get("season") or {}).get("year"), "round": None, "country": None},
            "teams": {s: {"id": int(teams[s]["team"]["id"]),
                          "name": teams[s]["team"].get("displayName") or teams[s]["team"].get("name")}
                      for s in ("home", "away")},
            "goals": {"home": score(teams["home"]), "away": score(teams["away"])},
        }

    # ---------- interfaz usada por el pipeline ----------
    def fixtures_by_date(self, day: str, ttl: float = 900) -> list[dict]:
        """Partidos cuya fecha LOCAL (zona configurada) es `day`, en las ligas configuradas."""
        d = date.fromisoformat(day)
        out, seen = [], set()
        for slug in CODE_TO_LEAGUE:
            for q in (d - timedelta(days=1), d, d + timedelta(days=1)):
                try:
                    body = self.client.get(f"/{slug}/scoreboard", {"dates": q.strftime("%Y%m%d")}, ttl)
                except Exception as exc:
                    log.warning("ESPN scoreboard %s %s: %s", slug, q, exc)
                    continue
                for ev in body.get("events", []):
                    fx = self._to_fixture(ev, slug)
                    if fx and fx["fixture"]["date"][:10] == day and fx["fixture"]["id"] not in seen:
                        seen.add(fx["fixture"]["id"])
                        out.append(fx)
        return out

    def team_last_fixtures(self, team_id: int, last: int) -> list[dict]:
        """Últimos partidos terminados del equipo en todas las competiciones (temporada actual y anterior)."""
        events: list[dict] = []
        year = datetime.now(self.tz).year
        for season in (None, year - 1):
            params = {"season": season} if season else {}
            try:
                body = self.client.get(f"/all/teams/{team_id}/schedule", params, ttl=6 * 3600)
            except Exception as exc:
                log.warning("ESPN schedule %s: %s", team_id, exc)
                continue
            for ev in body.get("events", []):
                slug = (ev.get("league") or {}).get("slug") or "all"
                name = (ev.get("league") or {}).get("name")
                fx = self._to_fixture(ev, slug, name)
                if fx and fx["fixture"]["status"]["short"] in FINISHED:
                    events.append(fx)
            if len(events) >= last:
                break
        uniq = {f["fixture"]["id"]: f for f in events}
        return sorted(uniq.values(), key=lambda f: f["fixture"]["date"], reverse=True)[:last]

    def store_fixture(self, fx: dict) -> dict:
        f, lg, t, g = fx["fixture"], fx["league"], fx["teams"], fx["goals"]
        row = {
            "fixture_id": f["id"], "date": f["date"][:10], "kickoff_utc": f["date"],
            "league_id": lg["id"], "league_name": lg.get("name"), "season": lg.get("season"),
            "round": lg.get("round"), "home_id": t["home"]["id"], "away_id": t["away"]["id"],
            "status": f["status"]["short"], "home_goals": g.get("home"), "away_goals": g.get("away"),
            "referee": f.get("referee"), "venue": (f.get("venue") or {}).get("fullName"),
            "espn_id": str(f["id"]), "updated_at": now_iso(),
        }
        old = self.db.q("SELECT referee, validated, validation_notes FROM matches WHERE fixture_id=?", (f["id"],))
        if old:
            row["referee"] = row["referee"] or old[0]["referee"]
            row["validated"], row["validation_notes"] = old[0]["validated"], old[0]["validation_notes"]
        self.db.upsert("matches", row)
        for side in ("home", "away"):
            self.db.conn.execute("INSERT OR IGNORE INTO teams (id, name, league_id, updated_at) VALUES (?,?,?,?)",
                                 (t[side]["id"], t[side]["name"], lg["id"] if lg["id"] > 0 else None, now_iso()))
            if lg["id"] > 0:
                self.db.conn.execute("UPDATE teams SET league_id=? WHERE id=?", (lg["id"], t[side]["id"]))
        return row

    def _summary(self, fid: int, slug: str, ttl: float) -> dict:
        try:
            return self.client.get(f"/{slug}/summary", {"event": fid}, ttl=ttl)
        except Exception:
            return self.client.get("/all/summary", {"event": fid}, ttl=ttl)

    def store_finished_match(self, fx: dict, with_players: bool = True) -> bool:
        match = self.store_fixture(fx)
        if match["status"] not in FINISHED:
            self.db.conn.commit()
            return False
        fid = match["fixture_id"]
        body = self._summary(fid, fx["league"].get("slug", "all"), ttl=-1)
        stats: dict[int, dict] = {}
        for tb in (body.get("boxscore") or {}).get("teams", []):
            vals = {col: None for col in ESPN_STAT_MAP.values()}
            for s in tb.get("statistics", []):
                col = ESPN_STAT_MAP.get(s.get("name"))
                if col:
                    vals[col] = _float(s.get("displayValue"))
            stats[int(tb["team"]["id"])] = vals
        h, a = match["home_id"], match["away_id"]
        if h not in stats or a not in stats or stats[h].get("corners") is None:
            self.db.conn.commit()
            return False
        for team, opp, is_home in ((h, a, 1), (a, h, 0)):
            s, o = stats[team], stats[opp]
            self.db.upsert("team_match_stats", {
                "fixture_id": fid, "team_id": team, "is_home": is_home,
                "goals": match["home_goals"] if is_home else match["away_goals"],
                "goals_against": match["away_goals"] if is_home else match["home_goals"],
                "corners": s["corners"], "corners_against": o["corners"],
                "yellow": s["yellow"], "red": s["red"], "yellow_against": o["yellow"], "red_against": o["red"],
                "shots": s["shots"], "shots_against": o["shots"],
                "shots_on": s["shots_on"], "shots_on_against": o["shots_on"],
                "fouls": s["fouls"], "possession": s["possession"], "xg": None,
            })
        for official in (body.get("gameInfo") or {}).get("officials", []) or []:
            if "referee" in str(official.get("position", {})).lower() or official.get("order") == 1:
                self.db.conn.execute("UPDATE matches SET referee=? WHERE fixture_id=?",
                                     (official.get("displayName") or official.get("fullName"), fid))
                break
        self._store_players(fid, body)  # vienen en el mismo resumen: no cuestan peticiones extra
        self.db.conn.commit()
        return True

    def _store_players(self, fid: int, body: dict) -> None:
        for r in body.get("rosters", []) or []:
            team_id = int(r["team"]["id"])
            for p in r.get("roster", []) or []:
                st = {s["name"]: s.get("value") for s in p.get("stats", []) or []}
                if not st.get("appearances") and not p.get("starter"):
                    continue
                # ESPN no da minutos: se aproximan con titularidad y cambios
                if p.get("starter"):
                    minutes = 70 if p.get("subbedOut") else 90
                else:
                    minutes = 20 if p.get("subbedIn") else 0
                self.db.upsert("player_match_stats", {
                    "fixture_id": fid, "player_id": int(p["athlete"]["id"]), "team_id": team_id,
                    "name": p["athlete"].get("displayName"),
                    "position": (p.get("position") or {}).get("abbreviation"), "minutes": minutes,
                    "shots": int(st.get("totalShots") or 0), "shots_on": int(st.get("shotsOnTarget") or 0),
                    "goals": int(st.get("totalGoals") or 0), "assists": int(st.get("goalAssists") or 0),
                    "yellow": int(st.get("yellowCards") or 0), "red": int(st.get("redCards") or 0),
                })

    # ---------- cuotas ----------
    def odds(self, fixture_id: int) -> dict:
        return self._odds.get(fixture_id, {})

    def parse_odds(self, o: dict) -> dict[tuple[str, str], float]:
        out: dict[tuple[str, str], float] = {}
        if not o:
            return out

        def close(node):
            node = node or {}
            return (node.get("close") or node.get("open") or {})

        ml = o.get("moneyline") or {}
        for side, sel in (("home", "1"), ("draw", "X"), ("away", "2")):
            dec = american_to_decimal(close(ml.get(side)).get("odds"))
            if dec:
                out[("1X2", sel)] = dec
        total = o.get("total") or {}
        for side, label in (("over", "Más de"), ("under", "Menos de")):
            c = close(total.get(side))
            line, dec = c.get("line"), american_to_decimal(c.get("odds"))
            if line and dec:
                out[("Goles totales", f"{label} {float(line[1:]):g}")] = dec
        spread = o.get("pointSpread") or {}
        for side, sel in (("home", "1X"), ("away", "X2")):
            c = close(spread.get(side))
            if c.get("line") == "+0.5":  # +0.5 asiático = gana o empata
                dec = american_to_decimal(c.get("odds"))
                if dec:
                    out[("Doble oportunidad", sel)] = dec
        return out


class NoValidator:
    """En modo ESPN no hay segunda fuente independiente: los partidos quedan como 'sin validar'."""

    def validate_fixture(self, fixture_id: int) -> int:
        return 0
