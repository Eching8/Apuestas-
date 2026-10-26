"""Contexto de cada equipo en cada partido: local/visitante, descanso, back-to-back, viajes y total implícito.

Todo sale del calendario (conocido de antemano) y de las líneas previas al partido, así que no hay fuga:
para el partido del día D solo se miran partidos anteriores del mismo equipo.
"""
from __future__ import annotations

import math

import duckdb
import pandas as pd


# Pabellón de cada equipo (abreviatura de ESPN): latitud, longitud y huso horario respecto a UTC
# en horario estándar (solo importan las diferencias entre ciudades).
ARENAS = {
    "ATL": (33.757, -84.396, -5), "BOS": (42.366, -71.062, -5), "BKN": (40.683, -73.976, -5),
    "CHA": (35.225, -80.839, -5), "CHI": (41.881, -87.674, -6), "CLE": (41.497, -81.688, -5),
    "DAL": (32.790, -96.810, -6), "DEN": (39.749, -105.008, -7), "DET": (42.341, -83.055, -5),
    "GS": (37.768, -122.388, -8), "HOU": (29.751, -95.362, -6), "IND": (39.764, -86.155, -5),
    "LAC": (33.945, -118.343, -8), "LAL": (34.043, -118.267, -8), "MEM": (35.138, -90.051, -6),
    "MIA": (25.781, -80.188, -5), "MIL": (43.045, -87.917, -6), "MIN": (44.980, -93.276, -6),
    "NO": (29.949, -90.082, -6), "NY": (40.751, -73.993, -5), "OKC": (35.463, -97.515, -6),
    "ORL": (28.539, -81.384, -5), "PHI": (39.901, -75.172, -5), "PHX": (33.446, -112.071, -7),
    "POR": (45.532, -122.667, -8), "SAC": (38.580, -121.500, -8), "SA": (29.427, -98.438, -6),
    "TOR": (43.643, -79.379, -5), "UTAH": (40.768, -111.901, -7), "WSH": (38.898, -77.021, -5),
}
# Preferencia de fuente para spread/total previos. El "cierre" de partido de SportsGameOdds no se usa:
# frente a DraftKings (ESPN) tiene correlación 0,71 en el spread y diferencias de >3 puntos en 1 de cada 4
# partidos (parece capturado ya en juego); su apertura sí cuadra (0,96) y queda como último recurso.
PRIORIDAD_LINEAS = ["espn:%|cierre", "espn_core:%|cierre", "espn:%|captura%", "sgo|captura%", "sgo|apertura"]
SPREAD_MAX, TOTAL_MIN, TOTAL_MAX = 25.0, 185.0, 265.0


def km(a: tuple, b: tuple) -> float:
    """Distancia del círculo máximo en km."""
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * 6371 * math.asin(math.sqrt(h))


def lineas_previas(con: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    """Una línea por partido (spread del local y total), según PRIORIDAD_LINEAS."""
    # Para partidos futuros solo hay capturas (la más reciente gana: kind = "captura AAAA-MM-DDTHH:MM").
    df = con.execute("SELECT game_id, source, kind, spread_home, total FROM game_lines ORDER BY kind DESC").df()
    if df.empty:
        return pd.DataFrame(columns=["game_id", "spread_home", "total", "linea_fuente"])
    plausible = df["total"].between(TOTAL_MIN, TOTAL_MAX) & (df["spread_home"].abs() <= SPREAD_MAX)
    df = df[plausible].copy()
    df["rango"] = 99
    for i, regla in enumerate(PRIORIDAD_LINEAS):
        fuente, kind = regla.split("|")
        coincide = (df["source"].str.match(fuente.replace("%", ".*") + "$")
                    & df["kind"].str.match(kind.replace("%", ".*") + "$"))
        df.loc[coincide & (df["rango"] == 99), "rango"] = i
    df = df[df["rango"] < 99].dropna(subset=["total"]).sort_values("rango", kind="stable").drop_duplicates("game_id")
    df["linea_fuente"] = df["source"] + "|" + df["kind"]
    return df[["game_id", "spread_home", "total", "linea_fuente"]]


def calcular(con: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    g = con.execute("""
        SELECT g.game_id, g.start_utc, g.fecha, g.season, g.neutral, g.home_id, g.away_id,
               h.abbr AS home_abbr, a.abbr AS away_abbr
        FROM games g JOIN teams h ON h.team_id = g.home_id JOIN teams a ON a.team_id = g.away_id""").df()
    if g.empty:
        return pd.DataFrame()
    filas = []
    for lado, otro in (("home", "away"), ("away", "home")):
        d = pd.DataFrame({
            "game_id": g["game_id"], "team_id": g[f"{lado}_id"], "opp_id": g[f"{otro}_id"],
            "is_home": lado == "home", "start_utc": g["start_utc"], "fecha": pd.to_datetime(g["fecha"]),
            "season": g["season"],
            # El partido se juega en la ciudad del local (los partidos en sede neutral se aproximan así).
            "sede": g["home_abbr"],
        })
        filas.append(d)
    t = pd.concat(filas).sort_values(["team_id", "start_utc"]).reset_index(drop=True)
    prev = t.groupby("team_id")
    t["fecha_prev"] = prev["fecha"].shift(1)
    t["sede_prev"] = prev["sede"].shift(1)
    t["season_prev"] = prev["season"].shift(1)
    nueva = t["season_prev"] != t["season"]
    t["dias_descanso"] = ((t["fecha"] - t["fecha_prev"]).dt.days - 1).where(~nueva)
    t["b2b"] = t["dias_descanso"] == 0
    # Partidos en los últimos 4 y 7 días contando el actual (3 en 4, 4 en 6...).
    t = t.set_index("fecha")
    t["partidos_4d"] = t.groupby("team_id")["game_id"].transform(lambda s: s.rolling("4D").count())
    t["partidos_7d"] = t.groupby("team_id")["game_id"].transform(lambda s: s.rolling("7D").count())
    t = t.reset_index()

    def viaje(r):
        if pd.isna(r["sede_prev"]) or r["sede"] not in ARENAS or r["sede_prev"] not in ARENAS:
            return 0.0, 0
        a, b = ARENAS[r["sede_prev"]], ARENAS[r["sede"]]
        return km(a, b), b[2] - a[2]

    v = t.apply(viaje, axis=1, result_type="expand")
    t["km_viaje"], t["cambio_huso"] = v[0].round(0), v[1].astype(int)
    t.loc[nueva, ["km_viaje", "cambio_huso"]] = 0

    # Total implícito: (total - spread del equipo) / 2. spread_home negativo = local favorito.
    l = lineas_previas(con)
    t = t.merge(l, on="game_id", how="left")
    t["spread_equipo"] = t["spread_home"].where(t["is_home"], -t["spread_home"])
    t["total_implicito"] = (t["total"] - t["spread_equipo"]) / 2
    t["total_implicito_rival"] = t["total"] - t["total_implicito"]
    cols = ["game_id", "team_id", "opp_id", "is_home", "start_utc", "dias_descanso", "b2b", "partidos_4d",
            "partidos_7d", "km_viaje", "cambio_huso", "spread_equipo", "total", "total_implicito",
            "total_implicito_rival", "linea_fuente"]
    return t[cols]


def guardar(con: duckdb.DuckDBPyConnection) -> int:
    df = calcular(con)
    con.execute("DROP TABLE IF EXISTS team_context")
    if df.empty:
        return 0
    con.register("_ctx", df)
    con.execute("CREATE TABLE team_context AS SELECT * FROM _ctx")
    con.unregister("_ctx")
    return len(df)
