"""Reporte en Markdown (y JSON) del análisis diario."""
from __future__ import annotations

import json
from pathlib import Path

from .markets import kelly

STAT_ES = {"goals": "Goles", "corners": "Córners", "cards": "Tarjetas", "shots": "Remates", "shots_on": "Al arco"}


def _pct(x: float | None) -> str:
    return "-" if x is None else f"{x * 100:.1f}%"


def to_markdown(result: dict) -> str:
    lines = [f"# Análisis de fútbol — {result['fecha']}", ""]
    perf = result.get("rendimiento") or {}
    if perf.get("picks"):
        lines += [f"**Histórico:** {perf['aciertos']}/{perf['picks']} picks acertados · ROI {_pct(perf['roi_picks'])} · "
                  f"Brier {perf['brier']:.3f} · combinadas {perf['combinadas_ganadas']}/{perf['combinadas']} "
                  f"(ROI {_pct(perf['roi_combinadas'])})", ""]

    v = result.get("validacion")
    if v:
        lines += [f"**Datos verificados con dos fuentes:** {v['partidos_validados']} partidos del historial confirmados "
                  f"({v['estadisticas_coinciden']}/{v['estadisticas_comparadas']} estadísticas coinciden), "
                  f"{v['con_discrepancia']} con discrepancias, {v['sin_segunda_fuente']} sin segunda fuente disponible.", ""]
    lines += ["## Combinadas", ""]
    if not result["combinadas"]:
        lines += ["_No hay combinadas que cumplan los filtros hoy._", ""]
    for i, c in enumerate(result["combinadas"], 1):
        ev = (f" · EV {_pct(c['ev'])}" if c["ev"] is not None
              else " · cuota mínima a exigir (las patas marcadas con * no tienen cuota real)")
        lines.append(f"### {i}. {c['tipo']} — prob. {_pct(c['probabilidad'])} · cuota {c['cuota']:.2f}{ev}")
        for s in c["selecciones"]:
            star = "" if s.get("cuota_real") else "*"
            lines.append(f"- {s['partido']}: **{s['mercado']} — {s['seleccion']}** ({_pct(s['prob'])} @ {s['cuota']:.2f}{star})")
        lines.append("")

    lines += ["## Partidos", ""]
    for m in result["partidos"]:
        lines += [f"### {m['partido']}", f"{m['liga']} · {m['hora']} · árbitro: {m['arbitro'] or 'N/D'} · "
                  f"calidad de datos {m['calidad_datos']:.0%} · forma {m['forma']['local'] or '-'} / {m['forma']['visitante'] or '-'}", ""]
        lines += ["| Estadística | Local | Visitante | Total |", "|---|---|---|---|"]
        for s, v in m["esperado"].items():
            lines.append(f"| {STAT_ES[s]} | {v['local']:.2f} | {v['visitante']:.2f} | {v['local'] + v['visitante']:.2f} |")
        lines.append("")
        if m["jugadores"]:
            lines.append("Jugadores (remates / al arco esperados): " + ", ".join(
                f"{p['nombre']} {p['remates_esp']:.1f}/{p['al_arco_esp']:.1f}" for p in m["jugadores"][:4]))
            lines.append("")
        if m["mercados_optimos"]:
            lines += ["| Mercado | Selección | Prob. | Cuota justa | Cuota casa | Cuota mín. | EV | Stake (Kelly ¼) |",
                      "|---|---|---|---|---|---|---|---|"]
            for p in m["mercados_optimos"]:
                stake = _pct(kelly(p["prob"], p["odds"])) if p["odds"] else "-"
                lines.append(f"| {p['market']} | {p['selection']} | {_pct(p['prob'])} | {p['fair_odds']:.2f} | "
                             f"{p['odds'] or '-'} | {p['min_odds'] or '-'} | {_pct(p['ev'])} | {stake} |")
        else:
            lines.append("_Sin mercados que superen los filtros._")
        lines.append("")
    lines += ["---", "_Cuota mín.: en mercados sin cuota real, apuesta solo si tu casa paga al menos esa cuota._",
              "_Probabilidades estimadas por modelo estadístico; no garantizan resultados. Apuesta con responsabilidad._"]
    return "\n".join(lines)


def save(result: dict, out_dir: str = "reports") -> tuple[Path, Path]:
    path = Path(out_dir)
    path.mkdir(parents=True, exist_ok=True)
    md = path / f"analisis_{result['fecha']}.md"
    js = path / f"analisis_{result['fecha']}.json"
    md.write_text(to_markdown(result), encoding="utf-8")
    js.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return md, js
