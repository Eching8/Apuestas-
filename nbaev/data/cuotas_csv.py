"""Carga manual de cuotas (por ejemplo de bet365) desde CSV. Plantilla: plantillas/cuotas_manual.csv

Columnas obligatorias:
  capturado   fecha y hora de la captura, ISO 8601 con zona (2026-10-26T18:05:00-06:00);
              sin zona se interpreta en general.zona_horaria
  casa        bet365, ...
  fecha       fecha del partido (AAAA-MM-DD, calendario de EE. UU.)
  local, visitante  abreviatura (LAL), apodo (Lakers) o nombre completo del equipo
  jugador     nombre como lo escribe la casa
  mercado     pts, reb, oreb, dreb, ast, fg3m, stl, blk, tov, fgm, ftm, pr, pa, ra, pra, stocks,
              doble_doble, triple_doble, primera_canasta, primera_canasta_equipo, ... (otro texto = mercado nuevo)
  periodo     game, 1q, 1h
  linea       número (vacío en mercados sí/no)
  lado        over, under, yes, no
  cuota       decimal (1.90) o americana (-110, +150)
Opcional: tipo (captura | apertura | cierre).
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

import duckdb
import pandas as pd

from . import db
from .cuotas_sgo import MODELADOS, actualizar_catalogo, americana_a_decimal
from .nombres import clave_nombre, emparejar_jugadores

log = logging.getLogger(__name__)

OBLIGATORIAS = ["capturado", "casa", "fecha", "local", "visitante", "jugador", "mercado", "periodo", "linea",
                "lado", "cuota"]
LADOS = {"over", "under", "yes", "no"}


def a_decimal(v) -> float | None:
    try:
        x = float(str(v).strip().replace(",", "."))
    except ValueError:
        return None
    if 1.0 < x < 100:
        return x
    return americana_a_decimal(x)


def a_utc(v, zona: str) -> datetime:
    t = pd.Timestamp(v)
    if t.tzinfo is None:
        t = t.tz_localize(ZoneInfo(zona))
    return t.tz_convert(timezone.utc).tz_localize(None).to_pydatetime()


def _equipo(con, texto: str) -> str | None:
    k = clave_nombre(texto)
    for tid, abbr, name, nick in con.execute("SELECT team_id, abbr, name, nickname FROM teams").fetchall():
        if k in {clave_nombre(abbr or ""), clave_nombre(name or ""), clave_nombre(nick or "")}:
            return tid
    return None


def importar(con: duckdb.DuckDBPyConnection, archivo: str, kind: str = "captura", zona: str = "America/Mexico_City") -> dict:
    df = pd.read_csv(archivo, dtype=str).fillna("")
    faltan = [c for c in OBLIGATORIAS if c not in df.columns]
    if faltan:
        raise ValueError(f"Faltan columnas en {archivo}: {faltan}")
    errores, filas = [], []
    for i, r in df.iterrows():
        linea_csv = i + 2
        cuota = a_decimal(r["cuota"])
        lado = r["lado"].strip().lower()
        if cuota is None or lado not in LADOS:
            errores.append(f"fila {linea_csv}: cuota o lado no válidos")
            continue
        h, a = _equipo(con, r["local"]), _equipo(con, r["visitante"])
        partido = con.execute("SELECT game_id, start_utc FROM games WHERE fecha = ? AND home_id = ? AND away_id = ?",
                              [r["fecha"], h, a]).fetchone() if h and a else None
        if not partido:
            errores.append(f"fila {linea_csv}: no encuentro el partido {r['visitante']} @ {r['local']} del {r['fecha']}")
            continue
        try:
            linea = float(r["linea"].replace(",", ".")) if r["linea"].strip() else None
        except ValueError:
            errores.append(f"fila {linea_csv}: línea no válida")
            continue
        mercado = r["mercado"].strip().lower()
        filas.append({
            "source": "csv", "kind": (r.get("tipo") or kind).strip() or kind,
            "snapshot_at": a_utc(r["capturado"], zona), "book": r["casa"].strip().lower(),
            "event_id": partido[0], "game_id": partido[0], "start_utc": partido[1],
            "stat_id": mercado, "market": mercado if mercado in MODELADOS else None,
            "period": r["periodo"].strip().lower() or "game", "bet_type": "ou" if linea is not None else "yn",
            "source_player_id": clave_nombre(r["jugador"]), "player_name": r["jugador"].strip(),
            "side": lado, "line": linea, "odds": cuota, "_equipos": [h, a],
        })
    for gid in {f["game_id"] for f in filas}:
        del_partido = [f for f in filas if f["game_id"] == gid]
        mapa = emparejar_jugadores(con, "csv", {f["source_player_id"]: f["player_name"] for f in del_partido},
                                   del_partido[0]["_equipos"], del_partido[0]["start_utc"])
        for f in del_partido:
            f["player_id"], f["team_id"] = mapa.get(f["source_player_id"], (None, None))
            if f["player_id"] is None:
                errores.append(f"jugador sin emparejar: {f['player_name']} (se guarda igual)")
    for f in filas:
        f.pop("_equipos")
    # Los mercados del CSV también se registran en el catálogo, con su propia fuente.
    nuevos = actualizar_catalogo(con, filas)
    n = db.insertar(con, "prop_odds", filas)
    for e in errores[:30]:
        log.warning(e)
    return {"filas": len(df), "importadas": n, "errores": len(errores), "mercados_nuevos": nuevos}
