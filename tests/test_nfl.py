import random
import unittest
from datetime import date, timedelta
from pathlib import Path
from tempfile import TemporaryDirectory

from apuestas.db import Database
from apuestas.nfl import equipos
from apuestas.nfl.analizador import (Evaluacion, analizar_partido, con_valor, evaluar_equipo, guardar_picks, liquidar,
                                     rendimiento)
from apuestas.nfl.backtest import backtest, resumen
from apuestas.nfl.db import STATS_JUGADOR, NflDB, estado_duda, estado_fuera
from apuestas.nfl.fuentes import (agregar_pbp, cambios_semanales, parse_calendario, parse_lesiones_espn,
                                  parse_stats_jugador, traspasos_en_texto)
from apuestas.nfl.informe import escribir
from apuestas.nfl.mercado import emparejar, parse_evento
from apuestas.nfl.modelo import (Linea, construir_contexto, entorno, p_al_menos, preparar_equipo, prob_lados,
                                 proyectar)
from apuestas.nfl.modelo_partido import prob_partido, simular
from apuestas.nfl.razones import Razones
from apuestas.nfl.validar import (buscar_jugador, interpretar, interpretar_equipo, oferta_equipo, texto_veredicto,
                                  validar)

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

# Defensores: (id, nombre, posición, equipo, tacleadas por partido, probabilidad de sack por partido)
DEFENSORES = [(f"lb_{t.lower()}", f"Linebacker {t}", "LB", t, 8, 0.2) for t in EQUIPOS] + \
             [(f"de_{t.lower()}", f"Ala {t}", "DE", t, 3, 0.6) for t in EQUIPOS]


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
            for pid, nombre, pos, eq, tackles, sacks in DEFENSORES:
                if eq != opp:
                    continue      # el defensor de 'opp' defiende contra 'team'
                fila = {k: "0" for k in STATS_JUGADOR}
                fila.update({"player_id": pid, "player_display_name": nombre, "position": pos, "season": "2026",
                             "week": str(w), "season_type": "REG", "game_id": gid, "team": opp, "opponent_team": team,
                             "def_tackles_solo": str(max(0, int(rng.gauss(tackles * 0.6, 1.5)))),
                             "def_tackle_assists": str(max(0, int(rng.gauss(tackles * 0.4, 1)))),
                             "def_sacks": str(int(rng.random() < sacks))})
                stats.append(fila)
            fila = {k: "0" for k in STATS_JUGADOR}
            fila.update({"player_id": f"k_{team.lower()}", "player_display_name": f"Pateador {team}", "position": "K",
                         "season": "2026", "week": str(w), "season_type": "REG", "game_id": gid, "team": team,
                         "opponent_team": opp, "fg_made": str(rng.choice((1, 2, 2, 3))), "fg_att": "3",
                         "pat_made": str(tds)})
            stats.append(fila)
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
    db.reemplazar_pbp(2026, agregar_pbp(pbp))
    db.actualizar_roster([{"player_id": pid, "name": n, "position": pos, "team": t, "status": "ACT", "season": 2026,
                           "week": 8} for pid, n, pos, t, *_ in PLANTILLA + DEFENSORES]
                         + [{"player_id": f"k_{t.lower()}", "name": f"Pateador {t}", "position": "K", "team": t,
                             "status": "ACT", "season": 2026, "week": 8} for t in EQUIPOS])
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
        r = agregar_pbp(filas)
        jug, eq, primeros = r.jugadores, r.equipos, r.primeros
        j = {x["player_id"]: x for x in jug}
        self.assertEqual((j["a"]["rz_carries"], j["a"]["i10_carries"], j["a"]["i5_carries"]), (1, 1, 1))
        self.assertEqual((j["b"]["rz_targets"], j["b"]["ez_targets"]), (1, 1))
        self.assertEqual((j["q"]["scrambles"], j["q"]["designed_runs"]), (1, 0))  # la de 2 puntos no cuenta
        e = {x["team"]: x for x in eq}
        self.assertEqual((e["BUF"]["rush_tds"], e["BUF"]["rz_trips"], e["BUF"]["rz_tds"]), (1, 1, 1))
        self.assertEqual((e["LAC"]["dropbacks"], e["LAC"]["carries"], e["LAC"]["qb_rush_yds"]), (1, 1, 12))
        self.assertEqual(primeros, {"g": "a"})

    def test_anotaciones(self):
        base = {"game_id": "g", "home_team": "BUF", "away_team": "LAC", "season": "2026", "week": "1"}
        filas = [
            {**base, "play_id": "1", "qtr": "1", "total_home_score": "0", "total_away_score": "0"},
            {**base, "play_id": "2", "qtr": "1", "posteam": "BUF", "defteam": "LAC", "play_type": "run",
             "touchdown": "1", "td_team": "BUF", "td_player_id": "a", "total_home_score": "6", "total_away_score": "0"},
            {**base, "play_id": "3", "qtr": "1", "posteam": "BUF", "play_type": "extra_point",
             "extra_point_result": "good", "total_home_score": "7", "total_away_score": "0"},
            {**base, "play_id": "4", "qtr": "2", "posteam": "LAC", "play_type": "field_goal",
             "field_goal_result": "made", "kick_distance": "52", "total_home_score": "7", "total_away_score": "3"},
        ]
        r = agregar_pbp(filas)
        self.assertEqual([(a["tipo"], a["team"], a["puntos"]) for a in r.anotaciones],
                         [("TD", "BUF", 6), ("XP", "BUF", 1), ("FG", "LAC", 3)])
        self.assertEqual(r.anotaciones[-1]["distancia"], 52.0)


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

    def test_regreso_de_titular(self):
        # James Cook faltó las semanas 7 y 8: Ray Davis jugó esos partidos sin él. Si Cook vuelve, a Davis se le
        # descuenta lo que ganó en su ausencia; si Cook sigue fuera, no.
        self.db.conn.execute("DELETE FROM nfl_player_games WHERE player_id = 'rb_buf' AND week >= 7")
        ctx = construir_contexto(self.db.conn, HOY)
        ent = entorno(ctx, "BUF", "LAC", True)
        con = {j.player_id: j for j in preparar_equipo(ctx, "BUF")}
        self.assertTrue(any("sin James Cook" in n for n in con["rb2_buf"].notas))
        self.assertFalse(any("sin Ray Davis" in n for n in con["rb_buf"].notas))
        ctx.lesiones["rb_buf"] = {"status": "Out", "detail": ""}
        sin = {j.player_id: j for j in preparar_equipo(ctx, "BUF")}
        self.assertFalse(any("sin James Cook" in n for n in sin["rb2_buf"].notas))
        self.assertGreater(proyectar(ctx, sin["rb2_buf"], ent).medias["rush_att"],
                           proyectar(ctx, con["rb2_buf"], ent).medias["rush_att"])

    def test_zona_roja(self):
        from apuestas.nfl.zona_roja import candidatos as cand_rz, defensa_rz, mapa
        ctx = construir_contexto(self.db.conn, HOY)
        ent = entorno(ctx, "BUF", "LAC", True)
        proys = [proyectar(ctx, j, ent) for j in preparar_equipo(ctx, "BUF")]
        d = defensa_rz(ctx, "LAC")
        self.assertEqual(set(d), {"QB", "RB", "WR", "TE"})
        self.assertTrue(all(0 <= x.tasa_carrera <= 1 and 0 <= x.tasa_envio <= 1 for x in d.values()))
        c = cand_rz(ctx, ent, proys)
        self.assertTrue(c)
        self.assertTrue(all(c[i].tds_rz >= c[i + 1].tds_rz for i in range(len(c) - 1)))
        lineas = mapa(ctx, ent, proys)
        self.assertTrue(lineas[0].startswith("Dónde se le anota a Chargers en la zona roja"))

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



def _evento_completo() -> dict:
    """Evento con mercados de partido, de periodo, defensivos y de pateador."""
    def o(oid, stat, ent, bet, side, periodo="game", line=None, spread=None, odds="-110", books=None, pid=None):
        return oid, {"oddID": oid, "statID": stat, "statEntityID": pid or ent, "playerID": pid, "periodID": periodo,
                     "betTypeID": bet, "sideID": side, "bookOddsAvailable": True, "bookOverUnder": line,
                     "bookSpread": spread, "bookOdds": odds,
                     "byBookmaker": books or {"fanduel": {"odds": odds, "overUnder": line, "spread": spread,
                                                         "available": True}}}
    odds = dict([
        o("ml-h", "points", "home", "ml", "home", odds="-200"), o("ml-a", "points", "away", "ml", "away", odds="+170"),
        o("sp-h", "points", "home", "sp", "home", spread="-4.5"), o("sp-a", "points", "away", "sp", "away", spread="+4.5"),
        o("tot-o", "points", "all", "ou", "over", line="48.5"), o("tot-u", "points", "all", "ou", "under", line="48.5"),
        o("tt-h", "points", "home", "ou", "over", line="26.5"),
        o("1h-o", "points", "all", "ou", "over", "1h", line="24.5"),
        o("3w-d", "points", "all", "ml3way", "draw", "1q", odds="+300"),
        o("eo", "points", "all", "eo", "even", odds="-105"),
        o("pri", "firstToScore", "home", "ml", "home", odds="-130"),
        o("amb", "bothTeamsScored", "all", "yn", "yes", "1q", odds="+130"),
        o("lead", "largestLead", "all", "ou", "over", line="14.5"),
        o("tds", "touchdowns", "all", "ou", "over", line="5.5"),
        o("perd", "turnovers", "all", "ou", "under", line="2.5"),
        o("sack", "defense_sacks", None, "ou", "over", line="0.5", odds="+150", pid="ALA_BUF_1_NFL"),
        o("tack", "defense_combinedTackles", None, "ou", "over", line="6.5", pid="LINEBACKER_BUF_1_NFL"),
        o("fg", "fieldGoals_made", None, "ou", "over", line="1.5", pid="PATEADOR_BUF_1_NFL"),
        o("ry1q", "rushing_yards", None, "ou", "over", "1q", line="20.5", pid="JAMES_COOK_1_NFL"),
        o("fan", "fantasyScore", None, "ou", "over", line="15.5", pid="JAMES_COOK_1_NFL"),
    ])
    for a, b in (("ml-h", "ml-a"), ("sp-h", "sp-a"), ("tot-o", "tot-u")):
        odds[a]["opposingOddID"], odds[b]["opposingOddID"] = b, a
    jugadores = {"ALA_BUF_1_NFL": "Ala BUF", "LINEBACKER_BUF_1_NFL": "Linebacker BUF",
                 "PATEADOR_BUF_1_NFL": "Pateador BUF", "JAMES_COOK_1_NFL": "James Cook"}
    return {"eventID": "EV2", "teams": {"home": {"names": {"long": "Buffalo Bills"}},
                                        "away": {"names": {"long": "Los Angeles Chargers"}}},
            "status": {}, "odds": odds,
            "players": {k: {"name": v, "teamID": "BUFFALO_BILLS_NFL"} for k, v in jugadores.items()}}


class TodosLosMercadosTest(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.db = Database(Path(self.tmp.name) / "t.db")
        self.nfl = NflDB(self.db.conn)
        _llenar(self.nfl)
        self.ctx = construir_contexto(self.db.conn, HOY)
        self.g = dict(self.db.conn.execute("SELECT * FROM nfl_games WHERE game_id = '2026_09_LAC_BUF'").fetchone())

    def tearDown(self):
        self.db.close()
        self.tmp.cleanup()

    def test_parse_mercados_de_partido(self):
        m = parse_evento(_evento_completo())
        cod = {(o.codigo, o.sgo_player_id, o.lado, o.line) for o in m.ofertas}
        self.assertIn(("pts@game/sp", "home", "home", -4.5), cod)
        self.assertIn(("pts@game/ml", "away", "away", 0.0), cod)
        self.assertIn(("pts@1h/ou", "all", "más", 24.5), cod)
        self.assertIn(("pts@1q/ml3way", "all", "draw", 0.0), cod)
        self.assertIn(("ambos@1q/yn", "all", "sí", 0.0), cod)
        self.assertIn(("rush_yds@1q", "JAMES_COOK_1_NFL", "más", 20.5), cod)
        self.assertIn(("sacks", "ALA_BUF_1_NFL", "más", 0.5), cod)
        self.assertEqual(m.spread_home, 4.5)
        sp = next(o for o in m.ofertas if o.codigo == "pts@game/sp" and o.lado == "home")
        self.assertAlmostEqual(sp.prob_casa(), 0.5, places=3)          # -110 / -110 sin margen

    def test_simulacion_coherente(self):
        sim = simular(self.ctx, "BUF", "LAC", n=1500)
        ph, _ = prob_partido(sim, "pts", "ml", "game", "home", "home", None)
        pa, _ = prob_partido(sim, "pts", "ml", "game", "away", "away", None)
        self.assertAlmostEqual(ph + pa, 1.0, places=6)
        o1, media = prob_partido(sim, "pts", "ou", "game", "all", "más", 40.5)
        o2, _ = prob_partido(sim, "pts", "ou", "game", "all", "más", 50.5)
        self.assertGreater(o1, o2)
        self.assertGreater(media, 20)
        f1, _ = prob_partido(sim, "primero", "ml", "game", "home", "home", None)
        f2, _ = prob_partido(sim, "primero", "ml", "game", "away", "away", None)
        self.assertAlmostEqual(f1 + f2, 1.0, places=6)
        d3, _ = prob_partido(sim, "pts", "ml3way", "1q", "all", "draw", None)
        self.assertTrue(0.05 < d3 < 0.6)
        h1, _ = prob_partido(sim, "pts", "ou", "1h", "all", "más", 0.5)
        self.assertGreater(h1, 0.9)

    def test_analisis_cubre_todo(self):
        m = parse_evento(_evento_completo())
        emparejar(m, [dict(r) for r in self.db.conn.execute("SELECT player_id, name, team FROM nfl_rosters")])
        a = analizar_partido(self.ctx, self.g, m)
        evaluadas = {e.codigo for e in a.evaluaciones}
        for c in ("pts@game/sp", "pts@game/ml", "pts@1h/ou", "pts@1q/ml3way", "pts@game/eo", "primero@game/ml",
                  "ambos@1q/yn", "ventaja@game/ou", "tds@game/ou", "perdidas@game/ou", "sacks", "tackles", "fg",
                  "rush_yds@1q", "fantasy"):
            self.assertIn(c, evaluadas, c)
        self.assertTrue(a.defensores)
        self.assertTrue(all(0 <= e.prob <= 1 for e in a.evaluaciones))

    def test_validar_equipo_y_liquidar(self):
        ap = interpretar_equipo("Bills -4.5")
        self.assertEqual((ap.bet, ap.entidad, ap.line), ("sp", "BUF", -4.5))
        ap2 = interpretar_equipo("más de 48.5 puntos Bills Chargers 1.ª mitad")
        self.assertEqual((ap2.bet, ap2.entidad, ap2.periodo, ap2.lado), ("ou", "ALL", "1h", "más"))
        m = parse_evento(_evento_completo())
        a = analizar_partido(self.ctx, self.g, m)
        of = oferta_equipo(ap, "BUF", "LAC", m)
        self.assertEqual(of.libros, {"fanduel": 1.909})
        e = evaluar_equipo(self.ctx, self.g, a.simulacion, of, a.claves)
        self.assertEqual(e.codigo, "pts@game/sp")
        primero = evaluar_equipo(self.ctx, self.g, a.simulacion,
                                 oferta_equipo(interpretar_equipo("Bills anota primero"), "BUF", "LAC", m), a.claves)
        guardar_picks(self.nfl, HOY, [e, primero], origen="validar")
        # Partido jugado: BUF 24 - LAC 17, LAC anota primero.
        c = self.db.conn
        c.execute("UPDATE nfl_games SET home_score = 24, away_score = 17 WHERE game_id = ?", (self.g["game_id"],))
        for k, (q, team, pts, h, aw) in enumerate([(1, "LAC", 7, 0, 7), (2, "BUF", 7, 7, 7), (3, "BUF", 10, 17, 7),
                                                    (4, "LAC", 10, 17, 17), (4, "BUF", 7, 24, 17)]):
            c.execute("INSERT INTO nfl_anotaciones(game_id, play_id, qtr, team, puntos, tipo, home_score, away_score) "
                      "VALUES (?, ?, ?, ?, ?, 'TD', ?, ?)", (self.g["game_id"], k, q, team, pts, h, aw))
        c.execute("INSERT INTO nfl_player_games(game_id, player_id, season, week, team, opp) "
                  "VALUES (?, 'rb_buf', 2026, 9, 'BUF', 'LAC')", (self.g["game_id"],))
        self.assertEqual(liquidar(self.nfl), 2)
        res = {r["stat"]: (r["resultado"], r["acierto"]) for r in c.execute("SELECT * FROM nfl_picks")}
        self.assertEqual(res["pts@game/sp"], (7.0, 1))         # ganó por 7 > 4.5
        self.assertEqual(res["primero@game/ml"], (0.0, 0))     # anotó primero LAC

    def test_razones_vacias_no_rompen_etiquetas(self):
        e = Evaluacion("g", "ALL", "Partido", "-", "ALL", "-", "pts", 44.5, "más", 0.5, 0.5, 0.5, 44, 1.9, "fd",
                       1.9, -0.05, Razones([], [], []), None, "1h", "equipo", "ou")
        self.assertEqual(e.etiqueta(), "Total más de 44.5 puntos (1.ª mitad)")


if __name__ == "__main__":
    unittest.main()
