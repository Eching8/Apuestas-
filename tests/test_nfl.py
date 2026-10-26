import random
import unittest
from datetime import date, timedelta
from pathlib import Path
from tempfile import TemporaryDirectory

from apuestas.db import Database
from apuestas.nfl import equipos
from apuestas.nfl.analizador import analizar_partido, con_valor, guardar_picks, liquidar, rendimiento
from apuestas.nfl.backtest import backtest, resumen
from apuestas.nfl.db import STATS_JUGADOR, NflDB, estado_duda, estado_fuera
from apuestas.nfl.fuentes import (agregar_pbp, cambios_semanales, parse_calendario, parse_lesiones_espn,
                                  parse_stats_jugador, traspasos_en_texto)
from apuestas.nfl.informe import escribir
from apuestas.nfl.mercado import emparejar, parse_evento
from apuestas.nfl.modelo import (Linea, construir_contexto, entorno, p_al_menos, preparar_equipo, prob_lados,
                                 proyectar)
from apuestas.nfl.validar import buscar_jugador, interpretar, texto_veredicto, validar

EQUIPOS = ("BUF", "LAC", "KC", "DEN")
INICIO = date(2026, 9, 10)
HOY = "2026-11-05"
# Jugadores: (id, nombre, posición, equipo, acarreos, envíos, % de acarreos dentro de la 10)
PLANTILLA = [
    ("qb_buf", "Josh Allen", "QB", "BUF", 7, 0, 0.45), ("rb_buf", "James Cook", "RB", "BUF", 17, 3, 0.45),
    ("rb2_buf", "Ray Davis", "RB", "BUF", 6, 1, 0.10), ("wr_buf", "Khalil Shakir", "WR", "BUF", 0, 8, 0.0),
    ("te_buf", "Dalton Kincaid", "TE", "BUF", 0, 5, 0.0),
    ("qb_lac", "Justin Herbert", "QB", "LAC", 3, 0, 0.1), ("rb_lac", "Omarion Hampton", "RB", "LAC", 18, 3, 0.7),
    ("wr_lac", "Ladd McConkey", "WR", "LAC", 0, 9, 0.0), ("te_lac", "Tyler Conklin", "TE", "LAC", 0, 4, 0.0),
    ("qb_kc", "Patrick Mahomes", "QB", "KC", 4, 0, 0.2), ("rb_kc", "Isiah Pacheco", "RB", "KC", 15, 2, 0.6),
    ("wr_kc", "Rashee Rice", "WR", "KC", 0, 9, 0.0), ("te_kc", "Travis Kelce", "TE", "KC", 0, 7, 0.0),
    ("qb_den", "Bo Nix", "QB", "DEN", 5, 0, 0.3), ("rb_den", "RJ Harvey", "RB", "DEN", 14, 3, 0.6),
    ("wr_den", "Courtland Sutton", "WR", "DEN", 0, 8, 0.0), ("te_den", "Evan Engram", "TE", "DEN", 0, 4, 0.0),
]


def _jornadas() -> list[tuple[int, str, str, str]]:
    """Ocho semanas de una liga de cuatro equipos: (semana, fecha, local, visitante)."""
    cruces = [(("BUF", "LAC"), ("KC", "DEN")), (("LAC", "KC"), ("DEN", "BUF")), (("BUF", "KC"), ("LAC", "DEN"))]
    out = []
    for w in range(1, 9):
        fecha = (INICIO + timedelta(days=7 * (w - 1))).isoformat()
        for h, a in cruces[w % 3]:
            out.append((w, fecha, h, a))
    return out


def _filas_sinteticas(seed: int = 7) -> tuple[list[dict], list[dict], list[dict]]:
    """Calendario, estadísticas por jugador y jugada a jugada con la forma de los CSV de nflverse."""
    rng = random.Random(seed)
    calendario, stats, pbp = [], [], []
    for w, fecha, h, a in _jornadas():
        gid = f"2026_{w:02d}_{a}_{h}"
        puntos = {}
        play = 0
        for team, opp in ((h, a), (a, h)):
            tds = 0
            for pid, nombre, pos, eq, car, tg, i10 in PLANTILLA:
                if eq != team:
                    continue
                c = max(0, int(rng.gauss(car, 2))) if car else 0
                t = max(0, int(rng.gauss(tg, 2))) if tg else 0
                rec = sum(rng.random() < 0.68 for _ in range(t))
                ry = sum(rng.choice((1, 2, 3, 4, 5, 6, 8, 12)) for _ in range(c))
                recy = sum(rng.choice((5, 7, 9, 12, 18)) for _ in range(rec))
                rtd = sum(rng.random() < (0.025 + i10 * 0.04) for _ in range(c))
                retd = sum(rng.random() < 0.07 for _ in range(rec))
                tds += rtd + retd
                fila = {k: "0" for k in STATS_JUGADOR}
                fila.update({"player_id": pid, "player_display_name": nombre, "position": pos, "season": "2026",
                             "week": str(w), "season_type": "REG", "game_id": gid, "team": team,
                             "opponent_team": opp, "carries": str(c), "rushing_yards": str(ry),
                             "rushing_tds": str(rtd), "targets": str(t), "receptions": str(rec),
                             "receiving_yards": str(recy), "receiving_tds": str(retd)})
                if pos == "QB":
                    att = int(rng.gauss(33, 4))
                    fila.update({"attempts": str(att), "completions": str(int(att * 0.65)),
                                 "passing_yards": str(int(att * 7)), "passing_tds": str(rng.choice((1, 2, 2, 3))),
                                 "passing_interceptions": str(rng.choice((0, 0, 1)))})
                stats.append(fila)
                # Jugadas: cada acarreo y envío, con la yarda de campo para la zona roja.
                for k in range(c):
                    play += 1
                    yl = 5 if k < round(c * i10) else 45
                    pbp.append({"play_id": str(play), "game_id": gid, "season": "2026", "week": str(w),
                                "home_team": h, "posteam": team, "defteam": opp, "play_type": "run",
                                "yardline_100": str(yl), "yards_gained": "4", "rusher_player_id": pid,
                                "qb_scramble": "0", "fixed_drive": str(k), "epa": "0.0", "success": "1",
                                "touchdown": "1" if k < rtd else "0", "td_team": team if k < rtd else "",
                                "td_player_id": pid if k < rtd else "", "rush_touchdown": "1" if k < rtd else "0"})
                for k in range(t):
                    play += 1
                    pbp.append({"play_id": str(play), "game_id": gid, "season": "2026", "week": str(w),
                                "home_team": h, "posteam": team, "defteam": opp, "play_type": "pass",
                                "yardline_100": "15" if k == 0 else "60", "air_yards": "16" if k == 0 else "8",
                                "yards_gained": "8", "receiver_player_id": pid, "passer_player_id": f"qb_{team.lower()}",
                                "pass_attempt": "1", "complete_pass": "1" if k < rec else "0", "qb_scramble": "0",
                                "epa": "0.1", "success": "1", "touchdown": "1" if k < retd else "0",
                                "td_team": team if k < retd else "", "td_player_id": pid if k < retd else "",
                                "pass_touchdown": "1" if k < retd else "0"})
            puntos[team] = 7 * tds + rng.choice((3, 6, 9))
        calendario.append({"game_id": gid, "season": "2026", "game_type": "REG", "week": str(w), "gameday": fecha,
                           "gametime": "13:00", "home_team": h, "away_team": a, "home_score": str(puntos[h]),
                           "away_score": str(puntos[a]), "spread_line": "3.0", "total_line": "45.5",
                           "home_qb_id": f"qb_{h.lower()}", "away_qb_id": f"qb_{a.lower()}", "roof": "outdoors"})
    # Semana 9 (por jugar): BUF recibe a LAC.
    calendario.append({"game_id": "2026_09_LAC_BUF", "season": "2026", "game_type": "REG", "week": "9",
                       "gameday": HOY, "gametime": "20:15", "home_team": "BUF", "away_team": "LAC",
                       "spread_line": "4.5", "total_line": "48.5", "roof": "outdoors", "wind": "5"})
    return calendario, stats, pbp


def _llenar(db: NflDB) -> None:
    calendario, stats, pbp = _filas_sinteticas()
    db.upsert_games(parse_calendario(calendario, {2026}))
    db.reemplazar_player_games(2026, parse_stats_jugador(stats, STATS_JUGADOR))
    jug, eq, primeros = agregar_pbp(pbp)
    db.reemplazar_pbp(2026, jug, eq, primeros)
    db.actualizar_roster([{"player_id": pid, "name": n, "position": pos, "team": t, "status": "ACT", "season": 2026,
                           "week": 8} for pid, n, pos, t, *_ in PLANTILLA])
    db.commit()


def _evento_sgo() -> dict:
    """Evento de SportsGameOdds para BUF-LAC con un TD (consenso y 2+ alternativo) y yardas."""
    def odd(oid, stat, pid, bet, side, line, book_odds, books, fair=None, fair_line=None, open_odds=None):
        rival = oid.replace("over", "under") if oid.endswith("over") else oid.replace("under", "over")
        return oid, {"oddID": oid, "opposingOddID": rival, "statID": stat, "statEntityID": pid or "all", "playerID": pid, "periodID": "game",
                     "betTypeID": bet, "sideID": side, "bookOddsAvailable": True, "bookOverUnder": line,
                     "bookOdds": book_odds, "fairOdds": fair, "fairOverUnder": fair_line, "openBookOdds": open_odds,
                     "openBookOverUnder": line, "byBookmaker": books}
    odds = dict([
        odd("td-cook-over", "touchdowns", "JAMES_COOK_1_NFL", "ou", "over", "0.5", "-120",
            {"fanduel": {"odds": "-110", "overUnder": "1.5", "available": True},
             "draftkings": {"odds": "+100", "overUnder": "0.5", "available": True}},
            fair="+110", fair_line="0.5", open_odds="+120"),
        odd("ry-cook-over", "rushing_yards", "JAMES_COOK_1_NFL", "ou", "over", "79.5", "-110",
            {"fanduel": {"odds": "-105", "overUnder": "79.5", "available": True}}),
        odd("ry-cook-under", "rushing_yards", "JAMES_COOK_1_NFL", "ou", "under", "79.5", "-110",
            {"fanduel": {"odds": "-115", "overUnder": "79.5", "available": True}}),
        # Relleno sin casas (+100/+100): no se puede apostar y se descarta.
        odd("lr-x", "receiving_longestReception", "KHALIL_SHAKIR_1_NFL", "ou", "over", "0.5", "+100", {}),
        odd("total", "points", None, "ou", "over", "47.5", "-110", {}, fair_line="48"),
    ])
    odds["td-cook-over"]["byBookmaker"]["fanduel"]["odds"] = "+400"
    return {"eventID": "EV1", "teams": {"home": {"names": {"long": "Buffalo Bills"}},
                                        "away": {"names": {"long": "Los Angeles Chargers"}}},
            "status": {"startsAt": "2026-11-06T01:15:00Z"},
            "players": {"JAMES_COOK_1_NFL": {"name": "James Cook", "teamID": "BUFFALO_BILLS_NFL"},
                        "KHALIL_SHAKIR_1_NFL": {"name": "Khalil Shakir", "teamID": "BUFFALO_BILLS_NFL"}},
            "odds": odds}


class EquiposYTextoTest(unittest.TestCase):
    def test_equipos(self):
        self.assertEqual(equipos.por_texto("los chargers".replace("los ", "")), "LAC")
        self.assertEqual(equipos.por_texto("Cargadores"), "LAC")
        self.assertEqual(equipos.por_nombre_largo("PHILADELPHIA_EAGLES_NFL"), "PHI")
        self.assertEqual(equipos.normalizar("LAR"), "LA")
        self.assertEqual(equipos.normalizar("WSH"), "WAS")

    def test_interpretar(self):
        a = interpretar("derrick henry +2 td")
        self.assertEqual((a.jugador, a.stat, a.line, a.lado), ("derrick henry", "tds", 1.5, "más"))
        a = interpretar("Josh Allen anotará 2 touchdowns contra los chargers")
        self.assertEqual((a.jugador, a.stat, a.line, a.rival), ("Josh Allen", "tds", 1.5, "LAC"))
        a = interpretar("Saquon Barkley más de 69.5 yardas por tierra")
        self.assertEqual((a.jugador, a.stat, a.line), ("Saquon Barkley", "rush_yds", 69.5))
        a = interpretar("CeeDee Lamb under 5.5 recepciones @ -120")
        self.assertEqual((a.stat, a.lado, a.line, round(a.cuota, 3)), ("rec", "menos", 5.5, 1.833))
        a = interpretar("Allen más de 1.5 td de pase")
        self.assertEqual(a.stat, "pass_tds")
        self.assertEqual(interpretar("Bijan Robinson primer td a +550").stat, "first_td")
        self.assertEqual(interpretar("Josh Allen anota").line, 0.5)
        with self.assertRaises(ValueError):
            interpretar("Josh Allen gana")

    def test_estados(self):
        self.assertTrue(estado_fuera("Injured Reserve"))
        self.assertTrue(estado_fuera("Out"))
        self.assertFalse(estado_fuera("Questionable"))
        self.assertTrue(estado_duda("Questionable"))

    def test_traspasos_y_cambios(self):
        t = traspasos_en_texto([
            {"fecha": "2026-10-12", "team": "ARI", "description": "Traded WR Marvin Harrison Jr. and a 2027 "
             "sixth-round draft pick to Houston for 2027 second- and seventh-round draft picks."},
            {"fecha": "2026-10-07", "team": "BAL", "description": "Traded a 2027 fifth-round pick to Philadelphia "
             "Eagles for G Cam Jurgens."}])
        self.assertEqual(t, [{"fecha": "2026-10-12", "name": "Marvin Harrison Jr.", "from_team": "ARI",
                              "to_team": "HOU"}])
        cambios = cambios_semanales([
            {"gsis_id": "x", "team": "ARI", "week": "5", "full_name": "X"},
            {"gsis_id": "x", "team": "HOU", "week": "6", "full_name": "X"},
            {"gsis_id": "x", "team": "ARI", "week": "4", "full_name": "X"}])
        self.assertEqual([(c["week"], c["from_team"], c["to_team"]) for c in cambios], [(6, "ARI", "HOU")])

    def test_lesiones_espn(self):
        data = {"injuries": [{"displayName": "Buffalo Bills", "injuries": [
            {"status": "Out", "date": "2026-10-26T01:00Z", "details": {"type": "Ankle"},
             "athlete": {"displayName": "James Cook", "position": {"abbreviation": "RB"},
                         "links": [{"href": "https://www.espn.com/nfl/player/_/id/4379399/james-cook"}]}}]}]}
        les = parse_lesiones_espn(data)
        self.assertEqual((les[0]["espn_id"], les[0]["team"], les[0]["status"]), ("4379399", "BUF", "Out"))


class PbpTest(unittest.TestCase):
    def test_agregar(self):
        filas = [
            {"play_id": "1", "game_id": "g", "season": "2026", "week": "1", "home_team": "BUF", "posteam": "BUF",
             "defteam": "LAC", "play_type": "run", "yardline_100": "4", "yards_gained": "4", "rusher_player_id": "a",
             "qb_scramble": "0", "fixed_drive": "1", "fixed_drive_result": "Touchdown", "touchdown": "1",
             "td_team": "BUF", "td_player_id": "a", "rush_touchdown": "1", "success": "1", "epa": "1.5"},
            {"play_id": "2", "game_id": "g", "season": "2026", "week": "1", "home_team": "BUF", "posteam": "LAC",
             "defteam": "BUF", "play_type": "pass", "yardline_100": "18", "air_yards": "18", "yards_gained": "0",
             "receiver_player_id": "b", "passer_player_id": "q", "pass_attempt": "1", "complete_pass": "0",
             "qb_scramble": "0", "fixed_drive": "2", "touchdown": "0", "success": "0", "epa": "-0.5"},
            {"play_id": "3", "game_id": "g", "season": "2026", "week": "1", "home_team": "BUF", "posteam": "LAC",
             "defteam": "BUF", "play_type": "run", "yardline_100": "30", "yards_gained": "12",
             "rusher_player_id": "q", "qb_scramble": "1", "fixed_drive": "2", "touchdown": "0", "success": "1",
             "epa": "0.8"},
            {"play_id": "4", "game_id": "g", "season": "2026", "week": "1", "home_team": "BUF", "posteam": "LAC",
             "defteam": "BUF", "play_type": "run", "two_point_attempt": "1", "rusher_player_id": "q"},
        ]
        jug, eq, primeros = agregar_pbp(filas)
        j = {x["player_id"]: x for x in jug}
        self.assertEqual((j["a"]["rz_carries"], j["a"]["i10_carries"], j["a"]["i5_carries"]), (1, 1, 1))
        self.assertEqual((j["b"]["rz_targets"], j["b"]["ez_targets"]), (1, 1))
        self.assertEqual((j["q"]["scrambles"], j["q"]["designed_runs"]), (1, 0))  # la de 2 puntos no cuenta
        e = {x["team"]: x for x in eq}
        self.assertEqual((e["BUF"]["rush_tds"], e["BUF"]["rz_trips"], e["BUF"]["rz_tds"]), (1, 1, 1))
        self.assertEqual((e["LAC"]["dropbacks"], e["LAC"]["carries"], e["LAC"]["qb_rush_yds"]), (1, 1, 12))
        self.assertEqual(primeros, {"g": "a"})


class MercadoTest(unittest.TestCase):
    def test_parse_evento(self):
        m = parse_evento(_evento_sgo())
        self.assertEqual((m.home, m.away, m.total), ("BUF", "LAC", 48.0))   # la línea justa manda
        of = {(o.stat, o.lado, o.line): o for o in m.ofertas}
        self.assertNotIn(("long_rec", "más", 0.5), of)                       # relleno sin casas
        td1, td2 = of[("tds", "más", 0.5)], of[("tds", "más", 1.5)]
        self.assertEqual(td1.libros, {"draftkings": 2.0})
        self.assertEqual(td2.libros, {"fanduel": 5.0})                       # 2+ TD: línea alternativa
        self.assertIsNone(td2.justa)                                         # la cuota justa es de la línea 0.5
        self.assertAlmostEqual(td1.prob_casa(), 1 / 2.1, places=3)
        self.assertAlmostEqual(td2.prob_casa(), 1 / 5.0 / 1.12, places=3)
        self.assertGreater(td1.presion(), 0)                                 # de +120 a -120: entra dinero
        ry = of[("rush_yds", "más", 79.5)]
        self.assertAlmostEqual(ry.prob_casa(), 0.5, places=3)
        n = emparejar(m, [{"player_id": "rb_buf", "name": "James Cook", "team": "BUF"},
                          {"player_id": "otro", "name": "James Cook", "team": "MIA"}])
        self.assertEqual(n, 4)
        self.assertTrue(all(o.player_id == "rb_buf" for o in m.ofertas))


class ModeloTest(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.db = Database(Path(self.tmp.name) / "t.db")
        self.nfl = NflDB(self.db.conn)
        _llenar(self.nfl)

    def tearDown(self):
        self.db.close()
        self.tmp.cleanup()

    def test_prob_lados(self):
        o, u = prob_lados(70.5, 75.0, 900.0)
        self.assertAlmostEqual(o + u, 1.0, places=9)
        self.assertAlmostEqual(p_al_menos(0.0, 1), 0.0)
        self.assertGreater(p_al_menos(0.8, 1), p_al_menos(0.8, 2))

    def test_proyeccion_y_tds(self):
        ctx = construir_contexto(self.db.conn, HOY)
        ent = entorno(ctx, "BUF", "LAC", True, Linea(total=48.5, spread_home=4.5))
        self.assertAlmostEqual(ent.puntos, 26.5)
        jugadores = {j.player_id: j for j in preparar_equipo(ctx, "BUF")}
        cook = proyectar(ctx, jugadores["rb_buf"], ent)
        davis = proyectar(ctx, jugadores["rb2_buf"], ent)
        # El RB titular tiene más acarreos, más yardas y más TD esperados que el suplente.
        self.assertGreater(cook.medias["rush_att"], 12)
        self.assertGreater(cook.medias["rush_yds"], davis.medias["rush_yds"])
        self.assertGreater(cook.lambdas["tds"], davis.lambdas["tds"])
        self.assertTrue(cook.factores["tds"])
        # El QB titular lanza casi todo y tiene TD de pase esperados.
        allen = proyectar(ctx, jugadores["qb_buf"], ent)
        self.assertAlmostEqual(allen.medias["pass_att"], 0.97 * ent.pass_att)
        self.assertGreater(allen.medias["pass_tds"], 0.5)

    def test_baja_reparte_volumen(self):
        ctx = construir_contexto(self.db.conn, HOY)
        ent = entorno(ctx, "BUF", "LAC", True)
        antes = {j.player_id: proyectar(ctx, j, ent) for j in preparar_equipo(ctx, "BUF")}
        ctx.lesiones["rb_buf"] = {"status": "Out", "detail": "Ankle"}
        despues = {j.player_id: proyectar(ctx, j, ent) for j in preparar_equipo(ctx, "BUF")}
        self.assertNotIn("rb_buf", despues)
        self.assertGreater(despues["rb2_buf"].medias["rush_att"], antes["rb2_buf"].medias["rush_att"] * 1.2)
        self.assertTrue(any("bajas" in n for n in despues["rb2_buf"].jugador.notas))
        self.assertEqual([b["player_id"] for b in ctx.bajas["BUF"]], ["rb_buf"])

    def test_analisis_validar_informe_y_liquidacion(self):
        ctx = construir_contexto(self.db.conn, HOY)
        g = dict(self.db.conn.execute("SELECT * FROM nfl_games WHERE game_id = '2026_09_LAC_BUF'").fetchone())
        m = parse_evento(_evento_sgo())
        emparejar(m, [dict(r) for r in self.db.conn.execute("SELECT player_id, name, team FROM nfl_rosters")])
        a = analizar_partido(ctx, g, m)
        self.assertEqual(set(a.entornos), {"BUF", "LAC"})
        self.assertTrue(a.tds)
        cook = next(t for t in a.tds if t.player_id == "rb_buf")
        self.assertIn("1+", cook.ofertas)
        self.assertIn("2+", cook.ofertas)
        self.assertAlmostEqual(cook.ofertas["2+"].prob_modelo, cook.p2, places=6)
        self.assertGreater(sum(t.p_first for t in a.tds), 0.5)
        self.assertLess(sum(t.p_first for t in a.tds), 1.0)
        self.assertTrue(a.claves["BUF"])
        # Validar como tipster.
        ap = interpretar("James Cook +2 TD")
        ids = buscar_jugador(ctx, ap.jugador)
        self.assertEqual(ids, ["rb_buf"])
        v = validar(ctx, ap, {g["game_id"]: a}, "rb_buf")
        self.assertEqual(v.evaluacion.odd, 5.0)
        self.assertTrue(v.narrativa)
        self.assertIn("¿Por qué la gente apuesta esto?", texto_veredicto(ctx, v))
        # Informe y selecciones.
        valor_ = con_valor([a], valor_min=-1.0, edge_min=-1.0)
        md, js = escribir(Path(self.tmp.name), HOY, HOY, [a], valor_, [], {"traspasos": [], "bajas": []})
        self.assertIn("¿Quién anota?", md.read_text(encoding="utf-8"))
        guardar_picks(self.nfl, HOY, [v.evaluacion], origen="validar")
        # El partido se juega: Cook anota 2 TD.
        self.db.conn.execute("UPDATE nfl_games SET home_score = 31, away_score = 20 WHERE game_id = ?",
                             (g["game_id"],))
        self.db.conn.execute(
            "INSERT INTO nfl_player_games(game_id, player_id, season, week, team, opp, name, position, rushing_tds, "
            "receiving_tds) VALUES (?, 'rb_buf', 2026, 9, 'BUF', 'LAC', 'James Cook', 'RB', 2, 0)", (g["game_id"],))
        self.assertEqual(liquidar(self.nfl), 1)
        r = rendimiento(self.nfl)
        self.assertEqual((r["total"]["n"], r["total"]["acierto"]), (1, 1.0))
        self.assertAlmostEqual(r["total"]["beneficio"], 4.0)

    def test_backtest(self):
        filas = backtest(self.db.conn, "2026-10-01", "2026-10-31")
        self.assertTrue(filas)
        r = resumen(filas)
        self.assertIn("tds_1", r["stats"])
        self.assertTrue(all(0 <= f["prob"] <= 1 for f in filas))


if __name__ == "__main__":
    unittest.main()
