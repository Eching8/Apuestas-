# Fase 4: backtest del mercado de puntos con cuotas reales

Líneas de apertura evaluadas: 6,429 (2026-01-31 00:00:00 a 2026-06-13 00:00:00). Cuotas de consenso de SportsGameOdds (casas de EE. UU.; bet365 no está en la fuente). Se apuesta a la cuota de apertura con la probabilidad mezcla modelo + mercado ajustada walk-forward. ROI con apuesta fija de 1 unidad; IC 95 % y p-valor por bootstrap remuestreando partidos; p-valor de Holm por haber probado varias estrategias.

## Estrategias

| estrategia                               |   apuestas |   acierto |   cuota_media |   edge_medio |     roi |   roi_ic_inf |   roi_ic_sup |   p_valor |   p_valor_holm |   max_drawdown_u |   clv_ajustado |   bate_cierre |
|:-----------------------------------------|-----------:|----------:|--------------:|-------------:|--------:|-------------:|-------------:|----------:|---------------:|-----------------:|---------------:|--------------:|
| Mezcla LightGBM, edge >= 4 % (principal) |       1529 |    0.5631 |        1.8898 |       0.0866 |  0.0620 |       0.0160 |       0.1080 |    0.0040 |         0.0320 |          20.5775 |         0.0175 |        0.7486 |
| Mezcla LightGBM, edge >= 2 %             |       1623 |    0.5582 |        1.8922 |       0.0835 |  0.0540 |       0.0103 |       0.0999 |    0.0045 |         0.0320 |          17.3906 |         0.0161 |        0.7399 |
| Mezcla LightGBM, edge >= 6 %             |       1140 |    0.5623 |        1.8882 |       0.0990 |  0.0598 |       0.0069 |       0.1099 |    0.0170 |         0.1020 |          13.1407 |         0.0249 |        0.7532 |
| Mezcla cuantílico, edge >= 4 %           |       1537 |    0.5719 |        1.8893 |       0.0905 |  0.0790 |       0.0337 |       0.1275 |    0.0000 |         0.0000 |          16.9066 |         0.0202 |        0.7481 |
| Mezcla baseline, edge >= 4 %             |       1270 |    0.5409 |        1.8839 |       0.0629 |  0.0170 |      -0.0327 |       0.0699 |    0.2615 |         1.0000 |          27.4872 |        -0.0101 |        0.6475 |
| LightGBM puro (sin mercado), edge >= 4 % |       1702 |    0.5511 |        1.8979 |       0.1561 |  0.0435 |       0.0009 |       0.0869 |    0.0235 |         0.1175 |          20.0505 |         0.0132 |        0.7340 |
| Baseline puro, edge >= 4 %               |       1705 |    0.5302 |        1.8994 |       0.1826 |  0.0048 |      -0.0379 |       0.0491 |    0.4250 |         1.0000 |          37.3883 |        -0.0140 |        0.6374 |
| Control: todos los over a la apertura    |       1732 |    0.5127 |        1.9075 |       0.0000 | -0.0236 |      -0.0671 |       0.0189 |    0.8500 |         1.0000 |          58.9504 |        -0.0431 |        0.4929 |
| Control: todos los under a la apertura   |       1732 |    0.4856 |        1.8912 |       0.0000 | -0.0831 |      -0.1275 |      -0.0386 |    1.0000 |         1.0000 |         148.2404 |        -0.0602 |        0.4559 |

## ¿De dónde sale el ROI a la apertura?

Por movimiento de la línea entre apertura y cierre (a favor = el mercado se movió hacia la apuesta):

| movimiento   |   apuestas |   acierto |     roi |
|:-------------|-----------:|----------:|--------:|
| a favor      |        728 |    0.6154 |  0.1515 |
| en contra    |        130 |    0.4923 | -0.0491 |
| sin cambio   |        606 |    0.5050 | -0.0413 |
| sin cierre   |         65 |    0.6615 |  0.2456 |

Por minutos habituales liberados en el equipo (bajas de compañeros conocidas solo poco antes del partido):

| minutos_liberados_equipo   |   apuestas |     roi |
|:---------------------------|-----------:|--------:|
| <= 5                       |        204 | -0.0544 |
| 5-15                       |        342 |  0.0372 |
| > 15                       |        983 |  0.0949 |

## Prueba realista: apostar a la cuota de cierre

El modelo usa información que solo se conoce cerca del salto (quién se viste, spread y total de cierre). Esa información no existía cuando se publicó la apertura, así que el ROI a la apertura no es alcanzable: quien la tiene ya ve cuotas parecidas al cierre. Esta es la medida honesta de la ventaja del modelo:

| estrategia                                        |   apuestas |   acierto |   cuota_media |   edge_medio |     roi |   roi_ic_inf |   roi_ic_sup |   p_valor |   p_valor_holm |   max_drawdown_u |   clv_ajustado |   bate_cierre |
|:--------------------------------------------------|-----------:|----------:|--------------:|-------------:|--------:|-------------:|-------------:|----------:|---------------:|-----------------:|---------------:|--------------:|
| Mezcla LightGBM a la cuota de cierre, edge >= 4 % |        407 |    0.4939 |        1.8862 |       0.0595 | -0.0719 |      -0.1595 |       0.0155 |    0.9425 |         1.0000 |          32.8211 |        -0.0615 |        0.0000 |
| Mezcla LightGBM a la cuota de cierre, edge >= 2 % |        620 |    0.5274 |        1.8843 |       0.0508 | -0.0086 |      -0.0835 |       0.0634 |    0.5935 |         1.0000 |          23.1263 |        -0.0596 |        0.0000 |
| LightGBM puro a la cuota de cierre, edge >= 4 %   |       1775 |    0.5110 |        1.8844 |       0.1472 | -0.0391 |      -0.0823 |       0.0062 |    0.9510 |         1.0000 |          72.1338 |        -0.0611 |        0.0000 |

## Mercado de puntos: **DESACTIVADO**

- A la apertura: 1529 apuestas, ROI +6.20% (IC 95 % [+1.60%, +10.80%]), CLV ajustado por línea +1.75%, bate el cierre en el 74.9%.
- A la cuota de cierre (realista): 407 apuestas, ROI -7.19% (IC 95 % [-15.95%, +1.55%]).
- Máximo drawdown con apuesta fija (apertura): 20.6 unidades.
- Banca con 1/4 Kelly (tope 2 % por apuesta, 10 % por día), empezando en 100: termina en 135.1, máximo drawdown 24.0% (no alcanzable por lo explicado arriba).
- Regla de validación: al menos 300 apuestas, CLV ajustado positivo, batir el cierre más de la mitad de las veces y ROI con IC 95 % por encima de 0 al apostar en el momento en que se conoce la información que usa el modelo.

## Por mes (estrategia principal)

| mes     |   apuestas |     roi |   clv_ajustado |   bate_cierre |
|:--------|-----------:|--------:|---------------:|--------------:|
| 2026-01 |         15 |  0.1303 |         0.0277 |        0.7143 |
| 2026-02 |        435 |  0.0639 |         0.0201 |        0.7537 |
| 2026-03 |        597 |  0.0674 |         0.0251 |        0.7808 |
| 2026-04 |        366 |  0.1024 |         0.0076 |        0.6988 |
| 2026-05 |        101 | -0.0882 |        -0.0030 |        0.7172 |
| 2026-06 |         15 | -0.2477 |        -0.0003 |        0.7333 |

## Por lado

| lado   |   apuestas |   acierto |    roi |   clv_ajustado |
|:-------|-----------:|----------:|-------:|---------------:|
| over   |        665 |    0.5955 | 0.1276 |         0.0371 |
| under  |        864 |    0.5382 | 0.0116 |         0.0031 |

## Calibración de las apuestas (probabilidad usada frente a acierto real)

| tramo       |   apuestas |   p_media |   acierto_real |     roi |
|:------------|-----------:|----------:|---------------:|--------:|
| (0.0, 0.45] |          1 |    0.3952 |         0.0000 | -1.0000 |
| (0.45, 0.5] |          5 |    0.4867 |         0.4000 | -0.1620 |
| (0.5, 0.55] |        312 |    0.5343 |         0.5513 |  0.0839 |
| (0.55, 0.6] |        751 |    0.5752 |         0.5526 |  0.0386 |
| (0.6, 0.65] |        347 |    0.6203 |         0.5677 |  0.0448 |
| (0.65, 0.7] |         77 |    0.6679 |         0.6494 |  0.2029 |
| (0.7, 1.0]  |         36 |    0.7626 |         0.6944 |  0.2852 |