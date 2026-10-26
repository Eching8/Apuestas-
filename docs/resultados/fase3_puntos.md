# Fase 3: modelo de puntos (validación walk-forward mensual)

85,732 actuaciones fuera de muestra (2023-10 a 2026-10) con minutos proyectados también fuera de muestra (fase 2). Distribución por simulación Monte Carlo (2.000 por jugador en validación; 10.000 en producción).

## Media de puntos (error absoluto medio)

| segmento                                              |     n |   MAE baseline |   MAE LightGBM |   sesgo LightGBM |   MAE línea casa |
|:------------------------------------------------------|------:|---------------:|---------------:|-----------------:|-----------------:|
| todos los que jugaron                                 | 85732 |         4.5721 |         4.4009 |           0.0500 |         nan      |
| con prop de puntos                                    |  9708 |         5.0211 |         4.9041 |          -0.0286 |         nan      |
| con línea de cierre: línea de la casa como estimación |  9570 |       nan      |         4.8895 |         nan      |           4.7831 |

## Calibración de la distribución simulada: PIT aleatorizado por deciles (ideal 0,10 en cada uno)

| modelo   |     d1 |     d2 |     d3 |     d4 |     d5 |     d6 |     d7 |     d8 |     d9 |    d10 |
|:---------|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|
| base     | 0.1340 | 0.1063 | 0.0986 | 0.0954 | 0.0955 | 0.0941 | 0.0936 | 0.0941 | 0.0955 | 0.0927 |
| lgb      | 0.1195 | 0.0998 | 0.0948 | 0.0950 | 0.0961 | 0.0959 | 0.0980 | 0.0983 | 0.0993 | 0.1032 |

## Probabilidad de superar la línea real de la casa (sin empates)

| líneas   | modelo               |    n |   log loss |   brier |
|:---------|:---------------------|-----:|-----------:|--------:|
| apertura | mercado (sin margen) | 9698 |     0.6921 |  0.2495 |
| apertura | baseline simulado    | 9698 |     0.7112 |  0.2579 |
| apertura | LightGBM simulado    | 9698 |     0.6964 |  0.2510 |
| apertura | LightGBM cuantílico  | 9698 |     0.6941 |  0.2498 |
| cierre   | mercado (sin margen) | 9570 |     0.6921 |  0.2495 |
| cierre   | baseline simulado    | 9570 |     0.7221 |  0.2630 |
| cierre   | LightGBM simulado    | 9570 |     0.7067 |  0.2560 |
| cierre   | LightGBM cuantílico  | 9570 |     0.7044 |  0.2547 |

## Calibración de P(over) del LightGBM simulado (líneas de cierre)

| tramo       |    n |   p_media |   frecuencia_real |
|:------------|-----:|----------:|------------------:|
| (0.0, 0.2]  |   46 |    0.1480 |            0.4783 |
| (0.2, 0.3]  |  237 |    0.2617 |            0.4641 |
| (0.3, 0.4]  | 1431 |    0.3626 |            0.4941 |
| (0.4, 0.45] | 1723 |    0.4275 |            0.4759 |
| (0.45, 0.5] | 2153 |    0.4762 |            0.4645 |
| (0.5, 0.55] | 2035 |    0.5239 |            0.5007 |
| (0.55, 0.6] | 1170 |    0.5727 |            0.5068 |
| (0.6, 0.7]  |  716 |    0.6333 |            0.5433 |
| (0.7, 0.8]  |   55 |    0.7334 |            0.5818 |
| (0.8, 1.0]  |    4 |    0.8722 |            0.7500 |

- Log loss LightGBM simulado - baseline simulado (cierre): -0.0154, IC 95 % [-0.0190, -0.0116]

- Log loss LightGBM simulado - mercado (cierre): +0.0146, IC 95 % [+0.0102, +0.0186]

- Log loss LightGBM cuantílico - LightGBM simulado (cierre): -0.0023, IC 95 % [-0.0042, -0.0002]

## ¿Aporta el modelo algo que la línea no tenga? Mezcla modelo + mercado (walk-forward)

Regresión logística sobre logit(mercado) y logit(modelo), reentrenada cada mes con los meses anteriores. Diferencia negativa = la mezcla predice mejor que el mercado solo.

| líneas   |    n |   meses |   log loss mercado |   log loss mezcla |   diferencia |   IC 95 % inf |   IC 95 % sup |   peso mercado |   peso modelo |
|:---------|-----:|--------:|-------------------:|------------------:|-------------:|--------------:|--------------:|---------------:|--------------:|
| apertura | 8040 |       5 |             0.6920 |            0.6891 |      -0.0030 |       -0.0053 |       -0.0008 |         0.7191 |        0.4534 |
| cierre   | 7931 |       5 |             0.6920 |            0.6924 |       0.0005 |       -0.0004 |        0.0013 |         1.0461 |        0.1233 |

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