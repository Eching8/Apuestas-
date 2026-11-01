"""Mercados de partido y de equipo: un simulador del partido posesión a posesión.

Cada simulación reparte las posesiones de los dos equipos por cuartos y decide el resultado de cada una
(touchdown, gol de campo, nada; muy de vez en cuando un safety o un TD de la defensa). Las probabilidades por
posesión salen del modelo propio (no de la línea de la casa, para poder compararlas): TD esperados del equipo
(ataque × defensa rival), goles de campo esperados y posesiones por partido. Cada equipo lleva además un factor
de forma aleatorio por simulación, que da a los marcadores la dispersión que tienen en la realidad.

De las mismas simulaciones salen todos los mercados, de forma coherente entre sí: moneyline, spread, total y
total por equipo (partido, mitades y cuartos), par/impar, resultado a 3 vías, si un equipo anota en un periodo,
quién anota primero y último, si anotan ambos en un cuarto, número de TD y de goles de campo, el gol de campo más
largo, la mayor ventaja, si hay safety, y las props de los pateadores (goles de campo, extras y puntos).
Pérdidas de balón, punts y sacks de equipo usan su propia media (ataque × defensa) con binomial negativa.
"""
from __future__ import annotations

import math
import random
from dataclasses import dataclass, field

from .modelo import Contexto, Linea, PERIODOS, cdf, entorno

N_SIMULACIONES = 4000
SIGMA_FORMA = 0.12          # dispersión del factor de forma de cada equipo en cada simulación
P_EXTRA = (0.935, 0.035, 0.03)   # tras un TD: extra bueno (7), fallado (6), conversión de 2 (8)
EMPATE_PRORROGA = 0.08      # parte de las prórrogas que terminan en empate (temporada regular)


@dataclass
class Simulacion:
    """Resultados de N simulaciones de un partido (local = 'home', visitante = 'away')."""
    n: int
    puntos: dict[str, list[list[int]]]          # lado -> por simulación [q1, q2, q3, q4, prórroga]
    tds: dict[str, list[list[int]]]             # lado -> por simulación TD por cuarto
    fgs: dict[str, list[list[int]]]             # lado -> por simulación FG por cuarto
    xps: dict[str, list[int]]                   # lado -> extras anotados por simulación
    primero: dict[str, list[str | None]]        # periodo -> por simulación lado que anotó primero
    ultimo: dict[str, list[str | None]]
    ventaja_max: list[int]
    fg_largo: list[float]
    safety: dict[str, list[bool]]
    medias: dict = field(default_factory=dict)  # lo esperado por equipo: TD, FG, puntos, posesiones


def _posesiones(ctx: Contexto, team: str, opp: str) -> float:
    a, d = ctx.perfiles[team].ataque, ctx.perfiles[opp].defensa
    oa, od = ctx.perfiles[opp].ataque, ctx.perfiles[team].defensa
    vals = [x for x in (a.get("drives"), d.get("drives"), oa.get("drives"), od.get("drives")) if x]
    return sum(vals) / len(vals) if vals else 11.0


def simular(ctx: Contexto, home: str, away: str, n: int = N_SIMULACIONES, semilla: int = 1,
            viento: float | None = None, techo: str | None = None) -> Simulacion:
    rng = random.Random(semilla)
    lg = ctx.liga
    medias = {}
    for lado, team, opp, local in (("home", home, away, True), ("away", away, home, False)):
        ent = entorno(ctx, team, opp, local, Linea(), viento, techo)   # sin la casa: modelo propio
        a, d = ctx.perfiles[team].ataque, ctx.perfiles[opp].defensa
        fg = (a.get("fgm") or 1.6) * (d.get("fgm") or 1.6) / (lg.get("fgm") or 1.6)
        medias[lado] = {"team": team, "tds": ent.tds, "fg": fg, "posesiones": _posesiones(ctx, team, opp),
                        "puntos": ent.puntos}
    reparto_pts = ctx.periodos.get("puntos") or {1: 0.25, 2: 0.25, 3: 0.25, 4: 0.25}
    peso_q = {q: 4 * reparto_pts.get(q, 0.25) for q in (1, 2, 3, 4)}
    dist_fg = ctx.periodos.get("distancias_fg") or [22, 28, 33, 36, 39, 42, 45, 48, 51, 54]
    p_saf = ctx.periodos.get("safety_por_drive", 0.003)
    p_tddef = ctx.periodos.get("td_def_por_drive", 0.007)
    sim = Simulacion(n, {"home": [], "away": []}, {"home": [], "away": []}, {"home": [], "away": []},
                     {"home": [], "away": []}, {p: [] for p in PERIODOS}, {p: [] for p in PERIODOS}, [], [],
                     {"home": [], "away": [], "all": []}, medias)
    otro = {"home": "away", "away": "home"}
    for _ in range(n):
        posesiones = max(8, round(rng.gauss((medias["home"]["posesiones"] + medias["away"]["posesiones"]) / 2, 1.0)))
        p = {}
        for lado in ("home", "away"):
            m = medias[lado]
            forma = math.exp(rng.gauss(0, SIGMA_FORMA) - SIGMA_FORMA ** 2 / 2)
            p_td = min(0.6, m["tds"] / m["posesiones"] * forma)
            p_fg = min(0.35, m["fg"] / m["posesiones"] * (0.6 + 0.4 * forma))
            p[lado] = (p_td, p_fg)
        pts = {"home": [0] * 5, "away": [0] * 5}
        tds = {"home": [0] * 4, "away": [0] * 4}
        fgs = {"home": [0] * 4, "away": [0] * 4}
        xps = {"home": 0, "away": 0}
        eventos: list[tuple[int, str]] = []
        lider_max, fg_largo, safety = 0, 0.0, {"home": False, "away": False}
        ataca = "home" if rng.random() < 0.5 else "away"
        total = 2 * posesiones
        marcador = {"home": 0, "away": 0}
        for k in range(total):
            q = min(4, 1 + 4 * k // total)
            p_td, p_fg = p[ataca]
            u = rng.random() / peso_q[q]
            anotador, puntos = None, 0
            if u < p_td:
                anotador, puntos = ataca, _puntos_td(rng)
                tds[ataca][q - 1] += 1
                xps[ataca] += puntos == 7
            elif u < p_td + p_fg:
                anotador, puntos = ataca, 3
                fgs[ataca][q - 1] += 1
                fg_largo = max(fg_largo, rng.choice(dist_fg))
            else:
                r = rng.random()
                if r < p_saf:
                    anotador, puntos = otro[ataca], 2
                    safety[otro[ataca]] = True
                elif r < p_saf + p_tddef:
                    anotador, puntos = otro[ataca], _puntos_td(rng)
                    tds[otro[ataca]][q - 1] += 1
                    xps[otro[ataca]] += puntos == 7
            if anotador:
                pts[anotador][q - 1] += puntos
                marcador[anotador] += puntos
                eventos.append((q, anotador))
                lider_max = max(lider_max, abs(marcador["home"] - marcador["away"]))
            ataca = otro[ataca]
        if marcador["home"] == marcador["away"] and rng.random() > EMPATE_PRORROGA:
            ph, pa = sum(p["home"]), sum(p["away"])
            gana = "home" if rng.random() < ph / (ph + pa) else "away"
            extra = 6 if rng.random() < 0.4 else 3
            pts[gana][4] += extra
            eventos.append((5, gana))
            lider_max = max(lider_max, extra)
        for lado in ("home", "away"):
            sim.puntos[lado].append(pts[lado])
            sim.tds[lado].append(tds[lado])
            sim.fgs[lado].append(fgs[lado])
            sim.xps[lado].append(xps[lado])
            sim.safety[lado].append(safety[lado])
        sim.safety["all"].append(safety["home"] or safety["away"])
        for periodo, cuartos in PERIODOS.items():
            en = [lado for q, lado in eventos if q in cuartos or (periodo in ("game", "2h") and q == 5)]
            sim.primero[periodo].append(en[0] if en else None)
            sim.ultimo[periodo].append(en[-1] if en else None)
        sim.ventaja_max.append(lider_max)
        sim.fg_largo.append(fg_largo)
    return sim


def _puntos_td(rng: random.Random) -> int:
    r = rng.random()
    return 7 if r < P_EXTRA[0] else 6 if r < P_EXTRA[0] + P_EXTRA[1] else 8


# --- Probabilidades de cada mercado ------------------------------------------------------------

def _periodo(valores: list[int], periodo: str) -> int:
    cuartos = PERIODOS[periodo]
    total = sum(valores[q - 1] for q in cuartos)
    if periodo in ("game", "2h") and len(valores) > 4:
        total += valores[4]          # la prórroga cuenta en el partido y en la 2.ª mitad
    return total


def _frecuencia(condiciones: list[bool | None]) -> float | None:
    """Proporción de True entre los casos decididos (None = devolución: empate en la línea)."""
    decididos = [c for c in condiciones if c is not None]
    return sum(decididos) / len(decididos) if decididos else None


def _comparar(valor: float, line: float, lado: str) -> bool | None:
    if valor == line:
        return None
    return valor > line if lado == "más" else valor < line


def prob_partido(sim: Simulacion, stat: str, bet: str, periodo: str, entidad: str, lado: str,
                 line: float | None) -> tuple[float, float] | None:
    """(probabilidad, valor esperado de la estadística) de una apuesta de partido o equipo según la simulación."""
    if periodo not in PERIODOS:
        return None
    n = sim.n
    ph = [_periodo(x, periodo) for x in sim.puntos["home"]]
    pa = [_periodo(x, periodo) for x in sim.puntos["away"]]
    if stat == "pts":
        if bet == "ml":
            res = [None if h == a else (h > a) == (lado == "home") for h, a in zip(ph, pa)]
            return _frecuencia(res), sum(h - a for h, a in zip(ph, pa)) / n
        if bet == "ml3way":
            res = [(h > a) if lado == "home" else (a > h) if lado == "away" else (h == a) for h, a in zip(ph, pa)]
            return _frecuencia(res), sum(h - a for h, a in zip(ph, pa)) / n
        if bet == "sp" and line is not None:
            dif = [(h - a) if lado == "home" else (a - h) for h, a in zip(ph, pa)]
            return _frecuencia([None if d + line == 0 else d + line > 0 for d in dif]), sum(dif) / n
        valores = ph if entidad == "home" else pa if entidad == "away" else [h + a for h, a in zip(ph, pa)]
        if bet == "ou" and line is not None:
            return _frecuencia([_comparar(v, line, lado) for v in valores]), sum(valores) / n
        if bet == "eo":
            return sum((v % 2 == 0) == (lado == "par") for v in valores) / n, sum(valores) / n
        if bet == "yn":
            return sum((v > 0) == (lado == "sí") for v in valores) / n, sum(valores) / n
        return None
    if stat in ("tds", "fg"):
        fuente = sim.tds if stat == "tds" else sim.fgs
        th = [sum(x[q - 1] for q in PERIODOS[periodo]) for x in fuente["home"]]
        ta = [sum(x[q - 1] for q in PERIODOS[periodo]) for x in fuente["away"]]
        valores = th if entidad == "home" else ta if entidad == "away" else [h + a for h, a in zip(th, ta)]
        if bet == "ou" and line is not None:
            return _frecuencia([_comparar(v, line, lado) for v in valores]), sum(valores) / n
        if bet == "yn":
            return sum((v > 0) == (lado == "sí") for v in valores) / n, sum(valores) / n
        return None
    if stat in ("primero", "ultimo") and bet == "ml":
        quien = (sim.primero if stat == "primero" else sim.ultimo)[periodo]
        return _frecuencia([None if x is None else x == lado for x in quien]), 0.0
    if stat == "ambos" and bet == "yn":
        return sum(((h > 0) and (a > 0)) == (lado == "sí") for h, a in zip(ph, pa)) / n, 0.0
    if stat == "ventaja" and bet == "ou" and line is not None:
        return _frecuencia([_comparar(v, line, lado) for v in sim.ventaja_max]), sum(sim.ventaja_max) / n
    if stat == "fg_largo" and bet == "ou" and line is not None:
        return _frecuencia([_comparar(v, line, lado) for v in sim.fg_largo]), sum(sim.fg_largo) / n
    if stat == "safety" and bet == "yn":
        valores = sim.safety.get(entidad, sim.safety["all"])
        return sum(v == (lado == "sí") for v in valores) / n, sum(valores) / n
    return None


def prob_pateador(sim: Simulacion, lado_equipo: str, stat: str, line: float, lado: str) -> tuple[float, float] | None:
    """Props del pateador de un equipo: goles de campo, extras y puntos de pateo (3 × FG + extras)."""
    fg = [sum(x) for x in sim.fgs[lado_equipo]]
    xp = sim.xps[lado_equipo]
    valores = fg if stat == "fg" else xp if stat == "xp" else [3 * f + x for f, x in zip(fg, xp)] \
        if stat == "kick_pts" else None
    if valores is None:
        return None
    return _frecuencia([_comparar(v, line, lado) for v in valores]), sum(valores) / sim.n


# --- Mercados de equipo con su propia media ------------------------------------------------------

def media_equipo(ctx: Contexto, home: str, away: str, stat: str, entidad: str) -> float | None:
    """Pérdidas de balón, punts o sacks esperados (de un equipo o del partido): ataque × defensa / liga."""
    col = {"perdidas": "turnovers", "punts": "punts", "sacks": "sacks"}.get(stat)
    if col is None:
        return None
    lg = ctx.liga.get(col) or 1.0

    def de(team: str, opp: str) -> float:
        a, d = ctx.perfiles[team].ataque.get(col) or lg, ctx.perfiles[opp].defensa.get(col) or lg
        return a * d / lg

    # Sacks "de un equipo" son los que logra su defensa: los que sufre el ataque rival.
    if stat == "sacks":
        valores = {"home": de(away, home), "away": de(home, away)}
    else:
        valores = {"home": de(home, away), "away": de(away, home)}
    return valores["home"] + valores["away"] if entidad == "all" else valores.get(entidad)


def prob_conteo(mu: float, line: float, lado: str, dispersion: float = 0.15) -> float:
    var = mu + dispersion * mu * mu
    k = math.floor(line)
    mas = 1 - cdf(k, mu, var)
    if line == int(line):
        empate = cdf(int(line), mu, var) - cdf(int(line) - 1, mu, var)
        menos = 1 - mas - empate
        return (mas if lado == "más" else menos) / (1 - empate) if empate < 1 else 0.5
    return mas if lado == "más" else 1 - mas
