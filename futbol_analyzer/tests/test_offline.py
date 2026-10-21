"""Pruebas sin red: matemáticas del modelo y pipeline completo con un API simulado."""
import random
import unittest
from datetime import date, timedelta

from futbol_analyzer.config import SETTINGS
from futbol_analyzer.db import Database
from futbol_analyzer.markets import build_picks, match_markets
from futbol_analyzer.model import dist, prob_over, score_matrix
from futbol_analyzer.pipeline import DailyAnalyzer
from futbol_analyzer.settle import settle_pick
from futbol_analyzer.sources.api_football import ApiFootball, _map_odd
from futbol_analyzer.validation import find_espn_event


class FakeApi(ApiFootball):
    """Genera respuestas con el mismo formato que API-Football."""

    def __init__(self, db, today):
        self.db = db
        self.rng = random.Random(7)
        self.teams = {i: f"Equipo {i}" for i in range(1, 9)}
        self.today = today
        self.fixtures, self.stats, self.players = {}, {}, {}
        fid = 1000
        for d in range(40, 0, -3):  # historial: 14 jornadas
            ids = list(self.teams)
            self.rng.shuffle(ids)
            for h, a in zip(ids[::2], ids[1::2]):
                fid += 1
                self._make(fid, (today - timedelta(days=d)).isoformat(), h, a, finished=True)
        for h, a in ((1, 2), (3, 4), (5, 6), (7, 8)):
            fid += 1
            self._make(fid, today.isoformat(), h, a, finished=False)

    def _make(self, fid, day, h, a, finished):
        strength = {t: 0.7 + t * 0.1 for t in self.teams}
        r = self.rng
        hg = sum(r.random() < 0.15 * strength[h] for _ in range(10)) if finished else None
        ag = sum(r.random() < 0.11 * strength[a] for _ in range(10)) if finished else None
        self.fixtures[fid] = {
            "fixture": {"id": fid, "date": f"{day}T20:00:00-06:00", "referee": "Árbitro Uno",
                        "status": {"short": "FT" if finished else "NS"}, "venue": {"name": "Estadio"}},
            "league": {"id": 140, "name": "La Liga", "season": 2026, "round": "R", "country": "Spain"},
            "teams": {"home": {"id": h, "name": self.teams[h]}, "away": {"id": a, "name": self.teams[a]}},
            "goals": {"home": hg, "away": ag},
        }
        if finished:
            def block(t):
                shots = r.randint(6, 20)
                return {"team": {"id": t}, "statistics": [
                    {"type": "Corner Kicks", "value": r.randint(1, 10)},
                    {"type": "Yellow Cards", "value": r.randint(0, 4) or None},
                    {"type": "Red Cards", "value": None},
                    {"type": "Total Shots", "value": shots},
                    {"type": "Shots on Goal", "value": r.randint(1, max(1, shots // 2))},
                    {"type": "Ball Possession", "value": "50%"},
                    {"type": "expected_goals", "value": "1.21"}]}
            self.stats[fid] = [block(h), block(a)]
            self.players[fid] = [{"team": {"id": t}, "players": [
                {"player": {"id": t * 100 + k, "name": f"Jugador {t}-{k}"},
                 "statistics": [{"games": {"minutes": 90, "position": "F"},
                                 "shots": {"total": r.randint(0, 4), "on": r.randint(0, 2)},
                                 "goals": {}, "cards": {}}]} for k in range(3)]} for t in (h, a)]

    def fixtures_by_date(self, day, ttl=0):
        return [f for f in self.fixtures.values() if f["fixture"]["date"][:10] == day]

    def team_last_fixtures(self, team_id, last):
        fx = [f for f in self.fixtures.values() if f["fixture"]["status"]["short"] == "FT"
              and team_id in (f["teams"]["home"]["id"], f["teams"]["away"]["id"])]
        return sorted(fx, key=lambda f: f["fixture"]["date"], reverse=True)[:last]

    def fixture_statistics(self, fid):
        return self.stats.get(fid, [])

    def fixture_players(self, fid):
        return self.players.get(fid, [])

    def odds(self, fid):
        return [{"bookmakers": [{"bets": [
            {"name": "Match Winner", "values": [{"value": "Home", "odd": "2.10"}, {"value": "Draw", "odd": "3.40"},
                                                {"value": "Away", "odd": "3.50"}]},
            {"name": "Goals Over/Under", "values": [{"value": "Over 1.5", "odd": "1.40"}, {"value": "Under 1.5", "odd": "2.90"}]},
            {"name": "Corners Over Under", "values": [{"value": "Over 7.5", "odd": "1.55"}, {"value": "Under 7.5", "odd": "2.40"}]},
            {"name": "Cards Over/Under", "values": [{"value": "Over 2.5", "odd": "1.50"}, {"value": "Under 2.5", "odd": "2.50"}]},
        ]}]}]


class FakeValidator:
    def validate_fixture(self, fid):
        return 0


class ModelTests(unittest.TestCase):
    def test_distributions_sum_to_one(self):
        for disp in (None, 5.0, 20.0):
            self.assertAlmostEqual(sum(dist(9.8, disp)), 1.0, places=6)
        m = score_matrix(1.6, 1.1)
        self.assertAlmostEqual(sum(map(sum, m)), 1.0, places=9)

    def test_overdispersion_widens_tails(self):
        self.assertGreater(prob_over(dist(10, 5.0), 14.5), prob_over(dist(10, None), 14.5))

    def test_odds_mapping(self):
        self.assertEqual(_map_odd("Corners Over Under", "Over 9.5"), ("Córners totales", "Más de 9.5"))
        self.assertEqual(_map_odd("Match Winner", "Draw"), ("1X2", "X"))

    def test_american_odds(self):
        from futbol_analyzer.sources.espn_provider import american_to_decimal
        self.assertEqual(american_to_decimal("+125"), 2.25)
        self.assertAlmostEqual(american_to_decimal("-200"), 1.5)

    def test_market_implied_goals(self):
        from futbol_analyzer.model import market_implied_goals
        lh, la = market_implied_goals({("1X2", "1"): 1.70, ("1X2", "X"): 3.90, ("1X2", "2"): 5.00,
                                       ("Goles totales", "Más de 2.5"): 1.80, ("Goles totales", "Menos de 2.5"): 2.00})
        self.assertGreater(lh, la)
        self.assertTrue(2.2 < lh + la < 3.2)

    def test_football_data_matching(self):
        from futbol_analyzer.sources.football_data import FootballData
        rows = [{"Date": "19/10/2026", "HomeTeam": "Nott'm Forest", "AwayTeam": "Arsenal"},
                {"Date": "19/10/2026", "HomeTeam": "Man City", "AwayTeam": "Everton"}]
        r = FootballData.find(rows, date(2026, 10, 18), "Nottingham Forest", "Arsenal")
        self.assertEqual(r["HomeTeam"], "Nott'm Forest")
        self.assertIsNone(FootballData.find(rows, date(2026, 10, 18), "Manchester United", "Everton"))

    def test_name_matching(self):
        events = [{"home": "Real Madrid", "away": "FC Barcelona"}, {"home": "Atlético Madrid", "away": "Sevilla"}]
        self.assertEqual(find_espn_event(events, "Real Madrid CF", "Barcelona")["home"], "Real Madrid")


class PipelineTests(unittest.TestCase):
    def test_end_to_end(self):
        today = date(2026, 10, 21)
        db = Database(":memory:")
        api = FakeApi(db, today)
        analyzer = DailyAnalyzer(db, api=api, validator=FakeValidator())
        result = analyzer.run(today)

        self.assertEqual(len(result["partidos"]), 4)
        self.assertGreater(db.q("SELECT COUNT(*) FROM team_match_stats")[0][0], 50)
        self.assertGreater(db.q("SELECT COUNT(*) FROM player_match_stats")[0][0], 0)
        self.assertEqual(db.q("SELECT COUNT(DISTINCT team_id) FROM team_ratings")[0][0], 8)
        m = result["partidos"][0]
        self.assertTrue(m["cuotas_disponibles"])
        for stat in ("goals", "corners", "cards", "shots", "shots_on"):
            self.assertGreater(m["esperado"][stat]["local"], 0)
        # complementos Más/Menos suman 1
        proj_picks = {(p["market"], p["selection"]): p for p in m["mercados_optimos"]}
        self.assertTrue(all(0 < p["prob"] < 1 for p in proj_picks.values()))
        for c in result["combinadas"]:
            self.assertGreaterEqual(c["probabilidad"], SETTINGS.combo_min_prob)
            self.assertEqual(len({s["partido"] for s in c["selecciones"]}), len(c["selecciones"]))

        # liquidación: marcamos el partido como terminado y comprobamos que se resuelven los picks
        fid = result["partidos"][0]["fixture_id"]
        fx = api.fixtures[fid]
        fx["fixture"]["status"]["short"] = "FT"
        fx["goals"] = {"home": 2, "away": 1}
        api.stats[fid] = [{"team": {"id": fx["teams"]["home"]["id"]}, "statistics": [
            {"type": "Corner Kicks", "value": 6}, {"type": "Yellow Cards", "value": 2}]},
            {"team": {"id": fx["teams"]["away"]["id"]}, "statistics": [
            {"type": "Corner Kicks", "value": 3}, {"type": "Yellow Cards", "value": 1}]}]
        api.store_finished_match(fx, with_players=False)
        self.assertEqual(settle_pick(db, fid, "1X2", "1"), 1)
        self.assertEqual(settle_pick(db, fid, "Córners totales", "Más de 8.5"), 1)
        self.assertEqual(settle_pick(db, fid, "Tarjetas totales", "Más de 3.5"), 0)
        self.assertEqual(settle_pick(db, fid, "Goles visitante", "Menos de 1.5"), 1)


if __name__ == "__main__":
    unittest.main()
