"""Comprueba con The Odds API las cuotas de las apuestas registradas del usuario (`apuestas_usuario/nfl/AAAA-MM-DD.json`)
y si Betano aparece entre las casas.

Gasta poco: la búsqueda de Betano es una consulta h2h de 1 crédito por región (eu primero, uk solo si eu no la trae) y
las cuotas se piden solo para los partidos de las patas que aún no han empezado y solo con los mercados de esas patas
(1 crédito por mercado y región). Nunca baja de la reserva de créditos.
"""
from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from statistics import median

from ..nba.sgo import clave_nombre
from . import equipos
from .db import NflDB
from .theodds import DEPORTE, TheOddsApiNfl
from .usuario import DIR

log = logging.getLogger(__name__)

# (estadística, lado) -> mercado de The Odds API. "2+ TD" es el over 1.5 de player_tds_over.
MERCADO = {"comp": "player_pass_completions", "rec": "player_receptions", "pass_tds": "player_pass_tds",
           "rec_yds": "player_reception_yds", "pass_yds": "player_pass_yds", "rush_yds": "player_rush_yds",
           "rush_att": "player_rush_attempts", "tds": "player_tds_over"}
LADO = {"más": "over", "menos": "under"}
CASA = "betano"


def buscar_betano(api: TheOddsApiNfl, regiones=("eu", "uk")) -> tuple[str | None, dict[str, list[str]]]:
    """La primera región donde aparece Betano (o None) y las casas vistas en cada región consultada."""
    vistas: dict[str, list[str]] = {}
    for region in regiones:
        datos = api._get(f"/sports/{DEPORTE}/odds", regions=region, markets="h2h", oddsFormat="decimal")
        casas = sorted({c["key"] for ev in datos for c in ev.get("bookmakers", [])})
        vistas[region] = casas
        if CASA in casas:
            return region, vistas
    return None, vistas


def _equipo(nfl: NflDB, pata: dict) -> str | None:
    if pata.get("equipo"):
        return equipos.por_texto(pata["equipo"])
    clave = clave_nombre(pata["jugador"])
    for r in nfl.conn.execute("SELECT name, team FROM nfl_rosters ORDER BY season DESC"):
        if clave_nombre(r["name"] or "") == clave:
            return r["team"]
    return None


def verificar(nfl: NflDB, api: TheOddsApiNfl, fecha: str, carpeta: Path = DIR, solo_reales: bool = True,
              reserva: int = 100, regiones: str = "us") -> str:
    datos = json.loads((carpeta / f"{fecha}.json").read_text(encoding="utf-8"))
    apuestas = [a for a in datos["apuestas"] if a.get("real") or not solo_reales]
    lineas = [f"# Verificación de cuotas con The Odds API ({fecha})", ""]

    region_betano, vistas = buscar_betano(api)
    for region, casas in vistas.items():
        lineas.append(f"- Casas de la NFL en la región **{region}**: {', '.join(casas) or '(ninguna)'}")
    lineas.append(f"- **Betano**: {'sí, en la región ' + region_betano if region_betano else 'no aparece'}"
                  f" (créditos restantes: {api.restantes})")
    lineas.append("")
    if region_betano and region_betano not in regiones.split(","):
        regiones = f"{regiones},{region_betano}"

    # Partido de cada pata y mercados que hacen falta por partido.
    ahora = datetime.now(timezone.utc)
    eventos = api._get(f"/sports/{DEPORTE}/events")
    por_equipo = {}
    for ev in eventos:
        for lado in ("home_team", "away_team"):
            t = equipos.por_nombre_largo(ev.get(lado) or "")
            if t and t not in por_equipo:
                por_equipo[t] = ev
    patas = []
    for ap in apuestas:
        for p in ap["patas"]:
            ev = por_equipo.get(_equipo(nfl, p))
            patas.append((ap, p, ev))
    pedir: dict[str, set[str]] = {}
    for _, p, ev in patas:
        if ev and p["stat"] in MERCADO and datetime.fromisoformat(ev["commence_time"].replace("Z", "+00:00")) > ahora:
            pedir.setdefault(ev["id"], set()).add(MERCADO[p["stat"]])

    n_regiones = len(regiones.split(","))
    odds: dict[str, dict] = {}
    for ev_id, mercados in pedir.items():
        creditos = api.creditos()
        if creditos is not None and creditos < reserva + len(mercados) * n_regiones:
            log.warning("The Odds API: quedan %d créditos (reserva %d); no pido más partidos.", creditos, reserva)
            break
        odds[ev_id] = api._get(f"/sports/{DEPORTE}/events/{ev_id}/odds", regions=regiones,
                               markets=",".join(sorted(mercados)), oddsFormat="decimal")

    for ap in apuestas:
        lineas.append(f"## {ap['nombre']} (cuota {ap.get('cuota')})")
        lineas.append("")
        lineas.append("| Pata | Partido | Cuota registrada | Betano | Mediana de las casas | Casas |")
        lineas.append("|---|---|---|---|---|---|")
        for ap2, p, ev in patas:
            if ap2 is not ap:
                continue
            texto = f"{p['jugador']} {p['lado']} {p['linea']} {p['stat']}"
            if ev is None:
                lineas.append(f"| {texto} | (sin partido) | {p.get('cuota')} | | | |")
                continue
            partido = f"{ev['away_team']} @ {ev['home_team']}"
            if ev["id"] not in odds:
                motivo = "ya empezó" if ev["id"] not in pedir else "sin créditos"
                lineas.append(f"| {texto} | {partido} | {p.get('cuota')} | | ({motivo}) | |")
                continue
            precios = _precios(odds[ev["id"]], p)
            casas = ", ".join(f"{k} {v:.2f}" for k, v in sorted(precios.items()))
            med = f"{median(precios.values()):.2f}" if precios else "no la ofrecen"
            bet = f"{precios[CASA]:.2f}" if CASA in precios else "—"
            lineas.append(f"| {texto} | {partido} | {p.get('cuota')} | {bet} | {med} | {casas} |")
        lineas.append("")
    lineas.append(f"Consultas: {api.peticiones}; créditos restantes: {api.restantes}.")
    return "\n".join(lineas)


def _precios(evento: dict, pata: dict) -> dict[str, float]:
    """Cuota de cada casa para la línea exacta y el lado de la pata."""
    mercado, lado, clave = MERCADO[pata["stat"]], LADO[pata["lado"]], clave_nombre(pata["jugador"])
    out = {}
    for casa in evento.get("bookmakers", []):
        for m in casa.get("markets", []):
            if m.get("key") != mercado:
                continue
            for o in m.get("outcomes", []):
                if ((o.get("name") or "").lower() == lado and clave_nombre(o.get("description") or "") == clave
                        and o.get("point") is not None and float(o["point"]) == float(pata["linea"])):
                    out[casa["key"]] = float(o["price"])
    return out
