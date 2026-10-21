"""API-Football simulada para las pruebas. Datos sintéticos: solo sirven para probar el código."""
from __future__ import annotations

import random
from datetime import datetime, timedelta, timezone

from apuestas.api_football import ApiFootball, PresupuestoAgotado

TEAMS = {i: f"Equipo {i}" for i in range(1, 9)}


class FakeApi(ApiFootball):
    def __init__(self, fecha: str, presupuesto: int = 10_000, seed: int = 7):
        self.presupuesto, self.peticiones, self.restantes_hoy = presupuesto, 0, None
        self.rng = random.Random(seed)
        self.fecha = fecha
        self.history: dict[int, dict] = {}
        self.today: list[dict] = []
        self.calls: list[str] = []
        self.alineaciones_publicadas = True
        self.ausentes: set[int] = set()
        base = datetime.fromisoformat(fecha).replace(hour=20, tzinfo=timezone.utc)
        fid = 1000
        # 10 jornadas previas: todos contra todos de forma rotativa.
        ids = list(TEAMS)
        for jornada in range(10, 0, -1):
            self.rng.shuffle(ids)
            for h, a in zip(ids[::2], ids[1::2]):
                fid += 1
                self.history[fid] = self._fixture(fid, base - timedelta(days=7 * jornada), h, a, "FT")
        for n, (h, a) in enumerate(((1, 2), (3, 4), (5, 6), (7, 8))):
            fid += 1
            fx = self._fixture(fid, base + timedelta(hours=n), h, a, "NS")
            self.today.append(fx)

    def _fixture(self, fid, dt, h, a, status):
        g = (self.rng.choice([0, 1, 1, 2, 2, 3]), self.rng.choice([0, 0, 1, 1, 2])) if status == "FT" else (None, None)
        return {
            "fixture": {"id": fid, "date": dt.isoformat(), "status": {"short": status}},
            "league": {"id": 39, "season": 2026, "name": "Liga Test", "country": "Testland"},
            "teams": {"home": {"id": h, "name": TEAMS[h]}, "away": {"id": a, "name": TEAMS[a]}},
            "goals": {"home": g[0], "away": g[1]},
        }

    def finish_today(self):
        for fx in self.today:
            fx["fixture"]["status"]["short"] = "FT"
            fx["goals"] = {"home": self.rng.choice([0, 1, 2, 3]), "away": self.rng.choice([0, 1, 2])}
            self.history[fx["fixture"]["id"]] = fx

    def _get(self, path, **params):
        if self.peticiones >= self.presupuesto:
            raise PresupuestoAgotado("fake")
        self.peticiones += 1
        self.calls.append(path)
        if path == "/fixtures" and "date" in params:
            return [fx for fx in self.today if fx["fixture"]["date"][:10] == params["date"]]
        if path == "/fixtures" and "team" in params:
            t = params["team"]
            own = [fx for fx in self.history.values() if t in (fx["teams"]["home"]["id"], fx["teams"]["away"]["id"])]
            return sorted(own, key=lambda f: f["fixture"]["date"], reverse=True)[: params["last"]]
        if path == "/fixtures/statistics":
            fx = self.history[params["fixture"]]
            r = random.Random(params["fixture"])
            out = []
            for side in ("home", "away"):
                out.append({"team": fx["teams"][side], "statistics": [
                    {"type": "Shots on Goal", "value": r.randint(1, 8)},
                    {"type": "Total Shots", "value": r.randint(6, 20)},
                    {"type": "Corner Kicks", "value": r.randint(1, 10)},
                    {"type": "Yellow Cards", "value": r.choice([None, 1, 2, 3])},
                    {"type": "Red Cards", "value": r.choice([None, None, None, 1])},
                    {"type": "Ball Possession", "value": "50%"},
                ]})
            return out
        if path == "/fixtures/players":
            fx = self.history[params["fixture"]]
            r = random.Random(params["fixture"] * 3)
            out = []
            for side in ("home", "away"):
                tid = fx["teams"][side]["id"]
                out.append({"team": fx["teams"][side], "players": [{
                    "player": {"id": tid * 100 + k, "name": f"Jugador {tid}-{k}"},
                    "statistics": [{"games": {"minutes": 90 if k < 11 else None, "position": "F"},
                                    "shots": {"total": r.randint(0, 5) if k < 3 else r.randint(0, 1),
                                              "on": r.randint(0, 2) if k < 3 else 0},
                                    "goals": {"total": r.choice([0, 0, 0, 1]), "assists": None},
                                    "cards": {"yellow": 0, "red": 0}}],
                } for k in range(14)]})
            return out
        if path == "/fixtures/lineups":
            fx = next((f for f in self.today if f["fixture"]["id"] == params["fixture"]), None)
            if fx is None or not self.alineaciones_publicadas:
                return []
            return [{"team": fx["teams"][side], "formation": "4-3-3", "startXI": [
                {"player": {"id": fx["teams"][side]["id"] * 100 + k, "name": f"Jugador {fx['teams'][side]['id']}-{k}",
                            "pos": "F"}}
                for k in range(14) if k < 11 and fx["teams"][side]["id"] * 100 + k not in self.ausentes
            ] + ([{"player": {"id": fx["teams"][side]["id"] * 100 + 11, "name": "Suplente", "pos": "F"}}]
                 if fx["teams"][side]["id"] * 100 in self.ausentes else [])} for side in ("home", "away")]
        if path == "/odds":
            return [{"bookmakers": [
                {"id": b, "name": f"Casa {b}", "bets": [
                    {"name": "Match Winner", "values": [{"value": "Home", "odd": "2.10"}, {"value": "Draw", "odd": "3.30"},
                                                         {"value": "Away", "odd": "3.60"}]},
                    {"name": "Goals Over/Under", "values": [{"value": "Over 1.5", "odd": "1.30"},
                                                             {"value": "Under 1.5", "odd": "3.40"},
                                                             {"value": "Over 2.5", "odd": "1.95"},
                                                             {"value": "Under 2.5", "odd": "1.85"}]},
                    {"name": "Corners Over Under", "values": [{"value": "Over 8.5", "odd": "1.55"},
                                                               {"value": "Under 8.5", "odd": "2.35"}]},
                    {"name": "Double Chance", "values": [{"value": "Home/Draw", "odd": "1.35"}]},
                ]} for b in (1, 2, 3)]}]
        raise AssertionError(f"ruta no simulada {path}")
