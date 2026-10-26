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


def mezcla_vigente(cfg: dict) -> Mezcla:
    """Coeficientes de la mezcla (se ajustan con las líneas fuera de muestra de la validación si faltan)."""
    ruta = RAIZ / cfg.get("apuestas", {}).get("mezcla", "data/modelos/mezcla_pts.json")
    if ruta.exists():
        return Mezcla.cargar(ruta)
    cache = RAIZ / "data" / "cache" / "puntos_lineas_oos.parquet"
    if not cache.exists():
        log.warning("Sin validación de puntos: se usa la probabilidad del mercado (peso del modelo 0)")
        return Mezcla()
    m = ajustar(pd.read_parquet(cache), kind=cfg.get("apuestas", {}).get("mezcla_con", "cierre"))
    m.guardar(ruta)
    return m


def nombres_partidos(con, ids) -> dict:
    filas = con.execute("""SELECT g.game_id, a.abbr || ' @ ' || h.abbr FROM games g
                           JOIN teams h ON h.team_id = g.home_id JOIN teams a ON a.team_id = g.away_id
                           WHERE g.game_id IN (SELECT unnest(?))""", [list(ids)]).fetchall()
    return dict(filas)


def ejecutar(con, cfg: dict, fecha: str, max_razones: int = 300) -> dict:
    from .models import minutos as mm
    from .models import puntos as mp
    liquidadas = registro.liquidar(con)
    out, sim = mp.proyectar(con, cfg, fecha, n_sims=cfg["puntos"]["simulaciones"])
    if out.empty:
        return {"tabla": pd.DataFrame(), "liquidadas": liquidadas}
    filas, sims = sim["filas"], sim["sims"]
    ahora = db.ahora_utc()
    cuotas = asof.cuotas_en(con, ahora, list(filas["game_id"].unique()))
    lineas = seleccion.lineas_con_lados(cuotas)
    cfg_ap = cfg.get("apuestas", {})
    banca = registro.banca_actual(con, cfg_ap.get("banca_inicial", 1000.0))
    tabla = seleccion.evaluar(lineas, filas, sims, mezcla_vigente(cfg), cfg, seleccion.estado_mercados(con), banca)
    if tabla.empty:
        log.warning("No hay cuotas capturadas para los partidos del %s", fecha)
        return {"tabla": tabla, "liquidadas": liquidadas, "banca": banca}
    partidos = nombres_partidos(con, tabla["game_id"].unique())
    tabla["partido"] = tabla["game_id"].map(partidos)
    tabla["p_over_modelo"] = tabla["p_modelo_over"]
    tabla["p_under_modelo"] = 1 - tabla["p_modelo_over"]

    # Razones SHAP de las líneas con EV > 0 (las demás no se van a apostar).
    m_pts = mp.modelo_vigente(con, cfg, RAIZ / cfg["puntos"]["modelo"])
    m_min = mm.modelo_vigente(con, cfg, RAIZ / cfg["minutos"]["modelo"])
    con_ev = tabla.index[tabla["ev"] > 0][:max_razones]
    tabla["razones"] = ""
    if len(con_ev):
        idx = tabla.loc[con_ev, "index"].to_numpy()
        f_sel = filas.loc[idx].reset_index(drop=True)
        contrib = explicar.contribuciones(m_pts, m_min, f_sel)
        txt = explicar.razones(contrib, f_sel, pd.Series(tabla.loc[con_ev, "lado"].to_numpy()))
        tabla.loc[con_ev, "razones"] = txt.to_numpy()

    registro.guardar_predicciones(con, tabla, ahora, pd.to_datetime(fecha).date())
    nuevas = registro.registrar_sugeridas(con, tabla, pd.to_datetime(fecha).date(), partidos)
    exportar(tabla, fecha, banca)
    return {"tabla": tabla, "liquidadas": liquidadas, "banca": banca, "sugeridas_nuevas": nuevas}


def exportar(tabla: pd.DataFrame, fecha: str, banca: float) -> Path:
    carpeta = RAIZ / "reportes" / "diario"
    carpeta.mkdir(parents=True, exist_ok=True)
    t = tabla[[c for c in COLUMNAS if c in tabla.columns]].rename(columns=COLUMNAS)
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
    ruta = carpeta / f"{fecha}.md"
    ruta.write_text("\n".join(md), encoding="utf-8")
    return ruta
