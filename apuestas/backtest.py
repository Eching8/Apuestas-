"""Backtest honesto del modelo histórico: ¿predice mejor que las casas? ¿habría ganado dinero?

Recorre las temporadas de prueba semana a semana. Antes de cada semana re-entrena el modelo solo
con los partidos jugados hasta ese lunes (nunca ve el futuro) y predice los partidos de la semana.

Métricas para 1X2 y más/menos de 2.5 goles:
- log-loss y Brier (más bajo = mejor) del modelo, de las cuotas previas y de las de cierre (sin margen);
- calibración: cuando el modelo dice 60 %, ¿ocurre el 60 % de las veces?
- apuestas simuladas de 1 unidad cuando valor = prob × cuota previa − 1 supera el umbral, con la
  cuota media de las casas. Además del beneficio (muy ruidoso), se mide el valor según la cuota de
  cierre sin margen (CLV): es el indicador más fiable de si el modelo encuentra valor real.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from datetime import date

from .historico import NOMBRES_LIGA, Partido
from .model import score_grid
from .modelo_historico import (PESO_MERCADO_DEFECTO, PESO_TIROS_DEFECTO, RIDGE_DEFECTO, XI_DEFECTO, entrenar_liga,
                               semana)

MERCADOS_1X2 = ("1", "X", "2")
MERCADOS_GOLES = ("over2.5", "under2.5")
CUOTA_MAX_APUESTA = 8.0      # las cuotas muy altas añaden mucho ruido y poco valor medible


def sin_margen(cuotas: dict[str, float], mercados: tuple[str, ...]) -> dict[str, float] | None:
    if not all(cuotas.get(m) for m in mercados):
        return None
    inv = {m: 1 / cuotas[m] for m in mercados}
    total = sum(inv.values())
    return {m: v / total for m, v in inv.items()}


def probs_modelo(lh: float, la: float, rho: float) -> dict[str, float]:
    grid = score_grid(lh, la, rho)
    n = len(grid)
    p1 = sum(grid[i][j] for i in range(n) for j in range(n) if i > j)
    px = sum(grid[i][i] for i in range(n))
    over = sum(grid[i][j] for i in range(n) for j in range(n) if i + j > 2.5)
    return {"1": p1, "X": px, "2": 1 - p1 - px, "over2.5": over, "under2.5": 1 - over}


def resultado(p: Partido) -> dict[str, int]:
    gl, gv = p.goles_local, p.goles_visitante
    return {"1": int(gl > gv), "X": int(gl == gv), "2": int(gl < gv),
            "over2.5": int(gl + gv > 2.5), "under2.5": int(gl + gv < 2.5)}


@dataclass
class Prediccion:
    partido: Partido
    modelo: dict[str, float]
    previa: dict[str, float]      # prob. sin margen de las cuotas previas (solo mercados con cuota)
    cierre: dict[str, float]      # prob. sin margen de las cuotas de cierre


@dataclass
class Apuestas:
    n: int = 0
    ganadas: int = 0
    beneficio: float = 0.0
    clv: float = 0.0           # suma de (cuota × prob. cierre sin margen − 1)
    con_clv: int = 0
    cuota_media: float = 0.0

    def add(self, cuota: float, gana: int, p_cierre: float | None) -> None:
        self.n += 1
        self.ganadas += gana
        self.beneficio += cuota - 1 if gana else -1
        self.cuota_media += cuota
        if p_cierre is not None:
            self.clv += cuota * p_cierre - 1
            self.con_clv += 1

    def resumen(self) -> dict:
        return {
            "apuestas": self.n,
            "acierto": self.ganadas / self.n if self.n else None,
            "cuota_media": self.cuota_media / self.n if self.n else None,
            "beneficio": self.beneficio,
            "roi": self.beneficio / self.n if self.n else None,
            "clv_medio": self.clv / self.con_clv if self.con_clv else None,
        }


@dataclass
class ResultadoBacktest:
    liga: str
    predicciones: list[Prediccion] = field(default_factory=list)

    def _metricas(self, mercados: tuple[str, ...], fuente: str, peso: float | None = None) -> dict | None:
        ll = brier = 0.0
        n = 0
        for pr in self.predicciones:
            if not all(m in pr.previa and m in pr.cierre for m in mercados):
                continue     # comparar siempre sobre los mismos partidos
            probs = _probs(pr, fuente, peso)
            res = resultado(pr.partido)
            total = sum(probs[m] for m in mercados)
            ll -= math.log(max(1e-12, sum(probs[m] / total * res[m] for m in mercados)))
            brier += sum((probs[m] / total - res[m]) ** 2 for m in mercados)
            n += 1
        return {"n": n, "logloss": ll / n, "brier": brier / n} if n else None

    def metricas(self, peso: float) -> dict:
        out = {}
        for nombre, mercados in (("1x2", MERCADOS_1X2), ("goles2.5", MERCADOS_GOLES)):
            out[nombre] = {
                "modelo": self._metricas(mercados, "modelo"),
                f"mezcla_{peso:.2f}": self._metricas(mercados, "mezcla", peso),
                "cuotas_previas": self._metricas(mercados, "previa"),
                "cuotas_cierre": self._metricas(mercados, "cierre"),
            }
        return out

    def calibracion(self, mercados: tuple[str, ...] = MERCADOS_1X2, cubos: int = 10) -> list[dict]:
        acum = [[0, 0.0, 0] for _ in range(cubos)]
        for pr in self.predicciones:
            res = resultado(pr.partido)
            for m in mercados:
                b = min(cubos - 1, int(pr.modelo[m] * cubos))
                acum[b][0] += 1
                acum[b][1] += pr.modelo[m]
                acum[b][2] += res[m]
        return [{"rango": f"{i / cubos:.0%}-{(i + 1) / cubos:.0%}", "n": n, "prob_media": s / n, "frecuencia": k / n}
                for i, (n, s, k) in enumerate(acum) if n]

    def apuestas(self, peso: float, valor_min: float) -> dict[str, dict]:
        por_mercado = {"1x2": Apuestas(), "goles2.5": Apuestas()}
        for pr in self.predicciones:
            probs = _probs(pr, "mezcla", peso)
            res = resultado(pr.partido)
            for grupo, mercados in (("1x2", MERCADOS_1X2), ("goles2.5", MERCADOS_GOLES)):
                for m in mercados:
                    cuota = pr.partido.cuotas.get(m)
                    if not cuota or cuota > CUOTA_MAX_APUESTA or probs[m] * cuota - 1 < valor_min:
                        continue
                    por_mercado[grupo].add(cuota, res[m], pr.cierre.get(m))
        return {k: v.resumen() for k, v in por_mercado.items()}


def _probs(pr: Prediccion, fuente: str, peso: float | None) -> dict[str, float]:
    if fuente == "modelo":
        return pr.modelo
    if fuente == "previa":
        return pr.previa
    if fuente == "cierre":
        return pr.cierre
    # Mezcla con el mercado previo (lo único que se conoce al apostar).
    return {m: peso * p + (1 - peso) * pr.previa[m] if m in pr.previa else p for m, p in pr.modelo.items()}


def backtest_liga(partidos: list[Partido], liga: str, desde: date, xi: float = XI_DEFECTO,
                  ridge: float = RIDGE_DEFECTO, peso_tiros: float = PESO_TIROS_DEFECTO,
                  peso_mercado: float = PESO_MERCADO_DEFECTO) -> ResultadoBacktest:
    de_liga = [p for p in partidos if p.liga == liga]
    res = ResultadoBacktest(liga)
    por_semana: dict[date, list[Partido]] = {}
    for p in de_liga:
        if p.fecha >= desde:
            por_semana.setdefault(semana(p.fecha), []).append(p)
    for lunes in sorted(por_semana):
        modelo = entrenar_liga(de_liga, liga, lunes, xi, ridge, con_conteos=False, peso_tiros=peso_tiros,
                               peso_mercado=peso_mercado)
        if modelo is None:
            continue
        for p in por_semana[lunes]:
            e = modelo.expectativa(p.local, p.visitante, p.temporada)
            res.predicciones.append(Prediccion(
                p, probs_modelo(e.home["goals"], e.away["goals"], e.rho),
                {**(sin_margen(p.cuotas, MERCADOS_1X2) or {}), **(sin_margen(p.cuotas, MERCADOS_GOLES) or {})},
                {**(sin_margen(p.cuotas_cierre, MERCADOS_1X2) or {}),
                 **(sin_margen(p.cuotas_cierre, MERCADOS_GOLES) or {})},
            ))
    return res


def _f(x: float | None, fmt: str) -> str:
    return "-" if x is None else format(x, fmt)


def render_backtest(resultados: list[ResultadoBacktest], desde: date, peso: float, valor_min: float) -> str:
    out = [f"# Backtest del modelo histórico (desde {desde.isoformat()})", "",
           "Entrenado semana a semana solo con partidos anteriores. Log-loss: más bajo = mejor. "
           "Las cuotas de cierre son el listón: casi ningún modelo público las supera.", ""]
    for nombre, titulo in (("1x2", "1X2"), ("goles2.5", "Más/menos de 2.5 goles")):
        out += [f"## {titulo}", "", f"| Liga | Partidos | Modelo | Mezcla {peso:.0%} modelo | Cuotas previas | Cuotas cierre |",
                "|---|---|---|---|---|---|"]
        for r in resultados:
            m = r.metricas(peso)[nombre]
            filas = list(m.values())
            if filas[0] is None:
                continue
            out.append(f"| {NOMBRES_LIGA.get(r.liga, r.liga)} | {filas[0]['n']} | "
                       + " | ".join(f"{x['logloss']:.4f}" for x in filas) + " |")
        out.append("")
    out += ["## Apuestas simuladas", "",
            f"1 unidad cuando valor = prob. (mezcla {peso:.0%} modelo) × cuota media previa − 1 ≥ {valor_min:.0%}, "
            f"cuotas ≤ {CUOTA_MAX_APUESTA:.0f}. CLV = valor medio según la cuota de cierre sin margen "
            "(positivo = el modelo encuentra valor real; es mucho más estable que el beneficio).", "",
            "| Liga | Mercado | Apuestas | Acierto | Cuota media | Beneficio | ROI | CLV medio |",
            "|---|---|---|---|---|---|---|---|"]
    for r in resultados:
        for mercado, a in r.apuestas(peso, valor_min).items():
            out.append(f"| {NOMBRES_LIGA.get(r.liga, r.liga)} | {mercado} | {a['apuestas']} | "
                       f"{_f(a['acierto'], '.1%')} | {_f(a['cuota_media'], '.2f')} | {a['beneficio']:+.2f} u | "
                       f"{_f(a['roi'], '+.1%')} | {_f(a['clv_medio'], '+.1%')} |")
    todas = ResultadoBacktest("todas", [p for r in resultados for p in r.predicciones])
    out += ["", "## Calibración del modelo (1X2, todas las ligas)", "",
            "| Prob. del modelo | Selecciones | Prob. media | Frecuencia real |", "|---|---|---|---|"]
    out += [f"| {c['rango']} | {c['n']} | {c['prob_media']:.1%} | {c['frecuencia']:.1%} |"
            for c in todas.calibracion()]
    return "\n".join(out) + "\n"


# --- Córners, tarjetas, remates y atajadas ------------------------------------------------

# Línea de referencia por estadística (total del partido) para medir el acierto de "más de".
LINEAS_CONTEO = {"corners": 9.5, "cards": 3.5, "shots_on": 8.5, "shots_total": 23.5, "saves": 5.5}


@dataclass
class ResultadoConteos:
    """Por estadística: (prob. modelo, prob. modelo sin árbitro, prob. media de la liga, ocurrió)."""
    liga: str
    filas: dict[str, list[tuple[float, float, float, int]]] = field(default_factory=dict)

    def metricas(self) -> dict[str, dict]:
        out = {}
        for stat, filas in self.filas.items():
            if not filas:
                continue
            ll = [0.0, 0.0, 0.0]
            for *ps, y in filas:
                for i, p in enumerate(ps):
                    p = min(max(p, 1e-6), 1 - 1e-6)
                    ll[i] -= math.log(p if y else 1 - p)
            n = len(filas)
            out[stat] = {"n": n, "linea": LINEAS_CONTEO[stat], "frecuencia": sum(f[3] for f in filas) / n,
                         "modelo": ll[0] / n, "sin_arbitro": ll[1] / n, "media_liga": ll[2] / n}
        return out

    def calibracion(self, stat: str, cubos: int = 5) -> list[dict]:
        acum = [[0, 0.0, 0] for _ in range(cubos)]
        for p, _, _, y in self.filas.get(stat, []):
            b = min(cubos - 1, int(p * cubos))
            acum[b][0] += 1
            acum[b][1] += p
            acum[b][2] += y
        return [{"rango": f"{i / cubos:.0%}-{(i + 1) / cubos:.0%}", "n": n, "prob_media": s / n, "frecuencia": k / n}
                for i, (n, s, k) in enumerate(acum) if n]


def backtest_conteos(partidos: list[Partido], liga: str, desde: date) -> ResultadoConteos:
    """Mismo esquema semana a semana que el 1X2, para las estadísticas de conteo (sin cuotas en los
    datos: se compara con la referencia ingenua de "la media de la liga")."""
    from .model import prob_over
    de_liga = [p for p in partidos if p.liga == liga]
    res = ResultadoConteos(liga, {s: [] for s in LINEAS_CONTEO})
    por_semana: dict[date, list[Partido]] = {}
    for p in de_liga:
        if p.fecha >= desde:
            por_semana.setdefault(semana(p.fecha), []).append(p)
    for lunes in sorted(por_semana):
        modelo = entrenar_liga(de_liga, liga, lunes)
        if modelo is None:
            continue
        for p in por_semana[lunes]:
            con = modelo.expectativa(p.local, p.visitante, p.temporada, p.arbitro or None)
            sin = modelo.expectativa(p.local, p.visitante, p.temporada)
            for stat, linea in LINEAS_CONTEO.items():
                aj, real = modelo.conteos.get(stat), p.valor(stat)
                if aj is None or real is None:
                    continue
                disp = aj.dispersion
                mu_c, mu_s = con.total(stat), sin.total(stat)
                media = 2 * math.exp(aj.mu + aj.local / 2)       # equipo medio, ventaja local repartida
                res.filas[stat].append((prob_over(linea, mu_c, mu_c * disp), prob_over(linea, mu_s, mu_s * disp),
                                        prob_over(linea, media, media * disp), int(real[0] + real[1] > linea)))
    return res


def render_conteos(resultados: list[ResultadoConteos]) -> str:
    from .model import NOMBRES
    out = ["## Córners, tarjetas, remates y atajadas", "",
           "Log-loss de \"más de la línea\" en el total del partido (más bajo = mejor). Sin cuotas en los "
           "datos, la referencia es usar siempre la media de la liga: el modelo solo aporta si la mejora.", "",
           "| Liga | Mercado | Partidos | Frecuencia real | Modelo | Sin árbitro | Media de la liga |",
           "|---|---|---|---|---|---|---|"]
    for r in resultados:
        for stat, m in r.metricas().items():
            out.append(f"| {NOMBRES_LIGA.get(r.liga, r.liga)} | más de {m['linea']} {NOMBRES[stat]} | {m['n']} | "
                       f"{m['frecuencia']:.1%} | {m['modelo']:.4f} | {m['sin_arbitro']:.4f} | {m['media_liga']:.4f} |")
    return "\n".join(out) + "\n"
