"""Props de defensores (sacks, tacleadas, intercepciones) y quién es el pateador de cada equipo.

Tacleadas: su media por partido (con más peso a lo reciente, contraída hacia su posición) × cuántas jugadas se
espera que haga el ataque rival frente a las que suele enfrentar su defensa × el tipo de jugadas (los LB y la
línea taclean más contra equipos de carrera; los DB, contra equipos de pase).
Sacks: su media × qué tanto deja que capturen a su QB el ataque rival × los dropbacks esperados del rival.
Intercepciones: su media × qué tanto pierde el balón el rival × los dropbacks esperados.
"""
from __future__ import annotations

import math
from collections import defaultdict
from dataclasses import replace

from . import equipos
from .modelo import (CV_DEFECTO, DECAY_JUGADOR, Contexto, Entorno, Factor, Jugador, Proyeccion, _equipo_actual,
                     _pesos, disponible, texto_rango, rango, valor)

GRUPOS_DEF = {"DE": "DL", "DT": "DL", "NT": "DL", "DL": "DL", "EDGE": "DL", "LB": "LB", "ILB": "LB", "OLB": "LB",
              "MLB": "LB", "CB": "DB", "S": "DB", "FS": "DB", "SS": "DB", "DB": "DB", "SAF": "DB"}
STATS_DEF = ("tackles", "solo", "asist", "sacks", "def_ints")
K_POSICION = 2.0     # partidos "virtuales" con la media de su posición


def grupo_def(pos: str | None) -> str | None:
    return GRUPOS_DEF.get((pos or "").upper())


def _medias_posicion(ctx: Contexto) -> dict[str, dict[str, float]]:
    """Media por partido de cada estadística defensiva por grupo (entre quienes registraron algo)."""
    if "_def" in ctx.periodos:
        return ctx.periodos["_def"]
    sumas: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
    n: dict[str, int] = defaultdict(int)
    for partidos in ctx.jugadores.values():
        for p in partidos:
            g = grupo_def(p.get("position"))
            if not g or p["season"] != ctx.temporada and p["season"] != ctx.temporada - 1:
                continue
            if valor(p, "tackles") + valor(p, "sacks") == 0:
                continue
            n[g] += 1
            for s in STATS_DEF:
                sumas[g][s] += valor(p, s)
    ctx.periodos["_def"] = {g: {s: v / n[g] for s, v in d.items()} for g, d in sumas.items()}
    return ctx.periodos["_def"]


def candidatos_defensa(ctx: Contexto, team: str, ultimos: int = 3) -> list[Jugador]:
    juegos = {f["game_id"] for f in ctx.defensa.get(team, [])[:ultimos]}
    out = []
    for pid, partidos in ctx.jugadores.items():
        pos = (ctx.roster.get(pid) or {}).get("position") or partidos[0].get("position")
        g = grupo_def(pos)
        if not g or _equipo_actual(ctx, pid, partidos) != team:
            continue
        if not any(p["game_id"] in juegos for p in partidos[:ultimos + 2]):
            continue
        juega, estado, detalle = disponible(ctx, pid)
        if not juega:
            continue
        con_equipo = [p for p in partidos if p["team"] == team]
        out.append(Jugador(pid, partidos[0].get("name") or pid, g, team, partidos, con_equipo, estado, detalle))
    return out


def proyectar_defensa(ctx: Contexto, j: Jugador, ataque_rival: Entorno) -> Proyeccion:
    """ataque_rival: el entorno del equipo rival atacando contra la defensa de este jugador."""
    medias_pos = _medias_posicion(ctx).get(j.pos, {})
    partidos = (j.con_equipo if len(j.con_equipo) >= 3 else j.partidos)[:12]
    pesos = _pesos(partidos, ctx.temporada, DECAY_JUGADOR)
    sw = sum(pesos)
    rival = equipos.apodo(ataque_rival.team)
    lg = ctx.liga
    defensa = ctx.perfiles[j.team].defensa
    jugadas = ataque_rival.dropbacks + ataque_rival.carries
    f_jugadas = jugadas / max(defensa.get("plays") or lg["plays"], 1)
    carrera = ataque_rival.carries / max(jugadas, 1)
    carrera_lg = lg["carries"] / max(lg["plays"], 1)
    mezcla = math.sqrt((carrera / carrera_lg) if j.pos in ("DL", "LB") else ((1 - carrera) / (1 - carrera_lg)))
    medias, var, fac = {}, {}, defaultdict(list)
    base = {}
    for s in STATS_DEF:
        base[s] = (sum(w * valor(p, s) for p, w in zip(partidos, pesos)) + K_POSICION * medias_pos.get(s, 0)) \
            / (sw + K_POSICION)
    textos_jugadas = Factor(f"{rival}: {jugadas:.0f} jugadas esperadas frente a las "
                            f"{defensa.get('plays') or lg['plays']:.0f} que suele enfrentar esta defensa "
                            f"({'más carreras' if carrera > carrera_lg else 'más pases'} de lo normal: "
                            f"{carrera * 100:.0f}% de carreras)", f_jugadas * mezcla, "rival")
    for s in ("tackles", "solo", "asist"):
        medias[s] = base[s] * f_jugadas * mezcla
        fac[s] = [Factor(f"promedia {base[s]:.1f} {s if s != 'tackles' else 'tacleadas'} por partido "
                         f"(contraído hacia su posición, {j.pos})", None, "volumen"), textos_jugadas]
    sack_lg = lg.get("sack_rate") or 0.065
    sack_rival = ctx.perfiles[ataque_rival.team].ataque.get("sack_rate") or sack_lg
    f_sack = (sack_rival / sack_lg) * (ataque_rival.dropbacks / max(defensa.get("dropbacks") or
                                                                    lg["dropbacks"], 1))
    medias["sacks"] = base["sacks"] * f_sack
    fac["sacks"] = [Factor(f"promedia {base['sacks']:.2f} sacks por partido", None, "volumen"),
                    Factor(f"{rival} deja que capturen a su QB en el {sack_rival * 100:.1f}% de los dropbacks "
                           f"(liga {sack_lg * 100:.1f}%; "
                           f"{texto_rango(rango(ctx, 'ataque', 'sack_rate', ataque_rival.team))})", f_sack, "rival")]
    perd_lg = lg.get("turnovers") or 1.2
    perd = ctx.perfiles[ataque_rival.team].ataque.get("turnovers") or perd_lg
    f_int = math.sqrt(perd / perd_lg) * ataque_rival.dropbacks / max(lg["dropbacks"], 1)
    medias["def_ints"] = base["def_ints"] * f_int
    fac["def_ints"] = [Factor(f"{rival} pierde {perd:.1f} balones por partido (liga {perd_lg:.1f})",
                              f_int, "rival")]
    for s, mu in medias.items():
        if s in ("sacks", "def_ints"):
            var[s] = mu + 0.1 * mu * mu
        else:
            vals = [valor(p, s) for p in partidos]
            m = sum(vals) / len(vals) if vals else 0
            cv0 = CV_DEFECTO.get(s, 0.5)
            cv2 = (sum((v - m) ** 2 for v in vals) / (len(vals) - 1) / m ** 2) if len(vals) >= 4 and m > 0 else cv0 ** 2
            n = len(vals)
            var[s] = max(mu * 1.05, (n * cv2 + 6 * cv0 ** 2) / (n + 6) * mu * mu)
    if j.estado:
        for s in medias:
            fac[s].append(Factor(f"en duda ({j.estado})", None, "lesion"))
    # El entorno desde el punto de vista del defensor (su equipo, su rival, si juega en casa).
    propio = replace(ataque_rival, team=j.team, opp=ataque_rival.team, local=not ataque_rival.local)
    return Proyeccion(j, propio, medias, var, dict(fac), {}, {"jugadas_rival": jugadas})


def pateador(ctx: Contexto, team: str) -> tuple[str, str] | None:
    """(player_id, nombre) del pateador del equipo: el que más goles de campo y extras intentó últimamente."""
    juegos = {f["game_id"] for f in ctx.ofensiva.get(team, [])[:4]}
    mejores = []
    for pid, partidos in ctx.jugadores.items():
        pos = (ctx.roster.get(pid) or {}).get("position") or partidos[0].get("position")
        if (pos or "").upper() != "K" or _equipo_actual(ctx, pid, partidos) != team:
            continue
        if not disponible(ctx, pid)[0]:
            continue
        recientes = sum((p.get("fg_att") or 0) + (p.get("pat_made") or 0) for p in partidos[:4]
                        if p["game_id"] in juegos)
        mejores.append((recientes, partidos[0]["gameday"], pid, partidos[0].get("name") or pid))
    if not mejores:
        return None
    _, _, pid, nombre = max(mejores)
    return pid, nombre
