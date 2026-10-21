import math
import random
import unittest
from datetime import date, timedelta
from pathlib import Path
from tempfile import TemporaryDirectory

from apuestas.analyzer import analyze_fixture
from apuestas.backtest import backtest_liga, probs_modelo, render_backtest, sin_margen
from apuestas.config import Config
from apuestas.db import Database
from apuestas.historico import Partido, parse_csv, temporada_de, temporadas_hasta
from apuestas.model import MatchExpectation, goal_markets, poisson_pmf, score_grid
from apuestas.modelo_historico import entrenar_liga, equipos_nuevos, goles_del_mercado
from apuestas.predicciones import filas_cuotas
from apuestas.puente import ModeloHistorico, emparejar

CSV_TEMPORADA = """﻿Div,Date,Time,HomeTeam,AwayTeam,FTHG,FTAG,FTR,HS,AS,HST,AST,HF,AF,HC,AC,HY,AY,HR,AR,AvgH,AvgD,AvgA,Avg>2.5,Avg<2.5,PSCH,PSCD,PSCA,AvgCH,AvgCD,AvgCA,AvgC>2.5,AvgC<2.5
E0,16/08/2025,20:00,Liverpool,Bournemouth,4,2,H,19,10,10,3,7,10,6,7,1,2,0,0,1.30,6.0,9.5,1.6,2.3,1.33,5.9,9.1,1.31,5.8,9.0,1.55,2.4
E0,17/08/2025,14:00,Man United,Arsenal,0,1,A,22,9,5,3,11,12,7,3,2,3,0,0,3.4,3.8,2.1,1.9,1.9,,,,3.5,3.7,2.1,,
E0,25/10/2026,16:30,Chelsea,Sunderland,,,,,,,,,,,,,,,,1.4,4.8,7.5,1.7,2.1,,,,,,,,
"""
CSV_EXTRA = """Country,League,Season,Date,Time,Home,Away,HG,AG,Res,PSCH,PSCD,PSCA,AvgCH,AvgCD,AvgCA
Mexico,Liga MX,2025/2026,02/08/2025,03:00,America,Toluca,1,1,D,2.1,3.4,3.3,2.0,3.3,3.2
"""


class ParseoHistoricoTest(unittest.TestCase):
    def test_csv_temporada(self):
        ps = parse_csv(CSV_TEMPORADA, "E0")
        self.assertEqual(len(ps), 3)
        p = ps[0]
        self.assertEqual((p.fecha, p.local, p.goles_local, p.goles_visitante), (date(2025, 8, 16), "Liverpool", 4, 2))
        self.assertEqual(p.valor("corners"), (6, 7))
        self.assertEqual(p.valor("cards"), (1, 2))
        self.assertEqual(p.cuotas["1"], 1.30)
        self.assertEqual(p.cuotas_cierre["1"], 1.33)             # Pinnacle antes que la media
        self.assertEqual(ps[1].cuotas_cierre["1"], 3.5)          # sin Pinnacle: media de cierre
        self.assertNotIn("over2.5", ps[1].cuotas_cierre)
        self.assertFalse(ps[2].jugado)
        self.assertEqual(ps[2].temporada, "2627")

    def test_csv_extra(self):
        (p,) = parse_csv(CSV_EXTRA)
        self.assertEqual((p.liga, p.temporada, p.local, p.goles_local), ("MEX", "2025/2026", "America", 1))
        self.assertEqual(p.stats, {})
        self.assertIsNone(p.valor("corners"))

    def test_temporadas(self):
        self.assertEqual(temporada_de(date(2026, 10, 21)), "2627")
        self.assertEqual(temporada_de(date(2027, 3, 1)), "2627")
        self.assertEqual(temporadas_hasta(date(2026, 10, 21), 3), ["2425", "2526", "2627"])


def liga_sintetica(seed: int = 1, temporadas: int = 3) -> tuple[list[Partido], dict[str, float]]:
    """Liga con fuerzas conocidas: cada equipo juega contra todos en casa y fuera cada temporada."""
    rnd = random.Random(seed)
    equipos = [f"Equipo {i}" for i in range(12)]
    fuerza = {e: (i - 5.5) * 0.06 for i, e in enumerate(equipos)}   # ataque = -defensa = fuerza

    def poisson(lam: float) -> int:
        k, p, u = 0, math.exp(-lam), rnd.random()
        acum = p
        while u > acum:
            k += 1
            p *= lam / k
            acum += p
        return k

    partidos = []
    inicio = date(2023, 8, 1)
    for t in range(temporadas):
        dia = inicio + timedelta(days=365 * t)
        temporada = temporada_de(dia)
        for jornada, (l, v) in enumerate((l, v) for l in equipos for v in equipos if l != v):
            fecha = dia + timedelta(days=jornada // 6 * 3)
            lh = math.exp(0.25 + 0.2 + fuerza[l] - fuerza[v])
            la = math.exp(0.25 + fuerza[v] - fuerza[l])
            gl, gv = poisson(lh), poisson(la)
            tl, tv = poisson(lh * 3.2), poisson(la * 3.2)
            partidos.append(Partido(
                fecha=fecha, liga="E0", temporada=temporada, local=l, visitante=v, goles_local=gl,
                goles_visitante=gv, stats={"shots_on": (tl, tv), "corners": (poisson(5.5), poisson(4.5)),
                                           "yellow": (poisson(1.8), poisson(2.0)), "red": (0, 0)},
                cuotas={"1": 2.4, "X": 3.4, "2": 3.0, "over2.5": 1.9, "under2.5": 1.9},
                cuotas_cierre={"1": 2.5, "X": 3.4, "2": 2.9, "over2.5": 1.95, "under2.5": 1.9},
            ))
    return partidos, fuerza


class ModeloHistoricoTest(unittest.TestCase):
    def test_recupera_fuerzas(self):
        partidos, fuerza = liga_sintetica()
        hoy = partidos[-1].fecha + timedelta(days=1)
        # Las cuotas sintéticas son planas: sin peso del mercado, solo cuentan los goles.
        modelo = entrenar_liga(partidos, "E0", hoy, xi=0.0005, peso_tiros=0.0, peso_mercado=0.0)
        aj = modelo.goles
        self.assertAlmostEqual(aj.local, 0.2, delta=0.08)
        estimada = {e: aj.ataque[i] - aj.defensa[i] for e, i in aj.equipos.items()}
        orden_estimado = sorted(estimada, key=estimada.get)
        self.assertIn("Equipo 0", orden_estimado[:3])
        self.assertIn("Equipo 11", orden_estimado[-3:])
        self.assertIn("corners", modelo.conteos)
        self.assertIn("cards", modelo.conteos)

        e = modelo.expectativa("Equipo 11", "Equipo 0", "2526")
        self.assertGreater(e.home["goals"], 2 * e.away["goals"])
        e2 = modelo.expectativa("Equipo 0", "Equipo 11", "2526")
        self.assertLess(e2.home["goals"], e2.away["goals"])

    def test_con_tiros_y_equipo_desconocido(self):
        partidos, _ = liga_sintetica(seed=2)
        hoy = partidos[-1].fecha + timedelta(days=1)
        modelo = entrenar_liga(partidos, "E0", hoy, peso_tiros=0.5, peso_mercado=0.0)
        self.assertFalse(modelo.conoce("Recién Llegado"))
        e = modelo.expectativa("Recién Llegado", "Equipo 5", "9999")
        self.assertTrue(0.2 < e.home["goals"] < 5)

    def test_goles_del_mercado(self):
        p = probs_modelo(1.8, 0.9, 0.0)
        cuotas = {m: 1 / (p[m] * 1.05) for m in p}     # con un 5 % de margen
        partido = Partido(date(2025, 9, 1), "E0", "2526", "A", "B", 2, 1, cuotas_cierre=cuotas)
        lh, la = goles_del_mercado(partido)
        self.assertAlmostEqual(lh, 1.8, delta=0.05)
        self.assertAlmostEqual(la, 0.9, delta=0.05)
        self.assertIsNone(goles_del_mercado(Partido(date(2025, 9, 1), "E0", "2526", "A", "B", 2, 1)))

    def test_con_mercado(self):
        partidos, _ = liga_sintetica(seed=4)
        hoy = partidos[-1].fecha + timedelta(days=1)
        modelo = entrenar_liga(partidos, "E0", hoy, peso_tiros=0.2, peso_mercado=0.5)
        e = modelo.expectativa("Equipo 11", "Equipo 0", "2526")
        self.assertGreater(e.home["goals"], e.away["goals"])

    def test_ascendidos(self):
        p = lambda t, l, v: Partido(date(2000 + int(t[:2]), 9, 1), "E0", t, l, v, 1, 0)
        nuevos = equipos_nuevos([p("2425", "A", "B"), p("2526", "A", "C"), p("2526", "C", "A")])
        self.assertEqual(nuevos, {("2526", "C")})

    def test_dixon_coles_suma_uno_y_rho_cero_es_poisson(self):
        g = score_grid(1.4, 1.1, -0.1)
        self.assertAlmostEqual(sum(map(sum, g)), 1.0, places=12)
        g0 = score_grid(1.4, 1.1, 0.0)
        self.assertAlmostEqual(g0[2][1], poisson_pmf(2, 1.4) * poisson_pmf(1, 1.1), places=6)
        # rho < 0 sube los empates bajos.
        self.assertGreater(g[0][0], g0[0][0])
        self.assertGreater(g[1][1], g0[1][1])
        e = MatchExpectation({"goals": 1.4}, {"goals": 1.1}, {"goals": 1.0}, 10, 10)
        m = {x.key: x.prob for x in goal_markets(e, "A", "B")}
        self.assertAlmostEqual(m["btts:yes"], (1 - math.exp(-1.4)) * (1 - math.exp(-1.1)), places=6)
        self.assertAlmostEqual(m["result:1"] + m["result:X"] + m["result:2"], 1.0, places=9)


class BacktestTest(unittest.TestCase):
    def test_sin_margen(self):
        p = sin_margen({"1": 2.0, "X": 3.5, "2": 4.0}, ("1", "X", "2"))
        self.assertAlmostEqual(sum(p.values()), 1.0)
        self.assertGreater(p["1"], p["2"])
        self.assertIsNone(sin_margen({"1": 2.0}, ("1", "X", "2")))

    def test_backtest_no_ve_el_futuro(self):
        partidos, _ = liga_sintetica(seed=3)
        desde = date(2025, 8, 1)
        r = backtest_liga(partidos, "E0", desde, peso_mercado=0.0)
        self.assertEqual(len(r.predicciones), sum(p.fecha >= desde for p in partidos))
        # El modelo entrenado con las fuerzas reales debe superar a unas cuotas planas.
        m = r.metricas(0.5)["1x2"]
        self.assertLess(m["modelo"]["logloss"], m["cuotas_cierre"]["logloss"])
        texto = render_backtest([r], desde, 0.5, 0.03)
        self.assertIn("Calibración", texto)
        a = r.apuestas(1.0, 0.03)
        self.assertGreater(a["1x2"]["apuestas"], 0)

    def test_probs_modelo(self):
        p = probs_modelo(1.5, 1.2, -0.05)
        self.assertAlmostEqual(p["1"] + p["X"] + p["2"], 1.0)
        self.assertAlmostEqual(p["over2.5"] + p["under2.5"], 1.0)


class PuenteTest(unittest.TestCase):
    def test_emparejar(self):
        equipos = {"Man United", "Man City", "Nott'm Forest", "Sheffield United", "Sheffield Weds", "Tottenham",
                   "Wolves", "Newcastle"}
        self.assertEqual(emparejar("Manchester United", equipos), "Man United")
        self.assertEqual(emparejar("Manchester City", equipos), "Man City")
        self.assertEqual(emparejar("Nottingham Forest", equipos), "Nott'm Forest")
        self.assertEqual(emparejar("Wolverhampton Wanderers", equipos), "Wolves")
        self.assertEqual(emparejar("Newcastle", equipos), "Newcastle")
        self.assertIsNone(emparejar("Real Madrid", equipos))

    def test_analizador_usa_modelo_historico_sin_historial_en_la_base(self):
        partidos, _ = liga_sintetica(seed=5)
        hoy = partidos[-1].fecha + timedelta(days=1)

        class HistoricoFalso:
            def partidos(self, ligas, temporadas, hoy):
                return partidos

        modelo = ModeloHistorico(HistoricoFalso(), ["E0"], 3, hoy)
        with TemporaryDirectory() as tmp:
            db = Database(Path(tmp) / "t.db")
            cfg = Config(api_football_key="x", db_path=Path(tmp) / "t.db", reportes_dir=Path(tmp), ligas=[])
            fx = {"id": 1, "league_id": 39, "home_id": 10, "away_id": 20, "home_name": "Equipo 11",
                  "away_name": "Equipo 0", "date_utc": f"{hoy.isoformat()}T19:00:00+00:00"}
            a = analyze_fixture(db, fx, cfg, historico=modelo)
            self.assertIsNotNone(a.expectation)
            self.assertFalse(a.solo_mercado)
            probs = {m.key: m.prob for m in a.markets}
            self.assertGreater(probs["result:1"], probs["result:2"])
            self.assertIn("corners:total:over:9.5", probs)
            # Liga sin cobertura: vuelve al comportamiento de siempre (sin historial ni cuotas = nada).
            b = analyze_fixture(db, {**fx, "league_id": 2}, cfg, historico=modelo)
            self.assertIsNone(b.expectation)
            self.assertTrue(any("sin cobertura" in n for n in b.notas))
            db.close()

    def test_filas_cuotas(self):
        p = Partido(date(2026, 10, 25), "E0", "2627", "A", "B", cuotas={"1": 2.0, "X": 3.4, "over2.5": 1.8})
        filas = {(f["bet"], f["value"]): f["odd"] for f in filas_cuotas(p)}
        self.assertEqual(filas[("Match Winner", "Home")], 2.0)
        self.assertEqual(filas[("Goals Over/Under", "Over 2.5")], 1.8)


if __name__ == "__main__":
    unittest.main()
