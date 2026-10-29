"""Carga de la configuración YAML y de los logs."""
from __future__ import annotations

import copy
import logging
import os
from functools import lru_cache
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any

import yaml

RAIZ = Path(__file__).resolve().parent.parent
CONFIG_DEFECTO = RAIZ / "config" / "config.yaml"


def _fusionar(base: dict, extra: dict) -> dict:
    """Fusión recursiva: los valores de `extra` sustituyen a los de `base`."""
    out = copy.deepcopy(base)
    for k, v in (extra or {}).items():
        out[k] = _fusionar(out[k], v) if isinstance(v, dict) and isinstance(out.get(k), dict) else v
    return out


@lru_cache(maxsize=4)
def cargar(ruta: str | None = None) -> dict[str, Any]:
    """Lee config/config.yaml y, si existe, config/local.yaml (no versionado) encima.
    La variable NBAEV_CONFIG permite apuntar a otro archivo."""
    ruta = Path(ruta or os.environ.get("NBAEV_CONFIG") or CONFIG_DEFECTO)
    with open(ruta, encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}
    local = ruta.with_name("local.yaml")
    if local.exists():
        with open(local, encoding="utf-8") as f:
            cfg = _fusionar(cfg, yaml.safe_load(f) or {})
    return cfg


def ruta(cfg: dict, clave: str) -> Path:
    """Ruta de general.<clave> resuelta respecto a la raíz del proyecto."""
    p = Path(cfg["general"][clave])
    return p if p.is_absolute() else RAIZ / p


def configurar_logs(cfg: dict, nombre: str = "nbaev") -> None:
    """Consola + archivo rotativo logs/nbaev.log."""
    nivel = getattr(logging, str(cfg["general"].get("nivel_log", "INFO")).upper(), logging.INFO)
    carpeta = ruta(cfg, "logs")
    carpeta.mkdir(parents=True, exist_ok=True)
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s", "%Y-%m-%d %H:%M:%S")
    raiz = logging.getLogger()
    raiz.setLevel(nivel)
    if not any(isinstance(h, RotatingFileHandler) for h in raiz.handlers):
        archivo = RotatingFileHandler(carpeta / f"{nombre}.log", maxBytes=5_000_000, backupCount=5, encoding="utf-8")
        archivo.setFormatter(fmt)
        raiz.addHandler(archivo)
        consola = logging.StreamHandler()
        consola.setFormatter(fmt)
        raiz.addHandler(consola)
    # Las librerías HTTP son muy verbosas en DEBUG.
    logging.getLogger("urllib3").setLevel(logging.WARNING)
