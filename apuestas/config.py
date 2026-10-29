"""Configuración del analizador. Todo se puede sobrescribir con variables de entorno o un archivo .env."""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Fecha desde la que empieza el seguimiento diario.
FECHA_INICIO = date(2026, 10, 21)


def _load_dotenv(path: Path) -> None:
    """Carga un .env sencillo (CLAVE=valor) sin dependencias externas."""
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


_load_dotenv(ROOT / ".env")


def _float(name: str, default: float) -> float:
    return float(os.environ.get(name, default))


def _int(name: str, default: int) -> int:
    return int(os.environ.get(name, default))


def _ligas() -> list[int]:
    raw = os.environ.get("APUESTAS_LIGAS", "").strip()
    return [int(x) for x in raw.split(",") if x.strip()]


@dataclass
class Config:
    api_football_key: str = field(default_factory=lambda: os.environ.get("API_FOOTBALL_KEY", ""))
    football_data_key: str = field(default_factory=lambda: os.environ.get("FOOTBALL_DATA_KEY", ""))
    zona_horaria: str = field(default_factory=lambda: os.environ.get("APUESTAS_TZ", "America/Mexico_City"))
    db_path: Path = field(default_factory=lambda: Path(os.environ.get("APUESTAS_DB", ROOT / "data" / "apuestas.db")))
    reportes_dir: Path = field(default_factory=lambda: Path(os.environ.get("APUESTAS_REPORTES", ROOT / "reportes")))

    # Ligas a analizar (ids de API-Football). Vacío = todas las del día (gasta muchas peticiones).
    ligas: list[int] = field(default_factory=_ligas)
    # Partidos recientes por equipo que se usan para el modelo.
    partidos_historial: int = field(default_factory=lambda: _int("APUESTAS_HISTORIAL", 6))
    # Tope de peticiones a la API por ejecución (plan gratuito: 100/día).
    presupuesto_peticiones: int = field(default_factory=lambda: _int("APUESTAS_PRESUPUESTO", 90))
    # Máximo de partidos del día a analizar.
    max_partidos: int = field(default_factory=lambda: _int("APUESTAS_MAX_PARTIDOS", 15))

    # Filtros de selecciones.
    prob_min_seleccion: float = field(default_factory=lambda: _float("APUESTAS_PROB_MIN", 0.62))
    valor_min: float = field(default_factory=lambda: _float("APUESTAS_VALOR_MIN", 0.03))
    cuota_min_seleccion: float = field(default_factory=lambda: _float("APUESTAS_CUOTA_MIN", 1.25))
    # Peso del modelo frente a la probabilidad implícita del mercado (0 = solo mercado, 1 = solo modelo).
    peso_modelo: float = field(default_factory=lambda: _float("APUESTAS_PESO_MODELO", 0.5))
    # Filtros de combinadas.
    prob_min_combinada: float = field(default_factory=lambda: _float("APUESTAS_PROB_MIN_COMBI", 0.35))
    max_selecciones_combinada: int = field(default_factory=lambda: _int("APUESTAS_MAX_SELECCIONES", 4))
    # Mínimo de partidos con datos para confiar en un equipo / jugador.
    min_partidos_equipo: int = 4
    min_partidos_jugador: int = 4

    # NBA: clave de SportsGameOdds (líneas de props) y filtros.
    sgo_key: str = field(default_factory=lambda: os.environ.get("SPORTSGAMEODDS_KEY", ""))
    nba_prob_min: float = field(default_factory=lambda: _float("APUESTAS_NBA_PROB_MIN", 0.65))
    nba_min_partidos: int = field(default_factory=lambda: _int("APUESTAS_NBA_MIN_PARTIDOS", 8))
    # Peso de la probabilidad de la casa (sin margen) en la probabilidad final de cada prop.
    nba_peso_mercado: float = field(default_factory=lambda: _float("APUESTAS_NBA_PESO_MERCADO", 0.4))
    # Probabilidad objetivo de los picks seguros (líneas bajas de titulares estables).
    nba_prob_segura: float = field(default_factory=lambda: _float("APUESTAS_NBA_PROB_SEGURA", 0.85))
    # Combinada segura: cuota mínima de cada selección (con cuota real de la casa).
    nba_cuota_min: float = field(default_factory=lambda: _float("APUESTAS_NBA_CUOTA_MIN", 1.30))

    # NFL: peso de la casa en la probabilidad final, valor mínimo para recomendar y días por delante a analizar.
    nfl_peso_mercado: float = field(default_factory=lambda: _float("APUESTAS_NFL_PESO_MERCADO", 0.35))
    nfl_valor_min: float = field(default_factory=lambda: _float("APUESTAS_NFL_VALOR_MIN", 0.04))
    nfl_dias: int = field(default_factory=lambda: _int("APUESTAS_NFL_DIAS", 7))


def load_config() -> Config:
    return Config()
