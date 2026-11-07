"""Informe del día de la NHL en Markdown y JSON (reportes/nhl/AAAA-MM-DD.*)."""
from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from ..report import AVISO
from .analizador import Partido, combinada_segura, cuota
from .combinadas import nombre_tipo
from .modelo import GRUPOS_TEXTO, NOMBRES, Contexto, Evaluacion, Segura

MAX_POR_JUGADOR = 2


def _pct(x: float) -> str:
    return f"{x * 100:.0f}%"


def etiqueta(e: Evaluacion) -> str:
    return f"{e.nombre}: {e.lado} de {e.line:g} {NOMBRES[e.stat]}"


def _cuota_txt(e: Evaluacion) -> str:
    if e.odd:
        return f"{e.odd:.2f}"
    return f"~{cuota(e):.2f} (estimada)"


def _fila(e: Evaluacion, partido: str | None = None) -> str:
    vs = ", ".join(f"{v:g}" for v in e.vs_rival) or "-"
    celdas = ([partido] if partido else []) + [
        f"**{etiqueta(e)}**" + (" ⚠️ papel menor" if not e.titular else "") + (" (línea estimada)" if e.estimada else ""),
        f"**{_pct(e.prob)}**", _pct(e.prob_modelo), _pct(e.prob_mercado) if e.prob_mercado is not None else "-",
        f"{e.mu:.1f} ± {e.sd:.1f}", f"{e.acierto_10[0]}/{e.acierto_10[1]}",
        f"{e.acierto_temporada[0]}/{e.acierto_temporada[1]}", vs, _cuota_txt(e)]
    return "| " + " | ".join(celdas) + " |"


CABECERA = "| Prop | Prob. final | Modelo | Casa | Esperado | Últ. 10 | Temporada | vs este rival | Cuota |"
SEPARADOR = "|---|---|---|---|---|---|---|---|---|"


def en_corto(e: Evaluacion) -> list[str]:
    out = [f"**{etiqueta(e)}** ({_pct(e.prob)}; esperado {e.mu:.1f})", ""] + [f"- {a}" for a in e.argumentos]
    if e.alertas:
        out.append(f"- ⚠️ Alertas: {', '.join(e.alertas)}")
    return out + [""]


def _fila_segura(s: Segura, partido: str | None = None) -> str:
    celdas = ([partido] if partido else []) + [
        s.nombre, f"**más de {s.line:g} {NOMBRES[s.stat]}**", f"**{_pct(s.prob)}**", f"{s.cuota_minima:.2f}",
        f"{s.mu:.1f}", f"{s.acierto_10[0]}/{s.acierto_10[1]}"]
    return "| " + " | ".join(celdas) + " |"


def seccion_seguras(partidos: list[Partido], n: int = 15) -> list[str]:
    todas = sorted(((p, s) for p in partidos for s in p.seguras), key=lambda x: (-x[1].prob, -x[1].line))
    if not todas:
        return []
    return ["## Picks seguros (líneas alternativas)", "",
            "Líneas bajas de jugadores de papel principal sin alertas, sin bajar de la mínima que suele abrir Betano. "
            "**Cuota mínima** = 1 / probabilidad.", "",
            "| Partido | Jugador | Selección | Prob. | Cuota mínima | Esperado | Últ. 10 |", "|---|---|---|---|---|---|---|"] \
        + [_fila_segura(s, p.titulo) for p, s in todas[:n]] + [""]


def seccion_combinadas(combis: list, candidatas: list[tuple[Partido, Evaluacion]], partidos: list[Partido]) -> list[str]:
    out = ["## Combinadas del día", "",
           "Por **probabilidad**, no por valor: jugadores constantes (papel principal, tiempo en hielo estable, sin "
           "cambio de línea ni de unidad de power play, traspaso ni lesión; 7+ de sus últimos 10 y 60 %+ de esta "
           "temporada; cada pata 62 %+), un partido por pata, las menos patas posibles. Con dinero real: patas del "
           "70 %+ y máximo 4-5. **Sin líneas de la casa la cuota es estimada** (la justa menos el margen de Betano): "
           "mándame las cuotas de Betano y evalúo esas exactas.", ""]
    for c in combis:
        if c.tipo == "builder":
            continue
        cuota_txt = f"cuota {'~' if c.estimada else ''}{c.cuota:.2f}{' (estimada)' if c.estimada else ''}" \
            if c.cuota else f"cuota justa {1 / c.prob:.2f}"
        out += [f"### {nombre_tipo(c.tipo)} ({len(c.patas)} patas)", "",
                f"Probabilidad de acertar todas: **{_pct(c.prob)}** (1 de cada {1 / c.prob:.1f}); {cuota_txt}.", ""]
        for x in c.patas:
            out.append(f"- **{x['nombre']}: {x['side']} de {x['line']:g} {NOMBRES[x['stat']]}** ({_pct(x['prob'])}) "
                       f"— {x['partido']}" + (" (línea estimada: confírmala en Betano)" if x.get("linea_estimada") else ""))
            out += [f"  - {a}" for a in x.get("argumentos", [])]
        out.append("")
    if not [c for c in combis if c.tipo != "builder"]:
        out += ["Hoy no hay suficientes patas de jugadores constantes para una combinada.", ""]
    out += ["### Las más seguras de jugadores constantes", "", "| Partido " + CABECERA, "|---" + SEPARADOR]
    out += [_fila(e, p.titulo) for p, e in candidatas[:15]] + [""]
    return out


def seccion_builders(builders: list) -> list[str]:
    if not builders:
        return []
    out = ["## Bet builders del día", "",
           "Por partido, 2-3 \"más de\" de jugadores constantes con el mismo guion, sin bajar de la línea mínima de "
           "Betano y que cada uno pasó en 2 de cada 3 partidos de esta temporada. La probabilidad tiene en cuenta que "
           "los del mismo partido se mueven juntos. **Cuota justa** = 1 / probabilidad: el bet builder de Betano "
           "recorta mucho; no lo aceptes por debajo.", ""]
    for b in builders:
        out += [f"**{b.partido.titulo}** — acertar las {len(b.piernas)}: **{_pct(b.prob)}**, cuota justa "
                f"{b.cuota_justa:.2f}", ""]
        out += [f"- {p.etiqueta} ({_pct(p.prob)}; esperado {p.mu:.1f}; últ. 10: {p.acierto_10[0]}/{p.acierto_10[1]})"
                for p in b.piernas] + [""]
    return out


def seccion_seguimiento(ayer: tuple[str, list] | None, acumulado: list) -> list[str]:
    out = []
    if ayer and ayer[1]:
        fecha, combis = ayer
        ganadas = sum(1 for c in combis if c["result"] == 1)
        cerradas = sum(1 for c in combis if c["result"] in (0, 1))
        out += [f"## Seguimiento: combinadas del {fecha}", "", f"Ganadas {ganadas} de {cerradas} liquidadas.", ""]
        marca = {1: "✅", 0: "❌", 2: "➖ anulada", None: "⏳"}
        for c in combis:
            estado = {1: "✅ GANADA", 0: "❌ perdida", 2: "➖ anulada", None: "⏳ pendiente"}[c["result"]]
            cuota_txt = f", cuota {c['cuota']:.2f}" if c["cuota"] else ""
            out.append(f"**{nombre_tipo(c['tipo'])}** — {estado} (prob. {_pct(c['prob'] or 0)}{cuota_txt})")
            out += [f"  - {marca[x['resultado']]} {x['nombre']}: {x['side']} de {x['line']:g} {NOMBRES[x['stat']]}"
                    + (f" → {x['real']:g}" if x["real"] is not None else "") for x in c["patas"]]
            out.append("")
    if acumulado:
        out += ["### Acumulado de las combinadas", "",
                "| Tipo | Jugadas | Ganadas | % ganadas | Prob. prometida | Beneficio (1 u) |", "|---|---|---|---|---|---|"]
        for a in acumulado:
            ben = "-" if a["beneficio"] is None else f"{a['beneficio']:+.2f} u en {a['con_cuota']}"
            out.append(f"| {nombre_tipo(a['tipo'])} | {a['n']} | {a['ganadas']} | {a['ganadas'] / a['n'] * 100:.0f}% | "
                       f"{_pct(a['prob_media'])} | {ben} |")
        out.append("")
    return out


def mejores_del_partido(part: Partido, n: int) -> list[Evaluacion]:
    out, por_jugador = [], {}
    for e in part.evaluaciones:
        if not e.titular or por_jugador.get(e.player_id, 0) >= MAX_POR_JUGADOR:
            continue
        por_jugador[e.player_id] = por_jugador.get(e.player_id, 0) + 1
        out.append(e)
        if len(out) == n:
            break
    return out


def escribir(dir_: Path, fecha: str, ctx: Contexto, partidos: list[Partido], picks: list[tuple[Partido, Evaluacion]],
             avisos: list[str], candidatas: list, combis: list, builders: list,
             ayer: tuple[str, list] | None = None, acumulado: list = (), por_partido: int = 8) -> tuple[Path, Path]:
    dir_ = dir_ / "nhl"
    dir_.mkdir(parents=True, exist_ok=True)
    md = [f"# Props NHL {fecha}", "", AVISO, "",
          "**Modelo** = tiempo en hielo esperado (igualdad y power play por separado) × tasa por minuto × defensa "
          "rival por posición (delanteros / defensas) × portero rival de hoy (goles y puntos) × penaltis del rival "
          "(tiempo en power play), mezclado con el acierto real del jugador sobre esa línea y calibrado con el "
          "backtest de 2025-26. **Casa** = probabilidad sin margen (solo si hay líneas). Cada pata trae su \"En "
          "corto\" con los datos que la respaldan.", ""]
    md += [f"> {a}" for a in avisos] + ([""] if avisos else [])
    md += seccion_seguimiento(ayer, list(acumulado))
    md += seccion_combinadas(combis, candidatas, partidos)
    md += seccion_builders(builders)
    md += seccion_seguras(partidos)
    md += ["## Las más probables del día (jugadores de papel principal)", ""]
    principales = [(p, e) for p, e in picks if e.titular and not e.alertas]
    if principales:
        md += ["| Partido " + CABECERA, "|---" + SEPARADOR] + [_fila(e, p.titulo) for p, e in principales[:30]]
        md += ["", "### En corto: las 10 más probables", ""]
        for p, e in principales[:10]:
            md += [f"*{p.titulo}*", ""] + en_corto(e)
    else:
        md.append("Ninguna prop supera el umbral de probabilidad hoy.")
    md.append("")
    for part in partidos:
        g = part.game
        md += [f"## {part.titulo}", ""]
        porteros = []
        for lado in ("away", "home"):
            pid = g.get(f"{lado}_goalie_id")
            nombre = ctx.nombres_porteros.get(pid) if pid else None
            sv = ctx.sv_portero.get(pid) if pid else None
            porteros.append(f"{g[f'{lado}_abbr']}: {nombre or 'sin confirmar'}"
                            + (f" ({sv * 100:.1f}% de paradas)" if sv else ""))
        md += ["Porteros probables (ESPN): " + "; ".join(porteros) + ".", ""]
        margen = ctx.margen.get(g["home_id"])
        if margen is not None:
            fav = g["home_name"] if margen > 0 else g["away_name"]
            md += [f"Diferencia esperada: {fav} por {abs(margen):.2f} goles"
                   + (f"; total de la casa {g['total_esperado']:g}" if g.get("total_esperado") else "") + ".", ""]
        if part.lesiones:
            md += ["Parte de lesiones: " + "; ".join(f"{l['name']} ({l['status']})" for l in part.lesiones) + ".", ""]
        elegidas = mejores_del_partido(part, por_partido)
        if not elegidas:
            md += ["Sin jugadores con historial suficiente.", ""]
            continue
        if part.seguras:
            md += ["Picks seguros:", "", "| Jugador | Selección | Prob. | Cuota mínima | Esperado | Últ. 10 |",
                   "|---|---|---|---|---|---|"] + [_fila_segura(s) for s in part.seguras[:6]] + [""]
        md += [f"Las {len(elegidas)} más probables de jugadores de papel principal (máximo {MAX_POR_JUGADOR} por "
               "jugador).", "", CABECERA, SEPARADOR] + [_fila(e) for e in elegidas] + [""]
        for e in elegidas[:3]:
            j = part.jugadores.get(e.player_id)
            if j and j.notas:
                md.append(f"- {e.nombre} ({GRUPOS_TEXTO.get(j.grupo, j.grupo)}): " + "; ".join(j.notas))
        md.append("")
    ruta_md = dir_ / f"{fecha}.md"
    ruta_md.write_text("\n".join(md), encoding="utf-8")
    ruta_js = dir_ / f"{fecha}.json"
    ruta_js.write_text(json.dumps({
        "fecha": fecha,
        "picks": [{"partido": p.titulo, **asdict(e)} for p, e in picks[:200]],
        "combinadas": [{"tipo": c.tipo, "prob": c.prob, "cuota": c.cuota, "patas": c.patas} for c in combis],
        "partidos": [{"partido": p.titulo, "game_id": p.game["id"], "lesiones": p.lesiones,
                      "seguras": [asdict(s) for s in p.seguras]} for p in partidos],
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    return ruta_md, ruta_js
