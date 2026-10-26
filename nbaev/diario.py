"""Flujo diario: datos -> proyección -> comparación con cuotas -> tabla de picks, registro y banca.

    python -m nbaev diario                 # actualiza datos y cuotas, proyecta y exporta reportes/diario/AAAA-MM-DD.*
    python -m nbaev diario --sin-actualizar

La tabla incluye TODAS las líneas evaluadas (también las descartadas, con el motivo). Solo los picks de
mercados VALIDADOS reciben monto; en mercados sin validar o desactivados el monto es 0 aunque haya EV+.
"""
from __future__ import annotations

import json
import logging
from pathlib import Path

import pandas as pd

from .betting import explicar, registro, seleccion
from .betting.mezcla import Mezcla, ajustar
from .config import RAIZ
from .data import asof, db

log = logging.getLogger(__name__)

COLUMNAS = {
    "name": "jugador", "partido": "partido", "market": "mercado", "period": "periodo", "line": "línea", "lado": "lado",
    "proyeccion": "proyección", "p_over_modelo": "P(over) modelo", "p_under_modelo": "P(under) modelo",
    "cuota": "cuota", "book": "casa", "p_justa": "prob. justa", "p_final": "prob. final", "edge": "edge", "ev": "EV",
    "monto": "monto sugerido", "estado_mercado": "estado del mercado", "pick": "pick", "motivo_descarte": "motivo",
    "razones": "razones (SHAP)", "min_si_juega": "minutos proyectados", "estado_lesion": "parte médico",
}


def mezclas_vigentes(cfg: dict) -> dict[str, Mezcla]:
    """Mezcla modelo + mercado de cada mercado, ajustada con las líneas reales fuera de muestra de la
    validación (puntos: fase 3; resto: fase 6). Mercados sin validación usan una mezcla por defecto
    conservadora (70 % mercado) y en cualquier caso no reciben monto hasta validarse."""
    import json
    ruta = RAIZ / cfg.get("apuestas", {}).get("mezclas", "data/modelos/mezclas.json")
    if ruta.exists():
        return {k: Mezcla(**v) for k, v in json.loads(ruta.read_text(encoding="utf-8")).items()}
    kind = cfg.get("apuestas", {}).get("mezcla_con", "cierre")
    out = {"_defecto": Mezcla(mercado="_defecto", peso_mercado=0.7, peso_modelo=0.3, sd_edge=0.04)}
    cache = RAIZ / "data" / "cache"
    if (cache / "mercados_lineas_oos.parquet").exists():
        lin = pd.read_parquet(cache / "mercados_lineas_oos.parquet")
        for mk, d in lin.groupby("market"):
            if (d["kind"] == kind).sum() >= 300:
                out[mk] = ajustar(d, kind=kind, mercado=mk)
    elif (cache / "puntos_lineas_oos.parquet").exists():
        out["pts"] = ajustar(pd.read_parquet(cache / "puntos_lineas_oos.parquet"), kind=kind)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    from dataclasses import asdict
    ruta.write_text(json.dumps({k: asdict(v) for k, v in out.items()}, indent=1), encoding="utf-8")
    return out


def nombres_partidos(con, ids) -> dict:
    filas = con.execute("""SELECT g.game_id, a.abbr || ' @ ' || h.abbr FROM games g
                           JOIN teams h ON h.team_id = g.home_id JOIN teams a ON a.team_id = g.away_id
                           WHERE g.game_id IN (SELECT unnest(?))""", [list(ids)]).fetchall()
    return dict(filas)


def ejecutar(con, cfg: dict, fecha: str, max_razones: int = 400) -> dict:
    from .betting import combinadas
    from .models import minutos as mm
    from .models import proyeccion
    liquidadas = registro.liquidar(con)
    salida = proyeccion.proyectar(con, cfg, fecha, n_sims=cfg["puntos"]["simulaciones"])
    if not salida:
        return {"tabla": pd.DataFrame(), "liquidadas": liquidadas}
    filas, sims = salida["filas"], salida["sims"]
    proyeccion.guardar_sims(salida, fecha)
    ahora = db.ahora_utc()
    cuotas = asof.cuotas_en(con, ahora, list(filas["game_id"].unique()))
    lineas = seleccion.lineas_con_lados(cuotas)
    cfg_ap = cfg.get("apuestas", {})
    banca = registro.banca_actual(con, cfg_ap.get("banca_inicial", 1000.0))
    tabla = seleccion.evaluar(lineas, filas, sims, mezclas_vigentes(cfg), cfg, seleccion.estado_mercados(con), banca,
                              primer=salida["primer"])
    partidos = nombres_partidos(con, filas["game_id"].unique())
    maximos = {gid: combinadas.maximo(filas, sims, gid).head(5) for gid in filas["game_id"].unique()}
    if tabla.empty:
        log.warning("No hay cuotas capturadas para los partidos del %s", fecha)
        exportar(tabla, fecha, banca, maximos, partidos, salida["primer"], filas)
        return {"tabla": tabla, "liquidadas": liquidadas, "banca": banca}
    tabla["partido"] = tabla["game_id"].map(partidos)
    tabla["p_over_modelo"] = tabla["p_modelo_over"]
    tabla["p_under_modelo"] = 1 - tabla["p_modelo_over"]

    # Razones SHAP de las líneas con EV > 0 (las demás no se van a apostar), con el modelo de cada mercado.
    m_min = mm.modelo_vigente(con, cfg, RAIZ / cfg["minutos"]["modelo"])
    tabla["razones"] = ""
    con_ev = tabla.index[(tabla["ev"] > 0) & (tabla["market"] != "primera_canasta")][:max_razones]
    for mk, idx in tabla.loc[con_ev].groupby("market").groups.items():
        f_sel = filas.loc[tabla.loc[idx, "index"].to_numpy()].reset_index(drop=True)
        contrib = explicar.contribuciones(salida["modelo"], m_min, f_sel, mk)
        txt = explicar.razones(contrib, f_sel, pd.Series(tabla.loc[idx, "lado"].to_numpy()))
        tabla.loc[idx, "razones"] = txt.to_numpy()
    tabla.loc[tabla["market"] == "primera_canasta", "razones"] = "salto inicial, quinteto titular y reparto de primeras canastas"

    registro.guardar_predicciones(con, tabla, ahora, pd.to_datetime(fecha).date())
    nuevas = registro.registrar_sugeridas(con, tabla, pd.to_datetime(fecha).date(), partidos)
    exportar(tabla, fecha, banca, maximos, partidos, salida["primer"], filas)
    # Copia de lo evaluado para el seguimiento posterior (docs/seguimiento/), aunque la base se pierda.
    from . import seguimiento
    seguimiento.exportar(con, fecha)
    return {"tabla": tabla, "liquidadas": liquidadas, "banca": banca, "sugeridas_nuevas": nuevas}


def exportar(tabla: pd.DataFrame, fecha: str, banca: float, maximos: dict | None = None, partidos: dict | None = None,
             primer: pd.DataFrame | None = None, filas: pd.DataFrame | None = None) -> Path:
    carpeta = RAIZ / "reportes" / "diario"
    carpeta.mkdir(parents=True, exist_ok=True)
    if tabla.empty:
        tabla = pd.DataFrame(columns=list(COLUMNAS) + ["EV"])
    t = tabla[[c for c in COLUMNAS if c in tabla.columns]].rename(columns=COLUMNAS)
    if "pick" not in t:
        t["pick"] = pd.Series(dtype=bool)
    t.to_csv(carpeta / f"{fecha}.csv", index=False)
    (carpeta / f"{fecha}.json").write_text(json.dumps(t.to_dict("records"), ensure_ascii=False, default=str, indent=1),
                                           encoding="utf-8")
    picks = t[t["pick"]]
    validados = picks[picks["monto sugerido"] > 0]
    md = [f"# Props NBA del {fecha}", "",
          f"Banca actual: {banca:,.2f}. Líneas evaluadas: {len(t)}. Picks con EV+ que pasan todos los filtros: "
          f"{len(picks)}; con monto (mercado validado): {len(validados)}.", "",
          "> Ningún mercado tiene ventaja demostrada hasta que el backtest lo valida. Un pick de un mercado sin "
          "validar o desactivado es solo informativo (monto 0). Las apuestas implican riesgo de perder dinero.", ""]
    cols = ["jugador", "partido", "mercado", "línea", "lado", "proyección", "P(over) modelo", "cuota", "casa",
            "prob. justa", "prob. final", "edge", "EV", "monto sugerido", "estado del mercado", "razones (SHAP)"]
    if not picks.empty:
        md += ["## Picks", "", picks[cols].to_markdown(index=False, floatfmt=".3f"), ""]
    top = t[~t["pick"]].sort_values("EV", ascending=False).head(25)
    if not top.empty:
        md += ["## Mayor EV descartadas (y por qué)", "",
               top[["jugador", "mercado", "línea", "lado", "cuota", "prob. final", "edge", "EV", "motivo"]]
               .to_markdown(index=False, floatfmt=".3f"), ""]
    # Mercados sin cuotas en la fuente: probabilidades y cuotas justas para comparar a mano (p. ej. con bet365).
    if maximos:
        md += ["## Máximo anotador del partido (cuota justa, sin validar)", ""]
        for gid, t_max in maximos.items():
            md += [f"**{(partidos or {}).get(gid, gid)}**: " + ", ".join(
                f"{r.jugador} {r.p:.0%} ({r.cuota_justa:.1f})" for r in t_max.itertuples()), ""]
    if primer is not None and not primer.empty and filas is not None:
        nombres = dict(zip(filas["player_id"], filas["name"]))
        md += ["## Primera canasta del partido (cuota justa, sin validar)", ""]
        for gid, g in primer[primer["player_id"] != "SUPLENTE"].groupby("game_id"):
            top = g.sort_values("p_partido", ascending=False).head(4)
            md += [f"**{(partidos or {}).get(gid, gid)}**: " + ", ".join(
                f"{nombres.get(r.player_id, r.player_id)} {r.p_partido:.1%} ({1 / r.p_partido:.1f})"
                for r in top.itertuples()), ""]
    ruta = carpeta / f"{fecha}.md"
    ruta.write_text("\n".join(md), encoding="utf-8")
    return ruta
