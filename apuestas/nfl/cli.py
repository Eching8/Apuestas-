"""Subcomandos de la NFL.

    python -m apuestas nfl actualizar                     # nflverse + ESPN: partidos, stats, lesiones, traspasos
    python -m apuestas nfl analizar                       # los próximos 7 días: props, TD, valor -> informe
    python -m apuestas nfl td                             # quién tiene más probabilidad de anotar (1+ y 2+)
    python -m apuestas nfl matchup BUF LAC                # el enfrentamiento: ataque contra defensa, métrica a métrica
    python -m apuestas nfl validar "Derrick Henry +2 TD"  # ¿es buena esta apuesta? ¿por qué la juega la gente?
    python -m apuestas nfl jugador "Josh Allen"           # ficha: rol, tendencias, rivales, próxima proyección
    python -m apuestas nfl rendimiento                    # acierto real de lo recomendado
    python -m apuestas nfl backtest --desde 2025-10-01 --hasta 2026-01-05
"""
from __future__ import annotations

import logging
from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from ..config import Config
from ..db import Database, now_iso
from ..report import AVISO
from . import equipos
from .analizador import (AnalisisPartido, analizar_partido, con_valor, guardar_picks, liquidar, mas_probables,
                         rendimiento)
from .backtest import backtest, resumen
from .db import NflDB
from .fuentes import EspnNfl, Nflverse
from .informe import escribir
from .mercado import Mercado, SportsGameOddsNfl, emparejar, filas_lineas, parse_evento
from .modelo import NOMBRES, Contexto, americana, construir_contexto, cuota_justa, rango, texto_rango, valor
from .razones import tendencias
from .recolector import actualizar
from .validar import buscar_jugador, interpretar, texto_veredicto, validar

log = logging.getLogger("apuestas")


def _hoy(cfg: Config) -> date:
    return datetime.now(ZoneInfo(cfg.zona_horaria)).date()


def temporadas_por_defecto(hoy: date) -> list[int]:
    actual = hoy.year if hoy.month >= 3 else hoy.year - 1
    return [actual - 2, actual - 1, actual]


def cmd_actualizar(args, cfg: Config, db: Database) -> int:
    nfl = NflDB(db.conn)
    temporadas = args.temporadas or temporadas_por_defecto(_hoy(cfg))
    nv = Nflverse()
    r = actualizar(nfl, nv, temporadas, None if args.sin_espn else EspnNfl(), forzar=args.forzar)
    liquidadas = liquidar(nfl)
    print(f"nflverse: {nv.descargas} archivos nuevos o cambiados (temporadas {', '.join(map(str, temporadas))}).")
    if r["partidos"]:
        print(f"  Calendario: {r['partidos']} partidos.")
    for season, n in r["jugadores"].items():
        print(f"  {season}: {n} filas de jugador por partido.")
    if r["pbp"]:
        print(f"  Jugada a jugada procesado: {', '.join(map(str, r['pbp']))}.")
    if r.get("traspasos"):
        print(f"  {len(r['traspasos'])} cambios de equipo esta temporada según las plantillas semanales.")
    print(f"  Lesiones: {r['lesiones']} en el parte oficial, {r.get('lesiones_espn', 0)} en ESPN; "
          f"{r.get('transacciones', 0)} movimientos de plantilla nuevos.")
    for t in r.get("traspasos_espn", []):
        print(f"  Traspaso (ESPN): {t['name']} {t['from_team']} → {t['to_team']} ({t['fecha']})")
    print(f"{liquidadas} selecciones liquidadas.")
    return 0


def _mercados(cfg: Config, nfl: NflDB, desde: str, dias: int, juegos: list[dict]) -> dict[str, Mercado]:
    """Líneas de SportsGameOdds para los partidos de la ventana, emparejadas con nflverse y guardadas."""
    sgo = SportsGameOddsNfl(cfg.sgo_key)
    ini = datetime.now(timezone.utc) - timedelta(hours=4)
    fin = datetime.fromisoformat(desde).replace(tzinfo=timezone.utc) + timedelta(days=dias + 1)
    eventos = sgo.eventos(max(ini, datetime.fromisoformat(desde).replace(tzinfo=timezone.utc) - timedelta(hours=12)), fin)
    roster = [dict(r) for r in nfl.conn.execute("SELECT player_id, name, team FROM nfl_rosters")]
    out, capturado = {}, now_iso()
    for ev in eventos:
        m = parse_evento(ev)
        juego = next((g for g in juegos if g["home_team"] == m.home and g["away_team"] == m.away), None)
        if juego is None:
            continue
        emparejar(m, roster)
        out[juego["game_id"]] = m
        nfl.guardar_lineas(filas_lineas(m, juego["game_id"], capturado))
    nfl.commit()
    log.info("SportsGameOdds: %d partidos con líneas (%d consultas).", len(out), sgo.peticiones)
    return out


def _ventana(args, cfg: Config) -> tuple[str, str, int]:
    desde = args.desde or _hoy(cfg).isoformat()
    dias = args.dias if args.dias is not None else cfg.nfl_dias
    return desde, (date.fromisoformat(desde) + timedelta(days=dias)).isoformat(), dias


def _analizar(args, cfg: Config, nfl: NflDB) -> tuple[Contexto, list[AnalisisPartido], str, str]:
    desde, hasta, dias = _ventana(args, cfg)
    juegos = [dict(g) for g in nfl.proximos_partidos(desde, hasta)]
    if getattr(args, "equipo", None):
        team = equipos.por_texto(args.equipo)
        juegos = [g for g in juegos if team in (g["home_team"], g["away_team"])]
    ctx = construir_contexto(nfl.conn, desde)
    mercados = {}
    if juegos and not getattr(args, "sin_lineas", False):
        try:
            mercados = _mercados(cfg, nfl, desde, dias, juegos)
        except Exception as e:  # sin líneas el análisis sigue (con cuotas justas)
            log.warning("No se pudieron descargar las líneas: %s", e)
    partidos = [analizar_partido(ctx, g, mercados.get(g["game_id"]), cfg.nfl_peso_mercado) for g in juegos
                if g["home_team"] in ctx.perfiles and g["away_team"] in ctx.perfiles]
    return ctx, partidos, desde, hasta


def _novedades(ctx: Contexto, nfl: NflDB, partidos: list[AnalisisPartido]) -> dict:
    ultima = nfl.conn.execute("SELECT MAX(week) FROM nfl_player_games WHERE season = ?", (ctx.temporada,)).fetchone()[0]
    traspasos = []
    for r in nfl.conn.execute(
            "SELECT m.*, r.name, r.position FROM nfl_movimientos m JOIN nfl_rosters r USING(player_id) "
            "WHERE m.season = ? AND m.week >= ? ORDER BY m.week DESC", (ctx.temporada, (ultima or 0) - 2)):
        partidos_j = ctx.jugadores.get(r["player_id"], [])
        if r["position"] in ("QB", "RB", "WR", "TE") and any(
                (p.get("targets") or 0) + (p.get("carries") or 0) + (p.get("attempts") or 0) >= 3
                for p in partidos_j[:8]):
            traspasos.append(f"{r['name']} ({r['position']}): {r['from_team']} → {r['to_team']} "
                             f"(semana {r['week']}, {r['fuente']})")
    equipos_jornada = {t for a in partidos for t in a.entornos}
    bajas = []
    for team in sorted(equipos_jornada):
        for b in ctx.bajas.get(team, []):
            if b["pos"] == "QB":
                rol = "QB titular" if b["titular_qb"] else f"QB, lanzó el {b['pases'] * 100:.0f}% de los pases cuando jugó"
            else:
                rol = (f"{b['acarreos'] * 100:.0f}% de los acarreos" if b["acarreos"] >= b["envios"]
                       else f"{b['envios'] * 100:.0f}% de los envíos")
            detalle = f" ({b['detalle']})" if b["detalle"] else ""
            bajas.append(f"{team}: {b['nombre']} ({rol if b['pos'] == 'QB' else b['pos'] + ', ' + rol}) — "
                         f"{b['estado']}{detalle}")
    les = nfl.conn.execute("SELECT MAX(updated_at) FROM nfl_injuries WHERE fuente = 'espn'").fetchone()[0]
    return {"temporada": ctx.temporada, "ultima_semana": ultima, "lesiones_al": (les or "-")[:16],
            "traspasos": list(dict.fromkeys(traspasos)), "bajas": bajas}


def cmd_analizar(args, cfg: Config, db: Database) -> int:
    nfl = NflDB(db.conn)
    if not args.sin_descarga:
        actualizar(nfl, Nflverse(), temporadas_por_defecto(_hoy(cfg)), EspnNfl())
        liquidar(nfl)
    ctx, partidos, desde, hasta = _analizar(args, cfg, nfl)
    if not partidos:
        print(f"No hay partidos entre {desde} y {hasta} (o falta ejecutar 'nfl actualizar').")
        return 0
    valor_ = con_valor(partidos, cfg.nfl_valor_min)
    probables = mas_probables(partidos)
    guardar_picks(nfl, desde, valor_)
    md, js = escribir(cfg.reportes_dir, desde, hasta, partidos, valor_, probables, _novedades(ctx, nfl, partidos))
    n_ofertas = sum(len(a.evaluaciones) for a in partidos)
    print(f"{len(partidos)} partidos entre {desde} y {hasta}; {n_ofertas} líneas de las casas evaluadas.")
    if valor_:
        print("Con valor:")
        for e in valor_[:args.top]:
            print(f"  EV {e.ev * 100:+4.0f}%  {e.prob * 100:4.0f}%  {e.etiqueta():<48} {e.odd:.2f} {e.book or '':<11}"
                  f" ({e.team} vs {e.opp})")
    tds = sorted((t for a in partidos for t in a.tds), key=lambda t: -t.p1)[:10]
    print("Más probables de anotar:")
    for t in tds:
        print(f"  {t.p1 * 100:4.0f}%  2+: {t.p2 * 100:4.1f}%  {t.nombre} ({t.pos}, {t.team} vs {t.opp})")
    print(f"Informe: {md}\nDatos: {js}\n")
    print(AVISO.replace("> ", "").replace("**", ""))
    return 0


def cmd_td(args, cfg: Config, db: Database) -> int:
    nfl = NflDB(db.conn)
    ctx, partidos, desde, hasta = _analizar(args, cfg, nfl)
    tds = sorted((t for a in partidos for t in a.tds), key=lambda t: -(t.p2 if args.multiples else t.p1))
    if not tds:
        print("Sin partidos en la ventana (o falta 'nfl actualizar').")
        return 0
    print(f"{'Jugador':<26}{'Eq.':<5}{'vs':<5}{'TD esp.':>8}{'P(1+)':>8}{'justa':>8}{'casa':>8}{'P(2+)':>8}"
          f"{'justa':>8}{'casa':>8}{'1º TD':>7}")
    for t in tds[:args.top]:
        o1, o2 = t.ofertas.get("1+"), t.ofertas.get("2+")
        print(f"{t.nombre[:25]:<26}{t.team:<5}{t.opp:<5}{t.lam:8.2f}{t.p1 * 100:7.0f}%"
              f"{americana(cuota_justa(t.p1)):>8}{americana(o1.odd) if o1 else '-':>8}{t.p2 * 100:7.1f}%"
              f"{americana(cuota_justa(t.p2)):>8}{americana(o2.odd) if o2 else '-':>8}{t.p_first * 100:6.1f}%")
    print("\n'justa' = cuota americana que corresponde a la probabilidad; 'casa' = mejor cuota encontrada.")
    print("Si la casa paga más que la justa, hay valor.")
    return 0


def cmd_matchup(args, cfg: Config, db: Database) -> int:
    nfl = NflDB(db.conn)
    a_team = equipos.por_texto(args.equipo)
    b_team = equipos.por_texto(args.rival) if args.rival else None
    if not a_team or (args.rival and not b_team):
        print("No reconozco el equipo. Usa la abreviatura (BUF), el apodo (Bills) o la ciudad.")
        return 2
    desde = args.desde or _hoy(cfg).isoformat()
    juegos = [dict(g) for g in nfl.proximos_partidos(desde, (date.fromisoformat(desde) + timedelta(days=21)).isoformat())
              if a_team in (g["home_team"], g["away_team"]) and (b_team is None or b_team in (g["home_team"], g["away_team"]))]
    ctx = construir_contexto(nfl.conn, desde)
    if juegos:
        g = juegos[0]
    else:
        if not b_team:
            print(f"{a_team} no tiene partido en las próximas 3 semanas; indica el rival.")
            return 2
        g = {"game_id": f"hipotetico_{a_team}_{b_team}", "home_team": b_team, "away_team": a_team,
             "gameday": desde, "gametime": None, "spread_line": None, "total_line": None, "wind": None, "roof": None,
             "temp": None}
    mercado = None
    if not args.sin_lineas and juegos:
        try:
            mercado = _mercados(cfg, nfl, desde, (date.fromisoformat(g["gameday"]) - date.fromisoformat(desde)).days + 1,
                                [g]).get(g["game_id"])
        except Exception as e:
            log.warning("Sin líneas: %s", e)
    a = analizar_partido(ctx, g, mercado, cfg.nfl_peso_mercado)
    print(f"# {a.titulo} ({g['gameday']})\n")
    for team, ent in a.entornos.items():
        p = ctx.perfiles[team]
        print(f"## Ataque de {equipos.nombre(team)} contra la defensa de {equipos.nombre(ent.opp)}")
        print(f"Puntos esperados {ent.puntos:.1f} ({ent.puntos_fuente}); {ent.tds:.2f} TD "
              f"({ent.rush_tds:.2f} por tierra, {ent.pass_tds:.2f} por aire). "
              f"{p.ataque['pts']:.1f} puntos por partido "
              f"({texto_rango(rango(ctx, 'ataque', 'pts', team))}); el rival concede "
              f"{ctx.perfiles[ent.opp].defensa['pts']:.1f} ({texto_rango(rango(ctx, 'defensa', 'pts', ent.opp), 'más concede', 'menos concede')}).")
        for c in a.claves[team]:
            print(f"  - {c}")
        for b in ctx.bajas.get(team, []):
            print(f"  - Baja: {b['nombre']} ({b['pos']}) {b['estado']}")
        print()
    print("## Touchdowns")
    for t in a.tds[:12]:
        print(f"  {t.nombre:<24} {t.team:<4} P(anota) {t.p1 * 100:4.0f}%  P(2+) {t.p2 * 100:4.1f}%  "
              f"(tierra {t.rush:.2f}, aire {t.rec:.2f})")
    print("\n## Proyecciones")
    for p in sorted(a.proyecciones, key=lambda p: (p.jugador.team, -sum(p.volumen.values()))):
        if sum(p.volumen.values()) < 2.5:
            continue
        txt = ", ".join(f"{p.medias[s]:.1f} {NOMBRES[s]}" for s in ("pass_yds", "pass_tds", "rush_yds", "rec", "rec_yds")
                        if s in p.medias)
        print(f"  {p.jugador.nombre:<24} {p.jugador.pos:<3}{p.jugador.team:<4} {txt}")
    if a.evaluaciones:
        print("\n## Mejores líneas")
        for e in sorted([e for e in a.evaluaciones if e.ev is not None], key=lambda e: -e.ev)[:8]:
            print(f"  EV {e.ev * 100:+4.0f}%  {e.etiqueta()}  {e.odd:.2f} ({e.book})")
            for r in e.razones.a_favor[:3]:
                print(f"      ✔ {r}")
            for r in e.razones.en_contra[:2]:
                print(f"      ✘ {r}")
    return 0


def cmd_validar(args, cfg: Config, db: Database) -> int:
    nfl = NflDB(db.conn)
    try:
        ap = interpretar(args.apuesta)
    except ValueError as e:
        print(f"No entendí la apuesta: {e}.\nEjemplos: \"Derrick Henry +2 TD\", \"Josh Allen 2 touchdowns vs "
              f"Chargers\", \"Saquon más de 69.5 yardas por tierra @ -110\".")
        return 2
    if args.cuota:
        ap.cuota = args.cuota
    desde = args.desde or _hoy(cfg).isoformat()
    ctx = construir_contexto(nfl.conn, desde)
    ids = buscar_jugador(ctx, ap.jugador)
    if not ids:
        print(f"No encuentro a '{ap.jugador}' en la base (¿ejecutaste 'nfl actualizar'?).")
        return 2
    pid = ids[0]
    team = (ctx.roster.get(pid) or {}).get("team") or ctx.jugadores[pid][0]["team"]
    hasta = (date.fromisoformat(desde) + timedelta(days=args.dias or 10)).isoformat()
    juegos = [dict(g) for g in nfl.proximos_partidos(desde, hasta) if team in (g["home_team"], g["away_team"])]
    if ap.rival and ap.rival != team:
        contra_rival = [g for g in juegos if ap.rival in (g["home_team"], g["away_team"])]
        if not contra_rival:
            print(f"_{team} no juega contra {ap.rival} entre {desde} y {hasta}: análisis hipotético en campo de "
                  f"{ap.rival}, sin líneas de las casas._\n")
            juegos = [{"game_id": f"hipotetico_{team}_{ap.rival}", "home_team": ap.rival, "away_team": team,
                       "gameday": desde, "gametime": None, "spread_line": None, "total_line": None, "wind": None,
                       "roof": None, "temp": None}]
        else:
            juegos = contra_rival
    if not juegos:
        print(f"{team} no juega entre {desde} y {hasta}. Indica el rival (\"vs Chargers\") para un análisis hipotético.")
        return 2
    g = juegos[0]
    mercado = None
    if not args.sin_lineas and not g["game_id"].startswith("hipotetico"):
        try:
            mercado = _mercados(cfg, nfl, desde, (date.fromisoformat(g["gameday"]) - date.fromisoformat(desde)).days + 1,
                                [g]).get(g["game_id"])
        except Exception as e:
            log.warning("Sin líneas: %s", e)
    a = analizar_partido(ctx, g, mercado, cfg.nfl_peso_mercado)
    try:
        v = validar(ctx, ap, {g["game_id"]: a}, pid)
    except ValueError as e:
        print(f"No se puede evaluar: {e}.")
        return 2
    print(texto_veredicto(ctx, v))
    if not g["game_id"].startswith("hipotetico"):
        guardar_picks(nfl, desde, [v.evaluacion], origen="validar")
    print("\n" + AVISO.replace("> ", "").replace("**", ""))
    return 0


def cmd_jugador(args, cfg: Config, db: Database) -> int:
    nfl = NflDB(db.conn)
    desde = args.desde or _hoy(cfg).isoformat()
    ctx = construir_contexto(nfl.conn, desde)
    ids = buscar_jugador(ctx, args.nombre)
    if not ids:
        print(f"No encuentro a '{args.nombre}'.")
        return 2
    pid = ids[0]
    partidos = ctx.jugadores[pid]
    r = ctx.roster.get(pid, {})
    pos = r.get("position") or partidos[0].get("position")
    team = r.get("team") or partidos[0]["team"]
    les = ctx.lesiones.get(pid)
    print(f"# {partidos[0]['name']} ({pos}, {equipos.nombre(team)})")
    if les:
        print(f"Parte de lesiones: {les['status']} {les.get('detail') or ''} — {les.get('comment') or ''}")
    for m in ctx.movimientos.get(pid, []):
        print(f"Movimiento: {m['from_team']} → {m['to_team']} (semana {m['week']})")
    stats = {"QB": ("pass_yds", "pass_tds", "ints", "rush_yds", "tds"), "RB": ("rush_att", "rush_yds", "rec", "rec_yds", "tds"),
             "WR": ("targets", "rec", "rec_yds", "tds"), "TE": ("targets", "rec", "rec_yds", "tds")}.get(
        "RB" if pos in ("RB", "FB") else pos, ("rec_yds", "tds"))
    print("\nÚltimos partidos:")
    print(f"  {'Sem.':<10}{'Rival':<6}" + "".join(f"{NOMBRES[s][:12]:>14}" for s in stats) + f"{'snaps':>8}{'zona roja':>11}")
    for p in partidos[:10]:
        rz = (p.get("rz_carries") or 0) + (p.get("rz_targets") or 0)
        print(f"  {p['season']}-{p['week']:<5}{('@' if not p['is_home'] else '') + p['opp']:<6}"
              + "".join(f"{valor(p, s):>14g}" for s in stats)
              + f"{(p.get('offense_pct') or 0) * 100:7.0f}%{rz:>11g}")
    print("\nTendencias (líneas de referencia = su mediana):")
    for s in stats:
        vals = sorted(valor(p, s) for p in partidos[:10])
        if not vals:
            continue
        line = 0.5 if s == "tds" else int(vals[len(vals) // 2]) + 0.5
        t = tendencias(ctx, partidos, s, line, "más", partidos[0]["opp"])
        niveles = ", ".join(f"vs defensas {k}: {m:.1f} ({n})" for k, (m, n) in t.por_nivel.items())
        print(f"  {NOMBRES[s]} más de {line:g}: últimos 5 {t.aciertos_5[0]}/{t.aciertos_5[1]}, últimos 10 "
              f"{t.aciertos_10[0]}/{t.aciertos_10[1]}, temporada {t.aciertos_temporada[0]}/{t.aciertos_temporada[1]}"
              f"; local {t.local or 0:.1f} / visitante {t.visitante or 0:.1f}; {niveles}")
    rivales: dict[str, list[float]] = {}
    for p in partidos:
        rivales.setdefault(p["opp"], []).append(valor(p, "tds"))
    mejores = sorted(((sum(v) / len(v), len(v), o) for o, v in rivales.items() if len(v) >= 2), reverse=True)[:5]
    if mejores:
        print("\nContra quién anota más (TD por partido, mínimo 2 partidos): "
              + ", ".join(f"{o} {m:.2f} ({n})" for m, n, o in mejores))
    return 0


def cmd_rendimiento(args, cfg: Config, db: Database) -> int:
    r = rendimiento(NflDB(db.conn))
    if not r["total"]:
        print("Aún no hay selecciones liquidadas. 'nfl actualizar' las liquida cuando nflverse publica el partido.")
        return 0

    def linea(nombre, x):
        ben = "" if x["beneficio"] is None else f"  {x['beneficio']:+.2f} u en {x['con_cuota']} con cuota"
        return (f"  {nombre:<26} n={x['n']:<5} acierto {x['acierto'] * 100:5.1f}%  "
                f"prob. media {x['prob_media'] * 100:5.1f}%{ben}")

    print(linea("Total", r["total"]))
    print("Por tramo de probabilidad (si el acierto queda por debajo del tramo, el modelo es optimista):")
    for t in r["tramos"]:
        print(linea(t["tramo"], t))
    print("Por estadística:")
    for s in r["stats"]:
        print(linea(NOMBRES.get(s["stat"], s["stat"]), s))
    for o in r["origen"]:
        print(linea(f"origen: {o['origen']}", o))
    return 0


def cmd_backtest(args, cfg: Config, db: Database) -> int:
    filas = backtest(db.conn, args.desde, args.hasta,
                     progreso=lambda d, n: log.info("%s: %d predicciones", d, n))
    if not filas:
        print("Sin partidos en ese rango (descárgalos antes con 'nfl actualizar --temporadas ...').")
        return 0
    r = resumen(filas)
    print("Brier (menor es mejor) del modelo frente a una referencia ingenua (su propia frecuencia histórica):")
    for s, x in sorted(r["stats"].items()):
        ing = f"{x['brier_ingenua']:.4f}" if x["brier_ingenua"] is not None else "-"
        print(f"  {s:<14} n={x['n']:<6} acierto {x['acierto'] * 100:5.1f}%  prob. media {x['prob_media'] * 100:5.1f}%  "
              f"Brier {x['brier']:.4f}  ingenua {ing}")
    print("Anotar 1+ TD por tramo (¿pasa lo que dice?):")
    for t in r["tramos_td"]:
        print(f"  {t['tramo']:<8} n={t['n']:<6} dice {t['prob_media'] * 100:5.1f}%  pasó {t['acierto'] * 100:5.1f}%")
    print("Yardas y conteos (línea = mediana de sus últimos 8):")
    for t in r["tramos"]:
        print(f"  {t['tramo']:<8} n={t['n']:<6} dice {t['prob_media'] * 100:5.1f}%  pasó {t['acierto'] * 100:5.1f}%")
    return 0


def registrar(sub) -> None:
    nfl = sub.add_parser("nfl", help="props, touchdowns y enfrentamientos de la NFL")
    s = nfl.add_subparsers(dest="nfl_cmd", required=True)

    u = s.add_parser("actualizar", help="descarga lo nuevo de nflverse y ESPN (stats, lesiones, traspasos)")
    u.add_argument("--temporadas", type=int, nargs="+", help="por defecto, la actual y las dos anteriores")
    u.add_argument("--forzar", action="store_true", help="vuelve a descargar todo aunque no haya cambiado")
    u.add_argument("--sin-espn", action="store_true", help="no consultar lesiones ni traspasos de ESPN")
    u.set_defaults(func=cmd_actualizar)

    def ventana(p):
        p.add_argument("--desde", help="AAAA-MM-DD (por defecto, hoy)")
        p.add_argument("--dias", type=int, help="días por delante (por defecto APUESTAS_NFL_DIAS = 7)")
        p.add_argument("--sin-lineas", action="store_true", help="no pedir líneas a SportsGameOdds")

    a = s.add_parser("analizar", help="props, touchdowns y valor de los próximos partidos -> informe")
    ventana(a)
    a.add_argument("--sin-descarga", action="store_true", help="no actualizar la base antes")
    a.add_argument("--equipo", help="solo los partidos de este equipo")
    a.add_argument("--top", type=int, default=15)
    a.set_defaults(func=cmd_analizar)

    t = s.add_parser("td", help="quién tiene más probabilidad de anotar (y de anotar 2 o más)")
    ventana(t)
    t.add_argument("--equipo", help="solo los partidos de este equipo")
    t.add_argument("--multiples", action="store_true", help="ordenar por P(2+ TD)")
    t.add_argument("--top", type=int, default=25)
    t.set_defaults(func=cmd_td)

    m = s.add_parser("matchup", help="el enfrentamiento de dos equipos, métrica a métrica")
    m.add_argument("equipo")
    m.add_argument("rival", nargs="?")
    m.add_argument("--desde")
    m.add_argument("--sin-lineas", action="store_true")
    m.set_defaults(func=cmd_matchup)

    v = s.add_parser("validar", help='¿es buena esta apuesta? p. ej. "Derrick Henry +2 TD"')
    v.add_argument("apuesta")
    v.add_argument("--cuota", type=float, help="tu cuota decimal (si no, la mejor que se encuentre)")
    v.add_argument("--desde")
    v.add_argument("--dias", type=int)
    v.add_argument("--sin-lineas", action="store_true")
    v.set_defaults(func=cmd_validar)

    j = s.add_parser("jugador", help="ficha de un jugador: rol, tendencias y rivales")
    j.add_argument("nombre")
    j.add_argument("--desde")
    j.set_defaults(func=cmd_jugador)

    r = s.add_parser("rendimiento", help="acierto real de las selecciones liquidadas")
    r.set_defaults(func=cmd_rendimiento)

    b = s.add_parser("backtest", help="calibración sobre partidos ya jugados")
    b.add_argument("--desde", required=True)
    b.add_argument("--hasta", required=True)
    b.set_defaults(func=cmd_backtest)
