"""Chequeo previo al partido: alineaciones confirmadas + cuotas actualizadas -> apuestas finales.

API-Football publica las alineaciones entre 20 y 40 minutos antes del inicio. Para cada partido con
selecciones del día, este módulo:

1. descarga los titulares (1 petición) y las cuotas del momento (1 petición);
2. mide cuánto pesan en ataque los habituales que faltan (su parte de los remates del equipo en los
   últimos partidos guardados) y rebaja en esa proporción lo esperado del equipo;
3. re-analiza el partido con esa corrección y las cuotas nuevas (el mercado ya incorpora la
   noticia de la alineación: si la cuota se movió en contra, el valor desaparece);
4. marca cada selección como confirmada o anulada, con el motivo.

Sin historial de jugadores en la base (al principio, con el plan gratuito) solo se puede comprobar
que la alineación está publicada, anular apuestas de jugadores suplentes y recalcular con las
cuotas del momento.
"""
from __future__ import annotations

import difflib
import json
import logging
import re
import unicodedata
import zlib
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone

import requests

from .analyzer import analyze_fixture, candidates
from .api_football import ApiError, ApiFootball, PresupuestoAgotado
from .bzzoiro import buscar
from .collector import POR_JUGAR, parse_odds
from .config import Config
from .db import Database, now_iso
from .model import MatchExpectation

ESPERA_ALINEACION = timedelta(minutes=20)   # si a menos de esto no hay alineación, se chequea sin ella
HABITUAL = 0.6            # titular en al menos el 60 % de los partidos recientes
RECUPERA_SUPLENTE = 0.5   # el sustituto aporta la mitad de lo que aportaba el habitual
FACTOR_MIN = 0.75
CAIDA_MAX_COMBINADA = 0.05  # una pierna de combinada se anula si su probabilidad cae más de esto
STATS_ATAQUE = ("goals", "shots_on", "shots_total", "corners")


def parse_alineaciones(response: list[dict]) -> dict[int, dict]:
    """team_id -> {"titulares": {player_id: (nombre, posición)}, "formacion": str}."""
    out = {}
    for entry in response:
        xi = {}
        for item in entry.get("startXI") or []:
            p = item.get("player") or {}
            if p.get("id") is not None:
                xi[p["id"]] = (p.get("name"), p.get("pos"))
        if xi:
            out[entry["team"]["id"]] = {"titulares": xi, "formacion": entry.get("formation")}
    return out


@dataclass
class Impacto:
    factor: float = 1.0
    notas: list[str] = field(default_factory=list)
    con_historial: bool = False


def impacto_alineacion(db: Database, team_id: int, nombre: str, antes_utc: str, titulares: dict[int, tuple],
                       partidos: int = 10) -> Impacto:
    """Cuánto ataque pierde el equipo por los habituales que no son titulares hoy."""
    filas = db.player_history(team_id, antes_utc, partidos)
    imp = Impacto()
    if not filas:
        imp.notas.append(f"{nombre}: sin historial de jugadores en la base; solo se comprueba la alineación")
        return imp
    imp.con_historial = True
    n_partidos = len({r["fixture_id"] for r in filas})
    remates_equipo = sum(r["shots_total"] for r in filas) or 1
    jugadores: dict[int, dict] = {}
    for r in filas:
        j = jugadores.setdefault(r["player_id"], {"nombre": r["name"], "pos": r["position"], "titular": 0,
                                                  "remates": 0, "minutos": 0})
        j["titular"] += r["minutes"] >= 60       # aproximación de titular con los datos guardados
        j["remates"] += r["shots_total"]
        j["minutos"] += r["minutes"]
    perdida = 0.0
    for pid, j in jugadores.items():
        if pid in titulares or j["titular"] < HABITUAL * n_partidos:
            continue
        cuota = j["remates"] / remates_equipo
        perdida += cuota
        if j["pos"] == "G":
            imp.notas.append(f"{nombre}: no juega su portero habitual ({j['nombre']})")
        elif cuota >= 0.08:
            imp.notas.append(f"{nombre}: no es titular {j['nombre']} ({cuota:.0%} de los remates del equipo)")
    imp.factor = max(FACTOR_MIN, 1 - RECUPERA_SUPLENTE * perdida)
    if imp.factor < 0.995:
        imp.notas.append(f"{nombre}: ataque esperado ×{imp.factor:.2f} por las ausencias")
    return imp


def aplicar_impacto(e: MatchExpectation, factor_local: float, factor_visitante: float) -> None:
    """Rebaja lo que genera cada equipo; las atajadas del portero rival bajan con sus tiros a puerta."""
    for stat in STATS_ATAQUE:
        if stat in e.home:
            e.home[stat] *= factor_local
            e.away[stat] *= factor_visitante
    if "saves" in e.home:
        e.away["saves"] *= factor_local
        e.home["saves"] *= factor_visitante


@dataclass
class ResultadoChequeo:
    fixture_id: int
    partido: str
    inicio_utc: str
    estado: str                      # chequeado | sin_alineacion | esperando | sin_presupuesto
    notas: list[str] = field(default_factory=list)
    confirmadas: list[str] = field(default_factory=list)
    anuladas: list[str] = field(default_factory=list)
    nuevas: list[str] = field(default_factory=list)


def partidos_a_chequear(db: Database, fecha: str, ahora: datetime, ventana: timedelta,
                        forzar: bool = False) -> list[dict]:
    """Partidos del día con selecciones pendientes que empiezan dentro de la ventana y no se han chequeado."""
    filas = db.conn.execute(
        """SELECT DISTINCT f.id FROM fixtures f JOIN picks p ON p.fixture_id = f.id
           LEFT JOIN lineup_checks c ON c.fixture_id = f.id
           WHERE p.fecha = ? AND p.result IS NULL AND (? OR c.fixture_id IS NULL)""",
        (fecha, int(forzar)),
    ).fetchall()
    out = []
    for r in filas:
        fx = dict(db.fixture(r["id"]))
        inicio = datetime.fromisoformat(fx["date_utc"])
        if fx["status"] in POR_JUGAR and ahora - timedelta(minutes=5) <= inicio <= ahora + ventana:
            out.append(fx)
    return sorted(out, key=lambda f: f["date_utc"])


def _normalizar(nombre: str | None) -> str:
    texto = unicodedata.normalize("NFKD", nombre or "").encode("ascii", "ignore").decode().lower()
    return " ".join(re.sub(r"[^a-z ]+", " ", texto).split())


def _mismo_jugador(a: str, b: str) -> bool:
    a, b = _normalizar(a), _normalizar(b)
    if not a or not b:
        return False
    if a == b or a.split()[-1] == b.split()[-1] and a[0] == b[0]:
        return True
    return difflib.SequenceMatcher(None, a, b).ratio() >= 0.85


def alineaciones_bzzoiro(bz, db: Database, fx: dict, eventos: list[dict]) -> tuple[dict[int, dict], list[str], str]:
    """Alineaciones y bajas de Bzzoiro para un partido, con los jugadores emparejados por nombre con los
    ids de la base (los que no aparecen reciben un id negativo propio). -> (alineaciones, bajas, estado)."""
    ev = buscar(eventos, fx["home_name"], fx["away_name"], datetime.fromisoformat(fx["date_utc"]))
    if ev is None:
        return {}, [], "no encontrado"
    al = bz.alineacion(ev["id"])
    if al is None:
        return {}, [], "sin alineación"
    out = {}
    if al["estado"] == "confirmed":
        for team_id, lado in ((fx["home_id"], "local"), (fx["away_id"], "visitante")):
            conocidos = db.conn.execute("SELECT DISTINCT player_id, name FROM player_stats WHERE team_id = ?",
                                        (team_id,)).fetchall()
            titulares = {}
            for nombre, pos in al[lado]:
                pid = next((r["player_id"] for r in conocidos if _mismo_jugador(nombre, r["name"])),
                           -(zlib.crc32(f"{team_id}:{_normalizar(nombre)}".encode()) % 10 ** 9) - 1)
                titulares[pid] = (nombre, "G" if (pos or "").upper().startswith("G") else pos)
            if titulares:
                out[team_id] = {"titulares": titulares, "formacion": None}
    return out, al["bajas"], al["estado"]


def chequear_partido(db: Database, api: ApiFootball, cfg: Config, fx: dict, ahora: datetime, historico=None,
                     con_cuotas: bool = True, bzzoiro=None, eventos_bzzoiro: list[dict] | None = None
                     ) -> ResultadoChequeo:
    partido = f"{fx['home_name']} vs {fx['away_name']}"
    res = ResultadoChequeo(fx["id"], partido, fx["date_utc"], "chequeado")
    inicio = datetime.fromisoformat(fx["date_utc"])
    alineaciones = parse_alineaciones(api.alineaciones(fx["id"]))
    completas = fx["home_id"] in alineaciones and fx["away_id"] in alineaciones
    if bzzoiro is not None and eventos_bzzoiro is not None:
        # Bzzoiro: bajas siempre; alineación confirmada solo si la fuente principal aún no la tiene.
        try:
            al_bz, bajas, estado_bz = alineaciones_bzzoiro(bzzoiro, db, fx, eventos_bzzoiro)
            if bajas:
                res.notas.append("Bajas (Bzzoiro): " + ", ".join(bajas[:12]))
            if not completas and fx["home_id"] in al_bz and fx["away_id"] in al_bz:
                alineaciones, completas = al_bz, True
                res.notas.append("Alineaciones confirmadas tomadas de Bzzoiro")
        except (ApiError, PresupuestoAgotado, requests.RequestException, ValueError, KeyError) as e:
            res.notas.append(f"Bzzoiro no disponible: {e}")
    if not completas and inicio - ahora > ESPERA_ALINEACION:
        res.estado = "esperando"
        res.notas.append("Alineaciones aún no publicadas: vuelve a chequear en 10-15 minutos")
        return res
    if not completas:
        res.estado = "sin_alineacion"
        res.notas.append("Sin alineaciones a menos de 20 minutos del inicio: chequeo solo con cuotas actuales")
    if con_cuotas:
        filas = parse_odds(api.cuotas(fx["id"]))
        if filas:
            with db.tx():
                db.save_odds(fx["id"], filas)

    impactos = {}
    titulares: set[int] = set()
    with db.tx():
        for team_id, lado in ((fx["home_id"], "home_name"), (fx["away_id"], "away_name")):
            al = alineaciones.get(team_id)
            if al is None:
                continue
            titulares |= set(al["titulares"])
            db.conn.execute("DELETE FROM lineups WHERE fixture_id = ? AND team_id = ?", (fx["id"], team_id))
            db.conn.executemany(
                "INSERT INTO lineups(fixture_id, team_id, player_id, name, position) VALUES (?, ?, ?, ?, ?)",
                [(fx["id"], team_id, pid, n, pos) for pid, (n, pos) in al["titulares"].items()])
            impactos[team_id] = impacto_alineacion(db, team_id, fx[lado], fx["date_utc"], al["titulares"])
    for imp in impactos.values():
        res.notas += imp.notas
    f_local = impactos[fx["home_id"]].factor if fx["home_id"] in impactos else 1.0
    f_visit = impactos[fx["away_id"]].factor if fx["away_id"] in impactos else 1.0

    a = analyze_fixture(db, fx, cfg, historico=historico,
                        ajuste=lambda e: aplicar_impacto(e, f_local, f_visit))
    if titulares:
        a.markets = [m for m in a.markets if m.scope != "player" or m.player_id in titulares]
    mercados = {m.key: m for m in a.markets}

    picks = db.conn.execute(
        "SELECT * FROM picks WHERE fixture_id = ? AND result IS NULL", (fx["id"],)).fetchall()
    with db.tx():
        for p in picks:
            estado, nota, m = _evaluar_pick(p, mercados, titulares, cfg)
            prob = None if m is None else (m.final_prob if m.final_prob is not None else m.prob)
            db.conn.execute("UPDATE picks SET estado = ?, nota = ?, prob_chequeo = ?, odd_chequeo = ? WHERE id = ?",
                            (estado, nota, prob, None if m is None else m.odd, p["id"]))
            texto = f"{p['label']}" + (f" ({nota})" if nota else "") + (" [combinada]" if p["combo_id"] else "")
            (res.confirmadas if estado == "confirmada" else res.anuladas).append(texto)
        # Selecciones que aparecen con la información nueva (se guardan para medir su acierto).
        ya = {p["market_key"] for p in picks if p["combo_id"] is None}
        if a.ok:
            for m in candidates(a, cfg):
                if m.key in ya:
                    continue
                db.conn.execute(
                    "INSERT INTO picks(fecha, fixture_id, market_key, label, prob, odd, edge, created_at, estado, "
                    "nota, prob_chequeo, odd_chequeo) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'nueva', ?, ?, ?)",
                    (fx["fecha_local"], fx["id"], m.key, m.label, m.final_prob or m.prob, m.odd, m.edge, now_iso(),
                     "aparece tras el chequeo", m.final_prob or m.prob, m.odd))
                res.nuevas.append(f"{m.label} ({(m.final_prob or m.prob) * 100:.0f}%, cuota {m.odd or m.fair_odd:.2f})")
        db.conn.execute(
            "INSERT OR REPLACE INTO lineup_checks(fixture_id, checked_at, lineups_ok, detail) VALUES (?, ?, ?, ?)",
            (fx["id"], now_iso(), int(completas), json.dumps({"notas": res.notas, "factor_local": f_local,
                                                               "factor_visitante": f_visit}, ensure_ascii=False)))
    return res


def _evaluar_pick(p, mercados: dict, titulares: set[int], cfg: Config):
    key = p["market_key"]
    if key.startswith("player:") and titulares and int(key.split(":")[1]) not in titulares:
        return "anulada", "no es titular", None
    m = mercados.get(key)
    if m is None:
        return "anulada", "mercado no disponible tras el chequeo", None
    prob = m.final_prob if m.final_prob is not None else m.prob
    if p["combo_id"] is not None:
        if prob < p["prob"] - CAIDA_MAX_COMBINADA:
            return "anulada", f"probabilidad baja de {p['prob']:.0%} a {prob:.0%}", m
        return "confirmada", f"{prob:.0%}", m
    if prob < cfg.prob_min_seleccion:
        return "anulada", f"probabilidad baja a {prob:.0%}", m
    if m.odd is not None and (m.edge or 0) < cfg.valor_min:
        return "anulada", f"sin valor con la cuota actual {m.odd:.2f}", m
    cuota = f", cuota {m.odd:.2f}" if m.odd else ""
    return "confirmada", f"{prob:.0%}{cuota}", m


def chequear(db: Database, api: ApiFootball, cfg: Config, fecha: str, ahora: datetime | None = None,
             ventana_min: int = 60, historico=None, forzar: bool = False,
             con_cuotas: bool = True, bzzoiro=None) -> list[ResultadoChequeo]:
    ahora = ahora or datetime.now(timezone.utc)
    out = []
    pendientes = partidos_a_chequear(db, fecha, ahora, timedelta(minutes=ventana_min), forzar)
    eventos_bz = None
    if bzzoiro is not None and pendientes:
        try:
            eventos_bz = bzzoiro.partidos(ahora.date(), (ahora + timedelta(minutes=ventana_min)).date())
        except (ApiError, PresupuestoAgotado, requests.RequestException, ValueError) as e:
            logging.getLogger(__name__).warning("Bzzoiro no disponible: %s", e)
    for fx in pendientes:
        try:
            out.append(chequear_partido(db, api, cfg, fx, ahora, historico, con_cuotas, bzzoiro, eventos_bz))
        except PresupuestoAgotado as e:
            logging.getLogger(__name__).warning("%s", e)
            out.append(ResultadoChequeo(fx["id"], f"{fx['home_name']} vs {fx['away_name']}", fx["date_utc"],
                                        "sin_presupuesto", [str(e)]))
            break
    return out


def agenda(db: Database, fecha: str, ahora: datetime | None = None, antelacion_min: int = 35,
           agrupar_min: int = 15) -> list[dict]:
    """Cuándo lanzar `chequeo`: un momento por grupo de partidos que empiezan casi a la vez."""
    ahora = ahora or datetime.now(timezone.utc)
    pendientes = partidos_a_chequear(db, fecha, ahora, timedelta(days=2))
    grupos: list[dict] = []
    for fx in pendientes:
        inicio = datetime.fromisoformat(fx["date_utc"])
        if grupos and inicio - grupos[-1]["primer_inicio"] <= timedelta(minutes=agrupar_min):
            grupos[-1]["partidos"].append(f"{fx['home_name']} vs {fx['away_name']}")
            continue
        grupos.append({"primer_inicio": inicio, "partidos": [f"{fx['home_name']} vs {fx['away_name']}"]})
    return [{"chequeo_utc": max(ahora, g["primer_inicio"] - timedelta(minutes=antelacion_min)).isoformat(timespec="minutes"),
             "inicio_utc": g["primer_inicio"].isoformat(timespec="minutes"), "partidos": g["partidos"]}
            for g in grupos]


def estado_combinadas(db: Database, fecha: str) -> list[dict]:
    out = []
    for c in db.conn.execute("SELECT * FROM combos WHERE fecha = ? AND result IS NULL", (fecha,)).fetchall():
        legs = db.conn.execute("SELECT label, estado FROM picks WHERE combo_id = ?", (c["id"],)).fetchall()
        estados = [l["estado"] for l in legs]
        if "anulada" in estados:
            estado = "rota"
        elif all(e == "confirmada" for e in estados):
            estado = "confirmada"
        else:
            estado = f"pendiente ({sum(e == 'confirmada' for e in estados)} de {len(estados)} chequeadas)"
        out.append({"perfil": c["perfil"], "cuota": c["odd"], "prob": c["prob"], "estado": estado,
                    "selecciones": [(l["label"], l["estado"] or "sin chequear") for l in legs]})
    return out


def render_chequeo(db: Database, fecha: str) -> str:
    """Informe del día con todo lo chequeado hasta ahora (se regenera en cada ejecución)."""
    out = [f"# Apuestas finales tras el chequeo de alineaciones — {fecha}", ""]
    filas = db.conn.execute(
        """SELECT p.*, f.date_utc, h.name AS home, a.name AS away, c.detail, c.lineups_ok
           FROM picks p JOIN fixtures f ON f.id = p.fixture_id JOIN teams h ON h.id = f.home_id
           JOIN teams a ON a.id = f.away_id JOIN lineup_checks c ON c.fixture_id = f.id
           WHERE p.fecha = ? ORDER BY f.date_utc, p.combo_id IS NOT NULL, p.id""", (fecha,)).fetchall()
    actual = None
    for r in filas:
        if r["fixture_id"] != actual:
            actual = r["fixture_id"]
            out += ["", f"## {r['home']} vs {r['away']} ({r['date_utc'][11:16]} UTC)",
                    "" if r["lineups_ok"] else "_Sin alineaciones confirmadas: chequeado solo con cuotas._"]
            out += [f"- _{n}_" for n in json.loads(r["detail"] or "{}").get("notas", [])]
            out.append("")
        marca = {"confirmada": "✅", "anulada": "❌", "nueva": "🆕"}.get(r["estado"], "·")
        cuota = f", cuota {r['odd_chequeo']:.2f}" if r["odd_chequeo"] else ""
        tipo = " (pierna de combinada)" if r["combo_id"] else ""
        nota = f" — {r['nota']}" if r["nota"] else ""
        if r["estado"] == "anulada":
            cuota = ""
        out.append(f"- {marca} {r['label']}{tipo}: {r['estado'] or 'sin chequear'}{nota}{cuota}")
    combos = estado_combinadas(db, fecha)
    if combos:
        out += ["", "## Combinadas del día", ""]
        for c in combos:
            cuota = f"cuota {c['cuota']:.2f}" if c["cuota"] else "cuota justa"
            out.append(f"- **{c['perfil']}** ({cuota}, prob. {c['prob']:.1%}): {c['estado']}")
    return "\n".join(out) + "\n"
