import math
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from apuestas.collector import Collector
from apuestas.db import Database
from apuestas.remates import PickRemates, Proyeccion, combinada, picks, proyectar

from tests.fake_api import FakeApi
from tests.test_apuestas import FECHA, cfg


class RematesTest(unittest.TestCase):
    def _base(self, tmp):
        c = cfg(tmp)
        db = Database(c.db_path)
        Collector(FakeApi(FECHA), db, c).collect_day(FECHA)
        return c, db, dict(db.fixtures_on(FECHA)[0])

    def test_proyeccion_sin_y_con_alineacion(self):
        with TemporaryDirectory() as tmp:
            c, db, fx = self._base(tmp)
            sin = proyectar(db, c, fx)
            self.assertTrue(sin.proyecciones)
            self.assertTrue(all(p.titular is None for p in sin.proyecciones))
            # El total de remates esperados de los jugadores no puede pasar del esperado del equipo.
            for equipo, esperado in sin.esperado.items():
                suma = sum(p.remates for p in sin.proyecciones if p.equipo == equipo)
                self.assertLessEqual(suma, esperado * 1.05)
            estrella = max(sin.proyecciones, key=lambda p: p.remates)
            tid = fx["home_id"] if estrella.equipo == fx["home_name"] else fx["away_id"]
            otro = fx["away_id"] if tid == fx["home_id"] else fx["home_id"]
            xi = lambda t, fuera=(): {t * 100 + k: (f"J{k}", "F") for k in range(11) if t * 100 + k not in fuera}
            al = {tid: {"titulares": xi(tid, {estrella.player_id})}, otro: {"titulares": xi(otro)}}
            con = proyectar(db, c, fx, alineaciones=al)
            self.assertTrue(con.con_alineacion)
            p = next(x for x in con.proyecciones if x.player_id == estrella.player_id)
            self.assertFalse(p.titular)
            self.assertLess(p.remates, estrella.remates)
            self.assertNotIn(estrella.player_id, {pk.jugador.player_id for pk in picks(con)})
            db.close()

    def test_combinada_un_pick_por_partido_hasta_objetivo(self):
        def pk(i, prob):
            j = Proyeccion(i, f"J{i}", "E", True, 90, 2.0, 500, [2, 2])
            return PickRemates({"id": i, "home_name": "A", "away_name": "B", "date_utc": "2026-10-22T16:45:00"},
                               j, 1.5, prob)
        legs = combinada([pk(i, 0.4) for i in range(10)], objetivo=100, max_legs=8)
        self.assertGreaterEqual(math.prod(p.cuota_justa for p in legs), 100)
        self.assertEqual(len(legs), 6)                   # 2.5^5 = 97.7 < 100 <= 2.5^6
        self.assertEqual(len({p.fixture["id"] for p in legs}), len(legs))
        self.assertEqual(len(combinada([pk(i, 0.4) for i in range(10)], objetivo=1000, max_legs=4)), 4)


if __name__ == "__main__":
    unittest.main()
