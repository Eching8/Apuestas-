"""Analiza cada partido: proyecciones, tabla de touchdowns, cruce con el mercado y selecciones con valor."""
from __future__ import annotations

import json
import math
import zlib
from dataclasses import dataclass, field

from ..db import now_iso
from . import equipos
from .db import NflDB
from .mercado import Mercado, Oferta
from .modelo import (NOMBRE_PERIODO, NOMBRES, Contexto, Entorno, Linea, Proyeccion, entorno, fraccion, p_al_menos,
                     preparar_equipo, proyectar, rango, texto_rango, valor)
from .modelo_defensa import candidatos_defensa, pateador, proyectar_defensa
from .modelo_partido import Simulacion, media_equipo, prob_conteo, prob_partido, prob_pateador, simular
from .razones import Razones, razones
from .zona_roja import ajustar_tds
from .zona_roja import mapa as mapa_rz

PESO_MERCADO = 0.35            # peso de la probabilidad de la casa (sin margen) en la probabilidad final
PESO_MERCADO_DUDOSO = 0.6      # si el jugador acaba de llegar, tiene poca muestra o está en duda
# Cuando modelo y casa discrepan mucho, casi siempre la casa sabe algo que los datos aún no muestran (un cambio
# de rol, una lesión, quién vuelve). Con más de 15 puntos de diferencia la casa pesa 0.6; con más de 25, 0.75.
DISCREPANCIA = ((0.25, 0.75), (0.15, 0.6))
TD_DEFENSA_ESPECIALES = 0.12   # TD por partido de defensa y equipos especiales (cuentan para el "primer TD")
# Spread, totales y moneyline son los mercados más eficientes: ahí la casa pesa más. En el backtest de 2025 el
# simulador acierta al ganador mejor que el azar (Brier 0.222), pero no le gana al spread ni al total de cierre
# (0.257 y 0.262 frente a 0.250): en esos dos la casa pesa 85 %.
PESO_MERCADO_PARTIDO = 0.6
PESO_MERCADO_SPREAD_TOTAL = 0.85
NOMBRES_EQUIPO = {"pts": "puntos", "tds": "touchdowns", "fg": "goles de campo", "fg_largo": "gol de campo más largo",
                  "ventaja": "mayor ventaja", "perdidas": "pérdidas de balón", "punts": "punts", "sacks": "sacks"}


@dataclass
class Evaluacion:
    game_id: str
    player_id: str
    nombre: str
    pos: str
    team: str
    opp: str
    stat: str
    line: float
    lado: str
    prob: float
    prob_modelo: float
    prob_casa: float | None
    mu: float
    odd: float | None
    book: str | None
    consenso: float | None
    ev: float | None
    razones: Razones
    oferta: Oferta | None = None
    periodo: str = "game"
    tipo: str = "jugador"          # 'jugador' o 'equipo'
    bet: str = "ou"

    @property
    def edge(self) -> float | None:
        return None if self.prob_casa is None else self.prob_modelo - self.prob_casa

    @property
    def codigo(self) -> str:
        """Lo que se guarda en nfl_picks.stat (ver mercado.Oferta.codigo)."""
        if self.tipo == "jugador":
            return self.stat if self.periodo == "game" else f"{self.stat}@{self.periodo}"
        return f"{self.stat}@{self.periodo}/{self.bet}"

    def etiqueta(self) -> str:
        per = f" ({NOMBRE_PERIODO[self.periodo]})" if self.periodo != "game" else ""
        if self.tipo == "equipo":
            return etiqueta_equipo(self) + per
        if self.stat in ("first_td", "last_td"):
            cual = "primer" if self.stat == "first_td" else "último"
            return f"{self.nombre} {cual} TD{' de la 2.ª mitad' if self.periodo == '2h' else ' del partido'}"
        if self.stat == "tds":
            k = int(self.line + 0.5)
            return (f"{self.nombre} {'anota' if k == 1 else f'{k}+ TD'}" if self.lado == "más" else
                    f"{self.nombre} no anota" if k == 1 else f"{self.nombre} menos de {k} TD") + per
        return f"{self.nombre} {self.lado} de {self.line:g} {NOMBRES.get(self.stat, self.stat)}{per}"


def etiqueta_equipo(e: "Evaluacion") -> str:
    equipo_lado = e.nombre if e.player_id != "ALL" else "Partido"
    if e.bet in ("ml", "ml3way") and e.stat == "pts":
        tres = " (3 vías)" if e.bet == "ml3way" else ""
        return f"Empate{tres}" if e.lado == "draw" else f"Gana {e.nombre}{tres}"
    if e.bet == "sp":
        return f"{e.nombre} {e.line:+g}"
    if e.stat in ("primero", "ultimo"):
        return f"{e.nombre} anota {'primero' if e.stat == 'primero' else 'último'}"
    if e.stat == "ambos":
        return f"Anotan los dos equipos: {e.lado}"
    if e.stat == "safety":
        return f"Hay safety{'' if e.player_id == 'ALL' else ' de ' + e.nombre}: {e.lado}"
    nombre = NOMBRES_EQUIPO.get(e.stat, e.stat)
    sujeto = "Total" if e.player_id == "ALL" else equipo_lado
    if e.bet == "eo":
        return f"{sujeto}: {nombre} {e.lado}"
    if e.bet == "yn":
        return f"{sujeto} {'anota' if e.stat == 'pts' else 'tiene ' + nombre}: {e.lado}"
    return f"{sujeto} {e.lado} de {e.line:g} {nombre}"


@dataclass
class TdJugador:
    game_id: str
    player_id: str
    nombre: str
    pos: str
    team: str
    opp: str
    lam: float
    p1: float
    p2: float
    p_first: float
    rush: float
    rec: float
    notas: list[str]
    ofertas: dict[str, Evaluacion] = field(default_factory=dict)   # '1+', '2+', 'primero'


@dataclass
class AnalisisPartido:
    game: dict
    entornos: dict[str, Entorno]
    proyecciones: list[Proyeccion]
    evaluaciones: list[Evaluacion]
    tds: list[TdJugador]
    claves: dict[str, list[str]]
    mercado: Mercado | None = None
    simulacion: Simulacion | None = None
    defensores: list[Proyeccion] = field(default_factory=list)
    zona_roja: dict[str, list[str]] = field(default_factory=dict)   # team -> mapa de la zona roja (ver zona_roja.mapa)

    @property
    def titulo(self) -> str:
        g = self.game
        return f"{equipos.nombre(g['away_team'])} @ {equipos.nombre(g['home_team'])}"


def _peso_mercado(proy: Proyeccion, base: float, p_mod: float, p_casa: float) -> float:
    j = proy.jugador
    w = base
    if (j.llegada and len(j.con_equipo) < 3) or j.n < 4 or j.estado:
        w = max(w, PESO_MERCADO_DUDOSO)
    for umbral, peso in DISCREPANCIA:
        if abs(p_mod - p_casa) > umbral:
            return max(w, peso)
    return w


def evaluar(ctx: Contexto, proy: Proyeccion, stat: str, line: float, lado: str, oferta: Oferta | None,
            peso_mercado: float = PESO_MERCADO, p_first: float | None = None, game_id: str = "",
            periodo: str = "game") -> Evaluacion | None:
    j, ent = proy.jugador, proy.entorno
    if stat in ("first_td", "last_td"):
        if p_first is None:
            return None
        p_mod, mu = (p_first if lado == "más" else 1 - p_first), p_first
    elif stat in proy.medias:
        lados = proy.prob_periodo(ctx, stat, periodo, line)
        if lados is None:
            return None
        p_mod = lados[0] if lado == "más" else lados[1]
        mu = proy.medias[stat] * (1.0 if periodo == "game" else
                                  fraccion(ctx, "TD" if stat in ("tds", "rush_tds", "rec_tds") else stat, periodo))
    else:
        return None
    p_casa = oferta.prob_casa() if oferta else None
    prob = p_mod if p_casa is None else (1 - (w := _peso_mercado(proy, peso_mercado, p_mod, p_casa))) * p_mod \
        + w * p_casa
    book, odd = oferta.mejor if oferta else (None, None)
    ev = prob * odd - 1 if odd else None
    r = razones(ctx, proy, stat, line, lado, oferta, p_mod, p_casa)
    if periodo != "game":
        r.contexto.insert(0, f"{NOMBRE_PERIODO[periodo]}: se espera {mu:.1f} (el periodo suele concentrar el "
                             f"{mu / max(proy.medias.get(stat, mu), 1e-9) * 100:.0f}% de lo del partido)")
    return Evaluacion(game_id, j.player_id, j.nombre, j.pos, j.team, ent.opp, stat, line, lado, prob, p_mod, p_casa,
                      mu, odd, book, oferta.consenso if oferta else None, ev, r, oferta, periodo)


def _evaluacion_simple(game: dict, of: Oferta, player_id: str, nombre: str, pos: str, team: str, opp: str,
                       p_mod: float, mu: float, peso: float, contexto: list[str]) -> Evaluacion:
    """Evaluación de un mercado de partido, de equipo o de pateador (probabilidad de la simulación)."""
    p_casa = of.prob_casa()
    prob = p_mod if p_casa is None else (1 - peso) * p_mod + peso * p_casa
    for umbral, w in DISCREPANCIA:
        if p_casa is not None and abs(p_mod - p_casa) > umbral:
            prob = (1 - max(peso, w)) * p_mod + max(peso, w) * p_casa
            break
    book, odd = of.mejor
    favor, contra = [], []
    if p_casa is not None:
        if p_mod - p_casa >= 0.04:
            favor.append(f"el modelo le da {p_mod * 100:.0f}% y la casa {p_casa * 100:.0f}%")
        elif p_mod - p_casa <= -0.04:
            contra.append(f"la casa le da {p_casa * 100:.0f}% y el modelo solo {p_mod * 100:.0f}%")
    mov = of.movimiento()
    if mov:
        (favor if of.presion() > 0.02 else contra if of.presion() < -0.02 else contexto).append(f"mercado: {mov}")
    if odd and of.consenso and odd > of.consenso * 1.04 and book:
        favor.append(f"mejor precio en {book}: {odd:.2f} frente a {of.consenso:.2f} de consenso")
    return Evaluacion(game["game_id"], player_id, nombre, pos, team, opp, of.stat, of.line, of.lado, prob, p_mod,
                      p_casa, mu, odd, book, of.consenso, prob * odd - 1 if odd else None,
                      Razones(favor, contra, contexto), of, of.periodo, "equipo" if pos == "-" else "jugador", of.bet)


def evaluar_equipo(ctx: Contexto, game: dict, sim: Simulacion, of: Oferta,
                   claves: dict[str, list[str]]) -> Evaluacion | None:
    home, away = game["home_team"], game["away_team"]
    ent = of.sgo_player_id
    lado_eq = of.lado if of.lado in ("home", "away") else ent if ent in ("home", "away") else None
    team = {"home": home, "away": away}.get(lado_eq or "", "ALL")
    if of.stat in ("perdidas", "punts", "sacks"):
        if of.bet != "ou":
            return None
        mu = media_equipo(ctx, home, away, of.stat, ent)
        if mu is None or of.periodo != "game":
            return None
        r = (prob_conteo(mu, of.line, of.lado), mu)
    else:
        r = prob_partido(sim, of.stat, of.bet, of.periodo, ent, of.lado, of.line)
    if r is None or r[0] is None:
        return None
    p_mod, mu = r
    mh, ma = sim.medias["home"], sim.medias["away"]
    contexto = [f"modelo propio (sin la casa): {equipos.apodo(home)} {mh['puntos']:.1f} – {equipos.apodo(away)} "
                f"{ma['puntos']:.1f}; TD esperados {mh['tds']:.2f} y {ma['tds']:.2f}; goles de campo "
                f"{mh['fg']:.2f} y {ma['fg']:.2f}; {mh['posesiones']:.1f} posesiones por equipo",
                f"valor medio simulado de este mercado: {mu:+.2f}" if of.bet in ("ml", "sp", "ml3way")
                else f"valor medio simulado: {mu:.2f}"]
    nombre = equipos.nombre(team) if team != "ALL" else "Partido"
    opp = {home: away, away: home}.get(team, "-")
    peso = PESO_MERCADO_SPREAD_TOTAL if of.stat == "pts" and of.bet in ("sp", "ou") else PESO_MERCADO_PARTIDO
    return _evaluacion_simple(game, of, team, nombre, "-", team, opp, p_mod, mu, peso, contexto)


def claves_enfrentamiento(ctx: Contexto, team: str, opp: str) -> list[str]:
    """Dónde se gana el partido cuando ataca `team`: su ataque frente a la defensa rival, métrica a métrica."""
    a, d = ctx.perfiles[team].ataque, ctx.perfiles[opp].defensa
    ta, td = equipos.apodo(team), equipos.apodo(opp)
    out = []

    def linea(nombre: str, m: str, fmt: str, mejor_alto: bool = True) -> None:
        ra, rd = rango(ctx, "ataque", m, team), rango(ctx, "defensa", m, opp)
        if not ra or not rd or a.get(m) is None or d.get(m) is None:
            return
        n = ra[1]
        # Puesto "de calidad": 1 = mejor ataque / defensa que más concede (la peor).
        qa = ra[0] if mejor_alto else n - ra[0] + 1
        qd = rd[0] if mejor_alto else n - rd[0] + 1
        if qa <= n / 3 and qd <= n / 3:
            veredicto = "VENTAJA CLARA DEL ATAQUE"
        elif qa > 2 * n / 3 and qd > 2 * n / 3:
            veredicto = "VENTAJA CLARA DE LA DEFENSA"
        elif qa <= n / 3 and qd > 2 * n / 3:
            veredicto = "fuerza contra fuerza"
        elif qa > 2 * n / 3 and qd <= n / 3:
            veredicto = "debilidad contra debilidad"
        elif qa <= n / 3 or qd <= n / 3:
            veredicto = "ventaja del ataque"
        elif qa > 2 * n / 3 or qd > 2 * n / 3:
            veredicto = "ventaja de la defensa"
        else:
            veredicto = "parejo"
        out.append(f"{nombre}: {ta} {fmt.format(a[m])} ({qa}º de {n}) contra {td} que concede {fmt.format(d[m])} "
                   f"({qd}º que más concede) → {veredicto}")

    linea("EPA por jugada", "epa_play", "{:+.3f}")
    linea("Carrera (EPA por acarreo)", "rush_epa", "{:+.3f}")
    linea("Yardas por acarreo", "ypc", "{:.2f}")
    linea("Pase (EPA por dropback)", "pass_epa", "{:+.3f}")
    linea("Yardas por intento de pase", "ypa", "{:.2f}")
    linea("Jugadas explosivas", "explosive", "{:.1%}")
    linea("Zona roja (TD por visita)", "rz_td_pct", "{:.0%}")
    linea("TD por partido", "off_tds", "{:.2f}")
    linea("Tercera oportunidad", "third_pct", "{:.0%}")
    linea("Sacks (por dropback)", "sack_rate", "{:.1%}", mejor_alto=False)
    # QB corredor: lo que corre su QB frente a lo que la defensa concede a los QB por tierra.
    qa, ql = a.get("qb_rush_yds") or 0, ctx.liga.get("qb_rush_yds") or 0
    qd, qdl = ctx.perfiles[opp].pos_defensa.get("QB.rushing_yards", 0), ctx.liga_pos.get("QB.rushing_yards", 0)
    if ql and qdl:
        out.append(f"QB corredor: el QB de {ta} corre {qa:.0f} yardas por partido (liga {ql:.0f}); {td} concede "
                   f"{qd:.0f} a los QB por tierra (liga {qdl:.0f}; "
                   f"{texto_rango(rango(ctx, 'pos', 'QB.rushing_yards', opp))})")
    proe = a.get("proe")
    if proe is not None:
        identidad = "de pase" if proe > 2 else "de carrera" if proe < -2 else "equilibrado"
        out.append(f"Identidad de {ta}: ataque {identidad} (pase sobre lo esperado {proe:+.1f}%, "
                   f"{a.get('plays', 0):.0f} jugadas por partido)")
    for pos in ("RB", "WR", "TE"):
        y = ctx.perfiles[opp].pos_defensa.get(f"{pos}.receiving_yards", 0) + \
            ctx.perfiles[opp].pos_defensa.get(f"{pos}.rushing_yards", 0)
        yl = ctx.liga_pos.get(f"{pos}.receiving_yards", 0) + ctx.liga_pos.get(f"{pos}.rushing_yards", 0)
        tds = ctx.perfiles[opp].pos_defensa.get(f"{pos}.receiving_tds", 0) + \
            ctx.perfiles[opp].pos_defensa.get(f"{pos}.rushing_tds", 0)
        tl = ctx.liga_pos.get(f"{pos}.receiving_tds", 0) + ctx.liga_pos.get(f"{pos}.rushing_tds", 0)
        if yl and (abs(y / yl - 1) >= 0.12 or (tl and abs(tds / tl - 1) >= 0.25)):
            out.append(f"{td} contra los {pos}: concede {y:.0f} yardas y {tds:.2f} TD por partido "
                       f"(liga {yl:.0f} y {tl:.2f})")
    return out


def primer_td(proys: list[Proyeccion]) -> dict[str, float]:
    total = sum(p.lambdas.get("tds", 0) for p in proys) + TD_DEFENSA_ESPECIALES
    p_alguno = 1 - math.exp(-total)
    return {p.jugador.player_id: p.lambdas.get("tds", 0) / total * p_alguno for p in proys} if total > 0 else {}


def primer_td_periodo(ctx: Contexto, proys: list[Proyeccion], periodo: str) -> dict[str, float]:
    """Primer (o último) TD de un periodo: P(hay alguno) × su parte de los TD esperados."""
    f = fraccion(ctx, "TD", periodo)
    total = (sum(p.lambdas.get("tds", 0) for p in proys) + TD_DEFENSA_ESPECIALES) * f
    p_alguno = 1 - math.exp(-total)
    return {p.jugador.player_id: p.lambdas.get("tds", 0) * f / total * p_alguno for p in proys} if total > 0 else {}


def analizar_partido(ctx: Contexto, game: dict, mercado: Mercado | None = None,
                     peso_mercado: float = PESO_MERCADO, simular_partido: bool = True) -> AnalisisPartido:
    home, away = game["home_team"], game["away_team"]
    linea = Linea(total=game.get("total_line"), spread_home=game.get("spread_line"))
    if mercado is not None:
        if mercado.total is not None:
            linea.total = mercado.total
        if mercado.spread_home is not None:
            linea.spread_home = mercado.spread_home
        linea.team_total = dict(mercado.team_total)
    entornos, proys, defensores = {}, [], []
    for team, opp, local in ((home, away, True), (away, home, False)):
        if team not in ctx.perfiles or opp not in ctx.perfiles:
            continue
        ent = entorno(ctx, team, opp, local, linea, game.get("wind"), game.get("roof"))
        entornos[team] = ent
        propios = [proyectar(ctx, j, ent) for j in preparar_equipo(ctx, team)]
        ajustar_tds(ctx, ent, propios)
        proys += propios
    for team, opp in ((home, away), (away, home)):
        if opp in entornos:
            defensores += [proyectar_defensa(ctx, j, entornos[opp]) for j in candidatos_defensa(ctx, team)]
    firsts = primer_td(proys)
    por_id = {p.jugador.player_id: p for p in proys + defensores}
    evaluaciones = []
    tds = []
    for p in proys:
        j = p.jugador
        lam = p.lambdas.get("tds", 0)
        if lam < 0.03:
            continue
        tds.append(TdJugador(game["game_id"], j.player_id, j.nombre, j.pos, j.team, p.entorno.opp, lam,
                             p_al_menos(lam, 1), p_al_menos(lam, 2), firsts.get(j.player_id, 0),
                             p.lambdas["rush_tds"], p.lambdas["rec_tds"], j.notas))
    tds.sort(key=lambda t: -t.lam)
    td_por_id = {t.player_id: t for t in tds}
    claves = {t: claves_enfrentamiento(ctx, t, e.opp) for t, e in entornos.items()}
    zona = {t: mapa_rz(ctx, e, proys) for t, e in entornos.items()}
    sim = None
    if simular_partido and len(entornos) == 2:
        sim = simular(ctx, home, away, semilla=zlib.crc32(game["game_id"].encode()), viento=game.get("wind"),
                      techo=game.get("roof"))
    pateadores = {}
    for lado, team in (("home", home), ("away", away)):
        k = pateador(ctx, team)
        if k:
            pateadores[k[0]] = (lado, team, k[1])
    if mercado is not None:
        primeros_periodo = {"game": firsts, "2h": primer_td_periodo(ctx, proys, "2h")}
        for of in mercado.ofertas:
            if of.tipo == "equipo":
                if sim is not None:
                    e = evaluar_equipo(ctx, game, sim, of, claves)
                    if e is not None:
                        evaluaciones.append(e)
                continue
            if of.player_id in pateadores and of.stat in ("fg", "xp", "kick_pts") and sim is not None:
                lado_k, team_k, nombre_k = pateadores[of.player_id]
                r = prob_pateador(sim, lado_k, of.stat, of.line, of.lado) if of.periodo == "game" else None
                if r and r[0] is not None:
                    opp_k = away if team_k == home else home
                    evaluaciones.append(_evaluacion_simple(
                        game, of, of.player_id, nombre_k, "K", team_k, opp_k, r[0], r[1], peso_mercado,
                        [f"simulación del partido: {r[1]:.2f} de media "
                         f"({sim.medias[lado_k]['fg']:.2f} goles de campo y {sim.medias[lado_k]['tds']:.2f} TD "
                         f"esperados de {equipos.apodo(team_k)})"]))
                continue
            p = por_id.get(of.player_id or "")
            if p is None:
                continue
            p_first = None
            if of.stat in ("first_td", "last_td"):
                p_first = primeros_periodo.get(of.periodo, {}).get(of.player_id)
            e = evaluar(ctx, p, of.stat, of.line, of.lado, of, peso_mercado, p_first, game["game_id"], of.periodo)
            if e is None:
                continue
            evaluaciones.append(e)
            t = td_por_id.get(of.player_id)
            if t and of.lado == "más" and of.periodo == "game":
                if of.stat == "tds" and of.line in (0.5, 1.5):
                    t.ofertas["1+" if of.line == 0.5 else "2+"] = e
                elif of.stat == "first_td":
                    t.ofertas["primero"] = e
    return AnalisisPartido(dict(game), entornos, proys, evaluaciones, tds, claves, mercado, sim, defensores, zona)


def _precio_caducado(e: Evaluacion) -> bool:
    """La mejor cuota paga más de 1.5 veces la de referencia: la menor entre el consenso y la cuota justa sin
    margen (cuando una sola casa ofrece la apuesta, su precio ES el consenso y solo la justa lo delata)."""
    refs = [x for x in (e.consenso, e.oferta.justa if e.oferta else None) if x]
    return bool(refs and e.odd and e.odd > 1.5 * min(refs))


def con_valor(partidos: list[AnalisisPartido], valor_min: float = 0.04, edge_min: float = 0.03,
              prob_min: float = 0.12, ratio_max: float = 1.6, discrepancia_max: float = 0.25) -> list[Evaluacion]:
    """Selecciones donde la probabilidad final paga más que la cuota (EV) y el modelo ve más que la casa.

    Se descartan los "chollos" imposibles: si el modelo ve más de 1.6 veces lo que ve la casa, lo normal es que
    al modelo le falte información (un suplente que no jugará, un rol que cambió), no que la casa se equivoque.
    Por lo mismo, tampoco entran las que difieren de la casa en más de 25 puntos, ni los precios de una casa que
    pagan más de 1.5 veces el consenso (suelen ser líneas caducadas que la casa no respetará).
    """
    out = [e for p in partidos for e in p.evaluaciones
           if e.ev is not None and e.ev >= valor_min and (e.edge or 0) >= edge_min and e.prob >= prob_min
           and e.prob_casa and e.prob_modelo / e.prob_casa <= ratio_max
           and abs(e.prob_modelo - e.prob_casa) <= discrepancia_max
           and not _precio_caducado(e)]
    return sorted(out, key=lambda e: -(e.ev or 0))


def mas_probables(partidos: list[AnalisisPartido], prob_min: float = 0.62, cuota_min: float = 1.30) -> list[Evaluacion]:
    out = [e for p in partidos for e in p.evaluaciones
           if e.prob >= prob_min and (e.odd or 0) >= cuota_min and (e.ev or 0) >= -0.02]
    return sorted(out, key=lambda e: -e.prob)


# --- Seguimiento ------------------------------------------------------------------------------

def guardar_picks(db: NflDB, fecha: str, evaluaciones: list[Evaluacion], origen: str = "informe") -> int:
    n = 0
    for e in evaluaciones:
        db.conn.execute(
            "INSERT OR REPLACE INTO nfl_picks(created_at, fecha, game_id, player_id, name, team, stat, line, lado, prob, "
            "prob_modelo, prob_casa, odd, book, ev, origen, razones) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, "
            "?, ?)",
            (now_iso(), fecha, e.game_id, e.player_id, e.nombre, e.team, e.codigo, e.line, e.lado, e.prob,
             e.prob_modelo, e.prob_casa, e.odd, e.book, e.ev, origen,
             json.dumps({"a_favor": e.razones.a_favor, "en_contra": e.razones.en_contra}, ensure_ascii=False)))
        n += 1
    db.commit()
    return n


def _cuartos(periodo: str) -> tuple[int, ...]:
    return {"game": (1, 2, 3, 4, 5), "1h": (1, 2), "2h": (3, 4, 5), "1q": (1,), "2q": (2,), "3q": (3,),
            "4q": (4,)}[periodo]


def resultado_equipo(conn, pk, game) -> float | None:
    """Valor real de un mercado de partido o equipo a partir de las anotaciones guardadas.

    Para ml/ml3way/sp devuelve la diferencia (equipo del pick menos rival); para sí/no y par/impar, 1 o 0 según
    se cumpla el lado; para el resto, el conteo del periodo. None si faltan datos."""
    stat_per, _, bet = pk["stat"].partition("/")
    stat, _, periodo = stat_per.partition("@")
    anot = conn.execute("SELECT * FROM nfl_anotaciones WHERE game_id = ? ORDER BY play_id",
                        (pk["game_id"],)).fetchall()
    if not anot and stat not in ("perdidas", "punts", "sacks"):
        return None
    home, away = game["home_team"], game["away_team"]
    qs = _cuartos(periodo or "game")
    en = [a for a in anot if (a["qtr"] or 0) in qs or (a["qtr"] or 0) > 5 and 5 in qs]
    pts = {home: sum(a["puntos"] for a in en if a["team"] == home), away: sum(a["puntos"] for a in en if a["team"] == away)}
    team = pk["player_id"]
    lado = pk["lado"]
    if stat == "pts":
        if bet in ("ml", "ml3way", "sp"):
            if lado == "draw":
                return float(pts[home] == pts[away])
            t = home if lado == "home" else away
            o = away if t == home else home
            return float(pts[t] - pts[o])
        total = pts.get(team, pts[home] + pts[away]) if team != "ALL" else pts[home] + pts[away]
        if bet == "eo":
            return float((total % 2 == 0) == (lado == "par"))
        if bet == "yn":
            return float((total > 0) == (lado == "sí"))
        return float(total)
    if stat in ("tds", "fg"):
        tipo = "TD" if stat == "tds" else "FG"
        n = sum(1 for a in en if a["tipo"] == tipo and (team == "ALL" or a["team"] == team))
        return float((n > 0) == (lado == "sí")) if bet == "yn" else float(n)
    if stat in ("primero", "ultimo"):
        if not en:
            return None                      # nadie anotó: se devuelve la apuesta
        quien = en[0]["team"] if stat == "primero" else en[-1]["team"]
        return float(quien == (home if lado == "home" else away))
    if stat == "ambos":
        return float((pts[home] > 0 and pts[away] > 0) == (lado == "sí"))
    if stat == "ventaja":
        return float(max((abs(a["home_score"] - a["away_score"]) for a in anot), default=0))
    if stat == "fg_largo":
        return float(max((a["distancia"] or 0 for a in anot if a["tipo"] == "FG"), default=0))
    if stat == "safety":
        hay = any(a["tipo"] == "SAF" and (team == "ALL" or a["team"] == team) for a in anot)
        return float(hay == (lado == "sí"))
    col = {"perdidas": "turnovers", "punts": "punts", "sacks": "sacks"}.get(stat)
    if col:
        filas = conn.execute(f"SELECT team, {col} FROM nfl_team_games WHERE game_id = ?", (pk["game_id"],)).fetchall()
        if not filas:
            return None
        if stat == "sacks" and team != "ALL":   # sacks de un equipo = los que sufre el ataque rival
            return float(sum(f[1] or 0 for f in filas if f[0] != team))
        return float(sum(f[1] or 0 for f in filas if team == "ALL" or f[0] == team))
    return None


def _acierto(pk, resultado: float) -> int | None:
    stat = pk["stat"]
    bet = stat.partition("/")[2]
    if stat.split("@")[0] in ("primero", "ultimo", "ambos", "safety"):
        return int(resultado == 1.0)
    if bet in ("ml", "ml3way"):
        if pk["lado"] == "draw":
            return int(resultado == 1.0)
        return None if resultado == 0 and bet == "ml" else int(resultado > 0)
    if bet == "sp":
        margen = resultado + pk["line"]
        return None if margen == 0 else int(margen > 0)
    if bet in ("eo", "yn") or stat.split("@")[0] in ("first_td", "last_td"):
        return int(resultado == 1.0)
    if resultado == pk["line"]:
        return None                          # push
    return int(resultado > pk["line"]) if pk["lado"] == "más" else int(resultado < pk["line"])


def liquidar(db: NflDB) -> int:
    """Liquida las selecciones de partidos ya jugados con las estadísticas reales."""
    n = 0
    pendientes = db.conn.execute(
        "SELECT p.*, g.home_team, g.away_team FROM nfl_picks p JOIN nfl_games g ON g.game_id = p.game_id "
        "WHERE p.settled_at IS NULL AND g.home_score IS NOT NULL").fetchall()
    for pk in pendientes:
        hay_datos = db.conn.execute("SELECT 1 FROM nfl_player_games WHERE game_id = ? LIMIT 1",
                                    (pk["game_id"],)).fetchone()
        if not hay_datos:
            continue
        stat_base, _, periodo = pk["stat"].partition("/")[0].partition("@")
        if "/" in pk["stat"]:
            resultado = resultado_equipo(db.conn, pk, pk)
            if resultado is None and not db.conn.execute("SELECT 1 FROM nfl_anotaciones WHERE game_id = ?",
                                                         (pk["game_id"],)).fetchone():
                continue                         # falta el jugada a jugada de ese partido
            acierto = None if resultado is None else _acierto(pk, resultado)
        else:
            fila = db.conn.execute(
                "SELECT pg.*, pp.long_rec, pp.long_rush, pp.long_pass FROM nfl_player_games pg "
                "LEFT JOIN nfl_player_pbp pp ON pp.game_id = pg.game_id AND pp.player_id = pg.player_id "
                "WHERE pg.game_id = ? AND pg.player_id = ?", (pk["game_id"], pk["player_id"])).fetchone()
            if fila is None:
                resultado, acierto = None, None      # no jugó: apuesta nula
            elif stat_base in ("first_td", "last_td"):
                tds = db.conn.execute(
                    "SELECT player_id, qtr FROM nfl_anotaciones WHERE game_id = ? AND tipo = 'TD' ORDER BY play_id",
                    (pk["game_id"],)).fetchall()
                if periodo == "2h":
                    tds = [t for t in tds if (t["qtr"] or 0) >= 3]
                if not tds:
                    primero = db.conn.execute("SELECT player_id FROM nfl_primer_td WHERE game_id = ?",
                                              (pk["game_id"],)).fetchone()
                    if primero is None and not db.conn.execute(
                            "SELECT 1 FROM nfl_anotaciones WHERE game_id = ?", (pk["game_id"],)).fetchone():
                        continue                 # falta el jugada a jugada de ese partido
                    tds = [primero] if primero and periodo != "2h" else []
                quien = (tds[0] if stat_base == "first_td" else tds[-1])["player_id"] if tds else None
                resultado = float(quien == pk["player_id"])
                acierto = int(resultado == 1.0) if pk["lado"] == "más" else int(resultado == 0.0)
            elif periodo:
                q = _cuartos(periodo)
                filas_q = db.conn.execute(
                    f"SELECT * FROM nfl_player_quarter WHERE game_id = ? AND player_id = ? AND qtr IN "
                    f"({', '.join('?' * len(q))})", (pk["game_id"], pk["player_id"], *q)).fetchall()
                suma = {}
                for f in filas_q:
                    for k in f.keys():
                        if k not in ("game_id", "player_id", "qtr"):
                            suma[k] = suma.get(k, 0) + (f[k] or 0)
                resultado = valor(suma, stat_base)
                acierto = _acierto(pk, resultado)
            else:
                resultado = valor(dict(fila), stat_base)
                acierto = _acierto(pk, resultado)
        db.conn.execute("UPDATE nfl_picks SET resultado = ?, acierto = ?, settled_at = ? WHERE id = ?",
                        (resultado, acierto, now_iso(), pk["id"]))
        n += 1
    db.commit()
    return n


TRAMOS = ((0.0, 0.2), (0.2, 0.35), (0.35, 0.5), (0.5, 0.6), (0.6, 0.7), (0.7, 0.8), (0.8, 1.01))


def rendimiento(db: NflDB) -> dict:
    filas = db.conn.execute("SELECT * FROM nfl_picks WHERE acierto IS NOT NULL").fetchall()

    def resumen(fs) -> dict | None:
        if not fs:
            return None
        con_cuota = [f for f in fs if f["odd"]]
        return {"n": len(fs), "acierto": sum(f["acierto"] for f in fs) / len(fs),
                "prob_media": sum(f["prob"] for f in fs) / len(fs), "con_cuota": len(con_cuota),
                "beneficio": sum((f["odd"] - 1) if f["acierto"] else -1 for f in con_cuota) if con_cuota else None}

    out = {"total": resumen(filas), "tramos": [], "stats": [], "origen": []}
    for lo, hi in TRAMOS:
        r = resumen([f for f in filas if lo <= f["prob"] < hi])
        if r:
            out["tramos"].append({"tramo": f"{lo * 100:.0f}-{min(hi, 1) * 100:.0f}%", **r})
    for stat in sorted({f["stat"] for f in filas}):
        out["stats"].append({"stat": stat, **resumen([f for f in filas if f["stat"] == stat])})
    for origen in sorted({f["origen"] for f in filas}):
        out["origen"].append({"origen": origen, **resumen([f for f in filas if f["origen"] == origen])})
    return out
