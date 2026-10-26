# Fase 3: modelo de puntos (validación walk-forward mensual)

85,732 actuaciones fuera de muestra (2023-10 a 2026-10) con minutos proyectados también fuera de muestra (fase 2). Distribución por simulación Monte Carlo (2.000 por jugador en validación; 10.000 en producción).

## Media de puntos (error absoluto medio)

| segmento                                              |     n |   MAE baseline |   MAE LightGBM |   sesgo LightGBM |   MAE línea casa |
|:------------------------------------------------------|------:|---------------:|---------------:|-----------------:|-----------------:|
| todos los que jugaron                                 | 85732 |         4.5721 |         4.4009 |           0.0500 |         nan      |
| con prop de puntos                                    |  9571 |         5.0260 |         4.9077 |          -0.0167 |         nan      |
| con línea de cierre: línea de la casa como estimación |  9428 |       nan      |         4.8905 |         nan      |           4.7863 |

## Calibración de la distribución simulada: PIT aleatorizado por deciles (ideal 0,10 en cada uno)

| modelo   |     d1 |     d2 |     d3 |     d4 |     d5 |     d6 |     d7 |     d8 |     d9 |    d10 |
|:---------|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|
| base     | 0.1340 | 0.1063 | 0.0986 | 0.0954 | 0.0955 | 0.0941 | 0.0936 | 0.0941 | 0.0955 | 0.0927 |
| lgb      | 0.1195 | 0.0998 | 0.0948 | 0.0950 | 0.0961 | 0.0959 | 0.0980 | 0.0983 | 0.0993 | 0.1032 |

## Probabilidad de superar la línea real de la casa (sin empates)

| líneas   | modelo               |    n |   log loss |   brier |
|:---------|:---------------------|-----:|-----------:|--------:|
| apertura | mercado (sin margen) | 7843 |     0.6918 |  0.2493 |
| apertura | baseline simulado    | 7843 |     0.7126 |  0.2585 |
| apertura | LightGBM simulado    | 7843 |     0.6966 |  0.2510 |
| apertura | LightGBM cuantílico  | 7843 |     0.6939 |  0.2495 |
| cierre   | mercado (sin margen) | 9428 |     0.6921 |  0.2495 |
| cierre   | baseline simulado    | 9428 |     0.7217 |  0.2629 |
| cierre   | LightGBM simulado    | 9428 |     0.7060 |  0.2557 |
| cierre   | LightGBM cuantílico  | 9428 |     0.7038 |  0.2545 |

## Calibración de P(over) del LightGBM simulado (líneas de cierre)

| tramo       |    n |   p_media |   frecuencia_real |
|:------------|-----:|----------:|------------------:|
| (0.0, 0.2]  |   43 |    0.1465 |            0.5116 |
| (0.2, 0.3]  |  222 |    0.2621 |            0.4550 |
| (0.3, 0.4]  | 1402 |    0.3628 |            0.4900 |
| (0.4, 0.45] | 1708 |    0.4274 |            0.4748 |
| (0.45, 0.5] | 2127 |    0.4762 |            0.4626 |
| (0.5, 0.55] | 2008 |    0.5239 |            0.5020 |
| (0.55, 0.6] | 1158 |    0.5728 |            0.5060 |
| (0.6, 0.7]  |  702 |    0.6332 |            0.5427 |
| (0.7, 0.8]  |   54 |    0.7324 |            0.5926 |
| (0.8, 1.0]  |    4 |    0.8722 |            0.7500 |

- Log loss LightGBM simulado - baseline simulado (cierre): -0.0157, IC 95 % [-0.0194, -0.0118]

- Log loss LightGBM simulado - mercado (cierre): +0.0139, IC 95 % [+0.0095, +0.0180]

- Log loss LightGBM cuantílico - LightGBM simulado (cierre): -0.0022, IC 95 % [-0.0041, -0.0001]

## ¿Aporta el modelo algo que la línea no tenga? Mezcla modelo + mercado (walk-forward)

Regresión logística sobre logit(mercado) y logit(modelo), reentrenada cada mes con los meses anteriores. Diferencia negativa = la mezcla predice mejor que el mercado solo.

| líneas   |    n |   meses |   log loss mercado |   log loss mezcla |   diferencia |   IC 95 % inf |   IC 95 % sup |   peso mercado |   peso modelo |
|:---------|-----:|--------:|-------------------:|------------------:|-------------:|--------------:|--------------:|---------------:|--------------:|
| apertura | 4652 |       4 |             0.6915 |            0.6888 |      -0.0027 |       -0.0057 |        0.0001 |         0.8030 |        0.4268 |
| cierre   | 7823 |       5 |             0.6919 |            0.6924 |       0.0005 |       -0.0005 |        0.0014 |         1.0182 |        0.1421 |

## Importancia de las variables (tasa de puntos por minuto)

| feature       |   ganancia |
|:--------------|-----------:|
| r_pts_comp    |     0.5490 |
| r_pts         |     0.1712 |
| usg_ewm       |     0.0787 |
| r_pts_temp    |     0.0423 |
| fga_libres    |     0.0179 |
| def_drtg      |     0.0140 |
| def_pos       |     0.0117 |
| min_base      |     0.0102 |
| ritmo_esp     |     0.0087 |
| libres        |     0.0080 |
| n_hist        |     0.0073 |
| titular_ewm   |     0.0068 |
| spread_equipo |     0.0067 |
| r_fta         |     0.0067 |
| libres_pos    |     0.0064 |