"""Modelo de props por probabilidad.

Para cada jugador y estadística:

    media = minutos esperados × tasa por minuto × ajuste por bajas × defensa rival × tipo de defensa

- Minutos esperados: últimos 10 partidos con más peso a los recientes; varianza propia de sus minutos.
- Tasa por minuto: toda la historia con decaimiento (la temporada anterior pesa la mitad) y contracción
  hacia la media de su posición cuando hay pocos partidos.
- Bajas: si un compañero importante está fuera, se compara al jugador con y sin él (minutos y tasas).
- Defensa rival por posición: lo que el rival concede por minuto a bases (G), aleros (F) o pívots (C).
- Zonas de tiro: dónde tira el jugador (aro, pintura, media, triple de esquina y frontal) y qué
  porcentaje concede el rival en cada zona. Ajusta puntos y triples.
- Tipo de defensa: cómo le fue al jugador contra defensas del mismo nivel que la de hoy.

La distribución es binomial negativa con la dispersión estimada del propio jugador más la
incertidumbre de sus minutos. La probabilidad final mezcla el modelo con su tasa de acierto real
sobre esa línea en los últimos partidos y, si hay cuotas, con la probabilidad de la casa sin margen.
"""
from __future__ import annotations

import math
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date, timedelta

from ..model import negbin_pmf
from .desglose import Motor, motores, promedios_equipo, tabla_metricas, tasas_liga, totales_por_partido
from . import marcajes
from .espn import grupo_posicion
from .zonas import VALOR, ZONAS

COMPONENTES = {
    "points": ("pts",), "rebounds": ("reb",), "assists": ("ast",), "threes": ("tpm",), "steals": ("stl",),
    "blocks": ("blk",), "turnovers": ("tov",), "pr": ("pts", "reb"), "pa": ("pts", "ast"), "ra": ("reb", "ast"),
    "pra": ("pts", "reb", "ast"), "stocks": ("stl", "blk"), "fgm": ("fgm",), "ftm": ("ftm",), "fta": ("fta",),
}
NOMBRES = {
    "points": "puntos", "rebounds": "rebotes", "assists": "asistencias", "threes": "triples",
    "steals": "robos", "blocks": "tapones", "turnovers": "pérdidas", "pr": "pts+reb", "pa": "pts+ast",
    "ra": "reb+ast", "pra": "pts+reb+ast", "stocks": "robos+tapones", "fgm": "tiros de campo anotados",
    "ftm": "tiros libres anotados", "fta": "tiros libres intentados",
}
BASICAS = ("pts", "reb", "ast", "tpm", "stl", "blk", "tov", "fgm", "ftm", "fta")

PESO_TEMPORADA_ANTERIOR = 0.5
# Peso máximo de la temporada anterior, en partidos, en cuanto hay partidos de la actual. Backtest del
# arranque de 2025-26 (22 oct-25 nov, con 2024-25 como anterior): en jugadores con cambio de rol (tasa
# ±30 % y ≤8 partidos) el Brier baja de 0.2274 (sin límite) a 0.2256 con 4; en el resto, igual.
K_TEMPORADA_ANTERIOR: float | None = 4.0
# Cambio de rol: tasa por minuto de esta temporada ±30 % frente a la anterior con menos de 10 partidos.
# Entonces la casa (que conoce el rol nuevo) pesa más en la probabilidad final.
CAMBIO_ROL = 0.3
PESO_MERCADO_CAMBIO_ROL = 0.6
# Al empezar la temporada la casa conoce roles y rotaciones nuevas mejor que unos pocos partidos: su peso
# baja de 0.7 (0 partidos de esta temporada) al normal (PESO_MERCADO) a los 15 partidos. El 25 oct 2026
# (769 props con resultado) la casa sola tuvo Brier 0.2449, el modelo solo 0.2500 y la mezcla 0.2456.
PESO_MERCADO_INICIO = 0.7
PARTIDOS_INICIO = 15
DECAY_TASA = 0.97          # peso del partido i-ésimo más reciente para las tasas
DECAY_MINUTOS = 0.8        # ídem para los minutos (cambian rápido: rol, rotación)
PARTIDOS_MINUTOS = 10
K_DEFENSA_MIN = 600.0      # minutos "virtuales" de media de liga en la defensa por posición
K_ZONA_TIROS = 120.0       # tiros "virtuales" de media de liga por zona (rival)
K_ZONA_JUGADOR = 25.0      # ídem para el porcentaje del jugador en cada zona
K_TIPO_MIN = 400.0         # minutos virtuales para el rendimiento contra un tipo de defensa
PESO_MODELO = 0.75         # resto: tasa de acierto real sobre la línea (suavizada)
# Peso de la proyección por componentes (desglose.py: tiros × acierto, % de rebotes disponibles, % de
# canastas asistidas...) frente a la de tasa por minuto × defensa rival por posición. En el backtest
# (feb-mar 2026) ambas aciertan casi igual (Brier 0.2270 con 0, 0.2271 con 0.3, 0.2282 con 1); 0.3 mejora
# un poco la calibración por encima del 70 % y deja cada media explicada por sus componentes.
PESO_MOTORES = 0.3
# Contracción hacia 50 %: el backtest (feb-mar 2026, 19.700 props) mostró que sin ella el modelo era
# ~3 puntos optimista por encima del 70 %. Con 0.9 queda calibrado (incluso algo conservador arriba).
CALIBRACION = 0.9
# Picks seguros: una línea más baja (p. ej. "15+ puntos") de un titular estable en vez de la línea normal.
# Backtest (22 oct-25 nov 2025 y 20 feb-10 mar 2026), titulares con 30+ minutos: eligiendo la línea al
# 85 % acertaron el 89-96 % según la estadística; al 90 %, el 93-99 %.
PROB_SEGURA = 0.85
MIN_SEGURA = 30.0
MEDIAS_SEGURA = {"points": 15, "rebounds": 7, "assists": 5, "pra": 25}   # media mínima en sus últimos 10
# Peso de la probabilidad de la casa (sin margen) en la probabilidad final. La línea recoge lo que el
# modelo no ve (rol, rotaciones, noticias de última hora).
PESO_MERCADO = 0.4
# Con menos de 3 partidos en su equipo actual (traspaso reciente), la casa sabe más de su nuevo rol.
PESO_MERCADO_TRASPASO = 0.7
# Los roles cambian entre temporadas: en cuanto hay partidos de la actual, los minutos de la anterior
# casi no cuentan.
PESO_MINUTOS_ANTERIOR = 0.15
MIN_COMPANERO = 20.0       # minutos medios para considerar importante la baja de un compañero
ESTADOS_FUERA = ("out", "doubtful")


# --- Distribución ---------------------------------------------------------------------

def cdf(k: int, mu: float, var: float) -> float:
    if k < 0:
        return 0.0
    return min(1.0, sum(negbin_pmf(i, mu, var) for i in range(k + 1)))


def prob_lados(line: float, mu: float, var: float) -> tuple[float, float]:
    """P(más de la línea), P(menos de la línea). Con línea entera, el empate (devolución) no cuenta."""
    if mu <= 0:
        return 0.0, 1.0
    over = 1.0 - cdf(math.floor(line), mu, var)
    under = cdf(math.ceil(line) - 1, mu, var)
    return max(0.0, over), max(0.0, under)


def linea_segura(mu: float, var: float, prob: float = 0.8) -> tuple[float | None, float | None]:
    """Línea .5 más alta con P(más) >= prob y la más baja con P(menos) >= prob."""
    over_l = under_l = None
    for k in range(0, int(mu * 3 + 20)):
        line = k + 0.5
        o, u = prob_lados(line, mu, var)
        if o >= prob:
            over_l = line
        if u >= prob and under_l is None:
            under_l = line
    return over_l, under_l


# --- Contexto de liga -----------------------------------------------------------------

@dataclass
class Contexto:
    fecha: str
    temporada: int
    filas: list[dict]                       # partidos de jugador anteriores a la fecha
    por_jugador: dict[str, list[dict]]      # ordenados del más reciente al más antiguo
    grupo: dict[str, str]                   # jugador -> G / F / C
    liga: dict[str, dict[str, float]]       # grupo -> stat -> por minuto
    defensa: dict[str, dict[str, dict[str, float]]]   # equipo -> grupo -> stat -> factor (1 = media)
    nivel: dict[str, dict[str, dict[str, str]]]       # grupo -> stat -> equipo -> fuerte/media/débil
    zona_liga: dict[str, tuple[float, float]]          # zona -> (% acierto, frecuencia)
    zona_rival: dict[str, dict[str, tuple[float, float]]]
    zona_jugador: dict[str, dict[str, tuple[float, float]]]  # jugador -> zona -> (intentos, anotados)
    ritmo: dict[str, float]                 # posesiones por partido de cada equipo
    ritmo_liga: float
    ultimo_partido: dict[str, str]          # equipo -> fecha de su último partido
    equipo_partido: dict = field(default_factory=dict)  # (partido, equipo) -> totales
    equipo_prom: dict = field(default_factory=dict)     # equipo -> ataque/defensa por 48'
    liga_equipo: dict = field(default_factory=dict)     # media de liga por equipo y 48'
    liga_motor: dict = field(default_factory=dict)      # grupo -> tasa de liga de cada componente
    marcajes: marcajes.Marcajes | None = None           # stats.nba.com, si se descargó


def _peso_temporada(season: int, actual: int) -> float:
    return 1.0 if season == actual else PESO_TEMPORADA_ANTERIOR


def construir_contexto(conn, fecha: str, dias: int = 420) -> Contexto:
    desde = (date.fromisoformat(fecha) - timedelta(days=dias)).isoformat()
    filas = [dict(r) for r in conn.execute(
        """SELECT pg.*, g.fecha, g.season FROM nba_player_games pg JOIN nba_games g ON g.id = pg.game_id
           WHERE g.fecha < ? AND g.fecha >= ? AND g.season_type IN (2, 3, 5) ORDER BY g.fecha DESC""",
        (fecha, desde))]
    temporada = max((f["season"] for f in filas), default=0)
    por_jugador: dict[str, list[dict]] = defaultdict(list)
    grupo: dict[str, str] = {}
    for f in filas:
        por_jugador[f["player_id"]].append(f)
        grupo.setdefault(f["player_id"], grupo_posicion(f["position"]))

    # Media de liga por grupo y defensa por posición (lo concedido por minuto).
    tot = defaultdict(lambda: defaultdict(float))
    conc = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
    for f in filas:
        w = _peso_temporada(f["season"], temporada)
        g = grupo[f["player_id"]]
        tot[g]["min"] += w * f["minutes"]
        conc[f["opp_id"]][g]["min"] += w * f["minutes"]
        for s in BASICAS:
            tot[g][s] += w * f[s]
            conc[f["opp_id"]][g][s] += w * f[s]
    liga = {g: {s: (d[s] / d["min"] if d["min"] else 0.0) for s in BASICAS} for g, d in tot.items()}
    defensa: dict = {}
    for team, por_g in conc.items():
        defensa[team] = {}
        for g, d in por_g.items():
            defensa[team][g] = {}
            for s in BASICAS:
                lg = liga.get(g, {}).get(s, 0.0)
                tasa = (d[s] + K_DEFENSA_MIN * lg) / (d["min"] + K_DEFENSA_MIN)
                defensa[team][g][s] = tasa / lg if lg else 1.0
    nivel: dict = defaultdict(dict)
    for g in liga:
        for s in BASICAS:
            orden = sorted((t for t in defensa if g in defensa[t]), key=lambda t: defensa[t][g][s])
            n = len(orden)
            nivel[g][s] = {t: ("fuerte" if i < n / 3 else "media" if i < 2 * n / 3 else "débil")
                           for i, t in enumerate(orden)}

    # Ritmo: posesiones por partido (FGA - OREB + TOV + 0.44 FTA).
    pos = defaultdict(float)
    ultimo: dict[str, str] = {}
    for f in filas:
        pos[(f["game_id"], f["team_id"])] += f["fga"] - f["oreb"] + f["tov"] + 0.44 * f["fta"]
        ultimo.setdefault(f["team_id"], f["fecha"])
    por_equipo = defaultdict(list)
    temporada_de = {f["game_id"]: f["season"] for f in filas}
    for (gid, team), p in pos.items():
        if temporada_de[gid] == temporada:
            por_equipo[team].append(p)
    ritmo = {t: sum(v) / len(v) for t, v in por_equipo.items() if v}
    ritmo_liga = sum(ritmo.values()) / len(ritmo) if ritmo else 100.0

    # Zonas de tiro.
    zl = defaultdict(lambda: [0.0, 0.0])
    zr = defaultdict(lambda: defaultdict(lambda: [0.0, 0.0]))
    zj = defaultdict(lambda: defaultdict(lambda: [0.0, 0.0]))
    for r in conn.execute(
        """SELECT s.player_id, s.opp_id, s.zone, g.season, COUNT(*) AS fga, SUM(s.made) AS fgm
           FROM nba_shots s JOIN nba_games g ON g.id = s.game_id
           WHERE g.fecha < ? AND g.fecha >= ? AND g.season_type IN (2, 3, 5)
           GROUP BY s.player_id, s.opp_id, s.zone, g.season""", (fecha, desde)):
        w = _peso_temporada(r["season"], temporada)
        for acc in (zl[r["zone"]], zr[r["opp_id"]][r["zone"]], zj[r["player_id"]][r["zone"]]):
            acc[0] += w * r["fga"]
            acc[1] += w * r["fgm"]
    total_liga = sum(v[0] for v in zl.values()) or 1.0
    zona_liga = {z: (zl[z][1] / zl[z][0] if zl[z][0] else 0.0, zl[z][0] / total_liga) for z in ZONAS}
    zona_rival = {}
    for t, por_z in zr.items():
        total = sum(v[0] for v in por_z.values()) or 1.0
        zona_rival[t] = {}
        for z in ZONAS:
            fga, fgm = por_z[z]
            pct_lg, frec_lg = zona_liga[z]
            pct = (fgm + K_ZONA_TIROS * pct_lg) / (fga + K_ZONA_TIROS)
            frec = (fga + K_ZONA_TIROS * frec_lg) / (total + K_ZONA_TIROS)
            zona_rival[t][z] = (pct, frec)
    zona_jugador = {p: {z: tuple(v) for z, v in por_z.items()} for p, por_z in zj.items()}

    equipo_partido = totales_por_partido(filas)
    equipo_prom, liga_equipo = promedios_equipo(equipo_partido, temporada_de, temporada, PESO_TEMPORADA_ANTERIOR)
    liga_motor = tasas_liga(filas, grupo, equipo_partido, temporada, PESO_TEMPORADA_ANTERIOR)
    return Contexto(fecha, temporada, filas, por_jugador, grupo, liga, defensa, nivel, zona_liga, zona_rival,
                    zona_jugador, ritmo, ritmo_liga, ultimo, equipo_partido, equipo_prom, liga_equipo, liga_motor,
                    marcajes.construir(conn, fecha, desde, grupo))


# --- Jugador --------------------------------------------------------------------------

@dataclass
class Prediccion:
    stat: str
    mu: float
    var: float
    factores: dict[str, float] = field(default_factory=dict)
    # Por componente (pts, reb, ast...): proyección por tasa, por motores y la final, con la explicación.
    componentes: dict[str, dict] = field(default_factory=dict)


@dataclass
class Jugador:
    player_id: str
    nombre: str
    team_id: str
    opp_id: str
    grupo: str
    partidos: list[dict]
    minutos: float
    minutos_sd: float
    notas: list[str] = field(default_factory=list)
    ajuste_bajas: dict[str, float] = field(default_factory=dict)   # stat básica -> multiplicador
    zonas: dict[str, dict] = field(default_factory=dict)
    motores: dict[str, Motor] | None = None
    enfrentamiento: marcajes.Enfrentamiento | None = None
    pocos_con_equipo: bool = False
    cambio_rol: dict[str, float] = field(default_factory=dict)   # stat básica -> tasa actual / anterior

    @property
    def n(self) -> int:
        return len(self.partidos)


def _pesos(partidos: list[dict], temporada: int, decay: float) -> list[float]:
    w = [decay ** i * _peso_temporada(p["season"], temporada) for i, p in enumerate(partidos)]
    # En cuanto hay partidos de esta temporada, la anterior vale como mucho K_TEMPORADA_ANTERIOR partidos:
    # si cambió de rol (más asistencias, más tiros), sus partidos nuevos pesan desde el principio.
    if K_TEMPORADA_ANTERIOR is not None and partidos and partidos[0]["season"] == temporada:
        previos = sum(wi for wi, p in zip(w, partidos) if p["season"] != temporada)
        if previos > K_TEMPORADA_ANTERIOR:
            f = K_TEMPORADA_ANTERIOR / previos
            w = [wi * f if p["season"] != temporada else wi for wi, p in zip(w, partidos)]
    return w


def valor(p: dict, stat: str) -> float:
    return sum(p[c] for c in COMPONENTES[stat])


def _bajas(ctx: Contexto, j: Jugador, ausentes: list[tuple[str, str]]) -> float:
    """Compara al jugador con y sin cada compañero ausente. Devuelve el cambio de minutos."""
    delta_total = 0.0
    for comp_id, comp_nombre in ausentes:
        comp = ctx.por_jugador.get(comp_id, [])
        recientes = [p for p in comp[:PARTIDOS_MINUTOS] if p["team_id"] == j.team_id]
        if not recientes or sum(p["minutes"] for p in recientes) / len(recientes) < MIN_COMPANERO:
            continue
        # Si ya faltaba en los últimos partidos, sus minutos recientes ya reflejan la baja: no se suma dos veces.
        ultimos = [p["game_id"] for p in j.partidos if p["team_id"] == j.team_id][:3]
        if ultimos and not {p["game_id"] for p in comp} & set(ultimos):
            j.notas.append(f"{comp_nombre} ya no jugó en sus últimos partidos: la baja ya está en sus minutos")
            continue
        temporadas = {p["season"] for p in comp if p["team_id"] == j.team_id}
        juegos_comp = {p["game_id"] for p in comp}
        mios = [p for p in j.partidos if p["team_id"] == j.team_id and p["season"] in temporadas]
        con = [p for p in mios if p["game_id"] in juegos_comp]
        sin = [p for p in mios if p["game_id"] not in juegos_comp]
        if len(sin) < 3 or len(con) < 3:
            j.notas.append(f"sin {comp_nombre}: muestra insuficiente ({len(sin)} partidos sin él)")
            continue
        m_con = sum(p["minutes"] for p in con) / len(con)
        m_sin = sum(p["minutes"] for p in sin) / len(sin)
        # Solo se suman minutos: la baja de un compañero no quita minutos, y cuando los datos dicen lo
        # contrario suele ser porque esos partidos fueron de descanso o ya decididos.
        delta = min(4.0, max(0.0, (m_sin - m_con) * len(sin) / (len(sin) + 4)))
        delta_total += delta
        cambios = []
        for s in BASICAS:
            t_con = sum(p[s] for p in con) / max(1.0, sum(p["minutes"] for p in con))
            t_sin = sum(p[s] for p in sin) / max(1.0, sum(p["minutes"] for p in sin))
            if t_con <= 0:
                continue
            ratio = 1 + (t_sin / t_con - 1) * len(sin) / (len(sin) + 8)
            ratio = min(1.35, max(0.75, ratio))
            j.ajuste_bajas[s] = j.ajuste_bajas.get(s, 1.0) * ratio
            if s in ("pts", "reb", "ast") and abs(ratio - 1) >= 0.05:
                cambios.append(f"{s} {ratio - 1:+.0%}/min")
        j.notas.append(f"sin {comp_nombre} ({len(sin)} partidos): {m_sin:.1f} min vs {m_con:.1f} con él"
                       + (f"; {', '.join(cambios)}" if cambios else ""))
    # Varias bajas del mismo puesto no se suman sin límite: los minutos se reparten entre varios.
    return min(6.0, delta_total)


def _cambio_rol(ctx: Contexto, partidos: list[dict]) -> dict[str, float]:
    actual = [p for p in partidos if p["season"] == ctx.temporada]
    anterior = [p for p in partidos if p["season"] != ctx.temporada]
    if not 2 <= len(actual) < 10 or len(anterior) < 10:
        return {}
    m_act = sum(p["minutes"] for p in actual)
    m_ant = sum(p["minutes"] for p in anterior)
    out = {}
    for c in ("pts", "reb", "ast", "tpm"):
        t_ant = sum(p[c] for p in anterior) / m_ant if m_ant else 0
        # Solo estadísticas con volumen (al menos ~1 por partido): en robos o tapones el ruido manda.
        if not m_act or t_ant * m_ant / len(anterior) < 1:
            continue
        r = (sum(p[c] for p in actual) / m_act) / t_ant
        if abs(r - 1) >= CAMBIO_ROL:
            out[c] = r
    return out


def preparar_jugador(ctx: Contexto, player_id: str, nombre: str, team_id: str, opp_id: str,
                     ausentes: list[tuple[str, str]] | None = None,
                     fuera_rival: list[str] | None = None) -> Jugador | None:
    partidos = ctx.por_jugador.get(player_id, [])[:120]
    if not partidos:
        return None
    recientes = partidos[:PARTIDOS_MINUTOS]
    hay_actual = partidos[0]["season"] == ctx.temporada
    w = [DECAY_MINUTOS ** i * (1.0 if p["season"] == ctx.temporada or not hay_actual else PESO_MINUTOS_ANTERIOR)
         for i, p in enumerate(recientes)]
    m = sum(wi * p["minutes"] for wi, p in zip(w, recientes)) / sum(w)
    var_m = sum(wi * (p["minutes"] - m) ** 2 for wi, p in zip(w, recientes)) / sum(w)
    j = Jugador(player_id, nombre, team_id, opp_id, ctx.grupo.get(player_id, "G"), partidos, m,
                max(3.0, math.sqrt(var_m)))
    if partidos[0]["team_id"] != team_id:
        j.notas.append("cambió de equipo hace poco: sus minutos pueden no reflejar su nuevo rol")
    base = j.minutos
    j.minutos = max(0.0, j.minutos + _bajas(ctx, j, ausentes or []))
    techo = max(p["minutes"] for p in recientes) + 2
    if j.minutos > max(base, techo):
        j.minutos = max(base, techo)
        j.notas.append(f"minutos limitados a {j.minutos:.0f} (su máximo reciente + 2)")
    con_equipo = [p for p in partidos if p["team_id"] == team_id and p["season"] == ctx.temporada]
    j.pocos_con_equipo = len(con_equipo) < 3 and any(p["team_id"] != team_id for p in partidos[:15])
    j.cambio_rol = _cambio_rol(ctx, partidos)
    if j.cambio_rol:
        j.notas.append("cambio de rol esta temporada (por minuto): " + ", ".join(
            f"{c} {r - 1:+.0%}" for c, r in j.cambio_rol.items()) + "; se da más peso a la línea de la casa")
    if j.pocos_con_equipo:
        j.notas.append(f"solo {len(con_equipo)} partidos con su equipo actual: su rol puede haber cambiado, "
                       "se da más peso a la línea de la casa")
    ayer = (date.fromisoformat(ctx.fecha) - timedelta(days=1)).isoformat()
    if ctx.ultimo_partido.get(team_id) == ayer and j.minutos > 28:
        j.minutos *= 0.97
        j.notas.append("segundo partido en dos noches: -3% de minutos")
    j.zonas = perfil_zonas(ctx, player_id, opp_id)
    j.enfrentamiento = marcajes.evaluar(ctx.marcajes, player_id, j.grupo, opp_id, set(fuera_rival or ()))
    return j


def perfil_zonas(ctx: Contexto, player_id: str, opp_id: str) -> dict:
    """Reparto de tiros del jugador por zona, su acierto (contraído a la liga) y lo que concede el rival."""
    propias = ctx.zona_jugador.get(player_id, {})
    total = sum(v[0] for v in propias.values())
    out = {}
    for z in ZONAS:
        fga, fgm = propias.get(z, (0.0, 0.0))
        pct_lg, frec_lg = ctx.zona_liga.get(z, (0.0, 0.0))
        out[z] = {
            "intentos": fga,
            "reparto": (fga + 5 * frec_lg) / (total + 5) if total + 5 else frec_lg,
            "pct": (fgm + K_ZONA_JUGADOR * pct_lg) / (fga + K_ZONA_JUGADOR),
            "pct_liga": pct_lg,
            "pct_rival": ctx.zona_rival.get(opp_id, {}).get(z, (pct_lg, frec_lg))[0],
        }
    return out


def _factor_zonas(j: Jugador, solo_triples: bool) -> float:
    num = den = 0.0
    for z, d in j.zonas.items():
        if solo_triples and VALOR[z] != 3:
            continue
        base = d["reparto"] * d["pct"] * (VALOR[z] if not solo_triples else 1)
        den += base
        num += base * (d["pct_rival"] / d["pct_liga"] if d["pct_liga"] else 1.0)
    return num / den if den else 1.0


def predecir(ctx: Contexto, j: Jugador, stat: str) -> Prediccion:
    w = _pesos(j.partidos, ctx.temporada, DECAY_TASA)
    sw_min = sum(wi * p["minutes"] for wi, p in zip(w, j.partidos))
    m_media = sw_min / sum(w)
    liga = ctx.liga.get(j.grupo, {})
    defensa = ctx.defensa.get(j.opp_id, {}).get(j.grupo, {})
    niveles = ctx.nivel.get(j.grupo, {})
    mu_min = 0.0
    fac_rival = fac_tipo = 0.0
    tasa_total = tasa_base = 0.0
    componentes: dict[str, dict] = {}
    if j.motores is None:
        j.motores = motores(ctx, j, w)
    for c in COMPONENTES[stat]:
        tasa = (sum(wi * p[c] for wi, p in zip(w, j.partidos)) + 2 * m_media * liga.get(c, 0.0)) / (sw_min + 2 * m_media)
        tasa_base += tasa
        tasa *= j.ajuste_bajas.get(c, 1.0)
        f_def = defensa.get(c, 1.0)
        if c == "pts":
            f_zona = _factor_zonas(j, solo_triples=False)
            fg_pts = sum(2 * p["fgm"] + p["tpm"] for p in j.partidos) / max(1, sum(p["pts"] for p in j.partidos))
            f_def = math.sqrt(f_def * (1 + fg_pts * (f_zona - 1)))
        elif c == "tpm":
            f_def = math.sqrt(f_def * _factor_zonas(j, solo_triples=True))
        # Cómo le fue contra defensas del mismo nivel que la de hoy.
        nivel_hoy = niveles.get(c, {}).get(j.opp_id)
        f_tipo = 1.0
        if nivel_hoy:
            mismos = [(wi, p) for wi, p in zip(w, j.partidos) if niveles[c].get(p["opp_id"]) == nivel_hoy]
            m_t = sum(wi * p["minutes"] for wi, p in mismos)
            if m_t and tasa:
                t_t = sum(wi * p[c] for wi, p in mismos) / m_t
                f_tipo = math.sqrt(1 + (t_t / tasa - 1) * m_t / (m_t + K_TIPO_MIN))
                f_tipo = min(1.15, max(0.85, f_tipo))
        mu_c = tasa * f_def * f_tipo
        motor = j.motores[c]
        mu_final = PESO_MOTORES * motor.mu + (1 - PESO_MOTORES) * mu_c * j.minutos
        componentes[c] = {"por_tasa": mu_c * j.minutos, "por_motores": motor.mu, "final": mu_final,
                          "explicacion": motor.explicacion, "datos": motor.datos}
        if j.enfrentamiento and c in ("pts", "fgm", "tpm"):
            mu_final *= j.enfrentamiento.factor
            componentes[c]["final"] = mu_final
            componentes[c]["explicacion"] += "; " + marcajes.explicar(j.enfrentamiento)
        mu_c = mu_final / j.minutos if j.minutos else 0.0
        mu_min += mu_c
        tasa_total += tasa
        fac_rival += tasa * f_def
        fac_tipo += tasa * f_tipo
    mu = mu_min * j.minutos
    # Dispersión del propio jugador: residuos frente a su tasa × minutos jugados.
    num = den = 0.0
    for wi, p in zip(w, j.partidos):
        e = tasa_base * p["minutes"]
        num += wi * (valor(p, stat) - e) ** 2
        den += wi * e
    phi = min(3.5, max(1.0, num / den)) if den else 1.0
    var = phi * mu + mu_min ** 2 * j.minutos_sd ** 2
    return Prediccion(stat, mu, var, {
        "minutos": j.minutos, "tasa_min": tasa_total,
        "rival": fac_rival / tasa_total if tasa_total else 1.0,
        "tipo_defensa": fac_tipo / tasa_total if tasa_total else 1.0, "dispersion": phi,
    }, componentes)


# --- Evaluación de una línea ----------------------------------------------------------

@dataclass
class Evaluacion:
    player_id: str
    nombre: str
    stat: str
    line: float
    lado: str               # "más" o "menos"
    prob: float
    prob_modelo: float      # modelo + acierto real, antes de mezclar con la casa
    prob_mercado: float | None
    mu: float
    sd: float
    acierto_10: tuple[int, int]
    acierto_temporada: tuple[int, int]
    vs_rival: list[float]
    media_10: float
    odd: float | None
    factores: dict
    linea_80: tuple[float | None, float | None]
    componentes: dict = field(default_factory=dict)   # de dónde sale la media: ver Prediccion
    metricas: list = field(default_factory=list)      # estadísticas relacionadas: últ. 5/10, temporada, rival
    titular: bool = True                              # suplente = riesgo de que el técnico le dé pocos minutos
    alertas: list = field(default_factory=list)       # motivos para no tomarla como pick "seguro"


def _aciertos(partidos: list[dict], stat: str, line: float, lado: str) -> tuple[int, int]:
    hits = sum((valor(p, stat) > line) if lado == "más" else (valor(p, stat) < line) for p in partidos)
    return hits, len(partidos)


MARGEN_UN_LADO = 1.05      # margen típico cuando la casa solo ofrece un lado y no se puede quitar exacto


def prob_mercado(over_odd: float | None, under_odd: float | None) -> tuple[float | None, float | None]:
    """Probabilidades de más/menos implícitas en las cuotas, sin el margen de la casa."""
    if over_odd and under_odd:
        o, u = 1 / over_odd, 1 / under_odd
        return o / (o + u), u / (o + u)
    return (1 / over_odd / MARGEN_UN_LADO if over_odd else None,
            1 / under_odd / MARGEN_UN_LADO if under_odd else None)


def _prob_jugador(j: Jugador, stat: str, line: float, lado: str, p_mod: float) -> float:
    """Modelo mezclado con su acierto real sobre la línea en los últimos 15 y calibrado."""
    hits, n = _aciertos(j.partidos[:15], stat, line, lado)
    p_emp = (hits + 5 * p_mod) / (n + 5)
    return 0.5 + (PESO_MODELO * p_mod + (1 - PESO_MODELO) * p_emp - 0.5) * CALIBRACION


MINUTOS_SD_ESTABLE = 6.0


def alertas(j: Jugador, stat: str) -> list[str]:
    """Lo que hace dudosa una prop aunque su probabilidad sea alta."""
    out = []
    if not es_titular(j):
        out.append("suplente")
    if j.minutos_sd > MINUTOS_SD_ESTABLE:
        out.append("minutos inestables")
    if set(COMPONENTES[stat]) & set(j.cambio_rol):
        out.append("cambio de rol")
    if j.pocos_con_equipo:
        out.append("traspaso reciente")
    if any(n.startswith("en el parte de lesiones") for n in j.notas):
        out.append("en el parte de lesiones")
    return out


def es_titular(j: Jugador) -> bool:
    return sum(p["starter"] for p in j.partidos[:5]) >= 3


@dataclass
class Segura:
    player_id: str
    nombre: str
    stat: str
    line: float
    prob: float
    mu: float
    media_10: float
    acierto_10: tuple[int, int]

    @property
    def cuota_minima(self) -> float:
        return 1 / self.prob


def seguras(ctx: Contexto, j: Jugador, objetivo: float = PROB_SEGURA) -> list[Segura]:
    """Para titulares estables, la línea de "más de" más alta que pasa con al menos esa probabilidad."""
    if j.minutos < MIN_SEGURA or not es_titular(j):
        return []
    out = []
    ult = j.partidos[:10]
    for stat, minimo in MEDIAS_SEGURA.items():
        media = sum(valor(p, stat) for p in ult) / len(ult)
        if media < minimo:
            continue
        pred = predecir(ctx, j, stat)
        for k in range(int(pred.mu), -1, -1):
            p = _prob_jugador(j, stat, k + 0.5, "más", prob_lados(k + 0.5, pred.mu, pred.var)[0])
            if p >= objetivo:
                out.append(Segura(j.player_id, j.nombre, stat, k + 0.5, p, pred.mu, media,
                                  _aciertos(ult, stat, k + 0.5, "más")))
                break
    return out


def evaluar(ctx: Contexto, j: Jugador, stat: str, line: float, over_odd: float | None = None,
            under_odd: float | None = None, peso_mercado: float = PESO_MERCADO, detalle: bool = True) -> Evaluacion:
    pred = predecir(ctx, j, stat)
    lados = {}
    con_cuota = bool(over_odd or under_odd)
    n_actual = sum(1 for p in j.partidos if p["season"] == ctx.temporada)
    peso_mercado = max(peso_mercado, peso_mercado + (PESO_MERCADO_INICIO - peso_mercado)
                       * max(0.0, 1 - n_actual / PARTIDOS_INICIO))
    if j.pocos_con_equipo:
        peso_mercado = max(peso_mercado, PESO_MERCADO_TRASPASO)
    if set(COMPONENTES[stat]) & set(j.cambio_rol):
        peso_mercado = max(peso_mercado, PESO_MERCADO_CAMBIO_ROL)
    for lado, p_mod, odd, p_casa in zip(("más", "menos"), prob_lados(line, pred.mu, pred.var),
                                        (over_odd, under_odd), prob_mercado(over_odd, under_odd)):
        if con_cuota and not odd:
            continue  # la casa no ofrece este lado: no se puede apostar
        p_jug = _prob_jugador(j, stat, line, lado, p_mod)
        final = p_jug if p_casa is None else (1 - peso_mercado) * p_jug + peso_mercado * p_casa
        lados[lado] = (final, p_jug, p_casa, odd)
    lado = max(lados, key=lambda k: lados[k][0])
    prob, p_jug, p_casa, odd = lados[lado]
    temporada = [p for p in j.partidos if p["season"] == ctx.temporada]
    vs = [valor(p, stat) for p in j.partidos if p["opp_id"] == j.opp_id][:5]
    return Evaluacion(
        j.player_id, j.nombre, stat, line, lado, prob, p_jug, p_casa, pred.mu, math.sqrt(pred.var),
        _aciertos(j.partidos[:10], stat, line, lado), _aciertos(temporada, stat, line, lado), vs,
        sum(valor(p, stat) for p in j.partidos[:10]) / min(10, j.n), odd, pred.factores,
        linea_segura(pred.mu, pred.var), pred.componentes,
        tabla_metricas(ctx, j, COMPONENTES[stat]) if detalle else [], es_titular(j), alertas(j, stat),
    )


def mejor_contra(ctx: Contexto, j: Jugador, stat: str) -> dict[str, float]:
    """Rendimiento por minuto del jugador contra defensas fuertes, medias y débiles (1 = su media)."""
    # En las combinadas se usa el nivel de la defensa en la primera componente (puntos o rebotes).
    niveles = ctx.nivel.get(j.grupo, {}).get(COMPONENTES[stat][0], {})
    out = {}
    total = sum(valor(p, stat) for p in j.partidos) / max(1.0, sum(p["minutes"] for p in j.partidos))
    for nivel in ("fuerte", "media", "débil"):
        ps = [p for p in j.partidos if niveles.get(p["opp_id"]) == nivel]
        mins = sum(p["minutes"] for p in ps)
        if mins >= 60 and total:
            out[nivel] = (sum(valor(p, stat) for p in ps) / mins) / total
    return out
