"""Modelo de props de la NHL por probabilidad (misma arquitectura que apuestas/nba/modelo.py).

Para cada jugador de campo y estadística:

    media = Σ (tasa por minuto × tiempo en hielo esperado) en igualdad y en power play
            × defensa rival por posición (delanteros / defensas) × tipo de defensa × portero rival (goles y puntos)

- Tiempo en hielo esperado: últimos 10 partidos con más peso a los recientes, aparte el de power play (el tiempo en
  power play de hoy sube o baja con los penaltis que suele cometer el rival).
- Tasas: toda la historia con decaimiento (la temporada anterior vale como mucho K_TEMPORADA_ANTERIOR partidos en
  cuanto hay partidos de esta), contraídas hacia la media de su posición; la de power play, aparte.
- Defensa rival por posición: lo que el rival concede por minuto a delanteros (F) o defensas (D).
- Portero rival (el probable de ESPN el día del partido): su % de paradas frente al de su equipo.

Porteros (paradas): tiros que genera el rival × tiros que concede su equipo / media de la liga × su % de paradas.

La distribución es binomial negativa (Poisson si no hay sobredispersión) con la dispersión del propio jugador más la
incertidumbre de su tiempo en hielo. La probabilidad final mezcla el modelo con su acierto real sobre esa línea en sus
últimos 15 partidos, calibrada por estadística con el backtest de 2025-26 (`nhl backtest`), y con la casa si hay
cuotas. Cada factor entró solo si mejoró el backtest (ver las constantes y el README).
"""
from __future__ import annotations

import math
import unicodedata
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date, timedelta

from ..model import negbin_pmf

COMPONENTES = {
    "shots": ("sog",), "points": ("g", "a"), "goals": ("g",), "assists": ("a",), "blocked": ("bs",),
    "hits": ("hits",), "saves": ("sv",),
}
NOMBRES = {"shots": "tiros a puerta", "points": "puntos", "goals": "goles", "assists": "asistencias",
           "blocked": "tiros bloqueados", "hits": "hits", "saves": "paradas"}
NOMBRE_COMP = {"sog": "tiros a puerta", "g": "goles", "a": "asistencias", "bs": "tiros bloqueados", "hits": "hits",
               "sv": "paradas", "pts": "puntos"}
BASICAS = ("sog", "g", "a", "bs", "hits")
DEFENSIVAS = BASICAS + ("pts",)       # "pts" (goles + asistencias) solo para explicar la defensa en puntos
CON_PP = ("sog", "g", "a")            # componentes con tasa propia en power play
GRUPOS_TEXTO = {"F": "delanteros", "D": "defensas", "G": "porteros"}

PESO_TEMPORADA_ANTERIOR = 0.5
K_TEMPORADA_ANTERIOR = 6.0
PESO_MERCADO_INICIO = 0.7
PARTIDOS_INICIO = 12
PESO_MERCADO = 0.4
PESO_MERCADO_TRASPASO = 0.7
DECAY_TASA = 0.97
DECAY_MINUTOS = 0.8
PARTIDOS_MINUTOS = 10
PESO_MINUTOS_ANTERIOR = 0.15
K_DEFENSA_MIN = 1500.0     # minutos "virtuales" de media de liga en la defensa por posición
K_TIPO_MIN = 600.0
K_PP_MIN = 8.0             # minutos virtuales de power play con la tasa de la liga
# Contracción hacia la media de su posición, en partidos "virtuales" con la tasa de la liga. Los goles y las
# asistencias son raros y ruidosos: sin contraerlos más, el backtest de 2025-26 esperaba 1.22 puntos de los mejores
# (hubo 1.06) y 0.21 de los que casi no anotan (hubo 0.27).
K_PRIOR = {"sog": 2.0, "g": 2.0, "a": 2.0, "bs": 2.0, "hits": 2.0}
# Goles = tiros × % de tiro: el % de tiro del jugador se contrae hacia el de la liga con K_TIRO_PCT tiros virtuales.
K_TIRO_PCT: float | None = None
PESO_MODELO = 0.75
# Calibración (contracción hacia 50 %) por estadística: backtest de 2025-26 (ver README, "NHL").
CALIBRACION = 0.9
CALIBRACION_STAT: dict[str, float] = {}
ESTADOS_FUERA = ("out", "injured reserve", "suspen", "doubtful")

# Factores del hockey. Cada uno con su backtest (2025-26); los que no mejoraron quedan en 0 / desactivados y solo
# se usan para explicar.
# % de paradas del portero rival de hoy frente al de su equipo (goles y asistencias). Backtest 2025-26: log-loss de
# puntos 0.6150 con él y 0.6154 sin él, asistencias 0.5464 / 0.5467, goles 0.4183 / 0.4184 (pequeño pero en las tres).
USAR_PORTERO = True
K_PORTERO_TIROS = 900.0    # tiros virtuales con el % de paradas de la liga
PESO_PORTERO = 1.0
# Penaltis que comete el rival -> tiempo en power play de hoy. Backtest 2025-26: no mejoró (log-loss 0.5735 con él,
# 0.5734 sin él; tiros a puerta 0.6301 frente a 0.6300): queda solo como explicación en "En corto".
USAR_PENALTIS = False
K_PENALTIS = 15            # partidos virtuales con la media de la liga
PESO_PENALTIS = 1.0
# Segundo partido en dos noches (backtest 2025-26, ~4.000 jugadores en cada caso, real / esperado frente a los partidos
# sin cansancio): su equipo cansado, -2 % de tiros y -4 % de puntos; el rival cansado, +5.5 % de tiros, +3 % de puntos
# y -5.5 % de tiros bloqueados (su equipo ataca más). Si los dos jugaron anoche, se compensan.
USAR_B2B = True
B2B_PROPIO = {"sog": -0.022, "g": -0.04, "a": -0.04}
B2B_RIVAL = {"sog": 0.055, "g": 0.033, "a": 0.033, "bs": -0.055}
# Diferencia esperada (goles): los favoritos tiran algo más y bloquean menos (2025-26: +2.8 % de tiros y -5.5 % de
# bloqueados por gol de ventaja esperada; en puntos, sin efecto claro).
USAR_MARGEN = True
MARGEN_EFECTO = {"sog": 0.028, "bs": -0.055}
MARGEN_TOPE = 1.5
# Corrección de la media por estadística: en el backtest de 2025-26 el modelo esperaba un 2-2.5 % más de tiros, tiros
# bloqueados y hits de los que hubo (con el tiempo en hielo bien previsto: real / esperado 0.999).
SESGO = {"sog": 0.98, "bs": 0.976, "hits": 0.975}


def cdf(k: int, mu: float, var: float) -> float:
    if k < 0:
        return 0.0
    return min(1.0, sum(negbin_pmf(i, mu, var) for i in range(k + 1)))


def prob_lados(line: float, mu: float, var: float) -> tuple[float, float]:
    """P(más de la línea), P(menos de la línea)."""
    if mu <= 0:
        return 0.0, 1.0
    over = 1.0 - cdf(math.floor(line), mu, var)
    under = cdf(math.ceil(line) - 1, mu, var)
    return max(0.0, over), max(0.0, under)


def valor(p: dict, stat: str) -> float:
    return sum(p.get(c) or 0 for c in COMPONENTES[stat])


def _peso_temporada(season: int, actual: int) -> float:
    return 1.0 if season == actual else PESO_TEMPORADA_ANTERIOR


# --- Contexto de liga -----------------------------------------------------------------

@dataclass
class Contexto:
    fecha: str
    temporada: int
    filas: list[dict]
    por_jugador: dict[str, list[dict]]
    grupo: dict[str, str]
    liga: dict[str, dict[str, float]]           # grupo -> comp -> por minuto (total)
    liga_pp: dict[str, dict[str, float]]        # grupo -> comp -> por minuto de power play
    defensa: dict[str, dict[str, dict[str, float]]]
    nivel: dict[str, dict[str, dict[str, str]]]
    ultimo_partido: dict[str, str]
    partidos_equipo: dict[str, list[str]]       # equipo -> fechas de sus partidos (recientes primero)
    porteros: dict[str, list[dict]]             # portero -> sus partidos como titular (recientes primero)
    sv_portero: dict[str, float]                # % de paradas contraído a la liga
    sv_equipo: dict[str, float]                 # % de paradas de los porteros de cada equipo esta temporada
    sv_liga: float
    tiros_equipo: dict[str, dict[str, float]]   # equipo -> {"a_favor", "en_contra", "intentos_contra", "pen", ...}
    tiros_liga: float
    penaltis_liga: float
    intentos: dict[str, dict[str, int]] = field(default_factory=dict)   # jugador -> partido -> intentos de tiro
    tipos: dict[str, dict[str, int]] = field(default_factory=dict)      # jugador -> tipo de tiro -> tiros (temporada)
    distancia: dict[str, float] = field(default_factory=dict)           # jugador -> distancia media de sus tiros
    margen: dict[str, float] = field(default_factory=dict)              # equipo -> goles de diferencia esperados hoy
    portero_hoy: dict[str, str] = field(default_factory=dict)           # equipo -> portero titular de hoy
    margen_partido: dict[tuple[str, str], int] = field(default_factory=dict)   # (partido, equipo) -> diferencia
    siglas: dict[str, str] = field(default_factory=dict)
    nombres_porteros: dict[str, str] = field(default_factory=dict)


def construir_contexto(conn, fecha: str, dias: int = 420) -> Contexto:
    desde = (date.fromisoformat(fecha) - timedelta(days=dias)).isoformat()
    filas = [dict(r) for r in conn.execute(
        """SELECT pg.*, g.fecha, g.season FROM nhl_player_games pg JOIN nhl_games g ON g.id = pg.game_id
           WHERE g.fecha < ? AND g.fecha >= ? AND g.season_type IN (2, 3) ORDER BY g.fecha DESC, g.id""",
        (fecha, desde))]
    # Goles y asistencias en power play (de la jugada a jugada).
    pp: dict[tuple[str, str], list[int]] = defaultdict(lambda: [0, 0])
    for r in conn.execute(
            """SELECT go.game_id, go.scorer_id, go.a1_id, go.a2_id FROM nhl_goals go JOIN nhl_games g ON g.id = go.game_id
               WHERE go.strength = 'PP' AND g.fecha < ? AND g.fecha >= ?""", (fecha, desde)):
        pp[(r[0], r[1])][0] += 1
        for a in (r[2], r[3]):
            if a:
                pp[(r[0], a)][1] += 1
    temporada = max((f["season"] for f in filas), default=0)
    por_jugador: dict[str, list[dict]] = defaultdict(list)
    grupo: dict[str, str] = {}
    for f in filas:
        f["pp_g"], f["pp_a"] = pp.get((f["game_id"], f["player_id"]), (0, 0))
        f["pp_sog"] = f.get("pp_sog") or 0
        por_jugador[f["player_id"]].append(f)
        grupo.setdefault(f["player_id"], f["grupo"] or "F")

    tot = defaultdict(lambda: defaultdict(float))
    conc = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
    for f in filas:
        w = _peso_temporada(f["season"], temporada)
        g = grupo[f["player_id"]]
        tot[g]["min"] += w * f["toi"]
        tot[g]["pp_min"] += w * (f["pptoi"] or 0)
        conc[f["opp_id"]][g]["min"] += w * f["toi"]
        f["pts"] = (f["g"] or 0) + (f["a"] or 0)
        for s in DEFENSIVAS:
            tot[g][s] += w * (f[s] or 0)
            conc[f["opp_id"]][g][s] += w * (f[s] or 0)
        for s in CON_PP:
            tot[g]["pp_" + s] += w * (f["pp_" + s] or 0)
    liga = {g: {s: (d[s] / d["min"] if d["min"] else 0.0) for s in DEFENSIVAS} for g, d in tot.items()}
    liga_pp = {g: {s: (d["pp_" + s] / d["pp_min"] if d["pp_min"] else 0.0) for s in CON_PP} for g, d in tot.items()}
    defensa: dict = {}
    for team, por_g in conc.items():
        defensa[team] = {}
        for g, d in por_g.items():
            defensa[team][g] = {}
            for s in DEFENSIVAS:
                lg = liga.get(g, {}).get(s, 0.0)
                tasa = (d[s] + K_DEFENSA_MIN * lg) / (d["min"] + K_DEFENSA_MIN)
                defensa[team][g][s] = tasa / lg if lg else 1.0
    nivel: dict = defaultdict(dict)
    for g in liga:
        for s in DEFENSIVAS:
            orden = sorted((t for t in defensa if g in defensa[t]), key=lambda t: defensa[t][g][s])
            n = len(orden)
            nivel[g][s] = {t: ("fuerte" if i < n / 3 else "media" if i < 2 * n / 3 else "débil")
                           for i, t in enumerate(orden)}

    ultimo: dict[str, str] = {}
    partidos_equipo: dict[str, list[str]] = defaultdict(list)
    vistos = set()
    for f in filas:
        ultimo.setdefault(f["team_id"], f["fecha"])
        if (f["game_id"], f["team_id"]) not in vistos:
            vistos.add((f["game_id"], f["team_id"]))
            partidos_equipo[f["team_id"]].append(f["fecha"])

    # Porteros.
    gfilas = [dict(r) for r in conn.execute(
        """SELECT gg.*, g.fecha, g.season FROM nhl_goalie_games gg JOIN nhl_games g ON g.id = gg.game_id
           WHERE g.fecha < ? AND g.fecha >= ? AND g.season_type IN (2, 3) ORDER BY g.fecha DESC""", (fecha, desde))]
    porteros: dict[str, list[dict]] = defaultdict(list)
    nombres_porteros: dict[str, str] = {}
    acc_p = defaultdict(lambda: [0.0, 0.0])
    acc_e = defaultdict(lambda: [0.0, 0.0])
    liga_sa = liga_sv = 0.0
    for r in gfilas:
        nombres_porteros.setdefault(r["player_id"], r["name"])
        if r["starter"] and r["toi"] >= 40:
            porteros[r["player_id"]].append(r)
        w = _peso_temporada(r["season"], temporada)
        acc_p[r["player_id"]][0] += w * r["sa"]
        acc_p[r["player_id"]][1] += w * r["sv"]
        if r["season"] == temporada:
            acc_e[r["team_id"]][0] += r["sa"]
            acc_e[r["team_id"]][1] += r["sv"]
        liga_sa += w * r["sa"]
        liga_sv += w * r["sv"]
    sv_liga = liga_sv / liga_sa if liga_sa else 0.9
    sv_portero = {p: (v[1] + K_PORTERO_TIROS * sv_liga) / (v[0] + K_PORTERO_TIROS) for p, v in acc_p.items()}
    sv_equipo = {t: (v[1] + K_PORTERO_TIROS * sv_liga) / (v[0] + K_PORTERO_TIROS) for t, v in acc_e.items()}

    # Totales de equipo de esta temporada: tiros a favor y en contra, intentos en contra y penaltis.
    eq = defaultdict(lambda: defaultdict(float))
    goles_partido: dict[tuple[str, str], int] = defaultdict(int)
    por_partido_eq = defaultdict(lambda: defaultdict(float))
    for f in filas:
        clave = (f["game_id"], f["team_id"])
        por_partido_eq[clave]["sog"] += f["sog"] or 0
        por_partido_eq[clave]["g"] += f["g"] or 0
        por_partido_eq[clave]["bs"] += f["bs"] or 0
        por_partido_eq[clave]["missed"] += f["missed"] or 0
        por_partido_eq[clave]["pim"] += f["pim"] or 0
        por_partido_eq[clave]["pptoi"] = max(por_partido_eq[clave]["pptoi"], f["pptoi"] or 0)
        por_partido_eq[clave]["season"] = f["season"]
        por_partido_eq[clave]["opp"] = f["opp_id"]
    margen_partido = {}
    for (gid, team), d in por_partido_eq.items():
        rival = por_partido_eq.get((gid, d["opp"]))
        if rival is None:
            continue
        margen_partido[(gid, team)] = int(d["g"] - rival["g"])
        if d["season"] != temporada:
            continue
        e = eq[team]
        e["n"] += 1
        e["a_favor"] += d["sog"]
        e["en_contra"] += rival["sog"]
        # Intentos del rival = a puerta + fuera + los que bloqueó este equipo.
        e["intentos_contra"] += rival["sog"] + rival["missed"] + d["bs"]
        e["intentos_favor"] += d["sog"] + d["missed"] + rival["bs"]
        e["pp_rival"] += rival["pptoi"]    # minutos de power play que le dio al rival (penaltis que comete)
        e["goles_favor"] += d["g"]
        e["goles_contra"] += rival["g"]
    tiros_equipo = {t: {k: v / e["n"] for k, v in e.items() if k != "n"} | {"n": e["n"]}
                    for t, e in eq.items() if e["n"]}
    tiros_liga = (sum(v["a_favor"] for v in tiros_equipo.values()) / len(tiros_equipo)) if tiros_equipo else 28.0
    penaltis_liga = (sum(v["pp_rival"] for v in tiros_equipo.values()) / len(tiros_equipo)) if tiros_equipo else 5.0

    # Intentos de tiro por jugador y partido, tipo de tiro y distancia (jugada a jugada).
    intentos: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    tipos: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    dist = defaultdict(lambda: [0.0, 0])
    for r in conn.execute(
            """SELECT s.player_id, s.game_id, s.shot_type, s.dist, s.result, g.season FROM nhl_shots s
               JOIN nhl_games g ON g.id = s.game_id WHERE g.fecha < ? AND g.fecha >= ?""", (fecha, desde)):
        intentos[r[0]][r[1]] += 1
        if r[5] == temporada and r[4] in ("sog", "goal"):
            if r[2]:
                tipos[r[0]][r[2]] += 1
            if r[3] is not None:
                dist[r[0]][0] += r[3]
                dist[r[0]][1] += 1
    ctx = Contexto(fecha, temporada, filas, por_jugador, grupo, liga, liga_pp, defensa, nivel, ultimo,
                   partidos_equipo, porteros, sv_portero, sv_equipo, sv_liga, tiros_equipo, tiros_liga, penaltis_liga,
                   intentos, tipos, {p: v[0] / v[1] for p, v in dist.items() if v[1] >= 10})
    ctx.margen_partido = margen_partido
    ctx.nombres_porteros = nombres_porteros
    ctx.margen = _margenes(conn, fecha, temporada, tiros_equipo)
    ctx.portero_hoy = _porteros_hoy(conn, fecha)
    try:
        ctx.siglas = {r[0]: r[1] for r in conn.execute("SELECT id, abbr FROM nhl_teams")}
    except Exception:
        ctx.siglas = {}
    return ctx


LOCALIA = 0.15      # goles de ventaja del local (2025-26: ~0.1-0.2)
K_MARGEN = 10


def _margenes(conn, fecha: str, temporada: int, tiros_equipo: dict) -> dict[str, float]:
    """Goles de diferencia esperados hoy: los de la casa (ESPN) o, si no hay, la diferencia de goles de cada equipo
    esta temporada (encogida con K_MARGEN partidos de 0) más la ventaja del local."""
    out = {}
    for local, visita, casa in conn.execute(
            "SELECT home_id, away_id, margen_esperado FROM nhl_games WHERE fecha = ?", (fecha,)).fetchall():
        def neto(t):
            e = tiros_equipo.get(t)
            if not e:
                return 0.0
            return (e["goles_favor"] - e["goles_contra"]) * e["n"] / (e["n"] + K_MARGEN)
        m = casa if casa is not None else neto(local) - neto(visita) + LOCALIA
        out[local], out[visita] = m, -m
    return out


def _porteros_hoy(conn, fecha: str) -> dict[str, str]:
    out = {}
    for local, visita, pl, pv in conn.execute(
            "SELECT home_id, away_id, home_goalie_id, away_goalie_id FROM nhl_games WHERE fecha = ?", (fecha,)):
        if pl:
            out[local] = pl
        if pv:
            out[visita] = pv
    return out


# --- Jugador --------------------------------------------------------------------------

@dataclass
class Prediccion:
    stat: str
    mu: float
    var: float
    factores: dict[str, float] = field(default_factory=dict)


@dataclass
class Jugador:
    player_id: str
    nombre: str
    team_id: str
    opp_id: str
    grupo: str
    partidos: list[dict]
    minutos: float           # tiempo en hielo esperado
    minutos_sd: float
    minutos_pp: float = 0.0  # de ellos, en power play
    notas: list[str] = field(default_factory=list)
    pocos_con_equipo: bool = False
    cambio_pp: str | None = None
    cambio_linea: float | None = None     # tiempo en igualdad de los últimos 3 / el de antes
    vuelve: int = 0                       # partidos de su equipo que se perdió justo antes de hoy
    factor_penaltis: float = 1.0
    factor_portero: float = 1.0
    portero_rival: str | None = None
    b2b: bool = False
    rival_b2b: bool = False
    bajas_rival: list[str] = field(default_factory=list)
    bajas_equipo: list[str] = field(default_factory=list)
    es_portero: bool = False

    @property
    def n(self) -> int:
        return len(self.partidos)


ROL_MIN = {"F": 14.0, "D": 17.0}       # tiempo en hielo de los últimos 5 para no ser "papel menor"
TOI_SD_ESTABLE = 3.5
BAJA_TOI = {"F": 16.0, "D": 20.0}       # compañero o rival "importante" (top 6 / top 4)


def _pesos(partidos: list[dict], temporada: int, decay: float) -> list[float]:
    w = [decay ** i * _peso_temporada(p["season"], temporada) for i, p in enumerate(partidos)]
    if K_TEMPORADA_ANTERIOR is not None and partidos and partidos[0]["season"] == temporada:
        previos = sum(wi for wi, p in zip(w, partidos) if p["season"] != temporada)
        if previos > K_TEMPORADA_ANTERIOR:
            f = K_TEMPORADA_ANTERIOR / previos
            w = [wi * f if p["season"] != temporada else wi for wi, p in zip(w, partidos)]
    return w


def _media_ponderada(partidos: list[dict], campo: str, temporada: int) -> tuple[float, float]:
    hay_actual = bool(partidos) and partidos[0]["season"] == temporada
    w = [DECAY_MINUTOS ** i * (1.0 if p["season"] == temporada or not hay_actual else PESO_MINUTOS_ANTERIOR)
         for i, p in enumerate(partidos)]
    m = sum(wi * (p[campo] or 0) for wi, p in zip(w, partidos)) / sum(w)
    var = sum(wi * ((p[campo] or 0) - m) ** 2 for wi, p in zip(w, partidos)) / sum(w)
    return m, math.sqrt(var)


def preparar_jugador(ctx: Contexto, player_id: str, nombre: str, team_id: str, opp_id: str,
                     ausentes: list[str] | None = None, fuera_rival: list[str] | None = None) -> Jugador | None:
    partidos = ctx.por_jugador.get(player_id, [])[:100]
    if not partidos:
        return None
    recientes = partidos[:PARTIDOS_MINUTOS]
    m, sd = _media_ponderada(recientes, "toi", ctx.temporada)
    m_pp, _ = _media_ponderada(recientes, "pptoi", ctx.temporada)
    j = Jugador(player_id, nombre, team_id, opp_id, ctx.grupo.get(player_id, "F"), partidos, m, max(1.5, sd), m_pp)
    con_equipo = [p for p in partidos if p["team_id"] == team_id and p["season"] == ctx.temporada]
    j.pocos_con_equipo = len(con_equipo) < 3 and any(p["team_id"] != team_id for p in partidos[:15])
    if j.pocos_con_equipo:
        j.notas.append(f"solo {len(con_equipo)} partidos con su equipo actual: su rol puede haber cambiado")
    # Cambio de unidad de power play: tiempo en PP de los últimos 3 frente a los 10 anteriores.
    ult3, antes = partidos[:3], partidos[3:13]
    if len(ult3) == 3 and len(antes) >= 5:
        pp3 = sum(p["pptoi"] or 0 for p in ult3) / 3
        pp_antes = sum(p["pptoi"] or 0 for p in antes) / len(antes)
        if pp_antes >= 1.5 and pp3 < 0.5 * pp_antes:
            j.cambio_pp = f"bajó de unidad de power play ({pp_antes:.1f} min por partido antes, {pp3:.1f} ahora)"
        elif pp_antes < 0.8 and pp3 >= 1.8:
            j.cambio_pp = f"subió a la unidad de power play ({pp_antes:.1f} min antes, {pp3:.1f} ahora)"
        if j.cambio_pp:
            j.notas.append(j.cambio_pp)
        es3 = sum((p["toi"] or 0) - (p["pptoi"] or 0) for p in ult3) / 3
        es_antes = sum((p["toi"] or 0) - (p["pptoi"] or 0) for p in antes) / len(antes)
        if es_antes:
            j.cambio_linea = es3 / es_antes
            if abs(j.cambio_linea - 1) >= 0.2:
                j.notas.append(f"cambio de línea o de rol: {es3:.1f} min en igualdad en sus últimos 3 frente a "
                               f"{es_antes:.1f} antes")
    # Vuelve de lesión o de no jugar: partidos de su equipo entre su último partido y hoy.
    fechas = ctx.partidos_equipo.get(team_id, [])
    j.vuelve = sum(1 for f in fechas if f > partidos[0]["fecha"])
    if j.vuelve >= 3:
        j.notas.append(f"vuelve tras {j.vuelve} partidos de su equipo sin jugar")
    ayer = (date.fromisoformat(ctx.fecha) - timedelta(days=1)).isoformat()
    j.b2b = ctx.ultimo_partido.get(team_id) == ayer
    j.rival_b2b = ctx.ultimo_partido.get(opp_id) == ayer
    if j.b2b and not j.rival_b2b:
        j.notas.append("segundo partido en dos noches (el rival descansó)")
    elif j.rival_b2b and not j.b2b:
        j.notas.append("el rival juega el segundo partido en dos noches")
    # Penaltis del rival: más (o menos) power play hoy.
    if USAR_PENALTIS and opp_id in ctx.tiros_equipo and ctx.penaltis_liga:
        e = ctx.tiros_equipo[opp_id]
        rel = 1 + (e["pp_rival"] / ctx.penaltis_liga - 1) * e["n"] / (e["n"] + K_PENALTIS)
        j.factor_penaltis = 1 + (rel - 1) * PESO_PENALTIS
    # Portero rival de hoy frente al promedio de su equipo.
    pr = ctx.portero_hoy.get(opp_id)
    if pr:
        j.portero_rival = pr
        if USAR_PORTERO and pr in ctx.sv_portero and opp_id in ctx.sv_equipo:
            f = (1 - ctx.sv_portero[pr]) / max(1e-3, 1 - ctx.sv_equipo[opp_id])
            j.factor_portero = 1 + (min(1.3, max(0.75, f)) - 1) * PESO_PORTERO
    hace_15 = (date.fromisoformat(ctx.fecha) - timedelta(days=15)).isoformat()
    for lista, ids in ((j.bajas_rival, fuera_rival or ()), (j.bajas_equipo, ausentes or ())):
        for pid in ids:
            rec = ctx.por_jugador.get(pid, [])[:10]
            if rec and rec[0]["fecha"] >= hace_15:
                g = ctx.grupo.get(pid, "F")
                if sum(p["toi"] for p in rec) / len(rec) >= BAJA_TOI.get(g, 16):
                    lista.append(rec[0]["name"])
    return j


def preparar_portero(ctx: Contexto, player_id: str, nombre: str, team_id: str, opp_id: str) -> Jugador | None:
    partidos = ctx.porteros.get(player_id, [])[:60]
    if not partidos:
        return None
    j = Jugador(player_id, nombre, team_id, opp_id, "G", partidos, 58.0, 4.0, es_portero=True)
    con_equipo = [p for p in partidos if p["team_id"] == team_id and p["season"] == ctx.temporada]
    j.pocos_con_equipo = len(con_equipo) < 3 and any(p["team_id"] != team_id for p in partidos[:15])
    fechas = ctx.partidos_equipo.get(team_id, [])
    j.vuelve = sum(1 for f in fechas[:10] if f > partidos[0]["fecha"])
    ayer = (date.fromisoformat(ctx.fecha) - timedelta(days=1)).isoformat()
    j.b2b = ctx.ultimo_partido.get(team_id) == ayer
    j.rival_b2b = ctx.ultimo_partido.get(opp_id) == ayer
    return j


# --- Predicción -----------------------------------------------------------------------

def tiros_esperados_contra(ctx: Contexto, team_id: str, opp_id: str) -> float:
    """Tiros a puerta que se esperan del rival: los que genera × los que concede este equipo / media de la liga."""
    a = ctx.tiros_equipo.get(opp_id, {})
    b = ctx.tiros_equipo.get(team_id, {})
    lg = ctx.tiros_liga or 28.0

    def enc(v, n):
        return (v * n + lg * 8) / (n + 8) if v else lg
    genera = enc(a.get("a_favor"), a.get("n", 0))
    concede = enc(b.get("en_contra"), b.get("n", 0))
    return genera * concede / lg


def _predecir_paradas(ctx: Contexto, j: Jugador) -> Prediccion:
    sa = tiros_esperados_contra(ctx, j.team_id, j.opp_id)
    sv = ctx.sv_portero.get(j.player_id, ctx.sv_liga)
    mu = sa * sv * 0.97     # a veces lo cambian antes de terminar
    ult = j.partidos[:20]
    media = sum(p["sv"] for p in ult) / len(ult)
    var_emp = sum((p["sv"] - media) ** 2 for p in ult) / len(ult) if len(ult) > 3 else mu
    phi = min(3.0, max(1.0, var_emp / max(1.0, media)))
    return Prediccion("saves", mu, phi * mu, {"minutos": 60.0, "tiros_contra": sa, "sv": sv, "dispersion": phi,
                                              "rival": sa / (ctx.tiros_liga or 28.0), "tipo_defensa": 1.0})


def predecir(ctx: Contexto, j: Jugador, stat: str) -> Prediccion:
    if j.es_portero:
        return _predecir_paradas(ctx, j)
    w = _pesos(j.partidos, ctx.temporada, DECAY_TASA)
    sw_min = sum(wi * p["toi"] for wi, p in zip(w, j.partidos))
    sw_pp = sum(wi * (p["pptoi"] or 0) for wi, p in zip(w, j.partidos))
    m_media = sw_min / sum(w)
    liga = ctx.liga.get(j.grupo, {})
    liga_pp = ctx.liga_pp.get(j.grupo, {})
    defensa = ctx.defensa.get(j.opp_id, {}).get(j.grupo, {})
    niveles = ctx.nivel.get(j.grupo, {})
    m_pp = j.minutos_pp * j.factor_penaltis
    m_resto = max(0.0, j.minutos - j.minutos_pp)
    mu = 0.0
    tasa_base = 0.0
    fac_rival = fac_tipo = tot = 0.0
    for c in COMPONENTES[stat]:
        if c in CON_PP:
            # Igualdad (y inferioridad) y power play por separado.
            resto = sum(wi * ((p[c] or 0) - (p["pp_" + c] or 0)) for wi, p in zip(w, j.partidos))
            pp = sum(wi * (p["pp_" + c] or 0) for wi, p in zip(w, j.partidos))
            lg_total = liga.get(c, 0.0)
            lg_pp = liga_pp.get(c, 0.0)
            lg_resto = lg_total   # aproximación: la tasa de liga total (la de igualdad es algo menor)
            k = K_PRIOR.get(c, 2.0)
            t_resto = (resto + k * m_media * lg_resto) / (sw_min - sw_pp + k * m_media)
            t_pp = (pp + K_PP_MIN * k / 2 * lg_pp) / (sw_pp + K_PP_MIN * k / 2)
            mu_c = t_resto * m_resto + t_pp * m_pp
            base_c = (t_resto * m_resto + t_pp * j.minutos_pp) / j.minutos if j.minutos else 0.0
        else:
            k = K_PRIOR.get(c, 2.0)
            tasa = (sum(wi * (p[c] or 0) for wi, p in zip(w, j.partidos)) + k * m_media * liga.get(c, 0.0)) / (
                sw_min + k * m_media)
            mu_c = tasa * j.minutos
            base_c = tasa
        if c == "g" and K_TIRO_PCT:
            # % de tiro contraído: sus goles / sus tiros frente al de la liga de su posición.
            tiros = sum(wi * (p["sog"] or 0) for wi, p in zip(w, j.partidos))
            goles = sum(wi * (p["g"] or 0) for wi, p in zip(w, j.partidos))
            lg_sh = liga.get("g", 0.0) / liga["sog"] if liga.get("sog") else 0.1
            if tiros and goles:
                f_sh = ((goles + K_TIRO_PCT * lg_sh) / (tiros + K_TIRO_PCT)) / (goles / tiros)
                mu_c *= f_sh
                base_c *= f_sh
        tasa_base += base_c
        f_def = defensa.get(c, 1.0)
        nivel_hoy = niveles.get(c, {}).get(j.opp_id)
        f_tipo = 1.0
        if nivel_hoy and base_c:
            mismos = [(wi, p) for wi, p in zip(w, j.partidos) if niveles[c].get(p["opp_id"]) == nivel_hoy]
            m_t = sum(wi * p["toi"] for wi, p in mismos)
            if m_t:
                t_t = sum(wi * (p[c] or 0) for wi, p in mismos) / m_t
                f_tipo = math.sqrt(1 + (t_t / base_c - 1) * m_t / (m_t + K_TIPO_MIN))
                f_tipo = min(1.15, max(0.85, f_tipo))
        mu_c *= f_def * f_tipo
        if c in ("g", "a"):
            mu_c *= j.factor_portero
        mu_c *= SESGO.get(c, 1.0)
        if USAR_B2B and j.b2b != j.rival_b2b:
            mu_c *= 1 + (B2B_PROPIO if j.b2b else B2B_RIVAL).get(c, 0.0)
        if USAR_MARGEN and c in MARGEN_EFECTO and ctx.margen.get(j.team_id) is not None:
            mu_c *= 1 + MARGEN_EFECTO[c] * max(-MARGEN_TOPE, min(MARGEN_TOPE, ctx.margen[j.team_id]))
        mu += mu_c
        tot += base_c
        fac_rival += base_c * f_def
        fac_tipo += base_c * f_tipo
    num = den = 0.0
    for wi, p in zip(w, j.partidos):
        e = tasa_base * p["toi"]
        num += wi * (valor(p, stat) - e) ** 2
        den += wi * e
    phi = min(3.0, max(1.0, num / den)) if den else 1.0
    tasa_min = mu / j.minutos if j.minutos else 0.0
    var = phi * mu + tasa_min ** 2 * j.minutos_sd ** 2
    return Prediccion(stat, mu, var, {
        "minutos": j.minutos, "minutos_pp": m_pp, "tasa_min": tasa_min, "dispersion": phi,
        "rival": fac_rival / tot if tot else 1.0, "tipo_defensa": fac_tipo / tot if tot else 1.0,
        "portero": j.factor_portero, "penaltis": j.factor_penaltis})


# --- Evaluación de una línea ----------------------------------------------------------

@dataclass
class Evaluacion:
    player_id: str
    nombre: str
    stat: str
    line: float
    lado: str
    prob: float
    prob_modelo: float
    prob_mercado: float | None
    mu: float
    sd: float
    acierto_10: tuple[int, int]
    acierto_temporada: tuple[int, int]
    vs_rival: list[float]
    media_10: float
    odd: float | None
    factores: dict
    titular: bool = True
    alertas: list = field(default_factory=list)
    defensa: str = ""
    argumentos: list = field(default_factory=list)
    estimada: bool = False                      # línea estimada (sin línea de la casa)
    team_id: str = ""


def _aciertos(partidos: list[dict], stat: str, line: float, lado: str) -> tuple[int, int]:
    hits = sum((valor(p, stat) > line) if lado == "más" else (valor(p, stat) < line) for p in partidos)
    return hits, len(partidos)


MARGEN_UN_LADO = 1.05


def prob_mercado(over_odd: float | None, under_odd: float | None) -> tuple[float | None, float | None]:
    if over_odd and under_odd:
        o, u = 1 / over_odd, 1 / under_odd
        return o / (o + u), u / (o + u)
    return (1 / over_odd / MARGEN_UN_LADO if over_odd else None,
            1 / under_odd / MARGEN_UN_LADO if under_odd else None)


def _prob_jugador(j: Jugador, stat: str, line: float, lado: str, p_mod: float) -> float:
    hits, n = _aciertos(j.partidos[:15], stat, line, lado)
    p_emp = (hits + 5 * p_mod) / (n + 5)
    return 0.5 + (PESO_MODELO * p_mod + (1 - PESO_MODELO) * p_emp - 0.5) * CALIBRACION_STAT.get(stat, CALIBRACION)


DISCREPANCIA_MAX = 0.25
VETADOS: set[tuple[str, str]] = set()


def vetada(nombre: str, stat: str) -> bool:
    clave = "".join(ch for ch in unicodedata.normalize("NFKD", nombre.lower()) if ch.isalnum())
    return (clave, stat) in VETADOS


def es_titular(j: Jugador) -> bool:
    """Papel principal: tiempo en hielo de top 9 (delanteros) o top 4 (defensas) en sus últimos 5."""
    if j.es_portero:
        return True
    ult = j.partidos[:5]
    return sum(p["toi"] for p in ult) / len(ult) >= ROL_MIN.get(j.grupo, 14.0)


def alertas(ctx: Contexto, j: Jugador, stat: str) -> list[str]:
    out = ["vetada por el usuario"] if vetada(j.nombre, stat) else []
    if j.es_portero:
        if ctx.portero_hoy.get(j.team_id) != j.player_id:
            out.append("portero no confirmado")
    else:
        if not es_titular(j):
            out.append("papel menor")
        if j.minutos_sd > TOI_SD_ESTABLE:
            out.append("tiempo en hielo inestable")
        if j.cambio_pp:
            out.append("cambio de unidad de PP")
        if j.cambio_linea is not None and abs(j.cambio_linea - 1) >= 0.2:
            out.append("cambio de línea o de rol")
    if j.pocos_con_equipo:
        out.append("traspaso reciente")
    if j.vuelve >= 3:
        out.append("vuelve de lesión")
    if any(n.startswith("en el parte de lesiones") for n in j.notas):
        out.append("en el parte de lesiones")
    return out


def _motivo_fallo(ctx: Contexto, j: Jugador, p: dict) -> str | None:
    if j.es_portero:
        if p["toi"] < 50:
            return f"lo cambiaron (jugó {p['toi']:.0f} min)"
        return None
    if p["toi"] < j.minutos - 4:
        return f"jugó {p['toi']:.0f} min"
    m = ctx.margen_partido.get((p["game_id"], p["team_id"]))
    if m is not None and abs(m) >= 4:
        return f"paliza de {abs(m)}"
    return None


FALLOS_NORMALES_MAX = 0.3
FALLOS_NORMALES_MIN_PARTIDOS = 5


def _falla_en_normales(ctx: Contexto, j: Jugador, stat: str, line: float) -> list[str]:
    temp = [p for p in j.partidos if p["season"] == ctx.temporada]
    if len(temp) < FALLOS_NORMALES_MIN_PARTIDOS:
        return []
    malos = [p for p in temp if valor(p, stat) >= line and not _motivo_fallo(ctx, j, p)]
    if len(malos) / len(temp) < FALLOS_NORMALES_MAX:
        return []
    return [f"falla en partidos normales ({len(malos)} de {len(temp)} esta temporada)"]


def _puesto(valores: dict[str, float], equipo: str) -> int | None:
    if equipo not in valores:
        return None
    return sorted(valores, key=lambda t: -valores[t]).index(equipo) + 1


def _equipos(ctx: Contexto) -> set[str]:
    return set(ctx.tiros_equipo)


def _comp_defensa(stat: str) -> str:
    return "pts" if stat == "points" else COMPONENTES[stat][0]


def texto_defensa(ctx: Contexto, j: Jugador, stat: str, pred: Prediccion) -> str:
    if j.es_portero:
        return (f"se esperan {pred.factores['tiros_contra']:.1f} tiros a puerta del rival (media de la liga "
                f"{ctx.tiros_liga:.1f}); su % de paradas {pred.factores['sv'] * 100:.1f}%")
    c = _comp_defensa(stat)
    nivel = ctx.nivel.get(j.grupo, {}).get(c, {}).get(j.opp_id, "media")
    rel = ctx.defensa.get(j.opp_id, {}).get(j.grupo, {}).get(c, 1.0) - 1
    return (f"el rival concede {rel * 100:+.0f}% de {NOMBRE_COMP[c]} por minuto a {GRUPOS_TEXTO[j.grupo]} "
            f"(defensa {nivel})")


def argumentos(ctx: Contexto, j: Jugador, stat: str, line: float, lado: str, pred: Prediccion) -> list[str]:
    """Lo esencial de cada pata en datos concretos, al estilo de un analista ("En corto")."""
    out = []
    pasa = (lambda v: v > line) if lado == "más" else (lambda v: v < line)
    temp = [p for p in j.partidos if p["season"] == ctx.temporada]
    equipos = _equipos(ctx)
    if temp:
        fallos = [p for p in temp if not pasa(valor(p, stat))]
        texto = f"La pasó en {len(temp) - len(fallos)} de {len(temp)} esta temporada"
        motivos = [_motivo_fallo(ctx, j, p) for p in fallos]
        if fallos and all(motivos):
            texto += f"; los fallos, en partidos raros ({', '.join(motivos[:5])})"
        elif fallos:
            texto += f" (falló con {', '.join(f'{valor(p, stat):g}' for p in fallos[:5])})"
        out.append(texto)
    if j.es_portero:
        sa = pred.factores["tiros_contra"]
        genera = {t: v["a_favor"] for t, v in ctx.tiros_equipo.items()}
        concede = {t: v["en_contra"] for t, v in ctx.tiros_equipo.items()}
        if j.opp_id in genera:
            out.append(f"El rival es #{_puesto(genera, j.opp_id)} de {len(genera)} en tiros a puerta por partido "
                       f"({genera[j.opp_id]:.1f}; #1 = el que más tira)")
        if j.team_id in concede:
            out.append(f"Su equipo es #{_puesto(concede, j.team_id)} de {len(concede)} en tiros que concede "
                       f"({concede[j.team_id]:.1f} por partido; #1 = el que más concede)")
        sv = ctx.sv_portero.get(j.player_id, ctx.sv_liga)
        out.append(f"Oportunidades: se esperan {sa:.1f} tiros a puerta en contra; su % de paradas es "
                   f"{sv * 100:.1f}% (liga {ctx.sv_liga * 100:.1f}%): {pred.mu:.1f} paradas esperadas")
        ult = j.partidos[:10]
        out.append(f"Últimos 10 como titular: {sum(p['sv'] for p in ult) / len(ult):.1f} paradas y "
                   f"{sum(p['sa'] for p in ult) / len(ult):.1f} tiros recibidos por partido")
        if j.rival_b2b:
            out.append("El rival jugó anoche")
        return out
    umbral = j.minutos - 2
    normales = [p for p in j.partidos[:15] if p["toi"] >= umbral]
    if 3 <= len(normales) < len(j.partidos[:15]):
        h = sum(pasa(valor(p, stat)) for p in normales)
        out.append(f"Con {umbral:.0f}+ minutos en hielo (hoy se esperan {j.minutos:.0f}): {h} de {len(normales)} "
                   "en sus últimos 15")
    c = _comp_defensa(stat)
    niveles = ctx.nivel.get(j.grupo, {}).get(c, {})
    fuertes = [p for p in j.partidos[:40] if niveles.get(p["opp_id"]) == "fuerte"]
    if len(fuertes) >= 3:
        h = sum(pasa(valor(p, stat)) for p in fuertes)
        out.append(f"Contra las ~10 mejores defensas en {NOMBRE_COMP[c]} a {GRUPOS_TEXTO[j.grupo]}: {h} de "
                   f"{len(fuertes)} (últimos 40 partidos)")
    hoy = niveles.get(j.opp_id)
    ambas = [p for p in j.partidos[:60] if hoy and niveles.get(p["opp_id"]) == hoy and p["toi"] >= umbral]
    if len(ambas) >= 4:
        h = sum(pasa(valor(p, stat)) for p in ambas)
        media = sum(valor(p, stat) for p in ambas) / len(ambas)
        plural = {"fuerte": "fuertes", "media": "medias", "débil": "débiles"}.get(hoy, hoy)
        out.append(f"Contra defensas {plural} como la de hoy y con {umbral:.0f}+ minutos: {h} de {len(ambas)}, "
                   f"con {media:.1f} de media")
    concede = {t: d.get(j.grupo, {}).get(c) for t, d in ctx.defensa.items()
               if t in equipos and d.get(j.grupo, {}).get(c)}
    pu = _puesto(concede, j.opp_id)
    if pu:
        out.append(f"El rival es #{pu} de {len(concede)} en {NOMBRE_COMP[c]} que concede a {GRUPOS_TEXTO[j.grupo]} "
                   f"por minuto (#1 = el que más concede; {(concede[j.opp_id] - 1) * 100:+.0f}% frente a la media)")
    ult = j.partidos[:10]
    if c == "sog":
        intentos = [ctx.intentos.get(j.player_id, {}).get(p["game_id"], 0) for p in ult]
        if sum(intentos):
            a_puerta = sum(p["sog"] for p in ult)
            out.append(f"Oportunidades: {sum(intentos) / len(ult):.1f} intentos de tiro por partido (últimos 10) y "
                       f"el {a_puerta / sum(intentos) * 100:.0f}% van a puerta; {sum(p['pp_sog'] for p in ult) / len(ult):.1f} "
                       f"de sus tiros a puerta por partido son en power play")
        intentos_rival = {t: v["intentos_contra"] for t, v in ctx.tiros_equipo.items()}
        if j.opp_id in intentos_rival:
            out.append(f"El rival concede {intentos_rival[j.opp_id]:.1f} intentos de tiro por partido "
                       f"(#{_puesto(intentos_rival, j.opp_id)} de {len(intentos_rival)}, #1 = el que más)")
        tipos = ctx.tipos.get(j.player_id)
        if tipos and sum(tipos.values()) >= 15:
            orden = sorted(tipos.items(), key=lambda kv: -kv[1])[:2]
            total = sum(tipos.values())
            texto = "Cómo tira: " + ", ".join(f"{_TIPO_ES.get(t, t)} {n / total * 100:.0f}%" for t, n in orden)
            if j.player_id in ctx.distancia:
                texto += f"; a {ctx.distancia[j.player_id]:.0f} pies de media de la portería"
            out.append(texto)
    if c in ("g", "a", "pts"):
        ppp = sum(p["pp_g"] + p["pp_a"] for p in temp)
        pts = sum(p["g"] + p["a"] for p in temp)
        out.append(f"Oportunidades: {j.minutos_pp:.1f} min de power play por partido; {ppp} de sus {pts} puntos de "
                   "esta temporada fueron en power play")
        if j.portero_rival:
            sv = ctx.sv_portero.get(j.portero_rival)
            nombre = ctx.nombres_porteros.get(j.portero_rival, "el portero rival")
            if sv:
                porteros = {p: v for p, v in ctx.sv_portero.items() if len(ctx.porteros.get(p, [])) >= 5}
                pp = sorted(porteros, key=lambda p: porteros[p]).index(j.portero_rival) + 1 \
                    if j.portero_rival in porteros else None
                sv_eq = ctx.sv_equipo.get(j.opp_id)
                out.append(f"Portero rival: {nombre}, {sv * 100:.1f}% de paradas (liga {ctx.sv_liga * 100:.1f}%"
                           + (f"; #{pp} de {len(porteros)}, #1 = el que menos para" if pp else "") + ")"
                           + (f"; los porteros de su equipo paran el {sv_eq * 100:.1f}% (ya está en la defensa), así que "
                              f"el ajuste por portero es {(j.factor_portero - 1) * 100:+.0f}%"
                              if sv_eq and abs(j.factor_portero - 1) >= 0.01 else ""))
        goles = {t: v["goles_contra"] for t, v in ctx.tiros_equipo.items()}
        if j.opp_id in goles:
            out.append(f"El rival concede {goles[j.opp_id]:.2f} goles por partido (#{_puesto(goles, j.opp_id)} de "
                       f"{len(goles)}, #1 = el que más)")
    if c in ("sog", "g", "a", "pts") and j.minutos_pp >= 1.0:
        pen = {t: v["pp_rival"] for t, v in ctx.tiros_equipo.items()}
        if j.opp_id in pen:
            out.append(f"El rival da {pen[j.opp_id]:.1f} min de power play por partido (#{_puesto(pen, j.opp_id)} de "
                       f"{len(pen)} en penaltis, #1 = el que más)"
                       + (f"; ajuste a su tiempo en PP {(j.factor_penaltis - 1) * 100:+.0f}%"
                          if abs(j.factor_penaltis - 1) >= 0.01 else ""))
    if c == "bs":
        intentos_rival = {t: v["intentos_favor"] for t, v in ctx.tiros_equipo.items()}
        if j.opp_id in intentos_rival:
            out.append(f"Oportunidades: el rival intenta {intentos_rival[j.opp_id]:.1f} tiros por partido "
                       f"(#{_puesto(intentos_rival, j.opp_id)} de {len(intentos_rival)}, #1 = el que más); él bloquea "
                       f"{sum(p['bs'] for p in ult) / len(ult):.1f} por partido con {sum(p['shtoi'] or 0 for p in ult) / len(ult):.1f} "
                       "min en inferioridad")
    if j.bajas_rival:
        out.append("El rival no tiene a " + ", ".join(j.bajas_rival))
    if j.bajas_equipo:
        out.append("Su equipo no tiene a " + ", ".join(j.bajas_equipo) + ": más hielo y más power play para el resto")
    if j.b2b or j.rival_b2b:
        texto = ("Los dos juegan el segundo partido en dos noches (se compensa)" if j.b2b and j.rival_b2b else
                 ("Su equipo" if j.b2b else "El rival") + " juega el segundo partido en dos noches")
        efecto = {} if j.b2b == j.rival_b2b else (B2B_PROPIO if j.b2b else B2B_RIVAL)
        aj = sum(efecto.get(x, 0.0) for x in COMPONENTES[stat]) / len(COMPONENTES[stat])
        if USAR_B2B and aj:
            texto += f": ajuste aplicado {aj * 100:+.1f}% (backtest 2025-26)"
        out.append(texto)
    m = ctx.margen.get(j.team_id)
    if m is not None and abs(m) >= 0.3:
        texto = f"Diferencia esperada: su equipo {'favorito' if m > 0 else 'no favorito'} por {abs(m):.1f} goles"
        aj = MARGEN_EFECTO.get(COMPONENTES[stat][0], 0.0) * max(-MARGEN_TOPE, min(MARGEN_TOPE, m))
        if USAR_MARGEN and aj and len(COMPONENTES[stat]) == 1:
            texto += f" (ajuste {aj * 100:+.1f}%: los favoritos tiran más y bloquean menos)"
        out.append(texto)
    out.append(f"Tiempo en hielo: {j.minutos:.1f} min esperados (±{j.minutos_sd:.1f}), {j.minutos_pp:.1f} en power play"
               f"; {'papel principal' if es_titular(j) else 'papel menor'}")
    return out


_TIPO_ES = {"Wrist Shot": "muñeca", "Snap Shot": "snap", "Slap Shot": "slap", "Backhand": "revés",
            "Tip-In": "desvío (tip-in)", "Deflected": "desviado", "Wrap-around": "wrap-around", "Poke": "poke"}


@dataclass
class Segura:
    player_id: str
    nombre: str
    stat: str
    line: float
    prob: float
    mu: float
    media_10: float
    acierto_10: tuple[int, int]
    team_id: str = ""

    @property
    def cuota_minima(self) -> float:
        return 1 / self.prob


# Líneas mínimas de Betano (estimadas; comprobar con las que mande el usuario). Puntos, goles y asistencias no bajan
# de 0.5; tiros a puerta, bloqueados y hits, una por debajo de la principal; paradas, ~4 por debajo.
BAJADA_CASA = {"shots": 1, "blocked": 1, "hits": 1, "saves": 4}


def linea_minima_casa(principal: float, stat: str) -> float:
    return max(0.5, principal - BAJADA_CASA.get(stat, 0))


def linea_estimada(j: Jugador, stat: str, mu: float) -> float:
    """La línea principal que pondría la casa (sin línea): entre lo que espera el modelo y su media de los últimos 10.
    Puntos, goles y asistencias casi siempre van a 0.5."""
    if stat in ("points", "goals", "assists"):
        return 0.5
    ult = j.partidos[:10]
    media = sum(valor(p, stat) for p in ult) / len(ult) if ult else mu
    # Las casas no ponen una línea principal de tiros a puerta por debajo de 1.5.
    return max(LINEA_MINIMA_PRINCIPAL.get(stat, 0.5), math.floor((mu + media) / 2) + 0.5)


LINEA_MINIMA_PRINCIPAL = {"shots": 1.5}


def piso_casa(j: Jugador, stat: str, mu: float, principal: float | None = None) -> float:
    return linea_minima_casa(principal if principal is not None else linea_estimada(j, stat, mu), stat)


PROB_SEGURA = 0.85
PROB_JUGABLE = 0.75
MEDIAS_SEGURA = {"shots": 2.5, "points": 0.9, "blocked": 1.8, "saves": 24.0}


def seguras(ctx: Contexto, j: Jugador, objetivo: float = PROB_SEGURA, principales: dict | None = None) -> list[Segura]:
    """Para jugadores de papel principal sin alertas, la línea de "más de" más alta con esa probabilidad, sin bajar
    de la mínima que ofrecería la casa."""
    if alertas(ctx, j, "shots" if not j.es_portero else "saves"):
        return []
    out = []
    ult = j.partidos[:10]
    for stat, minimo in MEDIAS_SEGURA.items():
        if (stat == "saves") != j.es_portero or vetada(j.nombre, stat):
            continue
        media = sum(valor(p, stat) for p in ult) / len(ult)
        if media < minimo:
            continue
        pred = predecir(ctx, j, stat)
        piso = piso_casa(j, stat, pred.mu, (principales or {}).get((j.player_id, stat)))
        ultima = None
        for k in range(int(pred.mu), -1, -1):
            if k + 0.5 < piso:
                break
            p = _prob_jugador(j, stat, k + 0.5, "más", prob_lados(k + 0.5, pred.mu, pred.var)[0])
            ultima = (k + 0.5, p)
            if p >= objetivo:
                out.append(Segura(j.player_id, j.nombre, stat, k + 0.5, p, pred.mu, media,
                                  _aciertos(ult, stat, k + 0.5, "más"), j.team_id))
                break
        else:
            ultima = None
        if ultima and objetivo > ultima[1] >= PROB_JUGABLE:
            out.append(Segura(j.player_id, j.nombre, stat, ultima[0], ultima[1], pred.mu, media,
                              _aciertos(ult, stat, ultima[0], "más"), j.team_id))
    return out


def evaluar(ctx: Contexto, j: Jugador, stat: str, line: float, over_odd: float | None = None,
            under_odd: float | None = None, peso_mercado: float = PESO_MERCADO, detalle: bool = True,
            estimada: bool = False) -> Evaluacion:
    pred = predecir(ctx, j, stat)
    lados = {}
    con_cuota = bool(over_odd or under_odd)
    n_actual = sum(1 for p in j.partidos if p["season"] == ctx.temporada)
    peso_mercado = max(peso_mercado, peso_mercado + (PESO_MERCADO_INICIO - peso_mercado)
                       * max(0.0, 1 - n_actual / PARTIDOS_INICIO))
    if j.pocos_con_equipo:
        peso_mercado = max(peso_mercado, PESO_MERCADO_TRASPASO)
    for lado, p_mod, odd, p_casa in zip(("más", "menos"), prob_lados(line, pred.mu, pred.var),
                                        (over_odd, under_odd), prob_mercado(over_odd, under_odd)):
        if con_cuota and not odd:
            continue
        p_jug = _prob_jugador(j, stat, line, lado, p_mod)
        final = p_jug if p_casa is None else (1 - peso_mercado) * p_jug + peso_mercado * p_casa
        lados[lado] = (final, p_jug, p_casa, odd)
    lado = max(lados, key=lambda k: lados[k][0])
    prob, p_jug, p_casa, odd = lados[lado]
    temporada = [p for p in j.partidos if p["season"] == ctx.temporada]
    vs = [valor(p, stat) for p in j.partidos if p["opp_id"] == j.opp_id][:5]
    al = alertas(ctx, j, stat) if detalle else []
    if detalle:
        if p_casa is not None and p_jug - p_casa > DISCREPANCIA_MAX:
            al.append("muy lejos de la casa")
        if lado == "menos":
            al += _falla_en_normales(ctx, j, stat, line)
            if j.bajas_equipo and stat != "blocked" and stat != "saves":
                al.append(f"sin {j.bajas_equipo[0]}: más hielo para él")
    return Evaluacion(
        j.player_id, j.nombre, stat, line, lado, prob, p_jug, p_casa, pred.mu, math.sqrt(pred.var),
        _aciertos(j.partidos[:10], stat, line, lado), _aciertos(temporada, stat, line, lado), vs,
        sum(valor(p, stat) for p in j.partidos[:10]) / min(10, j.n), odd, pred.factores, es_titular(j), al,
        texto_defensa(ctx, j, stat, pred) if detalle else "",
        argumentos(ctx, j, stat, line, lado, pred) if detalle else [], estimada, j.team_id)
