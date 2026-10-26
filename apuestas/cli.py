"""Línea de comandos.

    python -m apuestas analizar              # partidos de hoy: descarga, analiza, combinadas, informe
    python -m apuestas actualizar            # resultados de ayer + liquidación de selecciones
    python -m apuestas diario                # actualizar (ayer) + analizar (hoy), para programarlo
    python -m apuestas validar --fecha 2026-10-21
    python -m apuestas rendimiento
    python -m apuestas nba analizar          # props de la NBA (ver apuestas/nba/cli.py)
"""
from __future__ import annotations

import argparse
import logging
import sys
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from .analyzer import analyze_fixture, candidates
from .api_football import ApiError, ApiFootball
from .collector import ANULADOS, Collector
from .combinadas import Leg, build_combos
from .config import FECHA_INICIO, Config, load_config
from .db import Database
from .football_data import FootballData, validate_day
from .nba.cli import registrar as registrar_nba
from .report import AVISO, save_picks, write_reports
from .settle import settle_pending, summary

log = logging.getLogger("apuestas")
SELECCIONES_POR_PARTIDO = 8


def _hoy(cfg: Config) -> date:
    return datetime.now(ZoneInfo(cfg.zona_horaria)).date()


def _fecha(value: str | None, cfg: Config, offset: int = 0) -> str:
    if value:
        return date.fromisoformat(value).isoformat()
    return (_hoy(cfg) + timedelta(days=offset)).isoformat()


def cmd_analizar(args, cfg: Config, db: Database) -> int:
    fecha = _fecha(args.fecha, cfg)
    if date.fromisoformat(fecha) < FECHA_INICIO:
        log.error("El seguimiento empieza el %s; usa una fecha igual o posterior.", FECHA_INICIO)
        return 2
    if not args.sin_descarga:
        api = ApiFootball(cfg.api_football_key, cfg.presupuesto_peticiones)
        Collector(api, db, cfg).collect_day(fecha, con_jugadores=not args.sin_jugadores,
                                            con_cuotas=not args.sin_cuotas_api)
        log.info("Peticiones usadas: %d (quedan hoy según la API: %s)", api.peticiones, api.restantes_hoy)

    fixtures = [dict(r) for r in db.fixtures_on(fecha) if r["status"] not in ANULADOS]
    if cfg.ligas:
        fixtures = [f for f in fixtures if f["league_id"] in cfg.ligas]
    analyses = [analyze_fixture(db, fx, cfg, con_jugadores=not args.sin_jugadores) for fx in fixtures]
    analyses = [a for a in analyses if a.ok] + [a for a in analyses if not a.ok]

    picks, legs = {}, []
    for a in analyses:
        if not a.ok:
            continue
        sel = candidates(a, cfg, sin_cuotas=args.incluir_sin_cuota)
        sel.sort(key=lambda m: ((m.edge or 0), m.final_prob or m.prob), reverse=True)
        picks[a.fixture["id"]] = sel[:SELECCIONES_POR_PARTIDO]
        partido = f"{a.fixture['home_name']} vs {a.fixture['away_name']}"
        legs += [Leg(a.fixture["id"], partido, m) for m in sel]

    combos = build_combos(legs, cfg.prob_min_combinada, cfg.max_selecciones_combinada)
    md, js = write_reports(cfg.reportes_dir, fecha, analyses, picks, combos)
    save_picks(db, fecha, picks, combos)

    analizados = sum(a.ok for a in analyses)
    print(f"{analizados} de {len(analyses)} partidos analizados el {fecha}.")
    for perfil, lista in combos.items():
        for c in lista[:1]:
            legs_txt = " + ".join(f"{l.market.label}" for l in c.legs)
            print(f"  [{perfil}] prob {c.prob * 100:.0f}% cuota {c.odd:.2f}: {legs_txt}")
    print(f"Informe: {md}\nDatos: {js}\n")
    print(AVISO.replace("> ", "").replace("**", ""))
    return 0


def cmd_actualizar(args, cfg: Config, db: Database) -> int:
    fecha = _fecha(args.fecha, cfg, offset=-1)
    api = ApiFootball(cfg.api_football_key, cfg.presupuesto_peticiones)
    n = Collector(api, db, cfg).update_results(fecha, con_jugadores=not args.sin_jugadores)
    liquidadas = settle_pending(db)
    print(f"{n} partidos terminados guardados del {fecha}; {liquidadas} selecciones liquidadas. "
          f"Peticiones usadas: {api.peticiones}.")
    return 0


def cmd_diario(args, cfg: Config, db: Database) -> int:
    args.fecha = None
    if _hoy(cfg) - timedelta(days=1) >= FECHA_INICIO:
        cmd_actualizar(args, cfg, db)
    args.sin_descarga = False
    return cmd_analizar(args, cfg, db)


def cmd_validar(args, cfg: Config, db: Database) -> int:
    if not cfg.football_data_key:
        log.error("Falta FOOTBALL_DATA_KEY (gratis en https://www.football-data.org/client/register).")
        return 2
    fecha = _fecha(args.fecha, cfg)
    res = validate_day(db, FootballData(cfg.football_data_key), fecha)
    print(f"Validación {fecha} con football-data.org: {res}")
    for r in db.conn.execute(
        """SELECT v.detail, h.name AS home, a.name AS away FROM validations v JOIN fixtures f ON f.id = v.fixture_id
           JOIN teams h ON h.id = f.home_id JOIN teams a ON a.id = f.away_id WHERE f.fecha_local = ? AND v.ok = 0""",
        (fecha,),
    ):
        print(f"  Discrepancia {r['home']} vs {r['away']}: {r['detail']}")
    return 0


def cmd_rendimiento(args, cfg: Config, db: Database) -> int:
    s = summary(db)
    if not s["selecciones"] and not s["combinadas"]:
        print("Aún no hay selecciones liquidadas. Ejecuta 'actualizar' después de los partidos.")
        return 0
    print("Selecciones sueltas por mercado (beneficio apostando 1 unidad a la cuota mediana):")
    for r in s["selecciones"]:
        ben = "-" if r["beneficio"] is None else f"{r['beneficio']:+.2f} u en {r['con_cuota']} con cuota"
        print(f"  {r['tipo']:<12} n={r['n']:<4} acierto {r['acierto'] * 100:5.1f}%  "
              f"prob. media {r['prob_media'] * 100:5.1f}%  {ben}")
    print("Combinadas:")
    for r in s["combinadas"]:
        ben = "-" if r["beneficio"] is None else f"{r['beneficio']:+.2f} u"
        print(f"  {r['perfil']:<18} n={r['n']:<4} acierto {r['acierto'] * 100:5.1f}%  "
              f"prob. media {r['prob_media'] * 100:5.1f}%  {ben}")
    print("\nSi el acierto real queda por debajo de la probabilidad media, el modelo es optimista: "
          "sube APUESTAS_PROB_MIN o baja APUESTAS_PESO_MODELO.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="apuestas", description="Analizador diario de partidos y combinadas")
    p.add_argument("-v", "--verbose", action="store_true")
    sub = p.add_subparsers(dest="cmd", required=True)

    def comunes(sp, fecha_help):
        sp.add_argument("--fecha", help=fecha_help)
        sp.add_argument("--sin-jugadores", action="store_true", help="no descargar ni analizar jugadores (ahorra peticiones)")

    a = sub.add_parser("analizar", help="analiza los partidos de un día y genera combinadas")
    comunes(a, "AAAA-MM-DD (por defecto, hoy)")
    a.add_argument("--sin-descarga", action="store_true", help="usar solo lo que ya está en la base")
    a.add_argument("--sin-cuotas-api", action="store_true", help="no descargar cuotas")
    a.add_argument("--incluir-sin-cuota", action="store_true",
                   help="incluir selecciones sin cuota disponible (se usa la cuota justa del modelo)")
    a.set_defaults(func=cmd_analizar)

    u = sub.add_parser("actualizar", help="guarda resultados y estadísticas de un día jugado y liquida")
    comunes(u, "AAAA-MM-DD (por defecto, ayer)")
    u.set_defaults(func=cmd_actualizar)

    d = sub.add_parser("diario", help="actualizar ayer + analizar hoy")
    comunes(d, argparse.SUPPRESS)
    d.add_argument("--sin-cuotas-api", action="store_true")
    d.add_argument("--incluir-sin-cuota", action="store_true")
    d.set_defaults(func=cmd_diario)

    v = sub.add_parser("validar", help="contrasta horarios y marcadores con football-data.org")
    v.add_argument("--fecha")
    v.set_defaults(func=cmd_validar)

    r = sub.add_parser("rendimiento", help="acierto real del modelo con las selecciones liquidadas")
    r.set_defaults(func=cmd_rendimiento)

    registrar_nba(sub)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO, format="%(levelname)s %(message)s")
    cfg = load_config()
    db = Database(cfg.db_path)
    try:
        return args.func(args, cfg, db)
    except ApiError as e:
        log.error("%s", e)
        return 1
    finally:
        db.close()


if __name__ == "__main__":
    sys.exit(main())
