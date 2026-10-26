"""Quién lo va a defender y cómo le va contra ese tipo de defensor (datos de stats.nba.com).

Con la tabla nba_matchups (atacante, defensor, posesiones y puntos):

- Calidad de cada defensor: puntos que permite por 100 posesiones que defiende, contraído a la media.
  Los defensores con muestra suficiente se reparten en élite / medio / débil.
- Defensores esperados hoy: cómo repartió el rival sus posesiones defensivas contra atacantes de la
  misma posición del jugador en sus partidos recientes (sin los que están fuera hoy).
- Su historial: puntos por 100 posesiones contra cada nivel de defensor y contra cada defensor concreto.

El ajuste final es la raíz de (calidad de los defensores × su rendimiento contra ese nivel × su historial
directo), acotado a ±12 %. Se aplica a puntos, tiros anotados y triples.
"""
from __future__ import annotations

import math
from collections import defaultdict
from dataclasses import dataclass, field

K_DEFENSOR = 300.0     # posesiones virtuales de media de liga en la calidad de un defensor
K_NIVEL = 150.0        # ídem en el rendimiento del jugador contra un nivel de defensor
K_DIRECTO = 60.0       # ídem contra un defensor concreto
MIN_POS_NIVEL = 200.0  # posesiones para clasificar a un defensor
TOPE = 0.12
PARTIDOS_REPARTO = 15  # partidos recientes del rival para estimar a quién pone a defender


@dataclass
class Marcajes:
    ppp_liga: float
    defensor: dict[str, tuple[float, float]]            # id -> (puntos por posesión contraídos, posesiones)
    nivel: dict[str, str]                               # id -> élite / medio / débil
    nombre: dict[str, str]
    reparto: dict[str, dict[str, dict[str, float]]]     # equipo -> grupo del atacante -> defensor -> posesiones
    ataque: dict[str, list[dict]]                       # atacante -> filas (defensor, posesiones, puntos)


@dataclass
class Enfrentamiento:
    factor: float
    defensores: list[dict] = field(default_factory=list)   # los más probables hoy, con su calidad y el historial
    por_nivel: dict[str, dict] = field(default_factory=dict)
    partes: dict[str, float] = field(default_factory=dict)


def construir(conn, fecha: str, desde: str, grupo: dict[str, str]) -> Marcajes | None:
    filas = [dict(r) for r in conn.execute(
        """SELECT m.*, g.fecha, g.season FROM nba_matchups m JOIN nba_games g ON g.id = m.game_id
           WHERE g.fecha < ? AND g.fecha >= ? AND m.off_player_id IS NOT NULL AND m.def_player_id IS NOT NULL
           ORDER BY g.fecha DESC""", (fecha, desde))]
    if not filas:
        return None
    temporada = max(f["season"] for f in filas)
    pts = sum(f["pts"] for f in filas)
    pos = sum(f["posesiones"] for f in filas)
    ppp = pts / pos if pos else 1.0
    acc = defaultdict(lambda: [0.0, 0.0])
    nombre, ataque = {}, defaultdict(list)
    for f in filas:
        w = 1.0 if f["season"] == temporada else 0.5
        a = acc[f["def_player_id"]]
        a[0] += w * f["pts"]
        a[1] += w * f["posesiones"]
        nombre[f["def_player_id"]] = f["def_name"]
        nombre.setdefault(f["off_player_id"], f["off_name"])
        ataque[f["off_player_id"]].append(f)
    defensor = {d: ((p + K_DEFENSOR * ppp) / (n + K_DEFENSOR), n) for d, (p, n) in acc.items()}
    clasificables = sorted((d for d, (_, n) in defensor.items() if n >= MIN_POS_NIVEL), key=lambda d: defensor[d][0])
    k = len(clasificables)
    nivel = {d: ("élite" if i < k / 3 else "medio" if i < 2 * k / 3 else "débil") for i, d in enumerate(clasificables)}

    # Reparto reciente de cada equipo: sus últimos partidos con datos.
    juegos = defaultdict(list)
    for f in filas:
        if f["def_team_id"] and f["game_id"] not in juegos[f["def_team_id"]]:
            juegos[f["def_team_id"]].append(f["game_id"])
    recientes = {t: set(g[:PARTIDOS_REPARTO]) for t, g in juegos.items()}
    reparto = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
    for f in filas:
        t = f["def_team_id"]
        if t and f["game_id"] in recientes.get(t, ()):
            reparto[t][grupo.get(f["off_player_id"], "G")][f["def_player_id"]] += f["posesiones"]
    return Marcajes(ppp, defensor, nivel, nombre, reparto, ataque)


def _ppp(filas: list[dict]) -> tuple[float, float]:
    pos = sum(f["posesiones"] for f in filas)
    return (sum(f["pts"] for f in filas) / pos if pos else 0.0), pos


def evaluar(m: Marcajes | None, player_id: str, grupo: str, opp_id: str, fuera: set[str]) -> Enfrentamiento | None:
    if m is None:
        return None
    reparto = {d: n for d, n in m.reparto.get(opp_id, {}).get(grupo, {}).items() if d not in fuera}
    total = sum(reparto.values())
    if total <= 0:
        return None
    propio = m.ataque.get(player_id, [])
    ppp_propio, pos_propio = _ppp(propio)
    ppp_base = (ppp_propio * pos_propio + K_NIVEL * m.ppp_liga) / (pos_propio + K_NIVEL)

    # Calidad de los defensores que se espera que lo marquen.
    f_calidad = sum(n / total * m.defensor.get(d, (m.ppp_liga, 0))[0] for d, n in reparto.items()) / m.ppp_liga

    # Su rendimiento contra cada nivel de defensor.
    por_nivel = {}
    for niv in ("élite", "medio", "débil"):
        ppp_n, pos_n = _ppp([f for f in propio if m.nivel.get(f["def_player_id"]) == niv])
        rel = 1 + ((ppp_n / ppp_base if ppp_base else 1) - 1) * pos_n / (pos_n + K_NIVEL) if pos_n else 1.0
        por_nivel[niv] = {"posesiones": pos_n, "pts_100": ppp_n * 100, "relativo": rel}
    f_nivel = sum(n / total * por_nivel.get(m.nivel.get(d, ""), {"relativo": 1.0})["relativo"]
                  for d, n in reparto.items())

    # Su historial directo contra cada defensor.
    f_directo, defensores = 0.0, []
    for d, n in sorted(reparto.items(), key=lambda kv: -kv[1]):
        ppp_d, pos_d = _ppp([f for f in propio if f["def_player_id"] == d])
        rel = ((ppp_d * pos_d + K_DIRECTO * ppp_base) / (pos_d + K_DIRECTO)) / ppp_base if ppp_base else 1.0
        f_directo += n / total * rel
        if len(defensores) < 4 and n / total >= 0.08:
            q = m.defensor.get(d, (m.ppp_liga, 0))[0]
            defensores.append({"id": d, "nombre": m.nombre.get(d, d), "reparto": n / total,
                               "nivel": m.nivel.get(d, "sin muestra"), "permite_100": q * 100,
                               "liga_100": m.ppp_liga * 100, "vs_el_posesiones": pos_d, "vs_el_pts_100": ppp_d * 100})
    factor = math.sqrt(f_calidad * f_nivel * f_directo)
    factor = min(1 + TOPE, max(1 - TOPE, factor))
    return Enfrentamiento(factor, defensores, por_nivel,
                          {"calidad_defensores": f_calidad, "vs_ese_nivel": f_nivel, "historial_directo": f_directo})


def explicar(e: Enfrentamiento) -> str:
    partes = [f"{d['nombre']} ({d['reparto'] * 100:.0f}% de las posesiones contra su posición; defensor "
              f"{d['nivel']}, permite {d['permite_100']:.0f} pts/100 vs {d['liga_100']:.0f} de media"
              + (f"; contra él: {d['vs_el_pts_100']:.0f} pts/100 en {d['vs_el_posesiones']:.0f} posesiones"
                 if d["vs_el_posesiones"] else "") + ")" for d in e.defensores]
    niveles = ", ".join(f"vs {k} {v['pts_100']:.0f} pts/100 ({v['posesiones']:.0f} pos.)"
                        for k, v in e.por_nivel.items() if v["posesiones"])
    return (f"marcaje {(e.factor - 1) * 100:+.0f}%: defensores probables " + "; ".join(partes)
            + (f". Sus puntos por 100 posesiones según el defensor: {niveles}" if niveles else ""))
