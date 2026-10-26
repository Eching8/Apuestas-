# Fase 2: proyección de minutos (validación walk-forward mensual)

Filas evaluadas fuera de muestra: 102,378 (bloques 2023-10 a 2026-10). Cada mes se predice con un modelo entrenado solo con meses anteriores.

## Error absoluto medio (minutos) por segmento

| segmento                                 |      n |   MAE base (media exp.) |   MAE base normalizada a 240 |   MAE LightGBM |   MAE LightGBM + reparto |   sesgo LGB+reparto |
|:-----------------------------------------|-------:|------------------------:|-----------------------------:|---------------:|-------------------------:|--------------------:|
| todos                                    | 102378 |                   5.250 |                        5.235 |          4.491 |                    4.489 |               0.013 |
| con prop de puntos                       |  21582 |                   5.097 |                        5.262 |          4.524 |                    4.526 |              -0.255 |
| rotación (base >= 15 min)                |  62661 |                   5.007 |                        5.190 |          4.492 |                    4.500 |               0.010 |
| compañeros fuera (>= 15 min libres)      |  24795 |                   6.324 |                        6.261 |          5.158 |                    5.149 |              -0.002 |
| back-to-back                             |  16706 |                   5.543 |                        5.526 |          4.748 |                    4.747 |               0.005 |
| posible paliza (|spread| >= 12)          |  13884 |                   5.492 |                        5.376 |          4.679 |                    4.673 |               0.072 |
| vuelve tras >= 10 días                   |   3796 |                   6.339 |                        6.025 |          5.065 |                    5.059 |               0.262 |
| inicio de temporada (< 5 partidos)       |   9783 |                   5.959 |                        5.863 |          4.753 |                    4.740 |               0.025 |
| cambio de equipo reciente (< 5 partidos) |   5255 |                   6.343 |                        6.154 |          5.126 |                    5.091 |               0.059 |
| playoffs                                 |   6879 |                   5.113 |                        5.233 |          4.056 |                    4.041 |               0.010 |

## Por temporada

|   season |         n |   mae_base |   mae_norm |   mae_lgb |   rmse_lgb |
|---------:|----------:|-----------:|-----------:|----------:|-----------:|
| 2023.000 | 34005.000 |      5.150 |      5.139 |     4.474 |      5.958 |
| 2024.000 | 33736.000 |      5.224 |      5.211 |     4.440 |      5.952 |
| 2025.000 | 33451.000 |      5.327 |      5.309 |     4.530 |      6.045 |
| 2026.000 |  1186.000 |      6.653 |      6.587 |     5.157 |      6.805 |

## Bootstrap (remuestreo por partido): MAE(LightGBM + reparto) - MAE(base normalizada)

- Todos: -0.746 min, IC 95 % [-0.781, -0.712]
- Jugadores con prop: -0.736 min, IC 95 % [-0.798, -0.682]

## Distribución si juega: cobertura real de los cuantiles (nominal 10 / 50 / 90 %)

| segmento                    |     n |   MAE media si juega |   P(y <= q10) |   P(y <= q50) |   P(y <= q90) |   ancho medio q10-q90 |
|:----------------------------|------:|---------------------:|--------------:|--------------:|--------------:|----------------------:|
| jugaron                     | 85732 |                4.475 |         0.115 |         0.504 |         0.889 |                13.702 |
| jugaron, con prop de puntos | 21377 |                4.336 |         0.097 |         0.496 |         0.890 |                13.632 |

## Probabilidad de no jugar estando disponible (DNP técnico)

| modelo                    |   brier |   log loss |
|:--------------------------|--------:|-----------:|
| tasa reciente del jugador |   0.093 |      0.302 |
| LightGBM                  |   0.079 |      0.240 |

| tramo        |     n |   p_media |   frecuencia_real |
|:-------------|------:|----------:|------------------:|
| (0.0, 0.02]  | 55967 |     0.004 |             0.004 |
| (0.02, 0.05] |  6945 |     0.033 |             0.030 |
| (0.05, 0.1]  |  4792 |     0.072 |             0.071 |
| (0.1, 0.2]   |  5056 |     0.146 |             0.148 |
| (0.2, 0.4]   |  7974 |     0.302 |             0.307 |
| (0.4, 0.6]   | 10738 |     0.505 |             0.507 |
| (0.6, 1.0]   | 10906 |     0.697 |             0.666 |

## Importancia de las variables (ganancia, modelo final)

| feature      |   ganancia |
|:-------------|-----------:|
| min_norm     |      0.688 |
| rango_equipo |      0.160 |
| min_ult      |      0.045 |
| min_ewm3     |      0.034 |
| min_ewm10    |      0.012 |
| suma_base    |      0.012 |
| min_temp     |      0.007 |
| libres_pos   |      0.007 |
| libres       |      0.005 |
| dias_desde   |      0.004 |
| titular_ult  |      0.003 |
| partido_temp |      0.003 |
| min_temp_ant |      0.002 |
| min_std10    |      0.002 |
| titular_ewm  |      0.002 |