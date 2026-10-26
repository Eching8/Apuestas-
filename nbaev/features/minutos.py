"""Features para proyectar minutos (etapa A del modelo).

Población: cada jugador "vestido" para un partido, es decir, que jugó o que estaba disponible y no
jugó por decisión técnica (DNP-CD, minutos = 0). Los lesionados no son población: se sabe antes del
partido que no juegan (parte de lesiones). ESPN casi nunca lista a los lesionados en el box score, así
que las bajas de compañeros no se cuentan jugador a jugador: se mide cuántos minutos "habituales" hay
disponibles en el equipo y se compara con lo normal en ese equipo (minutos liberados).

Sin fuga: toda estadística del jugador o del equipo se calcula con `shift(1)` sobre partidos anteriores.
Lo único del propio partido es quién está disponible (conocido por el parte de lesiones y la lista de
inactivos) y el contexto previo (local, descanso, viaje, spread y total).
"""
from __future__ import annotations

import duckdb
import numpy as np
import pandas as pd

MINUTOS_PARTIDO = 240.0

# Columnas de entrada del modelo LightGBM.
FEATURES = [
    "min_ewm3", "min_ewm10", "min_temp", "min_temp_ant", "min_ult", "min_max10", "min_std10",
    "n_temp", "n_equipo", "titular_ewm", "titular_ult", "dnp_ewm", "pf36_ewm", "dias_desde",
    "cambio_equipo", "min_norm", "rango_equipo", "n_disponibles", "suma_base", "libres", "libres_pos",
    "is_home", "b2b", "dias_descanso", "partidos_4d", "km_viaje", "spread_abs", "spread_equipo", "total",
    "playoffs", "pos_g", "pos_f", "pos_c", "partido_temp",
]


def grupo_posicion(pos: str | None) -> str:
    """G (base/escolta), F (alero/ala-pívot) o C (pívot)."""
    p = (pos or "").upper()
    if p.startswith("C"):
        return "C"
    if p in ("PF", "SF", "F", "GF") or p.startswith("F"):
        return "F"
    return "G"


def cargar(con: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    """Filas jugador-partido (jugó o DNP técnico) con el contexto del partido."""
    return con.execute("""
        WITH filas AS (
            SELECT game_id, player_id, team_id, name, position, starter, minutes, pf, TRUE AS vestido
            FROM player_games
            UNION ALL
            SELECT game_id, player_id, team_id, name, position, FALSE, 0.0, 0, TRUE
            FROM player_absences WHERE kind = 'tecnica'
        )
        SELECT f.*, g.start_utc, g.fecha, g.season, g.season_type,
               c.opp_id, c.is_home, c.b2b, c.dias_descanso, c.partidos_4d, c.km_viaje, c.spread_equipo, c.total
        FROM filas f JOIN games g USING (game_id)
        LEFT JOIN team_context c ON c.game_id = f.game_id AND c.team_id = f.team_id
        WHERE g.status = 'STATUS_FINAL'
        ORDER BY f.player_id, g.start_utc""").df()


def _ewm_prev(s: pd.Series, grupos: pd.Series, halflife: float) -> pd.Series:
    """Media exponencial de los valores ANTERIORES de cada grupo (excluye la fila actual)."""
    return s.groupby(grupos).transform(lambda x: x.shift(1).ewm(halflife=halflife, min_periods=1).mean())


def construir(df: pd.DataFrame) -> pd.DataFrame:
    """Añade las features. `df` debe venir de `cargar` (o tener sus columnas) y puede incluir filas
    de partidos futuros con minutes = NaN: sus features usan solo las filas anteriores."""
    df = df.sort_values(["player_id", "start_utc"]).reset_index(drop=True)
    pid = df["player_id"]
    m = df["minutes"]
    jug = df.groupby("player_id")

    # --- Historial del jugador -----------------------------------------------------------------
    df["min_ewm3"] = _ewm_prev(m, pid, 3)
    df["min_ewm10"] = _ewm_prev(m, pid, 10)
    df["min_ult"] = jug["minutes"].shift(1)
    df["min_max10"] = jug["minutes"].transform(lambda x: x.shift(1).rolling(10, min_periods=1).max())
    df["min_std10"] = jug["minutes"].transform(lambda x: x.shift(1).rolling(10, min_periods=3).std())
    ps = df["player_id"] + "|" + df["season"].astype(str)
    df["min_temp"] = m.groupby(ps).transform(lambda x: x.shift(1).expanding().mean())
    df["n_temp"] = df.groupby(ps).cumcount()
    # Media de la temporada anterior completa (conocida al empezar la siguiente).
    media_temp = df.groupby(["player_id", "season"])["minutes"].mean().rename("min_temp_ant").reset_index()
    media_temp["season"] += 1
    df = df.merge(media_temp, on=["player_id", "season"], how="left")
    titular = df["starter"].astype(float)
    df["titular_ewm"] = _ewm_prev(titular, df["player_id"], 5)
    df["titular_ult"] = df.groupby("player_id")["starter"].shift(1).astype(float)
    df["dnp_ewm"] = _ewm_prev((df["minutes"] == 0).astype(float).where(df["minutes"].notna()), df["player_id"], 5)
    pf_ewm = _ewm_prev(df["pf"].astype(float), df["player_id"], 10)
    df["pf36_ewm"] = 36 * pf_ewm / df["min_ewm10"].clip(lower=5)
    df["dias_desde"] = df.groupby("player_id")["start_utc"].diff().dt.total_seconds() / 86400
    equipo_prev = df.groupby("player_id")["team_id"].shift(1)
    df["cambio_equipo"] = (equipo_prev.notna() & (equipo_prev != df["team_id"])).astype(float)
    df["n_equipo"] = df.groupby(["player_id", "team_id"]).cumcount()

    # Base del jugador: mezcla de corto y largo plazo; sin historia, la temporada anterior o 0.
    base = 0.5 * df["min_ewm3"] + 0.5 * df["min_ewm10"]
    df["min_base"] = base.fillna(df["min_temp_ant"]).fillna(0.0)

    # --- Equipo en este partido: minutos habituales disponibles -----------------------------------
    # prob_juega = 1 en el histórico (estaban vestidos); en partidos futuros sale del parte de lesiones.
    if "prob_juega" not in df.columns:
        df["prob_juega"] = 1.0
    df["prob_juega"] = df["prob_juega"].fillna(1.0)
    df["min_base_disp"] = df["min_base"] * df["prob_juega"]
    df["pos_grupo"] = df["position"].map(grupo_posicion)
    tg = df.groupby(["game_id", "team_id"])
    df["suma_base"] = tg["min_base_disp"].transform("sum")
    df["n_disponibles"] = tg["min_base"].transform("size")
    df["min_norm"] = df["min_base"] * MINUTOS_PARTIDO / df["suma_base"].clip(lower=1)
    df["rango_equipo"] = tg["min_base"].rank(ascending=False, method="first")
    # Lo "normal" del equipo: media exponencial de su suma_base en partidos anteriores.
    eq = (df.groupby(["game_id", "team_id"]).agg(suma_base=("suma_base", "first"), start_utc=("start_utc", "first"))
          .reset_index().sort_values(["team_id", "start_utc"]))
    eq["suma_habitual"] = eq.groupby("team_id")["suma_base"].transform(lambda x: x.shift(1).ewm(halflife=5).mean())
    pos = (df.groupby(["game_id", "team_id", "pos_grupo"]).agg(suma_pos=("min_base_disp", "sum"), start_utc=("start_utc", "first"))
           .reset_index().sort_values(["team_id", "pos_grupo", "start_utc"]))
    pos["suma_pos_habitual"] = pos.groupby(["team_id", "pos_grupo"])["suma_pos"].transform(
        lambda x: x.shift(1).ewm(halflife=5).mean())
    df = df.merge(eq[["game_id", "team_id", "suma_habitual"]], on=["game_id", "team_id"], how="left")
    df = df.merge(pos[["game_id", "team_id", "pos_grupo", "suma_pos", "suma_pos_habitual"]],
                  on=["game_id", "team_id", "pos_grupo"], how="left")
    df["libres"] = (df["suma_habitual"] - df["suma_base"]).fillna(0.0)
    df["libres_pos"] = (df["suma_pos_habitual"] - df["suma_pos"]).fillna(0.0)

    # --- Contexto ---------------------------------------------------------------------------------
    df["spread_abs"] = df["spread_equipo"].abs()
    df["playoffs"] = (df["season_type"] == 3).astype(float)
    df["is_home"] = df["is_home"].astype(float)
    df["b2b"] = df["b2b"].astype(float)
    for g in ("G", "F", "C"):
        df[f"pos_{g.lower()}"] = (df["pos_grupo"] == g).astype(float)
    orden = (df.groupby(["team_id", "season", "game_id"])["start_utc"].first().reset_index()
             .sort_values(["team_id", "start_utc"]))
    orden["partido_temp"] = orden.groupby(["team_id", "season"]).cumcount() + 1
    df = df.merge(orden[["team_id", "game_id", "partido_temp"]], on=["team_id", "game_id"], how="left")
    return df.sort_values(["start_utc", "game_id", "team_id", "player_id"]).reset_index(drop=True)


def dataset(con: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    return construir(cargar(con))


# --- Partidos futuros -----------------------------------------------------------------------------

def plantilla_probable(con: duckdb.DuckDBPyConnection, team_id: str, antes_de, n_partidos: int = 5) -> pd.DataFrame:
    """Jugadores que aparecieron (jugaron o vestidos) con el equipo en sus últimos `n_partidos` y cuya
    última aparición fue con este equipo (si después jugó con otro, se fue traspasado). La ventana es
    corta a propósito: con una larga, a principio de temporada entran jugadores de la temporada pasada
    que ya no se visten. Quien vuelve de una baja larga entra por el parte de lesiones."""
    return con.execute("""
        WITH apariciones AS (
            SELECT p.player_id, p.team_id, p.name, p.position, g.start_utc FROM player_games p JOIN games g USING (game_id)
            WHERE g.start_utc < ?
            UNION ALL
            SELECT a.player_id, a.team_id, a.name, a.position, g.start_utc FROM player_absences a JOIN games g USING (game_id)
            WHERE g.start_utc < ? AND a.kind = 'tecnica'
        ),
        del_equipo AS (
            SELECT game_id, season, start_utc FROM games
            WHERE (home_id = ? OR away_id = ?) AND start_utc < ? AND status = 'STATUS_FINAL'
        ),
        -- Con 2 o más partidos en la temporada actual, la temporada pasada ya no cuenta (la plantilla cambia).
        temporada AS (SELECT max(season) AS s, count(*) FILTER (WHERE season = (SELECT max(season) FROM del_equipo)) AS n
                      FROM del_equipo),
        recientes AS (
            SELECT game_id FROM del_equipo, temporada
            WHERE temporada.n < 2 OR del_equipo.season = temporada.s
            ORDER BY start_utc DESC LIMIT ?
        ),
        ultima AS (
            SELECT player_id, arg_max(team_id, start_utc) AS team_id, arg_max(name, start_utc) AS name,
                   arg_max(position, start_utc) AS position
            FROM apariciones GROUP BY player_id
        )
        SELECT u.* FROM ultima u
        WHERE u.team_id = ? AND u.player_id IN (
            SELECT player_id FROM player_games WHERE game_id IN (SELECT game_id FROM recientes) AND team_id = ?
            UNION SELECT player_id FROM player_absences WHERE game_id IN (SELECT game_id FROM recientes)
                  AND team_id = ? AND kind = 'tecnica')""",
        [antes_de, antes_de, team_id, team_id, antes_de, n_partidos, team_id, team_id, team_id]).df()


def prob_juega(estado: str | None, tabla: dict[str, float]) -> float:
    """Probabilidad de jugar según el estado del parte de lesiones (sin estado = disponible)."""
    if not estado:
        return 1.0
    e = estado.strip().lower()
    for clave, p in tabla.items():
        if clave.lower() == e:
            return float(p)
    return float(tabla.get("otro", 0.5))


def filas_futuras(con: duckdb.DuckDBPyConnection, game_ids: list[str], corte, tabla_estados: dict[str, float]
                  ) -> pd.DataFrame:
    """Filas (sin minutos) de los jugadores probables de cada partido, con su estado en el parte de
    lesiones conocido en `corte`. Los que tienen probabilidad 0 (Out) se excluyen."""
    from ..data import asof
    lesiones = asof.lesiones_en(con, corte)
    estado = dict(zip(lesiones["player_id"], lesiones["status"])) if not lesiones.empty else {}
    partidos = con.execute("""
        SELECT g.game_id, g.start_utc, g.fecha, g.season, g.season_type, g.home_id, g.away_id
        FROM games g WHERE g.game_id IN (SELECT unnest(?))""", [game_ids]).df()
    ctx = con.execute("SELECT * FROM team_context WHERE game_id IN (SELECT unnest(?))", [game_ids]).df()
    filas = []
    for p in partidos.itertuples():
        for team, opp in ((p.home_id, p.away_id), (p.away_id, p.home_id)):
            plantilla = plantilla_probable(con, team, p.start_utc)
            # Fichajes o jugadores que solo aparecen en el parte de lesiones del equipo.
            if not lesiones.empty:
                extra = lesiones[(lesiones["team_id"] == team) & ~lesiones["player_id"].isin(plantilla["player_id"])]
                plantilla = pd.concat([plantilla, extra[["player_id", "name"]].assign(team_id=team, position=None)])
            for j in plantilla.itertuples():
                pj = prob_juega(estado.get(j.player_id), tabla_estados)
                if pj <= 0:
                    continue
                filas.append({"game_id": p.game_id, "player_id": j.player_id, "team_id": team, "name": j.name,
                              "position": j.position, "starter": np.nan, "minutes": np.nan, "pf": np.nan,
                              "vestido": True, "start_utc": p.start_utc, "fecha": p.fecha, "season": p.season,
                              "season_type": p.season_type, "opp_id": opp, "prob_juega": pj,
                              "estado_lesion": estado.get(j.player_id)})
    out = pd.DataFrame(filas)
    if out.empty:
        return out
    cols = ["game_id", "team_id", "is_home", "b2b", "dias_descanso", "partidos_4d", "km_viaje", "spread_equipo", "total"]
    return out.merge(ctx[cols], on=["game_id", "team_id"], how="left")


def a_matriz(df: pd.DataFrame) -> pd.DataFrame:
    return df[FEATURES].astype(float).replace([np.inf, -np.inf], np.nan)
