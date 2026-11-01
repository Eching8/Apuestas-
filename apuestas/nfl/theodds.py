"""Respaldo de líneas de la NFL: The Odds API (https://the-odds-api.com), cuando SportsGameOdds no responde.

Listar los partidos no gasta créditos; las cuotas de un partido cuestan un crédito por mercado devuelto y región.
Con los mercados de MERCADOS son hasta 9 créditos por partido, así que solo se piden los partidos que empiezan
pronto (`APUESTAS_NFL_THEODDS_HORAS`), cada partido como mucho una vez cada REFRESCO_HORAS (el resto de la semana usa
las líneas guardadas) y nunca por debajo de `APUESTAS_NFL_THEODDS_RESERVA` créditos, para dejar cupo a la NBA.
"""
from __future__ import annotations

import logging
from datetime import datetime
from statistics import median

from ..nba.theodds import TheOddsApi, _iso
from . import equipos
from .mercado import CONTRARIO, Mercado, Oferta

log = logging.getLogger(__name__)

DEPORTE = "americanfootball_nfl"
# Mercado de The Odds API -> estadística interna (las que usan las combinadas y los touchdowns).
MERCADOS = {
    "player_pass_yds": "pass_yds", "player_pass_tds": "pass_tds", "player_pass_completions": "comp",
    "player_rush_yds": "rush_yds", "player_rush_attempts": "rush_att", "player_receptions": "rec",
    "player_reception_yds": "rec_yds", "player_anytime_td": "tds", "player_tds_over": "tds",
}
REFRESCO_HORAS = 20
PREFIJO = "theodds:"     # event_id de las líneas guardadas que vienen de aquí
LADOS = {"over": "más", "under": "menos", "yes": "más", "no": "menos"}


class TheOddsApiNfl(TheOddsApi):
    def partidos(self, inicio: datetime, fin: datetime) -> list[dict]:
        """Partidos de la NFL que empiezan entre inicio y fin (UTC). No gasta créditos."""
        return self._get(f"/sports/{DEPORTE}/events", commenceTimeFrom=_iso(inicio), commenceTimeTo=_iso(fin))

    def mercado(self, partido: dict) -> Mercado:
        odds = self._get(f"/sports/{DEPORTE}/events/{partido['id']}/odds", regions=self.regiones,
                         markets=",".join(MERCADOS), oddsFormat="decimal")
        return parse_evento({**partido, **odds})

    def creditos(self) -> int | None:
        try:
            return int(float(self.restantes)) if self.restantes is not None else None
        except ValueError:
            return None


def parse_evento(evento: dict) -> Mercado:
    """Las props del partido como Mercado: cada casa en `libros`, la mediana como consenso y la del otro lado de la
    misma línea como contraria (para quitar el margen)."""
    home = equipos.por_nombre_largo(evento.get("home_team") or "")
    away = equipos.por_nombre_largo(evento.get("away_team") or "")
    m = Mercado(PREFIJO + str(evento.get("id", "")), home, away, evento.get("commence_time"))
    ofertas: dict[tuple, Oferta] = {}
    for casa in evento.get("bookmakers", []):
        for mercado in casa.get("markets", []):
            stat = MERCADOS.get(mercado.get("key"))
            if not stat:
                continue
            for o in mercado.get("outcomes", []):
                lado_api = (o.get("name") or "").lower()
                lado, jugador, precio = LADOS.get(lado_api), o.get("description"), o.get("price")
                if lado is None or not jugador or not precio:
                    continue
                linea = 0.5 if lado_api in ("yes", "no") else o.get("point")
                if linea is None:
                    continue
                k = (jugador, stat, lado, float(linea))
                of = ofertas.get(k)
                if of is None:
                    of = ofertas[k] = Oferta(jugador, jugador, None, stat, lado, float(linea))
                # "Anota" y "más de 0.5 TD" son la misma apuesta: se queda el mejor precio de cada casa.
                of.libros[casa.get("key", "?")] = max(float(precio), of.libros.get(casa.get("key", "?"), 0.0))
    for of in ofertas.values():
        of.consenso = round(median(of.libros.values()), 3)
    for (jugador, stat, lado, linea), of in ofertas.items():
        otra = ofertas.get((jugador, stat, CONTRARIO[lado], linea))
        of.contraria = otra.consenso if otra else None
    m.ofertas = list(ofertas.values())
    return m
