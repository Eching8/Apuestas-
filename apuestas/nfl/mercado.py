"""El mercado: líneas y cuotas de cada casa (SportsGameOdds), mejor precio disponible y cómo se ha movido.

SportsGameOdds da, para cada apuesta, la línea de consenso, la de apertura (`openBookOverUnder`/`openBookOdds`),
una cuota justa sin margen (`fairOdds`) y la línea y cuota de cada casa (`byBookmaker`). Con eso:

- **Mejor línea**: la casa que paga más por el lado que nos interesa (o la línea más baja para un "más").
- **Movimiento**: de la apertura a ahora. Si la cuota del "sí" baja (o la línea sube) es que entra dinero en ese
  lado: es lo que el público o los apostadores profesionales están jugando.
- **Probabilidad de la casa**: la cuota justa de consenso (sin margen); si no está, se quita el margen a mano.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone

import requests

from ..api_football import ApiError
from ..nba.sgo import BASE_URL, americana_a_decimal, clave_nombre
from . import equipos

log = logging.getLogger(__name__)

STATS_SGO = {
    "passing_yards": "pass_yds", "passing_touchdowns": "pass_tds", "passing_attempts": "pass_att",
    "passing_completions": "comp", "passing_interceptions": "ints", "rushing_yards": "rush_yds",
    "rushing_attempts": "rush_att", "receiving_receptions": "rec", "receiving_yards": "rec_yds",
    "receiving_targets": "targets", "rushing+receiving_yards": "rush_rec_yds",
    "passing+rushing_yards": "pass_rush_yds", "touchdowns": "tds", "rushing_touchdowns": "rush_tds",
    "receiving_touchdowns": "rec_tds", "receiving_longestReception": "long_rec",
    "rushing_longestRush": "long_rush", "firstTouchdown": "first_td", "lastTouchdown": "last_td",
    "passing_longestCompletion": "long_pass", "rushing_yardsPerAttempt": "ypc", "fantasyScore": "fantasy",
    # Defensa y equipos especiales.
    "defense_sacks": "sacks", "defense_combinedTackles": "tackles", "defense_soloTackles": "solo",
    "defense_assistedTackles": "asist", "defense_interceptions": "def_ints", "fieldGoals_made": "fg",
    "extraPoints_kicksMade": "xp", "kicking_totalPoints": "kick_pts", "punting_numPunts": "punts",
}
# Mercados de partido y de equipo (statEntityID 'home', 'away' o 'all').
STATS_EQUIPO = {
    "points": "pts", "touchdowns": "tds", "fieldGoals_made": "fg", "fieldGoals_longestMade": "fg_largo",
    "firstToScore": "primero", "lastToScore": "ultimo", "bothTeamsScored": "ambos", "largestLead": "ventaja",
    "turnovers": "perdidas", "punting_numPunts": "punts", "defense_safeties": "safety", "defense_sacks": "sacks",
}
# Mercados de jugador sí/no que equivalen a "más de 0.5".
YN_JUGADOR = ("tds", "first_td", "last_td", "pass_tds", "rush_tds", "rec_tds", "ints", "rec", "sacks",
              "def_ints", "fg", "xp")
LADOS = {"over": "más", "under": "menos", "yes": "sí", "no": "no", "home": "home", "away": "away",
         "draw": "draw", "even": "par", "odd": "impar"}
MARGEN_UN_LADO = 1.07      # margen típico de un mercado de un solo lado (anotar sí/no, primer TD)
MARGEN_ALTERNATIVA = 1.045  # línea alternativa de over/under de una casa (sin el otro lado para quitarlo exacto)
MARGEN_MULTIPLES = 1.12     # 2+ TD y primer TD: las casas cobran más en los mercados de premio grande


class SportsGameOddsNfl:
    def __init__(self, api_key: str = "", session: requests.Session | None = None, base_url: str = BASE_URL):
        self.base_url = base_url
        self.session = session or requests.Session()
        if api_key:
            self.session.headers["X-Api-Key"] = api_key
        self.peticiones = 0

    def eventos(self, inicio: datetime, fin: datetime) -> list[dict]:
        out, cursor = [], None
        while True:
            params = {"leagueID": "NFL", "oddsAvailable": "true", "limit": 25,
                      "startsAfter": inicio.isoformat(), "startsBefore": fin.isoformat()}
            if cursor:
                params["cursor"] = cursor
            resp = self.session.get(f"{self.base_url}/events", params=params, timeout=60)
            self.peticiones += 1
            if resp.status_code == 401:
                raise ApiError("SportsGameOdds rechazó la clave: revisa SPORTSGAMEODDS_KEY en el .env")
            if resp.status_code != 200:
                raise ApiError(f"SportsGameOdds /events: HTTP {resp.status_code} {resp.text[:200]}")
            data = resp.json()
            out += data.get("data", [])
            cursor = data.get("nextCursor")
            if not cursor or not data.get("data"):
                return out


def ventana(desde: str, dias: int) -> tuple[datetime, datetime]:
    ini = datetime.fromisoformat(desde).replace(tzinfo=timezone.utc)
    return ini, ini + timedelta(days=dias, hours=12)


@dataclass
class Oferta:
    """Una apuesta concreta (jugador, estadística, lado, línea) con el precio de cada casa."""
    sgo_player_id: str         # id del jugador en SGO, o 'home' / 'away' / 'all' en mercados de equipo
    nombre: str
    sgo_team: str | None
    stat: str
    lado: str                  # 'más'/'menos'; equipo: 'home'/'away'/'draw', 'sí'/'no', 'par'/'impar'
    line: float                # línea (spread en 'sp'; 0 en moneyline, sí/no y par/impar)
    tipo: str = "jugador"      # 'jugador' o 'equipo'
    periodo: str = "game"      # 'game', '1h', '2h', '1q'...'4q'
    bet: str = "ou"            # ou, yn, ml, sp, ml3way, eo
    libros: dict[str, float] = field(default_factory=dict)   # casa -> cuota decimal
    consenso: float | None = None
    justa: float | None = None                                # cuota justa de consenso (sin margen)
    open_line: float | None = None
    open_odd: float | None = None
    contraria: float | None = None                            # cuota de consenso del otro lado
    player_id: str | None = None                              # id de nflverse tras emparejar

    @property
    def codigo(self) -> str:
        """Estadística con periodo y tipo de apuesta cuando no es la prop normal del partido: 'rec_yds@1q',
        'pts@1h/sp'."""
        if self.tipo == "jugador":
            return self.stat if self.periodo == "game" else f"{self.stat}@{self.periodo}"
        return f"{self.stat}@{self.periodo}/{self.bet}"

    @property
    def mejor(self) -> tuple[str | None, float | None]:
        if not self.libros:
            return None, self.consenso
        book = max(self.libros, key=self.libros.get)
        return book, self.libros[book]

    def prob_casa(self) -> float | None:
        if self.justa:
            return 1 / self.justa
        if self.consenso and self.contraria:
            a, b = 1 / self.consenso, 1 / self.contraria
            return a / (a + b)
        if self.consenso:
            return 1 / self.consenso / MARGEN_UN_LADO
        if self.libros:
            # Línea alternativa sin consenso: mediana de las casas que la ofrecen, con su margen típico.
            odds = sorted(self.libros.values())
            mediana = odds[len(odds) // 2]
            margen = MARGEN_MULTIPLES if self.stat in ("tds", "first_td", "last_td") or self.bet == "ml3way" \
                else MARGEN_ALTERNATIVA
            return 1 / mediana / margen
        return None

    def movimiento(self) -> str | None:
        """Texto con lo que se movió desde la apertura (o None si nada relevante)."""
        partes = []
        if self.open_line is not None and abs(self.open_line - self.line) >= 0.5 and self.stat != "tds":
            partes.append(f"la línea pasó de {self.open_line:g} a {self.line:g}")
        if self.open_odd and self.consenso and abs(1 / self.consenso - 1 / self.open_odd) >= 0.03:
            partes.append(f"la cuota de consenso pasó de {self.open_odd:.2f} a {self.consenso:.2f}")
        return " y ".join(partes) or None

    def presion(self) -> float:
        """> 0 si el mercado empujó este lado desde la apertura (más probabilidad implícita), < 0 si el contrario."""
        p = 0.0
        if self.open_odd and self.consenso:
            p += 1 / self.consenso - 1 / self.open_odd
        if self.open_line is not None and self.stat != "tds":
            d = self.line - self.open_line
            p += (0.02 if self.lado == "más" else -0.02) * d / max(1.0, 0.1 * abs(self.line))
        return p


@dataclass
class Mercado:
    event_id: str
    home: str | None
    away: str | None
    inicio: str | None
    total: float | None = None
    spread_home: float | None = None          # ventaja esperada del local (positivo = favorito)
    team_total: dict[str, float] = field(default_factory=dict)
    ofertas: list[Oferta] = field(default_factory=list)
    jugadores: dict[str, dict] = field(default_factory=dict)
    movimientos: list[str] = field(default_factory=list)


def _f(v) -> float | None:
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def parse_evento(evento: dict) -> Mercado:
    """Todas las apuestas del evento: props de jugador (partido y periodos) y mercados de partido y equipo."""
    teams = evento.get("teams", {})
    home = equipos.por_nombre_largo((teams.get("home", {}).get("names") or {}).get("long", ""))
    away = equipos.por_nombre_largo((teams.get("away", {}).get("names") or {}).get("long", ""))
    m = Mercado(evento.get("eventID", ""), home, away, (evento.get("status") or {}).get("startsAt"),
                jugadores=evento.get("players", {}))
    odds = evento.get("odds", {})
    nombres_equipo = {"home": equipos.nombre(home) if home else "Local",
                      "away": equipos.nombre(away) if away else "Visitante", "all": "Partido"}
    for o in odds.values():
        if o.get("cancelled") or not o.get("bookOddsAvailable"):
            continue
        stat_id, bet, side, ent = o.get("statID"), o.get("betTypeID"), o.get("sideID"), o.get("statEntityID")
        periodo = o.get("periodID") or "game"
        if not o.get("playerID") and stat_id == "points" and periodo == "game":
            _lineas_partido(m, o, home)
        lado = LADOS.get(side)
        if lado is None or bet not in ("ou", "yn", "ml", "sp", "ml3way", "eo"):
            continue
        if o.get("playerID"):
            stat = STATS_SGO.get(stat_id)
            if not stat or bet not in ("ou", "yn"):
                continue
            tipo, entidad = "jugador", o["playerID"]
            info = m.jugadores.get(entidad, {})
            nombre, sgo_team = info.get("name") or entidad, info.get("teamID")
            if bet == "yn":
                if stat not in YN_JUGADOR:
                    continue
                lado, linea = ("más" if lado == "sí" else "menos"), 0.5
            else:
                linea = _f(o.get("bookOverUnder"))
        else:
            stat = STATS_EQUIPO.get(stat_id)
            if not stat or ent not in ("home", "away", "all"):
                continue
            tipo, entidad, nombre, sgo_team = "equipo", ent, nombres_equipo[ent], None
            linea = _f(o.get("bookSpread")) if bet == "sp" else _f(o.get("bookOverUnder")) if bet == "ou" else 0.0
        if linea is None:
            continue
        campo_linea = {"sp": "Spread", "ou": "OverUnder"}.get(bet)
        contraria = odds.get(o.get("opposingOddID") or "", {})
        # La cuota justa y la de apertura pueden ser de otra línea: solo valen si coinciden con esta.
        # En over/under la línea tiene que venir confirmada: sin ella, SGO puede estar dando la justa de otra línea
        # (p. ej. la de "anota", 0.5, en la oferta de 2+ TD, 1.5).
        misma = (lambda pref: campo_linea is None or _f(o.get(f"{pref}{campo_linea}")) == linea
                 or (_f(o.get(f"{pref}{campo_linea}")) is None and bet == "sp"))
        base = Oferta(entidad, nombre, sgo_team, stat, lado, linea, tipo=tipo, periodo=periodo, bet=bet,
                      consenso=americana_a_decimal(o.get("bookOdds")),
                      justa=americana_a_decimal(o.get("fairOdds")) if misma("fair") else None,
                      open_line=_f(o.get(f"openBook{campo_linea}")) if campo_linea else None,
                      open_odd=americana_a_decimal(o.get("openBookOdds")) if misma("openBook") else None,
                      contraria=americana_a_decimal(contraria.get("bookOdds"))
                      if campo_linea is None or _f(contraria.get(f"book{campo_linea}")) in
                      (None, -linea if bet == "sp" else linea) else None)
        if bet == "ml3way":
            base.contraria = None     # tres resultados: el "otro lado" no es uno solo
        por_linea: dict[float, Oferta] = {linea: base}
        libros = o.get("byBookmaker") or {}
        disponibles = {k: v for k, v in libros.items() if v.get("available")} or libros
        for book, b in disponibles.items():
            odd = americana_a_decimal(b.get("odds"))
            if not odd:
                continue
            bl = _f(b.get("spread")) if bet == "sp" else _f(b.get("overUnder")) if bet == "ou" else linea
            bl = linea if bl is None else bl
            if bl not in por_linea:
                # Línea alternativa de esa casa (p. ej. 2+ TD = más de 1.5): sin consenso ni apertura.
                por_linea[bl] = Oferta(entidad, nombre, sgo_team, stat, lado, bl, tipo=tipo, periodo=periodo,
                                       bet=bet)
            por_linea[bl].libros[book] = odd
        for of in por_linea.values():
            # Sin ninguna casa detrás es un relleno de SportsGameOdds (+100/+100): no se puede apostar.
            if of.libros:
                m.ofertas.append(of)
    # Las ofertas de 'yn' y 'ou' de la misma apuesta (anotar = más de 0.5) se juntan.
    juntas: dict[tuple, Oferta] = {}
    for of in m.ofertas:
        k = (of.tipo, of.sgo_player_id, of.stat, of.periodo, of.bet if of.tipo == "equipo" else "", of.lado, of.line)
        if k in juntas:
            prev = juntas[k]
            for book, odd in of.libros.items():
                prev.libros[book] = max(odd, prev.libros.get(book, 0))
            for attr in ("consenso", "justa", "open_line", "open_odd", "contraria"):
                if getattr(prev, attr) is None:
                    setattr(prev, attr, getattr(of, attr))
        else:
            juntas[k] = of
    m.ofertas = list(juntas.values())
    return m


def _lineas_partido(m: Mercado, o: dict, home: str | None) -> None:
    """Total, spread y totales por equipo del partido completo (entorno de las props y movimiento)."""
    bet, side, ent = o.get("betTypeID"), o.get("sideID"), o.get("statEntityID")
    # La línea "justa" de SGO es la central; la de consenso a veces es una alternativa (30.5 a +235).
    if bet == "ou" and ent == "all" and side == "over":
        m.total = _f(o.get("fairOverUnder")) or _f(o.get("bookOverUnder"))
        ab, cd = _f(o.get("openBookOverUnder")), m.total
        if ab is not None and cd is not None and abs(ab - cd) >= 1:
            m.movimientos.append(f"total del partido: de {ab:g} a {cd:g}")
    elif bet == "sp" and ent == "home" and side == "home":
        sp = _f(o.get("bookSpread"))
        if sp is not None:
            m.spread_home = -sp
            op = _f(o.get("openBookSpread"))
            if op is not None and abs(op - sp) >= 1:
                m.movimientos.append(f"spread de {home}: de {op:+g} a {sp:+g}")
    elif bet == "ou" and ent in ("home", "away") and side == "over":
        t = m.home if ent == "home" else m.away
        v = _f(o.get("fairOverUnder")) or _f(o.get("bookOverUnder"))
        if t and v is not None:
            m.team_total[t] = v


def emparejar(m: Mercado, roster: list[dict]) -> int:
    """Asigna el id de nflverse a cada oferta por nombre y equipo. Devuelve cuántas quedaron emparejadas."""
    por_nombre: dict[str, list[dict]] = {}
    for r in roster:
        por_nombre.setdefault(clave_nombre(r["name"] or ""), []).append(r)
    equipos_partido = {m.home, m.away}
    n = 0
    for of in m.ofertas:
        if of.tipo != "jugador":
            continue
        team = equipos.por_nombre_largo(of.sgo_team or "")
        k = clave_nombre(of.nombre)
        cands = [r for r in por_nombre.get(k, []) if r["team"] in equipos_partido]
        if not cands:
            # Sin sufijos (Jr, II...) o con el nombre corto de SGO.
            k2 = clave_nombre(of.nombre.replace(" Jr.", "").replace(" Sr.", "").replace(" II", "").replace(" III", ""))
            cands = [r for kk, rs in por_nombre.items() if kk.startswith(k2) for r in rs if r["team"] in equipos_partido]
        if team:
            cands = [r for r in cands if r["team"] == team] or cands
        if len(cands) == 1:
            of.player_id = cands[0]["player_id"]
            n += 1
    return n


def filas_lineas(m: Mercado, game_id: str | None, capturado: str) -> list[dict]:
    """Filas para nfl_lineas: el consenso y cada casa de cada oferta, más el total y spread del partido."""
    filas = []
    for of in m.ofertas:
        comun = {"captured_at": capturado, "event_id": m.event_id, "game_id": game_id, "player_id": of.player_id,
                 "sgo_player_id": of.sgo_player_id, "entidad": of.sgo_player_id, "stat": of.codigo, "lado": of.lado,
                 "line": of.line}
        if of.consenso:
            filas.append({**comun, "book": "consenso", "odd": of.consenso, "open_line": of.open_line,
                          "open_odd": of.open_odd})
        for book, odd in of.libros.items():
            filas.append({**comun, "book": book, "odd": odd})
    for nombre, v in (("total", m.total), ("spread_home", m.spread_home)):
        if v is not None:
            filas.append({"captured_at": capturado, "event_id": m.event_id, "game_id": game_id, "entidad": "all",
                          "stat": nombre, "lado": "-", "book": "consenso", "line": v})
    return filas
