"""Desglose de cada estadística en las estadísticas que la producen.

Cada prop se proyecta desde sus "motores", no solo desde su media:

- Puntos   = tiros de campo × puntos por tiro (reparto por zonas × acierto, ajustado por lo que concede
             el rival en cada zona) + tiros libres × % de tiros libres.
- Triples  = triples intentados × % de triple (esquina y frontal, ajustado por el rival).
- Rebotes  = % de los fallos del rival que captura mientras está en pista × fallos esperados del rival
             + % de los fallos de su equipo que captura en ataque × fallos esperados de su equipo.
- Asist.   = % de las canastas de sus compañeros que asiste con él en pista × canastas esperadas.
- Robos    = % de las pérdidas del rival que roba × pérdidas esperadas del rival.
- Tapones  = % de los tiros de 2 del rival que tapona × tiros de 2 esperados del rival.
- Pérdidas = pérdidas por jugada que usa × jugadas que usa (tiros + 0.44 libres) × presión del rival.

Lo "esperado" del partido de hoy combina el ataque de un equipo con la defensa del otro:
ataque × defensa ÷ media de liga, todo por 48 minutos.
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field

from .zonas import NOMBRES as ZONAS_NOMBRE
from .zonas import VALOR

CAMPOS_EQUIPO = ("min", "fga", "fgm", "tpa", "tpm", "fta", "ftm", "oreb", "dreb", "reb", "ast", "stl", "blk", "tov")
FT_LIGA = 0.78
K_PARTIDOS = 3.0   # partidos "virtuales" de media de su posición que se suman a cada tasa del jugador


# --- Equipos --------------------------------------------------------------------------

def totales_por_partido(filas: list[dict]) -> dict[tuple[str, str], dict]:
    """(partido, equipo) -> suma de las estadísticas de sus jugadores."""
    tot: dict = defaultdict(lambda: defaultdict(float))
    for f in filas:
        t = tot[(f["game_id"], f["team_id"])]
        f_min = f["minutes"]
        t["min"] += f_min
        for c in CAMPOS_EQUIPO[1:]:
            t[c] += f[c]
    return {k: dict(v) for k, v in tot.items()}


def _derivados(t: dict) -> dict:
    """Por 48 minutos (240 minutos de jugador), con fallos y tiros de 2."""
    escala = 240.0 / t["min"] if t.get("min") else 1.0
    out = {c: t[c] * escala for c in CAMPOS_EQUIPO[1:]}
    out["fallos"] = out["fga"] - out["fgm"]
    out["t2a"] = out["fga"] - out["tpa"]
    return out


def promedios_equipo(totales: dict, temporada_de: dict[str, int], temporada: int, peso_anterior: float):
    """equipo -> {"ataque": lo que hace por 48', "defensa": lo que le hacen por 48'} y la media de liga."""
    juegos: dict[str, list[str]] = defaultdict(list)
    for gid, team in totales:
        juegos[gid].append(team)
    acc = defaultdict(lambda: {"ataque": defaultdict(float), "defensa": defaultdict(float), "w": 0.0})
    liga, w_liga = defaultdict(float), 0.0
    for gid, equipos in juegos.items():
        if len(equipos) != 2:
            continue
        w = 1.0 if temporada_de.get(gid) == temporada else peso_anterior
        a, b = equipos
        for yo, rival in ((a, b), (b, a)):
            mio, suyo = _derivados(totales[(gid, yo)]), _derivados(totales[(gid, rival)])
            for k, v in mio.items():
                acc[yo]["ataque"][k] += w * v
                liga[k] += w * v
            for k, v in suyo.items():
                acc[yo]["defensa"][k] += w * v
            acc[yo]["w"] += w
            w_liga += w
    prom = {t: {lado: {k: v / d["w"] for k, v in d[lado].items()} for lado in ("ataque", "defensa")}
            for t, d in acc.items() if d["w"]}
    return prom, {k: v / w_liga for k, v in liga.items()} if w_liga else {}


# --- Oportunidades del jugador -------------------------------------------------------

def oportunidades(p: dict, mio: dict | None, rival: dict | None) -> dict[str, tuple[float, float]]:
    """Numerador y denominador de cada tasa del jugador en un partido."""
    out = {
        "fga": (p["fga"], p["minutes"]), "tpa": (p["tpa"], p["minutes"]), "fta": (p["fta"], p["minutes"]),
        "ft": (p["ftm"], p["fta"]), "fg": (p["fgm"], p["fga"]), "tp": (p["tpm"], p["tpa"]),
        "tov": (p["tov"], p["fga"] + 0.44 * p["fta"] + p["tov"]),
        "uso": (p["fga"] + 0.44 * p["fta"] + p["tov"], p["minutes"]),
    }
    if mio and rival and mio.get("min"):
        en_pista = p["minutes"] / (mio["min"] / 5)
        out.update({
            "dreb": (p["dreb"], (rival["fga"] - rival["fgm"]) * en_pista),
            "oreb": (p["oreb"], (mio["fga"] - mio["fgm"]) * en_pista),
            "ast": (p["ast"], max(0.0, (mio["fgm"] - p["fgm"]) * en_pista)),
            "stl": (p["stl"], rival["tov"] * en_pista),
            "blk": (p["blk"], (rival["fga"] - rival["tpa"]) * en_pista),
        })
    return out


def tasas_liga(filas: list[dict], grupo: dict[str, str], totales: dict, temporada: int,
               peso_anterior: float) -> dict[str, dict[str, float]]:
    acc = defaultdict(lambda: defaultdict(lambda: [0.0, 0.0]))
    for f in filas:
        w = 1.0 if f["season"] == temporada else peso_anterior
        g = grupo[f["player_id"]]
        for k, (n, d) in oportunidades(f, totales.get((f["game_id"], f["team_id"])),
                                       totales.get((f["game_id"], f["opp_id"]))).items():
            acc[g][k][0] += w * n
            acc[g][k][1] += w * d
    return {g: {k: (n / d if d else 0.0) for k, (n, d) in por_k.items()} for g, por_k in acc.items()}


# --- Motores --------------------------------------------------------------------------

@dataclass
class Motor:
    """Proyección de una estadística básica a partir de sus componentes, con la explicación."""
    stat: str
    mu: float
    explicacion: str
    datos: dict = field(default_factory=dict)


def _tasa(partidos, pesos, ctx, k: str, grupo: str) -> tuple[float, float]:
    """Tasa del jugador (contraída a la de su posición) y la tasa sin contraer."""
    num = den = n = 0.0
    for w, p in zip(pesos, partidos):
        o = oportunidades(p, ctx.equipo_partido.get((p["game_id"], p["team_id"])),
                          ctx.equipo_partido.get((p["game_id"], p["opp_id"])))
        if k in o:
            num += w * o[k][0]
            den += w * o[k][1]
            n += w
    liga = ctx.liga_motor.get(grupo, {}).get(k, 0.0)
    k_den = K_PARTIDOS * den / n if n else 0.0
    propia = num / den if den else liga
    return ((num + k_den * liga) / (den + k_den) if den + k_den else liga), propia


def _hoy(ctx, team: str, opp: str, clave: str, lado_mio: str = "ataque", lado_rival: str = "defensa") -> float:
    """Valor esperado por 48' hoy: el de un equipo × el del otro ÷ la media de liga."""
    lg = ctx.liga_equipo.get(clave, 0.0)
    a = ctx.equipo_prom.get(team, {}).get(lado_mio, {}).get(clave, lg)
    b = ctx.equipo_prom.get(opp, {}).get(lado_rival, {}).get(clave, lg)
    return a * b / lg if lg else 0.0


def _factor(ctx, team: str, lado: str, clave: str) -> float:
    lg = ctx.liga_equipo.get(clave, 0.0)
    return ctx.equipo_prom.get(team, {}).get(lado, {}).get(clave, lg) / lg if lg else 1.0


def motores(ctx, j, pesos: list[float]) -> dict[str, Motor]:
    p, g, mins = j.partidos, j.grupo, j.minutos
    t, o = j.team_id, j.opp_id
    bajas = j.ajuste_bajas
    en_pista = mins / 48.0
    out: dict[str, Motor] = {}

    # Tiros: volumen × acierto por zona.
    fga_r, fga_p = _tasa(p, pesos, ctx, "fga", g)
    tpa_r, _ = _tasa(p, pesos, ctx, "tpa", g)
    fta_r, _ = _tasa(p, pesos, ctx, "fta", g)
    ft_num = sum(w * x["ftm"] for w, x in zip(pesos, p))
    ft_den = sum(w * x["fta"] for w, x in zip(pesos, p))
    ft_pct = (ft_num + 20 * FT_LIGA) / (ft_den + 20)
    f_fga = _factor(ctx, o, "defensa", "fga")
    f_fta = _factor(ctx, o, "defensa", "fta")
    f_tpa = _factor(ctx, o, "defensa", "tpa") / f_fga if f_fga else 1.0
    uso = bajas.get("pts", 1.0)
    fga = fga_r * mins * f_fga * uso
    fta = fta_r * mins * f_fta * uso
    zonas = j.zonas
    pts_tiro = fg_pct = 0.0
    tres_rep = tres_pct = 0.0
    lineas_zona = []
    for z, d in sorted(zonas.items(), key=lambda kv: -kv[1]["reparto"]):
        ajuste = d["pct_rival"] / d["pct_liga"] if d["pct_liga"] else 1.0
        pct = min(0.95, d["pct"] * ajuste)
        pts_tiro += d["reparto"] * pct * VALOR[z]
        fg_pct += d["reparto"] * pct
        if VALOR[z] == 3:
            tres_rep += d["reparto"]
            tres_pct += d["reparto"] * pct
        if d["reparto"] >= 0.1:
            lineas_zona.append(f"{ZONAS_NOMBRE[z]} {d['reparto'] * 100:.0f}% de sus tiros al {d['pct'] * 100:.0f}% "
                               f"(rival concede {d['pct_rival'] * 100:.0f}%, liga {d['pct_liga'] * 100:.0f}%)")
    tp_pct = tres_pct / tres_rep if tres_rep else 0.35
    pts = fga * pts_tiro + fta * ft_pct
    out["pts"] = Motor("pts", pts,
                       f"{fga:.1f} tiros de campo (su ritmo {fga_p * 36:.1f} por 36'; el rival concede "
                       f"{(f_fga - 1) * 100:+.0f}% de tiros) × {pts_tiro:.2f} puntos por tiro "
                       f"[{'; '.join(lineas_zona)}] + {fta:.1f} tiros libres × {ft_pct * 100:.0f}%",
                       {"fga": fga, "pts_por_tiro": pts_tiro, "fta": fta, "ft_pct": ft_pct,
                        "rival_tiros": f_fga, "rival_libres": f_fta})
    out["fgm"] = Motor("fgm", fga * fg_pct, f"{fga:.1f} tiros × {fg_pct * 100:.0f}% de acierto esperado",
                       {"fga": fga, "fg_pct": fg_pct})
    out["fta"] = Motor("fta", fta, f"{fta_r * 36:.1f} libres por 36' × {mins:.0f}' × rival {(f_fta - 1) * 100:+.0f}%",
                       {"fta": fta})
    out["ftm"] = Motor("ftm", fta * ft_pct, f"{fta:.1f} tiros libres × {ft_pct * 100:.0f}%", {"fta": fta, "ft_pct": ft_pct})
    tpa = tpa_r * mins * f_fga * f_tpa * uso
    out["tpm"] = Motor("tpm", tpa * tp_pct,
                       f"{tpa:.1f} triples intentados (su ritmo {tpa_r * 36:.1f} por 36'; el rival concede "
                       f"{(f_tpa - 1) * 100:+.0f}% de triples en su reparto) × {tp_pct * 100:.0f}% esperado",
                       {"tpa": tpa, "tp_pct": tp_pct})

    # Rebotes: su parte de los rebotes disponibles mientras está en pista.
    dreb_r, dreb_p = _tasa(p, pesos, ctx, "dreb", g)
    oreb_r, oreb_p = _tasa(p, pesos, ctx, "oreb", g)
    fallos_rival = _hoy(ctx, o, t, "fallos")
    fallos_mios = _hoy(ctx, t, o, "fallos")
    reb_b = bajas.get("reb", 1.0)
    dreb = dreb_r * fallos_rival * en_pista * reb_b
    oreb = oreb_r * fallos_mios * en_pista * reb_b
    out["reb"] = Motor("reb", dreb + oreb,
                       f"defensivos {dreb:.1f} = captura el {dreb_r * 100:.1f}% de los fallos del rival en pista × "
                       f"{fallos_rival:.1f} fallos esperados del rival (liga {ctx.liga_equipo.get('fallos', 0):.1f}) × "
                       f"{en_pista * 100:.0f}% del partido; ofensivos {oreb:.1f} = {oreb_r * 100:.1f}% de los fallos "
                       f"de su equipo × {fallos_mios:.1f}",
                       {"dreb": dreb, "oreb": oreb, "pct_dreb": dreb_r, "pct_oreb": oreb_r,
                        "fallos_rival": fallos_rival, "fallos_equipo": fallos_mios})

    # Asistencias: su parte de las canastas de los compañeros.
    ast_r, _ = _tasa(p, pesos, ctx, "ast", g)
    canastas = _hoy(ctx, t, o, "fgm")
    propias = out["fgm"].mu
    ast = ast_r * max(0.0, canastas * en_pista - propias) * bajas.get("ast", 1.0)
    out["ast"] = Motor("ast", ast,
                       f"asiste el {ast_r * 100:.1f}% de las canastas de sus compañeros en pista × "
                       f"{max(0.0, canastas * en_pista - propias):.1f} canastas de compañeros esperadas "
                       f"(su equipo {canastas:.1f} por 48' contra esta defensa)",
                       {"pct_ast": ast_r, "canastas_equipo": canastas})

    # Robos, tapones y pérdidas.
    stl_r, _ = _tasa(p, pesos, ctx, "stl", g)
    perd_rival = _hoy(ctx, o, t, "tov")
    out["stl"] = Motor("stl", stl_r * perd_rival * en_pista * bajas.get("stl", 1.0),
                       f"roba el {stl_r * 100:.1f}% de las pérdidas del rival en pista × {perd_rival:.1f} pérdidas "
                       f"esperadas del rival", {"pct_stl": stl_r, "perdidas_rival": perd_rival})
    blk_r, _ = _tasa(p, pesos, ctx, "blk", g)
    t2_rival = _hoy(ctx, o, t, "t2a")
    out["blk"] = Motor("blk", blk_r * t2_rival * en_pista * bajas.get("blk", 1.0),
                       f"tapona el {blk_r * 100:.1f}% de los tiros de 2 del rival en pista × {t2_rival:.1f} tiros de 2 "
                       f"esperados del rival", {"pct_blk": blk_r, "t2a_rival": t2_rival})
    tov_r, _ = _tasa(p, pesos, ctx, "tov", g)
    presion = _factor(ctx, o, "defensa", "tov")
    jugadas = fga + 0.44 * fta
    out["tov"] = Motor("tov", tov_r / (1 - tov_r) * jugadas * presion if tov_r < 1 else 0.0,
                       f"pierde el {tov_r * 100:.1f}% de las jugadas que usa × {jugadas:.1f} jugadas de tiro × "
                       f"presión del rival {(presion - 1) * 100:+.0f}%", {"pct_tov": tov_r, "presion_rival": presion})
    return out


# --- Base de datos de cada prop: métricas relacionadas --------------------------------

# Métricas que explican cada estadística básica: (clave, nombre, tipo). "media" = por partido;
# "tasa" (un porcentaje) y "por36" usan el numerador y denominador de oportunidades().
METRICAS = {
    "min": [("minutes", "Minutos", "media")],
    "pts": [("pts", "Puntos", "media"), ("fga", "Tiros de campo intentados", "media"), ("fg", "% tiros de campo", "tasa"),
            ("tpa", "Triples intentados", "media"), ("tp", "% triples", "tasa"), ("fta", "Tiros libres intentados", "media"),
            ("ft", "% tiros libres", "tasa"), ("uso", "Jugadas que usa por 36 min", "por36")],
    "reb": [("reb", "Rebotes", "media"), ("dreb", "% de los fallos del rival que captura", "tasa"),
            ("oreb", "% de los fallos de su equipo que captura", "tasa")],
    "ast": [("ast", "Asistencias", "media"), ("ast", "% de las canastas de compañeros que asiste", "tasa"),
            ("tov", "Pérdidas por jugada", "tasa")],
    "tpm": [("tpm", "Triples anotados", "media"), ("tpa", "Triples intentados", "media"), ("tp", "% triples", "tasa")],
    "stl": [("stl", "Robos", "media"), ("stl", "% de las pérdidas del rival que roba", "tasa")],
    "blk": [("blk", "Tapones", "media"), ("blk", "% de los tiros de 2 del rival que tapona", "tasa")],
    "tov": [("tov", "Pérdidas", "media"), ("tov", "Pérdidas por jugada", "tasa"), ("uso", "Jugadas que usa por 36 min", "por36")],
    "fgm": [("fgm", "Tiros de campo anotados", "media"), ("fga", "Tiros de campo intentados", "media"),
            ("fg", "% tiros de campo", "tasa")],
    "ftm": [("ftm", "Tiros libres anotados", "media"), ("fta", "Tiros libres intentados", "media"),
            ("ft", "% tiros libres", "tasa")],
    "fta": [("fta", "Tiros libres intentados", "media"), ("ft", "% tiros libres", "tasa")],
}


def _valor_metrica(ctx, partidos: list[dict], clave: str, tipo: str) -> float | None:
    if not partidos:
        return None
    if tipo == "media":
        return sum(p[clave] for p in partidos) / len(partidos)
    num = den = 0.0
    for p in partidos:
        o = oportunidades(p, ctx.equipo_partido.get((p["game_id"], p["team_id"])),
                          ctx.equipo_partido.get((p["game_id"], p["opp_id"])))
        if clave in o:
            num += o[clave][0]
            den += o[clave][1]
    if not den:
        return None
    return num / den * (36 if tipo == "por36" else 1)


def tabla_metricas(ctx, j, componentes: tuple[str, ...]) -> list[dict]:
    """Las estadísticas relacionadas con la prop en sus últimos 5 y 10, la temporada y contra este rival."""
    cortes = {
        "ult5": j.partidos[:5], "ult10": j.partidos[:10],
        "temporada": [p for p in j.partidos if p["season"] == ctx.temporada] or None,
        "anterior": [p for p in j.partidos if p["season"] != ctx.temporada] or None,
        "vs_rival": [p for p in j.partidos if p["opp_id"] == j.opp_id][:5] or None,
    }
    filas, vistas = [], set()
    for comp in ("min",) + componentes:
        for clave, nombre, tipo in METRICAS.get(comp, []):
            if nombre in vistas:
                continue
            vistas.add(nombre)
            filas.append({"metrica": nombre, "tipo": tipo,
                          **{k: (_valor_metrica(ctx, v, clave, tipo) if v else None) for k, v in cortes.items()}})
    return filas
