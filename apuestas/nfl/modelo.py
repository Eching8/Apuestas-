"""Modelo de props de la NFL: volumen × eficiencia × rival, y touchdowns por cuota de oportunidades.

Para cada partido:

1. **Entorno del equipo.** Puntos esperados (los de la casa si hay línea: total y spread; si no, ataque propio ×
   lo que concede el rival), jugadas de pase y carrera (ritmo propio, rival y guion: el favorito corre más al
   final) y touchdowns de ataque (puntos × TD por punto del equipo), repartidos entre pase y carrera según lo que
   hace el equipo y lo que concede el rival.
2. **Reparto dentro del equipo.** Cuota de acarreos, envíos y pases de cada jugador, y sus cuotas en zona roja,
   dentro de la 10 y la 5 y de envíos a la zona de anotación. Los que están fuera (lesión, suspensión, reserva)
   no juegan: su parte se reparte entre los que sí. Tras un traspaso solo cuentan los partidos con el equipo nuevo.
3. **Eficiencia del jugador** (yardas por acarreo, por envío, por pase, % de recepción) con contracción hacia la
   media de su posición, ajustada por lo que el rival concede **a esa posición**.
4. **Touchdowns**: TD de carrera del equipo × su cuota de oportunidades cerca de la zona de anotación (dentro de
   la 10 pesa más que la cuota general), lo mismo en recepción, y un ajuste por lo que el rival concede a su
   posición. P(1+ TD) y P(2+ TD) salen de una binomial negativa sobre ese número esperado.

Las yardas y conteos usan binomial negativa con la dispersión del propio jugador contraída hacia la típica de la
estadística. Cada ajuste queda registrado como un Factor con su efecto: de ahí sale el "¿por qué?".
"""
from __future__ import annotations

import math
from collections import defaultdict
from dataclasses import dataclass, field

from ..model import negbin_pmf
from .db import ROSTER_FUERA, estado_duda, estado_fuera

POSICIONES = ("QB", "RB", "WR", "TE")
NOMBRES = {
    "pass_yds": "yardas de pase", "pass_tds": "TD de pase", "pass_att": "pases intentados",
    "comp": "pases completos", "ints": "intercepciones", "rush_yds": "yardas por tierra", "rush_att": "acarreos",
    "rec": "recepciones", "rec_yds": "yardas por recepción", "targets": "envíos (targets)",
    "rush_rec_yds": "yardas de carrera + recepción", "pass_rush_yds": "yardas de pase + carrera",
    "tds": "touchdowns", "rush_tds": "TD por tierra", "rec_tds": "TD por recepción",
    "long_rec": "recepción más larga", "long_rush": "carrera más larga", "first_td": "primer TD del partido",
    "last_td": "último TD del partido", "long_pass": "pase completo más largo", "ypc": "yardas por acarreo",
    "fantasy": "puntos de fantasy", "sacks": "sacks", "tackles": "tacleadas (solo + asistidas)",
    "solo": "tacleadas en solitario", "asist": "tacleadas asistidas", "def_ints": "intercepciones (defensor)",
    "fg": "goles de campo", "xp": "puntos extra", "kick_pts": "puntos del pateador",
}
STATS_CONTEO = ("pass_tds", "ints", "tds", "rush_tds", "rec_tds", "sacks", "def_ints")
# Fantasy (puntuación de PrizePicks/Underdog, la de las líneas de las casas): yardas de pase /25, TD de pase 4,
# intercepción -1, yardas de carrera y recepción /10, recepción 1, TD 6, balón perdido -1.
FANTASY = {"passing_yards": 0.04, "passing_tds": 4, "passing_interceptions": -1, "rushing_yards": 0.1,
           "receiving_yards": 0.1, "receptions": 1, "rushing_tds": 6, "receiving_tds": 6, "special_teams_tds": 6,
           "rushing_fumbles_lost": -1, "receiving_fumbles_lost": -1}
# Dispersión típica (coeficiente de variación) de cada estadística entre partidos.
CV_DEFECTO = {"pass_yds": 0.30, "pass_att": 0.20, "comp": 0.23, "rush_yds": 0.55, "rush_att": 0.35, "rec": 0.50,
              "rec_yds": 0.65, "targets": 0.42, "rush_rec_yds": 0.45, "pass_rush_yds": 0.28, "long_rec": 0.60,
              "long_rush": 0.65, "long_pass": 0.35, "fantasy": 0.45, "tackles": 0.45, "solo": 0.5, "asist": 0.7}
STATS_POR_POSICION = {
    "QB": ("pass_yds", "pass_tds", "pass_att", "comp", "ints", "rush_yds", "rush_att", "pass_rush_yds", "tds"),
    "RB": ("rush_yds", "rush_att", "rec", "rec_yds", "rush_rec_yds", "tds", "long_rush", "targets"),
    "WR": ("rec", "rec_yds", "targets", "long_rec", "tds", "rush_rec_yds"),
    "TE": ("rec", "rec_yds", "targets", "long_rec", "tds"),
}

DECAY_JUGADOR = 0.85       # peso del partido i-ésimo más reciente: DECAY**i
DECAY_EQUIPO = 0.88
PESO_TEMPORADA = {0: 1.0, 1: 0.35, 2: 0.12}   # temporada actual, anterior y la de antes
K_EQUIPO = 3.0             # partidos "virtuales" de media de liga en cada perfil de equipo
VENTAJA_LOCAL = 1.5        # puntos
GUION_PASE = 0.008         # -0.8 % de pases por cada punto de favorito
GUION_CARRERA = 0.012      # +1.2 % de carreras por cada punto de favorito
VIENTO_FUERTE = 15.0       # mph
EFECTO_VIENTO = 0.93
# Calibración medida con el backtest de 2025 (semanas 5-18): las probabilidades de yardas y conteos se
# acercan a 50 % (logit × 0.75) y los TD esperados se comprimen hacia 0.3 (exponente 0.85).
CALIBRACION_LOGIT = 0.75
TD_REF, TD_EXP = 0.3, 0.85
FUGA_REPARTO = 0.03        # parte del volumen que se llevan jugadores marginales que no se proyectan
DUDA = 0.92                # recorte del volumen esperado de un jugador "questionable"
# QB suplente, medido en 33 equipos-temporada de 2024-2026 (cada equipo comparado consigo mismo): TD de pase -28 %,
# TD de carrera -7 %, puntos -13 %, visitas a la zona roja -15 %, y el RB1 recibe más balones cerca de la meta (+9 %
# de los acarreos dentro de la 10 en 22 de 33 equipos). Pero en el backtest de 2025 ajustar las probabilidades con eso
# no mejora (Brier de TD 0.1502 frente a 0.1500 sin ajustar): la línea de la casa ya descuenta al suplente y el
# equipo llega menos a la zona roja. Por eso se usa como razonamiento (con sus datos), no como multiplicador.


# --- Distribución ---------------------------------------------------------------------

def cdf(k: int, mu: float, var: float) -> float:
    if k < 0:
        return 0.0
    return min(1.0, sum(negbin_pmf(i, mu, var) for i in range(k + 1)))


def prob_lados(line: float, mu: float, var: float) -> tuple[float, float]:
    """P(más de la línea), P(menos de la línea). Con línea entera el empate (push) no cuenta."""
    if mu <= 0:
        return 0.0, 1.0
    over = 1.0 - cdf(math.floor(line), mu, var)
    under = cdf(math.ceil(line) - 1, mu, var)
    return max(0.0, min(1.0, over)), max(0.0, min(1.0, under))


def linea_justa(mu: float, var: float) -> float:
    """Línea .5 con las probabilidades de más y menos más parecidas."""
    mejor, dif = 0.5, 2.0
    for k in range(0, int(mu * 2.5 + 15)):
        o, u = prob_lados(k + 0.5, mu, var)
        if abs(o - u) < dif:
            mejor, dif = k + 0.5, abs(o - u)
    return mejor


def cuota_justa(p: float) -> float | None:
    return round(1 / p, 2) if p > 0.001 else None


def americana(decimal: float | None) -> str:
    if not decimal or decimal <= 1:
        return "-"
    return f"+{(decimal - 1) * 100:.0f}" if decimal >= 2 else f"-{100 / (decimal - 1):.0f}"


# --- Valores por partido ------------------------------------------------------------------

def _v(p: dict, c: str) -> float:
    return p.get(c) or 0.0


def valor(p: dict, stat: str) -> float:
    if stat == "pass_yds":
        return _v(p, "passing_yards")
    if stat == "pass_tds":
        return _v(p, "passing_tds")
    if stat == "pass_att":
        return _v(p, "attempts")
    if stat == "comp":
        return _v(p, "completions")
    if stat == "ints":
        return _v(p, "passing_interceptions")
    if stat == "rush_yds":
        return _v(p, "rushing_yards")
    if stat == "rush_att":
        return _v(p, "carries")
    if stat == "rec":
        return _v(p, "receptions")
    if stat == "rec_yds":
        return _v(p, "receiving_yards")
    if stat == "targets":
        return _v(p, "targets")
    if stat == "rush_rec_yds":
        return _v(p, "rushing_yards") + _v(p, "receiving_yards")
    if stat == "pass_rush_yds":
        return _v(p, "passing_yards") + _v(p, "rushing_yards")
    if stat == "tds":
        return _v(p, "rushing_tds") + _v(p, "receiving_tds") + _v(p, "special_teams_tds")
    if stat == "rush_tds":
        return _v(p, "rushing_tds")
    if stat == "rec_tds":
        return _v(p, "receiving_tds")
    if stat == "long_rec":
        return _v(p, "long_rec")
    if stat == "long_rush":
        return _v(p, "long_rush")
    if stat == "long_pass":
        return _v(p, "long_pass")
    if stat == "ypc":
        return _v(p, "rushing_yards") / _v(p, "carries") if _v(p, "carries") else 0.0
    if stat == "fantasy":
        return sum(peso * _v(p, col) for col, peso in FANTASY.items())
    if stat == "sacks":
        return _v(p, "def_sacks")
    if stat == "tackles":
        return _v(p, "def_tackles_solo") + _v(p, "def_tackle_assists")
    if stat == "solo":
        return _v(p, "def_tackles_solo")
    if stat == "asist":
        return _v(p, "def_tackle_assists")
    if stat == "def_ints":
        return _v(p, "def_interceptions")
    if stat == "fg":
        return _v(p, "fg_made")
    if stat == "xp":
        return _v(p, "pat_made")
    if stat == "kick_pts":
        return 3 * _v(p, "fg_made") + _v(p, "pat_made")
    raise KeyError(stat)


def grupo(pos: str | None) -> str | None:
    pos = (pos or "").upper()
    if pos in ("RB", "FB", "HB"):
        return "RB"
    return pos if pos in POSICIONES else None


# --- Contexto de liga ------------------------------------------------------------------

def _pesos(filas: list[dict], temporada: int, decay: float) -> list[float]:
    return [decay ** i * PESO_TEMPORADA.get(temporada - (f.get("season") or temporada), 0.0)
            for i, f in enumerate(filas)]


def _media(filas: list[dict], pesos: list[float], f) -> float | None:
    sw = sum(pesos)
    return sum(w * f(x) for x, w in zip(filas, pesos)) / sw if sw > 0 else None


def _razon(filas: list[dict], pesos: list[float], num, den) -> tuple[float, float]:
    return sum(w * num(x) for x, w in zip(filas, pesos)), sum(w * den(x) for x, w in zip(filas, pesos))


METRICAS_EQUIPO = {
    # nombre: (numerador, denominador o None = por partido)
    "pts": ("points", None), "plays": ("plays", None), "dropbacks": ("dropbacks", None),
    "pass_att": ("pass_att", None), "carries": ("carries", None), "targets": ("targets", None),
    "pass_yds": ("pass_yds", None), "rush_yds": ("rush_yds", None), "yards": ("yards", None),
    "ypp": ("yards", "plays"), "epa_play": ("epa", "plays"), "pass_epa": ("pass_epa", "dropbacks"),
    "rush_epa": ("rush_epa", "carries"), "success": ("success", "plays"), "ypc": ("rush_yds", "carries"),
    "ypa": ("pass_yds", "pass_att"), "explosive": ("explosive", "plays"), "rz_trips": ("rz_trips", None),
    "rz_td_pct": ("rz_tds", "rz_trips"), "pass_tds": ("pass_tds", None), "rush_tds": ("rush_tds", None),
    "off_tds": ("off_tds", None), "td_por_punto": ("off_tds", "points"), "pass_td_share": ("pass_tds", "off_tds"),
    "sack_rate": ("sacks", "dropbacks"), "turnovers": ("turnovers", None), "third_pct": ("third_conv", "third_att"),
    "proe": ("proe", None), "qb_rush_yds": ("qb_rush_yds", None), "pass_rate": ("dropbacks", "plays"),
    "targets_por_db": ("targets", "dropbacks"), "att_por_db": ("pass_att", "dropbacks"),
    "drives": ("drives", None), "fgm": ("fgm", None), "fga": ("fga", None), "punts": ("punts", None),
    "sacks": ("sacks", None),
}
# Contracción hacia la liga de las métricas que son razón: unidades "virtuales" del denominador.
K_RAZON = {"ypp": 120, "epa_play": 150, "pass_epa": 100, "rush_epa": 80, "success": 150, "ypc": 80, "ypa": 100,
           "explosive": 150, "rz_td_pct": 10, "td_por_punto": 60, "pass_td_share": 6, "sack_rate": 100,
           "third_pct": 30, "pass_rate": 150, "targets_por_db": 100, "att_por_db": 100}
METRICAS_POS = ("carries", "rushing_yards", "rushing_tds", "targets", "receptions", "receiving_yards",
                "receiving_tds", "attempts", "completions", "passing_yards", "passing_tds", "ints", "sacks",
                "rz_carries", "rz_targets", "designed_runs", "scrambles")


def _metricas(filas: list[dict], pesos: list[float], liga: dict | None = None) -> dict:
    out = {}
    for m, (num, den) in METRICAS_EQUIPO.items():
        if den is None:
            vals = [(x.get(num), w) for x, w in zip(filas, pesos) if x.get(num) is not None]
            sw = sum(w for _, w in vals)
            v = sum(a * w for a, w in vals) / sw if sw else None
            if liga is not None and liga.get(m) is not None:
                v = ((v or 0) * sw + K_EQUIPO * liga[m]) / (sw + K_EQUIPO)
        else:
            a, b = _razon(filas, pesos, lambda x: x.get(num) or 0, lambda x: x.get(den) or 0)
            if liga is not None and liga.get(m) is not None:
                k = K_RAZON.get(m, 50)   # en unidades del denominador (acarreos, pases, puntos...)
                v = (a + k * liga[m]) / (b + k)
            else:
                v = a / b if b else None
        out[m] = v
    out["n"] = sum(pesos)
    return out


@dataclass
class Perfil:
    """Lo que hace un equipo en ataque y lo que concede en defensa (ya contraído hacia la liga)."""
    team: str
    ataque: dict
    defensa: dict
    pos_defensa: dict          # pos -> métricas por partido concedidas a esa posición
    partidos: int


@dataclass
class Contexto:
    fecha: str
    temporada: int
    jugadores: dict[str, list[dict]]            # player_id -> partidos (más reciente primero)
    equipo_partido: dict[tuple[str, str], dict]  # (game_id, team) -> fila de ataque del equipo
    ofensiva: dict[str, list[dict]]             # team -> sus partidos (más reciente primero)
    defensa: dict[str, list[dict]]              # team -> filas de los rivales contra él
    pos_concedido: dict[str, list[dict]]        # team -> [{pos: métricas}] por partido (más reciente primero)
    equipo_pbp: dict[tuple[str, str], dict]     # (game_id, team) -> sumas de zona roja de sus jugadores
    roster: dict[str, dict]
    lesiones: dict[str, dict]
    movimientos: dict[str, list[dict]]
    titular_qb: dict[str, str]                  # team -> QB titular de su último partido
    liga: dict = field(default_factory=dict)
    liga_pos: dict = field(default_factory=dict)
    perfiles: dict[str, Perfil] = field(default_factory=dict)
    rangos: dict = field(default_factory=dict)
    bajas: dict[str, list[dict]] = field(default_factory=dict)   # team -> jugadores importantes fuera
    periodos: dict = field(default_factory=dict)  # reparto por cuarto de puntos, TD y estadísticas (ver _periodos)
    qb_principal: dict[str, str] = field(default_factory=dict)   # team -> QB con más titularidades de la temporada


def _temporada(conn, fecha: str) -> int:
    r = conn.execute("SELECT season FROM nfl_games WHERE gameday >= ? ORDER BY gameday LIMIT 1", (fecha,)).fetchone()
    if r:
        return r[0]
    r = conn.execute("SELECT MAX(season) FROM nfl_games").fetchone()
    return r[0] if r and r[0] else int(fecha[:4])


def construir_contexto(conn, fecha: str, usar_estado_actual: bool = True) -> Contexto:
    """Todo lo jugado antes de `fecha`. Con usar_estado_actual=False (backtest) no se usan lesiones ni plantillas."""
    temporada = _temporada(conn, fecha)
    desde = temporada - 2
    jugadores: dict[str, list[dict]] = defaultdict(list)
    for r in conn.execute(
            "SELECT pg.*, g.gameday, g.home_team, g.spread_line, g.total_line, g.roof, g.wind, "
            "pp.rz_carries, pp.i10_carries, pp.i5_carries, pp.rz_targets, pp.i10_targets, pp.ez_targets, "
            "pp.designed_runs, pp.scrambles, pp.long_rush, pp.long_rec, pp.long_pass, pp.rz_rec, pp.rz_rec_tds, "
            "pp.rz_rush_tds, pp.ez_rec, s.offense_pct, s.offense_snaps "
            "FROM nfl_player_games pg JOIN nfl_games g ON g.game_id = pg.game_id "
            "LEFT JOIN nfl_player_pbp pp ON pp.game_id = pg.game_id AND pp.player_id = pg.player_id "
            "LEFT JOIN nfl_snaps s ON s.game_id = pg.game_id AND s.player_id = pg.player_id "
            "WHERE g.gameday < ? AND pg.season >= ? ORDER BY g.gameday DESC", (fecha, desde)):
        p = dict(r)
        p["is_home"] = int(p["home_team"] == p["team"])
        # spread_line es la ventaja esperada del local: desde el punto de vista del jugador.
        if p["spread_line"] is not None:
            p["spread_equipo"] = p["spread_line"] if p["is_home"] else -p["spread_line"]
        jugadores[p["player_id"]].append(p)
    equipo_partido: dict[tuple[str, str], dict] = {}
    ofensiva: dict[str, list[dict]] = defaultdict(list)
    defensa: dict[str, list[dict]] = defaultdict(list)
    for r in conn.execute(
            "SELECT t.*, g.gameday FROM nfl_team_games t JOIN nfl_games g ON g.game_id = t.game_id "
            "WHERE g.gameday < ? AND t.season >= ? ORDER BY g.gameday DESC", (fecha, desde)):
        t = dict(r)
        t["off_tds"] = (t["pass_tds"] or 0) + (t["rush_tds"] or 0)
        t["explosive"] = (t["explosive_pass"] or 0) + (t["explosive_rush"] or 0)
        equipo_partido[(t["game_id"], t["team"])] = t
        ofensiva[t["team"]].append(t)
        defensa[t["opp"]].append(t)
    equipo_pbp: dict[tuple[str, str], dict] = defaultdict(lambda: defaultdict(float))
    for pid, partidos in jugadores.items():
        for p in partidos:
            e = equipo_pbp[(p["game_id"], p["team"])]
            for c in ("rz_carries", "i10_carries", "i5_carries", "rz_targets", "i10_targets", "ez_targets", "rz_rec",
                      "rz_rec_tds", "rz_rush_tds"):
                e[c] += p.get(c) or 0
            e["rushing_tds"] += p.get("rushing_tds") or 0
            e["receiving_tds"] += p.get("receiving_tds") or 0
    # Lo concedido a cada posición, partido a partido (0 si esa posición no hizo nada ese día).
    por_partido_pos: dict[tuple[str, str], dict] = defaultdict(lambda: defaultdict(float))
    for partidos in jugadores.values():
        for p in partidos:
            g = grupo(p.get("position"))
            if not g:
                continue
            d = por_partido_pos[(p["game_id"], p["opp"])]
            for c, src in (("carries", "carries"), ("rushing_yards", "rushing_yards"), ("rushing_tds", "rushing_tds"),
                           ("targets", "targets"), ("receptions", "receptions"),
                           ("receiving_yards", "receiving_yards"), ("receiving_tds", "receiving_tds"),
                           ("attempts", "attempts"), ("completions", "completions"),
                           ("passing_yards", "passing_yards"), ("passing_tds", "passing_tds"),
                           ("ints", "passing_interceptions"), ("sacks", "sacks_suffered"),
                           ("rz_carries", "rz_carries"), ("rz_targets", "rz_targets"),
                           ("rz_rec", "rz_rec"), ("rz_rec_tds", "rz_rec_tds"), ("rz_rush_tds", "rz_rush_tds"),
                           ("ez_targets", "ez_targets"), ("ez_rec", "ez_rec"),
                           ("designed_runs", "designed_runs"), ("scrambles", "scrambles")):
                d[f"{g}.{c}"] += p.get(src) or 0
    pos_concedido: dict[str, list[dict]] = {}
    for team, filas in defensa.items():
        pos_concedido[team] = [{**por_partido_pos.get((f["game_id"], team), {}), "season": f["season"]}
                               for f in filas]
    roster, lesiones, movimientos = {}, {}, defaultdict(list)
    if usar_estado_actual:
        roster = {r["player_id"]: dict(r) for r in conn.execute("SELECT * FROM nfl_rosters")}
        for r in conn.execute("SELECT * FROM nfl_injuries ORDER BY CASE fuente WHEN 'espn' THEN 1 ELSE 0 END"):
            lesiones[r["player_id"]] = dict(r)
        for r in conn.execute("SELECT * FROM nfl_movimientos WHERE season = ? ORDER BY week", (temporada,)):
            movimientos[r["player_id"]].append(dict(r))
    titular_qb = {}
    for r in conn.execute("SELECT home_team, away_team, home_qb_id, away_qb_id FROM nfl_games "
                          "WHERE gameday < ? AND season >= ? ORDER BY gameday", (fecha, desde)):
        if r["home_qb_id"]:
            titular_qb[r["home_team"]] = r["home_qb_id"]
        if r["away_qb_id"]:
            titular_qb[r["away_team"]] = r["away_qb_id"]
    ctx = Contexto(fecha, temporada, dict(jugadores), equipo_partido, dict(ofensiva), dict(defensa), pos_concedido,
                   dict(equipo_pbp), roster, lesiones, dict(movimientos), titular_qb)
    _preparar_liga(ctx)
    ctx.periodos = _periodos(conn, fecha, desde)
    # QB principal: el de más titularidades esta temporada (2+); si no hay, el de la temporada anterior.
    titularidades: dict[tuple[str, int], dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for r in conn.execute("SELECT season, home_team, away_team, home_qb_id, away_qb_id FROM nfl_games "
                          "WHERE gameday < ? AND season >= ?", (fecha, temporada - 1)):
        for t, q in ((r["home_team"], r["home_qb_id"]), (r["away_team"], r["away_qb_id"])):
            if q:
                titularidades[(t, r["season"])][q] += 1
    for (t, season), qbs in sorted(titularidades.items(), key=lambda kv: kv[0][1]):
        q, n = max(qbs.items(), key=lambda kv: kv[1])
        if season < temporada or n >= 2:
            ctx.qb_principal[t] = q
    return ctx


def qb_del_partido(ctx: Contexto, team: str) -> tuple[str | None, str | None, bool]:
    """(QB que se espera de titular, QB principal del equipo, si juega un suplente)."""
    principal = ctx.qb_principal.get(team)
    titular = ctx.titular_qb.get(team)
    if titular and not disponible(ctx, titular)[0]:
        titular = None
    if principal and titular != principal and disponible(ctx, principal)[0] and \
            _equipo_actual(ctx, principal, ctx.jugadores.get(principal, [])) == team:
        titular = principal       # el principal vuelve de lesión
    suplente = bool(principal) and titular != principal
    return titular, principal, suplente


def _nombre(ctx: Contexto, pid: str | None) -> str:
    if not pid:
        return "?"
    r = ctx.roster.get(pid)
    if r and r.get("name"):
        return r["name"]
    p = ctx.jugadores.get(pid)
    return (p[0].get("name") if p else None) or pid


# Reparto por cuarto si la base aún no tiene jugada a jugada (medias aproximadas de la NFL).
REPARTO_DEFECTO = {1: 0.22, 2: 0.30, 3: 0.21, 4: 0.27}
COLUMNAS_CUARTO = {"pass_yds": "passing_yards", "pass_att": "attempts", "comp": "completions",
                   "pass_tds": "passing_tds", "ints": "passing_interceptions", "rush_yds": "rushing_yards",
                   "rush_att": "carries", "rec": "receptions", "rec_yds": "receiving_yards", "targets": "targets"}


def _periodos(conn, fecha: str, desde: int) -> dict:
    """Qué parte de cada cosa pasa en cada cuarto (liga): puntos, TD, FG y cada estadística de jugador.

    También guarda las distancias de los FG anotados, y por posesión los safeties y los TD de defensa o
    equipos especiales, para el simulador de partidos.
    """
    out: dict = {"puntos": dict(REPARTO_DEFECTO), "TD": dict(REPARTO_DEFECTO), "FG": dict(REPARTO_DEFECTO),
                 "distancias_fg": [], "safety_por_drive": 0.003, "td_def_por_drive": 0.007, "partidos": 0}
    filas = conn.execute(
        "SELECT a.qtr, a.tipo, a.puntos, a.distancia, a.team, a.player_id, a.game_id FROM nfl_anotaciones a "
        "JOIN nfl_games g ON g.game_id = a.game_id WHERE g.gameday < ? AND g.season >= ?", (fecha, desde)).fetchall()
    if filas:
        for clave, filtro in (("puntos", lambda r: True), ("TD", lambda r: r["tipo"] == "TD"),
                              ("FG", lambda r: r["tipo"] == "FG")):
            por_q = defaultdict(float)
            for r in filas:
                if filtro(r) and 1 <= (r["qtr"] or 0) <= 4:
                    por_q[r["qtr"]] += r["puntos"] if clave == "puntos" else 1
            total = sum(por_q.values())
            if total:
                out[clave] = {q: por_q[q] / total for q in (1, 2, 3, 4)}
        out["distancias_fg"] = [r["distancia"] for r in filas if r["tipo"] == "FG" and r["distancia"]]
        drives = conn.execute(
            "SELECT SUM(t.drives), COUNT(DISTINCT t.game_id) FROM nfl_team_games t JOIN nfl_games g "
            "ON g.game_id = t.game_id WHERE g.gameday < ? AND g.season >= ?", (fecha, desde)).fetchone()
        if drives and drives[0]:
            out["partidos"] = drives[1]
            out["safety_por_drive"] = max(0.001, sum(r["tipo"] == "SAF" for r in filas) / drives[0])
            # TD que no son del ataque: el anotador no figura como corredor/receptor del equipo que anota.
            td_def = conn.execute(
                "SELECT COUNT(*) FROM nfl_anotaciones a JOIN nfl_games g ON g.game_id = a.game_id "
                "WHERE a.tipo = 'TD' AND g.gameday < ? AND g.season >= ? AND NOT EXISTS (SELECT 1 FROM "
                "nfl_player_quarter q WHERE q.game_id = a.game_id AND q.player_id = a.player_id AND "
                "(q.rushing_tds > 0 OR q.receiving_tds > 0))", (fecha, desde)).fetchone()[0]
            out["td_def_por_drive"] = max(0.002, td_def / drives[0])
    sumas = {}
    for stat, col in COLUMNAS_CUARTO.items():
        por_q = {r[0]: r[1] or 0 for r in conn.execute(
            f"SELECT q.qtr, SUM(q.{col}) FROM nfl_player_quarter q JOIN nfl_games g ON g.game_id = q.game_id "
            f"WHERE g.gameday < ? AND g.season >= ? AND q.qtr BETWEEN 1 AND 4 GROUP BY q.qtr", (fecha, desde))}
        total = sum(por_q.values())
        sumas[stat] = {q: por_q.get(q, 0) / total for q in (1, 2, 3, 4)} if total else dict(REPARTO_DEFECTO)
    out["stats"] = sumas
    return out


PERIODOS = {"game": (1, 2, 3, 4), "1h": (1, 2), "2h": (3, 4), "1q": (1,), "2q": (2,), "3q": (3,), "4q": (4,)}
NOMBRE_PERIODO = {"game": "", "1h": "1.ª mitad", "2h": "2.ª mitad", "1q": "1.er cuarto", "2q": "2.º cuarto",
                  "3q": "3.er cuarto", "4q": "4.º cuarto"}


def fraccion(ctx: Contexto, clave: str, periodo: str) -> float:
    """Parte del partido que corresponde a un periodo para puntos, TD o una estadística de jugador."""
    if periodo == "game":
        return 1.0
    reparto = ctx.periodos.get("stats", {}).get(clave) or ctx.periodos.get(clave) or REPARTO_DEFECTO
    return sum(reparto.get(q, 0.25) for q in PERIODOS[periodo])


def _preparar_liga(ctx: Contexto) -> None:
    filas = [f for fs in ctx.ofensiva.values() for f in fs]
    pesos = [PESO_TEMPORADA.get(ctx.temporada - f["season"], 0.0) for f in filas]
    ctx.liga = _metricas(filas, pesos)
    filas_pos = [x for fs in ctx.pos_concedido.values() for x in fs]
    pesos_pos = [PESO_TEMPORADA.get(ctx.temporada - x["season"], 0.0) for x in filas_pos]
    sw = sum(pesos_pos) or 1
    ctx.liga_pos = {k: sum(w * x.get(k, 0) for x, w in zip(filas_pos, pesos_pos)) / sw
                    for k in {k for x in filas_pos for k in x if k != "season"}}
    for team in ctx.ofensiva:
        of, de = ctx.ofensiva[team], ctx.defensa.get(team, [])
        pos = ctx.pos_concedido.get(team, [])
        wp = _pesos(pos, ctx.temporada, DECAY_EQUIPO)
        swp = sum(wp)
        pos_def = {k: (sum(w * x.get(k, 0) for x, w in zip(pos, wp)) + K_EQUIPO * v) / (swp + K_EQUIPO)
                   for k, v in ctx.liga_pos.items()}
        pos_def["_n"] = swp
        ctx.perfiles[team] = Perfil(team, _metricas(of, _pesos(of, ctx.temporada, DECAY_EQUIPO), ctx.liga),
                                    _metricas(de, _pesos(de, ctx.temporada, DECAY_EQUIPO), ctx.liga), pos_def,
                                    sum(1 for f in of if f["season"] == ctx.temporada))
    _rangos(ctx)


def _rangos(ctx: Contexto) -> None:
    """Puesto de cada equipo (1 = el que más) en cada métrica de ataque, de defensa y por posición."""
    activos = [t for t, p in ctx.perfiles.items() if any(f["season"] == ctx.temporada for f in ctx.ofensiva[t])]
    if len(activos) < 8:
        activos = list(ctx.perfiles)
    for lado in ("ataque", "defensa"):
        for m in METRICAS_EQUIPO:
            vals = sorted(((getattr(ctx.perfiles[t], lado).get(m), t) for t in activos
                           if getattr(ctx.perfiles[t], lado).get(m) is not None), reverse=True)
            for i, (_, t) in enumerate(vals):
                ctx.rangos[(lado, m, t)] = (i + 1, len(vals))
    for k in ctx.liga_pos:
        vals = sorted(((ctx.perfiles[t].pos_defensa.get(k, 0), t) for t in activos), reverse=True)
        for i, (_, t) in enumerate(vals):
            ctx.rangos[("pos", k, t)] = (i + 1, len(vals))


def rango(ctx: Contexto, lado: str, metrica: str, team: str) -> tuple[int, int] | None:
    return ctx.rangos.get((lado, metrica, team))


def texto_rango(r: tuple[int, int] | None, mas: str = "más", menos: str = "menos") -> str:
    if not r:
        return ""
    i, n = r
    if i <= n / 2:
        return f"{i}º que {mas} de {n}"
    return f"{n - i + 1}º que {menos} de {n}"


# --- Entorno del partido ------------------------------------------------------------------

@dataclass
class Linea:
    """Lo que dice el mercado del partido (si se sabe)."""
    total: float | None = None
    spread_home: float | None = None      # ventaja esperada del local (positivo = local favorito)
    team_total: dict[str, float] = field(default_factory=dict)


@dataclass
class Entorno:
    team: str
    opp: str
    local: bool
    puntos: float
    puntos_fuente: str
    spread: float                          # ventaja esperada del equipo (positivo = favorito)
    dropbacks: float
    pass_att: float
    targets: float
    carries: float
    tds: float
    pass_tds: float
    rush_tds: float
    viento: float | None
    techo: str | None
    factores: list = field(default_factory=list)
    qb_suplente: bool = False


def entorno(ctx: Contexto, team: str, opp: str, local: bool, linea: Linea | None = None,
            viento: float | None = None, techo: str | None = None) -> Entorno:
    linea = linea or Linea()
    of, de = ctx.perfiles[team].ataque, ctx.perfiles[opp].defensa
    lg = ctx.liga
    factores = []
    spread = None
    if linea.spread_home is not None:
        spread = linea.spread_home if local else -linea.spread_home
    if team in linea.team_total:
        pts, fuente = linea.team_total[team], "total del equipo en las casas"
    elif linea.total is not None and spread is not None:
        pts, fuente = (linea.total + spread) / 2, "total y spread de las casas"
    else:
        pts = of["pts"] * de["pts"] / lg["pts"] + (VENTAJA_LOCAL / 2 if local else -VENTAJA_LOCAL / 2)
        fuente = "modelo (ataque × defensa rival)"
    titular, principal, suplente = qb_del_partido(ctx, team)
    if spread is None:
        rival = ctx.perfiles[opp].ataque["pts"] * ctx.perfiles[team].defensa["pts"] / lg["pts"]
        spread = pts - (rival + (-VENTAJA_LOCAL / 2 if local else VENTAJA_LOCAL / 2))
    s = max(-14.0, min(14.0, spread))
    ritmo_db = math.sqrt(de["dropbacks"] / lg["dropbacks"])
    ritmo_car = math.sqrt(de["carries"] / lg["carries"])
    dropbacks = of["dropbacks"] * ritmo_db * (1 - GUION_PASE * s)
    carries = of["carries"] * ritmo_car * (1 + GUION_CARRERA * s)
    if abs(s) >= 3:
        factores.append(Factor(
            f"{'favorito' if s > 0 else 'no favorito'} por {abs(spread):.1f}: guion con "
            f"{'más carreras' if s > 0 else 'más pases'} ({1 + GUION_CARRERA * s:.2f}× carreras, "
            f"{1 - GUION_PASE * s:.2f}× pases)", None, "guion"))
    tdp = of["td_por_punto"]
    tds = pts * tdp
    share_of = of["pass_td_share"]
    share_de = de["pass_td_share"]
    p_pase = max(0.3, min(0.85, 0.5 * share_of + 0.5 * share_de))
    if suplente:
        factores.append(Factor(
            f"QB suplente: {_nombre(ctx, titular)} en lugar de {_nombre(ctx, principal)}. Con suplente los equipos "
            f"lanzan un 28% menos de TD, corren casi los mismos (-7%) y le dan más balones al RB1 cerca de la meta "
            f"(+9%), pero llegan un 15% menos a la zona roja", None, "qb"))
    if viento is not None and viento >= VIENTO_FUERTE and techo not in ("dome", "closed"):
        dropbacks *= 0.97
        carries *= 1.03
        p_pase = max(0.3, p_pase - 0.05)
        factores.append(Factor(f"viento de {viento:.0f} mph: menos juego aéreo", EFECTO_VIENTO, "clima"))
    return Entorno(team, opp, local, pts, fuente, spread, dropbacks, dropbacks * of["att_por_db"],
                   dropbacks * of["targets_por_db"], carries, tds, tds * p_pase, tds * (1 - p_pase), viento, techo,
                   factores, suplente)


# --- Jugadores -----------------------------------------------------------------------------

@dataclass
class Factor:
    texto: str
    efecto: float | None        # multiplicador sobre la media (None = dato de contexto)
    tipo: str = ""


@dataclass
class Jugador:
    player_id: str
    nombre: str
    pos: str
    team: str
    partidos: list[dict]               # todos (más reciente primero)
    con_equipo: list[dict]             # los jugados con su equipo actual
    estado: str = ""                   # parte de lesiones
    detalle_lesion: str = ""
    llegada: dict | None = None        # movimiento de esta temporada al equipo actual
    shares: dict = field(default_factory=dict)
    shares_base: dict = field(default_factory=dict)
    ajuste_reparto: dict = field(default_factory=dict)
    notas: list[str] = field(default_factory=list)

    @property
    def n(self) -> int:
        return len(self.partidos)


@dataclass
class Proyeccion:
    jugador: Jugador
    entorno: Entorno
    medias: dict[str, float]
    varianzas: dict[str, float]
    factores: dict[str, list[Factor]]
    lambdas: dict[str, float]          # TD esperados: rush_tds, rec_tds, tds
    volumen: dict[str, float]          # acarreos, envíos, pases esperados

    def prob(self, stat: str, line: float) -> tuple[float, float]:
        if stat in ("first_td", "last_td"):
            raise ValueError("el primer y el último TD se calculan por partido (ver analizador.primer_td)")
        if stat == "ypc":
            z = (line - self.medias[stat]) / math.sqrt(self.varianzas[stat])
            mas = 0.5 * math.erfc(z / math.sqrt(2))
            return calibrar(mas), calibrar(1 - mas)
        mas, menos = prob_lados(line, self.medias[stat], self.varianzas[stat])
        if stat in STATS_CONTEO:
            return mas, menos
        return calibrar(mas), calibrar(menos)

    def prob_periodo(self, ctx: "Contexto", stat: str, periodo: str, line: float) -> tuple[float, float] | None:
        """Prop de un cuarto o una mitad: la media del partido × la parte que suele pasar en ese periodo.

        La dispersión crece al acortar el periodo (la varianza relativa va como 1/fracción)."""
        if periodo == "game":
            return self.prob(stat, line)
        if stat not in self.medias or stat in ("ypc", "long_rec", "long_rush", "long_pass", "fantasy"):
            return None
        if stat in ("tds", "rush_tds", "rec_tds"):
            mu = self.medias[stat] * fraccion(ctx, "TD", periodo)
            return prob_lados(line, mu, mu + 0.05 * mu * mu)
        claves = {"rush_rec_yds": ("rush_yds", "rec_yds"), "pass_rush_yds": ("pass_yds", "rush_yds")}.get(stat, (stat,))
        f = sum(fraccion(ctx, c, periodo) for c in claves) / len(claves)
        mu = self.medias[stat] * f
        if stat in STATS_CONTEO:
            var = mu + 0.08 * mu * mu
        else:
            cv2 = self.varianzas[stat] / max(self.medias[stat], 1e-9) ** 2
            var = max(mu * 1.05, cv2 / max(f, 0.05) * mu * mu)
        mas, menos = prob_lados(line, mu, var)
        return (mas, menos) if stat in STATS_CONTEO else (calibrar(mas), calibrar(menos))


def calibrar(p: float) -> float:
    p = min(max(p, 1e-4), 1 - 1e-4)
    return 1 / (1 + math.exp(-CALIBRACION_LOGIT * math.log(p / (1 - p))))


def _equipo_actual(ctx: Contexto, pid: str, partidos: list[dict]) -> str | None:
    r = ctx.roster.get(pid)
    if r and r.get("team"):
        return r["team"]
    return partidos[0]["team"] if partidos else None


def disponible(ctx: Contexto, pid: str) -> tuple[bool, str, str]:
    """(juega, estado, detalle) según el parte de lesiones y el estado en la plantilla."""
    les = ctx.lesiones.get(pid)
    if les and estado_fuera(les.get("status")):
        return False, les["status"], les.get("detail") or ""
    r = ctx.roster.get(pid)
    if r and r.get("status") in ROSTER_FUERA and r.get("season") == ctx.temporada:
        return False, {"RES": "Reserva/IR", "CUT": "Cortado", "INA": "Inactivo", "DEV": "Equipo de prácticas",
                       "RET": "Retirado", "SUS": "Suspendido"}.get(r["status"], r["status"]), ""
    if les and estado_duda(les.get("status")):
        return True, les["status"], les.get("detail") or ""
    return True, "", ""


def candidatos(ctx: Contexto, team: str, ultimos: int = 4) -> list[Jugador]:
    """Jugadores del equipo que han tenido papel en sus últimos partidos (o que acaban de llegar)."""
    juegos = [f["game_id"] for f in ctx.ofensiva.get(team, [])[:ultimos]]
    ids = set()
    for pid, partidos in ctx.jugadores.items():
        if _equipo_actual(ctx, pid, partidos) != team:
            continue
        reciente = any(p["game_id"] in juegos for p in partidos[:ultimos + 2])
        llegada = any(m["to_team"] == team for m in ctx.movimientos.get(pid, []))
        if reciente or (llegada and partidos and partidos[0]["season"] >= ctx.temporada - 1):
            ids.add(pid)
    out = []
    for pid in ids:
        partidos = ctx.jugadores[pid]
        pos = grupo((ctx.roster.get(pid) or {}).get("position") or partidos[0].get("position"))
        if not pos:
            continue
        con_equipo = [p for p in partidos if p["team"] == team]
        llegada = next((m for m in reversed(ctx.movimientos.get(pid, [])) if m["to_team"] == team and m["week"] > 0),
                       None)
        juega, estado, detalle = disponible(ctx, pid)
        j = Jugador(pid, partidos[0].get("name") or pid, pos, team, partidos, con_equipo, estado, detalle, llegada)
        if not juega:
            j.notas.append(f"fuera: {estado}{f' ({detalle})' if detalle else ''}")
        out.append(j)
    return out


SHARES = {
    # nombre: (columna del jugador, columna del equipo, fuente del equipo)
    "carries": ("carries", "carries", "team"), "targets": ("targets", "targets", "team"),
    "att": ("attempts", "pass_att", "team"), "rz_carries": ("rz_carries", "rz_carries", "pbp"),
    "i10_carries": ("i10_carries", "i10_carries", "pbp"), "i5_carries": ("i5_carries", "i5_carries", "pbp"),
    "rz_targets": ("rz_targets", "rz_targets", "pbp"), "i10_targets": ("i10_targets", "i10_targets", "pbp"),
    "ez_targets": ("ez_targets", "ez_targets", "pbp"), "rush_tds": ("rushing_tds", "rushing_tds", "pbp"),
    "rec_tds": ("receiving_tds", "receiving_tds", "pbp"),
}


def _shares(ctx: Contexto, j: Jugador) -> dict:
    """Cuota de cada oportunidad del equipo en los partidos que jugó con él (con más peso a los recientes)."""
    partidos = j.con_equipo if len(j.con_equipo) >= 2 else j.partidos
    # Fuera los partidos que dejó a medias (lesión, expulsión): menos de la mitad de sus snaps habituales.
    snaps = sorted(p["offense_pct"] for p in partidos[:8] if p.get("offense_pct"))
    if len(snaps) >= 3:
        mediana = snaps[len(snaps) // 2]
        completos = [p for p in partidos if not p.get("offense_pct") or p["offense_pct"] >= 0.5 * mediana]
        if len(completos) >= 2:
            partidos = completos
    pesos = _pesos(partidos, ctx.temporada, DECAY_JUGADOR)
    out = {"_n": sum(1 for p in partidos if p["season"] == ctx.temporada), "_peso": sum(pesos),
           "_juegos": {p["game_id"]: w for p, w in zip(partidos, pesos)}}
    for nombre, (col_j, col_t, fuente) in SHARES.items():
        num = den = 0.0
        for p, w in zip(partidos, pesos):
            tabla = ctx.equipo_partido if fuente == "team" else ctx.equipo_pbp
            t = tabla.get((p["game_id"], p["team"]))
            if not t:
                continue
            num += w * (p.get(col_j) or 0)
            den += w * (t.get(col_t) or 0)
        out[nombre] = (num, den)
    return out


def _share(sh: dict, nombre: str, previo: float, k: float) -> float:
    num, den = sh[nombre]
    return (num + k * previo) / (den + k) if den + k > 0 else previo


def preparar_equipo(ctx: Contexto, team: str) -> list[Jugador]:
    """Cuotas de oportunidades de cada jugador disponible, repartiendo lo que dejan los que están fuera."""
    todos = candidatos(ctx, team)
    activos = [j for j in todos if not any(n.startswith("fuera") for n in j.notas)]
    fuera = [j for j in todos if j not in activos]
    for j in todos:
        sh = _shares(ctx, j)
        base = {}
        base["carries"] = _share(sh, "carries", 0.0, 0)
        base["targets"] = _share(sh, "targets", 0.0, 0)
        base["att"] = _share(sh, "att", 0.0, 0)
        # Zona roja: contraída hacia su cuota general (pocas jugadas por partido).
        base["rz_carries"] = _share(sh, "rz_carries", base["carries"], 6)
        base["i10_carries"] = _share(sh, "i10_carries", base["rz_carries"], 4)
        base["i5_carries"] = _share(sh, "i5_carries", base["i10_carries"], 3)
        base["rz_targets"] = _share(sh, "rz_targets", base["targets"], 6)
        base["i10_targets"] = _share(sh, "i10_targets", base["rz_targets"], 4)
        base["ez_targets"] = _share(sh, "ez_targets", base["targets"], 4)
        base["rush_tds"] = _share(sh, "rush_tds", base["i10_carries"], 3)
        base["rec_tds"] = _share(sh, "rec_tds", base["rz_targets"], 3)
        # Cuota de TD esperada: dentro de la 10 pesa más que la cuota general.
        base["td_rush"] = (0.40 * base["i10_carries"] + 0.15 * base["i5_carries"] + 0.20 * base["rz_carries"]
                           + 0.10 * base["carries"] + 0.15 * base["rush_tds"])
        base["td_rec"] = (0.30 * base["rz_targets"] + 0.15 * base["i10_targets"] + 0.15 * base["ez_targets"]
                          + 0.25 * base["targets"] + 0.15 * base["rec_tds"])
        if j.pos == "QB":
            base["att_hist"], base["att"] = base["att"], 0.0
        j.shares_base = base
        j.shares = dict(base)
        j.juegos = sh["_juegos"]
        if j.llegada and len(j.con_equipo) < 2:
            j.notas.append(f"llegó a {team} en la semana {j.llegada['week']} desde {j.llegada['from_team']}: "
                           f"{len(j.con_equipo)} partido(s) con su equipo nuevo")
    _corregir_regresos(ctx, team, activos)
    # QB suplente: queda anotado en el RB1 como razonamiento (ver el comentario de DUDA).
    titular, principal, suplente = qb_del_partido(ctx, team)
    rbs = [j for j in activos if j.pos == "RB"]
    if suplente and rbs:
        rb1 = max(rbs, key=lambda j: j.shares.get("carries", 0))
        rb1.notas.append(f"con {_nombre(ctx, titular)} de QB suplente, el plan lógico es apoyarse en él cerca de la "
                         f"meta (+9% de acarreos dentro de la 10 en equipos con suplente)")
    # QB: el titular (el de su último partido si está disponible; si no, el QB disponible con más pases).
    qbs = [j for j in activos if j.pos == "QB"]
    if qbs:
        titular = next((j for j in qbs if j.player_id == ctx.titular_qb.get(team)), None)
        if titular is None:
            titular = max(qbs, key=lambda j: sum(p.get("attempts") or 0 for p in j.partidos[:6]))
            ausente = next((j for j in fuera if j.player_id == ctx.titular_qb.get(team)), None)
            if ausente:
                titular.notas.append(f"titular por la baja de {ausente.nombre}")
        titular.shares["att"] = 0.97
        for j in qbs:
            if j is not titular:
                j.shares = {k: 0.0 for k in j.shares}
                j.notas.append("suplente: no se proyecta")
    # Reparto: los activos se quedan con lo que dejan los de fuera (proporcional a su cuota), con tope.
    nombres_fuera = ", ".join(j.nombre for j in fuera
                              if max(j.shares_base.get("carries", 0), j.shares_base.get("targets", 0)) >= 0.12)
    for clave in CLAVES_REPARTO:
        total = sum(j.shares.get(clave, 0) for j in activos)
        if total <= 0:
            continue
        f = max(0.75, min(1.5, (1 - FUGA_REPARTO) / total))
        for j in activos:
            j.shares[clave] = j.shares.get(clave, 0) * f
            j.ajuste_reparto[clave] = f
    ctx.bajas[team] = [
        {"player_id": j.player_id, "nombre": j.nombre, "pos": j.pos, "estado": j.estado, "detalle": j.detalle_lesion,
         "acarreos": j.shares_base.get("carries", 0), "envios": j.shares_base.get("targets", 0),
         "pases": j.shares_base.get("att_hist", 0),
         "titular_qb": j.player_id == ctx.titular_qb.get(team)}
        for j in fuera if j.player_id == ctx.titular_qb.get(team) or j.shares_base.get("att_hist", 0) >= 0.5
        or (j.pos != "QB" and max(j.shares_base.get("carries", 0), j.shares_base.get("targets", 0)) >= 0.12)]
    for j in activos:
        if j.pos == "QB":
            continue
        f = j.ajuste_reparto.get("carries" if j.pos == "RB" else "targets", 1.0)
        if f > 1.06 and nombres_fuera:
            j.notas.append(f"más volumen por las bajas de {nombres_fuera} (×{f:.2f})")
    return activos


CLAVES_REPARTO = ("carries", "targets", "rz_carries", "i10_carries", "i5_carries", "rz_targets", "i10_targets",
                  "ez_targets", "td_rush", "td_rec")
CUOTA_REGRESO = 0.15       # cuota mínima del que vuelve para corregir a sus compañeros
PARTIDOS_REGRESO = 6       # últimos partidos del equipo en los que se mira quién faltó
FUERZA_REGRESO = 0.5       # parte de la corrección que se aplica (el que vuelve suele tener carga limitada)


def _corregir_regresos(ctx: Contexto, team: str, activos: list[Jugador]) -> None:
    """Corrige el volumen de quienes jugaron sin un compañero que hoy sí juega (vuelve de lesión o acaba de llegar).

    En los partidos sin él, sus compañeros absorbieron su parte; si hoy juega, esa parte vuelve a él. Si ya jugaba
    en el equipo antes de empezar a faltar, a cada compañero se le descuenta, en la fracción de sus partidos que
    fueron sin él, la cuota del que vuelve: cuota × (1 − fracción_sin × cuota_del_que_vuelve). Es la lección de Saquon Barkley contra Dallas: el modelo le
    daba el puesto a Dameon Pierce, que había sido titular solo mientras Saquon estaba lesionado.
    """
    recientes = [f["game_id"] for f in ctx.ofensiva.get(team, [])[:PARTIDOS_REGRESO]
                 if f["season"] == ctx.temporada]
    for j in activos:
        if j.pos == "QB" or max(j.shares_base.get("carries", 0), j.shares_base.get("targets", 0)) < CUOTA_REGRESO:
            continue
        jugados = {p["game_id"] for p in j.partidos if p["team"] == team}
        sin_el = [g for g in recientes if g not in getattr(j, "juegos", {}) and g not in jugados] + \
                 [g for g in recientes if g in jugados and g not in getattr(j, "juegos", {})]   # los que dejó a medias
        if not sin_el:
            continue
        # Solo corrige quien ya jugaba en el equipo antes de empezar a faltar (el titular que vuelve); el que llegó
        # mientras él no estaba es el sustituto, no al revés.
        inicio = min(ctx.equipo_partido[(g, team)]["gameday"] for g in sin_el)
        if not any(p["team"] == team and p["gameday"] < inicio for p in j.partidos):
            continue
        for k in activos:
            if k is j or k.pos == "QB" or not getattr(k, "juegos", None):
                continue
            total = sum(k.juegos.values())
            frac = sum(w for g, w in k.juegos.items() if g in sin_el) / total if total else 0
            if frac <= 0:
                continue
            for clave in CLAVES_REPARTO:
                cuota_j = min(0.8, j.shares_base.get(clave, 0))
                k.shares[clave] = k.shares.get(clave, 0) * (1 - FUERZA_REGRESO * frac * cuota_j)
            efecto = 1 - FUERZA_REGRESO * frac * min(0.8, j.shares_base.get("carries" if k.pos == "RB" else "targets", 0))
            if efecto < 0.93:
                k.notas.append(f"parte de su volumen fue sin {j.nombre}, que hoy juega (×{efecto:.2f})")


def _eficiencia(ctx: Contexto, j: Jugador, num: str, den: str, previo: float, k: float) -> tuple[float, float]:
    pesos = _pesos(j.partidos, ctx.temporada, 0.92)
    a, b = _razon(j.partidos, pesos, lambda p: p.get(num) or 0, lambda p: p.get(den) or 0)
    return (a + k * previo) / (b + k), b


def _cv(ctx: Contexto, j: Jugador, stat: str, filtro=None) -> float:
    partidos = [p for p in j.partidos[:16] if filtro is None or filtro(p)]
    base = CV_DEFECTO.get(stat, 0.5)
    if len(partidos) < 4:
        return base
    vals = [valor(p, stat) for p in partidos]
    m = sum(vals) / len(vals)
    if m <= 0:
        return base
    cv2 = sum((v - m) ** 2 for v in vals) / (len(vals) - 1) / m ** 2
    n = len(vals)
    return math.sqrt((n * cv2 + 6 * base ** 2) / (n + 6))


def _pos_rate(ctx: Contexto, team: str | None, pos: str, num: str, den: str, k: float) -> tuple[float, float, float]:
    """Tasa que el rival concede a la posición frente a la de la liga: (factor contraído, del rival, de liga)."""
    lg_n, lg_d = ctx.liga_pos.get(f"{pos}.{num}", 0), ctx.liga_pos.get(f"{pos}.{den}", 0)
    liga = lg_n / lg_d if lg_d else 0
    if not team or team not in ctx.perfiles or not liga:
        return 1.0, liga, liga
    pd = ctx.perfiles[team].pos_defensa
    n = pd.get("_n", 0)
    a, b = pd.get(f"{pos}.{num}", 0) * (n + K_EQUIPO), pd.get(f"{pos}.{den}", 0) * (n + K_EQUIPO)
    rival = a / b if b else liga
    contraido = (a + k * liga) / (b + k)
    return contraido / liga, rival, liga


def _por_partido(ctx: Contexto, team: str, clave: str) -> tuple[float, float]:
    """Lo que el rival concede por partido (contraído) y la media de la liga."""
    return ctx.perfiles[team].pos_defensa.get(clave, 0), ctx.liga_pos.get(clave, 0)


def proyectar(ctx: Contexto, j: Jugador, ent: Entorno) -> Proyeccion:
    opp, pos, sh = ent.opp, j.pos, j.shares
    nombre_opp = opp
    medias, var, fac, lam, vol = {}, {}, defaultdict(list), {}, {}
    duda = DUDA if estado_duda(j.estado) else 1.0
    viento = ent.viento is not None and ent.viento >= VIENTO_FUERTE and ent.techo not in ("dome", "closed")
    local = 1.01 if ent.local else 0.99
    lp = {"QB": "QB", "RB": "RB", "WR": "WR", "TE": "TE"}[pos]

    # Volumen.
    carries = sh.get("carries", 0) * ent.carries * duda
    targets = sh.get("targets", 0) * ent.targets * duda
    att = sh.get("att", 0) * ent.pass_att * duda
    tg_r, tg_l = _por_partido(ctx, opp, f"{lp}.targets")
    if tg_l and pos in ("RB", "WR", "TE"):
        vol_f = math.sqrt(tg_r / tg_l)
        targets *= vol_f
        if abs(vol_f - 1) >= 0.05:
            fac["targets"].append(Factor(
                f"{nombre_opp} concede {tg_r:.1f} envíos por partido a los {lp} (media {tg_l:.1f}; "
                f"{texto_rango(rango(ctx, 'pos', f'{lp}.targets', opp))})", vol_f, "rival"))
    vol.update(carries=carries, targets=targets, att=att)

    # Eficiencia del jugador, contraída hacia su posición.
    lg_ypc = ctx.liga_pos.get(f"{lp}.rushing_yards", 0) / max(ctx.liga_pos.get(f"{lp}.carries", 0), 1e-9) or 4.3
    lg_ypt = ctx.liga_pos.get(f"{lp}.receiving_yards", 0) / max(ctx.liga_pos.get(f"{lp}.targets", 0), 1e-9) or 7.5
    lg_cr = ctx.liga_pos.get(f"{lp}.receptions", 0) / max(ctx.liga_pos.get(f"{lp}.targets", 0), 1e-9) or 0.65
    ypc, n_car = _eficiencia(ctx, j, "rushing_yards", "carries", lg_ypc, 40)
    ypt, n_tg = _eficiencia(ctx, j, "receiving_yards", "targets", lg_ypt, 30)
    cr, _ = _eficiencia(ctx, j, "receptions", "targets", lg_cr, 30)

    # Rival por posición.
    f_ypc, r_ypc, l_ypc = _pos_rate(ctx, opp, lp, "rushing_yards", "carries", 80)
    f_ypt, r_ypt, l_ypt = _pos_rate(ctx, opp, lp, "receiving_yards", "targets", 60)
    f_cr, r_cr, l_cr = _pos_rate(ctx, opp, lp, "receptions", "targets", 60)

    if pos in ("RB", "WR", "TE") or carries > 0.5:
        if pos == "QB":
            qb_r, qb_l = _por_partido(ctx, opp, "QB.rushing_yards")
            f_qb = (qb_r / qb_l) if qb_l else 1.0
            mu_ry = carries * ypc * f_qb * local
            fac["rush_yds"].append(Factor(
                f"{nombre_opp} concede {qb_r:.1f} yardas por tierra por partido a los QB (media {qb_l:.1f}; "
                f"{texto_rango(rango(ctx, 'pos', 'QB.rushing_yards', opp))})", f_qb, "rival"))
            carries *= math.sqrt(f_qb)
        else:
            mu_ry = carries * ypc * f_ypc * local
            if abs(f_ypc - 1) >= 0.03:
                fac["rush_yds"].append(Factor(
                    f"{nombre_opp} permite {r_ypc:.2f} yardas por acarreo a los {lp} (media {l_ypc:.2f}; "
                    f"{texto_rango(rango(ctx, 'defensa', 'ypc', opp))} en yardas por acarreo)", f_ypc, "rival"))
        fac["rush_yds"].insert(0, Factor(
            f"{carries:.1f} acarreos esperados ({sh.get('carries', 0) * 100:.0f}% de los {ent.carries:.0f} del equipo)"
            f" × {ypc:.2f} yardas por acarreo", None, "volumen"))
        medias["rush_att"], medias["rush_yds"] = carries, mu_ry
        fac["rush_att"].append(fac["rush_yds"][0])
    if pos in ("RB", "WR", "TE"):
        mu_rec = targets * cr * f_cr
        mu_recy = targets * ypt * f_ypt * local * (EFECTO_VIENTO if viento else 1.0)
        medias["targets"], medias["rec"], medias["rec_yds"] = targets, mu_rec, mu_recy
        fac["rec_yds"].insert(0, Factor(
            f"{targets:.1f} envíos esperados ({sh.get('targets', 0) * 100:.0f}% de los {ent.targets:.0f} del equipo)"
            f" × {ypt:.1f} yardas por envío", None, "volumen"))
        fac["rec"].insert(0, Factor(f"{targets:.1f} envíos × {cr * 100:.0f}% de recepción", None, "volumen"))
        if abs(f_ypt - 1) >= 0.03:
            fac["rec_yds"].append(Factor(
                f"{nombre_opp} concede {r_ypt:.1f} yardas por envío a los {lp} (media {l_ypt:.1f})", f_ypt, "rival"))
        if abs(f_cr - 1) >= 0.03:
            fac["rec"].append(Factor(
                f"{nombre_opp} permite {r_cr * 100:.0f}% de recepciones a los {lp} (media {l_cr * 100:.0f}%)",
                f_cr, "rival"))
        if viento:
            fac["rec_yds"] += ent.factores[-1:]
        medias["rush_rec_yds"] = medias.get("rush_yds", 0) + mu_recy

    if pos == "QB" and att > 0:
        lg_ypa = ctx.liga_pos.get("QB.passing_yards", 0) / max(ctx.liga_pos.get("QB.attempts", 0), 1e-9) or 6.8
        lg_cp = ctx.liga_pos.get("QB.completions", 0) / max(ctx.liga_pos.get("QB.attempts", 0), 1e-9) or 0.65
        lg_int = ctx.liga_pos.get("QB.ints", 0) / max(ctx.liga_pos.get("QB.attempts", 0), 1e-9) or 0.023
        ypa, _ = _eficiencia(ctx, j, "passing_yards", "attempts", lg_ypa, 120)
        cp, _ = _eficiencia(ctx, j, "completions", "attempts", lg_cp, 120)
        ir, _ = _eficiencia(ctx, j, "passing_interceptions", "attempts", lg_int, 250)
        f_ypa, r_ypa, l_ypa = _pos_rate(ctx, opp, "QB", "passing_yards", "attempts", 150)
        f_cp, _, _ = _pos_rate(ctx, opp, "QB", "completions", "attempts", 150)
        f_int, r_int, l_int = _pos_rate(ctx, opp, "QB", "ints", "attempts", 300)
        clima = EFECTO_VIENTO if viento else 1.0
        medias["pass_att"] = att
        medias["comp"] = att * cp * f_cp
        medias["pass_yds"] = att * ypa * f_ypa * local * clima
        medias["ints"] = att * ir * f_int
        medias["pass_tds"] = ent.pass_tds * sh.get("att", 0) * duda
        medias["pass_rush_yds"] = medias["pass_yds"] + medias.get("rush_yds", 0)
        fac["pass_yds"].insert(0, Factor(f"{att:.1f} pases esperados × {ypa:.2f} yardas por intento", None, "volumen"))
        fac["pass_yds"].append(Factor(
            f"{nombre_opp} permite {r_ypa:.2f} yardas por pase (media {l_ypa:.2f}; "
            f"{texto_rango(rango(ctx, 'defensa', 'ypa', opp))} en yardas por pase)", f_ypa, "rival"))
        rp = rango(ctx, "defensa", "pass_epa", opp)
        fac["pass_tds"].append(Factor(
            f"{ent.pass_tds:.2f} TD de pase esperados del equipo ({ent.puntos:.1f} puntos, {ent.puntos_fuente}); "
            f"{nombre_opp} es la {texto_rango(rp, 'peor', 'mejor')} defensa contra el pase por EPA", None, "entorno"))
        if abs(f_int - 1) >= 0.05:
            fac["ints"].append(Factor(f"{nombre_opp} intercepta {r_int * 100:.1f}% de los pases (media "
                                      f"{l_int * 100:.1f}%)", f_int, "rival"))
        if viento:
            fac["pass_yds"] += ent.factores[-1:]

    # Touchdowns.
    td_rush = ent.rush_tds * sh.get("td_rush", 0) * duda
    td_rec = ent.pass_tds * sh.get("td_rec", 0) * duda if pos != "QB" else 0.0
    # Lo que el rival concede a la posición en TD frente a la liga (contraído con 6 TD virtuales).
    pd = ctx.perfiles[opp].pos_defensa
    for tipo, col, total in (("rush", "rushing_tds", "rush_tds"), ("rec", "receiving_tds", "pass_tds")):
        lg_tot = sum(ctx.liga_pos.get(f"{p}.{col}", 0) for p in POSICIONES)
        r_tot = sum(pd.get(f"{p}.{col}", 0) for p in POSICIONES)
        lg_sh = ctx.liga_pos.get(f"{lp}.{col}", 0) / lg_tot if lg_tot else 0
        n = pd.get("_n", 0) + K_EQUIPO
        r_sh = ((pd.get(f"{lp}.{col}", 0) * n + 6 * lg_sh) / (r_tot * n + 6)) if lg_sh else 0
        f = max(0.75, min(1.35, r_sh / lg_sh)) if lg_sh else 1.0
        if tipo == "rush":
            td_rush *= f
        else:
            td_rec *= f
        if abs(f - 1) >= 0.08 and (td_rush if tipo == "rush" else td_rec) > 0.05:
            nombre_tipo = "por tierra" if tipo == "rush" else "por recepción"
            fac["tds"].append(Factor(
                f"{nombre_opp} concede a los {lp} el {r_sh * 100:.0f}% de sus TD {nombre_tipo} "
                f"(liga {lg_sh * 100:.0f}%)", f, "rival"))
    if pos == "QB":
        qb_r, qb_l = _por_partido(ctx, opp, "QB.rushing_tds")
        if qb_l:
            f = max(0.7, min(1.5, qb_r / qb_l))
            td_rush *= f
            if abs(f - 1) >= 0.08:
                fac["tds"].append(Factor(
                    f"{nombre_opp} concede {qb_r:.2f} TD por tierra por partido a los QB (liga {qb_l:.2f}; "
                    f"{texto_rango(rango(ctx, 'pos', 'QB.rushing_tds', opp))})", f, "rival"))
        yr, yl = _por_partido(ctx, opp, "QB.rushing_yards")
        if yl and abs(yr / yl - 1) >= 0.15:
            fac["tds"].append(Factor(
                f"{nombre_opp} concede {yr:.0f} yardas por tierra por partido a los QB (liga {yl:.0f}): "
                f"{'sufre' if yr > yl else 'contiene'} a los QB que corren", None, "rival"))
    if td_rush + td_rec > 0:
        comprimido = TD_REF * ((td_rush + td_rec) / TD_REF) ** TD_EXP
        escala = comprimido / (td_rush + td_rec)
        td_rush, td_rec = td_rush * escala, td_rec * escala
    lam.update(rush_tds=td_rush, rec_tds=td_rec, tds=td_rush + td_rec)
    if td_rush > 0.02:
        fac["tds"].insert(0, Factor(
            f"TD por tierra: {ent.rush_tds:.2f} esperados del equipo × {sh.get('td_rush', 0) * 100:.0f}% de cuota "
            f"(dentro de la 10: {sh.get('i10_carries', 0) * 100:.0f}% de los acarreos, zona roja "
            f"{sh.get('rz_carries', 0) * 100:.0f}%) = {td_rush:.2f}", None, "td"))
    if td_rec > 0.02:
        fac["tds"].insert(0, Factor(
            f"TD por recepción: {ent.pass_tds:.2f} esperados del equipo × {sh.get('td_rec', 0) * 100:.0f}% de cuota "
            f"(zona roja: {sh.get('rz_targets', 0) * 100:.0f}% de los envíos, a la zona de anotación "
            f"{sh.get('ez_targets', 0) * 100:.0f}%) = {td_rec:.2f}", None, "td"))
    fac["tds"].insert(0, Factor(f"{ent.team}: {ent.puntos:.1f} puntos esperados ({ent.puntos_fuente}) → "
                                f"{ent.tds:.2f} TD de ataque ({ent.rush_tds:.2f} por tierra, "
                                f"{ent.pass_tds:.2f} por aire)", None, "entorno"))
    medias["tds"], medias["rush_tds"], medias["rec_tds"] = lam["tds"], td_rush, td_rec

    # Jugada más larga: su media histórica escalada por el volumen esperado.
    for stat, col_vol, vol_esp in (("long_rec", "receptions", medias.get("rec", 0)),
                                   ("long_rush", "carries", carries),
                                   ("long_pass", "completions", medias.get("comp", 0))):
        hist = [p for p in j.partidos[:16] if (p.get(col_vol) or 0) > 0 and p.get(stat) is not None]
        if len(hist) >= 3 and vol_esp > 0.3:
            m = sum(p[stat] for p in hist) / len(hist)
            v_med = sum(p.get(col_vol) or 0 for p in hist) / len(hist)
            # Media condicionada a tocar el balón al menos una vez × probabilidad de tocarlo.
            medias[stat] = (m * (vol_esp / v_med) ** 0.3 if v_med else m) * (1 - math.exp(-vol_esp))

    # Fantasy: suma de sus componentes con la puntuación de las casas.
    medias["fantasy"] = (0.04 * medias.get("pass_yds", 0) + 4 * medias.get("pass_tds", 0) - medias.get("ints", 0)
                         + 0.1 * (medias.get("rush_yds", 0) + medias.get("rec_yds", 0)) + medias.get("rec", 0)
                         + 6 * lam["tds"])
    fac["fantasy"] = [Factor("puntuación: yardas de pase /25, TD de pase 4, intercepción -1, yardas de carrera y "
                             "recepción /10, recepción 1, TD 6", None, "volumen")]
    for stat, mu in medias.items():
        if stat in STATS_CONTEO:
            var[stat] = mu + 0.08 * mu * mu
        else:
            cv = _cv(ctx, j, stat)
            var[stat] = max(mu * 1.05, (cv * mu) ** 2)
    if "rush_rec_yds" in medias and "rush_yds" in var and "rec_yds" in var:
        var["rush_rec_yds"] = var["rush_yds"] + var["rec_yds"]
    if "pass_rush_yds" in medias and "rush_yds" in var:
        var["pass_rush_yds"] = var["pass_yds"] + var["rush_yds"]
    # Yardas por acarreo: media del partido con su desviación (menos acarreos = más variable).
    if carries >= 3 and "rush_yds" in medias:
        ypcs = [valor(p, "ypc") for p in j.partidos[:16] if (p.get("carries") or 0) >= 5]
        sd_emp = (sum((y - sum(ypcs) / len(ypcs)) ** 2 for y in ypcs) / (len(ypcs) - 1)) ** 0.5 \
            if len(ypcs) >= 4 else 2.4
        sd = math.sqrt((len(ypcs) * sd_emp ** 2 + 6 * 2.4 ** 2) / (len(ypcs) + 6)) * math.sqrt(14 / max(carries, 3))
        medias["ypc"], var["ypc"] = medias["rush_yds"] / carries, sd * sd
        fac["ypc"] = fac.get("rush_yds", [])[:3]
    for stat in ("rush_rec_yds", "pass_rush_yds"):
        if stat in medias:
            fac[stat] = fac.get("rush_yds", [])[:2] + fac.get("rec_yds" if stat == "rush_rec_yds" else "pass_yds", [])[:2]
    for nota in j.notas:
        for stat in medias:
            fac[stat].append(Factor(nota, None, "plantilla"))
    if duda < 1:
        for stat in medias:
            fac[stat].append(Factor(f"en duda ({j.estado}{f', {j.detalle_lesion}' if j.detalle_lesion else ''}): "
                                    f"volumen ×{DUDA}", DUDA, "lesion"))
    for stat in medias:
        fac[stat] += [f for f in ent.factores if f.tipo == "guion"]
    return Proyeccion(j, ent, medias, var, dict(fac), lam, vol)


def p_al_menos(lam: float, k: int) -> float:
    """P(X >= k) con la binomial negativa de los touchdowns."""
    if lam <= 0:
        return 0.0
    return max(0.0, 1.0 - cdf(k - 1, lam, lam + 0.08 * lam * lam))
