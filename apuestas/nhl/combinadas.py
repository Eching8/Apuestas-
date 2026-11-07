"""Combinadas de la NHL por probabilidad (mismo criterio que la NBA), su registro y su liquidación.

- alternas (segura A): el pick seguro más probable de cada partido (líneas alternativas al 85 %+).
- principales (segura B): la prop más probable de cada partido entre jugadores constantes.
- cuota_2 / cuota_3 / cuota_5: las menos patas posibles (partidos distintos, máximo 5) con más probabilidad de
  acertar todas cuya cuota llega al objetivo. Nada de combinadas "de valor".
- builder: bet builder por partido (2-3 "más de" del mismo partido con el mismo guion, ver builder.py).

Sin líneas de la casa, la cuota es estimada (la justa menos el margen de Betano): sirve para saber cuántas patas
hacen falta; la buena es la que mande el usuario.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from itertools import combinations

from ..db import now_iso
from .analizador import Partido, combinada_segura, cuota, resultado
from .db import NhlDB
from .modelo import NOMBRES, Evaluacion, Segura

OBJETIVOS = (2.0, 3.0, 5.0)
MAX_SELECCIONES = 5
CANDIDATAS_MAX = 18


@dataclass
class Combinada:
    tipo: str
    patas: list[dict] = field(default_factory=list)
    prob_fija: float | None = None

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

    @property
    def estimada(self) -> bool:
        return any(x.get("cuota_estimada") for x in self.patas)


def _pata_prop(p: Partido, e: Evaluacion) -> dict:
    return {"game_id": p.game["id"], "partido": p.titulo, "player_id": e.player_id, "nombre": e.nombre,
            "stat": e.stat, "line": e.line, "side": e.lado, "prob": e.prob, "odd": round(cuota(e), 3),
            "cuota_estimada": not e.odd, "linea_estimada": e.estimada, "defensa": e.defensa,
            "acierto_10": list(e.acierto_10), "acierto_temporada": list(e.acierto_temporada),
            "argumentos": list(e.argumentos)}


def _pata_segura(p: Partido, s: Segura) -> dict:
    return {"game_id": p.game["id"], "partido": p.titulo, "player_id": s.player_id, "nombre": s.nombre,
            "stat": s.stat, "line": s.line, "side": "más", "prob": s.prob, "odd": None}


def alternas(partidos: list[Partido], n: int = 4) -> Combinada | None:
    mejores = sorted(((p, p.seguras[0]) for p in partidos if p.seguras), key=lambda x: -x[1].prob)[:n]
    return Combinada("alternas", [_pata_segura(p, s) for p, s in mejores]) if len(mejores) >= 2 else None


def principales(candidatas: list[tuple[Partido, Evaluacion]], n: int = 4) -> Combinada | None:
    elegidas = combinada_segura(candidatas, n)
    return Combinada("principales", [_pata_prop(p, e) for p, e in elegidas]) if len(elegidas) >= 2 else None


def con_cuota(candidatas: list[tuple[Partido, Evaluacion]], objetivo: float, tipo: str = "cuota") -> Combinada | None:
    """Las menos patas (de partidos distintos) con más probabilidad de acertar todas y cuota >= objetivo."""
    por_partido: dict[str, list] = {}
    for p, e in candidatas:
        lista = por_partido.setdefault(p.game["id"], [])
        if len(lista) < 2:
            lista.append((p, e))
    pool = sorted((x for v in por_partido.values() for x in v), key=lambda x: -x[1].prob)[:CANDIDATAS_MAX]
    for k in range(2, MAX_SELECCIONES + 1):
        mejor = None
        for comb in combinations(pool, k):
            if len({p.game["id"] for p, _ in comb}) < k:
                continue
            c = prob = 1.0
            for _, e in comb:
                c *= cuota(e)
                prob *= e.prob
            if c >= objetivo and (mejor is None or prob > mejor[0]):
                mejor = (prob, comb)
        if mejor:   # las menos patas posibles: con k patas ya se llega
            return Combinada(f"{tipo}_{objetivo:g}", [_pata_prop(p, e) for p, e in mejor[1]])
    return None


def del_dia(partidos: list[Partido], candidatas: list[tuple[Partido, Evaluacion]]) -> list[Combinada]:
    out = [alternas(partidos), principales(candidatas)] + [con_cuota(candidatas, o) for o in OBJETIVOS]
    return [c for c in out if c]


def de_builders(builders: list) -> list[Combinada]:
    out = []
    for b in builders:
        patas = [{"game_id": b.partido.game["id"], "partido": b.partido.titulo, "player_id": x.player_id,
                  "nombre": x.nombre, "stat": x.stat, "line": x.line, "side": "más", "prob": x.prob, "odd": None}
                 for x in b.piernas]
        out.append(Combinada("builder", patas, b.prob))
    return out


# --- Registro y liquidación ----------------------------------------------------------

def guardar(db: NhlDB, fecha: str, combis: list[Combinada]) -> None:
    db.conn.execute("DELETE FROM nhl_combinadas WHERE fecha = ? AND result IS NULL AND tipo NOT LIKE 'usuario:%'",
                    (fecha,))
    db.conn.executemany(
        "INSERT INTO nhl_combinadas(fecha, tipo, patas, prob, cuota, created_at) VALUES (?, ?, ?, ?, ?, ?)",
        [(fecha, c.tipo, json.dumps(c.patas, ensure_ascii=False), c.prob, c.cuota, now_iso()) for c in combis])
    db.commit()


def _resultado_pata(db: NhlDB, x: dict) -> int | None:
    if not db.game_done(x["game_id"]):
        return None
    return resultado(db, x["game_id"], x["player_id"], x["stat"], x["line"], x["side"])[1]


def liquidar(db: NhlDB) -> int:
    """Una combinada gana si aciertan todas sus patas; las anuladas se quitan (como en las casas)."""
    n = 0
    for c in db.conn.execute("SELECT * FROM nhl_combinadas WHERE result IS NULL").fetchall():
        patas = json.loads(c["patas"])
        res = [_resultado_pata(db, x) for x in patas]
        if 0 in res:
            db.conn.execute("UPDATE nhl_combinadas SET result = 0, cuota_final = cuota, aciertos = ? WHERE id = ?",
                            (sum(r == 1 for r in res), c["id"]))
            n += 1
            continue
        if any(r is None for r in res):
            continue
        validas = [(x, r) for x, r in zip(patas, res) if r != 2]
        if not validas:
            res_final, cuota_final = 2, c["cuota"]
        else:
            res_final = int(all(r == 1 for _, r in validas))
            if c["cuota"] is None or any(x["odd"] is None for x, _ in validas):
                cuota_final = c["cuota"]
            else:
                cuota_final = 1.0
                for x, _ in validas:
                    cuota_final *= x["odd"]
        db.conn.execute("UPDATE nhl_combinadas SET result = ?, cuota_final = ?, aciertos = ? WHERE id = ?",
                        (res_final, cuota_final, sum(r == 1 for _, r in validas), c["id"]))
        n += 1
    db.commit()
    return n


NOMBRES_TIPO = {"alternas": "Combinada segura A (alternas)", "principales": "Combinada segura B (principales)",
                "builder": "Bet builder"}


def nombre_tipo(tipo: str) -> str:
    if tipo.startswith("usuario:"):
        return "Tu apuesta: " + tipo.split(":", 1)[1]
    if tipo == "usuario":
        return "Tus apuestas"
    if tipo in NOMBRES_TIPO:
        return NOMBRES_TIPO[tipo]
    base, c = tipo.rsplit("_", 1)
    return f"Segura cuota {c}+"


def detalle(db: NhlDB, fecha: str) -> list[dict]:
    from .analizador import fila_jugador
    from .modelo import valor
    out = []
    for c in db.conn.execute("SELECT * FROM nhl_combinadas WHERE fecha = ? ORDER BY id", (fecha,)).fetchall():
        patas = []
        for x in json.loads(c["patas"]):
            fila = fila_jugador(db, x["game_id"], x["player_id"], x["stat"])
            patas.append({**x, "resultado": _resultado_pata(db, x), "real": valor(fila, x["stat"]) if fila else None})
        out.append({"tipo": c["tipo"], "prob": c["prob"], "cuota": c["cuota_final"] or c["cuota"],
                    "result": c["result"], "patas": patas})
    return out


def resumen(db: NhlDB) -> list[dict]:
    por_tipo: dict[str, list] = {}
    for f in db.conn.execute("SELECT * FROM nhl_combinadas WHERE result IN (0, 1) ORDER BY tipo"):
        por_tipo.setdefault("usuario" if f["tipo"].startswith("usuario:") else f["tipo"], []).append(f)
    out = []
    for tipo, filas in por_tipo.items():
        n = len(filas)
        con_cuota = [f for f in filas if f["cuota_final"]]
        out.append({"tipo": tipo, "n": n, "ganadas": sum(f["result"] for f in filas),
                    "prob_media": sum(f["prob"] for f in filas) / n,
                    "beneficio": sum((f["cuota_final"] - 1) if f["result"] else -1 for f in con_cuota)
                    if con_cuota else None, "con_cuota": len(con_cuota)})
    return out


def etiqueta_pata(x: dict) -> str:
    return f"{x['nombre']}: {x['side']} de {x['line']:g} {NOMBRES[x['stat']]}"
