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
import unicodedata
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date, timedelta

from ..model import negbin_pmf
from .desglose import Motor, motores, promedios_equipo, tabla_metricas, tasas_liga, totales_por_partido
from . import marcajes
from .espn import grupo_posicion
from . import pbpstats
from .sgo import clave_nombre
from .zonas import NOMBRES as NOMBRE_ZONA
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
# Las defensivas y las pérdidas salían conservadoras con 0.9 (backtest 2025-26, 4.262 props de cada una: robos del
# 70-80 % acertaban 76.7 % prometiendo 74.7 %). Con estos valores quedan calibradas y mejora el log-loss.
CALIBRACION_STAT = {"steals": 1.0, "blocks": 0.95, "stocks": 1.0, "turnovers": 1.0}
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
    altura: dict = field(default_factory=dict)          # jugador -> estatura (pulgadas)
    altura_rival: dict = field(default_factory=dict)    # equipo -> grupo -> estatura media por minutos
    margen: dict = field(default_factory=dict)          # equipo -> por cuánto se espera que gane hoy (± puntos)
    pbp: dict = field(default_factory=dict)             # pbpstats.com (pbpstats.cargar), si se bajó
    jug_equipo: dict = field(default_factory=dict)      # (partido, equipo) -> jugada a jugada del equipo (jugadas.py)
    tipos_jugador: dict = field(default_factory=dict)   # jugador -> partido -> tipo de tiro -> fila (jugadas.py)
    tipos_equipo: dict = field(default_factory=dict)    # equipo -> partido -> tipo de tiro -> fila
    siglas: dict = field(default_factory=dict)          # equipo -> siglas de ESPN


def _peso_temporada(season: int, actual: int) -> float:
    return 1.0 if season == actual else PESO_TEMPORADA_ANTERIOR


# Diferencia de estatura con los rivales de su posición (pulgadas). Residuos del modelo, nov 2025-mar 2026
# (13.390 partidos de jugador): rebotes +0.67 % por pulgada (t = 2.9), tapones +1.5 % (t = 2.0), triples
# +0.7 % (t = 1.8), puntos +0.4 % (t = 1.9), asistencias sin efecto claro. Se usa la mitad de cada
# pendiente (contracción) y como mucho ±6 %.
EFECTO_ALTURA = {"reb": 0.0035, "blk": 0.0075, "tpm": 0.0035, "pts": 0.002, "fgm": 0.002}
TOPE_ALTURA = 0.06
PARTIDOS_ALTURA_RIVAL = 10


def _alturas(conn, filas: list[dict], grupo: dict[str, str]) -> tuple[dict, dict]:
    try:
        altura = {r[0]: r[1] for r in conn.execute("SELECT player_id, altura FROM nba_alturas WHERE altura > 0")}
    except Exception:
        return {}, {}
    if not altura:
        return {}, {}
    juegos: dict[str, list] = defaultdict(list)
    for f in filas:
        if f["game_id"] not in juegos[f["team_id"]]:
            juegos[f["team_id"]].append(f["game_id"])
    recientes = {t: set(g[:PARTIDOS_ALTURA_RIVAL]) for t, g in juegos.items()}
    acc = defaultdict(lambda: defaultdict(lambda: [0.0, 0.0]))
    for f in filas:
        if f["player_id"] in altura and f["game_id"] in recientes[f["team_id"]]:
            a = acc[f["team_id"]][grupo[f["player_id"]]]
            a[0] += f["minutes"] * altura[f["player_id"]]
            a[1] += f["minutes"]
    return altura, {t: {g: x / n for g, (x, n) in por_g.items() if n} for t, por_g in acc.items()}


def _unir_jugadas(conn, filas: list[dict], desde: str) -> dict:
    """Añade a cada partido de jugador sus oportunidades de rebote y transición (jugadas.py), si están."""
    try:
        rows = conn.execute(
            """SELECT j.* FROM nba_jugadas j JOIN nba_games g ON g.id = j.game_id WHERE g.fecha >= ?""",
            (desde,)).fetchall()
    except Exception:
        return {}
    por_jugador, por_equipo = {}, {}
    for r in rows:
        r = dict(r)
        if r["player_id"].startswith("equipo:"):
            por_equipo[(r["game_id"], r["team_id"])] = r
        else:
            por_jugador[(r["game_id"], r["player_id"])] = r
    for f in filas:
        j = por_jugador.get((f["game_id"], f["player_id"]))
        if j:
            f.update({"dreb_op": j["dreb_op"], "oreb_op": j["oreb_op"], "trans_pts": j["trans_pts"],
                      "trans_fga": j["trans_fga"], "comp_fga": j.get("comp_fga"), "comp_fgm": j.get("comp_fgm"),
                      "comp_xfgm": j.get("comp_xfgm"), "stl_op": j.get("stl_op"), "blk_op": j.get("blk_op")})
    return por_equipo


def _cargar_tipos(conn, desde: str) -> tuple[dict, dict]:
    try:
        rows = conn.execute("""SELECT t.*, g.fecha, g.season FROM nba_tiros_tipo t JOIN nba_games g ON g.id = t.game_id
                               WHERE g.fecha >= ?""", (desde,)).fetchall()
    except Exception:
        return {}, {}
    jug: dict = defaultdict(lambda: defaultdict(dict))
    eq: dict = defaultdict(lambda: defaultdict(dict))
    for r in rows:
        r = dict(r)
        if r["player_id"].startswith("equipo:"):
            eq[r["team_id"]][r["game_id"]][r["tipo"]] = r
        else:
            jug[r["player_id"]][r["game_id"]][r["tipo"]] = r
    return jug, eq


def construir_contexto(conn, fecha: str, dias: int = 420) -> Contexto:
    desde = (date.fromisoformat(fecha) - timedelta(days=dias)).isoformat()
    filas = [dict(r) for r in conn.execute(
        """SELECT pg.*, g.fecha, g.season FROM nba_player_games pg JOIN nba_games g ON g.id = pg.game_id
           WHERE g.fecha < ? AND g.fecha >= ? AND g.season_type IN (2, 3, 5) ORDER BY g.fecha DESC""",
        (fecha, desde))]
    jug_equipo = _unir_jugadas(conn, filas, desde)
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
    ctx = Contexto(fecha, temporada, filas, por_jugador, grupo, liga, defensa, nivel, zona_liga, zona_rival,
                   zona_jugador, ritmo, ritmo_liga, ultimo, equipo_partido, equipo_prom, liga_equipo, liga_motor,
                   marcajes.construir(conn, fecha, desde, grupo), *_alturas(conn, filas, grupo),
                   _margenes(conn, fecha, temporada))
    ctx.pbp = pbpstats.cargar(conn, temporada)
    ctx.jug_equipo = jug_equipo
    ctx.tipos_jugador, ctx.tipos_equipo = _cargar_tipos(conn, desde)
    try:
        ctx.siglas = {r[0]: r[1] for r in conn.execute("SELECT id, abbr FROM nba_teams")}
    except Exception:
        ctx.siglas = {}
    return ctx


# Partido desigual. Sin hándicap de la casa se estima con la diferencia media de puntos de cada equipo (temporada
# anterior a la mitad, K_MARGEN partidos de 0 para encoger) y LOCALIA puntos para el local; en 2025-26 el margen
# real sigue a esta estimación con pendiente 0.96.
K_MARGEN = 5
LOCALIA = 2.0


def _margenes(conn, fecha: str, temporada: int) -> dict[str, float]:
    # Bases abiertas sin NbaDB (backtest) pueden no tener aún la columna del hándicap.
    con_casa = "margen_esperado" in {r[1] for r in conn.execute("PRAGMA table_info(nba_games)")}
    hoy = conn.execute(f"SELECT home_id, away_id, {'margen_esperado' if con_casa else 'NULL'} FROM nba_games "
                       "WHERE fecha = ?", (fecha,)).fetchall()
    if not hoy:
        return {}
    neto: dict[str, list[float]] = defaultdict(lambda: [0.0, 0.0])
    for g in conn.execute(
            """SELECT home_id, away_id, home_pts, away_pts, season FROM nba_games WHERE fecha < ? AND season >= ?
               AND season_type = 2 AND home_pts IS NOT NULL""", (fecha, temporada - 1)):
        w = 1.0 if g[4] == temporada else PESO_TEMPORADA_ANTERIOR
        for t, m in ((g[0], g[2] - g[3]), (g[1], g[3] - g[2])):
            neto[t][0] += w * m
            neto[t][1] += w
    media = {t: v[0] / (v[1] + K_MARGEN) for t, v in neto.items()}
    out = {}
    for local, visita, casa in hoy:
        m = casa if casa is not None else media.get(local, 0.0) - media.get(visita, 0.0) + LOCALIA
        out[local], out[visita] = m, -m
    return out


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
    diferencia_altura: float | None = None   # su estatura menos la media de los rivales de su posición
    cambio_rol: dict[str, float] = field(default_factory=dict)   # stat básica -> tasa actual / anterior
    factor_paliza: float = 1.0               # minutos por partido desigual (ver PALIZA)
    bajas_rival: list[str] = field(default_factory=list)   # titulares del rival que no juegan
    bajas_rival_ids: list[str] = field(default_factory=list)
    sin_estrella: list[str] = field(default_factory=list)  # estrellas de su equipo que no juegan hoy
    factor_transicion: float = 1.0           # puntos según el contraataque que concede el rival (ver TRANSICION)
    mezcla_tiros: dict = field(default_factory=dict)   # tipo de tiro -> (parte de sus tiros, acierto) (ver TIPOS)
    suerte_companeros: float | None = None   # canastas de sus compañeros con él en pista / las esperadas (últimos 10)
    asistencias_esperadas: float | None = None   # sus asistencias por partido si sus compañeros tiraran a su nivel
    factor_suerte: float = 1.0               # corrección de sus asistencias por esa racha (ver SUERTE_ASISTENCIAS)
    factor_tipos: float = 1.0                # lo que deja el rival en sus tipos de tiro frente a la media
    punteria: float | None = None            # sus canastas / las esperadas por tipo de tiro (últimos 10)
    rival_cansado: bool = False              # el rival jugó anoche y él no (ver RIVAL_CANSADO)
    cansado_no_favorito: bool = False        # jugó anoche y hoy es no favorito (ver NO_FAVORITO_CANSADO)
    transicion_rival: float | None = None    # contraataque que concede el rival frente a la media (1 = media)

    @property
    def n(self) -> int:
        return len(self.partidos)


# Factor de paliza: 2025-26 (18.694 partidos de jugador, margen esperado sin hándicap real). Con 12+ puntos de
# diferencia esperada, los titulares de 28+ minutos jugaron un 3-4 % menos de lo previsto y produjeron un 3 % menos
# (pra 0.97 frente a 1.00 en partidos parejos), favoritos y no favoritos por igual; los de menos de 24 minutos, un
# 4 % más. Entre 9 y 12 puntos el efecto es la mitad o menos. No aumenta la dispersión de los minutos ni el riesgo
# de que fallen juntas varias piernas del mismo partido (4 titulares: 0.88 de lo independiente, igual que en
# partidos parejos), así que solo se baja la media.
# Bajas del rival: 2025-26 (15.080 partidos de jugador, titulares = 26+ min de media en sus últimos 10). Con un
# titular del rival fuera, el jugador hizo +2 % de puntos y +1.5 % de asistencias frente a lo esperado; con tres o
# más, +5 % y +3 %. Rebotes, sin efecto. Da igual que la baja sea de su posición o de otra (defensa de equipo).
BAJAS_RIVAL = {"pts": 0.017, "fgm": 0.017, "tpm": 0.017, "ftm": 0.017, "fta": 0.017, "ast": 0.015}
BAJAS_RIVAL_MAX = 3
TITULAR_MIN = 26.0

# Estrella ausente: 2024-25 y 2025-26 (1.107 partidos de compañeros con 20+ min). Cuando falta el jugador que más
# jugadas usa (28+ min y 20+ jugadas de tiro por 36'), sus compañeros hicieron por minuto +15 % de tiros y de puntos,
# +8 % de triples, +25 % de tiros libres y +12 % de asistencias frente a su ritmo con él (con la estrella jugando, la
# misma cuenta da 0.98-1.03), y la media ponderada que usaba el modelo seguía corta aunque llevara 3-5 partidos fuera.
# En el backtest de 2025-26 (4.068 jugadores en partidos sin su estrella) la mitad de ese efecto es lo que deja el
# error medio en cero (puntos: +0.13 antes, -0.06 con la mitad, -0.49 con el efecto entero) y mejora el log-loss de
# todas las estadísticas; los "menos de puntos" del 62 %+ pasan de acertar 63 % (prometían 67 %) a 67 % (67 %).
# 2 nov 2026: sin Anthony Edwards, el modelo dio a LaMelo 16 puntos (menos de 20.5 al 58 %) y metió 24 al descanso.
ESTRELLA_MIN = 28.0
ESTRELLA_USO_36 = 20.0
ESTRELLA_EFECTO = {"pts": 1.075, "fgm": 1.075, "tpm": 1.04, "ftm": 1.125, "fta": 1.125, "ast": 1.06, "reb": 1.02}
K_ESTRELLA = 8          # partidos "virtuales" del efecto medio que se suman a los suyos sin la estrella
ESTRELLA_TOPE = (0.85, 1.40)
NOMBRE_CORTO = {"pts": "puntos", "ast": "asistencias", "tpm": "triples"}
SUBEN_SIN_ESTRELLA = {"pts", "fgm", "tpm", "ftm", "ast"}   # un "menos" de estas no entra en combinadas

# Transición (jugadas.py): puntos al contraataque que concede el rival frente a la media de la liga, encogido con
# sus partidos (K_TRANSICION). Backtest 2025-26 (4.949 titulares, puntos): frente a rivales que conceden 12 %+
# más, los que sacan 15 %+ de sus puntos al contraataque anotaron un 4 % más de lo previsto; frente a los que
# conceden 12 %+ menos, un 10 % menos (los que no corren, -4 %). Los "menos" de puntos del 60 %+ contra rivales
# que conceden mucho acertaron 58.9 % prometiendo 66.3 % (n = 180).
TRANSICION_PENDIENTE = 1.75     # rival que concede poco: pendiente × % de sus puntos al contraataque × (concede − 1)
TRANSICION_PENDIENTE_ALTA = 2.9  # rival que concede mucho: solo lo que corra por encima de TRANSICION_CORRE
TRANSICION_CORRE = 0.08
TRANSICION_TOPE = 0.08
K_TRANSICION = 10
TRANSICION_ALTA = 1.12

# Rival en el segundo partido de dos noches seguidas (y él descansado). 2024-26 (2.672 partidos de titulares, frente
# a 15.030 con los dos descansados): +1.5 % de puntos y +2.3 % de asistencias por minuto; rebotes y triples, menos
# de +1 %. Si los dos jugaron anoche, se compensa (ya hay -3 % de minutos por su propio cansancio).
RIVAL_CANSADO = {"pts": 0.015, "fgm": 0.015, "ast": 0.02}

# Asistencias y puntería de los compañeros (jugadas.py: tiros de sus compañeros con él en pista y los que se esperaba
# que metieran según el tipo de tiro; lo que mide la "conversión de asistencias potenciales" de stats.nba.com).
# Backtest 2025-26 (2.672 titulares con 3+ asistencias): con los compañeros fríos en sus últimos 10 (10 % más frío,
# 0.95 o menos de lo esperado) sus asistencias salieron un 6 % por encima de lo previsto y los "menos" del 60 %+
# acertaron 59.3 % prometiendo 67.6 %; con los compañeros calientes, un 3 % por debajo.
SUERTE_PENDIENTE = 0.6             # compañeros fríos: sus asistencias vuelven a subir
SUERTE_PENDIENTE_CALIENTES = 0.25  # compañeros calientes: bajan menos de lo que suben las de los fríos
SUERTE_TOPE = 0.08
SUERTE_MIN_PARTIDOS = 5

PALIZA = {"titular": -0.03, "suplente": 0.04}
PALIZA_DESDE, PALIZA_PLENO = 9.0, 12.0


# Segundo partido en dos noches siendo no favorito por NO_FAVORITO_CANSADO+ puntos: los "más" de titulares a la línea
# más alta con 62 %+ acertaron 49.4 % prometiendo 65.8 % esta temporada (24 oct-7 nov 2026, 83 patas) y 62.2 % frente a
# 65.8 % en 2025-26 (325); con el resto de patas al +3 %. Randle 28+ PRA el 8 nov 2026 (BKN, perdió por 37): 21. Llevan
# la alerta "segunda noche y no favorito" y no entran en combinadas ni bet builders.
NO_FAVORITO_CANSADO = 5.0


def factor_paliza(minutos: float, margen: float) -> float:
    t = min(1.0, max(0.0, (abs(margen) - PALIZA_DESDE) / (PALIZA_PLENO - PALIZA_DESDE)))
    if minutos >= 28:
        return 1 + PALIZA["titular"] * t
    if minutos < 24:
        return 1 + PALIZA["suplente"] * t
    return 1.0


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
        estrella = _es_estrella(recientes)
        if estrella:
            j.sin_estrella.append(comp_nombre)
            _ajuste_estrella(ctx, j, comp, comp_nombre)
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
            if not estrella:
                j.notas.append(f"sin {comp_nombre}: muestra insuficiente ({len(sin)} partidos sin él)")
            continue
        m_con = sum(p["minutes"] for p in con) / len(con)
        m_sin = sum(p["minutes"] for p in sin) / len(sin)
        # Solo se suman minutos: la baja de un compañero no quita minutos, y cuando los datos dicen lo
        # contrario suele ser porque esos partidos fueron de descanso o ya decididos.
        delta = min(4.0, max(0.0, (m_sin - m_con) * len(sin) / (len(sin) + 4)))
        delta_total += delta
        cambios = []
        for s in ([] if estrella else BASICAS):   # con la estrella, las tasas ya las ajustó _ajuste_estrella
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


def _transicion(ctx: Contexto, j: Jugador) -> None:
    concede = _por_equipo_temporada(ctx, "trans_pts", propio=False)
    n = _por_equipo_temporada(ctx, "trans_pts", propio=False, contar=True).get(j.opp_id, 0)
    if j.opp_id not in concede or len(concede) < 20:
        return
    liga = sum(concede.values()) / len(concede)
    rel = 1 + (concede[j.opp_id] / liga - 1) * n / (n + K_TRANSICION)
    j.transicion_rival = rel
    prev = [p for p in j.partidos[:10] if p.get("trans_pts") is not None]
    puntos = sum(p["pts"] for p in prev)
    if len(prev) < 3 or not puntos:
        return
    corre = sum(p["trans_pts"] for p in prev) / puntos
    if rel < 1:   # un rival que no deja correr le quita a todos, más a los que corren
        efecto = TRANSICION_PENDIENTE * corre * (rel - 1)
    else:         # uno que deja correr solo ayuda a los que corren
        efecto = TRANSICION_PENDIENTE_ALTA * max(0.0, corre - TRANSICION_CORRE) * (rel - 1)
    efecto = max(-TRANSICION_TOPE, min(TRANSICION_TOPE, efecto))
    j.factor_transicion = 1 + efecto


# Tipos de tiro (jugadas.py): su mezcla en los últimos TIPOS_PARTIDOS partidos y lo que deja el rival en cada tipo
# esta temporada (puntos por tiro de los equipos que le juegan, encogido con K_TIPOS tiros de media de liga).
# Solo explica: en el backtest de 2025-26 (4.949 titulares) el emparejamiento por tipos no movió los puntos ni los
# triples respecto a lo que ya preveía el modelo (zonas de tiro y defensa por posición), así que no entra en la media.
TIPOS_PARTIDOS = 15
K_TIPOS = 150.0


def _defensa_tipos(ctx: Contexto) -> tuple[dict, dict]:
    """equipo -> tipo -> puntos por tiro que deja (encogido); y la media de liga por tipo. Una vez por contexto."""
    if getattr(ctx, "_def_tipos", None) is None:
        temporada = {f["game_id"]: f["team_id"] for f in ctx.filas if f.get("season") == ctx.temporada}
        rival_de = {}
        for f in ctx.filas:
            if f.get("season") == ctx.temporada:
                rival_de[(f["game_id"], f["team_id"])] = f["opp_id"]
        acc = defaultdict(lambda: defaultdict(lambda: [0.0, 0.0]))
        liga = defaultdict(lambda: [0.0, 0.0])
        for tid, partidos in ctx.tipos_equipo.items():
            for gid, tipos in partidos.items():
                defensor = rival_de.get((gid, tid))
                if gid not in temporada or not defensor:
                    continue
                for tipo, r in tipos.items():
                    acc[defensor][tipo][0] += r["pts"]
                    acc[defensor][tipo][1] += r["fga"]
                    liga[tipo][0] += r["pts"]
                    liga[tipo][1] += r["fga"]
        media = {t: p / a for t, (p, a) in liga.items() if a}
        ctx._def_tipos = ({e: {t: (p + K_TIPOS * media.get(t, 0)) / (a + K_TIPOS) for t, (p, a) in d.items()}
                           for e, d in acc.items()}, media)
    return ctx._def_tipos


def _tipos(ctx: Contexto, j: Jugador) -> None:
    partidos = ctx.tipos_jugador.get(j.player_id, {})
    ult = [partidos[p["game_id"]] for p in j.partidos[:TIPOS_PARTIDOS] if p["game_id"] in partidos]
    if len(ult) < 3:
        return
    tot = defaultdict(lambda: [0, 0])
    for tipos in ult:
        for tipo, r in tipos.items():
            tot[tipo][0] += r["fga"]
            tot[tipo][1] += r["fgm"]
    fga = sum(a for a, _ in tot.values())
    if not fga:
        return
    j.mezcla_tiros = {t: (a / fga, m / a if a else 0.0) for t, (a, m) in tot.items()}
    defensa, media = _defensa_tipos(ctx)
    rival = defensa.get(j.opp_id)
    if not rival:
        return
    num = den = 0.0
    for t, (parte, _) in j.mezcla_tiros.items():
        if media.get(t):
            num += parte * rival.get(t, media[t]) / media[t]
            den += parte
    if den:
        j.factor_tipos = num / den


def _suerte_companeros(j: Jugador) -> None:
    prev = [p for p in j.partidos[:10] if p.get("comp_xfgm")]
    if len(prev) < SUERTE_MIN_PARTIDOS:
        return
    metidas = sum(p["comp_fgm"] for p in prev)
    esperadas = sum(p["comp_xfgm"] for p in prev)
    if not esperadas or not metidas:
        return
    j.suerte_companeros = metidas / esperadas
    j.asistencias_esperadas = sum(p["ast"] for p in prev) / len(prev) / j.suerte_companeros
    pendiente = SUERTE_PENDIENTE if j.suerte_companeros < 1 else SUERTE_PENDIENTE_CALIENTES
    j.factor_suerte = 1 + max(-SUERTE_TOPE, min(SUERTE_TOPE, pendiente * (1 - j.suerte_companeros)))


# Su propia puntería: canastas en sus últimos 10 frente a las esperadas por tipo de tiro (2 o 3). Backtest 2025-26
# (4.992 titulares): los fríos (25 % más frío, 0.95 o menos) anotaron un 1.3 % más de lo previsto y los calientes
# (10 % más caliente) un 2 % menos; los "menos" de puntos del 60 %+ de un jugador frío acertaron 54.3 % prometiendo
# 65.0 % (n = 177): vuelve a meter lo de siempre.
PUNTERIA_PENDIENTE = 0.1
PUNTERIA_TOPE = 0.03
PUNTERIA_FRIA = 0.95


def _punteria(ctx: Contexto, j: Jugador) -> None:
    from .jugadas import ACIERTO_TIPO
    partidos = ctx.tipos_jugador.get(j.player_id, {})
    ult = [partidos[p["game_id"]] for p in j.partidos[:10] if p["game_id"] in partidos]
    if len(ult) < 5:
        return
    metidas = esperadas = 0.0
    for tipos in ult:
        for tipo, r in tipos.items():
            p2, p3 = ACIERTO_TIPO.get(tipo, (0.5, 0.35))
            metidas += r["fgm"]
            esperadas += (r["fga"] - r["tpa"]) * p2 + r["tpa"] * p3
    if esperadas >= 10:
        j.punteria = metidas / esperadas


def _es_estrella(recientes: list[dict]) -> bool:
    """El que más tiros usa de su equipo: 28+ minutos y 20+ jugadas de tiro (tiros + 0.44 libres + pérdidas) por 36'."""
    if len(recientes) < 3:
        return False
    mins = sum(p["minutes"] for p in recientes)
    uso = sum(p["fga"] + 0.44 * p["fta"] + p["tov"] for p in recientes)
    return mins / len(recientes) >= ESTRELLA_MIN and mins and uso * 36 / mins >= ESTRELLA_USO_36


def _ajuste_estrella(ctx: Contexto, j: Jugador, comp: list[dict], comp_nombre: str) -> None:
    """Sube sus tasas por minuto a lo que hacen los compañeros sin la estrella (ESTRELLA_EFECTO sobre su ritmo
    normal), corregido con sus propios partidos sin ella (K_ESTRELLA partidos virtuales), y descuenta lo que la
    media ponderada del modelo ya recoge de esos partidos."""
    juegos_comp = {p["game_id"] for p in comp}
    temporadas = {p["season"] for p in comp if p["team_id"] == j.team_id}
    w = _pesos(j.partidos, ctx.temporada, DECAY_TASA)
    es_sin = [p["team_id"] == j.team_id and p["season"] in temporadas and p["game_id"] not in juegos_comp
              for p in j.partidos]
    # Su ritmo "normal": todos sus partidos menos los que jugó sin la estrella (con ella o en otro equipo).
    normal = [(wi, p) for wi, p, x in zip(w, j.partidos, es_sin) if not x]
    sin = [p for p, x in zip(j.partidos, es_sin) if x and p["minutes"] > 0][:20]
    m_normal = sum(wi * p["minutes"] for wi, p in normal)
    m_todo = sum(wi * p["minutes"] for wi, p in zip(w, j.partidos))
    if len(normal) < 5 or not m_normal or not m_todo:
        return
    min_hoy = max(j.minutos, 1.0)
    m_sin = sum(p["minutes"] for p in sin)
    cambios = []
    for s, efecto in ESTRELLA_EFECTO.items():
        t_normal = sum(wi * p[s] for wi, p in normal) / m_normal
        t_modelo = sum(wi * p[s] for wi, p in zip(w, j.partidos)) / m_todo
        if t_normal <= 0 or t_modelo <= 0:
            continue
        objetivo = (sum(p[s] for p in sin) + K_ESTRELLA * min_hoy * t_normal * efecto) / (m_sin + K_ESTRELLA * min_hoy)
        ratio = min(ESTRELLA_TOPE[1], max(ESTRELLA_TOPE[0], objetivo / t_modelo))
        j.ajuste_bajas[s] = min(ESTRELLA_TOPE[1], j.ajuste_bajas.get(s, 1.0) * ratio)
        if s in ("pts", "ast", "tpm"):
            cambios.append(f"{NOMBRE_CORTO[s]} {ratio - 1:+.0%}")
    j.notas.append(f"sin {comp_nombre}, la estrella de su equipo ({len(sin)} partidos suyos sin él): "
                   f"más tiros y balón para él por minuto ({', '.join(cambios)})")


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
    j.rival_cansado = ctx.ultimo_partido.get(opp_id) == ayer and ctx.ultimo_partido.get(team_id) != ayer
    if ctx.ultimo_partido.get(team_id) == ayer and j.minutos > 28:
        j.minutos *= 0.97
        j.notas.append("segundo partido en dos noches: -3% de minutos")
    margen = ctx.margen.get(team_id)
    j.cansado_no_favorito = (ctx.ultimo_partido.get(team_id) == ayer and margen is not None
                             and margen <= -NO_FAVORITO_CANSADO)
    if margen is not None:
        j.factor_paliza = factor_paliza(j.minutos, margen)
        if j.factor_paliza != 1.0:
            j.minutos *= j.factor_paliza
            j.notas.append(f"partido desigual ({'favorito' if margen > 0 else 'no favorito'} por {abs(margen):.1f}): "
                           f"{'los titulares' if j.factor_paliza < 1 else 'los suplentes'} suelen jugar "
                           f"{(j.factor_paliza - 1) * 100:+.0f}% de minutos si se rompe")
    _transicion(ctx, j)
    _tipos(ctx, j)
    _suerte_companeros(j)
    _punteria(ctx, j)
    j.zonas = perfil_zonas(ctx, player_id, opp_id)
    if player_id in ctx.altura and ctx.altura_rival.get(opp_id, {}).get(j.grupo):
        j.diferencia_altura = ctx.altura[player_id] - ctx.altura_rival[opp_id][j.grupo]
    j.enfrentamiento = marcajes.evaluar(ctx.marcajes, player_id, j.grupo, opp_id, set(fuera_rival or ()))
    hace_10 = (date.fromisoformat(ctx.fecha) - timedelta(days=10)).isoformat()
    for pid in fuera_rival or ():
        rec = ctx.por_jugador.get(pid, [])[:10]
        if rec and rec[0]["fecha"] >= hace_10 and sum(p["minutes"] for p in rec) / len(rec) >= TITULAR_MIN:
            j.bajas_rival.append(rec[0]["name"])
            j.bajas_rival_ids.append(pid)
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
        sin_bajas = tasa
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
            if m_t and sin_bajas:
                # Contra su propio ritmo, no contra el ajustado por bajas (eso ya está en la tasa).
                t_t = sum(wi * p[c] for wi, p in mismos) / m_t
                f_tipo = math.sqrt(1 + (t_t / sin_bajas - 1) * m_t / (m_t + K_TIPO_MIN))
                f_tipo = min(1.15, max(0.85, f_tipo))
        mu_c = tasa * f_def * f_tipo
        motor = j.motores[c]
        mu_final = PESO_MOTORES * motor.mu + (1 - PESO_MOTORES) * mu_c * j.minutos
        componentes[c] = {"por_tasa": mu_c * j.minutos, "por_motores": motor.mu, "final": mu_final,
                          "explicacion": motor.explicacion, "datos": motor.datos}
        if j.diferencia_altura is not None and c in EFECTO_ALTURA:
            ajuste = min(1 + TOPE_ALTURA, max(1 - TOPE_ALTURA, 1 + EFECTO_ALTURA[c] * j.diferencia_altura))
            mu_final *= ajuste
            componentes[c]["final"] = mu_final
            componentes[c]["altura"] = ajuste
        if j.bajas_rival and c in BAJAS_RIVAL:
            mu_final *= 1 + BAJAS_RIVAL[c] * min(len(j.bajas_rival), BAJAS_RIVAL_MAX)
            componentes[c]["final"] = mu_final
        if j.factor_suerte != 1.0 and c == "ast":
            mu_final *= j.factor_suerte
            componentes[c]["final"] = mu_final
        if j.punteria is not None and c in ("pts", "fgm"):
            mu_final *= 1 + max(-PUNTERIA_TOPE, min(PUNTERIA_TOPE, PUNTERIA_PENDIENTE * (1 - j.punteria)))
            componentes[c]["final"] = mu_final
        if j.rival_cansado and c in RIVAL_CANSADO:
            mu_final *= 1 + RIVAL_CANSADO[c]
            componentes[c]["final"] = mu_final
        if j.factor_transicion != 1.0 and c in ("pts", "fgm"):
            mu_final *= j.factor_transicion
            componentes[c]["final"] = mu_final
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
    defensa: str = ""                                 # cómo defiende el rival esta estadística, en una línea
    razones: list = field(default_factory=list)       # el razonamiento completo, factor por factor
    argumentos: list = field(default_factory=list)    # lo esencial en 4-7 datos concretos (ver argumentos())


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


# "Menos de" en puntos y combinadas con puntos de anotadores de 20+ al inicio de temporada: backtest del
# 22 oct-25 nov 2025, prometía 67.3 % y acertó 59.5 % (a mitad de temporada, 66.8 % y 69.1 %: bien). Las
# estrellas arrancan fuertes y suben minutos. Se acerca su probabilidad a 50 % y queda fuera de combinadas.
CORRECCION_MENOS_ESTRELLA = 0.6
ESTRELLA_PUNTOS = 20.0


def _menos_estrella_inicio(ctx: Contexto, j: Jugador, stat: str) -> bool:
    if "pts" not in COMPONENTES[stat]:
        return False
    if sum(1 for p in j.partidos if p["season"] == ctx.temporada) >= PARTIDOS_INICIO:
        return False
    ult = j.partidos[:10]
    return sum(p["pts"] for p in ult) / len(ult) >= ESTRELLA_PUNTOS


GRUPOS_TEXTO = {"G": "bases/escoltas", "F": "aleros/ala-pívots", "C": "pívots"}
COMPONENTES_NOMBRE = {"pts": "points", "reb": "rebounds", "ast": "assists", "tpm": "threes", "stl": "steals",
                      "blk": "blocks", "tov": "turnovers", "fgm": "fgm", "ftm": "ftm", "fta": "fta"}


def _pulgadas(x: float) -> str:
    return f"{int(x // 12)}'{int(round(x % 12))}\""


def razones(ctx: Contexto, j: Jugador, stat: str, line: float, lado: str, pred: Prediccion) -> list[str]:
    """Cada factor del pick en una línea, marcado a favor (✅), en contra (❌) o neutro (➖) del lado elegido."""
    signo = 1 if lado == "más" else -1

    def marca(efecto: float, umbral: float = 0.02) -> str:
        return "✅" if efecto * signo > umbral else "❌" if efecto * signo < -umbral else "➖"

    out = []
    sd = j.minutos_sd
    out.append(f"{'✅' if sd <= MINUTOS_SD_ESTABLE and es_titular(j) else '❌'} Minutos: {j.minutos:.1f} esperados "
               f"({'titular' if es_titular(j) else 'suplente'}, ±{sd:.1f}).")
    ult5 = [valor(p, stat) for p in j.partidos[:5]]
    temp = [valor(p, stat) for p in j.partidos if p["season"] == ctx.temporada]
    ant = [valor(p, stat) for p in j.partidos if p["season"] != ctx.temporada][:60]
    if ult5:
        media5 = sum(ult5) / len(ult5)
        texto = f"Forma: {media5:.1f} en sus últimos 5"
        if temp:
            texto += f", {sum(temp) / len(temp):.1f} esta temporada ({len(temp)} partidos)"
        if ant:
            texto += f", {sum(ant) / len(ant):.1f} la temporada pasada"
        out.append(f"{marca((media5 - line) / max(line, 1), 0.05)} {texto} (línea {line:g}).")
    for c, d in pred.componentes.items():
        out.append(f"➖ Cómo produce {NOMBRES[COMPONENTES_NOMBRE.get(c, stat)]}: {d['explicacion'].split('; marcaje')[0]}.")
    rival = pred.factores.get("rival", 1) - 1
    out.append(f"{marca(rival)} Defensa: {texto_defensa(ctx, j, stat, pred)}.")
    if j.diferencia_altura is not None and abs(j.diferencia_altura) >= 1.5 and any(
            c in EFECTO_ALTURA for c in COMPONENTES[stat]):
        efecto = sum(d.get("altura", 1) - 1 for d in pred.componentes.values())
        out.append(f"{marca(efecto, 0.005)} Altura: mide {_pulgadas(ctx.altura[j.player_id])}, "
                   f"{abs(j.diferencia_altura):.1f} pulgadas {'más' if j.diferencia_altura > 0 else 'menos'} que los "
                   f"{GRUPOS_TEXTO[j.grupo]} del rival ({efecto * 100:+.1f}% en esta estadística).")
    if j.team_id in ctx.ritmo and j.opp_id in ctx.ritmo and ctx.ritmo_liga:
        ritmo = (ctx.ritmo[j.team_id] + ctx.ritmo[j.opp_id]) / 2 / ctx.ritmo_liga - 1
        out.append(f"{marca(ritmo, 0.015)} Ritmo del partido: {ritmo * 100:+.0f}% de posesiones frente a la media "
                   "(ya incluido en lo que concede el rival).")
    vs = [valor(p, stat) for p in j.partidos if p["opp_id"] == j.opp_id][:5]
    if vs:
        pasa = sum((v > line) if lado == "más" else (v < line) for v in vs)
        out.append(f"{'✅' if pasa / len(vs) >= 0.6 else '❌' if pasa / len(vs) < 0.4 else '➖'} Contra este rival: "
                   f"{', '.join(f'{v:g}' for v in vs)} ({pasa} de {len(vs)} a favor).")
    hits, n = _aciertos(j.partidos[:10], stat, line, lado)
    out.append(f"{'✅' if hits >= 7 else '❌' if hits <= 4 else '➖'} Últimos 10: la habría pasado {hits} de {n}.")
    hits_t, n_t = _aciertos([p for p in j.partidos if p["season"] == ctx.temporada], stat, line, lado)
    if n_t >= 3 and hits_t in (0, n_t):
        out.append(f"{'✅' if hits_t else '❌'} Racha: la {'pasó' if hits_t else 'falló'} en sus {n_t} partidos de esta "
                   "temporada (al inicio de 2025-26 estas rachas siguieron más de lo que esperaba el modelo).")
    if j.enfrentamiento:
        out.append(f"{marca(j.enfrentamiento.factor - 1)} Marcaje: {marcajes.explicar(j.enfrentamiento)}.")
    efecto = sum(BAJAS_RIVAL.get(c, 0) for c in COMPONENTES[stat]) / len(COMPONENTES[stat]) * min(
        len(j.bajas_rival), BAJAS_RIVAL_MAX)
    if j.bajas_rival and efecto:
        out.append(f"{marca(efecto, 0.005)} Bajas del rival: sin {', '.join(j.bajas_rival)} (titular"
                   f"{'es' if len(j.bajas_rival) > 1 else ''}); +{efecto * 100:.1f}% en esta estadística.")
    for n_ in j.notas:
        out.append(f"⚠️ {n_}.")
    return out


# --- Argumentos: el pick explicado en pocos datos concretos -------------------------------
# Al estilo de un analista: cuántas veces la pasó y por qué falló las que falló, con minutos normales, contra
# defensas buenas, en qué puesto (de 30) está el rival concediendo esa estadística a su posición y en su zona de
# tiro, cuántas oportunidades tiene (tiros, rebotes disponibles, canastas de compañeros) y las bajas que cambian
# el partido. Lo pidió el usuario el 4 nov 2026.

_ORDINAL_STAT = {"pts": "puntos", "reb": "rebotes", "ast": "asistencias", "tpm": "triples", "stl": "robos",
                 "blk": "tapones", "tov": "pérdidas", "fgm": "tiros de campo", "ftm": "tiros libres", "fta": "libres"}


def _puntos_equipo(t: dict) -> float:
    return 2 * t.get("fgm", 0) + t.get("tpm", 0) + t.get("ftm", 0)


def _margen_partido(ctx: Contexto, p: dict) -> float | None:
    mio, suyo = ctx.equipo_partido.get((p["game_id"], p["team_id"])), ctx.equipo_partido.get((p["game_id"], p["opp_id"]))
    if not mio or not suyo:
        return None
    return _puntos_equipo(mio) - _puntos_equipo(suyo)


def _equipos_temporada(ctx: Contexto) -> set[str]:
    """Los 30 equipos de esta temporada (fuera las selecciones del All-Star y similares). Se calcula una vez."""
    if getattr(ctx, "_equipos", None) is None:
        ctx._equipos = {p["team_id"] for p in ctx.filas if p.get("season") == ctx.temporada and p.get("minutes")}
    return ctx._equipos


def _puesto(valores: dict[str, float], equipo: str) -> int | None:
    """Puesto de 1 a N del equipo, 1 = el que más concede."""
    if equipo not in valores:
        return None
    orden = sorted(valores, key=lambda t: -valores[t])
    return orden.index(equipo) + 1


def _motivo_fallo(ctx: Contexto, j: Jugador, p: dict) -> str | None:
    if p["minutes"] < j.minutos - 6:
        return f"jugó {p['minutes']:.0f} min"
    if p.get("pf", 0) >= 5:
        return f"{p['pf']} faltas"
    m = _margen_partido(ctx, p)
    if m is not None and abs(m) >= 20:
        return f"paliza de {abs(m):.0f}"
    return None


# "Menos" que el jugador ya falló esta temporada en partidos normales (sin pocos minutos, 5+ faltas ni paliza).
# Backtest 2025-26 (titulares, picks del 62 %+): con 30 %+ de sus partidos así, acertaron 63.8 % prometiendo 66.0 %
# (n = 1.579; PRA 59.8 % frente a 66.1 %, asistencias 60.9 % frente a 66.8 %); con 40 %+, 60.5 % frente a 65.8 %.
# El resto de "menos" acertó lo prometido o más. En los "más" no se ve el efecto.
FALLOS_NORMALES_MAX = 0.3
FALLOS_NORMALES_MIN_PARTIDOS = 5


def _falla_en_normales(ctx: Contexto, j: Jugador, stat: str, line: float) -> list[str]:
    temp = [p for p in j.partidos if p["season"] == ctx.temporada]
    if len(temp) < FALLOS_NORMALES_MIN_PARTIDOS:
        return []
    malos = [p for p in temp if valor(p, stat) >= line and not _motivo_fallo(ctx, j, p)]
    if len(malos) / len(temp) < FALLOS_NORMALES_MAX:
        return []
    return [f"falla en partidos normales ({len(malos)} de {len(temp)} esta temporada)"]


def _por_equipo_temporada(ctx: Contexto, campo: str, propio: bool, contar: bool = False) -> dict[str, float]:
    """Media por partido de esta temporada de un total de equipo de la jugada a jugada: el suyo (propio) o el del
    rival en sus partidos (lo que concede). Se calcula una vez por contexto."""
    cache = getattr(ctx, "_por_equipo", None)
    if cache is None:
        cache = ctx._por_equipo = {}
    clave = (campo, propio, contar)
    if clave not in cache:
        temporada = {f["game_id"] for f in ctx.filas if f.get("season") == ctx.temporada}
        por_partido: dict[str, list] = defaultdict(list)
        for (gid, tid), r in ctx.jug_equipo.items():
            if gid in temporada:
                por_partido[gid].append(r)
        acc = defaultdict(list)
        for filas in por_partido.values():
            if len(filas) != 2:
                continue
            a, b = filas
            acc[a["team_id"]].append((a if propio else b)[campo])
            acc[b["team_id"]].append((b if propio else a)[campo])
        equipos = _equipos_temporada(ctx)
        cache[clave] = {t: (len(v) if contar else sum(v) / len(v)) for t, v in acc.items()
                        if len(v) >= 2 and t in equipos}
    return cache[clave]


def argumentos(ctx: Contexto, j: Jugador, stat: str, line: float, lado: str, pred: Prediccion) -> list[str]:
    out = []
    pasa = (lambda v: v > line) if lado == "más" else (lambda v: v < line)
    temp = [p for p in j.partidos if p["season"] == ctx.temporada]
    # 1. Esta temporada, y por qué falló las que falló.
    if temp:
        fallos = [p for p in temp if not pasa(valor(p, stat))]
        texto = f"La pasó en {len(temp) - len(fallos)} de {len(temp)} esta temporada"
        motivos = [_motivo_fallo(ctx, j, p) for p in fallos]
        if fallos and all(motivos):
            texto += f"; los fallos, en partidos raros ({', '.join(motivos)})"
        elif fallos:
            texto += f" (falló con {', '.join(f'{valor(p, stat):g}' for p in fallos[:4])})"
        out.append(texto)
    # 2. Con los minutos que se esperan hoy, esta temporada y la pasada (sirve sobre todo cuando le suben los
    #    minutos por bajas: cómo le fue la última vez que jugó tanto).
    umbral = j.minutos - 4
    normales = [p for p in j.partidos[:15] if p["minutes"] >= umbral]
    if 3 <= len(normales) < len(j.partidos[:15]):
        h = sum(pasa(valor(p, stat)) for p in normales)
        out.append(f"Con {umbral:.0f}+ minutos (hoy se esperan {j.minutos:.0f}): {h} de {len(normales)} "
                   "en sus últimos 15")
    recientes = sum(p["minutes"] for p in j.partidos[:10]) / max(1, len(j.partidos[:10]))
    if j.minutos >= recientes + 3:
        largos = [p for p in j.partidos[:82] if p["minutes"] >= umbral]
        if len(largos) >= 5:
            h = sum(pasa(valor(p, stat)) for p in largos)
            out.append(f"Hoy juega más que de costumbre ({j.minutos:.0f} min frente a {recientes:.0f}): con {umbral:.0f}+ "
                       f"minutos, esta temporada y la pasada, la pasó {h} de {len(largos)} "
                       f"({h / len(largos) * 100:.0f}%)")
    c = COMPONENTES[stat][0]
    # 3. Contra defensas fuertes en esa estadística (el tercio que menos concede, ~top 10).
    niveles = ctx.nivel.get(j.grupo, {}).get(c, {})
    fuertes = [p for p in j.partidos[:40] if niveles.get(p["opp_id"]) == "fuerte"]
    if len(fuertes) >= 3:
        h = sum(pasa(valor(p, stat)) for p in fuertes)
        out.append(f"Contra las ~10 mejores defensas en {_ORDINAL_STAT.get(c, c)} a {GRUPOS_TEXTO[j.grupo]}: "
                   f"{h} de {len(fuertes)} (últimos 40 partidos)")
    # 3b. Las dos condiciones de hoy a la vez: una defensa como la de hoy y sus minutos.
    hoy = niveles.get(j.opp_id)
    ambas = [p for p in j.partidos[:60] if hoy and niveles.get(p["opp_id"]) == hoy and p["minutes"] >= umbral]
    if len(ambas) >= 4:
        h = sum(pasa(valor(p, stat)) for p in ambas)
        media = sum(valor(p, stat) for p in ambas) / len(ambas)
        plural = {"fuerte": "fuertes", "media": "medias", "débil": "débiles"}.get(hoy, hoy)
        out.append(f"Contra defensas {plural} como la de hoy y con {umbral:.0f}+ minutos: {h} de {len(ambas)}, "
                   f"con {media:.1f} de media (últimos 60 partidos)")
    # 4. Puesto del rival concediendo esa estadística a su posición.
    equipos = _equipos_temporada(ctx)
    concede = {t: d.get(j.grupo, {}).get(c) for t, d in ctx.defensa.items()
               if t in equipos and d.get(j.grupo, {}).get(c)}
    puesto = _puesto(concede, j.opp_id)
    if puesto:
        out.append(f"El rival es #{puesto} de {len(concede)} en {_ORDINAL_STAT.get(c, c)} que concede a "
                   f"{GRUPOS_TEXTO[j.grupo]} por minuto (#1 = el que más concede; "
                   f"{(concede[j.opp_id] - 1) * 100:+.0f}% frente a la media)")
    # 4b. Rebotes: lo que concede el rival a todos (no solo a su posición) y en rebotes ofensivos.
    if c == "reb":
        for clave, texto in (("reb", "rebotes"), ("oreb", "rebotes ofensivos")):
            conc = {t: v.get("defensa", {}).get(clave) for t, v in ctx.equipo_prom.items()
                    if t in equipos and v.get("defensa", {}).get(clave)}
            pr = _puesto(conc, j.opp_id)
            if pr:
                out.append(f"El rival es #{pr} de {len(conc)} en {texto} que concede en total (#1 = el que más)")
    if j.rival_cansado:
        out.append("El rival jugó anoche y él no: +1.5% de puntos y +2% de asistencias aplicados (2024-26)")
    # 5. Sus dos zonas de tiro principales contra lo que concede el rival ahí, y los tiros libres que concede.
    if c in ("pts", "tpm") and j.zonas:
        zonas = {z: d for z, d in j.zonas.items() if c == "pts" or VALOR[z] == 3}
        for k, (z, d) in enumerate(sorted(zonas.items(), key=lambda kv: -kv[1]["reparto"])[:2]):
            if k and d["reparto"] < 0.2:
                break
            rival_z = {t: v[z][0] for t, v in ctx.zona_rival.items() if z in v and t in equipos}
            pz = _puesto(rival_z, j.opp_id)
            if pz:
                out.append(f"{'Su zona principal' if not k else 'Su segunda zona'} es {NOMBRE_ZONA[z]} "
                           f"({d['reparto'] * 100:.0f}% de sus tiros, {d['pct'] * 100:.0f}% de acierto); el rival es "
                           f"#{pz} de {len(rival_z)} en acierto que deja ahí ({d['pct_rival'] * 100:.0f}%, liga "
                           f"{d['pct_liga'] * 100:.0f}%)")
    if c == "pts":
        libres = {t: d.get(j.grupo, {}).get("fta") for t, d in ctx.defensa.items()
                  if t in equipos and d.get(j.grupo, {}).get("fta")}
        pl = _puesto(libres, j.opp_id)
        if pl:
            out.append(f"El rival es #{pl} de {len(libres)} en tiros libres que concede a {GRUPOS_TEXTO[j.grupo]} "
                       f"(#1 = el que más; {(libres[j.opp_id] - 1) * 100:+.0f}% frente a la media)")
    # 5b2. Su puntería reciente frente a la esperada por sus tipos de tiro.
    if c in ("pts", "fgm") and j.punteria is not None:
        out.append(f"Puntería: en sus últimos 10 metió el {j.punteria * 100:.0f}% de las canastas esperadas por sus tipos "
                   f"de tiro" + (" (viene frío: suele volver a su nivel)" if j.punteria < PUNTERIA_FRIA else
                                 " (viene caliente: suele bajar un poco)" if j.punteria > 1.15 else ""))
    # 5c. Asistencias "esperadas": las que tendría si sus compañeros metieran lo normal con él en pista.
    if c == "ast" and j.asistencias_esperadas is not None:
        reales = sum(p["ast"] for p in j.partidos[:10]) / len(j.partidos[:10])
        texto = (f"Asistencias esperadas: {j.asistencias_esperadas:.1f} por partido si sus compañeros metieran lo "
                 f"normal (tiene {reales:.1f}; con él en pista metieron el {j.suerte_companeros * 100:.0f}% de lo "
                 f"esperado por tipo de tiro, últimos 10)")
        if j.factor_suerte != 1.0:
            texto += f"; ajuste aplicado {(j.factor_suerte - 1) * 100:+.1f}%"
        out.append(texto)
    # 5b. Tipos de tiro (parecido a los "play types"): cómo tira y lo que deja el rival en su tipo principal.
    if c in ("pts", "tpm", "fgm") and j.mezcla_tiros:
        orden = sorted(j.mezcla_tiros.items(), key=lambda kv: -kv[1][0])[:3]
        texto = "Cómo tira (últimos 15): " + ", ".join(f"{t} {parte * 100:.0f}% ({pct * 100:.0f}% de acierto)"
                                                      for t, (parte, pct) in orden)
        defensa, media = _defensa_tipos(ctx)
        principal = orden[0][0]
        deja = {e: d[principal] for e, d in defensa.items() if principal in d and e in equipos}
        pt = _puesto(deja, j.opp_id)
        if pt and media.get(principal):
            texto += (f"; en {principal} el rival es #{pt} de {len(deja)} en lo que deja (#1 = el que más; "
                      f"{deja[j.opp_id]:.2f} puntos por tiro frente a {media[principal]:.2f} de media)")
        out.append(texto)
    # 6. Oportunidades: de dónde sale el número.
    comp = pred.componentes.get(c, {})
    datos = comp.get("datos", {})
    if c == "reb" and datos and not any(p.get("dreb_op") for p in j.partidos[:10]):
        out.append(f"Oportunidades: se esperan {datos['fallos_rival']:.0f} tiros fallados del rival y captura el "
                   f"{datos['pct_dreb'] * 100:.0f}% de los que caen con él en pista (+ {datos['oreb']:.1f} ofensivos)")
    elif c == "pts" and datos:
        out.append(f"Oportunidades: {datos['fga']:.1f} tiros de campo y {datos['fta']:.1f} libres esperados "
                   f"({datos['pts_por_tiro']:.2f} puntos por tiro)")
    elif c == "tpm" and datos:
        out.append(f"Oportunidades: {datos['tpa']:.1f} triples intentados esperados al {datos['tp_pct'] * 100:.0f}%")
    elif c == "ast" and datos:
        out.append(f"Oportunidades: asiste el {datos['pct_ast'] * 100:.0f}% de las canastas de sus compañeros con él "
                   "en pista")
    # 6a. Jugada a jugada (jugadas.py): oportunidades de rebote reales y transición, por partido.
    con_jug = [p for p in j.partidos[:10] if p.get("dreb_op")]
    linea_reb = linea_tr = False
    if c == "reb" and len(con_jug) >= 3:
        d_op = sum(p["dreb_op"] for p in con_jug)
        o_op = sum(p["oreb_op"] for p in con_jug)
        texto = (f"Rebotes disponibles con él en pista (últimos {len(con_jug)}): {d_op / len(con_jug):.1f} tiros "
                 f"fallados del rival y {o_op / len(con_jug):.1f} de su equipo por partido; se queda el "
                 f"{sum(p['dreb'] for p in con_jug) / max(1, d_op) * 100:.0f}% y el "
                 f"{sum(p['oreb'] for p in con_jug) / max(1, o_op) * 100:.0f}%")
        fallos = _por_equipo_temporada(ctx, "oreb_op", propio=True)
        if j.opp_id in fallos:
            texto += (f"; el rival falla {fallos[j.opp_id]:.1f} tiros por partido (#{_puesto(fallos, j.opp_id)} de "
                      f"{len(fallos)}, #1 = el que más falla)")
        out.append(texto)
        linea_reb = True
    if c == "pts":
        concede = _por_equipo_temporada(ctx, "trans_pts", propio=False)
        if j.opp_id in concede:
            texto = (f"Transición: el rival concede {concede[j.opp_id]:.1f} puntos por partido al contraataque "
                     f"(#{_puesto(concede, j.opp_id)} de {len(concede)}, #1 = el que más)")
            con_tr = [p for p in j.partidos[:10] if p.get("trans_pts") is not None and p.get("dreb_op") is not None]
            if len(con_tr) >= 3:
                texto += f"; él anota {sum(p['trans_pts'] for p in con_tr) / len(con_tr):.1f} así por partido"
            if j.factor_transicion != 1.0:
                texto += f" (ajuste aplicado {(j.factor_transicion - 1) * 100:+.1f}%)"
            out.append(texto)
            linea_tr = True
    # 6b. pbpstats (respaldo si no hay jugada a jugada): rebotes disponibles que se queda y transición.
    fila = ctx.pbp.get("jugadores", {}).get(clave_nombre(j.nombre))
    if c == "reb" and not linea_reb and fila and fila.get("DefFGReboundPct") is not None:
        out.append(f"Se queda el {fila['DefFGReboundPct'] * 100:.0f}% de los rebotes defensivos y el "
                   f"{(fila.get('OffFGReboundPct') or 0) * 100:.0f}% de los ofensivos que caen con él en pista "
                   f"(esta temporada, pbpstats)")
    sigla_rival = ctx.siglas.get(j.opp_id)
    concede_tr = {t: pbpstats.por_partido(f, "Points", ctx.pbp.get("equipos", {}).get(t, {}).get("GamesPlayed"))
                  for t, f in ctx.pbp.get("rivales_transicion", {}).items()}
    concede_tr = {t: v for t, v in concede_tr.items() if v is not None}
    if c == "pts" and not linea_tr and sigla_rival in concede_tr:
        texto = (f"Transición: el rival concede {concede_tr[sigla_rival]:.1f} puntos por partido tras robos "
                 f"(#{_puesto(concede_tr, sigla_rival)} de {len(concede_tr)}, #1 = el que más)")
        propio = ctx.pbp.get("equipos_transicion", {}).get(ctx.siglas.get(j.team_id))
        mio = pbpstats.por_partido(propio, "Points", ctx.pbp.get("equipos", {}).get(ctx.siglas.get(j.team_id), {})
                                   .get("GamesPlayed")) if propio else None
        if mio is not None:
            texto += f"; su equipo anota {mio:.1f} así"
        out.append(texto)
    # 6c. Estadísticas defensivas y pérdidas: sus oportunidades reales con él en pista y lo que hace el rival.
    con_def = [p for p in j.partidos[:10] if p.get("stl_op")]
    if c == "stl":
        if len(con_def) >= 3:
            op = sum(p["stl_op"] for p in con_def)
            out.append(f"Oportunidades de robo (últimos {len(con_def)}): el rival perdió {op / len(con_def):.1f} balones por "
                       f"partido con él en pista y robó el {sum(p['stl'] for p in con_def) / max(1, op) * 100:.0f}%")
        pierde = {t: v.get("ataque", {}).get("tov") for t, v in ctx.equipo_prom.items()
                  if t in equipos and v.get("ataque", {}).get("tov")}
        pp = _puesto(pierde, j.opp_id)
        if pp:
            out.append(f"El rival es #{pp} de {len(pierde)} en balones que pierde (#1 = el que más; "
                       f"{pierde[j.opp_id]:.1f} por partido)")
    if c == "blk":
        if len(con_def) >= 3:
            op = sum(p["blk_op"] or 0 for p in con_def)
            out.append(f"Oportunidades de tapón (últimos {len(con_def)}): {op / len(con_def):.1f} tiros de 2 del rival por "
                       f"partido con él en pista; taponó el {sum(p['blk'] for p in con_def) / max(1, op) * 100:.1f}%")
        dos = {t: v.get("ataque", {}).get("t2a") for t, v in ctx.equipo_prom.items()
               if t in equipos and v.get("ataque", {}).get("t2a")}
        pd = _puesto(dos, j.opp_id)
        if pd:
            out.append(f"El rival es #{pd} de {len(dos)} en tiros de 2 por partido (#1 = el que más; {dos[j.opp_id]:.1f})")
        if getattr(ctx, "_cerca_aro", None) is None:
            ctx._cerca_aro = {}
            for t, partidos in ctx.tipos_equipo.items():
                tot = cerca_aro = 0
                for tipos in partidos.values():
                    for tipo, r in tipos.items():
                        tot += r["fga"]
                        cerca_aro += r["fga"] if tipo in ("penetración", "corte", "palmeo", "aro", "poste") else 0
                if tot >= 200 and t in equipos:
                    ctx._cerca_aro[t] = cerca_aro / tot
        cerca = ctx._cerca_aro
        pc = _puesto(cerca, j.opp_id)
        if pc:
            out.append(f"El {cerca[j.opp_id] * 100:.0f}% de los tiros del rival son cerca del aro (penetración, corte, "
                       f"poste, palmeo): #{pc} de {len(cerca)}")
    if c == "tov":
        fuerza = {t: v.get("defensa", {}).get("tov") for t, v in ctx.equipo_prom.items()
                  if t in equipos and v.get("defensa", {}).get("tov")}
        pf = _puesto(fuerza, j.opp_id)
        if pf:
            out.append(f"El rival es #{pf} de {len(fuerza)} en pérdidas que provoca (#1 = el que más presiona; "
                       f"{fuerza[j.opp_id]:.1f} por partido)")
        ult = j.partidos[:10]
        jugadas = sum(p["fga"] + 0.44 * p["fta"] + p["tov"] for p in ult) / max(1, len(ult))
        out.append(f"Usa {jugadas:.1f} jugadas por partido (tiros, libres y pérdidas) y pierde el "
                   f"{sum(p['tov'] for p in ult) / max(1, jugadas * len(ult)) * 100:.0f}% de ellas")
    # 7. Bajas que cambian el partido.
    if j.bajas_rival_ids:
        partes = []
        for pid, nombre in zip(j.bajas_rival_ids, j.bajas_rival):
            rec = ctx.por_jugador.get(pid, [])[:10]
            if rec:
                media = sum(valor(p, stat) for p in rec) / len(rec)
                partes.append(f"{nombre} ({media:.1f} {NOMBRES[stat]} por partido)")
        if partes:
            out.append("El rival no tiene a " + ", ".join(partes))
    if j.sin_estrella and set(COMPONENTES[stat]) & SUBEN_SIN_ESTRELLA:
        out.append(f"Su equipo no tiene a {', '.join(j.sin_estrella)}: más tiros y balón para él")
    out.append(f"Minutos: {j.minutos:.0f} esperados ({'titular' if es_titular(j) else 'suplente'}, "
               f"±{j.minutos_sd:.0f})")
    return out


def texto_defensa(ctx: Contexto, j: Jugador, stat: str, pred: Prediccion) -> str:
    """'el rival concede −5 % de triples por minuto a aleros/ala-pívots (defensa fuerte); ajuste aplicado −3 %'."""
    c = COMPONENTES[stat][0]
    nivel = ctx.nivel.get(j.grupo, {}).get(c, {}).get(j.opp_id, "media")
    rel = ctx.defensa.get(j.opp_id, {}).get(j.grupo, {}).get(c, 1.0) - 1
    texto = (f"el rival concede {rel * 100:+.0f}% de {NOMBRES[COMPONENTES_NOMBRE.get(c, stat)]} por minuto a "
             f"{GRUPOS_TEXTO[j.grupo]} (defensa {nivel}); ajuste aplicado "
             f"{(pred.factores.get('rival', 1) - 1) * 100:+.0f}%")
    if c in ("pts", "tpm") and j.zonas:
        z = max(j.zonas.items(), key=lambda kv: kv[1]["reparto"] * (kv[0] in ("esquina3", "triple") if c == "tpm" else 1))
        texto += (f"; en su zona principal ({z[0]}) el rival concede {z[1]['pct_rival'] * 100:.0f}% "
                  f"(liga {z[1]['pct_liga'] * 100:.0f}%)")
    return texto


def _prob_jugador(j: Jugador, stat: str, line: float, lado: str, p_mod: float) -> float:
    """Modelo mezclado con su acierto real sobre la línea en los últimos 15 y calibrado."""
    hits, n = _aciertos(j.partidos[:15], stat, line, lado)
    p_emp = (hits + 5 * p_mod) / (n + 5)
    return 0.5 + (PESO_MODELO * p_mod + (1 - PESO_MODELO) * p_emp - 0.5) * CALIBRACION_STAT.get(stat, CALIBRACION)


MINUTOS_SD_ESTABLE = 6.0
# Si el modelo ve una prop más de 25 puntos más probable que la casa, la casa suele saber algo que el modelo
# no (minutos, rol, salud). 26 oct 2026: Giannis menos de 47.5 PRA, modelo 80 % y casa 51 %, perdió con 52.
DISCREPANCIA_MAX = 0.25


# Props que el usuario no quiere volver a jugar (nombre sin espacios ni signos, componente). Se descartan de picks
# seguros, combinadas, rachas y bet builders, por los dos lados.
# 2 nov 2026: Isaiah Jackson menos de 7.5 rebotes (con los pívots de los Clippers fuera) hizo 8 y tumbó las dos
# apuestas reales del día.
VETADOS = {("isaiahjackson", "reb")}


def vetada(nombre: str, stat: str) -> bool:
    clave = "".join(ch for ch in unicodedata.normalize("NFKD", nombre.lower()) if ch.isalnum())
    return any((clave, c) in VETADOS for c in COMPONENTES.get(stat, ()))


def alertas(j: Jugador, stat: str) -> list[str]:
    """Lo que hace dudosa una prop aunque su probabilidad sea alta."""
    out = ["vetada por el usuario"] if vetada(j.nombre, stat) else []
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


def linea_minima_casa(principal: float) -> float:
    """La línea alternativa más baja que suele ofrecer la casa: la principal menos ~10 % (al menos 1).
    27 oct 2026, Betano: Cade 8.5 asistencias -> 8+, Brunson 25.5 puntos -> 24+, Dončić 32.5 -> 30+,
    Reaves 5.5 asistencias -> 5+ (en rebotes y en algunos puntos ofrece incluso algo más bajo)."""
    return principal - max(1, math.floor(0.1 * principal))


# Sin línea principal de la casa (p. ej. partidos sin líneas por el racionamiento de The Odds API) se estima: la
# principal suele quedar en la media entre lo que espera el modelo y su media de los últimos 10. Contra las líneas
# mínimas de Betano del 6 nov 2026 (12 props) la estimación acierta en 3 de cada 4 o queda por encima (se puede jugar);
# con un punto más de margen no quedaba ningún bet builder ni pick seguro en 9 partidos, así que no se suma margen.
MARGEN_SIN_LINEA = 0.0
PROB_JUGABLE = 0.75   # pick "seguro" a la línea mínima de la casa cuando no hay ninguna al 85 %


def piso_casa(j: Jugador, stat: str, mu: float, principal: float | None = None) -> float:
    """La línea más baja de "más de" que se puede proponer: la mínima que ofrecería la casa."""
    if principal is not None:
        return linea_minima_casa(principal)
    ult = j.partidos[:10]
    media = sum(valor(p, stat) for p in ult) / len(ult) if ult else mu
    estimada = math.floor((mu + media) / 2) + 0.5
    return linea_minima_casa(estimada) + MARGEN_SIN_LINEA


def seguras(ctx: Contexto, j: Jugador, objetivo: float = PROB_SEGURA,
            principales: dict | None = None) -> list[Segura]:
    """Para titulares estables, la línea de "más de" más alta que pasa con al menos esa probabilidad, sin bajar de
    la mínima que ofrece la casa (si la línea queda por debajo, no es un pick seguro que se pueda jugar)."""
    if j.minutos < MIN_SEGURA or not es_titular(j):
        return []
    out = []
    ult = j.partidos[:10]
    for stat, minimo in MEDIAS_SEGURA.items():
        if vetada(j.nombre, stat):
            continue
        media = sum(valor(p, stat) for p in ult) / len(ult)
        if media < minimo:
            continue
        pred = predecir(ctx, j, stat)
        piso = piso_casa(j, stat, pred.mu, (principales or {}).get((j.player_id, stat)))
        ultima = None
        for k in range(int(pred.mu), -1, -1):
            if k + 0.5 < piso:
                break
            p = _prob_jugador(j, stat, k + 0.5, "más", prob_lados(k + 0.5, pred.mu, pred.var)[0])
            ultima = (k + 0.5, p)
            if p >= objetivo:
                out.append(Segura(j.player_id, j.nombre, stat, k + 0.5, p, pred.mu, media,
                                  _aciertos(ult, stat, k + 0.5, "más")))
                break
        else:
            ultima = None
        # La casa no ofrece una línea tan baja como para el 85 %: la más baja que sí ofrece, si llega a PROB_JUGABLE.
        if ultima and ultima[1] < objetivo and ultima[1] >= PROB_JUGABLE:
            out.append(Segura(j.player_id, j.nombre, stat, ultima[0], ultima[1], pred.mu, media,
                              _aciertos(ult, stat, ultima[0], "más")))
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
        if lado == "menos" and _menos_estrella_inicio(ctx, j, stat):
            p_jug = 0.5 + (p_jug - 0.5) * CORRECCION_MENOS_ESTRELLA
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
        tabla_metricas(ctx, j, COMPONENTES[stat]) if detalle else [], es_titular(j),
        alertas(j, stat) + (["muy lejos de la casa"] if p_casa is not None and p_jug - p_casa > DISCREPANCIA_MAX
                            else [])
        + ([f"sin {j.sin_estrella[0]}: más tiros para él"]
           if lado == "menos" and j.sin_estrella and set(COMPONENTES[stat]) & SUBEN_SIN_ESTRELLA else [])
        + (["menos de una estrella al inicio de temporada"]
           if lado == "menos" and _menos_estrella_inicio(ctx, j, stat) else [])
        + (_falla_en_normales(ctx, j, stat, line) if lado == "menos" else [])
        + (["viene fallando tiros que suele meter"] if lado == "menos" and "pts" in COMPONENTES[stat]
           and j.punteria is not None and j.punteria < PUNTERIA_FRIA else [])
        + (["segunda noche y no favorito"] if lado == "más" and j.cansado_no_favorito else [])
        + (["el rival concede mucho contraataque"] if lado == "menos" and "pts" in COMPONENTES[stat]
           and (j.transicion_rival or 1) >= TRANSICION_ALTA else []),
        texto_defensa(ctx, j, stat, pred), razones(ctx, j, stat, line, lado, pred),
        argumentos(ctx, j, stat, line, lado, pred) if detalle else [],
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
