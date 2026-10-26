"""El "¿por qué?" de cada apuesta: tendencias del jugador, el enfrentamiento y lo que dice el mercado.

Cada razón se clasifica a favor o en contra del lado elegido. Las razones salen de los Factor del modelo (cada
ajuste con su efecto), de las tendencias del jugador (acierto sobre esa línea, contra este rival, como local o
visitante, como favorito o no, contra defensas fuertes o débiles en lo que mide la apuesta) y del movimiento de
la línea.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

from . import equipos
from .mercado import Oferta
from .modelo import NOMBRES, Contexto, Proyeccion, rango, valor

# Métrica defensiva que mide a un rival para cada estadística: (lado, métrica, sentido).
# sentido 1 = un valor alto de la métrica es una defensa débil (concede mucho).
METRICA_RIVAL = {
    "rush_yds": ("defensa", "rush_epa"), "rush_att": ("defensa", "rush_epa"), "rush_tds": ("defensa", "rush_tds"),
    "rec": ("defensa", "pass_epa"), "rec_yds": ("defensa", "pass_epa"), "targets": ("defensa", "pass_epa"),
    "rec_tds": ("defensa", "pass_tds"), "pass_yds": ("defensa", "pass_epa"), "pass_tds": ("defensa", "pass_tds"),
    "pass_att": ("defensa", "pass_epa"), "comp": ("defensa", "pass_epa"), "ints": ("defensa", "turnovers"),
    "rush_rec_yds": ("defensa", "epa_play"), "pass_rush_yds": ("defensa", "epa_play"), "tds": ("defensa", "off_tds"),
    "long_rec": ("defensa", "explosive"), "long_rush": ("defensa", "explosive"),
}


@dataclass
class Tendencias:
    ultimos: list[float]
    aciertos_5: tuple[int, int]
    aciertos_10: tuple[int, int]
    aciertos_temporada: tuple[int, int]
    vs_rival: list[tuple[str, float]]
    local: float | None
    visitante: float | None
    favorito: float | None
    no_favorito: float | None
    por_nivel: dict[str, tuple[float, int]] = field(default_factory=dict)   # 'débiles' / 'medias' / 'fuertes'
    racha: int = 0              # partidos seguidos pasando la línea (negativo: fallando)


def _media(xs: list[float]) -> float | None:
    return sum(xs) / len(xs) if xs else None


def tendencias(ctx: Contexto, partidos: list[dict], stat: str, line: float, lado: str, opp: str) -> Tendencias:
    def pasa(v: float) -> bool:
        return v > line if lado == "más" else v < line

    vals = [valor(p, stat) for p in partidos]
    temporada = [valor(p, stat) for p in partidos if p["season"] == ctx.temporada]
    racha = 0
    if vals:
        primero = pasa(vals[0])
        for v in vals:
            if pasa(v) != primero:
                break
            racha += 1
        racha = racha if primero else -racha
    t = Tendencias(
        vals[:5], (sum(map(pasa, vals[:5])), len(vals[:5])), (sum(map(pasa, vals[:10])), len(vals[:10])),
        (sum(map(pasa, temporada)), len(temporada)),
        [(f"{p['season']} sem. {p['week']}", valor(p, stat)) for p in partidos if p["opp"] == opp][:6],
        _media([valor(p, stat) for p in partidos[:16] if p["is_home"]]),
        _media([valor(p, stat) for p in partidos[:16] if not p["is_home"]]),
        _media([valor(p, stat) for p in partidos[:16] if (p.get("spread_equipo") or 0) > 0]),
        _media([valor(p, stat) for p in partidos[:16] if (p.get("spread_equipo") or 0) < 0]),
        racha=racha)
    lado_m, metrica = METRICA_RIVAL.get(stat, ("defensa", "epa_play"))
    niveles: dict[str, list[float]] = {"débiles": [], "medias": [], "fuertes": []}
    for p in partidos[:24]:
        r = rango(ctx, lado_m, metrica, p["opp"])
        if not r:
            continue
        i, n = r
        nivel = "débiles" if i <= n / 3 else ("fuertes" if i > 2 * n / 3 else "medias")
        niveles[nivel].append(valor(p, stat))
    t.por_nivel = {k: (sum(v) / len(v), len(v)) for k, v in niveles.items() if v}
    return t


def nivel_rival(ctx: Contexto, stat: str, opp: str) -> str | None:
    lado_m, metrica = METRICA_RIVAL.get(stat, ("defensa", "epa_play"))
    r = rango(ctx, lado_m, metrica, opp)
    if not r:
        return None
    i, n = r
    return "débiles" if i <= n / 3 else ("fuertes" if i > 2 * n / 3 else "medias")


@dataclass
class Razones:
    a_favor: list[str]
    en_contra: list[str]
    contexto: list[str]


def _fmt(v: float) -> str:
    return f"{v:.0f}" if abs(v) >= 10 else f"{v:.1f}"


def razones(ctx: Contexto, proy: Proyeccion, stat: str, line: float, lado: str, oferta: Oferta | None = None,
            prob_modelo: float | None = None, prob_casa: float | None = None) -> Razones:
    j, ent = proy.jugador, proy.entorno
    favor, contra, contexto = [], [], []
    stat_m = "tds" if stat in ("first_td", "last_td") else stat
    signo = 1 if lado == "más" else -1
    nombre_opp = equipos.apodo(ent.opp)
    # 1. Ajustes del modelo: los multiplicadores a favor o en contra; los datos, como contexto.
    for f in sorted(proy.factores.get(stat_m, []), key=lambda f: -abs(math.log(f.efecto)) if f.efecto else 0):
        if f.efecto is None or abs(f.efecto - 1) < 0.02:
            if f.texto not in contexto:
                contexto.append(f.texto)
        elif (f.efecto > 1) == (signo > 0):
            favor.append(f"{f.texto} ({(f.efecto - 1) * 100:+.0f}%)")
        else:
            contra.append(f"{f.texto} ({(f.efecto - 1) * 100:+.0f}%)")
    # 2. Tendencias del jugador sobre esta misma línea.
    stat_t = "tds" if stat in ("first_td", "last_td") else stat
    line_t = 0.5 if stat in ("first_td", "last_td") else line
    t = tendencias(ctx, j.partidos, stat_t, line_t, lado, ent.opp)
    nombre = NOMBRES.get(stat_t, stat_t)
    k5, n5 = t.aciertos_5
    k10, n10 = t.aciertos_10
    kt, nt = t.aciertos_temporada
    if n10 >= 3:
        texto = (f"pasó {lado} de {line_t:g} {nombre} en {k5} de sus últimos {n5} y {k10} de {n10} "
                 f"(esta temporada {kt}/{nt}); últimos: {', '.join(_fmt(v) for v in t.ultimos)}")
        (favor if k10 / n10 >= 0.6 else contra if k10 / n10 <= 0.4 else contexto).append(texto)
    if abs(t.racha) >= 3:
        (favor if t.racha > 0 else contra).append(
            f"racha: {abs(t.racha)} partidos seguidos {'pasando' if t.racha > 0 else 'sin pasar'} esta línea")
    if t.vs_rival:
        vs = [v for _, v in t.vs_rival]
        k = sum((v > line_t) if lado == "más" else (v < line_t) for v in vs)
        texto = f"contra {nombre_opp}: {', '.join(_fmt(v) for v in vs)} ({k}/{len(vs)} pasando la línea)"
        (favor if k / len(vs) >= 0.6 else contra if k / len(vs) <= 0.4 else contexto).append(texto)
    nivel = nivel_rival(ctx, stat_t, ent.opp)
    if nivel and nivel in t.por_nivel and len(t.por_nivel) >= 2:
        m_nivel, n_nivel = t.por_nivel[nivel]
        resto = [(m, n) for k, (m, n) in t.por_nivel.items() if k != nivel]
        m_resto = sum(m * n for m, n in resto) / sum(n for _, n in resto)
        if n_nivel >= 2 and m_resto > 0 and abs(m_nivel / m_resto - 1) >= 0.12:
            texto = (f"{nombre_opp} es de las defensas {nivel} en lo que mide esta apuesta; contra ese tipo de "
                     f"defensa promedia {_fmt(m_nivel)} ({n_nivel} partidos) frente a {_fmt(m_resto)} contra el resto")
            ((favor if (m_nivel > m_resto) == (signo > 0) else contra)).append(texto)
    lv = t.local if ent.local else t.visitante
    otro = t.visitante if ent.local else t.local
    if lv is not None and otro and abs(lv / otro - 1) >= 0.2:
        texto = f"como {'local' if ent.local else 'visitante'} promedia {_fmt(lv)} (frente a {_fmt(otro)})"
        ((favor if (lv > otro) == (signo > 0) else contra)).append(texto)
    # 3. El mercado.
    if oferta is not None:
        mov = oferta.movimiento()
        presion = oferta.presion()
        if mov:
            if presion > 0.02:
                favor.append(f"el mercado empuja este lado: {mov}")
            elif presion < -0.02:
                contra.append(f"el mercado se mueve en contra: {mov}")
            else:
                contexto.append(f"mercado: {mov}")
        book, odd = oferta.mejor
        if odd and oferta.consenso and odd > oferta.consenso * 1.04 and book:
            favor.append(f"mejor precio en {book}: {odd:.2f} frente a {oferta.consenso:.2f} de consenso")
    if prob_modelo is not None and prob_casa is not None:
        dif = prob_modelo - prob_casa
        if dif >= 0.04:
            favor.append(f"el modelo le da {prob_modelo * 100:.0f}% y la casa {prob_casa * 100:.0f}%: "
                         f"la cuota paga más de lo que vale")
        elif dif <= -0.04:
            contra.append(f"la casa le da {prob_casa * 100:.0f}% y el modelo solo {prob_modelo * 100:.0f}%")
        if abs(dif) > 0.15:
            contra.append("modelo y casa discrepan mucho: suele significar que la casa sabe algo que los datos aún "
                          "no reflejan (rol, lesión, quién vuelve); la probabilidad final se apoya más en la casa")
    if j.n < 6:
        contra.append(f"muestra corta: {j.n} partidos en la base")
    return Razones(favor, contra, contexto)


def frase_principal(r: Razones, n: int = 2) -> str:
    """Las 1-2 razones más fuertes a favor, para una línea de resumen."""
    return "; ".join(r.a_favor[:n]) if r.a_favor else (r.contexto[0] if r.contexto else "")
