"""Validar una apuesta escrita como la diría un apostador: "Derrick Henry +2 TD", "Josh Allen 2 touchdowns vs
Chargers", "Saquon más de 69.5 yardas por tierra", "Lamb over 5.5 recepciones".

Responde como un tipster: por qué la gente la juega (la narrativa: rachas, el último partido, el rival, el
movimiento de la línea), qué dice la data (modelo, enfrentamiento, tendencias) y un veredicto con la cuota
mínima a la que vale la pena.
"""
from __future__ import annotations

import difflib
import re
from dataclasses import dataclass, field

from ..nba.sgo import clave_nombre
from . import equipos
from .analizador import (PESO_MERCADO, AnalisisPartido, Evaluacion, _evaluacion_simple, evaluar, primer_td,
                         primer_td_periodo)
from .mercado import Oferta
from .modelo import NOMBRES, Contexto, _nombre, cuota_justa, p_al_menos, qb_del_partido, valor
from .modelo_defensa import pateador
from .modelo_partido import prob_pateador
from .razones import lectura_td, tendencias

# Palabras -> estadística. El orden importa: primero las frases más específicas.
PATRONES_STAT = (
    (r"td(?:s)? de pase|pases? de td|passing td|pass(?:ing)? touchdowns?|touchdowns? de pase", "pass_tds"),
    (r"td(?:s)? por tierra|td(?:s)? de carrera|rushing td|rush(?:ing)? touchdowns?", "rush_tds"),
    (r"td(?:s)? de recepci[oó]n|td(?:s)? por recepci[oó]n|receiving td", "rec_tds"),
    (r"primer td|primer touchdown|first td|first touchdown|1st td", "first_td"),
    (r"[uú]ltimo td|[uú]ltimo touchdown|last td|last touchdown", "last_td"),
    (r"yardas? de pase \+ carrera|pass\+rush|pase y carrera", "pass_rush_yds"),
    (r"yardas? (?:de )?(?:carrera|tierra) ?\+ ?(?:de )?recepci[oó]n|rush\+rec|scrimmage|yardas? totales", "rush_rec_yds"),
    (r"yardas? (?:de |por )?pase|passing yards|pass yds", "pass_yds"),
    (r"yardas? (?:de |por )?(?:carrera|tierra)|rushing yards|rush yds", "rush_yds"),
    (r"yardas? (?:de |por )?recepci[oó]n|receiving yards|rec yds", "rec_yds"),
    (r"recepci[oó]n m[aá]s larga|longest reception", "long_rec"),
    (r"carrera m[aá]s larga|longest rush", "long_rush"),
    (r"recepciones|receptions|catches|atrapadas", "rec"),
    (r"acarreos|carries|intentos de carrera|rush attempts", "rush_att"),
    (r"pases completos|completions|completados", "comp"),
    (r"intentos de pase|pass attempts|pases intentados", "pass_att"),
    (r"intercepciones|interceptions|\bints?\b", "ints"),
    (r"targets|env[ií]os|objetivos", "targets"),
    (r"pase (?:completo )?m[aá]s largo|longest completion", "long_pass"),
    (r"yardas por acarreo|yards per (?:carry|attempt)|\bypc\b", "ypc"),
    (r"fantasy|puntos de fantas[ií]a", "fantasy"),
    (r"tacleadas? (?:en )?solitario|solo tackles", "solo"),
    (r"tacleadas? asistidas?|assisted tackles", "asist"),
    (r"tacleadas?|tackles|placajes", "tackles"),
    (r"\bsacks?\b|capturas", "sacks"),
    (r"intercepciones? \(?defens|defensive int", "def_ints"),
    (r"puntos (?:del )?pateador|kicking points", "kick_pts"),
    (r"goles? de campo|field goals?|\bfgs?\b", "fg"),
    (r"puntos? extras?|extra points?|\bxps?\b|\bpats?\b", "xp"),
    (r"touchdowns?|\btds?\b|anota(?:r[aá]?)?|anytime", "tds"),
)
PALABRAS_RUIDO = {"MAS", "MENOS", "DE", "OVER", "UNDER", "O", "Y", "EN", "EL", "LA", "LOS", "VS", "CONTRA", "ANTE",
                  "PARTIDO", "HOY", "APUESTA", "PARA", "UN", "UNA", "QUE", "ANOTADOS", "ANOTA", "ANOTARA", "ANOTAR",
                  "MULTIPLES", "VARIOS", "AL", "MENOS", "LO", "SE", "POR", "WILL", "SCORE", "PLUS", "MORE", "THAN"}


PERIODOS_TEXTO = (
    (r"1\.?\s*(?:er|º)?\s*cuarto|primer cuarto|1q\b|first quarter|1st quarter", "1q"),
    (r"2\.?\s*º?\s*cuarto|segundo cuarto|2q\b|second quarter", "2q"),
    (r"3\.?\s*(?:er|º)?\s*cuarto|tercer cuarto|3q\b|third quarter", "3q"),
    (r"4\.?\s*º?\s*cuarto|cuarto cuarto|[uú]ltimo cuarto|4q\b|fourth quarter", "4q"),
    (r"1\.?\s*ª?\s*mitad|primera mitad|primer tiempo|1h\b|first half|1st half", "1h"),
    (r"2\.?\s*ª?\s*mitad|segunda mitad|segundo tiempo|2h\b|second half|2nd half", "2h"),
)


@dataclass
class Apuesta:
    texto: str
    jugador: str
    stat: str
    line: float
    lado: str
    rival: str | None = None
    cuota: float | None = None
    periodo: str = "game"


def interpretar(texto: str) -> Apuesta:
    """Convierte el texto en (jugador, estadística, línea, lado). Lanza ValueError si no se entiende."""
    t = texto.strip()
    periodo = "game"
    for patron, p in PERIODOS_TEXTO:
        m_per = re.search(patron, t.lower())
        if m_per:
            periodo = p
            t = (t[:m_per.start()] + t[m_per.end():]).strip()
            break
    low = t.lower()
    stat, span = None, None
    for patron, s in PATRONES_STAT:
        m = re.search(patron, low)
        if m:
            stat, span = s, m.span()
            break
    if stat is None:
        raise ValueError("no reconozco la estadística (touchdowns, yardas por tierra, recepciones...)")
    cuota = None
    m_cuota = re.search(r"(?:@|\bcuota|\ba)\s*([+-]\d{3,4}|\d+\.\d+)\b", low)
    if m_cuota:
        v = m_cuota.group(1)
        if v.startswith(("+", "-")):
            a = float(v)
            cuota = round(1 + (a / 100 if a > 0 else 100 / -a), 3)
        elif float(v) > 1.01:
            cuota = float(v)
        low = low[:m_cuota.start()] + " " * (m_cuota.end() - m_cuota.start()) + low[m_cuota.end():]
    lado = "menos" if re.search(r"\b(menos|under|no anota|u\d)", low) else "más"
    line = None
    m = re.search(r"(?:m[aá]s de|menos de|over|under|o|u)\s*(\d+(?:\.\d)?)", low)
    if m:
        line = float(m.group(1))
    else:
        m = re.search(r"\+\s*(\d+)|(\d+)\s*\+|(\d+)\s*o m[aá]s|(\d+(?:\.\d)?)", low)
        if m:
            n = float(next(g for g in m.groups() if g))
            line = n - 0.5 if n == int(n) else n
    if line is None:
        line = 0.5   # "anota", "anytime TD", "primer TD"
    if stat in ("tds", "first_td", "last_td") and line >= 1 and line == int(line):
        line -= 0.5
    rival = None
    m = re.search(r"\b(?:vs\.?|contra|ante|frente a|v)\s+(?:los |las |the )?([a-zA-Z0-9 .]+)$", t, re.I)
    if m:
        rival = equipos.por_texto(m.group(1)) or equipos.por_texto(m.group(1).split()[0])
    # El nombre: lo que queda antes de la estadística sin números ni palabras de apuesta.
    resto = t[:span[0]] if span[0] > 2 else t[span[1]:]
    if m and m.start() < len(resto):
        resto = resto[:m.start()]
    palabras = [w for w in re.findall(r"[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ.'\-]*", resto) if clave_nombre(w) not in PALABRAS_RUIDO]
    if not palabras:
        raise ValueError("no encuentro el nombre del jugador")
    return Apuesta(texto, " ".join(palabras), stat, line, lado, rival, cuota, periodo)


def buscar_jugador(ctx: Contexto, nombre: str) -> list[str]:
    """ids de jugadores de ataque cuyo nombre se parece (nombre completo, apellido o abreviado)."""
    clave = clave_nombre(nombre)
    nombres = {}
    for pid, partidos in ctx.jugadores.items():
        n = (ctx.roster.get(pid) or {}).get("name") or partidos[0].get("name") or ""
        nombres[pid] = clave_nombre(n)
    exactos = [pid for pid, n in nombres.items() if n == clave]
    if exactos:
        return sorted(exactos, key=lambda p: -len(ctx.jugadores[p]))
    por_apellido = [pid for pid, n in nombres.items() if n.split("_")[-1] == clave.split("_")[-1]
                    and (len(clave.split("_")) == 1 or n.startswith(clave.split("_")[0][:1]))]
    if por_apellido:
        return sorted(por_apellido, key=lambda p: (-(ctx.jugadores[p][0]["season"]), -len(ctx.jugadores[p])))
    if "_" not in clave:
        # Solo el nombre de pila ("Saquon"): vale si en la temporada actual hay uno solo así.
        por_nombre = [pid for pid, n in nombres.items() if n.split("_")[0] == clave
                      and ctx.jugadores[pid][0]["season"] == ctx.temporada]
        if len(por_nombre) == 1:
            return por_nombre
    parecidos = difflib.get_close_matches(clave, list(nombres.values()), n=3, cutoff=0.75)
    return [pid for pid, n in nombres.items() if n in parecidos]


@dataclass
class Veredicto:
    apuesta: Apuesta
    evaluacion: Evaluacion
    analisis: AnalisisPartido
    narrativa: list[str] = field(default_factory=list)       # por qué la gente la juega
    veredicto: str = ""
    explicacion: str = ""
    cuota_minima: float | None = None
    linea_mercado: Evaluacion | None = None    # la misma apuesta en la línea que ofrecen las casas, si es otra


def narrativa(ctx: Contexto, e: Evaluacion, oferta: Oferta | None) -> list[str]:
    """Lo que hace atractiva la apuesta para el público, con datos (aunque no sea buena)."""
    partidos = ctx.jugadores.get(e.player_id, [])
    stat = "tds" if e.stat in ("first_td", "last_td") else e.stat
    line = 0.5 if e.stat in ("first_td", "last_td") else e.line
    out = []
    if not partidos:
        return out
    t = tendencias(ctx, partidos, stat, line, e.lado, e.opp)
    ult = partidos[0]
    v_ult = valor(ult, stat)
    nombre = NOMBRES.get(stat, stat)
    if (e.lado == "más" and v_ult > line) or (e.lado == "menos" and v_ult < line):
        out.append(f"Efecto último partido: hizo {v_ult:g} {nombre} contra {equipos.apodo(ult['opp'])} "
                   f"(semana {ult['week']}). Lo reciente pesa mucho en el público.")
    k5, n5 = t.aciertos_5
    if n5 and k5 >= 3:
        out.append(f"Racha: lo cumplió en {k5} de sus últimos {n5}.")
    temporada = [valor(p, stat) for p in partidos if p["season"] == ctx.temporada]
    if temporada and stat in ("tds", "rush_tds", "rec_tds", "pass_tds"):
        out.append(f"Volumen de anotaciones: {sum(temporada):g} {nombre} en {len(temporada)} partidos esta temporada.")
    if t.vs_rival:
        vs = [v for _, v in t.vs_rival]
        if max(vs) > line:
            out.append(f"Historial contra {equipos.apodo(e.opp)}: {', '.join(f'{v:g}' for v in vs)}.")
    if oferta and oferta.presion() > 0.02 and oferta.movimiento():
        out.append(f"El mercado se mueve a favor: {oferta.movimiento()} (entra dinero en este lado).")
    if stat == "tds" and e.pos == "RB":
        titular, principal, suplente = qb_del_partido(ctx, e.team)
        if suplente:
            out.append(f"Narrativa del QB suplente: con {_nombre(ctx, titular)} en lugar de {_nombre(ctx, principal)}, "
                       f"'se la van a dar al RB cerca de la meta'. Los datos la apoyan a medias: el RB1 recibe un 9% más "
                       f"de acarreos dentro de la 10, pero el equipo llega un 15% menos a la zona roja.")
    if e.stat == "tds" and e.line >= 1.5:
        out.append("Cuota alta y pago grande: las apuestas de múltiples TD atraen por el premio, no por la "
                   "probabilidad. Las casas cobran más margen en estos mercados.")
    if not out:
        out.append("Sin una narrativa clara en los datos recientes: es una apuesta de nombre o de intuición.")
    return out


def veredicto(e: Evaluacion, cuota_usuario: float | None = None) -> tuple[str, str, float | None]:
    """(veredicto corto, explicación, cuota mínima para que tenga valor)."""
    justa = cuota_justa(e.prob)
    minima = round(justa * 1.04, 2) if justa else None
    odd = cuota_usuario or e.odd
    if odd is None:
        return ("SIN CUOTA: solo vale si te pagan al menos la cuota mínima",
                f"Probabilidad del modelo {e.prob * 100:.1f}% → cuota justa {justa}. Con margen de seguridad, "
                f"juégala solo a {minima} o más.", minima)
    ev = e.prob * odd - 1
    if ev >= 0.08 and (e.edge is None or e.edge >= 0.03):
        v = "✅ BUENA APUESTA: la cuota paga bastante más de lo que vale"
    elif ev >= 0.03:
        v = "🟢 Valor pequeño: jugable con stake bajo"
    elif ev >= -0.03:
        v = "➖ Precio justo: no hay ventaja, es una moneda al aire con margen de la casa"
    elif ev >= -0.12:
        v = "🔴 NO: la cuota paga menos de lo que vale"
    else:
        v = "❌ NO, MUY MALA: el precio está muy por debajo de la probabilidad real"
    explicacion = (f"Probabilidad final {e.prob * 100:.1f}% (modelo {e.prob_modelo * 100:.1f}%"
                   f"{f', casa sin margen {e.prob_casa * 100:.1f}%' if e.prob_casa is not None else ''}) "
                   f"× cuota {odd:.2f} → valor esperado {ev * 100:+.1f}% por unidad. Cuota justa {justa}; "
                   f"mínima recomendable {minima}.")
    return v, explicacion, minima


def validar(ctx: Contexto, apuesta: Apuesta, analisis_por_juego: dict[str, AnalisisPartido],
            player_id: str) -> Veredicto:
    """Evalúa la apuesta con el análisis del próximo partido del jugador."""
    a = next((x for x in analisis_por_juego.values() if any(p.jugador.player_id == player_id
                                                            for p in x.proyecciones + x.defensores)), None)
    if a is None:
        a = next(iter(analisis_por_juego.values()), None)
        k = a and next((t for t in (a.game["home_team"], a.game["away_team"])
                        if (pateador(ctx, t) or ("",))[0] == player_id), None)
        if a is None or not k:
            raise ValueError("el jugador no tiene partido en la ventana analizada o está fuera (lesión/suspensión)")
        return _validar_pateador(ctx, apuesta, a, player_id, k)
    proy = next(p for p in a.proyecciones + a.defensores if p.jugador.player_id == player_id)
    oferta = None
    if a.mercado is not None:
        oferta = next((o for o in a.mercado.ofertas if o.player_id == player_id and o.stat == apuesta.stat
                       and o.periodo == apuesta.periodo and o.lado == apuesta.lado and o.line == apuesta.line), None)
    firsts = (primer_td(a.proyecciones) if apuesta.periodo == "game"
              else primer_td_periodo(ctx, a.proyecciones, apuesta.periodo))
    e = evaluar(ctx, proy, apuesta.stat, apuesta.line, apuesta.lado, oferta, p_first=firsts.get(player_id),
                game_id=a.game["game_id"], periodo=apuesta.periodo)
    if e is None:
        raise ValueError(f"el modelo no proyecta {NOMBRES.get(apuesta.stat, apuesta.stat)} para un "
                         f"{proy.jugador.pos}")
    if apuesta.cuota:
        e.odd, e.book = apuesta.cuota, "tu cuota"
        e.ev = e.prob * apuesta.cuota - 1
    alternativa = None
    if oferta is None and a.mercado is not None:
        # Las casas no tienen esa línea exacta: se evalúa también la más cercana que sí ofrecen.
        cercanas = [o for o in a.mercado.ofertas if o.player_id == player_id and o.stat == apuesta.stat
                    and o.periodo == apuesta.periodo and o.lado == apuesta.lado]
        if cercanas:
            o = min(cercanas, key=lambda o: abs(o.line - apuesta.line))
            alternativa = evaluar(ctx, proy, o.stat, o.line, o.lado, o, p_first=firsts.get(player_id),
                                  game_id=a.game["game_id"], periodo=o.periodo)
    v, expl, minima = veredicto(e, apuesta.cuota)
    return Veredicto(apuesta, e, a, narrativa(ctx, e, oferta), v, expl, minima, alternativa)


def _validar_pateador(ctx: Contexto, apuesta: Apuesta, a: AnalisisPartido, player_id: str, team: str) -> Veredicto:
    """Goles de campo, extras y puntos de un pateador: salen de la simulación del partido."""
    if apuesta.stat not in ("fg", "xp", "kick_pts") or a.simulacion is None:
        raise ValueError("para un pateador solo se evalúan goles de campo, puntos extra y puntos del pateador")
    lado_eq = "home" if team == a.game["home_team"] else "away"
    opp = a.game["away_team"] if lado_eq == "home" else a.game["home_team"]
    oferta = None
    if a.mercado is not None:
        oferta = next((o for o in a.mercado.ofertas if o.player_id == player_id and o.stat == apuesta.stat
                       and o.lado == apuesta.lado and o.line == apuesta.line), None)
    oferta = oferta or Oferta(player_id, "", None, apuesta.stat, apuesta.lado, apuesta.line)
    p_mod, mu = prob_pateador(a.simulacion, lado_eq, apuesta.stat, apuesta.line, apuesta.lado)
    nombre = (pateador(ctx, team) or ("", player_id))[1]
    sim = a.simulacion.medias[lado_eq]
    e = _evaluacion_simple(a.game, oferta, player_id, nombre, "K", team, opp, p_mod, mu, PESO_MERCADO,
                           [f"simulación del partido: {mu:.2f} de media; {equipos.apodo(team)} espera "
                            f"{sim['fg']:.2f} goles de campo y {sim['tds']:.2f} TD"])
    if apuesta.cuota:
        e.odd, e.book, e.ev = apuesta.cuota, "tu cuota", e.prob * apuesta.cuota - 1
    v, expl, minima = veredicto(e, apuesta.cuota)
    return Veredicto(apuesta, e, a, [], v, expl, minima)


def texto_veredicto(ctx: Contexto, v: Veredicto) -> str:
    e, a = v.evaluacion, v.analisis
    proy = next((p for p in a.proyecciones + a.defensores if p.jugador.player_id == e.player_id), None)
    if proy is None:          # pateador: evaluación de la simulación
        return texto_veredicto_equipo(e, a, v.apuesta.cuota)
    lineas = [f"## {e.etiqueta()}  ({e.team} vs {e.opp}, {a.game['gameday']})", ""]
    lineas.append(f"**Veredicto: {v.veredicto}**")
    lineas.append("")
    lineas.append(v.explicacion)
    if e.odd and e.book and e.book != "tu cuota":
        lineas.append(f"Mejor cuota encontrada: {e.odd:.2f} en {e.book}"
                      f"{f' (consenso {e.consenso:.2f})' if e.consenso else ''}.")
    alt = v.linea_mercado
    if alt is not None and alt.odd:
        v_alt, _, _ = veredicto(alt)
        lineas.append(f"Las casas tienen esta apuesta en {alt.line:g} (mejor cuota {alt.odd:.2f} en {alt.book}): ahí la "
                      f"probabilidad es {alt.prob * 100:.1f}% y el valor esperado {(alt.ev or 0) * 100:+.1f}% → "
                      f"{v_alt}.")
    lineas += ["", "### ¿Por qué la gente apuesta esto?"] + [f"- {x}" for x in v.narrativa]
    lineas += ["", "### ¿Qué dice la data?"]
    stat = "tds" if e.stat in ("first_td", "last_td") else e.stat
    if stat == "tds":
        lam = proy.lambdas["tds"]
        lineas.append(f"- TD esperados: {lam:.2f} ({proy.lambdas['rush_tds']:.2f} por tierra, "
                      f"{proy.lambdas['rec_tds']:.2f} por recepción) → P(anota) {p_al_menos(lam, 1) * 100:.0f}%, "
                      f"P(2+) {p_al_menos(lam, 2) * 100:.1f}%, P(3+) {p_al_menos(lam, 3) * 100:.1f}%")
        if proy.jugador.pos == "QB" and "pass_tds" in proy.medias:
            mas, _ = proy.prob("pass_tds", e.line)
            lineas.append(f"- Si te refieres a pases de TD: espera {proy.medias['pass_tds']:.2f}; "
                          f"P(más de {e.line:g} TD de pase) = {mas * 100:.0f}% (cuota justa {cuota_justa(mas)}). "
                          f"Para validarla escribe \"{proy.jugador.nombre} más de {e.line:g} TD de pase\".")
    else:
        lineas.append(f"- Proyección: {e.mu:.1f} {NOMBRES.get(stat, stat)} (línea {e.line:g})")
    if stat == "tds" and e.stat == "tds" and proy.jugador.pos in ("QB", "RB", "WR", "TE"):
        td = next((t for t in a.tds if t.player_id == e.player_id), None)
        lineas += ["", "### La lectura, paso a paso"]
        lineas += [f"{k}. {paso}" for k, paso in enumerate(lectura_td(ctx, proy, td.ofertas if td else {}), 1)]
    if e.razones.a_favor:
        lineas += ["", "**A favor:**"] + [f"- {x}" for x in e.razones.a_favor]
    if e.razones.en_contra:
        lineas += ["", "**En contra:**"] + [f"- {x}" for x in e.razones.en_contra]
    if e.razones.contexto:
        lineas += ["", "**Contexto:**"] + [f"- {x}" for x in e.razones.contexto]
    claves = a.claves.get(e.team, [])
    if claves:
        lineas += ["", f"### El enfrentamiento: ataque de {equipos.apodo(e.team)} contra defensa de "
                       f"{equipos.apodo(e.opp)}"] + [f"- {x}" for x in claves]
    return "\n".join(lineas)


# --- Apuestas de partido y de equipo --------------------------------------------------------------



@dataclass
class ApuestaEquipo:
    texto: str
    equipos: list[str]
    stat: str          # pts, tds, fg, primero, ultimo
    bet: str           # ml, sp, ou, ml3way
    periodo: str
    entidad: str       # abreviatura del equipo o 'ALL'
    lado: str
    line: float
    cuota: float | None = None


def interpretar_equipo(texto: str) -> ApuestaEquipo:
    """'Bills -3.5', 'Eagles ML', 'gana Dallas 1.ª mitad', 'más de 47.5 puntos Packers Panthers',
    'Bills más de 27.5 puntos', 'Bills anota primero', 'menos de 4.5 TD Bills Ravens'."""
    low = texto.lower()
    cuota = None
    m_cuota = re.search(r"(?:@|\bcuota|\ba)\s*([+-]\d{3,4}|\d+\.\d+)\s*$", low)
    if m_cuota:
        v = m_cuota.group(1)
        cuota = round(1 + (float(v) / 100 if float(v) > 0 else 100 / -float(v)), 3) if v[0] in "+-" else float(v)
        low = low[:m_cuota.start()]
    periodo = next((p for patron, p in PERIODOS_TEXTO if re.search(patron, low)), "game")
    for patron, _ in PERIODOS_TEXTO:
        low = re.sub(patron, " ", low)
    encontrados = []
    palabras = re.findall(r"[a-záéíóúñ0-9]+", low)
    i = 0
    while i < len(palabras):
        # Primero tres y dos palabras ("new york jets", "green bay"), luego una.
        for n in (3, 2, 1):
            t = equipos.por_texto(" ".join(palabras[i:i + n])) if i + n <= len(palabras) else None
            if t and not palabras[i].isdigit():
                if t not in encontrados:
                    encontrados.append(t)
                i += n
                break
        else:
            i += 1
    if not encontrados:
        raise ValueError("no reconozco ningún equipo")
    principal = encontrados[0]
    stat = "tds" if re.search(r"\btds?\b|touchdowns?", low) else "fg" if re.search(r"goles? de campo|\bfg\b", low) \
        else "pts"
    if re.search(r"anota(?:n|r[aá]n?)? primero|primero en anotar|first to score", low):
        return ApuestaEquipo(texto, encontrados, "primero", "ml", periodo, principal, "", 0.0, cuota)
    if re.search(r"anota(?:n|r[aá]n?)? [uú]ltimo|last to score", low):
        return ApuestaEquipo(texto, encontrados, "ultimo", "ml", periodo, principal, "", 0.0, cuota)
    m = re.search(r"(m[aá]s|menos|over|under|o|u)\s*(?:de\s*)?(\d+(?:\.\d)?)", low)
    if m:
        lado = "menos" if m.group(1) in ("menos", "under", "u") else "más"
        total = len(encontrados) >= 2 or re.search(r"\btotal\b|partido|juego", low)
        return ApuestaEquipo(texto, encontrados, stat, "ou", periodo, "ALL" if total else principal, lado,
                             float(m.group(2)), cuota)
    m = re.search(r"(?<![\w.])([+-]\d+(?:\.\d)?)\b", low)
    if m:
        return ApuestaEquipo(texto, encontrados, "pts", "sp", periodo, principal, "", float(m.group(1)), cuota)
    if re.search(r"\bml\b|moneyline|gana|ganar[aá]n?|victoria|\bwin", low):
        return ApuestaEquipo(texto, encontrados, "pts", "ml", periodo, principal, "", 0.0, cuota)
    raise ValueError("no reconozco el mercado (spread, ML, total, anota primero...)")


def oferta_equipo(ap: ApuestaEquipo, home: str, away: str, mercado) -> Oferta:
    """La oferta de las casas que corresponde a la apuesta (o una sin precio para evaluar solo el modelo)."""
    entidad = "all" if ap.entidad == "ALL" else ("home" if ap.entidad == home else "away")
    lado = ap.lado or entidad
    if mercado is not None:
        cands = [o for o in mercado.ofertas if o.tipo == "equipo" and o.stat == ap.stat and o.bet == ap.bet
                 and o.periodo == ap.periodo and o.lado == lado
                 and (ap.bet in ("ml", "sp") or o.sgo_player_id == entidad)]
        if ap.bet in ("sp", "ou"):
            exactas = [o for o in cands if o.line == ap.line]
            if exactas:
                return exactas[0]
        elif cands:
            return cands[0]
    return Oferta(entidad, equipos.nombre(ap.entidad) if ap.entidad != "ALL" else "Partido", None, ap.stat, lado,
                  ap.line, tipo="equipo", periodo=ap.periodo, bet=ap.bet)


def texto_veredicto_equipo(e: Evaluacion, a: AnalisisPartido, cuota: float | None) -> str:
    v, expl, _ = veredicto(e, cuota)
    L = [f"## {e.etiqueta()}  ({a.titulo}, {a.game['gameday']})", "", f"**Veredicto: {v}**", "", expl]
    if e.odd and e.book and not cuota:
        L.append(f"Mejor cuota encontrada: {e.odd:.2f} en {e.book}.")
    elif not e.odd and not cuota:
        L.append("Las casas no ofrecen esta línea exacta ahora mismo.")
    if a.simulacion:
        sim = a.simulacion
        L += ["", "### ¿Qué dice la simulación?", f"- {sim.n} partidos simulados posesión a posesión."]
    for titulo, lista in (("A favor", e.razones.a_favor), ("En contra", e.razones.en_contra),
                          ("Contexto", e.razones.contexto)):
        if lista:
            L += ["", f"**{titulo}:**"] + [f"- {x}" for x in lista]
    for team, claves in a.claves.items():
        L += ["", f"### Ataque de {equipos.apodo(team)} contra la defensa de "
                  f"{equipos.apodo(a.entornos[team].opp)}"] + [f"- {c}" for c in claves[:8]]
    return "\n".join(L)
