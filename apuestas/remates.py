"""Remates por jugador: proyección, mejor pick por partido y combinada de cuota alta.

Para cada jugador con minutos suficientes en los últimos partidos de su equipo:

    remates esperados = (su parte de los remates del equipo por minuto jugado)
                        × remates esperados del equipo hoy (modelo del partido)
                        × minutos esperados / 90

Con la alineación confirmada, los titulares juegan sus minutos habituales como titular y los
suplentes ~20; sin alineación, cada jugador cuenta con sus minutos medios por partido del equipo (los
partidos que no jugó suman 0), lo que penaliza a quien no es fijo. Probabilidades con binomial
negativa (algo más de varianza que Poisson).

No hay cuotas reales de remates por jugador en ninguna fuente gratuita: todo va con cuota justa, y
un pick solo merece la pena si la casa paga más que ella.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

from .analyzer import analyze_fixture
from .chequeo import aplicar_impacto, impacto_alineacion
from .config import Config
from .db import Database
from .model import prob_over

DISPERSION = 1.2
MIN_MINUTOS = 135           # menos minutos en la muestra: tasa poco fiable
MINUTOS_SUPLENTE = 20
PARTIDOS_MUESTRA = 6


@dataclass
class Proyeccion:
    player_id: int
    nombre: str
    equipo: str
    titular: bool | None          # None = alineación aún no publicada
    minutos: float                # esperados hoy
    remates: float                # esperados hoy
    minutos_muestra: int
    historial: list[int]          # remates en sus últimos partidos

    def prob(self, linea: float) -> float:
        return prob_over(linea, self.remates, self.remates * DISPERSION)


@dataclass
class PickRemates:
    fixture: dict
    jugador: Proyeccion
    linea: float
    prob: float

    @property
    def cuota_justa(self) -> float:
        return 1 / max(self.prob, 1e-9)

    @property
    def etiqueta(self) -> str:
        return f"{self.jugador.nombre} {int(self.linea + 0.5)}+ remates"

    @property
    def fiabilidad(self) -> float:
        """Más muestra y titularidad confirmada = más fiable."""
        f = min(1.0, self.jugador.minutos_muestra / 450)
        return f * (1.0 if self.jugador.titular else 0.9)


@dataclass
class AnalisisRemates:
    fixture: dict
    proyecciones: list[Proyeccion] = field(default_factory=list)
    esperado: dict[str, float] = field(default_factory=dict)
    notas: list[str] = field(default_factory=list)
    con_alineacion: bool = False


def proyectar(db: Database, cfg: Config, fx: dict, historico=None, alineaciones: dict | None = None) -> AnalisisRemates:
    res = AnalisisRemates(fx)
    equipos = {fx["home_id"]: fx["home_name"], fx["away_id"]: fx["away_name"]}
    res.con_alineacion = bool(alineaciones) and all(t in alineaciones for t in equipos)
    factores = {t: 1.0 for t in equipos}
    if res.con_alineacion:
        for tid, nombre in equipos.items():
            imp = impacto_alineacion(db, tid, nombre, fx["date_utc"], alineaciones[tid]["titulares"])
            factores[tid] = imp.factor
            res.notas += imp.notas
    a = analyze_fixture(db, fx, cfg, historico=historico, con_jugadores=False,
                        ajuste=lambda e: aplicar_impacto(e, factores[fx["home_id"]], factores[fx["away_id"]]))
    if a.expectation is None or "shots_total" not in a.expectation.home:
        res.notas.append("Sin modelo de remates para este partido (falta historial del equipo)")
        return res
    esperado = {fx["home_id"]: a.expectation.home["shots_total"], fx["away_id"]: a.expectation.away["shots_total"]}
    res.esperado = {equipos[t]: v for t, v in esperado.items()}

    for tid, nombre_equipo in equipos.items():
        filas = db.player_history(tid, fx["date_utc"], PARTIDOS_MUESTRA)
        partidos = {r["fixture_id"] for r in filas}
        if not partidos:
            res.notas.append(f"{nombre_equipo}: sin estadísticas de jugadores en la base")
            continue
        remates_equipo = sum(r["shots_total"] for r in db.team_history(tid, fx["date_utc"], PARTIDOS_MUESTRA * 2)
                             if r["fixture_id"] in partidos) or 1
        jugadores: dict[int, dict] = {}
        for r in filas:
            j = jugadores.setdefault(r["player_id"], {"nombre": r["name"], "min": 0, "rem": 0, "titular": [], "hist": []})
            j["min"] += r["minutes"]
            j["rem"] += r["shots_total"]
            j["hist"].append(r["shots_total"])
            if r["minutes"] >= 60:
                j["titular"].append(r["minutes"])
        titulares = (alineaciones or {}).get(tid, {}).get("titulares", {}) if res.con_alineacion else {}
        for pid, j in jugadores.items():
            if j["min"] < MIN_MINUTOS:
                continue
            if res.con_alineacion:
                titular = pid in titulares
                minutos = (sum(j["titular"]) / len(j["titular"]) if j["titular"] else 75) if titular else MINUTOS_SUPLENTE
            else:
                titular = None
                minutos = j["min"] / len(partidos)
            # (remates del jugador por minuto) / (remates del equipo por minuto) × remates del equipo hoy por minuto
            cuota_equipo = (j["rem"] / j["min"]) / (remates_equipo / (90 * len(partidos)))
            remates = cuota_equipo * esperado[tid] / 90 * minutos
            res.proyecciones.append(Proyeccion(pid, j["nombre"], nombre_equipo, titular, minutos, remates, j["min"],
                                               j["hist"]))
    return res


def picks(an: AnalisisRemates, rango: tuple[float, float] = (0.30, 0.50), lineas=(1.5, 2.5, 3.5, 4.5),
          remates_min: float = 1.2) -> list[PickRemates]:
    """Picks del partido con probabilidad en `rango` (cuota justa ~2-3.3), del más fiable al menos.

    Solo jugadores que rematan de verdad (≥ `remates_min` esperados) y líneas de 2+ remates: son los
    mercados que ofrecen las casas, y con más volumen el resultado depende menos del azar."""
    out = []
    for p in an.proyecciones:
        if p.titular is False or p.minutos_muestra < 2 * MIN_MINUTOS or p.remates < remates_min:
            continue
        for linea in lineas:
            prob = p.prob(linea)
            if rango[0] <= prob <= rango[1]:
                out.append(PickRemates(an.fixture, p, linea, prob))
    # Entre las líneas de un mismo jugador, la más probable; luego por probabilidad × fiabilidad.
    mejores: dict[int, PickRemates] = {}
    for pk in out:
        if pk.jugador.player_id not in mejores or pk.prob > mejores[pk.jugador.player_id].prob:
            mejores[pk.jugador.player_id] = pk
    return sorted(mejores.values(), key=lambda pk: pk.prob * pk.fiabilidad, reverse=True)


def combinada(mejores_por_partido: list[PickRemates], objetivo: float = 100.0, max_legs: int = 6) -> list[PickRemates]:
    """Un pick por partido (partidos distintos: independientes), los más fiables primero, hasta la cuota objetivo."""
    out: list[PickRemates] = []
    for pk in sorted(mejores_por_partido, key=lambda pk: pk.prob * pk.fiabilidad, reverse=True):
        if len(out) >= max_legs or math.prod(p.cuota_justa for p in out) >= objetivo:
            break
        out.append(pk)
    return out


def render(fecha: str, analisis: list[AnalisisRemates], grupos: dict[str, list[PickRemates]], objetivo: float) -> str:
    out = [f"# Remates por jugador — {fecha}", "",
           "> Cuotas **justas** (ninguna fuente gratuita da cuotas reales de remates por jugador): apuesta un "
           "pick solo si tu casa paga más. Las combinadas de cuota alta aciertan muy pocas veces: stake mínimo.", ""]
    for hora, legs in grupos.items():
        prob = math.prod(p.prob for p in legs) if legs else 0
        cuota = math.prod(p.cuota_justa for p in legs) if legs else 0
        confirmados = all(p.jugador.titular for p in legs)
        out += [f"## Combinada de las {hora} UTC (objetivo {objetivo:g})",
                f"Probabilidad {prob:.2%} · cuota justa {cuota:.1f} · "
                + ("alineaciones confirmadas" if confirmados else "**provisional: alineaciones sin confirmar**"), ""]
        out += [f"- {p.fixture['home_name']} vs {p.fixture['away_name']}: **{p.etiqueta}** — {p.prob:.0%}, "
                f"cuota justa {p.cuota_justa:.2f} (remates en sus últimos partidos: {p.jugador.historial})" for p in legs]
        out.append("")
    out += ["## Por partido", ""]
    for an in analisis:
        fx = an.fixture
        out.append(f"### {fx['home_name']} vs {fx['away_name']} ({fx['date_utc'][11:16]} UTC)")
        if an.esperado:
            out.append("Remates esperados: " + ", ".join(f"{k} {v:.1f}" for k, v in an.esperado.items())
                       + (" · alineaciones confirmadas" if an.con_alineacion else " · sin alineación"))
        out += [f"- _{n}_" for n in an.notas]
        out += [f"- {p.etiqueta} ({p.jugador.equipo}): {p.prob:.0%}, cuota justa {p.cuota_justa:.2f}, "
                f"{p.jugador.remates:.1f} esperados en {p.jugador.minutos:.0f} min" for p in picks(an)[:4]]
        out.append("")
    return "\n".join(out)
