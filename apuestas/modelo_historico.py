"""Modelo Dixon-Coles entrenado con el historial de football-data.co.uk.

Cada equipo tiene una fuerza de ataque y otra de defensa (en escala logarítmica) por estadística:

    goles esperados del local     = exp(media + ventaja_local + ataque_local + defensa_visitante)
    goles esperados del visitante = exp(media + ataque_visitante + defensa_local)

Se ajustan por máxima verosimilitud de Poisson con:
- decaimiento temporal: un partido de hace `dias` pesa exp(-xi · dias) (xi = 0.003 → vida media ~8 meses);
- regularización (ridge) hacia un equipo medio, que evita sobreajustar con pocos partidos;
- un ajuste propio para los recién ascendidos, que suelen ser más flojos que la media de la liga;
- la corrección de Dixon-Coles (rho) para los marcadores bajos (0-0, 1-0, 0-1, 1-1), que Poisson
  independiente subestima o sobreestima.

El mismo ajuste sirve para córners, tarjetas y tiros (sin rho y con binomial negativa para la
sobredispersión). El resultado es un `MatchExpectation` del modelo base, así que se reutilizan sus
mercados, el cruce con cuotas y las combinadas.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from datetime import date, timedelta

import numpy as np

from .historico import Partido
from .model import MAX_GOLES
from .model import MatchExpectation

XI_DEFECTO = 0.003            # vida media ~8 meses (la mejor en el backtest)
RIDGE_DEFECTO = 2.0
PESO_TIROS_DEFECTO = 0.0
PESO_MERCADO_DEFECTO = 0.8
VENTANA_DIAS = 4 * 365          # partidos más antiguos pesan < 0.1 %: no aportan y ralentizan
STATS_CONTEO = ("corners", "cards", "shots_on", "shots_total")
MIN_PARTIDOS_STAT = 150          # mínimo de partidos con la estadística para ajustarla


@dataclass
class Ajuste:
    stat: str
    equipos: dict[str, int]
    mu: float
    local: float
    nuevo_ataque: float
    nuevo_defensa: float
    ataque: np.ndarray
    defensa: np.ndarray
    partidos_equipo: dict[str, int]
    rho: float = 0.0
    dispersion: float = 1.0       # varianza / media por equipo y partido

    def esperado(self, local: str, visitante: str, nuevo_local: bool = False,
                 nuevo_visitante: bool = False) -> tuple[float, float]:
        def fuerza(equipo: str, nuevo: bool) -> tuple[float, float]:
            i = self.equipos.get(equipo)
            # Un equipo sin historial en la liga se trata como recién ascendido.
            nuevo = nuevo or i is None
            att = (self.ataque[i] if i is not None else 0.0) + (self.nuevo_ataque if nuevo else 0.0)
            dfn = (self.defensa[i] if i is not None else 0.0) + (self.nuevo_defensa if nuevo else 0.0)
            return att, dfn

        att_l, def_l = fuerza(local, nuevo_local)
        att_v, def_v = fuerza(visitante, nuevo_visitante)
        return (float(np.exp(self.mu + self.local + att_l + def_v)),
                float(np.exp(self.mu + att_v + def_l)))


_REJILLA: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray] | None = None


def _rejilla() -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """(lambdas, P(gana local), P(gana visitante), P(más de 2.5)) para cada par de goles esperados."""
    global _REJILLA
    if _REJILLA is None:
        lams = np.arange(0.15, 4.0, 0.025)
        k = np.arange(MAX_GOLES + 1)
        lgam = np.array([math.lgamma(x + 1) for x in k])
        pmf = np.exp(k[None, :] * np.log(lams[:, None]) - lams[:, None] - lgam[None, :])
        menor = np.concatenate([np.zeros((len(lams), 1)), np.cumsum(pmf, axis=1)[:, :-1]], axis=1)  # P(X < x)
        p1 = pmf @ menor.T
        p2 = menor @ pmf.T
        suma = lams[:, None] + lams[None, :]
        over = 1 - np.exp(-suma) * (1 + suma + suma ** 2 / 2)
        _REJILLA = (lams, p1, p2, over)
    return _REJILLA


def goles_del_mercado(p: Partido) -> tuple[float, float] | None:
    """Goles esperados que implican las cuotas (de cierre si las hay) de un partido.

    Resume lo que sabía el mercado de ambos equipos justo antes del partido: con ellos, el modelo
    aprende también de la opinión de las casas sobre partidos pasados (información legítima: ya era
    pública antes de los partidos que se predicen).
    """
    if p.xg_mercado is not None:
        return p.xg_mercado or None
    resultado = ()
    for cuotas in (p.cuotas_cierre, p.cuotas):
        if all(cuotas.get(m) for m in ("1", "X", "2")):
            inv = [1 / cuotas[m] for m in ("1", "X", "2")]
            q1, q2 = inv[0] / sum(inv), inv[2] / sum(inv)
            lams, p1, p2, over = _rejilla()
            error = (p1 - q1) ** 2 + (p2 - q2) ** 2
            if cuotas.get("over2.5") and cuotas.get("under2.5"):
                qo = (1 / cuotas["over2.5"]) / (1 / cuotas["over2.5"] + 1 / cuotas["under2.5"])
                error = error + (over - qo) ** 2
            i, j = np.unravel_index(np.argmin(error), error.shape)
            resultado = (float(lams[i]), float(lams[j]))
            break
    p.xg_mercado = resultado
    return resultado or None


def _tau(gl: np.ndarray, gv: np.ndarray, lh: np.ndarray, la: np.ndarray, rho: float) -> np.ndarray:
    tau = np.ones_like(lh)
    tau = np.where((gl == 0) & (gv == 0), 1 - lh * la * rho, tau)
    tau = np.where((gl == 0) & (gv == 1), 1 + lh * rho, tau)
    tau = np.where((gl == 1) & (gv == 0), 1 + la * rho, tau)
    tau = np.where((gl == 1) & (gv == 1), 1 - rho, tau)
    return tau


def _estimar_rho(gl, gv, lh, la, w) -> float:
    mejor, mejor_ll = 0.0, -np.inf
    for rho in np.arange(-0.25, 0.1501, 0.005):
        tau = _tau(gl, gv, lh, la, rho)
        if np.any(tau <= 0):
            continue
        ll = float(np.sum(w * np.log(tau)))
        if ll > mejor_ll:
            mejor, mejor_ll = float(rho), ll
    return mejor


def ajustar(partidos: list[Partido], stat: str, hoy: date, nuevos: set[tuple[str, str]],
            xi: float = XI_DEFECTO, ridge: float = RIDGE_DEFECTO, peso_tiros: float = 0.0,
            peso_mercado: float = 0.0) -> Ajuste | None:
    """Ajusta ataque/defensa de una estadística con los partidos jugados antes de `hoy`.

    `nuevos` = pares (temporada, equipo) de recién ascendidos (ver `equipos_nuevos`).
    `peso_tiros` (solo goles): fracción del objetivo que se toma de los tiros a puerta convertidos a
    goles con la tasa de la liga. Los goles tienen mucho azar; los tiros a puerta miden mejor lo que
    genera y concede cada equipo.
    `peso_mercado` (solo goles): fracción tomada de los goles esperados según las cuotas de cada partido.
    """
    filas = []
    for p in partidos:
        if p.fecha >= hoy or (hoy - p.fecha).days > VENTANA_DIAS:
            continue
        v = p.valor(stat)
        if v is None:
            continue
        filas.append((p, v))
    if len(filas) < (60 if stat == "goals" else MIN_PARTIDOS_STAT):
        return None
    goles_reales = None
    if stat == "goals" and (peso_tiros > 0 or peso_mercado > 0):
        goles_reales = [v for _, v in filas]
        filas = _objetivo_goles(filas, peso_tiros, peso_mercado)

    equipos: dict[str, int] = {}
    for p, _ in filas:
        for e in (p.local, p.visitante):
            equipos.setdefault(e, len(equipos))
    n, k = len(filas), len(equipos)
    ih = np.array([equipos[p.local] for p, _ in filas])
    ia = np.array([equipos[p.visitante] for p, _ in filas])
    nh = np.array([(p.temporada, p.local) in nuevos for p, _ in filas], dtype=float)
    na = np.array([(p.temporada, p.visitante) in nuevos for p, _ in filas], dtype=float)
    yh = np.array([v[0] for _, v in filas], dtype=float)
    ya = np.array([v[1] for _, v in filas], dtype=float)
    w = np.exp(-xi * np.array([(hoy - p.fecha).days for p, _ in filas], dtype=float))

    # Columnas: media, ventaja local, ataque de ascendido, defensa de ascendido, ataques, defensas.
    filas_idx = np.arange(n)
    X = np.zeros((2 * n, 4 + 2 * k))
    X[:, 0] = 1.0
    X[:n, 1] = 1.0
    X[:n, 2], X[:n, 3] = nh, na
    X[n:, 2], X[n:, 3] = na, nh
    X[filas_idx, 4 + ih] = 1.0
    X[filas_idx, 4 + k + ia] = 1.0
    X[n + filas_idx, 4 + ia] = 1.0
    X[n + filas_idx, 4 + k + ih] = 1.0
    y = np.concatenate([yh, ya])
    ww = np.concatenate([w, w])
    penal = np.concatenate([[0.0, 0.0, 0.5, 0.5], np.full(2 * k, ridge)])

    # Newton-Raphson sobre la log-verosimilitud de Poisson penalizada (cóncava: converge siempre).
    beta = np.zeros(X.shape[1])
    beta[0] = np.log(max(np.average(y, weights=ww), 1e-3))
    for _ in range(100):
        lam = np.exp(X @ beta)
        grad = X.T @ (ww * (y - lam)) - penal * beta
        hess = (X * (ww * lam)[:, None]).T @ X + np.diag(penal)
        paso = np.linalg.solve(hess, grad)
        beta += paso
        if np.max(np.abs(paso)) < 1e-7:
            break

    lam = np.exp(X @ beta)
    lh, la = lam[:n], lam[n:]
    pearson = float(np.sum(ww * (y - lam) ** 2 / lam) / np.sum(ww))
    conteo: dict[str, int] = {}
    for p, _ in filas:
        conteo[p.local] = conteo.get(p.local, 0) + 1
        conteo[p.visitante] = conteo.get(p.visitante, 0) + 1
    return Ajuste(
        stat=stat, equipos=equipos, mu=float(beta[0]), local=float(beta[1]), nuevo_ataque=float(beta[2]),
        nuevo_defensa=float(beta[3]), ataque=beta[4:4 + k].copy(), defensa=beta[4 + k:].copy(),
        partidos_equipo=conteo,
        rho=_estimar_rho(*_goles(goles_reales, yh, ya), lh, la, w) if stat == "goals" else 0.0,
        dispersion=1.0 if stat == "goals" else min(3.0, max(1.0, pearson)),
    )


def _objetivo_goles(filas: list[tuple[Partido, tuple[float, float]]], peso_tiros: float, peso_mercado: float
                    ) -> list[tuple[Partido, tuple[float, float]]]:
    """Mezcla, partido a partido, goles reales, tiros a puerta convertidos y goles según el mercado.

    Si a un partido le falta una fuente, su peso pasa a los goles reales."""
    con_tiros = [g for p, g in filas if p.valor("shots_on") is not None]
    tiros_total = sum(sum(p.valor("shots_on")) for p, _ in filas if p.valor("shots_on") is not None)
    conversion = sum(g[0] + g[1] for g in con_tiros) / tiros_total if tiros_total else 0.0
    out = []
    for p, g in filas:
        fuentes = [(1.0, g)]
        t = p.valor("shots_on")
        if peso_tiros > 0 and t is not None and conversion:
            fuentes.append((peso_tiros, (conversion * t[0], conversion * t[1])))
        m = goles_del_mercado(p) if peso_mercado > 0 else None
        if m is not None:
            fuentes.append((peso_mercado, m))
        resto = 1.0 - sum(w for w, _ in fuentes[1:])
        fuentes[0] = (resto, g)
        out.append((p, (sum(w * v[0] for w, v in fuentes), sum(w * v[1] for w, v in fuentes))))
    return out


def _goles(reales: list[tuple[float, float]] | None, yh: np.ndarray, ya: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    if reales is None:
        return yh, ya
    return np.array([g[0] for g in reales], dtype=float), np.array([g[1] for g in reales], dtype=float)


def equipos_por_temporada(partidos: list[Partido]) -> dict[str, dict[str, set[str]]]:
    """liga -> temporada -> equipos que jugaron en ella."""
    out: dict[str, dict[str, set[str]]] = {}
    for p in partidos:
        out.setdefault(p.liga, {}).setdefault(p.temporada, set()).update((p.local, p.visitante))
    return out


def es_nuevo(por_temporada: dict[str, set[str]], temporada: str, equipo: str) -> bool:
    """Recién ascendido: no jugó en la temporada anterior de la misma liga (si la conocemos)."""
    anteriores = sorted(t for t in por_temporada if t < temporada)
    return bool(anteriores) and equipo not in por_temporada[anteriores[-1]]


def equipos_nuevos(partidos: list[Partido]) -> set[tuple[str, str]]:
    out = set()
    for temporadas in equipos_por_temporada(partidos).values():
        for t, equipos in temporadas.items():
            out |= {(t, e) for e in equipos if es_nuevo(temporadas, t, e)}
    return out


@dataclass
class ModeloLiga:
    """Todos los ajustes de una liga a una fecha dada."""
    liga: str
    fecha: date
    goles: Ajuste
    conteos: dict[str, Ajuste] = field(default_factory=dict)
    por_temporada: dict[str, set[str]] = field(default_factory=dict)

    def conoce(self, equipo: str) -> bool:
        return equipo in self.goles.equipos

    def expectativa(self, local: str, visitante: str, temporada: str) -> MatchExpectation:
        nl = es_nuevo(self.por_temporada, temporada, local)
        nv = es_nuevo(self.por_temporada, temporada, visitante)
        home, away, disp = {}, {}, {}
        for stat, aj in {"goals": self.goles, **self.conteos}.items():
            home[stat], away[stat] = aj.esperado(local, visitante, nl, nv)
            disp[stat] = aj.dispersion
        return MatchExpectation(home, away, disp, self.goles.partidos_equipo.get(local, 0),
                                self.goles.partidos_equipo.get(visitante, 0), rho=self.goles.rho)


def entrenar_liga(partidos: list[Partido], liga: str, hoy: date, xi: float = XI_DEFECTO,
                  ridge: float = RIDGE_DEFECTO, con_conteos: bool = True,
                  peso_tiros: float = PESO_TIROS_DEFECTO,
                  peso_mercado: float = PESO_MERCADO_DEFECTO) -> ModeloLiga | None:
    de_liga = [p for p in partidos if p.liga == liga and p.fecha < hoy]
    nuevos = equipos_nuevos(de_liga)
    goles = ajustar(de_liga, "goals", hoy, nuevos, xi, ridge, peso_tiros, peso_mercado)
    if goles is None:
        return None
    conteos = {}
    if con_conteos:
        for stat in STATS_CONTEO:
            aj = ajustar(de_liga, stat, hoy, nuevos, xi, ridge)
            if aj is not None:
                conteos[stat] = aj
    return ModeloLiga(liga, hoy, goles, conteos, equipos_por_temporada(de_liga).get(liga, {}))


def semana(d: date) -> date:
    return d - timedelta(days=d.weekday())
