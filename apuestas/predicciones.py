"""Predicciones de los próximos partidos solo con datos de football-data.co.uk (sin clave de API).

Entrena el modelo histórico de cada liga con todo lo jugado hasta hoy, predice los partidos de
los próximos días que publica football-data.co.uk y los cruza con sus cuotas (1X2 y más/menos
de 2.5 goles: la media de las casas). El resto de mercados se muestran con su cuota justa.
"""
from __future__ import annotations

from datetime import date, timedelta

from .analyzer import Analysis, candidates
from .combinadas import Leg, build_combos
from .config import Config
from .historico import NOMBRES_LIGA, Historico, Partido
from .model import Market, match_markets
from .modelo_historico import entrenar_liga, nota_arbitro
from .odds import attach_odds

# Mercado interno -> (bet, value) con los nombres de API-Football que entiende odds.attach_odds.
FILAS_CUOTAS = {
    "1": ("Match Winner", "Home"), "X": ("Match Winner", "Draw"), "2": ("Match Winner", "Away"),
    "over2.5": ("Goals Over/Under", "Over 2.5"), "under2.5": ("Goals Over/Under", "Under 2.5"),
}


def filas_cuotas(p: Partido) -> list[dict]:
    return [{"bookmaker": "media", "bet": FILAS_CUOTAS[m][0], "value": FILAS_CUOTAS[m][1], "odd": o}
            for m, o in p.cuotas.items() if m in FILAS_CUOTAS]


def predecir(cfg: Config, hoy: date, dias: int, ligas: list[str] | None = None, sin_cuotas: bool = False
             ) -> tuple[list[Analysis], dict[int, list[Market]], dict]:
    ligas = ligas or cfg.ligas_historico
    hist = Historico(cfg.historico_dir)
    proximos = [p for p in hist.proximos(ligas) if hoy <= p.fecha <= hoy + timedelta(days=dias)]
    partidos = hist.partidos(sorted({p.liga for p in proximos}), cfg.temporadas_historico, hoy) if proximos else []
    modelos = {liga: entrenar_liga(partidos, liga, hoy) for liga in {p.liga for p in proximos}}

    analyses, picks, legs = [], {}, []
    for i, p in enumerate(proximos, 1):
        fx = {"id": -i, "home_name": p.local, "away_name": p.visitante, "league_id": p.liga,
              "league_name": NOMBRES_LIGA.get(p.liga, p.liga), "league_country": p.liga,
              "date_utc": p.fecha.isoformat(), "cuando": f"{p.fecha.isoformat()} {p.hora} (hora de Reino Unido)"}
        a = Analysis(fixture=fx)
        modelo = modelos.get(p.liga)
        if modelo is None:
            a.notas.append("Sin historial suficiente de la liga")
            analyses.append(a)
            continue
        for equipo in (p.local, p.visitante):
            if not modelo.conoce(equipo):
                a.notas.append(f"{equipo}: sin partidos en la liga en las últimas temporadas; "
                               "se usa la fuerza media de un recién ascendido")
        a.expectation = modelo.expectativa(p.local, p.visitante, p.temporada, p.arbitro or None)
        if p.arbitro:
            nota = nota_arbitro(modelo, p.arbitro).lstrip("; ")
            a.notas.append(nota[:1].upper() + nota[1:])
        a.markets = match_markets(a.expectation, p.local, p.visitante)
        attach_odds(a.markets, filas_cuotas(p), cfg.peso_modelo)
        analyses.append(a)
        sel = candidates(a, cfg, sin_cuotas=sin_cuotas)
        sel.sort(key=lambda m: ((m.edge or 0), m.final_prob or m.prob), reverse=True)
        picks[fx["id"]] = sel[:8]
        legs += [Leg(fx["id"], f"{p.local} vs {p.visitante}", m) for m in sel]
    combos = build_combos(legs, cfg.prob_min_combinada, cfg.max_selecciones_combinada)
    return analyses, picks, combos
