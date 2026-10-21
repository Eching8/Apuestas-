"""Pipeline diario:
  1. Actualiza resultados y estadísticas de los días anteriores (córners, tarjetas, tiros, jugadores).
  2. Valida cada partido terminado contra ESPN.
  3. Liquida las predicciones pendientes (seguimiento de aciertos y ROI).
  4. Descarga los partidos del día, completa el historial de cada equipo y guarda sus ratings.
  5. Proyecta cada partido, compara con cuotas, elige mercados óptimos y arma combinadas.
"""
from __future__ import annotations

import json
import logging
from datetime import date, timedelta

from .combos import Combo, build_combos
from .config import LEAGUES, SETTINGS, START_DATE
from .db import Database, now_iso
from .markets import Pick, build_picks, select_value_picks
from .model import STATS, blend_with_market, league_baseline, project_match, team_rating
from .settle import performance, settle_pending
from .sources.api_football import FINISHED, ApiFootball
from .sources.http import BudgetExceeded
from .validation import Validator

log = logging.getLogger(__name__)


class DailyAnalyzer:
    def __init__(self, db: Database, api: ApiFootball | None = None, validator: Validator | None = None):
        self.db = db
        self.api = api or ApiFootball(db)
        self.validator = validator or Validator(db)

    # ------------------------------------------------------------ 1-3: resultados
    def update_results(self, day: str) -> int:
        stored = 0
        for fx in self.api.fixtures_by_date(day, ttl=600):
            if fx["league"]["id"] not in LEAGUES:
                continue
            if fx["fixture"]["status"]["short"] in FINISHED:
                if self.api.store_finished_match(fx):
                    stored += 1
                    self.validator.validate_fixture(fx["fixture"]["id"])
            else:
                self.api.store_fixture(fx)
        self.db.conn.commit()
        return stored

    # ------------------------------------------------------------ 4: historial
    def ensure_history(self, team_id: int, matches: int | None = None) -> None:
        if self.db.match_count(team_id) >= SETTINGS.min_history:
            return
        matches = matches or SETTINGS.history_window
        for i, fx in enumerate(self.api.team_last_fixtures(team_id, matches)):
            exists = self.db.q("SELECT 1 FROM team_match_stats WHERE fixture_id=? AND corners IS NOT NULL",
                               (fx["fixture"]["id"],))
            if not exists:
                # estadísticas de jugadores solo para los 6 más recientes (ahorra peticiones)
                self.api.store_finished_match(fx, with_players=i < 6)

    def snapshot_ratings(self, team_id: int, day: str, league_id: int) -> None:
        base = league_baseline(self.db, league_id, day)
        r = team_rating(self.db, team_id, day, base)
        hist = self.db.team_history(team_id, day, SETTINGS.history_window)
        for stat, (cf, ca) in STATS.items():
            def avg(col):
                vals = [(h["yellow"] or 0) + (h["red"] or 0) if col == "cards" else
                        (h["yellow_against"] or 0) + (h["red_against"] or 0) if col == "cards_against" else h[col]
                        for h in hist]
                vals = [v for v in vals if v is not None]
                return sum(vals) / len(vals) if vals else None
            self.db.upsert("team_ratings", {
                "date": day, "team_id": team_id, "stat": stat,
                "attack": r.attack[stat], "defense": r.defense[stat],
                "avg_for": avg(cf), "avg_against": avg(ca), "sample": r.sample, "form": r.form,
            })

    # ------------------------------------------------------------ 5: análisis
    def analyze_day(self, day: str) -> dict:
        fixtures = [fx for fx in self.api.fixtures_by_date(day)
                    if fx["league"]["id"] in LEAGUES and fx["fixture"]["status"]["short"] in ("NS", "TBD")]
        log.info("%d partidos por analizar el %s", len(fixtures), day)
        analyses, all_picks = [], []
        for fx in fixtures:
            match = self.api.store_fixture(fx)
            home, away = fx["teams"]["home"]["name"], fx["teams"]["away"]["name"]
            try:
                self.ensure_history(match["home_id"])
                self.ensure_history(match["away_id"])
            except Exception as exc:  # cuota agotada o fuente caída: se analiza con lo que haya
                log.warning("Historial incompleto para %s: %s", label_of(fx), exc)
            for t in (match["home_id"], match["away_id"]):
                self.snapshot_ratings(t, day, match["league_id"])
            self.db.conn.commit()

            proj = project_match(self.db, match)
            try:
                odds = self.api.parse_odds(self.api.odds(match["fixture_id"]))
            except BudgetExceeded:
                odds = {}
            label = f"{home} vs {away}"
            blend_with_market(proj, odds)
            picks = build_picks(proj, label, odds)
            best = select_value_picks(picks)
            all_picks += best
            analyses.append({
                "fixture_id": match["fixture_id"], "partido": label, "liga": fx["league"]["name"],
                "hora": fx["fixture"]["date"][11:16], "arbitro": match["referee"],
                "calidad_datos": round(proj.data_quality, 2),
                "forma": {"local": proj.home_rating.form, "visitante": proj.away_rating.form},
                "esperado": {s: {"local": round(proj.exp_home[s], 2), "visitante": round(proj.exp_away[s], 2)}
                             for s in STATS},
                "jugadores": [{"nombre": p["name"], "remates_esp": round(p["exp_shots"], 2),
                               "al_arco_esp": round(p["exp_shots_on"], 2), "p_titular": round(p["p_play"], 2)}
                              for p in proj.players],
                "cuotas_disponibles": bool(odds),
                "goles_mercado": [round(x, 2) for x in proj.market_goals] if proj.market_goals else None,
                "mercados_optimos": [p.to_dict() for p in best[:8]],
            })
            for p in best:
                self._save_pick(day, p)

        combos = build_combos(all_picks)
        for c in combos:
            self._save_combo(day, c)
        self.db.conn.commit()
        return {"fecha": day, "partidos": analyses, "combinadas": [_combo_dict(c) for c in combos]}

    def _save_pick(self, day: str, p: Pick) -> None:
        self.db.conn.execute(
            """INSERT INTO predictions (fixture_id, date, market, selection, prob, fair_odds, odds, ev, confidence, created_at)
               VALUES (?,?,?,?,?,?,?,?,?,?)
               ON CONFLICT(fixture_id, market, selection) DO UPDATE SET
                 prob=excluded.prob, fair_odds=excluded.fair_odds, odds=excluded.odds, ev=excluded.ev,
                 confidence=excluded.confidence, created_at=excluded.created_at""",
            (p.fixture_id, day, p.market, p.selection, p.prob, p.fair_odds, p.odds, p.ev, p.confidence, now_iso()))

    def _save_combo(self, day: str, c: Combo) -> None:
        legs = json.dumps([{"fixture_id": l.fixture_id, "match": l.match, "market": l.market,
                            "selection": l.selection, "prob": l.prob, "odds": l.odds} for l in c.legs],
                          ensure_ascii=False)
        self.db.conn.execute("DELETE FROM combos WHERE date=? AND kind=? AND legs=? AND result IS NULL",
                             (day, c.kind, legs))
        self.db.conn.execute("INSERT INTO combos (date, kind, legs, prob, odds, ev, created_at) VALUES (?,?,?,?,?,?,?)",
                             (day, c.kind, legs, c.prob, c.odds, c.ev, now_iso()))

    def validation_summary(self) -> dict:
        row = self.db.q("""SELECT SUM(validated=1) ok, SUM(validated=-1) bad, SUM(validated=0) pend
                           FROM matches WHERE status IN ('FT','AET','PEN')""")[0]
        stats = self.db.q("SELECT COUNT(*) n, SUM(ok) ok FROM validations")[0]
        return {"partidos_validados": row["ok"] or 0, "con_discrepancia": row["bad"] or 0,
                "sin_segunda_fuente": row["pend"] or 0,
                "estadisticas_comparadas": stats["n"], "estadisticas_coinciden": stats["ok"] or 0}

    # ------------------------------------------------------------ orquestación
    def run(self, day: date, catchup_days: int = 2) -> dict:
        if day < START_DATE:
            raise ValueError(f"El análisis comienza el {START_DATE.isoformat()}")
        for back in range(catchup_days, 0, -1):
            prev = day - timedelta(days=back)
            try:
                n = self.update_results(prev.isoformat())
                log.info("Resultados %s: %d partidos guardados", prev, n)
            except BudgetExceeded as exc:
                log.warning(str(exc))
        if hasattr(self.validator, "validate_pending"):
            log.info("Validación cruzada del historial: %s", self.validator.validate_pending())
        settle_pending(self.db)
        result = self.analyze_day(day.isoformat())
        result["validacion"] = self.validation_summary()
        result["rendimiento"] = performance(self.db)
        return result


def label_of(fx: dict) -> str:
    return f"{fx['teams']['home']['name']} vs {fx['teams']['away']['name']}"


def _combo_dict(c: Combo) -> dict:
    return {
        "tipo": c.kind,
        "probabilidad": round(c.prob, 4),
        "cuota": round(c.odds, 2),
        "cuota_real": c.has_real_odds,
        "ev": round(c.ev, 4) if c.ev is not None else None,
        "selecciones": [{"partido": l.match, "mercado": l.market, "seleccion": l.selection,
                         "prob": l.prob, "cuota": l.odds or l.min_odds or l.fair_odds,
                         "cuota_real": l.odds is not None} for l in c.legs],
    }
