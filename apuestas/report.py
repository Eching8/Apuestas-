"""Informe diario en Markdown y JSON, y registro de las selecciones en la base de datos."""
from __future__ import annotations

import json
from pathlib import Path

from .analyzer import Analysis
from .combinadas import Combo
from .db import Database, now_iso
from .model import NOMBRES, STATS, Market

AVISO = (
    "> **Aviso:** las apuestas implican riesgo de perder dinero. Estas probabilidades son estimaciones "
    "estadísticas, no garantías: ningún modelo acierta siempre y las combinadas multiplican el riesgo. "
    "Apuesta solo lo que puedas permitirte perder. Si el juego deja de ser un entretenimiento, busca ayuda."
)


def _pct(p: float | None) -> str:
    return "-" if p is None else f"{p * 100:.0f}%"


def _odd(o: float | None) -> str:
    return "-" if o is None else f"{o:.2f}"


def _partido(fx) -> str:
    return f"{fx['home_name']} vs {fx['away_name']}"


def _market_row(m: Market) -> str:
    return (f"| {m.label} | {_pct(m.prob)} | {_pct(m.market_prob)} | {_pct(m.final_prob)} | "
            f"{_odd(m.fair_odd)} | {_odd(m.odd)} | {_odd(m.best_odd)} | "
            f"{'-' if m.edge is None else f'{m.edge * 100:+.1f}%'} |")


def render_markdown(fecha: str, analyses: list[Analysis], picks: dict[int, list[Market]],
                    combos: dict[str, list[Combo]], titulo: str = "Análisis de partidos") -> str:
    out = [f"# {titulo} — {fecha}", "", AVISO, ""]

    out += ["## Combinadas", ""]
    titulos = {"alta_probabilidad": "Alta probabilidad", "valor": "Alto valor (EV positivo)"}
    for perfil, lista in combos.items():
        out += [f"### {titulos.get(perfil, perfil)}", ""]
        if not lista:
            out += ["Ninguna combinada cumple los filtros hoy.", ""]
        for i, c in enumerate(lista, 1):
            cuota = f"cuota {c.odd:.2f}" if c.con_cuotas else f"cuota justa {c.odd:.2f} (pide más que esto a tu casa)"
            ev = f", EV {c.ev * 100:+.1f}%, stake sugerido {c.kelly * 100:.1f}% del bankroll" if c.con_cuotas else ""
            out.append(f"**{i}. Probabilidad {_pct(c.prob)}, {cuota}{ev}**")
            for l in c.legs:
                out.append(f"- {l.partido}: {l.market.label} ({_pct(l.prob)}, {_odd(l.market.odd or l.market.fair_odd)})")
            out.append("")

    out += ["## Partidos", ""]
    for a in analyses:
        fx = a.fixture
        liga = f"{fx['league_name'] or ''} ({fx['league_country'] or ''})"
        cuando = fx.get("cuando") or f"{fx['date_utc']} UTC"
        out += [f"### {_partido(fx)}", f"{liga} · {cuando}", ""]
        for n in a.notas:
            out.append(f"- _{n}_")
        if not a.ok:
            out.append("")
            continue
        e = a.expectation
        if e is not None:
            stats = [s for s in STATS if s in e.home]
            out += ["", "| Esperado | " + " | ".join(NOMBRES[s] for s in stats) + " |",
                    "|---|" + "---|" * len(stats)]
            out.append(f"| {fx['home_name']} | " + " | ".join(f"{e.home[s]:.2f}" for s in stats) + " |")
            out.append(f"| {fx['away_name']} | " + " | ".join(f"{e.away[s]:.2f}" for s in stats) + " |")
            out.append("| Total | " + " | ".join(f"{e.total(s):.2f}" for s in stats) + " |")
            out.append(f"\nPartidos usados: {e.n_home} (local) y {e.n_away} (visitante).\n")
        else:
            out.append("")
        sel = picks.get(fx["id"], [])
        if sel:
            out += ["| Selección | Modelo | Mercado | Final | Cuota justa | Cuota (mediana) | Mejor | Valor |",
                    "|---|---|---|---|---|---|---|---|"]
            out += [_market_row(m) for m in sel]
        else:
            out.append("Ninguna selección supera los filtros de probabilidad y valor.")
        out.append("")
    return "\n".join(out)


def _market_json(m: Market) -> dict:
    return {k: getattr(m, k) for k in ("key", "label", "prob", "market_prob", "final_prob", "fair_odd", "odd",
                                       "best_odd", "bookmakers", "edge")}


def write_reports(directory: Path, fecha: str, analyses: list[Analysis], picks: dict[int, list[Market]],
                  combos: dict[str, list[Combo]], prefijo: str = "",
                  titulo: str = "Análisis de partidos") -> tuple[Path, Path]:
    directory.mkdir(parents=True, exist_ok=True)
    md = directory / f"{prefijo}{fecha}.md"
    md.write_text(render_markdown(fecha, analyses, picks, combos, titulo), encoding="utf-8")
    data = {
        "fecha": fecha,
        "partidos": [{
            "fixture_id": a.fixture["id"], "partido": _partido(a.fixture), "notas": a.notas,
            "solo_mercado": a.solo_mercado,
            "esperado": None if a.expectation is None else {"local": a.expectation.home, "visitante": a.expectation.away},
            "selecciones": [_market_json(m) for m in picks.get(a.fixture["id"], [])],
        } for a in analyses],
        "combinadas": {perfil: [{
            "prob": c.prob, "cuota": c.odd, "con_cuotas": c.con_cuotas, "ev": c.ev, "kelly": c.kelly,
            "selecciones": [{"fixture_id": l.fixture_id, "partido": l.partido, **_market_json(l.market)} for l in c.legs],
        } for c in lista] for perfil, lista in combos.items()},
    }
    js = directory / f"{prefijo}{fecha}.json"
    js.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return md, js


def save_picks(db: Database, fecha: str, picks: dict[int, list[Market]], combos: dict[str, list[Combo]]) -> None:
    """Guarda las recomendaciones del día (sustituye las aún no liquidadas si se vuelve a ejecutar)."""
    ts = now_iso()
    with db.tx():
        db.conn.execute("DELETE FROM picks WHERE fecha = ? AND result IS NULL", (fecha,))
        db.conn.execute("DELETE FROM combos WHERE fecha = ? AND result IS NULL "
                        "AND NOT EXISTS (SELECT 1 FROM picks WHERE combo_id = combos.id)", (fecha,))
        for fixture_id, markets in picks.items():
            for m in markets:
                db.conn.execute(
                    "INSERT INTO picks(fecha, fixture_id, market_key, label, prob, odd, edge, created_at) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (fecha, fixture_id, m.key, m.label, m.final_prob or m.prob, m.odd, m.edge, ts),
                )
        for perfil, lista in combos.items():
            for c in lista:
                cur = db.conn.execute(
                    "INSERT INTO combos(fecha, perfil, prob, odd, ev, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                    (fecha, perfil, c.prob, c.odd if c.con_cuotas else None, c.ev if c.con_cuotas else None, ts),
                )
                for l in c.legs:
                    db.conn.execute(
                        "INSERT INTO picks(fecha, fixture_id, market_key, label, prob, odd, edge, combo_id, created_at) "
                        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (fecha, l.fixture_id, l.market.key, l.market.label, l.prob, l.market.odd, l.market.edge,
                         cur.lastrowid, ts),
                    )
