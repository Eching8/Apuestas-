# Props NBA 2026-10-27

> **Aviso:** las apuestas implican riesgo de perder dinero. Estas probabilidades son estimaciones estadísticas, no garantías: ningún modelo acierta siempre y las combinadas multiplican el riesgo. Apuesta solo lo que puedas permitirte perder. Si el juego deja de ser un entretenimiento, busca ayuda.

**Modelo** = minutos, tasa por minuto, bajas, defensa rival por posición, zonas de tiro y tipo de defensa, mezclado con el acierto real del jugador sobre esa línea. **Casa** = probabilidad implícita en las cuotas sin el margen. **Prob. final** = mezcla de ambas. Si modelo y casa discrepan mucho, la casa suele saber algo (rol, rotación, una baja): revísalo antes de apostar.

Cada media se construye desde las estadísticas que la producen (tiros × acierto por zona, % de los rebotes disponibles que captura, % de las canastas de sus compañeros que asiste...) y se muestra con esas estadísticas en sus últimos 5 y 10 partidos, la temporada y contra este rival. Todo queda guardado en la tabla `nba_analisis` de la base.

## Estado de calibración

**En calibración: todos los picks son de prueba.**  0 de 8 criterios cumplidos:

- ⬜ Días con picks liquidados: 1 de 21
- ⬜ Props de línea principal: muestra: 12 de 150
- ⬜ Props de línea principal: aciertan lo prometido: acierto 50.0% vs prometido 67.3%
- ⬜ Picks seguros: muestra: 0 de 150
- ⬜ Picks seguros: aciertan lo prometido: sin datos
- ⬜ Props con cuota: beneficio positivo: -3.30 u en 12
- ⬜ Combinadas: muestra: 0 de 30
- ⬜ Combinadas: ganan lo prometido: sin datos

## Bet builders del día

Por partido, 4 "más de" de titulares estables sin alertas, en líneas un poco por debajo de su nivel (cada pierna ~72 %+). La probabilidad de acertar todas tiene en cuenta que los jugadores de un mismo partido se mueven algo juntos. **Cuota justa** = 1 / probabilidad: si tu casa paga más por el bet builder, tiene valor. Backtest 2025-26: prometían ~32 % y acertaron 38-40 % (conservador).

### Doble: Detroit Pistons @ New York Knicks + Sacramento Kings @ San Antonio Spurs

Probabilidad de acertar los dos bet builders: **15%** (1 de cada 6); cuota justa **6.46**.

**Detroit Pistons @ New York Knicks** — acertar las 4: **46%**, cuota justa 2.17

- OG Anunoby 4+ rebotes (76%; esperado 5.9; últ. 10: 8/10)
- Josh Hart 1+ triples (81%; esperado 2.0; últ. 10: 8/10)
- Jalen Brunson 1+ triples (84%; esperado 1.9; últ. 10: 10/10)
- Cade Cunningham 1+ triples (88%; esperado 2.5; últ. 10: 9/10)

**Sacramento Kings @ San Antonio Spurs** — acertar las 4: **34%**, cuota justa 2.98

- Precious Achiuwa 12+ puntos (74%; esperado 15.9; últ. 10: 8/10)
- Dylan Harper 4+ rebotes (74%; esperado 5.2; últ. 10: 9/10)
- Zach LaVine 2+ triples (75%; esperado 2.9; últ. 10: 7/10)
- Victor Wembanyama 1+ triples (80%; esperado 1.8; últ. 10: 9/10)

## Combinada segura del día

**Opción A, líneas alternativas (la más segura):** el pick seguro más probable de cada partido, de titulares estables. Búscalas en las líneas alternativas de tu casa ("15+", "20+"...): cada una vale la pena si paga al menos su cuota mínima.

| Partido | Selección | Prob. | Cuota mínima | Esperado | Últ. 10 |
|---|---|---|---|---|---|
| Sacramento Kings @ San Antonio Spurs | **Domantas Sabonis: más de 1.5 asistencias** | **90%** | 1.11 | 5.0 | 10/10 |
| Detroit Pistons @ New York Knicks | **Josh Hart: más de 3.5 rebotes** | **89%** | 1.12 | 7.2 | 10/10 |
| Portland Trail Blazers @ Los Angeles Lakers | **Deni Avdija: más de 1.5 asistencias** | **89%** | 1.13 | 4.8 | 10/10 |
| Brooklyn Nets @ Boston Celtics | **Julius Randle: más de 2.5 rebotes** | **89%** | 1.13 | 6.2 | 10/10 |

| Selecciones | Probabilidad de acertar todas |
|---|---|
| 2 | **80%** |
| 3 | **71%** |
| 4 | **63%** |

**Opción B, líneas principales con cuota real:**

Se elige por **probabilidad**, no por valor: la más probable de cada partido entre jugadores constantes (titulares con minutos estables, sin cambio de rol, traspaso ni lesión, que la habrían pasado en 7+ de sus últimos 10 y en el 60 %+ de esta temporada) y con cuota real de la casa. Si tu casa no ofrece esa línea, usa la siguiente de la lista "Las más seguras con cuota".

| Partido | Selección | Prob. | Cuota | Últ. 10 | Temporada |
|---|---|---|---|---|---|
| Sacramento Kings @ San Antonio Spurs | **Victor Wembanyama: menos de 1.5 robos**<br>el rival concede -9% de robos por minuto a aleros/ala-pívots (defensa fuerte); ajuste aplicado -9% | **69%** | 1.37 | 7/10 | 3/3 |
| Brooklyn Nets @ Boston Celtics | **Jordan Walsh: menos de 1.5 robos**<br>el rival concede +5% de robos por minuto a bases/escoltas (defensa débil); ajuste aplicado +5% | **69%** | 1.41 | 7/10 | 2/3 |
| Detroit Pistons @ New York Knicks | **Cade Cunningham: más de 1.5 triples**<br>el rival concede -2% de triples por minuto a bases/escoltas (defensa media); ajuste aplicado -2%; en su zona principal (triple) el rival concede 35% (liga 35%) | **64%** | 1.55 | 8/10 | 2/3 |

| Selecciones | Probabilidad de acertar todas | Cuota |
|---|---|---|
| 2 | **48%** | 1.93 |
| 3 | **31%** | 2.99 |

### Las más seguras con cuota

| Partido | Prop | Prob. final | Modelo | Casa | Esperado | Últ. 10 | Temporada | vs este rival | Cuota (implícita) |
|---|---|---|---|---|---|---|---|---|---|
| Sacramento Kings @ San Antonio Spurs | **Victor Wembanyama: menos de 1.5 robos** | **69%** | 74% | 67% | 0.9 ± 0.9 | 7/10 | 3/3 | 0, 1 | 1.37 (73%) |
| Brooklyn Nets @ Boston Celtics | **Jordan Walsh: menos de 1.5 robos** | **69%** | 75% | 65% | 0.9 ± 1.1 | 7/10 | 2/3 | 0, 0, 1, 0 | 1.41 (71%) |
| Sacramento Kings @ San Antonio Spurs | **Stephon Castle: menos de 1.5 robos** | **68%** | 69% | 67% | 1.2 ± 1.1 | 9/10 | 2/3 | 0, 0, 1 | 1.39 (72%) |
| Detroit Pistons @ New York Knicks | **Cade Cunningham: más de 1.5 triples** | **64%** | 70% | 61% | 2.5 ± 1.6 | 8/10 | 2/3 | 5, 1, 3 | 1.55 (65%) |
| Detroit Pistons @ New York Knicks | **OG Anunoby: menos de 1.5 robos** | **64%** | 66% | 62% | 1.1 ± 1.2 | 7/10 | 3/3 | 0, 3 | 1.51 (66%) |
| Brooklyn Nets @ Boston Celtics | **Jayson Tatum: menos de 1.5 robos** | **64%** | 62% | 65% | 1.2 ± 1.1 | 7/10 | 2/3 | - | 1.44 (69%) |

## Combinadas con cuota objetivo

La combinación de jugadores constantes (mismos filtros que la opción B, partidos distintos) con más probabilidad de acertar todas cuya cuota llega al objetivo. Se registran como picks de prueba y se liquidan solas: `nba rendimiento` dice cuándo el sistema está listo para dinero real. Una cuota alta nunca es segura: cuota 15 justa acierta 1 de cada 15. Lo que la data puede hacer es acercarse o superar esa probabilidad; si no llega (valor negativo), esa combinada no conviene ese día. **Segura** = solo los picks más probables de jugadores constantes. **De valor** = solo picks donde el modelo ve más de lo que paga la casa. Se registran las dos para ver cuál gana con resultados reales.

**Segura, cuota 2+:** cuota 2.12, probabilidad de acertar todas **45%** (1 de cada 2); valor -6% ⚠️ sin valor: la cuota paga menos de lo que vale el riesgo, mejor no jugarla hoy

- Victor Wembanyama: menos de 1.5 robos (69%, cuota 1.37) — Sacramento Kings @ San Antonio Spurs — 5 factores a favor, 0 en contra
  - el rival concede -9% de robos por minuto a aleros/ala-pívots (defensa fuerte); ajuste aplicado -9%
- Cade Cunningham: más de 1.5 triples (64%, cuota 1.55) — Detroit Pistons @ New York Knicks — 5 factores a favor, 1 en contra
  - el rival concede -2% de triples por minuto a bases/escoltas (defensa media); ajuste aplicado -2%; en su zona principal (triple) el rival concede 35% (liga 35%)

**Segura, cuota 3+:** cuota 3.03, probabilidad de acertar todas **30%** (1 de cada 3); valor -9% ⚠️ sin valor: la cuota paga menos de lo que vale el riesgo, mejor no jugarla hoy

- Jordan Walsh: menos de 1.5 robos (69%, cuota 1.41) — Brooklyn Nets @ Boston Celtics — 4 factores a favor, 1 en contra
  - el rival concede +5% de robos por minuto a bases/escoltas (defensa débil); ajuste aplicado +5%
- Stephon Castle: menos de 1.5 robos (68%, cuota 1.39) — Sacramento Kings @ San Antonio Spurs — 4 factores a favor, 1 en contra
  - el rival concede +6% de robos por minuto a bases/escoltas (defensa débil); ajuste aplicado +6%
- Cade Cunningham: más de 1.5 triples (64%, cuota 1.55) — Detroit Pistons @ New York Knicks — 5 factores a favor, 1 en contra
  - el rival concede -2% de triples por minuto a bases/escoltas (defensa media); ajuste aplicado -2%; en su zona principal (triple) el rival concede 35% (liga 35%)

**De valor, cuota 5+:** cuota 6.02, probabilidad de acertar todas **21%** (1 de cada 5); valor +27% ✅ con valor

- Ziaire Williams: más de 11.5 pts+reb (60%, cuota 1.82) — Portland Trail Blazers @ Los Angeles Lakers — 4 factores a favor, 0 en contra
  - el rival concede -3% de puntos por minuto a aleros/ala-pívots (defensa fuerte); ajuste aplicado -2%; en su zona principal (triple) el rival concede 35% (liga 35%)
- Precious Achiuwa: más de 18.5 pts+reb (60%, cuota 1.81) — Sacramento Kings @ San Antonio Spurs — 3 factores a favor, 3 en contra
  - el rival concede -5% de puntos por minuto a aleros/ala-pívots (defensa fuerte); ajuste aplicado -5%; en su zona principal (aro) el rival concede 63% (liga 68%)
- Karl-Anthony Towns: menos de 35.5 pts+reb+ast (58%, cuota 1.83) — Detroit Pistons @ New York Knicks — 5 factores a favor, 1 en contra
  - el rival concede -13% de puntos por minuto a pívots (defensa fuerte); ajuste aplicado -8%; en su zona principal (aro) el rival concede 64% (liga 68%)

**De valor, cuota 10+:** cuota 10.69, probabilidad de acertar todas **12%** (1 de cada 8); valor +29% ✅ con valor

- Ziaire Williams: más de 11.5 pts+reb (60%, cuota 1.82) — Portland Trail Blazers @ Los Angeles Lakers — 4 factores a favor, 0 en contra
  - el rival concede -3% de puntos por minuto a aleros/ala-pívots (defensa fuerte); ajuste aplicado -2%; en su zona principal (triple) el rival concede 35% (liga 35%)
- Precious Achiuwa: más de 18.5 pts+reb (60%, cuota 1.81) — Sacramento Kings @ San Antonio Spurs — 3 factores a favor, 3 en contra
  - el rival concede -5% de puntos por minuto a aleros/ala-pívots (defensa fuerte); ajuste aplicado -5%; en su zona principal (aro) el rival concede 63% (liga 68%)
- Karl-Anthony Towns: menos de 35.5 pts+reb+ast (58%, cuota 1.83) — Detroit Pistons @ New York Knicks — 5 factores a favor, 1 en contra
  - el rival concede -13% de puntos por minuto a pívots (defensa fuerte); ajuste aplicado -8%; en su zona principal (aro) el rival concede 64% (liga 68%)
- Day'Ron Sharpe: menos de 18.5 pts+reb (58%, cuota 1.77) — Brooklyn Nets @ Boston Celtics — 4 factores a favor, 0 en contra
  - el rival concede -3% de puntos por minuto a pívots (defensa fuerte); ajuste aplicado -4%; en su zona principal (aro) el rival concede 66% (liga 68%)

## Picks seguros de titulares estables

Líneas bajas (alternativas) de titulares con 30+ minutos: mejor un "15+ puntos" casi seguro de una estrella que la línea normal de un suplente. En el backtest, elegidas al 85 % acertaron el 89-96 %. **Cuota mínima** = la que hace falta para que valga la pena (1 / probabilidad); búscala en las líneas alternativas de tu casa.

| Partido | Jugador | Pick seguro | Prob. | Cuota mínima | Esperado | Últ. 10 |
|---|---|---|---|---|---|---|
| Sacramento Kings @ San Antonio Spurs | Domantas Sabonis | **más de 1.5 asistencias** | **90%** | 1.11 | 5.0 | 10/10 |
| Sacramento Kings @ San Antonio Spurs | Domantas Sabonis | **más de 6.5 rebotes** | **90%** | 1.12 | 12.6 | 10/10 |
| Detroit Pistons @ New York Knicks | Josh Hart | **más de 3.5 rebotes** | **89%** | 1.12 | 7.2 | 10/10 |
| Detroit Pistons @ New York Knicks | Karl-Anthony Towns | **más de 5.5 rebotes** | **89%** | 1.12 | 10.7 | 10/10 |
| Portland Trail Blazers @ Los Angeles Lakers | Deni Avdija | **más de 1.5 asistencias** | **89%** | 1.13 | 4.8 | 10/10 |
| Detroit Pistons @ New York Knicks | OG Anunoby | **más de 9.5 puntos** | **89%** | 1.13 | 17.4 | 10/10 |
| Brooklyn Nets @ Boston Celtics | Julius Randle | **más de 2.5 rebotes** | **89%** | 1.13 | 6.2 | 10/10 |
| Sacramento Kings @ San Antonio Spurs | Precious Achiuwa | **más de 4.5 rebotes** | **88%** | 1.14 | 8.5 | 10/10 |
| Detroit Pistons @ New York Knicks | Karl-Anthony Towns | **más de 19.5 pts+reb+ast** | **88%** | 1.14 | 30.7 | 9/10 |
| Brooklyn Nets @ Boston Celtics | Jayson Tatum | **más de 3.5 rebotes** | **88%** | 1.14 | 8.1 | 10/10 |
| Portland Trail Blazers @ Los Angeles Lakers | Walker Kessler | **más de 13.5 pts+reb+ast** | **88%** | 1.14 | 26.5 | 7/8 |
| Brooklyn Nets @ Boston Celtics | Jayson Tatum | **más de 11.5 puntos** | **87%** | 1.14 | 20.8 | 10/10 |
| Brooklyn Nets @ Boston Celtics | Jayson Tatum | **más de 2.5 asistencias** | **87%** | 1.14 | 5.8 | 10/10 |
| Detroit Pistons @ New York Knicks | Jalen Brunson | **más de 13.5 puntos** | **87%** | 1.14 | 21.8 | 10/10 |
| Brooklyn Nets @ Boston Celtics | Julius Randle | **más de 8.5 puntos** | **87%** | 1.15 | 17.4 | 9/10 |

## Las más probables del día

| Partido | Prop | Prob. final | Modelo | Casa | Esperado | Últ. 10 | Temporada | vs este rival | Cuota (implícita) |
|---|---|---|---|---|---|---|---|---|---|
| Detroit Pistons @ New York Knicks | **Ausar Thompson: menos de 0.5 triples** | **78%** | 71% | 82% | 0.4 ± 0.6 | 9/10 | 2/2 | 0, 0, 0 | 1.13 (88%) |
| Sacramento Kings @ San Antonio Spurs | **Victor Wembanyama: menos de 1.5 robos** | **69%** | 74% | 67% | 0.9 ± 0.9 | 7/10 | 3/3 | 0, 1 | 1.37 (73%) |
| Brooklyn Nets @ Boston Celtics | **Jordan Walsh: menos de 1.5 robos** | **69%** | 75% | 65% | 0.9 ± 1.1 | 7/10 | 2/3 | 0, 0, 1, 0 | 1.41 (71%) |
| Sacramento Kings @ San Antonio Spurs | **Stephon Castle: menos de 1.5 robos** | **68%** | 69% | 67% | 1.2 ± 1.1 | 9/10 | 2/3 | 0, 0, 1 | 1.39 (72%) |
| Brooklyn Nets @ Boston Celtics | **Derrick White: menos de 1.5 robos** | **66%** | 69% | 64% | 1.2 ± 1.2 | 8/10 | 2/3 | 1, 1, 2 | 1.44 (69%) |
| Portland Trail Blazers @ Los Angeles Lakers | **Robert Williams III: más de 0.5 tapones** ⚠️ suplente | **65%** | 60% | 68% | 0.9 ± 1.0 | 8/10 | 2/2 | 1, 0 | 1.41 (71%) |

**Si haces combinada:** cada selección que añades multiplica el riesgo. Probabilidad de acertar todas con las más probables de partidos distintos:

- 2 selecciones: **54%**
- 3 selecciones: **37%**
- 4 selecciones: **24%**

Dentro de un mismo partido (bet builder) las selecciones no son independientes y el cálculo es aún menos fiable. Con 12 selecciones al 65 % la probabilidad de acertar todas es menor del 1 %.

### En qué se basan las 10 más probables

#### Ausar Thompson: menos de 0.5 triples (78%) — Detroit Pistons @ New York Knicks

**¿Por qué 0.4 triples?** (línea 0.5; 25.8 minutos esperados)

Razonamiento (4 factores a favor, 2 en contra):

- ❌ Minutos: 25.8 esperados (titular, ±6.8).
- ✅ Forma: 0.2 en sus últimos 5, 0.0 esta temporada (2 partidos), 0.0 la temporada pasada (línea 0.5).
- ➖ Cómo produce triples: 1.7 triples intentados (su ritmo 2.6 por 36'; el rival concede +8% de triples en su reparto) × 32% esperado.
- ➖ Defensa: el rival concede -2% de triples por minuto a bases/escoltas (defensa media); ajuste aplicado -1%; en su zona principal (esquina3) el rival concede 38% (liga 38%).
- ❌ Altura: mide 6'7", 3.2 pulgadas más que los bases/escoltas del rival (+1.1% en esta estadística).
- ✅ Ritmo del partido: -2% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 0, 0, 0 (3 de 3 a favor).
- ✅ Últimos 10: la habría pasado 9 de 10.
- ⚠️ en el parte de lesiones: day-to-day.
- ⚠️ sin Jalen Duren (10 partidos): 26.2 min vs 26.7 con él; pts -12%/min.
- ⚠️ cambio de rol esta temporada (por minuto): ast +64%; se da más peso a la línea de la casa.

- ⚠️ Alertas: minutos inestables, en el parte de lesiones.
- Triples **0.4** (por componentes 0.5 · por tasa por minuto y defensa rival 0.3): 1.7 triples intentados (su ritmo 2.6 por 36'; el rival concede +8% de triples en su reparto) × 32% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 24.8 | 29.3 | 26.0 | 26.6 | 25.0 |
| Triples anotados | 0.2 | 0.1 | 0.0 | 0.1 | 0.0 |
| Triples intentados | 1.0 | 0.7 | 1.0 | 0.4 | 0.0 |
| % triples | 20.0% | 14.3% | 0.0% | 23.3% | - |

#### Victor Wembanyama: menos de 1.5 robos (69%) — Sacramento Kings @ San Antonio Spurs

**¿Por qué 0.9 robos?** (línea 1.5; 32.2 minutos esperados)

Razonamiento (5 factores a favor, 0 en contra):

- ✅ Minutos: 32.2 esperados (titular, ±3.4).
- ✅ Forma: 0.4 en sus últimos 5, 0.7 esta temporada (3 partidos), 1.1 la temporada pasada (línea 1.5).
- ➖ Cómo produce robos: roba el 10.6% de las pérdidas del rival en pista × 12.3 pérdidas esperadas del rival.
- ✅ Defensa: el rival concede -9% de robos por minuto a aleros/ala-pívots (defensa fuerte); ajuste aplicado -9%.
- ➖ Ritmo del partido: +1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 0, 1 (2 de 2 a favor).
- ✅ Últimos 10: la habría pasado 7 de 10.
- ⚠️ cambio de rol esta temporada (por minuto): tpm -33%; se da más peso a la línea de la casa.

- Robos **0.9** (por componentes 0.9 · por tasa por minuto y defensa rival 0.9): roba el 10.6% de las pérdidas del rival en pista × 12.3 pérdidas esperadas del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 35.4 | 36.4 | 31.7 | 29.9 | 26.0 |
| Robos | 0.4 | 1.0 | 0.7 | 1.0 | 0.5 |
| % de las pérdidas del rival que roba | 4.1% | 10.7% | 7.0% | 13.0% | 9.0% |

#### Jordan Walsh: menos de 1.5 robos (69%) — Brooklyn Nets @ Boston Celtics

**¿Por qué 0.9 robos?** (línea 1.5; 16.8 minutos esperados)

Razonamiento (4 factores a favor, 1 en contra):

- ✅ Minutos: 16.8 esperados (titular, ±3.5).
- ✅ Forma: 0.8 en sus últimos 5, 1.3 esta temporada (3 partidos), 0.7 la temporada pasada (línea 1.5).
- ➖ Cómo produce robos: roba el 16.7% de las pérdidas del rival en pista × 13.3 pérdidas esperadas del rival.
- ❌ Defensa: el rival concede +5% de robos por minuto a bases/escoltas (defensa débil); ajuste aplicado +5%.
- ➖ Ritmo del partido: -0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 0, 0, 1, 0 (4 de 4 a favor).
- ✅ Últimos 10: la habría pasado 7 de 10.
- ⚠️ cambio de rol esta temporada (por minuto): pts -39%; se da más peso a la línea de la casa.

- Robos **0.9** (por componentes 0.8 · por tasa por minuto y defensa rival 0.9): roba el 16.7% de las pérdidas del rival en pista × 13.3 pérdidas esperadas del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 15.0 | 14.0 | 17.0 | 17.4 | 16.2 |
| Robos | 0.8 | 0.8 | 1.3 | 0.7 | 0.2 |
| % de las pérdidas del rival que roba | 15.9% | 20.6% | 19.7% | 16.5% | 5.7% |

#### Stephon Castle: menos de 1.5 robos (68%) — Sacramento Kings @ San Antonio Spurs

**¿Por qué 1.2 robos?** (línea 1.5; 29.9 minutos esperados)

Razonamiento (4 factores a favor, 1 en contra):

- ✅ Minutos: 29.9 esperados (titular, ±3.0).
- ✅ Forma: 1.0 en sus últimos 5, 1.3 esta temporada (3 partidos), 1.0 la temporada pasada (línea 1.5).
- ➖ Cómo produce robos: roba el 13.4% de las pérdidas del rival en pista × 12.3 pérdidas esperadas del rival.
- ❌ Defensa: el rival concede +6% de robos por minuto a bases/escoltas (defensa débil); ajuste aplicado +6%.
- ➖ Ritmo del partido: +1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 0, 0, 1 (3 de 3 a favor).
- ✅ Últimos 10: la habría pasado 9 de 10.
- ⚠️ cambio de rol esta temporada (por minuto): ast -32%, tpm +199%; se da más peso a la línea de la casa.

- Robos **1.2** (por componentes 1.0 · por tasa por minuto y defensa rival 1.2): roba el 13.4% de las pérdidas del rival en pista × 12.3 pérdidas esperadas del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 29.4 | 31.5 | 29.7 | 30.8 | 21.0 |
| Robos | 1.0 | 0.9 | 1.3 | 1.1 | 0.3 |
| % de las pérdidas del rival que roba | 12.2% | 11.0% | 14.7% | 13.8% | 7.2% |

#### Derrick White: menos de 1.5 robos (66%) — Brooklyn Nets @ Boston Celtics

**¿Por qué 1.2 robos?** (línea 1.5; 27.8 minutos esperados)

Razonamiento (2 factores a favor, 3 en contra):

- ❌ Minutos: 27.8 esperados (titular, ±8.4).
- ❌ Forma: 1.6 en sus últimos 5, 1.7 esta temporada (3 partidos), 1.0 la temporada pasada (línea 1.5).
- ➖ Cómo produce robos: roba el 14.1% de las pérdidas del rival en pista × 13.3 pérdidas esperadas del rival.
- ❌ Defensa: el rival concede +5% de robos por minuto a bases/escoltas (defensa débil); ajuste aplicado +5%.
- ➖ Ritmo del partido: -0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 1, 1, 2 (2 de 3 a favor).
- ✅ Últimos 10: la habría pasado 8 de 10.
- ⚠️ cambio de rol esta temporada (por minuto): ast +36%; se da más peso a la línea de la casa.
- ⚠️ segundo partido en dos noches: -3% de minutos.

- ⚠️ Alertas: minutos inestables.
- Robos **1.2** (por componentes 1.1 · por tasa por minuto y defensa rival 1.2): roba el 14.1% de las pérdidas del rival en pista × 13.3 pérdidas esperadas del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 32.8 | 33.9 | 29.0 | 34.2 | 32.7 |
| Robos | 1.6 | 1.1 | 1.7 | 1.1 | 1.3 |
| % de las pérdidas del rival que roba | 16.7% | 13.2% | 15.3% | 13.7% | 15.4% |

#### Robert Williams III: más de 0.5 tapones (65%) — Portland Trail Blazers @ Los Angeles Lakers

**¿Por qué 0.9 tapones?** (línea 0.5; 17.5 minutos esperados)

Razonamiento (2 factores a favor, 3 en contra):

- ❌ Minutos: 17.5 esperados (suplente, ±3.0).
- ✅ Forma: 1.2 en sus últimos 5, 1.0 esta temporada (2 partidos), 1.5 la temporada pasada (línea 0.5).
- ➖ Cómo produce tapones: tapona el 5.6% de los tiros de 2 del rival en pista × 52.5 tiros de 2 esperados del rival.
- ❌ Defensa: el rival concede -24% de tapones por minuto a pívots (defensa fuerte); ajuste aplicado -24%.
- ❌ Altura: mide 6'9", 3.5 pulgadas menos que los pívots del rival (-2.6% en esta estadística).
- ➖ Ritmo del partido: -1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ➖ Contra este rival: 1, 0 (1 de 2 a favor).
- ✅ Últimos 10: la habría pasado 8 de 10.
- ⚠️ cambio de rol esta temporada (por minuto): ast -54%; se da más peso a la línea de la casa.

- ⚠️ Alertas: suplente.
- Tapones **0.9** (por componentes 1.1 · por tasa por minuto y defensa rival 0.9): tapona el 5.6% de los tiros de 2 del rival en pista × 52.5 tiros de 2 esperados del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 20.2 | 19.8 | 16.5 | 17.4 | 16.0 |
| Tapones | 1.2 | 1.1 | 1.0 | 1.4 | 0.5 |
| % de los tiros de 2 del rival que tapona | 5.4% | 4.9% | 5.2% | 7.3% | 2.6% |


## Brooklyn Nets @ Boston Celtics

Parte de lesiones: Devin Carter (Out); Mikel Brown Jr. (Day-To-Day); Tyler Bilodeau (Out).

Ventajas del partido (los dos lados): puntos esperados frente a su media de los últimos 10, ajuste por la defensa rival y diferencia de estatura con los rivales de su posición.

| Equipo | Jugador | Puntos esperados | Su media (últ. 10) | Defensa rival en puntos | Rebotes esperados | Altura vs rival |
|---|---|---|---|---|---|---|
| BOS | Jayson Tatum | 20.8 | 23.6 | +2% | 8.1 | -0.3" |
| BKN | Julius Randle | 17.4 | 17.0 | -3% | 6.2 | +1.0" |
| BOS | Paul George | 17.6 | 17.9 | +3% | 5.0 | -0.3" |
| BKN | Michael Porter Jr. | 18.6 | 21.8 | -3% | 5.5 | +2.0" |
| BOS | Derrick White | 11.7 | 11.2 | +1% | 3.5 | -0.8" |
| BOS | Payton Pritchard | 14.2 | 15.1 | +1% | 2.9 | -2.8" |
| BKN | Egor Demin | 10.3 | 8.2 | -4% | 3.0 | +3.4" |
| BKN | Keon Ellis | 7.6 | 3.5 | -4% | 2.2 | -0.6" |
| BKN | Day'Ron Sharpe | 9.2 | 9.8 | -3% | 6.7 | -0.9" |
| BOS | Neemias Queta | 9.3 | 9.0 | +4% | 6.2 | +1.4" |

Picks seguros de titulares estables:

| Jugador | Pick seguro | Prob. | Cuota mínima | Esperado | Últ. 10 |
|---|---|---|---|---|---|
| Julius Randle | **más de 2.5 rebotes** | **89%** | 1.13 | 6.2 | 10/10 |
| Jayson Tatum | **más de 3.5 rebotes** | **88%** | 1.14 | 8.1 | 10/10 |
| Jayson Tatum | **más de 11.5 puntos** | **87%** | 1.14 | 20.8 | 10/10 |
| Jayson Tatum | **más de 2.5 asistencias** | **87%** | 1.14 | 5.8 | 10/10 |
| Julius Randle | **más de 8.5 puntos** | **87%** | 1.15 | 17.4 | 9/10 |
| Julius Randle | **más de 16.5 pts+reb+ast** | **87%** | 1.15 | 27.4 | 9/10 |

Las 8 más probables (máximo 2 por jugador: las de un mismo jugador suelen ganar o perder juntas).

| Prop | Prob. final | Modelo | Casa | Esperado | Últ. 10 | Temporada | vs este rival | Cuota (implícita) |
|---|---|---|---|---|---|---|---|---|
| **Jordan Walsh: menos de 1.5 robos** | **69%** | 75% | 65% | 0.9 ± 1.1 | 7/10 | 2/3 | 0, 0, 1, 0 | 1.41 (71%) |
| **Derrick White: menos de 1.5 robos** | **66%** | 69% | 64% | 1.2 ± 1.2 | 8/10 | 2/3 | 1, 1, 2 | 1.44 (69%) |
| **Noah Clowney: menos de 1.5 triples** ⚠️ suplente | **64%** | 65% | 64% | 1.3 ± 1.1 | 8/10 | 3/3 | 2, 3, 3, 3 | 1.47 (68%) |
| **Keon Ellis: menos de 2.5 asistencias** | **64%** | 71% | 60% | 1.9 ± 1.5 | 8/10 | 1/3 | 0, 2, 1 | 1.55 (65%) |
| **Jayson Tatum: menos de 1.5 robos** | **64%** | 62% | 65% | 1.2 ± 1.1 | 7/10 | 2/3 | - | 1.44 (69%) |
| **Keon Ellis: menos de 1.5 triples** | **63%** | 67% | 61% | 1.3 ± 1.2 | 9/10 | 2/3 | 0, 2, 3 | 1.53 (66%) |
| **Julius Randle: menos de 5.5 asistencias** | **63%** | 75% | 56% | 3.8 ± 2.3 | 7/10 | 1/3 | 4, 6 | 1.68 (60%) |
| **Paul George: menos de 3.5 triples** | **62%** | 67% | 59% | 2.7 ± 1.9 | 5/10 | 2/3 | 2, 2 | 1.59 (63%) |

### Fichas de los jugadores destacados

#### Jordan Walsh (bases/escoltas) vs Brooklyn Nets

- Minutos esperados: **16.8** (± 3.5); 78 partidos en la base.
- cambio de rol esta temporada (por minuto): pts -39%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Jordan Walsh: menos de 1.5 robos** (69%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Brooklyn Nets contra bases/escoltas en robos: +5% respecto a la media; ajuste por su historial contra defensas similares: +4%.

**¿Por qué 0.9 robos?** (línea 1.5; 16.8 minutos esperados)

Razonamiento (4 factores a favor, 1 en contra):

- ✅ Minutos: 16.8 esperados (titular, ±3.5).
- ✅ Forma: 0.8 en sus últimos 5, 1.3 esta temporada (3 partidos), 0.7 la temporada pasada (línea 1.5).
- ➖ Cómo produce robos: roba el 16.7% de las pérdidas del rival en pista × 13.3 pérdidas esperadas del rival.
- ❌ Defensa: el rival concede +5% de robos por minuto a bases/escoltas (defensa débil); ajuste aplicado +5%.
- ➖ Ritmo del partido: -0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 0, 0, 1, 0 (4 de 4 a favor).
- ✅ Últimos 10: la habría pasado 7 de 10.
- ⚠️ cambio de rol esta temporada (por minuto): pts -39%; se da más peso a la línea de la casa.

- Robos **0.9** (por componentes 0.8 · por tasa por minuto y defensa rival 0.9): roba el 16.7% de las pérdidas del rival en pista × 13.3 pérdidas esperadas del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 15.0 | 14.0 | 17.0 | 17.4 | 16.2 |
| Robos | 0.8 | 0.8 | 1.3 | 0.7 | 0.2 |
| % de las pérdidas del rival que roba | 15.9% | 20.6% | 19.7% | 16.5% | 5.7% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -7%, vs defensa media -3%, vs defensa débil +11%; rebotes: vs defensa fuerte +5%, vs defensa media -21%, vs defensa débil +5%; asistencias: vs defensa fuerte -3%, vs defensa media +8%, vs defensa débil -6%; triples: vs defensa fuerte -15%, vs defensa media -1%, vs defensa débil +19%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 37% | 70% | 68% | 69% |
| triple frontal | 29% | 34% | 35% | 37% |
| triple de esquina | 18% | 38% | 38% | 41% |
| pintura | 13% | 39% | 45% | 46% |
| media distancia | 3% | 37% | 41% | 41% |

#### Derrick White (bases/escoltas) vs Brooklyn Nets

- Minutos esperados: **27.8** (± 8.4); 87 partidos en la base.
- cambio de rol esta temporada (por minuto): ast +36%; se da más peso a la línea de la casa
- segundo partido en dos noches: -3% de minutos
- Su prop más probable hoy: **Derrick White: menos de 1.5 robos** (66%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Brooklyn Nets contra bases/escoltas en robos: +5% respecto a la media; ajuste por su historial contra defensas similares: +7%.

**¿Por qué 1.2 robos?** (línea 1.5; 27.8 minutos esperados)

Razonamiento (2 factores a favor, 3 en contra):

- ❌ Minutos: 27.8 esperados (titular, ±8.4).
- ❌ Forma: 1.6 en sus últimos 5, 1.7 esta temporada (3 partidos), 1.0 la temporada pasada (línea 1.5).
- ➖ Cómo produce robos: roba el 14.1% de las pérdidas del rival en pista × 13.3 pérdidas esperadas del rival.
- ❌ Defensa: el rival concede +5% de robos por minuto a bases/escoltas (defensa débil); ajuste aplicado +5%.
- ➖ Ritmo del partido: -0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 1, 1, 2 (2 de 3 a favor).
- ✅ Últimos 10: la habría pasado 8 de 10.
- ⚠️ cambio de rol esta temporada (por minuto): ast +36%; se da más peso a la línea de la casa.
- ⚠️ segundo partido en dos noches: -3% de minutos.

- ⚠️ Alertas: minutos inestables.
- Robos **1.2** (por componentes 1.1 · por tasa por minuto y defensa rival 1.2): roba el 14.1% de las pérdidas del rival en pista × 13.3 pérdidas esperadas del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 32.8 | 33.9 | 29.0 | 34.2 | 32.7 |
| Robos | 1.6 | 1.1 | 1.7 | 1.1 | 1.3 |
| % de las pérdidas del rival que roba | 16.7% | 13.2% | 15.3% | 13.7% | 15.4% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +1%, vs defensa media -5%, vs defensa débil +4%; rebotes: vs defensa fuerte -5%, vs defensa media +2%, vs defensa débil +2%; asistencias: vs defensa fuerte -10%, vs defensa media -12%, vs defensa débil +23%; triples: vs defensa fuerte -6%, vs defensa media +4%, vs defensa débil +2%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 51% | 32% | 35% | 37% |
| pintura | 21% | 43% | 45% | 46% |
| media distancia | 12% | 42% | 41% | 41% |
| bajo el aro | 9% | 72% | 68% | 69% |
| triple de esquina | 7% | 37% | 38% | 41% |

#### Noah Clowney (aleros/ala-pívots) vs Boston Celtics

- Minutos esperados: **20.4** (± 3.0); 69 partidos en la base.
- cambio de rol esta temporada (por minuto): ast -47%, tpm -33%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Noah Clowney: menos de 1.5 triples** (64%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Boston Celtics contra aleros/ala-pívots en triples: +5% respecto a la media; ajuste por su historial contra defensas similares: +1%.

**¿Por qué 1.3 triples?** (línea 1.5; 20.4 minutos esperados)

Razonamiento (2 factores a favor, 4 en contra):

- ❌ Minutos: 20.4 esperados (suplente, ±3.0).
- ✅ Forma: 0.6 en sus últimos 5, 1.0 esta temporada (3 partidos), 2.1 la temporada pasada (línea 1.5).
- ➖ Cómo produce triples: 3.7 triples intentados (su ritmo 6.2 por 36'; el rival concede +8% de triples en su reparto) × 33% esperado.
- ❌ Defensa: el rival concede +10% de triples por minuto a aleros/ala-pívots (defensa débil); ajuste aplicado +5%; en su zona principal (triple) el rival concede 36% (liga 35%).
- ❌ Altura: mide 6'10", 2.0 pulgadas más que los aleros/ala-pívots del rival (+0.7% en esta estadística).
- ➖ Ritmo del partido: -0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ❌ Contra este rival: 2, 3, 3, 3 (0 de 4 a favor).
- ✅ Últimos 10: la habría pasado 8 de 10.
- ⚠️ cambio de rol esta temporada (por minuto): ast -47%, tpm -33%; se da más peso a la línea de la casa.

- ⚠️ Alertas: suplente, cambio de rol.
- Triples **1.3** (por componentes 1.2 · por tasa por minuto y defensa rival 1.3): 3.7 triples intentados (su ritmo 6.2 por 36'; el rival concede +8% de triples en su reparto) × 33% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 20.6 | 19.4 | 20.7 | 27.0 | 31.2 |
| Triples anotados | 0.6 | 1.0 | 1.0 | 2.0 | 2.8 |
| Triples intentados | 2.8 | 3.5 | 2.7 | 5.9 | 7.2 |
| % triples | 21.4% | 28.6% | 37.5% | 32.9% | 37.9% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -1%, vs defensa media -12%, vs defensa débil +12%; rebotes: vs defensa fuerte -23%, vs defensa media -7%, vs defensa débil +26%; asistencias: vs defensa fuerte -12%, vs defensa media +6%, vs defensa débil +8%; triples: vs defensa fuerte -19%, vs defensa media -10%, vs defensa débil +25%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 43% | 30% | 35% | 36% |
| pintura | 20% | 44% | 45% | 43% |
| triple de esquina | 18% | 42% | 38% | 36% |
| bajo el aro | 16% | 62% | 68% | 66% |
| media distancia | 3% | 38% | 41% | 43% |

#### Keon Ellis (bases/escoltas) vs Boston Celtics

- Minutos esperados: **23.5** (± 7.8); 85 partidos en la base.
- cambio de rol esta temporada (por minuto): reb -34%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Keon Ellis: menos de 2.5 asistencias** (64%). Con 80% de probabilidad: más de 0.5 / menos de 3.5.
- Defensa de Boston Celtics contra bases/escoltas en asistencias: -5% respecto a la media; ajuste por su historial contra defensas similares: -2%.

**¿Por qué 1.9 asistencias?** (línea 2.5; 23.5 minutos esperados)

Razonamiento (4 factores a favor, 1 en contra):

- ❌ Minutos: 23.5 esperados (titular, ±7.8).
- ✅ Forma: 1.8 en sus últimos 5, 2.7 esta temporada (3 partidos), 1.1 la temporada pasada (línea 2.5).
- ➖ Cómo produce asistencias: asiste el 12.4% de las canastas de sus compañeros en pista × 14.0 canastas de compañeros esperadas (su equipo 34.2 por 48' contra esta defensa).
- ✅ Defensa: el rival concede -5% de asistencias por minuto a bases/escoltas (defensa fuerte); ajuste aplicado -5%.
- ➖ Ritmo del partido: -0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 0, 2, 1 (3 de 3 a favor).
- ✅ Últimos 10: la habría pasado 8 de 10.
- ⚠️ cambio de rol esta temporada (por minuto): reb -34%; se da más peso a la línea de la casa.

- ⚠️ Alertas: minutos inestables.
- Asistencias **1.9** (por componentes 1.7 · por tasa por minuto y defensa rival 2.0): asiste el 12.4% de las canastas de sus compañeros en pista × 14.0 canastas de compañeros esperadas (su equipo 34.2 por 48' contra esta defensa).

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 19.2 | 12.2 | 26.3 | 19.0 | 23.7 |
| Asistencias | 1.8 | 1.1 | 2.7 | 0.9 | 1.0 |
| % de las canastas de compañeros que asiste | 13.6% | 13.0% | 14.5% | 6.0% | 6.2% |
| Pérdidas por jugada | 12.1% | 19.6% | 14.3% | 9.8% | 11.2% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -12%, vs defensa media +6%, vs defensa débil +9%; rebotes: vs defensa fuerte +2%, vs defensa media +0%, vs defensa débil -2%; asistencias: vs defensa fuerte -31%, vs defensa media +7%, vs defensa débil +25%; triples: vs defensa fuerte +16%, vs defensa media -20%, vs defensa débil -2%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 41% | 36% | 35% | 36% |
| triple de esquina | 24% | 37% | 38% | 36% |
| bajo el aro | 16% | 77% | 68% | 66% |
| pintura | 12% | 46% | 45% | 43% |
| media distancia | 6% | 33% | 41% | 43% |

#### Jayson Tatum (aleros/ala-pívots) vs Brooklyn Nets

- Minutos esperados: **32.8** (± 4.8); 25 partidos en la base.
- cambio de rol esta temporada (por minuto): reb -36%, ast +37%, tpm -46%; se da más peso a la línea de la casa
- segundo partido en dos noches: -3% de minutos
- Su prop más probable hoy: **Jayson Tatum: menos de 1.5 robos** (64%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Brooklyn Nets contra aleros/ala-pívots en robos: +6% respecto a la media; ajuste por su historial contra defensas similares: -3%.

**¿Por qué 1.2 robos?** (línea 1.5; 32.8 minutos esperados)

Razonamiento (3 factores a favor, 1 en contra):

- ✅ Minutos: 32.8 esperados (titular, ±4.8).
- ✅ Forma: 1.4 en sus últimos 5, 1.3 esta temporada (3 partidos), 1.3 la temporada pasada (línea 1.5).
- ➖ Cómo produce robos: roba el 13.1% de las pérdidas del rival en pista × 13.3 pérdidas esperadas del rival.
- ❌ Defensa: el rival concede +6% de robos por minuto a aleros/ala-pívots (defensa débil); ajuste aplicado +6%.
- ➖ Ritmo del partido: -0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Últimos 10: la habría pasado 7 de 10.
- ⚠️ cambio de rol esta temporada (por minuto): reb -36%, ast +37%, tpm -46%; se da más peso a la línea de la casa.
- ⚠️ segundo partido en dos noches: -3% de minutos.

- Robos **1.2** (por componentes 1.2 · por tasa por minuto y defensa rival 1.3): roba el 13.1% de las pérdidas del rival en pista × 13.3 pérdidas esperadas del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 34.6 | 36.1 | 34.3 | 33.6 | - |
| Robos | 1.4 | 1.2 | 1.3 | 1.3 | - |
| % de las pérdidas del rival que roba | 13.1% | 13.4% | 10.1% | 18.7% | - |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +5%, vs defensa media -5%, vs defensa débil +3%; rebotes: vs defensa fuerte -27%, vs defensa media +15%, vs defensa débil +12%; asistencias: vs defensa fuerte -1%, vs defensa media -4%, vs defensa débil +17%; triples: vs defensa fuerte +15%, vs defensa media -10%, vs defensa débil +6%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 42% | 32% | 35% | 37% |
| bajo el aro | 22% | 66% | 68% | 69% |
| pintura | 17% | 43% | 45% | 46% |
| media distancia | 15% | 40% | 41% | 41% |
| triple de esquina | 4% | 39% | 38% | 41% |

## Detroit Pistons @ New York Knicks

Parte de lesiones: Jose Alvarado (Out); Isaiah Joe (Day-To-Day); Jalen Duren (Out); Ausar Thompson (Day-To-Day).

Ventajas del partido (los dos lados): puntos esperados frente a su media de los últimos 10, ajuste por la defensa rival y diferencia de estatura con los rivales de su posición.

| Equipo | Jugador | Puntos esperados | Su media (últ. 10) | Defensa rival en puntos | Rebotes esperados | Altura vs rival |
|---|---|---|---|---|---|---|
| NY | Jalen Brunson | 21.8 | 26.5 | -4% | 3.2 | -3.5" |
| NY | OG Anunoby | 17.4 | 18.9 | -2% | 5.9 | -0.9" |
| NY | Josh Hart | 12.7 | 10.7 | -4% | 7.2 | -0.5" |
| DET | Cade Cunningham | 21.2 | 23.1 | -4% | 5.1 | +2.2" |
| NY | Karl-Anthony Towns | 17.1 | 16.5 | -9% | 10.7 | +2.4" |
| DET | Daniss Jenkins | 14.1 | 10.7 | -4% | 4.8 | +0.2" |
| NY | Mikal Bridges | 10.3 | 9.6 | -4% | 3.1 | +0.5" |
| DET | Duncan Robinson | 17.3 | 14.8 | -2% | 3.6 | -0.1" |
| DET | John Collins | 14.1 | 13.8 | -3% | 6.3 | +1.9" |
| DET | Ausar Thompson | 7.9 | 7.2 | -4% | 5.3 | +3.2" |

Picks seguros de titulares estables:

| Jugador | Pick seguro | Prob. | Cuota mínima | Esperado | Últ. 10 |
|---|---|---|---|---|---|
| Josh Hart | **más de 3.5 rebotes** | **89%** | 1.12 | 7.2 | 10/10 |
| Karl-Anthony Towns | **más de 5.5 rebotes** | **89%** | 1.12 | 10.7 | 10/10 |
| OG Anunoby | **más de 9.5 puntos** | **89%** | 1.13 | 17.4 | 10/10 |
| Karl-Anthony Towns | **más de 19.5 pts+reb+ast** | **88%** | 1.14 | 30.7 | 9/10 |
| Jalen Brunson | **más de 13.5 puntos** | **87%** | 1.14 | 21.8 | 10/10 |
| Jalen Brunson | **más de 20.5 pts+reb+ast** | **87%** | 1.15 | 29.4 | 10/10 |

Las 8 más probables (máximo 2 por jugador: las de un mismo jugador suelen ganar o perder juntas).

| Prop | Prob. final | Modelo | Casa | Esperado | Últ. 10 | Temporada | vs este rival | Cuota (implícita) |
|---|---|---|---|---|---|---|---|---|
| **Ausar Thompson: menos de 0.5 triples** | **78%** | 71% | 82% | 0.4 ± 0.6 | 9/10 | 2/2 | 0, 0, 0 | 1.13 (88%) |
| **Cade Cunningham: más de 1.5 triples** | **64%** | 70% | 61% | 2.5 ± 1.6 | 8/10 | 2/3 | 5, 1, 3 | 1.55 (65%) |
| **Cade Cunningham: menos de 1.5 robos** | **64%** | 65% | 64% | 1.2 ± 1.1 | 6/10 | 2/3 | 1, 0, 1 | 1.50 (67%) |
| **OG Anunoby: menos de 1.5 robos** | **64%** | 66% | 62% | 1.1 ± 1.2 | 7/10 | 3/3 | 0, 3 | 1.51 (66%) |
| **John Collins: menos de 1.5 asistencias** | **63%** | 67% | 61% | 1.2 ± 1.1 | 8/10 | 3/3 | 0 | 1.50 (67%) |
| **Ausar Thompson: más de 0.5 tapones** | **63%** | 57% | 66% | 0.9 ± 1.1 | 8/10 | 1/2 | 0, 3, 0 | 1.44 (70%) |
| **Duncan Robinson: más de 2.5 triples** | **62%** | 72% | 57% | 3.9 ± 2.0 | 8/10 | 3/3 | 3, 3, 2 | 1.65 (60%) |
| **Jalen Brunson: más de 0.5 robos** | **61%** | 56% | 64% | 1.0 ± 1.1 | 4/10 | 1/3 | 2, 2, 0 | 1.49 (67%) |

### Fichas de los jugadores destacados

#### Ausar Thompson (bases/escoltas) vs New York Knicks

- Minutos esperados: **25.8** (± 6.8); 87 partidos en la base.
- en el parte de lesiones: day-to-day
- sin Jalen Duren (10 partidos): 26.2 min vs 26.7 con él; pts -12%/min
- cambio de rol esta temporada (por minuto): ast +64%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Ausar Thompson: menos de 0.5 triples** (78%). Con 80% de probabilidad: más de - / menos de 1.5.
- Defensa de New York Knicks contra bases/escoltas en triples: -1% respecto a la media; ajuste por su historial contra defensas similares: -6%.

**¿Por qué 0.4 triples?** (línea 0.5; 25.8 minutos esperados)

Razonamiento (4 factores a favor, 2 en contra):

- ❌ Minutos: 25.8 esperados (titular, ±6.8).
- ✅ Forma: 0.2 en sus últimos 5, 0.0 esta temporada (2 partidos), 0.0 la temporada pasada (línea 0.5).
- ➖ Cómo produce triples: 1.7 triples intentados (su ritmo 2.6 por 36'; el rival concede +8% de triples en su reparto) × 32% esperado.
- ➖ Defensa: el rival concede -2% de triples por minuto a bases/escoltas (defensa media); ajuste aplicado -1%; en su zona principal (esquina3) el rival concede 38% (liga 38%).
- ❌ Altura: mide 6'7", 3.2 pulgadas más que los bases/escoltas del rival (+1.1% en esta estadística).
- ✅ Ritmo del partido: -2% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 0, 0, 0 (3 de 3 a favor).
- ✅ Últimos 10: la habría pasado 9 de 10.
- ⚠️ en el parte de lesiones: day-to-day.
- ⚠️ sin Jalen Duren (10 partidos): 26.2 min vs 26.7 con él; pts -12%/min.
- ⚠️ cambio de rol esta temporada (por minuto): ast +64%; se da más peso a la línea de la casa.

- ⚠️ Alertas: minutos inestables, en el parte de lesiones.
- Triples **0.4** (por componentes 0.5 · por tasa por minuto y defensa rival 0.3): 1.7 triples intentados (su ritmo 2.6 por 36'; el rival concede +8% de triples en su reparto) × 32% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 24.8 | 29.3 | 26.0 | 26.6 | 25.0 |
| Triples anotados | 0.2 | 0.1 | 0.0 | 0.1 | 0.0 |
| Triples intentados | 1.0 | 0.7 | 1.0 | 0.4 | 0.0 |
| % triples | 20.0% | 14.3% | 0.0% | 23.3% | - |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +9%, vs defensa media -8%, vs defensa débil -4%; rebotes: vs defensa fuerte +1%, vs defensa media -7%, vs defensa débil +3%; asistencias: vs defensa fuerte +5%, vs defensa media -9%, vs defensa débil +3%; triples: vs defensa fuerte -23%, vs defensa media +106%, vs defensa débil -59%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 50% | 68% | 68% | 65% |
| pintura | 39% | 40% | 45% | 43% |
| media distancia | 6% | 36% | 41% | 40% |
| triple de esquina | 3% | 31% | 38% | 38% |
| triple frontal | 2% | 34% | 35% | 35% |

#### Cade Cunningham (bases/escoltas) vs New York Knicks

- Minutos esperados: **33.3** (± 3.0); 82 partidos en la base.
- sin Jalen Duren (8 partidos): 31.1 min vs 35.2 con él; pts +8%/min, reb +14%/min, ast +10%/min
- Su prop más probable hoy: **Cade Cunningham: más de 1.5 triples** (64%). Con 80% de probabilidad: más de 0.5 / menos de 4.5.
- Defensa de New York Knicks contra bases/escoltas en triples: -2% respecto a la media; ajuste por su historial contra defensas similares: -2%.

**¿Por qué 2.5 triples?** (línea 1.5; 33.3 minutos esperados)

Razonamiento (5 factores a favor, 1 en contra):

- ✅ Minutos: 33.3 esperados (titular, ±3.0).
- ✅ Forma: 2.2 en sus últimos 5, 2.0 esta temporada (3 partidos), 2.0 la temporada pasada (línea 1.5).
- ➖ Cómo produce triples: 6.5 triples intentados (su ritmo 6.3 por 36'; el rival concede +8% de triples en su reparto) × 35% esperado.
- ➖ Defensa: el rival concede -2% de triples por minuto a bases/escoltas (defensa media); ajuste aplicado -2%; en su zona principal (triple) el rival concede 35% (liga 35%).
- ✅ Altura: mide 6'6", 2.2 pulgadas más que los bases/escoltas del rival (+0.8% en esta estadística).
- ❌ Ritmo del partido: -2% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 5, 1, 3 (2 de 3 a favor).
- ✅ Últimos 10: la habría pasado 8 de 10.
- ⚠️ sin Jalen Duren (8 partidos): 31.1 min vs 35.2 con él; pts +8%/min, reb +14%/min, ast +10%/min.

- Triples **2.5** (por componentes 2.2 · por tasa por minuto y defensa rival 2.6): 6.5 triples intentados (su ritmo 6.3 por 36'; el rival concede +8% de triples en su reparto) × 35% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 35.4 | 37.8 | 32.7 | 33.9 | 29.7 |
| Triples anotados | 2.2 | 2.3 | 2.0 | 2.0 | 3.0 |
| Triples intentados | 6.8 | 6.0 | 5.7 | 5.8 | 6.0 |
| % triples | 32.4% | 38.3% | 35.3% | 34.6% | 50.0% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -7%, vs defensa media -5%, vs defensa débil +10%; rebotes: vs defensa fuerte -10%, vs defensa media -16%, vs defensa débil +15%; asistencias: vs defensa fuerte -8%, vs defensa media -8%, vs defensa débil +19%; triples: vs defensa fuerte -10%, vs defensa media +6%, vs defensa débil +4%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| pintura | 31% | 44% | 45% | 43% |
| triple frontal | 30% | 35% | 35% | 35% |
| bajo el aro | 22% | 63% | 68% | 65% |
| media distancia | 16% | 46% | 41% | 40% |
| triple de esquina | 2% | 37% | 38% | 38% |

#### OG Anunoby (aleros/ala-pívots) vs Detroit Pistons

- Minutos esperados: **34.0** (± 3.0); 87 partidos en la base.
- cambio de rol esta temporada (por minuto): ast +62%; se da más peso a la línea de la casa
- Su prop más probable hoy: **OG Anunoby: menos de 1.5 robos** (64%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Detroit Pistons contra aleros/ala-pívots en robos: +6% respecto a la media; ajuste por su historial contra defensas similares: +2%.

**¿Por qué 1.1 robos?** (línea 1.5; 34.0 minutos esperados)

Razonamiento (4 factores a favor, 1 en contra):

- ✅ Minutos: 34.0 esperados (titular, ±3.0).
- ✅ Forma: 1.0 en sus últimos 5, 0.3 esta temporada (3 partidos), 1.5 la temporada pasada (línea 1.5).
- ➖ Cómo produce robos: roba el 11.1% de las pérdidas del rival en pista × 14.2 pérdidas esperadas del rival.
- ❌ Defensa: el rival concede +6% de robos por minuto a aleros/ala-pívots (defensa débil); ajuste aplicado +6%.
- ✅ Ritmo del partido: -2% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ➖ Contra este rival: 0, 3 (1 de 2 a favor).
- ✅ Últimos 10: la habría pasado 7 de 10.
- ⚠️ cambio de rol esta temporada (por minuto): ast +62%; se da más peso a la línea de la casa.

- Robos **1.1** (por componentes 1.1 · por tasa por minuto y defensa rival 1.1): roba el 11.1% de las pérdidas del rival en pista × 14.2 pérdidas esperadas del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 35.0 | 34.0 | 33.7 | 33.6 | 30.5 |
| Robos | 1.0 | 1.1 | 0.3 | 1.5 | 1.5 |
| % de las pérdidas del rival que roba | 11.8% | 12.6% | 4.0% | 16.1% | 16.4% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -0%, vs defensa media -3%, vs defensa débil +2%; rebotes: vs defensa fuerte -15%, vs defensa media +7%, vs defensa débil +7%; asistencias: vs defensa fuerte -9%, vs defensa media -2%, vs defensa débil +16%; triples: vs defensa fuerte +0%, vs defensa media -5%, vs defensa débil +7%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 35% | 69% | 68% | 64% |
| triple frontal | 26% | 34% | 35% | 33% |
| triple de esquina | 24% | 44% | 38% | 39% |
| pintura | 9% | 36% | 45% | 44% |
| media distancia | 6% | 42% | 41% | 40% |

#### John Collins (aleros/ala-pívots) vs New York Knicks

- Minutos esperados: **29.1** (± 4.6); 73 partidos en la base.
- sin Jalen Duren: muestra insuficiente (1 partidos sin él)
- cambio de rol esta temporada (por minuto): reb +31%, ast -39%, tpm +67%; se da más peso a la línea de la casa
- Su prop más probable hoy: **John Collins: menos de 1.5 asistencias** (63%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de New York Knicks contra aleros/ala-pívots en asistencias: -2% respecto a la media; ajuste por su historial contra defensas similares: -5%.

**¿Por qué 1.2 asistencias?** (línea 1.5; 29.1 minutos esperados)

Razonamiento (6 factores a favor, 0 en contra):

- ✅ Minutos: 29.1 esperados (titular, ±4.6).
- ✅ Forma: 0.4 en sus últimos 5, 0.7 esta temporada (3 partidos), 1.0 la temporada pasada (línea 1.5).
- ➖ Cómo produce asistencias: asiste el 6.7% de las canastas de sus compañeros en pista × 18.2 canastas de compañeros esperadas (su equipo 39.2 por 48' contra esta defensa).
- ✅ Defensa: el rival concede -2% de asistencias por minuto a aleros/ala-pívots (defensa media); ajuste aplicado -2%.
- ✅ Ritmo del partido: -2% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 0 (1 de 1 a favor).
- ✅ Últimos 10: la habría pasado 8 de 10.
- ⚠️ sin Jalen Duren: muestra insuficiente (1 partidos sin él).
- ⚠️ cambio de rol esta temporada (por minuto): reb +31%, ast -39%, tpm +67%; se da más peso a la línea de la casa.

- ⚠️ Alertas: cambio de rol.
- Asistencias **1.2** (por componentes 1.2 · por tasa por minuto y defensa rival 1.2): asiste el 6.7% de las canastas de sus compañeros en pista × 18.2 canastas de compañeros esperadas (su equipo 39.2 por 48' contra esta defensa).

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 26.0 | 24.7 | 29.3 | 27.0 | 33.0 |
| Asistencias | 0.4 | 0.8 | 0.7 | 1.0 | 0.0 |
| % de las canastas de compañeros que asiste | 2.1% | 4.3% | 3.1% | 5.2% | 0.0% |
| Pérdidas por jugada | 10.7% | 13.3% | 7.4% | 11.8% | 9.6% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -2%, vs defensa media +1%, vs defensa débil +1%; rebotes: vs defensa fuerte +3%, vs defensa media -15%, vs defensa débil +9%; asistencias: vs defensa fuerte +10%, vs defensa media -18%, vs defensa débil +5%; triples: vs defensa fuerte -11%, vs defensa media +5%, vs defensa débil +6%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 34% | 74% | 68% | 65% |
| pintura | 23% | 45% | 45% | 43% |
| triple de esquina | 20% | 43% | 38% | 38% |
| triple frontal | 14% | 37% | 35% | 35% |
| media distancia | 9% | 45% | 41% | 40% |

#### Duncan Robinson (aleros/ala-pívots) vs New York Knicks

- Minutos esperados: **29.4** (± 3.0); 92 partidos en la base.
- sin Jalen Duren (12 partidos): 26.1 min vs 27.9 con él; pts +15%/min, reb +18%/min
- cambio de rol esta temporada (por minuto): pts +53%, tpm +64%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Duncan Robinson: más de 2.5 triples** (62%). Con 80% de probabilidad: más de 1.5 / menos de 5.5.
- Defensa de New York Knicks contra aleros/ala-pívots en triples: +3% respecto a la media; ajuste por su historial contra defensas similares: +1%.

**¿Por qué 3.9 triples?** (línea 2.5; 29.4 minutos esperados)

Razonamiento (5 factores a favor, 1 en contra):

- ✅ Minutos: 29.4 esperados (titular, ±3.0).
- ✅ Forma: 4.4 en sus últimos 5, 5.0 esta temporada (3 partidos), 2.9 la temporada pasada (línea 2.5).
- ➖ Cómo produce triples: 8.4 triples intentados (su ritmo 8.6 por 36'; el rival concede +8% de triples en su reparto) × 41% esperado.
- ✅ Defensa: el rival concede +8% de triples por minuto a aleros/ala-pívots (defensa débil); ajuste aplicado +3%; en su zona principal (triple) el rival concede 35% (liga 35%).
- ❌ Ritmo del partido: -2% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 3, 3, 2 (2 de 3 a favor).
- ✅ Últimos 10: la habría pasado 8 de 10.
- ⚠️ sin Jalen Duren (12 partidos): 26.1 min vs 27.9 con él; pts +15%/min, reb +18%/min.
- ⚠️ cambio de rol esta temporada (por minuto): pts +53%, tpm +64%; se da más peso a la línea de la casa.

- ⚠️ Alertas: cambio de rol.
- Triples **3.9** (por componentes 3.5 · por tasa por minuto y defensa rival 4.0): 8.4 triples intentados (su ritmo 8.6 por 36'; el rival concede +8% de triples en su reparto) × 41% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 26.0 | 29.5 | 29.3 | 27.6 | 20.7 |
| Triples anotados | 4.4 | 3.8 | 5.0 | 2.9 | 2.7 |
| Triples intentados | 8.0 | 7.6 | 9.3 | 6.9 | 6.3 |
| % triples | 55.0% | 50.0% | 53.6% | 41.5% | 42.1% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -0%, vs defensa media +0%, vs defensa débil -0%; rebotes: vs defensa fuerte -12%, vs defensa media -3%, vs defensa débil +13%; asistencias: vs defensa fuerte +2%, vs defensa media -2%, vs defensa débil -0%; triples: vs defensa fuerte -13%, vs defensa media +8%, vs defensa débil +8%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 58% | 42% | 35% | 35% |
| triple de esquina | 20% | 41% | 38% | 38% |
| pintura | 11% | 50% | 45% | 43% |
| bajo el aro | 10% | 65% | 68% | 65% |
| media distancia | 2% | 39% | 41% | 40% |

## Sacramento Kings @ San Antonio Spurs

Parte de lesiones: Ben Simmons (Out); Dylan Cardwell (Out); Keegan Murray (Out); Maxime Raynaud (Out); Jayden Quaintance (Out); Tobias Harris (Out).

Ventajas del partido (los dos lados): puntos esperados frente a su media de los últimos 10, ajuste por la defensa rival y diferencia de estatura con los rivales de su posición.

| Equipo | Jugador | Puntos esperados | Su media (últ. 10) | Defensa rival en puntos | Rebotes esperados | Altura vs rival |
|---|---|---|---|---|---|---|
| SAC | Zach LaVine | 23.2 | 20.2 | -3% | 4.0 | +0.3" |
| SAC | Domantas Sabonis | 17.2 | 15.5 | -5% | 12.6 | -0.3" |
| SAC | Precious Achiuwa | 15.9 | 15.0 | -5% | 8.5 | -2.3" |
| SA | Devin Vassell | 13.5 | 11.5 | +4% | 4.4 | +0.8" |
| SA | Victor Wembanyama | 23.4 | 24.0 | +5% | 10.3 | +7.7" |
| SA | De'Aaron Fox | 17.1 | 13.6 | +5% | 4.2 | -1.2" |
| SA | Dylan Harper | 18.4 | 18.0 | +4% | 5.2 | +0.8" |
| SA | Stephon Castle | 17.6 | 16.4 | +4% | 5.2 | +1.8" |
| SAC | De'Andre Hunter | 9.8 | 9.7 | -4% | 4.3 | -3.3" |
| SAC | Daeqwon Plowden | 9.2 | 9.4 | -3% | 2.6 | +1.3" |

Picks seguros de titulares estables:

| Jugador | Pick seguro | Prob. | Cuota mínima | Esperado | Últ. 10 |
|---|---|---|---|---|---|
| Domantas Sabonis | **más de 1.5 asistencias** | **90%** | 1.11 | 5.0 | 10/10 |
| Domantas Sabonis | **más de 6.5 rebotes** | **90%** | 1.12 | 12.6 | 10/10 |
| Precious Achiuwa | **más de 4.5 rebotes** | **88%** | 1.14 | 8.5 | 10/10 |
| Victor Wembanyama | **más de 5.5 rebotes** | **87%** | 1.15 | 10.3 | 10/10 |
| De'Aaron Fox | **más de 3.5 asistencias** | **87%** | 1.15 | 6.6 | 10/10 |
| Precious Achiuwa | **más de 15.5 pts+reb+ast** | **87%** | 1.15 | 26.2 | 8/10 |

Las 8 más probables (máximo 2 por jugador: las de un mismo jugador suelen ganar o perder juntas).

| Prop | Prob. final | Modelo | Casa | Esperado | Últ. 10 | Temporada | vs este rival | Cuota (implícita) |
|---|---|---|---|---|---|---|---|---|
| **Victor Wembanyama: menos de 1.5 robos** | **69%** | 74% | 67% | 0.9 ± 0.9 | 7/10 | 3/3 | 0, 1 | 1.37 (73%) |
| **Stephon Castle: menos de 1.5 robos** | **68%** | 69% | 67% | 1.2 ± 1.1 | 9/10 | 2/3 | 0, 0, 1 | 1.39 (72%) |
| **Domantas Sabonis: menos de 6.5 asistencias** | **61%** | 72% | 56% | 5.0 ± 2.7 | 6/10 | 1/3 | 5 | 1.67 (60%) |
| **Devin Vassell: menos de 2.5 triples** | **61%** | 59% | 62% | 2.2 ± 1.5 | 6/10 | 3/3 | 2, 0 | 1.51 (66%) |
| **Domantas Sabonis: más de 0.5 robos** | **61%** | 61% | 61% | 1.0 ± 1.0 | 5/10 | 2/3 | 3 | 1.57 (64%) |
| **Precious Achiuwa: más de 10.5 puntos** | **60%** | 78% | 50% | 15.9 ± 5.9 | 8/10 | 3/3 | 10, 14, 1 | 1.85 (54%) |
| **Precious Achiuwa: más de 18.5 pts+reb** | **60%** | 75% | 52% | 24.4 ± 7.7 | 8/10 | 3/3 | 17, 17, 2 | 1.81 (55%) |
| **Devin Vassell: más de 3.5 rebotes** | **59%** | 67% | 55% | 4.4 ± 2.1 | 8/10 | 2/3 | 3, 3 | 1.70 (59%) |

### Fichas de los jugadores destacados

#### Victor Wembanyama (aleros/ala-pívots) vs Sacramento Kings

- Minutos esperados: **32.2** (± 3.4); 92 partidos en la base.
- cambio de rol esta temporada (por minuto): tpm -33%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Victor Wembanyama: menos de 1.5 robos** (69%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Sacramento Kings contra aleros/ala-pívots en robos: -9% respecto a la media; ajuste por su historial contra defensas similares: +1%.

**¿Por qué 0.9 robos?** (línea 1.5; 32.2 minutos esperados)

Razonamiento (5 factores a favor, 0 en contra):

- ✅ Minutos: 32.2 esperados (titular, ±3.4).
- ✅ Forma: 0.4 en sus últimos 5, 0.7 esta temporada (3 partidos), 1.1 la temporada pasada (línea 1.5).
- ➖ Cómo produce robos: roba el 10.6% de las pérdidas del rival en pista × 12.3 pérdidas esperadas del rival.
- ✅ Defensa: el rival concede -9% de robos por minuto a aleros/ala-pívots (defensa fuerte); ajuste aplicado -9%.
- ➖ Ritmo del partido: +1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 0, 1 (2 de 2 a favor).
- ✅ Últimos 10: la habría pasado 7 de 10.
- ⚠️ cambio de rol esta temporada (por minuto): tpm -33%; se da más peso a la línea de la casa.

- Robos **0.9** (por componentes 0.9 · por tasa por minuto y defensa rival 0.9): roba el 10.6% de las pérdidas del rival en pista × 12.3 pérdidas esperadas del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 35.4 | 36.4 | 31.7 | 29.9 | 26.0 |
| Robos | 0.4 | 1.0 | 0.7 | 1.0 | 0.5 |
| % de las pérdidas del rival que roba | 4.1% | 10.7% | 7.0% | 13.0% | 9.0% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -7%, vs defensa media -1%, vs defensa débil +23%; rebotes: vs defensa fuerte -4%, vs defensa media +2%, vs defensa débil +3%; asistencias: vs defensa fuerte -12%, vs defensa media -9%, vs defensa débil +27%; triples: vs defensa fuerte -17%, vs defensa media -3%, vs defensa débil +16%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 37% | 71% | 68% | 71% |
| triple frontal | 30% | 34% | 35% | 37% |
| pintura | 16% | 43% | 45% | 51% |
| media distancia | 15% | 36% | 41% | 43% |
| triple de esquina | 2% | 41% | 38% | 40% |

#### Stephon Castle (bases/escoltas) vs Sacramento Kings

- Minutos esperados: **29.9** (± 3.0); 95 partidos en la base.
- cambio de rol esta temporada (por minuto): ast -32%, tpm +199%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Stephon Castle: menos de 1.5 robos** (68%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Sacramento Kings contra bases/escoltas en robos: +6% respecto a la media; ajuste por su historial contra defensas similares: +5%.

**¿Por qué 1.2 robos?** (línea 1.5; 29.9 minutos esperados)

Razonamiento (4 factores a favor, 1 en contra):

- ✅ Minutos: 29.9 esperados (titular, ±3.0).
- ✅ Forma: 1.0 en sus últimos 5, 1.3 esta temporada (3 partidos), 1.0 la temporada pasada (línea 1.5).
- ➖ Cómo produce robos: roba el 13.4% de las pérdidas del rival en pista × 12.3 pérdidas esperadas del rival.
- ❌ Defensa: el rival concede +6% de robos por minuto a bases/escoltas (defensa débil); ajuste aplicado +6%.
- ➖ Ritmo del partido: +1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 0, 0, 1 (3 de 3 a favor).
- ✅ Últimos 10: la habría pasado 9 de 10.
- ⚠️ cambio de rol esta temporada (por minuto): ast -32%, tpm +199%; se da más peso a la línea de la casa.

- Robos **1.2** (por componentes 1.0 · por tasa por minuto y defensa rival 1.2): roba el 13.4% de las pérdidas del rival en pista × 12.3 pérdidas esperadas del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 29.4 | 31.5 | 29.7 | 30.8 | 21.0 |
| Robos | 1.0 | 0.9 | 1.3 | 1.1 | 0.3 |
| % de las pérdidas del rival que roba | 12.2% | 11.0% | 14.7% | 13.8% | 7.2% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -8%, vs defensa media +11%, vs defensa débil -2%; rebotes: vs defensa fuerte -4%, vs defensa media -4%, vs defensa débil +15%; asistencias: vs defensa fuerte -15%, vs defensa media +18%, vs defensa débil +15%; triples: vs defensa fuerte +13%, vs defensa media -13%, vs defensa débil +0%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 35% | 64% | 68% | 71% |
| triple frontal | 25% | 35% | 35% | 37% |
| pintura | 24% | 40% | 45% | 51% |
| triple de esquina | 8% | 35% | 38% | 40% |
| media distancia | 8% | 40% | 41% | 43% |

#### Domantas Sabonis (aleros/ala-pívots) vs San Antonio Spurs

- Minutos esperados: **35.0** (± 4.0); 22 partidos en la base.
- Dylan Cardwell ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- sin Keegan Murray: muestra insuficiente (20 partidos sin él)
- Maxime Raynaud ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- cambio de rol esta temporada (por minuto): ast +41%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Domantas Sabonis: menos de 6.5 asistencias** (61%). Con 80% de probabilidad: más de 2.5 / menos de 7.5.
- Defensa de San Antonio Spurs contra aleros/ala-pívots en asistencias: -3% respecto a la media; ajuste por su historial contra defensas similares: +2%.

**¿Por qué 5.0 asistencias?** (línea 6.5; 35.0 minutos esperados)

Razonamiento (4 factores a favor, 0 en contra):

- ✅ Minutos: 35.0 esperados (titular, ±4.0).
- ✅ Forma: 5.4 en sus últimos 5, 7.0 esta temporada (3 partidos), 4.1 la temporada pasada (línea 6.5).
- ➖ Cómo produce asistencias: asiste el 19.8% de las canastas de sus compañeros en pista × 22.7 canastas de compañeros esperadas (su equipo 40.1 por 48' contra esta defensa).
- ✅ Defensa: el rival concede -3% de asistencias por minuto a aleros/ala-pívots (defensa fuerte); ajuste aplicado -3%.
- ➖ Ritmo del partido: +1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 5 (1 de 1 a favor).
- ➖ Últimos 10: la habría pasado 6 de 10.
- ⚠️ Dylan Cardwell ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ sin Keegan Murray: muestra insuficiente (20 partidos sin él).
- ⚠️ Maxime Raynaud ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ cambio de rol esta temporada (por minuto): ast +41%; se da más peso a la línea de la casa.

- ⚠️ Alertas: cambio de rol.
- Asistencias **5.0** (por componentes 4.5 · por tasa por minuto y defensa rival 5.2): asiste el 19.8% de las canastas de sus compañeros en pista × 22.7 canastas de compañeros esperadas (su equipo 40.1 por 48' contra esta defensa).

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 32.0 | 28.6 | 36.0 | 29.7 | 36.0 |
| Asistencias | 5.4 | 5.3 | 7.0 | 4.1 | 5.0 |
| % de las canastas de compañeros que asiste | 23.8% | 25.7% | 27.7% | 18.9% | 19.7% |
| Pérdidas por jugada | 20.0% | 21.7% | 26.9% | 16.7% | 16.0% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -0%, vs defensa media +4%, vs defensa débil -3%; rebotes: vs defensa fuerte +1%, vs defensa media +2%, vs defensa débil -3%; asistencias: vs defensa fuerte -1%, vs defensa media +4%, vs defensa débil -3%; triples: vs defensa fuerte +13%, vs defensa media -17%, vs defensa débil +9%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 47% | 70% | 68% | 63% |
| pintura | 38% | 51% | 45% | 42% |
| triple frontal | 9% | 32% | 35% | 35% |
| media distancia | 4% | 45% | 41% | 42% |
| triple de esquina | 2% | 36% | 38% | 35% |

#### Devin Vassell (bases/escoltas) vs Sacramento Kings

- Minutos esperados: **33.5** (± 3.0); 94 partidos en la base.
- cambio de rol esta temporada (por minuto): pts -34%, tpm -48%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Devin Vassell: menos de 2.5 triples** (61%). Con 80% de probabilidad: más de 0.5 / menos de 3.5.
- Defensa de Sacramento Kings contra bases/escoltas en triples: +6% respecto a la media; ajuste por su historial contra defensas similares: +0%.

**¿Por qué 2.2 triples?** (línea 2.5; 33.5 minutos esperados)

Razonamiento (3 factores a favor, 1 en contra):

- ✅ Minutos: 33.5 esperados (titular, ±3.0).
- ✅ Forma: 2.2 en sus últimos 5, 1.3 esta temporada (3 partidos), 2.3 la temporada pasada (línea 2.5).
- ➖ Cómo produce triples: 5.7 triples intentados (su ritmo 6.1 por 36'; el rival concede -1% de triples en su reparto) × 39% esperado.
- ❌ Defensa: el rival concede +7% de triples por minuto a bases/escoltas (defensa débil); ajuste aplicado +6%; en su zona principal (triple) el rival concede 37% (liga 35%).
- ➖ Ritmo del partido: +1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 2, 0 (2 de 2 a favor).
- ➖ Últimos 10: la habría pasado 6 de 10.
- ⚠️ cambio de rol esta temporada (por minuto): pts -34%, tpm -48%; se da más peso a la línea de la casa.

- ⚠️ Alertas: cambio de rol.
- Triples **2.2** (por componentes 2.2 · por tasa por minuto y defensa rival 2.2): 5.7 triples intentados (su ritmo 6.1 por 36'; el rival concede -1% de triples en su reparto) × 39% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 35.6 | 34.9 | 33.0 | 31.6 | 29.0 |
| Triples anotados | 2.2 | 2.3 | 1.3 | 2.5 | 1.0 |
| Triples intentados | 5.2 | 5.6 | 4.3 | 6.5 | 3.5 |
| % triples | 42.3% | 41.1% | 30.8% | 38.2% | 28.6% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +1%, vs defensa media -2%, vs defensa débil +2%; rebotes: vs defensa fuerte +3%, vs defensa media -12%, vs defensa débil +18%; asistencias: vs defensa fuerte -9%, vs defensa media -4%, vs defensa débil +22%; triples: vs defensa fuerte -21%, vs defensa media +14%, vs defensa débil +9%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 40% | 38% | 35% | 37% |
| media distancia | 20% | 48% | 41% | 43% |
| triple de esquina | 18% | 37% | 38% | 40% |
| pintura | 12% | 42% | 45% | 51% |
| bajo el aro | 10% | 65% | 68% | 71% |

#### Precious Achiuwa (aleros/ala-pívots) vs San Antonio Spurs

- Minutos esperados: **34.5** (± 5.9); 76 partidos en la base.
- Dylan Cardwell ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- sin Keegan Murray (51 partidos): 25.2 min vs 22.3 con él; pts +6%/min, reb +7%/min
- Maxime Raynaud ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- cambio de rol esta temporada (por minuto): ast -45%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Precious Achiuwa: más de 10.5 puntos** (60%). Con 80% de probabilidad: más de 10.5 / menos de 21.5.
- Defensa de San Antonio Spurs contra aleros/ala-pívots en puntos: -5% respecto a la media; ajuste por su historial contra defensas similares: +0%.

**¿Por qué 15.9 puntos?** (línea 10.5; 34.5 minutos esperados)

Razonamiento (3 factores a favor, 2 en contra):

- ✅ Minutos: 34.5 esperados (titular, ±5.9).
- ✅ Forma: 14.6 en sus últimos 5, 13.7 esta temporada (3 partidos), 10.8 la temporada pasada (línea 10.5).
- ➖ Cómo produce puntos: 13.4 tiros de campo (su ritmo 12.9 por 36'; el rival concede +2% de tiros) × 1.06 puntos por tiro [bajo el aro 42% de sus tiros al 68% (rival concede 63%, liga 68%); pintura 39% de sus tiros al 48% (rival concede 42%, liga 45%)] + 3.3 tiros libres × 62%.
- ❌ Defensa: el rival concede -5% de puntos por minuto a aleros/ala-pívots (defensa fuerte); ajuste aplicado -5%; en su zona principal (aro) el rival concede 63% (liga 68%).
- ➖ Altura: mide 6'8", 2.3 pulgadas menos que los aleros/ala-pívots del rival (-0.5% en esta estadística).
- ➖ Ritmo del partido: +1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ❌ Contra este rival: 10, 14, 1 (1 de 3 a favor).
- ✅ Últimos 10: la habría pasado 8 de 10.
- ⚠️ Dylan Cardwell ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ sin Keegan Murray (51 partidos): 25.2 min vs 22.3 con él; pts +6%/min, reb +7%/min.
- ⚠️ Maxime Raynaud ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ cambio de rol esta temporada (por minuto): ast -45%; se da más peso a la línea de la casa.

- ⚠️ Alertas: muy lejos de la casa.
- Puntos **15.9** (por componentes 16.3 · por tasa por minuto y defensa rival 15.8): 13.4 tiros de campo (su ritmo 12.9 por 36'; el rival concede +2% de tiros) × 1.06 puntos por tiro [bajo el aro 42% de sus tiros al 68% (rival concede 63%, liga 68%); pintura 39% de sus tiros al 48% (rival concede 42%, liga 45%)] + 3.3 tiros libres × 62%.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 30.8 | 30.5 | 31.3 | 24.0 | 18.7 |
| Puntos | 14.6 | 15.0 | 13.7 | 10.1 | 8.3 |
| Tiros de campo intentados | 12.4 | 12.5 | 10.7 | 8.2 | 7.7 |
| % tiros de campo | 48.4% | 51.2% | 56.2% | 52.8% | 43.5% |
| Triples intentados | 1.8 | 1.6 | 0.7 | 1.3 | 2.3 |
| % triples | 11.1% | 12.5% | 50.0% | 27.8% | 28.6% |
| Tiros libres intentados | 4.8 | 4.4 | 3.7 | 1.9 | 1.7 |
| % tiros libres | 50.0% | 45.5% | 36.4% | 55.4% | 60.0% |
| Jugadas que usa por 36 min | 18.1 | 18.9 | 14.9 | 14.9 | 16.2 |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +1%, vs defensa media -3%, vs defensa débil +2%; rebotes: vs defensa fuerte -12%, vs defensa media +10%, vs defensa débil +4%; asistencias: vs defensa fuerte -7%, vs defensa media -4%, vs defensa débil +14%; triples: vs defensa fuerte -25%, vs defensa media +23%, vs defensa débil +20%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 42% | 68% | 68% | 63% |
| pintura | 39% | 48% | 45% | 42% |
| triple frontal | 9% | 33% | 35% | 35% |
| triple de esquina | 7% | 32% | 38% | 35% |
| media distancia | 4% | 38% | 41% | 42% |

## Portland Trail Blazers @ Los Angeles Lakers

Parte de lesiones: Branden Carlson (Day-To-Day); Scoot Henderson (Day-To-Day); Chris Youngblood (Out); Shaedon Sharpe (Out); Adou Thiero (Out).

Ventajas del partido (los dos lados): puntos esperados frente a su media de los últimos 10, ajuste por la defensa rival y diferencia de estatura con los rivales de su posición.

| Equipo | Jugador | Puntos esperados | Su media (últ. 10) | Defensa rival en puntos | Rebotes esperados | Altura vs rival |
|---|---|---|---|---|---|---|
| LAL | Austin Reaves | 22.5 | 21.5 | -0% | 3.8 | +0.9" |
| LAL | Luka Doncic | 30.0 | 36.6 | +0% | 6.7 | +3.9" |
| POR | Deni Avdija | 20.9 | 25.6 | +0% | 6.4 | -0.3" |
| LAL | Walker Kessler | 15.0 | 15.2 | +3% | 9.3 | +2.3" |
| LAL | Ziaire Williams | 12.3 | 13.8 | -2% | 3.7 | +1.5" |
| POR | Toumani Camara | 12.5 | 10.0 | -0% | 3.8 | -1.3" |
| POR | Jrue Holiday | 13.0 | 15.5 | -0% | 3.3 | -0.6" |
| POR | Ja Morant | 15.2 | 20.0 | +0% | 3.0 | -2.6" |
| LAL | Quentin Grimes | 10.1 | 7.3 | -0% | 3.3 | -0.1" |
| POR | Sidy Cissoko | 7.6 | 3.3 | +0% | 3.2 | +1.4" |

Picks seguros de titulares estables:

| Jugador | Pick seguro | Prob. | Cuota mínima | Esperado | Últ. 10 |
|---|---|---|---|---|---|
| Deni Avdija | **más de 1.5 asistencias** | **89%** | 1.13 | 4.8 | 10/10 |
| Walker Kessler | **más de 13.5 pts+reb+ast** | **88%** | 1.14 | 26.5 | 7/8 |
| Walker Kessler | **más de 5.5 rebotes** | **87%** | 1.15 | 9.3 | 8/8 |
| Deni Avdija | **más de 20.5 pts+reb+ast** | **87%** | 1.15 | 32.1 | 10/10 |
| Walker Kessler | **más de 4.5 puntos** | **87%** | 1.15 | 15.0 | 5/8 |
| Austin Reaves | **más de 14.5 puntos** | **86%** | 1.16 | 22.5 | 9/10 |

Las 8 más probables (máximo 2 por jugador: las de un mismo jugador suelen ganar o perder juntas).

| Prop | Prob. final | Modelo | Casa | Esperado | Últ. 10 | Temporada | vs este rival | Cuota (implícita) |
|---|---|---|---|---|---|---|---|---|
| **Robert Williams III: más de 0.5 tapones** ⚠️ suplente | **65%** | 60% | 68% | 0.9 ± 1.0 | 8/10 | 2/2 | 1, 0 | 1.41 (71%) |
| **Collin Sexton: más de 0.5 robos** | **65%** | 69% | 63% | 1.4 ± 1.4 | 9/10 | 1/2 | 1 | 1.51 (66%) |
| **Quentin Grimes: menos de 1.5 triples** ⚠️ suplente | **65%** | 66% | 64% | 1.2 ± 1.2 | 6/10 | 2/3 | 1 | 1.47 (68%) |
| **Deni Avdija: más de 0.5 robos** | **64%** | 61% | 66% | 1.0 ± 1.0 | 5/10 | 2/2 | 1, 1 | 1.44 (70%) |
| **Sandro Mamukelashvili: más de 0.5 triples** ⚠️ suplente | **63%** | 63% | 62% | 1.0 ± 1.0 | 5/10 | 2/3 | 3, 0 | 1.50 (67%) |
| **Jrue Holiday: más de 0.5 robos** | **62%** | 63% | 62% | 1.1 ± 1.1 | 7/10 | 2/2 | 0, 1, 1 | 1.54 (65%) |
| **Austin Reaves: menos de 2.5 triples** | **62%** | 63% | 61% | 2.2 ± 1.5 | 6/10 | 1/3 | 3 | 1.53 (66%) |
| **Ziaire Williams: más de 2.5 rebotes** | **61%** | 66% | 58% | 3.7 ± 2.0 | 5/10 | 2/3 | 4, 1 | 1.62 (62%) |

### Fichas de los jugadores destacados

#### Robert Williams III (pívots) vs Los Angeles Lakers

- Minutos esperados: **17.5** (± 3.0); 67 partidos en la base.
- cambio de rol esta temporada (por minuto): ast -54%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Robert Williams III: más de 0.5 tapones** (65%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Los Angeles Lakers contra pívots en tapones: -24% respecto a la media; ajuste por su historial contra defensas similares: -0%.

**¿Por qué 0.9 tapones?** (línea 0.5; 17.5 minutos esperados)

Razonamiento (2 factores a favor, 3 en contra):

- ❌ Minutos: 17.5 esperados (suplente, ±3.0).
- ✅ Forma: 1.2 en sus últimos 5, 1.0 esta temporada (2 partidos), 1.5 la temporada pasada (línea 0.5).
- ➖ Cómo produce tapones: tapona el 5.6% de los tiros de 2 del rival en pista × 52.5 tiros de 2 esperados del rival.
- ❌ Defensa: el rival concede -24% de tapones por minuto a pívots (defensa fuerte); ajuste aplicado -24%.
- ❌ Altura: mide 6'9", 3.5 pulgadas menos que los pívots del rival (-2.6% en esta estadística).
- ➖ Ritmo del partido: -1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ➖ Contra este rival: 1, 0 (1 de 2 a favor).
- ✅ Últimos 10: la habría pasado 8 de 10.
- ⚠️ cambio de rol esta temporada (por minuto): ast -54%; se da más peso a la línea de la casa.

- ⚠️ Alertas: suplente.
- Tapones **0.9** (por componentes 1.1 · por tasa por minuto y defensa rival 0.9): tapona el 5.6% de los tiros de 2 del rival en pista × 52.5 tiros de 2 esperados del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 20.2 | 19.8 | 16.5 | 17.4 | 16.0 |
| Tapones | 1.2 | 1.1 | 1.0 | 1.4 | 0.5 |
| % de los tiros de 2 del rival que tapona | 5.4% | 4.9% | 5.2% | 7.3% | 2.6% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -5%, vs defensa media +1%, vs defensa débil +4%; rebotes: vs defensa fuerte -5%, vs defensa media -7%, vs defensa débil +9%; asistencias: vs defensa fuerte -13%, vs defensa media -24%, vs defensa débil +22%; triples: vs defensa fuerte -18%, vs defensa media -35%, vs defensa débil +61%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 67% | 76% | 68% | 73% |
| pintura | 18% | 51% | 45% | 44% |
| triple de esquina | 9% | 39% | 38% | 37% |
| media distancia | 3% | 46% | 41% | 43% |
| triple frontal | 3% | 33% | 35% | 34% |

#### Collin Sexton (bases/escoltas) vs Portland Trail Blazers

- Minutos esperados: **20.2** (± 4.7); 70 partidos en la base.
- cambio de rol esta temporada (por minuto): ast -40%; se da más peso a la línea de la casa
- solo 2 partidos con su equipo actual: su rol puede haber cambiado, se da más peso a la línea de la casa
- Su prop más probable hoy: **Collin Sexton: más de 0.5 robos** (65%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Portland Trail Blazers contra bases/escoltas en robos: +24% respecto a la media; ajuste por su historial contra defensas similares: +2%.

**¿Por qué 1.4 robos?** (línea 0.5; 20.2 minutos esperados)

Razonamiento (5 factores a favor, 0 en contra):

- ✅ Minutos: 20.2 esperados (titular, ±4.7).
- ✅ Forma: 2.0 en sus últimos 5, 1.5 esta temporada (2 partidos), 1.2 la temporada pasada (línea 0.5).
- ➖ Cómo produce robos: roba el 17.5% de las pérdidas del rival en pista × 16.3 pérdidas esperadas del rival.
- ✅ Defensa: el rival concede +24% de robos por minuto a bases/escoltas (defensa débil); ajuste aplicado +24%.
- ➖ Ritmo del partido: -1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 1 (1 de 1 a favor).
- ✅ Últimos 10: la habría pasado 9 de 10.
- ⚠️ cambio de rol esta temporada (por minuto): ast -40%; se da más peso a la línea de la casa.
- ⚠️ solo 2 partidos con su equipo actual: su rol puede haber cambiado, se da más peso a la línea de la casa.

- ⚠️ Alertas: traspaso reciente.
- Robos **1.4** (por componentes 1.2 · por tasa por minuto y defensa rival 1.4): roba el 17.5% de las pérdidas del rival en pista × 16.3 pérdidas esperadas del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 25.0 | 26.8 | 18.0 | 23.7 | 18.0 |
| Robos | 2.0 | 2.0 | 1.5 | 1.1 | 1.0 |
| % de las pérdidas del rival que roba | 21.8% | 23.1% | 19.5% | 17.7% | 22.2% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -1%, vs defensa media -1%, vs defensa débil +1%; rebotes: vs defensa fuerte -10%, vs defensa media +8%, vs defensa débil +2%; asistencias: vs defensa fuerte -25%, vs defensa media +19%, vs defensa débil +12%; triples: vs defensa fuerte -1%, vs defensa media -12%, vs defensa débil +13%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 31% | 37% | 35% | 35% |
| bajo el aro | 30% | 66% | 68% | 66% |
| pintura | 23% | 44% | 45% | 46% |
| media distancia | 9% | 39% | 41% | 42% |
| triple de esquina | 7% | 43% | 38% | 38% |

#### Quentin Grimes (bases/escoltas) vs Portland Trail Blazers

- Minutos esperados: **25.0** (± 4.8); 90 partidos en la base.
- cambio de rol esta temporada (por minuto): tpm -32%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Quentin Grimes: menos de 1.5 triples** (65%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Portland Trail Blazers contra bases/escoltas en triples: -4% respecto a la media; ajuste por su historial contra defensas similares: -1%.

**¿Por qué 1.2 triples?** (línea 1.5; 25.0 minutos esperados)

Razonamiento (3 factores a favor, 1 en contra):

- ❌ Minutos: 25.0 esperados (suplente, ±4.8).
- ✅ Forma: 1.4 en sus últimos 5, 1.0 esta temporada (3 partidos), 1.4 la temporada pasada (línea 1.5).
- ➖ Cómo produce triples: 3.4 triples intentados (su ritmo 5.3 por 36'; el rival concede -6% de triples en su reparto) × 34% esperado.
- ✅ Defensa: el rival concede -8% de triples por minuto a bases/escoltas (defensa fuerte); ajuste aplicado -4%; en su zona principal (triple) el rival concede 35% (liga 35%).
- ➖ Ritmo del partido: -1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 1 (1 de 1 a favor).
- ➖ Últimos 10: la habría pasado 6 de 10.
- ⚠️ cambio de rol esta temporada (por minuto): tpm -32%; se da más peso a la línea de la casa.

- ⚠️ Alertas: suplente, cambio de rol.
- Triples **1.2** (por componentes 1.2 · por tasa por minuto y defensa rival 1.2): 3.4 triples intentados (su ritmo 5.3 por 36'; el rival concede -6% de triples en su reparto) × 34% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 23.2 | 23.6 | 26.0 | 28.5 | 40.0 |
| Triples anotados | 1.4 | 1.3 | 1.0 | 1.6 | 1.0 |
| Triples intentados | 3.6 | 3.4 | 2.7 | 4.8 | 4.0 |
| % triples | 38.9% | 38.2% | 37.5% | 33.9% | 25.0% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -1%, vs defensa media -2%, vs defensa débil +4%; rebotes: vs defensa fuerte -3%, vs defensa media +7%, vs defensa débil -0%; asistencias: vs defensa fuerte -4%, vs defensa media -8%, vs defensa débil +12%; triples: vs defensa fuerte -8%, vs defensa media -2%, vs defensa débil +12%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 39% | 31% | 35% | 35% |
| bajo el aro | 29% | 69% | 68% | 66% |
| pintura | 12% | 41% | 45% | 46% |
| triple de esquina | 12% | 43% | 38% | 38% |
| media distancia | 8% | 37% | 41% | 42% |

#### Deni Avdija (aleros/ala-pívots) vs Los Angeles Lakers

- Minutos esperados: **32.0** (± 7.0); 76 partidos en la base.
- cambio de rol esta temporada (por minuto): reb +38%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Deni Avdija: más de 0.5 robos** (64%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Los Angeles Lakers contra aleros/ala-pívots en robos: +7% respecto a la media; ajuste por su historial contra defensas similares: -0%.

**¿Por qué 1.0 robos?** (línea 0.5; 32.0 minutos esperados)

Razonamiento (3 factores a favor, 1 en contra):

- ❌ Minutos: 32.0 esperados (titular, ±7.0).
- ✅ Forma: 0.8 en sus últimos 5, 1.5 esta temporada (2 partidos), 0.8 la temporada pasada (línea 0.5).
- ➖ Cómo produce robos: roba el 10.5% de las pérdidas del rival en pista × 15.1 pérdidas esperadas del rival.
- ✅ Defensa: el rival concede +7% de robos por minuto a aleros/ala-pívots (defensa débil); ajuste aplicado +7%.
- ➖ Ritmo del partido: -1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 1, 1 (2 de 2 a favor).
- ➖ Últimos 10: la habría pasado 5 de 10.
- ⚠️ cambio de rol esta temporada (por minuto): reb +38%; se da más peso a la línea de la casa.

- ⚠️ Alertas: minutos inestables.
- Robos **1.0** (por componentes 1.1 · por tasa por minuto y defensa rival 1.0): roba el 10.5% de las pérdidas del rival en pista × 15.1 pérdidas esperadas del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 33.4 | 34.2 | 30.5 | 32.8 | 34.0 |
| Robos | 0.8 | 0.6 | 1.5 | 0.7 | 1.0 |
| % de las pérdidas del rival que roba | 8.5% | 6.0% | 16.4% | 7.4% | 7.1% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -1%, vs defensa media +2%, vs defensa débil -1%; rebotes: vs defensa fuerte -9%, vs defensa media -9%, vs defensa débil +25%; asistencias: vs defensa fuerte -13%, vs defensa media +4%, vs defensa débil +11%; triples: vs defensa fuerte -3%, vs defensa media +7%, vs defensa débil -3%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 33% | 67% | 68% | 73% |
| triple frontal | 32% | 33% | 35% | 34% |
| pintura | 26% | 42% | 45% | 44% |
| media distancia | 5% | 43% | 41% | 43% |
| triple de esquina | 4% | 35% | 38% | 37% |

#### Sandro Mamukelashvili (aleros/ala-pívots) vs Portland Trail Blazers

- Minutos esperados: **21.3** (± 3.3); 90 partidos en la base.
- cambio de rol esta temporada (por minuto): pts -37%, tpm -53%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Sandro Mamukelashvili: más de 0.5 triples** (63%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Portland Trail Blazers contra aleros/ala-pívots en triples: -5% respecto a la media; ajuste por su historial contra defensas similares: -2%.

**¿Por qué 1.0 triples?** (línea 0.5; 21.3 minutos esperados)

Razonamiento (1 factores a favor, 3 en contra):

- ❌ Minutos: 21.3 esperados (suplente, ±3.3).
- ❌ Forma: 0.4 en sus últimos 5, 0.7 esta temporada (3 partidos), 1.5 la temporada pasada (línea 0.5).
- ➖ Cómo produce triples: 2.7 triples intentados (su ritmo 4.9 por 36'; el rival concede -6% de triples en su reparto) × 38% esperado.
- ❌ Defensa: el rival concede -9% de triples por minuto a aleros/ala-pívots (defensa fuerte); ajuste aplicado -5%; en su zona principal (triple) el rival concede 35% (liga 35%).
- ✅ Altura: mide 6'9", 1.5 pulgadas más que los aleros/ala-pívots del rival (+0.5% en esta estadística).
- ➖ Ritmo del partido: -1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ➖ Contra este rival: 3, 0 (1 de 2 a favor).
- ➖ Últimos 10: la habría pasado 5 de 10.
- ⚠️ cambio de rol esta temporada (por minuto): pts -37%, tpm -53%; se da más peso a la línea de la casa.

- ⚠️ Alertas: suplente, cambio de rol.
- Triples **1.0** (por componentes 1.0 · por tasa por minuto y defensa rival 1.0): 2.7 triples intentados (su ritmo 4.9 por 36'; el rival concede -6% de triples en su reparto) × 38% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 18.0 | 17.0 | 22.3 | 21.3 | 27.0 |
| Triples anotados | 0.4 | 0.6 | 0.7 | 1.4 | 1.5 |
| Triples intentados | 1.6 | 1.9 | 1.7 | 3.6 | 3.5 |
| % triples | 25.0% | 31.6% | 40.0% | 38.4% | 42.9% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -9%, vs defensa media +0%, vs defensa débil +8%; rebotes: vs defensa fuerte +0%, vs defensa media +2%, vs defensa débil -2%; asistencias: vs defensa fuerte -6%, vs defensa media +9%, vs defensa débil -4%; triples: vs defensa fuerte -18%, vs defensa media +2%, vs defensa débil +11%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 37% | 71% | 68% | 66% |
| triple frontal | 36% | 39% | 35% | 35% |
| pintura | 16% | 46% | 45% | 46% |
| triple de esquina | 10% | 37% | 38% | 38% |
| media distancia | 1% | 40% | 41% | 42% |
