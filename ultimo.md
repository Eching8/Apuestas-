# Props NBA 2026-10-27

> **Aviso:** las apuestas implican riesgo de perder dinero. Estas probabilidades son estimaciones estadísticas, no garantías: ningún modelo acierta siempre y las combinadas multiplican el riesgo. Apuesta solo lo que puedas permitirte perder. Si el juego deja de ser un entretenimiento, busca ayuda.

**Modelo** = minutos, tasa por minuto, bajas, defensa rival por posición, zonas de tiro y tipo de defensa, mezclado con el acierto real del jugador sobre esa línea. **Casa** = probabilidad implícita en las cuotas sin el margen. **Prob. final** = mezcla de ambas. Si modelo y casa discrepan mucho, la casa suele saber algo (rol, rotación, una baja): revísalo antes de apostar.

Cada media se construye desde las estadísticas que la producen (tiros × acierto por zona, % de los rebotes disponibles que captura, % de las canastas de sus compañeros que asiste...) y se muestra con esas estadísticas en sus últimos 5 y 10 partidos, la temporada y contra este rival. Todo queda guardado en la tabla `nba_analisis` de la base.

## Estado de calibración

**En calibración: todos los picks son de prueba.**  0 de 8 criterios cumplidos:

- ⬜ Días con picks liquidados: 1 de 21
- ⬜ Props de línea principal: muestra: 10 de 150
- ⬜ Props de línea principal: aciertan lo prometido: acierto 50.0% vs prometido 67.4%
- ⬜ Picks seguros: muestra: 0 de 150
- ⬜ Picks seguros: aciertan lo prometido: sin datos
- ⬜ Props con cuota: beneficio positivo: -2.78 u en 10
- ⬜ Combinadas: muestra: 0 de 30
- ⬜ Combinadas: ganan lo prometido: sin datos

## Bet builders del día

Por partido, 4 "más de" de titulares estables sin alertas, en líneas un poco por debajo de su nivel (cada pierna ~72 %+). La probabilidad de acertar todas tiene en cuenta que los jugadores de un mismo partido se mueven algo juntos. **Cuota justa** = 1 / probabilidad: si tu casa paga más por el bet builder, tiene valor. Backtest 2025-26: prometían ~32 % y acertaron 38-40 % (conservador).

### Doble: Detroit Pistons @ New York Knicks + Portland Trail Blazers @ Los Angeles Lakers

Probabilidad de acertar los dos bet builders: **11%** (1 de cada 9); cuota justa **8.89**.

**Detroit Pistons @ New York Knicks** — acertar las 4: **34%**, cuota justa 2.97

- Jalen Brunson 18+ puntos (73%; esperado 21.8; últ. 10: 9/10)
- Cade Cunningham 17+ puntos (75%; esperado 21.2; últ. 10: 8/10)
- Karl-Anthony Towns 13+ puntos (76%; esperado 17.1; últ. 10: 8/10)
- OG Anunoby 13+ puntos (76%; esperado 17.4; últ. 10: 8/10)

**Portland Trail Blazers @ Los Angeles Lakers** — acertar las 4: **33%**, cuota justa 3.00

- Austin Reaves 18+ puntos (73%; esperado 22.5; últ. 10: 6/10)
- Luka Doncic 23+ puntos (75%; esperado 30.0; últ. 10: 9/10)
- Walker Kessler 9+ puntos (75%; esperado 15.0; últ. 10: 5/8)
- Donovan Clingan 6+ rebotes (76%; esperado 8.0; últ. 10: 9/10)

**Sacramento Kings @ San Antonio Spurs** — acertar las 4: **31%**, cuota justa 3.26

- Domantas Sabonis 13+ puntos (73%; esperado 17.2; últ. 10: 6/10)
- Precious Achiuwa 12+ puntos (74%; esperado 15.9; últ. 10: 8/10)
- Victor Wembanyama 18+ puntos (74%; esperado 23.4; últ. 10: 9/10)
- Stephon Castle 4+ asistencias (74%; esperado 5.6; últ. 10: 8/10)

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

Hoy ninguna línea principal cumple los filtros de jugador constante.

## Picks seguros de titulares estables

Líneas bajas (alternativas) de titulares con 30+ minutos: mejor un "15+ puntos" casi seguro de una estrella que la línea normal de un suplente. En el backtest, elegidas al 85 % acertaron el 89-96 %. **Cuota mínima** = la que hace falta para que valga la pena (1 / probabilidad); búscala en las líneas alternativas de tu casa.

| Partido | Jugador | Pick seguro | Prob. | Cuota mínima | Esperado | Últ. 10 |
|---|---|---|---|---|---|---|
| Sacramento Kings @ San Antonio Spurs | Domantas Sabonis | **más de 1.5 asistencias** | **90%** | 1.11 | 5.0 | 10/10 |
| Sacramento Kings @ San Antonio Spurs | Domantas Sabonis | **más de 6.5 rebotes** | **90%** | 1.12 | 12.7 | 10/10 |
| Detroit Pistons @ New York Knicks | Josh Hart | **más de 3.5 rebotes** | **89%** | 1.12 | 7.2 | 10/10 |
| Detroit Pistons @ New York Knicks | Karl-Anthony Towns | **más de 5.5 rebotes** | **89%** | 1.12 | 10.7 | 10/10 |
| Portland Trail Blazers @ Los Angeles Lakers | Deni Avdija | **más de 1.5 asistencias** | **89%** | 1.13 | 4.8 | 10/10 |
| Detroit Pistons @ New York Knicks | OG Anunoby | **más de 9.5 puntos** | **89%** | 1.13 | 17.4 | 10/10 |
| Brooklyn Nets @ Boston Celtics | Julius Randle | **más de 2.5 rebotes** | **89%** | 1.13 | 6.2 | 10/10 |
| Sacramento Kings @ San Antonio Spurs | Precious Achiuwa | **más de 4.5 rebotes** | **88%** | 1.14 | 8.6 | 10/10 |
| Brooklyn Nets @ Boston Celtics | Jayson Tatum | **más de 3.5 rebotes** | **88%** | 1.14 | 8.1 | 10/10 |
| Detroit Pistons @ New York Knicks | Karl-Anthony Towns | **más de 19.5 pts+reb+ast** | **88%** | 1.14 | 30.7 | 9/10 |
| Portland Trail Blazers @ Los Angeles Lakers | Walker Kessler | **más de 13.5 pts+reb+ast** | **88%** | 1.14 | 26.4 | 7/8 |
| Brooklyn Nets @ Boston Celtics | Jayson Tatum | **más de 11.5 puntos** | **87%** | 1.14 | 20.8 | 10/10 |
| Brooklyn Nets @ Boston Celtics | Jayson Tatum | **más de 2.5 asistencias** | **87%** | 1.14 | 5.8 | 10/10 |
| Detroit Pistons @ New York Knicks | Jalen Brunson | **más de 13.5 puntos** | **87%** | 1.14 | 21.8 | 10/10 |
| Brooklyn Nets @ Boston Celtics | Julius Randle | **más de 8.5 puntos** | **87%** | 1.15 | 17.4 | 9/10 |

## Las más probables del día

Ninguna prop supera el umbral de probabilidad hoy.

## Brooklyn Nets @ Boston Celtics

Parte de lesiones: Devin Carter (Out); Mikel Brown Jr. (Day-To-Day); Tyler Bilodeau (Out).

Sin líneas de props para este partido (o sin historial suficiente de los jugadores).

## Detroit Pistons @ New York Knicks

Parte de lesiones: Jose Alvarado (Out); Isaiah Joe (Day-To-Day); Jalen Duren (Out); Ausar Thompson (Day-To-Day).

Sin líneas de props para este partido (o sin historial suficiente de los jugadores).

## Sacramento Kings @ San Antonio Spurs

Parte de lesiones: Ben Simmons (Out); Dylan Cardwell (Out); Keegan Murray (Out); Maxime Raynaud (Out); Jayden Quaintance (Out); Tobias Harris (Out).

Sin líneas de props para este partido (o sin historial suficiente de los jugadores).

## Portland Trail Blazers @ Los Angeles Lakers

Parte de lesiones: Branden Carlson (Day-To-Day); Scoot Henderson (Day-To-Day); Chris Youngblood (Out); Shaedon Sharpe (Out); Adou Thiero (Out).

Sin líneas de props para este partido (o sin historial suficiente de los jugadores).
