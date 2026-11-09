import json
import random
import unittest
from datetime import date, timedelta
from pathlib import Path
from tempfile import TemporaryDirectory

from apuestas.db import Database
from apuestas.nba.theodds import partidos_hoy
from apuestas.nhl import builder, combinadas, usuario
from apuestas.nhl.analizador import (analizar, candidatas_seguras, guardar_analisis, guardar_picks, liquidar,
                                     menos_aceptable, mejores, rendimiento)
from apuestas.nhl.backtest import backtest, picks_constantes, resumen
from apuestas.nhl.db import NhlDB
from apuestas.nhl.espn import (americana, goles_esperados, grupo_posicion, parse_box, parse_injuries, parse_jugadas,
                               parse_scoreboard, toi)
from apuestas.nhl.informe import escribir
from apuestas.nhl.modelo import (alertas, construir_contexto, linea_minima_casa, piso_casa, predecir,
                                 preparar_jugador, preparar_portero, prob_lados, valor)
from apuestas.nhl.theodds import parse_props

FECHA = "2026-01-20"
EQUIPOS = {"1": "Equipo Uno", "2": "Equipo Dos", "3": "Equipo Tres", "4": "Equipo Cuatro"}
LABELS = ['BS', 'HT', 'TK', '+/-', 'TOI', 'PPTOI', 'SHTOI', 'ESTOI', 'SHFT', 'G', 'YTDG', 'A', 'S', 'SM', 'SOG',
          'FW', 'FL', 'FO%', 'GV', 'PN', 'PIM']
GLABELS = ['GA', 'SA', 'SOS', 'SOSA', 'SV', 'SV%', 'ESSV', 'PPSV', 'SHSV', 'TOI', 'YTDG', 'PIM']


def _mmss(m: float) -> str:
    return f"{int(m)}:{int(round((m - int(m)) * 60)):02d}"


def _summary() -> dict:
    """Resumen con la forma del de ESPN (comprobada el 7 nov 2026), solo los campos que se usan."""
    def atleta(pid, nombre, pos, s):
        return {"athlete": {"id": pid, "displayName": nombre, "position": {"abbreviation": pos}}, "stats": s}
    fila = lambda bs, t, pp, g, a, s: [str(bs), "1", "0", "1", _mmss(t), _mmss(pp), "0:00", _mmss(t - pp), "20",
                                       str(g), "5", str(a), str(s), "1", "0", "3", "2", "60.0", "1", "0", "0"]
    return {
        "boxscore": {"players": [
            {"team": {"id": "1"}, "statistics": [
                {"name": "forwards", "labels": LABELS,
                 "athletes": [atleta("10", "Ana Delantera", "C", fila(0, 19.5, 3.2, 1, 1, 4)),
                              {"athlete": {"id": "11", "displayName": "No Jugó"}, "didNotPlay": True, "stats": []}]},
                {"name": "defenses", "labels": LABELS, "athletes": [atleta("12", "Beto Defensa", "D",
                                                                            fila(3, 23.0, 0.5, 0, 0, 1))]},
                {"name": "skaters", "labels": LABELS, "athletes": []},
                {"name": "goalies", "labels": GLABELS,
                 "athletes": [atleta("13", "Carlos Portero", "G", ["2", "30", "0", "0", "28", ".933", "25", "3", "0",
                                                                   "60:00", "0", "0"])]}]},
            {"team": {"id": "2"}, "statistics": [
                {"name": "forwards", "labels": LABELS, "athletes": [atleta("20", "Dora Rival", "RW",
                                                                            fila(1, 17.0, 2.0, 1, 0, 3))]},
                {"name": "goalies", "labels": GLABELS,
                 "athletes": [atleta("23", "Eva Portera", "G", ["2", "5", "0", "0", "4", ".800", "4", "0", "0",
                                                                "50:00", "0", "0"])]}]},
        ]},
        "plays": [
            {"sequenceNumber": "5", "type": {"text": "Shot"}, "text": "Ana Delantera Wrist Shot saved by Eva Portera",
             "period": {"number": 1}, "team": {"id": "1"}, "coordinate": {"x": -70, "y": 5},
             "strength": {"abbreviation": "power-play"},
             "participants": [{"athlete": {"id": "10"}, "type": "shooter"}, {"athlete": {"id": "23"}, "type": "saver"}]},
            {"sequenceNumber": "6", "type": {"text": "Goal"}, "text": "Ana Delantera Goal (5) Snap Shot, assists: x",
             "period": {"number": 2}, "team": {"id": "1"}, "coordinate": {"x": 80, "y": 0},
             "strength": {"abbreviation": "power-play"},
             "participants": [{"athlete": {"id": "10"}, "type": "scorer"},
                              {"athlete": {"id": "12"}, "type": "assister"}]},
            {"sequenceNumber": "7", "type": {"text": "Tripping"}, "text": "Dora Rival Tripping against Ana Delantera",
             "period": {"number": 2}, "team": {"id": "2"}, "participants": [{"athlete": {"id": "20"}},
                                                                             {"athlete": {"id": "10"}}]},
            {"sequenceNumber": "8", "type": {"text": "Blocked"}, "text": "Dora Rival shot blocked by Beto Defensa",
             "period": {"number": 3}, "team": {"id": "2"}, "coordinate": {"x": 60, "y": -10},
             "strength": {"abbreviation": "even-strength"},
             "participants": [{"athlete": {"id": "20"}, "type": "shooter"},
                              {"athlete": {"id": "12"}, "type": "defender"}]},
            {"sequenceNumber": "9", "type": {"text": "Goal"}, "text": "tanda", "period": {"number": 5},
             "team": {"id": "2"}, "participants": [{"athlete": {"id": "20"}, "type": "scorer"}]},
        ],
        "injuries": [{"team": {"id": "1"}, "injuries": [
            {"athlete": {"id": "14", "displayName": "Lesionado"}, "status": "Injured Reserve",
             "details": {"type": "Knee"}}]}],
    }


class TestParsers(unittest.TestCase):
    def test_box(self):
        skaters, goalies = parse_box(_summary())
        self.assertEqual({s["player_id"] for s in skaters}, {"10", "12", "20"})
        ana = next(s for s in skaters if s["player_id"] == "10")
        self.assertEqual((ana["sog"], ana["g"], ana["a"], ana["grupo"]), (4, 1, 1, "F"))
        self.assertAlmostEqual(ana["toi"], 19.5, places=1)
        self.assertAlmostEqual(ana["pptoi"], 3.2, places=1)
        self.assertEqual(next(s for s in skaters if s["player_id"] == "12")["grupo"], "D")
        self.assertEqual({g["player_id"]: g["starter"] for g in goalies}, {"13": 1, "23": 1})
        self.assertEqual(next(g for g in goalies if g["player_id"] == "13")["sv"], 28)

    def test_jugadas(self):
        tiros, goles, pen = parse_jugadas(_summary())
        self.assertEqual(len(tiros), 3)            # la tanda de penaltis no cuenta
        self.assertEqual([t["result"] for t in tiros], ["sog", "goal", "blocked"])
        self.assertEqual(tiros[0]["strength"], "PP")
        self.assertEqual(tiros[0]["shot_type"], "Wrist Shot")
        self.assertEqual(goles[0]["a1_id"], "12")
        self.assertEqual(len(pen), 1)
        self.assertEqual(parse_injuries(_summary())[0]["status"], "Injured Reserve")

    def test_utilidades(self):
        self.assertAlmostEqual(toi("13:30"), 13.5)
        self.assertEqual(grupo_posicion("LW"), "F")
        self.assertEqual(grupo_posicion("D"), "D")
        self.assertAlmostEqual(americana("-150"), 0.6)
        h, a = goles_esperados(0.6, 6.0)
        self.assertAlmostEqual(h + a, 6.0, places=3)
        self.assertGreater(h, a)
        self.assertAlmostEqual(*goles_esperados(0.5, 5.5), places=3)

    def test_scoreboard(self):
        sb = {"events": [{"id": "99", "date": "2026-01-20T00:00Z", "season": {"year": 2026, "type": 2},
                          "status": {"type": {"name": "STATUS_SCHEDULED"}, "period": 0},
                          "competitions": [{"competitors": [
                              {"homeAway": "home", "team": {"id": "1", "displayName": "Equipo Uno", "name": "Uno"},
                               "probables": [{"name": "probableStartingGoalie",
                                              "athlete": {"id": "13", "displayName": "Carlos Portero"}}]},
                              {"homeAway": "away", "team": {"id": "2", "displayName": "Equipo Dos", "name": "Dos"}}],
                              "odds": [{"overUnder": 6.5, "homeTeamOdds": {}, "awayTeamOdds": {},
                                        "moneyline": {"home": {"close": {"odds": "-150"}},
                                                      "away": {"close": {"odds": "+130"}}}}]}]}]}
        g = parse_scoreboard(sb)[0]
        self.assertEqual(g["probables"]["home"]["player_id"], "13")
        self.assertEqual(g["total_esperado"], 6.5)
        self.assertGreater(g["margen_esperado"], 0)

    def test_props_theodds(self):
        ev = {"bookmakers": [{"key": "dk", "markets": [{"key": "player_shots_on_goal", "outcomes": [
            {"name": "Over", "description": "Ana Delantera", "point": 3.5, "price": 1.9},
            {"name": "Under", "description": "Ana Delantera", "point": 3.5, "price": 1.9}]}]}]}
        filas = parse_props(ev)
        self.assertEqual((filas[0]["stat"], filas[0]["line"]), ("shots", 3.5))

    def test_reparto_creditos(self):
        from datetime import datetime
        dia = datetime(2026, 11, 20)
        self.assertEqual(partidos_hoy("118", dia, 2), 5)        # (118 − 8) / 11 días / 2 mercados
        self.assertEqual(partidos_hoy("118", dia, 2, 0.3), 1)


def _base(tmp: str) -> tuple[Database, NhlDB]:
    """4 equipos, 24 partidos jugados cada uno (temporada 2026) y dos partidos el día FECHA."""
    db = Database(Path(tmp) / "t.db")
    nhl = NhlDB(db.conn)
    rng = random.Random(3)
    perfiles = {}   # jugador -> (equipo, grupo, toi, pptoi, tiros por partido, puntos por partido)
    for t in EQUIPOS:
        for k in range(12):
            grupo = "D" if k >= 8 else "F"
            toi_ = (19 - k * 0.8) if grupo == "F" else (24 - (k - 8) * 2)
            perfiles[f"{t}{k:02d}"] = (t, grupo, toi_, 3.0 if k < 4 else 0.3, 4.2 - k * 0.3, 1.1 - k * 0.07)
    inicio = date(2025, 12, 1)
    gid = 1000
    for d in range(24):
        fecha = (inicio + timedelta(days=d * 2)).isoformat()
        for h, a in (("1", "2"), ("3", "4")) if d % 2 == 0 else (("1", "3"), ("2", "4")):
            gid += 1
            game = {"id": str(gid), "date_utc": fecha + "T00:00Z", "season": 2026, "season_type": 2,
                    "status": "STATUS_FINAL", "home": {"id": h, "abbr": h, "name": EQUIPOS[h], "nickname": h},
                    "away": {"id": a, "abbr": a, "name": EQUIPOS[a], "nickname": a}, "home_goals": 3, "away_goals": 2}
            nhl.upsert_game(game, fecha)
            skaters, goalies = [], []
            for pid, (t, grupo, toi_, pp, tiros, pts) in perfiles.items():
                if t not in (h, a):
                    continue
                g = int(rng.random() < pts * 0.4)
                skaters.append({"player_id": pid, "team_id": t, "opp_id": a if t == h else h, "name": f"Jugador {pid}",
                                "position": "D" if grupo == "D" else "C", "grupo": grupo,
                                "toi": toi_ + rng.uniform(-1, 1), "pptoi": pp, "shtoi": 0.5, "estoi": toi_ - pp,
                                "shifts": 20, "g": g, "a": int(rng.random() < pts * 0.6) + int(rng.random() < 0.1),
                                "sog": max(0, int(rng.gauss(tiros, 1.3))), "missed": 1,
                                "bs": max(0, int(rng.gauss(2.0 if grupo == "D" else 0.6, 1))), "hits": 1, "tk": 0,
                                "gv": 0, "pm": 0, "pim": 2, "fow": 0, "fol": 0})
            for t in (h, a):
                goalies.append({"player_id": f"G{t}", "team_id": t, "opp_id": a if t == h else h,
                                "name": f"Portero {t}", "position": "G", "toi": 60.0, "sa": 30,
                                "sv": 27 + rng.randint(-2, 2), "ga": 3, "es_sv": 25, "pp_sv": 2, "sh_sv": 0,
                                "starter": 1})
            nhl.save_box(str(gid), h, skaters, goalies, [], [], [])
    for h, a in (("1", "2"), ("3", "4")):
        gid += 1
        nhl.upsert_game({"id": str(gid), "date_utc": FECHA + "T00:00Z", "season": 2026, "season_type": 2,
                         "status": "STATUS_SCHEDULED", "home": {"id": h, "abbr": h, "name": EQUIPOS[h], "nickname": h},
                         "away": {"id": a, "abbr": a, "name": EQUIPOS[a], "nickname": a},
                         "probables": {"home": {"player_id": f"G{h}"}, "away": {"player_id": f"G{a}"}},
                         "margen_esperado": 0.3, "total_esperado": 6.0}, FECHA)
    nhl.save_injuries(FECHA, [{"team_id": "1", "player_id": "100", "name": "Jugador 100", "status": "Out",
                               "detail": "Knee"}])
    nhl.commit()
    return db, nhl


class TestModelo(unittest.TestCase):
    def test_prediccion_y_alertas(self):
        with TemporaryDirectory() as tmp:
            db, nhl = _base(tmp)
            ctx = construir_contexto(db.conn, FECHA)
            self.assertEqual(ctx.portero_hoy["1"], "G1")
            j = preparar_jugador(ctx, "100", "Jugador 100", "1", "2")
            self.assertAlmostEqual(j.minutos, 19, delta=1.5)
            pred = predecir(ctx, j, "shots")
            self.assertAlmostEqual(pred.mu, 4.0, delta=1.0)
            self.assertAlmostEqual(predecir(ctx, j, "points").mu, 1.2, delta=0.6)
            self.assertEqual(alertas(ctx, j, "shots"), [])
            suplente = preparar_jugador(ctx, "107", "Jugador 107", "1", "2")
            self.assertIn("papel menor", alertas(ctx, suplente, "shots"))
            portero = preparar_portero(ctx, "G1", "Portero 1", "1", "2")
            # Tiros del rival (suma de sus tiros a puerta, ~24 en estos datos) × su % de paradas (0.9).
            self.assertAlmostEqual(predecir(ctx, portero, "saves").mu, 21.5, delta=3)
            o, u = prob_lados(3.5, 4.0, 4.0)
            self.assertAlmostEqual(o + u, 1.0)

    def test_lineas_minimas(self):
        self.assertEqual(linea_minima_casa(3.5, "shots"), 2.5)
        self.assertEqual(linea_minima_casa(0.5, "points"), 0.5)
        self.assertEqual(linea_minima_casa(27.5, "saves"), 23.5)
        with TemporaryDirectory() as tmp:
            db, nhl = _base(tmp)
            ctx = construir_contexto(db.conn, FECHA)
            j = preparar_jugador(ctx, "100", "Jugador 100", "1", "2")
            self.assertGreaterEqual(piso_casa(j, "shots", 4.0), 2.5)
            self.assertEqual(piso_casa(j, "points", 1.0), 0.5)


class TestFlujo(unittest.TestCase):
    def test_analizar_combinadas_informe_liquidar(self):
        with TemporaryDirectory() as tmp:
            db, nhl = _base(tmp)
            partidos, ctx = analizar(nhl, FECHA)
            self.assertEqual(len(partidos), 2)
            uno = partidos[0]
            self.assertNotIn("100", uno.jugadores)           # Out en el parte de lesiones
            self.assertTrue(uno.evaluaciones)
            self.assertTrue(all(e.estimada for e in uno.evaluaciones))   # sin líneas de la casa
            e = uno.evaluaciones[0]
            self.assertTrue(e.argumentos and e.argumentos[0].startswith("La pasó en"))
            candidatas = candidatas_seguras(partidos)
            for p, e in candidatas:
                self.assertFalse(e.alertas)
                self.assertGreaterEqual(e.prob, 0.62)
                self.assertTrue(menos_aceptable(e))
            builders = builder.del_dia(ctx, partidos)
            for b in builders:
                self.assertLessEqual(len(b.piernas), 3)
                self.assertEqual(len({x.player_id for x in b.piernas}), len(b.piernas))
            combis = combinadas.del_dia(partidos, candidatas) + combinadas.de_builders(builders)
            for c in combis:
                if c.tipo.startswith("cuota_") or c.tipo == "principales":
                    self.assertEqual(len({x["game_id"] for x in c.patas}), len(c.patas))   # un partido por pata
                    self.assertLessEqual(len(c.patas), 5)
            combinadas.guardar(nhl, FECHA, combis)
            picks = mejores(partidos, 0.6)
            guardar_picks(nhl, FECHA, picks, partidos)
            guardar_analisis(nhl, FECHA, partidos)
            md, js = escribir(Path(tmp), FECHA, ctx, partidos, picks, ["aviso"], candidatas, combis, builders)
            texto = md.read_text(encoding="utf-8")
            self.assertIn("# Props NHL", texto)
            self.assertIn("Porteros probables", texto)
            json.loads(js.read_text(encoding="utf-8"))
            # Resultados: se juega el partido del 1 contra el 2.
            g = partidos[0].game
            skaters = [{"player_id": pid, "team_id": j.team_id, "opp_id": j.opp_id, "name": j.nombre,
                        "position": "C", "grupo": j.grupo, "toi": 18.0, "pptoi": 2.0, "shtoi": 0, "estoi": 16,
                        "shifts": 20, "g": 1, "a": 1, "sog": 5, "missed": 0, "bs": 3, "hits": 1, "tk": 0, "gv": 0,
                        "pm": 0, "pim": 0, "fow": 0, "fol": 0} for pid, j in partidos[0].jugadores.items()
                       if not j.es_portero]
            goalies = [{"player_id": f"G{t}", "team_id": t, "opp_id": "2" if t == "1" else "1", "name": "P",
                        "position": "G", "toi": 60, "sa": 40, "sv": 38, "ga": 2, "es_sv": 30, "pp_sv": 8, "sh_sv": 0,
                        "starter": 1} for t in ("1", "2")]
            nhl.save_box(g["id"], g["home_id"], skaters, goalies, [], [], [])
            nhl.commit()
            self.assertGreater(liquidar(nhl), 0)
            combinadas.liquidar(nhl)
            r = rendimiento(nhl)
            self.assertIsNotNone(r["total"])
            self.assertTrue(combinadas.detalle(nhl, FECHA))

    def test_apuestas_usuario(self):
        with TemporaryDirectory() as tmp:
            db, nhl = _base(tmp)
            carpeta = Path(tmp) / "nhl"
            carpeta.mkdir()
            (carpeta / f"{FECHA}.json").write_text(json.dumps({"fecha": FECHA, "apuestas": [
                {"nombre": "Prueba", "cuota": 2.5, "prob": 0.4, "real": False,
                 "patas": [{"jugador": "Jugador 101", "stat": "shots", "lado": "más", "linea": 2.5},
                           {"jugador": "Portero 3", "stat": "saves", "lado": "más", "linea": 24.5}]}]}),
                encoding="utf-8")
            self.assertEqual(usuario.registrar(nhl, carpeta), 1)
            self.assertEqual(usuario.registrar(nhl, carpeta), 0)   # no se duplica

    def test_backtest(self):
        with TemporaryDirectory() as tmp:
            db, nhl = _base(tmp)
            filas = backtest(db.conn, date(2026, 1, 1), date(2026, 1, 16))
            self.assertTrue(filas)
            r = resumen(filas)
            self.assertGreater(r["total"]["n"], 50)
            self.assertIn("saves", r["stats"])
            for f in picks_constantes(filas):
                self.assertGreaterEqual(f["prob"], 0.62)


if __name__ == "__main__":
    unittest.main()
