"""Validación del modelo de puntos (fase 3): walk-forward mensual con minutos proyectados fuera de muestra.

Para cada mes de prueba se entrena con todo lo anterior y se predicen los puntos de quienes jugaron (las
props se anulan si el jugador no juega). Se mide:
- error de la media frente a los puntos reales (baseline, LightGBM y, donde hay prop, la línea de la casa);
- calibración de la distribución simulada (cuantiles);
- probabilidad de superar las líneas REALES de las casas (consenso de SportsGameOdds, apertura y cierre):
  log loss y Brier del modelo frente a la probabilidad justa del mercado (sin margen).
"""
from __future__ import annotations

import logging
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd

from ..features import produccion as fp
from ..models import puntos as mp
from ..models import simulacion as sim
from .walkforward import bloques_mensuales

log = logging.getLogger(__name__)


# Tolerancia entre la línea de cierre y la de apertura para dar el cierre por bueno.
TOLERANCIA_CIERRE = 3.0


def lineas_pts(con: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    """Líneas de puntos (partido completo) con cuota over/under y probabilidad justa (multiplicativa).

    Los "cierres" de SportsGameOdds de octubre a mediados de enero de 2025-26 incluyen ~10 % de líneas
    capturadas con el partido empezado (líneas muy por debajo de lo normal del jugador; la tasa cae al
    nivel natural cuando aparece la apertura). Por eso un cierre solo se acepta si hay apertura del mismo
    jugador y partido y la línea no se mueve más de TOLERANCIA_CIERRE puntos."""
    df = con.execute("""
        SELECT game_id, player_id, kind, line,
               max(CASE WHEN side = 'over' THEN odds END) AS cuota_over,
               max(CASE WHEN side = 'under' THEN odds END) AS cuota_under
        FROM prop_odds
        WHERE market = 'pts' AND period = 'game' AND bet_type = 'ou' AND book = 'consenso'
          AND kind IN ('apertura', 'cierre') AND player_id IS NOT NULL
        GROUP BY ALL HAVING cuota_over IS NOT NULL AND cuota_under IS NOT NULL""").df()
    ap = df[df["kind"] == "apertura"].groupby(["game_id", "player_id"])["line"].median().rename("linea_apertura")
    df = df.merge(ap, on=["game_id", "player_id"], how="left")
    valido = (df["kind"] == "apertura") | ((df["line"] - df["linea_apertura"]).abs() <= TOLERANCIA_CIERRE)
    df = df[valido].copy()
    io, iu = 1 / df["cuota_over"], 1 / df["cuota_under"]
    df["margen"] = io + iu - 1
    df["p_mercado"] = io / (io + iu)
    return df[(df["margen"] > -0.02) & (df["margen"] < 0.25)]


def ajustar_paliza(train: pd.DataFrame, disp: sim.Dispersion) -> None:
    """Pendiente de los minutos frente al margen anómalo, con los minutos proyectados fuera de muestra."""
    d = train.dropna(subset=["min_si_juega", "margen_real", "spread_equipo"])
    if len(d) < 1000:
        return
    disp.sd_margen = float((d["margen_real"] + d["spread_equipo"]).std())
    exceso = d["margen_real"].abs() - np.sqrt(d["spread_equipo"] ** 2 + (disp.sd_margen * 0.7979) ** 2)
    resid = d["minutes"] - d["min_si_juega"]
    for nombre, mask in (("paliza_titular", d["min_base"] >= 28), ("paliza_banquillo", d["min_base"] < 20)):
        x, y = exceso[mask], resid[mask]
        setattr(disp, nombre, float(((x - x.mean()) * (y - y.mean())).sum() / ((x - x.mean()) ** 2).sum()))


def validar(con: duckdb.DuckDBPyConnection, minutos_oos: pd.DataFrame, desde: str = "2023-10-01",
            n_sims: int = 2000, semilla: int = 11) -> dict:
    df = fp.construir(con)
    cols_min = ["game_id", "player_id", "min_si_juega", "min_q10", "min_q50", "min_q90", "p_dnp"]
    df = df.merge(minutos_oos[cols_min], on=["game_id", "player_id"], how="left")
    lineas = lineas_pts(con)
    filas, por_linea = [], []
    for ini, fin in bloques_mensuales(df["start_utc"], desde):
        train = df[df["start_utc"] < ini]
        test = df[(df["start_utc"] >= ini) & (df["start_utc"] < fin) & df["min_si_juega"].notna()].copy()
        if test.empty:
            continue
        m = mp.entrenar(train)
        ajustar_paliza(train, m.disp)
        res = {}
        for nombre, usar in (("base", False), ("lgb", True)):
            entrada = mp.entrada_simulacion(m, test, usar_lgb=usar)
            s = sim.simular(entrada, m.disp, n_sims=n_sims, semilla=semilla)["pts"]
            res[nombre] = s
            test[f"media_{nombre}"] = s.mean(axis=1)
            test[f"tasa_{nombre}"] = entrada["tasa_pts"].to_numpy()
        # PIT aleatorizado (la prueba de calibración correcta para una variable discreta): uniforme si la
        # distribución simulada es la correcta.
        y = test["pts"].to_numpy()[:, None]
        u = np.random.default_rng(semilla).uniform(size=len(test))
        for nombre in ("base", "lgb"):
            test[f"pit_{nombre}"] = (res[nombre] < y).mean(1) + u * (res[nombre] == y).mean(1)
        test["bloque"] = ini.strftime("%Y-%m")
        filas.append(test)

        # Probabilidades frente a las líneas reales de ese mes.
        lt = lineas.merge(test[["game_id", "player_id", "pts"]].reset_index(), on=["game_id", "player_id"])
        if not lt.empty:
            i = lt["index"].map({ix: k for k, ix in enumerate(test.index)}).to_numpy()
            for nombre in ("base", "lgb"):
                p_over, p_push = sim.prob_over(res[nombre][i], lt["line"].to_numpy())
                lt[f"p_{nombre}"] = p_over / np.clip(1 - p_push, 1e-6, None)
            if m.cuantiles:
                lt["p_cuant"] = mp.cdf_cuantiles(m, test.loc[lt["index"]], lt["line"].to_numpy())
            lt["bloque"] = ini.strftime("%Y-%m")
            por_linea.append(lt)
        log.info("Bloque %s: %d jugadores, %d líneas; dispersión %s", ini.strftime("%Y-%m"), len(test), len(lt),
                 {k: round(v, 3) for k, v in vars(m.disp).items()})
    pred = pd.concat(filas, ignore_index=True)
    lin = pd.concat(por_linea, ignore_index=True) if por_linea else pd.DataFrame()
    if not lin.empty:
        lin = lin[lin["pts"] != lin["line"]].copy()        # los empates (push) se devuelven
        lin["y"] = (lin["pts"] > lin["line"]).astype(float)
    return {"pred": pred, "lineas": lin, "importancia": importancia(mp.entrenar(df, cuantilico=False))}


def importancia(m: mp.ModeloPuntos) -> pd.DataFrame:
    g = m.tasa.feature_importance("gain")
    return (pd.DataFrame({"feature": mp.FEATURES_PTS, "ganancia": g / g.sum()})
            .sort_values("ganancia", ascending=False).reset_index(drop=True))


# --- Métricas -----------------------------------------------------------------------------------------

def _logloss(p, y):
    p = np.clip(p, 1e-4, 1 - 1e-4)
    return float(-(y * np.log(p) + (1 - y) * np.log(1 - p)).mean())


def tabla_media(pred: pd.DataFrame, lin: pd.DataFrame) -> pd.DataFrame:
    filas = []
    for seg, d in (("todos los que jugaron", pred),
                   ("con prop de puntos", pred.merge(lin[["game_id", "player_id"]].drop_duplicates(),
                                                     on=["game_id", "player_id"]))):
        fila = {"segmento": seg, "n": len(d), "MAE baseline": (d["media_base"] - d["pts"]).abs().mean(),
                "MAE LightGBM": (d["media_lgb"] - d["pts"]).abs().mean(),
                "sesgo LightGBM": (d["media_lgb"] - d["pts"]).mean()}
        filas.append(fila)
    cierre = lin[lin["kind"] == "cierre"].drop_duplicates(["game_id", "player_id"])
    cierre = cierre.merge(pred[["game_id", "player_id", "media_lgb"]], on=["game_id", "player_id"])
    filas.append({"segmento": "con línea de cierre: línea de la casa como estimación", "n": len(cierre),
                  "MAE baseline": np.nan, "MAE LightGBM": (cierre["media_lgb"] - cierre["pts"]).abs().mean(),
                  "MAE línea casa": (cierre["line"] - cierre["pts"]).abs().mean(), "sesgo LightGBM": np.nan})
    return pd.DataFrame(filas)


def tabla_pit(pred: pd.DataFrame) -> pd.DataFrame:
    """Fracción de casos en cada decil del PIT (ideal: 0,10 en todos)."""
    filas = []
    for nombre in ("base", "lgb"):
        h = np.histogram(pred[f"pit_{nombre}"], bins=np.linspace(0, 1, 11))[0] / len(pred)
        filas.append({"modelo": nombre, **{f"d{i + 1}": v for i, v in enumerate(h)}})
    return pd.DataFrame(filas)


def tabla_probabilidades(lin: pd.DataFrame) -> pd.DataFrame:
    filas = []
    for kind in ("apertura", "cierre"):
        d = lin[lin["kind"] == kind]
        if d.empty:
            continue
        for nombre, col in (("mercado (sin margen)", "p_mercado"), ("baseline simulado", "p_base"),
                            ("LightGBM simulado", "p_lgb"), ("LightGBM cuantílico", "p_cuant")):
            if col not in d:
                continue
            filas.append({"líneas": kind, "modelo": nombre, "n": len(d), "log loss": _logloss(d[col], d["y"]),
                          "brier": float(((d[col] - d["y"]) ** 2).mean())})
    return pd.DataFrame(filas)


def tabla_calibracion(lin: pd.DataFrame, col: str = "p_lgb") -> pd.DataFrame:
    tr = pd.cut(lin[col], [0, 0.2, 0.3, 0.4, 0.45, 0.5, 0.55, 0.6, 0.7, 0.8, 1.0])
    t = (lin.assign(tramo=tr).groupby("tramo", observed=True)
         .agg(n=("y", "size"), p_media=(col, "mean"), frecuencia_real=("y", "mean")).reset_index())
    t["tramo"] = t["tramo"].astype(str)
    return t


def bootstrap_logloss(lin: pd.DataFrame, a: str, b: str, n: int = 1000, semilla: int = 3) -> dict:
    """IC 95 % de logloss(a) - logloss(b) remuestreando partidos."""
    def ll(p, y):
        p = np.clip(p, 1e-4, 1 - 1e-4)
        return -(y * np.log(p) + (1 - y) * np.log(1 - p))
    e = ll(lin[a], lin["y"]) - ll(lin[b], lin["y"])
    g = e.groupby(lin["game_id"]).agg(["sum", "size"])
    s, c = g["sum"].to_numpy(), g["size"].to_numpy()
    idx = np.random.default_rng(semilla).integers(0, len(s), size=(n, len(s)))
    difs = s[idx].sum(1) / c[idx].sum(1)
    return {"diferencia": s.sum() / c.sum(), "ic95": (float(np.quantile(difs, 0.025)), float(np.quantile(difs, 0.975)))}


def mezcla_walk_forward(lin: pd.DataFrame, col: str = "p_lgb") -> pd.DataFrame:
    """¿Aporta el modelo información que la línea no tiene? Regresión logística y ~ logit(mercado) +
    logit(modelo), ajustada cada mes solo con los meses anteriores. Si la mezcla mejora el log loss del
    mercado fuera de muestra, el modelo sabe algo que la casa no ha incorporado en esa línea."""
    from sklearn.linear_model import LogisticRegression

    def logit(p):
        p = np.clip(p, 1e-3, 1 - 1e-3)
        return np.log(p / (1 - p))

    filas = []
    for kind in ("apertura", "cierre"):
        d = lin[lin["kind"] == kind].copy()
        d["p_mezcla"], coefs = np.nan, []
        for b in sorted(d["bloque"].unique()):
            tr, te = d[d["bloque"] < b], d["bloque"] == b
            if len(tr) < 1500:
                continue
            m = LogisticRegression(C=1e3).fit(np.column_stack([logit(tr["p_mercado"]), logit(tr[col])]), tr["y"])
            coefs.append(m.coef_[0])
            d.loc[te, "p_mezcla"] = m.predict_proba(
                np.column_stack([logit(d.loc[te, "p_mercado"]), logit(d.loc[te, col])]))[:, 1]
        e = d.dropna(subset=["p_mezcla"])
        if e.empty:
            continue
        b = bootstrap_logloss(e, "p_mezcla", "p_mercado")
        c = np.mean(coefs, axis=0)
        filas.append({"líneas": kind, "n": len(e), "meses": e["bloque"].nunique(),
                      "log loss mercado": _logloss(e["p_mercado"], e["y"]), "log loss mezcla": _logloss(e["p_mezcla"], e["y"]),
                      "diferencia": b["diferencia"], "IC 95 % inf": b["ic95"][0], "IC 95 % sup": b["ic95"][1],
                      "peso mercado": c[0], "peso modelo": c[1]})
    return pd.DataFrame(filas)


def informe(r: dict) -> str:
    f = lambda t: t.to_markdown(index=False, floatfmt=".4f")  # noqa: E731
    pred, lin = r["pred"], r["lineas"]
    partes = [
        "# Fase 3: modelo de puntos (validación walk-forward mensual)",
        f"{len(pred):,} actuaciones fuera de muestra ({pred['bloque'].min()} a {pred['bloque'].max()}) con minutos "
        "proyectados también fuera de muestra (fase 2). Distribución por simulación Monte Carlo (2.000 por jugador "
        "en validación; 10.000 en producción).",
        "## Media de puntos (error absoluto medio)", f(tabla_media(pred, lin)),
        "## Calibración de la distribución simulada: PIT aleatorizado por deciles (ideal 0,10 en cada uno)",
        f(tabla_pit(pred)),
    ]
    if not lin.empty:
        cierre = lin[lin["kind"] == "cierre"]
        partes += ["## Probabilidad de superar la línea real de la casa (sin empates)", f(tabla_probabilidades(lin)),
                   "## Calibración de P(over) del LightGBM simulado (líneas de cierre)", f(tabla_calibracion(cierre))]
        for a, b, txt in (("p_lgb", "p_base", "LightGBM simulado - baseline simulado"),
                          ("p_lgb", "p_mercado", "LightGBM simulado - mercado"),
                          ("p_cuant", "p_lgb", "LightGBM cuantílico - LightGBM simulado")):
            if a in cierre and b in cierre:
                bb = bootstrap_logloss(cierre, a, b)
                partes.append(f"- Log loss {txt} (cierre): {bb['diferencia']:+.4f}, IC 95 % "
                              f"[{bb['ic95'][0]:+.4f}, {bb['ic95'][1]:+.4f}]")
        partes += ["## ¿Aporta el modelo algo que la línea no tenga? Mezcla modelo + mercado (walk-forward)",
                   "Regresión logística sobre logit(mercado) y logit(modelo), reentrenada cada mes con los meses "
                   "anteriores. Diferencia negativa = la mezcla predice mejor que el mercado solo.",
                   f(mezcla_walk_forward(lin))]
    partes += ["## Importancia de las variables (tasa de puntos por minuto)", f(r["importancia"].head(15))]
    return "\n\n".join(partes)


def guardar(r: dict, carpeta: Path) -> None:
    carpeta.mkdir(parents=True, exist_ok=True)
    (carpeta / "fase3_puntos.md").write_text(informe(r), encoding="utf-8")
