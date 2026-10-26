"""Analiza cada partido: proyecciones, tabla de touchdowns, cruce con el mercado y selecciones con valor."""
from __future__ import annotations

import json
import math
from dataclasses import dataclass, field

from ..db import now_iso
from . import equipos
from .db import NflDB
from .mercado import Mercado, Oferta
from .modelo import (NOMBRES, Contexto, Entorno, Linea, Proyeccion, entorno, p_al_menos, preparar_equipo,
                     proyectar, rango, texto_rango, valor)
from .razones import Razones, razones

PESO_MERCADO = 0.35            # peso de la probabilidad de la casa (sin margen) en la probabilidad final
PESO_MERCADO_DUDOSO = 0.6      # si el jugador acaba de llegar, tiene poca muestra o está en duda
# Cuando modelo y casa discrepan mucho, casi siempre la casa sabe algo que los datos aún no muestran (un cambio
# de rol, una lesión, quién vuelve). Con más de 15 puntos de diferencia la casa pesa 0.6; con más de 25, 0.75.
DISCREPANCIA = ((0.25, 0.75), (0.15, 0.6))
TD_DEFENSA_ESPECIALES = 0.12   # TD por partido de defensa y equipos especiales (cuentan para el "primer TD")


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

    @property
    def edge(self) -> float | None:
        return None if self.prob_casa is None else self.prob_modelo - self.prob_casa

    def etiqueta(self) -> str:
        if self.stat == "first_td":
            return f"{self.nombre} primer TD del partido"
        if self.stat == "tds":
            k = int(self.line + 0.5)
            return f"{self.nombre} {'anota' if k == 1 else f'{k}+ TD'}" if self.lado == "más" else \
                f"{self.nombre} no anota" if k == 1 else f"{self.nombre} menos de {k} TD"
        return f"{self.nombre} {self.lado} de {self.line:g} {NOMBRES.get(self.stat, self.stat)}"


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
            peso_mercado: float = PESO_MERCADO, p_first: float | None = None, game_id: str = "") -> Evaluacion | None:
    j, ent = proy.jugador, proy.entorno
    if stat == "first_td":
        if p_first is None:
            return None
        p_mod, mu = p_first, p_first
    elif stat in proy.medias:
        mas, menos = proy.prob(stat, line)
        p_mod, mu = (mas if lado == "más" else menos), proy.medias[stat]
    else:
        return None
    p_casa = oferta.prob_casa() if oferta else None
    prob = p_mod if p_casa is None else (1 - (w := _peso_mercado(proy, peso_mercado, p_mod, p_casa))) * p_mod \
        + w * p_casa
    book, odd = oferta.mejor if oferta else (None, None)
    ev = prob * odd - 1 if odd else None
    r = razones(ctx, proy, stat, line, lado, oferta, p_mod, p_casa)
    return Evaluacion(game_id, j.player_id, j.nombre, j.pos, j.team, ent.opp, stat, line, lado, prob, p_mod, p_casa,
                      mu, odd, book, oferta.consenso if oferta else None, ev, r, oferta)


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


def analizar_partido(ctx: Contexto, game: dict, mercado: Mercado | None = None,
                     peso_mercado: float = PESO_MERCADO) -> AnalisisPartido:
    home, away = game["home_team"], game["away_team"]
    linea = Linea(total=game.get("total_line"), spread_home=game.get("spread_line"))
    if mercado is not None:
        if mercado.total is not None:
            linea.total = mercado.total
        if mercado.spread_home is not None:
            linea.spread_home = mercado.spread_home
        linea.team_total = dict(mercado.team_total)
    entornos, proys = {}, []
    for team, opp, local in ((home, away, True), (away, home, False)):
        if team not in ctx.perfiles or opp not in ctx.perfiles:
            continue
        ent = entorno(ctx, team, opp, local, linea, game.get("wind"), game.get("roof"))
        entornos[team] = ent
        proys += [proyectar(ctx, j, ent) for j in preparar_equipo(ctx, team)]
    firsts = primer_td(proys)
    por_id = {p.jugador.player_id: p for p in proys}
    evaluaciones = []
    tds = []
    for p in proys:
        j = p.jugador
        lam = p.lambdas.get("tds", 0)
        if lam < 0.03:
            continue
        tds.append(TdJugador(game["game_id"], j.player_id, j.nombre, j.pos, j.team, p.entorno.opp, lam, p_al_menos(lam, 1),
                             p_al_menos(lam, 2), firsts.get(j.player_id, 0), p.lambdas["rush_tds"],
                             p.lambdas["rec_tds"], j.notas))
    tds.sort(key=lambda t: -t.lam)
    td_por_id = {t.player_id: t for t in tds}
    if mercado is not None:
        for of in mercado.ofertas:
            p = por_id.get(of.player_id or "")
            if p is None:
                continue
            e = evaluar(ctx, p, of.stat, of.line, of.lado, of, peso_mercado, firsts.get(of.player_id),
                        game["game_id"])
            if e is None:
                continue
            evaluaciones.append(e)
            t = td_por_id.get(of.player_id)
            if t and of.lado == "más":
                if of.stat == "tds" and of.line in (0.5, 1.5):
                    t.ofertas["1+" if of.line == 0.5 else "2+"] = e
                elif of.stat == "first_td":
                    t.ofertas["primero"] = e
    claves = {t: claves_enfrentamiento(ctx, t, e.opp) for t, e in entornos.items()}
    return AnalisisPartido(dict(game), entornos, proys, evaluaciones, tds, claves, mercado)


def con_valor(partidos: list[AnalisisPartido], valor_min: float = 0.04, edge_min: float = 0.03,
              prob_min: float = 0.12, ratio_max: float = 1.6, discrepancia_max: float = 0.25) -> list[Evaluacion]:
    """Selecciones donde la probabilidad final paga más que la cuota (EV) y el modelo ve más que la casa.

    Se descartan los "chollos" imposibles: si el modelo ve más de 1.6 veces lo que ve la casa, lo normal es que
    al modelo le falte información (un suplente que no jugará, un rol que cambió), no que la casa se equivoque.
    Por lo mismo, tampoco entran las que difieren de la casa en más de 25 puntos.
    """
    out = [e for p in partidos for e in p.evaluaciones
           if e.ev is not None and e.ev >= valor_min and (e.edge or 0) >= edge_min and e.prob >= prob_min
           and e.prob_casa and e.prob_modelo / e.prob_casa <= ratio_max
           and abs(e.prob_modelo - e.prob_casa) <= discrepancia_max]
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
            (now_iso(), fecha, e.game_id, e.player_id, e.nombre, e.team, e.stat, e.line, e.lado, e.prob,
             e.prob_modelo, e.prob_casa, e.odd, e.book, e.ev, origen,
             json.dumps({"a_favor": e.razones.a_favor, "en_contra": e.razones.en_contra}, ensure_ascii=False)))
        n += 1
    db.commit()
    return n


def liquidar(db: NflDB) -> int:
    """Liquida las selecciones de partidos ya jugados con las estadísticas reales."""
    n = 0
    pendientes = db.conn.execute(
        "SELECT p.* FROM nfl_picks p JOIN nfl_games g ON g.game_id = p.game_id "
        "WHERE p.settled_at IS NULL AND g.home_score IS NOT NULL").fetchall()
    for pk in pendientes:
        hay_datos = db.conn.execute("SELECT 1 FROM nfl_player_games WHERE game_id = ? LIMIT 1",
                                    (pk["game_id"],)).fetchone()
        if not hay_datos:
            continue
        fila = db.conn.execute(
            "SELECT pg.*, pp.long_rec, pp.long_rush FROM nfl_player_games pg LEFT JOIN nfl_player_pbp pp "
            "ON pp.game_id = pg.game_id AND pp.player_id = pg.player_id WHERE pg.game_id = ? AND pg.player_id = ?",
            (pk["game_id"], pk["player_id"])).fetchone()
        if fila is None:
            resultado, acierto = None, None   # no jugó: apuesta nula
        elif pk["stat"] == "first_td":
            primero = db.conn.execute("SELECT player_id FROM nfl_primer_td WHERE game_id = ?",
                                      (pk["game_id"],)).fetchone()
            if primero is None:
                continue                      # falta el jugada a jugada de ese partido
            resultado = float(primero[0] == pk["player_id"])
            acierto = int(resultado == 1.0)
        else:
            resultado = valor(dict(fila), pk["stat"])
            acierto = int(resultado > pk["line"]) if pk["lado"] == "más" else int(resultado < pk["line"])
            if resultado == pk["line"]:
                acierto = None                # push
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
