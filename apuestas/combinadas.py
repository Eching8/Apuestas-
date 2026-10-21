"""Construcción de combinadas a partir de las selecciones candidatas.

Se usa como máximo una selección por partido: dos selecciones del mismo partido (p. ej. "más
de 2.5 goles" y "ambos marcan") están correlacionadas y multiplicar sus probabilidades
sobrestimaría la de la combinada.
"""
from __future__ import annotations

import itertools
import math
from dataclasses import dataclass

from .model import Market

POOL_MAX = 24        # selecciones que entran en la búsqueda
POR_PARTIDO = 3      # mejores selecciones por partido que se consideran


@dataclass
class Leg:
    fixture_id: int
    partido: str
    market: Market

    @property
    def prob(self) -> float:
        return self.market.final_prob if self.market.final_prob is not None else self.market.prob

    @property
    def odd(self) -> float:
        # Sin cuota real se usa la cuota justa: la combinada solo vale si la casa paga más que eso.
        return self.market.odd or self.market.fair_odd


@dataclass
class Combo:
    perfil: str
    legs: list[Leg]

    @property
    def prob(self) -> float:
        return math.prod(l.prob for l in self.legs)

    @property
    def odd(self) -> float:
        return math.prod(l.odd for l in self.legs)

    @property
    def con_cuotas(self) -> bool:
        return all(l.market.odd for l in self.legs)

    @property
    def ev(self) -> float:
        return self.prob * self.odd - 1

    @property
    def kelly(self) -> float:
        """Fracción de Kelly al 25 %, con tope del 2 % del bankroll (lotería: stake simbólico fijo)."""
        if self.perfil == "loteria":
            return STAKE_LOTERIA
        if not self.con_cuotas or self.odd <= 1:
            return 0.0
        f = (self.prob * self.odd - 1) / (self.odd - 1)
        return max(0.0, min(0.02, f / 4))


def _pool(legs: list[Leg], score) -> list[Leg]:
    by_fx: dict[int, list[Leg]] = {}
    for l in sorted(legs, key=score, reverse=True):
        by_fx.setdefault(l.fixture_id, [])
        if len(by_fx[l.fixture_id]) < POR_PARTIDO:
            by_fx[l.fixture_id].append(l)
    return sorted((l for ls in by_fx.values() for l in ls), key=score, reverse=True)[:POOL_MAX]


def _enumerate(pool: list[Leg], max_size: int):
    for size in range(2, max_size + 1):
        for combo in itertools.combinations(pool, size):
            if len({l.fixture_id for l in combo}) == size:
                yield list(combo)


def _top(combos: list[Combo], key, n: int) -> list[Combo]:
    """Las n mejores combinadas que no repiten exactamente los mismos partidos."""
    out, seen = [], set()
    for c in sorted(combos, key=key, reverse=True):
        firma = frozenset(l.fixture_id for l in c.legs)
        if firma in seen:
            continue
        seen.add(firma)
        out.append(c)
        if len(out) == n:
            break
    return out


def build_combos(legs: list[Leg], prob_min: float, max_size: int = 4, cuota_min: float = 2.0,
                 n: int = 3) -> dict[str, list[Combo]]:
    """Devuelve combinadas por perfil:

    - alta_probabilidad: la mayor probabilidad conjunta con cuota total >= cuota_min.
    - valor: el mayor valor esperado (EV) con probabilidad conjunta >= prob_min.
    """
    if len({l.fixture_id for l in legs}) < 2:
        return {"alta_probabilidad": [], "valor": []}

    seguras = [Combo("alta_probabilidad", c) for c in _enumerate(_pool(legs, lambda l: l.prob), max_size)]
    seguras = [c for c in seguras if c.odd >= cuota_min]

    valor_pool = _pool(legs, lambda l: l.prob * l.odd)
    valor = [Combo("valor", c) for c in _enumerate(valor_pool, max_size)]
    valor = [c for c in valor if c.prob >= prob_min and c.con_cuotas and c.ev > 0]

    return {
        "alta_probabilidad": _top(seguras, lambda c: c.prob, n),
        "valor": _top(valor, lambda c: c.ev, n),
    }


# --- Lotería: la combinada más probable con cuota total >= objetivo ------------------------

PASO_LOG = 0.002          # resolución (en log-cuota): como mucho pierde combinadas un ~2 % por encima del objetivo
STAKE_LOTERIA = 0.001     # 0.1 % del bankroll: el EV de estas combinadas es negativo


def build_loteria(legs: list[Leg], objetivo: float = 100.0, max_selecciones: int = 12, n: int = 3,
                  cuota_min: float = 1.2) -> list[Combo]:
    """Combinadas de partidos distintos con cuota real >= `objetivo` y la mayor probabilidad posible.

    Es una mochila: maximizar la suma de log(prob) con la suma de log(cuota) >= log(objetivo) y como
    máximo una selección por partido. Se resuelve exacta por programación dinámica sobre la log-cuota
    (redondeada hacia abajo: la cuota real nunca queda por debajo del objetivo). Las alternativas se
    obtienen quitando cada vez la selección "más cara" (más probabilidad perdida por unidad de cuota).
    """
    pool = [l for l in legs if l.market.odd and l.market.odd >= cuota_min and 0 < l.prob < 1]
    prohibidas: set[int] = set()
    out: list[Combo] = []
    for _ in range(n):
        sol = _mochila([l for l in pool if id(l) not in prohibidas], objetivo, max_selecciones)
        if not sol:
            break
        out.append(Combo("loteria", sol))
        prohibidas.add(id(max(sol, key=lambda l: -math.log(l.prob) / math.log(l.odd))))
    return out


def _mochila(legs: list[Leg], objetivo: float, max_sel: int) -> list[Leg] | None:
    import numpy as np
    B = math.ceil(math.log(objetivo) / PASO_LOG)
    por_partido: dict[int, list[Leg]] = {}
    for l in legs:
        por_partido.setdefault(l.fixture_id, []).append(l)
    grupos = list(por_partido.values())
    if not grupos:
        return None
    C = min(max_sel, len(grupos))
    mejor = np.full((C + 1, B + 1), -np.inf)
    mejor[0, 0] = 0.0
    columnas = np.arange(B + 1)
    trazas = []
    for grupo in grupos:
        cands, previos = [mejor], [np.broadcast_to(columnas, mejor.shape)]
        for l in grupo:
            k = min(B, int(math.log(l.odd) / PASO_LOG))
            sh = np.full_like(mejor, -np.inf)
            prev = np.zeros(mejor.shape, dtype=int)
            if k < B:
                sh[1:, k:B] = mejor[:-1, :B - k]
                prev[:, k:B] = columnas[:B - k]
            tramo = mejor[:-1, B - k:]                    # cualquier origen que llegue al objetivo
            sh[1:, B] = tramo.max(axis=1)
            prev[1:, B] = B - k + tramo.argmax(axis=1)
            cands.append(sh + math.log(l.prob))
            previos.append(prev)
        pila = np.stack(cands)
        eleccion = pila.argmax(axis=0)
        mejor = pila.max(axis=0)
        trazas.append((grupo, eleccion, np.stack(previos)))
    if not np.isfinite(mejor[:, B]).any():
        return None
    c, b = int(mejor[:, B].argmax()), B
    sol = []
    for grupo, eleccion, previos in reversed(trazas):
        j = int(eleccion[c, b])
        if j > 0:
            sol.append(grupo[j - 1])
            b = int(previos[j, c, b])
            c -= 1
    return sol[::-1]


# --- "Crea tu apuesta": varias selecciones del mismo partido, con la correlación simulada -------

@dataclass
class CreaTuApuesta:
    fixture_id: int
    partido: str
    markets: list[Market]
    prob: float                     # probabilidad conjunta simulada

    @property
    def cuota_justa(self) -> float:
        return 1 / max(self.prob, 1e-9)

    @property
    def cuota_producto(self) -> float | None:
        """Producto de las cuotas sueltas: la casa paga menos en "crea tu apuesta" (lo corrige)."""
        return math.prod(m.odd for m in self.markets) if all(m.odd for m in self.markets) else None


def crea_tu_apuesta(fixture_id: int, partido: str, expectativa, markets: list[Market], objetivo: float = 3.0,
                    max_selecciones: int = 4) -> CreaTuApuesta | None:
    """La combinación del mismo partido con mayor probabilidad conjunta y cuota justa >= objetivo.

    De cada familia de mercados (resultado, ambos marcan, goles totales, córners del local...) entran
    dos líneas: la más probable (hasta 95 %) y la más cercana al 65 %."""
    import numpy as np
    from .simulacion import cumple, familia, simular
    sim = simular(expectativa, seed=abs(fixture_id) % (2 ** 32))
    por_familia: dict[str, list[Market]] = {}
    for m in markets:
        if 0.5 <= m.prob <= 0.95 and m.scope != "player":
            por_familia.setdefault(familia(m), []).append(m)
    pool = []
    for fam, ms in por_familia.items():
        elegidas = {max(ms, key=lambda m: m.prob).key: None, min(ms, key=lambda m: abs(m.prob - 0.65)).key: None}
        for m in ms:
            if m.key in elegidas:
                v = cumple(sim, m)
                if v is not None:
                    pool.append((m, fam, np.packbits(v)))
    n = len(sim["goals_home"])
    mejor: CreaTuApuesta | None = None
    for size in range(2, max_selecciones + 1):
        for combo in itertools.combinations(pool, size):
            if len({fam for _, fam, _ in combo}) < size:
                continue
            gana = combo[0][2]
            for _, _, v in combo[1:]:
                gana = gana & v
            p = int(np.bitwise_count(gana).sum()) / n
            if 0 < p <= 1 / objetivo and (mejor is None or p > mejor.prob):
                mejor = CreaTuApuesta(fixture_id, partido, [m for m, _, _ in combo], p)
    return mejor
