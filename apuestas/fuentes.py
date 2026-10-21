"""Qué fuente de datos se usa para cada cosa, y el enriquecimiento con las fuentes secundarias.

- Partidos, resultados, estadísticas, jugadores, alineaciones y cuotas 1X2/goles: ESPN (por defecto,
  sin clave ni cuota) o API-Football (`APUESTAS_FUENTE=api-football`).
- Bzzoiro (opcional, gratis con registro): árbitro, cuotas de consenso y alineaciones/bajas de respaldo.
- SportsGameOdds (opcional, 2.500 objetos al mes): cuotas de córners, tarjetas y tiros.

Las secundarias nunca bloquean el análisis: si no hay clave, se agotó su cupo o fallan, se sigue sin ellas.
"""
from __future__ import annotations

import json
import logging
import os
from datetime import date, datetime, timedelta
from pathlib import Path

import requests

from .api_football import ApiError, ApiFootball, PresupuestoAgotado
from .bzzoiro import Bzzoiro, buscar, inicio_utc
from .config import Config, ligas_filtro
from .db import Database
from .espn import LIGAS_ESPN, EspnApi
from .registro import Registro
from .sgo import SportsGameOdds

log = logging.getLogger(__name__)
ERRORES = (ApiError, PresupuestoAgotado, requests.RequestException, ValueError, KeyError)


def _datos(cfg: Config, nombre: str) -> Path:
    return cfg.db_path.parent / nombre


def cliente_partidos(cfg: Config, presupuesto: int | None = None):
    if cfg.fuente == "api-football":
        return ApiFootball(cfg.api_football_key, presupuesto or cfg.presupuesto_peticiones)
    return EspnApi(ligas_filtro(cfg) or list(LIGAS_ESPN), presupuesto or cfg.presupuesto_espn)


def cliente_bzzoiro(cfg: Config) -> Bzzoiro | None:
    if not cfg.usar_bzzoiro:
        return None
    return Bzzoiro(cfg.bzzoiro_token, registro=Registro(_datos(cfg, "uso_bzzoiro.json"), "dia"))


def cliente_sgo(cfg: Config) -> SportsGameOdds | None:
    if not cfg.usar_sgo:
        return None
    return SportsGameOdds(cfg.sgo_api_key, registro=Registro(_datos(cfg, "uso_sgo.json"), "mes"))


def _ligas_sgo(cfg: Config, sgo: SportsGameOdds) -> dict[int, str]:
    """Correspondencia de ligas con SportsGameOdds, guardada para no gastar objetos cada día."""
    path = _datos(cfg, "sgo_ligas.json")
    try:
        guardado = json.loads(path.read_text(encoding="utf-8"))
        if guardado.get("fecha", "") >= (date.today() - timedelta(days=30)).isoformat():
            return {int(k): v for k, v in guardado["ligas"].items()}
    except (OSError, ValueError, KeyError):
        pass
    ligas = sgo.ligas()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"fecha": date.today().isoformat(), "ligas": ligas}), encoding="utf-8")
    return ligas


def enriquecer(db: Database, cfg: Config, fixtures: list[dict]) -> list[str]:
    """Añade árbitro y cuotas de las fuentes secundarias a los partidos del día. Devuelve notas."""
    notas: list[str] = []
    if not fixtures:
        return notas
    inicios = {fx["id"]: inicio_utc(fx["date_utc"]) for fx in fixtures}
    desde, hasta = min(inicios.values()), max(inicios.values())

    bz = cliente_bzzoiro(cfg)
    if bz is not None:
        try:
            eventos = bz.partidos(desde.date(), hasta.date())
            n_cuotas = n_arbitros = 0
            with db.tx():
                for fx in fixtures:
                    ev = buscar(eventos, fx["home_name"], fx["away_name"], inicios[fx["id"]])
                    if ev is None:
                        continue
                    if ev["arbitro"]:
                        db.conn.execute("UPDATE fixtures SET referee = COALESCE(referee, ?) WHERE id = ?",
                                        (ev["arbitro"], fx["id"]))
                        n_arbitros += 1
                    if ev["cuotas"]:
                        db.save_odds(fx["id"], [("Bzzoiro (consenso)", b, v, o) for b, v, o in ev["cuotas"]])
                        n_cuotas += 1
            notas.append(f"Bzzoiro: cuotas de consenso en {n_cuotas} partidos y árbitro en {n_arbitros} "
                         f"({bz.peticiones} peticiones)")
        except ERRORES as e:
            notas.append(f"Bzzoiro no disponible: {e}")

    sgo = cliente_sgo(cfg)
    if sgo is not None:
        try:
            ligas = _ligas_sgo(cfg, sgo)
            buscadas = sorted({ligas[fx["league_id"]] for fx in fixtures if fx.get("league_id") in ligas})
            eventos = sgo.partidos(buscadas, desde - timedelta(hours=1), hasta + timedelta(hours=1),
                                   max_objetos=min(60, 2 * len(fixtures)))
            n = 0
            with db.tx():
                for fx in fixtures:
                    ev = buscar(eventos, fx["home_name"], fx["away_name"], inicios[fx["id"]])
                    if ev and ev["cuotas"]:
                        db.save_odds(fx["id"], ev["cuotas"])
                        n += 1
            notas.append(f"SportsGameOdds: cuotas (córners, tarjetas, tiros...) en {n} partidos; "
                         f"{sgo.registro.usadas() if sgo.registro else '?'} objetos usados este mes")
        except ERRORES as e:
            notas.append(f"SportsGameOdds no disponible: {e}")
    return notas


def estado_fuentes(cfg: Config) -> list[tuple[str, bool, str]]:
    """(fuente, ok, detalle) de cada fuente. Gasta como mucho una petición por fuente."""
    from .api_football import REGISTRO_USO, estado as estado_api, leer_registro
    out = []
    try:
        out.append(("ESPN (partidos, estadísticas, alineaciones)", True, EspnApi([39], presupuesto=1).disponible()))
    except ERRORES as e:
        out.append(("ESPN (partidos, estadísticas, alineaciones)", False, str(e)))
    for nombre, cliente in (("Bzzoiro (árbitro, consenso de cuotas, bajas)", cliente_bzzoiro(cfg)),
                            ("SportsGameOdds (cuotas de córners y tarjetas)", cliente_sgo(cfg))):
        if cliente is None:
            out.append((nombre, False, "desactivada en la configuración"))
            continue
        try:
            uso = cliente.registro.usadas() if cliente.registro else "?"
            out.append((nombre, True, f"{cliente.disponible()}; registro propio: {uso} usadas en el periodo"))
        except ERRORES as e:
            out.append((nombre, False, str(e)))
    if cfg.fuente != "api-football" and not cfg.api_football_key:
        return out
    try:
        r = estado_api(api_key=cfg.api_football_key)
        req = r.get("requests") or {}
        propio = leer_registro(REGISTRO_USO)
        out.append(("API-Football (opcional)", True, f"plan {(r.get('subscription') or {}).get('plan', '?')}; "
                    f"{max(int(req.get('current') or 0), int(propio.get('peticiones') or 0))} de "
                    f"{req.get('limit_day', '?')} hoy"))
    except (ApiError, OSError, ValueError) as e:
        out.append(("API-Football (opcional)", False, str(e)[:160]))
    return out
