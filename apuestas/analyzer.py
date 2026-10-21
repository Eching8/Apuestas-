"""Analiza un partido con los datos guardados: valores esperados y probabilidades por mercado."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from .combinadas import Combo, CreaTuApuesta, Leg, build_loteria, crea_tu_apuesta
from .config import Config
from .db import Database
from .model import (MEDIAS_POR_DEFECTO, STATS, Market, MatchExpectation, expect_match, match_markets,
                    player_markets, team_profile)
from .odds import attach_odds, market_only
from .puente import ModeloHistorico


@dataclass
class Analysis:
    fixture: dict
    expectation: MatchExpectation | None = None
    markets: list[Market] = field(default_factory=list)
    notas: list[str] = field(default_factory=list)
    # Sin historial suficiente: solo probabilidades implícitas de las casas, sin modelo propio.
    solo_mercado: bool = False

    @property
    def ok(self) -> bool:
        return self.expectation is not None or (self.solo_mercado and bool(self.markets))


def analyze_fixture(db: Database, fx: dict, cfg: Config, con_jugadores: bool = True,
                    historico: ModeloHistorico | None = None,
                    ajuste: Callable[[MatchExpectation], None] | None = None) -> Analysis:
    a = _analyze_fixture(db, fx, cfg, con_jugadores, historico, ajuste)
    if fx.get("league_id") in cfg.ligas_solo_tarjetas:
        a.markets = [m for m in a.markets if m.stat == "cards" and m.scope != "player"]
        a.notas.append("Liga solo para el modelo de tarjetas: el resto de mercados no se analiza")
    return a


def _analyze_fixture(db: Database, fx: dict, cfg: Config, con_jugadores: bool,
                     historico: ModeloHistorico | None,
                     ajuste: Callable[[MatchExpectation], None] | None) -> Analysis:
    """Modelo histórico (Dixon-Coles con años de datos) si cubre el partido; si no, el modelo de forma
    reciente con lo guardado en la base; y si tampoco hay historial, solo las cuotas de las casas.

    `ajuste` corrige lo esperado antes de calcular los mercados (p. ej. por la alineación)."""
    a = Analysis(fixture=fx)
    hist_h = db.team_history(fx["home_id"], fx["date_utc"], cfg.partidos_historial)
    hist_a = db.team_history(fx["away_id"], fx["date_utc"], cfg.partidos_historial)
    faltan = [f"{name}: solo {len(hist)} partidos con estadísticas (mínimo {cfg.min_partidos_equipo})"
              for name, hist in ((fx["home_name"], hist_h), (fx["away_name"], hist_a))
              if len(hist) < cfg.min_partidos_equipo]

    if historico is not None:
        a.expectation, nota = historico.expectativa(fx)
        a.notas.append(nota if a.expectation is not None else f"Modelo histórico no disponible: {nota}")
    if a.expectation is None and faltan:
        a.notas += faltan
        a.markets = market_only(db.odds_for(fx["id"]), fx["home_name"], fx["away_name"])
        if a.markets:
            a.solo_mercado = True
            a.notas.append("Análisis solo con cuotas de las casas (probabilidad implícita sin margen); "
                           "el modelo propio se activa cuando haya historial suficiente")
        return a

    if not faltan:
        means = db.league_means(fx["league_id"], fx["date_utc"])
        if means is None:
            means = db.league_means(None, fx["date_utc"])
            if a.expectation is None:
                a.notas.append("Media de liga estimada con todos los partidos guardados (pocos datos de esta liga)")
        means = {s: (means or {}).get(s) or MEDIAS_POR_DEFECTO[s] for s in STATS}
        prof_h, prof_a = team_profile(fx["home_id"], hist_h), team_profile(fx["away_id"], hist_a)
        if a.expectation is None:
            a.expectation = expect_match(prof_h, prof_a, means)
    if ajuste is not None:
        ajuste(a.expectation)
    a.markets = match_markets(a.expectation, fx["home_name"], fx["away_name"])

    # Mercados de jugador: necesitan el historial por jugador de la base.
    if con_jugadores and not faltan:
        for team_id, rival in ((fx["home_id"], prof_a), (fx["away_id"], prof_h)):
            factor = {s: (rival.contra.get(s) or means[s]) / means[s] for s in ("shots_on", "shots_total", "goals")}
            rows = db.player_history(team_id, fx["date_utc"], cfg.partidos_historial)
            a.markets += player_markets(rows, factor, cfg.min_partidos_jugador)

    attach_odds(a.markets, db.odds_for(fx["id"]), cfg.peso_modelo)
    if not any(m.odd for m in a.markets):
        a.notas.append("Sin cuotas disponibles: solo se muestra la cuota justa del modelo")
    return a


def candidates(analysis: Analysis, cfg: Config, sin_cuotas: bool = False) -> list[Market]:
    """Selecciones que cumplen los filtros de probabilidad y valor."""
    out = []
    for m in analysis.markets:
        p = m.final_prob if m.final_prob is not None else m.prob
        if p < cfg.prob_min_seleccion:
            continue
        if m.odd is not None:
            if m.odd < cfg.cuota_min_seleccion:
                continue
            # En modo mercado el "valor" es siempre negativo (margen de la casa): no se filtra por él.
            if not analysis.solo_mercado and (m.edge or 0) < cfg.valor_min:
                continue
        elif not sin_cuotas or m.fair_odd < cfg.cuota_min_seleccion:
            continue
        out.append(m)
    return out


def combinadas_extra(analyses: list[Analysis], cfg: Config) -> tuple[list[Combo], list[CreaTuApuesta]]:
    """Combinadas lotería (entre partidos, con cuotas reales) y "crea tu apuesta" (dentro de cada partido)."""
    loteria, builders = [], []
    if cfg.cuota_loteria > 1:
        legs = [Leg(a.fixture["id"], f"{a.fixture['home_name']} vs {a.fixture['away_name']}", m)
                for a in analyses if a.ok for m in a.markets if m.odd and m.scope != "player"]
        loteria = build_loteria(legs, cfg.cuota_loteria, cfg.max_selecciones_loteria)
    if cfg.cuota_crea_tu_apuesta > 1:
        for a in analyses:
            if a.expectation is None:
                continue
            b = crea_tu_apuesta(a.fixture["id"], f"{a.fixture['home_name']} vs {a.fixture['away_name']}",
                                a.expectation, a.markets, cfg.cuota_crea_tu_apuesta)
            if b is not None:
                builders.append(b)
    return loteria, builders
