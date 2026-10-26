"""Cuotas de SportsGameOdds (https://sportsgameodds.com/docs): props de jugadores y líneas del partido.

- Capturas del día (`kind = captura`): consenso y cada casa disponible, con la hora de la captura.
- Histórico (`kind = apertura | cierre`): líneas de consenso de apertura y de cierre de partidos pasados,
  con el resultado real de cada prop. Los valores por casa de un partido terminado pueden ser de
  apuestas en vivo, así que en el histórico solo se usa el consenso.

El plan amateur permite 10 peticiones por minuto y 2.500 "entidades" (partidos) al mes: cada partido
devuelto cuesta una entidad. Antes de descargar histórico se consulta el saldo y se respeta
`reserva_entidades` para las capturas diarias. bet365 no aparece en esta fuente: sus cuotas se cargan
por CSV (ver cuotas_csv.py).
"""
from __future__ import annotations

import logging
import os
from datetime import date, datetime, time, timedelta, timezone

import duckdb

from . import db, espn
from .http import ClienteHttp, Limitador
from .nombres import clave_nombre, emparejar_jugadores

log = logging.getLogger(__name__)

# statID de SportsGameOdds -> mercado normalizado. Lo que no esté aquí se guarda igual (market NULL)
# y entra en el catálogo como mercado nuevo "sin validar".
MERCADOS = {
    "points": "pts", "rebounds": "reb", "offensiveRebounds": "oreb", "defensiveRebounds": "dreb",
    "assists": "ast", "threePointersMade": "fg3m", "steals": "stl", "blocks": "blk", "turnovers": "tov",
    "fieldGoalsMade": "fgm", "freeThrowsMade": "ftm", "points+rebounds": "pr", "points+assists": "pa",
    "rebounds+assists": "ra", "points+rebounds+assists": "pra", "blocks+steals": "stocks",
    "doubleDouble": "doble_doble", "tripleDouble": "triple_doble", "firstBasket": "primera_canasta",
    "firstToScore": "primer_anotador", "teamFirstBasket": "primera_canasta_equipo",
}
# Mercados que el sistema sabe modelar (los demás se registran pero no se evalúan).
MODELADOS = set(MERCADOS.values())


def americana_a_decimal(v) -> float | None:
    try:
        a = float(str(v).replace("+", ""))
    except (TypeError, ValueError):
        return None
    if a == 0 or -100 < a < 100:
        return None
    return round(1 + (a / 100 if a > 0 else 100 / -a), 4)


def _num(v) -> float | None:
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


class SportsGameOdds:
    def __init__(self, cfg: dict, session=None):
        c = cfg["fuentes"]["sportsgameodds"]
        clave = os.environ.get("SPORTSGAMEODDS_KEY", "")
        # En este entorno el proxy inyecta la clave; fuera de él se usa SPORTSGAMEODDS_KEY.
        self.http = ClienteHttp(c["url"], Limitador(0.2, c["max_peticiones_minuto"]), reintentos=4, timeout=40,
                                cabeceras={"X-Api-Key": clave} if clave else None, session=session,
                                nombre="SportsGameOdds")
        self.reserva = int(c.get("reserva_entidades", 0))

    def uso(self) -> dict:
        lim = self.http.get_json("/account/usage")["data"]["rateLimits"]["per-month"]
        maximo = lim.get("max-entities")
        usado = int(lim.get("current-entities") or 0)
        restante = None if maximo in (None, "unlimited") else int(maximo) - usado
        return {"max": maximo, "usado": usado, "restante": restante}

    def eventos(self, inicio: datetime, fin: datetime, **extra) -> list[dict]:
        """Partidos de la NBA que empiezan entre inicio y fin (UTC)."""
        out, cursor = [], None
        while True:
            params = {"leagueID": "NBA", "limit": 25, "startsAfter": inicio.strftime("%Y-%m-%dT%H:%M:%SZ"),
                      "startsBefore": fin.strftime("%Y-%m-%dT%H:%M:%SZ"), **extra}
            if cursor:
                params["cursor"] = cursor
            data = self.http.get_json("/events", **params)
            if data.get("notice"):
                log.debug("SportsGameOdds: %s", data["notice"])
            out += data.get("data", [])
            cursor = data.get("nextCursor")
            if not cursor or not data.get("data"):
                return out


def ventana_et(fecha: date) -> tuple[datetime, datetime]:
    """Día de la NBA (hora del este) de 06:00 a 06:00 del día siguiente, en UTC."""
    ini = datetime.combine(fecha, time(6), tzinfo=espn.ET).astimezone(timezone.utc)
    return ini, ini + timedelta(days=1)


# --- Parseo -------------------------------------------------------------------------------------

def parse_props(evento: dict, kind: str, snapshot_at: datetime | None) -> list[dict]:
    """Filas de prop_odds. kind = captura (consenso + cada casa) | historico (apertura y cierre)."""
    jugadores = evento.get("players") or {}
    start = espn.utc_naive(evento["status"]["startsAt"])
    filas = []
    for o in (evento.get("odds") or {}).values():
        pid = o.get("playerID")
        if not pid or o.get("betTypeID") not in ("ou", "yn"):
            continue
        info = jugadores.get(pid) or {}
        base = {"source": "sgo", "event_id": evento["eventID"], "start_utc": start, "stat_id": o.get("statID"),
                "market": MERCADOS.get(o.get("statID")), "period": o.get("periodID"), "bet_type": o.get("betTypeID"),
                "source_player_id": pid, "player_name": info.get("name") or o.get("marketName", pid),
                "side": o.get("sideID"), "result": _num(o.get("score"))}
        if kind == "captura":
            if o.get("cancelled") or not o.get("bookOddsAvailable"):
                continue
            filas.append({**base, "kind": "captura", "snapshot_at": snapshot_at, "book": "consenso",
                          "line": _num(o.get("bookOverUnder")), "odds": americana_a_decimal(o.get("bookOdds"))})
            for casa, b in (o.get("byBookmaker") or {}).items():
                if not b.get("available"):
                    continue
                filas.append({**base, "kind": "captura", "snapshot_at": snapshot_at, "book": casa,
                              "line": _num(b.get("overUnder")), "odds": americana_a_decimal(b.get("odds"))})
        else:
            if o.get("cancelled"):
                continue
            for k, pref in (("apertura", "open"), ("cierre", "close")):
                cuota = americana_a_decimal(o.get(f"{pref}BookOdds"))
                if cuota is None:
                    continue
                filas.append({**base, "kind": k, "snapshot_at": None, "book": "consenso",
                              "line": _num(o.get(f"{pref}BookOverUnder")), "odds": cuota})
    return [f for f in filas if f["odds"] is not None]


def parse_lineas_partido(evento: dict, kind: str, snapshot_at: datetime | None) -> list[dict]:
    """Spread, total y ganador del partido (consenso)."""
    odds = evento.get("odds") or {}

    def buscar(stat_entity, bet, side):
        for o in odds.values():
            if (o.get("statID") == "points" and o.get("statEntityID") == stat_entity and o.get("periodID") == "game"
                    and o.get("betTypeID") == bet and o.get("sideID") == side):
                return o
        return None

    sp, tot = buscar("home", "sp", "home"), buscar("all", "ou", "over")
    mlh, mla = buscar("home", "ml", "home"), buscar("away", "ml", "away")
    filas = []
    tomas = [("captura", "")] if kind == "captura" else [("apertura", "open"), ("cierre", "close")]
    for k, pref in tomas:
        campo = (lambda n: f"{pref}{n[0].upper()}{n[1:]}") if pref else (lambda n: n)
        fila = {"source": "sgo", "kind": k, "snapshot_at": snapshot_at,
                "spread_home": _num(sp and sp.get(campo("bookSpread"))),
                "total": _num(tot and tot.get(campo("bookOverUnder"))),
                "ml_home": _num(mlh and str(mlh.get(campo("bookOdds"))).replace("+", "")),
                "ml_away": _num(mla and str(mla.get(campo("bookOdds"))).replace("+", ""))}
        if any(fila[c] is not None for c in ("spread_home", "total", "ml_home")):
            filas.append(fila)
    return filas


# --- Emparejamiento con ESPN --------------------------------------------------------------------

def emparejar_evento(con: duckdb.DuckDBPyConnection, evento: dict) -> str | None:
    """game_id de ESPN del mismo partido: mismo apodo de local y visitante y hora de inicio cercana."""
    previo = con.execute("SELECT game_id FROM event_map WHERE source = 'sgo' AND event_id = ?",
                         [evento["eventID"]]).fetchone()
    if previo:
        return previo[0]
    t = evento.get("teams") or {}
    apodo = {lado: clave_nombre((t.get(lado, {}).get("names") or {}).get("medium", "")) for lado in ("home", "away")}
    start = espn.utc_naive(evento["status"]["startsAt"])
    filas = con.execute("""
        SELECT g.game_id, h.nickname, a.nickname FROM games g
        JOIN teams h ON h.team_id = g.home_id JOIN teams a ON a.team_id = g.away_id
        WHERE g.start_utc BETWEEN ? AND ?""", [start - timedelta(hours=14), start + timedelta(hours=14)]).fetchall()
    for gid, hn, an in filas:
        if clave_nombre(hn) == apodo["home"] and clave_nombre(an) == apodo["away"]:
            db.upsert(con, "event_map", [{"source": "sgo", "event_id": evento["eventID"], "game_id": gid}])
            return gid
    return None


def completar_ids(con: duckdb.DuckDBPyConnection, filas: list[dict], game_id: str | None) -> None:
    """Rellena game_id, player_id y team_id de ESPN en las filas de un evento."""
    if not filas:
        return
    if game_id is None:
        for f in filas:
            f["game_id"] = None
            f["player_id"] = None
        return
    home, away, inicio = con.execute("SELECT home_id, away_id, start_utc FROM games WHERE game_id = ?",
                                     [game_id]).fetchone()
    nombres = {f["source_player_id"]: f["player_name"] for f in filas}
    mapa = emparejar_jugadores(con, "sgo", nombres, [home, away], inicio)
    for f in filas:
        f["game_id"] = game_id
        f["player_id"], f["team_id"] = mapa.get(f["source_player_id"], (None, None))


def reemparejar_pendientes(con: duckdb.DuckDBPyConnection) -> int:
    """Vuelve a emparejar los jugadores sin player_id de las cuotas ya guardadas (tras mejorar el emparejamiento)."""
    pendientes = con.execute("""SELECT DISTINCT game_id FROM prop_odds
                                WHERE player_id IS NULL AND game_id IS NOT NULL""").fetchall()
    for (gid,) in pendientes:
        filas = con.execute("""SELECT DISTINCT source, source_player_id, player_name FROM prop_odds
                               WHERE game_id = ? AND player_id IS NULL""", [gid]).df().to_dict("records")
        for fuente in {f["source"] for f in filas}:
            de_fuente = [f for f in filas if f["source"] == fuente]
            home, away, inicio = con.execute("SELECT home_id, away_id, start_utc FROM games WHERE game_id = ?",
                                             [gid]).fetchone()
            mapa = emparejar_jugadores(con, fuente, {f["source_player_id"]: f["player_name"] for f in de_fuente},
                                       [home, away], inicio)
            for sid, (pid, team) in mapa.items():
                if pid:
                    con.execute("""UPDATE prop_odds SET player_id = ?, team_id = ? WHERE game_id = ? AND source = ?
                                   AND source_player_id = ? AND player_id IS NULL""", [pid, team, gid, fuente, sid])
    return con.execute("SELECT count(*) FROM prop_odds WHERE player_id IS NULL").fetchone()[0]


# --- Catálogo de mercados -----------------------------------------------------------------------

def actualizar_catalogo(con: duckdb.DuckDBPyConnection, filas: list[dict]) -> list[tuple]:
    """Registra cada combinación (fuente, stat, periodo, tipo) vista. Devuelve las nuevas, que entran
    como 'sin validar' (el backtest es el único que puede cambiar ese estado)."""
    vistos: dict[tuple, list] = {}
    for f in filas:
        k = (f["source"], f["stat_id"], f["period"], f["bet_type"])
        vistos.setdefault(k, [f["market"], 0])[1] += 1
    ahora = db.ahora_utc()
    nuevos = []
    for (fuente, stat, per, bet), (mercado, n) in vistos.items():
        clave = [fuente, stat, per, bet]
        if con.execute("SELECT 1 FROM market_catalog WHERE source = ? AND stat_id = ? AND period = ? AND bet_type = ?",
                       clave).fetchone():
            con.execute("UPDATE market_catalog SET last_seen = ?, veces = veces + ? WHERE source = ? AND stat_id = ? "
                        "AND period = ? AND bet_type = ?", [ahora, n, *clave])
            continue
        con.execute("INSERT INTO market_catalog VALUES (?, ?, ?, ?, ?, ?, 'sin validar', ?, ?, ?)",
                    [*clave, mercado, mercado in MODELADOS, ahora, ahora, n])
        nuevos.append((fuente, stat, per, bet))
    if nuevos:
        log.warning("Mercados nuevos detectados (sin validar): %s", ", ".join("/".join(map(str, x)) for x in nuevos))
    return nuevos


# --- Flujos ---------------------------------------------------------------------------------------

def _guardar_evento(con, ev, kind, snapshot_at) -> tuple[int, str | None]:
    gid = emparejar_evento(con, ev)
    filas = parse_props(ev, kind, snapshot_at)
    completar_ids(con, filas, gid)
    actualizar_catalogo(con, filas)
    if kind != "captura":
        # El histórico de un evento se reemplaza entero (idempotente).
        con.execute("DELETE FROM prop_odds WHERE source = 'sgo' AND event_id = ? AND kind IN ('apertura', 'cierre')",
                    [ev["eventID"]])
    db.insertar(con, "prop_odds", filas)
    if gid:
        lineas = [{"game_id": gid, **l} for l in parse_lineas_partido(ev, kind, snapshot_at)]
        if kind == "captura":
            for l in lineas:
                l["kind"] = f"captura {snapshot_at:%Y-%m-%dT%H:%M}"
        db.upsert(con, "game_lines", lineas)
    return len(filas), gid


def capturar_dia(con: duckdb.DuckDBPyConnection, cfg: dict, fecha: date, cliente: SportsGameOdds | None = None) -> dict:
    """Captura las cuotas actuales de los partidos de una fecha (hora del este) aún no empezados."""
    cli = cliente or SportsGameOdds(cfg)
    ini, fin = ventana_et(fecha)
    eventos = cli.eventos(ini, fin, oddsAvailable="true")
    ahora = db.ahora_utc()
    total, sin_partido = 0, 0
    for ev in eventos:
        if (ev.get("status") or {}).get("started"):
            continue
        n, gid = _guardar_evento(con, ev, "captura", ahora)
        total += n
        sin_partido += gid is None
    db.registrar(con, "sgo", f"captura:{fecha}:{ahora:%H%M}", "ok", f"{len(eventos)} eventos, {total} cuotas")
    return {"eventos": len(eventos), "cuotas": total, "sin_emparejar": sin_partido, "peticiones": cli.http.peticiones}


def descargar_historico(con: duckdb.DuckDBPyConnection, cfg: dict, desde: date, hasta: date,
                        max_partidos: int | None = None, cliente: SportsGameOdds | None = None,
                        respetar_reserva: bool = True) -> dict:
    """Apertura y cierre de consenso de cada prop, día a día. Para antes de gastar la reserva mensual
    (salvo en el cierre diario de ayer, que es justo para lo que existe la reserva)."""
    cli = cliente or SportsGameOdds(cfg)
    uso = cli.uso()
    reserva = cli.reserva if respetar_reserva else 0
    disponible = None if uso["restante"] is None else uso["restante"] - reserva
    if max_partidos is not None:
        disponible = max_partidos if disponible is None else min(disponible, max_partidos)
    log.info("SportsGameOdds: usado %s de %s entidades este mes; disponibles para histórico: %s",
             uso["usado"], uso["max"], disponible)
    hechos = {r[0] for r in con.execute(
        "SELECT key FROM ingest_log WHERE source = 'sgo' AND status = 'ok' AND key LIKE 'historico:%'").fetchall()}
    # Solo días con partidos en la base (evita gastar peticiones en días sin NBA).
    dias = [r[0] for r in con.execute(
        "SELECT DISTINCT fecha FROM games WHERE fecha BETWEEN ? AND ? AND status = 'STATUS_FINAL' ORDER BY fecha",
        [desde, hasta]).fetchall()]
    gastado = eventos_ok = cuotas = 0
    for dia in dias:
        if f"historico:{dia}" in hechos:
            continue
        n_partidos = con.execute("SELECT count(*) FROM games WHERE fecha = ?", [dia]).fetchone()[0]
        if disponible is not None and gastado + n_partidos > disponible:
            log.warning("Se alcanza el tope de entidades: paro antes del %s", dia)
            break
        ini, fin = ventana_et(dia)
        eventos = cli.eventos(ini, fin)
        gastado += len(eventos)
        for ev in eventos:
            n, _ = _guardar_evento(con, ev, "historico", None)
            cuotas += n
            eventos_ok += 1
        db.registrar(con, "sgo", f"historico:{dia}", "ok", f"{len(eventos)} eventos")
    return {"dias": len(dias), "eventos": eventos_ok, "cuotas": cuotas, "entidades_gastadas": gastado,
            "peticiones": cli.http.peticiones}
