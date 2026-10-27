"""Combinadas por probabilidad, su registro diario y la liquidación con los resultados reales.

Tipos que se guardan cada día (todas "fantasma" hasta que el sistema esté calibrado):

- alternas: el pick seguro más probable de cada partido (líneas alternativas de titulares estables).
- principales: la línea principal más probable de cada partido entre jugadores constantes.
- cuota_2 / cuota_3 / cuota_5: la combinación de líneas principales de jugadores constantes con mayor
  probabilidad de acertar todas cuya cuota llega al objetivo.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from itertools import combinations

from ..db import now_iso
from .analizador import Partido, combinada_segura
from .db import NbaDB
from .modelo import Evaluacion, Segura, valor

OBJETIVOS = (2.0, 3.0, 5.0)
MAX_SELECCIONES = 5
CANDIDATAS_MAX = 16


@dataclass
class Combinada:
    tipo: str
    patas: list[dict] = field(default_factory=list)   # game_id, partido, player_id, nombre, stat, line, side, prob, odd

    @property
    def prob(self) -> float:
        p = 1.0
        for x in self.patas:
            p *= x["prob"]
        return p

    @property
    def cuota(self) -> float | None:
        if any(x["odd"] is None for x in self.patas):
            return None
        c = 1.0
        for x in self.patas:
            c *= x["odd"]
        return c


def _pata_prop(p: Partido, e: Evaluacion) -> dict:
    return {"game_id": p.game["id"], "partido": p.titulo, "player_id": e.player_id, "nombre": e.nombre,
            "stat": e.stat, "line": e.line, "side": e.lado, "prob": e.prob, "odd": e.odd}


def _pata_segura(p: Partido, s: Segura) -> dict:
    return {"game_id": p.game["id"], "partido": p.titulo, "player_id": s.player_id, "nombre": s.nombre,
            "stat": s.stat, "line": s.line, "side": "más", "prob": s.prob, "odd": None}


def alternas(partidos: list[Partido], n: int = 4) -> Combinada | None:
    mejores = sorted(((p, p.seguras[0]) for p in partidos if p.seguras), key=lambda x: -x[1].prob)[:n]
    return Combinada("alternas", [_pata_segura(p, s) for p, s in mejores]) if len(mejores) >= 2 else None


def principales(candidatas: list[tuple[Partido, Evaluacion]], n: int = 4) -> Combinada | None:
    elegidas = combinada_segura(candidatas, n)
    return Combinada("principales", [_pata_prop(p, e) for p, e in elegidas]) if len(elegidas) >= 2 else None


def con_cuota(candidatas: list[tuple[Partido, Evaluacion]], objetivo: float) -> Combinada | None:
    """La combinación de partidos distintos con más probabilidad de acertar todas y cuota >= objetivo."""
    # La mejor candidata de cada partido y, como alternativa, la segunda: así hay donde elegir sin repetir partido.
    por_partido: dict[str, list] = {}
    for p, e in candidatas:
        por_partido.setdefault(p.game["id"], [])
        if len(por_partido[p.game["id"]]) < 2:
            por_partido[p.game["id"]].append((p, e))
    pool = sorted((x for v in por_partido.values() for x in v), key=lambda x: -x[1].prob)[:CANDIDATAS_MAX]
    mejor = None
    for k in range(2, MAX_SELECCIONES + 1):
        for comb in combinations(pool, k):
            if len({p.game["id"] for p, _ in comb}) < k:
                continue
            cuota = prob = 1.0
            for _, e in comb:
                cuota *= e.odd
                prob *= e.prob
            if cuota >= objetivo and (mejor is None or prob > mejor[0]):
                mejor = (prob, comb)
    if mejor is None:
        return None
    return Combinada(f"cuota_{objetivo:g}", [_pata_prop(p, e) for p, e in mejor[1]])


def del_dia(partidos: list[Partido], candidatas: list[tuple[Partido, Evaluacion]]) -> list[Combinada]:
    out = [alternas(partidos), principales(candidatas)] + [con_cuota(candidatas, o) for o in OBJETIVOS]
    return [c for c in out if c]


# --- Registro y liquidación ----------------------------------------------------------

def guardar(db: NbaDB, fecha: str, combis: list[Combinada]) -> None:
    db.conn.execute("DELETE FROM nba_combinadas WHERE fecha = ? AND result IS NULL", (fecha,))
    db.conn.executemany(
        "INSERT INTO nba_combinadas(fecha, tipo, patas, prob, cuota, created_at) VALUES (?, ?, ?, ?, ?, ?)",
        [(fecha, c.tipo, json.dumps(c.patas, ensure_ascii=False), c.prob, c.cuota, now_iso()) for c in combis])
    db.commit()


def _resultado_pata(db: NbaDB, x: dict) -> int | None:
    """1 acierto, 0 fallo, 2 anulada (no jugó o empate exacto), None si el partido no ha terminado."""
    if not db.game_done(x["game_id"]):
        return None
    fila = db.conn.execute("SELECT * FROM nba_player_games WHERE game_id = ? AND player_id = ?",
                           (x["game_id"], x["player_id"])).fetchone()
    if fila is None:
        return 2
    actual = valor(dict(fila), x["stat"])
    if actual == x["line"]:
        return 2
    return int((actual > x["line"]) == (x["side"] == "más"))


def liquidar(db: NbaDB) -> int:
    """Una combinada gana si aciertan todas sus patas; las anuladas se quitan (como en las casas)."""
    n = 0
    for c in db.conn.execute("SELECT * FROM nba_combinadas WHERE result IS NULL").fetchall():
        patas = json.loads(c["patas"])
        res = [_resultado_pata(db, x) for x in patas]
        if any(r is None for r in res):
            continue
        validas = [(x, r) for x, r in zip(patas, res) if r != 2]
        if not validas:
            resultado, cuota = 2, c["cuota"]
        else:
            resultado = int(all(r == 1 for _, r in validas))
            cuota = None if c["cuota"] is None else _producto(x["odd"] for x, _ in validas)
        db.conn.execute("UPDATE nba_combinadas SET result = ?, cuota_final = ?, aciertos = ? WHERE id = ?",
                        (resultado, cuota, sum(r == 1 for _, r in validas), c["id"]))
        n += 1
    db.commit()
    return n


def _producto(valores) -> float:
    p = 1.0
    for v in valores:
        p *= v
    return p


def resumen(db: NbaDB) -> list[dict]:
    out = []
    for tipo, filas in _por_tipo(db).items():
        n = len(filas)
        con_cuota = [f for f in filas if f["cuota_final"]]
        out.append({"tipo": tipo, "n": n, "ganadas": sum(f["result"] for f in filas),
                    "prob_media": sum(f["prob"] for f in filas) / n,
                    "beneficio": sum((f["cuota_final"] - 1) if f["result"] else -1 for f in con_cuota)
                    if con_cuota else None, "con_cuota": len(con_cuota)})
    return out


def _por_tipo(db: NbaDB) -> dict[str, list]:
    out: dict[str, list] = {}
    for f in db.conn.execute("SELECT * FROM nba_combinadas WHERE result IN (0, 1) ORDER BY tipo"):
        out.setdefault(f["tipo"], []).append(f)
    return out


# --- ¿Listo para dinero real? ----------------------------------------------------------

MIN_PICKS = 150          # por tipo (props y seguras)
MIN_COMBINADAS = 30
MIN_DIAS = 21
TOLERANCIA = 0.02        # el acierto real puede quedar como mucho 2 puntos por debajo de lo prometido


def listo(db: NbaDB) -> list[tuple[str, bool, str]]:
    """Criterios para pasar de picks de prueba a dinero real: (criterio, cumple, detalle)."""
    out = []
    dias = db.conn.execute("SELECT COUNT(DISTINCT fecha) FROM nba_picks WHERE result IN (0, 1)").fetchone()[0]
    out.append(("Días con picks liquidados", dias >= MIN_DIAS, f"{dias} de {MIN_DIAS}"))
    for tipo, nombre in (("prop", "Props de línea principal"), ("segura", "Picks seguros")):
        f = db.conn.execute("""SELECT COUNT(*), AVG(result), AVG(prob) FROM nba_picks
                               WHERE result IN (0, 1) AND tipo = ?""", (tipo,)).fetchone()
        n, acierto, prob = f[0], f[1] or 0, f[2] or 0
        out.append((f"{nombre}: muestra", n >= MIN_PICKS, f"{n} de {MIN_PICKS}"))
        out.append((f"{nombre}: aciertan lo prometido", n > 0 and acierto >= prob - TOLERANCIA,
                    f"acierto {acierto * 100:.1f}% vs prometido {prob * 100:.1f}%" if n else "sin datos"))
    f = db.conn.execute("""SELECT COUNT(*), SUM(CASE WHEN result = 1 THEN odd - 1 ELSE -1 END) FROM nba_picks
                           WHERE result IN (0, 1) AND tipo = 'prop' AND odd IS NOT NULL""").fetchone()
    out.append(("Props con cuota: beneficio positivo", (f[1] or 0) > 0, f"{f[1] or 0:+.2f} u en {f[0]}"))
    combis = db.conn.execute("SELECT COUNT(*), AVG(result), AVG(prob) FROM nba_combinadas WHERE result IN (0, 1)"
                             ).fetchone()
    n, ganadas, prob = combis[0], combis[1] or 0, combis[2] or 0
    out.append(("Combinadas: muestra", n >= MIN_COMBINADAS, f"{n} de {MIN_COMBINADAS}"))
    out.append(("Combinadas: ganan lo prometido", n > 0 and ganadas >= prob - TOLERANCIA,
                f"ganadas {ganadas * 100:.1f}% vs prometido {prob * 100:.1f}%" if n else "sin datos"))
    return out
