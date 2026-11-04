# Props NBA 2026-11-04

> **Aviso:** las apuestas implican riesgo de perder dinero. Estas probabilidades son estimaciones estadísticas, no garantías: ningún modelo acierta siempre y las combinadas multiplican el riesgo. Apuesta solo lo que puedas permitirte perder. Si el juego deja de ser un entretenimiento, busca ayuda.

**Modelo** = minutos, tasa por minuto, bajas, defensa rival por posición, zonas de tiro y tipo de defensa, mezclado con el acierto real del jugador sobre esa línea. **Casa** = probabilidad implícita en las cuotas sin el margen. **Prob. final** = mezcla de ambas. Si modelo y casa discrepan mucho, la casa suele saber algo (rol, rotación, una baja): revísalo antes de apostar.

Cada media se construye desde las estadísticas que la producen (tiros × acierto por zona, % de los rebotes disponibles que captura, % de las canastas de sus compañeros que asiste...) y se muestra con esas estadísticas en sus últimos 5 y 10 partidos, la temporada y contra este rival. Todo queda guardado en la tabla `nba_analisis` de la base.

## Estado de calibración

**En calibración: todos los picks son de prueba.**  6 de 8 criterios cumplidos:

- ⬜ Días con picks liquidados: 8 de 21
- ⬜ Props de línea principal: muestra: 88 de 150
- ✅ Props de línea principal: aciertan lo prometido: acierto 70.5% vs prometido 67.1%
- ✅ Picks seguros: muestra: 538 de 150
- ✅ Picks seguros: aciertan lo prometido: acierto 87.9% vs prometido 86.9%
- ✅ Props con cuota: beneficio positivo: +0.64 u en 88
- ✅ Combinadas: muestra: 73 de 30
- ✅ Combinadas: ganan lo prometido: ganadas 34.2% vs prometido 28.2%

### Acumulado de las combinadas de prueba

| Tipo | Jugadas | Ganadas | % ganadas | Prob. prometida | Beneficio (1 u, con cuota) |
|---|---|---|---|---|---|
| Combinada segura A (alternas) | 7 | 4 | 57% | 69% | - |
| Bet builder | 15 | 5 | 33% | 36% | - |
| Segura cuota 10+ | 2 | 0 | 0% | 10% | -2.00 u en 2 |
| Segura cuota 15+ | 2 | 0 | 0% | 7% | -2.00 u en 2 |
| Segura cuota 2+ | 6 | 5 | 83% | 45% | +4.49 u en 6 |
| Segura cuota 3+ | 5 | 5 | 100% | 30% | +10.85 u en 5 |
| Segura cuota 5+ | 3 | 1 | 33% | 19% | +2.03 u en 3 |
| Doble de bet builders | 4 | 0 | 0% | 14% | - |
| Combinada segura B (principales) | 6 | 4 | 67% | 27% | +8.56 u en 6 |
| Rachas de temporada (4 patas) | 5 | 0 | 0% | 16% | -5.00 u en 5 |
| Rachas de temporada (8 patas) | 3 | 0 | 0% | 3% | -3.00 u en 3 |
| Tus apuestas | 11 | 0 | 0% | 8% | -11.00 u en 11 |
| De valor cuota 10+ | 4 | 0 | 0% | 13% | -4.00 u en 4 |
| De valor cuota 15+ | 3 | 1 | 33% | 9% | +12.17 u en 3 |
| De valor cuota 30+ | 2 | 0 | 0% | 5% | -2.00 u en 2 |
| De valor cuota 5+ | 6 | 0 | 0% | 22% | -6.00 u en 6 |

## Bet builders del día

Por partido, 4 "más de" de titulares estables sin alertas, en líneas un poco por debajo de su nivel (cada pierna ~72 %+). La probabilidad de acertar todas tiene en cuenta que los jugadores de un mismo partido se mueven algo juntos. **Cuota justa** = 1 / probabilidad (solo para saber cuánto debería pagar; se elige por probabilidad). Backtest 2025-26: prometían ~32 % y acertaron 38-40 % (conservador).

### Doble: Indiana Pacers @ Memphis Grizzlies + Portland Trail Blazers @ Phoenix Suns

Probabilidad de acertar los dos bet builders: **15%** (1 de cada 7); cuota justa **6.76**.

**Indiana Pacers @ Memphis Grizzlies** — acertar las 4: **40%**, cuota justa 2.50

- Javon Small 7+ puntos (78%; esperado 10.4; últ. 10: 9/10)
- Aaron Nesmith 1+ triples (78%; esperado 1.6; últ. 10: 9/10)
- Jaylen Wells 1+ triples (80%; esperado 1.9; últ. 10: 7/10)
- Cedric Coward 1+ triples (81%; esperado 1.9; últ. 10: 10/10)

**Portland Trail Blazers @ Phoenix Suns** — acertar las 4: **37%**, cuota justa 2.70

- Jalen Green 2+ asistencias (79%; esperado 3.4; últ. 10: 8/10)
- Toumani Camara 2+ triples (72%; esperado 2.6; últ. 10: 8/10)
- Miles Bridges 1+ triples (80%; esperado 1.8; últ. 10: 8/10)
- Deni Avdija 1+ triples (80%; esperado 1.7; últ. 10: 9/10)

**Miami Heat @ LA Clippers** — acertar las 4: **35%**, cuota justa 2.89

- Davion Mitchell 11+ puntos (77%; esperado 14.6; últ. 10: 9/10)
- Andrew Wiggins 1+ triples (76%; esperado 1.6; últ. 10: 7/10)
- Klay Thompson 2+ triples (76%; esperado 3.1; últ. 10: 8/10)
- Derrick Jones Jr. 1+ triples (77%; esperado 1.7; últ. 10: 9/10)

**Dallas Mavericks @ San Antonio Spurs** — acertar las 4: **32%**, cuota justa 3.14

- Victor Wembanyama 2+ asistencias (76%; esperado 2.9; últ. 10: 9/10)
- Dylan Harper 1+ triples (73%; esperado 1.4; últ. 10: 8/10)
- Devin Vassell 1+ triples (74%; esperado 1.6; últ. 10: 8/10)
- Stephon Castle 1+ triples (76%; esperado 1.8; últ. 10: 8/10)

## Combinada segura del día

**Opción A, líneas alternativas (la más segura):** el pick seguro más probable de cada partido, de titulares estables. Búscalas en las líneas alternativas de tu casa ("15+", "20+"...): cada una vale la pena si paga al menos su cuota mínima.

| Partido | Selección | Prob. | Cuota mínima | Esperado | Últ. 10 |
|---|---|---|---|---|---|
| Portland Trail Blazers @ Phoenix Suns | **Devin Booker: más de 1.5 asistencias** | **92%** | 1.08 | 5.2 | 10/10 |
| Philadelphia 76ers @ Detroit Pistons | **Joel Embiid: más de 3.5 rebotes** | **91%** | 1.09 | 8.3 | 10/10 |
| Milwaukee Bucks @ Boston Celtics | **Jayson Tatum: más de 2.5 asistencias** | **91%** | 1.10 | 6.4 | 10/10 |
| Cleveland Cavaliers @ Oklahoma City Thunder | **Shai Gilgeous-Alexander: más de 1.5 asistencias** | **90%** | 1.11 | 4.9 | 10/10 |

| Selecciones | Probabilidad de acertar todas |
|---|---|
| 2 | **84%** |
| 3 | **77%** |
| 4 | **70%** |

**Opción B, líneas principales con cuota real:**

Se elige por **probabilidad**, no por valor: la más probable de cada partido entre jugadores constantes (titulares con minutos estables, sin cambio de rol, traspaso ni lesión, que la habrían pasado en 7+ de sus últimos 10 y en el 60 %+ de esta temporada) y con cuota real de la casa. Si tu casa no ofrece esa línea, usa la siguiente de la lista "Las más seguras con cuota".

| Partido | Selección | Prob. | Cuota | Últ. 10 | Temporada |
|---|---|---|---|---|---|
| Milwaukee Bucks @ Boston Celtics | **Jaime Jaquez Jr.: más de 0.5 triples**<br>el rival concede +12% de triples por minuto a aleros/ala-pívots (defensa débil); ajuste aplicado +5%; en su zona principal (triple) el rival concede 36% (liga 35%) | **69%** | 1.45 | 9/10 | 6/7 |
| Philadelphia 76ers @ Detroit Pistons | **Cade Cunningham: menos de 8.5 asistencias**<br>el rival concede +0% de asistencias por minuto a bases/escoltas (defensa media); ajuste aplicado +0% | **63%** | 1.71 | 10/10 | 7/7 |
| Charlotte Hornets @ Brooklyn Nets | **Moussa Diabate: más de 1.5 asistencias**<br>el rival concede +5% de asistencias por minuto a aleros/ala-pívots (defensa débil); ajuste aplicado +5% | **63%** | 1.54 | 7/10 | 6/8 |
| Utah Jazz @ New Orleans Pelicans | **Keyonte George: menos de 6.5 asistencias**<br>el rival concede +6% de asistencias por minuto a bases/escoltas (defensa débil); ajuste aplicado +6% | **62%** | 1.64 | 8/10 | 5/7 |

| Selecciones | Probabilidad de acertar todas | Cuota |
|---|---|---|
| 2 | **43%** | 2.48 |
| 3 | **27%** | 3.82 |
| 4 | **17%** | 6.26 |

### Las más seguras con cuota

| Partido | Prop | Prob. final | Modelo | Casa | Esperado | Últ. 10 | Temporada | vs este rival | Cuota (implícita) |
|---|---|---|---|---|---|---|---|---|---|
| Milwaukee Bucks @ Boston Celtics | **Jaime Jaquez Jr.: más de 0.5 triples** | **69%** | 74% | 65% | 1.4 ± 1.2 | 9/10 | 6/7 | 2, 1, 1 | 1.45 (69%) |
| Philadelphia 76ers @ Detroit Pistons | **Cade Cunningham: menos de 8.5 asistencias** | **63%** | 74% | 55% | 6.8 ± 2.8 | 10/10 | 7/7 | 8, 13, 11 | 1.71 (58%) |
| Charlotte Hornets @ Brooklyn Nets | **Moussa Diabate: más de 1.5 asistencias** | **63%** | 65% | 61% | 2.3 ± 1.6 | 7/10 | 6/8 | 3, 1, 1, 0 | 1.54 (65%) |
| Utah Jazz @ New Orleans Pelicans | **Keyonte George: menos de 6.5 asistencias** | **62%** | 69% | 57% | 5.3 ± 2.9 | 8/10 | 5/7 | 10, 4 | 1.64 (61%) |

## Combinadas con cuota objetivo

La combinación de jugadores constantes (mismos filtros que la opción B, partidos distintos) con más probabilidad de acertar todas cuya cuota llega al objetivo. Se registran como picks de prueba y se liquidan solas: `nba rendimiento` dice cuándo el sistema está listo para dinero real. Una cuota alta nunca es segura: cuota 15 justa acierta 1 de cada 15. Lo que la data puede hacer es acercarse o superar esa probabilidad. Se eligen solo por probabilidad de acertar (nunca por valor): como mucho 5 patas, sin "menos" de anotación dudosos.

**Segura, cuota 2+ (2 patas):** cuota 2.48, probabilidad de acertar todas **43%** (1 de cada 2)

- Jaime Jaquez Jr.: más de 0.5 triples (69%, cuota 1.45) — Milwaukee Bucks @ Boston Celtics — 5 factores a favor, 1 en contra
  - el rival concede +12% de triples por minuto a aleros/ala-pívots (defensa débil); ajuste aplicado +5%; en su zona principal (triple) el rival concede 36% (liga 35%)
- Cade Cunningham: menos de 8.5 asistencias (63%, cuota 1.71) — Philadelphia 76ers @ Detroit Pistons — 4 factores a favor, 1 en contra
  - el rival concede +0% de asistencias por minuto a bases/escoltas (defensa media); ajuste aplicado +0%

**Segura, cuota 3+ (3 patas):** cuota 3.82, probabilidad de acertar todas **27%** (1 de cada 4)

- Jaime Jaquez Jr.: más de 0.5 triples (69%, cuota 1.45) — Milwaukee Bucks @ Boston Celtics — 5 factores a favor, 1 en contra
  - el rival concede +12% de triples por minuto a aleros/ala-pívots (defensa débil); ajuste aplicado +5%; en su zona principal (triple) el rival concede 36% (liga 35%)
- Cade Cunningham: menos de 8.5 asistencias (63%, cuota 1.71) — Philadelphia 76ers @ Detroit Pistons — 4 factores a favor, 1 en contra
  - el rival concede +0% de asistencias por minuto a bases/escoltas (defensa media); ajuste aplicado +0%
- Moussa Diabate: más de 1.5 asistencias (63%, cuota 1.54) — Charlotte Hornets @ Brooklyn Nets — 4 factores a favor, 2 en contra
  - el rival concede +5% de asistencias por minuto a aleros/ala-pívots (defensa débil); ajuste aplicado +5%

**Segura, cuota 5+ (4 patas):** cuota 6.26, probabilidad de acertar todas **17%** (1 de cada 6)

- Jaime Jaquez Jr.: más de 0.5 triples (69%, cuota 1.45) — Milwaukee Bucks @ Boston Celtics — 5 factores a favor, 1 en contra
  - el rival concede +12% de triples por minuto a aleros/ala-pívots (defensa débil); ajuste aplicado +5%; en su zona principal (triple) el rival concede 36% (liga 35%)
- Cade Cunningham: menos de 8.5 asistencias (63%, cuota 1.71) — Philadelphia 76ers @ Detroit Pistons — 4 factores a favor, 1 en contra
  - el rival concede +0% de asistencias por minuto a bases/escoltas (defensa media); ajuste aplicado +0%
- Moussa Diabate: más de 1.5 asistencias (63%, cuota 1.54) — Charlotte Hornets @ Brooklyn Nets — 4 factores a favor, 2 en contra
  - el rival concede +5% de asistencias por minuto a aleros/ala-pívots (defensa débil); ajuste aplicado +5%
- Keyonte George: menos de 6.5 asistencias (62%, cuota 1.64) — Utah Jazz @ New Orleans Pelicans — 3 factores a favor, 2 en contra
  - el rival concede +6% de asistencias por minuto a bases/escoltas (defensa débil); ajuste aplicado +6%

## Picks seguros de titulares estables

Líneas bajas (alternativas) de titulares con 30+ minutos: mejor un "15+ puntos" casi seguro de una estrella que la línea normal de un suplente. En el backtest, elegidas al 85 % acertaron el 89-96 %. **Cuota mínima** = la que hace falta para que valga la pena (1 / probabilidad); búscala en las líneas alternativas de tu casa.

| Partido | Jugador | Pick seguro | Prob. | Cuota mínima | Esperado | Últ. 10 |
|---|---|---|---|---|---|---|
| Portland Trail Blazers @ Phoenix Suns | Devin Booker | **más de 1.5 asistencias** | **92%** | 1.08 | 5.2 | 10/10 |
| Philadelphia 76ers @ Detroit Pistons | Joel Embiid | **más de 3.5 rebotes** | **91%** | 1.09 | 8.3 | 10/10 |
| Portland Trail Blazers @ Phoenix Suns | Deni Avdija | **más de 1.5 asistencias** | **91%** | 1.09 | 5.2 | 10/10 |
| Milwaukee Bucks @ Boston Celtics | Jayson Tatum | **más de 2.5 asistencias** | **91%** | 1.10 | 6.4 | 10/10 |
| Cleveland Cavaliers @ Oklahoma City Thunder | Shai Gilgeous-Alexander | **más de 1.5 asistencias** | **90%** | 1.11 | 4.9 | 10/10 |
| Indiana Pacers @ Memphis Grizzlies | Pascal Siakam | **más de 2.5 rebotes** | **90%** | 1.11 | 6.7 | 10/10 |
| Los Angeles Lakers @ Sacramento Kings | Austin Reaves | **más de 1.5 asistencias** | **90%** | 1.11 | 5.3 | 9/10 |
| Philadelphia 76ers @ Detroit Pistons | Tyrese Maxey | **más de 1.5 asistencias** | **90%** | 1.11 | 4.6 | 10/10 |
| Utah Jazz @ New Orleans Pelicans | Dejounte Murray | **más de 2.5 asistencias** | **90%** | 1.11 | 6.4 | 10/10 |
| Los Angeles Lakers @ Sacramento Kings | Domantas Sabonis | **más de 6.5 rebotes** | **90%** | 1.11 | 12.0 | 10/10 |
| Chicago Bulls @ New York Knicks | Karl-Anthony Towns | **más de 7.5 rebotes** | **90%** | 1.12 | 12.8 | 10/10 |
| Miami Heat @ LA Clippers | Davion Mitchell | **más de 2.5 asistencias** | **89%** | 1.12 | 7.0 | 8/10 |
| Utah Jazz @ New Orleans Pelicans | Zion Williamson | **más de 14.5 puntos** | **89%** | 1.12 | 22.1 | 9/10 |
| Philadelphia 76ers @ Detroit Pistons | Tyrese Maxey | **más de 16.5 puntos** | **89%** | 1.12 | 24.6 | 10/10 |
| Philadelphia 76ers @ Detroit Pistons | LeBron James | **más de 2.5 asistencias** | **89%** | 1.12 | 5.7 | 10/10 |

## Las más probables del día

| Partido | Prop | Prob. final | Modelo | Casa | Esperado | Últ. 10 | Temporada | vs este rival | Cuota (implícita) |
|---|---|---|---|---|---|---|---|---|---|
| Portland Trail Blazers @ Phoenix Suns | **Khaman Maluach: menos de 0.5 triples** | **71%** | 75% | 68% | 0.3 ± 0.5 | 9/10 | 4/5 | 0, 1 | 1.38 (72%) |
| Milwaukee Bucks @ Boston Celtics | **Jaime Jaquez Jr.: más de 0.5 triples** | **69%** | 74% | 65% | 1.4 ± 1.2 | 9/10 | 6/7 | 2, 1, 1 | 1.45 (69%) |
| Utah Jazz @ New Orleans Pelicans | **Herbert Jones: más de 0.5 triples** | **67%** | 68% | 66% | 1.2 ± 1.1 | 7/10 | 4/7 | 1, 3, 2 | 1.41 (71%) |
| Miami Heat @ LA Clippers | **Kris Dunn: menos de 1.5 triples** | **67%** | 68% | 66% | 1.2 ± 1.1 | 9/10 | 6/7 | 1, 2 | 1.42 (70%) |
| Cleveland Cavaliers @ Oklahoma City Thunder | **Jaylin Williams: menos de 6.5 rebotes** ⚠️ suplente | **66%** | 76% | 57% | 4.6 ± 2.6 | 7/10 | 6/7 | 3, 3, 3 | 1.63 (61%) |
| Philadelphia 76ers @ Detroit Pistons | **Javonte Green: más de 0.5 triples** ⚠️ suplente | **66%** | 68% | 64% | 1.3 ± 1.4 | 8/10 | 6/7 | 0, 0, 4, 3, 1 | 1.47 (68%) |
| Minnesota Timberwolves @ Houston Rockets | **Tari Eason: menos de 1.5 triples** ⚠️ suplente | **66%** | 66% | 65% | 1.1 ± 1.2 | 6/10 | 6/8 | 0, 1 | 1.43 (70%) |
| Charlotte Hornets @ Brooklyn Nets | **Naz Reid: menos de 2.5 asistencias** | **65%** | 70% | 61% | 1.9 ± 1.8 | 9/10 | 7/8 | 7, 1, 2 | 1.53 (65%) |

**Si haces combinada:** cada selección que añades multiplica el riesgo. Probabilidad de acertar todas con las más probables de partidos distintos:

- 2 selecciones: **49%**
- 3 selecciones: **33%**
- 4 selecciones: **22%**
- 5 selecciones: **14%**
- 6 selecciones: **9%**

Dentro de un mismo partido (bet builder) las selecciones no son independientes y el cálculo es aún menos fiable. Con 12 selecciones al 65 % la probabilidad de acertar todas es menor del 1 %.

### En qué se basan las 10 más probables

#### Khaman Maluach: menos de 0.5 triples (71%) — Portland Trail Blazers @ Phoenix Suns

**¿Por qué 0.3 triples?** (línea 0.5; 18.8 minutos esperados)

Razonamiento (2 factores a favor, 4 en contra):

- ❌ Minutos: 18.8 esperados (titular, ±6.1).
- ✅ Forma: 0.2 en sus últimos 5, 0.2 esta temporada (5 partidos), 0.1 la temporada pasada (línea 0.5).
- ➖ Cómo produce triples: 0.8 triples intentados (su ritmo 1.7 por 36'; el rival concede -6% de triples en su reparto) × 33% esperado.
- ❌ Defensa: el rival concede +22% de triples por minuto a pívots (defensa débil); ajuste aplicado +10%; en su zona principal (triple) el rival concede 35% (liga 35%).
- ❌ Altura: mide 7'2", 2.2 pulgadas más que los pívots del rival (+0.8% en esta estadística).
- ➖ Ritmo del partido: -1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ➖ Contra este rival: 0, 1 (1 de 2 a favor).
- ✅ Últimos 10: la habría pasado 9 de 10.
- ❌ Bajas del rival: sin Ja Morant (titular); +1.7% en esta estadística.
- ⚠️ Mark Williams ya no jugó en sus últimos partidos: la baja ya está en sus minutos.

- ⚠️ Alertas: minutos inestables.
- Triples **0.3** (por componentes 0.3 · por tasa por minuto y defensa rival 0.3): 0.8 triples intentados (su ritmo 1.7 por 36'; el rival concede -6% de triples en su reparto) × 33% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 20.2 | 15.2 | 20.2 | 9.0 | 16.5 |
| Triples anotados | 0.2 | 0.1 | 0.2 | 0.1 | 0.5 |
| Triples intentados | 0.6 | 0.5 | 0.6 | 0.5 | 0.5 |
| % triples | 33.3% | 20.0% | 33.3% | 21.7% | 100.0% |

#### Jaime Jaquez Jr.: más de 0.5 triples (69%) — Milwaukee Bucks @ Boston Celtics

**¿Por qué 1.4 triples?** (línea 0.5; 27.3 minutos esperados)

Razonamiento (5 factores a favor, 1 en contra):

- ✅ Minutos: 27.3 esperados (titular, ±3.5).
- ✅ Forma: 1.6 en sus últimos 5, 1.6 esta temporada (7 partidos), 0.9 la temporada pasada (línea 0.5).
- ➖ Cómo produce triples: 3.7 triples intentados (su ritmo 4.6 por 36'; el rival concede +9% de triples en su reparto) × 34% esperado.
- ✅ Defensa: el rival concede +12% de triples por minuto a aleros/ala-pívots (defensa débil); ajuste aplicado +5%; en su zona principal (triple) el rival concede 36% (liga 35%).
- ❌ Altura: mide 6'6", 2.0 pulgadas menos que los aleros/ala-pívots del rival (-0.7% en esta estadística).
- ➖ Ritmo del partido: +1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 2, 1, 1 (3 de 3 a favor).
- ✅ Últimos 10: la habría pasado 9 de 10.
- ⚠️ cambio de rol esta temporada (por minuto): reb +48%, ast -39%; se da más peso a la línea de la casa.

- Triples **1.4** (por componentes 1.3 · por tasa por minuto y defensa rival 1.4): 3.7 triples intentados (su ritmo 4.6 por 36'; el rival concede +9% de triples en su reparto) × 34% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 26.0 | 29.9 | 28.0 | 28.5 | 32.3 |
| Triples anotados | 1.6 | 1.7 | 1.6 | 0.8 | 1.3 |
| Triples intentados | 3.8 | 3.8 | 3.6 | 2.5 | 4.3 |
| % triples | 42.1% | 44.7% | 44.0% | 31.7% | 30.8% |

#### Herbert Jones: más de 0.5 triples (67%) — Utah Jazz @ New Orleans Pelicans

**¿Por qué 1.2 triples?** (línea 0.5; 23.9 minutos esperados)

Razonamiento (7 factores a favor, 1 en contra):

- ✅ Minutos: 23.9 esperados (titular, ±5.7).
- ✅ Forma: 0.8 en sus últimos 5, 0.9 esta temporada (7 partidos), 1.4 la temporada pasada (línea 0.5).
- ➖ Cómo produce triples: 3.8 triples intentados (su ritmo 5.2 por 36'; el rival concede +7% de triples en su reparto) × 33% esperado.
- ✅ Defensa: el rival concede +10% de triples por minuto a aleros/ala-pívots (defensa débil); ajuste aplicado +7%; en su zona principal (triple) el rival concede 37% (liga 35%).
- ❌ Altura: mide 6'7", 2.5 pulgadas menos que los aleros/ala-pívots del rival (-0.9% en esta estadística).
- ✅ Ritmo del partido: +3% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 1, 3, 2 (3 de 3 a favor).
- ✅ Últimos 10: la habría pasado 7 de 10.
- ✅ Bajas del rival: sin Jaren Jackson Jr. (titular); +1.7% en esta estadística.
- ⚠️ Yves Missi ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ cambio de rol esta temporada (por minuto): ast -54%; se da más peso a la línea de la casa.

- Triples **1.2** (por componentes 1.3 · por tasa por minuto y defensa rival 1.2): 3.8 triples intentados (su ritmo 5.2 por 36'; el rival concede +7% de triples en su reparto) × 33% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 24.0 | 20.3 | 22.1 | 28.4 | 26.7 |
| Triples anotados | 0.8 | 1.0 | 0.9 | 1.4 | 2.0 |
| Triples intentados | 3.2 | 2.9 | 2.7 | 4.6 | 4.3 |
| % triples | 25.0% | 34.5% | 31.6% | 30.9% | 46.2% |

#### Kris Dunn: menos de 1.5 triples (67%) — Miami Heat @ LA Clippers

**¿Por qué 1.2 triples?** (línea 1.5; 29.6 minutos esperados)

Razonamiento (3 factores a favor, 2 en contra):

- ✅ Minutos: 29.6 esperados (titular, ±3.0).
- ✅ Forma: 0.6 en sus últimos 5, 0.9 esta temporada (7 partidos), 1.0 la temporada pasada (línea 1.5).
- ➖ Cómo produce triples: 3.4 triples intentados (su ritmo 3.9 por 36'; el rival concede +2% de triples en su reparto) × 37% esperado.
- ❌ Defensa: el rival concede +10% de triples por minuto a bases/escoltas (defensa débil); ajuste aplicado +6%; en su zona principal (triple) el rival concede 35% (liga 35%).
- ❌ Ritmo del partido: +2% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ➖ Contra este rival: 1, 2 (1 de 2 a favor).
- ✅ Últimos 10: la habría pasado 9 de 10.
- ⚠️ Jordan Miller ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ Bradley Beal ya no jugó en sus últimos partidos: la baja ya está en sus minutos.

- Triples **1.2** (por componentes 1.3 · por tasa por minuto y defensa rival 1.2): 3.4 triples intentados (su ritmo 3.9 por 36'; el rival concede +2% de triples en su reparto) × 37% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 29.6 | 29.0 | 29.9 | 27.3 | 24.5 |
| Triples anotados | 0.6 | 0.8 | 0.9 | 1.0 | 1.5 |
| Triples intentados | 2.0 | 2.5 | 2.6 | 2.6 | 2.0 |
| % triples | 30.0% | 32.0% | 33.3% | 37.5% | 75.0% |

#### Jaylin Williams: menos de 6.5 rebotes (66%) — Cleveland Cavaliers @ Oklahoma City Thunder

**¿Por qué 4.6 rebotes?** (línea 6.5; 19.9 minutos esperados)

Razonamiento (3 factores a favor, 1 en contra):

- ❌ Minutos: 19.9 esperados (suplente, ±6.1).
- ✅ Forma: 3.6 en sus últimos 5, 4.1 esta temporada (7 partidos), 5.5 la temporada pasada (línea 6.5).
- ➖ Cómo produce rebotes: defensivos 4.0 = captura el 20.1% de los fallos del rival en pista × 48.2 fallos esperados del rival (liga 47.0) × 41% del partido; ofensivos 0.5 = 2.6% de los fallos de su equipo × 47.2.
- ➖ Defensa: el rival concede -2% de rebotes por minuto a aleros/ala-pívots (defensa media); ajuste aplicado -2%.
- ➖ Ritmo del partido: -0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 3, 3, 3 (3 de 3 a favor).
- ✅ Últimos 10: la habría pasado 7 de 10.
- ⚠️ en el parte de lesiones: day-to-day.
- ⚠️ Chet Holmgren ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ Cason Wallace ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ cambio de rol esta temporada (por minuto): pts -57%, tpm -49%; se da más peso a la línea de la casa.

- ⚠️ Alertas: suplente, minutos inestables, en el parte de lesiones.
- Rebotes **4.6** (por componentes 4.5 · por tasa por minuto y defensa rival 4.6): defensivos 4.0 = captura el 20.1% de los fallos del rival en pista × 48.2 fallos esperados del rival (liga 47.0) × 41% del partido; ofensivos 0.5 = 2.6% de los fallos de su equipo × 47.2.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 19.4 | 19.8 | 18.4 | 19.0 | 15.0 |
| Rebotes | 3.6 | 5.2 | 4.1 | 5.2 | 3.0 |
| % de los fallos del rival que captura | 16.8% | 22.1% | 19.7% | 24.3% | 17.2% |
| % de los fallos de su equipo que captura | 1.0% | 2.9% | 1.5% | 2.7% | 2.2% |

#### Javonte Green: más de 0.5 triples (66%) — Philadelphia 76ers @ Detroit Pistons

**¿Por qué 1.3 triples?** (línea 0.5; 19.4 minutos esperados)

Razonamiento (3 factores a favor, 2 en contra):

- ❌ Minutos: 19.4 esperados (suplente, ±3.1).
- ✅ Forma: 0.8 en sus últimos 5, 1.4 esta temporada (7 partidos), 1.2 la temporada pasada (línea 0.5).
- ➖ Cómo produce triples: 4.0 triples intentados (su ritmo 7.4 por 36'; el rival concede +2% de triples en su reparto) × 35% esperado.
- ❌ Defensa: el rival concede -3% de triples por minuto a bases/escoltas (defensa fuerte); ajuste aplicado -3%; en su zona principal (triple) el rival concede 34% (liga 35%).
- ➖ Ritmo del partido: -1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 0, 0, 4, 3, 1 (3 de 5 a favor).
- ✅ Últimos 10: la habría pasado 8 de 10.
- ⚠️ Jalen Duren ya no jugó en sus últimos partidos: la baja ya está en sus minutos.

- ⚠️ Alertas: suplente.
- Triples **1.3** (por componentes 1.4 · por tasa por minuto y defensa rival 1.3): 4.0 triples intentados (su ritmo 7.4 por 36'; el rival concede +2% de triples en su reparto) × 35% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 20.4 | 15.3 | 19.0 | 17.1 | 22.4 |
| Triples anotados | 0.8 | 1.2 | 1.4 | 1.1 | 1.6 |
| Triples intentados | 3.8 | 3.7 | 4.3 | 3.0 | 4.0 |
| % triples | 21.1% | 32.4% | 33.3% | 36.9% | 40.0% |

#### Tari Eason: menos de 1.5 triples (66%) — Minnesota Timberwolves @ Houston Rockets

**¿Por qué 1.1 triples?** (línea 1.5; 25.6 minutos esperados)

Razonamiento (3 factores a favor, 2 en contra):

- ❌ Minutos: 25.6 esperados (suplente, ±6.8).
- ✅ Forma: 1.4 en sus últimos 5, 0.9 esta temporada (8 partidos), 1.5 la temporada pasada (línea 1.5).
- ➖ Cómo produce triples: 3.4 triples intentados (su ritmo 5.2 por 36'; el rival concede -8% de triples en su reparto) × 34% esperado.
- ✅ Defensa: el rival concede -10% de triples por minuto a aleros/ala-pívots (defensa fuerte); ajuste aplicado -6%; en su zona principal (esquina3) el rival concede 38% (liga 38%).
- ➖ Ritmo del partido: -1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 0, 1 (2 de 2 a favor).
- ➖ Últimos 10: la habría pasado 6 de 10.
- ❌ Bajas del rival: sin Anthony Edwards (titular); +1.7% en esta estadística.
- ⚠️ Steven Adams ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ cambio de rol esta temporada (por minuto): tpm -40%; se da más peso a la línea de la casa.

- ⚠️ Alertas: suplente, minutos inestables, cambio de rol.
- Triples **1.1** (por componentes 1.2 · por tasa por minuto y defensa rival 1.0): 3.4 triples intentados (su ritmo 5.2 por 36'; el rival concede -8% de triples en su reparto) × 34% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 27.2 | 26.5 | 24.6 | 26.5 | 22.5 |
| Triples anotados | 1.4 | 1.1 | 0.9 | 1.6 | 0.5 |
| Triples intentados | 4.0 | 3.8 | 3.1 | 4.4 | 2.0 |
| % triples | 35.0% | 28.9% | 28.0% | 35.5% | 25.0% |

#### Naz Reid: menos de 2.5 asistencias (65%) — Charlotte Hornets @ Brooklyn Nets

**¿Por qué 1.9 asistencias?** (línea 2.5; 28.8 minutos esperados)

Razonamiento (5 factores a favor, 1 en contra):

- ❌ Minutos: 28.8 esperados (titular, ±7.0).
- ✅ Forma: 1.2 en sus últimos 5, 1.9 esta temporada (8 partidos), 2.0 la temporada pasada (línea 2.5).
- ➖ Cómo produce asistencias: asiste el 10.3% de las canastas de sus compañeros en pista × 18.3 canastas de compañeros esperadas (su equipo 39.8 por 48' contra esta defensa).
- ✅ Defensa: el rival concede -6% de asistencias por minuto a pívots (defensa fuerte); ajuste aplicado -6%.
- ✅ Ritmo del partido: -2% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 7, 1, 2 (2 de 3 a favor).
- ✅ Últimos 10: la habría pasado 9 de 10.
- ⚠️ Grant Williams ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ Kon Knueppel ya no jugó en sus últimos partidos: la baja ya está en sus minutos.

- ⚠️ Alertas: minutos inestables.
- Asistencias **1.9** (por componentes 1.9 · por tasa por minuto y defensa rival 1.9): asiste el 10.3% de las canastas de sus compañeros en pista × 18.3 canastas de compañeros esperadas (su equipo 39.8 por 48' contra esta defensa).

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 27.2 | 29.4 | 28.9 | 26.1 | 28.7 |
| Asistencias | 1.2 | 1.8 | 1.9 | 2.2 | 3.3 |
| % de las canastas de compañeros que asiste | 7.0% | 9.9% | 10.5% | 10.9% | 16.5% |
| Pérdidas por jugada | 14.7% | 12.7% | 14.8% | 11.9% | 6.7% |


## Philadelphia 76ers @ Detroit Pistons

Diferencia esperada: Detroit Pistons por 2.5.

Parte de lesiones: Isaiah Joe (Out); Jalen Duren (Out); Dominick Barlow (Out); Ariel Hukporti (Out).

Ventajas del partido (los dos lados): puntos esperados frente a su media de los últimos 10, ajuste por la defensa rival y diferencia de estatura con los rivales de su posición.

| Equipo | Jugador | Puntos esperados | Su media (últ. 10) | Defensa rival en puntos | Rebotes esperados | Altura vs rival |
|---|---|---|---|---|---|---|
| PHI | Tyrese Maxey | 24.6 | 26.7 | -5% | 3.8 | -3.4" |
| PHI | Jaylen Brown | 21.1 | 21.7 | -5% | 5.9 | +0.6" |
| PHI | VJ Edgecombe | 13.1 | 12.5 | -5% | 5.7 | -0.4" |
| PHI | LeBron James | 17.1 | 19.0 | -3% | 6.5 | +0.8" |
| PHI | Joel Embiid | 19.1 | 20.1 | -8% | 8.3 | +2.4" |
| DET | Cade Cunningham | 21.0 | 21.9 | -2% | 5.1 | +1.7" |
| DET | Duncan Robinson | 15.8 | 15.6 | -1% | 3.0 | -1.6" |
| DET | Paul Reed | 14.3 | 13.0 | -1% | 7.6 | +0.4" |
| DET | Ausar Thompson | 9.8 | 8.6 | -2% | 6.3 | +2.7" |
| DET | Daniss Jenkins | 10.0 | 10.3 | -2% | 3.4 | -0.3" |

Picks seguros de titulares estables:

| Jugador | Pick seguro | Prob. | Cuota mínima | Esperado | Últ. 10 |
|---|---|---|---|---|---|
| Joel Embiid | **más de 3.5 rebotes** | **91%** | 1.09 | 8.3 | 10/10 |
| Tyrese Maxey | **más de 1.5 asistencias** | **90%** | 1.11 | 4.6 | 10/10 |
| Tyrese Maxey | **más de 16.5 puntos** | **89%** | 1.12 | 24.6 | 10/10 |
| LeBron James | **más de 2.5 asistencias** | **89%** | 1.12 | 5.7 | 10/10 |
| Jaylen Brown | **más de 20.5 pts+reb+ast** | **87%** | 1.15 | 30.8 | 10/10 |
| Cade Cunningham | **más de 12.5 puntos** | **87%** | 1.15 | 21.0 | 10/10 |

Las 8 más probables (máximo 2 por jugador: las de un mismo jugador suelen ganar o perder juntas).

| Prop | Prob. final | Modelo | Casa | Esperado | Últ. 10 | Temporada | vs este rival | Cuota (implícita) |
|---|---|---|---|---|---|---|---|---|
| **Javonte Green: más de 0.5 triples** ⚠️ suplente | **66%** | 68% | 64% | 1.3 ± 1.4 | 8/10 | 6/7 | 0, 0, 4, 3, 1 | 1.47 (68%) |
| **Kevin Huerter: menos de 1.5 triples** ⚠️ suplente | **64%** | 63% | 65% | 1.3 ± 1.2 | 8/10 | 5/7 | 1, 1, 2, 1, 2 | 1.43 (70%) |
| **Daniss Jenkins: menos de 1.5 triples** ⚠️ suplente | **64%** | 61% | 66% | 1.3 ± 1.2 | 5/10 | 4/7 | 3, 2, 0, 5 | 1.41 (71%) |
| **LeBron James: más de 0.5 triples** | **64%** | 66% | 62% | 1.1 ± 1.1 | 7/10 | 3/6 | 0, 1, 3 | 1.51 (66%) |
| **Cade Cunningham: menos de 8.5 asistencias** | **63%** | 74% | 55% | 6.8 ± 2.8 | 10/10 | 7/7 | 8, 13, 11 | 1.71 (58%) |
| **Anfernee Simons: más de 1.5 rebotes** ⚠️ suplente | **62%** | 65% | 59% | 2.2 ± 1.5 | 7/10 | 6/8 | 3, 2, 3, 0, 1 | 1.59 (63%) |
| **Joel Embiid: más de 0.5 triples** | **61%** | 54% | 65% | 0.9 ± 1.0 | 4/10 | 2/6 | - | 1.43 (70%) |
| **Anfernee Simons: más de 1.5 triples** ⚠️ suplente | **60%** | 63% | 58% | 2.5 ± 1.9 | 5/10 | 4/8 | 1, 0, 1, 0, 1 | 1.62 (62%) |

### Fichas de los jugadores destacados

#### Javonte Green (bases/escoltas) vs Philadelphia 76ers

- Minutos esperados: **19.4** (± 3.1); 99 partidos en la base.
- Jalen Duren ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Su prop más probable hoy: **Javonte Green: más de 0.5 triples** (66%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Philadelphia 76ers contra bases/escoltas en triples: -3% respecto a la media; ajuste por su historial contra defensas similares: -3%.

**¿Por qué 1.3 triples?** (línea 0.5; 19.4 minutos esperados)

Razonamiento (3 factores a favor, 2 en contra):

- ❌ Minutos: 19.4 esperados (suplente, ±3.1).
- ✅ Forma: 0.8 en sus últimos 5, 1.4 esta temporada (7 partidos), 1.2 la temporada pasada (línea 0.5).
- ➖ Cómo produce triples: 4.0 triples intentados (su ritmo 7.4 por 36'; el rival concede +2% de triples en su reparto) × 35% esperado.
- ❌ Defensa: el rival concede -3% de triples por minuto a bases/escoltas (defensa fuerte); ajuste aplicado -3%; en su zona principal (triple) el rival concede 34% (liga 35%).
- ➖ Ritmo del partido: -1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 0, 0, 4, 3, 1 (3 de 5 a favor).
- ✅ Últimos 10: la habría pasado 8 de 10.
- ⚠️ Jalen Duren ya no jugó en sus últimos partidos: la baja ya está en sus minutos.

- ⚠️ Alertas: suplente.
- Triples **1.3** (por componentes 1.4 · por tasa por minuto y defensa rival 1.3): 4.0 triples intentados (su ritmo 7.4 por 36'; el rival concede +2% de triples en su reparto) × 35% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 20.4 | 15.3 | 19.0 | 17.1 | 22.4 |
| Triples anotados | 0.8 | 1.2 | 1.4 | 1.1 | 1.6 |
| Triples intentados | 3.8 | 3.7 | 4.3 | 3.0 | 4.0 |
| % triples | 21.1% | 32.4% | 33.3% | 36.9% | 40.0% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +5%, vs defensa media -19%, vs defensa débil +14%; rebotes: vs defensa fuerte -3%, vs defensa media -5%, vs defensa débil +6%; asistencias: vs defensa fuerte -4%, vs defensa media +2%, vs defensa débil +3%; triples: vs defensa fuerte -8%, vs defensa media +12%, vs defensa débil -2%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 38% | 29% | 35% | 34% |
| triple de esquina | 26% | 45% | 38% | 37% |
| bajo el aro | 24% | 65% | 68% | 67% |
| pintura | 9% | 40% | 45% | 42% |
| media distancia | 3% | 40% | 41% | 40% |

#### Kevin Huerter (bases/escoltas) vs Philadelphia 76ers

- Minutos esperados: **20.4** (± 3.5); 80 partidos en la base.
- Jalen Duren ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Su prop más probable hoy: **Kevin Huerter: menos de 1.5 triples** (64%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Philadelphia 76ers contra bases/escoltas en triples: -3% respecto a la media; ajuste por su historial contra defensas similares: +0%.

**¿Por qué 1.3 triples?** (línea 1.5; 20.4 minutos esperados)

Razonamiento (3 factores a favor, 3 en contra):

- ❌ Minutos: 20.4 esperados (suplente, ±3.5).
- ❌ Forma: 1.6 en sus últimos 5, 1.4 esta temporada (7 partidos), 1.4 la temporada pasada (línea 1.5).
- ➖ Cómo produce triples: 3.9 triples intentados (su ritmo 6.7 por 36'; el rival concede +2% de triples en su reparto) × 32% esperado.
- ✅ Defensa: el rival concede -3% de triples por minuto a bases/escoltas (defensa fuerte); ajuste aplicado -3%; en su zona principal (triple) el rival concede 34% (liga 35%).
- ❌ Altura: mide 6'6", 1.7 pulgadas más que los bases/escoltas del rival (+0.6% en esta estadística).
- ➖ Ritmo del partido: -1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 1, 1, 2, 1, 2 (3 de 5 a favor).
- ✅ Últimos 10: la habría pasado 8 de 10.
- ⚠️ Jalen Duren ya no jugó en sus últimos partidos: la baja ya está en sus minutos.

- ⚠️ Alertas: suplente.
- Triples **1.3** (por componentes 1.2 · por tasa por minuto y defensa rival 1.3): 3.9 triples intentados (su ritmo 6.7 por 36'; el rival concede +2% de triples en su reparto) × 32% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 21.0 | 16.7 | 20.4 | 21.8 | 25.0 |
| Triples anotados | 1.6 | 1.1 | 1.4 | 1.4 | 1.4 |
| Triples intentados | 3.4 | 2.9 | 3.7 | 4.5 | 5.6 |
| % triples | 47.1% | 37.9% | 38.5% | 30.9% | 25.0% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -0%, vs defensa media -4%, vs defensa débil +3%; rebotes: vs defensa fuerte -11%, vs defensa media -7%, vs defensa débil +14%; asistencias: vs defensa fuerte -14%, vs defensa media +11%, vs defensa débil +5%; triples: vs defensa fuerte -9%, vs defensa media -5%, vs defensa débil +23%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 43% | 32% | 35% | 34% |
| bajo el aro | 22% | 75% | 68% | 67% |
| pintura | 17% | 45% | 45% | 42% |
| triple de esquina | 12% | 36% | 38% | 37% |
| media distancia | 5% | 39% | 41% | 40% |

#### Daniss Jenkins (bases/escoltas) vs Philadelphia 76ers

- Minutos esperados: **24.5** (± 5.2); 91 partidos en la base.
- Jalen Duren ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Su prop más probable hoy: **Daniss Jenkins: menos de 1.5 triples** (64%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Philadelphia 76ers contra bases/escoltas en triples: -3% respecto a la media; ajuste por su historial contra defensas similares: -1%.

**¿Por qué 1.3 triples?** (línea 1.5; 24.5 minutos esperados)

Razonamiento (1 factores a favor, 3 en contra):

- ❌ Minutos: 24.5 esperados (suplente, ±5.2).
- ❌ Forma: 1.6 en sus últimos 5, 1.4 esta temporada (7 partidos), 1.1 la temporada pasada (línea 1.5).
- ➖ Cómo produce triples: 3.8 triples intentados (su ritmo 5.4 por 36'; el rival concede +2% de triples en su reparto) × 35% esperado.
- ✅ Defensa: el rival concede -3% de triples por minuto a bases/escoltas (defensa fuerte); ajuste aplicado -3%; en su zona principal (triple) el rival concede 34% (liga 35%).
- ➖ Ritmo del partido: -1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ❌ Contra este rival: 3, 2, 0, 5 (1 de 4 a favor).
- ➖ Últimos 10: la habría pasado 5 de 10.
- ⚠️ Jalen Duren ya no jugó en sus últimos partidos: la baja ya está en sus minutos.

- ⚠️ Alertas: suplente.
- Triples **1.3** (por componentes 1.3 · por tasa por minuto y defensa rival 1.3): 3.8 triples intentados (su ritmo 5.4 por 36'; el rival concede +2% de triples en su reparto) × 35% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 26.6 | 25.6 | 24.3 | 20.3 | 31.2 |
| Triples anotados | 1.6 | 1.5 | 1.4 | 1.0 | 2.5 |
| Triples intentados | 4.2 | 3.8 | 3.4 | 2.9 | 4.5 |
| % triples | 38.1% | 39.5% | 41.7% | 35.3% | 55.6% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -4%, vs defensa media -4%, vs defensa débil +14%; rebotes: vs defensa fuerte -17%, vs defensa media +2%, vs defensa débil +15%; asistencias: vs defensa fuerte -20%, vs defensa media +3%, vs defensa débil +16%; triples: vs defensa fuerte -5%, vs defensa media +8%, vs defensa débil -3%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 26% | 36% | 35% | 34% |
| pintura | 26% | 34% | 45% | 42% |
| bajo el aro | 20% | 60% | 68% | 67% |
| media distancia | 16% | 43% | 41% | 40% |
| triple de esquina | 11% | 37% | 38% | 37% |

#### LeBron James (aleros/ala-pívots) vs Detroit Pistons

- Minutos esperados: **32.9** (± 3.0); 79 partidos en la base.
- cambio de rol esta temporada (por minuto): tpm -38%; se da más peso a la línea de la casa
- Su prop más probable hoy: **LeBron James: más de 0.5 triples** (64%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Detroit Pistons contra aleros/ala-pívots en triples: -2% respecto a la media; ajuste por su historial contra defensas similares: -3%.

**¿Por qué 1.1 triples?** (línea 0.5; 32.9 minutos esperados)

Razonamiento (4 factores a favor, 1 en contra):

- ✅ Minutos: 32.9 esperados (titular, ±3.0).
- ✅ Forma: 1.0 en sus últimos 5, 0.8 esta temporada (6 partidos), 1.3 la temporada pasada (línea 0.5).
- ➖ Cómo produce triples: 4.0 triples intentados (su ritmo 4.4 por 36'; el rival concede +4% de triples en su reparto) × 31% esperado.
- ❌ Defensa: el rival concede +1% de triples por minuto a aleros/ala-pívots (defensa media); ajuste aplicado -2%; en su zona principal (triple) el rival concede 33% (liga 35%).
- ➖ Ritmo del partido: -1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 0, 1, 3 (2 de 3 a favor).
- ✅ Últimos 10: la habría pasado 7 de 10.
- ⚠️ cambio de rol esta temporada (por minuto): tpm -38%; se da más peso a la línea de la casa.

- ⚠️ Alertas: cambio de rol.
- Triples **1.1** (por componentes 1.2 · por tasa por minuto y defensa rival 1.1): 4.0 triples intentados (su ritmo 4.4 por 36'; el rival concede +4% de triples en su reparto) × 31% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 32.8 | 34.9 | 33.0 | 32.8 | 34.7 |
| Triples anotados | 1.0 | 1.3 | 0.8 | 1.3 | 1.3 |
| Triples intentados | 3.6 | 4.3 | 3.5 | 4.1 | 5.0 |
| % triples | 27.8% | 30.2% | 23.8% | 32.1% | 26.7% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -0%, vs defensa media +2%, vs defensa débil -2%; rebotes: vs defensa fuerte -11%, vs defensa media +6%, vs defensa débil +10%; asistencias: vs defensa fuerte -12%, vs defensa media +2%, vs defensa débil +11%; triples: vs defensa fuerte +6%, vs defensa media +3%, vs defensa débil -12%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 35% | 74% | 68% | 64% |
| pintura | 22% | 40% | 45% | 44% |
| triple frontal | 22% | 33% | 35% | 33% |
| media distancia | 16% | 42% | 41% | 39% |
| triple de esquina | 5% | 31% | 38% | 39% |

#### Cade Cunningham (bases/escoltas) vs Philadelphia 76ers

- Minutos esperados: **31.9** (± 4.6); 86 partidos en la base.
- Jalen Duren ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Su prop más probable hoy: **Cade Cunningham: menos de 8.5 asistencias** (63%). Con 80% de probabilidad: más de 3.5 / menos de 9.5.
- Defensa de Philadelphia 76ers contra bases/escoltas en asistencias: +0% respecto a la media; ajuste por su historial contra defensas similares: +1%.

**¿Por qué 6.8 asistencias?** (línea 8.5; 31.9 minutos esperados)

Razonamiento (4 factores a favor, 1 en contra):

- ✅ Minutos: 31.9 esperados (titular, ±4.6).
- ✅ Forma: 6.8 en sus últimos 5, 7.1 esta temporada (7 partidos), 9.2 la temporada pasada (línea 8.5).
- ➖ Cómo produce asistencias: asiste el 31.4% de las canastas de sus compañeros en pista × 20.4 canastas de compañeros esperadas (su equipo 41.4 por 48' contra esta defensa).
- ➖ Defensa: el rival concede +0% de asistencias por minuto a bases/escoltas (defensa media); ajuste aplicado +0%.
- ➖ Ritmo del partido: -1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ❌ Contra este rival: 8, 13, 11 (1 de 3 a favor).
- ✅ Últimos 10: la habría pasado 10 de 10.
- ✅ Racha: la pasó en sus 7 partidos de esta temporada (al inicio de 2025-26 estas rachas siguieron más de lo que esperaba el modelo).
- ⚠️ Jalen Duren ya no jugó en sus últimos partidos: la baja ya está en sus minutos.

- Asistencias **6.8** (por componentes 6.4 · por tasa por minuto y defensa rival 7.0): asiste el 31.4% de las canastas de sus compañeros en pista × 20.4 canastas de compañeros esperadas (su equipo 41.4 por 48' contra esta defensa).

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 32.6 | 34.6 | 32.6 | 33.9 | 34.0 |
| Asistencias | 6.8 | 6.9 | 7.1 | 9.2 | 10.7 |
| % de las canastas de compañeros que asiste | 34.2% | 30.3% | 33.7% | 39.0% | 44.6% |
| Pérdidas por jugada | 12.2% | 17.8% | 16.3% | 15.6% | 19.6% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -7%, vs defensa media +7%, vs defensa débil +4%; rebotes: vs defensa fuerte -5%, vs defensa media -3%, vs defensa débil +6%; asistencias: vs defensa fuerte -8%, vs defensa media -6%, vs defensa débil +18%; triples: vs defensa fuerte -7%, vs defensa media -4%, vs defensa débil +19%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 30% | 35% | 35% | 34% |
| pintura | 30% | 45% | 45% | 42% |
| bajo el aro | 22% | 62% | 68% | 67% |
| media distancia | 16% | 47% | 41% | 40% |
| triple de esquina | 2% | 35% | 38% | 37% |

## Atlanta Hawks @ Washington Wizards

Diferencia esperada: Atlanta Hawks por 2.5.

Parte de lesiones: Anthony Gill (Day-To-Day); Jock Landale (Out); Reece Beekman (Out); Justin Champagnie (Out); Jalen Johnson (Day-To-Day); Mouhamed Gueye (Out); Tristan Vukcevic (Out); Henri Veesaar (Out); Alex Sarr (Day-To-Day).

Ventajas del partido (los dos lados): puntos esperados frente a su media de los últimos 10, ajuste por la defensa rival y diferencia de estatura con los rivales de su posición.

| Equipo | Jugador | Puntos esperados | Su media (últ. 10) | Defensa rival en puntos | Rebotes esperados | Altura vs rival |
|---|---|---|---|---|---|---|
| WSH | Trae Young | 19.9 | 18.6 | -1% | 3.7 | -2.6" |
| WSH | Anthony Davis | 21.8 | 22.7 | +2% | 10.0 | +1.2" |
| WSH | Kyshawn George | 16.6 | 15.4 | +1% | 5.4 | -0.8" |
| ATL | Jalen Johnson | 19.3 | 18.1 | +4% | 9.2 | -0.1" |
| ATL | Nickeil Alexander-Walker | 19.7 | 19.6 | +1% | 3.3 | +0.0" |
| ATL | Onyeka Okongwu | 14.2 | 11.6 | +4% | 8.0 | +1.9" |
| ATL | Dyson Daniels | 11.1 | 9.8 | +1% | 5.7 | +2.0" |
| WSH | Bilal Coulibaly | 10.5 | 11.3 | -1% | 4.0 | +2.4" |
| ATL | CJ McCollum | 15.4 | 13.1 | +0% | 3.1 | -2.0" |
| WSH | Alex Sarr | 11.3 | 8.4 | +2% | 6.4 | +1.2" |

Picks seguros de titulares estables:

| Jugador | Pick seguro | Prob. | Cuota mínima | Esperado | Últ. 10 |
|---|---|---|---|---|---|
| Trae Young | **más de 11.5 puntos** | **88%** | 1.13 | 19.9 | 9/10 |
| Jalen Johnson | **más de 2.5 asistencias** | **87%** | 1.15 | 6.8 | 10/10 |
| Anthony Davis | **más de 5.5 rebotes** | **87%** | 1.15 | 10.0 | 9/10 |
| Nickeil Alexander-Walker | **más de 10.5 puntos** | **87%** | 1.16 | 19.7 | 10/10 |
| Anthony Davis | **más de 12.5 puntos** | **86%** | 1.16 | 21.8 | 9/10 |
| Jalen Johnson | **más de 24.5 pts+reb+ast** | **86%** | 1.17 | 35.3 | 8/10 |

Las 8 más probables (máximo 2 por jugador: las de un mismo jugador suelen ganar o perder juntas).

| Prop | Prob. final | Modelo | Casa | Esperado | Últ. 10 | Temporada | vs este rival | Cuota (implícita) |
|---|---|---|---|---|---|---|---|---|
| **CJ McCollum: menos de 2.5 triples** | **63%** | 66% | 61% | 2.0 ± 1.6 | 8/10 | 6/8 | 2, 0 | 1.54 (65%) |
| **Aaron Wiggins: menos de 2.5 triples** ⚠️ suplente | **63%** | 66% | 60% | 2.0 ± 1.5 | 6/10 | 4/8 | 1, 0 | 1.55 (65%) |
| **Trae Young: menos de 2.5 triples** | **62%** | 67% | 58% | 1.9 ± 1.7 | 7/10 | 5/7 | - | 1.61 (62%) |
| **Dyson Daniels: menos de 0.5 triples** | **61%** | 63% | 58% | 0.5 ± 0.7 | 7/10 | 7/8 | 1, 0, 0, 1 | 1.61 (62%) |
| **Tre Johnson: menos de 1.5 triples** ⚠️ suplente | **60%** | 60% | 60% | 1.4 ± 1.3 | 7/10 | 4/6 | 2, 0 | 1.56 (64%) |
| **Dyson Daniels: menos de 5.5 asistencias** | **60%** | 65% | 55% | 4.7 ± 2.2 | 9/10 | 7/8 | 11, 7, 3, 7 | 1.70 (59%) |
| **Trae Young: más de 2.5 rebotes** | **59%** | 63% | 57% | 3.7 ± 2.2 | 7/10 | 5/7 | - | 1.64 (61%) |
| **Kyshawn George: menos de 4.5 asistencias** | **59%** | 59% | 60% | 4.5 ± 2.3 | 7/10 | 4/7 | 2, 7 | 1.57 (64%) |

### Fichas de los jugadores destacados

#### CJ McCollum (bases/escoltas) vs Washington Wizards

- Minutos esperados: **27.5** (± 4.4); 90 partidos en la base.
- Su prop más probable hoy: **CJ McCollum: menos de 2.5 triples** (63%). Con 80% de probabilidad: más de 0.5 / menos de 3.5.
- Defensa de Washington Wizards contra bases/escoltas en triples: -2% respecto a la media; ajuste por su historial contra defensas similares: +2%.

**¿Por qué 2.0 triples?** (línea 2.5; 27.5 minutos esperados)

Razonamiento (6 factores a favor, 0 en contra):

- ✅ Minutos: 27.5 esperados (titular, ±4.4).
- ✅ Forma: 1.8 en sus últimos 5, 2.0 esta temporada (8 partidos), 2.2 la temporada pasada (línea 2.5).
- ➖ Cómo produce triples: 5.6 triples intentados (su ritmo 7.2 por 36'; el rival concede -2% de triples en su reparto) × 36% esperado.
- ✅ Defensa: el rival concede -3% de triples por minuto a bases/escoltas (defensa fuerte); ajuste aplicado -2%; en su zona principal (triple) el rival concede 34% (liga 35%).
- ✅ Altura: mide 6'3", 2.0 pulgadas menos que los bases/escoltas del rival (-0.7% en esta estadística).
- ➖ Ritmo del partido: +0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 2, 0 (2 de 2 a favor).
- ✅ Últimos 10: la habría pasado 8 de 10.

- Triples **2.0** (por componentes 2.0 · por tasa por minuto y defensa rival 2.0): 5.6 triples intentados (su ritmo 7.2 por 36'; el rival concede -2% de triples en su reparto) × 36% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 27.4 | 27.0 | 26.8 | 29.9 | 24.5 |
| Triples anotados | 1.8 | 1.7 | 2.0 | 2.5 | 1.0 |
| Triples intentados | 5.0 | 4.9 | 5.4 | 6.6 | 7.0 |
| % triples | 36.0% | 34.7% | 37.2% | 37.0% | 14.3% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -3%, vs defensa media +4%, vs defensa débil +2%; rebotes: vs defensa fuerte -10%, vs defensa media +5%, vs defensa débil +6%; asistencias: vs defensa fuerte -21%, vs defensa media +32%, vs defensa débil -3%; triples: vs defensa fuerte -2%, vs defensa media -13%, vs defensa débil +31%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 37% | 37% | 35% | 34% |
| pintura | 23% | 48% | 45% | 42% |
| media distancia | 17% | 45% | 41% | 42% |
| bajo el aro | 16% | 65% | 68% | 70% |
| triple de esquina | 6% | 38% | 38% | 40% |

#### Aaron Wiggins (bases/escoltas) vs Washington Wizards

- Minutos esperados: **24.6** (± 3.2); 84 partidos en la base.
- cambio de rol esta temporada (por minuto): tpm +58%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Aaron Wiggins: menos de 2.5 triples** (63%). Con 80% de probabilidad: más de 0.5 / menos de 3.5.
- Defensa de Washington Wizards contra bases/escoltas en triples: -2% respecto a la media; ajuste por su historial contra defensas similares: -1%.

**¿Por qué 2.0 triples?** (línea 2.5; 24.6 minutos esperados)

Razonamiento (2 factores a favor, 1 en contra):

- ❌ Minutos: 24.6 esperados (suplente, ±3.2).
- ✅ Forma: 2.2 en sus últimos 5, 2.6 esta temporada (8 partidos), 1.0 la temporada pasada (línea 2.5).
- ➖ Cómo produce triples: 5.6 triples intentados (su ritmo 8.0 por 36'; el rival concede -2% de triples en su reparto) × 36% esperado.
- ➖ Defensa: el rival concede -3% de triples por minuto a bases/escoltas (defensa fuerte); ajuste aplicado -2%; en su zona principal (triple) el rival concede 34% (liga 35%).
- ➖ Ritmo del partido: +0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 1, 0 (2 de 2 a favor).
- ➖ Últimos 10: la habría pasado 6 de 10.
- ⚠️ cambio de rol esta temporada (por minuto): tpm +58%; se da más peso a la línea de la casa.

- ⚠️ Alertas: suplente, cambio de rol.
- Triples **2.0** (por componentes 2.0 · por tasa por minuto y defensa rival 2.1): 5.6 triples intentados (su ritmo 8.0 por 36'; el rival concede -2% de triples en su reparto) × 36% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 24.4 | 21.3 | 25.6 | 19.6 | 22.5 |
| Triples anotados | 2.2 | 2.2 | 2.6 | 1.3 | 0.5 |
| Triples intentados | 6.6 | 5.3 | 6.5 | 3.7 | 3.5 |
| % triples | 33.3% | 41.5% | 40.4% | 34.8% | 14.3% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +3%, vs defensa media -9%, vs defensa débil +6%; rebotes: vs defensa fuerte -12%, vs defensa media +2%, vs defensa débil +16%; asistencias: vs defensa fuerte +12%, vs defensa media -18%, vs defensa débil +1%; triples: vs defensa fuerte +3%, vs defensa media -11%, vs defensa débil +14%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 35% | 35% | 35% | 34% |
| bajo el aro | 23% | 64% | 68% | 70% |
| pintura | 19% | 44% | 45% | 42% |
| triple de esquina | 16% | 40% | 38% | 40% |
| media distancia | 6% | 36% | 41% | 42% |

#### Trae Young (bases/escoltas) vs Atlanta Hawks

- Minutos esperados: **35.6** (± 3.0); 22 partidos en la base.
- Justin Champagnie ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- cambio de rol esta temporada (por minuto): reb +31%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Trae Young: menos de 2.5 triples** (62%). Con 80% de probabilidad: más de - / menos de 3.5.
- Defensa de Atlanta Hawks contra bases/escoltas en triples: -4% respecto a la media; ajuste por su historial contra defensas similares: -4%.

**¿Por qué 1.9 triples?** (línea 2.5; 35.6 minutos esperados)

Razonamiento (5 factores a favor, 0 en contra):

- ✅ Minutos: 35.6 esperados (titular, ±3.0).
- ✅ Forma: 1.8 en sus últimos 5, 1.9 esta temporada (7 partidos), 1.8 la temporada pasada (línea 2.5).
- ➖ Cómo produce triples: 6.6 triples intentados (su ritmo 6.9 por 36'; el rival concede -3% de triples en su reparto) × 31% esperado.
- ✅ Defensa: el rival concede -6% de triples por minuto a bases/escoltas (defensa fuerte); ajuste aplicado -4%; en su zona principal (triple) el rival concede 34% (liga 35%).
- ✅ Altura: mide 6'2", 2.6 pulgadas menos que los bases/escoltas del rival (-0.9% en esta estadística).
- ➖ Ritmo del partido: +0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Últimos 10: la habría pasado 7 de 10.
- ⚠️ Justin Champagnie ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ cambio de rol esta temporada (por minuto): reb +31%; se da más peso a la línea de la casa.

- Triples **1.9** (por componentes 2.0 · por tasa por minuto y defensa rival 1.9): 6.6 triples intentados (su ritmo 6.9 por 36'; el rival concede -3% de triples en su reparto) × 31% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 35.6 | 31.9 | 36.1 | 25.5 | - |
| Triples anotados | 1.8 | 1.8 | 1.9 | 1.8 | - |
| Triples intentados | 6.4 | 5.9 | 6.9 | 5.3 | - |
| % triples | 28.1% | 30.5% | 27.1% | 33.8% | - |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -26%, vs defensa media +15%, vs defensa débil +13%; rebotes: vs defensa fuerte +13%, vs defensa media +3%, vs defensa débil -18%; asistencias: vs defensa fuerte -13%, vs defensa media -7%, vs defensa débil +17%; triples: vs defensa fuerte -40%, vs defensa media -24%, vs defensa débil +45%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 43% | 31% | 35% | 34% |
| pintura | 24% | 52% | 45% | 44% |
| media distancia | 15% | 39% | 41% | 42% |
| bajo el aro | 14% | 67% | 68% | 67% |
| triple de esquina | 5% | 40% | 38% | 37% |

#### Dyson Daniels (bases/escoltas) vs Washington Wizards

- Minutos esperados: **29.2** (± 3.0); 90 partidos en la base.
- Su prop más probable hoy: **Dyson Daniels: menos de 0.5 triples** (61%). Con 80% de probabilidad: más de - / menos de 1.5.
- Defensa de Washington Wizards contra bases/escoltas en triples: -2% respecto a la media; ajuste por su historial contra defensas similares: -10%.

**¿Por qué 0.5 triples?** (línea 0.5; 29.2 minutos esperados)

Razonamiento (3 factores a favor, 1 en contra):

- ✅ Minutos: 29.2 esperados (titular, ±3.0).
- ✅ Forma: 0.0 en sus últimos 5, 0.1 esta temporada (8 partidos), 0.3 la temporada pasada (línea 0.5).
- ➖ Cómo produce triples: 2.2 triples intentados (su ritmo 2.7 por 36'; el rival concede -2% de triples en su reparto) × 25% esperado.
- ➖ Defensa: el rival concede -3% de triples por minuto a bases/escoltas (defensa fuerte); ajuste aplicado -2%; en su zona principal (triple) el rival concede 34% (liga 35%).
- ❌ Altura: mide 6'7", 2.0 pulgadas más que los bases/escoltas del rival (+0.7% en esta estadística).
- ➖ Ritmo del partido: +0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ➖ Contra este rival: 1, 0, 0, 1 (2 de 4 a favor).
- ✅ Últimos 10: la habría pasado 7 de 10.

- Triples **0.5** (por componentes 0.6 · por tasa por minuto y defensa rival 0.4): 2.2 triples intentados (su ritmo 2.7 por 36'; el rival concede -2% de triples en su reparto) × 25% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 29.2 | 27.3 | 29.1 | 32.8 | 31.2 |
| Triples anotados | 0.0 | 0.4 | 0.1 | 0.3 | 0.5 |
| Triples intentados | 1.2 | 1.7 | 1.2 | 1.6 | 3.2 |
| % triples | 0.0% | 23.5% | 10.0% | 19.8% | 15.4% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +2%, vs defensa media +1%, vs defensa débil -5%; rebotes: vs defensa fuerte -3%, vs defensa media -2%, vs defensa débil +6%; asistencias: vs defensa fuerte -8%, vs defensa media +3%, vs defensa débil +9%; triples: vs defensa fuerte -21%, vs defensa media +39%, vs defensa débil -34%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 45% | 68% | 68% | 70% |
| pintura | 37% | 44% | 45% | 42% |
| triple frontal | 11% | 23% | 35% | 34% |
| triple de esquina | 5% | 30% | 38% | 40% |
| media distancia | 2% | 38% | 41% | 42% |

#### Tre Johnson (bases/escoltas) vs Atlanta Hawks

- Minutos esperados: **20.6** (± 4.3); 66 partidos en la base.
- sin Justin Champagnie (11 partidos): 21.0 min vs 24.2 con él; pts +6%/min, reb +13%/min, ast -9%/min
- cambio de rol esta temporada (por minuto): ast -63%, tpm -31%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Tre Johnson: menos de 1.5 triples** (60%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Atlanta Hawks contra bases/escoltas en triples: -4% respecto a la media; ajuste por su historial contra defensas similares: -4%.

**¿Por qué 1.4 triples?** (línea 1.5; 20.6 minutos esperados)

Razonamiento (3 factores a favor, 1 en contra):

- ❌ Minutos: 20.6 esperados (suplente, ±4.3).
- ✅ Forma: 1.4 en sus últimos 5, 1.2 esta temporada (6 partidos), 1.9 la temporada pasada (línea 1.5).
- ➖ Cómo produce triples: 4.6 triples intentados (su ritmo 7.4 por 36'; el rival concede -3% de triples en su reparto) × 34% esperado.
- ✅ Defensa: el rival concede -6% de triples por minuto a bases/escoltas (defensa fuerte); ajuste aplicado -4%; en su zona principal (triple) el rival concede 34% (liga 35%).
- ➖ Ritmo del partido: +0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ➖ Contra este rival: 2, 0 (1 de 2 a favor).
- ✅ Últimos 10: la habría pasado 7 de 10.
- ⚠️ sin Justin Champagnie (11 partidos): 21.0 min vs 24.2 con él; pts +6%/min, reb +13%/min, ast -9%/min.
- ⚠️ cambio de rol esta temporada (por minuto): ast -63%, tpm -31%; se da más peso a la línea de la casa.

- ⚠️ Alertas: suplente, cambio de rol.
- Triples **1.4** (por componentes 1.6 · por tasa por minuto y defensa rival 1.4): 4.6 triples intentados (su ritmo 7.4 por 36'; el rival concede -3% de triples en su reparto) × 34% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 21.4 | 22.0 | 21.0 | 24.0 | 22.0 |
| Triples anotados | 1.4 | 1.2 | 1.2 | 1.9 | 1.0 |
| Triples intentados | 4.8 | 4.7 | 4.3 | 5.3 | 3.5 |
| % triples | 29.2% | 25.5% | 26.9% | 35.8% | 28.6% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -8%, vs defensa media -10%, vs defensa débil +18%; rebotes: vs defensa fuerte -10%, vs defensa media -4%, vs defensa débil +14%; asistencias: vs defensa fuerte -15%, vs defensa media +17%, vs defensa débil -3%; triples: vs defensa fuerte -17%, vs defensa media -2%, vs defensa débil +34%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 39% | 33% | 35% | 34% |
| pintura | 24% | 44% | 45% | 44% |
| media distancia | 16% | 48% | 41% | 42% |
| triple de esquina | 10% | 40% | 38% | 37% |
| bajo el aro | 10% | 65% | 68% | 67% |

## Milwaukee Bucks @ Boston Celtics

Diferencia esperada: Boston Celtics por 11.5 — algo desigual: titulares hasta -1.5% de minutos.

Parte de lesiones: Jayson Tatum (Day-To-Day); Payton Pritchard (Day-To-Day); Devin Carter (Out).

Ventajas del partido (los dos lados): puntos esperados frente a su media de los últimos 10, ajuste por la defensa rival y diferencia de estatura con los rivales de su posición.

| Equipo | Jugador | Puntos esperados | Su media (últ. 10) | Defensa rival en puntos | Rebotes esperados | Altura vs rival |
|---|---|---|---|---|---|---|
| BOS | Jayson Tatum | 23.3 | 26.0 | +1% | 7.7 | +0.3" |
| BOS | Paul George | 17.9 | 18.2 | +1% | 5.5 | +0.3" |
| BOS | Derrick White | 12.1 | 12.1 | +3% | 3.5 | -0.3" |
| MIL | Tyler Herro | 18.1 | 19.6 | -4% | 4.4 | +0.5" |
| BOS | Payton Pritchard | 14.1 | 13.3 | +3% | 3.4 | -2.3" |
| MIL | Jaime Jaquez Jr. | 14.5 | 17.8 | -3% | 5.6 | -2.0" |
| MIL | Myles Turner | 9.8 | 9.2 | -2% | 5.3 | -0.4" |
| MIL | Kyle Kuzma | 10.4 | 9.6 | -3% | 5.0 | -0.0" |
| MIL | Ryan Rollins | 11.8 | 14.8 | -4% | 3.7 | -1.5" |
| BOS | Neemias Queta | 10.5 | 9.8 | +1% | 6.7 | +1.0" |

Picks seguros de titulares estables:

| Jugador | Pick seguro | Prob. | Cuota mínima | Esperado | Últ. 10 |
|---|---|---|---|---|---|
| Jayson Tatum | **más de 2.5 asistencias** | **91%** | 1.10 | 6.4 | 10/10 |
| Paul George | **más de 8.5 puntos** | **87%** | 1.15 | 17.9 | 9/10 |
| Jayson Tatum | **más de 3.5 rebotes** | **86%** | 1.16 | 7.7 | 10/10 |
| Jayson Tatum | **más de 27.5 pts+reb+ast** | **86%** | 1.16 | 37.3 | 10/10 |
| Paul George | **más de 16.5 pts+reb+ast** | **86%** | 1.16 | 27.6 | 9/10 |
| Jayson Tatum | **más de 14.5 puntos** | **86%** | 1.17 | 23.3 | 9/10 |

Las 8 más probables (máximo 2 por jugador: las de un mismo jugador suelen ganar o perder juntas).

| Prop | Prob. final | Modelo | Casa | Esperado | Últ. 10 | Temporada | vs este rival | Cuota (implícita) |
|---|---|---|---|---|---|---|---|---|
| **Jaime Jaquez Jr.: más de 0.5 triples** | **69%** | 74% | 65% | 1.4 ± 1.2 | 9/10 | 6/7 | 2, 1, 1 | 1.45 (69%) |
| **Kyle Kuzma: más de 0.5 triples** | **65%** | 65% | 65% | 1.4 ± 1.4 | 6/10 | 4/7 | 2, 2, 1 | 1.43 (70%) |
| **Derrick White: menos de 16.5 puntos** | **63%** | 79% | 51% | 12.1 ± 5.2 | 8/10 | 6/7 | 17, 18, 17, 11 | 1.83 (55%) |
| **Derrick White: menos de 2.5 triples** | **63%** | 68% | 60% | 1.9 ± 1.4 | 7/10 | 6/7 | 5, 4, 3, 2 | 1.56 (64%) |
| **AJ Green: más de 1.5 triples** ⚠️ suplente | **62%** | 67% | 58% | 2.2 ± 1.5 | 8/10 | 5/7 | 5, 0, 1 | 1.62 (62%) |
| **Tyler Herro: menos de 4.5 asistencias** | **62%** | 68% | 57% | 3.4 ± 2.2 | 6/10 | 5/7 | 7, 3 | 1.62 (62%) |
| **Kel'el Ware: más de 0.5 triples** ⚠️ suplente | **61%** | 63% | 59% | 1.1 ± 1.1 | 6/10 | 3/7 | 2, 0, 1, 6 | 1.59 (63%) |
| **Jayson Tatum: menos de 7.5 asistencias** | **60%** | 65% | 56% | 6.4 ± 2.6 | 6/10 | 4/7 | 9 | 1.67 (60%) |

### Fichas de los jugadores destacados

#### Jaime Jaquez Jr. (aleros/ala-pívots) vs Boston Celtics

- Minutos esperados: **27.3** (± 3.5); 83 partidos en la base.
- cambio de rol esta temporada (por minuto): reb +48%, ast -39%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Jaime Jaquez Jr.: más de 0.5 triples** (69%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Boston Celtics contra aleros/ala-pívots en triples: +5% respecto a la media; ajuste por su historial contra defensas similares: -0%.

**¿Por qué 1.4 triples?** (línea 0.5; 27.3 minutos esperados)

Razonamiento (5 factores a favor, 1 en contra):

- ✅ Minutos: 27.3 esperados (titular, ±3.5).
- ✅ Forma: 1.6 en sus últimos 5, 1.6 esta temporada (7 partidos), 0.9 la temporada pasada (línea 0.5).
- ➖ Cómo produce triples: 3.7 triples intentados (su ritmo 4.6 por 36'; el rival concede +9% de triples en su reparto) × 34% esperado.
- ✅ Defensa: el rival concede +12% de triples por minuto a aleros/ala-pívots (defensa débil); ajuste aplicado +5%; en su zona principal (triple) el rival concede 36% (liga 35%).
- ❌ Altura: mide 6'6", 2.0 pulgadas menos que los aleros/ala-pívots del rival (-0.7% en esta estadística).
- ➖ Ritmo del partido: +1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 2, 1, 1 (3 de 3 a favor).
- ✅ Últimos 10: la habría pasado 9 de 10.
- ⚠️ cambio de rol esta temporada (por minuto): reb +48%, ast -39%; se da más peso a la línea de la casa.

- Triples **1.4** (por componentes 1.3 · por tasa por minuto y defensa rival 1.4): 3.7 triples intentados (su ritmo 4.6 por 36'; el rival concede +9% de triples en su reparto) × 34% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 26.0 | 29.9 | 28.0 | 28.5 | 32.3 |
| Triples anotados | 1.6 | 1.7 | 1.6 | 0.8 | 1.3 |
| Triples intentados | 3.8 | 3.8 | 3.6 | 2.5 | 4.3 |
| % triples | 42.1% | 44.7% | 44.0% | 31.7% | 30.8% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -16%, vs defensa media +7%, vs defensa débil +7%; rebotes: vs defensa fuerte -12%, vs defensa media +5%, vs defensa débil +9%; asistencias: vs defensa fuerte -14%, vs defensa media +2%, vs defensa débil +13%; triples: vs defensa fuerte -20%, vs defensa media -5%, vs defensa débil +25%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| pintura | 38% | 43% | 45% | 43% |
| bajo el aro | 33% | 69% | 68% | 67% |
| triple frontal | 14% | 32% | 35% | 36% |
| triple de esquina | 8% | 40% | 38% | 36% |
| media distancia | 7% | 49% | 41% | 42% |

#### Kyle Kuzma (aleros/ala-pívots) vs Boston Celtics

- Minutos esperados: **24.8** (± 5.0); 76 partidos en la base.
- cambio de rol esta temporada (por minuto): reb +41%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Kyle Kuzma: más de 0.5 triples** (65%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Boston Celtics contra aleros/ala-pívots en triples: +6% respecto a la media; ajuste por su historial contra defensas similares: +4%.

**¿Por qué 1.4 triples?** (línea 0.5; 24.8 minutos esperados)

Razonamiento (4 factores a favor, 0 en contra):

- ✅ Minutos: 24.8 esperados (titular, ±5.0).
- ✅ Forma: 1.2 en sus últimos 5, 1.3 esta temporada (7 partidos), 1.2 la temporada pasada (línea 0.5).
- ➖ Cómo produce triples: 4.2 triples intentados (su ritmo 5.7 por 36'; el rival concede +9% de triples en su reparto) × 34% esperado.
- ✅ Defensa: el rival concede +12% de triples por minuto a aleros/ala-pívots (defensa débil); ajuste aplicado +6%; en su zona principal (triple) el rival concede 36% (liga 35%).
- ➖ Ritmo del partido: +1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 2, 2, 1 (3 de 3 a favor).
- ➖ Últimos 10: la habría pasado 6 de 10.
- ⚠️ cambio de rol esta temporada (por minuto): reb +41%; se da más peso a la línea de la casa.

- Triples **1.4** (por componentes 1.4 · por tasa por minuto y defensa rival 1.4): 4.2 triples intentados (su ritmo 5.7 por 36'; el rival concede +9% de triples en su reparto) × 34% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 25.4 | 25.2 | 26.3 | 26.2 | 30.0 |
| Triples anotados | 1.2 | 1.2 | 1.3 | 1.2 | 1.7 |
| Triples intentados | 4.4 | 3.7 | 4.4 | 3.5 | 3.7 |
| % triples | 27.3% | 32.4% | 29.0% | 34.7% | 45.5% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +6%, vs defensa media -9%, vs defensa débil +5%; rebotes: vs defensa fuerte -3%, vs defensa media -10%, vs defensa débil +8%; asistencias: vs defensa fuerte -27%, vs defensa media -12%, vs defensa débil +40%; triples: vs defensa fuerte +8%, vs defensa media -39%, vs defensa débil +31%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 35% | 69% | 68% | 67% |
| triple frontal | 23% | 32% | 35% | 36% |
| pintura | 22% | 42% | 45% | 43% |
| triple de esquina | 14% | 37% | 38% | 36% |
| media distancia | 6% | 43% | 41% | 42% |

#### Derrick White (bases/escoltas) vs Milwaukee Bucks

- Minutos esperados: **29.4** (± 5.2); 91 partidos en la base.
- cambio de rol esta temporada (por minuto): tpm -33%; se da más peso a la línea de la casa
- partido desigual (favorito por 11.5): los titulares suelen jugar -3% de minutos si se rompe
- Su prop más probable hoy: **Derrick White: menos de 16.5 puntos** (63%). Con 80% de probabilidad: más de 7.5 / menos de 16.5.
- Defensa de Milwaukee Bucks contra bases/escoltas en puntos: +3% respecto a la media; ajuste por su historial contra defensas similares: +0%.

**¿Por qué 12.1 puntos?** (línea 16.5; 29.4 minutos esperados)

Razonamiento (3 factores a favor, 2 en contra):

- ✅ Minutos: 29.4 esperados (titular, ±5.2).
- ✅ Forma: 9.8 en sus últimos 5, 11.1 esta temporada (7 partidos), 15.5 la temporada pasada (línea 16.5).
- ➖ Cómo produce puntos: 10.4 tiros de campo (su ritmo 12.5 por 36'; el rival concede +0% de tiros) × 0.99 puntos por tiro [triple frontal 50% de sus tiros al 32% (rival concede 36%, liga 35%); pintura 21% de sus tiros al 43% (rival concede 42%, liga 45%); media distancia 12% de sus tiros al 42% (rival concede 42%, liga 41%)] + 1.8 tiros libres × 85%.
- ❌ Defensa: el rival concede +5% de puntos por minuto a bases/escoltas (defensa débil); ajuste aplicado +3%; en su zona principal (triple) el rival concede 36% (liga 35%).
- ➖ Ritmo del partido: +1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ❌ Contra este rival: 17, 18, 17, 11 (1 de 4 a favor).
- ✅ Últimos 10: la habría pasado 8 de 10.
- ⚠️ cambio de rol esta temporada (por minuto): tpm -33%; se da más peso a la línea de la casa.
- ⚠️ partido desigual (favorito por 11.5): los titulares suelen jugar -3% de minutos si se rompe.

- ⚠️ Alertas: muy lejos de la casa.
- Puntos **12.1** (por componentes 11.9 · por tasa por minuto y defensa rival 12.3): 10.4 tiros de campo (su ritmo 12.5 por 36'; el rival concede +0% de tiros) × 0.99 puntos por tiro [triple frontal 50% de sus tiros al 32% (rival concede 36%, liga 35%); pintura 21% de sus tiros al 43% (rival concede 42%, liga 45%); media distancia 12% de sus tiros al 42% (rival concede 42%, liga 41%)] + 1.8 tiros libres × 85%.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 28.2 | 32.3 | 30.0 | 34.2 | 31.5 |
| Puntos | 9.8 | 12.1 | 11.1 | 16.0 | 15.8 |
| Tiros de campo intentados | 9.0 | 11.1 | 9.9 | 14.2 | 13.8 |
| % tiros de campo | 40.0% | 39.6% | 43.5% | 38.9% | 36.4% |
| Triples intentados | 4.2 | 6.0 | 4.9 | 8.3 | 9.2 |
| % triples | 28.6% | 31.7% | 32.4% | 32.2% | 37.8% |
| Tiros libres intentados | 1.4 | 1.5 | 1.0 | 2.6 | 2.2 |
| % tiros libres | 100.0% | 93.3% | 100.0% | 89.9% | 100.0% |
| Jugadas que usa por 36 min | 15.9 | 15.6 | 15.6 | 17.9 | 19.1 |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -5%, vs defensa media +1%, vs defensa débil +5%; rebotes: vs defensa fuerte -5%, vs defensa media +20%, vs defensa débil -8%; asistencias: vs defensa fuerte -12%, vs defensa media -12%, vs defensa débil +27%; triples: vs defensa fuerte -7%, vs defensa media +5%, vs defensa débil +6%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 50% | 32% | 35% | 36% |
| pintura | 21% | 43% | 45% | 42% |
| media distancia | 12% | 42% | 41% | 42% |
| bajo el aro | 10% | 71% | 68% | 70% |
| triple de esquina | 7% | 37% | 38% | 40% |

#### AJ Green (bases/escoltas) vs Boston Celtics

- Minutos esperados: **22.0** (± 3.6); 85 partidos en la base.
- partido desigual (no favorito por 11.5): los suplentes suelen jugar +3% de minutos si se rompe
- Su prop más probable hoy: **AJ Green: más de 1.5 triples** (62%). Con 80% de probabilidad: más de 0.5 / menos de 3.5.
- Defensa de Boston Celtics contra bases/escoltas en triples: -1% respecto a la media; ajuste por su historial contra defensas similares: -0%.

**¿Por qué 2.2 triples?** (línea 1.5; 22.0 minutos esperados)

Razonamiento (2 factores a favor, 2 en contra):

- ❌ Minutos: 22.0 esperados (suplente, ±3.6).
- ✅ Forma: 2.2 en sus últimos 5, 2.3 esta temporada (7 partidos), 3.0 la temporada pasada (línea 1.5).
- ➖ Cómo produce triples: 5.4 triples intentados (su ritmo 8.4 por 36'; el rival concede +9% de triples en su reparto) × 41% esperado.
- ➖ Defensa: el rival concede -1% de triples por minuto a bases/escoltas (defensa media); ajuste aplicado -1%; en su zona principal (triple) el rival concede 36% (liga 35%).
- ➖ Ritmo del partido: +1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ❌ Contra este rival: 5, 0, 1 (1 de 3 a favor).
- ✅ Últimos 10: la habría pasado 8 de 10.
- ⚠️ partido desigual (no favorito por 11.5): los suplentes suelen jugar +3% de minutos si se rompe.

- ⚠️ Alertas: suplente.
- Triples **2.2** (por componentes 2.3 · por tasa por minuto y defensa rival 2.3): 5.4 triples intentados (su ritmo 8.4 por 36'; el rival concede +9% de triples en su reparto) × 41% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 21.4 | 24.6 | 19.9 | 29.1 | 26.0 |
| Triples anotados | 2.2 | 3.6 | 2.3 | 3.0 | 2.0 |
| Triples intentados | 5.2 | 7.2 | 4.9 | 7.1 | 5.7 |
| % triples | 42.3% | 50.0% | 47.1% | 41.9% | 35.3% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +6%, vs defensa media -4%, vs defensa débil -6%; rebotes: vs defensa fuerte -11%, vs defensa media +6%, vs defensa débil +8%; asistencias: vs defensa fuerte -12%, vs defensa media -9%, vs defensa débil +24%; triples: vs defensa fuerte -8%, vs defensa media +10%, vs defensa débil +1%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 64% | 40% | 35% | 36% |
| triple de esquina | 25% | 45% | 38% | 36% |
| media distancia | 4% | 38% | 41% | 42% |
| pintura | 3% | 49% | 45% | 43% |
| bajo el aro | 3% | 65% | 68% | 67% |

#### Tyler Herro (bases/escoltas) vs Boston Celtics

- Minutos esperados: **29.1** (± 3.0); 41 partidos en la base.
- cambio de rol esta temporada (por minuto): tpm +44%; se da más peso a la línea de la casa
- partido desigual (no favorito por 11.5): los titulares suelen jugar -3% de minutos si se rompe
- Su prop más probable hoy: **Tyler Herro: menos de 4.5 asistencias** (62%). Con 80% de probabilidad: más de 0.5 / menos de 5.5.
- Defensa de Boston Celtics contra bases/escoltas en asistencias: -5% respecto a la media; ajuste por su historial contra defensas similares: -4%.

**¿Por qué 3.4 asistencias?** (línea 4.5; 29.1 minutos esperados)

Razonamiento (3 factores a favor, 0 en contra):

- ✅ Minutos: 29.1 esperados (titular, ±3.0).
- ✅ Forma: 3.0 en sus últimos 5, 4.0 esta temporada (7 partidos), 4.2 la temporada pasada (línea 4.5).
- ➖ Cómo produce asistencias: asiste el 18.5% de las canastas de sus compañeros en pista × 16.0 canastas de compañeros esperadas (su equipo 37.4 por 48' contra esta defensa).
- ✅ Defensa: el rival concede -5% de asistencias por minuto a bases/escoltas (defensa fuerte); ajuste aplicado -5%.
- ➖ Ritmo del partido: +1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ➖ Contra este rival: 7, 3 (1 de 2 a favor).
- ➖ Últimos 10: la habría pasado 6 de 10.
- ⚠️ cambio de rol esta temporada (por minuto): tpm +44%; se da más peso a la línea de la casa.
- ⚠️ partido desigual (no favorito por 11.5): los titulares suelen jugar -3% de minutos si se rompe.

- Asistencias **3.4** (por componentes 3.0 · por tasa por minuto y defensa rival 3.5): asiste el 18.5% de las canastas de sus compañeros en pista × 16.0 canastas de compañeros esperadas (su equipo 37.4 por 48' contra esta defensa).

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 29.6 | 29.6 | 30.3 | 31.3 | 35.5 |
| Asistencias | 3.0 | 4.6 | 4.0 | 4.2 | 5.0 |
| % de las canastas de compañeros que asiste | 14.8% | 20.8% | 19.3% | 18.0% | 19.3% |
| Pérdidas por jugada | 11.7% | 11.2% | 10.8% | 10.2% | 11.2% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -0%, vs defensa media -1%, vs defensa débil +2%; rebotes: vs defensa fuerte -5%, vs defensa media -14%, vs defensa débil +13%; asistencias: vs defensa fuerte -20%, vs defensa media +19%, vs defensa débil +3%; triples: vs defensa fuerte -2%, vs defensa media -3%, vs defensa débil +15%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 39% | 40% | 35% | 36% |
| pintura | 30% | 52% | 45% | 43% |
| bajo el aro | 15% | 66% | 68% | 67% |
| media distancia | 11% | 36% | 41% | 42% |
| triple de esquina | 5% | 36% | 38% | 36% |

## Charlotte Hornets @ Brooklyn Nets

Diferencia esperada: Charlotte Hornets por 3.5.

Parte de lesiones: Grant Williams (Out); Coby White (Day-To-Day); Kon Knueppel (Out); Tyler Bilodeau (Out); Egor Demin (Out).

Ventajas del partido (los dos lados): puntos esperados frente a su media de los últimos 10, ajuste por la defensa rival y diferencia de estatura con los rivales de su posición.

| Equipo | Jugador | Puntos esperados | Su media (últ. 10) | Defensa rival en puntos | Rebotes esperados | Altura vs rival |
|---|---|---|---|---|---|---|
| BKN | Julius Randle | 19.7 | 17.8 | -0% | 6.9 | +0.9" |
| CHA | Brandon Miller | 22.3 | 22.5 | +2% | 5.6 | -1.9" |
| BKN | Michael Porter Jr. | 21.0 | 22.1 | +0% | 6.6 | +1.9" |
| CHA | Dennis Schroder | 11.3 | 9.4 | +0% | 3.3 | -3.7" |
| CHA | Naz Reid | 15.3 | 15.4 | +4% | 7.8 | -1.5" |
| CHA | Moussa Diabate | 9.6 | 8.3 | +2% | 8.7 | +1.1" |
| CHA | Grayson Allen | 13.9 | 13.8 | +1% | 2.9 | -1.7" |
| BKN | Chaney Johnson | 8.3 | 7.1 | +0% | 3.9 | -0.1" |
| BKN | Nolan Traore | 11.0 | 12.2 | -3% | 2.3 | -0.5" |
| BKN | Keon Ellis | 6.5 | 4.2 | -2% | 2.1 | +0.5" |

Picks seguros de titulares estables:

| Jugador | Pick seguro | Prob. | Cuota mínima | Esperado | Últ. 10 |
|---|---|---|---|---|---|
| Brandon Miller | **más de 17.5 pts+reb+ast** | **87%** | 1.15 | 30.8 | 9/10 |
| Julius Randle | **más de 3.5 rebotes** | **87%** | 1.15 | 6.9 | 10/10 |
| Michael Porter Jr. | **más de 12.5 puntos** | **87%** | 1.15 | 21.0 | 9/10 |
| Michael Porter Jr. | **más de 18.5 pts+reb+ast** | **86%** | 1.16 | 29.7 | 9/10 |
| Julius Randle | **más de 11.5 puntos** | **86%** | 1.16 | 19.7 | 8/10 |
| Julius Randle | **más de 19.5 pts+reb+ast** | **86%** | 1.17 | 30.8 | 9/10 |

Las 8 más probables (máximo 2 por jugador: las de un mismo jugador suelen ganar o perder juntas).

| Prop | Prob. final | Modelo | Casa | Esperado | Últ. 10 | Temporada | vs este rival | Cuota (implícita) |
|---|---|---|---|---|---|---|---|---|
| **Naz Reid: menos de 2.5 asistencias** | **65%** | 70% | 61% | 1.9 ± 1.8 | 9/10 | 7/8 | 7, 1, 2 | 1.53 (65%) |
| **Moussa Diabate: más de 1.5 asistencias** | **63%** | 65% | 61% | 2.3 ± 1.6 | 7/10 | 6/8 | 3, 1, 1, 0 | 1.54 (65%) |
| **Noah Clowney: más de 0.5 triples** ⚠️ suplente | **62%** | 60% | 64% | 1.0 ± 1.1 | 5/10 | 4/7 | 1, 0, 2, 1 | 1.47 (68%) |
| **Day'Ron Sharpe: menos de 2.5 asistencias** | **62%** | 63% | 61% | 2.0 ± 1.4 | 6/10 | 4/7 | 3, 3, 0 | 1.54 (65%) |
| **Naz Reid: menos de 2.5 triples** | **61%** | 64% | 58% | 2.0 ± 1.5 | 5/10 | 5/8 | 4, 3, 4 | 1.62 (62%) |
| **Nolan Traore: menos de 2.5 rebotes** | **61%** | 61% | 60% | 2.3 ± 1.6 | 8/10 | 6/7 | 2, 5, 0 | 1.54 (65%) |
| **Dennis Schroder: más de 3.5 asistencias** | **60%** | 64% | 57% | 4.9 ± 2.4 | 7/10 | 6/8 | 6, 5, 3 | 1.64 (61%) |
| **Michael Porter Jr.: más de 2.5 triples** | **59%** | 61% | 58% | 3.3 ± 1.9 | 7/10 | 5/7 | 5, 7, 2 | 1.62 (62%) |

### Fichas de los jugadores destacados

#### Naz Reid (pívots) vs Brooklyn Nets

- Minutos esperados: **28.8** (± 7.0); 96 partidos en la base.
- Grant Williams ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Kon Knueppel ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Su prop más probable hoy: **Naz Reid: menos de 2.5 asistencias** (65%). Con 80% de probabilidad: más de - / menos de 3.5.
- Defensa de Brooklyn Nets contra pívots en asistencias: -6% respecto a la media; ajuste por su historial contra defensas similares: +1%.

**¿Por qué 1.9 asistencias?** (línea 2.5; 28.8 minutos esperados)

Razonamiento (5 factores a favor, 1 en contra):

- ❌ Minutos: 28.8 esperados (titular, ±7.0).
- ✅ Forma: 1.2 en sus últimos 5, 1.9 esta temporada (8 partidos), 2.0 la temporada pasada (línea 2.5).
- ➖ Cómo produce asistencias: asiste el 10.3% de las canastas de sus compañeros en pista × 18.3 canastas de compañeros esperadas (su equipo 39.8 por 48' contra esta defensa).
- ✅ Defensa: el rival concede -6% de asistencias por minuto a pívots (defensa fuerte); ajuste aplicado -6%.
- ✅ Ritmo del partido: -2% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 7, 1, 2 (2 de 3 a favor).
- ✅ Últimos 10: la habría pasado 9 de 10.
- ⚠️ Grant Williams ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ Kon Knueppel ya no jugó en sus últimos partidos: la baja ya está en sus minutos.

- ⚠️ Alertas: minutos inestables.
- Asistencias **1.9** (por componentes 1.9 · por tasa por minuto y defensa rival 1.9): asiste el 10.3% de las canastas de sus compañeros en pista × 18.3 canastas de compañeros esperadas (su equipo 39.8 por 48' contra esta defensa).

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 27.2 | 29.4 | 28.9 | 26.1 | 28.7 |
| Asistencias | 1.2 | 1.8 | 1.9 | 2.2 | 3.3 |
| % de las canastas de compañeros que asiste | 7.0% | 9.9% | 10.5% | 10.9% | 16.5% |
| Pérdidas por jugada | 14.7% | 12.7% | 14.8% | 11.9% | 6.7% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -5%, vs defensa media -5%, vs defensa débil +9%; rebotes: vs defensa fuerte -1%, vs defensa media -2%, vs defensa débil +3%; asistencias: vs defensa fuerte -11%, vs defensa media -13%, vs defensa débil +19%; triples: vs defensa fuerte +5%, vs defensa media -3%, vs defensa débil -0%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 34% | 33% | 35% | 36% |
| pintura | 26% | 45% | 45% | 46% |
| bajo el aro | 19% | 68% | 68% | 69% |
| triple de esquina | 16% | 42% | 38% | 40% |
| media distancia | 5% | 39% | 41% | 41% |

#### Moussa Diabate (aleros/ala-pívots) vs Brooklyn Nets

- Minutos esperados: **28.4** (± 4.9); 83 partidos en la base.
- Grant Williams ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Kon Knueppel ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Su prop más probable hoy: **Moussa Diabate: más de 1.5 asistencias** (63%). Con 80% de probabilidad: más de 0.5 / menos de 3.5.
- Defensa de Brooklyn Nets contra aleros/ala-pívots en asistencias: +5% respecto a la media; ajuste por su historial contra defensas similares: -2%.

**¿Por qué 2.3 asistencias?** (línea 1.5; 28.4 minutos esperados)

Razonamiento (4 factores a favor, 2 en contra):

- ✅ Minutos: 28.4 esperados (titular, ±4.9).
- ✅ Forma: 2.2 en sus últimos 5, 2.1 esta temporada (8 partidos), 2.1 la temporada pasada (línea 1.5).
- ➖ Cómo produce asistencias: asiste el 11.1% de las canastas de sus compañeros en pista × 19.5 canastas de compañeros esperadas (su equipo 39.8 por 48' contra esta defensa).
- ✅ Defensa: el rival concede +5% de asistencias por minuto a aleros/ala-pívots (defensa débil); ajuste aplicado +5%.
- ❌ Ritmo del partido: -2% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ❌ Contra este rival: 3, 1, 1, 0 (1 de 4 a favor).
- ✅ Últimos 10: la habría pasado 7 de 10.
- ⚠️ Grant Williams ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ Kon Knueppel ya no jugó en sus últimos partidos: la baja ya está en sus minutos.

- Asistencias **2.3** (por componentes 2.2 · por tasa por minuto y defensa rival 2.3): asiste el 11.1% de las canastas de sus compañeros en pista × 19.5 canastas de compañeros esperadas (su equipo 39.8 por 48' contra esta defensa).

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 30.6 | 28.4 | 28.8 | 26.1 | 26.0 |
| Asistencias | 2.2 | 2.0 | 2.1 | 1.9 | 1.2 |
| % de las canastas de compañeros que asiste | 11.3% | 10.4% | 11.3% | 9.4% | 6.4% |
| Pérdidas por jugada | 18.2% | 20.2% | 20.5% | 14.3% | 17.8% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -19%, vs defensa media +3%, vs defensa débil +14%; rebotes: vs defensa fuerte -13%, vs defensa media -7%, vs defensa débil +13%; asistencias: vs defensa fuerte +26%, vs defensa media -4%, vs defensa débil -23%; triples: vs defensa fuerte -100%, vs defensa media +183%, vs defensa débil -100%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 74% | 72% | 68% | 69% |
| pintura | 23% | 38% | 45% | 46% |
| media distancia | 2% | 41% | 41% | 41% |
| triple frontal | 1% | 34% | 35% | 36% |
| triple de esquina | 0% | 39% | 38% | 40% |

#### Noah Clowney (aleros/ala-pívots) vs Charlotte Hornets

- Minutos esperados: **21.8** (± 3.0); 73 partidos en la base.
- Egor Demin ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- cambio de rol esta temporada (por minuto): pts -45%, reb +42%, ast -35%, tpm -64%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Noah Clowney: más de 0.5 triples** (62%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Charlotte Hornets contra aleros/ala-pívots en triples: +4% respecto a la media; ajuste por su historial contra defensas similares: +1%.

**¿Por qué 1.0 triples?** (línea 0.5; 21.8 minutos esperados)

Razonamiento (3 factores a favor, 3 en contra):

- ❌ Minutos: 21.8 esperados (suplente, ±3.0).
- ❌ Forma: 0.4 en sus últimos 5, 0.6 esta temporada (7 partidos), 2.1 la temporada pasada (línea 0.5).
- ➖ Cómo produce triples: 3.0 triples intentados (su ritmo 5.2 por 36'; el rival concede -3% de triples en su reparto) × 33% esperado.
- ✅ Defensa: el rival concede +7% de triples por minuto a aleros/ala-pívots (defensa débil); ajuste aplicado +4%; en su zona principal (triple) el rival concede 36% (liga 35%).
- ✅ Altura: mide 6'10", 1.9 pulgadas más que los aleros/ala-pívots del rival (+0.7% en esta estadística).
- ❌ Ritmo del partido: -2% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 1, 0, 2, 1 (3 de 4 a favor).
- ➖ Últimos 10: la habría pasado 5 de 10.
- ⚠️ Egor Demin ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ cambio de rol esta temporada (por minuto): pts -45%, reb +42%, ast -35%, tpm -64%; se da más peso a la línea de la casa.

- ⚠️ Alertas: suplente, cambio de rol.
- Triples **1.0** (por componentes 1.0 · por tasa por minuto y defensa rival 1.0): 3.0 triples intentados (su ritmo 5.2 por 36'; el rival concede -3% de triples en su reparto) × 33% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 22.0 | 21.3 | 21.7 | 27.0 | 23.0 |
| Triples anotados | 0.4 | 0.7 | 0.6 | 2.0 | 1.0 |
| Triples intentados | 2.0 | 2.6 | 2.0 | 5.9 | 3.0 |
| % triples | 20.0% | 26.9% | 28.6% | 32.9% | 33.3% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -3%, vs defensa media -9%, vs defensa débil +16%; rebotes: vs defensa fuerte -17%, vs defensa media -6%, vs defensa débil +18%; asistencias: vs defensa fuerte -10%, vs defensa media +4%, vs defensa débil +12%; triples: vs defensa fuerte -23%, vs defensa media -2%, vs defensa débil +19%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 43% | 29% | 35% | 36% |
| pintura | 20% | 42% | 45% | 44% |
| triple de esquina | 17% | 42% | 38% | 38% |
| bajo el aro | 17% | 65% | 68% | 68% |
| media distancia | 3% | 38% | 41% | 38% |

#### Day'Ron Sharpe (pívots) vs Charlotte Hornets

- Minutos esperados: **22.4** (± 3.9); 69 partidos en la base.
- Egor Demin ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- cambio de rol esta temporada (por minuto): ast -34%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Day'Ron Sharpe: menos de 2.5 asistencias** (62%). Con 80% de probabilidad: más de 0.5 / menos de 3.5.
- Defensa de Charlotte Hornets contra pívots en asistencias: -4% respecto a la media; ajuste por su historial contra defensas similares: -2%.

**¿Por qué 2.0 asistencias?** (línea 2.5; 22.4 minutos esperados)

Razonamiento (4 factores a favor, 1 en contra):

- ✅ Minutos: 22.4 esperados (titular, ±3.9).
- ✅ Forma: 1.8 en sus últimos 5, 1.9 esta temporada (7 partidos), 2.4 la temporada pasada (línea 2.5).
- ➖ Cómo produce asistencias: asiste el 13.9% de las canastas de sus compañeros en pista × 13.2 canastas de compañeros esperadas (su equipo 36.2 por 48' contra esta defensa).
- ✅ Defensa: el rival concede -4% de asistencias por minuto a pívots (defensa fuerte); ajuste aplicado -4%.
- ✅ Ritmo del partido: -2% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ❌ Contra este rival: 3, 3, 0 (1 de 3 a favor).
- ➖ Últimos 10: la habría pasado 6 de 10.
- ⚠️ Egor Demin ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ cambio de rol esta temporada (por minuto): ast -34%; se da más peso a la línea de la casa.

- ⚠️ Alertas: cambio de rol.
- Asistencias **2.0** (por componentes 1.8 · por tasa por minuto y defensa rival 2.0): asiste el 13.9% de las canastas de sus compañeros en pista × 13.2 canastas de compañeros esperadas (su equipo 36.2 por 48' contra esta defensa).

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 21.0 | 21.5 | 22.6 | 18.7 | 19.7 |
| Asistencias | 1.8 | 2.0 | 1.9 | 2.3 | 2.0 |
| % de las canastas de compañeros que asiste | 13.7% | 13.8% | 12.6% | 17.8% | 14.2% |
| Pérdidas por jugada | 24.4% | 22.6% | 24.4% | 20.0% | 32.1% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -18%, vs defensa media -2%, vs defensa débil +28%; rebotes: vs defensa fuerte -3%, vs defensa media +2%, vs defensa débil +2%; asistencias: vs defensa fuerte -7%, vs defensa media +16%, vs defensa débil -1%; triples: vs defensa fuerte +29%, vs defensa media -3%, vs defensa débil -25%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 62% | 69% | 68% | 68% |
| pintura | 24% | 45% | 45% | 44% |
| triple frontal | 8% | 31% | 35% | 36% |
| triple de esquina | 5% | 38% | 38% | 38% |
| media distancia | 1% | 38% | 41% | 38% |

#### Nolan Traore (bases/escoltas) vs Charlotte Hornets

- Minutos esperados: **23.4** (± 6.6); 63 partidos en la base.
- Egor Demin ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- cambio de rol esta temporada (por minuto): pts +33%, tpm +63%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Nolan Traore: menos de 2.5 rebotes** (61%). Con 80% de probabilidad: más de 0.5 / menos de 4.5.
- Defensa de Charlotte Hornets contra bases/escoltas en rebotes: -3% respecto a la media; ajuste por su historial contra defensas similares: +2%.

**¿Por qué 2.3 rebotes?** (línea 2.5; 23.4 minutos esperados)

Razonamiento (5 factores a favor, 1 en contra):

- ❌ Minutos: 23.4 esperados (titular, ±6.6).
- ✅ Forma: 2.0 en sus últimos 5, 2.0 esta temporada (7 partidos), 1.8 la temporada pasada (línea 2.5).
- ➖ Cómo produce rebotes: defensivos 1.8 = captura el 8.5% de los fallos del rival en pista × 44.2 fallos esperados del rival (liga 47.0) × 49% del partido; ofensivos 0.5 = 2.2% de los fallos de su equipo × 46.4.
- ✅ Defensa: el rival concede -3% de rebotes por minuto a bases/escoltas (defensa fuerte); ajuste aplicado -3%.
- ✅ Ritmo del partido: -2% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 2, 5, 0 (2 de 3 a favor).
- ✅ Últimos 10: la habría pasado 8 de 10.
- ⚠️ Egor Demin ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ cambio de rol esta temporada (por minuto): pts +33%, tpm +63%; se da más peso a la línea de la casa.

- ⚠️ Alertas: minutos inestables.
- Rebotes **2.3** (por componentes 2.3 · por tasa por minuto y defensa rival 2.2): defensivos 1.8 = captura el 8.5% de los fallos del rival en pista × 44.2 fallos esperados del rival (liga 47.0) × 49% del partido; ofensivos 0.5 = 2.2% de los fallos de su equipo × 46.4.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 25.8 | 20.3 | 21.4 | 22.2 | 16.0 |
| Rebotes | 2.0 | 2.1 | 2.0 | 1.8 | 2.3 |
| % de los fallos del rival que captura | 7.6% | 8.9% | 7.2% | 7.8% | 10.6% |
| % de los fallos de su equipo que captura | 0.8% | 2.6% | 2.7% | 1.2% | 4.4% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -7%, vs defensa media -7%, vs defensa débil +19%; rebotes: vs defensa fuerte +12%, vs defensa media -18%, vs defensa débil +4%; asistencias: vs defensa fuerte -13%, vs defensa media -7%, vs defensa débil +21%; triples: vs defensa fuerte -8%, vs defensa media -5%, vs defensa débil +18%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 30% | 36% | 35% | 36% |
| pintura | 29% | 42% | 45% | 44% |
| bajo el aro | 25% | 52% | 68% | 68% |
| triple de esquina | 10% | 36% | 38% | 38% |
| media distancia | 6% | 37% | 41% | 38% |

## Chicago Bulls @ New York Knicks

Diferencia esperada: New York Knicks por 11.5 — algo desigual: titulares hasta -1.5% de minutos.

Parte de lesiones: Josh Hart (Day-To-Day); Nic Claxton (Out); Jalen Smith (Day-To-Day).

Ventajas del partido (los dos lados): puntos esperados frente a su media de los últimos 10, ajuste por la defensa rival y diferencia de estatura con los rivales de su posición.

| Equipo | Jugador | Puntos esperados | Su media (últ. 10) | Defensa rival en puntos | Rebotes esperados | Altura vs rival |
|---|---|---|---|---|---|---|
| NY | OG Anunoby | 18.3 | 18.7 | +5% | 6.1 | -1.2" |
| NY | Jalen Brunson | 24.1 | 28.5 | +1% | 3.1 | -2.0" |
| NY | Karl-Anthony Towns | 19.3 | 16.8 | +5% | 12.8 | - |
| NY | Josh Hart | 10.5 | 9.5 | +1% | 7.0 | +1.0" |
| CHI | Norman Powell | 18.6 | 18.5 | -3% | 3.0 | +0.2" |
| CHI | Josh Giddey | 11.3 | 9.7 | -4% | 5.4 | +3.2" |
| CHI | Jalen Smith | 12.0 | 11.0 | -3% | 7.7 | +1.0" |
| NY | Landry Shamet | 10.5 | 7.6 | +1% | 1.9 | +1.0" |
| CHI | Matas Buzelis | 13.0 | 13.3 | -3% | 4.5 | +1.0" |
| CHI | Tre Jones | 10.2 | 13.3 | -4% | 2.6 | -2.8" |

Picks seguros de titulares estables:

| Jugador | Pick seguro | Prob. | Cuota mínima | Esperado | Últ. 10 |
|---|---|---|---|---|---|
| Karl-Anthony Towns | **más de 7.5 rebotes** | **90%** | 1.12 | 12.8 | 10/10 |
| Jalen Brunson | **más de 2.5 asistencias** | **89%** | 1.13 | 5.9 | 10/10 |
| Josh Hart | **más de 3.5 rebotes** | **88%** | 1.14 | 7.0 | 10/10 |
| Jalen Brunson | **más de 23.5 pts+reb+ast** | **87%** | 1.16 | 33.1 | 10/10 |
| Karl-Anthony Towns | **más de 24.5 pts+reb+ast** | **86%** | 1.16 | 35.9 | 8/10 |
| Jalen Brunson | **más de 15.5 puntos** | **86%** | 1.17 | 24.1 | 10/10 |

Las 8 más probables (máximo 2 por jugador: las de un mismo jugador suelen ganar o perder juntas).

| Prop | Prob. final | Modelo | Casa | Esperado | Últ. 10 | Temporada | vs este rival | Cuota (implícita) |
|---|---|---|---|---|---|---|---|---|
| **Norman Powell: menos de 2.5 asistencias** | **65%** | 68% | 63% | 2.0 ± 1.5 | 8/10 | 5/7 | 2, 3, 3, 0, 3 | 1.50 (67%) |
| **Mikal Bridges: menos de 3.5 rebotes** | **63%** | 68% | 59% | 2.7 ± 1.9 | 7/10 | 5/7 | 0, 2, 2, 5, 4 | 1.57 (64%) |
| **Mikal Bridges: menos de 1.5 triples** | **62%** | 65% | 60% | 1.2 ± 1.3 | 7/10 | 5/7 | 1, 0, 3, 2, 4 | 1.55 (64%) |
| **Tre Jones: menos de 3.5 asistencias** ⚠️ suplente | **62%** | 64% | 59% | 2.9 ± 2.0 | 7/10 | 5/7 | 3, 8, 3, 5, 3 | 1.58 (63%) |
| **OG Anunoby: menos de 2.5 triples** | **60%** | 61% | 59% | 2.2 ± 1.5 | 6/10 | 5/7 | 2, 7, 0, 3, 5 | 1.57 (64%) |
| **Landry Shamet: más de 1.5 triples** ⚠️ suplente | **60%** | 62% | 59% | 2.2 ± 1.6 | 5/10 | 5/7 | 4, 2, 4, 3, 1 | 1.59 (63%) |
| **Josh Giddey: menos de 1.5 triples** | **59%** | 59% | 60% | 1.4 ± 1.2 | 7/10 | 5/7 | 1, 0, 0, 1, 4 | 1.57 (63%) |
| **Josh Giddey: menos de 6.5 rebotes** | **59%** | 63% | 56% | 5.4 ± 2.7 | 5/10 | 4/7 | 8, 5, 2, 11, 10 | 1.67 (60%) |

### Fichas de los jugadores destacados

#### Norman Powell (bases/escoltas) vs New York Knicks

- Minutos esperados: **29.4** (± 4.5); 68 partidos en la base.
- cambio de rol esta temporada (por minuto): ast -31%; se da más peso a la línea de la casa
- partido desigual (no favorito por 11.5): los titulares suelen jugar -3% de minutos si se rompe
- Su prop más probable hoy: **Norman Powell: menos de 2.5 asistencias** (65%). Con 80% de probabilidad: más de 0.5 / menos de 3.5.
- Defensa de New York Knicks contra bases/escoltas en asistencias: -9% respecto a la media; ajuste por su historial contra defensas similares: -1%.

**¿Por qué 2.0 asistencias?** (línea 2.5; 29.4 minutos esperados)

Razonamiento (4 factores a favor, 0 en contra):

- ✅ Minutos: 29.4 esperados (titular, ±4.5).
- ✅ Forma: 2.0 en sus últimos 5, 1.7 esta temporada (7 partidos), 2.4 la temporada pasada (línea 2.5).
- ➖ Cómo produce asistencias: asiste el 11.1% de las canastas de sus compañeros en pista × 18.0 canastas de compañeros esperadas (su equipo 38.6 por 48' contra esta defensa).
- ✅ Defensa: el rival concede -9% de asistencias por minuto a bases/escoltas (defensa fuerte); ajuste aplicado -9%.
- ➖ Ritmo del partido: +1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ➖ Contra este rival: 2, 3, 3, 0, 3 (2 de 5 a favor).
- ✅ Últimos 10: la habría pasado 8 de 10.
- ⚠️ cambio de rol esta temporada (por minuto): ast -31%; se da más peso a la línea de la casa.
- ⚠️ partido desigual (no favorito por 11.5): los titulares suelen jugar -3% de minutos si se rompe.

- ⚠️ Alertas: cambio de rol.
- Asistencias **2.0** (por componentes 2.0 · por tasa por minuto y defensa rival 2.0): asiste el 11.1% de las canastas de sus compañeros en pista × 18.0 canastas de compañeros esperadas (su equipo 38.6 por 48' contra esta defensa).

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 30.8 | 26.8 | 29.9 | 28.7 | 33.8 |
| Asistencias | 2.0 | 1.5 | 1.7 | 2.4 | 2.2 |
| % de las canastas de compañeros que asiste | 9.5% | 7.6% | 8.4% | 11.2% | 9.4% |
| Pérdidas por jugada | 11.1% | 9.4% | 9.2% | 9.8% | 8.0% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +3%, vs defensa media -2%, vs defensa débil -4%; rebotes: vs defensa fuerte -17%, vs defensa media +3%, vs defensa débil +21%; asistencias: vs defensa fuerte -1%, vs defensa media +10%, vs defensa débil -14%; triples: vs defensa fuerte -4%, vs defensa media -2%, vs defensa débil +12%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 41% | 37% | 35% | 34% |
| bajo el aro | 22% | 63% | 68% | 65% |
| pintura | 20% | 54% | 45% | 43% |
| media distancia | 10% | 37% | 41% | 41% |
| triple de esquina | 7% | 36% | 38% | 38% |

#### Mikal Bridges (bases/escoltas) vs Chicago Bulls

- Minutos esperados: **24.2** (± 8.4); 107 partidos en la base.
- cambio de rol esta temporada (por minuto): pts -45%, ast -39%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Mikal Bridges: menos de 3.5 rebotes** (63%). Con 80% de probabilidad: más de 0.5 / menos de 4.5.
- Defensa de Chicago Bulls contra bases/escoltas en rebotes: +2% respecto a la media; ajuste por su historial contra defensas similares: -2%.

**¿Por qué 2.7 rebotes?** (línea 3.5; 24.2 minutos esperados)

Razonamiento (3 factores a favor, 2 en contra):

- ❌ Minutos: 24.2 esperados (titular, ±8.4).
- ✅ Forma: 3.0 en sus últimos 5, 2.7 esta temporada (7 partidos), 3.1 la temporada pasada (línea 3.5).
- ➖ Cómo produce rebotes: defensivos 2.0 = captura el 8.2% de los fallos del rival en pista × 48.2 fallos esperados del rival (liga 47.0) × 50% del partido; ofensivos 0.7 = 3.0% de los fallos de su equipo × 48.4.
- ➖ Defensa: el rival concede +2% de rebotes por minuto a bases/escoltas (defensa media); ajuste aplicado +2%.
- ❌ Altura: mide 6'6", 2.0 pulgadas más que los bases/escoltas del rival (+0.7% en esta estadística).
- ➖ Ritmo del partido: +1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 0, 2, 2, 5, 4 (3 de 5 a favor).
- ✅ Últimos 10: la habría pasado 7 de 10.
- ⚠️ cambio de rol esta temporada (por minuto): pts -45%, ast -39%; se da más peso a la línea de la casa.

- ⚠️ Alertas: minutos inestables.
- Rebotes **2.7** (por componentes 2.7 · por tasa por minuto y defensa rival 2.6): defensivos 2.0 = captura el 8.2% de los fallos del rival en pista × 48.2 fallos esperados del rival (liga 47.0) × 50% del partido; ofensivos 0.7 = 3.0% de los fallos de su equipo × 48.4.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 25.2 | 27.7 | 25.9 | 33.0 | 27.8 |
| Rebotes | 3.0 | 2.8 | 2.7 | 3.7 | 2.6 |
| % de los fallos del rival que captura | 7.4% | 7.5% | 6.7% | 9.0% | 7.5% |
| % de los fallos de su equipo que captura | 4.4% | 2.4% | 3.6% | 2.7% | 2.2% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +1%, vs defensa media -14%, vs defensa débil +11%; rebotes: vs defensa fuerte -8%, vs defensa media -4%, vs defensa débil +10%; asistencias: vs defensa fuerte -13%, vs defensa media -6%, vs defensa débil +25%; triples: vs defensa fuerte -8%, vs defensa media +3%, vs defensa débil +14%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 23% | 33% | 35% | 37% |
| bajo el aro | 22% | 75% | 68% | 67% |
| triple de esquina | 21% | 39% | 38% | 37% |
| pintura | 20% | 44% | 45% | 43% |
| media distancia | 14% | 45% | 41% | 42% |

#### Tre Jones (bases/escoltas) vs New York Knicks

- Minutos esperados: **19.2** (± 3.0); 72 partidos en la base.
- cambio de rol esta temporada (por minuto): reb +35%; se da más peso a la línea de la casa
- partido desigual (no favorito por 11.5): los suplentes suelen jugar +3% de minutos si se rompe
- Su prop más probable hoy: **Tre Jones: menos de 3.5 asistencias** (62%). Con 80% de probabilidad: más de 0.5 / menos de 4.5.
- Defensa de New York Knicks contra bases/escoltas en asistencias: -9% respecto a la media; ajuste por su historial contra defensas similares: -1%.

**¿Por qué 2.9 asistencias?** (línea 3.5; 19.2 minutos esperados)

Razonamiento (4 factores a favor, 1 en contra):

- ❌ Minutos: 19.2 esperados (suplente, ±3.0).
- ✅ Forma: 2.6 en sus últimos 5, 3.0 esta temporada (7 partidos), 5.3 la temporada pasada (línea 3.5).
- ➖ Cómo produce asistencias: asiste el 22.5% de las canastas de sus compañeros en pista × 11.7 canastas de compañeros esperadas (su equipo 38.6 por 48' contra esta defensa).
- ✅ Defensa: el rival concede -9% de asistencias por minuto a bases/escoltas (defensa fuerte); ajuste aplicado -9%.
- ➖ Ritmo del partido: +1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 3, 8, 3, 5, 3 (3 de 5 a favor).
- ✅ Últimos 10: la habría pasado 7 de 10.
- ⚠️ cambio de rol esta temporada (por minuto): reb +35%; se da más peso a la línea de la casa.
- ⚠️ partido desigual (no favorito por 11.5): los suplentes suelen jugar +3% de minutos si se rompe.

- ⚠️ Alertas: suplente.
- Asistencias **2.9** (por componentes 2.6 · por tasa por minuto y defensa rival 3.0): asiste el 22.5% de las canastas de sus compañeros en pista × 11.7 canastas de compañeros esperadas (su equipo 38.6 por 48' contra esta defensa).

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 18.0 | 20.2 | 18.1 | 27.0 | 25.0 |
| Asistencias | 2.6 | 3.0 | 3.0 | 5.4 | 4.4 |
| % de las canastas de compañeros que asiste | 19.8% | 20.0% | 22.5% | 25.5% | 22.8% |
| Pérdidas por jugada | 12.6% | 7.0% | 8.9% | 11.4% | 9.4% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -5%, vs defensa media +16%, vs defensa débil -4%; rebotes: vs defensa fuerte -12%, vs defensa media +7%, vs defensa débil +9%; asistencias: vs defensa fuerte -1%, vs defensa media -10%, vs defensa débil +13%; triples: vs defensa fuerte -22%, vs defensa media +27%, vs defensa débil +6%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 51% | 69% | 68% | 65% |
| pintura | 25% | 43% | 45% | 43% |
| triple frontal | 13% | 31% | 35% | 34% |
| triple de esquina | 7% | 37% | 38% | 38% |
| media distancia | 5% | 42% | 41% | 41% |

#### OG Anunoby (aleros/ala-pívots) vs Chicago Bulls

- Minutos esperados: **33.9** (± 3.0); 91 partidos en la base.
- partido desigual (favorito por 11.5): los titulares suelen jugar -3% de minutos si se rompe
- Su prop más probable hoy: **OG Anunoby: menos de 2.5 triples** (60%). Con 80% de probabilidad: más de 0.5 / menos de 3.5.
- Defensa de Chicago Bulls contra aleros/ala-pívots en triples: +5% respecto a la media; ajuste por su historial contra defensas similares: +1%.

**¿Por qué 2.2 triples?** (línea 2.5; 33.9 minutos esperados)

Razonamiento (2 factores a favor, 1 en contra):

- ✅ Minutos: 33.9 esperados (titular, ±3.0).
- ✅ Forma: 2.0 en sus últimos 5, 1.9 esta temporada (7 partidos), 2.5 la temporada pasada (línea 2.5).
- ➖ Cómo produce triples: 6.0 triples intentados (su ritmo 6.2 por 36'; el rival concede -2% de triples en su reparto) × 39% esperado.
- ❌ Defensa: el rival concede +8% de triples por minuto a aleros/ala-pívots (defensa débil); ajuste aplicado +5%; en su zona principal (triple) el rival concede 37% (liga 35%).
- ➖ Ritmo del partido: +1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ➖ Contra este rival: 2, 7, 0, 3, 5 (2 de 5 a favor).
- ➖ Últimos 10: la habría pasado 6 de 10.
- ⚠️ partido desigual (favorito por 11.5): los titulares suelen jugar -3% de minutos si se rompe.

- Triples **2.2** (por componentes 2.3 · por tasa por minuto y defensa rival 2.2): 6.0 triples intentados (su ritmo 6.2 por 36'; el rival concede -2% de triples en su reparto) × 39% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 34.8 | 35.2 | 34.3 | 33.6 | 33.4 |
| Triples anotados | 2.0 | 2.4 | 1.9 | 2.4 | 3.4 |
| Triples intentados | 5.6 | 6.4 | 6.1 | 6.0 | 6.8 |
| % triples | 35.7% | 37.5% | 30.2% | 40.4% | 50.0% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +1%, vs defensa media -4%, vs defensa débil +3%; rebotes: vs defensa fuerte -7%, vs defensa media -1%, vs defensa débil +6%; asistencias: vs defensa fuerte -12%, vs defensa media -1%, vs defensa débil +15%; triples: vs defensa fuerte -3%, vs defensa media -4%, vs defensa débil +11%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 36% | 68% | 68% | 67% |
| triple frontal | 26% | 34% | 35% | 37% |
| triple de esquina | 24% | 44% | 38% | 37% |
| pintura | 9% | 34% | 45% | 43% |
| media distancia | 5% | 42% | 41% | 42% |

#### Landry Shamet (bases/escoltas) vs Chicago Bulls

- Minutos esperados: **25.2** (± 5.9); 76 partidos en la base.
- cambio de rol esta temporada (por minuto): ast +41%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Landry Shamet: más de 1.5 triples** (60%). Con 80% de probabilidad: más de 0.5 / menos de 3.5.
- Defensa de Chicago Bulls contra bases/escoltas en triples: +3% respecto a la media; ajuste por su historial contra defensas similares: +2%.

**¿Por qué 2.2 triples?** (línea 1.5; 25.2 minutos esperados)

Razonamiento (3 factores a favor, 1 en contra):

- ❌ Minutos: 25.2 esperados (suplente, ±5.9).
- ✅ Forma: 2.6 en sus últimos 5, 2.3 esta temporada (7 partidos), 1.9 la temporada pasada (línea 1.5).
- ➖ Cómo produce triples: 5.2 triples intentados (su ritmo 7.2 por 36'; el rival concede -2% de triples en su reparto) × 41% esperado.
- ✅ Defensa: el rival concede +3% de triples por minuto a bases/escoltas (defensa débil); ajuste aplicado +3%; en su zona principal (triple) el rival concede 37% (liga 35%).
- ➖ Ritmo del partido: +1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 4, 2, 4, 3, 1 (4 de 5 a favor).
- ➖ Últimos 10: la habría pasado 5 de 10.
- ⚠️ cambio de rol esta temporada (por minuto): ast +41%; se da más peso a la línea de la casa.

- ⚠️ Alertas: suplente.
- Triples **2.2** (por componentes 2.1 · por tasa por minuto y defensa rival 2.3): 5.2 triples intentados (su ritmo 7.2 por 36'; el rival concede -2% de triples en su reparto) × 41% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 25.6 | 23.1 | 24.9 | 21.1 | 20.2 |
| Triples anotados | 2.6 | 1.8 | 2.3 | 1.9 | 2.8 |
| Triples intentados | 5.2 | 4.8 | 5.0 | 4.6 | 5.4 |
| % triples | 50.0% | 37.5% | 45.7% | 40.1% | 51.9% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -8%, vs defensa media +13%, vs defensa débil +2%; rebotes: vs defensa fuerte +1%, vs defensa media -4%, vs defensa débil +3%; asistencias: vs defensa fuerte +1%, vs defensa media -24%, vs defensa débil +24%; triples: vs defensa fuerte -19%, vs defensa media +18%, vs defensa débil +10%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 40% | 38% | 35% | 37% |
| triple de esquina | 31% | 42% | 38% | 37% |
| bajo el aro | 17% | 65% | 68% | 67% |
| pintura | 6% | 38% | 45% | 43% |
| media distancia | 6% | 40% | 41% | 42% |

## Indiana Pacers @ Memphis Grizzlies

Diferencia esperada: Memphis Grizzlies por 6.5.

Parte de lesiones: T.J. McConnell (Out); Kelly Oubre Jr. (Day-To-Day); Ivica Zubac (Out); Obi Toppin (Out); Scotty Pippen Jr. (Out); Quinten Post (Day-To-Day); Johnny Furphy (Out).

Ventajas del partido (los dos lados): puntos esperados frente a su media de los últimos 10, ajuste por la defensa rival y diferencia de estatura con los rivales de su posición.

| Equipo | Jugador | Puntos esperados | Su media (últ. 10) | Defensa rival en puntos | Rebotes esperados | Altura vs rival |
|---|---|---|---|---|---|---|
| IND | Pascal Siakam | 21.0 | 23.5 | +2% | 6.7 | +0.8" |
| IND | Andrew Nembhard | 22.3 | 16.6 | +3% | 3.2 | +0.2" |
| MEM | Ty Jerome | 26.2 | 24.4 | +3% | 3.9 | +0.1" |
| MEM | Cedric Coward | 13.5 | 14.4 | +1% | 7.5 | -2.5" |
| MEM | Jaylen Wells | 13.2 | 10.8 | +1% | 3.8 | -0.5" |
| IND | Jarace Walker | 11.4 | 9.4 | +1% | 6.6 | -0.2" |
| IND | Aaron Nesmith | 11.9 | 13.7 | +3% | 4.2 | +1.2" |
| IND | Quenton Jackson | 12.2 | 11.8 | +3% | 3.3 | +0.2" |
| MEM | Jerami Grant | 12.0 | 10.8 | +1% | 3.1 | -0.5" |
| MEM | Javon Small | 10.4 | 11.8 | +2% | 3.1 | -3.9" |

Picks seguros de titulares estables:

| Jugador | Pick seguro | Prob. | Cuota mínima | Esperado | Últ. 10 |
|---|---|---|---|---|---|
| Pascal Siakam | **más de 2.5 rebotes** | **90%** | 1.11 | 6.7 | 10/10 |
| Pascal Siakam | **más de 12.5 puntos** | **88%** | 1.13 | 21.0 | 10/10 |
| Andrew Nembhard | **más de 13.5 puntos** | **88%** | 1.14 | 22.3 | 8/10 |
| Ty Jerome | **más de 2.5 asistencias** | **87%** | 1.14 | 5.7 | 10/10 |
| Pascal Siakam | **más de 21.5 pts+reb+ast** | **87%** | 1.15 | 31.5 | 10/10 |
| Andrew Nembhard | **más de 22.5 pts+reb+ast** | **86%** | 1.16 | 31.8 | 9/10 |

Las 8 más probables (máximo 2 por jugador: las de un mismo jugador suelen ganar o perder juntas).

| Prop | Prob. final | Modelo | Casa | Esperado | Últ. 10 | Temporada | vs este rival | Cuota (implícita) |
|---|---|---|---|---|---|---|---|---|
| **Kelly Oubre Jr.: menos de 1.5 triples** | **62%** | 67% | 58% | 1.2 ± 1.1 | 7/10 | 6/7 | 1 | 1.63 (61%) |
| **Andrew Nembhard: menos de 3.5 rebotes** | **62%** | 64% | 60% | 3.2 ± 1.8 | 9/10 | 6/6 | - | 1.56 (64%) |
| **Pascal Siakam: menos de 4.5 asistencias** | **61%** | 64% | 58% | 3.7 ± 2.0 | 5/10 | 4/7 | 6 | 1.61 (62%) |
| **Andrew Nembhard: menos de 8.5 asistencias** | **60%** | 69% | 54% | 6.3 ± 3.4 | 3/10 | 3/6 | - | 1.73 (58%) |
| **Ty Jerome: menos de 6.5 asistencias** | **59%** | 64% | 55% | 5.7 ± 2.5 | 7/10 | 5/6 | - | 1.71 (59%) |
| **Aaron Nesmith: más de 1.5 asistencias** | **58%** | 70% | 49% | 3.0 ± 1.8 | 5/10 | 3/6 | 1 | 1.88 (53%) |
| **Jaylen Wells: más de 1.5 triples** | **57%** | 59% | 56% | 1.9 ± 1.4 | 6/10 | 5/7 | 2, 0 | 1.66 (60%) |
| **Cam Spencer: más de 7.5 puntos** ⚠️ suplente | **57%** | 65% | 50% | 9.7 ± 4.9 | 9/10 | 6/7 | 10, 8 | 1.87 (53%) |

### Fichas de los jugadores destacados

#### Kelly Oubre Jr. (bases/escoltas) vs Memphis Grizzlies

- Minutos esperados: **23.1** (± 4.0); 69 partidos en la base.
- en el parte de lesiones: day-to-day
- Ivica Zubac ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- sin Obi Toppin: muestra insuficiente (2 partidos sin él)
- Johnny Furphy ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- cambio de rol esta temporada (por minuto): reb -31%, ast +44%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Kelly Oubre Jr.: menos de 1.5 triples** (62%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Memphis Grizzlies contra bases/escoltas en triples: +3% respecto a la media; ajuste por su historial contra defensas similares: -3%.

**¿Por qué 1.2 triples?** (línea 1.5; 23.1 minutos esperados)

Razonamiento (4 factores a favor, 2 en contra):

- ✅ Minutos: 23.1 esperados (titular, ±4.0).
- ✅ Forma: 1.2 en sus últimos 5, 1.0 esta temporada (7 partidos), 1.6 la temporada pasada (línea 1.5).
- ➖ Cómo produce triples: 3.8 triples intentados (su ritmo 5.7 por 36'; el rival concede +2% de triples en su reparto) × 34% esperado.
- ❌ Defensa: el rival concede +6% de triples por minuto a bases/escoltas (defensa débil); ajuste aplicado +3%; en su zona principal (triple) el rival concede 34% (liga 35%).
- ❌ Altura: mide 6'8", 4.2 pulgadas más que los bases/escoltas del rival (+1.5% en esta estadística).
- ➖ Ritmo del partido: +1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 1 (1 de 1 a favor).
- ✅ Últimos 10: la habría pasado 7 de 10.
- ⚠️ en el parte de lesiones: day-to-day.
- ⚠️ Ivica Zubac ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ sin Obi Toppin: muestra insuficiente (2 partidos sin él).
- ⚠️ Johnny Furphy ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ cambio de rol esta temporada (por minuto): reb -31%, ast +44%; se da más peso a la línea de la casa.

- ⚠️ Alertas: en el parte de lesiones.
- Triples **1.2** (por componentes 1.3 · por tasa por minuto y defensa rival 1.1): 3.8 triples intentados (su ritmo 5.7 por 36'; el rival concede +2% de triples en su reparto) × 34% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 23.0 | 26.5 | 23.3 | 31.9 | 38.0 |
| Triples anotados | 1.2 | 1.2 | 1.0 | 1.6 | 1.0 |
| Triples intentados | 3.6 | 3.9 | 3.9 | 4.6 | 9.0 |
| % triples | 33.3% | 30.8% | 25.9% | 35.1% | 11.1% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -5%, vs defensa media +5%, vs defensa débil +5%; rebotes: vs defensa fuerte -13%, vs defensa media +2%, vs defensa débil +19%; asistencias: vs defensa fuerte -19%, vs defensa media +21%, vs defensa débil +19%; triples: vs defensa fuerte +10%, vs defensa media -5%, vs defensa débil -3%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 27% | 66% | 68% | 69% |
| triple frontal | 26% | 31% | 35% | 34% |
| pintura | 24% | 46% | 45% | 45% |
| triple de esquina | 18% | 39% | 38% | 39% |
| media distancia | 5% | 42% | 41% | 43% |

#### Andrew Nembhard (bases/escoltas) vs Memphis Grizzlies

- Minutos esperados: **34.0** (± 3.0); 63 partidos en la base.
- Ivica Zubac ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- sin Obi Toppin (48 partidos): 31.8 min vs 30.5 con él; pts +18%/min, ast -17%/min
- Johnny Furphy ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Su prop más probable hoy: **Andrew Nembhard: menos de 3.5 rebotes** (62%). Con 80% de probabilidad: más de 1.5 / menos de 5.5.
- Defensa de Memphis Grizzlies contra bases/escoltas en rebotes: +3% respecto a la media; ajuste por su historial contra defensas similares: -1%.

**¿Por qué 3.2 rebotes?** (línea 3.5; 34.0 minutos esperados)

Razonamiento (4 factores a favor, 1 en contra):

- ✅ Minutos: 34.0 esperados (titular, ±3.0).
- ✅ Forma: 2.2 en sus últimos 5, 2.2 esta temporada (6 partidos), 2.8 la temporada pasada (línea 3.5).
- ➖ Cómo produce rebotes: defensivos 2.8 = captura el 8.0% de los fallos del rival en pista × 48.4 fallos esperados del rival (liga 47.0) × 71% del partido; ofensivos 0.5 = 1.5% de los fallos de su equipo × 47.8.
- ❌ Defensa: el rival concede +3% de rebotes por minuto a bases/escoltas (defensa débil); ajuste aplicado +3%.
- ➖ Ritmo del partido: +1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Últimos 10: la habría pasado 9 de 10.
- ✅ Racha: la pasó en sus 6 partidos de esta temporada (al inicio de 2025-26 estas rachas siguieron más de lo que esperaba el modelo).
- ⚠️ Ivica Zubac ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ sin Obi Toppin (48 partidos): 31.8 min vs 30.5 con él; pts +18%/min, ast -17%/min.
- ⚠️ Johnny Furphy ya no jugó en sus últimos partidos: la baja ya está en sus minutos.

- Rebotes **3.2** (por componentes 3.3 · por tasa por minuto y defensa rival 3.1): defensivos 2.8 = captura el 8.0% de los fallos del rival en pista × 48.4 fallos esperados del rival (liga 47.0) × 71% del partido; ofensivos 0.5 = 1.5% de los fallos de su equipo × 47.8.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 32.4 | 33.3 | 32.7 | 31.3 | - |
| Rebotes | 2.2 | 2.6 | 2.2 | 2.8 | - |
| % de los fallos del rival que captura | 6.6% | 7.1% | 6.4% | 8.0% | - |
| % de los fallos de su equipo que captura | 0.7% | 1.0% | 0.5% | 1.4% | - |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +2%, vs defensa media -1%, vs defensa débil -2%; rebotes: vs defensa fuerte -16%, vs defensa media +14%, vs defensa débil +9%; asistencias: vs defensa fuerte -10%, vs defensa media +5%, vs defensa débil +8%; triples: vs defensa fuerte -8%, vs defensa media +8%, vs defensa débil -2%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 37% | 38% | 35% | 34% |
| media distancia | 22% | 38% | 41% | 43% |
| pintura | 21% | 49% | 45% | 45% |
| bajo el aro | 17% | 65% | 68% | 69% |
| triple de esquina | 3% | 34% | 38% | 39% |

#### Pascal Siakam (aleros/ala-pívots) vs Memphis Grizzlies

- Minutos esperados: **34.3** (± 3.8); 71 partidos en la base.
- Ivica Zubac ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- sin Obi Toppin (51 partidos): 33.6 min vs 31.8 con él; pts -8%/min, reb -15%/min
- Johnny Furphy ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- cambio de rol esta temporada (por minuto): tpm -30%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Pascal Siakam: menos de 4.5 asistencias** (61%). Con 80% de probabilidad: más de 1.5 / menos de 5.5.
- Defensa de Memphis Grizzlies contra aleros/ala-pívots en asistencias: +2% respecto a la media; ajuste por su historial contra defensas similares: -0%.

**¿Por qué 3.7 asistencias?** (línea 4.5; 34.3 minutos esperados)

Razonamiento (1 factores a favor, 3 en contra):

- ✅ Minutos: 34.3 esperados (titular, ±3.8).
- ❌ Forma: 4.8 en sus últimos 5, 4.0 esta temporada (7 partidos), 3.6 la temporada pasada (línea 4.5).
- ➖ Cómo produce asistencias: asiste el 16.7% de las canastas de sus compañeros en pista × 22.2 canastas de compañeros esperadas (su equipo 42.2 por 48' contra esta defensa).
- ❌ Defensa: el rival concede +2% de asistencias por minuto a aleros/ala-pívots (defensa media); ajuste aplicado +2%.
- ➖ Ritmo del partido: +1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ❌ Contra este rival: 6 (0 de 1 a favor).
- ➖ Últimos 10: la habría pasado 5 de 10.
- ⚠️ Ivica Zubac ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ sin Obi Toppin (51 partidos): 33.6 min vs 31.8 con él; pts -8%/min, reb -15%/min.
- ⚠️ Johnny Furphy ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ cambio de rol esta temporada (por minuto): tpm -30%; se da más peso a la línea de la casa.

- Asistencias **3.7** (por componentes 3.5 · por tasa por minuto y defensa rival 3.8): asiste el 16.7% de las canastas de sus compañeros en pista × 22.2 canastas de compañeros esperadas (su equipo 42.2 por 48' contra esta defensa).

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 32.4 | 31.3 | 32.3 | 32.4 | 26.0 |
| Asistencias | 4.8 | 4.1 | 4.0 | 3.7 | 6.0 |
| % de las canastas de compañeros que asiste | 23.1% | 18.8% | 19.0% | 17.2% | 35.9% |
| Pérdidas por jugada | 13.3% | 11.7% | 13.6% | 9.5% | 13.4% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -4%, vs defensa media +3%, vs defensa débil +0%; rebotes: vs defensa fuerte -10%, vs defensa media -1%, vs defensa débil +10%; asistencias: vs defensa fuerte -10%, vs defensa media +3%, vs defensa débil +7%; triples: vs defensa fuerte +7%, vs defensa media -17%, vs defensa débil +8%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| pintura | 31% | 50% | 45% | 45% |
| bajo el aro | 27% | 69% | 68% | 69% |
| triple frontal | 20% | 34% | 35% | 34% |
| media distancia | 16% | 33% | 41% | 43% |
| triple de esquina | 5% | 36% | 38% | 39% |

#### Ty Jerome (bases/escoltas) vs Indiana Pacers

- Minutos esperados: **31.1** (± 4.6); 21 partidos en la base.
- cambio de rol esta temporada (por minuto): tpm -31%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Ty Jerome: menos de 6.5 asistencias** (59%). Con 80% de probabilidad: más de 3.5 / menos de 8.5.
- Defensa de Indiana Pacers contra bases/escoltas en asistencias: +0% respecto a la media; ajuste por su historial contra defensas similares: +2%.

**¿Por qué 5.7 asistencias?** (línea 6.5; 31.1 minutos esperados)

Razonamiento (3 factores a favor, 0 en contra):

- ✅ Minutos: 31.1 esperados (titular, ±4.6).
- ✅ Forma: 5.4 en sus últimos 5, 5.5 esta temporada (6 partidos), 5.7 la temporada pasada (línea 6.5).
- ➖ Cómo produce asistencias: asiste el 26.2% de las canastas de sus compañeros en pista × 19.6 canastas de compañeros esperadas (su equipo 43.5 por 48' contra esta defensa).
- ➖ Defensa: el rival concede +0% de asistencias por minuto a bases/escoltas (defensa media); ajuste aplicado +0%.
- ➖ Ritmo del partido: +1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Últimos 10: la habría pasado 7 de 10.
- ⚠️ cambio de rol esta temporada (por minuto): tpm -31%; se da más peso a la línea de la casa.

- Asistencias **5.7** (por componentes 5.1 · por tasa por minuto y defensa rival 6.0): asiste el 26.2% de las canastas de sus compañeros en pista × 19.6 canastas de compañeros esperadas (su equipo 43.5 por 48' contra esta defensa).

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 31.0 | 28.6 | 31.2 | 22.7 | - |
| Asistencias | 5.4 | 5.6 | 5.5 | 5.7 | - |
| % de las canastas de compañeros que asiste | 25.1% | 29.2% | 26.3% | 34.3% | - |
| Pérdidas por jugada | 11.1% | 9.6% | 9.6% | 10.1% | - |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -8%, vs defensa media -14%, vs defensa débil +11%; rebotes: vs defensa fuerte -1%, vs defensa media -29%, vs defensa débil +31%; asistencias: vs defensa fuerte -15%, vs defensa media +19%, vs defensa débil -7%; triples: vs defensa fuerte -5%, vs defensa media +18%, vs defensa débil -9%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| pintura | 37% | 52% | 45% | 47% |
| triple frontal | 36% | 40% | 35% | 34% |
| media distancia | 12% | 42% | 41% | 44% |
| bajo el aro | 11% | 67% | 68% | 67% |
| triple de esquina | 3% | 41% | 38% | 40% |

#### Aaron Nesmith (bases/escoltas) vs Memphis Grizzlies

- Minutos esperados: **26.1** (± 4.5); 51 partidos en la base.
- Ivica Zubac ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- sin Obi Toppin (33 partidos): 29.5 min vs 27.6 con él; pts -12%/min, reb +33%/min, ast +35%/min
- Johnny Furphy ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- cambio de rol esta temporada (por minuto): reb -33%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Aaron Nesmith: más de 1.5 asistencias** (58%). Con 80% de probabilidad: más de 0.5 / menos de 4.5.
- Defensa de Memphis Grizzlies contra bases/escoltas en asistencias: +4% respecto a la media; ajuste por su historial contra defensas similares: -2%.

**¿Por qué 3.0 asistencias?** (línea 1.5; 26.1 minutos esperados)

Razonamiento (3 factores a favor, 1 en contra):

- ✅ Minutos: 26.1 esperados (titular, ±4.5).
- ✅ Forma: 2.0 en sus últimos 5, 1.8 esta temporada (6 partidos), 1.9 la temporada pasada (línea 1.5).
- ➖ Cómo produce asistencias: asiste el 11.6% de las canastas de sus compañeros en pista × 19.1 canastas de compañeros esperadas (su equipo 42.2 por 48' contra esta defensa).
- ✅ Defensa: el rival concede +4% de asistencias por minuto a bases/escoltas (defensa media); ajuste aplicado +4%.
- ➖ Ritmo del partido: +1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ❌ Contra este rival: 1 (0 de 1 a favor).
- ➖ Últimos 10: la habría pasado 5 de 10.
- ⚠️ Ivica Zubac ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ sin Obi Toppin (33 partidos): 29.5 min vs 27.6 con él; pts -12%/min, reb +33%/min, ast +35%/min.
- ⚠️ Johnny Furphy ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ cambio de rol esta temporada (por minuto): reb -33%; se da más peso a la línea de la casa.

- Asistencias **3.0** (por componentes 3.0 · por tasa por minuto y defensa rival 2.9): asiste el 11.6% de las canastas de sus compañeros en pista × 19.1 canastas de compañeros esperadas (su equipo 42.2 por 48' contra esta defensa).

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 23.6 | 26.5 | 23.0 | 29.6 | 31.0 |
| Asistencias | 2.0 | 1.6 | 1.8 | 1.9 | 1.0 |
| % de las canastas de compañeros que asiste | 12.0% | 8.0% | 11.1% | 8.6% | 5.0% |
| Pérdidas por jugada | 13.8% | 14.4% | 13.2% | 10.1% | 0.0% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -11%, vs defensa media -2%, vs defensa débil +17%; rebotes: vs defensa fuerte -5%, vs defensa media -16%, vs defensa débil +16%; asistencias: vs defensa fuerte +3%, vs defensa media -16%, vs defensa débil +8%; triples: vs defensa fuerte -4%, vs defensa media -11%, vs defensa débil +17%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 39% | 36% | 35% | 34% |
| pintura | 18% | 44% | 45% | 45% |
| bajo el aro | 17% | 58% | 68% | 69% |
| triple de esquina | 16% | 38% | 38% | 39% |
| media distancia | 10% | 41% | 41% | 43% |

## Utah Jazz @ New Orleans Pelicans

Diferencia esperada: New Orleans Pelicans por 5.5.

Parte de lesiones: Jusuf Nurkic (Out); Mo Bamba (Day-To-Day); Jordan Poole (Out); Jaren Jackson Jr. (Out); Trey Murphy III (Day-To-Day); Trey Alexander (Out); Yves Missi (Out).

Ventajas del partido (los dos lados): puntos esperados frente a su media de los últimos 10, ajuste por la defensa rival y diferencia de estatura con los rivales de su posición.

| Equipo | Jugador | Puntos esperados | Su media (últ. 10) | Defensa rival en puntos | Rebotes esperados | Altura vs rival |
|---|---|---|---|---|---|---|
| NO | Trey Murphy III | 18.4 | 15.2 | +5% | 5.4 | -1.5" |
| NO | Zion Williamson | 22.1 | 19.4 | +6% | 5.9 | -3.5" |
| UTAH | Lauri Markkanen | 22.5 | 19.1 | -0% | 5.8 | +5.3" |
| NO | Dejounte Murray | 18.7 | 14.7 | +8% | 5.4 | -1.8" |
| UTAH | Ace Bailey | 14.8 | 13.7 | +3% | 6.2 | +4.6" |
| NO | Jeremiah Fears | 16.7 | 20.2 | +8% | 4.5 | -2.8" |
| UTAH | Keyonte George | 19.6 | 18.8 | +3% | 3.7 | -0.4" |
| NO | Saddiq Bey | 17.2 | 17.6 | +5% | 4.7 | -1.5" |
| UTAH | Jaxson Hayes | 10.2 | 7.7 | +5% | 6.5 | +2.6" |
| UTAH | Isaiah Collier | 8.7 | 10.4 | +4% | 2.6 | -0.4" |

Picks seguros de titulares estables:

| Jugador | Pick seguro | Prob. | Cuota mínima | Esperado | Últ. 10 |
|---|---|---|---|---|---|
| Dejounte Murray | **más de 2.5 asistencias** | **90%** | 1.11 | 6.4 | 10/10 |
| Zion Williamson | **más de 14.5 puntos** | **89%** | 1.12 | 22.1 | 9/10 |
| Dejounte Murray | **más de 22.5 pts+reb+ast** | **87%** | 1.15 | 30.5 | 9/10 |
| Lauri Markkanen | **más de 11.5 puntos** | **86%** | 1.16 | 22.5 | 9/10 |
| Trey Murphy III | **más de 9.5 puntos** | **86%** | 1.16 | 18.4 | 8/10 |
| Ace Bailey | **más de 2.5 rebotes** | **85%** | 1.17 | 6.2 | 10/10 |

Las 8 más probables (máximo 2 por jugador: las de un mismo jugador suelen ganar o perder juntas).

| Prop | Prob. final | Modelo | Casa | Esperado | Últ. 10 | Temporada | vs este rival | Cuota (implícita) |
|---|---|---|---|---|---|---|---|---|
| **Herbert Jones: más de 0.5 triples** | **67%** | 68% | 66% | 1.2 ± 1.1 | 7/10 | 4/7 | 1, 3, 2 | 1.41 (71%) |
| **Ace Bailey: más de 1.5 asistencias** | **64%** | 69% | 60% | 2.6 ± 1.7 | 7/10 | 5/7 | 2, 2, 1 | 1.56 (64%) |
| **Keyonte George: menos de 6.5 asistencias** | **62%** | 69% | 57% | 5.3 ± 2.9 | 8/10 | 5/7 | 10, 4 | 1.64 (61%) |
| **Keyonte George: menos de 2.5 triples** | **60%** | 63% | 58% | 2.2 ± 1.7 | 7/10 | 4/7 | 3, 1 | 1.62 (62%) |
| **Dejounte Murray: menos de 1.5 triples** | **60%** | 60% | 59% | 1.4 ± 1.2 | 8/10 | 3/4 | 0, 2 | 1.58 (63%) |
| **Jeremiah Fears: menos de 1.5 triples** | **59%** | 55% | 62% | 1.6 ± 1.3 | 8/10 | 6/7 | 1, 1, 2, 2 | 1.52 (66%) |
| **Zion Williamson: más de 2.5 asistencias** | **58%** | 57% | 58% | 3.1 ± 1.8 | 5/10 | 3/7 | 2, 2, 4 | 1.61 (62%) |
| **Trey Murphy III: más de 4.5 rebotes** | **57%** | 63% | 53% | 5.4 ± 2.4 | 7/10 | 5/7 | 6 | 1.77 (56%) |

### Fichas de los jugadores destacados

#### Herbert Jones (aleros/ala-pívots) vs Utah Jazz

- Minutos esperados: **23.9** (± 5.7); 63 partidos en la base.
- Yves Missi ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- cambio de rol esta temporada (por minuto): ast -54%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Herbert Jones: más de 0.5 triples** (67%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Utah Jazz contra aleros/ala-pívots en triples: +7% respecto a la media; ajuste por su historial contra defensas similares: +2%.

**¿Por qué 1.2 triples?** (línea 0.5; 23.9 minutos esperados)

Razonamiento (7 factores a favor, 1 en contra):

- ✅ Minutos: 23.9 esperados (titular, ±5.7).
- ✅ Forma: 0.8 en sus últimos 5, 0.9 esta temporada (7 partidos), 1.4 la temporada pasada (línea 0.5).
- ➖ Cómo produce triples: 3.8 triples intentados (su ritmo 5.2 por 36'; el rival concede +7% de triples en su reparto) × 33% esperado.
- ✅ Defensa: el rival concede +10% de triples por minuto a aleros/ala-pívots (defensa débil); ajuste aplicado +7%; en su zona principal (triple) el rival concede 37% (liga 35%).
- ❌ Altura: mide 6'7", 2.5 pulgadas menos que los aleros/ala-pívots del rival (-0.9% en esta estadística).
- ✅ Ritmo del partido: +3% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 1, 3, 2 (3 de 3 a favor).
- ✅ Últimos 10: la habría pasado 7 de 10.
- ✅ Bajas del rival: sin Jaren Jackson Jr. (titular); +1.7% en esta estadística.
- ⚠️ Yves Missi ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ cambio de rol esta temporada (por minuto): ast -54%; se da más peso a la línea de la casa.

- Triples **1.2** (por componentes 1.3 · por tasa por minuto y defensa rival 1.2): 3.8 triples intentados (su ritmo 5.2 por 36'; el rival concede +7% de triples en su reparto) × 33% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 24.0 | 20.3 | 22.1 | 28.4 | 26.7 |
| Triples anotados | 0.8 | 1.0 | 0.9 | 1.4 | 2.0 |
| Triples intentados | 3.2 | 2.9 | 2.7 | 4.6 | 4.3 |
| % triples | 25.0% | 34.5% | 31.6% | 30.9% | 46.2% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +0%, vs defensa media -8%, vs defensa débil +9%; rebotes: vs defensa fuerte +7%, vs defensa media -5%, vs defensa débil -7%; asistencias: vs defensa fuerte -7%, vs defensa media +10%, vs defensa débil -4%; triples: vs defensa fuerte -6%, vs defensa media -17%, vs defensa débil +33%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 35% | 31% | 35% | 37% |
| bajo el aro | 28% | 60% | 68% | 72% |
| triple de esquina | 17% | 35% | 38% | 38% |
| pintura | 15% | 40% | 45% | 49% |
| media distancia | 5% | 40% | 41% | 42% |

#### Ace Bailey (bases/escoltas) vs New Orleans Pelicans

- Minutos esperados: **30.9** (± 6.6); 79 partidos en la base.
- Jusuf Nurkic ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Jaren Jackson Jr. ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- cambio de rol esta temporada (por minuto): reb +66%, tpm -31%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Ace Bailey: más de 1.5 asistencias** (64%). Con 80% de probabilidad: más de 0.5 / menos de 4.5.
- Defensa de New Orleans Pelicans contra bases/escoltas en asistencias: +6% respecto a la media; ajuste por su historial contra defensas similares: +2%.

**¿Por qué 2.6 asistencias?** (línea 1.5; 30.9 minutos esperados)

Razonamiento (5 factores a favor, 1 en contra):

- ❌ Minutos: 30.9 esperados (titular, ±6.6).
- ✅ Forma: 2.0 en sus últimos 5, 2.1 esta temporada (7 partidos), 1.9 la temporada pasada (línea 1.5).
- ➖ Cómo produce asistencias: asiste el 11.6% de las canastas de sus compañeros en pista × 22.0 canastas de compañeros esperadas (su equipo 43.3 por 48' contra esta defensa).
- ✅ Defensa: el rival concede +6% de asistencias por minuto a bases/escoltas (defensa débil); ajuste aplicado +6%.
- ✅ Ritmo del partido: +3% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 2, 2, 1 (2 de 3 a favor).
- ✅ Últimos 10: la habría pasado 7 de 10.
- ⚠️ Jusuf Nurkic ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ Jaren Jackson Jr. ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ cambio de rol esta temporada (por minuto): reb +66%, tpm -31%; se da más peso a la línea de la casa.

- ⚠️ Alertas: minutos inestables.
- Asistencias **2.6** (por componentes 2.6 · por tasa por minuto y defensa rival 2.6): asiste el 11.6% de las canastas de sus compañeros en pista × 22.0 canastas de compañeros esperadas (su equipo 43.3 por 48' contra esta defensa).

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 32.8 | 30.1 | 30.0 | 27.6 | 27.0 |
| Asistencias | 2.0 | 2.0 | 2.1 | 1.8 | 1.7 |
| % de las canastas de compañeros que asiste | 9.7% | 9.4% | 11.0% | 8.7% | 8.6% |
| Pérdidas por jugada | 12.9% | 12.9% | 12.0% | 10.3% | 8.3% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -6%, vs defensa media -2%, vs defensa débil +9%; rebotes: vs defensa fuerte +4%, vs defensa media -7%, vs defensa débil +1%; asistencias: vs defensa fuerte +2%, vs defensa media -5%, vs defensa débil +3%; triples: vs defensa fuerte -1%, vs defensa media -2%, vs defensa débil +3%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 32% | 35% | 35% | 34% |
| media distancia | 21% | 37% | 41% | 41% |
| bajo el aro | 19% | 69% | 68% | 68% |
| pintura | 15% | 54% | 45% | 49% |
| triple de esquina | 13% | 33% | 38% | 37% |

#### Keyonte George (bases/escoltas) vs New Orleans Pelicans

- Minutos esperados: **29.6** (± 5.2); 61 partidos en la base.
- Jusuf Nurkic ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Jaren Jackson Jr. ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Su prop más probable hoy: **Keyonte George: menos de 6.5 asistencias** (62%). Con 80% de probabilidad: más de 2.5 / menos de 8.5.
- Defensa de New Orleans Pelicans contra bases/escoltas en asistencias: +6% respecto a la media; ajuste por su historial contra defensas similares: +5%.

**¿Por qué 5.3 asistencias?** (línea 6.5; 29.6 minutos esperados)

Razonamiento (3 factores a favor, 2 en contra):

- ✅ Minutos: 29.6 esperados (titular, ±5.2).
- ✅ Forma: 4.6 en sus últimos 5, 5.4 esta temporada (7 partidos), 6.1 la temporada pasada (línea 6.5).
- ➖ Cómo produce asistencias: asiste el 24.1% de las canastas de sus compañeros en pista × 20.2 canastas de compañeros esperadas (su equipo 43.3 por 48' contra esta defensa).
- ❌ Defensa: el rival concede +6% de asistencias por minuto a bases/escoltas (defensa débil); ajuste aplicado +6%.
- ❌ Ritmo del partido: +3% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ➖ Contra este rival: 10, 4 (1 de 2 a favor).
- ✅ Últimos 10: la habría pasado 8 de 10.
- ⚠️ Jusuf Nurkic ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ Jaren Jackson Jr. ya no jugó en sus últimos partidos: la baja ya está en sus minutos.

- Asistencias **5.3** (por componentes 4.9 · por tasa por minuto y defensa rival 5.5): asiste el 24.1% de las canastas de sus compañeros en pista × 20.2 canastas de compañeros esperadas (su equipo 43.3 por 48' contra esta defensa).

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 30.8 | 28.8 | 30.7 | 33.1 | 27.5 |
| Asistencias | 4.6 | 4.9 | 5.4 | 6.1 | 7.0 |
| % de las canastas de compañeros que asiste | 23.8% | 26.4% | 27.7% | 26.2% | 37.5% |
| Pérdidas por jugada | 17.3% | 14.6% | 18.3% | 13.7% | 16.6% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -1%, vs defensa media +3%, vs defensa débil -3%; rebotes: vs defensa fuerte -5%, vs defensa media +11%, vs defensa débil -6%; asistencias: vs defensa fuerte -9%, vs defensa media +3%, vs defensa débil +9%; triples: vs defensa fuerte +2%, vs defensa media +14%, vs defensa débil -21%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 36% | 36% | 35% | 34% |
| pintura | 29% | 48% | 45% | 49% |
| media distancia | 17% | 43% | 41% | 41% |
| bajo el aro | 13% | 69% | 68% | 68% |
| triple de esquina | 5% | 39% | 38% | 37% |

#### Dejounte Murray (bases/escoltas) vs Utah Jazz

- Minutos esperados: **31.9** (± 3.0); 18 partidos en la base.
- sin Yves Missi (4 partidos): 29.0 min vs 28.8 con él; reb -5%/min
- cambio de rol esta temporada (por minuto): tpm -52%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Dejounte Murray: menos de 1.5 triples** (60%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Utah Jazz contra bases/escoltas en triples: +9% respecto a la media; ajuste por su historial contra defensas similares: -1%.

**¿Por qué 1.4 triples?** (línea 1.5; 31.9 minutos esperados)

Razonamiento (4 factores a favor, 3 en contra):

- ✅ Minutos: 31.9 esperados (titular, ±3.0).
- ✅ Forma: 0.6 en sus últimos 5, 0.8 esta temporada (4 partidos), 1.4 la temporada pasada (línea 1.5).
- ➖ Cómo produce triples: 4.7 triples intentados (su ritmo 5.3 por 36'; el rival concede +7% de triples en su reparto) × 33% esperado.
- ❌ Defensa: el rival concede +15% de triples por minuto a bases/escoltas (defensa débil); ajuste aplicado +9%; en su zona principal (triple) el rival concede 37% (liga 35%).
- ✅ Altura: mide 6'4", 1.8 pulgadas menos que los bases/escoltas del rival (-0.6% en esta estadística).
- ❌ Ritmo del partido: +3% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ➖ Contra este rival: 0, 2 (1 de 2 a favor).
- ✅ Últimos 10: la habría pasado 8 de 10.
- ❌ Bajas del rival: sin Jaren Jackson Jr. (titular); +1.7% en esta estadística.
- ⚠️ sin Yves Missi (4 partidos): 29.0 min vs 28.8 con él; reb -5%/min.
- ⚠️ cambio de rol esta temporada (por minuto): tpm -52%; se da más peso a la línea de la casa.

- ⚠️ Alertas: cambio de rol.
- Triples **1.4** (por componentes 1.6 · por tasa por minuto y defensa rival 1.3): 4.7 triples intentados (su ritmo 5.3 por 36'; el rival concede +7% de triples en su reparto) × 33% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 31.4 | 30.2 | 32.2 | 27.9 | 28.0 |
| Triples anotados | 0.6 | 0.9 | 0.8 | 1.4 | 1.0 |
| Triples intentados | 3.4 | 4.0 | 3.8 | 4.4 | 4.5 |
| % triples | 17.6% | 22.5% | 20.0% | 30.6% | 22.2% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -1%, vs defensa media -12%, vs defensa débil +12%; rebotes: vs defensa fuerte +6%, vs defensa media +7%, vs defensa débil -29%; asistencias: vs defensa fuerte -6%, vs defensa media +3%, vs defensa débil +6%; triples: vs defensa fuerte -59%, vs defensa media +12%, vs defensa débil +31%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 31% | 66% | 68% | 72% |
| pintura | 22% | 49% | 45% | 49% |
| triple frontal | 21% | 33% | 35% | 37% |
| media distancia | 16% | 45% | 41% | 42% |
| triple de esquina | 10% | 31% | 38% | 38% |

#### Jeremiah Fears (bases/escoltas) vs Utah Jazz

- Minutos esperados: **29.7** (± 6.0); 89 partidos en la base.
- Yves Missi ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- cambio de rol esta temporada (por minuto): ast +35%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Jeremiah Fears: menos de 1.5 triples** (59%). Con 80% de probabilidad: más de - / menos de 3.5.
- Defensa de Utah Jazz contra bases/escoltas en triples: +10% respecto a la media; ajuste por su historial contra defensas similares: +1%.

**¿Por qué 1.6 triples?** (línea 1.5; 29.7 minutos esperados)

Razonamiento (3 factores a favor, 4 en contra):

- ❌ Minutos: 29.7 esperados (titular, ±6.0).
- ✅ Forma: 1.0 en sus últimos 5, 1.0 esta temporada (7 partidos), 1.2 la temporada pasada (línea 1.5).
- ➖ Cómo produce triples: 5.2 triples intentados (su ritmo 5.8 por 36'; el rival concede +7% de triples en su reparto) × 33% esperado.
- ❌ Defensa: el rival concede +15% de triples por minuto a bases/escoltas (defensa débil); ajuste aplicado +10%; en su zona principal (triple) el rival concede 37% (liga 35%).
- ✅ Altura: mide 6'3", 2.8 pulgadas menos que los bases/escoltas del rival (-1.0% en esta estadística).
- ❌ Ritmo del partido: +3% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ➖ Contra este rival: 1, 1, 2, 2 (2 de 4 a favor).
- ✅ Últimos 10: la habría pasado 8 de 10.
- ❌ Bajas del rival: sin Jaren Jackson Jr. (titular); +1.7% en esta estadística.
- ⚠️ Yves Missi ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ cambio de rol esta temporada (por minuto): ast +35%; se da más peso a la línea de la casa.

- ⚠️ Alertas: minutos inestables.
- Triples **1.6** (por componentes 1.7 · por tasa por minuto y defensa rival 1.5): 5.2 triples intentados (su ritmo 5.8 por 36'; el rival concede +7% de triples en su reparto) × 33% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 29.0 | 31.3 | 27.1 | 25.7 | 29.5 |
| Triples anotados | 1.0 | 1.1 | 1.0 | 1.2 | 1.5 |
| Triples intentados | 4.0 | 5.1 | 4.1 | 3.7 | 5.8 |
| % triples | 25.0% | 21.6% | 24.1% | 33.0% | 26.1% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -9%, vs defensa media +6%, vs defensa débil +1%; rebotes: vs defensa fuerte -10%, vs defensa media +1%, vs defensa débil +7%; asistencias: vs defensa fuerte -13%, vs defensa media -3%, vs defensa débil +18%; triples: vs defensa fuerte -23%, vs defensa media -13%, vs defensa débil +41%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 37% | 60% | 68% | 72% |
| triple frontal | 26% | 30% | 35% | 37% |
| pintura | 23% | 38% | 45% | 49% |
| media distancia | 9% | 34% | 41% | 42% |
| triple de esquina | 5% | 41% | 38% | 38% |

## Cleveland Cavaliers @ Oklahoma City Thunder

Diferencia esperada: Oklahoma City Thunder por 3.5.

Parte de lesiones: Jaylin Williams (Day-To-Day); Chet Holmgren (Out); Peyton Watson (Out); Cason Wallace (Out); Jaylon Tyson (Out); Thomas Sorber (Out); Nikola Topic (Out).

Ventajas del partido (los dos lados): puntos esperados frente a su media de los últimos 10, ajuste por la defensa rival y diferencia de estatura con los rivales de su posición.

| Equipo | Jugador | Puntos esperados | Su media (últ. 10) | Defensa rival en puntos | Rebotes esperados | Altura vs rival |
|---|---|---|---|---|---|---|
| OKC | Shai Gilgeous-Alexander | 26.9 | 28.1 | -2% | 3.9 | +1.8" |
| CLE | James Harden | 16.8 | 15.9 | -4% | 4.6 | +0.3" |
| OKC | Jalen Williams | 17.6 | 14.6 | -2% | 4.8 | +0.8" |
| CLE | Donovan Mitchell | 21.0 | 23.9 | -4% | 4.8 | -2.7" |
| CLE | Evan Mobley | 16.2 | 17.8 | -7% | 8.0 | -2.0" |
| OKC | Ajay Mitchell | 15.3 | 13.5 | -2% | 3.6 | -0.2" |
| CLE | Jarrett Allen | 13.3 | 13.5 | -8% | 8.0 | -4.0" |
| OKC | Jared McCain | 12.1 | 11.7 | -1% | 3.3 | -1.2" |
| OKC | Isaiah Hartenstein | 9.6 | 9.1 | -3% | 10.2 | +2.0" |
| CLE | Sam Merrill | 9.7 | 8.0 | -3% | 2.8 | -0.7" |

Picks seguros de titulares estables:

| Jugador | Pick seguro | Prob. | Cuota mínima | Esperado | Últ. 10 |
|---|---|---|---|---|---|
| Shai Gilgeous-Alexander | **más de 1.5 asistencias** | **90%** | 1.11 | 4.9 | 10/10 |
| Evan Mobley | **más de 18.5 pts+reb+ast** | **87%** | 1.15 | 27.4 | 10/10 |
| James Harden | **más de 10.5 puntos** | **86%** | 1.16 | 16.8 | 10/10 |
| James Harden | **más de 2.5 asistencias** | **86%** | 1.16 | 5.6 | 8/10 |
| Donovan Mitchell | **más de 21.5 pts+reb+ast** | **86%** | 1.16 | 30.5 | 10/10 |
| Evan Mobley | **más de 4.5 rebotes** | **86%** | 1.17 | 8.0 | 9/10 |

Las 8 más probables (máximo 2 por jugador: las de un mismo jugador suelen ganar o perder juntas).

| Prop | Prob. final | Modelo | Casa | Esperado | Últ. 10 | Temporada | vs este rival | Cuota (implícita) |
|---|---|---|---|---|---|---|---|---|
| **Jaylin Williams: menos de 6.5 rebotes** ⚠️ suplente | **66%** | 76% | 57% | 4.6 ± 2.6 | 7/10 | 6/7 | 3, 3, 3 | 1.63 (61%) |
| **Ajay Mitchell: menos de 1.5 triples** | **65%** | 72% | 60% | 1.0 ± 1.0 | 9/10 | 6/7 | 0, 0 | 1.56 (64%) |
| **Jaylin Williams: menos de 2.5 asistencias** ⚠️ suplente | **65%** | 69% | 61% | 1.9 ± 1.5 | 7/10 | 5/7 | 2, 0, 2 | 1.53 (65%) |
| **Isaiah Hartenstein: menos de 3.5 asistencias** | **63%** | 72% | 57% | 2.4 ± 1.8 | 8/10 | 6/7 | 4, 4 | 1.63 (61%) |
| **Shai Gilgeous-Alexander: menos de 2.5 triples** | **63%** | 64% | 62% | 2.1 ± 1.5 | 6/10 | 3/7 | 4, 1 | 1.50 (67%) |
| **Jared McCain: menos de 2.5 triples** | **61%** | 68% | 56% | 1.9 ± 2.2 | 7/10 | 5/7 | 0, 2, 0 | 1.68 (60%) |
| **Sam Merrill: menos de 2.5 triples** ⚠️ suplente | **60%** | 67% | 56% | 2.1 ± 1.5 | 8/10 | 6/7 | 2, 6 | 1.69 (59%) |
| **Donovan Mitchell: menos de 5.5 asistencias** | **60%** | 67% | 55% | 4.6 ± 2.7 | 7/10 | 4/7 | 11, 5, 3 | 1.72 (58%) |

### Fichas de los jugadores destacados

#### Jaylin Williams (aleros/ala-pívots) vs Cleveland Cavaliers

- Minutos esperados: **19.9** (± 6.1); 87 partidos en la base.
- en el parte de lesiones: day-to-day
- Chet Holmgren ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Cason Wallace ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- cambio de rol esta temporada (por minuto): pts -57%, tpm -49%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Jaylin Williams: menos de 6.5 rebotes** (66%). Con 80% de probabilidad: más de 1.5 / menos de 7.5.
- Defensa de Cleveland Cavaliers contra aleros/ala-pívots en rebotes: -2% respecto a la media; ajuste por su historial contra defensas similares: -0%.

**¿Por qué 4.6 rebotes?** (línea 6.5; 19.9 minutos esperados)

Razonamiento (3 factores a favor, 1 en contra):

- ❌ Minutos: 19.9 esperados (suplente, ±6.1).
- ✅ Forma: 3.6 en sus últimos 5, 4.1 esta temporada (7 partidos), 5.5 la temporada pasada (línea 6.5).
- ➖ Cómo produce rebotes: defensivos 4.0 = captura el 20.1% de los fallos del rival en pista × 48.2 fallos esperados del rival (liga 47.0) × 41% del partido; ofensivos 0.5 = 2.6% de los fallos de su equipo × 47.2.
- ➖ Defensa: el rival concede -2% de rebotes por minuto a aleros/ala-pívots (defensa media); ajuste aplicado -2%.
- ➖ Ritmo del partido: -0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 3, 3, 3 (3 de 3 a favor).
- ✅ Últimos 10: la habría pasado 7 de 10.
- ⚠️ en el parte de lesiones: day-to-day.
- ⚠️ Chet Holmgren ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ Cason Wallace ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ cambio de rol esta temporada (por minuto): pts -57%, tpm -49%; se da más peso a la línea de la casa.

- ⚠️ Alertas: suplente, minutos inestables, en el parte de lesiones.
- Rebotes **4.6** (por componentes 4.5 · por tasa por minuto y defensa rival 4.6): defensivos 4.0 = captura el 20.1% de los fallos del rival en pista × 48.2 fallos esperados del rival (liga 47.0) × 41% del partido; ofensivos 0.5 = 2.6% de los fallos de su equipo × 47.2.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 19.4 | 19.8 | 18.4 | 19.0 | 15.0 |
| Rebotes | 3.6 | 5.2 | 4.1 | 5.2 | 3.0 |
| % de los fallos del rival que captura | 16.8% | 22.1% | 19.7% | 24.3% | 17.2% |
| % de los fallos de su equipo que captura | 1.0% | 2.9% | 1.5% | 2.7% | 2.2% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -5%, vs defensa media -0%, vs defensa débil +9%; rebotes: vs defensa fuerte -7%, vs defensa media +10%, vs defensa débil +5%; asistencias: vs defensa fuerte -17%, vs defensa media +5%, vs defensa débil +18%; triples: vs defensa fuerte -34%, vs defensa media +15%, vs defensa débil +42%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 54% | 36% | 35% | 36% |
| triple de esquina | 19% | 34% | 38% | 39% |
| bajo el aro | 12% | 61% | 68% | 64% |
| pintura | 9% | 45% | 45% | 44% |
| media distancia | 5% | 42% | 41% | 41% |

#### Ajay Mitchell (bases/escoltas) vs Cleveland Cavaliers

- Minutos esperados: **28.2** (± 4.3); 75 partidos en la base.
- Chet Holmgren ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Cason Wallace ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- cambio de rol esta temporada (por minuto): tpm -49%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Ajay Mitchell: menos de 1.5 triples** (65%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Cleveland Cavaliers contra bases/escoltas en triples: +3% respecto a la media; ajuste por su historial contra defensas similares: -5%.

**¿Por qué 1.0 triples?** (línea 1.5; 28.2 minutos esperados)

Razonamiento (4 factores a favor, 1 en contra):

- ✅ Minutos: 28.2 esperados (titular, ±4.3).
- ✅ Forma: 0.8 en sus últimos 5, 0.6 esta temporada (7 partidos), 1.1 la temporada pasada (línea 1.5).
- ➖ Cómo produce triples: 3.7 triples intentados (su ritmo 4.6 por 36'; el rival concede +0% de triples en su reparto) × 34% esperado.
- ❌ Defensa: el rival concede +2% de triples por minuto a bases/escoltas (defensa media); ajuste aplicado +3%; en su zona principal (triple) el rival concede 36% (liga 35%).
- ➖ Ritmo del partido: -0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 0, 0 (2 de 2 a favor).
- ✅ Últimos 10: la habría pasado 9 de 10.
- ⚠️ Chet Holmgren ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ Cason Wallace ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ cambio de rol esta temporada (por minuto): tpm -49%; se da más peso a la línea de la casa.

- ⚠️ Alertas: cambio de rol.
- Triples **1.0** (por componentes 1.2 · por tasa por minuto y defensa rival 0.9): 3.7 triples intentados (su ritmo 4.6 por 36'; el rival concede +0% de triples en su reparto) × 34% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 28.4 | 26.7 | 26.9 | 26.3 | 30.0 |
| Triples anotados | 0.8 | 0.4 | 0.6 | 1.1 | 0.0 |
| Triples intentados | 3.2 | 2.5 | 3.0 | 3.2 | 2.0 |
| % triples | 25.0% | 16.0% | 19.0% | 34.3% | 0.0% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -24%, vs defensa media +20%, vs defensa débil -3%; rebotes: vs defensa fuerte +0%, vs defensa media +3%, vs defensa débil -4%; asistencias: vs defensa fuerte -1%, vs defensa media -4%, vs defensa débil +5%; triples: vs defensa fuerte -23%, vs defensa media +19%, vs defensa débil +2%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| pintura | 34% | 50% | 45% | 44% |
| bajo el aro | 28% | 66% | 68% | 64% |
| triple frontal | 21% | 31% | 35% | 36% |
| media distancia | 10% | 39% | 41% | 41% |
| triple de esquina | 8% | 39% | 38% | 39% |

#### Isaiah Hartenstein (pívots) vs Cleveland Cavaliers

- Minutos esperados: **25.5** (± 3.0); 69 partidos en la base.
- Chet Holmgren ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Cason Wallace ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- cambio de rol esta temporada (por minuto): ast -32%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Isaiah Hartenstein: menos de 3.5 asistencias** (63%). Con 80% de probabilidad: más de 0.5 / menos de 4.5.
- Defensa de Cleveland Cavaliers contra pívots en asistencias: -5% respecto a la media; ajuste por su historial contra defensas similares: -3%.

**¿Por qué 2.4 asistencias?** (línea 3.5; 25.5 minutos esperados)

Razonamiento (4 factores a favor, 1 en contra):

- ✅ Minutos: 25.5 esperados (titular, ±3.0).
- ✅ Forma: 2.2 en sus últimos 5, 2.3 esta temporada (7 partidos), 3.3 la temporada pasada (línea 3.5).
- ➖ Cómo produce asistencias: asiste el 13.4% de las canastas de sus compañeros en pista × 17.9 canastas de compañeros esperadas (su equipo 41.9 por 48' contra esta defensa).
- ✅ Defensa: el rival concede -5% de asistencias por minuto a pívots (defensa fuerte); ajuste aplicado -5%.
- ➖ Ritmo del partido: -0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ❌ Contra este rival: 4, 4 (0 de 2 a favor).
- ✅ Últimos 10: la habría pasado 8 de 10.
- ⚠️ Chet Holmgren ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ Cason Wallace ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ cambio de rol esta temporada (por minuto): ast -32%; se da más peso a la línea de la casa.

- ⚠️ Alertas: cambio de rol.
- Asistencias **2.4** (por componentes 2.4 · por tasa por minuto y defensa rival 2.5): asiste el 13.4% de las canastas de sus compañeros en pista × 17.9 canastas de compañeros esperadas (su equipo 41.9 por 48' contra esta defensa).

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 26.4 | 24.0 | 24.6 | 24.1 | 27.0 |
| Asistencias | 2.2 | 2.3 | 2.3 | 3.3 | 4.0 |
| % de las canastas de compañeros que asiste | 11.0% | 13.0% | 12.3% | 17.2% | 18.7% |
| Pérdidas por jugada | 15.5% | 17.0% | 17.2% | 19.5% | 10.7% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -24%, vs defensa media +3%, vs defensa débil +14%; rebotes: vs defensa fuerte -8%, vs defensa media -4%, vs defensa débil +10%; asistencias: vs defensa fuerte -10%, vs defensa media +38%, vs defensa débil -16%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 53% | 71% | 68% | 64% |
| pintura | 39% | 47% | 45% | 44% |
| media distancia | 5% | 42% | 41% | 41% |
| triple frontal | 2% | 30% | 35% | 36% |
| triple de esquina | 1% | 35% | 38% | 39% |

#### Shai Gilgeous-Alexander (bases/escoltas) vs Cleveland Cavaliers

- Minutos esperados: **33.6** (± 4.2); 90 partidos en la base.
- Chet Holmgren ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Cason Wallace ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- cambio de rol esta temporada (por minuto): ast -41%, tpm +44%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Shai Gilgeous-Alexander: menos de 2.5 triples** (63%). Con 80% de probabilidad: más de 0.5 / menos de 3.5.
- Defensa de Cleveland Cavaliers contra bases/escoltas en triples: +2% respecto a la media; ajuste por su historial contra defensas similares: +3%.

**¿Por qué 2.1 triples?** (línea 2.5; 33.6 minutos esperados)

Razonamiento (2 factores a favor, 2 en contra):

- ✅ Minutos: 33.6 esperados (titular, ±4.2).
- ✅ Forma: 2.0 en sus últimos 5, 2.3 esta temporada (7 partidos), 1.4 la temporada pasada (línea 2.5).
- ➖ Cómo produce triples: 5.8 triples intentados (su ritmo 6.2 por 36'; el rival concede +0% de triples en su reparto) × 38% esperado.
- ❌ Defensa: el rival concede +2% de triples por minuto a bases/escoltas (defensa media); ajuste aplicado +2%; en su zona principal (triple) el rival concede 36% (liga 35%).
- ❌ Altura: mide 6'6", 1.8 pulgadas más que los bases/escoltas del rival (+0.6% en esta estadística).
- ➖ Ritmo del partido: -0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ➖ Contra este rival: 4, 1 (1 de 2 a favor).
- ➖ Últimos 10: la habría pasado 6 de 10.
- ⚠️ Chet Holmgren ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ Cason Wallace ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ cambio de rol esta temporada (por minuto): ast -41%, tpm +44%; se da más peso a la línea de la casa.

- ⚠️ Alertas: cambio de rol.
- Triples **2.1** (por componentes 2.2 · por tasa por minuto y defensa rival 2.1): 5.8 triples intentados (su ritmo 6.2 por 36'; el rival concede +0% de triples en su reparto) × 38% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 32.8 | 34.3 | 33.6 | 33.8 | 36.5 |
| Triples anotados | 2.0 | 2.0 | 2.3 | 1.6 | 2.5 |
| Triples intentados | 6.0 | 6.1 | 6.9 | 4.3 | 6.0 |
| % triples | 33.3% | 32.8% | 33.3% | 37.3% | 41.7% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -8%, vs defensa media +1%, vs defensa débil +9%; rebotes: vs defensa fuerte -7%, vs defensa media -11%, vs defensa débil +28%; asistencias: vs defensa fuerte -4%, vs defensa media +8%, vs defensa débil -0%; triples: vs defensa fuerte -11%, vs defensa media +4%, vs defensa débil +16%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| media distancia | 28% | 50% | 41% | 41% |
| pintura | 25% | 51% | 45% | 44% |
| bajo el aro | 23% | 70% | 68% | 64% |
| triple frontal | 22% | 37% | 35% | 36% |
| triple de esquina | 1% | 35% | 38% | 39% |

#### Jared McCain (bases/escoltas) vs Cleveland Cavaliers

- Minutos esperados: **26.2** (± 3.7); 88 partidos en la base.
- Chet Holmgren ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Cason Wallace ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Su prop más probable hoy: **Jared McCain: menos de 2.5 triples** (61%). Con 80% de probabilidad: más de - / menos de 3.5.
- Defensa de Cleveland Cavaliers contra bases/escoltas en triples: +3% respecto a la media; ajuste por su historial contra defensas similares: -3%.

**¿Por qué 1.9 triples?** (línea 2.5; 26.2 minutos esperados)

Razonamiento (4 factores a favor, 1 en contra):

- ✅ Minutos: 26.2 esperados (titular, ±3.7).
- ✅ Forma: 1.0 en sus últimos 5, 1.6 esta temporada (7 partidos), 1.6 la temporada pasada (línea 2.5).
- ➖ Cómo produce triples: 5.8 triples intentados (su ritmo 7.9 por 36'; el rival concede +0% de triples en su reparto) × 37% esperado.
- ❌ Defensa: el rival concede +2% de triples por minuto a bases/escoltas (defensa media); ajuste aplicado +3%; en su zona principal (triple) el rival concede 36% (liga 35%).
- ➖ Ritmo del partido: -0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 0, 2, 0 (3 de 3 a favor).
- ✅ Últimos 10: la habría pasado 7 de 10.
- ⚠️ Chet Holmgren ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ Cason Wallace ya no jugó en sus últimos partidos: la baja ya está en sus minutos.

- Triples **1.9** (por componentes 2.2 · por tasa por minuto y defensa rival 1.8): 5.8 triples intentados (su ritmo 7.9 por 36'; el rival concede +0% de triples en su reparto) × 37% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 27.0 | 25.8 | 25.0 | 17.5 | 17.7 |
| Triples anotados | 1.0 | 1.8 | 1.6 | 1.5 | 0.7 |
| Triples intentados | 5.6 | 5.8 | 5.6 | 4.0 | 2.7 |
| % triples | 17.9% | 31.0% | 28.2% | 38.2% | 25.0% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -1%, vs defensa media +8%, vs defensa débil -12%; rebotes: vs defensa fuerte -5%, vs defensa media +5%, vs defensa débil -2%; asistencias: vs defensa fuerte -19%, vs defensa media +24%, vs defensa débil +5%; triples: vs defensa fuerte -5%, vs defensa media +1%, vs defensa débil +7%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 38% | 36% | 35% | 36% |
| pintura | 21% | 40% | 45% | 44% |
| bajo el aro | 19% | 58% | 68% | 64% |
| triple de esquina | 14% | 36% | 38% | 39% |
| media distancia | 8% | 41% | 41% | 41% |

## Minnesota Timberwolves @ Houston Rockets

Diferencia esperada: Houston Rockets por 7.5.

Parte de lesiones: Steven Adams (Out); Clint Capela (Day-To-Day); Donte DiVincenzo (Out); Terrence Shannon Jr. (Day-To-Day); Anthony Edwards (Out).

Ventajas del partido (los dos lados): puntos esperados frente a su media de los últimos 10, ajuste por la defensa rival y diferencia de estatura con los rivales de su posición.

| Equipo | Jugador | Puntos esperados | Su media (últ. 10) | Defensa rival en puntos | Rebotes esperados | Altura vs rival |
|---|---|---|---|---|---|---|
| HOU | Alperen Sengun | 21.0 | 22.3 | -2% | 9.1 | -1.2" |
| HOU | Jabari Smith Jr. | 17.0 | 17.8 | -2% | 6.5 | +2.3" |
| MIN | Jaden McDaniels | 17.0 | 16.4 | -3% | 4.7 | -0.8" |
| HOU | Kevin Durant | 20.0 | 22.2 | -3% | 5.3 | +2.3" |
| MIN | Ayo Dosunmu | 16.9 | 15.2 | -3% | 5.0 | +0.1" |
| MIN | Jonathan Kuminga | 14.5 | 12.2 | -3% | 5.4 | -2.8" |
| HOU | Amen Thompson | 15.4 | 16.1 | -2% | 5.8 | +2.3" |
| MIN | Rudy Gobert | 11.9 | 6.7 | -3% | 10.8 | +2.5" |
| MIN | LaMelo Ball | 17.4 | 18.8 | -3% | 3.8 | +3.1" |
| HOU | Tari Eason | 10.7 | 11.5 | -2% | 6.0 | -0.7" |

Picks seguros de titulares estables:

| Jugador | Pick seguro | Prob. | Cuota mínima | Esperado | Últ. 10 |
|---|---|---|---|---|---|
| Jabari Smith Jr. | **más de 2.5 rebotes** | **89%** | 1.12 | 6.5 | 9/10 |
| Jaden McDaniels | **más de 16.5 pts+reb+ast** | **89%** | 1.12 | 24.6 | 10/10 |
| Amen Thompson | **más de 8.5 puntos** | **88%** | 1.14 | 15.4 | 9/10 |
| Kevin Durant | **más de 12.5 puntos** | **87%** | 1.15 | 20.0 | 9/10 |
| Jaden McDaniels | **más de 11.5 puntos** | **87%** | 1.15 | 17.0 | 10/10 |
| Ayo Dosunmu | **más de 9.5 puntos** | **87%** | 1.15 | 16.9 | 8/10 |

Las 8 más probables (máximo 2 por jugador: las de un mismo jugador suelen ganar o perder juntas).

| Prop | Prob. final | Modelo | Casa | Esperado | Últ. 10 | Temporada | vs este rival | Cuota (implícita) |
|---|---|---|---|---|---|---|---|---|
| **Tari Eason: menos de 1.5 triples** ⚠️ suplente | **66%** | 66% | 65% | 1.1 ± 1.2 | 6/10 | 6/8 | 0, 1 | 1.43 (70%) |
| **Marcus Smart: menos de 1.5 triples** ⚠️ suplente | **59%** | 58% | 61% | 1.5 ± 1.8 | 5/10 | 2/5 | 1, 1 | 1.55 (65%) |
| **LaMelo Ball: menos de 4.5 rebotes** | **59%** | 62% | 57% | 3.8 ± 2.5 | 6/10 | 5/8 | 7, 6 | 1.63 (61%) |
| **Ayo Dosunmu: menos de 4.5 asistencias** | **59%** | 64% | 54% | 4.0 ± 2.9 | 7/10 | 6/8 | 4, 3 | 1.73 (58%) |
| **LaMelo Ball: menos de 6.5 asistencias** | **58%** | 64% | 52% | 5.5 ± 2.6 | 6/10 | 5/8 | 7, 4 | 1.79 (56%) |
| **Jonathan Kuminga: menos de 5.5 rebotes** | **57%** | 59% | 56% | 5.4 ± 3.0 | 6/10 | 4/8 | - | 1.67 (60%) |
| **Rudy Gobert: más de 8.5 puntos** | **57%** | 63% | 52% | 11.9 ± 5.3 | 4/10 | 3/7 | 14, 10 | 1.77 (56%) |
| **Jonathan Kuminga: menos de 1.5 triples** | **56%** | 53% | 59% | 1.6 ± 1.3 | 4/10 | 2/8 | - | 1.59 (63%) |

### Fichas de los jugadores destacados

#### Tari Eason (aleros/ala-pívots) vs Minnesota Timberwolves

- Minutos esperados: **25.6** (± 6.8); 74 partidos en la base.
- Steven Adams ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- cambio de rol esta temporada (por minuto): tpm -40%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Tari Eason: menos de 1.5 triples** (66%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Minnesota Timberwolves contra aleros/ala-pívots en triples: -6% respecto a la media; ajuste por su historial contra defensas similares: -4%.

**¿Por qué 1.1 triples?** (línea 1.5; 25.6 minutos esperados)

Razonamiento (3 factores a favor, 2 en contra):

- ❌ Minutos: 25.6 esperados (suplente, ±6.8).
- ✅ Forma: 1.4 en sus últimos 5, 0.9 esta temporada (8 partidos), 1.5 la temporada pasada (línea 1.5).
- ➖ Cómo produce triples: 3.4 triples intentados (su ritmo 5.2 por 36'; el rival concede -8% de triples en su reparto) × 34% esperado.
- ✅ Defensa: el rival concede -10% de triples por minuto a aleros/ala-pívots (defensa fuerte); ajuste aplicado -6%; en su zona principal (esquina3) el rival concede 38% (liga 38%).
- ➖ Ritmo del partido: -1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 0, 1 (2 de 2 a favor).
- ➖ Últimos 10: la habría pasado 6 de 10.
- ❌ Bajas del rival: sin Anthony Edwards (titular); +1.7% en esta estadística.
- ⚠️ Steven Adams ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ cambio de rol esta temporada (por minuto): tpm -40%; se da más peso a la línea de la casa.

- ⚠️ Alertas: suplente, minutos inestables, cambio de rol.
- Triples **1.1** (por componentes 1.2 · por tasa por minuto y defensa rival 1.0): 3.4 triples intentados (su ritmo 5.2 por 36'; el rival concede -8% de triples en su reparto) × 34% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 27.2 | 26.5 | 24.6 | 26.5 | 22.5 |
| Triples anotados | 1.4 | 1.1 | 0.9 | 1.6 | 0.5 |
| Triples intentados | 4.0 | 3.8 | 3.1 | 4.4 | 2.0 |
| % triples | 35.0% | 28.9% | 28.0% | 35.5% | 25.0% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -12%, vs defensa media -8%, vs defensa débil +32%; rebotes: vs defensa fuerte -12%, vs defensa media +3%, vs defensa débil +12%; asistencias: vs defensa fuerte -15%, vs defensa media +19%, vs defensa débil -5%; triples: vs defensa fuerte -10%, vs defensa media -4%, vs defensa débil +21%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 30% | 68% | 68% | 66% |
| triple de esquina | 23% | 39% | 38% | 38% |
| triple frontal | 21% | 30% | 35% | 34% |
| pintura | 19% | 33% | 45% | 43% |
| media distancia | 7% | 33% | 41% | 39% |

#### Marcus Smart (bases/escoltas) vs Minnesota Timberwolves

- Minutos esperados: **24.6** (± 7.2); 77 partidos en la base.
- Steven Adams ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- cambio de rol esta temporada (por minuto): pts +37%, reb +36%, tpm +70%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Marcus Smart: menos de 1.5 triples** (59%). Con 80% de probabilidad: más de - / menos de 3.5.
- Defensa de Minnesota Timberwolves contra bases/escoltas en triples: -7% respecto a la media; ajuste por su historial contra defensas similares: -4%.

**¿Por qué 1.5 triples?** (línea 1.5; 24.6 minutos esperados)

Razonamiento (3 factores a favor, 3 en contra):

- ❌ Minutos: 24.6 esperados (suplente, ±7.2).
- ❌ Forma: 2.2 en sus últimos 5, 2.2 esta temporada (5 partidos), 1.7 la temporada pasada (línea 1.5).
- ➖ Cómo produce triples: 4.3 triples intentados (su ritmo 6.8 por 36'; el rival concede -8% de triples en su reparto) × 34% esperado.
- ✅ Defensa: el rival concede -11% de triples por minuto a bases/escoltas (defensa fuerte); ajuste aplicado -7%; en su zona principal (triple) el rival concede 34% (liga 35%).
- ✅ Altura: mide 6'3", 1.7 pulgadas menos que los bases/escoltas del rival (-0.6% en esta estadística).
- ➖ Ritmo del partido: -1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 1, 1 (2 de 2 a favor).
- ➖ Últimos 10: la habría pasado 5 de 10.
- ❌ Bajas del rival: sin Anthony Edwards (titular); +1.7% en esta estadística.
- ⚠️ Steven Adams ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ cambio de rol esta temporada (por minuto): pts +37%, reb +36%, tpm +70%; se da más peso a la línea de la casa.

- ⚠️ Alertas: suplente, minutos inestables, cambio de rol.
- Triples **1.5** (por componentes 1.4 · por tasa por minuto y defensa rival 1.5): 4.3 triples intentados (su ritmo 6.8 por 36'; el rival concede -8% de triples en su reparto) × 34% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 24.0 | 28.9 | 24.0 | 29.4 | 26.0 |
| Triples anotados | 2.2 | 1.7 | 2.2 | 1.6 | 1.0 |
| Triples intentados | 5.4 | 5.2 | 5.4 | 4.8 | 2.5 |
| % triples | 40.7% | 32.7% | 40.7% | 33.2% | 40.0% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +2%, vs defensa media +5%, vs defensa débil -6%; rebotes: vs defensa fuerte -8%, vs defensa media +12%, vs defensa débil -1%; asistencias: vs defensa fuerte +4%, vs defensa media -18%, vs defensa débil +12%; triples: vs defensa fuerte -4%, vs defensa media -0%, vs defensa débil +3%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 42% | 32% | 35% | 34% |
| pintura | 21% | 40% | 45% | 43% |
| triple de esquina | 19% | 39% | 38% | 38% |
| bajo el aro | 13% | 68% | 68% | 66% |
| media distancia | 5% | 44% | 41% | 39% |

#### LaMelo Ball (bases/escoltas) vs Houston Rockets

- Minutos esperados: **27.0** (± 5.5); 82 partidos en la base.
- Donte DiVincenzo ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- sin Anthony Edwards, la estrella de su equipo (4 partidos suyos sin él): más tiros y balón para él por minuto (puntos +4%, triples +3%, asistencias +5%)
- Anthony Edwards ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Su prop más probable hoy: **LaMelo Ball: menos de 4.5 rebotes** (59%). Con 80% de probabilidad: más de 1.5 / menos de 6.5.
- Defensa de Houston Rockets contra bases/escoltas en rebotes: -8% respecto a la media; ajuste por su historial contra defensas similares: -3%.

**¿Por qué 3.8 rebotes?** (línea 4.5; 27.0 minutos esperados)

Razonamiento (2 factores a favor, 2 en contra):

- ✅ Minutos: 27.0 esperados (titular, ±5.5).
- ➖ Forma: 4.4 en sus últimos 5, 3.8 esta temporada (8 partidos), 4.5 la temporada pasada (línea 4.5).
- ➖ Cómo produce rebotes: defensivos 3.0 = captura el 11.2% de los fallos del rival en pista × 47.0 fallos esperados del rival (liga 47.0) × 56% del partido; ofensivos 0.9 = 3.4% de los fallos de su equipo × 46.5.
- ✅ Defensa: el rival concede -8% de rebotes por minuto a bases/escoltas (defensa fuerte); ajuste aplicado -8%.
- ❌ Altura: mide 6'7", 3.1 pulgadas más que los bases/escoltas del rival (+1.1% en esta estadística).
- ➖ Ritmo del partido: -1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ❌ Contra este rival: 7, 6 (0 de 2 a favor).
- ➖ Últimos 10: la habría pasado 6 de 10.
- ⚠️ Donte DiVincenzo ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ sin Anthony Edwards, la estrella de su equipo (4 partidos suyos sin él): más tiros y balón para él por minuto (puntos +4%, triples +3%, asistencias +5%).
- ⚠️ Anthony Edwards ya no jugó en sus últimos partidos: la baja ya está en sus minutos.

- Rebotes **3.8** (por componentes 3.9 · por tasa por minuto y defensa rival 3.6): defensivos 3.0 = captura el 11.2% de los fallos del rival en pista × 47.0 fallos esperados del rival (liga 47.0) × 56% del partido; ofensivos 0.9 = 3.4% de los fallos de su equipo × 46.5.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 28.2 | 27.5 | 26.2 | 28.1 | 30.0 |
| Rebotes | 4.4 | 3.7 | 3.8 | 4.8 | 6.5 |
| % de los fallos del rival que captura | 11.2% | 9.9% | 10.0% | 14.3% | 21.6% |
| % de los fallos de su equipo que captura | 3.4% | 3.1% | 3.7% | 3.2% | 1.6% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -11%, vs defensa media +4%, vs defensa débil +8%; rebotes: vs defensa fuerte -0%, vs defensa media +9%, vs defensa débil -8%; asistencias: vs defensa fuerte -12%, vs defensa media +2%, vs defensa débil +12%; triples: vs defensa fuerte +5%, vs defensa media -13%, vs defensa débil +10%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 52% | 35% | 35% | 34% |
| pintura | 21% | 44% | 45% | 45% |
| bajo el aro | 13% | 61% | 68% | 67% |
| triple de esquina | 7% | 41% | 38% | 38% |
| media distancia | 6% | 38% | 41% | 40% |

#### Ayo Dosunmu (bases/escoltas) vs Houston Rockets

- Minutos esperados: **32.2** (± 5.1); 87 partidos en la base.
- Donte DiVincenzo ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- sin Anthony Edwards, la estrella de su equipo (12 partidos suyos sin él): más tiros y balón para él por minuto (puntos +4%, triples +0%, asistencias -0%)
- Anthony Edwards ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- cambio de rol esta temporada (por minuto): reb +55%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Ayo Dosunmu: menos de 4.5 asistencias** (59%). Con 80% de probabilidad: más de 0.5 / menos de 6.5.
- Defensa de Houston Rockets contra bases/escoltas en asistencias: -7% respecto a la media; ajuste por su historial contra defensas similares: +2%.

**¿Por qué 4.0 asistencias?** (línea 4.5; 32.2 minutos esperados)

Razonamiento (5 factores a favor, 0 en contra):

- ✅ Minutos: 32.2 esperados (titular, ±5.1).
- ✅ Forma: 3.4 en sus últimos 5, 4.1 esta temporada (8 partidos), 3.9 la temporada pasada (línea 4.5).
- ➖ Cómo produce asistencias: asiste el 17.9% de las canastas de sus compañeros en pista × 20.6 canastas de compañeros esperadas (su equipo 40.5 por 48' contra esta defensa).
- ✅ Defensa: el rival concede -7% de asistencias por minuto a bases/escoltas (defensa fuerte); ajuste aplicado -7%.
- ➖ Ritmo del partido: -1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 4, 3 (2 de 2 a favor).
- ✅ Últimos 10: la habría pasado 7 de 10.
- ⚠️ Donte DiVincenzo ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ sin Anthony Edwards, la estrella de su equipo (12 partidos suyos sin él): más tiros y balón para él por minuto (puntos +4%, triples +0%, asistencias -0%).
- ⚠️ Anthony Edwards ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ cambio de rol esta temporada (por minuto): reb +55%; se da más peso a la línea de la casa.

- ⚠️ Alertas: sin Anthony Edwards: más tiros para él.
- Asistencias **4.0** (por componentes 3.7 · por tasa por minuto y defensa rival 4.1): asiste el 17.9% de las canastas de sus compañeros en pista × 20.6 canastas de compañeros esperadas (su equipo 40.5 por 48' contra esta defensa).

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 32.6 | 29.8 | 30.2 | 27.5 | 24.5 |
| Asistencias | 3.4 | 4.6 | 4.1 | 3.7 | 3.5 |
| % de las canastas de compañeros que asiste | 14.0% | 21.1% | 17.9% | 17.8% | 16.5% |
| Pérdidas por jugada | 13.4% | 12.9% | 14.0% | 10.6% | 5.0% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -2%, vs defensa media -1%, vs defensa débil +3%; rebotes: vs defensa fuerte -18%, vs defensa media -1%, vs defensa débil +20%; asistencias: vs defensa fuerte +6%, vs defensa media -15%, vs defensa débil +12%; triples: vs defensa fuerte -4%, vs defensa media -4%, vs defensa débil +12%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 39% | 67% | 68% | 67% |
| triple frontal | 27% | 42% | 35% | 34% |
| pintura | 21% | 38% | 45% | 45% |
| triple de esquina | 10% | 42% | 38% | 38% |
| media distancia | 4% | 46% | 41% | 40% |

#### Jonathan Kuminga (aleros/ala-pívots) vs Houston Rockets

- Minutos esperados: **31.6** (± 5.9); 50 partidos en la base.
- Donte DiVincenzo ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- sin Anthony Edwards, la estrella de su equipo (4 partidos suyos sin él): más tiros y balón para él por minuto (puntos +6%, triples +1%, asistencias +4%)
- Anthony Edwards ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Su prop más probable hoy: **Jonathan Kuminga: menos de 5.5 rebotes** (57%). Con 80% de probabilidad: más de 2.5 / menos de 8.5.
- Defensa de Houston Rockets contra aleros/ala-pívots en rebotes: -12% respecto a la media; ajuste por su historial contra defensas similares: -1%.

**¿Por qué 5.4 rebotes?** (línea 5.5; 31.6 minutos esperados)

Razonamiento (3 factores a favor, 1 en contra):

- ✅ Minutos: 31.6 esperados (titular, ±5.9).
- ❌ Forma: 6.0 en sus últimos 5, 5.4 esta temporada (8 partidos), 5.3 la temporada pasada (línea 5.5).
- ➖ Cómo produce rebotes: defensivos 4.4 = captura el 14.0% de los fallos del rival en pista × 47.0 fallos esperados del rival (liga 47.0) × 66% del partido; ofensivos 1.5 = 4.7% de los fallos de su equipo × 46.5.
- ✅ Defensa: el rival concede -12% de rebotes por minuto a aleros/ala-pívots (defensa fuerte); ajuste aplicado -12%.
- ✅ Altura: mide 6'7", 2.8 pulgadas menos que los aleros/ala-pívots del rival (-1.0% en esta estadística).
- ➖ Ritmo del partido: -1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ➖ Últimos 10: la habría pasado 6 de 10.
- ⚠️ Donte DiVincenzo ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ sin Anthony Edwards, la estrella de su equipo (4 partidos suyos sin él): más tiros y balón para él por minuto (puntos +6%, triples +1%, asistencias +4%).
- ⚠️ Anthony Edwards ya no jugó en sus últimos partidos: la baja ya está en sus minutos.

- Rebotes **5.4** (por componentes 5.9 · por tasa por minuto y defensa rival 5.3): defensivos 4.4 = captura el 14.0% de los fallos del rival en pista × 47.0 fallos esperados del rival (liga 47.0) × 66% del partido; ofensivos 1.5 = 4.7% de los fallos de su equipo × 46.5.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 32.6 | 28.6 | 30.8 | 23.5 | - |
| Rebotes | 6.0 | 4.9 | 5.4 | 5.3 | - |
| % de los fallos del rival que captura | 12.7% | 13.0% | 12.5% | 17.7% | - |
| % de los fallos de su equipo que captura | 4.7% | 4.1% | 4.3% | 5.6% | - |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -6%, vs defensa media +1%, vs defensa débil +9%; rebotes: vs defensa fuerte -12%, vs defensa media +8%, vs defensa débil +11%; asistencias: vs defensa fuerte +2%, vs defensa media -11%, vs defensa débil +8%; triples: vs defensa fuerte +7%, vs defensa media +35%, vs defensa débil -33%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 32% | 64% | 68% | 67% |
| pintura | 24% | 42% | 45% | 45% |
| triple de esquina | 18% | 37% | 38% | 38% |
| triple frontal | 17% | 34% | 35% | 34% |
| media distancia | 9% | 39% | 41% | 40% |

## Toronto Raptors @ Denver Nuggets

Diferencia esperada: Denver Nuggets por 4.5.

Parte de lesiones: Jakob Poeltl (Day-To-Day); Cameron Johnson (Day-To-Day); Alpha Diallo (Day-To-Day); Julian Strawther (Out); Nate Bittle (Out); Spencer Jones (Out); Kawhi Leonard (Out).

Ventajas del partido (los dos lados): puntos esperados frente a su media de los últimos 10, ajuste por la defensa rival y diferencia de estatura con los rivales de su posición.

| Equipo | Jugador | Puntos esperados | Su media (últ. 10) | Defensa rival en puntos | Rebotes esperados | Altura vs rival |
|---|---|---|---|---|---|---|
| DEN | Jamal Murray | 25.4 | 26.4 | +0% | 4.9 | +1.5" |
| DEN | Nikola Jokic | 22.0 | 23.4 | -4% | 11.1 | -1.0" |
| DEN | Christian Braun | 15.0 | 12.6 | +1% | 4.4 | +3.5" |
| TOR | Scottie Barnes | 22.8 | 23.7 | +3% | 7.4 | -0.3" |
| TOR | RJ Barrett | 21.1 | 21.7 | +3% | 6.1 | -2.3" |
| TOR | Immanuel Quickley | 17.4 | 14.4 | -1% | 3.9 | -2.7" |
| TOR | Ja'Kobe Walter | 12.7 | 14.0 | -1% | 4.0 | -0.7" |
| DEN | Aaron Gordon | 13.1 | 10.9 | -4% | 5.9 | +0.8" |
| DEN | Cameron Johnson | 10.7 | 11.7 | -4% | 4.3 | +0.8" |
| TOR | Jamal Shead | 6.8 | 8.0 | -1% | 1.8 | -3.7" |

Picks seguros de titulares estables:

| Jugador | Pick seguro | Prob. | Cuota mínima | Esperado | Últ. 10 |
|---|---|---|---|---|---|
| Jamal Murray | **más de 2.5 asistencias** | **89%** | 1.12 | 5.6 | 10/10 |
| Immanuel Quickley | **más de 1.5 asistencias** | **89%** | 1.13 | 5.3 | 10/10 |
| Scottie Barnes | **más de 2.5 rebotes** | **89%** | 1.13 | 7.4 | 10/10 |
| Scottie Barnes | **más de 2.5 asistencias** | **89%** | 1.13 | 6.0 | 10/10 |
| Nikola Jokic | **más de 6.5 rebotes** | **88%** | 1.14 | 11.1 | 10/10 |
| RJ Barrett | **más de 13.5 puntos** | **87%** | 1.14 | 21.1 | 9/10 |

Las 8 más probables (máximo 2 por jugador: las de un mismo jugador suelen ganar o perder juntas).

| Prop | Prob. final | Modelo | Casa | Esperado | Últ. 10 | Temporada | vs este rival | Cuota (implícita) |
|---|---|---|---|---|---|---|---|---|
| **Christian Braun: más de 1.5 asistencias** | **62%** | 68% | 57% | 2.6 ± 1.6 | 6/10 | 4/6 | 2 | 1.63 (61%) |
| **Cameron Johnson: más de 1.5 asistencias** | **61%** | 59% | 62% | 2.1 ± 1.6 | 7/10 | 2/3 | 2 | 1.51 (66%) |
| **Ja'Kobe Walter: más de 1.5 asistencias** | **61%** | 71% | 54% | 2.7 ± 1.7 | 8/10 | 6/7 | 2, 0 | 1.73 (58%) |
| **Jamal Shead: más de 0.5 triples** ⚠️ suplente | **60%** | 55% | 63% | 0.9 ± 1.0 | 5/10 | 2/7 | 0, 0 | 1.48 (68%) |
| **DeMar DeRozan: menos de 2.5 rebotes** ⚠️ suplente | **58%** | 61% | 56% | 2.2 ± 1.5 | 7/10 | 4/6 | 1, 1 | 1.66 (60%) |
| **Nikola Jokic: menos de 1.5 triples** | **58%** | 65% | 52% | 1.2 ± 1.1 | 7/10 | 4/6 | 1 | 1.78 (56%) |
| **Scottie Barnes: más de 0.5 triples** | **58%** | 55% | 60% | 0.9 ± 0.9 | 4/10 | 3/7 | 1, 2 | 1.57 (64%) |
| **Collin Murray-Boyles: menos de 5.5 rebotes** ⚠️ suplente | **57%** | 61% | 55% | 4.8 ± 2.4 | 6/10 | 4/7 | 9 | 1.71 (58%) |

### Fichas de los jugadores destacados

#### Christian Braun (bases/escoltas) vs Toronto Raptors

- Minutos esperados: **36.2** (± 3.0); 55 partidos en la base.
- Su prop más probable hoy: **Christian Braun: más de 1.5 asistencias** (62%). Con 80% de probabilidad: más de 0.5 / menos de 4.5.
- Defensa de Toronto Raptors contra bases/escoltas en asistencias: -6% respecto a la media; ajuste por su historial contra defensas similares: -4%.

**¿Por qué 2.6 asistencias?** (línea 1.5; 36.2 minutos esperados)

Razonamiento (3 factores a favor, 1 en contra):

- ✅ Minutos: 36.2 esperados (titular, ±3.0).
- ✅ Forma: 2.4 en sus últimos 5, 2.2 esta temporada (6 partidos), 2.7 la temporada pasada (línea 1.5).
- ➖ Cómo produce asistencias: asiste el 11.2% de las canastas de sus compañeros en pista × 24.7 canastas de compañeros esperadas (su equipo 40.2 por 48' contra esta defensa).
- ❌ Defensa: el rival concede -6% de asistencias por minuto a bases/escoltas (defensa fuerte); ajuste aplicado -6%.
- ➖ Ritmo del partido: -0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 2 (1 de 1 a favor).
- ➖ Últimos 10: la habría pasado 6 de 10.

- Asistencias **2.6** (por componentes 2.8 · por tasa por minuto y defensa rival 2.6): asiste el 11.2% de las canastas de sus compañeros en pista × 24.7 canastas de compañeros esperadas (su equipo 40.2 por 48' contra esta defensa).

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 36.8 | 34.1 | 36.2 | 31.8 | 33.0 |
| Asistencias | 2.4 | 2.2 | 2.2 | 2.7 | 2.0 |
| % de las canastas de compañeros que asiste | 9.3% | 9.3% | 8.7% | 10.5% | 7.5% |
| Pérdidas por jugada | 11.7% | 11.5% | 12.4% | 8.8% | 10.0% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -12%, vs defensa media +1%, vs defensa débil +7%; rebotes: vs defensa fuerte -9%, vs defensa media -4%, vs defensa débil +11%; asistencias: vs defensa fuerte -10%, vs defensa media +2%, vs defensa débil +19%; triples: vs defensa fuerte -2%, vs defensa media +23%, vs defensa débil -21%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 42% | 71% | 68% | 68% |
| triple frontal | 20% | 32% | 35% | 34% |
| triple de esquina | 19% | 37% | 38% | 38% |
| pintura | 13% | 44% | 45% | 43% |
| media distancia | 6% | 42% | 41% | 39% |

#### Cameron Johnson (aleros/ala-pívots) vs Toronto Raptors

- Minutos esperados: **28.2** (± 9.7); 62 partidos en la base.
- en el parte de lesiones: day-to-day
- cambio de rol esta temporada (por minuto): reb +57%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Cameron Johnson: más de 1.5 asistencias** (61%). Con 80% de probabilidad: más de 0.5 / menos de 3.5.
- Defensa de Toronto Raptors contra aleros/ala-pívots en asistencias: -9% respecto a la media; ajuste por su historial contra defensas similares: -1%.

**¿Por qué 2.1 asistencias?** (línea 1.5; 28.2 minutos esperados)

Razonamiento (3 factores a favor, 2 en contra):

- ❌ Minutos: 28.2 esperados (titular, ±9.7).
- ✅ Forma: 2.6 en sus últimos 5, 2.0 esta temporada (3 partidos), 2.4 la temporada pasada (línea 1.5).
- ➖ Cómo produce asistencias: asiste el 10.7% de las canastas de sus compañeros en pista × 19.7 canastas de compañeros esperadas (su equipo 40.2 por 48' contra esta defensa).
- ❌ Defensa: el rival concede -9% de asistencias por minuto a aleros/ala-pívots (defensa fuerte); ajuste aplicado -9%.
- ➖ Ritmo del partido: -0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 2 (1 de 1 a favor).
- ✅ Últimos 10: la habría pasado 7 de 10.
- ⚠️ en el parte de lesiones: day-to-day.
- ⚠️ cambio de rol esta temporada (por minuto): reb +57%; se da más peso a la línea de la casa.

- ⚠️ Alertas: minutos inestables, en el parte de lesiones.
- Asistencias **2.1** (por componentes 2.1 · por tasa por minuto y defensa rival 2.1): asiste el 10.7% de las canastas de sus compañeros en pista × 19.7 canastas de compañeros esperadas (su equipo 40.2 por 48' contra esta defensa).

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 28.4 | 29.4 | 26.3 | 30.4 | 31.0 |
| Asistencias | 2.6 | 2.6 | 2.0 | 2.4 | 2.0 |
| % de las canastas de compañeros que asiste | 12.6% | 11.9% | 10.5% | 9.6% | 7.4% |
| Pérdidas por jugada | 15.5% | 11.1% | 18.0% | 8.1% | 10.7% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -8%, vs defensa media +7%, vs defensa débil +13%; rebotes: vs defensa fuerte +13%, vs defensa media -21%, vs defensa débil +6%; asistencias: vs defensa fuerte -9%, vs defensa media +5%, vs defensa débil +8%; triples: vs defensa fuerte -25%, vs defensa media +23%, vs defensa débil +33%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 35% | 38% | 35% | 34% |
| bajo el aro | 24% | 68% | 68% | 68% |
| triple de esquina | 19% | 42% | 38% | 38% |
| pintura | 13% | 45% | 45% | 43% |
| media distancia | 9% | 39% | 41% | 39% |

#### Ja'Kobe Walter (bases/escoltas) vs Denver Nuggets

- Minutos esperados: **31.2** (± 3.9); 86 partidos en la base.
- Kawhi Leonard ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- cambio de rol esta temporada (por minuto): ast +54%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Ja'Kobe Walter: más de 1.5 asistencias** (61%). Con 80% de probabilidad: más de 0.5 / menos de 4.5.
- Defensa de Denver Nuggets contra bases/escoltas en asistencias: +0% respecto a la media; ajuste por su historial contra defensas similares: +0%.

**¿Por qué 2.7 asistencias?** (línea 1.5; 31.2 minutos esperados)

Razonamiento (3 factores a favor, 0 en contra):

- ✅ Minutos: 31.2 esperados (titular, ±3.9).
- ✅ Forma: 2.4 en sus últimos 5, 2.6 esta temporada (7 partidos), 1.4 la temporada pasada (línea 1.5).
- ➖ Cómo produce asistencias: asiste el 11.2% de las canastas de sus compañeros en pista × 23.7 canastas de compañeros esperadas (su equipo 43.0 por 48' contra esta defensa).
- ➖ Defensa: el rival concede +0% de asistencias por minuto a bases/escoltas (defensa media); ajuste aplicado +0%.
- ➖ Ritmo del partido: -0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ➖ Contra este rival: 2, 0 (1 de 2 a favor).
- ✅ Últimos 10: la habría pasado 8 de 10.
- ⚠️ Kawhi Leonard ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ cambio de rol esta temporada (por minuto): ast +54%; se da más peso a la línea de la casa.

- ⚠️ Alertas: cambio de rol.
- Asistencias **2.7** (por componentes 2.7 · por tasa por minuto y defensa rival 2.7): asiste el 11.2% de las canastas de sus compañeros en pista × 23.7 canastas de compañeros esperadas (su equipo 43.0 por 48' contra esta defensa).

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 31.8 | 32.2 | 29.4 | 21.5 | 23.0 |
| Asistencias | 2.4 | 2.2 | 2.6 | 1.2 | 1.0 |
| % de las canastas de compañeros que asiste | 9.4% | 8.9% | 10.7% | 7.0% | 5.5% |
| Pérdidas por jugada | 5.6% | 6.0% | 5.5% | 7.4% | 7.2% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -8%, vs defensa media +19%, vs defensa débil -9%; rebotes: vs defensa fuerte -7%, vs defensa media -8%, vs defensa débil +17%; asistencias: vs defensa fuerte -13%, vs defensa media -13%, vs defensa débil +27%; triples: vs defensa fuerte -13%, vs defensa media +20%, vs defensa débil -14%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 40% | 35% | 35% | 34% |
| triple de esquina | 28% | 43% | 38% | 37% |
| bajo el aro | 19% | 65% | 68% | 69% |
| pintura | 9% | 39% | 45% | 45% |
| media distancia | 3% | 42% | 41% | 40% |

#### Jamal Shead (bases/escoltas) vs Denver Nuggets

- Minutos esperados: **22.3** (± 3.0); 96 partidos en la base.
- Kawhi Leonard ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- cambio de rol esta temporada (por minuto): tpm -58%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Jamal Shead: más de 0.5 triples** (60%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Denver Nuggets contra bases/escoltas en triples: -0% respecto a la media; ajuste por su historial contra defensas similares: +5%.

**¿Por qué 0.9 triples?** (línea 0.5; 22.3 minutos esperados)

Razonamiento (1 factores a favor, 3 en contra):

- ❌ Minutos: 22.3 esperados (suplente, ±3.0).
- ✅ Forma: 0.6 en sus últimos 5, 0.4 esta temporada (7 partidos), 1.1 la temporada pasada (línea 0.5).
- ➖ Cómo produce triples: 3.1 triples intentados (su ritmo 4.9 por 36'; el rival concede +2% de triples en su reparto) × 31% esperado.
- ➖ Defensa: el rival concede +1% de triples por minuto a bases/escoltas (defensa media); ajuste aplicado -0%; en su zona principal (triple) el rival concede 34% (liga 35%).
- ❌ Altura: mide 6'1", 3.7 pulgadas menos que los bases/escoltas del rival (-1.3% en esta estadística).
- ➖ Ritmo del partido: -0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ❌ Contra este rival: 0, 0 (0 de 2 a favor).
- ➖ Últimos 10: la habría pasado 5 de 10.
- ⚠️ Kawhi Leonard ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ cambio de rol esta temporada (por minuto): tpm -58%; se da más peso a la línea de la casa.

- ⚠️ Alertas: suplente, cambio de rol.
- Triples **0.9** (por componentes 1.0 · por tasa por minuto y defensa rival 0.8): 3.1 triples intentados (su ritmo 4.9 por 36'; el rival concede +2% de triples en su reparto) × 31% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 22.4 | 25.5 | 21.7 | 23.3 | 21.0 |
| Triples anotados | 0.6 | 1.1 | 0.4 | 1.1 | 0.0 |
| Triples intentados | 3.2 | 4.1 | 2.3 | 3.4 | 3.5 |
| % triples | 18.8% | 26.8% | 18.8% | 32.2% | 0.0% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +2%, vs defensa media -18%, vs defensa débil +12%; rebotes: vs defensa fuerte -5%, vs defensa media +1%, vs defensa débil +6%; asistencias: vs defensa fuerte -11%, vs defensa media -10%, vs defensa débil +25%; triples: vs defensa fuerte -22%, vs defensa media +6%, vs defensa débil +22%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 41% | 32% | 35% | 34% |
| pintura | 23% | 37% | 45% | 45% |
| bajo el aro | 19% | 62% | 68% | 69% |
| triple de esquina | 11% | 32% | 38% | 37% |
| media distancia | 6% | 34% | 41% | 40% |

#### DeMar DeRozan (bases/escoltas) vs Toronto Raptors

- Minutos esperados: **24.3** (± 3.5); 83 partidos en la base.
- Su prop más probable hoy: **DeMar DeRozan: menos de 2.5 rebotes** (58%). Con 80% de probabilidad: más de 0.5 / menos de 3.5.
- Defensa de Toronto Raptors contra bases/escoltas en rebotes: -3% respecto a la media; ajuste por su historial contra defensas similares: -2%.

**¿Por qué 2.2 rebotes?** (línea 2.5; 24.3 minutos esperados)

Razonamiento (4 factores a favor, 2 en contra):

- ❌ Minutos: 24.3 esperados (suplente, ±3.5).
- ✅ Forma: 2.0 en sus últimos 5, 2.0 esta temporada (6 partidos), 2.8 la temporada pasada (línea 2.5).
- ➖ Cómo produce rebotes: defensivos 1.8 = captura el 7.5% de los fallos del rival en pista × 47.1 fallos esperados del rival (liga 47.0) × 51% del partido; ofensivos 0.5 = 2.4% de los fallos de su equipo × 42.3.
- ✅ Defensa: el rival concede -3% de rebotes por minuto a bases/escoltas (defensa fuerte); ajuste aplicado -3%.
- ❌ Altura: mide 6'6", 3.5 pulgadas más que los bases/escoltas del rival (+1.2% en esta estadística).
- ➖ Ritmo del partido: -0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 1, 1 (2 de 2 a favor).
- ✅ Últimos 10: la habría pasado 7 de 10.

- ⚠️ Alertas: suplente.
- Rebotes **2.2** (por componentes 2.3 · por tasa por minuto y defensa rival 2.1): defensivos 1.8 = captura el 7.5% de los fallos del rival en pista × 47.1 fallos esperados del rival (liga 47.0) × 51% del partido; ofensivos 0.5 = 2.4% de los fallos de su equipo × 42.3.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 24.6 | 24.9 | 25.2 | 31.3 | 34.0 |
| Rebotes | 2.0 | 1.9 | 2.0 | 2.9 | 1.0 |
| % de los fallos del rival que captura | 6.0% | 5.1% | 5.3% | 8.5% | 0.0% |
| % de los fallos de su equipo que captura | 2.8% | 3.0% | 2.9% | 1.5% | 2.9% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +5%, vs defensa media -2%, vs defensa débil -2%; rebotes: vs defensa fuerte +4%, vs defensa media -12%, vs defensa débil +3%; asistencias: vs defensa fuerte -1%, vs defensa media -14%, vs defensa débil +16%; triples: vs defensa fuerte -3%, vs defensa media +7%, vs defensa débil -5%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| media distancia | 47% | 46% | 41% | 39% |
| pintura | 27% | 51% | 45% | 43% |
| bajo el aro | 11% | 72% | 68% | 68% |
| triple frontal | 9% | 31% | 35% | 34% |
| triple de esquina | 6% | 36% | 38% | 38% |

## Portland Trail Blazers @ Phoenix Suns

Diferencia esperada: Portland Trail Blazers por 3.5.

Parte de lesiones: Jordan Goodwin (Day-To-Day); Ja Morant (Out); Mark Williams (Out); Shaedon Sharpe (Out); Rasheer Fleming (Day-To-Day).

Ventajas del partido (los dos lados): puntos esperados frente a su media de los últimos 10, ajuste por la defensa rival y diferencia de estatura con los rivales de su posición.

| Equipo | Jugador | Puntos esperados | Su media (últ. 10) | Defensa rival en puntos | Rebotes esperados | Altura vs rival |
|---|---|---|---|---|---|---|
| PHX | Devin Booker | 23.5 | 22.0 | +0% | 3.8 | +1.1" |
| PHX | Miles Bridges | 17.4 | 15.9 | -2% | 6.7 | -0.5" |
| POR | Deni Avdija | 22.0 | 22.4 | -2% | 6.2 | +0.2" |
| PHX | Dillon Brooks | 17.2 | 20.1 | -2% | 4.4 | -0.5" |
| PHX | Jalen Green | 15.5 | 17.8 | -0% | 3.8 | +0.1" |
| POR | Toumani Camara | 12.3 | 11.2 | -2% | 3.8 | -0.8" |
| POR | Jrue Holiday | 13.5 | 15.2 | +0% | 4.3 | +0.5" |
| PHX | Collin Gillespie | 10.2 | 8.3 | -0% | 2.9 | -2.9" |
| POR | Donovan Clingan | 10.6 | 9.1 | -0% | 10.4 | +0.6" |
| POR | Scoot Henderson | 11.0 | 10.9 | +0% | 2.5 | -0.5" |

Picks seguros de titulares estables:

| Jugador | Pick seguro | Prob. | Cuota mínima | Esperado | Últ. 10 |
|---|---|---|---|---|---|
| Devin Booker | **más de 1.5 asistencias** | **92%** | 1.08 | 5.2 | 10/10 |
| Deni Avdija | **más de 1.5 asistencias** | **91%** | 1.09 | 5.2 | 10/10 |
| Miles Bridges | **más de 17.5 pts+reb+ast** | **87%** | 1.15 | 26.8 | 8/10 |
| Deni Avdija | **más de 24.5 pts+reb+ast** | **87%** | 1.15 | 33.4 | 9/10 |
| Devin Booker | **más de 12.5 puntos** | **87%** | 1.16 | 23.5 | 9/10 |
| Miles Bridges | **más de 10.5 puntos** | **86%** | 1.16 | 17.4 | 7/10 |

Las 8 más probables (máximo 2 por jugador: las de un mismo jugador suelen ganar o perder juntas).

| Prop | Prob. final | Modelo | Casa | Esperado | Últ. 10 | Temporada | vs este rival | Cuota (implícita) |
|---|---|---|---|---|---|---|---|---|
| **Khaman Maluach: menos de 0.5 triples** | **71%** | 75% | 68% | 0.3 ± 0.5 | 9/10 | 4/5 | 0, 1 | 1.38 (72%) |
| **Donovan Clingan: más de 0.5 triples** | **61%** | 61% | 61% | 0.9 ± 1.0 | 8/10 | 4/6 | 2, 0, 3, 3, 0 | 1.53 (65%) |
| **Toumani Camara: menos de 4.5 rebotes** | **61%** | 66% | 58% | 3.8 ± 2.0 | 6/10 | 5/6 | 2, 4, 10, 11, 2 | 1.62 (62%) |
| **Jalen Green: más de 2.5 asistencias** | **60%** | 63% | 58% | 3.4 ± 2.0 | 7/10 | 3/5 | 3, 2, 1 | 1.62 (62%) |
| **Jrue Holiday: más de 1.5 triples** ⚠️ suplente | **59%** | 60% | 59% | 2.0 ± 1.5 | 8/10 | 5/6 | 0, 4, 0, 1 | 1.58 (63%) |
| **Dillon Brooks: más de 1.5 triples** | **58%** | 58% | 58% | 2.0 ± 1.4 | 8/10 | 3/5 | 1, 2, 1, 1 | 1.61 (62%) |
| **Collin Gillespie: más de 1.5 triples** ⚠️ suplente | **58%** | 57% | 58% | 2.1 ± 1.5 | 5/10 | 3/5 | 0, 1, 4, 8, 4 | 1.61 (62%) |
| **Scoot Henderson: menos de 13.5 puntos** ⚠️ suplente | **57%** | 66% | 51% | 11.0 ± 5.9 | 6/10 | 4/6 | 15, 9, 11 | 1.83 (55%) |

### Fichas de los jugadores destacados

#### Khaman Maluach (pívots) vs Portland Trail Blazers

- Minutos esperados: **18.8** (± 6.1); 56 partidos en la base.
- Mark Williams ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Su prop más probable hoy: **Khaman Maluach: menos de 0.5 triples** (71%). Con 80% de probabilidad: más de - / menos de 1.5.
- Defensa de Portland Trail Blazers contra pívots en triples: +10% respecto a la media; ajuste por su historial contra defensas similares: -1%.

**¿Por qué 0.3 triples?** (línea 0.5; 18.8 minutos esperados)

Razonamiento (2 factores a favor, 4 en contra):

- ❌ Minutos: 18.8 esperados (titular, ±6.1).
- ✅ Forma: 0.2 en sus últimos 5, 0.2 esta temporada (5 partidos), 0.1 la temporada pasada (línea 0.5).
- ➖ Cómo produce triples: 0.8 triples intentados (su ritmo 1.7 por 36'; el rival concede -6% de triples en su reparto) × 33% esperado.
- ❌ Defensa: el rival concede +22% de triples por minuto a pívots (defensa débil); ajuste aplicado +10%; en su zona principal (triple) el rival concede 35% (liga 35%).
- ❌ Altura: mide 7'2", 2.2 pulgadas más que los pívots del rival (+0.8% en esta estadística).
- ➖ Ritmo del partido: -1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ➖ Contra este rival: 0, 1 (1 de 2 a favor).
- ✅ Últimos 10: la habría pasado 9 de 10.
- ❌ Bajas del rival: sin Ja Morant (titular); +1.7% en esta estadística.
- ⚠️ Mark Williams ya no jugó en sus últimos partidos: la baja ya está en sus minutos.

- ⚠️ Alertas: minutos inestables.
- Triples **0.3** (por componentes 0.3 · por tasa por minuto y defensa rival 0.3): 0.8 triples intentados (su ritmo 1.7 por 36'; el rival concede -6% de triples en su reparto) × 33% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 20.2 | 15.2 | 20.2 | 9.0 | 16.5 |
| Triples anotados | 0.2 | 0.1 | 0.2 | 0.1 | 0.5 |
| Triples intentados | 0.6 | 0.5 | 0.6 | 0.5 | 0.5 |
| % triples | 33.3% | 20.0% | 33.3% | 21.7% | 100.0% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +7%, vs defensa media +4%, vs defensa débil -15%; rebotes: vs defensa fuerte -15%, vs defensa media +6%, vs defensa débil +20%; asistencias: vs defensa fuerte -25%, vs defensa media -50%, vs defensa débil +63%; triples: vs defensa fuerte -3%, vs defensa media -26%, vs defensa débil +61%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 62% | 67% | 68% | 66% |
| pintura | 17% | 42% | 45% | 46% |
| triple frontal | 13% | 31% | 35% | 35% |
| triple de esquina | 6% | 37% | 38% | 38% |
| media distancia | 2% | 42% | 41% | 42% |

#### Donovan Clingan (pívots) vs Phoenix Suns

- Minutos esperados: **24.7** (± 6.4); 89 partidos en la base.
- sin Ja Morant: muestra insuficiente (2 partidos sin él)
- Su prop más probable hoy: **Donovan Clingan: más de 0.5 triples** (61%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Phoenix Suns contra pívots en triples: -1% respecto a la media; ajuste por su historial contra defensas similares: +0%.

**¿Por qué 0.9 triples?** (línea 0.5; 24.7 minutos esperados)

Razonamiento (3 factores a favor, 1 en contra):

- ❌ Minutos: 24.7 esperados (titular, ±6.4).
- ✅ Forma: 0.8 en sus últimos 5, 1.0 esta temporada (6 partidos), 1.2 la temporada pasada (línea 0.5).
- ➖ Cómo produce triples: 2.4 triples intentados (su ritmo 3.7 por 36'; el rival concede +0% de triples en su reparto) × 35% esperado.
- ➖ Defensa: el rival concede -2% de triples por minuto a pívots (defensa media); ajuste aplicado -1%; en su zona principal (triple) el rival concede 35% (liga 35%).
- ➖ Ritmo del partido: -1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 2, 0, 3, 3, 0 (3 de 5 a favor).
- ✅ Últimos 10: la habría pasado 8 de 10.
- ⚠️ sin Ja Morant: muestra insuficiente (2 partidos sin él).

- ⚠️ Alertas: minutos inestables.
- Triples **0.9** (por componentes 0.8 · por tasa por minuto y defensa rival 1.0): 2.4 triples intentados (su ritmo 3.7 por 36'; el rival concede +0% de triples en su reparto) × 35% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 24.6 | 22.9 | 24.0 | 26.9 | 26.2 |
| Triples anotados | 0.8 | 1.1 | 1.0 | 1.1 | 1.6 |
| Triples intentados | 1.8 | 3.5 | 2.2 | 3.3 | 3.4 |
| % triples | 44.4% | 31.4% | 46.2% | 32.5% | 47.1% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -6%, vs defensa media -2%, vs defensa débil +8%; rebotes: vs defensa fuerte -12%, vs defensa media +4%, vs defensa débil +8%; asistencias: vs defensa fuerte -13%, vs defensa media +2%, vs defensa débil +9%; triples: vs defensa fuerte -23%, vs defensa media +12%, vs defensa débil +12%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 50% | 65% | 68% | 68% |
| triple frontal | 34% | 35% | 35% | 35% |
| pintura | 12% | 44% | 45% | 46% |
| triple de esquina | 3% | 33% | 38% | 37% |
| media distancia | 1% | 43% | 41% | 42% |

#### Toumani Camara (aleros/ala-pívots) vs Phoenix Suns

- Minutos esperados: **28.2** (± 3.2); 94 partidos en la base.
- sin Ja Morant: muestra insuficiente (2 partidos sin él)
- cambio de rol esta temporada (por minuto): pts +35%, reb -32%, ast -39%, tpm +82%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Toumani Camara: menos de 4.5 rebotes** (61%). Con 80% de probabilidad: más de 1.5 / menos de 5.5.
- Defensa de Phoenix Suns contra aleros/ala-pívots en rebotes: -4% respecto a la media; ajuste por su historial contra defensas similares: -2%.

**¿Por qué 3.8 rebotes?** (línea 4.5; 28.2 minutos esperados)

Razonamiento (4 factores a favor, 0 en contra):

- ✅ Minutos: 28.2 esperados (titular, ±3.2).
- ✅ Forma: 3.0 en sus últimos 5, 2.8 esta temporada (6 partidos), 5.0 la temporada pasada (línea 4.5).
- ➖ Cómo produce rebotes: defensivos 3.1 = captura el 10.9% de los fallos del rival en pista × 48.3 fallos esperados del rival (liga 47.0) × 59% del partido; ofensivos 1.0 = 3.8% de los fallos de su equipo × 47.0.
- ✅ Defensa: el rival concede -4% de rebotes por minuto a aleros/ala-pívots (defensa fuerte); ajuste aplicado -4%.
- ➖ Ritmo del partido: -1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 2, 4, 10, 11, 2 (3 de 5 a favor).
- ➖ Últimos 10: la habría pasado 6 de 10.
- ⚠️ sin Ja Morant: muestra insuficiente (2 partidos sin él).
- ⚠️ cambio de rol esta temporada (por minuto): pts +35%, reb -32%, ast -39%, tpm +82%; se da más peso a la línea de la casa.

- ⚠️ Alertas: cambio de rol.
- Rebotes **3.8** (por componentes 4.1 · por tasa por minuto y defensa rival 3.7): defensivos 3.1 = captura el 10.9% de los fallos del rival en pista × 48.3 fallos esperados del rival (liga 47.0) × 59% del partido; ofensivos 1.0 = 3.8% de los fallos de su equipo × 47.0.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 27.8 | 29.4 | 27.0 | 33.3 | 32.8 |
| Rebotes | 3.0 | 4.2 | 2.8 | 5.1 | 5.8 |
| % de los fallos del rival que captura | 9.0% | 11.2% | 8.2% | 11.0% | 12.0% |
| % de los fallos de su equipo que captura | 2.2% | 3.6% | 2.5% | 4.6% | 5.4% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -9%, vs defensa media -5%, vs defensa débil +18%; rebotes: vs defensa fuerte -7%, vs defensa media +5%, vs defensa débil +6%; asistencias: vs defensa fuerte -4%, vs defensa media -5%, vs defensa débil +9%; triples: vs defensa fuerte -6%, vs defensa media +9%, vs defensa débil -7%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 46% | 39% | 35% | 35% |
| triple de esquina | 22% | 35% | 38% | 37% |
| bajo el aro | 20% | 68% | 68% | 68% |
| pintura | 10% | 43% | 45% | 46% |
| media distancia | 2% | 40% | 41% | 42% |

#### Jalen Green (bases/escoltas) vs Portland Trail Blazers

- Minutos esperados: **30.0** (± 5.0); 43 partidos en la base.
- Mark Williams ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- cambio de rol esta temporada (por minuto): pts -44%, tpm -66%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Jalen Green: más de 2.5 asistencias** (60%). Con 80% de probabilidad: más de 1.5 / menos de 5.5.
- Defensa de Portland Trail Blazers contra bases/escoltas en asistencias: -3% respecto a la media; ajuste por su historial contra defensas similares: -1%.

**¿Por qué 3.4 asistencias?** (línea 2.5; 30.0 minutos esperados)

Razonamiento (4 factores a favor, 2 en contra):

- ✅ Minutos: 30.0 esperados (titular, ±5.0).
- ✅ Forma: 3.6 en sus últimos 5, 3.6 esta temporada (5 partidos), 2.9 la temporada pasada (línea 2.5).
- ➖ Cómo produce asistencias: asiste el 16.7% de las canastas de sus compañeros en pista × 19.5 canastas de compañeros esperadas (su equipo 40.6 por 48' contra esta defensa).
- ❌ Defensa: el rival concede -3% de asistencias por minuto a bases/escoltas (defensa fuerte); ajuste aplicado -3%.
- ➖ Ritmo del partido: -1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ❌ Contra este rival: 3, 2, 1 (1 de 3 a favor).
- ✅ Últimos 10: la habría pasado 7 de 10.
- ✅ Bajas del rival: sin Ja Morant (titular); +1.5% en esta estadística.
- ⚠️ Mark Williams ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ cambio de rol esta temporada (por minuto): pts -44%, tpm -66%; se da más peso a la línea de la casa.

- Asistencias **3.4** (por componentes 3.2 · por tasa por minuto y defensa rival 3.4): asiste el 16.7% de las canastas de sus compañeros en pista × 19.5 canastas de compañeros esperadas (su equipo 40.6 por 48' contra esta defensa).

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 28.6 | 33.4 | 28.6 | 27.9 | 28.7 |
| Asistencias | 3.6 | 3.6 | 3.6 | 2.9 | 2.0 |
| % de las canastas de compañeros que asiste | 16.7% | 16.0% | 16.7% | 15.9% | 13.3% |
| Pérdidas por jugada | 16.7% | 13.6% | 16.7% | 11.7% | 11.8% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -4%, vs defensa media -22%, vs defensa débil +23%; rebotes: vs defensa fuerte -5%, vs defensa media +12%, vs defensa débil -4%; asistencias: vs defensa fuerte -8%, vs defensa media +20%, vs defensa débil -10%; triples: vs defensa fuerte -7%, vs defensa media +4%, vs defensa débil +3%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 33% | 29% | 35% | 35% |
| bajo el aro | 26% | 62% | 68% | 66% |
| media distancia | 17% | 45% | 41% | 42% |
| pintura | 15% | 43% | 45% | 46% |
| triple de esquina | 9% | 38% | 38% | 38% |

#### Jrue Holiday (bases/escoltas) vs Phoenix Suns

- Minutos esperados: **26.6** (± 4.5); 65 partidos en la base.
- sin Ja Morant: muestra insuficiente (2 partidos sin él)
- Su prop más probable hoy: **Jrue Holiday: más de 1.5 triples** (59%). Con 80% de probabilidad: más de 0.5 / menos de 3.5.
- Defensa de Phoenix Suns contra bases/escoltas en triples: -0% respecto a la media; ajuste por su historial contra defensas similares: -1%.

**¿Por qué 2.0 triples?** (línea 1.5; 26.6 minutos esperados)

Razonamiento (2 factores a favor, 2 en contra):

- ❌ Minutos: 26.6 esperados (suplente, ±4.5).
- ✅ Forma: 2.4 en sus últimos 5, 2.0 esta temporada (6 partidos), 2.6 la temporada pasada (línea 1.5).
- ➖ Cómo produce triples: 5.3 triples intentados (su ritmo 7.4 por 36'; el rival concede +0% de triples en su reparto) × 37% esperado.
- ➖ Defensa: el rival concede -1% de triples por minuto a bases/escoltas (defensa media); ajuste aplicado -0%; en su zona principal (triple) el rival concede 35% (liga 35%).
- ➖ Ritmo del partido: -1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ❌ Contra este rival: 0, 4, 0, 1 (1 de 4 a favor).
- ✅ Últimos 10: la habría pasado 8 de 10.
- ⚠️ sin Ja Morant: muestra insuficiente (2 partidos sin él).

- ⚠️ Alertas: suplente.
- Triples **2.0** (por componentes 2.0 · por tasa por minuto y defensa rival 2.1): 5.3 triples intentados (su ritmo 7.4 por 36'; el rival concede +0% de triples en su reparto) × 37% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 26.6 | 31.1 | 25.7 | 30.3 | 29.2 |
| Triples anotados | 2.4 | 2.3 | 2.0 | 2.6 | 1.2 |
| Triples intentados | 5.6 | 5.8 | 5.2 | 6.9 | 5.8 |
| % triples | 42.9% | 39.7% | 38.7% | 37.6% | 21.7% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -14%, vs defensa media -11%, vs defensa débil +23%; rebotes: vs defensa fuerte -19%, vs defensa media +13%, vs defensa débil +6%; asistencias: vs defensa fuerte -6%, vs defensa media +1%, vs defensa débil +5%; triples: vs defensa fuerte -18%, vs defensa media -12%, vs defensa débil +34%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 43% | 36% | 35% | 35% |
| pintura | 24% | 49% | 45% | 46% |
| bajo el aro | 17% | 66% | 68% | 68% |
| triple de esquina | 9% | 44% | 38% | 37% |
| media distancia | 8% | 40% | 41% | 42% |

## Dallas Mavericks @ San Antonio Spurs

Diferencia esperada: San Antonio Spurs por 11.5 — algo desigual: titulares hasta -1.5% de minutos.

Parte de lesiones: Max Christie (Out); Santi Aldama (Out); Dereck Lively II (Out); Jayden Quaintance (Out); Tarik Biberovic (Out); Sergio de Larrea (Out); Tobias Harris (Out).

Ventajas del partido (los dos lados): puntos esperados frente a su media de los últimos 10, ajuste por la defensa rival y diferencia de estatura con los rivales de su posición.

| Equipo | Jugador | Puntos esperados | Su media (últ. 10) | Defensa rival en puntos | Rebotes esperados | Altura vs rival |
|---|---|---|---|---|---|---|
| DAL | Cooper Flagg | 22.0 | 23.0 | -4% | 6.0 | -1.0" |
| DAL | P.J. Washington | 12.6 | 13.4 | -4% | 7.4 | -3.0" |
| SA | Dylan Harper | 17.8 | 18.7 | +1% | 5.8 | +2.1" |
| SA | Devin Vassell | 12.4 | 12.4 | +1% | 4.2 | +2.1" |
| SA | Victor Wembanyama | 24.1 | 25.5 | +2% | 9.9 | +8.0" |
| SA | De'Aaron Fox | 15.3 | 14.8 | +1% | 4.1 | +0.1" |
| SA | Stephon Castle | 14.5 | 14.5 | +1% | 5.1 | +3.1" |
| DAL | Naji Marshall | 13.5 | 13.1 | -4% | 3.9 | -4.0" |
| DAL | Zaccharie Risacher | 9.3 | 6.8 | -4% | 5.3 | -2.0" |
| DAL | Daniel Gafford | 9.4 | 9.2 | -5% | 7.0 | +0.0" |

Picks seguros de titulares estables:

| Jugador | Pick seguro | Prob. | Cuota mínima | Esperado | Últ. 10 |
|---|---|---|---|---|---|
| Victor Wembanyama | **más de 11.5 puntos** | **89%** | 1.13 | 24.1 | 10/10 |
| Cooper Flagg | **más de 1.5 asistencias** | **88%** | 1.13 | 5.5 | 9/10 |
| Cooper Flagg | **más de 10.5 puntos** | **88%** | 1.14 | 22.0 | 9/10 |
| Victor Wembanyama | **más de 5.5 rebotes** | **87%** | 1.15 | 9.9 | 10/10 |
| Victor Wembanyama | **más de 23.5 pts+reb+ast** | **87%** | 1.15 | 36.9 | 10/10 |
| P.J. Washington | **más de 3.5 rebotes** | **86%** | 1.16 | 7.4 | 10/10 |

Las 8 más probables (máximo 2 por jugador: las de un mismo jugador suelen ganar o perder juntas).

| Prop | Prob. final | Modelo | Casa | Esperado | Últ. 10 | Temporada | vs este rival | Cuota (implícita) |
|---|---|---|---|---|---|---|---|---|
| **Keldon Johnson: más de 3.5 rebotes** ⚠️ suplente | **64%** | 75% | 56% | 5.5 ± 2.4 | 9/10 | 7/7 | 6, 6, 4, 6, 5 | 1.68 (60%) |
| **Dylan Harper: menos de 1.5 triples** | **59%** | 57% | 61% | 1.4 ± 1.2 | 5/10 | 4/7 | 3, 0, 1, 0, 1 | 1.52 (66%) |
| **De'Aaron Fox: menos de 1.5 triples** | **59%** | 62% | 57% | 1.3 ± 1.2 | 6/10 | 4/7 | 2, 2, 1, 3 | 1.65 (61%) |
| **Victor Wembanyama: menos de 11.5 rebotes** | **58%** | 66% | 52% | 9.9 ± 3.7 | 5/10 | 4/7 | 7, 13, 11, 11, 15 | 1.78 (56%) |
| **Stephon Castle: menos de 5.5 rebotes** | **57%** | 60% | 56% | 5.1 ± 2.5 | 7/10 | 4/7 | 4, 12, 7, 7 | 1.68 (60%) |
| **Keldon Johnson: más de 8.5 puntos** ⚠️ suplente | **57%** | 63% | 53% | 11.4 ± 5.1 | 4/10 | 4/7 | 7, 17, 8, 12, 11 | 1.79 (56%) |
| **Devin Vassell: menos de 4.5 rebotes** | **57%** | 57% | 58% | 4.2 ± 2.2 | 6/10 | 5/7 | 4, 2, 4, 7, 3 | 1.62 (62%) |
| **De'Aaron Fox: más de 3.5 rebotes** | **57%** | 56% | 58% | 4.1 ± 2.2 | 5/10 | 4/7 | 3, 1, 2, 3 | 1.61 (62%) |

### Fichas de los jugadores destacados

#### Keldon Johnson (aleros/ala-pívots) vs Dallas Mavericks

- Minutos esperados: **24.5** (± 3.0); 113 partidos en la base.
- cambio de rol esta temporada (por minuto): tpm -76%; se da más peso a la línea de la casa
- partido desigual (favorito por 11.5): los suplentes suelen jugar +3% de minutos si se rompe
- Su prop más probable hoy: **Keldon Johnson: más de 3.5 rebotes** (64%). Con 80% de probabilidad: más de 2.5 / menos de 7.5.
- Defensa de Dallas Mavericks contra aleros/ala-pívots en rebotes: +1% respecto a la media; ajuste por su historial contra defensas similares: +0%.

**¿Por qué 5.5 rebotes?** (línea 3.5; 24.5 minutos esperados)

Razonamiento (4 factores a favor, 2 en contra):

- ❌ Minutos: 24.5 esperados (suplente, ±3.0).
- ✅ Forma: 5.8 en sus últimos 5, 5.6 esta temporada (7 partidos), 4.1 la temporada pasada (línea 3.5).
- ➖ Cómo produce rebotes: defensivos 3.4 = captura el 13.3% de los fallos del rival en pista × 50.6 fallos esperados del rival (liga 47.0) × 51% del partido; ofensivos 2.0 = 8.3% de los fallos de su equipo × 48.3.
- ➖ Defensa: el rival concede +1% de rebotes por minuto a aleros/ala-pívots (defensa media); ajuste aplicado +1%.
- ❌ Altura: mide 6'6", 2.0 pulgadas menos que los aleros/ala-pívots del rival (-0.7% en esta estadística).
- ➖ Ritmo del partido: +0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 6, 6, 4, 6, 5 (5 de 5 a favor).
- ✅ Últimos 10: la habría pasado 9 de 10.
- ✅ Racha: la pasó en sus 7 partidos de esta temporada (al inicio de 2025-26 estas rachas siguieron más de lo que esperaba el modelo).
- ⚠️ cambio de rol esta temporada (por minuto): tpm -76%; se da más peso a la línea de la casa.
- ⚠️ partido desigual (favorito por 11.5): los suplentes suelen jugar +3% de minutos si se rompe.

- ⚠️ Alertas: suplente.
- Rebotes **5.5** (por componentes 5.5 · por tasa por minuto y defensa rival 5.5): defensivos 3.4 = captura el 13.3% de los fallos del rival en pista × 50.6 fallos esperados del rival (liga 47.0) × 51% del partido; ofensivos 2.0 = 8.3% de los fallos de su equipo × 48.3.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 24.4 | 21.2 | 23.0 | 22.1 | 22.0 |
| Rebotes | 5.8 | 5.0 | 5.6 | 4.9 | 5.4 |
| % de los fallos del rival que captura | 13.6% | 13.1% | 13.0% | 14.4% | 14.6% |
| % de los fallos de su equipo que captura | 9.0% | 9.7% | 10.3% | 7.5% | 9.8% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -10%, vs defensa media +8%, vs defensa débil +12%; rebotes: vs defensa fuerte -0%, vs defensa media -2%, vs defensa débil +2%; asistencias: vs defensa fuerte -14%, vs defensa media +4%, vs defensa débil +15%; triples: vs defensa fuerte -16%, vs defensa media -2%, vs defensa débil +23%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 42% | 62% | 68% | 69% |
| pintura | 24% | 48% | 45% | 45% |
| triple de esquina | 16% | 35% | 38% | 36% |
| triple frontal | 16% | 37% | 35% | 35% |
| media distancia | 1% | 41% | 41% | 43% |

#### Dylan Harper (bases/escoltas) vs Dallas Mavericks

- Minutos esperados: **31.8** (± 4.8); 100 partidos en la base.
- partido desigual (favorito por 11.5): los titulares suelen jugar -3% de minutos si se rompe
- Su prop más probable hoy: **Dylan Harper: menos de 1.5 triples** (59%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Dallas Mavericks contra bases/escoltas en triples: -3% respecto a la media; ajuste por su historial contra defensas similares: +3%.

**¿Por qué 1.4 triples?** (línea 1.5; 31.8 minutos esperados)

Razonamiento (3 factores a favor, 2 en contra):

- ✅ Minutos: 31.8 esperados (titular, ±4.8).
- ❌ Forma: 1.6 en sus últimos 5, 1.3 esta temporada (7 partidos), 1.1 la temporada pasada (línea 1.5).
- ➖ Cómo produce triples: 3.9 triples intentados (su ritmo 4.5 por 36'; el rival concede -6% de triples en su reparto) × 35% esperado.
- ✅ Defensa: el rival concede -4% de triples por minuto a bases/escoltas (defensa fuerte); ajuste aplicado -3%; en su zona principal (triple) el rival concede 35% (liga 35%).
- ❌ Altura: mide 6'5", 2.1 pulgadas más que los bases/escoltas del rival (+0.7% en esta estadística).
- ➖ Ritmo del partido: +0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 3, 0, 1, 0, 1 (4 de 5 a favor).
- ➖ Últimos 10: la habría pasado 5 de 10.
- ⚠️ partido desigual (favorito por 11.5): los titulares suelen jugar -3% de minutos si se rompe.

- Triples **1.4** (por componentes 1.4 · por tasa por minuto y defensa rival 1.4): 3.9 triples intentados (su ritmo 4.5 por 36'; el rival concede -6% de triples en su reparto) × 35% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 32.2 | 32.4 | 32.7 | 23.7 | 23.8 |
| Triples anotados | 1.6 | 1.5 | 1.3 | 1.0 | 1.0 |
| Triples intentados | 3.8 | 4.3 | 3.6 | 2.7 | 2.6 |
| % triples | 42.1% | 34.9% | 36.0% | 35.0% | 38.5% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -5%, vs defensa media +2%, vs defensa débil +4%; rebotes: vs defensa fuerte -5%, vs defensa media -1%, vs defensa débil +5%; asistencias: vs defensa fuerte -19%, vs defensa media +13%, vs defensa débil +30%; triples: vs defensa fuerte +7%, vs defensa media -9%, vs defensa débil +2%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 45% | 67% | 68% | 69% |
| triple frontal | 20% | 37% | 35% | 35% |
| pintura | 18% | 42% | 45% | 45% |
| media distancia | 10% | 37% | 41% | 43% |
| triple de esquina | 7% | 32% | 38% | 36% |

#### De'Aaron Fox (bases/escoltas) vs Dallas Mavericks

- Minutos esperados: **29.6** (± 6.2); 104 partidos en la base.
- cambio de rol esta temporada (por minuto): tpm -33%; se da más peso a la línea de la casa
- partido desigual (favorito por 11.5): los titulares suelen jugar -3% de minutos si se rompe
- Su prop más probable hoy: **De'Aaron Fox: menos de 1.5 triples** (59%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Dallas Mavericks contra bases/escoltas en triples: -3% respecto a la media; ajuste por su historial contra defensas similares: -1%.

**¿Por qué 1.3 triples?** (línea 1.5; 29.6 minutos esperados)

Razonamiento (2 factores a favor, 2 en contra):

- ❌ Minutos: 29.6 esperados (titular, ±6.2).
- ✅ Forma: 1.2 en sus últimos 5, 1.1 esta temporada (7 partidos), 1.4 la temporada pasada (línea 1.5).
- ➖ Cómo produce triples: 3.8 triples intentados (su ritmo 4.7 por 36'; el rival concede -6% de triples en su reparto) × 32% esperado.
- ✅ Defensa: el rival concede -4% de triples por minuto a bases/escoltas (defensa fuerte); ajuste aplicado -3%; en su zona principal (triple) el rival concede 35% (liga 35%).
- ➖ Ritmo del partido: +0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ❌ Contra este rival: 2, 2, 1, 3 (1 de 4 a favor).
- ➖ Últimos 10: la habría pasado 6 de 10.
- ⚠️ cambio de rol esta temporada (por minuto): tpm -33%; se da más peso a la línea de la casa.
- ⚠️ partido desigual (favorito por 11.5): los titulares suelen jugar -3% de minutos si se rompe.

- ⚠️ Alertas: minutos inestables, cambio de rol.
- Triples **1.3** (por componentes 1.2 · por tasa por minuto y defensa rival 1.3): 3.8 triples intentados (su ritmo 4.7 por 36'; el rival concede -6% de triples en su reparto) × 32% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 30.0 | 32.7 | 30.9 | 30.8 | 28.5 |
| Triples anotados | 1.2 | 1.3 | 1.1 | 1.7 | 2.0 |
| Triples intentados | 2.6 | 4.2 | 2.9 | 5.2 | 4.8 |
| % triples | 46.2% | 31.0% | 40.0% | 32.4% | 42.1% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -14%, vs defensa media +8%, vs defensa débil +9%; rebotes: vs defensa fuerte -8%, vs defensa media +12%, vs defensa débil +3%; asistencias: vs defensa fuerte -4%, vs defensa media +6%, vs defensa débil +4%; triples: vs defensa fuerte +1%, vs defensa media -1%, vs defensa débil +1%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| pintura | 30% | 50% | 45% | 45% |
| triple frontal | 27% | 31% | 35% | 35% |
| bajo el aro | 23% | 68% | 68% | 69% |
| media distancia | 12% | 47% | 41% | 43% |
| triple de esquina | 9% | 40% | 38% | 36% |

#### Victor Wembanyama (aleros/ala-pívots) vs Dallas Mavericks

- Minutos esperados: **30.1** (± 5.4); 96 partidos en la base.
- partido desigual (favorito por 11.5): los titulares suelen jugar -3% de minutos si se rompe
- Su prop más probable hoy: **Victor Wembanyama: menos de 11.5 rebotes** (58%). Con 80% de probabilidad: más de 6.5 / menos de 13.5.
- Defensa de Dallas Mavericks contra aleros/ala-pívots en rebotes: +1% respecto a la media; ajuste por su historial contra defensas similares: -1%.

**¿Por qué 9.9 rebotes?** (línea 11.5; 30.1 minutos esperados)

Razonamiento (3 factores a favor, 1 en contra):

- ✅ Minutos: 30.1 esperados (titular, ±5.4).
- ✅ Forma: 9.8 en sus últimos 5, 10.7 esta temporada (7 partidos), 11.3 la temporada pasada (línea 11.5).
- ➖ Cómo produce rebotes: defensivos 7.4 = captura el 23.4% de los fallos del rival en pista × 50.6 fallos esperados del rival (liga 47.0) × 63% del partido; ofensivos 2.1 = 6.8% de los fallos de su equipo × 48.3.
- ➖ Defensa: el rival concede +1% de rebotes por minuto a aleros/ala-pívots (defensa media); ajuste aplicado +1%.
- ❌ Altura: mide 7'4", 8.0 pulgadas más que los aleros/ala-pívots del rival (+2.8% en esta estadística).
- ➖ Ritmo del partido: +0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 7, 13, 11, 11, 15 (3 de 5 a favor).
- ➖ Últimos 10: la habría pasado 5 de 10.
- ⚠️ partido desigual (favorito por 11.5): los titulares suelen jugar -3% de minutos si se rompe.

- Rebotes **9.9** (por componentes 9.5 · por tasa por minuto y defensa rival 9.7): defensivos 7.4 = captura el 23.4% de los fallos del rival en pista × 50.6 fallos esperados del rival (liga 47.0) × 63% del partido; ofensivos 2.1 = 6.8% de los fallos de su equipo × 48.3.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 30.6 | 34.0 | 31.3 | 29.9 | 29.2 |
| Rebotes | 9.8 | 11.0 | 10.7 | 11.1 | 11.4 |
| % de los fallos del rival que captura | 23.9% | 23.5% | 26.0% | 28.4% | 29.5% |
| % de los fallos de su equipo que captura | 6.5% | 8.0% | 7.1% | 7.3% | 8.1% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -7%, vs defensa media -0%, vs defensa débil +18%; rebotes: vs defensa fuerte -6%, vs defensa media +2%, vs defensa débil +4%; asistencias: vs defensa fuerte -8%, vs defensa media -15%, vs defensa débil +30%; triples: vs defensa fuerte -10%, vs defensa media -9%, vs defensa débil +13%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 37% | 73% | 68% | 69% |
| triple frontal | 29% | 33% | 35% | 35% |
| pintura | 16% | 43% | 45% | 45% |
| media distancia | 15% | 35% | 41% | 43% |
| triple de esquina | 2% | 42% | 38% | 36% |

#### Stephon Castle (bases/escoltas) vs Dallas Mavericks

- Minutos esperados: **27.5** (± 5.2); 99 partidos en la base.
- cambio de rol esta temporada (por minuto): tpm +104%; se da más peso a la línea de la casa
- partido desigual (favorito por 11.5): los titulares suelen jugar -3% de minutos si se rompe
- Su prop más probable hoy: **Stephon Castle: menos de 5.5 rebotes** (57%). Con 80% de probabilidad: más de 2.5 / menos de 7.5.
- Defensa de Dallas Mavericks contra bases/escoltas en rebotes: +7% respecto a la media; ajuste por su historial contra defensas similares: +1%.

**¿Por qué 5.1 rebotes?** (línea 5.5; 27.5 minutos esperados)

Razonamiento (3 factores a favor, 3 en contra):

- ✅ Minutos: 27.5 esperados (titular, ±5.2).
- ✅ Forma: 5.0 en sus últimos 5, 5.6 esta temporada (7 partidos), 5.3 la temporada pasada (línea 5.5).
- ➖ Cómo produce rebotes: defensivos 3.6 = captura el 12.2% de los fallos del rival en pista × 50.6 fallos esperados del rival (liga 47.0) × 57% del partido; ofensivos 1.3 = 4.5% de los fallos de su equipo × 48.3.
- ❌ Defensa: el rival concede +7% de rebotes por minuto a bases/escoltas (defensa débil); ajuste aplicado +7%.
- ❌ Altura: mide 6'6", 3.1 pulgadas más que los bases/escoltas del rival (+1.1% en esta estadística).
- ➖ Ritmo del partido: +0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ❌ Contra este rival: 4, 12, 7, 7 (1 de 4 a favor).
- ✅ Últimos 10: la habría pasado 7 de 10.
- ⚠️ cambio de rol esta temporada (por minuto): tpm +104%; se da más peso a la línea de la casa.
- ⚠️ partido desigual (favorito por 11.5): los titulares suelen jugar -3% de minutos si se rompe.

- Rebotes **5.1** (por componentes 4.8 · por tasa por minuto y defensa rival 5.2): defensivos 3.6 = captura el 12.2% de los fallos del rival en pista × 50.6 fallos esperados del rival (liga 47.0) × 57% del partido; ofensivos 1.3 = 4.5% de los fallos de su equipo × 48.3.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 28.2 | 29.8 | 28.9 | 30.8 | 27.8 |
| Rebotes | 5.0 | 5.4 | 5.6 | 5.3 | 7.5 |
| % de los fallos del rival que captura | 11.9% | 13.0% | 13.9% | 11.7% | 19.4% |
| % de los fallos de su equipo que captura | 4.9% | 4.6% | 4.8% | 4.9% | 6.7% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -7%, vs defensa media +12%, vs defensa débil -4%; rebotes: vs defensa fuerte -5%, vs defensa media +4%, vs defensa débil +3%; asistencias: vs defensa fuerte -14%, vs defensa media +18%, vs defensa débil +13%; triples: vs defensa fuerte +3%, vs defensa media -10%, vs defensa débil +6%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 34% | 63% | 68% | 69% |
| triple frontal | 26% | 34% | 35% | 35% |
| pintura | 24% | 41% | 45% | 45% |
| triple de esquina | 8% | 34% | 38% | 36% |
| media distancia | 8% | 40% | 41% | 43% |

## Los Angeles Lakers @ Sacramento Kings

Diferencia esperada: Los Angeles Lakers por 11.5 — algo desigual: titulares hasta -1.5% de minutos.

Parte de lesiones: Ben Simmons (Out); Precious Achiuwa (Day-To-Day); Keegan Murray (Out); Maxime Raynaud (Out); Adou Thiero (Out).

Ventajas del partido (los dos lados): puntos esperados frente a su media de los últimos 10, ajuste por la defensa rival y diferencia de estatura con los rivales de su posición.

| Equipo | Jugador | Puntos esperados | Su media (últ. 10) | Defensa rival en puntos | Rebotes esperados | Altura vs rival |
|---|---|---|---|---|---|---|
| LAL | Austin Reaves | 22.8 | 23.3 | +4% | 3.8 | +1.2" |
| LAL | Luka Doncic | 34.6 | 36.3 | +4% | 7.3 | +4.2" |
| SAC | Domantas Sabonis | 15.8 | 15.4 | +1% | 12.0 | +1.7" |
| SAC | De'Andre Hunter | 14.4 | 12.2 | +0% | 5.0 | -1.3" |
| SAC | Zach LaVine | 19.3 | 21.6 | +1% | 2.7 | -0.1" |
| LAL | Walker Kessler | 14.5 | 13.7 | +7% | 10.4 | +2.2" |
| SAC | Precious Achiuwa | 12.1 | 12.6 | +1% | 6.3 | -0.3" |
| LAL | Quentin Grimes | 10.2 | 8.0 | +4% | 3.2 | +0.2" |
| LAL | Jake LaRavia | 7.8 | 5.2 | +6% | 3.9 | -1.3" |
| SAC | Leaky Black | 6.5 | 5.6 | +0% | 3.1 | -2.3" |

Picks seguros de titulares estables:

| Jugador | Pick seguro | Prob. | Cuota mínima | Esperado | Últ. 10 |
|---|---|---|---|---|---|
| Austin Reaves | **más de 1.5 asistencias** | **90%** | 1.11 | 5.3 | 9/10 |
| Domantas Sabonis | **más de 6.5 rebotes** | **90%** | 1.11 | 12.0 | 10/10 |
| Luka Doncic | **más de 3.5 asistencias** | **89%** | 1.13 | 7.9 | 9/10 |
| Austin Reaves | **más de 14.5 puntos** | **88%** | 1.13 | 22.8 | 10/10 |
| Domantas Sabonis | **más de 7.5 puntos** | **88%** | 1.14 | 15.8 | 10/10 |
| Luka Doncic | **más de 3.5 rebotes** | **88%** | 1.14 | 7.3 | 10/10 |

Las 8 más probables (máximo 2 por jugador: las de un mismo jugador suelen ganar o perder juntas).

| Prop | Prob. final | Modelo | Casa | Esperado | Últ. 10 | Temporada | vs este rival | Cuota (implícita) |
|---|---|---|---|---|---|---|---|---|
| **Malik Monk: menos de 1.5 rebotes** ⚠️ suplente | **64%** | 61% | 66% | 1.3 ± 1.3 | 8/10 | 5/6 | 1, 1, 2, 1 | 1.41 (71%) |
| **Quentin Grimes: menos de 1.5 triples** ⚠️ suplente | **64%** | 67% | 62% | 1.2 ± 1.2 | 7/10 | 7/8 | 3 | 1.52 (66%) |
| **Domantas Sabonis: menos de 6.5 asistencias** | **60%** | 66% | 55% | 5.3 ± 2.4 | 4/10 | 2/7 | 3 | 1.69 (59%) |
| **Malik Monk: menos de 1.5 triples** ⚠️ suplente | **59%** | 64% | 56% | 1.4 ± 1.6 | 7/10 | 5/6 | 2, 7, 3, 3 | 1.67 (60%) |
| **Precious Achiuwa: menos de 7.5 rebotes** | **59%** | 65% | 54% | 6.3 ± 3.1 | 6/10 | 4/7 | 9, 7, 3 | 1.72 (58%) |
| **Quentin Grimes: más de 2.5 rebotes** ⚠️ suplente | **58%** | 58% | 59% | 3.2 ± 2.0 | 5/10 | 5/8 | 5 | 1.59 (63%) |
| **Jake LaRavia: más de 0.5 triples** | **58%** | 60% | 56% | 1.1 ± 1.1 | 7/10 | 5/7 | 0, 0, 0, 2 | 1.67 (60%) |
| **Matisse Thybulle: menos de 2.5 rebotes** | **58%** | 62% | 55% | 2.3 ± 1.6 | 8/10 | 6/8 | 1 | 1.69 (59%) |

### Fichas de los jugadores destacados

#### Malik Monk (bases/escoltas) vs Los Angeles Lakers

- Minutos esperados: **17.2** (± 8.3); 68 partidos en la base.
- Keegan Murray ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Maxime Raynaud ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- cambio de rol esta temporada (por minuto): ast +74%; se da más peso a la línea de la casa
- partido desigual (no favorito por 11.5): los suplentes suelen jugar +3% de minutos si se rompe
- Su prop más probable hoy: **Malik Monk: menos de 1.5 rebotes** (64%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Los Angeles Lakers contra bases/escoltas en rebotes: -9% respecto a la media; ajuste por su historial contra defensas similares: +0%.

**¿Por qué 1.3 rebotes?** (línea 1.5; 17.2 minutos esperados)

Razonamiento (5 factores a favor, 1 en contra):

- ❌ Minutos: 17.2 esperados (suplente, ±8.3).
- ✅ Forma: 1.0 en sus últimos 5, 1.0 esta temporada (6 partidos), 1.9 la temporada pasada (línea 1.5).
- ➖ Cómo produce rebotes: defensivos 1.1 = captura el 7.9% de los fallos del rival en pista × 38.9 fallos esperados del rival (liga 47.0) × 36% del partido; ofensivos 0.2 = 1.5% de los fallos de su equipo × 46.0.
- ✅ Defensa: el rival concede -9% de rebotes por minuto a bases/escoltas (defensa fuerte); ajuste aplicado -9%.
- ✅ Altura: mide 6'3", 2.1 pulgadas menos que los bases/escoltas del rival (-0.7% en esta estadística).
- ➖ Ritmo del partido: +0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 1, 1, 2, 1 (3 de 4 a favor).
- ✅ Últimos 10: la habría pasado 8 de 10.
- ⚠️ Keegan Murray ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ Maxime Raynaud ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ cambio de rol esta temporada (por minuto): ast +74%; se da más peso a la línea de la casa.
- ⚠️ partido desigual (no favorito por 11.5): los suplentes suelen jugar +3% de minutos si se rompe.

- ⚠️ Alertas: suplente, minutos inestables.
- Rebotes **1.3** (por componentes 1.4 · por tasa por minuto y defensa rival 1.3): defensivos 1.1 = captura el 7.9% de los fallos del rival en pista × 38.9 fallos esperados del rival (liga 47.0) × 36% del partido; ofensivos 0.2 = 1.5% de los fallos de su equipo × 46.0.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 15.4 | 15.3 | 14.8 | 22.0 | 22.8 |
| Rebotes | 1.0 | 1.1 | 1.0 | 1.9 | 1.2 |
| % de los fallos del rival que captura | 5.7% | 7.4% | 6.1% | 8.0% | 4.9% |
| % de los fallos de su equipo que captura | 1.4% | 0.7% | 1.2% | 1.1% | 1.2% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -2%, vs defensa media +2%, vs defensa débil -0%; rebotes: vs defensa fuerte +3%, vs defensa media +12%, vs defensa débil -12%; asistencias: vs defensa fuerte -8%, vs defensa media +12%, vs defensa débil -2%; triples: vs defensa fuerte -23%, vs defensa media +25%, vs defensa débil -7%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 42% | 39% | 35% | 34% |
| pintura | 28% | 40% | 45% | 44% |
| bajo el aro | 14% | 67% | 68% | 72% |
| media distancia | 10% | 43% | 41% | 43% |
| triple de esquina | 7% | 35% | 38% | 38% |

#### Quentin Grimes (bases/escoltas) vs Sacramento Kings

- Minutos esperados: **25.9** (± 5.4); 95 partidos en la base.
- cambio de rol esta temporada (por minuto): tpm -50%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Quentin Grimes: menos de 1.5 triples** (64%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Sacramento Kings contra bases/escoltas en triples: +6% respecto a la media; ajuste por su historial contra defensas similares: -0%.

**¿Por qué 1.2 triples?** (línea 1.5; 25.9 minutos esperados)

Razonamiento (2 factores a favor, 3 en contra):

- ❌ Minutos: 25.9 esperados (suplente, ±5.4).
- ✅ Forma: 0.6 en sus últimos 5, 0.8 esta temporada (8 partidos), 1.4 la temporada pasada (línea 1.5).
- ➖ Cómo produce triples: 3.5 triples intentados (su ritmo 4.9 por 36'; el rival concede -1% de triples en su reparto) × 35% esperado.
- ❌ Defensa: el rival concede +7% de triples por minuto a bases/escoltas (defensa débil); ajuste aplicado +6%; en su zona principal (triple) el rival concede 37% (liga 35%).
- ➖ Ritmo del partido: +0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ❌ Contra este rival: 3 (0 de 1 a favor).
- ✅ Últimos 10: la habría pasado 7 de 10.
- ⚠️ cambio de rol esta temporada (por minuto): tpm -50%; se da más peso a la línea de la casa.

- ⚠️ Alertas: suplente, cambio de rol.
- Triples **1.2** (por componentes 1.2 · por tasa por minuto y defensa rival 1.1): 3.5 triples intentados (su ritmo 4.9 por 36'; el rival concede -1% de triples en su reparto) × 35% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 26.4 | 24.8 | 26.2 | 28.5 | 32.0 |
| Triples anotados | 0.6 | 1.0 | 0.8 | 1.6 | 3.0 |
| Triples intentados | 3.0 | 3.3 | 2.9 | 4.8 | 6.0 |
| % triples | 20.0% | 30.3% | 26.1% | 33.9% | 50.0% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -0%, vs defensa media -7%, vs defensa débil +5%; rebotes: vs defensa fuerte -8%, vs defensa media +8%, vs defensa débil +1%; asistencias: vs defensa fuerte -6%, vs defensa media -10%, vs defensa débil +19%; triples: vs defensa fuerte +3%, vs defensa media -8%, vs defensa débil +10%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 38% | 31% | 35% | 37% |
| bajo el aro | 29% | 71% | 68% | 71% |
| triple de esquina | 13% | 40% | 38% | 40% |
| pintura | 12% | 41% | 45% | 51% |
| media distancia | 8% | 35% | 41% | 42% |

#### Domantas Sabonis (aleros/ala-pívots) vs Los Angeles Lakers

- Minutos esperados: **34.9** (± 3.5); 26 partidos en la base.
- Keegan Murray ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Maxime Raynaud ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- cambio de rol esta temporada (por minuto): ast +37%; se da más peso a la línea de la casa
- partido desigual (no favorito por 11.5): los titulares suelen jugar -3% de minutos si se rompe
- Su prop más probable hoy: **Domantas Sabonis: menos de 6.5 asistencias** (60%). Con 80% de probabilidad: más de 2.5 / menos de 7.5.
- Defensa de Los Angeles Lakers contra aleros/ala-pívots en asistencias: -3% respecto a la media; ajuste por su historial contra defensas similares: +1%.

**¿Por qué 5.3 asistencias?** (línea 6.5; 34.9 minutos esperados)

Razonamiento (4 factores a favor, 1 en contra):

- ✅ Minutos: 34.9 esperados (titular, ±3.5).
- ✅ Forma: 6.0 en sus últimos 5, 6.9 esta temporada (7 partidos), 4.1 la temporada pasada (línea 6.5).
- ➖ Cómo produce asistencias: asiste el 21.1% de las canastas de sus compañeros en pista × 23.9 canastas de compañeros esperadas (su equipo 41.6 por 48' contra esta defensa).
- ✅ Defensa: el rival concede -3% de asistencias por minuto a aleros/ala-pívots (defensa fuerte); ajuste aplicado -3%.
- ➖ Ritmo del partido: +0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 3 (1 de 1 a favor).
- ❌ Últimos 10: la habría pasado 4 de 10.
- ⚠️ Keegan Murray ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ Maxime Raynaud ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ cambio de rol esta temporada (por minuto): ast +37%; se da más peso a la línea de la casa.
- ⚠️ partido desigual (no favorito por 11.5): los titulares suelen jugar -3% de minutos si se rompe.

- ⚠️ Alertas: cambio de rol.
- Asistencias **5.3** (por componentes 5.0 · por tasa por minuto y defensa rival 5.5): asiste el 21.1% de las canastas de sus compañeros en pista × 23.9 canastas de compañeros esperadas (su equipo 41.6 por 48' contra esta defensa).

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 36.2 | 33.9 | 36.3 | 29.7 | 31.0 |
| Asistencias | 6.0 | 6.1 | 6.9 | 4.1 | 3.0 |
| % de las canastas de compañeros que asiste | 22.0% | 25.1% | 26.0% | 18.9% | 11.3% |
| Pérdidas por jugada | 29.2% | 23.4% | 28.1% | 16.7% | 18.4% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +7%, vs defensa media -8%, vs defensa débil +0%; rebotes: vs defensa fuerte +6%, vs defensa media -3%, vs defensa débil -2%; asistencias: vs defensa fuerte -8%, vs defensa media +6%, vs defensa débil -0%; triples: vs defensa fuerte +41%, vs defensa media -32%, vs defensa débil +23%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 52% | 71% | 68% | 72% |
| pintura | 33% | 50% | 45% | 44% |
| triple frontal | 8% | 31% | 35% | 34% |
| media distancia | 4% | 45% | 41% | 43% |
| triple de esquina | 2% | 36% | 38% | 38% |

#### Precious Achiuwa (aleros/ala-pívots) vs Los Angeles Lakers

- Minutos esperados: **27.8** (± 8.2); 80 partidos en la base.
- en el parte de lesiones: day-to-day
- Keegan Murray ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Maxime Raynaud ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- partido desigual (no favorito por 11.5): los titulares suelen jugar -3% de minutos si se rompe
- Su prop más probable hoy: **Precious Achiuwa: menos de 7.5 rebotes** (59%). Con 80% de probabilidad: más de 3.5 / menos de 9.5.
- Defensa de Los Angeles Lakers contra aleros/ala-pívots en rebotes: -4% respecto a la media; ajuste por su historial contra defensas similares: -1%.

**¿Por qué 6.3 rebotes?** (línea 7.5; 27.8 minutos esperados)

Razonamiento (3 factores a favor, 1 en contra):

- ❌ Minutos: 27.8 esperados (titular, ±8.2).
- ✅ Forma: 7.0 en sus últimos 5, 6.6 esta temporada (7 partidos), 7.1 la temporada pasada (línea 7.5).
- ➖ Cómo produce rebotes: defensivos 4.0 = captura el 17.8% de los fallos del rival en pista × 38.9 fallos esperados del rival (liga 47.0) × 58% del partido; ofensivos 2.1 = 7.8% de los fallos de su equipo × 46.0.
- ✅ Defensa: el rival concede -4% de rebotes por minuto a aleros/ala-pívots (defensa fuerte); ajuste aplicado -4%.
- ➖ Ritmo del partido: +0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 9, 7, 3 (2 de 3 a favor).
- ➖ Últimos 10: la habría pasado 6 de 10.
- ⚠️ en el parte de lesiones: day-to-day.
- ⚠️ Keegan Murray ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ Maxime Raynaud ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ partido desigual (no favorito por 11.5): los titulares suelen jugar -3% de minutos si se rompe.

- ⚠️ Alertas: minutos inestables, en el parte de lesiones.
- Rebotes **6.3** (por componentes 6.1 · por tasa por minuto y defensa rival 6.4): defensivos 4.0 = captura el 17.8% de los fallos del rival en pista × 38.9 fallos esperados del rival (liga 47.0) × 58% del partido; ofensivos 2.1 = 7.8% de los fallos de su equipo × 46.0.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 29.2 | 29.5 | 28.7 | 24.0 | 25.7 |
| Rebotes | 7.0 | 6.9 | 6.6 | 6.7 | 6.3 |
| % de los fallos del rival que captura | 20.0% | 17.6% | 17.7% | 19.1% | 15.5% |
| % de los fallos de su equipo que captura | 6.4% | 7.4% | 7.1% | 10.3% | 12.1% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +1%, vs defensa media -4%, vs defensa débil +3%; rebotes: vs defensa fuerte -12%, vs defensa media +13%, vs defensa débil +1%; asistencias: vs defensa fuerte -17%, vs defensa media +5%, vs defensa débil +15%; triples: vs defensa fuerte -9%, vs defensa media +6%, vs defensa débil +14%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 43% | 67% | 68% | 72% |
| pintura | 38% | 49% | 45% | 44% |
| triple frontal | 8% | 32% | 35% | 34% |
| triple de esquina | 7% | 31% | 38% | 38% |
| media distancia | 4% | 40% | 41% | 43% |

#### Jake LaRavia (aleros/ala-pívots) vs Sacramento Kings

- Minutos esperados: **24.9** (± 5.7); 97 partidos en la base.
- Su prop más probable hoy: **Jake LaRavia: más de 0.5 triples** (58%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Sacramento Kings contra aleros/ala-pívots en triples: +4% respecto a la media; ajuste por su historial contra defensas similares: -1%.

**¿Por qué 1.1 triples?** (línea 0.5; 24.9 minutos esperados)

Razonamiento (4 factores a favor, 1 en contra):

- ✅ Minutos: 24.9 esperados (titular, ±5.7).
- ✅ Forma: 1.2 en sus últimos 5, 1.1 esta temporada (7 partidos), 0.9 la temporada pasada (línea 0.5).
- ➖ Cómo produce triples: 2.6 triples intentados (su ritmo 3.8 por 36'; el rival concede -1% de triples en su reparto) × 37% esperado.
- ✅ Defensa: el rival concede +3% de triples por minuto a aleros/ala-pívots (defensa media); ajuste aplicado +4%; en su zona principal (triple) el rival concede 37% (liga 35%).
- ➖ Ritmo del partido: +0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ❌ Contra este rival: 0, 0, 0, 2 (1 de 4 a favor).
- ✅ Últimos 10: la habría pasado 7 de 10.

- Triples **1.1** (por componentes 1.0 · por tasa por minuto y defensa rival 1.1): 2.6 triples intentados (su ritmo 3.8 por 36'; el rival concede -1% de triples en su reparto) × 37% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 26.6 | 20.6 | 23.7 | 24.2 | 27.8 |
| Triples anotados | 1.2 | 1.0 | 1.1 | 0.9 | 0.5 |
| Triples intentados | 2.0 | 1.9 | 2.1 | 2.8 | 4.0 |
| % triples | 60.0% | 52.6% | 53.3% | 32.0% | 12.5% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -6%, vs defensa media +16%, vs defensa débil -3%; rebotes: vs defensa fuerte -0%, vs defensa media -5%, vs defensa débil +4%; asistencias: vs defensa fuerte -17%, vs defensa media +11%, vs defensa débil +6%; triples: vs defensa fuerte -4%, vs defensa media +7%, vs defensa débil -0%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 30% | 69% | 68% | 71% |
| triple frontal | 23% | 35% | 35% | 37% |
| triple de esquina | 23% | 35% | 38% | 40% |
| pintura | 23% | 43% | 45% | 51% |
| media distancia | 2% | 37% | 41% | 42% |

## Miami Heat @ LA Clippers

Diferencia esperada: Miami Heat por 4.5.

Parte de lesiones: Giannis Antetokounmpo (Day-To-Day); Brandon Ingram (Out); Jordan Miller (Out); Myron Gardner (Day-To-Day); Yanic Konan Niederhauser (Out); Bradley Beal (Out).

Ventajas del partido (los dos lados): puntos esperados frente a su media de los últimos 10, ajuste por la defensa rival y diferencia de estatura con los rivales de su posición.

| Equipo | Jugador | Puntos esperados | Su media (últ. 10) | Defensa rival en puntos | Rebotes esperados | Altura vs rival |
|---|---|---|---|---|---|---|
| LAC | Darius Garland | 20.4 | 19.3 | +3% | 2.7 | -2.3" |
| MIA | Davion Mitchell | 14.6 | 16.7 | +2% | 2.3 | -4.2" |
| MIA | Giannis Antetokounmpo | 26.9 | 28.3 | -3% | 10.6 | +3.6" |
| MIA | Bam Adebayo | 17.2 | 16.5 | +1% | 8.6 | -4.0" |
| LAC | Rui Hachimura | 14.2 | 16.8 | +2% | 5.3 | -0.3" |
| LAC | Kris Dunn | 9.9 | 7.9 | +4% | 4.2 | -0.3" |
| MIA | Pelle Larsson | 12.9 | 12.0 | +2% | 3.6 | +0.8" |
| LAC | Derrick Jones Jr. | 11.6 | 10.3 | +1% | 4.8 | -2.3" |
| LAC | Kobe Sanders | 12.8 | 9.5 | +4% | 3.8 | +4.7" |
| MIA | Andrew Wiggins | 11.8 | 11.4 | -3% | 3.4 | -0.4" |

Picks seguros de titulares estables:

| Jugador | Pick seguro | Prob. | Cuota mínima | Esperado | Últ. 10 |
|---|---|---|---|---|---|
| Davion Mitchell | **más de 2.5 asistencias** | **89%** | 1.12 | 7.0 | 8/10 |
| Davion Mitchell | **más de 8.5 puntos** | **89%** | 1.13 | 14.6 | 10/10 |
| Bam Adebayo | **más de 4.5 rebotes** | **88%** | 1.14 | 8.6 | 9/10 |
| Giannis Antetokounmpo | **más de 1.5 asistencias** | **87%** | 1.15 | 5.1 | 9/10 |
| Davion Mitchell | **más de 16.5 pts+reb+ast** | **87%** | 1.15 | 23.9 | 9/10 |
| Bam Adebayo | **más de 17.5 pts+reb+ast** | **86%** | 1.16 | 28.8 | 8/10 |

Las 8 más probables (máximo 2 por jugador: las de un mismo jugador suelen ganar o perder juntas).

| Prop | Prob. final | Modelo | Casa | Esperado | Últ. 10 | Temporada | vs este rival | Cuota (implícita) |
|---|---|---|---|---|---|---|---|---|
| **Kris Dunn: menos de 1.5 triples** | **67%** | 68% | 66% | 1.2 ± 1.1 | 9/10 | 6/7 | 1, 2 | 1.42 (70%) |
| **Bam Adebayo: menos de 1.5 triples** | **65%** | 68% | 63% | 1.1 ± 1.3 | 8/10 | 6/7 | 5, 2 | 1.49 (67%) |
| **Giannis Antetokounmpo: menos de 6.5 asistencias** | **62%** | 66% | 58% | 5.1 ± 3.1 | 6/10 | 4/7 | - | 1.62 (62%) |
| **Isaiah Jackson: menos de 7.5 rebotes** | **61%** | 65% | 58% | 6.8 ± 2.8 | 8/10 | 5/7 | - | 1.62 (62%) |
| **Rui Hachimura: menos de 2.5 triples** | **60%** | 56% | 62% | 2.3 ± 1.5 | 3/10 | 3/5 | 1, 3 | 1.50 (66%) |
| **Brook Lopez: menos de 1.5 triples** ⚠️ suplente | **59%** | 64% | 56% | 1.2 ± 1.1 | 7/10 | 5/7 | 1 | 1.68 (60%) |
| **Davion Mitchell: más de 11.5 puntos** | **59%** | 71% | 52% | 14.6 ± 4.7 | 8/10 | 5/7 | 16, 8 | 1.82 (55%) |
| **Davion Mitchell: menos de 7.5 asistencias** | **58%** | 59% | 57% | 7.0 ± 3.0 | 5/10 | 3/7 | 12, 9 | 1.64 (61%) |

### Fichas de los jugadores destacados

#### Kris Dunn (bases/escoltas) vs Miami Heat

- Minutos esperados: **29.6** (± 3.0); 90 partidos en la base.
- Jordan Miller ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Bradley Beal ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Su prop más probable hoy: **Kris Dunn: menos de 1.5 triples** (67%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Miami Heat contra bases/escoltas en triples: +6% respecto a la media; ajuste por su historial contra defensas similares: +4%.

**¿Por qué 1.2 triples?** (línea 1.5; 29.6 minutos esperados)

Razonamiento (3 factores a favor, 2 en contra):

- ✅ Minutos: 29.6 esperados (titular, ±3.0).
- ✅ Forma: 0.6 en sus últimos 5, 0.9 esta temporada (7 partidos), 1.0 la temporada pasada (línea 1.5).
- ➖ Cómo produce triples: 3.4 triples intentados (su ritmo 3.9 por 36'; el rival concede +2% de triples en su reparto) × 37% esperado.
- ❌ Defensa: el rival concede +10% de triples por minuto a bases/escoltas (defensa débil); ajuste aplicado +6%; en su zona principal (triple) el rival concede 35% (liga 35%).
- ❌ Ritmo del partido: +2% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ➖ Contra este rival: 1, 2 (1 de 2 a favor).
- ✅ Últimos 10: la habría pasado 9 de 10.
- ⚠️ Jordan Miller ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ Bradley Beal ya no jugó en sus últimos partidos: la baja ya está en sus minutos.

- Triples **1.2** (por componentes 1.3 · por tasa por minuto y defensa rival 1.2): 3.4 triples intentados (su ritmo 3.9 por 36'; el rival concede +2% de triples en su reparto) × 37% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 29.6 | 29.0 | 29.9 | 27.3 | 24.5 |
| Triples anotados | 0.6 | 0.8 | 0.9 | 1.0 | 1.5 |
| Triples intentados | 2.0 | 2.5 | 2.6 | 2.6 | 2.0 |
| % triples | 30.0% | 32.0% | 33.3% | 37.5% | 75.0% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -4%, vs defensa media -12%, vs defensa débil +17%; rebotes: vs defensa fuerte -8%, vs defensa media +4%, vs defensa débil +5%; asistencias: vs defensa fuerte -2%, vs defensa media +10%, vs defensa débil -5%; triples: vs defensa fuerte -49%, vs defensa media +16%, vs defensa débil +39%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| pintura | 28% | 50% | 45% | 46% |
| triple frontal | 27% | 34% | 35% | 35% |
| bajo el aro | 25% | 67% | 68% | 67% |
| triple de esquina | 17% | 41% | 38% | 40% |
| media distancia | 3% | 35% | 41% | 41% |

#### Bam Adebayo (pívots) vs LA Clippers

- Minutos esperados: **31.6** (± 4.0); 81 partidos en la base.
- cambio de rol esta temporada (por minuto): tpm -66%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Bam Adebayo: menos de 1.5 triples** (65%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de LA Clippers contra pívots en triples: +4% respecto a la media; ajuste por su historial contra defensas similares: +7%.

**¿Por qué 1.1 triples?** (línea 1.5; 31.6 minutos esperados)

Razonamiento (4 factores a favor, 3 en contra):

- ✅ Minutos: 31.6 esperados (titular, ±4.0).
- ✅ Forma: 0.6 en sus últimos 5, 0.6 esta temporada (7 partidos), 1.7 la temporada pasada (línea 1.5).
- ➖ Cómo produce triples: 3.7 triples intentados (su ritmo 4.3 por 36'; el rival concede -1% de triples en su reparto) × 32% esperado.
- ❌ Defensa: el rival concede +6% de triples por minuto a pívots (defensa débil); ajuste aplicado +4%; en su zona principal (triple) el rival concede 36% (liga 35%).
- ✅ Altura: mide 6'9", 4.0 pulgadas menos que los pívots del rival (-1.4% en esta estadística).
- ❌ Ritmo del partido: +2% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ❌ Contra este rival: 5, 2 (0 de 2 a favor).
- ✅ Últimos 10: la habría pasado 8 de 10.
- ⚠️ cambio de rol esta temporada (por minuto): tpm -66%; se da más peso a la línea de la casa.

- ⚠️ Alertas: cambio de rol.
- Triples **1.1** (por componentes 1.2 · por tasa por minuto y defensa rival 1.1): 3.7 triples intentados (su ritmo 4.3 por 36'; el rival concede -1% de triples en su reparto) × 32% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 33.2 | 29.8 | 31.4 | 32.1 | 31.0 |
| Triples anotados | 0.6 | 0.8 | 0.6 | 1.7 | 3.5 |
| Triples intentados | 3.2 | 3.3 | 3.3 | 5.4 | 6.0 |
| % triples | 18.8% | 24.2% | 17.4% | 31.8% | 58.3% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -13%, vs defensa media +2%, vs defensa débil +14%; rebotes: vs defensa fuerte -3%, vs defensa media +4%, vs defensa débil +1%; asistencias: vs defensa fuerte -7%, vs defensa media +6%, vs defensa débil +2%; triples: vs defensa fuerte -32%, vs defensa media +18%, vs defensa débil +28%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| pintura | 31% | 46% | 45% | 45% |
| bajo el aro | 25% | 69% | 68% | 70% |
| triple frontal | 23% | 31% | 35% | 36% |
| triple de esquina | 11% | 31% | 38% | 39% |
| media distancia | 11% | 36% | 41% | 39% |

#### Giannis Antetokounmpo (aleros/ala-pívots) vs LA Clippers

- Minutos esperados: **32.2** (± 3.7); 43 partidos en la base.
- en el parte de lesiones: day-to-day
- Su prop más probable hoy: **Giannis Antetokounmpo: menos de 6.5 asistencias** (62%). Con 80% de probabilidad: más de 2.5 / menos de 8.5.
- Defensa de LA Clippers contra aleros/ala-pívots en asistencias: -1% respecto a la media; ajuste por su historial contra defensas similares: +1%.

**¿Por qué 5.1 asistencias?** (línea 6.5; 32.2 minutos esperados)

Razonamiento (1 factores a favor, 1 en contra):

- ✅ Minutos: 32.2 esperados (titular, ±3.7).
- ➖ Forma: 6.8 en sus últimos 5, 5.7 esta temporada (7 partidos), 5.4 la temporada pasada (línea 6.5).
- ➖ Cómo produce asistencias: asiste el 24.5% de las canastas de sus compañeros en pista × 18.3 canastas de compañeros esperadas (su equipo 43.2 por 48' contra esta defensa).
- ➖ Defensa: el rival concede -1% de asistencias por minuto a aleros/ala-pívots (defensa media); ajuste aplicado -1%.
- ❌ Ritmo del partido: +2% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ➖ Últimos 10: la habría pasado 6 de 10.
- ⚠️ en el parte de lesiones: day-to-day.

- ⚠️ Alertas: en el parte de lesiones.
- Asistencias **5.1** (por componentes 4.5 · por tasa por minuto y defensa rival 5.4): asiste el 24.5% de las canastas de sus compañeros en pista × 18.3 canastas de compañeros esperadas (su equipo 43.2 por 48' contra esta defensa).

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 32.0 | 30.7 | 31.9 | 28.9 | - |
| Asistencias | 6.8 | 5.4 | 5.7 | 5.4 | - |
| % de las canastas de compañeros que asiste | 30.2% | 26.7% | 27.5% | 29.3% | - |
| Pérdidas por jugada | 14.5% | 11.9% | 13.0% | 13.2% | - |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -3%, vs defensa media -2%, vs defensa débil +3%; rebotes: vs defensa fuerte -17%, vs defensa media -1%, vs defensa débil +22%; asistencias: vs defensa fuerte +0%, vs defensa media -4%, vs defensa débil +3%; triples: vs defensa fuerte +65%, vs defensa media -13%, vs defensa débil -50%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 59% | 75% | 68% | 70% |
| pintura | 19% | 52% | 45% | 45% |
| media distancia | 13% | 31% | 41% | 39% |
| triple frontal | 9% | 31% | 35% | 36% |
| triple de esquina | 0% | 39% | 38% | 39% |

#### Isaiah Jackson (aleros/ala-pívots) vs Miami Heat

- Minutos esperados: **22.8** (± 3.4); 62 partidos en la base.
- Jordan Miller ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Bradley Beal ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Su prop más probable hoy: **Isaiah Jackson: menos de 7.5 rebotes** (61%). Con 80% de probabilidad: más de 3.5 / menos de 9.5.
- Defensa de Miami Heat contra aleros/ala-pívots en rebotes: +6% respecto a la media; ajuste por su historial contra defensas similares: +1%.

**¿Por qué 6.8 rebotes?** (línea 7.5; 22.8 minutos esperados)

Razonamiento (3 factores a favor, 2 en contra):

- ✅ Minutos: 22.8 esperados (titular, ±3.4).
- ✅ Forma: 6.8 en sus últimos 5, 6.4 esta temporada (7 partidos), 5.3 la temporada pasada (línea 7.5).
- ➖ Cómo produce rebotes: defensivos 4.1 = captura el 18.2% de los fallos del rival en pista × 47.7 fallos esperados del rival (liga 47.0) × 47% del partido; ofensivos 2.4 = 11.3% de los fallos de su equipo × 45.6.
- ❌ Defensa: el rival concede +6% de rebotes por minuto a aleros/ala-pívots (defensa débil); ajuste aplicado +6%.
- ❌ Ritmo del partido: +2% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Últimos 10: la habría pasado 8 de 10.
- ⚠️ Jordan Miller ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ Bradley Beal ya no jugó en sus últimos partidos: la baja ya está en sus minutos.

- ⚠️ Alertas: vetada por el usuario.
- Rebotes **6.8** (por componentes 6.5 · por tasa por minuto y defensa rival 6.9): defensivos 4.1 = captura el 18.2% de los fallos del rival en pista × 47.7 fallos esperados del rival (liga 47.0) × 47% del partido; ofensivos 2.4 = 11.3% de los fallos de su equipo × 45.6.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 22.6 | 21.0 | 22.3 | 16.5 | - |
| Rebotes | 6.8 | 5.9 | 6.4 | 5.3 | - |
| % de los fallos del rival que captura | 17.3% | 17.4% | 18.1% | 20.5% | - |
| % de los fallos de su equipo que captura | 14.0% | 12.6% | 13.3% | 12.5% | - |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -3%, vs defensa media +6%, vs defensa débil -2%; rebotes: vs defensa fuerte -13%, vs defensa media -10%, vs defensa débil +17%; asistencias: vs defensa fuerte +43%, vs defensa media -33%, vs defensa débil -25%; triples: vs defensa fuerte +220%, vs defensa media -100%, vs defensa débil -100%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 67% | 73% | 68% | 67% |
| pintura | 25% | 43% | 45% | 46% |
| media distancia | 5% | 37% | 41% | 41% |
| triple frontal | 2% | 37% | 35% | 35% |
| triple de esquina | 1% | 37% | 38% | 40% |

#### Rui Hachimura (aleros/ala-pívots) vs Miami Heat

- Minutos esperados: **30.0** (± 3.2); 83 partidos en la base.
- Jordan Miller ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Bradley Beal ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- cambio de rol esta temporada (por minuto): reb +74%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Rui Hachimura: menos de 2.5 triples** (60%). Con 80% de probabilidad: más de 0.5 / menos de 3.5.
- Defensa de Miami Heat contra aleros/ala-pívots en triples: +4% respecto a la media; ajuste por su historial contra defensas similares: -1%.

**¿Por qué 2.3 triples?** (línea 2.5; 30.0 minutos esperados)

Razonamiento (1 factores a favor, 3 en contra):

- ✅ Minutos: 30.0 esperados (titular, ±3.2).
- ➖ Forma: 2.4 en sus últimos 5, 2.4 esta temporada (5 partidos), 1.9 la temporada pasada (línea 2.5).
- ➖ Cómo produce triples: 5.5 triples intentados (su ritmo 6.1 por 36'; el rival concede +2% de triples en su reparto) × 44% esperado.
- ❌ Defensa: el rival concede +5% de triples por minuto a aleros/ala-pívots (defensa débil); ajuste aplicado +4%; en su zona principal (triple) el rival concede 35% (liga 35%).
- ❌ Ritmo del partido: +2% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ➖ Contra este rival: 1, 3 (1 de 2 a favor).
- ❌ Últimos 10: la habría pasado 3 de 10.
- ⚠️ Jordan Miller ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ Bradley Beal ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ cambio de rol esta temporada (por minuto): reb +74%; se da más peso a la línea de la casa.

- Triples **2.3** (por componentes 2.4 · por tasa por minuto y defensa rival 2.2): 5.5 triples intentados (su ritmo 6.1 por 36'; el rival concede +2% de triples en su reparto) × 44% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 30.0 | 34.3 | 30.0 | 29.7 | 24.5 |
| Triples anotados | 2.4 | 3.3 | 2.4 | 1.9 | 2.0 |
| Triples intentados | 6.2 | 6.7 | 6.2 | 4.1 | 3.5 |
| % triples | 38.7% | 49.3% | 38.7% | 46.6% | 57.1% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -2%, vs defensa media -5%, vs defensa débil +7%; rebotes: vs defensa fuerte -5%, vs defensa media -3%, vs defensa débil +7%; asistencias: vs defensa fuerte +5%, vs defensa media +6%, vs defensa débil -12%; triples: vs defensa fuerte +0%, vs defensa media -12%, vs defensa débil +10%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 27% | 43% | 35% | 35% |
| media distancia | 22% | 45% | 41% | 41% |
| bajo el aro | 18% | 65% | 68% | 67% |
| triple de esquina | 17% | 44% | 38% | 40% |
| pintura | 14% | 49% | 45% | 46% |

## Sin emparejar con ESPN

Líneas de The Odds API (SportsGameOdds sin respuesta)
