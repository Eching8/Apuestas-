"""La hoja de picks de cada partido: los dos lados, ya analizados y listos para elegir.

Para cada equipo del partido:

- **Sus ventajas**: dónde su ataque supera a la defensa rival (métrica a métrica), el punto débil de la defensa
  rival en la zona roja y la situación del QB.
- **Touchdowns**: sus candidatos de cualquier posición con P(anota) y P(2+), cuota justa, mejor cuota, valor
  esperado y cuál de las dos apuestas tiene sentido (o la cuota mínima si ninguna lo tiene hoy).
- **Props**: las que tienen valor (pasan los filtros de selección) y las más probables con precio jugable.
- **Defensa**: sus defensores con más tacleadas y sacks esperados.

Y al final, los picks recomendados del partido de los dos lados, ordenados por valor esperado.
"""
from __future__ import annotations

from . import equipos
from .analizador import AnalisisPartido, Evaluacion, TdJugador, con_valor
from .modelo import Contexto, cuota_justa, qb_del_partido, _nombre
from .zona_roja import defensa_rz

VALOR_TD = 0.03          # valor esperado mínimo para recomendar una apuesta de TD


def _pct(p: float | None, dec: int = 0) -> str:
    return "-" if p is None else f"{p * 100:.{dec}f}%"


def _ev(e: float | None) -> str:
    return "-" if e is None else f"{e * 100:+.0f}%"


def opcion_td(t: TdJugador) -> tuple[str, float | None, Evaluacion | None]:
    """La apuesta de TD que tiene sentido para este jugador: (texto, valor esperado, evaluación)."""
    candidatas = [(k, e) for k, e in t.ofertas.items() if k in ("1+", "2+") and e.odd and e.ev is not None]
    con_valor_ = [(k, e) for k, e in candidatas if e.ev >= VALOR_TD and (e.edge or 0) > 0]
    if con_valor_:
        k, e = max(con_valor_, key=lambda x: x[1].ev)
        return (f"✅ {'anota' if k == '1+' else '2+ TD'} a {e.odd:.2f} ({e.book}), valor {_ev(e.ev)}", e.ev, e)
    minimo = cuota_justa(t.p1)
    if candidatas:
        mejor = max(candidatas, key=lambda x: x[1].ev)[1]
        return (f"sin valor hoy: anota solo a {minimo * 1.04:.2f} o más (la mejor es {mejor.odd:.2f})"
                if minimo else "sin valor hoy", mejor.ev, None)
    return (f"sin línea: anota vale a partir de {minimo * 1.04:.2f}" if minimo else "sin línea", None, None)


def ventajas(ctx: Contexto, a: AnalisisPartido, team: str) -> list[str]:
    out = []
    ent = a.entornos[team]
    rival = equipos.apodo(ent.opp)
    for c in a.claves.get(team, []):
        if "VENTAJA CLARA DEL ATAQUE" in c or ("ventaja del ataque" in c and len(out) < 2):
            out.append(c.split(" → ")[0] + (" (ventaja clara)" if "CLARA" in c else ""))
    d = sorted(defensa_rz(ctx, ent.opp).values(), key=lambda x: -x.ratio)
    if d and d[0].ratio >= 1.2:
        out.append(f"Zona roja: {rival} concede a los {d[0].pos} {d[0].ratio:.1f} veces los TD de la media dentro de la 20")
    titular, principal, suplente = qb_del_partido(ctx, team)
    if suplente:
        out.append(f"Ojo: juega {_nombre(ctx, titular)}, QB suplente (menos puntos y menos zona roja; más balón al RB1 "
                   f"cerca de la meta)")
    return out[:5]


def hoja(ctx: Contexto, a: AnalisisPartido, top_td: int = 4, top_props: int = 4) -> list[str]:
    g = a.game
    L = [f"## {a.titulo} — {g['gameday']} {g.get('gametime') or ''}", ""]
    valor_partido = con_valor([a], valor_min=0.04)
    for team, ent in a.entornos.items():
        favorito = f"favorito por {ent.spread:.1f}" if ent.spread > 0 else f"no favorito por {abs(ent.spread):.1f}"
        L += [f"### {equipos.nombre(team)} ({ent.puntos:.1f} puntos esperados, {favorito}, {ent.tds:.1f} TD)", ""]
        v = ventajas(ctx, a, team)
        if v:
            L += ["**Ventajas sobre la defensa de " + equipos.apodo(ent.opp) + ":**"] + [f"- {x}" for x in v] + [""]
        tds = [t for t in a.tds if t.team == team][:top_td]
        if tds:
            L += ["**Touchdowns:**", "", "| Jugador | Anota | 2+ TD | Mejor cuota anota | Mejor cuota 2+ | Qué apostar |",
                  "|---|---|---|---|---|---|"]
            for t in tds:
                o1, o2 = t.ofertas.get("1+"), t.ofertas.get("2+")
                c1 = f"{o1.odd:.2f} ({_ev(o1.ev)})" if o1 and o1.odd else "-"
                c2 = f"{o2.odd:.2f} ({_ev(o2.ev)})" if o2 and o2.odd else "-"
                L.append(f"| {t.nombre} ({t.pos}) | {_pct(t.p1)} | {_pct(t.p2, 1)} | {c1} | {c2} | {opcion_td(t)[0]} |")
            L.append("")
        propias = [e for e in a.evaluaciones if e.team == team and e.tipo == "jugador" and e.odd
                   and e.stat not in ("tds", "first_td", "last_td")]
        con = [e for e in valor_partido if e.team == team and e.tipo == "jugador"
               and e.stat not in ("tds", "first_td", "last_td")][:top_props]
        probables = sorted([e for e in propias if e.prob >= 0.6 and (e.ev or -1) >= -0.02 and e not in con
                            and e.periodo == "game"], key=lambda e: -e.prob)[:3]
        if con or probables:
            L.append("**Props:**")
            for e in con:
                L.append(f"- ✅ {e.etiqueta()} — {_pct(e.prob)} (modelo {_pct(e.prob_modelo)}, casa {_pct(e.prob_casa)}), "
                         f"{e.odd:.2f} en {e.book}, valor {_ev(e.ev)}. "
                         + ("; ".join(e.razones.a_favor[:2]) or (e.razones.contexto[0] if e.razones.contexto else "")))
            for e in probables:
                L.append(f"- 🔒 {e.etiqueta()} — {_pct(e.prob)}, {e.odd:.2f} en {e.book}, valor {_ev(e.ev)} (de las "
                         f"más probables)")
            L.append("")
        defensa = sorted([d for d in a.defensores if d.jugador.team == team],
                         key=lambda d: -d.medias.get("tackles", 0))[:3]
        sacks = sorted([d for d in a.defensores if d.jugador.team == team],
                       key=lambda d: -d.medias.get("sacks", 0))[:2]
        if defensa:
            L.append("**Defensa:** tacleadas: " + ", ".join(f"{d.jugador.nombre} {d.medias['tackles']:.1f}" for d in defensa)
                     + "; sacks: " + ", ".join(f"{d.jugador.nombre} {d.medias['sacks']:.2f}" for d in sacks) + ".")
            L.append("")
    # Picks del partido, los dos lados juntos.
    picks = [e for e in valor_partido]
    for t in a.tds:
        _, ev, e = opcion_td(t)
        if e is not None and e not in picks:
            picks.append(e)
    picks.sort(key=lambda e: -(e.ev or 0))
    L += ["### Picks recomendados del partido (los dos lados)", ""]
    if picks:
        for e in picks[:8]:
            lado = equipos.apodo(e.team) if e.team in equipos.EQUIPOS else "Partido"
            L.append(f"- [{lado}] **{e.etiqueta()}** — prob. {_pct(e.prob)}, {e.odd:.2f} en {e.book}, valor {_ev(e.ev)}")
    else:
        L.append("- Ninguna apuesta de este partido supera los filtros de valor con las cuotas de ahora.")
    L.append("")
    return L
