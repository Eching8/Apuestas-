# Fase 4: backtest del mercado de puntos con cuotas reales

Líneas de apertura evaluadas: 8,040 (2026-01-31 00:00:00 a 2026-06-13 00:00:00). Cuotas de consenso de SportsGameOdds (casas de EE. UU.; bet365 no está en la fuente). Se apuesta a la cuota de apertura con la probabilidad mezcla modelo + mercado ajustada walk-forward. ROI con apuesta fija de 1 unidad; IC 95 % y p-valor por bootstrap remuestreando partidos; p-valor de Holm por haber probado varias estrategias.

## Estrategias

| estrategia                               |   apuestas |   acierto |   cuota_media |   edge_medio |     roi |   roi_ic_inf |   roi_ic_sup |   p_valor |   p_valor_holm |   max_drawdown_u |   clv_ajustado |   bate_cierre |
|:-----------------------------------------|-----------:|----------:|--------------:|-------------:|--------:|-------------:|-------------:|----------:|---------------:|-----------------:|---------------:|--------------:|
| Mezcla LightGBM, edge >= 4 % (principal) |       1694 |    0.5697 |        1.9162 |       0.0851 |  0.0892 |       0.0431 |       0.1345 |    0.0000 |         0.0000 |          18.5085 |         0.0346 |        0.7347 |
| Mezcla LightGBM, edge >= 2 %             |       1751 |    0.5608 |        1.9215 |       0.0825 |  0.0755 |       0.0312 |       0.1201 |    0.0010 |         0.0070 |          20.2701 |         0.0354 |        0.7294 |
| Mezcla LightGBM, edge >= 6 %             |       1286 |    0.5700 |        1.9128 |       0.0963 |  0.0886 |       0.0361 |       0.1402 |    0.0010 |         0.0070 |          16.3423 |         0.0419 |        0.7412 |
| Mezcla cuantílico, edge >= 4 %           |       1709 |    0.5705 |        1.9178 |       0.0896 |  0.0932 |       0.0492 |       0.1390 |    0.0000 |         0.0000 |          19.5173 |         0.0392 |        0.7448 |
| Mezcla baseline, edge >= 4 %             |       1508 |    0.5351 |        1.9099 |       0.0630 |  0.0215 |      -0.0260 |       0.0692 |    0.1810 |         0.5430 |          27.6285 |         0.0026 |        0.6377 |
| LightGBM puro (sin mercado), edge >= 4 % |       1778 |    0.5568 |        1.9218 |       0.1648 |  0.0678 |       0.0243 |       0.1124 |    0.0020 |         0.0100 |          17.6818 |         0.0324 |        0.7344 |
| Baseline puro, edge >= 4 %               |       1778 |    0.5354 |        1.9244 |       0.1939 |  0.0297 |      -0.0154 |       0.0753 |    0.0855 |         0.3420 |          25.4967 |         0.0017 |        0.6329 |
| Control: todos los over a la apertura    |       1778 |    0.5079 |        1.9487 |       0.0000 | -0.0110 |      -0.0609 |       0.0351 |    0.6935 |         1.0000 |          59.4511 |        -0.0166 |        0.5009 |
| Control: todos los under a la apertura   |       1778 |    0.4978 |        1.9366 |       0.0000 | -0.0359 |      -0.0799 |       0.0119 |    0.9320 |         1.0000 |          66.3238 |        -0.0424 |        0.4254 |

## ¿De dónde sale el ROI a la apertura?

Por movimiento de la línea entre apertura y cierre (a favor = el mercado se movió hacia la apuesta):

| movimiento   |   apuestas |   acierto |     roi |
|:-------------|-----------:|----------:|--------:|
| a favor      |        822 |    0.6350 |  0.2066 |
| en contra    |        148 |    0.4595 | -0.1001 |
| sin cambio   |        662 |    0.5000 | -0.0388 |
| sin cierre   |         62 |    0.7097 |  0.3513 |

Por minutos habituales liberados en el equipo (bajas de compañeros conocidas solo poco antes del partido):

| minutos_liberados_equipo   |   apuestas |    roi |
|:---------------------------|-----------:|-------:|
| <= 5                       |        229 | 0.0120 |
| 5-15                       |        402 | 0.0536 |
| > 15                       |       1063 | 0.1193 |

## Prueba realista: apostar a la cuota de cierre

El modelo usa información que solo se conoce cerca del salto (quién se viste, spread y total de cierre). Esa información no existía cuando se publicó la apertura, así que el ROI a la apertura no es alcanzable: quien la tiene ya ve cuotas parecidas al cierre. Esta es la medida honesta de la ventaja del modelo:

| estrategia                                        |   apuestas |   acierto |   cuota_media |   edge_medio |     roi |   roi_ic_inf |   roi_ic_sup |   p_valor |   p_valor_holm |   max_drawdown_u |   clv_ajustado |   bate_cierre |
|:--------------------------------------------------|-----------:|----------:|--------------:|-------------:|--------:|-------------:|-------------:|----------:|---------------:|-----------------:|---------------:|--------------:|
| Mezcla LightGBM a la cuota de cierre, edge >= 4 % |        327 |    0.4587 |        1.8966 |       0.0562 | -0.1338 |      -0.2291 |      -0.0372 |    0.9965 |         1.0000 |          43.9452 |        -0.0581 |        0.0000 |
| Mezcla LightGBM a la cuota de cierre, edge >= 2 % |        526 |    0.4962 |        1.9008 |       0.0476 | -0.0586 |      -0.1373 |       0.0198 |    0.9220 |         1.0000 |          33.4793 |        -0.0544 |        0.0000 |
| LightGBM puro a la cuota de cierre, edge >= 4 %   |       1776 |    0.5113 |        1.8885 |       0.1491 | -0.0367 |      -0.0806 |       0.0092 |    0.9450 |         1.0000 |          72.9689 |        -0.0591 |        0.0000 |

## Mercado de puntos: **DESACTIVADO**

- A la apertura: 1694 apuestas, ROI +8.92% (IC 95 % [+4.31%, +13.45%]), CLV ajustado por línea +3.46%, bate el cierre en el 73.5%.
- A la cuota de cierre (realista): 327 apuestas, ROI -13.38% (IC 95 % [-22.91%, -3.72%]).
- Máximo drawdown con apuesta fija (apertura): 18.5 unidades.
- Banca con 1/4 Kelly (tope 2 % por apuesta, 10 % por día), empezando en 100: termina en 161.7, máximo drawdown 19.5% (no alcanzable por lo explicado arriba).
- Regla de validación: al menos 300 apuestas, CLV ajustado positivo, batir el cierre más de la mitad de las veces y ROI con IC 95 % por encima de 0 al apostar en el momento en que se conoce la información que usa el modelo.

## Por mes (estrategia principal)

| mes     |   apuestas |     roi |   clv_ajustado |   bate_cierre |
|:--------|-----------:|--------:|---------------:|--------------:|
| 2026-01 |         15 |  0.1303 |         0.0277 |        0.7143 |
| 2026-02 |        488 |  0.0931 |         0.0408 |        0.7192 |
| 2026-03 |        674 |  0.1107 |         0.0431 |        0.7758 |
| 2026-04 |        399 |  0.0940 |         0.0256 |        0.7045 |
| 2026-05 |        103 | -0.0647 |        -0.0103 |        0.6634 |
| 2026-06 |         15 | -0.1144 |         0.0011 |        0.6667 |

## Por lado

| lado   |   apuestas |   acierto |    roi |   clv_ajustado |
|:-------|-----------:|----------:|-------:|---------------:|
| over   |        693 |    0.6118 | 0.1764 |         0.0613 |
| under  |       1001 |    0.5405 | 0.0288 |         0.0171 |

## Calibración de las apuestas (probabilidad usada frente a acierto real)

| tramo       |   apuestas |   p_media |   acierto_real |     roi |
|:------------|-----------:|----------:|---------------:|--------:|
| (0.0, 0.45] |          1 |    0.4015 |         0.0000 | -1.0000 |
| (0.45, 0.5] |          3 |    0.4869 |         0.0000 | -1.0000 |
| (0.5, 0.55] |        300 |    0.5365 |         0.5500 |  0.0856 |
| (0.55, 0.6] |        918 |    0.5743 |         0.5588 |  0.0702 |
| (0.6, 0.65] |        364 |    0.6193 |         0.6016 |  0.1275 |
| (0.65, 0.7] |         80 |    0.6683 |         0.6125 |  0.1381 |
| (0.7, 1.0]  |         28 |    0.7620 |         0.6786 |  0.2697 |