import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

import apuestas.espn as espn
from apuestas.api_football import PresupuestoAgotado
from apuestas.bzzoiro import alineacion_basica, buscar, evento_basico
from apuestas.chequeo import parse_alineaciones
from apuestas.collector import parse_fixture, parse_odds, parse_players, parse_statistics
from apuestas.espn import OFFSET, EspnApi, americana_a_decimal, evento_a_fixture
from apuestas.odds import OddsBook, _odds_for
from apuestas.model import Market
from apuestas.registro import Registro
from apuestas.sgo import cuotas_de_evento, stat_de


def competidor(lado, tid, nombre, goles):
    return {"homeAway": lado, "team": {"id": str(tid), "displayName": nombre}, "score": str(goles)}


EVENTO = {"id": "555", "date": "2026-10-22T19:00Z", "competitions": [{
    "status": {"type": {"name": "STATUS_FULL_TIME", "state": "post", "completed": True}},
    "competitors": [competidor("home", 1, "Local FC", 2), competidor("away", 2, "Visitante CF", 1)]}]}

RESUMEN = {
    "boxscore": {"teams": [
        {"team": {"id": "1"}, "statistics": [{"name": "wonCorners", "displayValue": "6"},
                                             {"name": "yellowCards", "displayValue": "2"},
                                             {"name": "redCards", "displayValue": "0"},
                                             {"name": "shotsOnTarget", "displayValue": "5"},
                                             {"name": "totalShots", "displayValue": "14"},
                                             {"name": "saves", "displayValue": "3"},
                                             {"name": "possessionPct", "displayValue": "58.1"}]},
        {"team": {"id": "2"}, "statistics": [{"name": "wonCorners", "displayValue": "3"},
                                             {"name": "yellowCards", "displayValue": "4"},
                                             {"name": "redCards", "displayValue": "1"},
                                             {"name": "shotsOnTarget", "displayValue": "4"},
                                             {"name": "totalShots", "displayValue": "9"},
                                             {"name": "saves", "displayValue": "3"}]}]},
    "rosters": [
        {"team": {"id": "1"}, "formation": "4-3-3", "roster": [
            {"athlete": {"id": "10", "displayName": "Portero Uno"}, "starter": True, "position": {"abbreviation": "G"},
             "stats": []},
            {"athlete": {"id": "11", "displayName": "Delantero Uno"}, "starter": True, "subbedOut": True,
             "position": {"abbreviation": "F"}, "plays": [{"clock": {"displayValue": "70'"}, "substitution": True}],
             "stats": [{"name": "totalShots", "value": 4}, {"name": "shotsOnTarget", "value": 2},
                       {"name": "totalGoals", "value": 1}]},
            {"athlete": {"id": "12", "displayName": "Suplente Uno"}, "starter": False, "subbedIn": True,
             "position": {"abbreviation": "SUB"}, "plays": [{"clock": {"displayValue": "70'"}, "substitution": True}],
             "stats": [{"name": "totalShots", "value": 1}]},
            {"athlete": {"id": "13", "displayName": "No Jugó"}, "starter": False, "stats": []}]},
        {"team": {"id": "2"}, "roster": [
            {"athlete": {"id": "20", "displayName": "Portero Dos"}, "starter": True, "position": {"abbreviation": "G"},
             "stats": []}]}],
    "pickcenter": [{"provider": {"name": "DraftKings"}, "overUnder": 2.5, "overOdds": -120, "underOdds": 100,
                    "homeTeamOdds": {"moneyLine": 150}, "awayTeamOdds": {"moneyLine": 190},
                    "drawOdds": {"moneyLine": 230}}],
}


class EspnTest(unittest.TestCase):
    def test_fixture_y_estados(self):
        fx = parse_fixture(evento_a_fixture(EVENTO, "eng.1", 2026, "Premier League"), "UTC")
        self.assertEqual((fx["id"], fx["home_id"], fx["league_id"], fx["status"]), (OFFSET + 555, OFFSET + 1, 39, "FT"))
        self.assertEqual((fx["home_goals"], fx["away_goals"]), (2, 1))
        previo = {**EVENTO, "competitions": [{**EVENTO["competitions"][0],
                                              "status": {"type": {"name": "STATUS_SCHEDULED", "state": "pre"}}}]}
        f2 = parse_fixture(evento_a_fixture(previo, "eng.1"), "UTC")
        self.assertEqual((f2["status"], f2["home_goals"]), ("NS", None))

    def test_resumen(self):
        fx = parse_fixture(evento_a_fixture(EVENTO, "eng.1"), "UTC")
        h, a = parse_statistics(fx, espn.resumen_a_estadisticas(RESUMEN))
        self.assertEqual((h["corners"], h["shots_on"], h["saves"], h["possession"]), (6, 5, 3, 58.1))
        self.assertEqual((a["cards"], a["goals"]), (5, 1))
        jugadores = {r["name"]: r for r in parse_players(fx["id"], espn.resumen_a_jugadores(RESUMEN))}
        self.assertEqual(jugadores["Delantero Uno"]["minutes"], 70)
        self.assertEqual(jugadores["Suplente Uno"]["minutes"], 20)
        self.assertNotIn("No Jugó", jugadores)
        self.assertEqual(jugadores["Portero Uno"]["position"], "G")
        al = parse_alineaciones(espn.resumen_a_alineaciones(RESUMEN))
        self.assertEqual(len(al[OFFSET + 1]["titulares"]), 2)
        filas = {(b, v): o for _, b, v, o in parse_odds(espn.resumen_a_cuotas(RESUMEN))}
        self.assertEqual(filas[("Match Winner", "Home")], 2.5)
        self.assertAlmostEqual(filas[("Goals Over/Under", "Over 2.5")], 1.833, places=3)

    def test_americana(self):
        self.assertEqual(americana_a_decimal(150), 2.5)
        self.assertAlmostEqual(americana_a_decimal(-200), 1.5)
        self.assertIsNone(americana_a_decimal("x"))

    def test_cliente_cachea_y_para_si_lo_bloquean(self):
        class Resp:
            def __init__(self, code, data):
                self.status_code, self._data = code, data

            def json(self):
                return self._data

            def raise_for_status(self):
                pass

        class Sesion:
            def __init__(self):
                self.urls = []

            def get(self, url, params=None, timeout=None):
                self.urls.append(url)
                if url.endswith("/scoreboard"):
                    return Resp(403, {})
                return Resp(200, RESUMEN)

        intervalo, espn.MIN_INTERVALO = espn.MIN_INTERVALO, 0.0
        try:
            s = Sesion()
            api = EspnApi([39], presupuesto=10, session=s)
            api.estadisticas_partido(OFFSET + 555)
            api.jugadores_partido(OFFSET + 555)
            api.cuotas(OFFSET + 555)
            self.assertEqual(len(s.urls), 1)                # un solo resumen por partido
            with self.assertRaises(PresupuestoAgotado):
                api.partidos_por_fecha("2026-10-22", "UTC")
            with self.assertRaises(PresupuestoAgotado):    # tras un bloqueo no vuelve a intentarlo
                api.alineaciones(OFFSET + 777)
        finally:
            espn.MIN_INTERVALO = intervalo


class SgoTest(unittest.TestCase):
    def test_stat_de(self):
        self.assertEqual(stat_de("cornerKicks"), "corners")
        self.assertEqual(stat_de("yellowCards"), "cards")
        self.assertEqual(stat_de("shots_onGoal"), "shots_on")
        self.assertEqual(stat_de("shots"), "shots_total")
        self.assertEqual(stat_de("points"), "goals")
        self.assertIsNone(stat_de("possession"))
        # Nombres reales de SportsGameOdds (octubre de 2026).
        self.assertEqual(stat_de("weightedCards"), "cards")
        self.assertEqual(stat_de("goalie_saves"), "saves")
        self.assertEqual(stat_de("bothTeamsScored"), "btts")
        self.assertEqual(stat_de("shots_onGoal"), "shots_on")

    def test_cuotas(self):
        ev = {"odds": {
            "cornerKicks-all-game-ou-over": {"statID": "cornerKicks", "statEntityID": "all", "periodID": "game",
                                             "betTypeID": "ou", "sideID": "over",
                                             "byBookmaker": {"bet365": {"odds": "-110", "overUnder": "9.5"}}},
            "yellowCards-home-game-ou-under": {"statID": "yellowCards", "statEntityID": "home", "periodID": "game",
                                               "betTypeID": "ou", "sideID": "under",
                                               "byBookmaker": {"pinnacle": {"odds": "+105", "overUnder": "2.5"}}},
            "points-home-game-ml3way-home": {"statID": "points", "statEntityID": "home", "periodID": "game",
                                             "betTypeID": "ml3way", "sideID": "home",
                                             "byBookmaker": {"pinnacle": {"odds": "+120"}}},
            "cornerKicks-all-1h-ou-over": {"statID": "cornerKicks", "statEntityID": "all", "periodID": "1h",
                                           "betTypeID": "ou", "sideID": "over",
                                           "byBookmaker": {"bet365": {"odds": "-110", "overUnder": "4.5"}}},
        }}
        filas = cuotas_de_evento(ev)
        self.assertIn(("bet365", "Corners Over Under", "Over 9.5", 1.909), filas)
        self.assertIn(("pinnacle", "Home Cards Over/Under", "Under 2.5", 2.05), filas)
        self.assertIn(("pinnacle", "Match Winner", "Home", 2.2), filas)
        self.assertEqual(len(filas), 3)                       # la de la primera parte no cuenta
        ev2 = {"odds": {
            "goalie_saves-home-game-ou-over": {"statID": "goalie_saves", "statEntityID": "home", "periodID": "game",
                                               "betTypeID": "ou", "sideID": "over",
                                               "byBookmaker": {"fanduel": {"odds": "-125", "overUnder": "3.5"}}},
            "bothTeamsScored-all-game-yn-yes": {"statID": "bothTeamsScored", "statEntityID": "all", "periodID": "game",
                                                "betTypeID": "yn", "sideID": "yes",
                                                "byBookmaker": {"fanduel": {"odds": "-150"}}}}}
        filas2 = cuotas_de_evento(ev2)
        self.assertIn(("fanduel", "Home Goalkeeper Saves", "Over 3.5", 1.8), filas2)
        self.assertIn(("fanduel", "Both Teams Score", "Yes", 1.667), filas2)
        book2 = OddsBook([{"bet": b, "value": v, "odd": o} for _, b, v, o in filas2])
        m2 = Market("saves:home:over:3.5", "x", 0.5, "saves", "home", "over", 3.5)
        self.assertEqual(_odds_for(book2, m2), [1.8])
        # Las filas llegan al modelo con los nombres que espera odds.py.
        book = OddsBook([{"bet": b, "value": v, "odd": o} for _, b, v, o in filas])
        m = Market("corners:total:over:9.5", "x", 0.5, "corners", "total", "over", 9.5)
        self.assertEqual(_odds_for(book, m), [1.909])


class BzzoiroTest(unittest.TestCase):
    def test_evento_y_busqueda(self):
        ev = evento_basico({"id": 7, "home_team": "Manchester United", "away_team": "Arsenal FC",
                            "event_date": "2026-10-22T19:00:00Z", "referee": {"name": "Michael Oliver"},
                            "odds_home": 2.4, "odds_draw": 3.4, "odds_away": 2.9, "odds_over_25": 1.8,
                            "odds_under_25": None, "odds_btts_yes": "1.7"})
        self.assertEqual(ev["arbitro"], "Michael Oliver")
        self.assertIn(("Match Winner", "Draw", 3.4), ev["cuotas"])
        self.assertIn(("Both Teams Score", "Yes", 1.7), ev["cuotas"])
        self.assertEqual(len(ev["cuotas"]), 5)
        inicio = datetime(2026, 10, 22, 19, 0, tzinfo=timezone.utc)
        self.assertIs(buscar([ev], "Man United", "Arsenal", inicio), ev)
        self.assertIsNone(buscar([ev], "Chelsea", "Liverpool", inicio))

    def test_alineacion(self):
        al = alineacion_basica({"lineup_status": "confirmed", "lineups": {
            "home": {"players": [{"name": "A", "position": "G"}]}, "away": {"players": [{"name": "B", "position": "F"}]}},
            "unavailable_players": {"home": [{"name": "Lesionado"}], "away": []}})
        self.assertEqual((al["estado"], al["local"], al["bajas"]), ("confirmed", [("A", "G")], ["Lesionado"]))
        self.assertIsNone(alineacion_basica({"lineup_status": "unavailable", "lineups": None}))


class RegistroTest(unittest.TestCase):
    def test_periodos(self):
        with tempfile.TemporaryDirectory() as tmp:
            r = Registro(Path(tmp) / "uso.json", "mes")
            r.sumar(3)
            r.sumar(2)
            r.anotar_restantes(10)
            otro = Registro(Path(tmp) / "uso.json", "mes")
            self.assertEqual((otro.usadas(), otro.restantes()), (5, 10))
            self.assertEqual(len(otro.clave()), 7)


if __name__ == "__main__":
    unittest.main()
