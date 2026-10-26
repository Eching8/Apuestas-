"""Simulación Monte Carlo de la producción de cada jugador en un partido.

Cada simulación genera, para cada jugador: minutos -> intentos de tiro (de 2, de 3 y libres) -> aciertos.
Los puntos salen de esos componentes, así que puntos, triples, tiros de campo y libres anotados son
coherentes entre sí en cada simulación (y todas las líneas de un mercado salen de la misma distribución:
P(25+) nunca puede superar a P(20+)).

Distribuciones:
- Minutos si juega: normal con la media y el ancho de los cuantiles 10-90 de la fase 2, recortada a [1, 48],
  más un ajuste por paliza: en cada simulación se sortea el margen final del partido a partir del spread y,
  cuanto mayor es la diferencia respecto a lo esperado, menos juegan los titulares y más los suplentes.
- Intentos: binomial negativa (más varianza que Poisson). El reparto 2/3 es beta-binomial.
- Aciertos: beta-binomial (hay noches de acierto alto o bajo: más varianza que una binomial).
- Factores compartidos: ritmo del partido (todos los jugadores de ambos equipos) y acierto de cada equipo.
  Introducen la correlación entre jugadores que necesitan las combinadas y los mercados comparativos.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

Z90 = 1.2816  # cuantil 90 de la normal estándar


@dataclass
class Dispersion:
    """Parámetros de varianza estimados con datos (ver `estimar_dispersion`)."""
    tam_fga: float = 12.0        # tamaño de la binomial negativa de intentos de campo
    tam_fta: float = 2.5         # ... de tiros libres
    conc_3a: float = 40.0        # concentración beta del reparto de triples sobre los intentos
    conc_fg2: float = 60.0       # concentración beta del acierto de 2
    conc_fg3: float = 60.0       # ... de 3
    conc_ft: float = 40.0        # ... de libres
    sd_ritmo: float = 0.035      # desviación (log) del ritmo del partido respecto a lo esperado
    sd_acierto: float = 0.12     # desviación (logit) del acierto de cada equipo en el partido
    sd_margen: float = 12.5      # desviación del margen final respecto al spread
    paliza_titular: float = -0.30  # minutos por punto de margen anómalo (titulares: min_base >= 28)
    paliza_banquillo: float = 0.15  # ... (suplentes: min_base < 20)


def _beta_binomial(rng, n, p, conc):
    p = np.clip(p, 1e-4, 1 - 1e-4)
    q = rng.beta(p * conc, (1 - p) * conc)
    return rng.binomial(n, q)


def _negbin(rng, mu, tam):
    mu = np.maximum(mu, 1e-6)
    return rng.negative_binomial(tam, tam / (tam + mu))


def simular(jug: pd.DataFrame, disp: Dispersion, n_sims: int = 10_000, semilla: int | None = None,
            grupos: str = "game_id") -> dict[str, np.ndarray]:
    """Simula la producción de todos los jugadores de `jug` (pueden ser varios partidos).

    Columnas necesarias: game_id, team_id, min_media, min_sd, min_base, spread_equipo, r_fga, r_fg3a,
    r_fta, p_fg2, p_fg3, p_ft (tasas por minuto ya ajustadas al partido).
    Devuelve arrays (n_jugadores, n_sims) con min, pts, fgm, fg3m, ftm, fga, fg3a, fta.
    """
    rng = np.random.default_rng(semilla)
    n = len(jug)
    juegos, idx_juego = np.unique(jug[grupos].to_numpy(), return_inverse=True)
    equipos, idx_equipo = np.unique((jug[grupos].astype(str) + "|" + jug["team_id"].astype(str)).to_numpy(),
                                    return_inverse=True)

    # Factores compartidos por partido y por equipo.
    ritmo = np.exp(rng.normal(-0.5 * disp.sd_ritmo ** 2, disp.sd_ritmo, size=(len(juegos), n_sims)))[idx_juego]
    acierto = rng.normal(0, disp.sd_acierto, size=(len(equipos), n_sims))[idx_equipo]
    # Margen final (a favor del equipo del jugador) y su desviación absoluta respecto a lo esperado.
    spread = jug["spread_equipo"].fillna(0).to_numpy()[:, None]
    z = rng.normal(0, 1, size=(len(juegos), n_sims))[idx_juego]
    lado = np.where(jug["is_home"].fillna(1).to_numpy()[:, None] == 1, 1.0, -1.0)
    margen = -spread + disp.sd_margen * z * lado            # mismo sorteo, signo opuesto para el rival
    esperado = np.abs(spread) + 0.0                           # aproximación de E|margen| centrada en el spread
    exceso = np.abs(margen) - np.sqrt(esperado ** 2 + (disp.sd_margen * 0.7979) ** 2)

    base = jug["min_base"].fillna(0).to_numpy()[:, None]
    pend = np.where(base >= 28, disp.paliza_titular, np.where(base < 20, disp.paliza_banquillo, 0.0))
    mins = (jug["min_media"].to_numpy()[:, None] + jug["min_sd"].to_numpy()[:, None] * rng.normal(size=(n, n_sims))
            + pend * exceso)
    mins = np.clip(mins, 1.0, 48.0)

    def col(c):
        return jug[c].to_numpy(dtype=float)[:, None]

    fga = _negbin(rng, col("r_fga") * mins * ritmo, disp.tam_fga)
    reparto3 = np.clip(col("r_fg3a") / np.maximum(col("r_fga"), 1e-6), 0, 1)
    fg3a = _beta_binomial(rng, fga, np.broadcast_to(reparto3, fga.shape), disp.conc_3a)
    fg2a = fga - fg3a
    logit = lambda p: np.log(p / (1 - p))  # noqa: E731
    sig = lambda x: 1 / (1 + np.exp(-x))   # noqa: E731
    p2 = sig(logit(np.clip(col("p_fg2"), 0.05, 0.95)) + acierto)
    p3 = sig(logit(np.clip(col("p_fg3"), 0.05, 0.95)) + acierto)
    fg2m = _beta_binomial(rng, fg2a, p2, disp.conc_fg2)
    fg3m = _beta_binomial(rng, fg3a, p3, disp.conc_fg3)
    fta = _negbin(rng, col("r_fta") * mins * ritmo, disp.tam_fta)
    ftm = _beta_binomial(rng, fta, np.broadcast_to(np.clip(col("p_ft"), 0.05, 0.99), fta.shape), disp.conc_ft)
    return {"min": mins, "pts": 2 * fg2m + 3 * fg3m + ftm, "fgm": fg2m + fg3m, "fg3m": fg3m, "ftm": ftm,
            "fga": fga, "fg3a": fg3a, "fta": fta}


def prob_over(sims: np.ndarray, lineas: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """P(estadística > línea) y P(= línea) por fila (las líneas enteras pueden empatar: se devuelve el push)."""
    l = np.asarray(lineas, dtype=float)[:, None]
    return (sims > l).mean(axis=1), (sims == l).mean(axis=1)


def resumen(sims: np.ndarray, cuantiles=(0.1, 0.25, 0.5, 0.75, 0.9)) -> pd.DataFrame:
    q = np.quantile(sims, cuantiles, axis=1).T
    return pd.DataFrame(np.column_stack([sims.mean(axis=1), q]),
                        columns=["media"] + [f"q{int(c * 100)}" for c in cuantiles])


def estimar_dispersion(df: pd.DataFrame) -> Dispersion:
    """Estima la varianza de cada componente por el método de los momentos, con los minutos reales y las
    tasas previas al partido (las de `features.produccion`). Solo usa las filas que recibe (entrenamiento)."""
    d = df[(df["minutes"] >= 5)].copy()
    disp = Dispersion()

    def inv_tam(y, mu):
        # Var = mu + mu^2 / tam  ->  1/tam = E[(y-mu)^2 - mu] / E[mu^2]
        return max(((y - mu) ** 2 - mu).mean() / (mu ** 2).mean(), 1e-3)

    # Ritmo del partido: desviación del ritmo real respecto al esperado (en log).
    if "pace" in d and "ritmo_esp" in d:
        r = np.log(d["pace"] / (d["ritmo_esp"] * d["liga_pace"])).dropna()
        disp.sd_ritmo = float(np.clip(r.groupby(d.loc[r.index, "game_id"]).first().std(), 0.01, 0.08))
    v_ritmo = disp.sd_ritmo ** 2
    mu_fga = d["r_fga"] * d["minutes"]
    disp.tam_fga = 1 / max(inv_tam(d["fga"], mu_fga) - v_ritmo, 0.005)
    mu_fta = d["r_fta"] * d["minutes"]
    disp.tam_fta = 1 / max(inv_tam(d["fta"], mu_fta) - v_ritmo, 0.02)

    def conc(hechos, intentos, p):
        # Beta-binomial: Var = n p (1-p) [1 + (n-1)/(c+1)]  ->  c a partir del exceso de varianza.
        m = intentos >= 2
        h, n, p = hechos[m], intentos[m], p[m]
        exceso = (((h - n * p) ** 2) / (n * p * (1 - p)) - 1).mean() / (n - 1).mean()
        return float(np.clip(1 / max(exceso, 1e-3) - 1, 5, 500))

    disp.conc_3a = conc(d["fg3a"], d["fga"], (d["r_fg3a"] / d["r_fga"]).clip(0.01, 0.99))
    disp.conc_fg2 = conc(d["fgm"] - d["fg3m"], d["fga"] - d["fg3a"], d["p_fg2"])
    disp.conc_fg3 = conc(d["fg3m"], d["fg3a"], d["p_fg3"])
    disp.conc_ft = conc(d["ftm"], d["fta"], d["p_ft"])
    return disp
