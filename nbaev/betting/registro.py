"""Registro de predicciones y apuestas, liquidación con el resultado real y estado de la banca."""
from __future__ import annotations

import logging

import duckdb
import pandas as pd

from ..data import db
from . import margen as mg

log = logging.getLogger(__name__)

# Valor real de cada mercado a partir del box score.
EXPRESION = {"pts": "pts", "reb": "reb", "oreb": "oreb", "dreb": "dreb", "ast": "ast", "fg3m": "fg3m",
             "stl": "stl", "blk": "blk", "tov": "tov", "fgm": "fgm", "ftm": "ftm", "pr": "pts + reb",
             "pa": "pts + ast", "ra": "reb + ast", "pra": "pts + reb + ast", "stocks": "stl + blk"}
COLS_PRED = ["snapshot_at", "fecha", "game_id", "player_id", "jugador", "market", "period", "line", "lado", "book",
             "cuota", "proyeccion", "p_modelo", "p_justa", "p_final", "p_empate", "edge", "ev", "p_valor", "pasa_bh",
             "estado_mercado", "pick", "monto", "motivo_descarte"]


def guardar_predicciones(con: duckdb.DuckDBPyConnection, tabla: pd.DataFrame, snapshot_at, fecha) -> int:
    t = tabla.rename(columns={"name": "jugador"}).assign(snapshot_at=snapshot_at, fecha=fecha)
    return db.upsert(con, "predicciones", t[[c for c in COLS_PRED if c in t.columns]])


def registrar_sugeridas(con: duckdb.DuckDBPyConnection, tabla: pd.DataFrame, fecha, partidos: dict) -> int:
    """Guarda como 'sugerida' cada pick con monto > 0 que no esté ya registrado ese día."""
    picks = tabla[tabla["pick"] & (tabla["monto"] > 0)]
    n = 0
    for r in picks.itertuples():
        ya = con.execute("""SELECT 1 FROM apuestas WHERE game_id = ? AND player_id = ? AND market = ? AND period = ?
                            AND line = ? AND lado = ? AND estado <> 'descartada'""",
                         [r.game_id, r.player_id, r.market, r.period, r.line, r.lado]).fetchone()
        if ya:
            continue
        con.execute("""INSERT INTO apuestas (creada_at, fecha, game_id, player_id, jugador, partido, market, period, line,
                       lado, book, cuota, p_modelo, p_final, edge, ev, monto, estado, resultado)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'sugerida', 'pendiente')""",
                    [db.ahora_utc(), fecha, r.game_id, r.player_id, r.name, partidos.get(r.game_id, r.game_id), r.market,
                     r.period, r.line, r.lado, r.book, r.cuota, r.p_modelo, r.p_final, r.edge, r.ev, r.monto])
        n += 1
    return n


def confirmar(con: duckdb.DuckDBPyConnection, id_: int, cuota: float | None = None, monto: float | None = None) -> None:
    """El usuario hizo la apuesta (con la cuota y el monto reales, si difieren de los sugeridos)."""
    con.execute("""UPDATE apuestas SET estado = 'confirmada', cuota = coalesce(?, cuota), monto = coalesce(?, monto)
                   WHERE id = ?""", [cuota, monto, id_])


def descartar(con: duckdb.DuckDBPyConnection, id_: int) -> None:
    con.execute("UPDATE apuestas SET estado = 'descartada' WHERE id = ?", [id_])


def cierre_de(con: duckdb.DuckDBPyConnection, r) -> tuple[float | None, float | None]:
    """Cuota y probabilidad justa de cierre del lado apostado: cierre de consenso con la misma línea o,
    si no hay, la última captura de esa casa antes del inicio del partido."""
    filas = con.execute("""
        SELECT side, odds FROM prop_odds
        WHERE game_id = ? AND player_id = ? AND market = ? AND period = ? AND line = ? AND kind = 'cierre'
          AND book = 'consenso'""", [r["game_id"], r["player_id"], r["market"], r["period"], r["line"]]).fetchall()
    if len(filas) < 2:
        filas = con.execute("""
            SELECT side, arg_max(odds, snapshot_at) FROM prop_odds
            WHERE game_id = ? AND player_id = ? AND market = ? AND period = ? AND line = ? AND kind = 'captura'
              AND book = ? AND snapshot_at < start_utc GROUP BY side""",
                            [r["game_id"], r["player_id"], r["market"], r["period"], r["line"], r["book"]]).fetchall()
    lados = dict(filas)
    if r["lado"] not in lados:
        return None, None
    otro = "under" if r["lado"] == "over" else "over"
    p = mg.justa_dos_lados([lados[r["lado"]]], [lados[otro]])[0] if otro in lados else None
    return float(lados[r["lado"]]), (float(p) if p is not None else None)


def liquidar(con: duckdb.DuckDBPyConnection) -> int:
    """Liquida las apuestas pendientes de partidos terminados. Si el jugador no jugó, la apuesta es nula."""
    pend = con.execute("""SELECT a.* FROM apuestas a JOIN games g USING (game_id)
                          WHERE a.resultado = 'pendiente' AND a.estado <> 'descartada' AND g.box_ok""").df()
    n = 0
    for _, r in pend.iterrows():
        expr = EXPRESION.get(r["market"])
        if expr is None or r["period"] != "game":
            continue        # mercados por periodo, sí/no y comparativos: fase 6
        fila = con.execute(f"SELECT {expr} FROM player_games WHERE game_id = ? AND player_id = ?",
                           [r["game_id"], r["player_id"]]).fetchone()
        if fila is None:
            resultado, valor, ganancia = "nula", None, 0.0
        else:
            valor = float(fila[0])
            if valor == r["line"]:
                resultado, ganancia = "nula", 0.0
            else:
                gana = valor > r["line"] if r["lado"] == "over" else valor < r["line"]
                resultado = "ganada" if gana else "perdida"
                ganancia = r["monto"] * (r["cuota"] - 1) if gana else -r["monto"]
        cuota_c, p_c = cierre_de(con, r)
        clv = r["cuota"] * p_c - 1 if p_c else None
        con.execute("""UPDATE apuestas SET resultado = ?, valor_real = ?, ganancia = ?, cuota_cierre = ?,
                       p_justa_cierre = ?, clv = ?, liquidada_at = ? WHERE id = ?""",
                    [resultado, valor, ganancia, cuota_c, p_c, clv, db.ahora_utc(), int(r["id"])])
        n += 1
    return n


def banca_actual(con: duckdb.DuckDBPyConnection, inicial: float) -> float:
    """Banca inicial + ganancias de las apuestas confirmadas ya liquidadas."""
    g = con.execute("SELECT coalesce(sum(ganancia), 0) FROM apuestas WHERE estado = 'confirmada' "
                    "AND resultado <> 'pendiente'").fetchone()[0]
    return float(inicial + g)


def resumen(con: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    """Rendimiento real por estado y mercado: apuestas, monto, ganancia, yield y CLV medio."""
    return con.execute("""
        SELECT estado, market, count(*) AS apuestas, sum(CAST(resultado = 'pendiente' AS INT)) AS pendientes,
               round(sum(monto), 2) AS monto, round(sum(ganancia), 2) AS ganancia,
               round(sum(ganancia) / nullif(sum(CASE WHEN resultado <> 'pendiente' THEN monto END), 0), 4) AS yield,
               round(avg(clv), 4) AS clv_medio
        FROM apuestas GROUP BY ALL ORDER BY 1, 2""").df()
