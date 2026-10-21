"""Descarga datos de API-Football y los guarda en la base de datos.

Cada partido terminado se descarga una sola vez: lo que ya está en la base no se vuelve a pedir,
así el plan gratuito (100 peticiones/día) rinde más con cada día que pasa.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from .api_football import ApiError, ApiFootball, PresupuestoAgotado
from .config import Config, ligas_filtro, prioridad
from .db import Database

log = logging.getLogger(__name__)

TERMINADOS = {"FT", "AET", "PEN"}
POR_JUGAR = {"NS", "TBD"}
# Ya no se jugarán (o no cuentan): no se analizan.
ANULADOS = {"PST", "CANC", "ABD", "AWD", "WO", "SUSP"}

# Sin cobertura de estadísticas en la API: se marca para no volver a pedirlo.
SIN_COBERTURA = -1

_STAT_MAP = {
    "Corner Kicks": "corners",
    "Yellow Cards": "yellow",
    "Red Cards": "red",
    "Shots on Goal": "shots_on",
    "Total Shots": "shots_total",
    "Fouls": "fouls",
    "Goalkeeper Saves": "saves",
    "Ball Possession": "possession",
    "expected_goals": "xg",
}


# --- Parseo de respuestas -------------------------------------------------------------

def _to_utc(iso: str) -> datetime:
    dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def parse_fixture(item: dict, zona_horaria: str) -> dict:
    fx, league, teams, goals = item["fixture"], item["league"], item["teams"], item["goals"]
    dt_utc = _to_utc(fx["date"])
    return {
        "id": fx["id"],
        "date_utc": dt_utc.isoformat(timespec="seconds"),
        "fecha_local": dt_utc.astimezone(ZoneInfo(zona_horaria)).date().isoformat(),
        "league_id": league.get("id"),
        "season": league.get("season"),
        "league_name": league.get("name"),
        "league_country": league.get("country"),
        "home_id": teams["home"]["id"],
        "home_name": teams["home"]["name"],
        "away_id": teams["away"]["id"],
        "away_name": teams["away"]["name"],
        "status": fx["status"]["short"],
        "referee": fx.get("referee"),
        "home_goals": goals.get("home"),
        "away_goals": goals.get("away"),
    }


def _num(value) -> float | None:
    if value is None:
        return None
    if isinstance(value, str):
        value = value.strip().rstrip("%")
        if not value:
            return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def parse_statistics(fx: dict, response: list[dict]) -> list[dict]:
    """Convierte /fixtures/statistics en dos filas (local y visitante). Lista vacía si no hay cobertura."""
    by_team: dict[int, dict] = {}
    for entry in response:
        stats = {}
        for s in entry.get("statistics") or []:
            key = _STAT_MAP.get(s.get("type"))
            if key:
                stats[key] = _num(s.get("value"))
        by_team[entry["team"]["id"]] = stats

    home, away = by_team.get(fx["home_id"]), by_team.get(fx["away_id"])
    # Sin córners ni tiros en la respuesta, la cobertura del partido es parcial y no sirve.
    if home is None or away is None or not ({"corners", "shots_total"} & (home.keys() | away.keys())):
        return []

    rows = []
    for team_id, opp_id, is_home, stats, goals in (
        (fx["home_id"], fx["away_id"], 1, home, fx["home_goals"]),
        (fx["away_id"], fx["home_id"], 0, away, fx["away_goals"]),
    ):
        # La API devuelve null cuando el valor es 0 en conteos.
        count = {k: int(stats.get(k) or 0) for k in ("corners", "yellow", "red", "shots_on", "shots_total", "fouls")}
        rows.append({
            "fixture_id": fx["id"], "team_id": team_id, "opponent_id": opp_id, "is_home": is_home,
            "goals": goals, **count, "cards": count["yellow"] + count["red"],
            "possession": stats.get("possession"), "xg": stats.get("xg"),
            # Si la API no informa atajadas del partido, se deja vacío (no es lo mismo que 0).
            "saves": int(stats.get("saves") or 0) if "saves" in stats else None,
        })
    return rows


def parse_players(fixture_id: int, response: list[dict]) -> list[dict]:
    rows = []
    for entry in response:
        team_id = entry["team"]["id"]
        for p in entry.get("players") or []:
            st = (p.get("statistics") or [{}])[0]
            minutes = (st.get("games") or {}).get("minutes")
            if not minutes:
                continue
            shots, goals, cards = st.get("shots") or {}, st.get("goals") or {}, st.get("cards") or {}
            rows.append({
                "fixture_id": fixture_id, "player_id": p["player"]["id"], "team_id": team_id,
                "name": p["player"].get("name"), "position": (st.get("games") or {}).get("position"),
                "minutes": int(minutes), "goals": int(goals.get("total") or 0),
                "assists": int(goals.get("assists") or 0), "shots_on": int(shots.get("on") or 0),
                "shots_total": int(shots.get("total") or 0), "yellow": int(cards.get("yellow") or 0),
                "red": int(cards.get("red") or 0),
            })
    return rows


def parse_odds(response: list[dict]) -> list[tuple[str, str, str, float]]:
    rows = []
    for entry in response:
        for bm in entry.get("bookmakers") or []:
            for bet in bm.get("bets") or []:
                for v in bet.get("values") or []:
                    odd = _num(v.get("odd"))
                    if odd and odd > 1:
                        rows.append((bm.get("name", str(bm.get("id"))), bet.get("name", ""), str(v.get("value")), odd))
    return rows


# --- Recolección ----------------------------------------------------------------------

class Collector:
    def __init__(self, api: ApiFootball, db: Database, cfg: Config):
        self.api, self.db, self.cfg = api, db, cfg
        # El plan gratuito no permite pedir el historial de un equipo (parámetro "last" ni temporadas
        # recientes): en ese caso el historial se construye día a día con 'actualizar'.
        self.historial_disponible = True

    def _store_fixture(self, fx: dict) -> None:
        self.db.upsert_team(fx["home_id"], fx["home_name"])
        self.db.upsert_team(fx["away_id"], fx["away_name"])
        if fx["league_id"] is not None:
            self.db.upsert_league(fx["league_id"], fx["season"], fx["league_name"], fx["league_country"])
        self.db.upsert_fixture(fx)

    def _fetch_match_data(self, fx: dict, con_jugadores: bool = True) -> None:
        """Descarga estadísticas (y jugadores) de un partido terminado si aún no están guardadas."""
        stats_ok, players_ok = self.db.has_stats(fx["id"])
        if stats_ok == 0:
            rows = parse_statistics(fx, self.api.estadisticas_partido(fx["id"]))
            with self.db.tx():
                if rows:
                    self.db.save_team_stats(rows)
                stats_ok = 1 if rows else SIN_COBERTURA
                self.db.mark_fixture(fx["id"], stats_ok=stats_ok)
            if not rows:
                log.info("Sin estadísticas para el partido %s", fx["id"])
        if con_jugadores and players_ok == 0 and stats_ok == 1:
            rows = parse_players(fx["id"], self.api.jugadores_partido(fx["id"]))
            with self.db.tx():
                if rows:
                    self.db.save_player_stats(rows)
                self.db.mark_fixture(fx["id"], players_ok=1 if rows else SIN_COBERTURA)

    def team_history(self, team_id: int, con_jugadores: bool = True) -> int:
        """Asegura que el historial reciente del equipo está en la base. Devuelve partidos guardados."""
        if not self.historial_disponible:
            return 0
        try:
            items = self.api.ultimos_partidos(team_id, self.cfg.partidos_historial)
        except ApiError as e:
            if "plan" not in str(e).lower():
                raise
            self.historial_disponible = False
            log.warning("Tu plan de API-Football no permite descargar el historial de los equipos. "
                        "La base se llenará día a día con 'actualizar' (o con un plan de pago).")
            return 0
        fixtures = [parse_fixture(i, self.cfg.zona_horaria) for i in items]
        with self.db.tx():
            for fx in fixtures:
                self._store_fixture(fx)
        terminados = [fx for fx in fixtures if fx["status"] in TERMINADOS]
        for fx in terminados:
            self._fetch_match_data(fx, con_jugadores)
        return len(terminados)

    def collect_day(self, fecha: str, con_jugadores: bool = True, con_cuotas: bool = True) -> list[int]:
        """Guarda los partidos del día, el historial de sus equipos y las cuotas.

        Devuelve los ids de los partidos cuyos datos se completaron (dentro del presupuesto).
        """
        items = self.api.partidos_por_fecha(fecha, self.cfg.zona_horaria)
        fixtures = [parse_fixture(i, self.cfg.zona_horaria) for i in items]
        filtro = ligas_filtro(self.cfg)
        if filtro:
            fixtures = [f for f in fixtures if f["league_id"] in filtro]
        fixtures = [f for f in fixtures if f["fecha_local"] == fecha]
        with self.db.tx():
            for fx in fixtures:
                self._store_fixture(fx)

        # Primero las ligas prioritarias (con el límite de peticiones, las últimas pueden quedar fuera).
        pendientes = sorted((f for f in fixtures if f["status"] in POR_JUGAR),
                            key=lambda f: (prioridad(self.cfg, f["league_id"]), f["date_utc"]))
        pendientes = pendientes[: self.cfg.max_partidos]
        log.info("%d partidos el %s, se analizarán %d", len(fixtures), fecha, len(pendientes))
        listos: list[int] = []
        vistos: set[int] = set()
        try:
            for fx in pendientes:
                jugadores = con_jugadores and fx["league_id"] not in self.cfg.ligas_solo_tarjetas
                for team_id in (fx["home_id"], fx["away_id"]):
                    if team_id not in vistos:
                        self.team_history(team_id, jugadores)
                        vistos.add(team_id)
                if con_cuotas:
                    rows = parse_odds(self.api.cuotas(fx["id"]))
                    with self.db.tx():
                        self.db.save_odds(fx["id"], rows)
                listos.append(fx["id"])
        except PresupuestoAgotado as e:
            log.warning("%s. Partidos completos: %d de %d. Sube APUESTAS_PRESUPUESTO o el plan de la API.",
                        e, len(listos), len(pendientes))
        return listos

    def update_results(self, fecha: str, con_jugadores: bool = True) -> int:
        """Actualiza resultados y estadísticas de los partidos de un día ya jugado. Devuelve terminados."""
        items = self.api.partidos_por_fecha(fecha, self.cfg.zona_horaria)
        fixtures = [parse_fixture(i, self.cfg.zona_horaria) for i in items]
        conocidos = {r["id"] for r in self.db.fixtures_on(fecha)}
        filtro = ligas_filtro(self.cfg)
        fixtures = [f for f in fixtures if f["id"] in conocidos or (filtro and f["league_id"] in filtro)]
        with self.db.tx():
            for fx in fixtures:
                self._store_fixture(fx)
        # Primero los que ya estaban en la base (selecciones que liquidar), luego por prioridad de liga.
        fixtures.sort(key=lambda f: (f["id"] not in conocidos, prioridad(self.cfg, f["league_id"])))
        n = 0
        try:
            for fx in fixtures:
                if fx["status"] in TERMINADOS:
                    self._fetch_match_data(fx, con_jugadores and fx["league_id"] not in self.cfg.ligas_solo_tarjetas)
                    n += 1
        except PresupuestoAgotado as e:
            log.warning("%s. Ejecuta 'actualizar' de nuevo mañana para completar.", e)
        return n
