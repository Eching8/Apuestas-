"""Convierte un summary de ESPN en filas de todas las tablas y comprueba que cuadren con el box score."""
from __future__ import annotations

from dataclasses import dataclass, field

from . import espn, pbp


@dataclass
class Partido:
    jugadores: list[dict] = field(default_factory=list)
    ausencias: list[dict] = field(default_factory=list)
    equipos: list[dict] = field(default_factory=list)
    jugadas: list[dict] = field(default_factory=list)
    periodos: list[dict] = field(default_factory=list)
    tramos: list[dict] = field(default_factory=list)
    tiros: list[dict] = field(default_factory=list)
    inicio: dict | None = None
    lineas: dict | None = None
    control: dict = field(default_factory=dict)


def procesar(summary: dict) -> Partido:
    game_id = str(summary["header"]["id"])
    comp = summary["header"]["competitions"][0]
    lados = {c["homeAway"]: str(c["team"]["id"]) for c in comp["competitors"]}
    out = Partido()
    out.jugadores, out.ausencias = espn.parse_box(summary)
    out.equipos = espn.parse_team_box(summary)
    out.lineas = espn.parse_lineas(summary)
    if not out.jugadores:
        return out

    equipo_de = pbp.jugadores_por_equipo(out.jugadores)
    titulares: dict[str, list[str]] = {}
    for r in out.jugadores:
        if r["starter"]:
            titulares.setdefault(r["team_id"], []).append(r["player_id"])

    jugadas = pbp.normalizar(summary)
    out.jugadas = jugadas
    if not jugadas:
        return out

    prod = pbp.produccion_por_periodo(jugadas)
    tramos, segundos = pbp.quintetos(jugadas, equipo_de, titulares)
    out.tramos = [{"game_id": game_id, **t} for t in tramos]
    claves = {k for k in prod if k[0] in equipo_de} | set(segundos)
    for pid, per in sorted(claves):
        if pid not in equipo_de:
            continue
        s = prod.get((pid, per), dict.fromkeys(pbp.STATS, 0))
        out.periodos.append({"game_id": game_id, "player_id": pid, "team_id": equipo_de[pid], "period": per,
                             "seconds": round(segundos.get((pid, per), 0.0), 1), **s})
    out.tiros = pbp.tiros(jugadas, equipo_de)
    out.inicio = {"game_id": game_id, **pbp.inicio_partido(jugadas, equipo_de, lados["home"], lados["away"], titulares)}
    out.control = control_calidad(out)
    return out


def control_calidad(p: Partido) -> dict:
    """Compara la suma por periodos del jugada a jugada con el box score de cada jugador.
    Devuelve el % de jugadores que cuadran exactamente por estadística y el error de minutos."""
    suma: dict[str, dict[str, float]] = {}
    for r in p.periodos:
        s = suma.setdefault(r["player_id"], dict.fromkeys(pbp.STATS + ("seconds",), 0.0))
        for k in pbp.STATS:
            s[k] += r[k]
        s["seconds"] += r["seconds"]
    n = len(p.jugadores)
    if not n:
        return {}
    ok = dict.fromkeys(pbp.STATS, 0)
    err_min = []
    for b in p.jugadores:
        s = suma.get(b["player_id"], dict.fromkeys(pbp.STATS + ("seconds",), 0.0))
        for k in pbp.STATS:
            ok[k] += int(s[k] == b[k])
        err_min.append(abs(s["seconds"] / 60 - b["minutes"]))
    return {**{f"ok_{k}": ok[k] / n for k in pbp.STATS}, "mae_min": sum(err_min) / n,
            "max_err_min": max(err_min), "n": n}
