"""CLI.

  python -m futbol_analyzer run                   # analiza hoy (desde el 21-10-2026 en adelante)
  python -m futbol_analyzer run --date 2026-10-22
  python -m futbol_analyzer results --date 2026-10-21   # solo actualizar resultados/estadísticas y validar
  python -m futbol_analyzer team 541              # ratings guardados de un equipo
  python -m futbol_analyzer performance           # aciertos y ROI históricos
"""
from __future__ import annotations

import argparse
import json
import logging
from datetime import date, datetime
from zoneinfo import ZoneInfo

import requests

from .config import SETTINGS, START_DATE
from .db import Database
from .pipeline import DailyAnalyzer
from .sources.football_data import ChainValidator, EspnPlusProvider, FootballDataValidator
from .sources.hybrid import ApiFootballValidator, HybridProvider
from .report import save, to_markdown
from .settle import performance, settle_pending


def _today() -> date:
    return datetime.now(ZoneInfo(SETTINGS.timezone)).date()


def _pick_source(choice: str) -> str:
    if choice != "auto":
        return choice
    if not SETTINGS.api_football_key:
        return "espn"
    try:
        r = requests.get("https://v3.football.api-sports.io/status", timeout=15,
                         headers={"x-apisports-key": SETTINGS.api_football_key})
        if r.ok and not r.json().get("errors"):
            return "hybrid"
        logging.warning("API-Football no disponible (%s); se usa ESPN", r.json().get("errors"))
    except Exception as exc:
        logging.warning("API-Football no disponible (%s); se usa ESPN", exc)
    return "espn"


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(prog="futbol_analyzer", description="Análisis diario de partidos y combinadas")
    ap.add_argument("-v", "--verbose", action="store_true")
    ap.add_argument("--source", choices=("auto", "hybrid", "api-football", "espn"), default="auto",
                    help="auto = híbrido (ESPN + API-Football) si la clave es válida, si no solo ESPN")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run", help="análisis completo del día")
    r.add_argument("--date", type=date.fromisoformat, default=None)
    r.add_argument("--out", default="reports")
    res = sub.add_parser("results", help="actualizar resultados y validar")
    res.add_argument("--date", type=date.fromisoformat, required=True)
    t = sub.add_parser("team", help="ver ratings de un equipo")
    t.add_argument("team_id", type=int)
    sub.add_parser("performance", help="rendimiento histórico")
    args = ap.parse_args(argv)

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO,
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    source = _pick_source(args.source)
    db = Database(SETTINGS.db_path if source == "api-football" else SETTINGS.db_path.replace(".db", "_espn.db"))
    logging.info("Fuente de datos: %s", source)

    def analyzer() -> DailyAnalyzer:
        if source == "espn":
            provider = EspnPlusProvider(db)
            return DailyAnalyzer(db, api=provider, validator=FootballDataValidator(db, provider.fd))
        if source == "hybrid":
            provider = HybridProvider(db)
            return DailyAnalyzer(db, api=provider, validator=ChainValidator(
                FootballDataValidator(db, provider.fd), ApiFootballValidator(db, provider)))
        return DailyAnalyzer(db)

    if args.cmd == "run":
        day = args.date or _today()
        if day < START_DATE:
            ap.error(f"La fecha debe ser igual o posterior a {START_DATE}")
        result = analyzer().run(day)
        md, js = save(result, args.out)
        print(to_markdown(result))
        print(f"\nReporte guardado en {md} y {js}")
    elif args.cmd == "results":
        n = analyzer().update_results(args.date.isoformat())
        settle_pending(db)
        print(f"{n} partidos terminados guardados y validados")
    elif args.cmd == "team":
        rows = db.q("SELECT * FROM team_ratings WHERE team_id=? ORDER BY date DESC, stat LIMIT 5", (args.team_id,))
        name = db.q("SELECT name FROM teams WHERE id=?", (args.team_id,))
        print(name[0]["name"] if name else args.team_id)
        for r in rows:
            print(f"{r['date']} {r['stat']:9} ataque {r['attack']:.2f} defensa {r['defense']:.2f} "
                  f"a favor {r['avg_for'] or 0:.2f} en contra {r['avg_against'] or 0:.2f} (n={r['sample']}, forma {r['form']})")
    elif args.cmd == "performance":
        print(json.dumps(performance(db), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
