"""Historial gratuito de football-data.co.uk: resultados, estadísticas y cuotas de muchas temporadas.

Sin clave ni límite de peticiones. Para las ligas principales cada partido trae goles, remates,
tiros a puerta, córners, faltas y tarjetas, más las cuotas medias de las casas antes del
partido y al cierre. Las ligas "extra" (México, Argentina, Brasil, MLS...) solo traen resultado
y cuotas de cierre.

También publica los partidos de los próximos días con sus cuotas (`fixtures.csv`), así que el
modelo puede predecir sin gastar peticiones de API-Football.
"""
from __future__ import annotations

import csv
import io
import logging
import time
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path

import requests

log = logging.getLogger(__name__)

BASE_URL = "https://www.football-data.co.uk"
# Ligas con un archivo por temporada (y estadísticas de partido en casi todas).
LIGAS = {
    "E0": "Premier League", "E1": "Championship", "SP1": "LaLiga", "SP2": "LaLiga Hypermotion",
    "I1": "Serie A", "I2": "Serie B", "D1": "Bundesliga", "D2": "2. Bundesliga", "F1": "Ligue 1",
    "F2": "Ligue 2", "N1": "Eredivisie", "P1": "Primeira Liga", "B1": "Jupiler Pro League",
    "T1": "Süper Lig", "SC0": "Scottish Premiership", "G1": "Super League Grecia",
}
# Ligas con un único archivo para todas las temporadas: solo resultado y cuotas de cierre.
LIGAS_EXTRA = {
    "MEX": ("Mexico", "Liga MX"), "ARG": ("Argentina", "Liga Profesional"), "BRA": ("Brazil", "Serie A"),
    "USA": ("USA", "MLS"), "JPN": ("Japan", "J1 League"), "SWE": ("Sweden", "Allsvenskan"),
    "NOR": ("Norway", "Eliteserien"), "DNK": ("Denmark", "Superliga"), "AUT": ("Austria", "Bundesliga"),
    "SWZ": ("Switzerland", "Super League"), "POL": ("Poland", "Ekstraklasa"), "CHN": ("China", "Super League"),
}
NOMBRES_LIGA = {**LIGAS, **{k: v[1] for k, v in LIGAS_EXTRA.items()}}

# Estadística -> (columna local, columna visitante).
COLUMNAS_STATS = {
    "shots_total": ("HS", "AS"), "shots_on": ("HST", "AST"), "corners": ("HC", "AC"),
    "fouls": ("HF", "AF"), "yellow": ("HY", "AY"), "red": ("HR", "AR"), "xg": ("HxG", "AxG"),
}
# Cuotas por mercado: columnas candidatas, en orden de preferencia.
# Antes del partido: media de las casas (lo que puede conseguir un apostador normal).
CUOTAS_PREVIAS = {
    "1": ("AvgH", "BbAvH", "B365H"), "X": ("AvgD", "BbAvD", "B365D"), "2": ("AvgA", "BbAvA", "B365A"),
    "over2.5": ("Avg>2.5", "BbAv>2.5", "B365>2.5"), "under2.5": ("Avg<2.5", "BbAv<2.5", "B365<2.5"),
}
# Al cierre: Pinnacle y Betfair Exchange (los mercados más eficientes), si no la media.
CUOTAS_CIERRE = {
    "1": ("PSCH", "BFECH", "AvgCH", "B365CH"), "X": ("PSCD", "BFECD", "AvgCD", "B365CD"),
    "2": ("PSCA", "BFECA", "AvgCA", "B365CA"),
    "over2.5": ("PC>2.5", "BFEC>2.5", "AvgC>2.5", "B365C>2.5"),
    "under2.5": ("PC<2.5", "BFEC<2.5", "AvgC<2.5", "B365C<2.5"),
}
MAX_EDAD_ARCHIVO = 6 * 3600   # la temporada en curso y los próximos partidos se refrescan cada 6 h


@dataclass
class Partido:
    fecha: date
    liga: str
    temporada: str
    local: str
    visitante: str
    goles_local: int | None = None       # None = aún no se ha jugado
    goles_visitante: int | None = None
    hora: str = ""
    arbitro: str = ""
    # stat -> (local, visitante); solo las que trae el archivo.
    stats: dict[str, tuple[float, float]] = field(default_factory=dict)
    cuotas: dict[str, float] = field(default_factory=dict)        # antes del partido
    cuotas_cierre: dict[str, float] = field(default_factory=dict)
    # Caché de modelo_historico.goles_del_mercado (() = no calculable).
    xg_mercado: tuple[float, float] | tuple[()] | None = field(default=None, repr=False, compare=False)

    @property
    def jugado(self) -> bool:
        return self.goles_local is not None and self.goles_visitante is not None

    def valor(self, stat: str) -> tuple[float, float] | None:
        if stat == "goals":
            return (self.goles_local, self.goles_visitante) if self.jugado else None
        if stat == "cards":
            y, r = self.stats.get("yellow"), self.stats.get("red")
            return (y[0] + r[0], y[1] + r[1]) if y and r else None
        if stat == "saves":
            # Atajadas del portero de cada equipo = tiros a puerta del rival que no fueron gol.
            t = self.stats.get("shots_on")
            if t is None or not self.jugado:
                return None
            return (max(0.0, t[1] - self.goles_visitante), max(0.0, t[0] - self.goles_local))
        return self.stats.get(stat)


def temporada_de(d: date) -> str:
    """Código de temporada europea (julio-junio): 2026-10-21 -> '2627'."""
    y = d.year if d.month >= 7 else d.year - 1
    return f"{y % 100:02d}{(y + 1) % 100:02d}"


def temporadas_hasta(d: date, n: int) -> list[str]:
    y = d.year if d.month >= 7 else d.year - 1
    return [f"{a % 100:02d}{(a + 1) % 100:02d}" for a in range(y - n + 1, y + 1)]


def _fecha(texto: str) -> date | None:
    for fmt in ("%d/%m/%Y", "%d/%m/%y"):
        try:
            return datetime.strptime(texto.strip(), fmt).date()
        except ValueError:
            pass
    return None


def _num(texto: str | None) -> float | None:
    try:
        v = float(texto)
    except (TypeError, ValueError):
        return None
    return v


def _primera(row: dict, columnas: tuple[str, ...]) -> float | None:
    for c in columnas:
        v = _num(row.get(c))
        if v is not None and v > 1.0:
            return v
    return None


def _cuotas(row: dict, tabla: dict[str, tuple[str, ...]]) -> dict[str, float]:
    out = {}
    for mercado, columnas in tabla.items():
        v = _primera(row, columnas)
        if v is not None:
            out[mercado] = v
    return out


def parse_csv(texto: str, liga: str | None = None) -> list[Partido]:
    """Lee un CSV de football-data.co.uk (formato por temporada, extra o de próximos partidos)."""
    texto = texto.lstrip("﻿")
    out = []
    for row in csv.DictReader(io.StringIO(texto)):
        row = {(k or "").strip(): (v or "").strip() for k, v in row.items()}
        local, visitante = row.get("HomeTeam") or row.get("Home"), row.get("AwayTeam") or row.get("Away")
        fecha = _fecha(row.get("Date", ""))
        if not local or not visitante or fecha is None:
            continue
        codigo = liga or row.get("Div") or _codigo_extra(row.get("Country", ""), row.get("League", ""))
        if not codigo:
            continue
        gl, gv = _num(row.get("FTHG", row.get("HG"))), _num(row.get("FTAG", row.get("AG")))
        stats = {}
        for stat, (ch, ca) in COLUMNAS_STATS.items():
            h, a = _num(row.get(ch)), _num(row.get(ca))
            if h is not None and a is not None:
                stats[stat] = (h, a)
        out.append(Partido(
            fecha=fecha, liga=codigo, temporada=row.get("Season") or temporada_de(fecha), local=local,
            visitante=visitante, goles_local=None if gl is None else int(gl),
            goles_visitante=None if gv is None else int(gv), hora=row.get("Time", ""),
            arbitro=row.get("Referee", ""), stats=stats,
            cuotas=_cuotas(row, CUOTAS_PREVIAS), cuotas_cierre=_cuotas(row, CUOTAS_CIERRE),
        ))
    return out


def _codigo_extra(pais: str, liga: str) -> str | None:
    for codigo, (p, l) in LIGAS_EXTRA.items():
        if p == pais and l == liga:
            return codigo
    return None


class Historico:
    """Descarga (con caché en disco) y carga del historial."""

    def __init__(self, cache_dir: Path, session: requests.Session | None = None):
        self.cache_dir = Path(cache_dir)
        self.session = session or requests.Session()

    def _descargar(self, url: str, destino: Path, refrescar: bool) -> str | None:
        fresco = destino.exists() and time.time() - destino.stat().st_mtime < MAX_EDAD_ARCHIVO
        if destino.exists() and (fresco or not refrescar):
            return destino.read_text(encoding="utf-8")
        try:
            resp = self.session.get(url, timeout=60)
            resp.raise_for_status()
        except requests.RequestException as e:
            if destino.exists():
                log.warning("No se pudo actualizar %s (%s); uso la copia guardada", url, e)
                return destino.read_text(encoding="utf-8")
            log.warning("No se pudo descargar %s: %s", url, e)
            return None
        # Algunos archivos antiguos vienen en latin-1.
        try:
            texto = resp.content.decode("utf-8-sig")
        except UnicodeDecodeError:
            texto = resp.content.decode("latin-1")
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(texto, encoding="utf-8")
        return texto

    def partidos(self, ligas: list[str], temporadas: int, hoy: date) -> list[Partido]:
        """Partidos jugados de las últimas `temporadas` temporadas (incluida la actual), ordenados por fecha."""
        actual = temporada_de(hoy)
        primera = temporadas_hasta(hoy, temporadas)[0]
        desde = date(2000 + int(primera[:2]), 7, 1)
        out: list[Partido] = []
        for liga in ligas:
            if liga in LIGAS:
                for t in temporadas_hasta(hoy, temporadas):
                    texto = self._descargar(f"{BASE_URL}/mmz4281/{t}/{liga}.csv",
                                            self.cache_dir / f"{t}_{liga}.csv", refrescar=t == actual)
                    if texto:
                        out += [p for p in parse_csv(texto, liga) if p.jugado]
            elif liga in LIGAS_EXTRA:
                texto = self._descargar(f"{BASE_URL}/new/{liga}.csv", self.cache_dir / f"extra_{liga}.csv",
                                        refrescar=True)
                if texto:
                    out += [p for p in parse_csv(texto, liga) if p.jugado and p.fecha >= desde]
            else:
                log.warning("Liga desconocida en football-data.co.uk: %s", liga)
        out.sort(key=lambda p: (p.fecha, p.liga, p.local))
        return out

    def proximos(self, ligas: list[str]) -> list[Partido]:
        """Partidos de los próximos días con cuotas, según football-data.co.uk."""
        out: list[Partido] = []
        for nombre in ("fixtures.csv", "new_league_fixtures.csv"):
            texto = self._descargar(f"{BASE_URL}/{nombre}", self.cache_dir / nombre, refrescar=True)
            if texto:
                out += [p for p in parse_csv(texto) if p.liga in ligas and not p.jugado]
        out.sort(key=lambda p: (p.fecha, p.hora, p.liga))
        return out
