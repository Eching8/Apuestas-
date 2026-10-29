"""Pruebas de la capa de datos con partidos sintéticos (nunca se usan fuera de las pruebas)."""
from __future__ import annotations

from datetime import datetime, timedelta

import pandas as pd
import pytest

from nbaev.data import asof, contexto, cuotas_csv, cuotas_sgo, db, espn, pbp
from nbaev.data.http import Limitador
from nbaev.data.nombres import clave_nombre, sin_sufijo
from nbaev.data.procesar import procesar

CASA, FUERA = "1", "2"
TIT_CASA = ["h1", "h2", "h3", "h4", "h5"]
TIT_FUERA = ["a1", "a2", "a3", "a4", "a5"]


def jugada(seq, periodo, reloj, tipo, texto, equipo=None, part=(), anota=False, valor=0, tiro=False, pa=0):
    return {"sequenceNumber": str(seq), "period": {"number": periodo}, "clock": {"displayValue": reloj},
            "type": {"id": str(seq), "text": tipo}, "text": texto, "team": {"id": equipo} if equipo else None,
            "participants": [{"athlete": {"id": p}} for p in part], "scoringPlay": anota,
            "scoreValue": valor, "shootingPlay": tiro, "pointsAttempted": pa}


def atleta(pid, starter, stats, dnp=False, reason=""):
    return {"athlete": {"id": pid, "displayName": f"Jugador {pid}", "position": {"abbreviation": "G"}},
            "starter": starter, "didNotPlay": dnp, "reason": reason, "stats": [] if dnp else stats}


LABELS = ["MIN", "PTS", "FG", "3PT", "FT", "REB", "AST", "TO", "STL", "BLK", "OREB", "DREB", "PF", "+/-"]


def resumen_sintetico():
    """Partido de 2 cuartos simplificado. h1 anota la primera canasta (triple asistido por h2)."""
    plays = [
        jugada(1, 1, "12:00", "Jumpball", "h5 vs. a5 (h1 gains possession)", CASA, ["h5", "a5", "h1"]),
        # Triple de h1 asistido por h2 (sin pointsAttempted, como en 2021: se deduce del valor anotado).
        jugada(2, 1, "11:40", "Jump Shot", "h1 makes 25-foot three point jumper (h2 assists)", CASA, ["h1", "h2"],
               anota=True, valor=3, tiro=True),
        # Fallo de a1 sin la palabra "three point" pero desde 26 pies: es triple.
        jugada(3, 1, "11:20", "Pullup Jump Shot", "a1 misses 26-foot pullup jump shot", FUERA, ["a1"], tiro=True),
        jugada(4, 1, "11:18", "Defensive Rebound", "h3 defensive rebound", CASA, ["h3"]),
        # Tapón: participantes [tirador, taponador].
        jugada(5, 1, "11:00", "Layup Shot", "a2 blocks h4 's layup", CASA, ["h4", "a2"], tiro=True, pa=2),
        jugada(6, 1, "10:58", "Offensive Rebound", "Team offensive rebound", CASA),  # de equipo: nadie
        # Pérdida con robo: [pierde, roba].
        jugada(7, 1, "10:40", "Bad Pass Turnover", "h2 bad pass (a3 steals)", CASA, ["h2", "a3"]),
        # "Kicked ball" es una violación, no una pérdida.
        jugada(8, 1, "10:30", "Kicked Ball", "a1 kicked ball violation", FUERA, ["a1"]),
        jugada(9, 1, "10:20", "Shooting Foul", "h3 shooting foul", CASA, ["h3"]),
        jugada(10, 1, "10:20", "Free Throw - 1 of 2", "a4 makes free throw 1 of 2", FUERA, ["a4"], anota=True, valor=1,
               tiro=True),
        jugada(11, 1, "10:20", "Free Throw - 2 of 2", "a4 misses free throw 2 of 2", FUERA, ["a4"], tiro=True),
        # Cambio a mitad del cuarto: [entra, sale].
        jugada(12, 1, "6:00", "Substitution", "h6 enters the game for h1", CASA, ["h6", "h1"]),
        jugada(13, 1, "0:00", "End Period", "End of the 1st Quarter"),
        # 2.º cuarto: h1 vuelve a empezar (sale en un cambio sin haber entrado: estaba en pista).
        jugada(14, 2, "9:00", "Substitution", "h6 enters the game for h1", CASA, ["h6", "h1"]),
        jugada(15, 2, "8:00", "Double Personal Foul", "h2 double personal foul (a1 draws the foul)", CASA, ["h2", "a1"]),
        jugada(16, 2, "5:00", "Driving Layup Shot", "a1 makes driving layup", FUERA, ["a1"], anota=True, valor=2,
               tiro=True, pa=2),
        jugada(17, 2, "0:00", "End Period", "End of the 2nd Quarter"),
    ]
    # El cuarto 2 empieza con h1 en lugar de h6: el 2.º cuarto, h6 no aparece antes de entrar.
    box_casa = [atleta(p, True, ["18", "0", "0-0", "0-0", "0-0", "0", "0", "0", "0", "0", "0", "0", "0", "0"])
                for p in TIT_CASA] + [atleta("h6", False, ["9", "0", "0-0", "0-0", "0-0", "0", "0", "0", "0", "0", "0", "0",
                                                          "0", "0"]),
                                      atleta("h7", False, [], dnp=True, reason="LEFT ANKLE SPRAIN"),
                                      atleta("h8", False, [], dnp=True, reason="COACH'S DECISION")]
    box_fuera = [atleta(p, True, ["24", "0", "0-0", "0-0", "0-0", "0", "0", "0", "0", "0", "0", "0", "0", "0"])
                 for p in TIT_FUERA]
    return {
        "header": {"id": "999", "competitions": [{
            "date": "2026-01-10T00:00Z", "status": {"type": {"name": "STATUS_FINAL"}},
            "competitors": [
                {"homeAway": "home", "team": {"id": CASA, "abbreviation": "AAA"}, "score": "3",
                 "linescores": [{"displayValue": "3"}, {"displayValue": "0"}]},
                {"homeAway": "away", "team": {"id": FUERA, "abbreviation": "BBB"}, "score": "3",
                 "linescores": [{"displayValue": "1"}, {"displayValue": "2"}]}]}]},
        "boxscore": {"players": [
            {"team": {"id": CASA}, "statistics": [{"labels": LABELS, "athletes": box_casa}]},
            {"team": {"id": FUERA}, "statistics": [{"labels": LABELS, "athletes": box_fuera}]}], "teams": []},
        "plays": plays,
        "pickcenter": [{"provider": {"name": "consensus", "priority": 0}, "details": "BBB -4.5", "overUnder": 221.5,
                        "homeTeamOdds": {"moneyLine": 160}, "awayTeamOdds": {"moneyLine": -190}}],
    }


# --- Jugada a jugada --------------------------------------------------------------------------------

def test_produccion_por_cuarto():
    p = procesar(resumen_sintetico())
    por = {(r["player_id"], r["period"]): r for r in p.periodos}
    assert por[("h1", 1)]["pts"] == 3 and por[("h1", 1)]["fg3m"] == 1
    assert por[("h2", 1)]["ast"] == 1 and por[("h2", 1)]["tov"] == 1
    assert por[("a3", 1)]["stl"] == 1
    assert por[("a2", 1)]["blk"] == 1 and por[("h4", 1)]["fga"] == 1 and por[("h4", 1)]["blk"] == 0
    assert por[("a1", 1)]["fg3a"] == 1          # triple deducido por la distancia
    assert por[("a1", 1)]["tov"] == 0           # kicked ball no es pérdida
    assert por[("a4", 1)]["ftm"] == 1 and por[("a4", 1)]["fta"] == 2 and por[("a4", 1)]["pts"] == 1
    assert por[("h3", 1)]["dreb"] == 1 and por[("h3", 1)]["pf"] == 1
    assert sum(r["oreb"] for r in p.periodos) == 0   # el rebote de equipo no es de nadie
    # Falta personal doble: cuenta para los dos.
    assert por[("h2", 2)]["pf"] == 1 and por[("a1", 2)]["pf"] == 1
    assert por[("a1", 2)]["pts"] == 2


def test_minutos_por_quinteto():
    p = procesar(resumen_sintetico())
    seg = {(r["player_id"], r["period"]): r["seconds"] for r in p.periodos}
    assert seg[("h1", 1)] == pytest.approx(360)      # sale a falta de 6:00
    assert seg[("h6", 1)] == pytest.approx(360)
    assert seg[("h1", 2)] == pytest.approx(180)      # empieza el 2.º cuarto y sale a falta de 9:00
    assert seg[("h6", 2)] == pytest.approx(540)
    assert seg[("h2", 1)] == pytest.approx(720) and seg[("h2", 2)] == pytest.approx(720)
    # Siempre cinco por equipo en cada tramo.
    assert all(len(t["lineup"]) == 5 for t in p.tramos)


def test_inicio_partido():
    ini = procesar(resumen_sintetico()).inicio
    assert ini["jump_winner_team"] == CASA
    assert ini["jump_home_player"] == "h5" and ini["jump_away_player"] == "a5"
    assert ini["first_fg_player"] == "h1" and ini["first_fg_team"] == CASA
    assert ini["away_first_pts_player"] == "a4"     # libre: primeros puntos del visitante
    assert ini["away_first_fg_player"] == "a1"      # primera canasta de campo del visitante
    assert ini["home_starters"] == TIT_CASA


def test_reloj_y_tiempo():
    assert pbp.reloj("11:38") == 698 and pbp.reloj("45.2") == pytest.approx(45.2)
    assert pbp.inicio_periodo(5) == 2880 and pbp.duracion(5) == 300


def test_ausencias_y_lineas():
    s = resumen_sintetico()
    jugaron, ausentes = espn.parse_box(s)
    assert {a["player_id"]: a["kind"] for a in ausentes} == {"h7": "lesion", "h8": "tecnica"}
    l = espn.parse_lineas(s)
    # Visitante favorito por 4.5 -> el local recibe +4.5.
    assert l["spread_home"] == 4.5 and l["total"] == 221.5


# --- HTTP ---------------------------------------------------------------------------------------------

def test_limitador_por_minuto():
    t = [0.0]
    esperas = []
    lim = Limitador(0, max_por_minuto=3, reloj=lambda: t[0], dormir=lambda s: (esperas.append(s), t.__setitem__(0, t[0] + s)))
    for _ in range(4):
        lim.esperar()
    assert len(esperas) == 1 and esperas[0] == pytest.approx(60.05)


# --- Cuotas ---------------------------------------------------------------------------------------

def test_americana_a_decimal():
    assert cuotas_sgo.americana_a_decimal("-110") == pytest.approx(1.9091, abs=1e-4)
    assert cuotas_sgo.americana_a_decimal("+150") == 2.5
    assert cuotas_sgo.americana_a_decimal("50") is None and cuotas_sgo.americana_a_decimal("x") is None


def evento_sgo(started=False):
    return {"eventID": "E1", "status": {"startsAt": "2026-01-10T00:00:00Z", "started": started},
            "teams": {"home": {"names": {"medium": "Aaa"}}, "away": {"names": {"medium": "Bbb"}}},
            "players": {"P1": {"name": "Jugador h1"}},
            "odds": {
                "o": {"statID": "points", "playerID": "P1", "periodID": "game", "betTypeID": "ou", "sideID": "over",
                      "bookOddsAvailable": True, "bookOdds": "-110", "bookOverUnder": "20.5",
                      "openBookOdds": "-115", "openBookOverUnder": "19.5", "closeBookOdds": "-125",
                      "closeBookOverUnder": "21.5", "score": 23,
                      "byBookmaker": {"fanduel": {"odds": "-105", "overUnder": "21.5", "available": True},
                                      "betmgm": {"odds": "-110", "overUnder": "20.5", "available": False}}},
                "n": {"statID": "fantasyScore", "playerID": "P1", "periodID": "1h", "betTypeID": "ou", "sideID": "over",
                      "bookOddsAvailable": True, "bookOdds": "+100", "bookOverUnder": "30.5"},
            }}


def test_parse_props_captura_e_historico():
    ahora = datetime(2026, 1, 9, 18)
    cap = cuotas_sgo.parse_props(evento_sgo(), "captura", ahora)
    assert {(f["book"], f["line"]) for f in cap if f["stat_id"] == "points"} == {("consenso", 20.5), ("fanduel", 21.5)}
    assert all(f["snapshot_at"] == ahora for f in cap)
    nuevo = [f for f in cap if f["stat_id"] == "fantasyScore"][0]
    assert nuevo["market"] is None
    hist = cuotas_sgo.parse_props(evento_sgo(), "historico", None)
    assert {(f["kind"], f["line"]) for f in hist} == {("apertura", 19.5), ("cierre", 21.5)}
    assert all(f["result"] == 23 for f in hist)


@pytest.fixture
def con():
    c = db.conectar(":memory:")
    db.upsert(c, "teams", [{"team_id": CASA, "abbr": "AAA", "name": "Equipo Aaa", "nickname": "Aaa"},
                           {"team_id": FUERA, "abbr": "BBB", "name": "Equipo Bbb", "nickname": "Bbb"},
                           {"team_id": "3", "abbr": "CCC", "name": "Equipo Ccc", "nickname": "Ccc"}])
    yield c
    c.close()


def _partido(gid, inicio, local, visitante, estado="STATUS_FINAL"):
    return {"game_id": gid, "season": 2025, "season_type": 2, "start_utc": inicio,
            "fecha": (inicio - timedelta(hours=5)).date(), "home_id": local, "away_id": visitante,
            "status": estado, "box_ok": True, "pbp_ok": True}


def test_catalogo_mercados_nuevos(con):
    filas = cuotas_sgo.parse_props(evento_sgo(), "captura", datetime(2026, 1, 9, 18))
    nuevos = cuotas_sgo.actualizar_catalogo(con, filas)
    assert ("sgo", "fantasyScore", "1h", "ou") in nuevos
    con.execute("UPDATE market_catalog SET estado = 'validado' WHERE stat_id = 'points'")
    assert cuotas_sgo.actualizar_catalogo(con, filas) == []      # ya conocidos
    estados = dict(con.execute("SELECT stat_id, estado FROM market_catalog").fetchall())
    assert estados == {"points": "validado", "fantasyScore": "sin validar"}   # no se pisa el estado


def test_emparejar_evento_y_jugadores(con):
    db.upsert(con, "games", [_partido("999", datetime(2026, 1, 10), CASA, FUERA)])
    guardar = __import__("nbaev.data.recolector", fromlist=["x"]).guardar_partido
    guardar(con, resumen_sintetico())
    n, gid = cuotas_sgo._guardar_evento(con, evento_sgo(), "captura", datetime(2026, 1, 9, 18))
    assert gid == "999"
    ids = con.execute("SELECT DISTINCT player_id, team_id FROM prop_odds").fetchall()
    assert ids == [("h1", CASA)]


# --- Anti-fuga -------------------------------------------------------------------------------------

def test_asof_partidos_y_cuotas(con):
    t0 = datetime(2026, 1, 10, 0, 0)
    db.upsert(con, "games", [_partido("g1", t0 - timedelta(days=1), CASA, FUERA),
                             _partido("g2", t0 - timedelta(hours=2), "3", FUERA),       # aún no "disponible"
                             _partido("g3", t0, CASA, "3", "STATUS_SCHEDULED")])
    previos = asof.partidos_previos(con, t0, horas=3.5)
    assert list(previos["game_id"]) == ["g1"]
    base = {"source": "sgo", "book": "consenso", "game_id": "g3", "start_utc": t0, "stat_id": "points",
            "period": "game", "bet_type": "ou", "source_player_id": "P1", "side": "over", "line": 20.5}
    db.insertar(con, "prop_odds", [
        {**base, "kind": "apertura", "snapshot_at": None, "odds": 1.9},
        {**base, "kind": "captura", "snapshot_at": t0 - timedelta(hours=3), "odds": 1.85},
        {**base, "kind": "captura", "snapshot_at": t0 + timedelta(minutes=5), "odds": 1.5},   # en vivo
        {**base, "kind": "cierre", "snapshot_at": None, "odds": 1.8, "result": 25},
    ])
    c = asof.cuotas_en(con, t0, ["g3"])
    assert list(c["odds"]) == [1.85] and "result" not in c.columns
    with pytest.raises(asof.FugaDeDatos):
        asof.verificar(pd.DataFrame({"start_utc": [t0]}), "start_utc", t0)


def test_lesiones_ultima_captura(con):
    t0 = datetime(2026, 1, 10)
    db.upsert(con, "injuries", [
        {"snapshot_at": t0 - timedelta(hours=10), "source": "espn", "team_id": CASA, "player_id": "h1", "status": "Out"},
        {"snapshot_at": t0 - timedelta(hours=1), "source": "espn", "team_id": CASA, "player_id": "h2",
         "status": "Questionable"},
        {"snapshot_at": t0 + timedelta(hours=1), "source": "espn", "team_id": CASA, "player_id": "h3", "status": "Out"},
    ])
    les = asof.lesiones_en(con, t0)
    assert list(les["player_id"]) == ["h2"]


# --- Contexto ---------------------------------------------------------------------------------------

def test_contexto_descanso_viaje_total(con):
    con.execute("UPDATE teams SET abbr = 'BOS' WHERE team_id = '1'")
    con.execute("UPDATE teams SET abbr = 'LAL' WHERE team_id = '2'")
    con.execute("UPDATE teams SET abbr = 'MIA' WHERE team_id = '3'")
    d = datetime(2026, 1, 10, 0)
    db.upsert(con, "games", [_partido("g1", d, "1", "2"), _partido("g2", d + timedelta(days=1), "3", "2"),
                             _partido("g3", d + timedelta(days=4), "2", "1")])
    db.upsert(con, "game_lines", [{"game_id": "g2", "source": "espn:consensus", "kind": "cierre", "spread_home": -6.0,
                                   "total": 220.0}])
    ctx = contexto.calcular(con).set_index(["game_id", "team_id"])
    lal_g2 = ctx.loc[("g2", "2")]
    assert lal_g2["b2b"] and lal_g2["dias_descanso"] == 0
    assert 2000 < lal_g2["km_viaje"] < 2200                     # Boston -> Miami
    assert lal_g2["total_implicito"] == pytest.approx(107.0)    # visitante: (220 - 6) / 2
    assert ctx.loc[("g2", "3")]["total_implicito"] == pytest.approx(113.0)
    assert ctx.loc[("g3", "2")]["dias_descanso"] == 2 and ctx.loc[("g3", "2")]["cambio_huso"] == -3


# --- CSV manual -----------------------------------------------------------------------------------

def test_importar_csv(con, tmp_path):
    db.upsert(con, "games", [_partido("999", datetime(2026, 1, 10), CASA, FUERA)])
    __import__("nbaev.data.recolector", fromlist=["x"]).guardar_partido(con, resumen_sintetico())
    f = tmp_path / "b365.csv"
    f.write_text("capturado,casa,fecha,local,visitante,jugador,mercado,periodo,linea,lado,cuota\n"
                 "2026-01-09T12:00:00-06:00,bet365,2026-01-09,AAA,Bbb,Jugador h1,pts,game,19.5,over,-120\n"
                 "2026-01-09T12:00:00-06:00,bet365,2026-01-09,AAA,Bbb,Jugador h1,pts_q3,3q,4.5,over,1.9\n"
                 "2026-01-09T12:00:00-06:00,bet365,2026-01-09,ZZZ,Bbb,Jugador h1,pts,game,19.5,over,1.9\n")
    r = cuotas_csv.importar(con, str(f))
    assert r["importadas"] == 2 and r["errores"] == 1
    fila = con.execute("SELECT player_id, odds, snapshot_at FROM prop_odds WHERE stat_id = 'pts'").fetchone()
    assert fila[0] == "h1" and fila[1] == pytest.approx(1.8333, abs=1e-3) and fila[2] == datetime(2026, 1, 9, 18)
    assert ("csv", "pts_q3", "3q", "ou") in r["mercados_nuevos"]


def test_emparejar_apodo(con):
    from nbaev.data.nombres import emparejar_jugadores
    db.upsert(con, "games", [_partido("g1", datetime(2026, 1, 10), CASA, FUERA)])
    db.insertar(con, "player_games", [{"game_id": "g1", "player_id": "77", "team_id": CASA, "name": "Ronald Holland II",
                                       "minutes": 20}, {"game_id": "g1", "player_id": "78", "team_id": FUERA,
                                                        "name": "Jalen Holland", "minutes": 20}])
    r = emparejar_jugadores(con, "sgo", {"RH": "Ron Holland", "XX": "Ron Smith"}, [CASA, FUERA], datetime(2026, 1, 11))
    assert r["RH"] == ("77", CASA) and r["XX"] == (None, None)


def test_nombres():
    assert clave_nombre("Nikola Jokić") == "NIKOLA_JOKIC"
    assert sin_sufijo(clave_nombre("Jaren Jackson Jr.")) == "JAREN_JACKSON"


def test_upsert_actualiza_solo_lo_que_viene(con):
    db.upsert(con, "teams", [{"team_id": CASA, "abbr": "XXX"}])
    assert con.execute("SELECT abbr, name FROM teams WHERE team_id = ?", [CASA]).fetchone() == ("XXX", "Equipo Aaa")


def test_odds_core_descarta_en_vivo():
    data = {"items": [{"provider": {"name": "ESPN Bet - Live Odds"}, "details": "BOS -2.5", "overUnder": 206.5},
                      {"provider": {"name": "ESPN BET"}, "details": "CLE -1.5", "overUnder": 229.5,
                       "homeTeamOdds": {"moneyLine": -125}, "awayTeamOdds": {"moneyLine": 105}}]}
    l = espn.parse_odds_core(data, "g1", "BOS", "CLE")
    assert l["source"] == "espn_core:ESPN BET" and l["spread_home"] == 1.5 and l["total"] == 229.5
    assert espn.spread_local("EVEN", "A", "B") == 0.0 and espn.spread_local("BOS -2.5", "BOS", "CLE") == -2.5
