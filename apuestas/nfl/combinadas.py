"""Combinadas de la NFL con el criterio de las de la NBA (ver CLAUDE.md), su registro y su liquidación.

Tipos que se arman cada día:

- segura_a: líneas alternativas de jugadores constantes al 85 %+ (la más probable de cada partido).
- segura_b: la línea principal más probable de cada partido entre jugadores constantes.
- cuota_2 / 3 / 5 / 10: la combinación de jugadores constantes con más probabilidad de acertar todas cuya cuota
  llega al objetivo, con las menos patas posibles.
- valor_5 / 10 / 15: lo mismo, solo con props donde el modelo ve más de lo que paga la casa.
- racha_4: líneas que el jugador pasó en todos sus partidos de esta temporada (3+), con el modelo del mismo lado y
  el resto del análisis a favor.
- builder (uno por partido) y doble_builder.

Jugador constante: sin alertas (papel menor, vuelve de lesión, cambio de rol, traspaso reciente, en el parte de
lesiones, muy lejos de la casa), que pasó la línea en 7+ de sus últimos 10 y en el 60 %+ de esta temporada.

Un partido por pata cuando hay varios partidos; con uno solo (jueves, lunes) las patas son del mismo partido y la
probabilidad tiene en cuenta cuánto se mueven juntas (ver CORRELACIONES): las yardas de un QB y las de sus
receptores van muy juntas, y la casa lo cobra en su bet builder.
"""
from __future__ import annotations

import json
import math
import random
from dataclasses import dataclass, field
from itertools import combinations
from statistics import NormalDist

from ..db import now_iso
from .analizador import AnalisisPartido, Evaluacion
from .db import NflDB
from .modelo import NOMBRES, Contexto, Proyeccion, valor
from .razones import tendencias

OBJETIVOS = (2.0, 3.0, 5.0, 10.0)
OBJETIVOS_VALOR = (5.0, 10.0, 15.0)
MAX_PATAS = 6
CANDIDATAS_MAX = 16
PROB_SEGURA_A = 0.85
PROB_PIERNA_BUILDER = 0.72
PIERNAS_BUILDER = 4
ACIERTO_TEMPORADA_MIN = 0.67      # bet builders: líneas que esta temporada pasa en 2 de cada 3
BALANCE_RACHA = 2                 # menos factores que en la NBA: 2 más a favor que en contra
SIMULACIONES = 20000

# Correlación de los desvíos frente a su media (2024-2026, mismo partido). Clases: P = pase del QB, R = carrera
# del RB, C = yardas de recepción, N = recepciones / envíos.
CORRELACIONES = {
    ("mismo", "C", "P"): 0.37, ("mismo", "N", "P"): 0.26, ("mismo", "P", "R"): -0.13,
    ("rival", "P", "P"): 0.11, ("rival", "R", "R"): -0.17, ("rival", "C", "P"): 0.06,
}
CLASE = {"pass_yds": "P", "pass_att": "P", "comp": "P", "pass_rush_yds": "P", "pass_tds": "P",
         "rec_yds": "C", "long_rec": "C", "rush_rec_yds": "C", "rec": "N", "targets": "N"}
# Alertas que descartan en las seguras y en los builders; el cambio de rol no en las rachas (suele ser su causa).
DESCARTA = {"papel menor", "vuelve de lesión", "traspaso reciente", "en el parte de lesiones", "muy lejos de la casa",
            "cambio de rol"}
DESCARTA_RACHA = DESCARTA - {"cambio de rol"}
STATS_PATA = ("rec", "rec_yds", "targets", "rush_yds", "rush_att", "pass_yds", "pass_att", "comp", "pass_tds",
              "rush_rec_yds", "pass_rush_yds", "tds", "sacks", "tackles", "long_rec")


# --- Patas ---------------------------------------------------------------------------------------

@dataclass
class Pata:
    game_id: str
    partido: str
    player_id: str
    nombre: str
    team: str
    pos: str
    stat: str
    line: float
    side: str
    prob: float
    odd: float | None
    book: str | None = None
    acierto_10: tuple[int, int] = (0, 0)
    acierto_temporada: tuple[int, int] = (0, 0)
    alertas: list[str] = field(default_factory=list)
    balance: int = 0

    @property
    def etiqueta(self) -> str:
        if self.stat == "tds":
            return f"{self.nombre} {'anota' if self.side == 'más' else 'no anota'}" if self.line == 0.5 else \
                f"{self.nombre} {int(self.line + 0.5)}+ TD"
        return f"{self.nombre} {self.side} de {self.line:g} {NOMBRES.get(self.stat, self.stat)}"

    def json(self) -> dict:
        return {"game_id": self.game_id, "partido": self.partido, "player_id": self.player_id, "nombre": self.nombre,
                "team": self.team, "stat": self.stat, "line": self.line, "side": self.side, "prob": self.prob,
                "odd": self.odd, "book": self.book, "acierto_10": list(self.acierto_10),
                "acierto_temporada": list(self.acierto_temporada)}


def alertas(ctx: Contexto, proy: Proyeccion, prob_modelo: float | None = None,
            prob_casa: float | None = None) -> list[str]:
    """Lo que hace dudosa una prop aunque su probabilidad sea alta."""
    j = proy.jugador
    out = []
    if j.pos != "QB":
        snaps = [p.get("offense_pct") for p in j.con_equipo[:4] if p.get("offense_pct") is not None]
        if snaps and sorted(snaps)[len(snaps) // 2] < 0.5:
            out.append("papel menor")
    elif any("suplente" in n for n in j.notas):
        out.append("papel menor")
    # Vuelve de lesión: faltó a 2+ de los partidos de su equipo de esta temporada o al último.
    equipo = [f for f in ctx.ofensiva.get(j.team, []) if f["season"] == ctx.temporada]
    jugados = {p["game_id"] for p in j.con_equipo if p["season"] == ctx.temporada}
    if equipo and (len(equipo) - len(jugados) >= 2 or equipo[0]["game_id"] not in jugados) and jugados:
        out.append("vuelve de lesión")
    if any("sin " in n and "hoy juega" in n for n in j.notas) or any("más volumen por las bajas" in n for n in j.notas):
        out.append("cambio de rol")
    if j.llegada and len(j.con_equipo) < 3:
        out.append("traspaso reciente")
    if j.estado:
        out.append("en el parte de lesiones")
    if prob_modelo is not None and prob_casa is not None and abs(prob_modelo - prob_casa) > 0.15:
        out.append("muy lejos de la casa")
    return out


def _pata(ctx: Contexto, a: AnalisisPartido, e: Evaluacion) -> Pata | None:
    proy = next((p for p in a.proyecciones + a.defensores if p.jugador.player_id == e.player_id), None)
    if proy is None or e.tipo != "jugador" or e.periodo != "game" or e.stat not in STATS_PATA:
        return None
    t = tendencias(ctx, proy.jugador.partidos, e.stat, e.line, e.lado, e.opp)
    return Pata(a.game["game_id"], a.titulo, e.player_id, e.nombre, e.team, e.pos, e.stat, e.line, e.lado, e.prob,
                e.odd, e.book, t.aciertos_10, t.aciertos_temporada, alertas(ctx, proy, e.prob_modelo, e.prob_casa),
                len(e.razones.a_favor) - len(e.razones.en_contra))


def patas_del_dia(ctx: Contexto, partidos: list[AnalisisPartido]) -> list[Pata]:
    out = []
    for a in partidos:
        for e in a.evaluaciones:
            p = _pata(ctx, a, e)
            if p is not None:
                out.append(p)
    return out


def constante(p: Pata, min_10: int = 7, temporada_min: float = 0.6) -> bool:
    h10, n10 = p.acierto_10
    ht, nt = p.acierto_temporada
    return (not set(p.alertas) & DESCARTA and n10 >= 6 and h10 >= min_10 * n10 / 10
            and (nt < 2 or ht / nt >= temporada_min))


def candidatas_seguras(patas: list[Pata], cuota_min: float = 1.30, prob_min: float = 0.62) -> list[Pata]:
    out = [p for p in patas if p.odd and p.odd >= cuota_min and p.prob >= prob_min and constante(p)]
    return sorted(out, key=lambda p: (p.prob, p.acierto_10[0]), reverse=True)


def candidatas_valor(patas: list[Pata], valor_min: float = 0.02, prob_min: float = 0.55) -> list[Pata]:
    out = [p for p in patas if p.odd and p.prob >= prob_min and p.prob * p.odd - 1 >= valor_min
           and constante(p, min_10=6)]
    return sorted(out, key=lambda p: p.prob, reverse=True)


def candidatas_racha(patas: list[Pata], prob_min: float = 0.52) -> list[Pata]:
    out = []
    for p in patas:
        ht, nt = p.acierto_temporada
        if nt < 3 or ht < nt or not p.odd or p.prob < prob_min:
            continue
        if set(p.alertas) & DESCARTA_RACHA or p.acierto_10[0] < 6 or p.balance < BALANCE_RACHA:
            continue
        out.append(p)
    return sorted(out, key=lambda p: (p.prob, p.acierto_10[0]), reverse=True)


# --- Probabilidad conjunta con la correlación del partido -----------------------------------------

def _rho(a: Pata, b: Pata) -> float:
    if a.game_id != b.game_id or a.player_id == b.player_id:
        return 0.0 if a.player_id != b.player_id else 0.6
    ca, cb = CLASE.get(a.stat), CLASE.get(b.stat)
    if a.pos == "RB" and a.stat in ("rush_yds", "rush_att"):
        ca = "R"
    if b.pos == "RB" and b.stat in ("rush_yds", "rush_att"):
        cb = "R"
    if not ca or not cb:
        return 0.0
    rel = "mismo" if a.team == b.team else "rival"
    r = CORRELACIONES.get((rel,) + tuple(sorted((ca, cb))), 0.0)
    # Un "menos de" es el lado contrario del mismo desvío.
    return r * (1 if a.side == b.side else -1)


def _cholesky(m: list[list[float]]) -> list[list[float]] | None:
    n = len(m)
    L = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for k in range(i + 1):
            s = sum(L[i][x] * L[k][x] for x in range(k))
            if i == k:
                v = m[i][i] - s
                if v <= 0:
                    return None
                L[i][k] = math.sqrt(v)
            else:
                L[i][k] = (m[i][k] - s) / L[k][k]
    return L


def prob_conjunta(patas: list[Pata], sims: int = SIMULACIONES, semilla: int = 11) -> float:
    """Probabilidad de acertar todas con una cópula normal (correlaciones de CORRELACIONES)."""
    if len({p.game_id for p in patas}) == len(patas):
        return math.prod(p.prob for p in patas)
    n = len(patas)
    m = [[1.0 if i == k else _rho(patas[i], patas[k]) for k in range(n)] for i in range(n)]
    L = _cholesky(m)
    if L is None:
        return math.prod(p.prob for p in patas)
    normal = NormalDist()
    umbrales = [normal.inv_cdf(min(max(p.prob, 1e-6), 1 - 1e-6)) for p in patas]
    rng = random.Random(semilla)
    aciertos = 0
    for _ in range(sims):
        e = [rng.gauss(0, 1) for _ in range(n)]
        z = [sum(L[i][k] * e[k] for k in range(i + 1)) for i in range(n)]
        aciertos += all(zi < u for zi, u in zip(z, umbrales))
    return aciertos / sims


# --- Combinadas ----------------------------------------------------------------------------------------

@dataclass
class Combinada:
    tipo: str
    patas: list[Pata]
    prob: float

    @property
    def cuota(self) -> float | None:
        return None if any(p.odd is None for p in self.patas) else math.prod(p.odd for p in self.patas)

    @property
    def cuota_justa(self) -> float:
        return 1 / self.prob if self.prob else float("inf")

    @property
    def ev(self) -> float | None:
        return None if self.cuota is None else self.prob * self.cuota - 1


def _combinar(patas: list[Pata]) -> Combinada:
    return Combinada("", list(patas), prob_conjunta(list(patas), sims=4000))


def con_cuota(candidatas: list[Pata], objetivo: float, tipo: str, un_partido: bool) -> Combinada | None:
    """La combinación con más probabilidad de acertar todas cuya cuota llega al objetivo, con las menos patas.

    Con varios partidos, una pata por partido; con uno solo, como mucho dos patas por equipo y una por jugador."""
    pool = []
    usados: dict[str, int] = {}
    for p in candidatas:
        clave = p.team if un_partido else p.game_id
        if usados.get(clave, 0) < 2:
            usados[clave] = usados.get(clave, 0) + 1
            pool.append(p)
    pool = pool[:CANDIDATAS_MAX]
    for k in range(2, MAX_PATAS + 1):
        mejor = None
        for comb in combinations(pool, k):
            if len({p.player_id for p in comb}) < k:
                continue
            if not un_partido and len({p.game_id for p in comb}) < k:
                continue
            if un_partido and max(sum(p.team == t for p in comb) for t in {p.team for p in comb}) > 2:
                continue
            cuota = math.prod(p.odd for p in comb)
            if cuota < objetivo:
                continue
            prob_ind = math.prod(p.prob for p in comb)
            if mejor is None or prob_ind > mejor[0]:
                mejor = (prob_ind, comb)
        if mejor is not None:   # las menos patas posibles
            c = _combinar(mejor[1])
            c.tipo = f"{tipo}_{objetivo:g}"
            return c
    return None


def seguras_a(ctx: Contexto, partidos: list[AnalisisPartido], prob_min: float = PROB_SEGURA_A) -> list[Pata]:
    """Líneas alternativas ("más de" .5 más alta con prob >= 85 %) de jugadores sin alertas, que pasan en 8+ de
    sus últimos 10 y en 2 de cada 3 partidos de esta temporada. Sin cuota: se da la justa."""
    out = []
    for a in partidos:
        for proy in a.proyecciones:
            if alertas(ctx, proy):
                continue
            mejor = None
            for stat in ("rec", "rec_yds", "rush_yds", "rush_att", "pass_yds", "comp", "pass_tds"):
                if stat not in proy.medias or proy.medias[stat] < {"rec": 2.5, "rec_yds": 25, "rush_yds": 35,
                                                                     "rush_att": 9, "pass_yds": 180, "comp": 15,
                                                                     "pass_tds": 1.0}[stat]:
                    continue
                for k in range(int(proy.medias[stat]), -1, -1):
                    line = k + 0.5
                    p = proy.prob(stat, line)[0]
                    if p < prob_min:
                        continue
                    t = tendencias(ctx, proy.jugador.partidos, stat, line, "más", proy.entorno.opp)
                    h10, n10 = t.aciertos_10
                    ht, nt = t.aciertos_temporada
                    if n10 >= 6 and h10 >= 0.8 * n10 and (nt < 3 or ht >= ACIERTO_TEMPORADA_MIN * nt):
                        cand = Pata(a.game["game_id"], a.titulo, proy.jugador.player_id, proy.jugador.nombre,
                                    proy.jugador.team, proy.jugador.pos, stat, line, "más", p, None, None,
                                    t.aciertos_10, t.aciertos_temporada)
                        if mejor is None or cand.prob > mejor.prob:
                            mejor = cand
                    break
            if mejor:
                out.append(mejor)
    return sorted(out, key=lambda p: -p.prob)


def builder(ctx: Contexto, a: AnalisisPartido, n: int = PIERNAS_BUILDER) -> Combinada | None:
    """Bet builder del partido: las piernas alternativas más probables (>= 72 %), una por jugador, como mucho dos
    por equipo, con la probabilidad conjunta corregida por la correlación del partido."""
    candidatas = seguras_a(ctx, [a], prob_min=PROB_PIERNA_BUILDER)
    elegidas, por_equipo = [], {}
    for p in candidatas:
        if por_equipo.get(p.team, 0) >= 2:
            continue
        por_equipo[p.team] = por_equipo.get(p.team, 0) + 1
        elegidas.append(p)
        if len(elegidas) == n:
            break
    if len(elegidas) < 2:
        return None
    return Combinada("builder", elegidas, prob_conjunta(elegidas))


def del_dia(ctx: Contexto, partidos: list[AnalisisPartido]) -> list[Combinada]:
    patas = patas_del_dia(ctx, partidos)
    un_partido = len(partidos) == 1
    seguras = candidatas_seguras(patas)
    valor_ = candidatas_valor(patas)
    out: list[Combinada | None] = []
    alt = seguras_a(ctx, partidos)
    if un_partido:
        por_equipo, sel = {}, []
        for p in alt:
            if por_equipo.get(p.team, 0) < 2:
                por_equipo[p.team] = por_equipo.get(p.team, 0) + 1
                sel.append(p)
            if len(sel) == 3:
                break
    else:
        sel, vistos = [], set()
        for p in alt:
            if p.game_id not in vistos:
                vistos.add(p.game_id)
                sel.append(p)
            if len(sel) == 4:
                break
    if len(sel) >= 2:
        out.append(Combinada("segura_a", sel, prob_conjunta(sel)))
    if not un_partido:
        sel, vistos = [], set()
        for p in seguras:
            if p.game_id not in vistos:
                vistos.add(p.game_id)
                sel.append(p)
            if len(sel) == 4:
                break
        if len(sel) >= 2:
            out.append(Combinada("segura_b", sel, math.prod(p.prob for p in sel)))
    out += [con_cuota(seguras, o, "cuota", un_partido) for o in OBJETIVOS]
    out += [con_cuota(valor_, o, "valor", un_partido) for o in OBJETIVOS_VALOR]
    rachas = candidatas_racha(patas)
    sel, jugadores, por_clave = [], set(), {}
    for p in rachas:
        clave = p.team if un_partido else p.game_id
        if p.player_id in jugadores or por_clave.get(clave, 0) >= 2:
            continue
        jugadores.add(p.player_id)
        por_clave[clave] = por_clave.get(clave, 0) + 1
        sel.append(p)
        if len(sel) == 4:
            break
    if len(sel) >= 3:
        out.append(Combinada(f"racha_{len(sel)}", sel, prob_conjunta(sel)))
    builders = sorted([b for b in (builder(ctx, a) for a in partidos) if b], key=lambda b: -b.prob)
    out += builders
    if len(builders) >= 2:
        out.append(Combinada("doble_builder", builders[0].patas + builders[1].patas, builders[0].prob * builders[1].prob))
    vistos_t = set()
    final = []
    for c in out:
        if c is None:
            continue
        clave = (c.tipo, tuple((p.player_id, p.stat, p.line, p.side) for p in c.patas))
        if clave not in vistos_t:
            vistos_t.add(clave)
            final.append(c)
    return final


NOMBRES_TIPO = {"segura_a": "Combinada segura A (líneas alternativas)", "segura_b": "Combinada segura B (principales)",
                "builder": "Bet builder", "doble_builder": "Doble de bet builders"}


def nombre_tipo(tipo: str) -> str:
    if tipo.startswith("usuario:"):
        return "Tu apuesta: " + tipo.split(":", 1)[1]
    if tipo in NOMBRES_TIPO:
        return NOMBRES_TIPO[tipo]
    base, cuota = tipo.rsplit("_", 1)
    return {"cuota": f"Segura cuota {cuota}+", "valor": f"De valor cuota {cuota}+",
            "racha": f"Rachas de temporada ({cuota} patas)"}.get(base, tipo)


# --- Registro, liquidación y acumulado ---------------------------------------------------------------

def guardar(db: NflDB, fecha: str, combis: list[Combinada]) -> None:
    db.conn.execute("DELETE FROM nfl_combinadas WHERE fecha = ? AND result IS NULL AND tipo NOT LIKE 'usuario:%'",
                    (fecha,))
    db.conn.executemany(
        "INSERT INTO nfl_combinadas(fecha, tipo, patas, prob, cuota, created_at) VALUES (?, ?, ?, ?, ?, ?)",
        [(fecha, c.tipo, json.dumps([p.json() for p in c.patas], ensure_ascii=False), c.prob, c.cuota, now_iso())
         for c in combis])
    db.commit()


def resultado_pata(db: NflDB, x: dict) -> tuple[int | None, float | None]:
    """(1 acierto / 0 fallo / 2 anulada / None pendiente, valor real)."""
    g = db.conn.execute("SELECT home_score FROM nfl_games WHERE game_id = ?", (x["game_id"],)).fetchone()
    if g is None or g[0] is None or not db.conn.execute("SELECT 1 FROM nfl_player_games WHERE game_id = ? LIMIT 1",
                                                        (x["game_id"],)).fetchone():
        return None, None
    fila = db.conn.execute(
        "SELECT pg.*, pp.long_rec, pp.long_rush, pp.long_pass FROM nfl_player_games pg LEFT JOIN nfl_player_pbp pp "
        "ON pp.game_id = pg.game_id AND pp.player_id = pg.player_id WHERE pg.game_id = ? AND pg.player_id = ?",
        (x["game_id"], x["player_id"])).fetchone()
    if fila is None:
        return 2, None
    real = valor(dict(fila), x["stat"])
    if real == x["line"]:
        return 2, real
    return int((real > x["line"]) == (x["side"] == "más")), real


def liquidar(db: NflDB) -> int:
    n = 0
    for c in db.conn.execute("SELECT * FROM nfl_combinadas WHERE result IS NULL").fetchall():
        patas = json.loads(c["patas"])
        res = [resultado_pata(db, x)[0] for x in patas]
        if 0 in res:
            db.conn.execute("UPDATE nfl_combinadas SET result = 0, aciertos = ? WHERE id = ?",
                            (sum(r == 1 for r in res), c["id"]))
            n += 1
            continue
        if any(r is None for r in res):
            continue
        validas = [x for x, r in zip(patas, res) if r != 2]
        resultado = 2 if not validas else 1
        db.conn.execute("UPDATE nfl_combinadas SET result = ?, aciertos = ? WHERE id = ?",
                        (resultado, sum(r == 1 for r in res), c["id"]))
        n += 1
    db.commit()
    return n


def detalle(db: NflDB, fecha: str) -> list[dict]:
    out = []
    for c in db.conn.execute("SELECT * FROM nfl_combinadas WHERE fecha = ? ORDER BY id", (fecha,)).fetchall():
        patas = []
        for x in json.loads(c["patas"]):
            r, real = resultado_pata(db, x)
            patas.append({**x, "resultado": r, "real": real})
        out.append({"tipo": c["tipo"], "prob": c["prob"], "cuota": c["cuota"], "result": c["result"], "patas": patas})
    return out


def resumen(db: NflDB) -> list[dict]:
    grupos: dict[str, list] = {}
    for f in db.conn.execute("SELECT * FROM nfl_combinadas WHERE result IN (0, 1)"):
        clave = "usuario" if f["tipo"].startswith("usuario:") else f["tipo"].rsplit("_", 1)[0] \
            if f["tipo"].startswith(("cuota_", "valor_", "racha_")) else f["tipo"]
        grupos.setdefault(clave, []).append(f)
    out = []
    for tipo, filas in sorted(grupos.items()):
        con = [f for f in filas if f["cuota"]]
        out.append({"tipo": tipo, "n": len(filas), "ganadas": sum(f["result"] for f in filas),
                    "prob_media": sum(f["prob"] for f in filas) / len(filas),
                    "beneficio": sum((f["cuota"] - 1) if f["result"] else -1 for f in con) if con else None,
                    "con_cuota": len(con)})
    return out


def texto(c: Combinada) -> list[str]:
    cuota = f"cuota {c.cuota:.2f} (mejores casas de EE. UU.), " if c.cuota else ""
    ev = f", valor {c.ev * 100:+.0f}%" if c.ev is not None else ""
    lineas = [f"**{nombre_tipo(c.tipo)}** — acierta {c.prob * 100:.1f}% ({cuota}cuota justa {c.cuota_justa:.2f}{ev})"]
    for p in c.patas:
        h10, n10 = p.acierto_10
        ht, nt = p.acierto_temporada
        precio = f"{p.odd:.2f} en {p.book}" if p.odd else f"justa {1 / p.prob:.2f}"
        lineas.append(f"- {p.etiqueta} ({p.team}) — {p.prob * 100:.0f}%, {precio}; pasó {h10}/{n10} últimos, "
                      f"{ht}/{nt} esta temporada")
    return lineas
