import math
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from apuestas.analyzer import analyze_fixture, candidates
from apuestas.collector import Collector, parse_statistics
from apuestas.combinadas import Leg, build_combos
from apuestas.config import Config
from apuestas.db import Database
from apuestas.model import Market, negbin_pmf, poisson_pmf, prob_over
from apuestas.odds import attach_odds
from apuestas.report import save_picks, write_reports
from apuestas.settle import evaluate, settle_pending, summary

from tests.fake_api import FakeApi

FECHA = "2026-10-21"


def cfg(tmp: str, **kw) -> Config:
    c = Config(api_football_key="x", zona_horaria="UTC", db_path=Path(tmp) / "t.db", reportes_dir=Path(tmp) / "r",
               ligas=[], partidos_historial=6)
    for k, v in kw.items():
        setattr(c, k, v)
    return c


class DistribucionesTest(unittest.TestCase):
    def test_pmfs_suman_uno(self):
        self.assertAlmostEqual(sum(poisson_pmf(k, 2.7) for k in range(60)), 1.0, places=9)
        self.assertAlmostEqual(sum(negbin_pmf(k, 9.5, 14.0) for k in range(200)), 1.0, places=9)

    def test_prob_over(self):
        lam = 2.5
        esperado = 1 - math.exp(-lam) * (1 + lam + lam ** 2 / 2)
        self.assertAlmostEqual(prob_over(2.5, lam), esperado, places=9)
        # Más varianza = más masa en las colas (sobre la media, P(over) baja al alejarse).
        self.assertLess(prob_over(12.5, 10, 18), 1.0)
        self.assertGreater(prob_over(14.5, 10, 18), prob_over(14.5, 10, 10))


class ParseoTest(unittest.TestCase):
    def test_estadisticas_null_es_cero_y_sin_cobertura_vacia(self):
        fx = {"id": 1, "home_id": 10, "away_id": 20, "home_goals": 2, "away_goals": 1}
        resp = [
            {"team": {"id": 10}, "statistics": [{"type": "Corner Kicks", "value": 6}, {"type": "Yellow Cards", "value": None},
                                                {"type": "Red Cards", "value": 1}, {"type": "Ball Possession", "value": "61%"}]},
            {"team": {"id": 20}, "statistics": [{"type": "Corner Kicks", "value": None}, {"type": "Yellow Cards", "value": 3}]},
        ]
        h, a = parse_statistics(fx, resp)
        self.assertEqual((h["corners"], h["cards"], h["possession"], h["goals"]), (6, 1, 61.0, 2))
        self.assertEqual((a["corners"], a["cards"]), (0, 3))
        self.assertEqual(parse_statistics(fx, []), [])
        self.assertEqual(parse_statistics(fx, [{"team": {"id": 10}, "statistics": []},
                                               {"team": {"id": 20}, "statistics": []}]), [])


class CuotasTest(unittest.TestCase):
    def test_mezcla_modelo_y_mercado(self):
        m = Market("goals:total:over:2.5", "", 0.60, "goals", "total", "over", 2.5)
        rows = [{"bet": "Goals Over/Under", "value": "Over 2.5", "odd": 2.0},
                {"bet": "Goals Over/Under", "value": "Under 2.5", "odd": 2.0}]
        attach_odds([m], rows, peso_modelo=0.5)
        self.assertAlmostEqual(m.market_prob, 0.5)
        self.assertAlmostEqual(m.final_prob, 0.55)
        self.assertAlmostEqual(m.edge, 0.10)


class LiquidacionTest(unittest.TestCase):
    def test_evaluate(self):
        t = {"home": {"goals": 2, "corners": 6, "cards": 2}, "away": {"goals": 0, "corners": 4, "cards": 3}}
        self.assertTrue(evaluate("result:1", t))
        self.assertTrue(evaluate("dc:1X", t))
        self.assertTrue(evaluate("btts:no", t))
        self.assertTrue(evaluate("corners:total:over:9.5", t))
        self.assertFalse(evaluate("cards:total:under:4.5", t))
        self.assertTrue(evaluate("corners:away:under:4.5", t))
        self.assertTrue(evaluate("player:5:shots_on:over:0.5", t, {"shots_on": 1}))
        self.assertIsNone(evaluate("player:5:shots_on:over:0.5", t, None))


class FlujoCompletoTest(unittest.TestCase):
    def test_descarga_analiza_combina_y_liquida(self):
        with TemporaryDirectory() as tmp:
            c = cfg(tmp, prob_min_seleccion=0.55, valor_min=-1.0)
            db = Database(c.db_path)
            api = FakeApi(FECHA)
            listos = Collector(api, db, c).collect_day(FECHA)
            self.assertEqual(len(listos), 4)
            n_calls = api.peticiones

            # Segunda pasada: los partidos ya guardados no se vuelven a pedir.
            Collector(api, db, c).collect_day(FECHA)
            self.assertLessEqual(api.peticiones - n_calls, 1 + 8 + 4)

            fixtures = [dict(r) for r in db.fixtures_on(FECHA)]
            analyses = [analyze_fixture(db, fx, c) for fx in fixtures]
            self.assertTrue(all(a.ok for a in analyses), [a.notas for a in analyses])
            a = analyses[0]
            for s in ("goals", "corners", "cards", "shots_on", "shots_total"):
                self.assertGreater(a.expectation.total(s), 0)
            keys = {m.key for m in a.markets}
            self.assertIn("corners:total:over:8.5", keys)
            self.assertTrue(any(k.startswith("player:") for k in keys))
            con_cuota = next(m for m in a.markets if m.key == "corners:total:over:8.5")
            self.assertEqual(con_cuota.odd, 1.55)
            self.assertIsNotNone(con_cuota.market_prob)
            p1 = sum(m.prob for m in a.markets if m.key in ("result:1", "result:X", "result:2"))
            self.assertAlmostEqual(p1, 1.0, places=6)

            picks, legs = {}, []
            for an in analyses:
                sel = candidates(an, c)
                picks[an.fixture["id"]] = sel
                legs += [Leg(an.fixture["id"], "x", m) for m in sel]
            combos = build_combos(legs, prob_min=0.0, cuota_min=1.0)
            self.assertTrue(combos["alta_probabilidad"])
            for combo in combos["alta_probabilidad"] + combos["valor"]:
                self.assertEqual(len({l.fixture_id for l in combo.legs}), len(combo.legs))

            md, js = write_reports(c.reportes_dir, FECHA, analyses, picks, combos)
            self.assertIn("Aviso", md.read_text(encoding="utf-8"))
            save_picks(db, FECHA, picks, combos)
            save_picks(db, FECHA, picks, combos)  # re-ejecutar no duplica
            n_picks = db.conn.execute("SELECT COUNT(*) FROM picks WHERE combo_id IS NULL").fetchone()[0]
            self.assertEqual(n_picks, sum(len(v) for v in picks.values()))

            api.finish_today()
            Collector(api, db, c).update_results(FECHA)
            self.assertGreater(settle_pending(db), 0)
            pend = db.conn.execute("SELECT COUNT(*) FROM picks WHERE result IS NULL AND market_key NOT LIKE 'player:%'")
            self.assertEqual(pend.fetchone()[0], 0)
            self.assertTrue(summary(db)["selecciones"])
            self.assertEqual(db.conn.execute("SELECT COUNT(*) FROM combos WHERE result IS NULL").fetchone()[0], 0)
            db.close()

    def test_presupuesto_corta_sin_romper(self):
        with TemporaryDirectory() as tmp:
            c = cfg(tmp, presupuesto_peticiones=20)
            db = Database(c.db_path)
            api = FakeApi(FECHA, presupuesto=20)
            listos = Collector(api, db, c).collect_day(FECHA)
            self.assertLess(len(listos), 4)
            self.assertEqual(api.peticiones, 20)
            db.close()


if __name__ == "__main__":
    unittest.main()
