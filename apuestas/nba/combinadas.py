"""Combinadas por probabilidad, su registro diario y la liquidación con los resultados reales.

Tipos que se guardan cada día (todas "fantasma" hasta que el sistema esté calibrado):

- alternas: el pick seguro más probable de cada partido (líneas alternativas de titulares estables).
- principales: la línea principal más probable de cada partido entre jugadores constantes.
- cuota_2 / cuota_3 / cuota_5 / cuota_10 / cuota_15: la combinación de líneas principales de jugadores constantes con mayor
  probabilidad de acertar todas cuya cuota llega al objetivo.
- valor_5 / valor_10 / valor_15 / valor_30: lo mismo, pero solo con props donde el modelo ve más probabilidad de la
  que paga la casa (valor > +2 %). Las más seguras suelen tener valor negativo (la casa también las ve
  seguras y paga poco); se registran ambas para ver con resultados reales cuál gana dinero.
- racha_4 / racha_8: líneas principales que el jugador pasó en todos sus partidos de esta temporada (3+), con el
  modelo del mismo lado. Backtest al inicio de 2025-26 (25 oct - 20 nov, línea = mediana de sus últimos 10):
  esas props acertaron el 78 % (n = 361) cuando el modelo decía 68 %; las de 0 de N, el 25 % frente al 30 %. Se
  permiten dos patas del mismo partido, como en los bet builders. Además, el resto del análisis (minutos, forma,
  defensa, altura, ritmo, historial contra el rival, últimos 10, marcaje) tiene que estar a favor: al menos
  BALANCE_RACHA factores más a favor que en contra. En el mismo backtest, con los filtros de abajo, las de balance
  3+ acertaron el 86 % (n = 209) y las de menos, el 62 % (n = 40).
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from itertools import combinations

from ..db import now_iso
from .analizador import Partido, combinada_segura
from .db import NbaDB
from .modelo import Evaluacion, Segura, valor

OBJETIVOS = (2.0, 3.0, 5.0, 10.0, 15.0)
MAX_SELECCIONES = 8
CANDIDATAS_MAX = 18


@dataclass
class Combinada:
    tipo: str
    patas: list[dict] = field(default_factory=list)   # game_id, partido, player_id, nombre, stat, line, side, prob, odd
    prob_fija: float | None = None                    # bet builders: probabilidad con la correlación del partido

    @property
    def prob(self) -> float:
        if self.prob_fija is not None:
            return self.prob_fija
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
            "stat": e.stat, "line": e.line, "side": e.lado, "prob": e.prob, "odd": e.odd,
            "defensa": e.defensa, "acierto_10": list(e.acierto_10), "acierto_temporada": list(e.acierto_temporada),
            "a_favor": sum(r.startswith("✅") for r in getattr(e, "razones", [])),
            "en_contra": sum(r.startswith("❌") for r in getattr(e, "razones", []))}


def _pata_segura(p: Partido, s: Segura) -> dict:
    return {"game_id": p.game["id"], "partido": p.titulo, "player_id": s.player_id, "nombre": s.nombre,
            "stat": s.stat, "line": s.line, "side": "más", "prob": s.prob, "odd": None}


def alternas(partidos: list[Partido], n: int = 4) -> Combinada | None:
    mejores = sorted(((p, p.seguras[0]) for p in partidos if p.seguras), key=lambda x: -x[1].prob)[:n]
    return Combinada("alternas", [_pata_segura(p, s) for p, s in mejores]) if len(mejores) >= 2 else None


def principales(candidatas: list[tuple[Partido, Evaluacion]], n: int = 4) -> Combinada | None:
    elegidas = combinada_segura(candidatas, n)
    return Combinada("principales", [_pata_prop(p, e) for p, e in elegidas]) if len(elegidas) >= 2 else None


def candidatas_valor(partidos: list[Partido], valor_min: float = 0.02, prob_min: float = 0.55,
                     min_aciertos: int = 6) -> list[tuple[Partido, Evaluacion]]:
    """Props donde el modelo ve más probabilidad que la que paga la casa, sin alertas y que la habrían
    pasado en al menos 6 de sus últimos 10."""
    out = []
    for p in partidos:
        for e in p.evaluaciones:
            if e.alertas or not e.odd or e.prob < prob_min or e.prob * e.odd - 1 < valor_min:
                continue
            if e.acierto_10[1] < 8 or e.acierto_10[0] < min_aciertos:
                continue
            out.append((p, e))
    return sorted(out, key=lambda x: x[1].prob, reverse=True)


def con_cuota(candidatas: list[tuple[Partido, Evaluacion]], objetivo: float, tipo: str = "cuota") -> Combinada | None:
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
    return Combinada(f"{tipo}_{objetivo:g}", [_pata_prop(p, e) for p, e in mejor[1]])


OBJETIVOS_VALOR = (5.0, 10.0, 15.0, 30.0)

RACHA_MIN_PARTIDOS = 3
RACHA_STATS = ("points", "rebounds", "assists", "threes", "pra", "pr", "pa", "ra")   # las del backtest
# "cambio de rol" y "traspaso reciente" no descartan: a menudo son justo la causa de la racha.
RACHA_DESCARTA = {"suplente", "minutos inestables", "en el parte de lesiones", "muy lejos de la casa",
                  "menos de una estrella al inicio de temporada"}
BALANCE_RACHA = 3


def balance(e: Evaluacion) -> int:
    """Factores del análisis a favor del lado elegido menos los que van en contra."""
    return sum(r.startswith("✅") for r in e.razones) - sum(r.startswith("❌") for r in e.razones)


def candidatas_racha(partidos: list[Partido], prob_min: float = 0.52, min_aciertos: int = 6
                     ) -> list[tuple[Partido, Evaluacion]]:
    """Props con cuota que el jugador pasó en todos sus partidos de esta temporada (al menos 3) y con el resto
    del análisis a favor."""
    out = []
    for p in partidos:
        for e in p.evaluaciones:
            hits, n = e.acierto_temporada
            if n < RACHA_MIN_PARTIDOS or hits < n or e.stat not in RACHA_STATS or not e.odd:
                continue
            if e.prob < prob_min or e.acierto_10[0] < min_aciertos or set(e.alertas) & RACHA_DESCARTA:
                continue
            if balance(e) < BALANCE_RACHA:
                continue
            out.append((p, e))
    return sorted(out, key=lambda x: (x[1].prob, x[1].acierto_10[0]), reverse=True)


def de_rachas(candidatas: list[tuple[Partido, Evaluacion]], n: int, por_partido: int = 2) -> Combinada | None:
    """Las n más probables, una por jugador y como mucho dos por partido."""
    elegidas, jugadores, partidos = [], set(), {}
    for p, e in candidatas:
        if e.player_id in jugadores or partidos.get(p.game["id"], 0) >= por_partido:
            continue
        jugadores.add(e.player_id)
        partidos[p.game["id"]] = partidos.get(p.game["id"], 0) + 1
        elegidas.append((p, e))
        if len(elegidas) == n:
            # Los factores que cuentan (sin la descomposición de cómo produce, que es neutra).
            return Combinada(f"racha_{n}", [{**_pata_prop(p, e), "razones": [
                r for r in e.razones if not r.startswith("➖ Cómo produce")]} for p, e in elegidas])
    return None


def del_dia(partidos: list[Partido], candidatas: list[tuple[Partido, Evaluacion]]) -> list[Combinada]:
    """Seguras (las más probables) y de valor (cuota mejor que su riesgo): se registran las dos para
    comparar con resultados reales cuál conviene jugar."""
    valor = candidatas_valor(partidos)
    out = [alternas(partidos), principales(candidatas)] + [con_cuota(candidatas, o) for o in OBJETIVOS]
    out += [con_cuota(valor, o, "valor") for o in OBJETIVOS_VALOR]
    rachas = candidatas_racha(partidos)
    out += [de_rachas(rachas, 4), de_rachas(rachas, 8)]
    return [c for c in out if c]


def de_builders(builders: list, doble) -> list[Combinada]:
    """Bet builders del día (uno por partido) y la doble de los dos más probables."""
    def patas(b) -> list[dict]:
        return [{"game_id": b.partido.game["id"], "partido": b.partido.titulo, "player_id": x.player_id,
                 "nombre": x.nombre, "stat": x.stat, "line": x.line, "side": "más", "prob": x.prob, "odd": None}
                for x in b.piernas]
    out = [Combinada("builder", patas(b), b.prob) for b in builders]
    if doble:
        out.append(Combinada("doble_builder", patas(doble[0]) + patas(doble[1]), doble[0].prob * doble[1].prob))
    return out


# --- Registro y liquidación ----------------------------------------------------------

def guardar(db: NbaDB, fecha: str, combis: list[Combinada]) -> None:
    # Las apuestas del usuario (tipo "usuario:...") no son del sistema: no se borran al regenerar el día.
    db.conn.execute("DELETE FROM nba_combinadas WHERE fecha = ? AND result IS NULL AND tipo NOT LIKE 'usuario:%'",
                    (fecha,))
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
        if 0 in res:
            # Una pierna perdida ya decide la combinada, aunque falten partidos por terminar.
            db.conn.execute("UPDATE nba_combinadas SET result = 0, cuota_final = cuota, aciertos = ? WHERE id = ?",
                            (sum(r == 1 for r in res), c["id"]))
            n += 1
            continue
        if any(r is None for r in res):
            continue
        validas = [(x, r) for x, r in zip(patas, res) if r != 2]
        if not validas:
            resultado, cuota = 2, c["cuota"]
        else:
            resultado = int(all(r == 1 for _, r in validas))
            if c["cuota"] is None or any(x["odd"] is None for x, _ in validas):
                cuota = c["cuota"]   # bet builders del usuario: la cuota es la de la casa, no el producto
            else:
                cuota = _producto(x["odd"] for x, _ in validas)
        db.conn.execute("UPDATE nba_combinadas SET result = ?, cuota_final = ?, aciertos = ? WHERE id = ?",
                        (resultado, cuota, sum(r == 1 for _, r in validas), c["id"]))
        n += 1
    db.commit()
    return n


NOMBRES_TIPO = {
    "alternas": "Combinada segura A (alternas)", "principales": "Combinada segura B (principales)",
    "builder": "Bet builder", "doble_builder": "Doble de bet builders",
}


def nombre_tipo(tipo: str) -> str:
    if tipo.startswith("usuario:"):
        return "Tu apuesta: " + tipo.split(":", 1)[1]
    if tipo == "usuario":
        return "Tus apuestas"
    if tipo in NOMBRES_TIPO:
        return NOMBRES_TIPO[tipo]
    base, cuota = tipo.rsplit("_", 1)
    if base == "racha":
        return f"Rachas de temporada ({cuota} patas)"
    return f"{'Segura' if base == 'cuota' else 'De valor'} cuota {cuota}+"


def detalle(db: NbaDB, fecha: str) -> list[dict]:
    """Las combinadas de un día con el resultado de cada pierna (valor real, ✅/❌/anulada/pendiente)."""
    out = []
    for c in db.conn.execute("SELECT * FROM nba_combinadas WHERE fecha = ? ORDER BY id", (fecha,)).fetchall():
        patas = []
        for x in json.loads(c["patas"]):
            fila = db.conn.execute("SELECT * FROM nba_player_games WHERE game_id = ? AND player_id = ?",
                                   (x["game_id"], x["player_id"])).fetchone()
            patas.append({**x, "resultado": _resultado_pata(db, x),
                          "real": valor(dict(fila), x["stat"]) if fila else None})
        out.append({"tipo": c["tipo"], "prob": c["prob"], "cuota": c["cuota_final"] or c["cuota"],
                    "result": c["result"], "patas": patas})
    return out


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
        out.setdefault("usuario" if f["tipo"].startswith("usuario:") else f["tipo"], []).append(f)
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
    combis = db.conn.execute("SELECT COUNT(*), AVG(result), AVG(prob) FROM nba_combinadas WHERE result IN (0, 1) "
                             "AND tipo NOT LIKE 'usuario:%'"
                             ).fetchone()
    n, ganadas, prob = combis[0], combis[1] or 0, combis[2] or 0
    out.append(("Combinadas: muestra", n >= MIN_COMBINADAS, f"{n} de {MIN_COMBINADAS}"))
    out.append(("Combinadas: ganan lo prometido", n > 0 and ganadas >= prob - TOLERANCIA,
                f"ganadas {ganadas * 100:.1f}% vs prometido {prob * 100:.1f}%" if n else "sin datos"))
    return out
