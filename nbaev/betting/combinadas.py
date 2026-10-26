"""Mercados comparativos (duelos, máximo anotador) y combinadas con probabilidad conjunta simulada.

Las selecciones del mismo partido están correlacionadas (minutos, ritmo, quién se queda los tiros), así
que la probabilidad de una combinada NO es el producto de las probabilidades: se cuenta en cuántas
simulaciones se cumplen todas a la vez. Entre partidos distintos sí se multiplican (son independientes).
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from ..models.proyeccion import valor


@dataclass
class Seleccion:
    jugador: str          # nombre (o player_id)
    mercado: str          # pts, reb, pra, doble_doble...
    linea: float | None   # None en mercados sí/no
    lado: str             # over/under/yes/no
    periodo: str = "game"
    cuota: float | None = None
    p_justa: float | None = None   # probabilidad justa de esa selección (sin margen), si se conoce


def _fila(filas: pd.DataFrame, jugador: str) -> int:
    m = (filas["player_id"] == jugador) | filas["name"].str.lower().eq(jugador.lower())
    if not m.any():
        m = filas["name"].str.lower().str.contains(jugador.lower(), regex=False)
    if m.sum() != 1:
        raise ValueError(f"Jugador ambiguo o no encontrado: {jugador} ({m.sum()} coincidencias)")
    return int(np.flatnonzero(m.to_numpy())[0])


def indicador(filas: pd.DataFrame, sims: dict, s: Seleccion) -> tuple[str, np.ndarray]:
    """(game_id, array booleano por simulación: se cumple la selección). Empate = no se cumple."""
    i = _fila(filas, s.jugador)
    v = valor(sims, s.mercado, s.periodo)[i]
    if s.linea is None:
        ok = v.astype(bool) if s.lado in ("yes", "over") else ~v.astype(bool)
    else:
        ok = v > s.linea if s.lado in ("over", "yes") else v < s.linea
    return filas.iloc[i]["game_id"], ok


def combinada(filas: pd.DataFrame, sims: dict, selecciones: list[Seleccion]) -> dict:
    por_partido: dict[str, np.ndarray] = {}
    marginales = []
    for s in selecciones:
        gid, ok = indicador(filas, sims, s)
        marginales.append(ok.mean())
        por_partido[gid] = ok if gid not in por_partido else (por_partido[gid] & ok)
    p_conj = float(np.prod([v.mean() for v in por_partido.values()]))
    p_indep = float(np.prod(marginales))
    out = {"p_conjunta": p_conj, "p_si_fueran_independientes": p_indep, "selecciones": len(selecciones),
           "partidos": len(por_partido), "marginales": marginales}
    cuotas = [s.cuota for s in selecciones]
    if all(c for c in cuotas):
        cuota = float(np.prod(cuotas))
        out.update({"cuota_combinada": cuota, "ev_combinada": p_conj * cuota - 1,
                    "ev_simples_medio": float(np.mean([p * c - 1 for p, c in zip(marginales, cuotas)]))})
        justas = [s.p_justa for s in selecciones]
        if all(j for j in justas):
            # Margen acumulado: probabilidad implícita de la combinada frente a la justa (producto de justas).
            out["margen_acumulado"] = (1 / cuota) / float(np.prod(justas)) - 1
            out["margen_medio_simple"] = float(np.mean([(1 / c) / j - 1 for c, j in zip(cuotas, justas)]))
    return out


def duelo(filas: pd.DataFrame, sims: dict, a: str, b: str, mercado: str = "pts") -> dict:
    """P(A supera a B), P(B supera a A) y P(empate) en un mercado."""
    va, vb = valor(sims, mercado)[_fila(filas, a)], valor(sims, mercado)[_fila(filas, b)]
    return {"p_a": float((va > vb).mean()), "p_b": float((vb > va).mean()), "p_empate": float((va == vb).mean())}


def maximo(filas: pd.DataFrame, sims: dict, game_id: str, mercado: str = "pts", team_id: str | None = None) -> pd.DataFrame:
    """P(ser el máximo del partido o del equipo) en un mercado; empates repartidos (dead heat)."""
    m = (filas["game_id"] == game_id) & ((filas["team_id"] == team_id) if team_id else True)
    idx = np.flatnonzero(m.to_numpy())
    v = valor(sims, mercado)[idx]
    es = v == v.max(0)
    p = (es / es.sum(0)).mean(1)
    return (pd.DataFrame({"jugador": filas.iloc[idx]["name"].to_numpy(), "p": p, "cuota_justa": 1 / np.maximum(p, 1e-6)})
            .sort_values("p", ascending=False).reset_index(drop=True))
