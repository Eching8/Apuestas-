import math
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from tempfile import TemporaryDirectory

from apuestas.analyzer import analyze_fixture, candidates, combinadas_extra
from apuestas.chequeo import agenda, aplicar_impacto, chequear, estado_combinadas, render_chequeo
from apuestas.collector import Collector
from apuestas.combinadas import Combo, Leg, build_loteria, crea_tu_apuesta
from apuestas.db import Database
from apuestas.model import Market, MatchExpectation, match_markets
from apuestas.modelo_historico import clave_arbitro
from apuestas.report import save_picks
from apuestas.simulacion import cumple, simular

from tests.fake_api import FakeApi
from tests.test_apuestas import FECHA, cfg


def expectativa() -> MatchExpectation:
    home = {"goals": 1.6, "corners": 5.5, "cards": 1.9, "shots_on": 5.0, "shots_total": 14.0, "saves": 2.8}
    away = {"goals": 1.1, "corners": 4.4, "cards": 2.2, "shots_on": 3.9, "shots_total": 11.0, "saves": 3.4}
    disp = {"goals": 1.0, "corners": 1.3, "cards": 1.2, "shots_on": 1.1, "shots_total": 1.4, "saves": 1.1}
    return MatchExpectation(home, away, disp, 20, 20, rho=-0.05)


class SimulacionTest(unittest.TestCase):
    def test_marginales_y_coherencia(self):
        e = expectativa()
        sim = simular(e, n=40_000, seed=1)
        self.assertAlmostEqual(sim["goals_home"].mean(), 1.6, delta=0.05)
        self.assertAlmostEqual(sim["corners_away"].mean(), 4.4, delta=0.1)
        # Tiros a puerta = goles + atajadas del portero rival: nunca menos tiros que goles.
        self.assertTrue((sim["shots_on_home"] >= sim["goals_home"]).all())
        self.assertTrue((sim["shots_total_home"] >= sim["shots_on_home"]).all())
        markets = {m.key: m for m in match_markets(e, "A", "B")}
        for key in ("result:1", "goals:total:over:2.5", "btts:yes"):
            self.assertAlmostEqual(cumple(sim, markets[key]).mean(), markets[key].prob, delta=0.015)

    def test_correlacion_en_crea_tu_apuesta(self):
        e = expectativa()
        markets = match_markets(e, "A", "B")
        b = crea_tu_apuesta(1, "A vs B", e, markets, objetivo=3.0)
        self.assertIsNotNone(b)
        self.assertLessEqual(b.prob, 1 / 3.0)
        self.assertGreaterEqual(len(b.markets), 2)
        self.assertEqual(len({m.key.split(":")[0] + (m.stat if m.scope != "match" else "") + m.scope
                              for m in b.markets}), len(b.markets))
        # "Gana el local" y "más de 2.5 goles" están correlacionadas positivamente.
        sim = simular(e, seed=2)
        m = {x.key: x for x in markets}
        conj = (cumple(sim, m["result:1"]) & cumple(sim, m["goals:total:over:2.5"])).mean()
        self.assertGreater(conj, m["result:1"].prob * m["goals:total:over:2.5"].prob)


class LoteriaTest(unittest.TestCase):
    def test_mochila_exacta(self):
        def leg(fid, p, o):
            return Leg(fid, f"P{fid}", Market(f"k{fid}{o}", "x", p, "goals", "match", "1", odd=o, final_prob=p))
        legs = ([leg(i, 0.47, 2.1) for i in range(8)] + [leg(i, 0.18, 5.3) for i in range(8)]
                + [leg(20, 0.88, 1.12)] + [leg(21, 0.6, 1.55)])
        (mejor, *_) = build_loteria(legs, objetivo=100.0, n=3)
        self.assertGreaterEqual(mejor.odd, 100.0)
        self.assertEqual(len({l.fixture_id for l in mejor.legs}), len(mejor.legs))
        # Fuerza bruta: no hay combinación de partidos distintos más probable con cuota >= 100.
        import itertools
        def fuerza_bruta(objetivo):
            mejor_p = 0.0
            por_fx = {}
            for l in legs:
                por_fx.setdefault(l.fixture_id, []).append(l)
            for eleccion in itertools.product(*[[None] + v for v in por_fx.values()]):
                sel = [l for l in eleccion if l]
                if sel and math.prod(l.odd for l in sel) >= objetivo:
                    mejor_p = max(mejor_p, math.prod(l.prob for l in sel))
            return mejor_p
        # La búsqueda redondea la log-cuota hacia abajo: es exacta salvo por un margen de ~2 %.
        self.assertLessEqual(mejor.prob, fuerza_bruta(100.0) + 1e-12)
        self.assertGreaterEqual(mejor.prob, fuerza_bruta(102.5) - 1e-12)
        self.assertAlmostEqual(mejor.kelly, 0.001)

    def test_sin_cuota_suficiente(self):
        legs = [Leg(1, "P", Market("k", "x", 0.5, "goals", "match", "1", odd=2.0, final_prob=0.5))]
        self.assertEqual(build_loteria(legs, objetivo=100.0), [])


class ArbitroTest(unittest.TestCase):
    def test_clave(self):
        self.assertEqual(clave_arbitro("Michael Oliver, England"), "m oliver")
        self.assertEqual(clave_arbitro("M Oliver"), "m oliver")
        self.assertEqual(clave_arbitro("Antonio Mateu Lahoz, Spain"), "a lahoz")
        self.assertEqual(clave_arbitro(None), "")


class ChequeoTest(unittest.TestCase):
    def _preparar(self, tmp, c, api):
        db = Database(c.db_path)
        Collector(api, db, c).collect_day(FECHA)
        fixtures = [dict(r) for r in db.fixtures_on(FECHA)]
        analyses = [analyze_fixture(db, fx, c) for fx in fixtures]
        picks = {a.fixture["id"]: candidates(a, c) for a in analyses}
        # Una selección de jugador del primer partido: su habitual faltará en la alineación.
        a0 = analyses[0]
        jugador = next(m for m in a0.markets if m.scope == "player" and m.player_id == a0.fixture["home_id"] * 100)
        picks[a0.fixture["id"]] = picks[a0.fixture["id"]] + [jugador]
        loteria, builders = combinadas_extra(analyses, c)
        save_picks(db, FECHA, picks, {"loteria": loteria})
        return db, fixtures, jugador

    def test_alineacion_anula_y_ajusta(self):
        with TemporaryDirectory() as tmp:
            c = cfg(tmp, prob_min_seleccion=0.55, valor_min=-1.0, cuota_loteria=20.0)
            api = FakeApi(FECHA)
            db, fixtures, jugador = self._preparar(tmp, c, api)
            fx = fixtures[0]
            inicio = datetime.fromisoformat(fx["date_utc"])
            api.ausentes = {fx["home_id"] * 100}

            # Lejos del inicio y sin alineación publicada: esperar.
            api.alineaciones_publicadas = False
            r = chequear(db, api, c, FECHA, ahora=inicio - timedelta(minutes=50), ventana_min=60)
            self.assertEqual([x.estado for x in r], ["esperando"])
            self.assertEqual(db.conn.execute("SELECT COUNT(*) FROM lineup_checks").fetchone()[0], 0)

            api.alineaciones_publicadas = True
            r = chequear(db, api, c, FECHA, ahora=inicio - timedelta(minutes=35), ventana_min=60)
            self.assertEqual(r[0].estado, "chequeado")
            self.assertTrue(any(jugador.label in t and "no es titular" in t for t in r[0].anuladas))
            self.assertTrue(any("ataque esperado" in n for n in r[0].notas), r[0].notas)
            estados = {row["estado"] for row in db.conn.execute(
                "SELECT estado FROM picks WHERE fixture_id = ?", (fx["id"],))}
            self.assertLessEqual(estados, {"confirmada", "anulada", "nueva"})
            self.assertIn("anulada", estados)
            # Ya chequeado: no se repite (salvo --forzar).
            self.assertEqual(chequear(db, api, c, FECHA, ahora=inicio - timedelta(minutes=30), ventana_min=60), [])
            texto = render_chequeo(db, FECHA)
            self.assertIn("no es titular", texto)
            self.assertTrue(estado_combinadas(db, FECHA))
            db.close()

    def test_agenda(self):
        with TemporaryDirectory() as tmp:
            c = cfg(tmp, prob_min_seleccion=0.55, valor_min=-1.0)
            api = FakeApi(FECHA)
            db, fixtures, _ = self._preparar(tmp, c, api)
            inicio = datetime.fromisoformat(fixtures[0]["date_utc"])
            momentos = agenda(db, FECHA, ahora=inicio - timedelta(hours=5))
            # Los partidos del simulador empiezan con una hora de diferencia: un chequeo por partido.
            self.assertEqual(len(momentos), len({p["fixture_id"] for p in db.conn.execute(
                "SELECT DISTINCT fixture_id FROM picks")}))
            self.assertEqual(momentos[0]["chequeo_utc"], (inicio - timedelta(minutes=35)).isoformat(timespec="minutes"))
            db.close()

    def test_aplicar_impacto(self):
        e = expectativa()
        aplicar_impacto(e, 0.8, 1.0)
        self.assertAlmostEqual(e.home["goals"], 1.28)
        self.assertAlmostEqual(e.away["saves"], 3.4 * 0.8)    # el portero visitante recibe menos tiros
        self.assertAlmostEqual(e.away["goals"], 1.1)


if __name__ == "__main__":
    unittest.main()
