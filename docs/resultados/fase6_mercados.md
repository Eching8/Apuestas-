# Fase 6: todos los mercados de jugador

Una sola simulación por partido para todos los mercados (minutos -> tiros -> puntos, triples, tiros de campo y libres; rebotes ofensivos y defensivos, asistencias, robos, tapones y pérdidas con su propio LightGBM de tasa y su binomial negativa; reparto por periodos; primer anotador). Validación walk-forward mensual de la temporada 2025-26 con minutos proyectados fuera de muestra.

## 1. Calibración de cada distribución (PIT aleatorizado; ideal 0,10 en cada decil)

Incluye las props de 1.er cuarto y 1.ª mitad, que no tienen cuotas históricas: es su única validación hasta acumular capturas diarias.

| estadística   |     n |   decil 1 |   decil 5 |   decil 10 |   máx. desviación |
|:--------------|------:|----------:|----------:|-----------:|------------------:|
| pts           | 29480 |    0.1176 |    0.0970 |     0.1004 |            0.0176 |
| reb           | 29480 |    0.1042 |    0.0999 |     0.0962 |            0.0044 |
| ast           | 29480 |    0.1018 |    0.0986 |     0.0912 |            0.0088 |
| fg3m          | 29480 |    0.1052 |    0.0991 |     0.0973 |            0.0086 |
| stl           | 29480 |    0.1044 |    0.1002 |     0.1000 |            0.0044 |
| blk           | 29480 |    0.1030 |    0.1047 |     0.0961 |            0.0047 |
| tov           | 29480 |    0.0954 |    0.1026 |     0.0984 |            0.0046 |
| pra           | 29480 |    0.1199 |    0.0956 |     0.1016 |            0.0199 |
| pts_1q        | 24802 |    0.1203 |    0.0850 |     0.0839 |            0.0236 |
| pts_1h        | 26555 |    0.1106 |    0.1008 |     0.0811 |            0.0189 |
| reb_1q        | 24802 |    0.0908 |    0.1048 |     0.0891 |            0.0109 |
| reb_1h        | 26555 |    0.0931 |    0.1044 |     0.0838 |            0.0162 |
| ast_1q        | 24802 |    0.0923 |    0.1033 |     0.0936 |            0.0077 |
| ast_1h        | 26555 |    0.0918 |    0.1059 |     0.0867 |            0.0133 |

## 2. Probabilidad frente a las líneas reales de cada mercado (log loss; menor es mejor)

| mercado      | líneas   |     n |   margen medio |   log loss mercado |   log loss LightGBM |   log loss baseline |
|:-------------|:---------|------:|---------------:|-------------------:|--------------------:|--------------------:|
| ast          | apertura |  7832 |         0.0554 |             0.6869 |              0.6842 |              0.6992 |
| ast          | cierre   |  7776 |         0.0688 |             0.6840 |              0.6936 |              0.7071 |
| blk          | apertura |  9365 |         0.0805 |             0.6061 |              0.6058 |              0.6082 |
| blk          | cierre   |  9891 |         0.0875 |             0.6015 |              0.6023 |              0.6044 |
| doble_doble  | apertura |  7032 |         0.0566 |             0.3230 |              0.3230 |              0.3270 |
| doble_doble  | cierre   |  7088 |         0.0598 |             0.3209 |              0.3256 |              0.3297 |
| fg3m         | apertura |  9338 |         0.0605 |             0.6754 |              0.6853 |              0.6839 |
| fg3m         | cierre   |  9497 |         0.0718 |             0.6711 |              0.6898 |              0.6884 |
| fgm          | apertura |  9606 |         0.0783 |             0.6868 |              0.6867 |              0.6991 |
| fgm          | cierre   |  9516 |         0.0715 |             0.6888 |              0.6941 |              0.7062 |
| ftm          | apertura |  3389 |         0.0350 |             0.6929 |              0.7094 |              0.7206 |
| ftm          | cierre   |  3335 |         0.0215 |             0.6926 |              0.7101 |              0.7208 |
| pa           | apertura | 10278 |         0.0508 |             0.6923 |              0.6981 |              0.7165 |
| pa           | cierre   |  9487 |         0.0666 |             0.6919 |              0.7047 |              0.7234 |
| pr           | apertura | 10197 |         0.0596 |             0.6926 |              0.6990 |              0.7124 |
| pr           | cierre   |  9468 |         0.0691 |             0.6926 |              0.7092 |              0.7232 |
| pra          | apertura | 10459 |         0.0437 |             0.6929 |              0.7003 |              0.7192 |
| pra          | cierre   |  9785 |         0.0623 |             0.6924 |              0.7110 |              0.7297 |
| pts          | apertura |  9698 |         0.0519 |             0.6921 |              0.6964 |              0.7106 |
| pts          | cierre   |  8933 |         0.0654 |             0.6920 |              0.7059 |              0.7198 |
| ra           | apertura | 10282 |         0.0512 |             0.6919 |              0.6951 |              0.7107 |
| ra           | cierre   |  9946 |         0.0671 |             0.6892 |              0.7021 |              0.7161 |
| reb          | apertura |  9871 |         0.0583 |             0.6893 |              0.6907 |              0.7002 |
| reb          | cierre   |  9801 |         0.0690 |             0.6878 |              0.6970 |              0.7058 |
| stl          | apertura |  9233 |         0.0666 |             0.6786 |              0.6731 |              0.6738 |
| stl          | cierre   |  9706 |         0.0757 |             0.6743 |              0.6724 |              0.6738 |
| stocks       | apertura |  9330 |         0.0661 |             0.6790 |              0.6773 |              0.6823 |
| stocks       | cierre   |  9451 |         0.0718 |             0.6768 |              0.6761 |              0.6810 |
| tov          | apertura |  4690 |         0.0019 |             0.6932 |              0.6840 |              0.6964 |
| tov          | cierre   |  4529 |         0.0281 |             0.6924 |              0.6843 |              0.6967 |
| triple_doble | apertura |  1106 |         0.0355 |             0.1691 |              0.1669 |              0.1898 |
| triple_doble | cierre   |  1112 |         0.0351 |             0.1686 |              0.1679 |              0.1907 |

## 3. Backtest de apuestas por mercado

Mismas reglas que la fase 4: mezcla modelo + mercado ajustada walk-forward, edge >= 4 %, máximo 1 por jugador y 3 por partido. 'ROI al cierre' es la prueba realista (apostar cuando se conoce lo que usa el modelo). Validado = >= 300 apuestas, CLV ajustado > 0, bate el cierre > 50 % y ROI al cierre con IC 95 % > 0.

| mercado      |   líneas apertura |   apuestas |   ROI apertura |   IC inf |   IC sup |   CLV ajustado |   bate cierre |   apuestas al cierre |   ROI al cierre |   IC inf cierre |   IC sup cierre | estado      |
|:-------------|------------------:|-----------:|---------------:|---------:|---------:|---------------:|--------------:|---------------------:|----------------:|----------------:|----------------:|:------------|
| ast          |              4787 |  1396.0000 |         0.0985 |   0.0501 |   0.1478 |         0.0093 |        0.7522 |             539.0000 |         -0.0229 |         -0.0925 |          0.0506 | desactivado |
| blk          |              7333 |  1162.0000 |        -0.0528 |  -0.1254 |   0.0204 |        -0.0273 |        0.6488 |             909.0000 |         -0.0453 |         -0.1176 |          0.0293 | desactivado |
| doble_doble  |              5699 |   566.0000 |         0.0362 |  -0.0145 |   0.0889 |        -0.0369 |        0.6496 |             254.0000 |         -0.0165 |         -0.0844 |          0.0429 | desactivado |
| fg3m         |              6318 |   965.0000 |         0.0200 |  -0.0429 |   0.0800 |        -0.0136 |        0.6783 |              64.0000 |         -0.1067 |         -0.2731 |          0.0589 | desactivado |
| fgm          |              7421 |  1593.0000 |         0.0353 |  -0.0103 |   0.0814 |        -0.0365 |        0.5669 |            1028.0000 |         -0.0446 |         -0.0999 |          0.0112 | desactivado |
| ftm          |               492 |   262.0000 |         0.0573 |  -0.0610 |   0.1744 |        -0.0479 |        0.6495 |             256.0000 |          0.0417 |         -0.0811 |          0.1551 | sin validar |
| pa           |              6122 |  1488.0000 |         0.0438 |  -0.0011 |   0.0853 |        -0.0089 |        0.6438 |             708.0000 |         -0.0425 |         -0.1093 |          0.0258 | desactivado |
| pr           |              6836 |  1595.0000 |         0.0775 |   0.0313 |   0.1229 |        -0.0087 |        0.6991 |             480.0000 |         -0.0551 |         -0.1395 |          0.0235 | desactivado |
| pra          |              5967 |  1390.0000 |         0.0517 |   0.0058 |   0.1000 |         0.0004 |        0.6705 |             714.0000 |         -0.0542 |         -0.1171 |          0.0119 | desactivado |
| pts          |              6429 |  1546.0000 |         0.0901 |   0.0432 |   0.1352 |        -0.0054 |        0.7071 |             594.0000 |         -0.0254 |         -0.1018 |          0.0506 | desactivado |
| ra           |              6514 |  1571.0000 |         0.0575 |   0.0096 |   0.1033 |        -0.0033 |        0.6442 |             735.0000 |          0.0198 |         -0.0455 |          0.0855 | desactivado |
| reb          |              6639 |  1507.0000 |         0.0698 |   0.0183 |   0.1195 |         0.0126 |        0.7372 |             877.0000 |          0.0351 |         -0.0310 |          0.0952 | desactivado |
| stl          |              6672 |  1489.0000 |         0.1151 |   0.0594 |   0.1705 |        -0.0326 |        0.6389 |            1555.0000 |          0.0761 |          0.0221 |          0.1307 | desactivado |
| stocks       |              6957 |  1458.0000 |         0.0974 |   0.0429 |   0.1455 |        -0.0386 |        0.6226 |            1431.0000 |          0.0575 |          0.0043 |          0.1103 | desactivado |
| triple_doble |                96 |     3.0000 |         0.0190 |   0.0190 |   0.0190 |        -0.0384 |        1.0000 |               0.0000 |        nan      |        nan      |        nan      | sin validar |

## 4. Máximo anotador del partido (comparativo, sin cuotas históricas)

|   partidos |   log loss modelo |   log loss uniforme |
|-----------:|------------------:|--------------------:|
|  1361.0000 |            0.1209 |              0.1867 |

| tramo       |     n |   p_media |   frecuencia_real |
|:------------|------:|----------:|------------------:|
| (0.0, 0.05] | 16920 |    0.0104 |            0.0110 |
| (0.05, 0.1] |  2187 |    0.0721 |            0.0703 |
| (0.1, 0.2]  |  1946 |    0.1427 |            0.1298 |
| (0.2, 0.3]  |   899 |    0.2459 |            0.2490 |
| (0.3, 0.45] |   813 |    0.3650 |            0.3848 |
| (0.45, 1.0] |   434 |    0.5351 |            0.5353 |

## 5. Primera canasta (submodelo propio, sin cuotas históricas)

Log loss multiclase de quién anota la primera canasta de campo (titulares + 'un suplente'), partidos desde octubre de 2024, con información anterior a cada partido y los titulares confirmados.

|   partidos |   log loss modelo |   log loss volumen de tiro |   log loss uniforme (1/11) |
|-----------:|------------------:|---------------------------:|---------------------------:|
|  2680.0000 |            2.2908 |                     2.3810 |                     2.3979 |

| tramo        |    n |   p_media |   frecuencia_real |
|:-------------|-----:|----------:|------------------:|
| (0.0, 0.05]  | 6767 |    0.0087 |            0.0151 |
| (0.05, 0.08] | 5944 |    0.0678 |            0.0754 |
| (0.08, 0.11] | 9983 |    0.0946 |            0.0922 |
| (0.11, 0.14] | 6366 |    0.1231 |            0.1219 |
| (0.14, 0.18] | 2808 |    0.1546 |            0.1364 |
| (0.18, 1.0]  |  291 |    0.1915 |            0.1753 |