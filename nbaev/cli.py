"""Línea de comandos: python -m nbaev <grupo> <comando>."""
from __future__ import annotations

import argparse
import logging
import sys
from datetime import date

from . import config

log = logging.getLogger("nbaev")


def _con(cfg, solo_lectura: bool = False):
    from .data import db
    return db.conectar(config.ruta(cfg, "db"), solo_lectura=solo_lectura)


def _espn(cfg):
    from .data.espn import Espn
    return Espn(cfg, crudos=config.ruta(cfg, "crudos"))


def cmd_historial(cfg, args) -> None:
    """Calendario y partidos terminados desde la temporada configurada hasta ayer."""
    from .data import recolector
    con, cli = _con(cfg), _espn(cfg)
    hasta = date.fromisoformat(args.hasta) if args.hasta else recolector.ayer_et()
    desde = args.desde or cfg["temporadas"]["desde"]
    n = recolector.actualizar_calendario(con, cli, desde, hasta, tuple(cfg["temporadas"]["tipos"]))
    log.info("Partidos en calendario actualizados: %d", n)
    r = recolector.descargar_partidos(con, cli, limite=args.limite)
    log.info("Partidos descargados: %s", r)
    log.info("Líneas rellenadas: %s", recolector.rellenar_lineas(con, cli))
    _contexto(con)


def _contexto(con) -> None:
    from .data import contexto
    log.info("Contexto de partidos (descanso, viajes, total implícito): %d filas", contexto.guardar(con))


def cmd_reprocesar(cfg, args) -> None:
    """Vuelve a procesar los partidos desde crudos/ (tras cambiar un parser), sin descargar."""
    from .data import recolector
    con, cli = _con(cfg), _espn(cfg)
    log.info("Reprocesados: %s", recolector.descargar_partidos(con, cli, reprocesar=True))
    _contexto(con)


def cmd_lesiones(cfg, args) -> None:
    from .data import recolector
    con, cli = _con(cfg), _espn(cfg)
    log.info("Lesiones guardadas: %d", recolector.guardar_lesiones(con, cli))


def cmd_cuotas(cfg, args) -> None:
    """Captura las cuotas de props de hoy (SportsGameOdds) con hora de captura."""
    from .data import cuotas_sgo, recolector
    con = _con(cfg)
    fecha = date.fromisoformat(args.fecha) if args.fecha else recolector.hoy_et()
    log.info("Cuotas: %s", cuotas_sgo.capturar_dia(con, cfg, fecha))


def cmd_cuotas_historicas(cfg, args) -> None:
    """Aperturas y cierres de props de partidos pasados (gasta entidades del plan de SportsGameOdds)."""
    from .data import cuotas_sgo
    con = _con(cfg)
    r = cuotas_sgo.descargar_historico(con, cfg, date.fromisoformat(args.desde), date.fromisoformat(args.hasta),
                                       max_partidos=args.max_partidos)
    log.info("Cuotas históricas: %s", r)


def cmd_importar_csv(cfg, args) -> None:
    from .data import cuotas_csv
    con = _con(cfg)
    log.info("Filas importadas: %s", cuotas_csv.importar(con, args.archivo, kind=args.tipo))


def cmd_nba_api(cfg, args) -> None:
    """Métricas avanzadas y tracking de stats.nba.com (solo desde redes no bloqueadas)."""
    from .data import nba_stats
    con = _con(cfg)
    log.info("stats.nba.com: %s", nba_stats.descargar(con, cfg, args.temporada, args.hasta))


def cmd_diario(cfg, args) -> None:
    """Actualización diaria: partidos de ayer, lesiones, cuotas de hoy y emparejamiento de ids."""
    from .data import cuotas_sgo, recolector
    con, cli = _con(cfg), _espn(cfg)
    hoy = recolector.hoy_et()
    recolector.actualizar_calendario(con, cli, recolector.temporada_de(hoy), hoy, tuple(cfg["temporadas"]["tipos"]))
    log.info("Partidos: %s", recolector.descargar_partidos(con, cli))
    log.info("Líneas rellenadas: %s", recolector.rellenar_lineas(con, cli))
    log.info("Lesiones: %d", recolector.guardar_lesiones(con, cli))
    if not args.sin_cuotas:
        try:
            # Cierre y resultado de las props de ayer (para CLV y liquidación) y captura de las de hoy.
            ayer = recolector.ayer_et()
            log.info("Cierres de ayer: %s", cuotas_sgo.descargar_historico(con, cfg, ayer, ayer, respetar_reserva=False))
            log.info("Cuotas de hoy: %s", cuotas_sgo.capturar_dia(con, cfg, hoy))
        except Exception as e:
            log.error("No se pudieron descargar las cuotas: %s", e)
    _contexto(con)
    if cfg["fuentes"]["nba_api"]["modo"] != "no":
        from .data import nba_stats
        log.info("stats.nba.com: %s", nba_stats.descargar(con, cfg, recolector.temporada_de(hoy), None))


def cmd_estado(cfg, args) -> None:
    from .data import calidad
    con = _con(cfg, solo_lectura=True)
    print(calidad.informe(con))


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="nbaev", description="Props NBA con valor esperado")
    ap.add_argument("--config", help="ruta a un YAML de configuración")
    grupos = ap.add_subparsers(dest="grupo", required=True)

    d = grupos.add_parser("datos", help="descarga y mantenimiento de la base").add_subparsers(dest="cmd", required=True)
    p = d.add_parser("historial", help="calendario y box scores/jugada a jugada hasta ayer")
    p.add_argument("--desde", type=int, help="año de inicio de la primera temporada (2021 = 2021-22)")
    p.add_argument("--hasta", help="AAAA-MM-DD (por defecto ayer)")
    p.add_argument("--limite", type=int, help="máximo de partidos a descargar en esta ejecución")
    p.set_defaults(f=cmd_historial)
    d.add_parser("reprocesar", help="rehace las tablas desde crudos/ sin descargar").set_defaults(f=cmd_reprocesar)
    d.add_parser("lesiones", help="captura el parte de lesiones actual").set_defaults(f=cmd_lesiones)
    p = d.add_parser("cuotas", help="captura las cuotas de props del día")
    p.add_argument("--fecha")
    p.set_defaults(f=cmd_cuotas)
    p = d.add_parser("cuotas-historicas", help="aperturas y cierres de partidos pasados (SportsGameOdds)")
    p.add_argument("--desde", required=True)
    p.add_argument("--hasta", required=True)
    p.add_argument("--max-partidos", type=int, help="tope de partidos (entidades) a gastar")
    p.set_defaults(f=cmd_cuotas_historicas)
    p = d.add_parser("importar-csv", help="importa cuotas cargadas a mano (p. ej. bet365)")
    p.add_argument("archivo")
    p.add_argument("--tipo", default="captura", choices=["captura", "apertura", "cierre"])
    p.set_defaults(f=cmd_importar_csv)
    p = d.add_parser("nba-api", help="métricas avanzadas y tracking de stats.nba.com")
    p.add_argument("--temporada", type=int, required=True)
    p.add_argument("--hasta", help="AAAA-MM-DD: datos acumulados hasta esa fecha (sin fuga)")
    p.set_defaults(f=cmd_nba_api)
    p = d.add_parser("diario", help="actualización diaria completa")
    p.add_argument("--sin-cuotas", action="store_true")
    p.set_defaults(f=cmd_diario)
    d.add_parser("estado", help="cobertura y calidad de los datos").set_defaults(f=cmd_estado)

    args = ap.parse_args(argv)
    cfg = config.cargar(args.config)
    config.configurar_logs(cfg)
    args.f(cfg, args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
