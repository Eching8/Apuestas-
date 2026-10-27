"""El enfrentamiento en la zona roja, posición por posición.

Tres preguntas para cada ataque contra cada defensa:

1. **¿Dónde se le anota a esta defensa en la zona roja?** Por posición (carreras del QB, RB, WR, TE): cuántas
   oportunidades concede dentro de la 20 por partido y qué parte termina en TD, frente a la media de la liga
   (contraído hacia la liga con 15 oportunidades virtuales).
2. **¿Cómo reparte este ataque la zona roja?** Quién se lleva los acarreos dentro de la 20 y de la 10, quién es el
   blanco principal en la zona roja y quién recibe los envíos a la zona de anotación (el que "está abierto" cuando
   se lanza al end zone), y cómo convierte cada uno frente a la media de su posición.
3. **¿Quién tiene más probabilidad de anotar ahí?** Oportunidades esperadas en la zona roja de cada jugador ×
   lo que la defensa deja convertir a su posición × su propia eficiencia, y la probabilidad de recibir 2 o más
   envíos en la zona roja (la puerta a los 2+ TD).
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

from . import equipos
from .modelo import DECAY_EQUIPO, POSICIONES, Contexto, Entorno, Factor, Proyeccion, _pesos, texto_rango

K_DEFENSA = 15.0       # oportunidades "virtuales" con la tasa de la liga en la defensa por posición
K_JUGADOR = 20.0       # ídem para la eficiencia del jugador
NOMBRE_POS = {"QB": "QB (carreras)", "RB": "RB", "WR": "WR", "TE": "TE"}


@dataclass
class DefensaPosicion:
    pos: str
    acarreos: float           # por partido dentro de la 20
    envios: float
    tds: float                # TD en la zona roja por partido
    tasa_carrera: float       # TD por acarreo en la zona roja (contraído)
    tasa_envio: float         # TD por envío en la zona roja (contraído)
    liga_tds: float
    liga_carrera: float
    liga_envio: float
    rango_tds: tuple[int, int] | None

    @property
    def ratio(self) -> float:
        return self.tds / self.liga_tds if self.liga_tds else 1.0


@dataclass
class JugadorRZ:
    proy: Proyeccion
    acarreos_rz: float        # esperados hoy
    envios_rz: float
    envios_ez: float
    tds_rz: float             # TD esperados en la zona roja
    p_2_envios: float         # P(2+ envíos en la zona roja)
    conversion: float | None  # TD por oportunidad en la zona roja (su historial)
    conversion_liga: float
    oportunidades_hist: float
    notas: list[str] = field(default_factory=list)


def _tasa(td: float, opp: float, liga: float, k: float) -> float:
    return (td + k * liga) / (opp + k) if opp + k > 0 else liga


def defensa_rz(ctx: Contexto, opp: str) -> dict[str, DefensaPosicion]:
    pd, lg = ctx.perfiles[opp].pos_defensa, ctx.liga_pos
    n = pd.get("_n", 0) + 3.0
    out = {}
    for g in POSICIONES:
        car, env = pd.get(f"{g}.rz_carries", 0), pd.get(f"{g}.rz_targets", 0)
        t_car, t_env = pd.get(f"{g}.rz_rush_tds", 0), pd.get(f"{g}.rz_rec_tds", 0)
        l_car, l_env = lg.get(f"{g}.rz_carries", 0), lg.get(f"{g}.rz_targets", 0)
        lt_car, lt_env = lg.get(f"{g}.rz_rush_tds", 0), lg.get(f"{g}.rz_rec_tds", 0)
        liga_carrera = lt_car / l_car if l_car else 0.0
        liga_envio = lt_env / l_env if l_env else 0.0
        # Totales de la temporada (no por partido) para contraer con oportunidades reales.
        tasa_c = _tasa(t_car * n, car * n, liga_carrera, K_DEFENSA)
        tasa_e = _tasa(t_env * n, env * n, liga_envio, K_DEFENSA)
        out[g] = DefensaPosicion(g, car, env, t_car + t_env, tasa_c, tasa_e, lt_car + lt_env, liga_carrera, liga_envio,
                                 _rango_suma(ctx, opp, g))
    return out


def _rango_suma(ctx: Contexto, opp: str, g: str) -> tuple[int, int] | None:
    """Puesto de la defensa en TD concedidos a la posición en la zona roja (1 = la que más concede)."""
    vals = sorted(((p.pos_defensa.get(f"{g}.rz_rush_tds", 0) + p.pos_defensa.get(f"{g}.rz_rec_tds", 0), t)
                   for t, p in ctx.perfiles.items() if any(f["season"] == ctx.temporada for f in ctx.ofensiva.get(t, []))),
                  reverse=True)
    for i, (_, t) in enumerate(vals):
        if t == opp:
            return i + 1, len(vals)
    return None


def _promedio_equipo(ctx: Contexto, filas: list[dict], equipo_de: str, clave: str) -> float:
    """Media ponderada por partido de una suma de zona roja (de los jugadores de `equipo_de` en esos partidos)."""
    pesos = _pesos(filas, ctx.temporada, DECAY_EQUIPO)
    sw = sum(pesos)
    if not sw:
        return 0.0
    return sum(w * (ctx.equipo_pbp.get((f["game_id"], f[equipo_de]), {}).get(clave, 0)) for f, w in zip(filas, pesos)) / sw


def oportunidades_equipo(ctx: Contexto, team: str, opp: str) -> dict[str, float]:
    """Acarreos, envíos y envíos a la zona de anotación esperados del equipo dentro de la 20."""
    out = {}
    for clave in ("rz_carries", "rz_targets", "ez_targets"):
        propio = _promedio_equipo(ctx, ctx.ofensiva.get(team, []), "team", clave)
        concede = _promedio_equipo(ctx, ctx.defensa.get(opp, []), "team", clave)
        filas = [f for fs in ctx.ofensiva.values() for f in fs if f["season"] >= ctx.temporada - 1]
        liga = sum(ctx.equipo_pbp.get((f["game_id"], f["team"]), {}).get(clave, 0) for f in filas) / max(len(filas), 1)
        out[clave] = math.sqrt(propio * concede) if propio and concede else propio or liga
        out[f"{clave}_liga"] = liga
    return out


def _conversion(proy: Proyeccion) -> tuple[float, float]:
    """(TD en la zona roja, oportunidades en la zona roja) en sus últimos 16 partidos."""
    partidos = proy.jugador.partidos[:16]
    td = sum((p.get("rz_rush_tds") or 0) + (p.get("rz_rec_tds") or 0) for p in partidos)
    op = sum((p.get("rz_carries") or 0) + (p.get("rz_targets") or 0) for p in partidos)
    return td, op


def candidatos(ctx: Contexto, ent: Entorno, proys: list[Proyeccion]) -> list[JugadorRZ]:
    """Quién tiene más TD esperados en la zona roja hoy, de cualquier posición."""
    defensa = defensa_rz(ctx, ent.opp)
    opp_eq = oportunidades_equipo(ctx, ent.team, ent.opp)
    out = []
    for p in proys:
        if p.jugador.team != ent.team or p.jugador.pos not in POSICIONES:
            continue
        sh, d = p.jugador.shares, defensa[p.jugador.pos]
        car = sh.get("rz_carries", 0) * opp_eq["rz_carries"]
        env = sh.get("rz_targets", 0) * opp_eq["rz_targets"]
        ez = sh.get("ez_targets", 0) * opp_eq["ez_targets"]
        if car + env < 0.15:
            continue
        td_h, op_h = _conversion(p)
        liga_conv = ((d.liga_carrera * car + d.liga_envio * env) / (car + env)) if car + env else 0
        propia = _tasa(td_h, op_h, liga_conv, K_JUGADOR)
        habilidad = propia / liga_conv if liga_conv else 1.0
        tds = (car * d.tasa_carrera + env * d.tasa_envio) * habilidad
        p2 = 1 - math.exp(-env) * (1 + env)
        out.append(JugadorRZ(p, car, env, ez, tds, p2, td_h / op_h if op_h else None, liga_conv, op_h))
    return sorted(out, key=lambda c: -c.tds_rz)


def mapa(ctx: Contexto, ent: Entorno, proys: list[Proyeccion], top: int = 5) -> list[str]:
    """El enfrentamiento en la zona roja en frases: dónde atacar, cómo reparte el ataque y quién es el candidato."""
    yo, rival = equipos.apodo(ent.team), equipos.apodo(ent.opp)
    defensa = defensa_rz(ctx, ent.opp)
    lineas = []
    debiles = sorted(defensa.values(), key=lambda d: -d.ratio)
    partes = []
    for d in debiles:
        if d.liga_tds < 0.05:
            continue
        etiqueta = "débil" if d.ratio >= 1.2 else "fuerte" if d.ratio <= 0.8 else "normal"
        partes.append(f"{NOMBRE_POS[d.pos]} {d.tds:.2f} TD por partido (liga {d.liga_tds:.2f}, "
                      f"{texto_rango(d.rango_tds, 'más concede', 'menos concede')}: {etiqueta})")
    lineas.append(f"Dónde se le anota a {rival} en la zona roja: " + "; ".join(partes) + ".")
    peor = debiles[0]
    if peor.ratio >= 1.15:
        tasa = peor.tasa_envio if peor.pos in ("WR", "TE") else peor.tasa_carrera
        liga = peor.liga_envio if peor.pos in ("WR", "TE") else peor.liga_carrera
        via = "por envío" if peor.pos in ("WR", "TE") else "por acarreo"
        lineas.append(f"Su punto débil: los {NOMBRE_POS[peor.pos]}. Les concede {peor.tds / peor.liga_tds:.1f} veces los TD "
                      f"de la media en la zona roja y les deja convertir el {tasa * 100:.0f}% {via} "
                      f"(liga {liga * 100:.0f}%).")
    cands = candidatos(ctx, ent, proys)
    opp_eq = oportunidades_equipo(ctx, ent.team, ent.opp)
    lineas.append(f"Cómo reparte {yo} la zona roja (hoy se esperan {opp_eq['rz_carries']:.1f} acarreos y "
                  f"{opp_eq['rz_targets']:.1f} envíos dentro de la 20, {opp_eq['ez_targets']:.1f} a la zona de anotación):")
    por_envios = sorted(cands, key=lambda c: -c.envios_rz)
    principal = por_envios[0] if por_envios and por_envios[0].envios_rz > 0.3 else None
    abierto = max(cands, key=lambda c: c.envios_ez, default=None)
    for c in cands[:top]:
        j = c.proy.jugador
        papel = []
        if c.acarreos_rz >= 0.3:
            papel.append(f"{j.shares.get('rz_carries', 0) * 100:.0f}% de los acarreos en la zona roja "
                         f"({j.shares.get('i10_carries', 0) * 100:.0f}% dentro de la 10)")
        if c.envios_rz >= 0.2:
            papel.append(f"{j.shares.get('rz_targets', 0) * 100:.0f}% de los envíos en la zona roja")
        if c.envios_ez >= 0.15:
            papel.append(f"{j.shares.get('ez_targets', 0) * 100:.0f}% de los envíos a la zona de anotación")
        etiquetas = []
        if principal is not None and c is principal:
            etiquetas.append("blanco principal en la zona roja")
        if abierto is not None and c is abierto and c.envios_ez >= 0.2:
            etiquetas.append("el más buscado en la zona de anotación")
        conv = (f"; convierte {c.conversion * 100:.0f}% de sus oportunidades en la zona roja "
                f"({c.oportunidades_hist:g} en 16 partidos; media de su perfil {c.conversion_liga * 100:.0f}%)"
                if c.conversion is not None and c.oportunidades_hist >= 5 else "")
        lineas.append(f"- {j.nombre} ({j.pos}){' — ' + ', '.join(etiquetas) if etiquetas else ''}: "
                      f"{', '.join(papel) or 'papel menor'}{conv}. TD esperados en la zona roja: {c.tds_rz:.2f}; "
                      f"P(2+ envíos en la zona roja) {c.p_2_envios * 100:.0f}%.")
    if cands:
        mejor = cands[0]
        lineas.append(f"Candidato principal en la zona roja: {mejor.proy.jugador.nombre} ({mejor.proy.jugador.pos}), "
                      f"{mejor.tds_rz:.2f} TD esperados ahí.")
    return lineas


# Parte de los TD de cada posición que se anotan en jugadas que empiezan dentro de la 20 (para pasar de "TD en la
# zona roja" a TD totales). Se calcula de los datos de la liga al construir el contexto.
def parte_rz(ctx: Contexto, pos: str) -> float:
    clave = f"_parte_rz_{pos}"
    if clave not in ctx.periodos:
        rz = tot = 0.0
        for partidos in ctx.jugadores.values():
            for p in partidos:
                if p["season"] < ctx.temporada - 1 or (p.get("position") or "") not in (
                        (pos,) if pos != "RB" else ("RB", "FB")):
                    continue
                rz += (p.get("rz_rush_tds") or 0) + (p.get("rz_rec_tds") or 0)
                tot += (p.get("rushing_tds") or 0) + (p.get("receiving_tds") or 0)
        ctx.periodos[clave] = rz / tot if tot else 0.75
    return ctx.periodos[clave]


# Peso de la vía "zona roja" en los TD esperados (el resto, el modelo de cuotas de TD). Backtest de 2025 (Brier de
# anotar): 0 → 0.14657, 0.3 → 0.14643, 0.5 → 0.14663, 0.7 → 0.14705. Con más peso, el ruido de pocas jugadas por
# defensa y posición pesa más que la señal.
PESO_RZ = 0.3


def ajustar_tds(ctx: Contexto, ent: Entorno, proys: list[Proyeccion], peso: float = PESO_RZ) -> None:
    """Mezcla los TD esperados del modelo con los de la zona roja (oportunidades × lo que la defensa deja convertir a
    su posición × su eficiencia), pasados a TD totales con la parte de los TD de su posición que llegan desde ahí."""
    if peso <= 0:
        return
    for c in candidatos(ctx, ent, proys):
        p = c.proy
        lam = p.lambdas.get("tds", 0)
        if lam <= 0 or p.jugador.pos == "QB" and c.acarreos_rz < 0.3:
            continue
        via_rz = c.tds_rz / max(parte_rz(ctx, p.jugador.pos), 0.3)
        nuevo = (1 - peso) * lam + peso * via_rz
        f = nuevo / lam
        p.lambdas = {k: v * f for k, v in p.lambdas.items()}
        p.medias.update({k: p.medias[k] * f for k in ("tds", "rush_tds", "rec_tds") if k in p.medias})
        p.varianzas.update({k: p.medias[k] + 0.08 * p.medias[k] ** 2 for k in ("tds", "rush_tds", "rec_tds")
                            if k in p.medias})
        if f > 1.05 or f < 0.95:
            p.factores.setdefault("tds", []).append(Factor(
                f"zona roja: {c.tds_rz:.2f} TD esperados ahí contra {equipos.apodo(ent.opp)} (oportunidades × lo que "
                f"concede a los {p.jugador.pos} en la zona roja × su eficiencia)", f, "rival"))


def cruces(ctx: Contexto, ent: Entorno, proys: list[Proyeccion], ratio_min: float = 1.2) -> list[dict]:
    """Los cruces a explotar: posiciones contra las que la defensa rival es débil en la zona roja y el jugador del
    ataque que las ocupa (el que más TD esperados tiene ahí en esa posición)."""
    defensa = defensa_rz(ctx, ent.opp)
    cands = candidatos(ctx, ent, proys)
    out = []
    for pos, d in defensa.items():
        if d.liga_tds < 0.05 or d.ratio < ratio_min:
            continue
        mejor = next((c for c in cands if c.proy.jugador.pos == pos), None)
        if mejor is None or mejor.tds_rz < 0.1:
            continue
        out.append({"team": ent.team, "opp": ent.opp, "pos": pos, "ratio": d.ratio, "tds_def": d.tds,
                    "liga": d.liga_tds, "rango": d.rango_tds, "jugador": mejor})
    return out
