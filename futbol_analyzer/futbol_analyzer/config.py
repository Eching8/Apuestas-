"""Configuración central. Todo se puede sobreescribir con variables de entorno o un archivo .env."""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path


def _load_dotenv(path: Path = Path(".env")) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


_load_dotenv()

# El análisis arranca el 21 de octubre de 2026; no se procesan fechas anteriores.
START_DATE = date(2026, 10, 21)

# Ligas a analizar: id de API-Football -> (nombre, código de liga en ESPN para validación cruzada)
LEAGUES: dict[int, tuple[str, str]] = {
    2: ("UEFA Champions League", "uefa.champions"),
    3: ("UEFA Europa League", "uefa.europa"),
    848: ("UEFA Conference League", "uefa.europa.conf"),
    39: ("Premier League", "eng.1"),
    140: ("La Liga", "esp.1"),
    135: ("Serie A", "ita.1"),
    78: ("Bundesliga", "ger.1"),
    61: ("Ligue 1", "fra.1"),
    94: ("Primeira Liga", "por.1"),
    88: ("Eredivisie", "ned.1"),
    262: ("Liga MX", "mex.1"),
    253: ("MLS", "usa.1"),
    128: ("Liga Profesional Argentina", "arg.1"),
    71: ("Brasileirão Serie A", "bra.1"),
    239: ("Liga BetPlay Colombia", "col.1"),
}


@dataclass
class Settings:
    api_football_key: str = field(default_factory=lambda: os.getenv("API_FOOTBALL_KEY", ""))
    odds_api_key: str = field(default_factory=lambda: os.getenv("ODDS_API_KEY", ""))
    db_path: str = field(default_factory=lambda: os.getenv("FUTBOL_DB", "futbol.db"))
    timezone: str = field(default_factory=lambda: os.getenv("FUTBOL_TZ", "America/Mexico_City"))
    # Casa de apuestas preferida en API-Football (8 = Bet365)
    bookmaker_id: int = int(os.getenv("FUTBOL_BOOKMAKER", "8"))
    # Presupuesto de peticiones por ejecución (plan gratis de API-Football = 100/día)
    request_budget: int = int(os.getenv("FUTBOL_REQUEST_BUDGET", "90"))
    # Segundos entre peticiones a API-Football (plan gratis: máx. 10 por minuto)
    api_football_interval: float = float(os.getenv("FUTBOL_AF_INTERVAL", "6.5"))
    # Modo híbrido: máximo de partidos terminados a validar contra API-Football por ejecución
    validation_budget: int = int(os.getenv("FUTBOL_VALIDATION_BUDGET", "30"))

    # Historial
    min_history: int = 6          # partidos mínimos por equipo antes de confiar en el modelo
    history_window: int = 15      # últimos N partidos usados en las medias
    decay: float = 0.92           # peso exponencial: partidos recientes pesan más
    prior_weight: float = 4.0     # encogimiento hacia la media de la liga (partidos "virtuales")

    # Selección de picks
    min_prob_pick: float = 0.62   # probabilidad mínima para considerar un mercado
    min_ev: float = 0.03          # valor esperado mínimo (3 %) cuando hay cuota
    max_odds_pick: float = 2.60

    # Combinadas
    combo_min_legs: int = 2
    combo_max_legs: int = 4
    combo_min_prob: float = 0.40  # probabilidad conjunta mínima
    combo_leg_min_prob: float = 0.70
    combo_count: int = 5

    # Validación cruzada: tolerancia absoluta por estadística entre fuentes
    validation_tolerance: dict = field(default_factory=lambda: {
        "goals": 0, "corners": 1, "yellow": 1, "red": 0, "shots_on": 2, "shots": 3,
    })


SETTINGS = Settings()
