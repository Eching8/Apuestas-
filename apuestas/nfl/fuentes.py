"""Fuentes de datos de la NFL, todas gratuitas y sin clave.

- nflverse (https://github.com/nflverse/nflverse-data): estadísticas por jugador y partido, jugada a jugada,
  calendario con líneas de cierre y clima, plantillas semana a semana, parte oficial de lesiones y snaps.
  Se actualiza cada noche durante la temporada.
- ESPN (API pública): calendario del día, parte de lesiones al momento y movimientos de plantilla (traspasos).
"""
from __future__ import annotations

import csv
import gzip
import io
import logging
import re
import time
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Iterator

import requests

from ..api_football import ApiError
from ..nba.espn import Espn
from . import equipos

log = logging.getLogger(__name__)

NFLVERSE_URL = "https://github.com/nflverse/nflverse-data/releases/download"
ESPN_NFL_URL = "https://site.api.espn.com/apis/site/v2/sports/football/nfl"
POSICIONES_ATAQUE = ("QB", "RB", "FB", "WR", "TE")


class Nflverse:
    def __init__(self, session: requests.Session | None = None, base_url: str = NFLVERSE_URL):
        self.base_url = base_url
        self.session = session or requests.Session()
        self.descargas = 0

    def url(self, ruta: str) -> str:
        return f"{self.base_url}/{ruta}"

    def descargar(self, ruta: str, etag: str | None = None) -> tuple[list[dict] | None, str | None]:
        """Filas del CSV (o None si no cambió desde el etag dado, o si aún no existe) y el etag nuevo."""
        url = self.url(ruta)
        headers = {"If-None-Match": etag} if etag else {}
        for intento in range(4):
            try:
                resp = self.session.get(url, headers=headers, timeout=180)
            except requests.RequestException as e:
                log.warning("nflverse %s: %s (reintento %d)", ruta, e, intento + 1)
                time.sleep(2 ** intento)
                continue
            if resp.status_code == 304:
                return None, etag
            if resp.status_code == 404:
                log.info("nflverse aún no publica %s", ruta)
                return None, etag
            if resp.status_code in (429, 500, 502, 503, 504):
                time.sleep(2 ** (intento + 1))
                continue
            if resp.status_code != 200:
                raise ApiError(f"nflverse {ruta}: HTTP {resp.status_code}")
            self.descargas += 1
            data = resp.content
            if ruta.endswith(".gz"):
                data = gzip.decompress(data)
            return list(csv.DictReader(io.StringIO(data.decode("utf-8")))), resp.headers.get("ETag")
        raise ApiError(f"nflverse {ruta}: sin respuesta tras varios intentos")


class EspnNfl(Espn):
    def __init__(self, session: requests.Session | None = None):
        super().__init__(session, base_url=ESPN_NFL_URL)

    def lesiones(self) -> list[dict]:
        return parse_lesiones_espn(self._get("/injuries"))

    def transacciones(self, limite: int = 200) -> list[dict]:
        return parse_transacciones(self._get("/transactions", limit=limite))


# --- Conversión ------------------------------------------------------------------------

def num(v) -> float | None:
    if v in (None, "", "NA", "nan"):
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _int(v) -> int | None:
    x = num(v)
    return None if x is None else int(x)


# --- Calendario --------------------------------------------------------------------------

def parse_calendario(filas: Iterator[dict], temporadas: set[int]) -> list[dict]:
    out = []
    for f in filas:
        season = _int(f.get("season"))
        if season not in temporadas:
            continue
        out.append({
            "game_id": f["game_id"], "season": season, "game_type": f.get("game_type"), "week": _int(f.get("week")),
            "gameday": f["gameday"], "gametime": f.get("gametime"),
            "home_team": equipos.normalizar(f["home_team"]) or f["home_team"],
            "away_team": equipos.normalizar(f["away_team"]) or f["away_team"],
            "home_score": _int(f.get("home_score")), "away_score": _int(f.get("away_score")),
            "spread_line": num(f.get("spread_line")), "total_line": num(f.get("total_line")),
            "home_moneyline": num(f.get("home_moneyline")), "away_moneyline": num(f.get("away_moneyline")),
            "roof": f.get("roof") or None, "surface": f.get("surface") or None,
            "temp": num(f.get("temp")), "wind": num(f.get("wind")), "div_game": _int(f.get("div_game")),
            "home_rest": _int(f.get("home_rest")), "away_rest": _int(f.get("away_rest")),
            "home_qb_id": f.get("home_qb_id") or None, "away_qb_id": f.get("away_qb_id") or None,
            "espn_id": f.get("espn") or None,
        })
    return out


# --- Estadísticas por jugador ------------------------------------------------------------

def parse_stats_jugador(filas: Iterator[dict], columnas: tuple[str, ...]) -> list[dict]:
    out = []
    for f in filas:
        if not f.get("player_id") or not f.get("game_id"):
            continue  # filas de equipo sin jugador
        fila = {
            "game_id": f["game_id"], "player_id": f["player_id"], "season": _int(f["season"]),
            "week": _int(f["week"]), "season_type": f.get("season_type"),
            "team": equipos.normalizar(f["team"]) or f["team"],
            "opp": equipos.normalizar(f["opponent_team"]) or f["opponent_team"],
            "name": f.get("player_display_name") or f.get("player_name"), "position": f.get("position") or None,
        }
        for c in columnas:
            fila[c] = num(f.get(c))
        out.append(fila)
    return out


# --- Jugada a jugada ---------------------------------------------------------------------

@dataclass
class ResumenPbp:
    jugadores: list[dict]                 # una fila por jugador y partido (zona roja, jugada más larga...)
    equipos: list[dict]                   # una fila por equipo y partido (ataque)
    primeros: dict[str, str]              # game_id -> autor del primer TD
    anotaciones: list[dict] = field(default_factory=list)   # cada cambio en el marcador
    cuartos: list[dict] = field(default_factory=list)       # jugador × partido × cuarto


def _tipo_anotacion(f: dict) -> str:
    if num(f.get("touchdown")) == 1:
        return "TD"
    if f.get("field_goal_result") == "made":
        return "FG"
    if f.get("extra_point_result") == "good":
        return "XP"
    if f.get("two_point_conv_result") == "success" or num(f.get("defensive_two_point_conv")) == 1:
        return "2PT"
    if num(f.get("safety")) == 1:
        return "SAF"
    return "OTRO"


def agregar_pbp(filas: Iterator[dict]) -> ResumenPbp:
    """Resume el jugada a jugada: jugadores, equipos, primer TD, anotaciones y estadísticas por cuarto."""
    jug: dict[tuple[str, str], dict] = defaultdict(lambda: {
        "rz_carries": 0, "i10_carries": 0, "i5_carries": 0, "rz_targets": 0, "i10_targets": 0, "ez_targets": 0,
        "designed_runs": 0, "scrambles": 0, "long_rush": 0.0, "long_rec": 0.0, "long_pass": 0.0,
        "rush_success": 0, "rec_success": 0})
    eq: dict[tuple[str, str], dict] = {}
    rz_drives: dict[tuple[str, str], set] = defaultdict(set)
    rz_td_drives: dict[tuple[str, str], set] = defaultdict(set)
    qb_ids: set[str] = set()
    carreras: dict[tuple[str, str, str], list[float]] = defaultdict(lambda: [0, 0.0])
    proe: dict[tuple[str, str], list[float]] = defaultdict(lambda: [0.0, 0])
    primeros: dict[str, tuple[float, str]] = {}
    marcador: dict[str, tuple[int, int]] = {}
    anotaciones: list[dict] = []
    especiales: dict[tuple[str, str], dict] = defaultdict(lambda: {"drives": set(), "punts": 0, "fga": 0, "fgm": 0})
    cuartos: dict[tuple[str, str, int], dict] = defaultdict(lambda: defaultdict(float))
    for f in filas:
        tipo = f.get("play_type")
        game, pos, de = f.get("game_id"), f.get("posteam"), f.get("defteam")
        if num(f.get("touchdown")) == 1 and f.get("td_player_id") and game:
            orden = num(f.get("play_id")) or 0
            if game not in primeros or orden < primeros[game][0]:
                primeros[game] = (orden, f["td_player_id"])
        if game:
            h, a = _int(f.get("total_home_score")), _int(f.get("total_away_score"))
            if h is not None and a is not None:
                ph, pa = marcador.get(game, (0, 0))
                if (h, a) != (ph, pa) and h >= ph and a >= pa:
                    local = equipos.normalizar(f.get("home_team")) or f.get("home_team")
                    visitante = equipos.normalizar(f.get("away_team")) or f.get("away_team")
                    anotaciones.append({
                        "game_id": game, "play_id": num(f.get("play_id")) or 0, "qtr": _int(f.get("qtr")) or 0,
                        "team": local if h > ph else visitante, "puntos": (h - ph) + (a - pa),
                        "tipo": _tipo_anotacion(f), "home_score": h, "away_score": a,
                        "player_id": f.get("td_player_id") or f.get("kicker_player_id") or None,
                        "distancia": num(f.get("kick_distance")) if f.get("field_goal_result") == "made" else None})
                marcador[game] = (h, a)
            if pos:
                esp = especiales[(game, equipos.normalizar(pos) or pos)]
                drive = f.get("fixed_drive")
                if drive and tipo in ("pass", "run", "punt", "field_goal"):
                    esp["drives"].add(drive)
                if tipo == "punt":
                    esp["punts"] += 1
                if tipo == "field_goal":
                    esp["fga"] += 1
                    esp["fgm"] += int(f.get("field_goal_result") == "made")
        if not game or not pos or not de or tipo not in ("pass", "run"):
            continue
        if num(f.get("two_point_attempt")) == 1 or num(f.get("aborted_play")) == 1:
            continue
        pos, de = equipos.normalizar(pos) or pos, equipos.normalizar(de) or de
        clave = (game, pos)
        e = eq.get(clave)
        if e is None:
            e = eq[clave] = {
                "game_id": game, "team": pos, "opp": de, "season": _int(f.get("season")), "week": _int(f.get("week")),
                "is_home": int(equipos.normalizar(f.get("home_team")) == pos), "points": None, "opp_points": None,
                "plays": 0, "dropbacks": 0, "pass_att": 0, "carries": 0, "designed_runs": 0, "targets": 0,
                "pass_yds": 0.0, "rush_yds": 0.0, "yards": 0.0, "epa": 0.0, "pass_epa": 0.0, "rush_epa": 0.0,
                "success": 0, "explosive_pass": 0, "explosive_rush": 0, "sacks": 0, "turnovers": 0, "rz_trips": 0,
                "rz_tds": 0, "pass_tds": 0, "rush_tds": 0, "third_att": 0, "third_conv": 0, "proe": None,
                "qb_rush_yds": 0.0, "qb_rush_att": 0}
        yds = num(f.get("yards_gained")) or 0.0
        epa = num(f.get("epa")) or 0.0
        yl = num(f.get("yardline_100"))
        drive = f.get("fixed_drive") or f.get("drive")
        scramble = num(f.get("qb_scramble")) == 1
        e["plays"] += 1
        e["yards"] += yds
        e["epa"] += epa
        e["success"] += int(num(f.get("success")) == 1)
        if num(f.get("down")) == 3:
            e["third_att"] += 1
            e["third_conv"] += int(num(f.get("third_down_converted")) == 1)
        if num(f.get("interception")) == 1 or num(f.get("fumble_lost")) == 1:
            e["turnovers"] += 1
        if yl is not None and yl <= 20 and drive:
            rz_drives[clave].add(drive)
            if f.get("fixed_drive_result") == "Touchdown":
                rz_td_drives[clave].add(drive)
        oe = num(f.get("pass_oe"))
        if oe is not None:
            proe[clave][0] += oe
            proe[clave][1] += 1
        td_propio = num(f.get("touchdown")) == 1 and equipos.normalizar(f.get("td_team")) == pos
        if tipo == "pass" and not scramble:
            e["dropbacks"] += 1
            e["pass_epa"] += epa
            if num(f.get("sack")) == 1:
                e["sacks"] += 1
            if num(f.get("pass_attempt")) == 1 and num(f.get("sack")) != 1:
                e["pass_att"] += 1
            if num(f.get("complete_pass")) == 1:
                e["pass_yds"] += yds
                if yds >= 20:
                    e["explosive_pass"] += 1
            if td_propio and num(f.get("pass_touchdown")) == 1:
                e["pass_tds"] += 1
            passer, rec = f.get("passer_player_id"), f.get("receiver_player_id")
            q = _int(f.get("qtr")) or 0
            completo = num(f.get("complete_pass")) == 1
            td_pase = int(td_propio and num(f.get("pass_touchdown")) == 1)
            if passer:
                c = cuartos[(game, passer, q)]
                if num(f.get("pass_attempt")) == 1 and num(f.get("sack")) != 1:
                    c["attempts"] += 1
                c["completions"] += int(completo)
                c["passing_yards"] += yds if completo else 0
                c["passing_tds"] += td_pase
                c["passing_interceptions"] += int(num(f.get("interception")) == 1)
            if rec:
                c = cuartos[(game, rec, q)]
                c["targets"] += 1
                c["receptions"] += int(completo)
                c["receiving_yards"] += yds if completo else 0
                c["receiving_tds"] += td_pase
            if passer:
                qb_ids.add(passer)
                if num(f.get("complete_pass")) == 1:
                    j = jug[(game, passer)]
                    j["long_pass"] = max(j["long_pass"], yds)
            if rec:
                e["targets"] += 1
                j = jug[(game, rec)]
                if yl is not None:
                    j["rz_targets"] += int(yl <= 20)
                    j["i10_targets"] += int(yl <= 10)
                    air = num(f.get("air_yards"))
                    j["ez_targets"] += int(air is not None and air >= yl)
                if num(f.get("complete_pass")) == 1:
                    j["long_rec"] = max(j["long_rec"], yds)
                j["rec_success"] += int(num(f.get("success")) == 1)
        else:
            # Carrera diseñada o scramble del QB (que cuenta como carrera en las estadísticas).
            e["carries"] += 1
            e["rush_yds"] += yds
            e["rush_epa"] += epa
            e["designed_runs"] += int(not scramble)
            if yds >= 10:
                e["explosive_rush"] += 1
            if td_propio and num(f.get("rush_touchdown")) == 1:
                e["rush_tds"] += 1
            rusher = f.get("rusher_player_id")
            if rusher:
                c = cuartos[(game, rusher, _int(f.get("qtr")) or 0)]
                c["carries"] += 1
                c["rushing_yards"] += yds
                c["rushing_tds"] += int(td_propio and num(f.get("rush_touchdown")) == 1)
                j = jug[(game, rusher)]
                if yl is not None:
                    j["rz_carries"] += int(yl <= 20)
                    j["i10_carries"] += int(yl <= 10)
                    j["i5_carries"] += int(yl <= 5)
                j["designed_runs"] += int(not scramble)
                j["scrambles"] += int(scramble)
                j["long_rush"] = max(j["long_rush"], yds)
                j["rush_success"] += int(num(f.get("success")) == 1)
                c = carreras[(game, pos, rusher)]
                c[0] += 1
                c[1] += yds
                if scramble:
                    qb_ids.add(rusher)
    # Carreras de QB (diseñadas y scrambles) por equipo: los QB son quienes lanzaron algún pase.
    for (game, team, pid), (att, yds) in carreras.items():
        if pid in qb_ids:
            eq[(game, team)]["qb_rush_att"] += att
            eq[(game, team)]["qb_rush_yds"] += yds
    jugadores = [{"game_id": g, "player_id": p, **v} for (g, p), v in jug.items()]
    for clave, e in eq.items():
        esp = especiales.get(clave)
        e["drives"] = len(esp["drives"]) if esp else None
        e["punts"] = esp["punts"] if esp else 0
        e["fga"] = esp["fga"] if esp else 0
        e["fgm"] = esp["fgm"] if esp else 0
        e["rz_trips"] = len(rz_drives[clave])
        e["rz_tds"] = len(rz_td_drives[clave])
        suma, n_oe = proe[clave]
        e["proe"] = round(suma / n_oe, 4) if n_oe else None
    filas_cuartos = [{"game_id": g, "player_id": p, "qtr": q, **v} for (g, p, q), v in cuartos.items() if q]
    return ResumenPbp(jugadores, list(eq.values()), {g: pid for g, (_, pid) in primeros.items()}, anotaciones,
                      filas_cuartos)


# --- Plantillas, snaps y lesiones ----------------------------------------------------------

def parse_roster_semanal(filas: Iterator[dict]) -> list[dict]:
    """Última entrada de cada jugador en la temporada (equipo y estado de esa semana)."""
    ultimo: dict[str, dict] = {}
    for f in filas:
        pid = f.get("gsis_id")
        if not pid:
            continue
        fila = {"player_id": pid, "name": f.get("full_name"), "position": f.get("position") or None,
                "team": equipos.normalizar(f.get("team")) or f.get("team"), "status": f.get("status"),
                "season": _int(f.get("season")), "week": _int(f.get("week")) or 0,
                "espn_id": (f.get("espn_id") or "").split(".")[0] or None, "pfr_id": f.get("pfr_id") or None,
                "depth_position": f.get("depth_chart_position") or None, "years_exp": _int(f.get("years_exp"))}
        prev = ultimo.get(pid)
        if prev is None or fila["week"] >= prev["week"]:
            ultimo[pid] = fila
    return list(ultimo.values())


def cambios_semanales(filas: Iterator[dict]) -> list[dict]:
    """Cambios de equipo dentro de la temporada según las plantillas semana a semana."""
    por_jugador: dict[str, list[tuple[int, str, str]]] = defaultdict(list)
    for f in filas:
        pid, team = f.get("gsis_id"), equipos.normalizar(f.get("team"))
        if pid and team and f.get("status") not in ("CUT",):
            por_jugador[pid].append((_int(f.get("week")) or 0, team, f.get("full_name")))
    out = []
    for pid, semanas in por_jugador.items():
        semanas.sort()
        for (w0, t0, _), (w1, t1, nombre) in zip(semanas, semanas[1:]):
            if t0 != t1:
                out.append({"player_id": pid, "name": nombre, "week": w1, "from_team": t0, "to_team": t1})
    return out


def parse_snaps(filas: Iterator[dict], pfr_a_gsis: dict[str, str]) -> list[dict]:
    out = []
    for f in filas:
        pid = pfr_a_gsis.get(f.get("pfr_player_id") or "")
        if not pid or not f.get("game_id"):
            continue
        out.append({"game_id": f["game_id"], "player_id": pid, "offense_snaps": _int(f.get("offense_snaps")),
                    "offense_pct": num(f.get("offense_pct"))})
    return out


def parse_lesiones_nflverse(filas: Iterator[dict]) -> list[dict]:
    """Parte oficial: se queda con la semana más reciente de cada jugador."""
    ultimo: dict[str, dict] = {}
    for f in filas:
        pid = f.get("gsis_id")
        if not pid:
            continue
        semana = _int(f.get("week")) or 0
        fila = {"player_id": pid, "name": f.get("full_name"), "team": equipos.normalizar(f.get("team")),
                "position": f.get("position"), "status": f.get("report_status") or f.get("practice_status") or "",
                "detail": f.get("report_primary_injury") or f.get("practice_primary_injury"),
                "comment": f.get("practice_status"), "season": _int(f.get("season")), "week": semana}
        if pid not in ultimo or semana >= ultimo[pid]["week"]:
            ultimo[pid] = fila
    return list(ultimo.values())


def parse_lesiones_espn(data: dict) -> list[dict]:
    out = []
    for t in data.get("injuries", []):
        team = equipos.por_nombre_largo(t.get("displayName", ""))
        for i in t.get("injuries", []):
            ath = i.get("athlete") or {}
            espn_id = None
            for link in ath.get("links", []):
                m = re.search(r"/id/(\d+)", link.get("href", ""))
                if m:
                    espn_id = m.group(1)
                    break
            if not espn_id:
                continue
            out.append({"espn_id": espn_id, "name": ath.get("displayName"), "team": team,
                        "position": (ath.get("position") or {}).get("abbreviation"), "status": i.get("status") or "",
                        "detail": ((i.get("details") or {}).get("type") or ""), "comment": i.get("shortComment"),
                        "fecha": (i.get("date") or "")[:10]})
    return out


_TRASPASO = re.compile(
    r"Traded (?:(?:QB|RB|FB|WR|TE|DB|CB|S|LB|DE|DT|OT|G|C|K|P|LS|OL|DL|EDGE) )?"
    r"([A-Z][A-Za-z.'\-]+(?: [A-Z][A-Za-z.'\-]+)*?(?: Jr\.| Sr\.| II| III| IV)?)"
    r"(?: and [^.]*?)? to (?:the )?([A-Z][A-Za-z.]+(?: [A-Z0-9][A-Za-z0-9.]+)*)")


def parse_transacciones(data: dict) -> list[dict]:
    out = []
    for t in data.get("transactions", []):
        team = equipos.normalizar((t.get("team") or {}).get("abbreviation"))
        if team and t.get("description"):
            out.append({"fecha": (t.get("date") or "")[:10], "team": team, "description": t["description"]})
    return out


def traspasos_en_texto(transacciones: list[dict]) -> list[dict]:
    """'Traded WR Marvin Harrison Jr. and a 2027 pick to Houston for ...' -> jugador y equipo de destino."""
    out = []
    for t in transacciones:
        for m in _TRASPASO.finditer(t["description"]):
            nombre, destino = m.group(1), m.group(2)
            if re.match(r"(a|an|the)\b", nombre, re.I) or re.search(r"\d", nombre):
                continue  # se traspasó una elección del draft
            to_team = None
            palabras = destino.split()
            for n in range(len(palabras), 0, -1):
                to_team = equipos.por_texto(" ".join(palabras[:n]))
                if to_team:
                    break
            if to_team and to_team != t["team"]:
                out.append({"fecha": t["fecha"], "name": nombre, "from_team": t["team"], "to_team": to_team})
    return out
