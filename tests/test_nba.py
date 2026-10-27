import random
import unittest
from datetime import date, timedelta
from pathlib import Path
from tempfile import TemporaryDirectory

from apuestas.db import Database
import json

from apuestas.nba.analizador import (analizar, emparejar_props, guardar_analisis, guardar_picks, liquidar, mejores,
                                     rendimiento)
from apuestas.nba.desglose import oportunidades
from apuestas.nba.db import NbaDB
from apuestas.nba.espn import grupo_posicion, parse_box, parse_shots
from apuestas.nba.informe import escribir
from apuestas.nba.modelo import construir_contexto, linea_segura, preparar_jugador, predecir, prob_lados
from apuestas.nba.sgo import americana_a_decimal, clave_nombre, parse_props
from apuestas.nba.zonas import zona

FECHA = "2026-03-01"
EQUIPOS = {"1": "Equipo Uno", "2": "Equipo Dos", "3": "Equipo Tres", "4": "Equipo Cuatro"}


def _summary(home: str, away: str, jugadores: list[dict], tiros: list[dict]) -> dict:
    """Resumen con la forma del de ESPN (solo los campos que se usan)."""
    labels = ["MIN", "PTS", "FG", "3PT", "FT", "REB", "AST", "TO", "STL", "BLK", "OREB", "DREB", "PF", "+/-"]
    players = []
    for team in (home, away):
        atletas = []
        for j in jugadores:
            if j["team"] != team:
                continue
            if j.get("dnp"):
                atletas.append({"athlete": {"id": j["id"], "displayName": j["name"]}, "didNotPlay": True, "stats": []})
                continue
            stats = [str(j["min"]), str(j["pts"]), f"{j['fgm']}-{j['fga']}", f"{j['tpm']}-{j['tpa']}",
                     f"{j['ftm']}-{j['fta']}", str(j["reb"]), str(j["ast"]), "2", "1", "1", "1",
                     str(j["reb"] - 1), "2", "0"]
            atletas.append({"athlete": {"id": j["id"], "displayName": j["name"],
                                        "position": {"abbreviation": j["pos"]}},
                            "starter": True, "stats": stats})
        players.append({"team": {"id": team}, "statistics": [{"labels": labels, "athletes": atletas}]})
    plays = [{"id": f"9{i}", "sequenceNumber": str(i), "shootingPlay": True, "type": {"text": "Jump Shot"},
              "text": t.get("text", "makes jumper"), "scoringPlay": t["made"], "pointsAttempted": t["value"],
              "coordinate": {"x": t["x"], "y": t["y"]}, "team": {"id": t["team"]},
              "participants": [{"athlete": {"id": t["player"]}}], "period": {"number": 1}}
             for i, t in enumerate(tiros)]
    plays.append({"id": "999", "sequenceNumber": "999", "shootingPlay": True, "type": {"text": "Free Throw - 1 of 2"},
                  "text": "x makes free throw 1 of 2", "scoringPlay": True, "pointsAttempted": 1,
                  "coordinate": {"x": -214748340, "y": -214748365}, "team": {"id": home},
                  "participants": [{"athlete": {"id": "p1"}}]})
    return {"boxscore": {"players": players}, "plays": plays}


def _llenar(db: NbaDB, dias: int = 30, seed: int = 3) -> None:
    """Liga sintética de 4 equipos: el jugador 'a1' anota de media 25 puntos en 34 minutos."""
    rng = random.Random(seed)
    base = date.fromisoformat(FECHA)
    for d in range(dias, 0, -1):
        fecha = (base - timedelta(days=d)).isoformat()
        cruces = (("1", "2"), ("3", "4")) if d % 2 else (("1", "3"), ("2", "4"))
        for k, (h, a) in enumerate(cruces):
            gid = f"g{d}{k}"
            g = {"id": gid, "date_utc": fecha + "T23:00Z", "season": 2026, "season_type": 2, "status": "STATUS_FINAL",
                 "home": {"id": h, "abbr": h, "name": EQUIPOS[h], "nickname": EQUIPOS[h].split()[1]},
                 "away": {"id": a, "abbr": a, "name": EQUIPOS[a], "nickname": EQUIPOS[a].split()[1]},
                 "home_pts": 100, "away_pts": 98}
            db.upsert_game(g, fecha)
            jugadores = []
            for team in (h, a):
                for n, pos in enumerate(("PG", "SF", "C")):
                    pts = max(0, int(rng.gauss(25 if (team, n) == ("1", 0) else 12, 5)))
                    jugadores.append({"team": team, "id": f"p{team}{n}" if (team, n) != ("1", 0) else "a1",
                                      "name": "Ángel Pérez Jr." if (team, n) == ("1", 0) else f"Jugador {team}{n}",
                                      "pos": pos, "min": 34 if n == 0 else 28, "pts": pts, "fgm": pts // 3,
                                      "fga": pts // 3 * 2 + 1, "tpm": 1, "tpa": 3, "ftm": 2, "fta": 3,
                                      "reb": rng.randint(3, 9), "ast": rng.randint(1, 7)})
            tiros = [{"team": h, "player": "a1" if h == "1" else f"p{h}0", "x": 25, "y": 2, "value": 2, "made": True},
                     {"team": a, "player": f"p{a}0", "x": 2, "y": 3, "value": 3, "made": False}]
            s = _summary(h, a, jugadores, tiros)
            db.save_box(gid, h, parse_box(s), parse_shots(s))
    db.commit()


class ParsersTest(unittest.TestCase):
    def test_zonas(self):
        self.assertEqual(zona(25, 1, 2), "aro")
        self.assertEqual(zona(23, 8, 2), "pintura")
        self.assertEqual(zona(6, 11, 2), "media")
        self.assertEqual(zona(1, 0, 3), "esquina3")
        self.assertEqual(zona(10, 22, 3), "triple")
        self.assertIsNone(zona(44, 51, 3))  # lanzamiento desde campo propio

    def test_box_y_tiros(self):
        s = _summary("1", "2", [
            {"team": "1", "id": "p1", "name": "Uno", "pos": "PG", "min": 30, "pts": 20, "fgm": 8, "fga": 15, "tpm": 2,
             "tpa": 5, "ftm": 2, "fta": 2, "reb": 5, "ast": 7},
            {"team": "2", "id": "p2", "name": "Dos", "pos": "C", "min": 25, "pts": 10, "fgm": 5, "fga": 8, "tpm": 0,
             "tpa": 0, "ftm": 0, "fta": 0, "reb": 12, "ast": 1},
            {"team": "2", "id": "p3", "name": "Tres", "dnp": True},
        ], [{"team": "1", "player": "p1", "x": 25, "y": 1, "value": 2, "made": True, "text": "p1 makes layup (p9 assists)"}])
        box = parse_box(s)
        self.assertEqual([b["player_id"] for b in box], ["p1", "p2"])  # quien no jugó no aparece
        self.assertEqual((box[0]["fgm"], box[0]["fga"], box[0]["opp_id"]), (8, 15, "2"))
        tiros = parse_shots(s)
        self.assertEqual(len(tiros), 1)  # el tiro libre no cuenta como tiro de campo
        self.assertEqual((tiros[0]["zone"], tiros[0]["assisted"], tiros[0]["opp_id"]), ("aro", 1, "2"))

    def test_minutos(self):
        from apuestas.nba.espn import _minutos
        self.assertEqual([_minutos(v) for v in ("34", "34:30", "-", "--", "DNP", None)], [34, 34.5, 0, 0, 0, 0])

    def test_posiciones(self):
        self.assertEqual([grupo_posicion(p) for p in ("PG", "SG", "G", "SF", "PF", "F", "C", None)],
                         ["G", "G", "G", "F", "F", "F", "C", "G"])

    def test_nombres_y_cuotas(self):
        self.assertEqual(clave_nombre("Jaren Jackson Jr."), "JAREN_JACKSON_JR")
        self.assertEqual(clave_nombre("Nikola Jokić"), "NIKOLA_JOKIC")
        self.assertEqual(clave_nombre("De'Aaron Fox"), "DEAARON_FOX")
        self.assertAlmostEqual(americana_a_decimal("+150"), 2.5)
        self.assertAlmostEqual(americana_a_decimal("-200"), 1.5)
        self.assertIsNone(americana_a_decimal(None))

    def test_parse_props(self):
        ev = {"players": {"X_1_NBA": {"name": "Equis"}}, "odds": {
            "a": {"statID": "points", "playerID": "X_1_NBA", "periodID": "game", "betTypeID": "ou", "sideID": "over",
                  "bookOddsAvailable": True, "bookOverUnder": "20.5", "bookOdds": "-110", "byBookmaker": {"fd": {}}},
            "b": {"statID": "points", "playerID": "X_1_NBA", "periodID": "game", "betTypeID": "ou", "sideID": "under",
                  "bookOddsAvailable": True, "bookOverUnder": "20.5", "bookOdds": "-110"},
            "c": {"statID": "points", "playerID": "X_1_NBA", "periodID": "1q", "betTypeID": "ou", "sideID": "over",
                  "bookOddsAvailable": True, "bookOverUnder": "5.5", "bookOdds": "-110"},
        }}
        props = parse_props(ev)
        self.assertEqual(len(props), 1)
        # Una línea sin ninguna casa detrás no es apostable: se descarta.
        del ev["odds"]["a"]["byBookmaker"]
        self.assertEqual(parse_props(ev), [])
        ev["odds"]["a"]["byBookmaker"] = {"fd": {}}
        props = parse_props(ev)
        self.assertEqual((props[0]["stat"], props[0]["line"], props[0]["books"]), ("points", 20.5, 1))
        # El lado "menos" no lo ofrece ninguna casa: sin cuota, no se puede apostar.
        self.assertEqual((props[0]["over_odd"], props[0]["under_odd"]), (americana_a_decimal("-110"), None))


class ModeloTest(unittest.TestCase):
    def test_prob_lados(self):
        o, u = prob_lados(20.5, 22.0, 40.0)
        self.assertAlmostEqual(o + u, 1.0, places=9)
        o, u = prob_lados(20, 22.0, 40.0)  # línea entera: el empate no es ni más ni menos
        self.assertLess(o + u, 1.0)
        mas, menos = linea_segura(22.0, 40.0, 0.8)
        self.assertGreaterEqual(prob_lados(mas, 22.0, 40.0)[0], 0.8)
        self.assertLess(prob_lados(mas + 1, 22.0, 40.0)[0], 0.8)
        self.assertGreaterEqual(prob_lados(menos, 22.0, 40.0)[1], 0.8)

    def test_media_coherente_con_historial(self):
        with TemporaryDirectory() as tmp:
            db = NbaDB(Database(Path(tmp) / "t.db").conn)
            _llenar(db)
            ctx = construir_contexto(db.conn, FECHA)
            j = preparar_jugador(ctx, "a1", "Ángel Pérez Jr.", "1", "2")
            # Juega todos los días en la liga sintética: segundo partido en dos noches, -3% de minutos.
            self.assertAlmostEqual(j.minutos, 34.0 * 0.97, places=6)
            self.assertTrue(any("dos noches" in n for n in j.notas))
            media = sum(p["pts"] for p in ctx.por_jugador["a1"]) / len(ctx.por_jugador["a1"]) * 0.97
            pred = predecir(ctx, j, "points")
            self.assertLess(abs(pred.mu - media), 0.2 * media)
            self.assertGreater(pred.var, pred.mu)  # incluye la incertidumbre de los minutos
            pra = predecir(ctx, j, "pra")
            self.assertGreater(pra.mu, pred.mu)
            # La media de PRA es la suma de sus componentes, cada uno con su explicación.
            self.assertEqual(set(pra.componentes), {"pts", "reb", "ast"})
            self.assertAlmostEqual(sum(c["final"] for c in pra.componentes.values()), pra.mu, places=6)
            self.assertIn("tiros de campo", pra.componentes["pts"]["explicacion"])
            self.assertIn("fallos del rival", pra.componentes["reb"]["explicacion"])

    def test_seguras(self):
        from apuestas.nba.modelo import es_titular, seguras
        with TemporaryDirectory() as tmp:
            db = NbaDB(Database(Path(tmp) / "t.db").conn)
            _llenar(db)
            ctx = construir_contexto(db.conn, FECHA)
            j = preparar_jugador(ctx, "a1", "Ángel Pérez Jr.", "1", "2")
            self.assertTrue(es_titular(j))
            s = {x.stat: x for x in seguras(ctx, j, 0.85)}
            # Titular con ~25 puntos: línea de puntos bastante por debajo de su media, al 85 % o más.
            self.assertIn("points", s)
            self.assertGreaterEqual(s["points"].prob, 0.85)
            self.assertLess(s["points"].line, s["points"].mu)
            self.assertAlmostEqual(s["points"].cuota_minima, 1 / s["points"].prob)
            # Con menos de 30 minutos esperados no hay picks seguros.
            j.minutos = 25
            self.assertEqual(seguras(ctx, j, 0.85), [])

    def test_columna_tipo_en_bases_viejas(self):
        import sqlite3
        conn = sqlite3.connect(":memory:")
        conn.execute("CREATE TABLE nba_picks (id INTEGER PRIMARY KEY, fecha TEXT)")
        NbaDB(conn)
        self.assertIn("tipo", {r[1] for r in conn.execute("PRAGMA table_info(nba_picks)")})

    def test_oportunidades(self):
        p = {"minutes": 24, "fga": 10, "fgm": 5, "tpa": 4, "tpm": 2, "fta": 4, "ftm": 3, "tov": 2, "oreb": 1,
             "dreb": 5, "ast": 6, "stl": 1, "blk": 1}
        mio = {"min": 240, "fga": 90, "fgm": 41, "tpa": 35, "tov": 12}
        rival = {"min": 240, "fga": 88, "fgm": 40, "tpa": 30, "tov": 15}
        o = oportunidades(p, mio, rival)
        # Medio partido en pista: la mitad de los 48 fallos del rival y de las 36 canastas de sus compañeros.
        self.assertEqual(o["dreb"], (5, 24.0))
        self.assertEqual(o["ast"], (6, 18.0))
        self.assertEqual(o["blk"], (1, 29.0))

    def test_flujo_completo(self):
        with TemporaryDirectory() as tmp:
            db = NbaDB(Database(Path(tmp) / "t.db").conn)
            _llenar(db)
            g = {"id": "hoy", "date_utc": FECHA + "T23:00Z", "season": 2026, "season_type": 2,
                 "status": "STATUS_SCHEDULED", "home_pts": None, "away_pts": None,
                 "home": {"id": "1", "abbr": "1", "name": "Equipo Uno", "nickname": "Uno"},
                 "away": {"id": "2", "abbr": "2", "name": "Equipo Dos", "nickname": "Dos"}}
            db.upsert_game(g, FECHA)
            db.save_injuries(FECHA, [{"team_id": "1", "player_id": "p11", "name": "Jugador 11", "status": "Out",
                                      "detail": ""}])
            evento = {"teams": {"home": {"names": {"long": "Equipo Uno", "medium": "Uno"}},
                                "away": {"names": {"long": "Equipo Dos", "medium": "Dos"}}},
                      "players": {"ANGEL_PEREZ_JR_1_NBA": {"name": "Angel Perez Jr."},
                                  "JUGADOR_11_1_NBA": {"name": "Jugador 11"}},
                      "odds": {f"{lado}{pid}": {"statID": "points", "playerID": pid, "periodID": "game",
                                                "betTypeID": "ou", "sideID": lado, "bookOddsAvailable": True,
                                                "bookOverUnder": "14.5", "bookOdds": "-110",
                                                "byBookmaker": {"fanduel": {}}}
                               for lado in ("over", "under") for pid in ("ANGEL_PEREZ_JR_1_NBA", "JUGADOR_11_1_NBA")}}
            ctx = construir_contexto(db.conn, FECHA)
            n, sin = emparejar_props(db, FECHA, [evento], ctx)
            self.assertEqual((n, sin), (2, []))  # el nombre con tilde se empareja igual
            partidos, ctx = analizar(db, FECHA)
            evs = partidos[0].evaluaciones
            self.assertEqual([e.player_id for e in evs], ["a1"])  # el lesionado (Out) queda fuera
            self.assertEqual(evs[0].lado, "más")
            self.assertGreater(evs[0].prob_modelo, 0.9)
            # Cuotas -110 / -110: la casa dice 50%, y la probabilidad final queda entre ambas.
            self.assertAlmostEqual(evs[0].prob_mercado, 0.5)
            self.assertAlmostEqual(evs[0].prob, 0.6 * evs[0].prob_modelo + 0.4 * 0.5)
            picks = mejores(partidos, 0.65)
            guardar_picks(db, FECHA, picks)
            guardar_analisis(db, FECHA, partidos)
            fila = db.conn.execute("SELECT * FROM nba_analisis WHERE player_id = 'a1'").fetchone()
            detalle = json.loads(fila["detalle"])
            self.assertIn("pts", detalle["componentes"])
            self.assertIn("Tiros de campo intentados", [m["metrica"] for m in detalle["metricas"]])
            md, js = escribir(Path(tmp), FECHA, ctx, partidos, picks, [])
            texto = md.read_text(encoding="utf-8")
            self.assertIn("Ángel Pérez Jr.: más de 14.5 puntos", texto)
            self.assertIn("¿Por qué", texto)

            # Liquidación: el partido termina con 30 puntos de a1.
            db.save_box("hoy", "1", [{"player_id": "a1", "team_id": "1", "opp_id": "2", "name": "a", "position": "G",
                                      "starter": 1, "minutes": 35, "pts": 30, "fgm": 10, "fga": 20, "tpm": 2,
                                      "tpa": 6, "ftm": 8, "fta": 9, "reb": 5, "oreb": 1, "dreb": 4, "ast": 6,
                                      "stl": 1, "blk": 0, "tov": 2, "pf": 2}], [])
            db.commit()
            self.assertEqual(liquidar(db), 1)
            r = rendimiento(db)
            self.assertEqual((r["total"]["n"], r["total"]["acierto"]), (1, 1.0))


if __name__ == "__main__":
    unittest.main()


class NbaStatsFalso:
    """stats.nba.com simulado con la forma de leaguegamelog y boxscorematchupsv3 (datos sintéticos)."""

    def __init__(self, db: NbaDB):
        self.peticiones = 0
        self.juegos = {}
        for g in db.conn.execute("SELECT g.*, h.name AS hn, a.name AS an FROM nba_games g JOIN nba_teams h ON "
                                 "h.id = g.home_id JOIN nba_teams a ON a.id = g.away_id WHERE g.box_ok = 1"):
            self.juegos["00" + g["id"]] = (g["fecha"], g["hn"], g["an"], g["home_id"], g["away_id"])

    def partidos(self, season, season_type):
        return [{"GAME_ID": gid, "GAME_DATE": f, "TEAM_NAME": n}
                for gid, (f, hn, an, _, _) in self.juegos.items() for n in (hn, an)]

    def enfrentamientos(self, gid):
        _, hn, an, h, a = self.juegos[gid]

        def equipo(nombre, team, rival):
            jugadores = []
            for n in range(3):
                pid = "a1" if (team, n) == ("1", 0) else f"p{team}{n}"
                nom = ("Angel", "Perez Jr.") if pid == "a1" else ("Jugador", f"{team}{n}")
                # Cada atacante lo marca sobre todo su par del rival; el base del equipo 2 defiende muy mal.
                marcas = []
                for k in range(3):
                    d = "a1" if (rival, k) == ("1", 0) else f"p{rival}{k}"
                    pos = 30.0 if k == n else 5.0
                    pts = pos * (1.6 if d == "p20" else 1.0)
                    marcas.append({"personId": hash(d) % 10 ** 6, "firstName": "Angel" if d == "a1" else "Jugador",
                                   "familyName": "Perez Jr." if d == "a1" else d[1:],
                                   "statistics": {"matchupMinutes": "6:30", "partialPossessions": pos,
                                                  "playerPoints": pts, "matchupFieldGoalsMade": 3,
                                                  "matchupFieldGoalsAttempted": 6}})
                jugadores.append({"personId": hash(pid) % 10 ** 6, "firstName": nom[0], "familyName": nom[1],
                                  "position": "G", "matchups": marcas})
            return {"teamName": nombre.split()[1], "players": jugadores}

        return {"boxScoreMatchups": {"gameId": gid, "homeTeam": equipo(hn, h, a), "awayTeam": equipo(an, a, h)}}


class EnfrentamientosTest(unittest.TestCase):
    def test_parse_y_marcaje(self):
        from apuestas.nba.enfrentamientos import descargar_temporada
        from apuestas.nba.nbastats import parse_enfrentamientos, temporada_nba
        self.assertEqual(temporada_nba(2026), "2025-26")
        with TemporaryDirectory() as tmp:
            db = NbaDB(Database(Path(tmp) / "t.db").conn)
            _llenar(db)
            ns = NbaStatsFalso(db)
            filas = parse_enfrentamientos(ns.enfrentamientos(next(iter(ns.juegos))))
            self.assertEqual(len(filas), 18)  # 6 atacantes × 3 defensores
            self.assertEqual(filas[0]["minutos"], 6.5)
            n = descargar_temporada(ns, db, 2026, 2)
            self.assertEqual((n["nuevos"], n["sin_espn"], n["jugadores_sin_emparejar"]), (60, 0, 0))
            # Ya descargados: no se vuelven a pedir.
            self.assertEqual(descargar_temporada(ns, db, 2026, 2)["nuevos"], 0)

            ctx = construir_contexto(db.conn, FECHA)
            j = preparar_jugador(ctx, "a1", "Ángel Pérez Jr.", "1", "2")
            e = j.enfrentamiento
            self.assertEqual(e.defensores[0]["nombre"], "Jugador 20")  # su par habitual en el rival
            self.assertGreater(e.factor, 1.0)  # Jugador 20 permite más puntos que la media
            self.assertLessEqual(e.factor, 1.12)
            pred = predecir(ctx, j, "points")
            self.assertIn("marcaje", pred.componentes["pts"]["explicacion"])
            # Si su defensor habitual está fuera hoy, deja de contar.
            j2 = preparar_jugador(ctx, "a1", "Ángel Pérez Jr.", "1", "2", fuera_rival=["p20"])
            self.assertNotIn("Jugador 20", [d["nombre"] for d in j2.enfrentamiento.defensores])
