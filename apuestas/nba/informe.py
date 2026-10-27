"""Informe del día en Markdown y JSON (reportes/nba/AAAA-MM-DD.*)."""
from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from ..report import AVISO
from .analizador import Partido, combinada_segura
from .modelo import NOMBRES, Contexto, Evaluacion, Segura, mejor_contra
from .zonas import NOMBRES as ZONAS_NOMBRE

MAX_POR_JUGADOR = 2
GRUPOS = {"G": "bases/escoltas", "F": "aleros/ala-pívots", "C": "pívots"}
COMPONENTE = {"pts": "Puntos", "reb": "Rebotes", "ast": "Asistencias", "tpm": "Triples", "stl": "Robos",
              "blk": "Tapones", "tov": "Pérdidas", "fgm": "Tiros de campo anotados", "ftm": "Tiros libres anotados",
              "fta": "Tiros libres intentados"}
CORTES = (("ult5", "Últ. 5"), ("ult10", "Últ. 10"), ("temporada", "Temporada"), ("anterior", "Temp. anterior"),
          ("vs_rival", "vs este rival"))


def _pct(x: float) -> str:
    return f"{x * 100:.0f}%"


def _rel(x: float) -> str:
    return f"{(x - 1) * 100:+.0f}%"


def etiqueta(e: Evaluacion) -> str:
    return f"{e.nombre}: {e.lado} de {e.line:g} {NOMBRES[e.stat]}"


def _etiqueta_fila(e: Evaluacion) -> str:
    # Un suplente depende de los minutos que le dé el técnico: en puntos y combinadas es el mayor riesgo.
    return f"**{etiqueta(e)}**" + ("" if e.titular else " ⚠️ suplente")


def _cuota(e: Evaluacion) -> str:
    return f"{e.odd:.2f} ({_pct(1 / e.odd)})" if e.odd else "-"


def _fila(e: Evaluacion, partido: str | None = None) -> str:
    vs = ", ".join(f"{v:g}" for v in e.vs_rival) or "-"
    celdas = ([partido] if partido else []) + [
        _etiqueta_fila(e), f"**{_pct(e.prob)}**", _pct(e.prob_modelo),
        _pct(e.prob_mercado) if e.prob_mercado is not None else "-", f"{e.mu:.1f} ± {e.sd:.1f}",
        f"{e.acierto_10[0]}/{e.acierto_10[1]}", f"{e.acierto_temporada[0]}/{e.acierto_temporada[1]}", vs,
        _cuota(e),
    ]
    return "| " + " | ".join(celdas) + " |"


CABECERA = ("| Prop | Prob. final | Modelo | Casa | Esperado | Últ. 10 | Temporada | vs este rival "
            "| Cuota (implícita) |")
SEPARADOR = "|---|---|---|---|---|---|---|---|---|"


def _metrica(v: float | None, tipo: str) -> str:
    if v is None:
        return "-"
    return f"{v * 100:.1f}%" if tipo == "tasa" else f"{v:.1f}"


def por_que(e: Evaluacion) -> list[str]:
    """De dónde sale la media de la prop y las estadísticas relacionadas en que se basa."""
    out = [f"**¿Por qué {e.mu:.1f} {NOMBRES[e.stat]}?** (línea {e.line:g}; {e.factores['minutos']:.1f} minutos esperados)", ""]
    for c, d in e.componentes.items():
        out.append(f"- {COMPONENTE[c]} **{d['final']:.1f}** (por componentes {d['por_motores']:.1f} · por tasa por "
                   f"minuto y defensa rival {d['por_tasa']:.1f}): {d['explicacion']}.")
    if e.metricas:
        out += ["", "| Estadística | " + " | ".join(n for _, n in CORTES) + " |",
                "|---" * (len(CORTES) + 1) + "|"]
        for m in e.metricas:
            out.append(f"| {m['metrica']} | " + " | ".join(_metrica(m[k], m["tipo"]) for k, _ in CORTES) + " |")
    return out + [""]


def _ficha(ctx: Contexto, part: Partido, pid: str) -> list[str]:
    j = part.jugadores[pid]
    evs = [e for e in part.evaluaciones if e.player_id == pid]
    rival = part.game["home_name"] if j.opp_id == part.game["home_id"] else part.game["away_name"]
    out = [f"#### {j.nombre} ({GRUPOS[j.grupo]}) vs {rival}", ""]
    out.append(f"- Minutos esperados: **{j.minutos:.1f}** (± {j.minutos_sd:.1f}); {j.n} partidos en la base.")
    for n in j.notas:
        out.append(f"- {n}")
    if evs:
        top = evs[0]
        out.append(f"- Su prop más probable hoy: **{etiqueta(top)}** ({_pct(top.prob)}). "
                   f"Con 80% de probabilidad: más de {top.linea_80[0] if top.linea_80[0] is not None else '-'} "
                   f"/ menos de {top.linea_80[1] if top.linea_80[1] is not None else '-'}.")
        ajuste = top.factores
        out.append(f"- Defensa de {rival} contra {GRUPOS[j.grupo]} en {NOMBRES[top.stat]}: {_rel(ajuste['rival'])} "
                   f"respecto a la media; ajuste por su historial contra defensas similares: "
                   f"{_rel(ajuste['tipo_defensa'])}.")
        out += [""] + por_que(top)
    if j.enfrentamiento:
        e = j.enfrentamiento
        out.append(f"- Marcaje (stats.nba.com): ajuste a sus puntos {_rel(e.factor)}. Defensores probables: "
                   + "; ".join(f"{d['nombre']} ({_pct(d['reparto'])}, defensor {d['nivel']}, permite "
                               f"{d['permite_100']:.0f} pts/100 vs {d['liga_100']:.0f} de media"
                               + (f"; él le anota {d['vs_el_pts_100']:.0f}/100 en {d['vs_el_posesiones']:.0f} pos."
                                  if d["vs_el_posesiones"] else "") + ")" for d in e.defensores) + ".")
        niveles = [f"{k} {v['pts_100']:.0f} pts/100 en {v['posesiones']:.0f} pos." for k, v in e.por_nivel.items()
                   if v["posesiones"]]
        if niveles:
            out.append("- Contra qué defensores le va mejor (sus puntos por 100 posesiones): " + "; ".join(niveles) + ".")
    tipos = []
    for stat in ("points", "rebounds", "assists", "threes"):
        m = mejor_contra(ctx, j, stat)
        if m:
            tipos.append(f"{NOMBRES[stat]}: " + ", ".join(f"vs defensa {k} {_rel(v)}" for k, v in m.items()))
    if tipos:
        out.append("- Rendimiento por minuto según la defensa rival (frente a su media): " + "; ".join(tipos) + ".")
    if sum(z["intentos"] for z in j.zonas.values()) >= 30:
        out += ["", "| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |", "|---|---|---|---|---|"]
        for z, d in sorted(j.zonas.items(), key=lambda kv: -kv[1]["reparto"]):
            out.append(f"| {ZONAS_NOMBRE[z]} | {_pct(d['reparto'])} | {_pct(d['pct'])} | {_pct(d['pct_liga'])} | "
                       f"{_pct(d['pct_rival'])} |")
    return out + [""]


def combinadas(picks: list[tuple[Partido, Evaluacion]]) -> list[str]:
    """Probabilidad de acertar todas: las más probables de partidos distintos, multiplicadas."""
    elegidas, partidos = [], set()
    for p, e in picks:
        if p.game["id"] not in partidos:
            partidos.add(p.game["id"])
            elegidas.append(e)
    if len(elegidas) < 2:
        return []
    out = ["**Si haces combinada:** cada selección que añades multiplica el riesgo. Probabilidad de acertar "
           "todas con las más probables de partidos distintos:", ""]
    prob = elegidas[0].prob
    for n, e in enumerate(elegidas[1:6], 2):
        prob *= e.prob
        out.append(f"- {n} selecciones: **{_pct(prob)}**")
    return out + ["", "Dentro de un mismo partido (bet builder) las selecciones no son independientes y el "
                  "cálculo es aún menos fiable. Con 12 selecciones al 65 % la probabilidad de acertar todas es "
                  "menor del 1 %.", ""]


CABECERA_SEGURAS = "| Jugador | Pick seguro | Prob. | Cuota mínima | Esperado | Últ. 10 |"
SEPARADOR_SEGURAS = "|---|---|---|---|---|---|"


def _fila_segura(s: Segura, partido: str | None = None) -> str:
    celdas = ([partido] if partido else []) + [
        s.nombre, f"**más de {s.line:g} {NOMBRES[s.stat]}**", f"**{_pct(s.prob)}**", f"{s.cuota_minima:.2f}",
        f"{s.mu:.1f}", f"{s.acierto_10[0]}/{s.acierto_10[1]}"]
    return "| " + " | ".join(celdas) + " |"


def seccion_seguras(partidos: list[Partido], n: int = 15) -> list[str]:
    todas = sorted(((p, s) for p in partidos for s in p.seguras), key=lambda x: (-x[1].prob, -x[1].line))
    if not todas:
        return []
    return ["## Picks seguros de titulares estables", "",
            "Líneas bajas (alternativas) de titulares con 30+ minutos: mejor un \"15+ puntos\" casi seguro de "
            "una estrella que la línea normal de un suplente. En el backtest, elegidas al 85 % acertaron el "
            "89-96 %. **Cuota mínima** = la que hace falta para que valga la pena (1 / probabilidad); búscala en "
            "las líneas alternativas de tu casa.", "",
            "| Partido " + CABECERA_SEGURAS, "|---" + SEPARADOR_SEGURAS] + \
        [_fila_segura(s, p.titulo) for p, s in todas[:n]] + [""]


def combinada_alternas(partidos: list[Partido], n: int = 4) -> list[tuple[Partido, Segura]]:
    """El pick seguro más probable de cada partido (líneas alternativas de titulares estables)."""
    mejores = [(p, p.seguras[0]) for p in partidos if p.seguras]
    return sorted(mejores, key=lambda x: -x[1].prob)[:n]


def seccion_combinada_segura(candidatas: list[tuple[Partido, Evaluacion]], partidos: list[Partido] = (),
                             n: int = 4) -> list[str]:
    out = ["## Combinada segura del día", ""]
    alternas = combinada_alternas(list(partidos), n)
    if len(alternas) >= 2:
        out += ["**Opción A, líneas alternativas (la más segura):** el pick seguro más probable de cada partido, "
                "de titulares estables. Búscalas en las líneas alternativas de tu casa (\"15+\", \"20+\"...): "
                "cada una vale la pena si paga al menos su cuota mínima.", "",
                "| Partido | Selección | Prob. | Cuota mínima | Esperado | Últ. 10 |", "|---|---|---|---|---|---|"]
        prob = 1.0
        filas = []
        for k, (p, s_) in enumerate(alternas, 1):
            out.append(f"| {p.titulo} | **{s_.nombre}: más de {s_.line:g} {NOMBRES[s_.stat]}** | **{_pct(s_.prob)}** | "
                       f"{s_.cuota_minima:.2f} | {s_.mu:.1f} | {s_.acierto_10[0]}/{s_.acierto_10[1]} |")
            prob *= s_.prob
            if k >= 2:
                filas.append(f"| {k} | **{_pct(prob)}** |")
        out += ["", "| Selecciones | Probabilidad de acertar todas |", "|---|---|"] + filas + [""]
    combi = combinada_segura(candidatas, n)
    if not combi:
        return out + ["Hoy ninguna línea principal cumple los filtros de jugador constante.", ""]
    out += [f"**Opción {'B' if len(alternas) >= 2 else 'A'}, líneas principales con cuota real:**", "",
           "Se elige por **probabilidad**, no por valor: la más probable de cada partido entre jugadores "
           "constantes (titulares con minutos estables, sin cambio de rol, traspaso ni lesión, que la habrían "
           "pasado en 7+ de sus últimos 10 y en el 60 %+ de esta temporada) y con cuota real de la casa. Si tu "
           "casa no ofrece esa línea, usa la siguiente de la lista \"Las más seguras con cuota\".", "",
           "| Partido | Selección | Prob. | Cuota | Últ. 10 | Temporada |", "|---|---|---|---|---|---|"]
    for p, e in combi:
        out.append(f"| {p.titulo} | **{etiqueta(e)}** | **{_pct(e.prob)}** | {e.odd:.2f} | "
                   f"{e.acierto_10[0]}/{e.acierto_10[1]} | {e.acierto_temporada[0]}/{e.acierto_temporada[1]} |")
    out += ["", "| Selecciones | Probabilidad de acertar todas | Cuota |", "|---|---|---|"]
    prob = cuota = 1.0
    for k, (_, e) in enumerate(combi, 1):
        prob *= e.prob
        cuota *= e.odd
        if k >= 2:
            out.append(f"| {k} | **{_pct(prob)}** | {cuota:.2f} |")
    out += ["", "### Las más seguras con cuota", "", "| Partido " + CABECERA, "|---" + SEPARADOR]
    out += [_fila(e, p.titulo) for p, e in candidatas[:12]] + [""]
    return out


def seccion_cuotadas(combis: list) -> list[str]:
    cuotadas = [c for c in combis if c.tipo.startswith("cuota_")]
    if not cuotadas:
        return []
    out = ["## Combinadas con cuota objetivo", "",
           "La combinación de jugadores constantes (mismos filtros que la opción B, partidos distintos) con más "
           "probabilidad de acertar todas cuya cuota llega al objetivo. Se registran como picks de prueba y se "
           "liquidan solas: `nba rendimiento` dice cuándo el sistema está listo para dinero real.", ""]
    for c in cuotadas:
        out += [f"**Cuota {c.tipo.split('_')[1]}+:** cuota {c.cuota:.2f}, probabilidad de acertar todas "
                f"**{_pct(c.prob)}**", ""]
        out += [f"- {x['nombre']}: {x['side']} de {x['line']:g} {NOMBRES[x['stat']]} ({_pct(x['prob'])}, cuota "
                f"{x['odd']:.2f}) — {x['partido']}" for x in c.patas] + [""]
    return out


def mejores_del_partido(part: Partido, n: int) -> list[Evaluacion]:
    out, por_jugador = [], {}
    for e in part.evaluaciones:
        if por_jugador.get(e.player_id, 0) >= MAX_POR_JUGADOR:
            continue
        por_jugador[e.player_id] = por_jugador.get(e.player_id, 0) + 1
        out.append(e)
        if len(out) == n:
            break
    return out


def escribir(dir_: Path, fecha: str, ctx: Contexto, partidos: list[Partido],
             picks: list[tuple[Partido, Evaluacion]], sin_emparejar: list[str],
             por_partido: int = 8, candidatas: list[tuple[Partido, Evaluacion]] = (),
             combis: list = (), criterios: list = ()) -> tuple[Path, Path]:
    dir_ = dir_ / "nba"
    dir_.mkdir(parents=True, exist_ok=True)
    md = [f"# Props NBA {fecha}", "", AVISO, "",
          "**Modelo** = minutos, tasa por minuto, bajas, defensa rival por posición, zonas de tiro y tipo de "
          "defensa, mezclado con el acierto real del jugador sobre esa línea. **Casa** = probabilidad implícita "
          "en las cuotas sin el margen. **Prob. final** = mezcla de ambas. Si modelo y casa discrepan mucho, "
          "la casa suele saber algo (rol, rotación, una baja): revísalo antes de apostar.", "",
          "Cada media se construye desde las estadísticas que la producen (tiros × acierto por zona, % de los "
          "rebotes disponibles que captura, % de las canastas de sus compañeros que asiste...) y se muestra con "
          "esas estadísticas en sus últimos 5 y 10 partidos, la temporada y contra este rival. Todo queda "
          "guardado en la tabla `nba_analisis` de la base.", ""]
    if criterios:
        cumplidos = sum(ok for _, ok, _ in criterios)
        listo = cumplidos == len(criterios)
        md += ["## Estado de calibración", "",
               ("**Listo para dinero real.**" if listo else "**En calibración: todos los picks son de prueba.** ")
               + f" {cumplidos} de {len(criterios)} criterios cumplidos:", ""]
        md += [f"- {'✅' if ok else '⬜'} {nombre}: {detalle}" for nombre, ok, detalle in criterios] + [""]
    md += seccion_combinada_segura(list(candidatas), partidos)
    md += seccion_cuotadas(combis)
    md += seccion_seguras(partidos)
    md += ["## Las más probables del día", ""]
    if picks:
        md += ["| Partido " + CABECERA, "|---" + SEPARADOR]
        md += [_fila(e, p.titulo) for p, e in picks[:30]]
        md += [""] + combinadas(picks) + ["### En qué se basan las 10 más probables", ""]
        for p, e in picks[:10]:
            md += [f"#### {etiqueta(e)} ({_pct(e.prob)}) — {p.titulo}", ""] + por_que(e)
    else:
        md.append("Ninguna prop supera el umbral de probabilidad hoy.")
    md.append("")
    for part in partidos:
        g = part.game
        md += [f"## {part.titulo}", ""]
        if part.lesiones:
            md.append("Parte de lesiones: " + "; ".join(f"{l['name']} ({l['status']})" for l in part.lesiones) + ".")
            md.append("")
        if not part.evaluaciones:
            md += ["Sin líneas de props para este partido (o sin historial suficiente de los jugadores).", ""]
            continue
        elegidas = mejores_del_partido(part, por_partido)
        if part.seguras:
            md += ["Picks seguros de titulares estables:", "", CABECERA_SEGURAS, SEPARADOR_SEGURAS]
            md += [_fila_segura(s) for s in part.seguras[:6]] + [""]
        md += [f"Las {len(elegidas)} más probables (máximo {MAX_POR_JUGADOR} por jugador: las de un mismo jugador "
               "suelen ganar o perder juntas).", "", CABECERA, SEPARADOR] + [_fila(e) for e in elegidas] + [""]
        destacados = list(dict.fromkeys(e.player_id for e in elegidas))[:5]
        md += ["### Fichas de los jugadores destacados", ""]
        for pid in destacados:
            md += _ficha(ctx, part, pid)
    if sin_emparejar:
        md += ["## Sin emparejar con ESPN", "", ", ".join(sin_emparejar), ""]
    ruta_md = dir_ / f"{fecha}.md"
    ruta_md.write_text("\n".join(md), encoding="utf-8")
    ruta_js = dir_ / f"{fecha}.json"
    ruta_js.write_text(json.dumps({
        "fecha": fecha,
        "picks": [{"partido": p.titulo, **asdict(e)} for p, e in picks],
        "partidos": [{"partido": p.titulo, "game_id": p.game["id"], "lesiones": p.lesiones,
                      "seguras": [asdict(s) for s in p.seguras],
                      "evaluaciones": [asdict(e) for e in p.evaluaciones]} for p in partidos],
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    return ruta_md, ruta_js
