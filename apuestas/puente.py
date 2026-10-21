"""Une los partidos de API-Football con el modelo histórico de football-data.co.uk.

Las dos fuentes usan ids de liga y nombres de equipo distintos ("Manchester United" frente a
"Man United"). Se emparejan por liga y por similitud de nombre, con una tabla de abreviaturas
conocidas. Si un equipo no se puede emparejar con seguridad, el partido queda fuera del modelo
histórico (mejor sin predicción que con la de otro equipo).
"""
from __future__ import annotations

import logging
from datetime import date

from .football_data import _norm, _similar
from .historico import Historico, Partido, temporada_de
from .model import MatchExpectation
from .modelo_historico import ModeloLiga, entrenar_liga, nota_arbitro

log = logging.getLogger(__name__)

# id de liga en API-Football -> código en football-data.co.uk
LIGA_API_A_FD = {
    39: "E0", 40: "E1", 140: "SP1", 141: "SP2", 135: "I1", 136: "I2", 78: "D1", 79: "D2", 61: "F1", 62: "F2",
    88: "N1", 94: "P1", 144: "B1", 203: "T1", 179: "SC0", 197: "G1",
    262: "MEX", 128: "ARG", 71: "BRA", 253: "USA", 98: "JPN", 113: "SWE", 103: "NOR", 119: "DNK", 218: "AUT",
    207: "SWZ", 106: "POL", 169: "CHN",
}
# Abreviaturas de football-data.co.uk -> nombre completo habitual.
ALIAS = {
    "Man United": "Manchester United", "Man City": "Manchester City", "Nott'm Forest": "Nottingham Forest",
    "Wolves": "Wolverhampton Wanderers", "Sheffield Weds": "Sheffield Wednesday", "Spurs": "Tottenham",
    "QPR": "Queens Park Rangers", "West Brom": "West Bromwich Albion", "Ath Madrid": "Atletico Madrid",
    "Ath Bilbao": "Athletic Club", "Sociedad": "Real Sociedad", "Betis": "Real Betis", "Espanol": "Espanyol",
    "Vallecano": "Rayo Vallecano", "Celta": "Celta Vigo", "La Coruna": "Deportivo La Coruna",
    "Sp Gijon": "Sporting Gijon", "M'gladbach": "Borussia Monchengladbach", "Ein Frankfurt": "Eintracht Frankfurt",
    "FC Koln": "1. FC Koln", "Bayern Munich": "Bayern Munchen", "Leverkusen": "Bayer Leverkusen",
    "Dortmund": "Borussia Dortmund", "Paris SG": "Paris Saint Germain", "St Etienne": "Saint Etienne",
    "Sp Lisbon": "Sporting CP", "Sp Braga": "SC Braga", "Milan": "AC Milan", "Inter": "Inter",
    "Club Brugge": "Club Brugge KV", "St Truiden": "Sint-Truiden", "Greuther Furth": "SpVgg Greuther Furth",
}
SIMILITUD_MIN = 0.72


def _variantes(nombre_fd: str) -> list[str]:
    return [nombre_fd] + ([ALIAS[nombre_fd]] if nombre_fd in ALIAS else [])


def emparejar(nombre_api: str, candidatos: set[str]) -> str | None:
    """Nombre de football-data.co.uk para un equipo de API-Football, o None si no es seguro."""
    puntos = sorted(((max(_similar(nombre_api, v) for v in _variantes(c)), c) for c in candidatos), reverse=True)
    if not puntos or puntos[0][0] < SIMILITUD_MIN:
        return None
    # Ambiguo: dos candidatos casi igual de parecidos (p. ej. "Sheffield United" y "Sheffield Weds").
    if len(puntos) > 1 and puntos[1][0] >= puntos[0][0] - 0.02 and _norm(nombre_api) not in {
            _norm(v) for v in _variantes(puntos[0][1])}:
        return None
    return puntos[0][1]


class ModeloHistorico:
    """Entrena (una vez por liga y día) y da expectativas para partidos de API-Football."""

    def __init__(self, historico: Historico, ligas: list[str], temporadas: int, hoy: date, **parametros):
        self.historico = historico
        self.ligas = ligas
        self.temporadas = temporadas
        self.hoy = hoy
        self.parametros = parametros
        self._partidos: list[Partido] | None = None
        self._modelos: dict[str, ModeloLiga | None] = {}

    def partidos(self) -> list[Partido]:
        if self._partidos is None:
            self._partidos = self.historico.partidos(self.ligas, self.temporadas, self.hoy)
        return self._partidos

    def modelo(self, liga: str) -> ModeloLiga | None:
        if liga not in self._modelos:
            self._modelos[liga] = entrenar_liga(self.partidos(), liga, self.hoy, **self.parametros)
        return self._modelos[liga]

    def expectativa(self, fx: dict) -> tuple[MatchExpectation | None, str]:
        """(expectativa, nota) para una fila de `fixtures` con home_name/away_name/league_id."""
        liga = LIGA_API_A_FD.get(fx["league_id"])
        if liga is None or liga not in self.ligas:
            return None, "liga sin cobertura en el modelo histórico"
        modelo = self.modelo(liga)
        if modelo is None:
            return None, "sin historial suficiente de la liga en football-data.co.uk"
        temporada = temporada_de(self.hoy)
        # Candidatos: equipos de la temporada actual (o de la última conocida), luego cualquiera.
        actuales = modelo.por_temporada.get(temporada) or modelo.por_temporada.get(max(modelo.por_temporada, default=""), set())
        nombres = []
        for nombre in (fx["home_name"], fx["away_name"]):
            fd = emparejar(nombre, actuales) or emparejar(nombre, set(modelo.goles.equipos))
            if fd is None:
                return None, f"no se pudo emparejar '{nombre}' con un equipo de football-data.co.uk"
            nombres.append(fd)
        if nombres[0] == nombres[1]:
            return None, "emparejamiento ambiguo de equipos"
        arbitro = fx.get("referee")
        e = modelo.expectativa(nombres[0], nombres[1], temporada, arbitro)
        nota = f"Modelo histórico Dixon-Coles ({nombres[0]} vs {nombres[1]} en football-data.co.uk)"
        return e, nota + nota_arbitro(modelo, arbitro)
