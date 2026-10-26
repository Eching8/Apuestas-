"""Informe de la jornada en Markdown y JSON (reportes/nfl/AAAA-MM-DD.md y .json)."""
from __future__ import annotations

import json
from pathlib import Path

from ..report import AVISO
from . import equipos
from .analizador import AnalisisPartido, Evaluacion
from .modelo import NOMBRES, americana, cuota_justa, p_al_menos


def _pct(p: float | None, dec: int = 0) -> str:
    return "-" if p is None else f"{p * 100:.{dec}f}%"


def _odd(o: float | None) -> str:
    return "-" if not o else f"{o:.2f} ({americana(o)})"


def _ev(e: float | None) -> str:
    return "-" if e is None else f"{e * 100:+.0f}%"


def _fila_eval(e: Evaluacion, partido: str) -> str:
    razon = "; ".join(e.razones.a_favor[:2]) or (e.razones.contexto[0] if e.razones.contexto else "")
    casa = f"{_odd(e.odd)} {e.book or ''}".strip()
    return (f"| {e.etiqueta()} | {partido} | {_pct(e.prob)} | {_pct(e.prob_modelo)} | {_pct(e.prob_casa)} | "
            f"{casa} | {_ev(e.ev)} | {razon} |")


def _titulo_corto(a: AnalisisPartido) -> str:
    return f"{a.game['away_team']} @ {a.game['home_team']}"


def markdown(desde: str, hasta: str, partidos: list[AnalisisPartido], valor: list[Evaluacion],
             probables: list[Evaluacion], novedades: dict, top_td: int = 25) -> str:
    L = [f"# NFL: props y touchdowns del {desde} al {hasta}", "", AVISO, ""]
    L.append(f"{len(partidos)} partidos. Datos hasta la semana {novedades.get('ultima_semana', '?')} "
             f"({novedades.get('temporada', '')}); lesiones de ESPN de {novedades.get('lesiones_al', '?')}.")
    L.append("")
    # Novedades: traspasos y bajas importantes.
    if novedades.get("traspasos"):
        L += ["## Traspasos y cambios de equipo recientes", ""]
        L += [f"- {t}" for t in novedades["traspasos"]] + [""]
    if novedades.get("bajas"):
        L += ["## Bajas que mueven el reparto", ""]
        L += [f"- {b}" for b in novedades["bajas"]] + [""]
    por_juego = {a.game["game_id"]: _titulo_corto(a) for a in partidos}
    L += ["## Apuestas con valor (la cuota paga más de lo que vale)", "",
          "Probabilidad final = mezcla del modelo y la casa sin margen. EV = probabilidad × mejor cuota − 1.", ""]
    if valor:
        L += ["| Selección | Partido | Prob. | Modelo | Casa | Mejor cuota | EV | Por qué |", "|---|---|---|---|---|---|---|---|"]
        L += [_fila_eval(e, por_juego.get(e.game_id, "")) for e in valor[:30]]
    else:
        L.append("_Ninguna selección supera los filtros de valor (o no hay líneas de las casas todavía)._")
    L.append("")
    if probables:
        L += ["## Las más probables (con cuota jugable)", "",
              "| Selección | Partido | Prob. | Modelo | Casa | Mejor cuota | EV | Por qué |", "|---|---|---|---|---|---|---|---|"]
        L += [_fila_eval(e, por_juego.get(e.game_id, "")) for e in probables[:20]] + [""]
    # Touchdowns.
    tds = sorted((t for a in partidos for t in a.tds), key=lambda t: -t.p1)
    fechas = {a.game["game_id"]: a.game["gameday"][5:] for a in partidos}
    L += ["## ¿Quién anota? Probabilidad de touchdown", "",
          "| Jugador | Equipo | vs | TD esp. | P(anota) | Cuota justa | Mejor cuota (EV) | P(2+) | Cuota justa 2+ | "
          "Mejor cuota 2+ (EV) | P(primer TD) |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for t in tds[:top_td]:
        o1, o2 = t.ofertas.get("1+"), t.ofertas.get("2+")
        L.append(f"| {t.nombre} ({t.pos}) | {t.team} | {t.opp} {fechas.get(t.game_id, '')} | {t.lam:.2f} | {_pct(t.p1)} | "
                 f"{_odd(cuota_justa(t.p1))} | {_odd(o1.odd) + ' ' + _ev(o1.ev) if o1 and o1.odd else '-'} | "
                 f"{_pct(t.p2, 1)} | {_odd(cuota_justa(t.p2))} | "
                 f"{_odd(o2.odd) + ' ' + _ev(o2.ev) if o2 and o2.odd else '-'} | {_pct(t.p_first, 1)} |")
    L.append("")
    multi = sorted(tds, key=lambda t: -t.p2)[:12]
    L += ["### Candidatos a 2 o más touchdowns", ""]
    for t in multi:
        o2 = t.ofertas.get("2+")
        precio = f"; la casa paga {_odd(o2.odd)} (EV {_ev(o2.ev)})" if o2 and o2.odd else ""
        L.append(f"- **{t.nombre}** ({t.team} vs {t.opp}, {fechas.get(t.game_id, '')}): P(2+) {_pct(t.p2, 1)}, cuota justa "
                 f"{_odd(cuota_justa(t.p2))}{precio}. {t.rush:.2f} TD esperados por tierra y {t.rec:.2f} por aire.")
    L.append("")
    # Partido a partido.
    for a in partidos:
        g = a.game
        L += [f"## {a.titulo} — {g['gameday']} {g.get('gametime') or ''}", ""]
        clima = []
        if g.get("roof"):
            clima.append(f"estadio: {g['roof']}")
        if g.get("wind") is not None:
            clima.append(f"viento {g['wind']:.0f} mph")
        if g.get("temp") is not None:
            clima.append(f"{g['temp']:.0f} °F")
        for team, ent in a.entornos.items():
            L.append(f"- **{equipos.apodo(team)}**: {ent.puntos:.1f} puntos esperados ({ent.puntos_fuente}), "
                     f"{'favorito' if ent.spread > 0 else 'no favorito'} por {abs(ent.spread):.1f}; "
                     f"{ent.dropbacks:.0f} dropbacks y {ent.carries:.0f} carreras; {ent.tds:.2f} TD esperados.")
        if clima:
            L.append(f"- {', '.join(clima)}")
        if a.mercado and a.mercado.movimientos:
            L.append(f"- Mercado: {'; '.join(a.mercado.movimientos)}")
        L.append("")
        for team, claves in a.claves.items():
            if claves:
                L += [f"**Ataque de {equipos.apodo(team)} contra la defensa de "
                      f"{equipos.apodo(a.entornos[team].opp)}:**", ""] + [f"- {c}" for c in claves] + [""]
        principales = [e for e in a.evaluaciones if e.tipo == "equipo" and e.stat == "pts"
                       and e.periodo in ("game", "1h") and e.bet in ("ml", "sp", "ou") and e.consenso]
        if principales:
            orden = {"ml": 0, "sp": 1, "ou": 2}
            principales.sort(key=lambda e: (e.periodo != "game", orden[e.bet], e.player_id == "ALL", e.etiqueta()))
            L += ["**Mercados del partido** (simulación propia sin la casa; en la probabilidad final la casa pesa "
                  "60 % en el ganador y 85 % en spread y totales, donde el modelo no ha demostrado ventaja):", "",
                  "| Mercado | Modelo | Casa | Prob. | Mejor cuota | EV |", "|---|---|---|---|---|---|"]
            for e in principales:
                L.append(f"| {e.etiqueta()} | {_pct(e.prob_modelo)} | {_pct(e.prob_casa)} | {_pct(e.prob)} | "
                         f"{_odd(e.odd)} {e.book or ''} | {_ev(e.ev)} |")
            L.append("")
        otros = sorted([e for e in a.evaluaciones if e.ev is not None and e not in principales
                        and (e.tipo == "equipo" or e.pos in ("K", "DL", "LB", "DB") or e.periodo != "game")],
                       key=lambda e: -(e.ev or 0))[:8]
        if otros:
            L += ["**Otros mercados con mejor valor esperado** (cuartos, mitades, TD y FG del partido, quién anota "
                  "primero, defensores y pateadores):", ""]
            L += [f"- {e.etiqueta()}: prob. {_pct(e.prob)} (modelo {_pct(e.prob_modelo)}, casa {_pct(e.prob_casa)}), "
                  f"{_odd(e.odd)} en {e.book or '-'}, EV {_ev(e.ev)}" for e in otros] + [""]
        defensa = sorted(a.defensores, key=lambda d: -d.medias.get("tackles", 0))[:6]
        if defensa:
            L += ["**Defensores a seguir:** " + "; ".join(
                f"{d.jugador.nombre} ({d.jugador.pos}, {d.jugador.team}) {d.medias['tackles']:.1f} tacleadas, "
                f"{d.medias['sacks']:.2f} sacks" for d in defensa), ""]
        L += ["| Jugador | Proyección |", "|---|---|"]
        for p in sorted(a.proyecciones, key=lambda p: (p.jugador.team, -sum(p.volumen.values()))):
            if sum(p.volumen.values()) < 2.5:
                continue
            claves_stats = [s for s in ("pass_yds", "pass_tds", "rush_yds", "rec", "rec_yds") if s in p.medias]
            txt = ", ".join(f"{p.medias[s]:.1f} {NOMBRES[s]}" for s in claves_stats)
            notas = f" — {'; '.join(p.jugador.notas)}" if p.jugador.notas else ""
            L.append(f"| {p.jugador.nombre} ({p.jugador.pos}, {p.jugador.team}) | {txt}, "
                     f"P(TD) {_pct(p_al_menos(p.lambdas['tds'], 1))}{notas} |")
        L.append("")
        mejores = sorted([e for e in a.evaluaciones if e.ev is not None], key=lambda e: -(e.ev or 0))[:6]
        if mejores:
            L += ["**Las mejores líneas del partido:**", ""]
            for e in mejores:
                L.append(f"- **{e.etiqueta()}** — prob. {_pct(e.prob)} (modelo {_pct(e.prob_modelo)}, casa "
                         f"{_pct(e.prob_casa)}), mejor cuota {_odd(e.odd)} en {e.book or '-'}, EV {_ev(e.ev)}")
                for r in e.razones.a_favor[:4]:
                    L.append(f"  - ✔ {r}")
                for r in e.razones.en_contra[:3]:
                    L.append(f"  - ✘ {r}")
            L.append("")
    return "\n".join(L)


def _eval_json(e: Evaluacion) -> dict:
    return {"game_id": e.game_id, "player_id": e.player_id, "jugador": e.nombre, "pos": e.pos, "equipo": e.team,
            "rival": e.opp, "stat": e.stat, "codigo": e.codigo, "periodo": e.periodo, "tipo": e.tipo,
            "mercado": e.etiqueta(), "linea": e.line, "lado": e.lado, "prob": round(e.prob, 4),
            "prob_modelo": round(e.prob_modelo, 4), "prob_casa": e.prob_casa and round(e.prob_casa, 4),
            "media": round(e.mu, 2), "cuota": e.odd, "casa": e.book, "consenso": e.consenso,
            "ev": e.ev and round(e.ev, 4), "a_favor": e.razones.a_favor, "en_contra": e.razones.en_contra,
            "contexto": e.razones.contexto}


def escribir(directorio: Path, desde: str, hasta: str, partidos: list[AnalisisPartido], valor: list[Evaluacion],
             probables: list[Evaluacion], novedades: dict) -> tuple[Path, Path]:
    d = Path(directorio) / "nfl"
    d.mkdir(parents=True, exist_ok=True)
    md, js = d / f"{desde}.md", d / f"{desde}.json"
    md.write_text(markdown(desde, hasta, partidos, valor, probables, novedades), encoding="utf-8")
    datos = {
        "desde": desde, "hasta": hasta, "novedades": novedades,
        "valor": [_eval_json(e) for e in valor], "probables": [_eval_json(e) for e in probables],
        "partidos": [{
            "game_id": a.game["game_id"], "titulo": a.titulo, "fecha": a.game["gameday"],
            "entorno": {t: {"puntos": round(e.puntos, 2), "fuente": e.puntos_fuente, "spread": round(e.spread, 1),
                            "tds": round(e.tds, 3), "pass_tds": round(e.pass_tds, 3), "rush_tds": round(e.rush_tds, 3)}
                        for t, e in a.entornos.items()},
            "claves": a.claves,
            "touchdowns": [{"player_id": t.player_id, "jugador": t.nombre, "pos": t.pos, "equipo": t.team,
                            "lambda": round(t.lam, 3), "p_anota": round(t.p1, 4), "p_2mas": round(t.p2, 4),
                            "p_primero": round(t.p_first, 4), "notas": t.notas,
                            "ofertas": {k: _eval_json(v) for k, v in t.ofertas.items()}} for t in a.tds],
            "proyecciones": [{"player_id": p.jugador.player_id, "jugador": p.jugador.nombre, "pos": p.jugador.pos,
                              "equipo": p.jugador.team, "medias": {k: round(v, 2) for k, v in p.medias.items()},
                              "notas": p.jugador.notas} for p in a.proyecciones],
            "evaluaciones": [_eval_json(e) for e in a.evaluaciones],
            "simulacion": a.simulacion.medias if a.simulacion else None,
        } for a in partidos],
    }
    js.write_text(json.dumps(datos, ensure_ascii=False, indent=1), encoding="utf-8")
    return md, js
