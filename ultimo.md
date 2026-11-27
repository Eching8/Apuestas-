# Props NBA 2026-11-27

> **Aviso:** las apuestas implican riesgo de perder dinero. Estas probabilidades son estimaciones estadísticas, no garantías: ningún modelo acierta siempre y las combinadas multiplican el riesgo. Apuesta solo lo que puedas permitirte perder. Si el juego deja de ser un entretenimiento, busca ayuda.

**Modelo** = minutos, tasa por minuto, bajas, defensa rival por posición, zonas de tiro y tipo de defensa, mezclado con el acierto real del jugador sobre esa línea. **Casa** = probabilidad implícita en las cuotas sin el margen. **Prob. final** = mezcla de ambas. Si modelo y casa discrepan mucho, la casa suele saber algo (rol, rotación, una baja): revísalo antes de apostar.

Cada media se construye desde las estadísticas que la producen (tiros × acierto por zona, % de los rebotes disponibles que captura, % de las canastas de sus compañeros que asiste...) y se muestra con esas estadísticas en sus últimos 5 y 10 partidos, la temporada y contra este rival. Todo queda guardado en la tabla `nba_analisis` de la base.

## Estado de calibración

**Listo para dinero real.** 8 de 8 criterios cumplidos:

- ✅ Días con picks liquidados: 29 de 21
- ✅ Props de línea principal: muestra: 475 de 150
- ✅ Props de línea principal: aciertan lo prometido: acierto 66.7% vs prometido 67.5%
- ✅ Picks seguros: muestra: 831 de 150
- ✅ Picks seguros: aciertan lo prometido: acierto 88.8% vs prometido 86.7%
- ✅ Props con cuota: beneficio positivo: +1.44 u en 475
- ✅ Combinadas: muestra: 245 de 30
- ✅ Combinadas: ganan lo prometido: ganadas 37.1% vs prometido 33.4%

### Acumulado de las combinadas de prueba

| Tipo | Jugadas | Ganadas | % ganadas | Prob. prometida | Beneficio (1 u, con cuota) |
|---|---|---|---|---|---|
| Combinada segura A (alternas) | 16 | 11 | 69% | 65% | - |
| Bet builder | 88 | 39 | 44% | 40% | - |
| Segura cuota 10+ | 6 | 0 | 0% | 12% | -6.00 u en 6 |
| Segura cuota 15+ | 3 | 0 | 0% | 8% | -3.00 u en 3 |
| Segura cuota 2+ | 24 | 14 | 58% | 47% | +5.68 u en 24 |
| Segura cuota 3+ | 21 | 11 | 52% | 33% | +13.58 u en 21 |
| Segura cuota 5+ | 18 | 3 | 17% | 21% | -3.36 u en 18 |
| Doble de bet builders | 22 | 4 | 18% | 19% | - |
| Combinada segura B (principales) | 24 | 8 | 33% | 25% | +4.90 u en 24 |
| Rachas de temporada (4 patas) | 5 | 0 | 0% | 16% | -5.00 u en 5 |
| Rachas de temporada (8 patas) | 3 | 0 | 0% | 3% | -3.00 u en 3 |
| Tus apuestas | 39 | 3 | 8% | 12% | -31.28 u en 38 |
| De valor cuota 10+ | 4 | 0 | 0% | 13% | -4.00 u en 4 |
| De valor cuota 15+ | 3 | 1 | 33% | 9% | +12.17 u en 3 |
| De valor cuota 30+ | 2 | 0 | 0% | 5% | -2.00 u en 2 |
| De valor cuota 5+ | 6 | 0 | 0% | 22% | -6.00 u en 6 |

## Bet builders del día

Por partido, 4 "más de" de titulares estables sin alertas, en líneas un poco por debajo de su nivel (cada pierna ~72 %+). La probabilidad de acertar todas tiene en cuenta que los jugadores de un mismo partido se mueven algo juntos. **Cuota justa** = 1 / probabilidad (solo para saber cuánto debería pagar; se elige por probabilidad). Backtest 2025-26: prometían ~32 % y acertaron 38-40 % (conservador).

### Doble: Philadelphia 76ers @ Indiana Pacers + Golden State Warriors @ Portland Trail Blazers

Probabilidad de acertar los dos bet builders: **28%** (1 de cada 4); cuota justa **3.57**.

**Philadelphia 76ers @ Indiana Pacers** — acertar las 4: **54%**, cuota justa 1.84

- Pascal Siakam 1+ triples (78%; esperado 1.8; últ. 10: 9/10)
- VJ Edgecombe 1+ triples (81%; esperado 1.9; últ. 10: 8/10)
- Andrew Nembhard 1+ triples (85%; esperado 2.2; últ. 10: 10/10)

**Golden State Warriors @ Portland Trail Blazers** — acertar las 4: **52%**, cuota justa 1.94

- De'Anthony Melton 2+ asistencias (76%; esperado 3.0; últ. 10: 8/10)
- Sidy Cissoko 1+ triples (78%; esperado 1.7; últ. 10: 9/10)
- Deni Avdija 1+ triples (86%; esperado 2.3; últ. 10: 10/10)

**Memphis Grizzlies @ Minnesota Timberwolves** — acertar las 4: **46%**, cuota justa 2.19

- Jaden McDaniels 3+ asistencias (73%; esperado 3.7; últ. 10: 9/10)
- Jaylen Wells 1+ triples (78%; esperado 1.7; últ. 10: 9/10)
- Cedric Coward 1+ triples (79%; esperado 1.9; últ. 10: 7/10)

**Dallas Mavericks @ Phoenix Suns** — acertar las 4: **37%**, cuota justa 2.67

- Miles Bridges 2+ asistencias (78%; esperado 2.9; últ. 10: 9/10)
- P.J. Washington 1+ triples (74%; esperado 1.5; últ. 10: 9/10)
- Dillon Brooks 1+ triples (77%; esperado 1.9; últ. 10: 7/10)
- Devin Booker 1+ triples (83%; esperado 2.0; últ. 10: 9/10)

**Miami Heat @ New York Knicks** — acertar las 4: **37%**, cuota justa 2.68

- Pelle Larsson 2+ asistencias (76%; esperado 2.9; últ. 10: 9/10)
- Landry Shamet 2+ triples (74%; esperado 2.8; últ. 10: 9/10)
- Jalen Brunson 2+ triples (76%; esperado 2.9; últ. 10: 8/10)
- Davion Mitchell 1+ triples (85%; esperado 2.3; últ. 10: 9/10)

**Milwaukee Bucks @ Detroit Pistons** — acertar las 4: **37%**, cuota justa 2.72

- Jaime Jaquez Jr. 2+ asistencias (77%; esperado 2.9; últ. 10: 9/10)
- Myles Turner 1+ asistencias (82%; esperado 2.1; últ. 10: 9/10)
- Tyler Herro 2+ triples (73%; esperado 2.8; últ. 10: 6/10)
- Kyle Kuzma 1+ triples (78%; esperado 1.8; últ. 10: 10/10)

**Atlanta Hawks @ Boston Celtics** — acertar las 4: **36%**, cuota justa 2.76

- Nickeil Alexander-Walker 2+ asistencias (74%; esperado 3.0; últ. 10: 8/10)
- Paul George 2+ triples (75%; esperado 3.0; últ. 10: 8/10)
- Jayson Tatum 2+ triples (78%; esperado 3.0; últ. 10: 9/10)
- Derrick White 1+ triples (83%; esperado 1.9; últ. 10: 9/10)

**New Orleans Pelicans @ LA Clippers** — acertar las 4: **36%**, cuota justa 2.76

- Saddiq Bey 2+ asistencias (76%; esperado 3.0; últ. 10: 9/10)
- Trey Murphy III 2+ asistencias (81%; esperado 3.5; últ. 10: 9/10)
- Jeremiah Fears 1+ triples (76%; esperado 1.6; últ. 10: 8/10)
- Brook Lopez 1+ triples (77%; esperado 1.5; últ. 10: 10/10)

**Denver Nuggets @ Utah Jazz** — acertar las 4: **33%**, cuota justa 3.00

- Christian Braun 1+ triples (74%; esperado 1.7; últ. 10: 8/10)
- Jamal Murray 2+ triples (75%; esperado 3.4; últ. 10: 7/10)
- Darryn Peterson 1+ triples (76%; esperado 1.8; últ. 10: 7/10)
- Ace Bailey 1+ triples (78%; esperado 1.6; últ. 10: 9/10)

**Los Angeles Lakers @ San Antonio Spurs** — acertar las 4: **32%**, cuota justa 3.11

- Austin Reaves 17+ puntos (74%; esperado 21.5; últ. 10: 9/10)
- Quentin Grimes 2+ asistencias (74%; esperado 3.3; últ. 10: 7/10)
- Victor Wembanyama 2+ asistencias (76%; esperado 2.9; últ. 10: 8/10)
- Devin Vassell 1+ triples (75%; esperado 1.9; últ. 10: 7/10)

## Combinada segura del día

**Opción A, líneas principales con cuota real:**

Se elige por **probabilidad**, no por valor: la más probable de cada partido entre jugadores constantes (titulares con minutos estables, sin cambio de rol, traspaso ni lesión, que la habrían pasado en 7+ de sus últimos 10 y en el 60 %+ de esta temporada) y con cuota real de la casa. Si tu casa no ofrece esa línea, usa la siguiente de la lista "Las más seguras con cuota".

| Partido | Selección | Prob. | Cuota | Últ. 10 | Temporada |
|---|---|---|---|---|---|
| Atlanta Hawks @ Boston Celtics | **Jayson Tatum: menos de 1.5 robos**<br>el rival concede +6% de robos por minuto a aleros/ala-pívots (defensa débil); ajuste aplicado +6% | **73%** | 1.42 | 9/10 | 14/16 |
| Golden State Warriors @ Portland Trail Blazers | **Sidy Cissoko: menos de 1.5 robos**<br>el rival concede +11% de robos por minuto a bases/escoltas (defensa débil); ajuste aplicado +11% | **71%** | 1.45 | 8/10 | 16/18 |
| Denver Nuggets @ Utah Jazz | **Cameron Johnson: más de 0.5 robos**<br>el rival concede +7% de robos por minuto a aleros/ala-pívots (defensa débil); ajuste aplicado +7% | **70%** | 1.44 | 9/10 | 11/13 |
| Miami Heat @ New York Knicks | **Josh Hart: menos de 0.5 tapones**<br>el rival concede +9% de tapones por minuto a bases/escoltas (defensa débil); ajuste aplicado +9% | **70%** | 1.41 | 8/10 | 11/15 |

| Selecciones | Probabilidad de acertar todas | Cuota |
|---|---|---|
| 2 | **52%** | 2.05 |
| 3 | **36%** | 2.97 |
| 4 | **25%** | 4.17 |

**Jayson Tatum: menos de 1.5 robos** (73%):

- La pasó en 14 de 16 esta temporada (falló con 2, 3)
- Con 31+ minutos (hoy se esperan 35): 9 de 11 en sus últimos 15
- Contra las ~10 mejores defensas en robos a aleros/ala-pívots: 13 de 19 (últimos 40 partidos)
- Contra defensas débiles como la de hoy y con 31+ minutos: 4 de 6, con 1.0 de media (últimos 60 partidos)
- El rival es #8 de 30 en robos que concede a aleros/ala-pívots por minuto (#1 = el que más concede; +6% frente a la media)
- Oportunidades de robo (últimos 10): el rival perdió 10.6 balones por partido con él en pista y robó el 8%
- El rival es #19 de 30 en balones que pierde (#1 = el que más; 13.7 por partido)
- Minutos: 35 esperados (titular, ±3)

**Sidy Cissoko: menos de 1.5 robos** (71%):

- La pasó en 16 de 18 esta temporada (falló con 2, 3)
- Con 23+ minutos (hoy se esperan 27): 6 de 8 en sus últimos 15
- Contra las ~10 mejores defensas en robos a bases/escoltas: 16 de 18 (últimos 40 partidos)
- Contra defensas débiles como la de hoy y con 23+ minutos: 4 de 6, con 0.8 de media (últimos 60 partidos)
- El rival es #4 de 30 en robos que concede a bases/escoltas por minuto (#1 = el que más concede; +11% frente a la media)
- Oportunidades de robo (últimos 10): el rival perdió 8.0 balones por partido con él en pista y robó el 12%
- El rival es #4 de 30 en balones que pierde (#1 = el que más; 15.2 por partido)
- Minutos: 27 esperados (titular, ±4)

**Cameron Johnson: más de 0.5 robos** (70%):

- La pasó en 11 de 13 esta temporada (falló con 0, 0)
- Con 27+ minutos (hoy se esperan 31): 10 de 11 en sus últimos 15
- Contra las ~10 mejores defensas en robos a aleros/ala-pívots: 6 de 14 (últimos 40 partidos)
- Contra defensas débiles como la de hoy y con 27+ minutos: 11 de 15, con 1.2 de media (últimos 60 partidos)
- El rival es #7 de 30 en robos que concede a aleros/ala-pívots por minuto (#1 = el que más concede; +7% frente a la media)
- Oportunidades de robo (últimos 10): el rival perdió 9.1 balones por partido con él en pista y robó el 13%
- El rival es #3 de 30 en balones que pierde (#1 = el que más; 15.3 por partido)
- Minutos: 31 esperados (titular, ±3)

**Josh Hart: menos de 0.5 tapones** (70%):

- La pasó en 11 de 15 esta temporada (falló con 1, 1, 1, 1)
- Con 29+ minutos (hoy se esperan 33): 5 de 9 en sus últimos 15
- Contra las ~10 mejores defensas en tapones a bases/escoltas: 6 de 7 (últimos 40 partidos)
- Contra defensas débiles como la de hoy y con 29+ minutos: 9 de 12, con 0.3 de media (últimos 60 partidos)
- El rival es #5 de 30 en tapones que concede a bases/escoltas por minuto (#1 = el que más concede; +9% frente a la media)
- Oportunidades de tapón (últimos 10): 29.9 tiros de 2 del rival por partido con él en pista; taponó el 0.7%
- El rival es #9 de 30 en tiros de 2 por partido (#1 = el que más; 53.2)
- El 50% de los tiros del rival son cerca del aro (penetración, corte, poste, palmeo): #6 de 30
- Minutos: 33 esperados (titular, ±5)

### Las más seguras con cuota

| Partido | Prop | Prob. final | Modelo | Casa | Esperado | Últ. 10 | Temporada | vs este rival | Cuota (implícita) |
|---|---|---|---|---|---|---|---|---|---|
| Atlanta Hawks @ Boston Celtics | **Jayson Tatum: menos de 1.5 robos** | **73%** | 77% | 66% | 1.0 ± 1.0 | 9/10 | 14/16 | 0 | 1.42 (71%) |
| Golden State Warriors @ Portland Trail Blazers | **Sidy Cissoko: menos de 1.5 robos** | **71%** | 76% | 63% | 1.0 ± 1.0 | 8/10 | 16/18 | 0, 1, 1 | 1.45 (69%) |
| Golden State Warriors @ Portland Trail Blazers | **Yaxel Lendeborg: más de 0.5 robos** | **71%** | 73% | 67% | 1.4 ± 1.2 | 7/10 | 12/18 | - | 1.42 (71%) |
| Denver Nuggets @ Utah Jazz | **Cameron Johnson: más de 0.5 robos** | **70%** | 73% | 66% | 1.2 ± 1.1 | 9/10 | 11/13 | 2, 1, 0 | 1.44 (69%) |
| Miami Heat @ New York Knicks | **Josh Hart: menos de 0.5 tapones** | **70%** | 72% | 66% | 0.3 ± 0.6 | 8/10 | 11/15 | 0, 1, 0, 0 | 1.41 (71%) |
| New Orleans Pelicans @ LA Clippers | **Trey Murphy III: más de 0.5 robos** | **68%** | 72% | 65% | 1.2 ± 1.1 | 9/10 | 9/11 | 1, 1, 3, 2, 2 | 1.47 (68%) |
| Brooklyn Nets @ Toronto Raptors | **Day'Ron Sharpe: más de 0.5 tapones** | **68%** | 72% | 63% | 1.5 ± 1.3 | 7/10 | 11/17 | 0, 0 | 1.50 (67%) |
| Atlanta Hawks @ Boston Celtics | **Dyson Daniels: menos de 0.5 tapones** | **68%** | 69% | 66% | 0.4 ± 0.8 | 7/10 | 12/17 | 0, 1, 1 | 1.41 (71%) |
| Brooklyn Nets @ Toronto Raptors | **Day'Ron Sharpe: más de 0.5 robos** | **68%** | 70% | 65% | 1.2 ± 1.1 | 8/10 | 12/17 | 0, 0 | 1.48 (68%) |
| Golden State Warriors @ Portland Trail Blazers | **Brandin Podziemski: más de 0.5 robos** | **67%** | 68% | 65% | 1.2 ± 1.1 | 7/10 | 11/16 | 2, 1, 3, 2 | 1.47 (68%) |
| Milwaukee Bucks @ Detroit Pistons | **Tyler Herro: más de 0.5 robos** | **67%** | 69% | 63% | 1.1 ± 1.1 | 8/10 | 14/18 | 1, 0 | 1.50 (67%) |
| Atlanta Hawks @ Boston Celtics | **Nickeil Alexander-Walker: menos de 0.5 tapones** | **67%** | 68% | 64% | 0.4 ± 0.6 | 7/10 | 12/17 | 0, 0, 0, 1 | 1.46 (69%) |

## Combinadas con cuota objetivo

La combinación de jugadores constantes (mismos filtros que la opción B, partidos distintos) con más probabilidad de acertar todas cuya cuota llega al objetivo. Se registran como picks de prueba y se liquidan solas: `nba rendimiento` dice cuándo el sistema está listo para dinero real. Una cuota alta nunca es segura: cuota 15 justa acierta 1 de cada 15. Lo que la data puede hacer es acercarse o superar esa probabilidad. Se eligen solo por probabilidad de acertar (nunca por valor): como mucho 5 patas, sin "menos" de anotación dudosos.

**Segura, cuota 2+ (2 patas):** cuota 2.05, probabilidad de acertar todas **52%** (1 de cada 2)

- Jayson Tatum: menos de 1.5 robos (73%, cuota 1.42) — Atlanta Hawks @ Boston Celtics — 4 factores a favor, 1 en contra
  - La pasó en 14 de 16 esta temporada (falló con 2, 3)
  - Con 31+ minutos (hoy se esperan 35): 9 de 11 en sus últimos 15
  - Contra las ~10 mejores defensas en robos a aleros/ala-pívots: 13 de 19 (últimos 40 partidos)
  - Contra defensas débiles como la de hoy y con 31+ minutos: 4 de 6, con 1.0 de media (últimos 60 partidos)
  - El rival es #8 de 30 en robos que concede a aleros/ala-pívots por minuto (#1 = el que más concede; +6% frente a la media)
  - Oportunidades de robo (últimos 10): el rival perdió 10.6 balones por partido con él en pista y robó el 8%
  - El rival es #19 de 30 en balones que pierde (#1 = el que más; 13.7 por partido)
  - Minutos: 35 esperados (titular, ±3)
- Sidy Cissoko: menos de 1.5 robos (71%, cuota 1.45) — Golden State Warriors @ Portland Trail Blazers — 3 factores a favor, 2 en contra
  - La pasó en 16 de 18 esta temporada (falló con 2, 3)
  - Con 23+ minutos (hoy se esperan 27): 6 de 8 en sus últimos 15
  - Contra las ~10 mejores defensas en robos a bases/escoltas: 16 de 18 (últimos 40 partidos)
  - Contra defensas débiles como la de hoy y con 23+ minutos: 4 de 6, con 0.8 de media (últimos 60 partidos)
  - El rival es #4 de 30 en robos que concede a bases/escoltas por minuto (#1 = el que más concede; +11% frente a la media)
  - Oportunidades de robo (últimos 10): el rival perdió 8.0 balones por partido con él en pista y robó el 12%
  - El rival es #4 de 30 en balones que pierde (#1 = el que más; 15.2 por partido)
  - Minutos: 27 esperados (titular, ±4)

**Segura, cuota 3+ (3 patas):** cuota 3.03, probabilidad de acertar todas **35%** (1 de cada 3)

- Jayson Tatum: menos de 1.5 robos (73%, cuota 1.42) — Atlanta Hawks @ Boston Celtics — 4 factores a favor, 1 en contra
  - La pasó en 14 de 16 esta temporada (falló con 2, 3)
  - Con 31+ minutos (hoy se esperan 35): 9 de 11 en sus últimos 15
  - Contra las ~10 mejores defensas en robos a aleros/ala-pívots: 13 de 19 (últimos 40 partidos)
  - Contra defensas débiles como la de hoy y con 31+ minutos: 4 de 6, con 1.0 de media (últimos 60 partidos)
  - El rival es #8 de 30 en robos que concede a aleros/ala-pívots por minuto (#1 = el que más concede; +6% frente a la media)
  - Oportunidades de robo (últimos 10): el rival perdió 10.6 balones por partido con él en pista y robó el 8%
  - El rival es #19 de 30 en balones que pierde (#1 = el que más; 13.7 por partido)
  - Minutos: 35 esperados (titular, ±3)
- Sidy Cissoko: menos de 1.5 robos (71%, cuota 1.45) — Golden State Warriors @ Portland Trail Blazers — 3 factores a favor, 2 en contra
  - La pasó en 16 de 18 esta temporada (falló con 2, 3)
  - Con 23+ minutos (hoy se esperan 27): 6 de 8 en sus últimos 15
  - Contra las ~10 mejores defensas en robos a bases/escoltas: 16 de 18 (últimos 40 partidos)
  - Contra defensas débiles como la de hoy y con 23+ minutos: 4 de 6, con 0.8 de media (últimos 60 partidos)
  - El rival es #4 de 30 en robos que concede a bases/escoltas por minuto (#1 = el que más concede; +11% frente a la media)
  - Oportunidades de robo (últimos 10): el rival perdió 8.0 balones por partido con él en pista y robó el 12%
  - El rival es #4 de 30 en balones que pierde (#1 = el que más; 15.2 por partido)
  - Minutos: 27 esperados (titular, ±4)
- Trey Murphy III: más de 0.5 robos (68%, cuota 1.47) — New Orleans Pelicans @ LA Clippers — 5 factores a favor, 1 en contra
  - La pasó en 9 de 11 esta temporada (falló con 0, 0)
  - Con 29+ minutos (hoy se esperan 33): 10 de 13 en sus últimos 15
  - Contra las ~10 mejores defensas en robos a aleros/ala-pívots: 14 de 17 (últimos 40 partidos)
  - Contra defensas fuertes como la de hoy y con 29+ minutos: 15 de 20, con 1.4 de media (últimos 60 partidos)
  - El rival es #25 de 30 en robos que concede a aleros/ala-pívots por minuto (#1 = el que más concede; -6% frente a la media)
  - Oportunidades de robo (últimos 10): el rival perdió 10.1 balones por partido con él en pista y robó el 13%
  - El rival es #13 de 30 en balones que pierde (#1 = el que más; 14.3 por partido)
  - Minutos: 33 esperados (titular, ±3)

**Segura, cuota 5+ (4 patas):** cuota 5.36, probabilidad de acertar todas **23%** (1 de cada 4)

- Jayson Tatum: menos de 1.5 robos (73%, cuota 1.42) — Atlanta Hawks @ Boston Celtics — 4 factores a favor, 1 en contra
  - La pasó en 14 de 16 esta temporada (falló con 2, 3)
  - Con 31+ minutos (hoy se esperan 35): 9 de 11 en sus últimos 15
  - Contra las ~10 mejores defensas en robos a aleros/ala-pívots: 13 de 19 (últimos 40 partidos)
  - Contra defensas débiles como la de hoy y con 31+ minutos: 4 de 6, con 1.0 de media (últimos 60 partidos)
  - El rival es #8 de 30 en robos que concede a aleros/ala-pívots por minuto (#1 = el que más concede; +6% frente a la media)
  - Oportunidades de robo (últimos 10): el rival perdió 10.6 balones por partido con él en pista y robó el 8%
  - El rival es #19 de 30 en balones que pierde (#1 = el que más; 13.7 por partido)
  - Minutos: 35 esperados (titular, ±3)
- Sidy Cissoko: menos de 1.5 robos (71%, cuota 1.45) — Golden State Warriors @ Portland Trail Blazers — 3 factores a favor, 2 en contra
  - La pasó en 16 de 18 esta temporada (falló con 2, 3)
  - Con 23+ minutos (hoy se esperan 27): 6 de 8 en sus últimos 15
  - Contra las ~10 mejores defensas en robos a bases/escoltas: 16 de 18 (últimos 40 partidos)
  - Contra defensas débiles como la de hoy y con 23+ minutos: 4 de 6, con 0.8 de media (últimos 60 partidos)
  - El rival es #4 de 30 en robos que concede a bases/escoltas por minuto (#1 = el que más concede; +11% frente a la media)
  - Oportunidades de robo (últimos 10): el rival perdió 8.0 balones por partido con él en pista y robó el 12%
  - El rival es #4 de 30 en balones que pierde (#1 = el que más; 15.2 por partido)
  - Minutos: 27 esperados (titular, ±4)
- Cameron Johnson: más de 0.5 robos (70%, cuota 1.44) — Denver Nuggets @ Utah Jazz — 5 factores a favor, 0 en contra
  - La pasó en 11 de 13 esta temporada (falló con 0, 0)
  - Con 27+ minutos (hoy se esperan 31): 10 de 11 en sus últimos 15
  - Contra las ~10 mejores defensas en robos a aleros/ala-pívots: 6 de 14 (últimos 40 partidos)
  - Contra defensas débiles como la de hoy y con 27+ minutos: 11 de 15, con 1.2 de media (últimos 60 partidos)
  - El rival es #7 de 30 en robos que concede a aleros/ala-pívots por minuto (#1 = el que más concede; +7% frente a la media)
  - Oportunidades de robo (últimos 10): el rival perdió 9.1 balones por partido con él en pista y robó el 13%
  - El rival es #3 de 30 en balones que pierde (#1 = el que más; 15.3 por partido)
  - Minutos: 31 esperados (titular, ±3)
- Austin Reaves: más de 16.5 puntos (64%, cuota 1.81) — Los Angeles Lakers @ San Antonio Spurs — 4 factores a favor, 2 en contra
  - La pasó en 11 de 12 esta temporada (falló con 16)
  - Con 30+ minutos (hoy se esperan 34): 13 de 14 en sus últimos 15
  - Contra las ~10 mejores defensas en puntos a bases/escoltas: 9 de 16 (últimos 40 partidos)
  - Contra defensas fuertes como la de hoy y con 30+ minutos: 10 de 18, con 22.1 de media (últimos 60 partidos)
  - El rival es #26 de 30 en puntos que concede a bases/escoltas por minuto (#1 = el que más concede; -4% frente a la media)
  - Su zona principal es triple frontal (35% de sus tiros, 36% de acierto); el rival es #10 de 30 en acierto que deja ahí (36%, liga 35%)
  - Su segunda zona es pintura (34% de sus tiros, 53% de acierto); el rival es #28 de 30 en acierto que deja ahí (42%, liga 45%)
  - El rival es #28 de 30 en tiros libres que concede a bases/escoltas (#1 = el que más; -12% frente a la media)
  - Puntería: en sus últimos 10 metió el 111% de las canastas esperadas por sus tipos de tiro
  - Cómo tira (últimos 15): creado 41% (48% de acierto), penetración 35% (56% de acierto), recibe y tira 18% (43% de acierto); en creado el rival es #21 de 30 en lo que deja (#1 = el que más; 0.91 puntos por tiro frente a 0.93 de media)
  - Oportunidades: 15.1 tiros de campo y 5.3 libres esperados (1.08 puntos por tiro)
  - Transición: el rival concede 12.4 puntos por partido al contraataque (#26 de 30, #1 = el que más); él anota 2.1 así por partido (ajuste aplicado -1.2%)
  - El rival no tiene a Dylan Harper (19.0 puntos por partido)
  - Minutos: 34 esperados (titular, ±5)

## Picks seguros de titulares estables

Líneas bajas (alternativas) de titulares con 30+ minutos: mejor un "15+ puntos" casi seguro de una estrella que la línea normal de un suplente. En el backtest, elegidas al 85 % acertaron el 89-96 %. **Cuota mínima** = la que hace falta para que valga la pena (1 / probabilidad); búscala en las líneas alternativas de tu casa.

| Partido | Jugador | Pick seguro | Prob. | Cuota mínima | Esperado | Últ. 10 |
|---|---|---|---|---|---|---|
| Los Angeles Lakers @ San Antonio Spurs | Austin Reaves | **más de 21.5 pts+reb+ast** | **82%** | 1.22 | 29.4 | 10/10 |
| Los Angeles Lakers @ San Antonio Spurs | Austin Reaves | **más de 15.5 puntos** | **79%** | 1.26 | 21.5 | 10/10 |

## Las más probables del día

| Partido | Prop | Prob. final | Modelo | Casa | Esperado | Últ. 10 | Temporada | vs este rival | Cuota (implícita) |
|---|---|---|---|---|---|---|---|---|---|
| Milwaukee Bucks @ Detroit Pistons | **Nate Ament: menos de 1.5 asistencias** ⚠️ suplente | **80%** | 81% | 77% | 0.7 ± 0.9 | 10/10 | 16/17 | - | 1.25 (80%) |
| Atlanta Hawks @ Boston Celtics | **Neemias Queta: menos de 0.5 triples** | **79%** | 73% | 87% | 0.3 ± 0.5 | 7/10 | 12/17 | 0, 0 | 1.08 (93%) |
| Atlanta Hawks @ Boston Celtics | **Jayson Tatum: menos de 1.5 robos** | **73%** | 77% | 66% | 1.0 ± 1.0 | 9/10 | 14/16 | 0 | 1.42 (71%) |
| Golden State Warriors @ Portland Trail Blazers | **Scoot Henderson: menos de 3.5 asistencias** ⚠️ suplente | **72%** | 81% | 58% | 2.1 ± 1.5 | 9/10 | 17/18 | - | 1.61 (62%) |
| Golden State Warriors @ Portland Trail Blazers | **Sidy Cissoko: menos de 1.5 robos** | **71%** | 76% | 63% | 1.0 ± 1.0 | 8/10 | 16/18 | 0, 1, 1 | 1.45 (69%) |
| Golden State Warriors @ Portland Trail Blazers | **Yaxel Lendeborg: más de 0.5 robos** | **71%** | 73% | 67% | 1.4 ± 1.2 | 7/10 | 12/18 | - | 1.42 (71%) |
| Memphis Grizzlies @ Minnesota Timberwolves | **Taylor Hendricks: menos de 1.5 triples** ⚠️ suplente | **71%** | 73% | 67% | 1.0 ± 1.1 | 9/10 | 12/14 | 0, 1, 0 | 1.48 (68%) |
| Milwaukee Bucks @ Detroit Pistons | **Kel'el Ware: menos de 1.5 asistencias** ⚠️ suplente | **70%** | 69% | 72% | 1.1 ± 1.0 | 7/10 | 15/19 | 0, 0, 0 | 1.32 (76%) |
| Dallas Mavericks @ Phoenix Suns | **Naji Marshall: más de 0.5 robos** ⚠️ suplente | **70%** | 72% | 68% | 1.2 ± 1.1 | 10/10 | 14/15 | 1, 1 | 1.41 (71%) |
| Denver Nuggets @ Utah Jazz | **DeMar DeRozan: menos de 0.5 triples** ⚠️ suplente | **70%** | 70% | 70% | 0.4 ± 0.6 | 9/10 | 13/15 | 1, 1, 1, 0 | 1.32 (75%) |
| Memphis Grizzlies @ Minnesota Timberwolves | **Kris Murray: menos de 5.5 reb+ast** ⚠️ suplente | **70%** | 79% | 57% | 3.5 ± 3.1 | 9/10 | 14/15 | 0, 2, 6, 0 | 1.65 (61%) |
| Denver Nuggets @ Utah Jazz | **Cameron Johnson: más de 0.5 robos** | **70%** | 73% | 66% | 1.2 ± 1.1 | 9/10 | 11/13 | 2, 1, 0 | 1.44 (69%) |
| Miami Heat @ New York Knicks | **Josh Hart: menos de 0.5 tapones** | **70%** | 72% | 66% | 0.3 ± 0.6 | 8/10 | 11/15 | 0, 1, 0, 0 | 1.41 (71%) |
| Miami Heat @ New York Knicks | **Bam Adebayo: menos de 1.5 triples** | **69%** | 72% | 65% | 1.0 ± 1.2 | 8/10 | 14/17 | 0, 1 | 1.45 (69%) |
| Philadelphia 76ers @ Indiana Pacers | **Kelly Oubre Jr.: más de 0.5 asistencias** | **69%** | 71% | 64% | 1.4 ± 1.2 | 5/10 | 11/16 | 2, 1 | 1.44 (69%) |
| Memphis Grizzlies @ Minnesota Timberwolves | **Zach Edey: menos de 1.5 asistencias** | **69%** | 71% | 65% | 1.1 ± 1.1 | 9/10 | 12/15 | 0 | 1.43 (70%) |
| Miami Heat @ New York Knicks | **Giannis Antetokounmpo: más de 0.5 tapones** | **69%** | 71% | 65% | 1.2 ± 1.1 | 8/10 | 12/16 | 0, 2 | 1.43 (70%) |
| New Orleans Pelicans @ LA Clippers | **Trey Murphy III: más de 0.5 robos** | **68%** | 72% | 65% | 1.2 ± 1.1 | 9/10 | 9/11 | 1, 1, 3, 2, 2 | 1.47 (68%) |
| Philadelphia 76ers @ Indiana Pacers | **Tyrese Maxey: menos de 1.5 robos** | **68%** | 70% | 65% | 1.1 ± 1.1 | 9/10 | 12/18 | 1, 1, 2, 2, 8 | 1.42 (71%) |
| Brooklyn Nets @ Toronto Raptors | **Day'Ron Sharpe: más de 0.5 tapones** | **68%** | 72% | 63% | 1.5 ± 1.3 | 7/10 | 11/17 | 0, 0 | 1.50 (67%) |
| New Orleans Pelicans @ LA Clippers | **Derik Queen: menos de 0.5 triples** ⚠️ suplente | **68%** | 68% | 69% | 0.5 ± 1.0 | 7/10 | 13/19 | 0, 1, 1, 0, 0 | 1.37 (73%) |
| Atlanta Hawks @ Boston Celtics | **Dyson Daniels: menos de 0.5 tapones** | **68%** | 69% | 66% | 0.4 ± 0.8 | 7/10 | 12/17 | 0, 1, 1 | 1.41 (71%) |
| Miami Heat @ New York Knicks | **Bobby Portis: más de 0.5 triples** ⚠️ suplente | **68%** | 71% | 63% | 1.3 ± 1.2 | 8/10 | 14/17 | 2, 1, 1 | 1.50 (67%) |
| New Orleans Pelicans @ LA Clippers | **Derrick Jones Jr.: más de 0.5 triples** | **68%** | 70% | 64% | 1.3 ± 1.2 | 6/10 | 12/16 | 0, 1, 0, 3, 2 | 1.46 (68%) |
| Brooklyn Nets @ Toronto Raptors | **Noah Clowney: más de 0.5 asistencias** ⚠️ suplente | **68%** | 72% | 62% | 1.4 ± 1.2 | 7/10 | 12/17 | 2, 1, 3 | 1.53 (66%) |
| Brooklyn Nets @ Toronto Raptors | **Day'Ron Sharpe: más de 0.5 robos** | **68%** | 70% | 65% | 1.2 ± 1.1 | 8/10 | 12/17 | 0, 0 | 1.48 (68%) |
| Miami Heat @ New York Knicks | **Andrew Wiggins: más de 0.5 triples** ⚠️ suplente | **68%** | 71% | 63% | 1.4 ± 1.2 | 7/10 | 12/17 | 2, 0, 1, 1 | 1.48 (67%) |
| New Orleans Pelicans @ LA Clippers | **Herbert Jones: menos de 1.5 robos** | **67%** | 68% | 65% | 1.2 ± 1.3 | 6/10 | 13/19 | 0, 2, 5, 0, 1 | 1.44 (69%) |
| Los Angeles Lakers @ San Antonio Spurs | **Jake LaRavia: más de 0.5 robos** | **67%** | 69% | 63% | 1.2 ± 1.1 | 6/10 | 13/17 | 0, 1, 1, 0 | 1.50 (67%) |
| Los Angeles Lakers @ San Antonio Spurs | **De'Aaron Fox: menos de 1.5 triples** | **67%** | 69% | 64% | 1.0 ± 1.1 | 8/10 | 11/16 | 0, 0, 4 | 1.48 (68%) |

**Si haces combinada:** cada selección que añades multiplica el riesgo. Probabilidad de acertar todas con las más probables de partidos distintos:

- 2 selecciones: **63%**
- 3 selecciones: **45%**
- 4 selecciones: **32%**
- 5 selecciones: **22%**
- 6 selecciones: **16%**

Dentro de un mismo partido (bet builder) las selecciones no son independientes y el cálculo es aún menos fiable. Con 12 selecciones al 65 % la probabilidad de acertar todas es menor del 1 %.

### En qué se basan las 10 más probables

#### Nate Ament: menos de 1.5 asistencias (80%) — Milwaukee Bucks @ Detroit Pistons

**¿Por qué 0.7 asistencias?** (línea 1.5; 22.0 minutos esperados)

En corto:

- La pasó en 16 de 17 esta temporada; los fallos, en partidos raros (paliza de 25)
- Con 18+ minutos (hoy se esperan 22): 8 de 9 en sus últimos 15
- Contra las ~10 mejores defensas en asistencias a aleros/ala-pívots: 10 de 10 (últimos 40 partidos)
- Contra defensas fuertes como la de hoy y con 18+ minutos: 7 de 7, con 0.7 de media (últimos 60 partidos)
- El rival es #27 de 30 en asistencias que concede a aleros/ala-pívots por minuto (#1 = el que más concede; -6% frente a la media)
- Asistencias esperadas: 0.7 por partido si sus compañeros metieran lo normal (tiene 0.7; con él en pista metieron el 95% de lo esperado por tipo de tiro, últimos 10); ajuste aplicado +3.2%
- Oportunidades: asiste el 5% de las canastas de sus compañeros con él en pista
- El rival no tiene a Cade Cunningham (8.6 asistencias por partido)
- Minutos: 22 esperados (suplente, ±6)

Razonamiento (3 factores a favor, 2 en contra):

- ❌ Minutos: 22.0 esperados (suplente, ±5.9).
- ✅ Forma: 0.4 en sus últimos 5, 0.5 esta temporada (17 partidos) (línea 1.5).
- ➖ Cómo produce asistencias: asiste el 5.3% de las canastas de sus compañeros en pista × 13.5 canastas de compañeros esperadas (su equipo 36.3 por 48' contra esta defensa).
- ✅ Defensa: el rival concede -6% de asistencias por minuto a aleros/ala-pívots (defensa fuerte); ajuste aplicado -6%.
- ➖ Ritmo del partido: -1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Últimos 10: la habría pasado 10 de 10.
- ❌ Bajas del rival: sin Cade Cunningham (titular); +1.5% en esta estadística.
- ⚠️ partido desigual (no favorito por 9.5): los suplentes suelen jugar +1% de minutos si se rompe.

- ⚠️ Alertas: suplente.
- Asistencias **0.7** (por componentes 0.7 · por tasa por minuto y defensa rival 0.7): asiste el 5.3% de las canastas de sus compañeros en pista × 13.5 canastas de compañeros esperadas (su equipo 36.3 por 48' contra esta defensa).

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 22.4 | 21.8 | 19.0 | - | - |
| Asistencias | 0.4 | 0.7 | 0.5 | - | - |
| % de las canastas de compañeros que asiste | 2.3% | 4.5% | 3.8% | - | - |
| Pérdidas por jugada | 12.6% | 11.6% | 11.7% | - | - |

#### Neemias Queta: menos de 0.5 triples (79%) — Atlanta Hawks @ Boston Celtics

**¿Por qué 0.3 triples?** (línea 0.5; 25.8 minutos esperados)

En corto:

- La pasó en 12 de 17 esta temporada (falló con 1, 1, 1, 1)
- Con 22+ minutos (hoy se esperan 26): 7 de 10 en sus últimos 15
- Contra las ~10 mejores defensas en triples a pívots: 9 de 12 (últimos 40 partidos)
- Contra defensas fuertes como la de hoy y con 22+ minutos: 16 de 18, con 0.1 de media (últimos 60 partidos)
- El rival es #27 de 30 en triples que concede a pívots por minuto (#1 = el que más concede; -10% frente a la media)
- Su zona principal es triple de esquina (2% de sus tiros, 46% de acierto); el rival es #25 de 30 en acierto que deja ahí (37%, liga 38%)
- Cómo tira (últimos 15): corte 33% (71% de acierto), penetración 25% (52% de acierto), palmeo 20% (75% de acierto); en corte el rival es #16 de 30 en lo que deja (#1 = el que más; 1.52 puntos por tiro frente a 1.52 de media)
- Oportunidades: 0.6 triples intentados esperados al 38%
- Minutos: 26 esperados (titular, ±5)

Razonamiento (5 factores a favor, 0 en contra):

- ✅ Minutos: 25.8 esperados (titular, ±5.0).
- ✅ Forma: 0.4 en sus últimos 5, 0.3 esta temporada (17 partidos), 0.0 la temporada pasada (línea 0.5).
- ➖ Cómo produce triples: 0.6 triples intentados (su ritmo 0.8 por 36'; el rival concede -3% de triples en su reparto) × 38% esperado.
- ✅ Defensa: el rival concede -10% de triples por minuto a pívots (defensa fuerte); ajuste aplicado -6%; en su zona principal (esquina3) el rival concede 37% (liga 38%).
- ➖ Ritmo del partido: +1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 0, 0 (2 de 2 a favor).
- ✅ Últimos 10: la habría pasado 7 de 10.

- Triples **0.3** (por componentes 0.2 · por tasa por minuto y defensa rival 0.3): 0.6 triples intentados (su ritmo 0.8 por 36'; el rival concede -3% de triples en su reparto) × 38% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 25.4 | 24.6 | 23.4 | 25.0 | 26.0 |
| Triples anotados | 0.4 | 0.3 | 0.3 | 0.0 | 0.0 |
| Triples intentados | 0.6 | 0.4 | 0.4 | 0.1 | 0.0 |
| % triples | 66.7% | 75.0% | 71.4% | 12.5% | - |

#### Jayson Tatum: menos de 1.5 robos (73%) — Atlanta Hawks @ Boston Celtics

**¿Por qué 1.0 robos?** (línea 1.5; 35.4 minutos esperados)

En corto:

- La pasó en 14 de 16 esta temporada (falló con 2, 3)
- Con 31+ minutos (hoy se esperan 35): 9 de 11 en sus últimos 15
- Contra las ~10 mejores defensas en robos a aleros/ala-pívots: 13 de 19 (últimos 40 partidos)
- Contra defensas débiles como la de hoy y con 31+ minutos: 4 de 6, con 1.0 de media (últimos 60 partidos)
- El rival es #8 de 30 en robos que concede a aleros/ala-pívots por minuto (#1 = el que más concede; +6% frente a la media)
- Oportunidades de robo (últimos 10): el rival perdió 10.6 balones por partido con él en pista y robó el 8%
- El rival es #19 de 30 en balones que pierde (#1 = el que más; 13.7 por partido)
- Minutos: 35 esperados (titular, ±3)

Razonamiento (4 factores a favor, 1 en contra):

- ✅ Minutos: 35.4 esperados (titular, ±3.1).
- ✅ Forma: 1.0 en sus últimos 5, 0.8 esta temporada (16 partidos), 1.3 la temporada pasada (línea 1.5).
- ➖ Cómo produce robos: roba el 9.0% de las pérdidas del rival en pista × 12.7 pérdidas esperadas del rival.
- ❌ Defensa: el rival concede +6% de robos por minuto a aleros/ala-pívots (defensa débil); ajuste aplicado +6%.
- ➖ Ritmo del partido: +1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 0 (1 de 1 a favor).
- ✅ Últimos 10: la habría pasado 9 de 10.

- Robos **1.0** (por componentes 0.8 · por tasa por minuto y defensa rival 1.0): roba el 9.0% de las pérdidas del rival en pista × 12.7 pérdidas esperadas del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 35.6 | 33.8 | 34.5 | 33.6 | 37.0 |
| Robos | 1.0 | 0.8 | 0.8 | 1.3 | 0.0 |
| % de las pérdidas del rival que roba | 8.9% | 7.5% | 6.6% | 19.3% | 0.0% |

#### Scoot Henderson: menos de 3.5 asistencias (72%) — Golden State Warriors @ Portland Trail Blazers

**¿Por qué 2.1 asistencias?** (línea 3.5; 24.6 minutos esperados)

En corto:

- La pasó en 17 de 18 esta temporada; los fallos, en partidos raros (paliza de 20)
- Con 21+ minutos (hoy se esperan 25): 12 de 13 en sus últimos 15
- Contra las ~10 mejores defensas en asistencias a bases/escoltas: 16 de 17 (últimos 40 partidos)
- Contra defensas medias como la de hoy y con 21+ minutos: 10 de 14, con 3.6 de media (últimos 60 partidos)
- El rival es #15 de 30 en asistencias que concede a bases/escoltas por minuto (#1 = el que más concede; +2% frente a la media)
- Asistencias esperadas: 1.7 por partido si sus compañeros metieran lo normal (tiene 1.7; con él en pista metieron el 102% de lo esperado por tipo de tiro, últimos 10); ajuste aplicado -0.6%
- Oportunidades: asiste el 11% de las canastas de sus compañeros con él en pista
- Su equipo no tiene a Damian Lillard: más tiros y balón para él
- Minutos: 25 esperados (suplente, ±4)

Razonamiento (2 factores a favor, 1 en contra):

- ❌ Minutos: 24.6 esperados (suplente, ±4.1).
- ✅ Forma: 1.8 en sus últimos 5, 1.5 esta temporada (18 partidos), 3.3 la temporada pasada (línea 3.5).
- ➖ Cómo produce asistencias: asiste el 11.4% de las canastas de sus compañeros en pista × 16.4 canastas de compañeros esperadas (su equipo 40.5 por 48' contra esta defensa).
- ➖ Defensa: el rival concede +2% de asistencias por minuto a bases/escoltas (defensa media); ajuste aplicado +2%.
- ➖ Ritmo del partido: -0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Últimos 10: la habría pasado 9 de 10.
- ⚠️ Ja Morant ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ sin Damian Lillard, la estrella de su equipo (0 partidos suyos sin él): más tiros y balón para él por minuto (puntos +7%, triples +4%, asistencias +6%).

- ⚠️ Alertas: suplente, sin Damian Lillard: más tiros para él.
- Asistencias **2.1** (por componentes 2.0 · por tasa por minuto y defensa rival 2.2): asiste el 11.4% de las canastas de sus compañeros en pista × 16.4 canastas de compañeros esperadas (su equipo 40.5 por 48' contra esta defensa).

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 25.6 | 24.0 | 23.2 | 25.2 | - |
| Asistencias | 1.8 | 1.7 | 1.5 | 3.3 | - |
| % de las canastas de compañeros que asiste | 9.6% | 9.8% | 8.6% | 18.0% | - |
| Pérdidas por jugada | 12.8% | 10.6% | 16.0% | 15.6% | - |

#### Sidy Cissoko: menos de 1.5 robos (71%) — Golden State Warriors @ Portland Trail Blazers

**¿Por qué 1.0 robos?** (línea 1.5; 27.5 minutos esperados)

En corto:

- La pasó en 16 de 18 esta temporada (falló con 2, 3)
- Con 23+ minutos (hoy se esperan 27): 6 de 8 en sus últimos 15
- Contra las ~10 mejores defensas en robos a bases/escoltas: 16 de 18 (últimos 40 partidos)
- Contra defensas débiles como la de hoy y con 23+ minutos: 4 de 6, con 0.8 de media (últimos 60 partidos)
- El rival es #4 de 30 en robos que concede a bases/escoltas por minuto (#1 = el que más concede; +11% frente a la media)
- Oportunidades de robo (últimos 10): el rival perdió 8.0 balones por partido con él en pista y robó el 12%
- El rival es #4 de 30 en balones que pierde (#1 = el que más; 15.2 por partido)
- Minutos: 27 esperados (titular, ±4)

Razonamiento (3 factores a favor, 2 en contra):

- ✅ Minutos: 27.5 esperados (titular, ±3.9).
- ❌ Forma: 1.6 en sus últimos 5, 0.7 esta temporada (18 partidos), 0.8 la temporada pasada (línea 1.5).
- ➖ Cómo produce robos: roba el 11.5% de las pérdidas del rival en pista × 15.8 pérdidas esperadas del rival.
- ❌ Defensa: el rival concede +11% de robos por minuto a bases/escoltas (defensa débil); ajuste aplicado +11%.
- ➖ Ritmo del partido: -0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 0, 1, 1 (3 de 3 a favor).
- ✅ Últimos 10: la habría pasado 8 de 10.
- ⚠️ Ja Morant ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ sin Damian Lillard, la estrella de su equipo (0 partidos suyos sin él): más tiros y balón para él por minuto (puntos +7%, triples +4%, asistencias +6%).

- Robos **1.0** (por componentes 1.0 · por tasa por minuto y defensa rival 1.0): roba el 11.5% de las pérdidas del rival en pista × 15.8 pérdidas esperadas del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 28.0 | 27.2 | 24.8 | 18.5 | 25.7 |
| Robos | 1.6 | 1.0 | 0.7 | 0.7 | 0.7 |
| % de las pérdidas del rival que roba | 17.4% | 12.5% | 10.4% | 11.3% | 8.7% |

#### Yaxel Lendeborg: más de 0.5 robos (71%) — Golden State Warriors @ Portland Trail Blazers

**¿Por qué 1.4 robos?** (línea 0.5; 31.7 minutos esperados)

En corto:

- La pasó en 12 de 18 esta temporada (falló con 0, 0, 0, 0)
- Con 28+ minutos (hoy se esperan 32): 9 de 12 en sus últimos 15
- Contra las ~10 mejores defensas en robos a aleros/ala-pívots: 2 de 5 (últimos 40 partidos)
- Contra defensas débiles como la de hoy y con 28+ minutos: 4 de 4, con 1.8 de media (últimos 60 partidos)
- El rival es #1 de 30 en robos que concede a aleros/ala-pívots por minuto (#1 = el que más concede; +21% frente a la media)
- Oportunidades de robo (últimos 10): el rival perdió 8.6 balones por partido con él en pista y robó el 15%
- El rival es #1 de 30 en balones que pierde (#1 = el que más; 15.8 por partido)
- El rival no tiene a Damian Lillard (0.6 robos por partido)
- Minutos: 32 esperados (titular, ±3)

Razonamiento (4 factores a favor, 0 en contra):

- ✅ Minutos: 31.7 esperados (titular, ±3.1).
- ✅ Forma: 1.4 en sus últimos 5, 1.1 esta temporada (18 partidos) (línea 0.5).
- ➖ Cómo produce robos: roba el 11.8% de las pérdidas del rival en pista × 17.4 pérdidas esperadas del rival.
- ✅ Defensa: el rival concede +21% de robos por minuto a aleros/ala-pívots (defensa débil); ajuste aplicado +21%.
- ➖ Ritmo del partido: -0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Últimos 10: la habría pasado 7 de 10.
- ⚠️ Kristaps Porzingis ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ Stephen Curry ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ Moses Moody ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ sin Jimmy Butler III, la estrella de su equipo (0 partidos suyos sin él): más tiros y balón para él por minuto (puntos +7%, triples +4%, asistencias +6%).
- ⚠️ Jimmy Butler III ya no jugó en sus últimos partidos: la baja ya está en sus minutos.

- Robos **1.4** (por componentes 1.4 · por tasa por minuto y defensa rival 1.4): roba el 11.8% de las pérdidas del rival en pista × 17.4 pérdidas esperadas del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 32.2 | 31.5 | 31.7 | - | - |
| Robos | 1.4 | 1.3 | 1.1 | - | - |
| % de las pérdidas del rival que roba | 14.3% | 15.1% | 11.5% | - | - |

#### Taylor Hendricks: menos de 1.5 triples (71%) — Memphis Grizzlies @ Minnesota Timberwolves

**¿Por qué 1.0 triples?** (línea 1.5; 22.9 minutos esperados)

En corto:

- La pasó en 12 de 14 esta temporada; los fallos, en partidos raros (paliza de 31, jugó 4 min)
- Con 19+ minutos (hoy se esperan 23): 7 de 9 en sus últimos 15
- Contra las ~10 mejores defensas en triples a aleros/ala-pívots: 13 de 15 (últimos 40 partidos)
- Contra defensas fuertes como la de hoy y con 19+ minutos: 11 de 13, con 0.9 de media (últimos 60 partidos)
- El rival es #27 de 30 en triples que concede a aleros/ala-pívots por minuto (#1 = el que más concede; -9% frente a la media)
- Su zona principal es triple frontal (28% de sus tiros, 33% de acierto); el rival es #27 de 30 en acierto que deja ahí (34%, liga 35%)
- Cómo tira (últimos 15): recibe y tira 38% (43% de acierto), penetración 37% (66% de acierto), corte 9% (71% de acierto); en recibe y tira el rival es #24 de 30 en lo que deja (#1 = el que más; 1.03 puntos por tiro frente a 1.07 de media)
- Oportunidades: 2.9 triples intentados esperados al 35%
- El rival no tiene a LaMelo Ball (3.3 triples por partido)
- Su equipo no tiene a Cameron Boozer: más tiros y balón para él
- Minutos: 23 esperados (suplente, ±4)

Razonamiento (4 factores a favor, 2 en contra):

- ❌ Minutos: 22.9 esperados (suplente, ±4.0).
- ✅ Forma: 0.4 en sus últimos 5, 0.7 esta temporada (14 partidos), 1.1 la temporada pasada (línea 1.5).
- ➖ Cómo produce triples: 2.9 triples intentados (su ritmo 4.9 por 36'; el rival concede -8% de triples en su reparto) × 35% esperado.
- ✅ Defensa: el rival concede -9% de triples por minuto a aleros/ala-pívots (defensa fuerte); ajuste aplicado -6%; en su zona principal (triple) el rival concede 34% (liga 35%).
- ➖ Ritmo del partido: +1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 0, 1, 0 (3 de 3 a favor).
- ✅ Últimos 10: la habría pasado 9 de 10.
- ❌ Bajas del rival: sin LaMelo Ball (titular); +1.7% en esta estadística.
- ⚠️ Jerami Grant ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ sin Cameron Boozer, la estrella de su equipo (3 partidos suyos sin él): más tiros y balón para él por minuto (puntos +4%, triples +0%, asistencias +4%).
- ⚠️ Cameron Boozer ya no jugó en sus últimos partidos: la baja ya está en sus minutos.

- ⚠️ Alertas: suplente, sin Cameron Boozer: más tiros para él.
- Triples **1.0** (por componentes 1.0 · por tasa por minuto y defensa rival 0.9): 2.9 triples intentados (su ritmo 4.9 por 36'; el rival concede -8% de triples en su reparto) × 35% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 23.4 | 21.1 | 16.4 | 19.0 | 22.7 |
| Triples anotados | 0.4 | 0.7 | 0.7 | 1.1 | 0.3 |
| Triples intentados | 2.2 | 2.1 | 1.9 | 3.1 | 3.3 |
| % triples | 18.2% | 33.3% | 37.0% | 34.2% | 10.0% |

#### Kel'el Ware: menos de 1.5 asistencias (70%) — Milwaukee Bucks @ Detroit Pistons

**¿Por qué 1.1 asistencias?** (línea 1.5; 21.7 minutos esperados)

En corto:

- La pasó en 15 de 19 esta temporada (falló con 2, 3, 2, 3)
- Con 18+ minutos (hoy se esperan 22): 3 de 7 en sus últimos 15
- Contra las ~10 mejores defensas en asistencias a pívots: 14 de 18 (últimos 40 partidos)
- Contra defensas fuertes como la de hoy y con 18+ minutos: 7 de 10, con 1.4 de media (últimos 60 partidos)
- El rival es #29 de 30 en asistencias que concede a pívots por minuto (#1 = el que más concede; -12% frente a la media)
- Asistencias esperadas: 1.3 por partido si sus compañeros metieran lo normal (tiene 1.2; con él en pista metieron el 90% de lo esperado por tipo de tiro, últimos 10); ajuste aplicado +5.9%
- Oportunidades: asiste el 7% de las canastas de sus compañeros con él en pista
- El rival no tiene a Cade Cunningham (8.6 asistencias por partido)
- Minutos: 22 esperados (suplente, ±4)

Razonamiento (4 factores a favor, 2 en contra):

- ❌ Minutos: 21.7 esperados (suplente, ±3.5).
- ✅ Forma: 1.2 en sus últimos 5, 0.9 esta temporada (19 partidos), 0.8 la temporada pasada (línea 1.5).
- ➖ Cómo produce asistencias: asiste el 7.3% de las canastas de sus compañeros en pista × 12.5 canastas de compañeros esperadas (su equipo 36.3 por 48' contra esta defensa).
- ✅ Defensa: el rival concede -12% de asistencias por minuto a pívots (defensa fuerte); ajuste aplicado -12%.
- ➖ Ritmo del partido: -1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 0, 0, 0 (3 de 3 a favor).
- ✅ Últimos 10: la habría pasado 7 de 10.
- ❌ Bajas del rival: sin Cade Cunningham (titular); +1.5% en esta estadística.
- ⚠️ partido desigual (no favorito por 9.5): los suplentes suelen jugar +1% de minutos si se rompe.

- ⚠️ Alertas: suplente.
- Asistencias **1.1** (por componentes 0.9 · por tasa por minuto y defensa rival 1.0): asiste el 7.3% de las canastas de sus compañeros en pista × 12.5 canastas de compañeros esperadas (su equipo 36.3 por 48' contra esta defensa).

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 22.0 | 20.1 | 19.2 | 22.4 | 25.0 |
| Asistencias | 1.2 | 1.2 | 0.9 | 0.8 | 0.0 |
| % de las canastas de compañeros que asiste | 7.0% | 8.2% | 6.7% | 4.2% | 0.0% |
| Pérdidas por jugada | 11.5% | 13.3% | 13.4% | 8.1% | 13.9% |

#### Naji Marshall: más de 0.5 robos (70%) — Dallas Mavericks @ Phoenix Suns

**¿Por qué 1.2 robos?** (línea 0.5; 22.7 minutos esperados)

En corto:

- La pasó en 14 de 15 esta temporada (falló con 0)
- Con 19+ minutos (hoy se esperan 23): 12 de 13 en sus últimos 15
- Contra las ~10 mejores defensas en robos a aleros/ala-pívots: 10 de 15 (últimos 40 partidos)
- Contra defensas medias como la de hoy y con 19+ minutos: 14 de 19, con 1.1 de media (últimos 60 partidos)
- El rival es #16 de 30 en robos que concede a aleros/ala-pívots por minuto (#1 = el que más concede; -0% frente a la media)
- Oportunidades de robo (últimos 10): el rival perdió 8.3 balones por partido con él en pista y robó el 19%
- El rival es #22 de 30 en balones que pierde (#1 = el que más; 13.3 por partido)
- Minutos: 23 esperados (suplente, ±5)

Razonamiento (3 factores a favor, 1 en contra):

- ❌ Minutos: 22.7 esperados (suplente, ±4.5).
- ✅ Forma: 2.0 en sus últimos 5, 1.5 esta temporada (15 partidos), 1.1 la temporada pasada (línea 0.5).
- ➖ Cómo produce robos: roba el 16.6% de las pérdidas del rival en pista × 13.0 pérdidas esperadas del rival.
- ➖ Defensa: el rival concede -0% de robos por minuto a aleros/ala-pívots (defensa media); ajuste aplicado -0%.
- ➖ Ritmo del partido: -0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 1, 1 (2 de 2 a favor).
- ✅ Últimos 10: la habría pasado 10 de 10.

- ⚠️ Alertas: suplente.
- Robos **1.2** (por componentes 1.0 · por tasa por minuto y defensa rival 1.2): roba el 16.6% de las pérdidas del rival en pista × 13.0 pérdidas esperadas del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 22.2 | 22.9 | 24.1 | 29.5 | 31.0 |
| Robos | 2.0 | 1.6 | 1.5 | 1.1 | 1.0 |
| % de las pérdidas del rival que roba | 25.0% | 19.3% | 18.1% | 14.2% | 15.4% |

#### DeMar DeRozan: menos de 0.5 triples (70%) — Denver Nuggets @ Utah Jazz

**¿Por qué 0.4 triples?** (línea 0.5; 19.7 minutos esperados)

En corto:

- La pasó en 13 de 15 esta temporada (falló con 1, 2)
- Con 16+ minutos (hoy se esperan 20): 12 de 14 en sus últimos 15
- Contra las ~10 mejores defensas en triples a bases/escoltas: 10 de 11 (últimos 40 partidos)
- Contra defensas débiles como la de hoy y con 16+ minutos: 14 de 19, con 0.3 de media (últimos 60 partidos)
- El rival es #1 de 30 en triples que concede a bases/escoltas por minuto (#1 = el que más concede; +11% frente a la media)
- Su zona principal es triple frontal (8% de sus tiros, 30% de acierto); el rival es #3 de 30 en acierto que deja ahí (36%, liga 35%)
- Cómo tira (últimos 15): creado 38% (36% de acierto), recibe y tira 26% (30% de acierto), penetración 19% (50% de acierto); en creado el rival es #9 de 30 en lo que deja (#1 = el que más; 0.96 puntos por tiro frente a 0.93 de media)
- Oportunidades: 1.6 triples intentados esperados al 31%
- Minutos: 20 esperados (suplente, ±3)

Razonamiento (2 factores a favor, 3 en contra):

- ❌ Minutos: 19.7 esperados (suplente, ±3.3).
- ✅ Forma: 0.2 en sus últimos 5, 0.2 esta temporada (15 partidos), 0.6 la temporada pasada (línea 0.5).
- ➖ Cómo produce triples: 1.6 triples intentados (su ritmo 2.7 por 36'; el rival concede +5% de triples en su reparto) × 31% esperado.
- ❌ Defensa: el rival concede +11% de triples por minuto a bases/escoltas (defensa débil); ajuste aplicado +5%; en su zona principal (triple) el rival concede 36% (liga 35%).
- ➖ Ritmo del partido: -0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ❌ Contra este rival: 1, 1, 1, 0 (1 de 4 a favor).
- ✅ Últimos 10: la habría pasado 9 de 10.
- ⚠️ partido desigual (favorito por 9.5): los suplentes suelen jugar +1% de minutos si se rompe.

- ⚠️ Alertas: suplente.
- Triples **0.4** (por componentes 0.5 · por tasa por minuto y defensa rival 0.3): 1.6 triples intentados (su ritmo 2.7 por 36'; el rival concede +5% de triples en su reparto) × 31% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 19.2 | 20.1 | 22.1 | 31.3 | 35.0 |
| Triples anotados | 0.2 | 0.1 | 0.2 | 0.6 | 0.8 |
| Triples intentados | 1.0 | 1.0 | 1.3 | 1.9 | 2.2 |
| % triples | 20.0% | 10.0% | 15.8% | 32.0% | 33.3% |


## Miami Heat @ New York Knicks

Diferencia esperada: New York Knicks por 2.5.

Parte de lesiones: Jordan Clarkson (Out); Giannis Antetokounmpo (Day-To-Day); Karl-Anthony Towns (Day-To-Day); OG Anunoby (Out); Miles McBride (Out); Andre Drummond (Out).

Ventajas del partido (los dos lados): puntos esperados frente a su media de los últimos 10, ajuste por la defensa rival y diferencia de estatura con los rivales de su posición.

| Equipo | Jugador | Puntos esperados | Su media (últ. 10) | Defensa rival en puntos | Rebotes esperados | Altura vs rival |
|---|---|---|---|---|---|---|
| MIA | Davion Mitchell | 15.5 | 18.0 | -4% | 3.0 | -3.7" |
| NY | Jalen Brunson | 26.9 | 26.5 | +4% | 3.5 | -0.8" |
| NY | Karl-Anthony Towns | 22.4 | 21.9 | -0% | 12.8 | +3.0" |
| MIA | Bam Adebayo | 17.2 | 21.0 | -7% | 8.4 | -2.6" |
| MIA | Giannis Antetokounmpo | 26.0 | 28.6 | -4% | 11.5 | +3.5" |
| NY | Josh Hart | 9.8 | 6.2 | +3% | 7.6 | +2.2" |
| NY | Mikal Bridges | 11.6 | 10.2 | +4% | 4.3 | +3.2" |
| NY | Landry Shamet | 12.6 | 12.9 | +4% | 2.3 | +2.2" |
| MIA | Pelle Larsson | 10.7 | 12.2 | -4% | 3.2 | +1.3" |
| MIA | Klay Thompson | 13.7 | 16.6 | -4% | 1.9 | +1.3" |

Las 8 más probables (máximo 2 por jugador: las de un mismo jugador suelen ganar o perder juntas).

| Prop | Prob. final | Modelo | Casa | Esperado | Últ. 10 | Temporada | vs este rival | Cuota (implícita) |
|---|---|---|---|---|---|---|---|---|
| **Josh Hart: menos de 0.5 tapones** | **70%** | 72% | 66% | 0.3 ± 0.6 | 8/10 | 11/15 | 0, 1, 0, 0 | 1.41 (71%) |
| **Bam Adebayo: menos de 1.5 triples** | **69%** | 72% | 65% | 1.0 ± 1.2 | 8/10 | 14/17 | 0, 1 | 1.45 (69%) |
| **Giannis Antetokounmpo: más de 0.5 tapones** | **69%** | 71% | 65% | 1.2 ± 1.1 | 8/10 | 12/16 | 0, 2 | 1.43 (70%) |
| **Bobby Portis: más de 0.5 triples** ⚠️ suplente | **68%** | 71% | 63% | 1.3 ± 1.2 | 8/10 | 14/17 | 2, 1, 1 | 1.50 (67%) |
| **Andrew Wiggins: más de 0.5 triples** ⚠️ suplente | **68%** | 71% | 63% | 1.4 ± 1.2 | 7/10 | 12/17 | 2, 0, 1, 1 | 1.48 (67%) |
| **Jose Alvarado: menos de 14.5 pts+reb+ast** ⚠️ suplente | **66%** | 77% | 54% | 10.2 ± 6.7 | 8/10 | 9/11 | 15 | 1.73 (58%) |
| **Klay Thompson: menos de 2.5 rebotes** | **66%** | 70% | 59% | 1.9 ± 1.7 | 8/10 | 13/16 | 5, 2 | 1.57 (64%) |
| **Bam Adebayo: más de 1.5 robos+tapones** | **65%** | 67% | 61% | 2.2 ± 1.6 | 7/10 | 14/17 | 0, 1 | 1.52 (66%) |

### Fichas de los jugadores destacados

#### Josh Hart (bases/escoltas) vs Miami Heat

- Minutos esperados: **32.6** (± 5.0); 100 partidos en la base.
- OG Anunoby ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Su prop más probable hoy: **Josh Hart: menos de 0.5 tapones** (70%). Con 80% de probabilidad: más de - / menos de 1.5.
- Defensa de Miami Heat contra bases/escoltas en tapones: +9% respecto a la media; ajuste por su historial contra defensas similares: +2%.

**¿Por qué 0.3 tapones?** (línea 0.5; 32.6 minutos esperados)

En corto:

- La pasó en 11 de 15 esta temporada (falló con 1, 1, 1, 1)
- Con 29+ minutos (hoy se esperan 33): 5 de 9 en sus últimos 15
- Contra las ~10 mejores defensas en tapones a bases/escoltas: 6 de 7 (últimos 40 partidos)
- Contra defensas débiles como la de hoy y con 29+ minutos: 9 de 12, con 0.3 de media (últimos 60 partidos)
- El rival es #5 de 30 en tapones que concede a bases/escoltas por minuto (#1 = el que más concede; +9% frente a la media)
- Oportunidades de tapón (últimos 10): 29.9 tiros de 2 del rival por partido con él en pista; taponó el 0.7%
- El rival es #9 de 30 en tiros de 2 por partido (#1 = el que más; 53.2)
- El 50% de los tiros del rival son cerca del aro (penetración, corte, poste, palmeo): #6 de 30
- Minutos: 33 esperados (titular, ±5)

Razonamiento (4 factores a favor, 2 en contra):

- ✅ Minutos: 32.6 esperados (titular, ±5.0).
- ✅ Forma: 0.4 en sus últimos 5, 0.3 esta temporada (15 partidos), 0.2 la temporada pasada (línea 0.5).
- ➖ Cómo produce tapones: tapona el 0.9% de los tiros de 2 del rival en pista × 48.9 tiros de 2 esperados del rival.
- ❌ Defensa: el rival concede +9% de tapones por minuto a bases/escoltas (defensa débil); ajuste aplicado +9%.
- ❌ Altura: mide 6'5", 2.2 pulgadas más que los bases/escoltas del rival (+1.6% en esta estadística).
- ➖ Ritmo del partido: -0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 0, 1, 0, 0 (3 de 4 a favor).
- ✅ Últimos 10: la habría pasado 8 de 10.
- ⚠️ OG Anunoby ya no jugó en sus últimos partidos: la baja ya está en sus minutos.

- Tapones **0.3** (por componentes 0.3 · por tasa por minuto y defensa rival 0.3): tapona el 0.9% de los tiros de 2 del rival en pista × 48.9 tiros de 2 esperados del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 33.8 | 30.2 | 31.1 | 30.6 | 32.5 |
| Tapones | 0.4 | 0.2 | 0.3 | 0.3 | 0.2 |
| % de los tiros de 2 del rival que tapona | 1.2% | 0.7% | 0.9% | 0.9% | 0.7% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -3%, vs defensa media +12%, vs defensa débil -6%; rebotes: vs defensa fuerte -15%, vs defensa media +2%, vs defensa débil +11%; asistencias: vs defensa fuerte -14%, vs defensa media +10%, vs defensa débil +4%; triples: vs defensa fuerte +4%, vs defensa media +4%, vs defensa débil -13%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 32% | 35% | 35% | 36% |
| bajo el aro | 30% | 66% | 67% | 66% |
| pintura | 16% | 46% | 45% | 47% |
| triple de esquina | 14% | 37% | 38% | 39% |
| media distancia | 8% | 35% | 41% | 41% |

#### Bam Adebayo (pívots) vs New York Knicks

- Minutos esperados: **32.9** (± 6.6); 91 partidos en la base.
- Su prop más probable hoy: **Bam Adebayo: menos de 1.5 triples** (69%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de New York Knicks contra pívots en triples: +0% respecto a la media; ajuste por su historial contra defensas similares: -2%.

**¿Por qué 1.0 triples?** (línea 1.5; 32.9 minutos esperados)

En corto:

- La pasó en 14 de 17 esta temporada (falló con 3, 2, 2)
- Con 29+ minutos (hoy se esperan 33): 11 de 14 en sus últimos 15
- Contra las ~10 mejores defensas en triples a pívots: 14 de 20 (últimos 40 partidos)
- Contra defensas medias como la de hoy y con 29+ minutos: 7 de 14, con 1.9 de media (últimos 60 partidos)
- El rival es #11 de 30 en triples que concede a pívots por minuto (#1 = el que más concede; +2% frente a la media)
- Su zona principal es triple frontal (21% de sus tiros, 31% de acierto); el rival es #26 de 30 en acierto que deja ahí (34%, liga 35%)
- Cómo tira (últimos 15): recibe y tira 31% (22% de acierto), penetración 26% (73% de acierto), creado 16% (59% de acierto); en recibe y tira el rival es #20 de 30 en lo que deja (#1 = el que más; 1.05 puntos por tiro frente a 1.07 de media)
- Oportunidades: 3.6 triples intentados esperados al 31%
- El rival no tiene a OG Anunoby (2.1 triples por partido)
- Minutos: 33 esperados (titular, ±7)

Razonamiento (4 factores a favor, 2 en contra):

- ❌ Minutos: 32.9 esperados (titular, ±6.6).
- ✅ Forma: 1.0 en sus últimos 5, 0.8 esta temporada (17 partidos), 1.7 la temporada pasada (línea 1.5).
- ➖ Cómo produce triples: 3.6 triples intentados (su ritmo 3.8 por 36'; el rival concede +6% de triples en su reparto) × 31% esperado.
- ➖ Defensa: el rival concede +2% de triples por minuto a pívots (defensa media); ajuste aplicado +0%; en su zona principal (triple) el rival concede 34% (liga 35%).
- ✅ Altura: mide 6'9", 2.6 pulgadas menos que los pívots del rival (-0.9% en esta estadística).
- ➖ Ritmo del partido: -0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 0, 1 (2 de 2 a favor).
- ✅ Últimos 10: la habría pasado 8 de 10.
- ❌ Bajas del rival: sin OG Anunoby (titular); +1.7% en esta estadística.

- ⚠️ Alertas: minutos inestables.
- Triples **1.0** (por componentes 1.1 · por tasa por minuto y defensa rival 1.0): 3.6 triples intentados (su ritmo 3.8 por 36'; el rival concede +6% de triples en su reparto) × 31% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 30.8 | 33.7 | 32.8 | 32.1 | 36.0 |
| Triples anotados | 1.0 | 0.9 | 0.8 | 1.7 | 0.5 |
| Triples intentados | 2.8 | 2.9 | 3.1 | 5.4 | 4.0 |
| % triples | 35.7% | 31.0% | 25.0% | 31.8% | 12.5% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -11%, vs defensa media +1%, vs defensa débil +13%; rebotes: vs defensa fuerte -2%, vs defensa media +2%, vs defensa débil +1%; asistencias: vs defensa fuerte +8%, vs defensa media -15%, vs defensa débil +5%; triples: vs defensa fuerte -26%, vs defensa media -4%, vs defensa débil +40%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| pintura | 31% | 49% | 45% | 42% |
| bajo el aro | 25% | 70% | 67% | 65% |
| triple frontal | 21% | 31% | 35% | 34% |
| media distancia | 12% | 34% | 41% | 39% |
| triple de esquina | 11% | 32% | 38% | 37% |

#### Giannis Antetokounmpo (aleros/ala-pívots) vs New York Knicks

- Minutos esperados: **32.7** (± 3.0); 52 partidos en la base.
- en el parte de lesiones: day-to-day
- Su prop más probable hoy: **Giannis Antetokounmpo: más de 0.5 tapones** (69%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de New York Knicks contra aleros/ala-pívots en tapones: +5% respecto a la media; ajuste por su historial contra defensas similares: +1%.

**¿Por qué 1.2 tapones?** (línea 0.5; 32.7 minutos esperados)

En corto:

- La pasó en 12 de 16 esta temporada (falló con 0, 0, 0, 0)
- Con 29+ minutos (hoy se esperan 33): 12 de 14 en sus últimos 15
- Contra las ~10 mejores defensas en tapones a aleros/ala-pívots: 7 de 17 (últimos 40 partidos)
- Contra defensas medias como la de hoy y con 29+ minutos: 9 de 12, con 1.1 de media (últimos 60 partidos)
- El rival es #11 de 30 en tapones que concede a aleros/ala-pívots por minuto (#1 = el que más concede; +5% frente a la media)
- Oportunidades de tapón (últimos 10): 31.0 tiros de 2 del rival por partido con él en pista; taponó el 5.2%
- El rival es #19 de 30 en tiros de 2 por partido (#1 = el que más; 50.3)
- El 44% de los tiros del rival son cerca del aro (penetración, corte, poste, palmeo): #24 de 30
- El rival no tiene a OG Anunoby (1.0 tapones por partido)
- Minutos: 33 esperados (titular, ±3)

Razonamiento (5 factores a favor, 0 en contra):

- ✅ Minutos: 32.7 esperados (titular, ±3.0).
- ✅ Forma: 1.8 en sus últimos 5, 1.2 esta temporada (16 partidos), 0.7 la temporada pasada (línea 0.5).
- ➖ Cómo produce tapones: tapona el 3.4% de los tiros de 2 del rival en pista × 51.8 tiros de 2 esperados del rival.
- ✅ Defensa: el rival concede +5% de tapones por minuto a aleros/ala-pívots (defensa media); ajuste aplicado +5%.
- ✅ Altura: mide 6'11", 3.5 pulgadas más que los aleros/ala-pívots del rival (+2.6% en esta estadística).
- ➖ Ritmo del partido: -0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ➖ Contra este rival: 0, 2 (1 de 2 a favor).
- ✅ Últimos 10: la habría pasado 8 de 10.
- ⚠️ en el parte de lesiones: day-to-day.

- ⚠️ Alertas: en el parte de lesiones.
- Tapones **1.2** (por componentes 1.2 · por tasa por minuto y defensa rival 1.2): tapona el 3.4% de los tiros de 2 del rival en pista × 51.8 tiros de 2 esperados del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 31.8 | 33.0 | 32.4 | 28.9 | 30.5 |
| Tapones | 1.8 | 1.6 | 1.2 | 0.7 | 1.0 |
| % de los tiros de 2 del rival que tapona | 5.6% | 5.2% | 3.9% | 2.1% | 2.8% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -7%, vs defensa media +4%, vs defensa débil +2%; rebotes: vs defensa fuerte -10%, vs defensa media -4%, vs defensa débil +17%; asistencias: vs defensa fuerte +6%, vs defensa media -1%, vs defensa débil -6%; triples: vs defensa fuerte +19%, vs defensa media +20%, vs defensa débil -31%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 57% | 75% | 67% | 65% |
| pintura | 18% | 51% | 45% | 42% |
| media distancia | 15% | 39% | 41% | 39% |
| triple frontal | 9% | 30% | 35% | 34% |
| triple de esquina | 0% | 38% | 38% | 37% |

#### Bobby Portis (aleros/ala-pívots) vs New York Knicks

- Minutos esperados: **18.0** (± 3.0); 84 partidos en la base.
- Su prop más probable hoy: **Bobby Portis: más de 0.5 triples** (68%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de New York Knicks contra aleros/ala-pívots en triples: +1% respecto a la media; ajuste por su historial contra defensas similares: -1%.

**¿Por qué 1.3 triples?** (línea 0.5; 18.0 minutos esperados)

En corto:

- La pasó en 14 de 17 esta temporada (falló con 0, 0, 0)
- Contra las ~10 mejores defensas en triples a aleros/ala-pívots: 9 de 13 (últimos 40 partidos)
- Contra defensas medias como la de hoy y con 14+ minutos: 15 de 18, con 1.8 de media (últimos 60 partidos)
- El rival es #10 de 30 en triples que concede a aleros/ala-pívots por minuto (#1 = el que más concede; +4% frente a la media)
- Su zona principal es triple frontal (25% de sus tiros, 39% de acierto); el rival es #26 de 30 en acierto que deja ahí (34%, liga 35%)
- Cómo tira (últimos 15): recibe y tira 59% (29% de acierto), penetración 12% (43% de acierto), poste 11% (50% de acierto); en recibe y tira el rival es #20 de 30 en lo que deja (#1 = el que más; 1.05 puntos por tiro frente a 1.07 de media)
- Oportunidades: 3.6 triples intentados esperados al 39%
- El rival no tiene a OG Anunoby (2.1 triples por partido)
- Minutos: 18 esperados (suplente, ±3)

Razonamiento (4 factores a favor, 1 en contra):

- ❌ Minutos: 18.0 esperados (suplente, ±3.0).
- ✅ Forma: 1.2 en sus últimos 5, 1.2 esta temporada (17 partidos), 2.1 la temporada pasada (línea 0.5).
- ➖ Cómo produce triples: 3.6 triples intentados (su ritmo 7.0 por 36'; el rival concede +6% de triples en su reparto) × 39% esperado.
- ➖ Defensa: el rival concede +4% de triples por minuto a aleros/ala-pívots (defensa media); ajuste aplicado +1%; en su zona principal (triple) el rival concede 34% (liga 35%).
- ➖ Ritmo del partido: -0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 2, 1, 1 (3 de 3 a favor).
- ✅ Últimos 10: la habría pasado 8 de 10.
- ✅ Bajas del rival: sin OG Anunoby (titular); +1.7% en esta estadística.

- ⚠️ Alertas: suplente.
- Triples **1.3** (por componentes 1.4 · por tasa por minuto y defensa rival 1.2): 3.6 triples intentados (su ritmo 7.0 por 36'; el rival concede +6% de triples en su reparto) × 39% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 18.8 | 17.8 | 19.6 | 24.1 | 17.0 |
| Triples anotados | 1.2 | 0.9 | 1.2 | 2.0 | 1.3 |
| Triples intentados | 4.2 | 3.8 | 4.0 | 4.4 | 3.7 |
| % triples | 28.6% | 23.7% | 30.9% | 45.6% | 36.4% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -10%, vs defensa media +5%, vs defensa débil +4%; rebotes: vs defensa fuerte -2%, vs defensa media +9%, vs defensa débil -4%; asistencias: vs defensa fuerte +3%, vs defensa media +24%, vs defensa débil -32%; triples: vs defensa fuerte +4%, vs defensa media -4%, vs defensa débil +0%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| media distancia | 26% | 44% | 41% | 39% |
| triple frontal | 25% | 39% | 35% | 34% |
| triple de esquina | 18% | 42% | 38% | 37% |
| pintura | 17% | 47% | 45% | 42% |
| bajo el aro | 14% | 64% | 67% | 65% |

#### Andrew Wiggins (aleros/ala-pívots) vs New York Knicks

- Minutos esperados: **25.5** (± 4.5); 86 partidos en la base.
- Su prop más probable hoy: **Andrew Wiggins: más de 0.5 triples** (68%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de New York Knicks contra aleros/ala-pívots en triples: +1% respecto a la media; ajuste por su historial contra defensas similares: -2%.

**¿Por qué 1.4 triples?** (línea 0.5; 25.5 minutos esperados)

En corto:

- La pasó en 12 de 17 esta temporada (falló con 0, 0, 0, 0)
- Con 22+ minutos (hoy se esperan 26): 9 de 12 en sus últimos 15
- Contra las ~10 mejores defensas en triples a aleros/ala-pívots: 11 de 13 (últimos 40 partidos)
- Contra defensas medias como la de hoy y con 22+ minutos: 10 de 15, con 1.6 de media (últimos 60 partidos)
- El rival es #10 de 30 en triples que concede a aleros/ala-pívots por minuto (#1 = el que más concede; +4% frente a la media)
- Su zona principal es triple frontal (31% de sus tiros, 38% de acierto); el rival es #26 de 30 en acierto que deja ahí (34%, liga 35%)
- Cómo tira (últimos 15): recibe y tira 48% (36% de acierto), penetración 24% (72% de acierto), creado 11% (50% de acierto); en recibe y tira el rival es #20 de 30 en lo que deja (#1 = el que más; 1.05 puntos por tiro frente a 1.07 de media)
- Oportunidades: 3.9 triples intentados esperados al 38%
- El rival no tiene a OG Anunoby (2.1 triples por partido)
- Minutos: 26 esperados (suplente, ±4)

Razonamiento (4 factores a favor, 1 en contra):

- ❌ Minutos: 25.5 esperados (suplente, ±4.5).
- ✅ Forma: 1.0 en sus últimos 5, 1.2 esta temporada (17 partidos), 2.1 la temporada pasada (línea 0.5).
- ➖ Cómo produce triples: 3.9 triples intentados (su ritmo 5.3 por 36'; el rival concede +6% de triples en su reparto) × 38% esperado.
- ➖ Defensa: el rival concede +4% de triples por minuto a aleros/ala-pívots (defensa media); ajuste aplicado +1%; en su zona principal (triple) el rival concede 34% (liga 35%).
- ➖ Ritmo del partido: -0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 2, 0, 1, 1 (3 de 4 a favor).
- ✅ Últimos 10: la habría pasado 7 de 10.
- ✅ Bajas del rival: sin OG Anunoby (titular); +1.7% en esta estadística.

- ⚠️ Alertas: suplente.
- Triples **1.4** (por componentes 1.5 · por tasa por minuto y defensa rival 1.3): 3.9 triples intentados (su ritmo 5.3 por 36'; el rival concede +6% de triples en su reparto) × 38% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 25.8 | 25.6 | 26.1 | 30.5 | 31.0 |
| Triples anotados | 1.0 | 1.1 | 1.2 | 2.1 | 1.0 |
| Triples intentados | 3.2 | 3.0 | 3.8 | 4.9 | 4.2 |
| % triples | 31.2% | 36.7% | 32.8% | 41.6% | 23.5% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -8%, vs defensa media +8%, vs defensa débil +1%; rebotes: vs defensa fuerte -7%, vs defensa media +11%, vs defensa débil -0%; asistencias: vs defensa fuerte -14%, vs defensa media -1%, vs defensa débil +23%; triples: vs defensa fuerte -15%, vs defensa media -30%, vs defensa débil +42%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 31% | 38% | 35% | 34% |
| bajo el aro | 24% | 68% | 67% | 65% |
| pintura | 22% | 41% | 45% | 42% |
| triple de esquina | 12% | 41% | 38% | 37% |
| media distancia | 11% | 43% | 41% | 39% |

## Milwaukee Bucks @ Detroit Pistons

Diferencia esperada: Detroit Pistons por 9.5 — algo desigual: titulares hasta -1.5% de minutos.

Parte de lesiones: Taurean Prince (Out); Duncan Robinson (Out); Cade Cunningham (Out); Jalen Duren (Out); Kasparas Jakucionis (Out); Ebuka Okorie (Out).

Ventajas del partido (los dos lados): puntos esperados frente a su media de los últimos 10, ajuste por la defensa rival y diferencia de estatura con los rivales de su posición.

| Equipo | Jugador | Puntos esperados | Su media (últ. 10) | Defensa rival en puntos | Rebotes esperados | Altura vs rival |
|---|---|---|---|---|---|---|
| DET | Daniss Jenkins | 20.1 | 17.1 | +2% | 4.9 | -0.4" |
| DET | Kevin Huerter | 16.9 | 13.0 | +2% | 4.6 | +1.6" |
| DET | Ausar Thompson | 12.4 | 11.4 | +2% | 8.1 | +2.6" |
| MIL | Tyler Herro | 21.6 | 22.3 | -5% | 4.2 | -0.4" |
| MIL | Kyle Kuzma | 13.9 | 15.1 | -2% | 5.1 | -0.5" |
| DET | Paul Reed | 16.2 | 10.2 | +1% | 8.2 | +1.0" |
| MIL | Jaime Jaquez Jr. | 13.8 | 12.5 | -2% | 4.5 | -2.5" |
| DET | Javonte Green | 11.4 | 7.3 | +3% | 4.3 | +0.6" |
| MIL | Myles Turner | 8.7 | 7.9 | -7% | 5.9 | +3.0" |
| MIL | Brayden Burries | 11.8 | 11.7 | -5% | 5.2 | -1.4" |

Las 8 más probables (máximo 2 por jugador: las de un mismo jugador suelen ganar o perder juntas).

| Prop | Prob. final | Modelo | Casa | Esperado | Últ. 10 | Temporada | vs este rival | Cuota (implícita) |
|---|---|---|---|---|---|---|---|---|
| **Nate Ament: menos de 1.5 asistencias** ⚠️ suplente | **80%** | 81% | 77% | 0.7 ± 0.9 | 10/10 | 16/17 | - | 1.25 (80%) |
| **Kel'el Ware: menos de 1.5 asistencias** ⚠️ suplente | **70%** | 69% | 72% | 1.1 ± 1.0 | 7/10 | 15/19 | 0, 0, 0 | 1.32 (76%) |
| **Tyler Herro: más de 0.5 robos** | **67%** | 69% | 63% | 1.1 ± 1.1 | 8/10 | 14/18 | 1, 0 | 1.50 (67%) |
| **Javonte Green: menos de 1.5 asistencias** ⚠️ suplente | **66%** | 68% | 63% | 1.2 ± 1.1 | 9/10 | 15/17 | 0, 0, 2, 0 | 1.41 (71%) |
| **Brayden Burries: menos de 1.5 triples** ⚠️ suplente | **65%** | 64% | 66% | 1.3 ± 1.1 | 6/10 | 14/19 | - | 1.43 (70%) |
| **Isaiah Joe: menos de 3.5 rebotes** ⚠️ suplente | **65%** | 71% | 60% | 2.5 ± 1.9 | 7/10 | 6/7 | 4, 1 | 1.59 (63%) |
| **Kevin Huerter: menos de 1.5 robos** | **65%** | 67% | 62% | 1.4 ± 1.2 | 9/10 | 16/17 | 0, 0 | 1.53 (66%) |
| **Paul Reed: menos de 0.5 triples** ⚠️ suplente | **65%** | 60% | 72% | 0.6 ± 0.8 | 10/10 | 14/17 | 0, 0, 1, 0 | 1.31 (76%) |

### Fichas de los jugadores destacados

#### Nate Ament (aleros/ala-pívots) vs Detroit Pistons

- Minutos esperados: **22.0** (± 5.9); 17 partidos en la base.
- partido desigual (no favorito por 9.5): los suplentes suelen jugar +1% de minutos si se rompe
- Su prop más probable hoy: **Nate Ament: menos de 1.5 asistencias** (80%). Con 80% de probabilidad: más de - / menos de 1.5.
- Defensa de Detroit Pistons contra aleros/ala-pívots en asistencias: -6% respecto a la media; ajuste por su historial contra defensas similares: -5%.

**¿Por qué 0.7 asistencias?** (línea 1.5; 22.0 minutos esperados)

En corto:

- La pasó en 16 de 17 esta temporada; los fallos, en partidos raros (paliza de 25)
- Con 18+ minutos (hoy se esperan 22): 8 de 9 en sus últimos 15
- Contra las ~10 mejores defensas en asistencias a aleros/ala-pívots: 10 de 10 (últimos 40 partidos)
- Contra defensas fuertes como la de hoy y con 18+ minutos: 7 de 7, con 0.7 de media (últimos 60 partidos)
- El rival es #27 de 30 en asistencias que concede a aleros/ala-pívots por minuto (#1 = el que más concede; -6% frente a la media)
- Asistencias esperadas: 0.7 por partido si sus compañeros metieran lo normal (tiene 0.7; con él en pista metieron el 95% de lo esperado por tipo de tiro, últimos 10); ajuste aplicado +3.2%
- Oportunidades: asiste el 5% de las canastas de sus compañeros con él en pista
- El rival no tiene a Cade Cunningham (8.6 asistencias por partido)
- Minutos: 22 esperados (suplente, ±6)

Razonamiento (3 factores a favor, 2 en contra):

- ❌ Minutos: 22.0 esperados (suplente, ±5.9).
- ✅ Forma: 0.4 en sus últimos 5, 0.5 esta temporada (17 partidos) (línea 1.5).
- ➖ Cómo produce asistencias: asiste el 5.3% de las canastas de sus compañeros en pista × 13.5 canastas de compañeros esperadas (su equipo 36.3 por 48' contra esta defensa).
- ✅ Defensa: el rival concede -6% de asistencias por minuto a aleros/ala-pívots (defensa fuerte); ajuste aplicado -6%.
- ➖ Ritmo del partido: -1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Últimos 10: la habría pasado 10 de 10.
- ❌ Bajas del rival: sin Cade Cunningham (titular); +1.5% en esta estadística.
- ⚠️ partido desigual (no favorito por 9.5): los suplentes suelen jugar +1% de minutos si se rompe.

- ⚠️ Alertas: suplente.
- Asistencias **0.7** (por componentes 0.7 · por tasa por minuto y defensa rival 0.7): asiste el 5.3% de las canastas de sus compañeros en pista × 13.5 canastas de compañeros esperadas (su equipo 36.3 por 48' contra esta defensa).

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 22.4 | 21.8 | 19.0 | - | - |
| Asistencias | 0.4 | 0.7 | 0.5 | - | - |
| % de las canastas de compañeros que asiste | 2.3% | 4.5% | 3.8% | - | - |
| Pérdidas por jugada | 12.6% | 11.6% | 11.7% | - | - |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +12%, vs defensa media +3%, vs defensa débil -37%; rebotes: vs defensa fuerte -19%, vs defensa media +18%, vs defensa débil +11%; asistencias: vs defensa fuerte -15%, vs defensa media +44%; triples: vs defensa fuerte -5%, vs defensa media -45%, vs defensa débil +90%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 34% | 73% | 67% | 65% |
| triple frontal | 26% | 35% | 35% | 32% |
| triple de esquina | 21% | 37% | 38% | 38% |
| pintura | 13% | 35% | 45% | 44% |
| media distancia | 5% | 34% | 41% | 40% |

#### Kel'el Ware (pívots) vs Detroit Pistons

- Minutos esperados: **21.7** (± 3.5); 97 partidos en la base.
- partido desigual (no favorito por 9.5): los suplentes suelen jugar +1% de minutos si se rompe
- Su prop más probable hoy: **Kel'el Ware: menos de 1.5 asistencias** (70%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Detroit Pistons contra pívots en asistencias: -12% respecto a la media; ajuste por su historial contra defensas similares: +1%.

**¿Por qué 1.1 asistencias?** (línea 1.5; 21.7 minutos esperados)

En corto:

- La pasó en 15 de 19 esta temporada (falló con 2, 3, 2, 3)
- Con 18+ minutos (hoy se esperan 22): 3 de 7 en sus últimos 15
- Contra las ~10 mejores defensas en asistencias a pívots: 14 de 18 (últimos 40 partidos)
- Contra defensas fuertes como la de hoy y con 18+ minutos: 7 de 10, con 1.4 de media (últimos 60 partidos)
- El rival es #29 de 30 en asistencias que concede a pívots por minuto (#1 = el que más concede; -12% frente a la media)
- Asistencias esperadas: 1.3 por partido si sus compañeros metieran lo normal (tiene 1.2; con él en pista metieron el 90% de lo esperado por tipo de tiro, últimos 10); ajuste aplicado +5.9%
- Oportunidades: asiste el 7% de las canastas de sus compañeros con él en pista
- El rival no tiene a Cade Cunningham (8.6 asistencias por partido)
- Minutos: 22 esperados (suplente, ±4)

Razonamiento (4 factores a favor, 2 en contra):

- ❌ Minutos: 21.7 esperados (suplente, ±3.5).
- ✅ Forma: 1.2 en sus últimos 5, 0.9 esta temporada (19 partidos), 0.8 la temporada pasada (línea 1.5).
- ➖ Cómo produce asistencias: asiste el 7.3% de las canastas de sus compañeros en pista × 12.5 canastas de compañeros esperadas (su equipo 36.3 por 48' contra esta defensa).
- ✅ Defensa: el rival concede -12% de asistencias por minuto a pívots (defensa fuerte); ajuste aplicado -12%.
- ➖ Ritmo del partido: -1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 0, 0, 0 (3 de 3 a favor).
- ✅ Últimos 10: la habría pasado 7 de 10.
- ❌ Bajas del rival: sin Cade Cunningham (titular); +1.5% en esta estadística.
- ⚠️ partido desigual (no favorito por 9.5): los suplentes suelen jugar +1% de minutos si se rompe.

- ⚠️ Alertas: suplente.
- Asistencias **1.1** (por componentes 0.9 · por tasa por minuto y defensa rival 1.0): asiste el 7.3% de las canastas de sus compañeros en pista × 12.5 canastas de compañeros esperadas (su equipo 36.3 por 48' contra esta defensa).

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 22.0 | 20.1 | 19.2 | 22.4 | 25.0 |
| Asistencias | 1.2 | 1.2 | 0.9 | 0.8 | 0.0 |
| % de las canastas de compañeros que asiste | 7.0% | 8.2% | 6.7% | 4.2% | 0.0% |
| Pérdidas por jugada | 11.5% | 13.3% | 13.4% | 8.1% | 13.9% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -10%, vs defensa media +2%, vs defensa débil +13%; rebotes: vs defensa fuerte -7%, vs defensa media +3%, vs defensa débil +6%; asistencias: vs defensa fuerte -9%, vs defensa media -9%, vs defensa débil +15%; triples: vs defensa fuerte -19%, vs defensa media +11%, vs defensa débil +12%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 49% | 67% | 67% | 65% |
| triple frontal | 27% | 33% | 35% | 32% |
| pintura | 14% | 36% | 45% | 44% |
| triple de esquina | 9% | 44% | 38% | 38% |
| media distancia | 2% | 35% | 41% | 40% |

#### Tyler Herro (bases/escoltas) vs Detroit Pistons

- Minutos esperados: **33.4** (± 5.9); 52 partidos en la base.
- partido desigual (no favorito por 9.5): los titulares suelen jugar -1% de minutos si se rompe
- Su prop más probable hoy: **Tyler Herro: más de 0.5 robos** (67%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Detroit Pistons contra bases/escoltas en robos: -0% respecto a la media; ajuste por su historial contra defensas similares: +5%.

**¿Por qué 1.1 robos?** (línea 0.5; 33.4 minutos esperados)

En corto:

- La pasó en 14 de 18 esta temporada (falló con 0, 0, 0, 0)
- Con 29+ minutos (hoy se esperan 33): 8 de 10 en sus últimos 15
- Contra las ~10 mejores defensas en robos a bases/escoltas: 8 de 16 (últimos 40 partidos)
- Contra defensas medias como la de hoy y con 29+ minutos: 8 de 12, con 0.9 de media (últimos 60 partidos)
- El rival es #16 de 30 en robos que concede a bases/escoltas por minuto (#1 = el que más concede; -0% frente a la media)
- Oportunidades de robo (últimos 10): el rival perdió 8.6 balones por partido con él en pista y robó el 13%
- El rival es #15 de 30 en balones que pierde (#1 = el que más; 14.1 por partido)
- El rival no tiene a Cade Cunningham (1.4 robos por partido)
- Minutos: 33 esperados (titular, ±6)

Razonamiento (3 factores a favor, 0 en contra):

- ✅ Minutos: 33.4 esperados (titular, ±5.9).
- ✅ Forma: 1.4 en sus últimos 5, 1.1 esta temporada (18 partidos), 0.7 la temporada pasada (línea 0.5).
- ➖ Cómo produce robos: roba el 12.2% de las pérdidas del rival en pista × 12.7 pérdidas esperadas del rival.
- ➖ Defensa: el rival concede -0% de robos por minuto a bases/escoltas (defensa media); ajuste aplicado -0%.
- ➖ Ritmo del partido: -1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ➖ Contra este rival: 1, 0 (1 de 2 a favor).
- ✅ Últimos 10: la habría pasado 8 de 10.
- ⚠️ partido desigual (no favorito por 9.5): los titulares suelen jugar -1% de minutos si se rompe.

- Robos **1.1** (por componentes 1.1 · por tasa por minuto y defensa rival 1.1): roba el 12.2% de las pérdidas del rival en pista × 12.7 pérdidas esperadas del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 33.8 | 32.0 | 31.4 | 31.3 | 31.0 |
| Robos | 1.4 | 1.1 | 1.1 | 0.7 | 0.5 |
| % de las pérdidas del rival que roba | 17.9% | 12.8% | 12.9% | 8.3% | 6.7% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +2%, vs defensa media -7%, vs defensa débil +5%; rebotes: vs defensa fuerte -18%, vs defensa media +21%, vs defensa débil +3%; asistencias: vs defensa fuerte -15%, vs defensa media +16%, vs defensa débil +6%; triples: vs defensa fuerte +4%, vs defensa media -3%, vs defensa débil -2%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 38% | 38% | 35% | 32% |
| pintura | 28% | 53% | 45% | 44% |
| bajo el aro | 18% | 64% | 67% | 65% |
| media distancia | 10% | 36% | 41% | 40% |
| triple de esquina | 6% | 40% | 38% | 38% |

#### Javonte Green (bases/escoltas) vs Milwaukee Bucks

- Minutos esperados: **26.1** (± 6.8); 109 partidos en la base.
- Duncan Robinson ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- sin Cade Cunningham, la estrella de su equipo (20 partidos suyos sin él): más tiros y balón para él por minuto (puntos +13%, triples +1%, asistencias +20%)
- sin Cade Cunningham (20 partidos): 21.6 min vs 16.5 con él
- Jalen Duren ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Su prop más probable hoy: **Javonte Green: menos de 1.5 asistencias** (66%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Milwaukee Bucks contra bases/escoltas en asistencias: +4% respecto a la media; ajuste por su historial contra defensas similares: -4%.

**¿Por qué 1.2 asistencias?** (línea 1.5; 26.1 minutos esperados)

En corto:

- La pasó en 15 de 17 esta temporada (falló con 2, 2)
- Con 22+ minutos (hoy se esperan 26): 4 de 4 en sus últimos 15
- Hoy juega más que de costumbre (26 min frente a 20): con 22+ minutos, esta temporada y la pasada, la pasó 15 de 17 (88%)
- Contra las ~10 mejores defensas en asistencias a bases/escoltas: 16 de 17 (últimos 40 partidos)
- El rival es #10 de 30 en asistencias que concede a bases/escoltas por minuto (#1 = el que más concede; +4% frente a la media)
- Asistencias esperadas: 0.5 por partido si sus compañeros metieran lo normal (tiene 0.5; con él en pista metieron el 95% de lo esperado por tipo de tiro, últimos 10); ajuste aplicado +2.8%
- Oportunidades: asiste el 5% de las canastas de sus compañeros con él en pista
- Su equipo no tiene a Cade Cunningham: más tiros y balón para él
- Minutos: 26 esperados (suplente, ±7)

Razonamiento (3 factores a favor, 2 en contra):

- ❌ Minutos: 26.1 esperados (suplente, ±6.8).
- ✅ Forma: 0.4 en sus últimos 5, 0.5 esta temporada (17 partidos), 0.6 la temporada pasada (línea 1.5).
- ➖ Cómo produce asistencias: asiste el 5.4% de las canastas de sus compañeros en pista × 19.2 canastas de compañeros esperadas (su equipo 42.2 por 48' contra esta defensa).
- ❌ Defensa: el rival concede +4% de asistencias por minuto a bases/escoltas (defensa débil); ajuste aplicado +4%.
- ➖ Ritmo del partido: -1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 0, 0, 2, 0 (3 de 4 a favor).
- ✅ Últimos 10: la habría pasado 9 de 10.
- ⚠️ Duncan Robinson ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ sin Cade Cunningham, la estrella de su equipo (20 partidos suyos sin él): más tiros y balón para él por minuto (puntos +13%, triples +1%, asistencias +20%).
- ⚠️ sin Cade Cunningham (20 partidos): 21.6 min vs 16.5 con él.
- ⚠️ Jalen Duren ya no jugó en sus últimos partidos: la baja ya está en sus minutos.

- ⚠️ Alertas: suplente, minutos inestables, sin Cade Cunningham: más tiros para él.
- Asistencias **1.2** (por componentes 1.2 · por tasa por minuto y defensa rival 1.2): asiste el 5.4% de las canastas de sus compañeros en pista × 19.2 canastas de compañeros esperadas (su equipo 42.2 por 48' contra esta defensa).

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 25.2 | 19.6 | 19.4 | 17.1 | 15.5 |
| Asistencias | 0.4 | 0.5 | 0.5 | 0.6 | 0.5 |
| % de las canastas de compañeros que asiste | 2.1% | 3.3% | 3.1% | 4.5% | 3.8% |
| Pérdidas por jugada | 7.9% | 6.7% | 4.0% | 8.7% | 14.2% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +4%, vs defensa media -14%, vs defensa débil +12%; rebotes: vs defensa fuerte +1%, vs defensa media +4%, vs defensa débil -5%; asistencias: vs defensa fuerte -8%, vs defensa media +9%, vs defensa débil -0%; triples: vs defensa fuerte -9%, vs defensa media -5%, vs defensa débil +21%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 40% | 31% | 35% | 36% |
| triple de esquina | 25% | 44% | 38% | 39% |
| bajo el aro | 24% | 69% | 67% | 68% |
| pintura | 9% | 38% | 45% | 42% |
| media distancia | 3% | 40% | 41% | 43% |

#### Brayden Burries (bases/escoltas) vs Detroit Pistons

- Minutos esperados: **25.5** (± 3.1); 19 partidos en la base.
- Su prop más probable hoy: **Brayden Burries: menos de 1.5 triples** (65%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Detroit Pistons contra bases/escoltas en triples: -6% respecto a la media; ajuste por su historial contra defensas similares: +4%.

**¿Por qué 1.3 triples?** (línea 1.5; 25.5 minutos esperados)

En corto:

- La pasó en 14 de 19 esta temporada (falló con 2, 2, 3, 2)
- Con 22+ minutos (hoy se esperan 26): 8 de 12 en sus últimos 15
- Contra las ~10 mejores defensas en triples a bases/escoltas: 4 de 8 (últimos 40 partidos)
- Contra defensas fuertes como la de hoy y con 22+ minutos: 2 de 5, con 1.6 de media (últimos 60 partidos)
- El rival es #28 de 30 en triples que concede a bases/escoltas por minuto (#1 = el que más concede; -7% frente a la media)
- Su zona principal es triple frontal (31% de sus tiros, 33% de acierto); el rival es #30 de 30 en acierto que deja ahí (32%, liga 35%)
- Cómo tira (últimos 15): creado 34% (40% de acierto), penetración 33% (55% de acierto), recibe y tira 25% (29% de acierto); en creado el rival es #29 de 30 en lo que deja (#1 = el que más; 0.85 puntos por tiro frente a 0.93 de media)
- Oportunidades: 4.0 triples intentados esperados al 31%
- El rival no tiene a Cade Cunningham (1.7 triples por partido)
- Minutos: 26 esperados (suplente, ±3)

Razonamiento (1 factores a favor, 3 en contra):

- ❌ Minutos: 25.5 esperados (suplente, ±3.1).
- ❌ Forma: 1.6 en sus últimos 5, 1.1 esta temporada (19 partidos) (línea 1.5).
- ➖ Cómo produce triples: 4.0 triples intentados (su ritmo 5.7 por 36'; el rival concede +2% de triples en su reparto) × 31% esperado.
- ✅ Defensa: el rival concede -7% de triples por minuto a bases/escoltas (defensa fuerte); ajuste aplicado -6%; en su zona principal (triple) el rival concede 32% (liga 35%).
- ➖ Ritmo del partido: -1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ➖ Últimos 10: la habría pasado 6 de 10.
- ❌ Bajas del rival: sin Cade Cunningham (titular); +1.7% en esta estadística.

- ⚠️ Alertas: suplente.
- Triples **1.3** (por componentes 1.2 · por tasa por minuto y defensa rival 1.2): 4.0 triples intentados (su ritmo 5.7 por 36'; el rival concede +2% de triples en su reparto) × 31% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 26.0 | 25.6 | 23.0 | - | - |
| Triples anotados | 1.6 | 1.4 | 1.1 | - | - |
| Triples intentados | 4.0 | 3.7 | 3.6 | - | - |
| % triples | 40.0% | 37.8% | 30.4% | - | - |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +1%, vs defensa media -12%, vs defensa débil +12%; rebotes: vs defensa fuerte -5%, vs defensa media +4%, vs defensa débil +8%; asistencias: vs defensa fuerte +9%, vs defensa media +0%, vs defensa débil -23%; triples: vs defensa fuerte +34%, vs defensa media -49%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 31% | 33% | 35% | 32% |
| pintura | 25% | 46% | 45% | 44% |
| bajo el aro | 24% | 67% | 67% | 65% |
| triple de esquina | 11% | 34% | 38% | 38% |
| media distancia | 9% | 42% | 41% | 40% |

## Philadelphia 76ers @ Indiana Pacers

Diferencia esperada: Philadelphia 76ers por 3.5.

Parte de lesiones: T.J. McConnell (Day-To-Day); Larry Nance Jr. (Day-To-Day); Joel Embiid (Day-To-Day); Kelly Oubre Jr. (Day-To-Day); Jaylen Brown (Out); Tyrese Haliburton (Out); Ben Sheppard (Out); Ariel Hukporti (Out).

Ventajas del partido (los dos lados): puntos esperados frente a su media de los últimos 10, ajuste por la defensa rival y diferencia de estatura con los rivales de su posición.

| Equipo | Jugador | Puntos esperados | Su media (últ. 10) | Defensa rival en puntos | Rebotes esperados | Altura vs rival |
|---|---|---|---|---|---|---|
| PHI | VJ Edgecombe | 16.8 | 15.0 | +3% | 7.1 | +0.8" |
| PHI | Tyrese Maxey | 24.4 | 23.4 | +2% | 3.9 | -2.2" |
| IND | Andrew Nembhard | 17.0 | 16.0 | -2% | 2.9 | -0.3" |
| PHI | Joel Embiid | 24.7 | 20.0 | +4% | 9.9 | -0.2" |
| PHI | LeBron James | 19.0 | 17.5 | +1% | 7.0 | +1.3" |
| IND | Pascal Siakam | 23.9 | 24.0 | +1% | 6.6 | -0.4" |
| IND | Aaron Nesmith | 14.2 | 9.8 | -2% | 3.9 | +0.7" |
| PHI | Kentavious Caldwell-Pope | 9.1 | 5.7 | +3% | 3.8 | +0.8" |
| IND | Ivica Zubac | 12.5 | 11.6 | -1% | 9.6 | -0.3" |
| IND | Kelly Oubre Jr. | 13.2 | 14.2 | -2% | 4.1 | +3.7" |

Las 8 más probables (máximo 2 por jugador: las de un mismo jugador suelen ganar o perder juntas).

| Prop | Prob. final | Modelo | Casa | Esperado | Últ. 10 | Temporada | vs este rival | Cuota (implícita) |
|---|---|---|---|---|---|---|---|---|
| **Kelly Oubre Jr.: más de 0.5 asistencias** | **69%** | 71% | 64% | 1.4 ± 1.2 | 5/10 | 11/16 | 2, 1 | 1.44 (69%) |
| **Tyrese Maxey: menos de 1.5 robos** | **68%** | 70% | 65% | 1.1 ± 1.1 | 9/10 | 12/18 | 1, 1, 2, 2, 8 | 1.42 (71%) |
| **LeBron James: más de 0.5 robos** | **66%** | 67% | 64% | 1.1 ± 1.0 | 6/10 | 11/15 | 0, 1, 1 | 1.44 (70%) |
| **Anfernee Simons: más de 8.5 puntos** ⚠️ suplente | **63%** | 70% | 52% | 13.8 ± 7.3 | 6/10 | 10/19 | 12, 20, 9, 16, 8 | 1.79 (56%) |
| **Aaron Nesmith: más de 1.5 asistencias** | **63%** | 68% | 56% | 2.6 ± 1.7 | 7/10 | 9/15 | 4, 1, 1 | 1.68 (60%) |
| **Dean Wade: más de 0.5 triples** ⚠️ suplente | **62%** | 62% | 63% | 1.1 ± 1.1 | 6/10 | 8/15 | 3, 0, 1, 1, 0 | 1.49 (67%) |
| **Anfernee Simons: más de 1.5 triples** ⚠️ suplente | **62%** | 65% | 58% | 2.7 ± 1.9 | 5/10 | 9/19 | 1, 6, 1, 2, 2 | 1.61 (62%) |
| **LeBron James: menos de 1.5 triples** | **62%** | 62% | 62% | 1.3 ± 1.3 | 7/10 | 10/15 | 0, 2, 0 | 1.50 (67%) |

### Fichas de los jugadores destacados

#### Kelly Oubre Jr. (bases/escoltas) vs Philadelphia 76ers

- Minutos esperados: **26.2** (± 3.8); 78 partidos en la base.
- en el parte de lesiones: day-to-day
- sin Tyrese Haliburton, la estrella de su equipo (12 partidos suyos sin él): más tiros y balón para él por minuto (puntos +2%, triples -1%, asistencias +3%)
- Tyrese Haliburton ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Su prop más probable hoy: **Kelly Oubre Jr.: más de 0.5 asistencias** (69%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Philadelphia 76ers contra bases/escoltas en asistencias: +1% respecto a la media; ajuste por su historial contra defensas similares: -3%.

**¿Por qué 1.4 asistencias?** (línea 0.5; 26.2 minutos esperados)

En corto:

- La pasó en 11 de 16 esta temporada (falló con 0, 0, 0, 0)
- Con 22+ minutos (hoy se esperan 26): 6 de 10 en sus últimos 15
- Contra las ~10 mejores defensas en asistencias a bases/escoltas: 14 de 20 (últimos 40 partidos)
- Contra defensas medias como la de hoy y con 22+ minutos: 10 de 13, con 1.8 de media (últimos 60 partidos)
- El rival es #16 de 30 en asistencias que concede a bases/escoltas por minuto (#1 = el que más concede; +1% frente a la media)
- Asistencias esperadas: 0.8 por partido si sus compañeros metieran lo normal (tiene 0.8; con él en pista metieron el 97% de lo esperado por tipo de tiro, últimos 10); ajuste aplicado +1.5%
- Oportunidades: asiste el 7% de las canastas de sus compañeros con él en pista
- El rival no tiene a Jaylen Brown (3.0 asistencias por partido)
- Su equipo no tiene a Tyrese Haliburton: más tiros y balón para él
- Minutos: 26 esperados (titular, ±4)

Razonamiento (4 factores a favor, 0 en contra):

- ✅ Minutos: 26.2 esperados (titular, ±3.8).
- ✅ Forma: 0.8 en sus últimos 5, 1.1 esta temporada (16 partidos), 1.5 la temporada pasada (línea 0.5).
- ➖ Cómo produce asistencias: asiste el 7.5% de las canastas de sus compañeros en pista × 17.7 canastas de compañeros esperadas (su equipo 40.9 por 48' contra esta defensa).
- ➖ Defensa: el rival concede +1% de asistencias por minuto a bases/escoltas (defensa media); ajuste aplicado +1%.
- ➖ Ritmo del partido: +0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 2, 1 (2 de 2 a favor).
- ➖ Últimos 10: la habría pasado 5 de 10.
- ✅ Bajas del rival: sin Jaylen Brown (titular); +1.5% en esta estadística.
- ⚠️ en el parte de lesiones: day-to-day.
- ⚠️ sin Tyrese Haliburton, la estrella de su equipo (12 partidos suyos sin él): más tiros y balón para él por minuto (puntos +2%, triples -1%, asistencias +3%).
- ⚠️ Tyrese Haliburton ya no jugó en sus últimos partidos: la baja ya está en sus minutos.

- ⚠️ Alertas: en el parte de lesiones.
- Asistencias **1.4** (por componentes 1.4 · por tasa por minuto y defensa rival 1.4): asiste el 7.5% de las canastas de sus compañeros en pista × 17.7 canastas de compañeros esperadas (su equipo 40.9 por 48' contra esta defensa).

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 26.0 | 25.3 | 24.8 | 31.9 | 29.5 |
| Asistencias | 0.8 | 0.8 | 1.1 | 1.5 | 1.5 |
| % de las canastas de compañeros que asiste | 3.9% | 4.2% | 5.9% | 6.4% | 6.7% |
| Pérdidas por jugada | 11.7% | 8.0% | 8.2% | 9.7% | 14.5% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -6%, vs defensa media +7%, vs defensa débil +4%; rebotes: vs defensa fuerte -1%, vs defensa media -8%, vs defensa débil +8%; asistencias: vs defensa fuerte -19%, vs defensa media +18%, vs defensa débil +23%; triples: vs defensa fuerte -7%, vs defensa media -5%, vs defensa débil +23%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 29% | 67% | 67% | 68% |
| triple frontal | 25% | 31% | 35% | 35% |
| pintura | 22% | 49% | 45% | 42% |
| triple de esquina | 19% | 38% | 38% | 37% |
| media distancia | 5% | 40% | 41% | 39% |

#### Tyrese Maxey (bases/escoltas) vs Indiana Pacers

- Minutos esperados: **35.5** (± 3.0); 103 partidos en la base.
- sin Jaylen Brown, la estrella de su equipo (2 partidos suyos sin él): más tiros y balón para él por minuto (puntos +4%, triples -1%, asistencias +1%)
- Su prop más probable hoy: **Tyrese Maxey: menos de 1.5 robos** (68%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Indiana Pacers contra bases/escoltas en robos: -1% respecto a la media; ajuste por su historial contra defensas similares: -2%.

**¿Por qué 1.1 robos?** (línea 1.5; 35.5 minutos esperados)

En corto:

- La pasó en 12 de 18 esta temporada (falló con 2, 2, 2, 3)
- Contra las ~10 mejores defensas en robos a bases/escoltas: 14 de 20 (últimos 40 partidos)
- Contra defensas medias como la de hoy y con 32+ minutos: 11 de 16, con 1.1 de media (últimos 60 partidos)
- El rival es #17 de 30 en robos que concede a bases/escoltas por minuto (#1 = el que más concede; -1% frente a la media)
- Oportunidades de robo (últimos 10): el rival perdió 8.4 balones por partido con él en pista y robó el 7%
- El rival es #20 de 30 en balones que pierde (#1 = el que más; 13.6 por partido)
- Minutos: 36 esperados (titular, ±3)

Razonamiento (3 factores a favor, 0 en contra):

- ✅ Minutos: 35.5 esperados (titular, ±3.0).
- ✅ Forma: 0.6 en sus últimos 5, 1.1 esta temporada (18 partidos), 1.7 la temporada pasada (línea 1.5).
- ➖ Cómo produce robos: roba el 11.3% de las pérdidas del rival en pista × 13.8 pérdidas esperadas del rival.
- ➖ Defensa: el rival concede -1% de robos por minuto a bases/escoltas (defensa media); ajuste aplicado -1%.
- ➖ Ritmo del partido: +0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ➖ Contra este rival: 1, 1, 2, 2, 8 (2 de 5 a favor).
- ✅ Últimos 10: la habría pasado 9 de 10.
- ⚠️ sin Jaylen Brown, la estrella de su equipo (2 partidos suyos sin él): más tiros y balón para él por minuto (puntos +4%, triples -1%, asistencias +1%).

- ⚠️ Alertas: falla en partidos normales (6 de 18 esta temporada).
- Robos **1.1** (por componentes 1.2 · por tasa por minuto y defensa rival 1.1): roba el 11.3% de las pérdidas del rival en pista × 13.8 pérdidas esperadas del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 35.8 | 35.0 | 36.1 | 37.3 | 37.0 |
| Robos | 0.6 | 0.6 | 1.1 | 1.7 | 2.8 |
| % de las pérdidas del rival que roba | 6.4% | 7.1% | 10.9% | 15.4% | 20.0% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -3%, vs defensa media -1%, vs defensa débil +5%; rebotes: vs defensa fuerte -8%, vs defensa media -3%, vs defensa débil +14%; asistencias: vs defensa fuerte -8%, vs defensa media -2%, vs defensa débil +14%; triples: vs defensa fuerte -7%, vs defensa media +6%, vs defensa débil +1%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 36% | 37% | 35% | 35% |
| bajo el aro | 28% | 68% | 67% | 67% |
| pintura | 20% | 42% | 45% | 47% |
| media distancia | 13% | 43% | 41% | 43% |
| triple de esquina | 3% | 30% | 38% | 39% |

#### LeBron James (aleros/ala-pívots) vs Indiana Pacers

- Minutos esperados: **33.0** (± 3.0); 88 partidos en la base.
- sin Jaylen Brown, la estrella de su equipo (3 partidos suyos sin él): más tiros y balón para él por minuto (puntos +7%, triples +1%, asistencias +4%)
- sin Jaylen Brown (3 partidos): 33.3 min vs 32.4 con él
- Su prop más probable hoy: **LeBron James: más de 0.5 robos** (66%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Indiana Pacers contra aleros/ala-pívots en robos: -5% respecto a la media; ajuste por su historial contra defensas similares: -6%.

**¿Por qué 1.1 robos?** (línea 0.5; 33.0 minutos esperados)

En corto:

- La pasó en 11 de 15 esta temporada (falló con 0, 0, 0, 0)
- Contra las ~10 mejores defensas en robos a aleros/ala-pívots: 10 de 13 (últimos 40 partidos)
- Contra defensas fuertes como la de hoy y con 29+ minutos: 14 de 19, con 1.1 de media (últimos 60 partidos)
- El rival es #23 de 30 en robos que concede a aleros/ala-pívots por minuto (#1 = el que más concede; -5% frente a la media)
- Oportunidades de robo (últimos 10): el rival perdió 7.5 balones por partido con él en pista y robó el 12%
- El rival es #20 de 30 en balones que pierde (#1 = el que más; 13.6 por partido)
- Minutos: 33 esperados (titular, ±3)

Razonamiento (3 factores a favor, 1 en contra):

- ✅ Minutos: 33.0 esperados (titular, ±3.0).
- ✅ Forma: 0.8 en sus últimos 5, 1.1 esta temporada (15 partidos), 1.2 la temporada pasada (línea 0.5).
- ➖ Cómo produce robos: roba el 13.0% de las pérdidas del rival en pista × 13.8 pérdidas esperadas del rival.
- ❌ Defensa: el rival concede -5% de robos por minuto a aleros/ala-pívots (defensa fuerte); ajuste aplicado -5%.
- ➖ Ritmo del partido: +0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 0, 1, 1 (2 de 3 a favor).
- ➖ Últimos 10: la habría pasado 6 de 10.
- ⚠️ sin Jaylen Brown, la estrella de su equipo (3 partidos suyos sin él): más tiros y balón para él por minuto (puntos +7%, triples +1%, asistencias +4%).
- ⚠️ sin Jaylen Brown (3 partidos): 33.3 min vs 32.4 con él.

- Robos **1.1** (por componentes 1.2 · por tasa por minuto y defensa rival 1.0): roba el 13.0% de las pérdidas del rival en pista × 13.8 pérdidas esperadas del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 32.8 | 32.2 | 32.6 | 32.8 | 33.3 |
| Robos | 0.8 | 0.9 | 1.1 | 1.2 | 0.7 |
| % de las pérdidas del rival que roba | 11.8% | 12.0% | 13.6% | 12.4% | 6.7% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +1%, vs defensa media -4%, vs defensa débil +3%; rebotes: vs defensa fuerte -9%, vs defensa media +2%, vs defensa débil +8%; asistencias: vs defensa fuerte -13%, vs defensa media +3%, vs defensa débil +14%; triples: vs defensa fuerte -8%, vs defensa media +24%, vs defensa débil -10%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 35% | 73% | 67% | 67% |
| triple frontal | 22% | 33% | 35% | 35% |
| pintura | 22% | 41% | 45% | 47% |
| media distancia | 15% | 42% | 41% | 43% |
| triple de esquina | 5% | 32% | 38% | 39% |

#### Anfernee Simons (bases/escoltas) vs Indiana Pacers

- Minutos esperados: **25.5** (± 7.3); 74 partidos en la base.
- sin Jaylen Brown, la estrella de su equipo (3 partidos suyos sin él): más tiros y balón para él por minuto (puntos +9%, triples +8%, asistencias -3%)
- sin Jaylen Brown (3 partidos): 31.7 min vs 20.3 con él
- Su prop más probable hoy: **Anfernee Simons: más de 8.5 puntos** (63%). Con 80% de probabilidad: más de 7.5 / menos de 19.5.
- Defensa de Indiana Pacers contra bases/escoltas en puntos: +3% respecto a la media; ajuste por su historial contra defensas similares: +2%.

**¿Por qué 13.8 puntos?** (línea 8.5; 25.5 minutos esperados)

En corto:

- La pasó en 10 de 19 esta temporada (falló con 6, 3, 3, 6)
- Con 22+ minutos (hoy se esperan 26): 7 de 8 en sus últimos 15
- Hoy juega más que de costumbre (26 min frente a 21): con 22+ minutos, esta temporada y la pasada, la pasó 46 de 52 (88%)
- Contra las ~10 mejores defensas en puntos a bases/escoltas: 9 de 14 (últimos 40 partidos)
- Contra defensas débiles como la de hoy y con 22+ minutos: 17 de 19, con 18.1 de media (últimos 60 partidos)
- El rival es #4 de 30 en puntos que concede a bases/escoltas por minuto (#1 = el que más concede; +4% frente a la media)
- Su zona principal es triple frontal (54% de sus tiros, 38% de acierto); el rival es #12 de 30 en acierto que deja ahí (35%, liga 35%)
- El rival es #15 de 30 en tiros libres que concede a bases/escoltas (#1 = el que más; +1% frente a la media)
- Puntería: en sus últimos 10 metió el 120% de las canastas esperadas por sus tipos de tiro (viene caliente: suele bajar un poco)
- Cómo tira (últimos 15): recibe y tira 51% (45% de acierto), creado 30% (50% de acierto), penetración 17% (55% de acierto); en recibe y tira el rival es #7 de 30 en lo que deja (#1 = el que más; 1.12 puntos por tiro frente a 1.07 de media)
- Oportunidades: 11.3 tiros de campo y 1.5 libres esperados (1.12 puntos por tiro)
- Transición: el rival concede 11.3 puntos por partido al contraataque (#29 de 30, #1 = el que más); él anota 1.1 así por partido (ajuste aplicado -2.3%)
- Su equipo no tiene a Jaylen Brown: más tiros y balón para él
- Minutos: 26 esperados (suplente, ±7)

Razonamiento (3 factores a favor, 1 en contra):

- ❌ Minutos: 25.5 esperados (suplente, ±7.3).
- ✅ Forma: 10.8 en sus últimos 5, 10.5 esta temporada (19 partidos), 14.3 la temporada pasada (línea 8.5).
- ➖ Cómo produce puntos: 11.3 tiros de campo (su ritmo 14.5 por 36'; el rival concede +2% de tiros) × 1.12 puntos por tiro [triple frontal 54% de sus tiros al 38% (rival concede 35%, liga 35%); pintura 15% de sus tiros al 51% (rival concede 47%, liga 45%); media distancia 14% de sus tiros al 44% (rival concede 43%, liga 41%); bajo el aro 10% de sus tiros al 62% (rival concede 67%, liga 67%)] + 1.5 tiros libres × 82%.
- ✅ Defensa: el rival concede +4% de puntos por minuto a bases/escoltas (defensa débil); ajuste aplicado +3%; en su zona principal (triple) el rival concede 35% (liga 35%).
- ➖ Ritmo del partido: +0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 12, 20, 9, 16, 8 (4 de 5 a favor).
- ➖ Últimos 10: la habría pasado 6 de 10.
- ⚠️ sin Jaylen Brown, la estrella de su equipo (3 partidos suyos sin él): más tiros y balón para él por minuto (puntos +9%, triples +8%, asistencias -3%).
- ⚠️ sin Jaylen Brown (3 partidos): 31.7 min vs 20.3 con él.

- ⚠️ Alertas: suplente, minutos inestables.
- Puntos **13.8** (por componentes 14.0 · por tasa por minuto y defensa rival 14.6): 11.3 tiros de campo (su ritmo 14.5 por 36'; el rival concede +2% de tiros) × 1.12 puntos por tiro [triple frontal 54% de sus tiros al 38% (rival concede 35%, liga 35%); pintura 15% de sus tiros al 51% (rival concede 47%, liga 45%); media distancia 14% de sus tiros al 44% (rival concede 43%, liga 41%); bajo el aro 10% de sus tiros al 62% (rival concede 67%, liga 67%)] + 1.5 tiros libres × 82%.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 24.6 | 21.4 | 22.1 | 24.9 | 21.8 |
| Puntos | 10.8 | 10.9 | 10.5 | 14.3 | 13.0 |
| Tiros de campo intentados | 8.4 | 8.1 | 8.3 | 11.8 | 10.0 |
| % tiros de campo | 47.6% | 49.4% | 44.3% | 44.0% | 48.0% |
| Triples intentados | 5.6 | 5.1 | 5.6 | 6.9 | 6.2 |
| % triples | 35.7% | 41.2% | 40.2% | 38.5% | 38.7% |
| Tiros libres intentados | 1.0 | 0.9 | 1.0 | 1.4 | 1.2 |
| % tiros libres | 80.0% | 88.9% | 84.2% | 89.6% | 83.3% |
| Jugadas que usa por 36 min | 13.2 | 14.8 | 14.9 | 19.7 | 18.7 |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -15%, vs defensa media -0%, vs defensa débil +12%; rebotes: vs defensa fuerte +1%, vs defensa media -9%, vs defensa débil +5%; asistencias: vs defensa fuerte -21%, vs defensa media +15%, vs defensa débil +11%; triples: vs defensa fuerte -9%, vs defensa media -0%, vs defensa débil +14%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 54% | 38% | 35% | 35% |
| pintura | 15% | 51% | 45% | 47% |
| media distancia | 14% | 44% | 41% | 43% |
| bajo el aro | 10% | 62% | 67% | 67% |
| triple de esquina | 8% | 42% | 38% | 39% |

#### Aaron Nesmith (bases/escoltas) vs Philadelphia 76ers

- Minutos esperados: **30.6** (± 3.4); 60 partidos en la base.
- sin Tyrese Haliburton, la estrella de su equipo (12 partidos suyos sin él): más tiros y balón para él por minuto (puntos +8%, triples +11%, asistencias -2%)
- Tyrese Haliburton ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Su prop más probable hoy: **Aaron Nesmith: más de 1.5 asistencias** (63%). Con 80% de probabilidad: más de 0.5 / menos de 4.5.
- Defensa de Philadelphia 76ers contra bases/escoltas en asistencias: +1% respecto a la media; ajuste por su historial contra defensas similares: +2%.

**¿Por qué 2.6 asistencias?** (línea 1.5; 30.6 minutos esperados)

En corto:

- La pasó en 9 de 15 esta temporada (falló con 1, 1, 1, 1)
- Con 27+ minutos (hoy se esperan 31): 7 de 10 en sus últimos 15
- Contra las ~10 mejores defensas en asistencias a bases/escoltas: 9 de 15 (últimos 40 partidos)
- Contra defensas medias como la de hoy y con 27+ minutos: 7 de 13, con 2.4 de media (últimos 60 partidos)
- El rival es #16 de 30 en asistencias que concede a bases/escoltas por minuto (#1 = el que más concede; +1% frente a la media)
- Asistencias esperadas: 2.7 por partido si sus compañeros metieran lo normal (tiene 2.7; con él en pista metieron el 101% de lo esperado por tipo de tiro, últimos 10); ajuste aplicado -0.2%
- Oportunidades: asiste el 11% de las canastas de sus compañeros con él en pista
- El rival no tiene a Jaylen Brown (3.0 asistencias por partido)
- Su equipo no tiene a Tyrese Haliburton: más tiros y balón para él
- Minutos: 31 esperados (titular, ±3)

Razonamiento (4 factores a favor, 1 en contra):

- ✅ Minutos: 30.6 esperados (titular, ±3.4).
- ✅ Forma: 3.4 en sus últimos 5, 2.3 esta temporada (15 partidos), 1.9 la temporada pasada (línea 1.5).
- ➖ Cómo produce asistencias: asiste el 11.4% de las canastas de sus compañeros en pista × 21.3 canastas de compañeros esperadas (su equipo 40.9 por 48' contra esta defensa).
- ➖ Defensa: el rival concede +1% de asistencias por minuto a bases/escoltas (defensa media); ajuste aplicado +1%.
- ➖ Ritmo del partido: +0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ❌ Contra este rival: 4, 1, 1 (1 de 3 a favor).
- ✅ Últimos 10: la habría pasado 7 de 10.
- ✅ Bajas del rival: sin Jaylen Brown (titular); +1.5% en esta estadística.
- ⚠️ sin Tyrese Haliburton, la estrella de su equipo (12 partidos suyos sin él): más tiros y balón para él por minuto (puntos +8%, triples +11%, asistencias -2%).
- ⚠️ Tyrese Haliburton ya no jugó en sus últimos partidos: la baja ya está en sus minutos.

- Asistencias **2.6** (por componentes 2.4 · por tasa por minuto y defensa rival 2.6): asiste el 11.4% de las canastas de sus compañeros en pista × 21.3 canastas de compañeros esperadas (su equipo 40.9 por 48' contra esta defensa).

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 31.8 | 30.2 | 27.3 | 29.6 | 31.7 |
| Asistencias | 3.4 | 2.7 | 2.3 | 1.9 | 2.0 |
| % de las canastas de compañeros que asiste | 13.2% | 11.6% | 10.8% | 8.6% | 7.8% |
| Pérdidas por jugada | 6.1% | 9.3% | 10.0% | 10.1% | 17.6% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -7%, vs defensa media -3%, vs defensa débil +15%; rebotes: vs defensa fuerte +4%, vs defensa media -3%, vs defensa débil -2%; asistencias: vs defensa fuerte -2%, vs defensa media +2%, vs defensa débil +1%; triples: vs defensa fuerte -8%, vs defensa media -7%, vs defensa débil +18%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 37% | 33% | 35% | 35% |
| bajo el aro | 19% | 58% | 67% | 68% |
| pintura | 17% | 44% | 45% | 42% |
| triple de esquina | 17% | 37% | 38% | 37% |
| media distancia | 11% | 38% | 41% | 39% |

## Brooklyn Nets @ Toronto Raptors

Diferencia esperada: Toronto Raptors por 9.5 — algo desigual: titulares hasta -1.5% de minutos.

Parte de lesiones: Moritz Wagner (Out); RJ Barrett (Out); Nate Bittle (Out); Alijah Martin (Day-To-Day); Nolan Traore (Out); Kawhi Leonard (Out).

Ventajas del partido (los dos lados): puntos esperados frente a su media de los últimos 10, ajuste por la defensa rival y diferencia de estatura con los rivales de su posición.

| Equipo | Jugador | Puntos esperados | Su media (últ. 10) | Defensa rival en puntos | Rebotes esperados | Altura vs rival |
|---|---|---|---|---|---|---|
| TOR | Scottie Barnes | 22.1 | 24.7 | +3% | 7.7 | -1.8" |
| BKN | Julius Randle | 21.0 | 22.7 | -3% | 6.3 | +1.8" |
| TOR | Ja'Kobe Walter | 14.2 | 12.3 | +1% | 4.4 | -1.2" |
| BKN | Michael Porter Jr. | 20.5 | 17.9 | -4% | 7.3 | +2.8" |
| TOR | Immanuel Quickley | 18.1 | 17.5 | +1% | 4.0 | -3.2" |
| TOR | Jakob Poeltl | 10.3 | 10.7 | +4% | 7.7 | +1.6" |
| BKN | Day'Ron Sharpe | 8.9 | 10.1 | -1% | 7.7 | -2.0" |
| BKN | Noah Clowney | 11.4 | 8.9 | -3% | 4.0 | +2.8" |
| TOR | Collin Murray-Boyles | 10.8 | 9.4 | +3% | 6.0 | -2.8" |
| BKN | Egor Demin | 11.1 | 12.2 | +0% | 2.9 | +5.5" |

Las 8 más probables (máximo 2 por jugador: las de un mismo jugador suelen ganar o perder juntas).

| Prop | Prob. final | Modelo | Casa | Esperado | Últ. 10 | Temporada | vs este rival | Cuota (implícita) |
|---|---|---|---|---|---|---|---|---|
| **Day'Ron Sharpe: más de 0.5 tapones** | **68%** | 72% | 63% | 1.5 ± 1.3 | 7/10 | 11/17 | 0, 0 | 1.50 (67%) |
| **Noah Clowney: más de 0.5 asistencias** ⚠️ suplente | **68%** | 72% | 62% | 1.4 ± 1.2 | 7/10 | 12/17 | 2, 1, 3 | 1.53 (66%) |
| **Day'Ron Sharpe: más de 0.5 robos** | **68%** | 70% | 65% | 1.2 ± 1.1 | 8/10 | 12/17 | 0, 0 | 1.48 (68%) |
| **Jakob Poeltl: más de 0.5 robos** | **66%** | 67% | 64% | 1.2 ± 1.1 | 7/10 | 10/15 | 2, 0, 1 | 1.49 (67%) |
| **Allen Graves: menos de 5.5 rebotes** ⚠️ suplente | **65%** | 69% | 59% | 4.5 ± 2.9 | 9/10 | 15/17 | - | 1.60 (63%) |
| **Allen Graves: menos de 1.5 triples** ⚠️ suplente | **65%** | 68% | 60% | 1.2 ± 1.2 | 7/10 | 14/17 | - | 1.58 (63%) |
| **Ja'Kobe Walter: más de 1.5 asistencias** | **65%** | 68% | 59% | 2.5 ± 1.6 | 6/10 | 12/17 | 1, 0, 0, 0 | 1.61 (62%) |
| **Michael Porter Jr.: más de 0.5 robos** | **63%** | 62% | 64% | 0.9 ± 1.0 | 8/10 | 12/16 | 1, 1, 0 | 1.47 (68%) |

### Fichas de los jugadores destacados

#### Day'Ron Sharpe (pívots) vs Toronto Raptors

- Minutos esperados: **26.3** (± 3.7); 79 partidos en la base.
- sin Nolan Traore (24 partidos): 17.1 min vs 21.1 con él; pts -14%/min, reb -8%/min
- Su prop más probable hoy: **Day'Ron Sharpe: más de 0.5 tapones** (68%). Con 80% de probabilidad: más de - / menos de 3.5.
- Defensa de Toronto Raptors contra pívots en tapones: +1% respecto a la media; ajuste por su historial contra defensas similares: -4%.

**¿Por qué 1.5 tapones?** (línea 0.5; 26.3 minutos esperados)

En corto:

- La pasó en 11 de 17 esta temporada (falló con 0, 0, 0, 0)
- Con 22+ minutos (hoy se esperan 26): 5 de 9 en sus últimos 15
- Contra las ~10 mejores defensas en tapones a pívots: 9 de 20 (últimos 40 partidos)
- El rival es #15 de 30 en tapones que concede a pívots por minuto (#1 = el que más concede; +1% frente a la media)
- Oportunidades de tapón (últimos 10): 27.2 tiros de 2 del rival por partido con él en pista; taponó el 4.8%
- El rival es #5 de 30 en tiros de 2 por partido (#1 = el que más; 55.5)
- El 51% de los tiros del rival son cerca del aro (penetración, corte, poste, palmeo): #3 de 30
- El rival no tiene a RJ Barrett (0.6 tapones por partido)
- Minutos: 26 esperados (titular, ±4)

Razonamiento (3 factores a favor, 2 en contra):

- ✅ Minutos: 26.3 esperados (titular, ±3.7).
- ✅ Forma: 0.8 en sus últimos 5, 1.2 esta temporada (17 partidos), 0.4 la temporada pasada (línea 0.5).
- ➖ Cómo produce tapones: tapona el 4.2% de los tiros de 2 del rival en pista × 54.1 tiros de 2 esperados del rival.
- ➖ Defensa: el rival concede +1% de tapones por minuto a pívots (defensa media); ajuste aplicado +1%.
- ❌ Altura: mide 6'10", 2.0 pulgadas menos que los pívots del rival (-1.5% en esta estadística).
- ➖ Ritmo del partido: -0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ❌ Contra este rival: 0, 0 (0 de 2 a favor).
- ✅ Últimos 10: la habría pasado 7 de 10.
- ⚠️ sin Nolan Traore (24 partidos): 17.1 min vs 21.1 con él; pts -14%/min, reb -8%/min.

- Tapones **1.5** (por componentes 1.7 · por tasa por minuto y defensa rival 1.5): tapona el 4.2% de los tiros de 2 del rival en pista × 54.1 tiros de 2 esperados del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 26.0 | 25.6 | 24.4 | 18.7 | 18.5 |
| Tapones | 0.8 | 1.3 | 1.2 | 0.4 | 0.0 |
| % de los tiros de 2 del rival que tapona | 3.1% | 4.8% | 4.8% | 2.2% | 0.0% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -10%, vs defensa media -9%, vs defensa débil +20%; rebotes: vs defensa fuerte -5%, vs defensa media +11%, vs defensa débil -1%; asistencias: vs defensa fuerte -21%, vs defensa media +2%, vs defensa débil +15%; triples: vs defensa fuerte +35%, vs defensa media +1%, vs defensa débil -38%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 65% | 68% | 67% | 68% |
| pintura | 20% | 46% | 45% | 44% |
| triple frontal | 8% | 32% | 35% | 35% |
| triple de esquina | 6% | 34% | 38% | 38% |
| media distancia | 1% | 38% | 41% | 39% |

#### Noah Clowney (aleros/ala-pívots) vs Toronto Raptors

- Minutos esperados: **26.2** (± 5.5); 83 partidos en la base.
- sin Nolan Traore (24 partidos): 28.1 min vs 25.1 con él; pts +17%/min, reb -11%/min, ast +7%/min
- Su prop más probable hoy: **Noah Clowney: más de 0.5 asistencias** (68%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Toronto Raptors contra aleros/ala-pívots en asistencias: -11% respecto a la media; ajuste por su historial contra defensas similares: +1%.

**¿Por qué 1.4 asistencias?** (línea 0.5; 26.2 minutos esperados)

En corto:

- La pasó en 12 de 17 esta temporada (falló con 0, 0, 0, 0)
- Con 22+ minutos (hoy se esperan 26): 5 de 6 en sus últimos 15
- Hoy juega más que de costumbre (26 min frente a 22): con 22+ minutos, esta temporada y la pasada, la pasó 42 de 53 (79%)
- Contra las ~10 mejores defensas en asistencias a aleros/ala-pívots: 13 de 16 (últimos 40 partidos)
- Contra defensas fuertes como la de hoy y con 22+ minutos: 9 de 11, con 1.5 de media (últimos 60 partidos)
- El rival es #30 de 30 en asistencias que concede a aleros/ala-pívots por minuto (#1 = el que más concede; -11% frente a la media)
- Asistencias esperadas: 1.2 por partido si sus compañeros metieran lo normal (tiene 1.2; con él en pista metieron el 104% de lo esperado por tipo de tiro, últimos 10); ajuste aplicado -1.0%
- Oportunidades: asiste el 8% de las canastas de sus compañeros con él en pista
- El rival no tiene a RJ Barrett (4.6 asistencias por partido)
- Minutos: 26 esperados (suplente, ±5)

Razonamiento (4 factores a favor, 2 en contra):

- ❌ Minutos: 26.2 esperados (suplente, ±5.5).
- ✅ Forma: 1.6 en sus últimos 5, 1.1 esta temporada (17 partidos), 1.6 la temporada pasada (línea 0.5).
- ➖ Cómo produce asistencias: asiste el 7.9% de las canastas de sus compañeros en pista × 15.8 canastas de compañeros esperadas (su equipo 35.8 por 48' contra esta defensa).
- ❌ Defensa: el rival concede -11% de asistencias por minuto a aleros/ala-pívots (defensa fuerte); ajuste aplicado -11%.
- ➖ Ritmo del partido: -0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 2, 1, 3 (3 de 3 a favor).
- ✅ Últimos 10: la habría pasado 7 de 10.
- ✅ Bajas del rival: sin RJ Barrett (titular); +1.5% en esta estadística.
- ⚠️ sin Nolan Traore (24 partidos): 28.1 min vs 25.1 con él; pts +17%/min, reb -11%/min, ast +7%/min.

- ⚠️ Alertas: suplente.
- Asistencias **1.4** (por componentes 1.3 · por tasa por minuto y defensa rival 1.4): asiste el 7.9% de las canastas de sus compañeros en pista × 15.8 canastas de compañeros esperadas (su equipo 35.8 por 48' contra esta defensa).

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 23.6 | 21.8 | 21.8 | 27.0 | 35.0 |
| Asistencias | 1.6 | 1.2 | 1.1 | 1.6 | 2.0 |
| % de las canastas de compañeros que asiste | 9.0% | 7.2% | 6.6% | 8.6% | 9.6% |
| Pérdidas por jugada | 7.1% | 10.5% | 11.0% | 12.3% | 17.7% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -2%, vs defensa media -8%, vs defensa débil +13%; rebotes: vs defensa fuerte -15%, vs defensa media -16%, vs defensa débil +20%; asistencias: vs defensa fuerte -2%, vs defensa media -4%, vs defensa débil +8%; triples: vs defensa fuerte -19%, vs defensa media +1%, vs defensa débil +18%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 42% | 31% | 35% | 35% |
| triple de esquina | 19% | 38% | 38% | 38% |
| pintura | 19% | 44% | 45% | 44% |
| bajo el aro | 17% | 68% | 67% | 68% |
| media distancia | 3% | 38% | 41% | 39% |

#### Jakob Poeltl (pívots) vs Brooklyn Nets

- Minutos esperados: **26.7** (± 5.4); 68 partidos en la base.
- sin RJ Barrett, la estrella de su equipo (13 partidos suyos sin él): más tiros y balón para él por minuto (puntos -7%, asistencias +17%)
- RJ Barrett ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Kawhi Leonard ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Su prop más probable hoy: **Jakob Poeltl: más de 0.5 robos** (66%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Brooklyn Nets contra pívots en robos: +11% respecto a la media; ajuste por su historial contra defensas similares: +4%.

**¿Por qué 1.2 robos?** (línea 0.5; 26.7 minutos esperados)

En corto:

- La pasó en 10 de 15 esta temporada (falló con 0, 0, 0, 0)
- Con 23+ minutos (hoy se esperan 27): 7 de 9 en sus últimos 15
- Contra las ~10 mejores defensas en robos a pívots: 7 de 14 (últimos 40 partidos)
- Contra defensas débiles como la de hoy y con 23+ minutos: 11 de 14, con 1.4 de media (últimos 60 partidos)
- El rival es #7 de 30 en robos que concede a pívots por minuto (#1 = el que más concede; +11% frente a la media)
- Oportunidades de robo (últimos 10): el rival perdió 7.9 balones por partido con él en pista y robó el 14%
- El rival es #2 de 30 en balones que pierde (#1 = el que más; 15.4 por partido)
- Minutos: 27 esperados (titular, ±5)

Razonamiento (5 factores a favor, 0 en contra):

- ✅ Minutos: 26.7 esperados (titular, ±5.4).
- ✅ Forma: 1.2 en sus últimos 5, 0.9 esta temporada (15 partidos), 0.9 la temporada pasada (línea 0.5).
- ➖ Cómo produce robos: roba el 11.6% de las pérdidas del rival en pista × 17.2 pérdidas esperadas del rival.
- ✅ Defensa: el rival concede +11% de robos por minuto a pívots (defensa débil); ajuste aplicado +11%.
- ➖ Ritmo del partido: -0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 2, 0, 1 (2 de 3 a favor).
- ✅ Últimos 10: la habría pasado 7 de 10.
- ⚠️ sin RJ Barrett, la estrella de su equipo (13 partidos suyos sin él): más tiros y balón para él por minuto (puntos -7%, asistencias +17%).
- ⚠️ RJ Barrett ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ Kawhi Leonard ya no jugó en sus últimos partidos: la baja ya está en sus minutos.

- Robos **1.2** (por componentes 1.1 · por tasa por minuto y defensa rival 1.2): roba el 11.6% de las pérdidas del rival en pista × 17.2 pérdidas esperadas del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 24.8 | 26.2 | 24.2 | 24.2 | 18.7 |
| Robos | 1.2 | 1.1 | 0.9 | 0.9 | 1.0 |
| % de las pérdidas del rival que roba | 15.4% | 13.9% | 11.7% | 11.4% | 20.0% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +2%, vs defensa media -7%, vs defensa débil +4%; rebotes: vs defensa fuerte -5%, vs defensa media -11%, vs defensa débil +8%; asistencias: vs defensa fuerte -19%, vs defensa media +5%, vs defensa débil +20%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 59% | 75% | 67% | 69% |
| pintura | 33% | 48% | 45% | 46% |
| media distancia | 7% | 45% | 41% | 40% |
| triple frontal | 1% | 35% | 35% | 36% |
| triple de esquina | 0% | 38% | 38% | 41% |

#### Allen Graves (aleros/ala-pívots) vs Brooklyn Nets

- Minutos esperados: **24.1** (± 8.6); 17 partidos en la base.
- sin RJ Barrett, la estrella de su equipo (3 partidos suyos sin él): más tiros y balón para él por minuto (puntos +3%, triples +1%, asistencias +13%)
- RJ Barrett ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Kawhi Leonard ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- partido desigual (favorito por 9.5): los suplentes suelen jugar +1% de minutos si se rompe
- Su prop más probable hoy: **Allen Graves: menos de 5.5 rebotes** (65%). Con 80% de probabilidad: más de 1.5 / menos de 7.5.
- Defensa de Brooklyn Nets contra aleros/ala-pívots en rebotes: -1% respecto a la media; ajuste por su historial contra defensas similares: +3%.

**¿Por qué 4.5 rebotes?** (línea 5.5; 24.1 minutos esperados)

En corto:

- La pasó en 15 de 17 esta temporada (falló con 10, 6)
- Con 20+ minutos (hoy se esperan 24): 2 de 3 en sus últimos 15
- Contra las ~10 mejores defensas en rebotes a aleros/ala-pívots: 6 de 6 (últimos 40 partidos)
- El rival es #16 de 30 en rebotes que concede a aleros/ala-pívots por minuto (#1 = el que más concede; -1% frente a la media)
- El rival es #18 de 30 en rebotes que concede en total (#1 = el que más)
- El rival es #27 de 30 en rebotes ofensivos que concede en total (#1 = el que más)
- Rebotes disponibles con él en pista (últimos 10): 16.3 tiros fallados del rival y 19.3 de su equipo por partido; se queda el 11% y el 9%; el rival falla 46.6 tiros por partido (#24 de 30, #1 = el que más falla)
- Minutos: 24 esperados (suplente, ±9)

Razonamiento (3 factores a favor, 1 en contra):

- ❌ Minutos: 24.1 esperados (suplente, ±8.6).
- ✅ Forma: 4.6 en sus últimos 5, 3.1 esta temporada (17 partidos) (línea 5.5).
- ➖ Cómo produce rebotes: defensivos 2.5 = captura el 10.8% de los fallos del rival en pista × 44.2 fallos esperados del rival (liga 47.0) × 50% del partido; ofensivos 2.0 = 9.1% de los fallos de su equipo × 42.4.
- ➖ Defensa: el rival concede -1% de rebotes por minuto a aleros/ala-pívots (defensa media); ajuste aplicado -1%.
- ✅ Altura: mide 6'8", 1.8 pulgadas menos que los aleros/ala-pívots del rival (-0.6% en esta estadística).
- ➖ Ritmo del partido: -0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Últimos 10: la habría pasado 9 de 10.
- ⚠️ sin RJ Barrett, la estrella de su equipo (3 partidos suyos sin él): más tiros y balón para él por minuto (puntos +3%, triples +1%, asistencias +13%).
- ⚠️ RJ Barrett ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ Kawhi Leonard ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ partido desigual (favorito por 9.5): los suplentes suelen jugar +1% de minutos si se rompe.

- ⚠️ Alertas: suplente, minutos inestables.
- Rebotes **4.5** (por componentes 4.4 · por tasa por minuto y defensa rival 4.6): defensivos 2.5 = captura el 10.8% de los fallos del rival en pista × 44.2 fallos esperados del rival (liga 47.0) × 50% del partido; ofensivos 2.0 = 9.1% de los fallos de su equipo × 42.4.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 24.8 | 19.8 | 16.9 | - | - |
| Rebotes | 4.6 | 3.5 | 3.1 | - | - |
| % de los fallos del rival que captura | 12.4% | 11.0% | 9.6% | - | - |
| % de los fallos de su equipo que captura | 7.2% | 8.8% | 10.5% | - | - |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +17%, vs defensa media +6%, vs defensa débil -24%; rebotes: vs defensa fuerte -12%, vs defensa media +46%, vs defensa débil -20%; asistencias: vs defensa fuerte +45%, vs defensa débil -81%; triples: vs defensa fuerte +2%, vs defensa media -47%, vs defensa débil +33%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple de esquina | 29% | 34% | 38% | 41% |
| bajo el aro | 29% | 68% | 67% | 69% |
| triple frontal | 24% | 34% | 35% | 36% |
| pintura | 15% | 48% | 45% | 46% |
| media distancia | 3% | 38% | 41% | 40% |

#### Ja'Kobe Walter (bases/escoltas) vs Brooklyn Nets

- Minutos esperados: **34.3** (± 3.0); 96 partidos en la base.
- sin RJ Barrett, la estrella de su equipo (20 partidos suyos sin él): más tiros y balón para él por minuto (puntos +1%, triples -13%, asistencias -6%)
- RJ Barrett ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Kawhi Leonard ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- partido desigual (favorito por 9.5): los titulares suelen jugar -1% de minutos si se rompe
- Su prop más probable hoy: **Ja'Kobe Walter: más de 1.5 asistencias** (65%). Con 80% de probabilidad: más de 0.5 / menos de 4.5.
- Defensa de Brooklyn Nets contra bases/escoltas en asistencias: +5% respecto a la media; ajuste por su historial contra defensas similares: +5%.

**¿Por qué 2.5 asistencias?** (línea 1.5; 34.3 minutos esperados)

En corto:

- La pasó en 12 de 17 esta temporada (falló con 1, 0, 1, 0)
- Con 30+ minutos (hoy se esperan 34): 7 de 12 en sus últimos 15
- Contra las ~10 mejores defensas en asistencias a bases/escoltas: 5 de 13 (últimos 40 partidos)
- Contra defensas débiles como la de hoy y con 30+ minutos: 6 de 6, con 3.2 de media (últimos 60 partidos)
- El rival es #9 de 30 en asistencias que concede a bases/escoltas por minuto (#1 = el que más concede; +5% frente a la media)
- Asistencias esperadas: 1.9 por partido si sus compañeros metieran lo normal (tiene 1.9; con él en pista metieron el 98% de lo esperado por tipo de tiro, últimos 10); ajuste aplicado +1.4%
- Oportunidades: asiste el 10% de las canastas de sus compañeros con él en pista
- Su equipo no tiene a RJ Barrett: más tiros y balón para él
- Minutos: 34 esperados (titular, ±3)

Razonamiento (3 factores a favor, 1 en contra):

- ✅ Minutos: 34.3 esperados (titular, ±3.0).
- ✅ Forma: 2.8 en sus últimos 5, 2.2 esta temporada (17 partidos), 1.4 la temporada pasada (línea 1.5).
- ➖ Cómo produce asistencias: asiste el 9.8% de las canastas de sus compañeros en pista × 25.5 canastas de compañeros esperadas (su equipo 42.4 por 48' contra esta defensa).
- ✅ Defensa: el rival concede +5% de asistencias por minuto a bases/escoltas (defensa débil); ajuste aplicado +5%.
- ➖ Ritmo del partido: -0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ❌ Contra este rival: 1, 0, 0, 0 (0 de 4 a favor).
- ➖ Últimos 10: la habría pasado 6 de 10.
- ⚠️ sin RJ Barrett, la estrella de su equipo (20 partidos suyos sin él): más tiros y balón para él por minuto (puntos +1%, triples -13%, asistencias -6%).
- ⚠️ RJ Barrett ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ Kawhi Leonard ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ partido desigual (favorito por 9.5): los titulares suelen jugar -1% de minutos si se rompe.

- Asistencias **2.5** (por componentes 2.4 · por tasa por minuto y defensa rival 2.6): asiste el 9.8% de las canastas de sus compañeros en pista × 25.5 canastas de compañeros esperadas (su equipo 42.4 por 48' contra esta defensa).

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 35.2 | 33.3 | 31.7 | 21.5 | 20.2 |
| Asistencias | 2.8 | 1.9 | 2.2 | 1.2 | 0.2 |
| % de las canastas de compañeros que asiste | 10.9% | 7.8% | 9.0% | 7.0% | 1.6% |
| Pérdidas por jugada | 7.0% | 8.9% | 7.7% | 7.4% | 14.3% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -8%, vs defensa media +10%, vs defensa débil -2%; rebotes: vs defensa fuerte -21%, vs defensa media +12%, vs defensa débil +18%; asistencias: vs defensa fuerte -12%, vs defensa media -19%, vs defensa débil +33%; triples: vs defensa fuerte -7%, vs defensa media +24%, vs defensa débil -12%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 41% | 35% | 35% | 36% |
| triple de esquina | 28% | 40% | 38% | 41% |
| bajo el aro | 18% | 65% | 67% | 69% |
| pintura | 11% | 37% | 45% | 46% |
| media distancia | 3% | 41% | 41% | 40% |

## Atlanta Hawks @ Boston Celtics

Diferencia esperada: Boston Celtics por 8.5.

Parte de lesiones: CJ McCollum (Out); Jock Landale (Out); Mitchell Robinson (Out); Mouhamed Gueye (Out); Asa Newell (Out); Henri Veesaar (Out).

Ventajas del partido (los dos lados): puntos esperados frente a su media de los últimos 10, ajuste por la defensa rival y diferencia de estatura con los rivales de su posición.

| Equipo | Jugador | Puntos esperados | Su media (últ. 10) | Defensa rival en puntos | Rebotes esperados | Altura vs rival |
|---|---|---|---|---|---|---|
| BOS | Jayson Tatum | 26.0 | 26.7 | +2% | 8.2 | -0.6" |
| ATL | Dyson Daniels | 10.9 | 8.7 | -5% | 8.1 | +2.7" |
| ATL | Jalen Johnson | 18.7 | 18.2 | -4% | 8.9 | -0.2" |
| ATL | Onyeka Okongwu | 14.6 | 16.4 | -4% | 8.2 | +1.8" |
| ATL | Nickeil Alexander-Walker | 19.4 | 22.7 | -5% | 3.5 | +0.7" |
| BOS | Paul George | 18.8 | 19.9 | +2% | 5.6 | -0.6" |
| BOS | Derrick White | 12.7 | 13.2 | -1% | 3.5 | -0.8" |
| BOS | Payton Pritchard | 13.7 | 13.0 | -1% | 3.4 | -2.8" |
| BOS | Neemias Queta | 11.2 | 10.8 | +1% | 8.3 | +1.0" |
| ATL | Aaron Wiggins | 12.4 | 13.4 | -5% | 3.6 | +0.7" |

Las 8 más probables (máximo 2 por jugador: las de un mismo jugador suelen ganar o perder juntas).

| Prop | Prob. final | Modelo | Casa | Esperado | Últ. 10 | Temporada | vs este rival | Cuota (implícita) |
|---|---|---|---|---|---|---|---|---|
| **Neemias Queta: menos de 0.5 triples** | **79%** | 73% | 87% | 0.3 ± 0.5 | 7/10 | 12/17 | 0, 0 | 1.08 (93%) |
| **Jayson Tatum: menos de 1.5 robos** | **73%** | 77% | 66% | 1.0 ± 1.0 | 9/10 | 14/16 | 0 | 1.42 (71%) |
| **Dyson Daniels: menos de 0.5 tapones** | **68%** | 69% | 66% | 0.4 ± 0.8 | 7/10 | 12/17 | 0, 1, 1 | 1.41 (71%) |
| **Nickeil Alexander-Walker: menos de 0.5 tapones** | **67%** | 68% | 64% | 0.4 ± 0.6 | 7/10 | 12/17 | 0, 0, 0, 1 | 1.46 (69%) |
| **Baylor Scheierman: menos de 1.5 triples** ⚠️ suplente | **65%** | 66% | 64% | 1.1 ± 1.1 | 7/10 | 11/18 | 1, 1, 0, 3 | 1.45 (69%) |
| **Derrick White: más de 0.5 robos** | **65%** | 66% | 64% | 1.0 ± 1.0 | 7/10 | 13/17 | 1, 0, 1, 3 | 1.47 (68%) |
| **Paul George: menos de 0.5 tapones** | **65%** | 66% | 63% | 0.5 ± 0.7 | 6/10 | 11/15 | 1, 0 | 1.48 (68%) |
| **Dyson Daniels: menos de 0.5 triples** | **64%** | 63% | 65% | 0.5 ± 0.7 | 8/10 | 14/17 | 2, 0, 1 | 1.44 (69%) |

### Fichas de los jugadores destacados

#### Neemias Queta (pívots) vs Atlanta Hawks

- Minutos esperados: **25.8** (± 5.0); 100 partidos en la base.
- Su prop más probable hoy: **Neemias Queta: menos de 0.5 triples** (79%). Con 80% de probabilidad: más de - / menos de 1.5.
- Defensa de Atlanta Hawks contra pívots en triples: -6% respecto a la media; ajuste por su historial contra defensas similares: +2%.

**¿Por qué 0.3 triples?** (línea 0.5; 25.8 minutos esperados)

En corto:

- La pasó en 12 de 17 esta temporada (falló con 1, 1, 1, 1)
- Con 22+ minutos (hoy se esperan 26): 7 de 10 en sus últimos 15
- Contra las ~10 mejores defensas en triples a pívots: 9 de 12 (últimos 40 partidos)
- Contra defensas fuertes como la de hoy y con 22+ minutos: 16 de 18, con 0.1 de media (últimos 60 partidos)
- El rival es #27 de 30 en triples que concede a pívots por minuto (#1 = el que más concede; -10% frente a la media)
- Su zona principal es triple de esquina (2% de sus tiros, 46% de acierto); el rival es #25 de 30 en acierto que deja ahí (37%, liga 38%)
- Cómo tira (últimos 15): corte 33% (71% de acierto), penetración 25% (52% de acierto), palmeo 20% (75% de acierto); en corte el rival es #16 de 30 en lo que deja (#1 = el que más; 1.52 puntos por tiro frente a 1.52 de media)
- Oportunidades: 0.6 triples intentados esperados al 38%
- Minutos: 26 esperados (titular, ±5)

Razonamiento (5 factores a favor, 0 en contra):

- ✅ Minutos: 25.8 esperados (titular, ±5.0).
- ✅ Forma: 0.4 en sus últimos 5, 0.3 esta temporada (17 partidos), 0.0 la temporada pasada (línea 0.5).
- ➖ Cómo produce triples: 0.6 triples intentados (su ritmo 0.8 por 36'; el rival concede -3% de triples en su reparto) × 38% esperado.
- ✅ Defensa: el rival concede -10% de triples por minuto a pívots (defensa fuerte); ajuste aplicado -6%; en su zona principal (esquina3) el rival concede 37% (liga 38%).
- ➖ Ritmo del partido: +1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 0, 0 (2 de 2 a favor).
- ✅ Últimos 10: la habría pasado 7 de 10.

- Triples **0.3** (por componentes 0.2 · por tasa por minuto y defensa rival 0.3): 0.6 triples intentados (su ritmo 0.8 por 36'; el rival concede -3% de triples en su reparto) × 38% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 25.4 | 24.6 | 23.4 | 25.0 | 26.0 |
| Triples anotados | 0.4 | 0.3 | 0.3 | 0.0 | 0.0 |
| Triples intentados | 0.6 | 0.4 | 0.4 | 0.1 | 0.0 |
| % triples | 66.7% | 75.0% | 71.4% | 12.5% | - |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -5%, vs defensa media -13%, vs defensa débil +13%; rebotes: vs defensa fuerte -10%, vs defensa media +5%, vs defensa débil +4%; asistencias: vs defensa fuerte -6%, vs defensa media -0%, vs defensa débil +6%; triples: vs defensa fuerte +29%, vs defensa media +76%, vs defensa débil -100%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 62% | 73% | 67% | 67% |
| pintura | 32% | 50% | 45% | 44% |
| media distancia | 3% | 36% | 41% | 43% |
| triple de esquina | 2% | 46% | 38% | 37% |
| triple frontal | 2% | 31% | 35% | 35% |

#### Jayson Tatum (aleros/ala-pívots) vs Atlanta Hawks

- Minutos esperados: **35.4** (± 3.1); 38 partidos en la base.
- Su prop más probable hoy: **Jayson Tatum: menos de 1.5 robos** (73%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Atlanta Hawks contra aleros/ala-pívots en robos: +6% respecto a la media; ajuste por su historial contra defensas similares: +1%.

**¿Por qué 1.0 robos?** (línea 1.5; 35.4 minutos esperados)

En corto:

- La pasó en 14 de 16 esta temporada (falló con 2, 3)
- Con 31+ minutos (hoy se esperan 35): 9 de 11 en sus últimos 15
- Contra las ~10 mejores defensas en robos a aleros/ala-pívots: 13 de 19 (últimos 40 partidos)
- Contra defensas débiles como la de hoy y con 31+ minutos: 4 de 6, con 1.0 de media (últimos 60 partidos)
- El rival es #8 de 30 en robos que concede a aleros/ala-pívots por minuto (#1 = el que más concede; +6% frente a la media)
- Oportunidades de robo (últimos 10): el rival perdió 10.6 balones por partido con él en pista y robó el 8%
- El rival es #19 de 30 en balones que pierde (#1 = el que más; 13.7 por partido)
- Minutos: 35 esperados (titular, ±3)

Razonamiento (4 factores a favor, 1 en contra):

- ✅ Minutos: 35.4 esperados (titular, ±3.1).
- ✅ Forma: 1.0 en sus últimos 5, 0.8 esta temporada (16 partidos), 1.3 la temporada pasada (línea 1.5).
- ➖ Cómo produce robos: roba el 9.0% de las pérdidas del rival en pista × 12.7 pérdidas esperadas del rival.
- ❌ Defensa: el rival concede +6% de robos por minuto a aleros/ala-pívots (defensa débil); ajuste aplicado +6%.
- ➖ Ritmo del partido: +1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 0 (1 de 1 a favor).
- ✅ Últimos 10: la habría pasado 9 de 10.

- Robos **1.0** (por componentes 0.8 · por tasa por minuto y defensa rival 1.0): roba el 9.0% de las pérdidas del rival en pista × 12.7 pérdidas esperadas del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 35.6 | 33.8 | 34.5 | 33.6 | 37.0 |
| Robos | 1.0 | 0.8 | 0.8 | 1.3 | 0.0 |
| % de las pérdidas del rival que roba | 8.9% | 7.5% | 6.6% | 19.3% | 0.0% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -4%, vs defensa media +0%, vs defensa débil +3%; rebotes: vs defensa fuerte -14%, vs defensa media -5%, vs defensa débil +13%; asistencias: vs defensa fuerte +10%, vs defensa media -15%, vs defensa débil +6%; triples: vs defensa fuerte -37%, vs defensa media +3%, vs defensa débil +33%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 42% | 35% | 35% | 35% |
| bajo el aro | 24% | 66% | 67% | 67% |
| pintura | 15% | 41% | 45% | 44% |
| media distancia | 15% | 38% | 41% | 43% |
| triple de esquina | 4% | 34% | 38% | 37% |

#### Dyson Daniels (bases/escoltas) vs Boston Celtics

- Minutos esperados: **34.7** (± 3.8); 99 partidos en la base.
- CJ McCollum ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Su prop más probable hoy: **Dyson Daniels: menos de 0.5 tapones** (68%). Con 80% de probabilidad: más de - / menos de 1.5.
- Defensa de Boston Celtics contra bases/escoltas en tapones: -6% respecto a la media; ajuste por su historial contra defensas similares: +1%.

**¿Por qué 0.4 tapones?** (línea 0.5; 34.7 minutos esperados)

En corto:

- La pasó en 12 de 17 esta temporada (falló con 3, 1, 1, 1)
- Con 31+ minutos (hoy se esperan 35): 7 de 10 en sus últimos 15
- Contra las ~10 mejores defensas en tapones a bases/escoltas: 12 de 14 (últimos 40 partidos)
- Contra defensas medias como la de hoy y con 31+ minutos: 8 de 14, con 0.6 de media (últimos 60 partidos)
- El rival es #19 de 30 en tapones que concede a bases/escoltas por minuto (#1 = el que más concede; -6% frente a la media)
- Oportunidades de tapón (últimos 10): 34.2 tiros de 2 del rival por partido con él en pista; taponó el 1.5%
- El rival es #25 de 30 en tiros de 2 por partido (#1 = el que más; 46.5)
- El 38% de los tiros del rival son cerca del aro (penetración, corte, poste, palmeo): #30 de 30
- Minutos: 35 esperados (titular, ±4)

Razonamiento (3 factores a favor, 3 en contra):

- ✅ Minutos: 34.7 esperados (titular, ±3.8).
- ❌ Forma: 0.6 en sus últimos 5, 0.4 esta temporada (17 partidos), 0.4 la temporada pasada (línea 0.5).
- ➖ Cómo produce tapones: tapona el 1.3% de los tiros de 2 del rival en pista × 47.6 tiros de 2 esperados del rival.
- ✅ Defensa: el rival concede -6% de tapones por minuto a bases/escoltas (defensa media); ajuste aplicado -6%.
- ❌ Altura: mide 6'7", 2.7 pulgadas más que los bases/escoltas del rival (+2.0% en esta estadística).
- ➖ Ritmo del partido: +1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ❌ Contra este rival: 0, 1, 1 (1 de 3 a favor).
- ✅ Últimos 10: la habría pasado 7 de 10.
- ⚠️ CJ McCollum ya no jugó en sus últimos partidos: la baja ya está en sus minutos.

- Tapones **0.4** (por componentes 0.4 · por tasa por minuto y defensa rival 0.4): tapona el 1.3% de los tiros de 2 del rival en pista × 47.6 tiros de 2 esperados del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 34.8 | 33.6 | 31.6 | 32.8 | 35.0 |
| Tapones | 0.6 | 0.5 | 0.4 | 0.4 | 0.7 |
| % de los tiros de 2 del rival que tapona | 1.7% | 1.5% | 1.3% | 1.1% | 1.9% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +6%, vs defensa media +5%, vs defensa débil -15%; rebotes: vs defensa fuerte -6%, vs defensa media +5%, vs defensa débil +5%; asistencias: vs defensa fuerte -10%, vs defensa media +3%, vs defensa débil +10%; triples: vs defensa fuerte +5%, vs defensa media +19%, vs defensa débil -32%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 45% | 67% | 67% | 66% |
| pintura | 37% | 44% | 45% | 43% |
| triple frontal | 11% | 24% | 35% | 35% |
| triple de esquina | 5% | 26% | 38% | 36% |
| media distancia | 2% | 40% | 41% | 43% |

#### Nickeil Alexander-Walker (bases/escoltas) vs Boston Celtics

- Minutos esperados: **32.1** (± 3.4); 101 partidos en la base.
- CJ McCollum ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Su prop más probable hoy: **Nickeil Alexander-Walker: menos de 0.5 tapones** (67%). Con 80% de probabilidad: más de - / menos de 1.5.
- Defensa de Boston Celtics contra bases/escoltas en tapones: -6% respecto a la media; ajuste por su historial contra defensas similares: +4%.

**¿Por qué 0.4 tapones?** (línea 0.5; 32.1 minutos esperados)

En corto:

- La pasó en 12 de 17 esta temporada (falló con 1, 1, 2, 1)
- Con 28+ minutos (hoy se esperan 32): 10 de 14 en sus últimos 15
- Contra las ~10 mejores defensas en tapones a bases/escoltas: 12 de 15 (últimos 40 partidos)
- Contra defensas medias como la de hoy y con 28+ minutos: 11 de 23, con 0.6 de media (últimos 60 partidos)
- El rival es #19 de 30 en tapones que concede a bases/escoltas por minuto (#1 = el que más concede; -6% frente a la media)
- Oportunidades de tapón (últimos 10): 35.1 tiros de 2 del rival por partido con él en pista; taponó el 1.1%
- El rival es #25 de 30 en tiros de 2 por partido (#1 = el que más; 46.5)
- El 38% de los tiros del rival son cerca del aro (penetración, corte, poste, palmeo): #30 de 30
- Minutos: 32 esperados (titular, ±3)

Razonamiento (5 factores a favor, 0 en contra):

- ✅ Minutos: 32.1 esperados (titular, ±3.4).
- ✅ Forma: 0.4 en sus últimos 5, 0.4 esta temporada (17 partidos), 0.5 la temporada pasada (línea 0.5).
- ➖ Cómo produce tapones: tapona el 1.2% de los tiros de 2 del rival en pista × 47.6 tiros de 2 esperados del rival.
- ✅ Defensa: el rival concede -6% de tapones por minuto a bases/escoltas (defensa media); ajuste aplicado -6%.
- ➖ Ritmo del partido: +1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 0, 0, 0, 1 (3 de 4 a favor).
- ✅ Últimos 10: la habría pasado 7 de 10.
- ⚠️ CJ McCollum ya no jugó en sus últimos partidos: la baja ya está en sus minutos.

- Tapones **0.4** (por componentes 0.4 · por tasa por minuto y defensa rival 0.4): tapona el 1.2% de los tiros de 2 del rival en pista × 47.6 tiros de 2 esperados del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 33.2 | 32.7 | 31.6 | 33.5 | 33.2 |
| Tapones | 0.4 | 0.4 | 0.4 | 0.6 | 0.2 |
| % de los tiros de 2 del rival que tapona | 1.2% | 1.1% | 1.0% | 1.5% | 0.7% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -3%, vs defensa media +8%, vs defensa débil -3%; rebotes: vs defensa fuerte -1%, vs defensa media +9%, vs defensa débil -7%; asistencias: vs defensa fuerte -3%, vs defensa media +4%, vs defensa débil +1%; triples: vs defensa fuerte +8%, vs defensa media -4%, vs defensa débil -8%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 39% | 36% | 35% | 35% |
| bajo el aro | 24% | 60% | 67% | 66% |
| triple de esquina | 16% | 44% | 38% | 36% |
| pintura | 14% | 42% | 45% | 43% |
| media distancia | 8% | 41% | 41% | 43% |

#### Baylor Scheierman (bases/escoltas) vs Atlanta Hawks

- Minutos esperados: **17.1** (± 4.0); 102 partidos en la base.
- Su prop más probable hoy: **Baylor Scheierman: menos de 1.5 triples** (65%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Atlanta Hawks contra bases/escoltas en triples: -4% respecto a la media; ajuste por su historial contra defensas similares: +2%.

**¿Por qué 1.1 triples?** (línea 1.5; 17.1 minutos esperados)

En corto:

- La pasó en 11 de 18 esta temporada (falló con 2, 2, 3, 3)
- Con 13+ minutos (hoy se esperan 17): 7 de 13 en sus últimos 15
- Contra las ~10 mejores defensas en triples a bases/escoltas: 13 de 22 (últimos 40 partidos)
- Contra defensas fuertes como la de hoy y con 13+ minutos: 12 de 23, con 1.8 de media (últimos 60 partidos)
- El rival es #27 de 30 en triples que concede a bases/escoltas por minuto (#1 = el que más concede; -7% frente a la media)
- Su zona principal es triple frontal (47% de sus tiros, 37% de acierto); el rival es #20 de 30 en acierto que deja ahí (35%, liga 35%)
- Su segunda zona es triple de esquina (24% de sus tiros, 42% de acierto); el rival es #25 de 30 en acierto que deja ahí (37%, liga 38%)
- Cómo tira (últimos 15): recibe y tira 56% (40% de acierto), creado 22% (29% de acierto), penetración 17% (38% de acierto); en recibe y tira el rival es #18 de 30 en lo que deja (#1 = el que más; 1.07 puntos por tiro frente a 1.07 de media)
- Oportunidades: 3.0 triples intentados esperados al 38%
- Minutos: 17 esperados (suplente, ±4)

Razonamiento (4 factores a favor, 1 en contra):

- ❌ Minutos: 17.1 esperados (suplente, ±4.0).
- ✅ Forma: 0.6 en sus últimos 5, 1.2 esta temporada (18 partidos), 1.5 la temporada pasada (línea 1.5).
- ➖ Cómo produce triples: 3.0 triples intentados (su ritmo 6.5 por 36'; el rival concede -3% de triples en su reparto) × 38% esperado.
- ✅ Defensa: el rival concede -7% de triples por minuto a bases/escoltas (defensa fuerte); ajuste aplicado -4%; en su zona principal (triple) el rival concede 35% (liga 35%).
- ➖ Ritmo del partido: +1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 1, 1, 0, 3 (3 de 4 a favor).
- ✅ Últimos 10: la habría pasado 7 de 10.

- ⚠️ Alertas: suplente, falla en partidos normales (6 de 18 esta temporada).
- Triples **1.1** (por componentes 1.1 · por tasa por minuto y defensa rival 1.1): 3.0 triples intentados (su ritmo 6.5 por 36'; el rival concede -3% de triples en su reparto) × 38% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 15.2 | 17.5 | 19.0 | 18.2 | 25.8 |
| Triples anotados | 0.6 | 1.1 | 1.2 | 1.2 | 1.2 |
| Triples intentados | 3.6 | 3.5 | 3.3 | 3.1 | 4.0 |
| % triples | 16.7% | 31.4% | 37.3% | 39.8% | 31.2% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +11%, vs defensa media +1%, vs defensa débil -17%; rebotes: vs defensa fuerte +3%, vs defensa media -12%, vs defensa débil +8%; asistencias: vs defensa fuerte -0%, vs defensa media -4%, vs defensa débil +4%; triples: vs defensa fuerte +2%, vs defensa media -5%, vs defensa débil +3%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 47% | 37% | 35% | 35% |
| triple de esquina | 24% | 42% | 38% | 37% |
| pintura | 15% | 45% | 45% | 44% |
| bajo el aro | 8% | 68% | 67% | 67% |
| media distancia | 7% | 43% | 41% | 43% |

## Memphis Grizzlies @ Minnesota Timberwolves

Diferencia esperada: Minnesota Timberwolves por 2.5.

Parte de lesiones: Jerami Grant (Out); Donte DiVincenzo (Out); Scotty Pippen Jr. (Out); Jaylen Clark (Out); Isaiah Stewart (Day-To-Day); LaMelo Ball (Out); Anthony Edwards (Out); Zach Edey (Day-To-Day); Cameron Boozer (Out).

Ventajas del partido (los dos lados): puntos esperados frente a su media de los últimos 10, ajuste por la defensa rival y diferencia de estatura con los rivales de su posición.

| Equipo | Jugador | Puntos esperados | Su media (últ. 10) | Defensa rival en puntos | Rebotes esperados | Altura vs rival |
|---|---|---|---|---|---|---|
| MIN | Jaden McDaniels | 20.2 | 21.6 | +1% | 6.4 | +1.8" |
| MIN | Ayo Dosunmu | 19.1 | 19.6 | +2% | 4.6 | +1.1" |
| MIN | Jonathan Kuminga | 15.2 | 13.6 | +1% | 5.9 | -0.2" |
| MIN | Rudy Gobert | 10.1 | 7.8 | +1% | 10.8 | +1.3" |
| MEM | Cedric Coward | 15.9 | 16.5 | -3% | 7.5 | -3.7" |
| MEM | Ty Jerome | 22.7 | 22.4 | -3% | 3.6 | +0.0" |
| MEM | Cam Spencer | 13.6 | 14.9 | -2% | 2.9 | -2.0" |
| MEM | Jaylen Wells | 11.6 | 12.2 | -3% | 3.2 | -1.7" |
| MIN | Terrence Shannon Jr. | 14.5 | 12.3 | +2% | 3.1 | +3.1" |
| MEM | Taylor Hendricks | 10.2 | 9.9 | -3% | 4.5 | +0.3" |

Las 8 más probables (máximo 2 por jugador: las de un mismo jugador suelen ganar o perder juntas).

| Prop | Prob. final | Modelo | Casa | Esperado | Últ. 10 | Temporada | vs este rival | Cuota (implícita) |
|---|---|---|---|---|---|---|---|---|
| **Taylor Hendricks: menos de 1.5 triples** ⚠️ suplente | **71%** | 73% | 67% | 1.0 ± 1.1 | 9/10 | 12/14 | 0, 1, 0 | 1.48 (68%) |
| **Kris Murray: menos de 5.5 reb+ast** ⚠️ suplente | **70%** | 79% | 57% | 3.5 ± 3.1 | 9/10 | 14/15 | 0, 2, 6, 0 | 1.65 (61%) |
| **Zach Edey: menos de 1.5 asistencias** | **69%** | 71% | 65% | 1.1 ± 1.1 | 9/10 | 12/15 | 0 | 1.43 (70%) |
| **Bones Hyland: menos de 4.5 asistencias** ⚠️ suplente | **67%** | 75% | 55% | 3.0 ± 2.1 | 7/10 | 15/19 | 4, 0, 3, 4, 5 | 1.73 (58%) |
| **Bones Hyland: menos de 2.5 rebotes** ⚠️ suplente | **66%** | 73% | 57% | 1.9 ± 1.4 | 9/10 | 17/19 | 0, 2, 1, 1, 3 | 1.64 (61%) |
| **Kris Murray: menos de 11.5 pts+reb+ast** ⚠️ suplente | **65%** | 74% | 52% | 8.4 ± 6.6 | 8/10 | 13/15 | 7, 2, 22, 7 | 1.80 (56%) |
| **Terrence Shannon Jr.: menos de 7.5 reb+ast** ⚠️ suplente | **65%** | 72% | 54% | 6.0 ± 2.7 | 9/10 | 13/16 | 7, 1 | 1.71 (58%) |
| **Jaylen Wells: menos de 5.5 reb+ast** | **65%** | 71% | 56% | 4.2 ± 2.2 | 6/10 | 12/19 | 1, 1, 3, 7, 6 | 1.68 (60%) |

### Fichas de los jugadores destacados

#### Taylor Hendricks (aleros/ala-pívots) vs Minnesota Timberwolves

- Minutos esperados: **22.9** (± 4.0); 73 partidos en la base.
- Jerami Grant ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- sin Cameron Boozer, la estrella de su equipo (3 partidos suyos sin él): más tiros y balón para él por minuto (puntos +4%, triples +0%, asistencias +4%)
- Cameron Boozer ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Su prop más probable hoy: **Taylor Hendricks: menos de 1.5 triples** (71%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Minnesota Timberwolves contra aleros/ala-pívots en triples: -6% respecto a la media; ajuste por su historial contra defensas similares: -8%.

**¿Por qué 1.0 triples?** (línea 1.5; 22.9 minutos esperados)

En corto:

- La pasó en 12 de 14 esta temporada; los fallos, en partidos raros (paliza de 31, jugó 4 min)
- Con 19+ minutos (hoy se esperan 23): 7 de 9 en sus últimos 15
- Contra las ~10 mejores defensas en triples a aleros/ala-pívots: 13 de 15 (últimos 40 partidos)
- Contra defensas fuertes como la de hoy y con 19+ minutos: 11 de 13, con 0.9 de media (últimos 60 partidos)
- El rival es #27 de 30 en triples que concede a aleros/ala-pívots por minuto (#1 = el que más concede; -9% frente a la media)
- Su zona principal es triple frontal (28% de sus tiros, 33% de acierto); el rival es #27 de 30 en acierto que deja ahí (34%, liga 35%)
- Cómo tira (últimos 15): recibe y tira 38% (43% de acierto), penetración 37% (66% de acierto), corte 9% (71% de acierto); en recibe y tira el rival es #24 de 30 en lo que deja (#1 = el que más; 1.03 puntos por tiro frente a 1.07 de media)
- Oportunidades: 2.9 triples intentados esperados al 35%
- El rival no tiene a LaMelo Ball (3.3 triples por partido)
- Su equipo no tiene a Cameron Boozer: más tiros y balón para él
- Minutos: 23 esperados (suplente, ±4)

Razonamiento (4 factores a favor, 2 en contra):

- ❌ Minutos: 22.9 esperados (suplente, ±4.0).
- ✅ Forma: 0.4 en sus últimos 5, 0.7 esta temporada (14 partidos), 1.1 la temporada pasada (línea 1.5).
- ➖ Cómo produce triples: 2.9 triples intentados (su ritmo 4.9 por 36'; el rival concede -8% de triples en su reparto) × 35% esperado.
- ✅ Defensa: el rival concede -9% de triples por minuto a aleros/ala-pívots (defensa fuerte); ajuste aplicado -6%; en su zona principal (triple) el rival concede 34% (liga 35%).
- ➖ Ritmo del partido: +1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 0, 1, 0 (3 de 3 a favor).
- ✅ Últimos 10: la habría pasado 9 de 10.
- ❌ Bajas del rival: sin LaMelo Ball (titular); +1.7% en esta estadística.
- ⚠️ Jerami Grant ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ sin Cameron Boozer, la estrella de su equipo (3 partidos suyos sin él): más tiros y balón para él por minuto (puntos +4%, triples +0%, asistencias +4%).
- ⚠️ Cameron Boozer ya no jugó en sus últimos partidos: la baja ya está en sus minutos.

- ⚠️ Alertas: suplente, sin Cameron Boozer: más tiros para él.
- Triples **1.0** (por componentes 1.0 · por tasa por minuto y defensa rival 0.9): 2.9 triples intentados (su ritmo 4.9 por 36'; el rival concede -8% de triples en su reparto) × 35% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 23.4 | 21.1 | 16.4 | 19.0 | 22.7 |
| Triples anotados | 0.4 | 0.7 | 0.7 | 1.1 | 0.3 |
| Triples intentados | 2.2 | 2.1 | 1.9 | 3.1 | 3.3 |
| % triples | 18.2% | 33.3% | 37.0% | 34.2% | 10.0% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -18%, vs defensa media +10%, vs defensa débil +19%; rebotes: vs defensa fuerte -12%, vs defensa media +3%, vs defensa débil +12%; asistencias: vs defensa fuerte +2%, vs defensa media -19%, vs defensa débil +17%; triples: vs defensa fuerte -36%, vs defensa media +21%, vs defensa débil +28%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 33% | 66% | 67% | 64% |
| triple frontal | 28% | 33% | 35% | 34% |
| triple de esquina | 20% | 38% | 38% | 37% |
| pintura | 18% | 51% | 45% | 42% |
| media distancia | 1% | 41% | 41% | 39% |

#### Kris Murray (aleros/ala-pívots) vs Minnesota Timberwolves

- Minutos esperados: **17.7** (± 12.5); 78 partidos en la base.
- Jerami Grant ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- sin Cameron Boozer, la estrella de su equipo (3 partidos suyos sin él): más tiros y balón para él por minuto (puntos +7%, triples +3%, asistencias +3%)
- Cameron Boozer ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Su prop más probable hoy: **Kris Murray: menos de 5.5 reb+ast** (70%). Con 80% de probabilidad: más de 0.5 / menos de 6.5.
- Defensa de Minnesota Timberwolves contra aleros/ala-pívots en reb+ast: -4% respecto a la media; ajuste por su historial contra defensas similares: -1%.

**¿Por qué 3.5 reb+ast?** (línea 5.5; 17.7 minutos esperados)

En corto:

- La pasó en 14 de 15 esta temporada (falló con 7)
- Con 14+ minutos (hoy se esperan 18): 5 de 6 en sus últimos 15
- Hoy juega más que de costumbre (18 min frente a 13): con 14+ minutos, esta temporada y la pasada, la pasó 36 de 58 (62%)
- Contra las ~10 mejores defensas en rebotes a aleros/ala-pívots: 13 de 16 (últimos 40 partidos)
- Contra defensas medias como la de hoy y con 14+ minutos: 5 de 13, con 6.8 de media (últimos 60 partidos)
- El rival es #17 de 30 en rebotes que concede a aleros/ala-pívots por minuto (#1 = el que más concede; -1% frente a la media)
- El rival es #16 de 30 en rebotes que concede en total (#1 = el que más)
- El rival es #19 de 30 en rebotes ofensivos que concede en total (#1 = el que más)
- Rebotes disponibles con él en pista (últimos 10): 12.4 tiros fallados del rival y 12.3 de su equipo por partido; se queda el 6% y el 5%; el rival falla 46.5 tiros por partido (#25 de 30, #1 = el que más falla)
- El rival no tiene a LaMelo Ball (10.8 reb+ast por partido)
- Su equipo no tiene a Cameron Boozer: más tiros y balón para él
- Minutos: 18 esperados (suplente, ±12)

Razonamiento (4 factores a favor, 2 en contra):

- ❌ Minutos: 17.7 esperados (suplente, ±12.5).
- ✅ Forma: 2.4 en sus últimos 5, 2.4 esta temporada (15 partidos), 4.8 la temporada pasada (línea 5.5).
- ➖ Cómo produce rebotes: defensivos 1.5 = captura el 8.8% de los fallos del rival en pista × 46.4 fallos esperados del rival (liga 47.0) × 37% del partido; ofensivos 1.0 = 5.3% de los fallos de su equipo × 49.6.
- ➖ Cómo produce asistencias: asiste el 8.4% de las canastas de sus compañeros en pista × 12.9 canastas de compañeros esperadas (su equipo 40.7 por 48' contra esta defensa).
- ✅ Defensa: el rival concede -1% de rebotes por minuto a aleros/ala-pívots (defensa media); ajuste aplicado -4%.
- ➖ Ritmo del partido: +1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 0, 2, 6, 0 (3 de 4 a favor).
- ✅ Últimos 10: la habría pasado 9 de 10.
- ❌ Bajas del rival: sin LaMelo Ball (titular); +0.8% en esta estadística.
- ⚠️ Jerami Grant ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ sin Cameron Boozer, la estrella de su equipo (3 partidos suyos sin él): más tiros y balón para él por minuto (puntos +7%, triples +3%, asistencias +3%).
- ⚠️ Cameron Boozer ya no jugó en sus últimos partidos: la baja ya está en sus minutos.

- ⚠️ Alertas: suplente, minutos inestables, sin Cameron Boozer: más tiros para él.
- Rebotes **2.4** (por componentes 2.5 · por tasa por minuto y defensa rival 2.4): defensivos 1.5 = captura el 8.8% de los fallos del rival en pista × 46.4 fallos esperados del rival (liga 47.0) × 37% del partido; ofensivos 1.0 = 5.3% de los fallos de su equipo × 49.6.
- Asistencias **1.1** (por componentes 1.1 · por tasa por minuto y defensa rival 1.1): asiste el 8.4% de las canastas de sus compañeros en pista × 12.9 canastas de compañeros esperadas (su equipo 40.7 por 48' contra esta defensa).

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 17.2 | 12.6 | 13.1 | 21.8 | 19.0 |
| Rebotes | 1.6 | 1.4 | 1.6 | 3.4 | 1.8 |
| % de los fallos del rival que captura | 5.6% | 6.5% | 7.2% | 8.9% | 5.2% |
| % de los fallos de su equipo que captura | 3.4% | 4.9% | 5.0% | 6.5% | 3.5% |
| Asistencias | 0.8 | 0.8 | 0.8 | 1.3 | 0.2 |
| % de las canastas de compañeros que asiste | 5.8% | 7.8% | 7.2% | 7.7% | 1.8% |
| Pérdidas por jugada | 3.9% | 2.9% | 4.2% | 14.0% | 4.7% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +3%, vs defensa media -14%, vs defensa débil +10%; rebotes: vs defensa fuerte -17%, vs defensa media +1%, vs defensa débil +17%; asistencias: vs defensa fuerte -43%, vs defensa media +24%, vs defensa débil +17%; triples: vs defensa fuerte +45%, vs defensa media -60%, vs defensa débil -8%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 42% | 70% | 67% | 64% |
| triple de esquina | 32% | 29% | 38% | 37% |
| triple frontal | 17% | 28% | 35% | 34% |
| pintura | 9% | 42% | 45% | 42% |
| media distancia | 0% | 41% | 41% | 39% |

#### Zach Edey (pívots) vs Minnesota Timberwolves

- Minutos esperados: **19.0** (± 5.6); 26 partidos en la base.
- en el parte de lesiones: day-to-day
- Jerami Grant ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- sin Cameron Boozer, la estrella de su equipo (3 partidos suyos sin él): más tiros y balón para él por minuto (puntos +4%, triples -9%, asistencias +6%)
- Cameron Boozer ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Su prop más probable hoy: **Zach Edey: menos de 1.5 asistencias** (69%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Minnesota Timberwolves contra pívots en asistencias: +14% respecto a la media; ajuste por su historial contra defensas similares: -3%.

**¿Por qué 1.1 asistencias?** (línea 1.5; 19.0 minutos esperados)

En corto:

- La pasó en 12 de 15 esta temporada (falló con 2, 2, 3)
- Con 15+ minutos (hoy se esperan 19): 12 de 14 en sus últimos 15
- Contra las ~10 mejores defensas en asistencias a pívots: 9 de 9 (últimos 40 partidos)
- Contra defensas débiles como la de hoy y con 15+ minutos: 6 de 8, con 1.1 de media (últimos 60 partidos)
- El rival es #2 de 30 en asistencias que concede a pívots por minuto (#1 = el que más concede; +14% frente a la media)
- Asistencias esperadas: 0.9 por partido si sus compañeros metieran lo normal (tiene 0.9; con él en pista metieron el 105% de lo esperado por tipo de tiro, últimos 10); ajuste aplicado -1.4%
- Oportunidades: asiste el 7% de las canastas de sus compañeros con él en pista
- El rival no tiene a LaMelo Ball (5.6 asistencias por partido)
- Su equipo no tiene a Cameron Boozer: más tiros y balón para él
- Minutos: 19 esperados (titular, ±6)

Razonamiento (4 factores a favor, 2 en contra):

- ✅ Minutos: 19.0 esperados (titular, ±5.6).
- ✅ Forma: 1.0 en sus últimos 5, 0.9 esta temporada (15 partidos), 1.1 la temporada pasada (línea 1.5).
- ➖ Cómo produce asistencias: asiste el 6.7% de las canastas de sus compañeros en pista × 12.7 canastas de compañeros esperadas (su equipo 40.7 por 48' contra esta defensa).
- ❌ Defensa: el rival concede +14% de asistencias por minuto a pívots (defensa débil); ajuste aplicado +14%.
- ➖ Ritmo del partido: +1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 0 (1 de 1 a favor).
- ✅ Últimos 10: la habría pasado 9 de 10.
- ❌ Bajas del rival: sin LaMelo Ball (titular); +1.5% en esta estadística.
- ⚠️ en el parte de lesiones: day-to-day.
- ⚠️ Jerami Grant ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ sin Cameron Boozer, la estrella de su equipo (3 partidos suyos sin él): más tiros y balón para él por minuto (puntos +4%, triples -9%, asistencias +6%).
- ⚠️ Cameron Boozer ya no jugó en sus últimos partidos: la baja ya está en sus minutos.

- ⚠️ Alertas: en el parte de lesiones, sin Cameron Boozer: más tiros para él.
- Asistencias **1.1** (por componentes 0.9 · por tasa por minuto y defensa rival 1.1): asiste el 6.7% de las canastas de sus compañeros en pista × 12.7 canastas de compañeros esperadas (su equipo 40.7 por 48' contra esta defensa).

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 19.4 | 20.4 | 20.3 | 25.8 | 23.0 |
| Asistencias | 1.0 | 0.9 | 0.9 | 1.1 | 0.0 |
| % de las canastas de compañeros que asiste | 6.5% | 5.7% | 5.8% | 5.6% | 0.0% |
| Pérdidas por jugada | 14.3% | 17.6% | 16.9% | 18.8% | 20.0% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -23%, vs defensa media -4%, vs defensa débil +8%; rebotes: vs defensa fuerte +3%, vs defensa media -14%, vs defensa débil +5%; asistencias: vs defensa fuerte -64%, vs defensa media +50%, vs defensa débil +7%; triples: vs defensa fuerte +103%, vs defensa media -100%, vs defensa débil +40%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 53% | 72% | 67% | 64% |
| pintura | 42% | 49% | 45% | 42% |
| triple frontal | 4% | 36% | 35% | 34% |
| media distancia | 1% | 39% | 41% | 39% |
| triple de esquina | 0% | 38% | 38% | 37% |

#### Bones Hyland (bases/escoltas) vs Memphis Grizzlies

- Minutos esperados: **16.3** (± 3.0); 98 partidos en la base.
- Donte DiVincenzo ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- sin LaMelo Ball, la estrella de su equipo (0 partidos suyos sin él): más tiros y balón para él por minuto (puntos +7%, triples +4%, asistencias +6%)
- sin Anthony Edwards, la estrella de su equipo (20 partidos suyos sin él): más tiros y balón para él por minuto (puntos -3%, triples +0%, asistencias -5%)
- Anthony Edwards ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Su prop más probable hoy: **Bones Hyland: menos de 4.5 asistencias** (67%). Con 80% de probabilidad: más de 0.5 / menos de 5.5.
- Defensa de Memphis Grizzlies contra bases/escoltas en asistencias: +2% respecto a la media; ajuste por su historial contra defensas similares: +2%.

**¿Por qué 3.0 asistencias?** (línea 4.5; 16.3 minutos esperados)

En corto:

- La pasó en 15 de 19 esta temporada (falló con 6, 5, 8, 8)
- Con 12+ minutos (hoy se esperan 16): 10 de 14 en sus últimos 15
- Contra las ~10 mejores defensas en asistencias a bases/escoltas: 16 de 19 (últimos 40 partidos)
- Contra defensas medias como la de hoy y con 12+ minutos: 12 de 17, con 3.8 de media (últimos 60 partidos)
- El rival es #13 de 30 en asistencias que concede a bases/escoltas por minuto (#1 = el que más concede; +2% frente a la media)
- Asistencias esperadas: 3.0 por partido si sus compañeros metieran lo normal (tiene 3.1; con él en pista metieron el 104% de lo esperado por tipo de tiro, últimos 10); ajuste aplicado -1.1%
- Oportunidades: asiste el 23% de las canastas de sus compañeros con él en pista
- El rival no tiene a Cameron Boozer (5.1 asistencias por partido)
- Su equipo no tiene a LaMelo Ball, Anthony Edwards: más tiros y balón para él
- Minutos: 16 esperados (suplente, ±3)

Razonamiento (3 factores a favor, 3 en contra):

- ❌ Minutos: 16.3 esperados (suplente, ±3.0).
- ✅ Forma: 2.8 en sus últimos 5, 2.9 esta temporada (19 partidos), 2.7 la temporada pasada (línea 4.5).
- ➖ Cómo produce asistencias: asiste el 23.1% de las canastas de sus compañeros en pista × 11.1 canastas de compañeros esperadas (su equipo 43.4 por 48' contra esta defensa).
- ❌ Defensa: el rival concede +2% de asistencias por minuto a bases/escoltas (defensa media); ajuste aplicado +2%.
- ➖ Ritmo del partido: +1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 4, 0, 3, 4, 5 (4 de 5 a favor).
- ✅ Últimos 10: la habría pasado 7 de 10.
- ❌ Bajas del rival: sin Cameron Boozer (titular); +1.5% en esta estadística.
- ⚠️ Donte DiVincenzo ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ sin LaMelo Ball, la estrella de su equipo (0 partidos suyos sin él): más tiros y balón para él por minuto (puntos +7%, triples +4%, asistencias +6%).
- ⚠️ sin Anthony Edwards, la estrella de su equipo (20 partidos suyos sin él): más tiros y balón para él por minuto (puntos -3%, triples +0%, asistencias -5%).
- ⚠️ Anthony Edwards ya no jugó en sus últimos partidos: la baja ya está en sus minutos.

- ⚠️ Alertas: suplente, sin LaMelo Ball: más tiros para él.
- Asistencias **3.0** (por componentes 2.6 · por tasa por minuto y defensa rival 3.2): asiste el 23.1% de las canastas de sus compañeros en pista × 11.1 canastas de compañeros esperadas (su equipo 43.4 por 48' contra esta defensa).

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 16.2 | 16.1 | 14.4 | 16.3 | 18.4 |
| Asistencias | 2.8 | 3.1 | 2.9 | 2.6 | 3.2 |
| % de las canastas de compañeros que asiste | 22.0% | 24.6% | 25.6% | 19.7% | 21.1% |
| Pérdidas por jugada | 12.8% | 10.0% | 10.5% | 12.3% | 14.8% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -9%, vs defensa media +6%, vs defensa débil +5%; rebotes: vs defensa fuerte -15%, vs defensa media -0%, vs defensa débil +19%; asistencias: vs defensa fuerte -20%, vs defensa media +16%, vs defensa débil +6%; triples: vs defensa fuerte -14%, vs defensa media +17%, vs defensa débil -4%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 54% | 38% | 35% | 34% |
| bajo el aro | 20% | 65% | 67% | 69% |
| media distancia | 10% | 47% | 41% | 42% |
| triple de esquina | 9% | 38% | 38% | 40% |
| pintura | 7% | 40% | 45% | 45% |

#### Terrence Shannon Jr. (bases/escoltas) vs Memphis Grizzlies

- Minutos esperados: **23.2** (± 4.1); 67 partidos en la base.
- Donte DiVincenzo ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- sin LaMelo Ball, la estrella de su equipo (0 partidos suyos sin él): más tiros y balón para él por minuto (puntos +7%, triples +4%, asistencias +6%)
- sin Anthony Edwards, la estrella de su equipo (20 partidos suyos sin él): más tiros y balón para él por minuto (puntos +8%, triples +10%, asistencias -4%)
- Anthony Edwards ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Su prop más probable hoy: **Terrence Shannon Jr.: menos de 7.5 reb+ast** (65%). Con 80% de probabilidad: más de 3.5 / menos de 8.5.
- Defensa de Memphis Grizzlies contra bases/escoltas en reb+ast: +2% respecto a la media; ajuste por su historial contra defensas similares: -1%.

**¿Por qué 6.0 reb+ast?** (línea 7.5; 23.2 minutos esperados)

En corto:

- La pasó en 13 de 16 esta temporada (falló con 9, 8, 9)
- Con 19+ minutos (hoy se esperan 23): 10 de 13 en sus últimos 15
- Contra las ~10 mejores defensas en rebotes a bases/escoltas: 14 de 17 (últimos 40 partidos)
- Contra defensas medias como la de hoy y con 19+ minutos: 6 de 7, con 6.4 de media (últimos 60 partidos)
- El rival es #13 de 30 en rebotes que concede a bases/escoltas por minuto (#1 = el que más concede; +1% frente a la media)
- El rival es #11 de 30 en rebotes que concede en total (#1 = el que más)
- El rival es #2 de 30 en rebotes ofensivos que concede en total (#1 = el que más)
- Rebotes disponibles con él en pista (últimos 10): 24.8 tiros fallados del rival y 21.2 de su equipo por partido; se queda el 11% y el 1%; el rival falla 46.6 tiros por partido (#23 de 30, #1 = el que más falla)
- El rival no tiene a Cameron Boozer (13.5 reb+ast por partido)
- Su equipo no tiene a LaMelo Ball, Anthony Edwards: más tiros y balón para él
- Minutos: 23 esperados (suplente, ±4)

Razonamiento (3 factores a favor, 3 en contra):

- ❌ Minutos: 23.2 esperados (suplente, ±4.1).
- ✅ Forma: 6.0 en sus últimos 5, 6.2 esta temporada (16 partidos), 2.3 la temporada pasada (línea 7.5).
- ➖ Cómo produce rebotes: defensivos 2.7 = captura el 11.1% de los fallos del rival en pista × 49.6 fallos esperados del rival (liga 47.0) × 48% del partido; ofensivos 0.4 = 1.9% de los fallos de su equipo × 46.4.
- ➖ Cómo produce asistencias: asiste el 16.2% de las canastas de sus compañeros en pista × 16.0 canastas de compañeros esperadas (su equipo 43.4 por 48' contra esta defensa).
- ➖ Defensa: el rival concede +1% de rebotes por minuto a bases/escoltas (defensa media); ajuste aplicado +2%.
- ❌ Altura: mide 6'6", 3.1 pulgadas más que los bases/escoltas del rival (+1.1% en esta estadística).
- ➖ Ritmo del partido: +1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 7, 1 (2 de 2 a favor).
- ✅ Últimos 10: la habría pasado 9 de 10.
- ❌ Bajas del rival: sin Cameron Boozer (titular); +0.8% en esta estadística.
- ⚠️ Donte DiVincenzo ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ sin LaMelo Ball, la estrella de su equipo (0 partidos suyos sin él): más tiros y balón para él por minuto (puntos +7%, triples +4%, asistencias +6%).
- ⚠️ sin Anthony Edwards, la estrella de su equipo (20 partidos suyos sin él): más tiros y balón para él por minuto (puntos +8%, triples +10%, asistencias -4%).
- ⚠️ Anthony Edwards ya no jugó en sus últimos partidos: la baja ya está en sus minutos.

- ⚠️ Alertas: suplente, sin LaMelo Ball: más tiros para él.
- Rebotes **3.1** (por componentes 3.1 · por tasa por minuto y defensa rival 3.1): defensivos 2.7 = captura el 11.1% de los fallos del rival en pista × 49.6 fallos esperados del rival (liga 47.0) × 48% del partido; ofensivos 0.4 = 1.9% de los fallos de su equipo × 46.4.
- Asistencias **2.9** (por componentes 2.7 · por tasa por minuto y defensa rival 3.0): asiste el 16.2% de las canastas de sus compañeros en pista × 16.0 canastas de compañeros esperadas (su equipo 43.4 por 48' contra esta defensa).

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 23.0 | 22.9 | 22.8 | 13.8 | 18.5 |
| Rebotes | 2.6 | 3.0 | 3.2 | 1.3 | 3.0 |
| % de los fallos del rival que captura | 10.1% | 10.9% | 11.9% | 8.1% | 14.3% |
| % de los fallos de su equipo que captura | 1.0% | 1.4% | 1.7% | 1.8% | 0.0% |
| Asistencias | 3.4 | 3.4 | 3.0 | 1.0 | 1.0 |
| % de las canastas de compañeros que asiste | 19.1% | 19.8% | 16.8% | 8.9% | 7.0% |
| Pérdidas por jugada | 13.0% | 13.7% | 13.7% | 10.1% | 15.0% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -9%, vs defensa media +9%, vs defensa débil +3%; rebotes: vs defensa fuerte -11%, vs defensa media -1%, vs defensa débil +15%; asistencias: vs defensa fuerte +14%, vs defensa media -23%, vs defensa débil -4%; triples: vs defensa fuerte -33%, vs defensa media +19%, vs defensa débil +36%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 35% | 62% | 67% | 69% |
| triple frontal | 26% | 37% | 35% | 34% |
| pintura | 18% | 39% | 45% | 45% |
| triple de esquina | 15% | 37% | 38% | 40% |
| media distancia | 6% | 36% | 41% | 42% |

## Dallas Mavericks @ Phoenix Suns

Diferencia esperada: Phoenix Suns por 3.5.

Parte de lesiones: Dereck Lively II (Out); Mark Williams (Out); Tobi Lawal (Out); Tarik Biberovic (Out); Sergio de Larrea (Out); Kyrie Irving (Day-To-Day).

Ventajas del partido (los dos lados): puntos esperados frente a su media de los últimos 10, ajuste por la defensa rival y diferencia de estatura con los rivales de su posición.

| Equipo | Jugador | Puntos esperados | Su media (últ. 10) | Defensa rival en puntos | Rebotes esperados | Altura vs rival |
|---|---|---|---|---|---|---|
| PHX | Devin Booker | 25.4 | 23.9 | +1% | 3.4 | +1.8" |
| DAL | Cooper Flagg | 21.8 | 24.3 | -2% | 6.0 | +1.0" |
| DAL | Kyrie Irving | 20.8 | 21.2 | +0% | 3.9 | -1.7" |
| PHX | Jalen Green | 15.8 | 14.5 | +0% | 4.2 | +0.8" |
| PHX | Dillon Brooks | 16.4 | 13.2 | +2% | 4.1 | -1.0" |
| PHX | Miles Bridges | 13.8 | 11.6 | +2% | 6.4 | -1.0" |
| DAL | P.J. Washington | 11.8 | 14.1 | -3% | 5.4 | -1.0" |
| DAL | Caleb Martin | 7.6 | 7.0 | -3% | 4.1 | -3.0" |
| PHX | Collin Gillespie | 10.1 | 12.2 | -0% | 3.2 | -2.2" |
| DAL | Daniel Gafford | 9.8 | 8.8 | -2% | 5.9 | +2.0" |

Las 8 más probables (máximo 2 por jugador: las de un mismo jugador suelen ganar o perder juntas).

| Prop | Prob. final | Modelo | Casa | Esperado | Últ. 10 | Temporada | vs este rival | Cuota (implícita) |
|---|---|---|---|---|---|---|---|---|
| **Naji Marshall: más de 0.5 robos** ⚠️ suplente | **70%** | 72% | 68% | 1.2 ± 1.1 | 10/10 | 14/15 | 1, 1 | 1.41 (71%) |
| **Zaccharie Risacher: más de 0.5 asistencias** | **66%** | 69% | 62% | 1.2 ± 1.1 | 6/10 | 14/18 | 4 | 1.49 (67%) |
| **Devin Booker: más de 0.5 robos** | **65%** | 68% | 61% | 1.2 ± 1.1 | 8/10 | 11/17 | 0, 2, 2 | 1.50 (67%) |
| **Jalen Green: más de 0.5 robos** | **65%** | 66% | 62% | 1.2 ± 1.1 | 7/10 | 10/17 | 0, 0 | 1.50 (67%) |
| **P.J. Washington: menos de 1.5 asistencias** | **63%** | 64% | 63% | 1.2 ± 1.1 | 7/10 | 10/16 | 1, 0 | 1.48 (68%) |
| **Caleb Martin: menos de 1.5 triples** | **63%** | 64% | 62% | 1.2 ± 1.1 | 6/10 | 8/14 | 0, 0 | 1.51 (66%) |
| **Cooper Flagg: menos de 32.5 pts+reb** | **63%** | 71% | 51% | 27.8 ± 8.3 | 8/10 | 12/17 | 22, 32, 22 | 1.83 (55%) |
| **Cooper Flagg: menos de 39.5 pts+reb+ast** | **63%** | 70% | 51% | 33.5 ± 9.5 | 6/10 | 11/17 | 28, 34, 28 | 1.84 (54%) |

### Fichas de los jugadores destacados

#### Naji Marshall (aleros/ala-pívots) vs Phoenix Suns

- Minutos esperados: **22.7** (± 4.5); 89 partidos en la base.
- Su prop más probable hoy: **Naji Marshall: más de 0.5 robos** (70%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Phoenix Suns contra aleros/ala-pívots en robos: -0% respecto a la media; ajuste por su historial contra defensas similares: -1%.

**¿Por qué 1.2 robos?** (línea 0.5; 22.7 minutos esperados)

En corto:

- La pasó en 14 de 15 esta temporada (falló con 0)
- Con 19+ minutos (hoy se esperan 23): 12 de 13 en sus últimos 15
- Contra las ~10 mejores defensas en robos a aleros/ala-pívots: 10 de 15 (últimos 40 partidos)
- Contra defensas medias como la de hoy y con 19+ minutos: 14 de 19, con 1.1 de media (últimos 60 partidos)
- El rival es #16 de 30 en robos que concede a aleros/ala-pívots por minuto (#1 = el que más concede; -0% frente a la media)
- Oportunidades de robo (últimos 10): el rival perdió 8.3 balones por partido con él en pista y robó el 19%
- El rival es #22 de 30 en balones que pierde (#1 = el que más; 13.3 por partido)
- Minutos: 23 esperados (suplente, ±5)

Razonamiento (3 factores a favor, 1 en contra):

- ❌ Minutos: 22.7 esperados (suplente, ±4.5).
- ✅ Forma: 2.0 en sus últimos 5, 1.5 esta temporada (15 partidos), 1.1 la temporada pasada (línea 0.5).
- ➖ Cómo produce robos: roba el 16.6% de las pérdidas del rival en pista × 13.0 pérdidas esperadas del rival.
- ➖ Defensa: el rival concede -0% de robos por minuto a aleros/ala-pívots (defensa media); ajuste aplicado -0%.
- ➖ Ritmo del partido: -0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 1, 1 (2 de 2 a favor).
- ✅ Últimos 10: la habría pasado 10 de 10.

- ⚠️ Alertas: suplente.
- Robos **1.2** (por componentes 1.0 · por tasa por minuto y defensa rival 1.2): roba el 16.6% de las pérdidas del rival en pista × 13.0 pérdidas esperadas del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 22.2 | 22.9 | 24.1 | 29.5 | 31.0 |
| Robos | 2.0 | 1.6 | 1.5 | 1.1 | 1.0 |
| % de las pérdidas del rival que roba | 25.0% | 19.3% | 18.1% | 14.2% | 15.4% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +2%, vs defensa media -8%, vs defensa débil +4%; rebotes: vs defensa fuerte +1%, vs defensa media -4%, vs defensa débil +2%; asistencias: vs defensa fuerte -19%, vs defensa media -4%, vs defensa débil +20%; triples: vs defensa fuerte -13%, vs defensa media +5%, vs defensa débil +14%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| pintura | 39% | 52% | 45% | 46% |
| bajo el aro | 25% | 70% | 67% | 69% |
| triple frontal | 16% | 26% | 35% | 35% |
| triple de esquina | 13% | 36% | 38% | 36% |
| media distancia | 7% | 37% | 41% | 41% |

#### Zaccharie Risacher (aleros/ala-pívots) vs Phoenix Suns

- Minutos esperados: **22.9** (± 5.1); 88 partidos en la base.
- Su prop más probable hoy: **Zaccharie Risacher: más de 0.5 asistencias** (66%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Phoenix Suns contra aleros/ala-pívots en asistencias: -2% respecto a la media; ajuste por su historial contra defensas similares: -2%.

**¿Por qué 1.2 asistencias?** (línea 0.5; 22.9 minutos esperados)

En corto:

- La pasó en 14 de 18 esta temporada; los fallos, en partidos raros (paliza de 22, paliza de 37, jugó 14 min, jugó 15 min)
- Con 19+ minutos (hoy se esperan 23): 9 de 10 en sus últimos 15
- Contra las ~10 mejores defensas en asistencias a aleros/ala-pívots: 6 de 15 (últimos 40 partidos)
- Contra defensas medias como la de hoy y con 19+ minutos: 6 de 8, con 1.1 de media (últimos 60 partidos)
- El rival es #17 de 30 en asistencias que concede a aleros/ala-pívots por minuto (#1 = el que más concede; -2% frente a la media)
- Asistencias esperadas: 1.1 por partido si sus compañeros metieran lo normal (tiene 0.9; con él en pista metieron el 84% de lo esperado por tipo de tiro, últimos 10); ajuste aplicado +8.0%
- Oportunidades: asiste el 7% de las canastas de sus compañeros con él en pista
- Minutos: 23 esperados (titular, ±5)

Razonamiento (3 factores a favor, 0 en contra):

- ✅ Minutos: 22.9 esperados (titular, ±5.1).
- ✅ Forma: 0.8 en sus últimos 5, 1.2 esta temporada (18 partidos), 1.1 la temporada pasada (línea 0.5).
- ➖ Cómo produce asistencias: asiste el 7.1% de las canastas de sus compañeros en pista × 15.6 canastas de compañeros esperadas (su equipo 40.3 por 48' contra esta defensa).
- ➖ Defensa: el rival concede -2% de asistencias por minuto a aleros/ala-pívots (defensa media); ajuste aplicado -2%.
- ➖ Ritmo del partido: -0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 4 (1 de 1 a favor).
- ➖ Últimos 10: la habría pasado 6 de 10.

- Asistencias **1.2** (por componentes 1.1 · por tasa por minuto y defensa rival 1.2): asiste el 7.1% de las canastas de sus compañeros en pista × 15.6 canastas de compañeros esperadas (su equipo 40.3 por 48' contra esta defensa).

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 24.6 | 21.4 | 23.8 | 21.8 | 26.0 |
| Asistencias | 0.8 | 0.9 | 1.2 | 1.1 | 4.0 |
| % de las canastas de compañeros que asiste | 4.5% | 5.7% | 6.7% | 6.1% | 18.9% |
| Pérdidas por jugada | 9.3% | 8.3% | 10.5% | 9.0% | 7.1% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +4%, vs defensa media -4%, vs defensa débil +0%; rebotes: vs defensa fuerte -7%, vs defensa media -5%, vs defensa débil +10%; asistencias: vs defensa fuerte -3%, vs defensa media +11%, vs defensa débil -6%; triples: vs defensa fuerte -10%, vs defensa media +18%, vs defensa débil -2%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 34% | 33% | 35% | 35% |
| bajo el aro | 34% | 65% | 67% | 69% |
| pintura | 13% | 45% | 45% | 46% |
| triple de esquina | 12% | 37% | 38% | 36% |
| media distancia | 7% | 38% | 41% | 41% |

#### Devin Booker (bases/escoltas) vs Dallas Mavericks

- Minutos esperados: **36.0** (± 4.2); 90 partidos en la base.
- Mark Williams ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Su prop más probable hoy: **Devin Booker: más de 0.5 robos** (65%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Dallas Mavericks contra bases/escoltas en robos: +8% respecto a la media; ajuste por su historial contra defensas similares: -7%.

**¿Por qué 1.2 robos?** (línea 0.5; 36.0 minutos esperados)

En corto:

- La pasó en 11 de 17 esta temporada (falló con 0, 0, 0, 0)
- Con 32+ minutos (hoy se esperan 36): 8 de 12 en sus últimos 15
- Contra las ~10 mejores defensas en robos a bases/escoltas: 5 de 14 (últimos 40 partidos)
- Contra defensas débiles como la de hoy y con 32+ minutos: 8 de 15, con 0.8 de media (últimos 60 partidos)
- El rival es #8 de 30 en robos que concede a bases/escoltas por minuto (#1 = el que más concede; +8% frente a la media)
- Oportunidades de robo (últimos 10): el rival perdió 10.5 balones por partido con él en pista y robó el 13%
- El rival es #14 de 30 en balones que pierde (#1 = el que más; 14.1 por partido)
- Minutos: 36 esperados (titular, ±4)

Razonamiento (5 factores a favor, 0 en contra):

- ✅ Minutos: 36.0 esperados (titular, ±4.2).
- ✅ Forma: 1.2 en sus últimos 5, 1.2 esta temporada (17 partidos), 0.7 la temporada pasada (línea 0.5).
- ➖ Cómo produce robos: roba el 10.4% de las pérdidas del rival en pista × 15.6 pérdidas esperadas del rival.
- ✅ Defensa: el rival concede +8% de robos por minuto a bases/escoltas (defensa débil); ajuste aplicado +8%.
- ➖ Ritmo del partido: -0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 0, 2, 2 (2 de 3 a favor).
- ✅ Últimos 10: la habría pasado 8 de 10.
- ⚠️ Mark Williams ya no jugó en sus últimos partidos: la baja ya está en sus minutos.

- Robos **1.2** (por componentes 1.2 · por tasa por minuto y defensa rival 1.2): roba el 10.4% de las pérdidas del rival en pista × 15.6 pérdidas esperadas del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 37.2 | 34.6 | 34.5 | 33.0 | 35.7 |
| Robos | 1.2 | 1.4 | 1.2 | 0.7 | 1.3 |
| % de las pérdidas del rival que roba | 10.7% | 13.3% | 10.9% | 6.9% | 10.5% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -8%, vs defensa media +8%, vs defensa débil +3%; rebotes: vs defensa fuerte -7%, vs defensa media -4%, vs defensa débil +16%; asistencias: vs defensa fuerte -12%, vs defensa media +5%, vs defensa débil +8%; triples: vs defensa fuerte -5%, vs defensa media -8%, vs defensa débil +10%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 29% | 33% | 35% | 34% |
| media distancia | 28% | 46% | 41% | 42% |
| pintura | 27% | 48% | 45% | 46% |
| bajo el aro | 14% | 68% | 67% | 69% |
| triple de esquina | 2% | 33% | 38% | 36% |

#### Jalen Green (bases/escoltas) vs Dallas Mavericks

- Minutos esperados: **29.7** (± 5.9); 55 partidos en la base.
- Mark Williams ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Su prop más probable hoy: **Jalen Green: más de 0.5 robos** (65%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Dallas Mavericks contra bases/escoltas en robos: +8% respecto a la media; ajuste por su historial contra defensas similares: -2%.

**¿Por qué 1.2 robos?** (línea 0.5; 29.7 minutos esperados)

En corto:

- La pasó en 10 de 17 esta temporada (falló con 0, 0, 0, 0)
- Con 26+ minutos (hoy se esperan 30): 6 de 8 en sus últimos 15
- Contra las ~10 mejores defensas en robos a bases/escoltas: 8 de 14 (últimos 40 partidos)
- Contra defensas débiles como la de hoy y con 26+ minutos: 9 de 11, con 1.4 de media (últimos 60 partidos)
- El rival es #8 de 30 en robos que concede a bases/escoltas por minuto (#1 = el que más concede; +8% frente a la media)
- Oportunidades de robo (últimos 10): el rival perdió 8.2 balones por partido con él en pista y robó el 13%
- El rival es #14 de 30 en balones que pierde (#1 = el que más; 14.1 por partido)
- Minutos: 30 esperados (titular, ±6)

Razonamiento (4 factores a favor, 1 en contra):

- ✅ Minutos: 29.7 esperados (titular, ±5.9).
- ✅ Forma: 1.4 en sus últimos 5, 0.9 esta temporada (17 partidos), 1.2 la temporada pasada (línea 0.5).
- ➖ Cómo produce robos: roba el 12.5% de las pérdidas del rival en pista × 15.6 pérdidas esperadas del rival.
- ✅ Defensa: el rival concede +8% de robos por minuto a bases/escoltas (defensa débil); ajuste aplicado +8%.
- ➖ Ritmo del partido: -0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ❌ Contra este rival: 0, 0 (0 de 2 a favor).
- ✅ Últimos 10: la habría pasado 7 de 10.
- ⚠️ Mark Williams ya no jugó en sus últimos partidos: la baja ya está en sus minutos.

- Robos **1.2** (por componentes 1.2 · por tasa por minuto y defensa rival 1.1): roba el 12.5% de las pérdidas del rival en pista × 15.6 pérdidas esperadas del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 30.8 | 27.5 | 27.9 | 27.9 | 12.0 |
| Robos | 1.4 | 1.1 | 0.9 | 1.2 | 0.0 |
| % de las pérdidas del rival que roba | 14.6% | 13.4% | 11.7% | 13.6% | 0.0% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -10%, vs defensa media -13%, vs defensa débil +23%; rebotes: vs defensa fuerte -3%, vs defensa media +3%, vs defensa débil +1%; asistencias: vs defensa fuerte -1%, vs defensa media +10%, vs defensa débil -9%; triples: vs defensa fuerte -14%, vs defensa media -14%, vs defensa débil +28%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 31% | 29% | 35% | 34% |
| bajo el aro | 26% | 65% | 67% | 69% |
| pintura | 17% | 40% | 45% | 46% |
| media distancia | 16% | 42% | 41% | 42% |
| triple de esquina | 9% | 40% | 38% | 36% |

#### P.J. Washington (aleros/ala-pívots) vs Phoenix Suns

- Minutos esperados: **26.3** (± 5.3); 72 partidos en la base.
- Su prop más probable hoy: **P.J. Washington: menos de 1.5 asistencias** (63%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Phoenix Suns contra aleros/ala-pívots en asistencias: -2% respecto a la media; ajuste por su historial contra defensas similares: -2%.

**¿Por qué 1.2 asistencias?** (línea 1.5; 26.3 minutos esperados)

En corto:

- La pasó en 10 de 16 esta temporada (falló con 2, 4, 3, 2)
- Con 22+ minutos (hoy se esperan 26): 9 de 14 en sus últimos 15
- Contra las ~10 mejores defensas en asistencias a aleros/ala-pívots: 8 de 17 (últimos 40 partidos)
- Contra defensas medias como la de hoy y con 22+ minutos: 9 de 16, con 1.5 de media (últimos 60 partidos)
- El rival es #17 de 30 en asistencias que concede a aleros/ala-pívots por minuto (#1 = el que más concede; -2% frente a la media)
- Asistencias esperadas: 1.3 por partido si sus compañeros metieran lo normal (tiene 1.3; con él en pista metieron el 98% de lo esperado por tipo de tiro, últimos 10); ajuste aplicado +1.0%
- Oportunidades: asiste el 7% de las canastas de sus compañeros con él en pista
- Minutos: 26 esperados (titular, ±5)

Razonamiento (4 factores a favor, 0 en contra):

- ✅ Minutos: 26.3 esperados (titular, ±5.3).
- ✅ Forma: 1.4 en sus últimos 5, 1.2 esta temporada (16 partidos), 1.8 la temporada pasada (línea 1.5).
- ➖ Cómo produce asistencias: asiste el 6.7% de las canastas de sus compañeros en pista × 17.9 canastas de compañeros esperadas (su equipo 40.3 por 48' contra esta defensa).
- ➖ Defensa: el rival concede -2% de asistencias por minuto a aleros/ala-pívots (defensa media); ajuste aplicado -2%.
- ➖ Ritmo del partido: -0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 1, 0 (2 de 2 a favor).
- ✅ Últimos 10: la habría pasado 7 de 10.

- Asistencias **1.2** (por componentes 1.2 · por tasa por minuto y defensa rival 1.2): asiste el 6.7% de las canastas de sus compañeros en pista × 17.9 canastas de compañeros esperadas (su equipo 40.3 por 48' contra esta defensa).

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 23.4 | 28.7 | 30.6 | 30.9 | 15.5 |
| Asistencias | 1.4 | 1.3 | 1.2 | 1.8 | 0.5 |
| % de las canastas de compañeros que asiste | 8.2% | 6.2% | 5.4% | 7.6% | 4.5% |
| Pérdidas por jugada | 10.1% | 9.7% | 10.7% | 11.3% | 11.0% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -7%, vs defensa media +5%, vs defensa débil +5%; rebotes: vs defensa fuerte -7%, vs defensa media -13%, vs defensa débil +18%; asistencias: vs defensa fuerte +21%, vs defensa media -12%, vs defensa débil -15%; triples: vs defensa fuerte -6%, vs defensa media +16%, vs defensa débil -9%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| pintura | 27% | 45% | 45% | 46% |
| triple frontal | 25% | 32% | 35% | 35% |
| bajo el aro | 25% | 63% | 67% | 69% |
| triple de esquina | 17% | 39% | 38% | 36% |
| media distancia | 5% | 36% | 41% | 41% |

## Los Angeles Lakers @ San Antonio Spurs

Diferencia esperada: San Antonio Spurs por 6.5.

Parte de lesiones: De'Aaron Fox (Day-To-Day); Dylan Harper (Out); Jayden Quaintance (Out); Tobias Harris (Out).

Ventajas del partido (los dos lados): puntos esperados frente a su media de los últimos 10, ajuste por la defensa rival y diferencia de estatura con los rivales de su posición.

| Equipo | Jugador | Puntos esperados | Su media (últ. 10) | Defensa rival en puntos | Rebotes esperados | Altura vs rival |
|---|---|---|---|---|---|---|
| LAL | Luka Doncic | 32.6 | 36.0 | -3% | 6.5 | +3.7" |
| LAL | Austin Reaves | 21.5 | 24.5 | -3% | 3.7 | +0.7" |
| LAL | Quentin Grimes | 13.7 | 14.5 | -4% | 4.1 | -0.3" |
| SA | Stephon Castle | 18.1 | 17.9 | +1% | 5.0 | +0.8" |
| SA | Devin Vassell | 13.0 | 12.0 | +0% | 3.8 | -0.2" |
| LAL | Walker Kessler | 14.1 | 13.8 | -3% | 10.9 | +1.8" |
| SA | Victor Wembanyama | 28.9 | 32.0 | +0% | 11.7 | +7.8" |
| SA | Julian Champagnie | 12.0 | 12.4 | -1% | 4.8 | -1.2" |
| SA | De'Aaron Fox | 14.0 | 9.9 | +1% | 3.0 | -2.2" |
| LAL | Jake LaRavia | 7.5 | 6.6 | -5% | 4.7 | -2.0" |

Picks seguros de titulares estables:

| Jugador | Pick seguro | Prob. | Cuota mínima | Esperado | Últ. 10 |
|---|---|---|---|---|---|
| Austin Reaves | **más de 21.5 pts+reb+ast** | **82%** | 1.22 | 29.4 | 10/10 |
| Austin Reaves | **más de 15.5 puntos** | **79%** | 1.26 | 21.5 | 10/10 |

Las 8 más probables (máximo 2 por jugador: las de un mismo jugador suelen ganar o perder juntas).

| Prop | Prob. final | Modelo | Casa | Esperado | Últ. 10 | Temporada | vs este rival | Cuota (implícita) |
|---|---|---|---|---|---|---|---|---|
| **Jake LaRavia: más de 0.5 robos** | **67%** | 69% | 63% | 1.2 ± 1.1 | 6/10 | 13/17 | 0, 1, 1, 0 | 1.50 (67%) |
| **De'Aaron Fox: menos de 1.5 triples** | **67%** | 69% | 64% | 1.0 ± 1.1 | 8/10 | 11/16 | 0, 0, 4 | 1.48 (68%) |
| **Victor Wembanyama: menos de 1.5 robos** | **66%** | 66% | 66% | 1.2 ± 1.1 | 8/10 | 13/18 | 2, 2, 1 | 1.41 (71%) |
| **Quentin Grimes: más de 2.5 rebotes** | **65%** | 71% | 56% | 4.1 ± 2.2 | 6/10 | 10/16 | 2, 2 | 1.65 (61%) |
| **Collin Sexton: más de 12.5 pts+reb+ast** ⚠️ suplente | **65%** | 74% | 52% | 16.6 ± 5.7 | 9/10 | 13/17 | 26, 24 | 1.81 (55%) |
| **Matisse Thybulle: más de 0.5 asistencias** | **65%** | 66% | 63% | 1.2 ± 1.1 | 5/10 | 11/18 | 2, 0, 1, 1, 0 | 1.47 (68%) |
| **Austin Reaves: más de 16.5 puntos** | **64%** | 74% | 52% | 21.5 ± 7.5 | 9/10 | 11/12 | 15 | 1.81 (55%) |
| **Austin Reaves: más de 23.5 pts+reb+ast** | **64%** | 75% | 51% | 29.4 ± 8.6 | 9/10 | 11/12 | 30 | 1.83 (55%) |

### Fichas de los jugadores destacados

#### Jake LaRavia (aleros/ala-pívots) vs San Antonio Spurs

- Minutos esperados: **28.8** (± 5.6); 107 partidos en la base.
- Su prop más probable hoy: **Jake LaRavia: más de 0.5 robos** (67%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de San Antonio Spurs contra aleros/ala-pívots en robos: -4% respecto a la media; ajuste por su historial contra defensas similares: +0%.

**¿Por qué 1.2 robos?** (línea 0.5; 28.8 minutos esperados)

En corto:

- La pasó en 13 de 17 esta temporada (falló con 0, 0, 0, 0)
- Con 25+ minutos (hoy se esperan 29): 9 de 10 en sus últimos 15
- Contra las ~10 mejores defensas en robos a aleros/ala-pívots: 7 de 9 (últimos 40 partidos)
- Contra defensas fuertes como la de hoy y con 25+ minutos: 4 de 6, con 1.7 de media (últimos 60 partidos)
- El rival es #20 de 30 en robos que concede a aleros/ala-pívots por minuto (#1 = el que más concede; -4% frente a la media)
- Oportunidades de robo (últimos 10): el rival perdió 9.9 balones por partido con él en pista y robó el 9%
- El rival es #26 de 30 en balones que pierde (#1 = el que más; 12.6 por partido)
- El rival no tiene a Dylan Harper (0.9 robos por partido)
- Minutos: 29 esperados (titular, ±6)

Razonamiento (2 factores a favor, 1 en contra):

- ✅ Minutos: 28.8 esperados (titular, ±5.6).
- ✅ Forma: 1.2 en sus últimos 5, 1.2 esta temporada (17 partidos), 1.2 la temporada pasada (línea 0.5).
- ➖ Cómo produce robos: roba el 12.6% de las pérdidas del rival en pista × 13.4 pérdidas esperadas del rival.
- ❌ Defensa: el rival concede -4% de robos por minuto a aleros/ala-pívots (defensa fuerte); ajuste aplicado -4%.
- ➖ Ritmo del partido: +0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ➖ Contra este rival: 0, 1, 1, 0 (2 de 4 a favor).
- ➖ Últimos 10: la habría pasado 6 de 10.

- Robos **1.2** (por componentes 1.0 · por tasa por minuto y defensa rival 1.2): roba el 12.6% de las pérdidas del rival en pista × 13.4 pérdidas esperadas del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 29.2 | 27.4 | 25.9 | 24.2 | 26.0 |
| Robos | 1.2 | 0.9 | 1.2 | 1.2 | 0.5 |
| % de las pérdidas del rival que roba | 10.3% | 9.1% | 12.7% | 16.4% | 5.9% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -3%, vs defensa media +7%, vs defensa débil -1%; rebotes: vs defensa fuerte -8%, vs defensa media -1%, vs defensa débil +8%; asistencias: vs defensa fuerte +12%, vs defensa media -21%, vs defensa débil +8%; triples: vs defensa fuerte -7%, vs defensa media +39%, vs defensa débil -26%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 32% | 68% | 67% | 62% |
| triple de esquina | 23% | 36% | 38% | 35% |
| triple frontal | 22% | 34% | 35% | 36% |
| pintura | 21% | 42% | 45% | 42% |
| media distancia | 2% | 34% | 41% | 41% |

#### De'Aaron Fox (bases/escoltas) vs Los Angeles Lakers

- Minutos esperados: **29.0** (± 5.3); 113 partidos en la base.
- en el parte de lesiones: day-to-day
- sin Dylan Harper (13 partidos): 32.6 min vs 31.1 con él; pts +7%/min, reb -7%/min
- Su prop más probable hoy: **De'Aaron Fox: menos de 1.5 triples** (67%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Los Angeles Lakers contra bases/escoltas en triples: -0% respecto a la media; ajuste por su historial contra defensas similares: +6%.

**¿Por qué 1.0 triples?** (línea 1.5; 29.0 minutos esperados)

En corto:

- La pasó en 11 de 16 esta temporada (falló con 2, 2, 2, 2)
- Con 25+ minutos (hoy se esperan 29): 7 de 12 en sus últimos 15
- Contra las ~10 mejores defensas en triples a bases/escoltas: 13 de 23 (últimos 40 partidos)
- Contra defensas medias como la de hoy y con 25+ minutos: 4 de 12, con 1.9 de media (últimos 60 partidos)
- El rival es #12 de 30 en triples que concede a bases/escoltas por minuto (#1 = el que más concede; +1% frente a la media)
- Su zona principal es triple frontal (27% de sus tiros, 31% de acierto); el rival es #23 de 30 en acierto que deja ahí (34%, liga 35%)
- Cómo tira (últimos 15): penetración 37% (61% de acierto), creado 28% (31% de acierto), recibe y tira 27% (32% de acierto); en penetración el rival es #25 de 30 en lo que deja (#1 = el que más; 1.04 puntos por tiro frente a 1.08 de media)
- Oportunidades: 3.6 triples intentados esperados al 32%
- Minutos: 29 esperados (titular, ±5)

Razonamiento (5 factores a favor, 0 en contra):

- ✅ Minutos: 29.0 esperados (titular, ±5.3).
- ✅ Forma: 0.4 en sus últimos 5, 0.8 esta temporada (16 partidos), 1.4 la temporada pasada (línea 1.5).
- ➖ Cómo produce triples: 3.6 triples intentados (su ritmo 4.6 por 36'; el rival concede +2% de triples en su reparto) × 32% esperado.
- ➖ Defensa: el rival concede +1% de triples por minuto a bases/escoltas (defensa media); ajuste aplicado -0%; en su zona principal (triple) el rival concede 34% (liga 35%).
- ✅ Altura: mide 6'3", 2.2 pulgadas menos que los bases/escoltas del rival (-0.8% en esta estadística).
- ➖ Ritmo del partido: +0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 0, 0, 4 (2 de 3 a favor).
- ✅ Últimos 10: la habría pasado 8 de 10.
- ⚠️ en el parte de lesiones: day-to-day.
- ⚠️ sin Dylan Harper (13 partidos): 32.6 min vs 31.1 con él; pts +7%/min, reb -7%/min.

- ⚠️ Alertas: en el parte de lesiones.
- Triples **1.0** (por componentes 1.1 · por tasa por minuto y defensa rival 1.0): 3.6 triples intentados (su ritmo 4.6 por 36'; el rival concede +2% de triples en su reparto) × 32% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 28.0 | 27.2 | 29.1 | 30.8 | 27.3 |
| Triples anotados | 0.4 | 0.6 | 0.8 | 1.7 | 1.3 |
| Triples intentados | 3.8 | 3.0 | 3.1 | 5.2 | 5.0 |
| % triples | 10.5% | 20.0% | 26.5% | 32.4% | 26.7% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -9%, vs defensa media +10%, vs defensa débil +4%; rebotes: vs defensa fuerte -9%, vs defensa media +5%, vs defensa débil +10%; asistencias: vs defensa fuerte -5%, vs defensa media +4%, vs defensa débil +6%; triples: vs defensa fuerte -7%, vs defensa media +10%, vs defensa débil +1%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| pintura | 30% | 50% | 45% | 44% |
| triple frontal | 27% | 31% | 35% | 34% |
| bajo el aro | 22% | 68% | 67% | 72% |
| media distancia | 11% | 47% | 41% | 42% |
| triple de esquina | 9% | 36% | 38% | 38% |

#### Victor Wembanyama (aleros/ala-pívots) vs Los Angeles Lakers

- Minutos esperados: **31.7** (± 4.2); 107 partidos en la base.
- Dylan Harper ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Su prop más probable hoy: **Victor Wembanyama: menos de 1.5 robos** (66%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Los Angeles Lakers contra aleros/ala-pívots en robos: +5% respecto a la media; ajuste por su historial contra defensas similares: -3%.

**¿Por qué 1.2 robos?** (línea 1.5; 31.7 minutos esperados)

En corto:

- La pasó en 13 de 18 esta temporada (falló con 4, 2, 2, 2)
- Con 28+ minutos (hoy se esperan 32): 5 de 9 en sus últimos 15
- Contra las ~10 mejores defensas en robos a aleros/ala-pívots: 10 de 16 (últimos 40 partidos)
- Contra defensas débiles como la de hoy y con 28+ minutos: 9 de 13, con 1.1 de media (últimos 60 partidos)
- El rival es #9 de 30 en robos que concede a aleros/ala-pívots por minuto (#1 = el que más concede; +5% frente a la media)
- Oportunidades de robo (últimos 10): el rival perdió 8.7 balones por partido con él en pista y robó el 14%
- El rival es #10 de 30 en balones que pierde (#1 = el que más; 14.5 por partido)
- Minutos: 32 esperados (titular, ±4)

Razonamiento (2 factores a favor, 3 en contra):

- ✅ Minutos: 31.7 esperados (titular, ±4.2).
- ❌ Forma: 1.6 en sus últimos 5, 1.2 esta temporada (18 partidos), 1.1 la temporada pasada (línea 1.5).
- ➖ Cómo produce robos: roba el 13.1% de las pérdidas del rival en pista × 13.1 pérdidas esperadas del rival.
- ❌ Defensa: el rival concede +5% de robos por minuto a aleros/ala-pívots (defensa débil); ajuste aplicado +5%.
- ➖ Ritmo del partido: +0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ❌ Contra este rival: 2, 2, 1 (1 de 3 a favor).
- ✅ Últimos 10: la habría pasado 8 de 10.
- ⚠️ Dylan Harper ya no jugó en sus últimos partidos: la baja ya está en sus minutos.

- Robos **1.2** (por componentes 1.1 · por tasa por minuto y defensa rival 1.2): roba el 13.1% de las pérdidas del rival en pista × 13.1 pérdidas esperadas del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 33.8 | 29.7 | 30.6 | 29.9 | 28.3 |
| Robos | 1.6 | 1.2 | 1.2 | 1.0 | 1.7 |
| % de las pérdidas del rival que roba | 16.3% | 13.8% | 13.3% | 12.3% | 18.5% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -7%, vs defensa media +1%, vs defensa débil +15%; rebotes: vs defensa fuerte -4%, vs defensa media +2%, vs defensa débil +2%; asistencias: vs defensa fuerte -16%, vs defensa media -0%, vs defensa débil +29%; triples: vs defensa fuerte -14%, vs defensa media +1%, vs defensa débil +14%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 37% | 75% | 67% | 72% |
| triple frontal | 30% | 33% | 35% | 34% |
| media distancia | 16% | 37% | 41% | 42% |
| pintura | 15% | 48% | 45% | 44% |
| triple de esquina | 2% | 40% | 38% | 38% |

#### Quentin Grimes (bases/escoltas) vs San Antonio Spurs

- Minutos esperados: **32.6** (± 5.7); 103 partidos en la base.
- Su prop más probable hoy: **Quentin Grimes: más de 2.5 rebotes** (65%). Con 80% de probabilidad: más de 1.5 / menos de 6.5.
- Defensa de San Antonio Spurs contra bases/escoltas en rebotes: +3% respecto a la media; ajuste por su historial contra defensas similares: +3%.

**¿Por qué 4.1 rebotes?** (línea 2.5; 32.6 minutos esperados)

En corto:

- La pasó en 10 de 16 esta temporada (falló con 1, 0, 1, 1)
- Con 29+ minutos (hoy se esperan 33): 7 de 8 en sus últimos 15
- Contra las ~10 mejores defensas en rebotes a bases/escoltas: 10 de 19 (últimos 40 partidos)
- Contra defensas débiles como la de hoy y con 29+ minutos: 7 de 7, con 5.3 de media (últimos 60 partidos)
- El rival es #10 de 30 en rebotes que concede a bases/escoltas por minuto (#1 = el que más concede; +3% frente a la media)
- El rival es #20 de 30 en rebotes que concede en total (#1 = el que más)
- El rival es #26 de 30 en rebotes ofensivos que concede en total (#1 = el que más)
- Rebotes disponibles con él en pista (últimos 10): 30.8 tiros fallados del rival y 27.9 de su equipo por partido; se queda el 8% y el 4%; el rival falla 49.5 tiros por partido (#6 de 30, #1 = el que más falla)
- El rival no tiene a Dylan Harper (5.5 rebotes por partido)
- Minutos: 33 esperados (titular, ±6)

Razonamiento (3 factores a favor, 1 en contra):

- ✅ Minutos: 32.6 esperados (titular, ±5.7).
- ✅ Forma: 5.4 en sus últimos 5, 3.4 esta temporada (16 partidos), 3.4 la temporada pasada (línea 2.5).
- ➖ Cómo produce rebotes: defensivos 2.9 = captura el 9.4% de los fallos del rival en pista × 45.9 fallos esperados del rival (liga 47.0) × 68% del partido; ofensivos 0.9 = 3.0% de los fallos de su equipo × 44.9.
- ✅ Defensa: el rival concede +3% de rebotes por minuto a bases/escoltas (defensa débil); ajuste aplicado +3%.
- ➖ Ritmo del partido: +0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ❌ Contra este rival: 2, 2 (0 de 2 a favor).
- ➖ Últimos 10: la habría pasado 6 de 10.

- Rebotes **4.1** (por componentes 3.8 · por tasa por minuto y defensa rival 4.2): defensivos 2.9 = captura el 9.4% de los fallos del rival en pista × 45.9 fallos esperados del rival (liga 47.0) × 68% del partido; ofensivos 0.9 = 3.0% de los fallos de su equipo × 44.9.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 35.8 | 30.5 | 29.1 | 28.5 | 22.5 |
| Rebotes | 5.4 | 3.4 | 3.4 | 3.5 | 2.0 |
| % de los fallos del rival que captura | 10.1% | 7.8% | 8.9% | 10.4% | 9.3% |
| % de los fallos de su equipo que captura | 5.3% | 3.6% | 3.1% | 2.0% | 0.0% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -2%, vs defensa media +1%, vs defensa débil +2%; rebotes: vs defensa fuerte -5%, vs defensa media -1%, vs defensa débil +8%; asistencias: vs defensa fuerte -9%, vs defensa media -11%, vs defensa débil +22%; triples: vs defensa fuerte +14%, vs defensa media -20%, vs defensa débil +9%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 39% | 34% | 35% | 36% |
| bajo el aro | 29% | 69% | 67% | 62% |
| pintura | 12% | 40% | 45% | 42% |
| triple de esquina | 12% | 39% | 38% | 35% |
| media distancia | 8% | 32% | 41% | 41% |

#### Collin Sexton (bases/escoltas) vs San Antonio Spurs

- Minutos esperados: **20.9** (± 4.1); 85 partidos en la base.
- Su prop más probable hoy: **Collin Sexton: más de 12.5 pts+reb+ast** (65%). Con 80% de probabilidad: más de 11.5 / menos de 21.5.
- Defensa de San Antonio Spurs contra bases/escoltas en pts+reb+ast: -3% respecto a la media; ajuste por su historial contra defensas similares: -0%.

**¿Por qué 16.6 pts+reb+ast?** (línea 12.5; 20.9 minutos esperados)

En corto:

- La pasó en 13 de 17 esta temporada (falló con 1, 12, 3, 8)
- Con 17+ minutos (hoy se esperan 21): 9 de 9 en sus últimos 15
- Contra las ~10 mejores defensas en puntos a bases/escoltas: 10 de 12 (últimos 40 partidos)
- Contra defensas fuertes como la de hoy y con 17+ minutos: 15 de 16, con 21.4 de media (últimos 60 partidos)
- El rival es #26 de 30 en puntos que concede a bases/escoltas por minuto (#1 = el que más concede; -4% frente a la media)
- Su zona principal es triple frontal (31% de sus tiros, 35% de acierto); el rival es #10 de 30 en acierto que deja ahí (36%, liga 35%)
- Su segunda zona es bajo el aro (29% de sus tiros, 66% de acierto); el rival es #29 de 30 en acierto que deja ahí (62%, liga 67%)
- El rival es #28 de 30 en tiros libres que concede a bases/escoltas (#1 = el que más; -12% frente a la media)
- Puntería: en sus últimos 10 metió el 89% de las canastas esperadas por sus tipos de tiro (viene frío: suele volver a su nivel)
- Cómo tira (últimos 15): penetración 43% (50% de acierto), recibe y tira 27% (31% de acierto), creado 22% (36% de acierto); en penetración el rival es #26 de 30 en lo que deja (#1 = el que más; 1.02 puntos por tiro frente a 1.08 de media)
- Oportunidades: 9.5 tiros de campo y 2.8 libres esperados (1.03 puntos por tiro)
- Transición: el rival concede 12.4 puntos por partido al contraataque (#26 de 30, #1 = el que más); él anota 2.0 así por partido (ajuste aplicado -2.5%)
- El rival no tiene a Dylan Harper (28.9 pts+reb+ast por partido)
- Minutos: 21 esperados (suplente, ±4)

Razonamiento (4 factores a favor, 2 en contra):

- ❌ Minutos: 20.9 esperados (suplente, ±4.1).
- ✅ Forma: 16.4 en sus últimos 5, 15.2 esta temporada (17 partidos), 20.6 la temporada pasada (línea 12.5).
- ➖ Cómo produce puntos: 9.5 tiros de campo (su ritmo 16.5 por 36'; el rival concede +2% de tiros) × 1.03 puntos por tiro [triple frontal 31% de sus tiros al 35% (rival concede 36%, liga 35%); bajo el aro 29% de sus tiros al 66% (rival concede 62%, liga 67%); pintura 25% de sus tiros al 44% (rival concede 42%, liga 45%)] + 2.8 tiros libres × 77%.
- ➖ Cómo produce rebotes: defensivos 1.4 = captura el 6.9% de los fallos del rival en pista × 45.9 fallos esperados del rival (liga 47.0) × 44% del partido; ofensivos 0.6 = 2.8% de los fallos de su equipo × 44.9.
- ➖ Cómo produce asistencias: asiste el 18.2% de las canastas de sus compañeros en pista × 13.1 canastas de compañeros esperadas (su equipo 39.9 por 48' contra esta defensa).
- ❌ Defensa: el rival concede -4% de puntos por minuto a bases/escoltas (defensa fuerte); ajuste aplicado -3%; en su zona principal (triple) el rival concede 36% (liga 35%).
- ➖ Ritmo del partido: +0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 26, 24 (2 de 2 a favor).
- ✅ Últimos 10: la habría pasado 9 de 10.
- ✅ Bajas del rival: sin Dylan Harper (titular); +1.1% en esta estadística.

- ⚠️ Alertas: suplente.
- Puntos **11.8** (por componentes 12.1 · por tasa por minuto y defensa rival 11.8): 9.5 tiros de campo (su ritmo 16.5 por 36'; el rival concede +2% de tiros) × 1.03 puntos por tiro [triple frontal 31% de sus tiros al 35% (rival concede 36%, liga 35%); bajo el aro 29% de sus tiros al 66% (rival concede 62%, liga 67%); pintura 25% de sus tiros al 44% (rival concede 42%, liga 45%)] + 2.8 tiros libres × 77%.
- Rebotes **2.0** (por componentes 1.9 · por tasa por minuto y defensa rival 2.0): defensivos 1.4 = captura el 6.9% de los fallos del rival en pista × 45.9 fallos esperados del rival (liga 47.0) × 44% del partido; ofensivos 0.6 = 2.8% de los fallos de su equipo × 44.9.
- Asistencias **2.8** (por componentes 2.4 · por tasa por minuto y defensa rival 2.6): asiste el 18.2% de las canastas de sus compañeros en pista × 13.1 canastas de compañeros esperadas (su equipo 39.9 por 48' contra esta defensa).

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 22.0 | 20.1 | 19.0 | 23.7 | 22.5 |
| Puntos | 12.0 | 11.5 | 10.8 | 15.4 | 20.5 |
| Tiros de campo intentados | 9.6 | 8.8 | 8.6 | 10.9 | 11.5 |
| % tiros de campo | 41.7% | 42.0% | 42.9% | 48.5% | 65.2% |
| Triples intentados | 4.2 | 3.4 | 3.6 | 4.1 | 5.5 |
| % triples | 28.6% | 29.4% | 27.9% | 40.1% | 72.7% |
| Tiros libres intentados | 3.6 | 4.0 | 3.2 | 3.8 | 1.5 |
| % tiros libres | 77.8% | 77.5% | 74.1% | 85.5% | 100.0% |
| Jugadas que usa por 36 min | 21.2 | 21.6 | 21.7 | 22.2 | 21.1 |
| Rebotes | 1.4 | 1.5 | 1.7 | 2.3 | 1.5 |
| % de los fallos del rival que captura | 4.7% | 4.8% | 6.2% | 6.9% | 6.5% |
| % de los fallos de su equipo que captura | 1.6% | 2.4% | 2.8% | 2.5% | 0.0% |
| Asistencias | 3.0 | 2.8 | 2.7 | 3.3 | 3.0 |
| % de las canastas de compañeros que asiste | 19.4% | 18.7% | 18.7% | 18.8% | 18.9% |
| Pérdidas por jugada | 13.9% | 12.4% | 12.3% | 14.2% | 7.6% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -2%, vs defensa media -3%, vs defensa débil +4%; rebotes: vs defensa fuerte -11%, vs defensa media +2%, vs defensa débil +7%; asistencias: vs defensa fuerte -23%, vs defensa media +12%, vs defensa débil +14%; triples: vs defensa fuerte +4%, vs defensa media -23%, vs defensa débil +19%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 31% | 35% | 35% | 36% |
| bajo el aro | 29% | 66% | 67% | 62% |
| pintura | 25% | 44% | 45% | 42% |
| triple de esquina | 8% | 40% | 38% | 35% |
| media distancia | 7% | 40% | 41% | 41% |

## Denver Nuggets @ Utah Jazz

Diferencia esperada: Denver Nuggets por 9.5 — algo desigual: titulares hasta -1.5% de minutos.

Parte de lesiones: Jusuf Nurkic (Out); Lauri Markkanen (Out); Mo Bamba (Day-To-Day); Jaren Jackson Jr. (Out); Jaxson Hayes (Day-To-Day).

Ventajas del partido (los dos lados): puntos esperados frente a su media de los últimos 10, ajuste por la defensa rival y diferencia de estatura con los rivales de su posición.

| Equipo | Jugador | Puntos esperados | Su media (últ. 10) | Defensa rival en puntos | Rebotes esperados | Altura vs rival |
|---|---|---|---|---|---|---|
| DEN | Jamal Murray | 26.6 | 24.9 | +6% | 4.8 | -1.8" |
| DEN | Nikola Jokic | 25.8 | 26.2 | +4% | 11.8 | -0.7" |
| UTAH | Keyonte George | 22.9 | 19.1 | -1% | 3.3 | -0.6" |
| DEN | Christian Braun | 15.3 | 13.0 | +6% | 4.5 | +0.2" |
| DEN | Cameron Johnson | 14.9 | 14.2 | +3% | 4.2 | +0.8" |
| UTAH | Ace Bailey | 14.3 | 14.1 | -1% | 5.2 | +4.4" |
| UTAH | Darryn Peterson | 15.8 | 18.1 | -1% | 4.1 | +0.4" |
| DEN | Aaron Gordon | 13.1 | 11.3 | +3% | 5.3 | +0.8" |
| UTAH | Svi Mykhailiuk | 11.1 | 9.3 | -1% | 3.3 | +2.4" |
| UTAH | Mo Bamba | 10.2 | 8.5 | -1% | 8.9 | +1.0" |

Las 8 más probables (máximo 2 por jugador: las de un mismo jugador suelen ganar o perder juntas).

| Prop | Prob. final | Modelo | Casa | Esperado | Últ. 10 | Temporada | vs este rival | Cuota (implícita) |
|---|---|---|---|---|---|---|---|---|
| **DeMar DeRozan: menos de 0.5 triples** ⚠️ suplente | **70%** | 70% | 70% | 0.4 ± 0.6 | 9/10 | 13/15 | 1, 1, 1, 0 | 1.32 (75%) |
| **Cameron Johnson: más de 0.5 robos** | **70%** | 73% | 66% | 1.2 ± 1.1 | 9/10 | 11/13 | 2, 1, 0 | 1.44 (69%) |
| **Josh Green: menos de 1.5 triples** | **66%** | 68% | 63% | 1.1 ± 1.1 | 6/10 | 13/17 | 1 | 1.49 (67%) |
| **Josh Green: menos de 1.5 asistencias** | **65%** | 65% | 66% | 1.3 ± 1.2 | 8/10 | 14/17 | 0 | 1.42 (70%) |
| **Darryn Peterson: más de 0.5 robos** | **65%** | 66% | 63% | 1.0 ± 1.0 | 8/10 | 14/19 | - | 1.50 (67%) |
| **Jamal Murray: más de 0.5 robos** | **64%** | 66% | 62% | 1.3 ± 1.3 | 5/10 | 10/16 | 1, 0, 2, 1 | 1.50 (66%) |
| **Aaron Gordon: menos de 1.5 triples** | **64%** | 66% | 61% | 1.2 ± 1.1 | 9/10 | 12/16 | 1, 0 | 1.54 (65%) |
| **Jamal Murray: más de 1.5 robos+tapones** | **63%** | 67% | 57% | 2.3 ± 1.6 | 7/10 | 12/16 | 3, 0, 2, 1 | 1.67 (60%) |

### Fichas de los jugadores destacados

#### DeMar DeRozan (bases/escoltas) vs Utah Jazz

- Minutos esperados: **19.7** (± 3.3); 92 partidos en la base.
- partido desigual (favorito por 9.5): los suplentes suelen jugar +1% de minutos si se rompe
- Su prop más probable hoy: **DeMar DeRozan: menos de 0.5 triples** (70%). Con 80% de probabilidad: más de - / menos de 1.5.
- Defensa de Utah Jazz contra bases/escoltas en triples: +5% respecto a la media; ajuste por su historial contra defensas similares: -8%.

**¿Por qué 0.4 triples?** (línea 0.5; 19.7 minutos esperados)

En corto:

- La pasó en 13 de 15 esta temporada (falló con 1, 2)
- Con 16+ minutos (hoy se esperan 20): 12 de 14 en sus últimos 15
- Contra las ~10 mejores defensas en triples a bases/escoltas: 10 de 11 (últimos 40 partidos)
- Contra defensas débiles como la de hoy y con 16+ minutos: 14 de 19, con 0.3 de media (últimos 60 partidos)
- El rival es #1 de 30 en triples que concede a bases/escoltas por minuto (#1 = el que más concede; +11% frente a la media)
- Su zona principal es triple frontal (8% de sus tiros, 30% de acierto); el rival es #3 de 30 en acierto que deja ahí (36%, liga 35%)
- Cómo tira (últimos 15): creado 38% (36% de acierto), recibe y tira 26% (30% de acierto), penetración 19% (50% de acierto); en creado el rival es #9 de 30 en lo que deja (#1 = el que más; 0.96 puntos por tiro frente a 0.93 de media)
- Oportunidades: 1.6 triples intentados esperados al 31%
- Minutos: 20 esperados (suplente, ±3)

Razonamiento (2 factores a favor, 3 en contra):

- ❌ Minutos: 19.7 esperados (suplente, ±3.3).
- ✅ Forma: 0.2 en sus últimos 5, 0.2 esta temporada (15 partidos), 0.6 la temporada pasada (línea 0.5).
- ➖ Cómo produce triples: 1.6 triples intentados (su ritmo 2.7 por 36'; el rival concede +5% de triples en su reparto) × 31% esperado.
- ❌ Defensa: el rival concede +11% de triples por minuto a bases/escoltas (defensa débil); ajuste aplicado +5%; en su zona principal (triple) el rival concede 36% (liga 35%).
- ➖ Ritmo del partido: -0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ❌ Contra este rival: 1, 1, 1, 0 (1 de 4 a favor).
- ✅ Últimos 10: la habría pasado 9 de 10.
- ⚠️ partido desigual (favorito por 9.5): los suplentes suelen jugar +1% de minutos si se rompe.

- ⚠️ Alertas: suplente.
- Triples **0.4** (por componentes 0.5 · por tasa por minuto y defensa rival 0.3): 1.6 triples intentados (su ritmo 2.7 por 36'; el rival concede +5% de triples en su reparto) × 31% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 19.2 | 20.1 | 22.1 | 31.3 | 35.0 |
| Triples anotados | 0.2 | 0.1 | 0.2 | 0.6 | 0.8 |
| Triples intentados | 1.0 | 1.0 | 1.3 | 1.9 | 2.2 |
| % triples | 20.0% | 10.0% | 15.8% | 32.0% | 33.3% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +7%, vs defensa media -1%, vs defensa débil -7%; rebotes: vs defensa fuerte +5%, vs defensa media -11%, vs defensa débil +2%; asistencias: vs defensa fuerte -3%, vs defensa media -9%, vs defensa débil +12%; triples: vs defensa fuerte +10%, vs defensa media -13%, vs defensa débil +5%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| media distancia | 47% | 46% | 41% | 42% |
| pintura | 27% | 49% | 45% | 49% |
| bajo el aro | 11% | 73% | 67% | 71% |
| triple frontal | 8% | 30% | 35% | 36% |
| triple de esquina | 7% | 33% | 38% | 36% |

#### Cameron Johnson (aleros/ala-pívots) vs Utah Jazz

- Minutos esperados: **31.0** (± 3.4); 72 partidos en la base.
- partido desigual (favorito por 9.5): los titulares suelen jugar -1% de minutos si se rompe
- Su prop más probable hoy: **Cameron Johnson: más de 0.5 robos** (70%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Utah Jazz contra aleros/ala-pívots en robos: +7% respecto a la media; ajuste por su historial contra defensas similares: +5%.

**¿Por qué 1.2 robos?** (línea 0.5; 31.0 minutos esperados)

En corto:

- La pasó en 11 de 13 esta temporada (falló con 0, 0)
- Con 27+ minutos (hoy se esperan 31): 10 de 11 en sus últimos 15
- Contra las ~10 mejores defensas en robos a aleros/ala-pívots: 6 de 14 (últimos 40 partidos)
- Contra defensas débiles como la de hoy y con 27+ minutos: 11 de 15, con 1.2 de media (últimos 60 partidos)
- El rival es #7 de 30 en robos que concede a aleros/ala-pívots por minuto (#1 = el que más concede; +7% frente a la media)
- Oportunidades de robo (últimos 10): el rival perdió 9.1 balones por partido con él en pista y robó el 13%
- El rival es #3 de 30 en balones que pierde (#1 = el que más; 15.3 por partido)
- Minutos: 31 esperados (titular, ±3)

Razonamiento (5 factores a favor, 0 en contra):

- ✅ Minutos: 31.0 esperados (titular, ±3.4).
- ✅ Forma: 1.2 en sus últimos 5, 1.2 esta temporada (13 partidos), 0.8 la temporada pasada (línea 0.5).
- ➖ Cómo produce robos: roba el 12.4% de las pérdidas del rival en pista × 13.1 pérdidas esperadas del rival.
- ✅ Defensa: el rival concede +7% de robos por minuto a aleros/ala-pívots (defensa débil); ajuste aplicado +7%.
- ➖ Ritmo del partido: -0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 2, 1, 0 (2 de 3 a favor).
- ✅ Últimos 10: la habría pasado 9 de 10.
- ⚠️ partido desigual (favorito por 9.5): los titulares suelen jugar -1% de minutos si se rompe.

- Robos **1.2** (por componentes 1.1 · por tasa por minuto y defensa rival 1.3): roba el 12.4% de las pérdidas del rival en pista × 13.1 pérdidas esperadas del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 30.4 | 30.3 | 29.4 | 30.4 | 30.0 |
| Robos | 1.2 | 1.2 | 1.2 | 0.8 | 1.0 |
| % de las pérdidas del rival que roba | 11.3% | 13.2% | 13.0% | 10.5% | 15.0% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -9%, vs defensa media +6%, vs defensa débil +16%; rebotes: vs defensa fuerte +5%, vs defensa media -12%, vs defensa débil +6%; asistencias: vs defensa fuerte +7%, vs defensa media -16%, vs defensa débil +11%; triples: vs defensa fuerte -11%, vs defensa media +17%, vs defensa débil -1%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 35% | 37% | 35% | 36% |
| bajo el aro | 23% | 70% | 67% | 71% |
| triple de esquina | 20% | 42% | 38% | 36% |
| pintura | 13% | 43% | 45% | 49% |
| media distancia | 9% | 41% | 41% | 42% |

#### Josh Green (bases/escoltas) vs Denver Nuggets

- Minutos esperados: **22.2** (± 5.7); 77 partidos en la base.
- Jusuf Nurkic ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- sin Lauri Markkanen, la estrella de su equipo (11 partidos suyos sin él): más tiros y balón para él por minuto (puntos +1%, triples -1%, asistencias +4%)
- Lauri Markkanen ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Jaren Jackson Jr. ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- partido desigual (no favorito por 9.5): los suplentes suelen jugar +1% de minutos si se rompe
- Su prop más probable hoy: **Josh Green: menos de 1.5 triples** (66%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Denver Nuggets contra bases/escoltas en triples: -2% respecto a la media; ajuste por su historial contra defensas similares: +3%.

**¿Por qué 1.1 triples?** (línea 1.5; 22.2 minutos esperados)

En corto:

- La pasó en 13 de 17 esta temporada (falló con 2, 2, 2, 2)
- Con 18+ minutos (hoy se esperan 22): 7 de 10 en sus últimos 15
- Contra las ~10 mejores defensas en triples a bases/escoltas: 15 de 18 (últimos 40 partidos)
- Contra defensas medias como la de hoy y con 18+ minutos: 2 de 7, con 1.7 de media (últimos 60 partidos)
- El rival es #13 de 30 en triples que concede a bases/escoltas por minuto (#1 = el que más concede; -1% frente a la media)
- Su zona principal es triple de esquina (44% de sus tiros, 42% de acierto); el rival es #24 de 30 en acierto que deja ahí (37%, liga 38%)
- Su segunda zona es triple frontal (25% de sus tiros, 36% de acierto); el rival es #18 de 30 en acierto que deja ahí (35%, liga 35%)
- Cómo tira (últimos 15): recibe y tira 57% (38% de acierto), penetración 23% (50% de acierto), creado 17% (50% de acierto); en recibe y tira el rival es #5 de 30 en lo que deja (#1 = el que más; 1.13 puntos por tiro frente a 1.07 de media)
- Oportunidades: 3.0 triples intentados esperados al 38%
- Su equipo no tiene a Lauri Markkanen: más tiros y balón para él
- Minutos: 22 esperados (titular, ±6)

Razonamiento (3 factores a favor, 0 en contra):

- ✅ Minutos: 22.2 esperados (titular, ±5.7).
- ✅ Forma: 1.4 en sus últimos 5, 0.9 esta temporada (17 partidos), 1.0 la temporada pasada (línea 1.5).
- ➖ Cómo produce triples: 3.0 triples intentados (su ritmo 4.7 por 36'; el rival concede +2% de triples en su reparto) × 38% esperado.
- ➖ Defensa: el rival concede -1% de triples por minuto a bases/escoltas (defensa media); ajuste aplicado -2%; en su zona principal (esquina3) el rival concede 37% (liga 38%).
- ➖ Ritmo del partido: -0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 1 (1 de 1 a favor).
- ➖ Últimos 10: la habría pasado 6 de 10.
- ⚠️ Jusuf Nurkic ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ sin Lauri Markkanen, la estrella de su equipo (11 partidos suyos sin él): más tiros y balón para él por minuto (puntos +1%, triples -1%, asistencias +4%).
- ⚠️ Lauri Markkanen ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ Jaren Jackson Jr. ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ partido desigual (no favorito por 9.5): los suplentes suelen jugar +1% de minutos si se rompe.

- ⚠️ Alertas: sin Lauri Markkanen: más tiros para él.
- Triples **1.1** (por componentes 1.1 · por tasa por minuto y defensa rival 1.1): 3.0 triples intentados (su ritmo 4.7 por 36'; el rival concede +2% de triples en su reparto) × 38% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 22.4 | 22.5 | 20.1 | 15.4 | 13.0 |
| Triples anotados | 1.4 | 1.1 | 0.9 | 1.0 | 1.0 |
| Triples intentados | 2.4 | 2.7 | 2.3 | 2.3 | 2.0 |
| % triples | 58.3% | 40.7% | 38.5% | 41.4% | 50.0% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +2%, vs defensa media +10%, vs defensa débil -14%; rebotes: vs defensa fuerte +22%, vs defensa media -19%, vs defensa débil -7%; asistencias: vs defensa fuerte -30%, vs defensa media +13%, vs defensa débil +20%; triples: vs defensa fuerte +7%, vs defensa media -1%, vs defensa débil -8%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple de esquina | 44% | 42% | 38% | 37% |
| triple frontal | 25% | 36% | 35% | 35% |
| bajo el aro | 16% | 65% | 67% | 70% |
| pintura | 11% | 47% | 45% | 45% |
| media distancia | 4% | 41% | 41% | 40% |

#### Darryn Peterson (bases/escoltas) vs Denver Nuggets

- Minutos esperados: **28.7** (± 4.6); 19 partidos en la base.
- Jusuf Nurkic ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- sin Lauri Markkanen, la estrella de su equipo (11 partidos suyos sin él): más tiros y balón para él por minuto (puntos +2%, triples +5%, asistencias +1%)
- Lauri Markkanen ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Jaren Jackson Jr. ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- partido desigual (no favorito por 9.5): los titulares suelen jugar -1% de minutos si se rompe
- Su prop más probable hoy: **Darryn Peterson: más de 0.5 robos** (65%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Denver Nuggets contra bases/escoltas en robos: -7% respecto a la media; ajuste por su historial contra defensas similares: +1%.

**¿Por qué 1.0 robos?** (línea 0.5; 28.7 minutos esperados)

En corto:

- La pasó en 14 de 19 esta temporada (falló con 0, 0, 0, 0)
- Con 25+ minutos (hoy se esperan 29): 12 de 14 en sus últimos 15
- Contra las ~10 mejores defensas en robos a bases/escoltas: 5 de 7 (últimos 40 partidos)
- Contra defensas fuertes como la de hoy y con 25+ minutos: 5 de 7, con 1.1 de media (últimos 60 partidos)
- El rival es #23 de 30 en robos que concede a bases/escoltas por minuto (#1 = el que más concede; -7% frente a la media)
- Oportunidades de robo (últimos 10): el rival perdió 7.9 balones por partido con él en pista y robó el 13%
- El rival es #27 de 30 en balones que pierde (#1 = el que más; 12.3 por partido)
- Minutos: 29 esperados (titular, ±5)

Razonamiento (3 factores a favor, 1 en contra):

- ✅ Minutos: 28.7 esperados (titular, ±4.6).
- ✅ Forma: 0.8 en sus últimos 5, 1.1 esta temporada (19 partidos) (línea 0.5).
- ➖ Cómo produce robos: roba el 14.2% de las pérdidas del rival en pista × 11.9 pérdidas esperadas del rival.
- ❌ Defensa: el rival concede -7% de robos por minuto a bases/escoltas (defensa fuerte); ajuste aplicado -7%.
- ➖ Ritmo del partido: -0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Últimos 10: la habría pasado 8 de 10.
- ⚠️ Jusuf Nurkic ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ sin Lauri Markkanen, la estrella de su equipo (11 partidos suyos sin él): más tiros y balón para él por minuto (puntos +2%, triples +5%, asistencias +1%).
- ⚠️ Lauri Markkanen ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ Jaren Jackson Jr. ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ partido desigual (no favorito por 9.5): los titulares suelen jugar -1% de minutos si se rompe.

- Robos **1.0** (por componentes 1.0 · por tasa por minuto y defensa rival 1.0): roba el 14.2% de las pérdidas del rival en pista × 11.9 pérdidas esperadas del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 27.2 | 30.3 | 30.3 | - | - |
| Robos | 0.8 | 1.0 | 1.1 | - | - |
| % de las pérdidas del rival que roba | 14.3% | 12.7% | 14.5% | - | - |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +21%, vs defensa media -5%, vs defensa débil -12%; rebotes: vs defensa fuerte -12%, vs defensa media +14%, vs defensa débil +6%; asistencias: vs defensa fuerte +2%, vs defensa media -24%, vs defensa débil +7%; triples: vs defensa fuerte +30%, vs defensa media -43%, vs defensa débil -8%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| pintura | 37% | 45% | 45% | 45% |
| triple frontal | 35% | 32% | 35% | 35% |
| media distancia | 10% | 33% | 41% | 40% |
| bajo el aro | 10% | 73% | 67% | 70% |
| triple de esquina | 8% | 34% | 38% | 37% |

#### Jamal Murray (bases/escoltas) vs Utah Jazz

- Minutos esperados: **37.3** (± 4.1); 98 partidos en la base.
- partido desigual (favorito por 9.5): los titulares suelen jugar -1% de minutos si se rompe
- Su prop más probable hoy: **Jamal Murray: más de 0.5 robos** (64%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Utah Jazz contra bases/escoltas en robos: +18% respecto a la media; ajuste por su historial contra defensas similares: +4%.

**¿Por qué 1.3 robos?** (línea 0.5; 37.3 minutos esperados)

En corto:

- La pasó en 10 de 16 esta temporada (falló con 0, 0, 0, 0)
- Con 33+ minutos (hoy se esperan 37): 8 de 13 en sus últimos 15
- Contra las ~10 mejores defensas en robos a bases/escoltas: 9 de 15 (últimos 40 partidos)
- Contra defensas débiles como la de hoy y con 33+ minutos: 10 de 16, con 1.2 de media (últimos 60 partidos)
- El rival es #2 de 30 en robos que concede a bases/escoltas por minuto (#1 = el que más concede; +18% frente a la media)
- Oportunidades de robo (últimos 10): el rival perdió 10.8 balones por partido con él en pista y robó el 10%
- El rival es #3 de 30 en balones que pierde (#1 = el que más; 15.3 por partido)
- Minutos: 37 esperados (titular, ±4)

Razonamiento (4 factores a favor, 0 en contra):

- ✅ Minutos: 37.3 esperados (titular, ±4.1).
- ✅ Forma: 1.8 en sus últimos 5, 1.1 esta temporada (16 partidos), 0.8 la temporada pasada (línea 0.5).
- ➖ Cómo produce robos: roba el 10.6% de las pérdidas del rival en pista × 13.1 pérdidas esperadas del rival.
- ✅ Defensa: el rival concede +18% de robos por minuto a bases/escoltas (defensa débil); ajuste aplicado +18%.
- ➖ Ritmo del partido: -0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 1, 0, 2, 1 (3 de 4 a favor).
- ➖ Últimos 10: la habría pasado 5 de 10.
- ⚠️ partido desigual (favorito por 9.5): los titulares suelen jugar -1% de minutos si se rompe.

- Robos **1.3** (por componentes 1.1 · por tasa por minuto y defensa rival 1.4): roba el 10.6% de las pérdidas del rival en pista × 13.1 pérdidas esperadas del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 38.0 | 36.1 | 36.9 | 35.0 | 35.2 |
| Robos | 1.8 | 1.1 | 1.1 | 0.9 | 1.0 |
| % de las pérdidas del rival que roba | 14.5% | 10.2% | 10.1% | 11.0% | 13.3% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -4%, vs defensa media +1%, vs defensa débil +3%; rebotes: vs defensa fuerte -11%, vs defensa media +6%, vs defensa débil +7%; asistencias: vs defensa fuerte -12%, vs defensa media +8%, vs defensa débil +12%; triples: vs defensa fuerte -5%, vs defensa media -2%, vs defensa débil +8%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 36% | 42% | 35% | 36% |
| pintura | 22% | 45% | 45% | 49% |
| media distancia | 20% | 45% | 41% | 42% |
| bajo el aro | 17% | 66% | 67% | 71% |
| triple de esquina | 5% | 47% | 38% | 36% |

## New Orleans Pelicans @ LA Clippers

Diferencia esperada: LA Clippers por 2.5.

Parte de lesiones: Dejounte Murray (Out); Jordan Miller (Out); Trendon Watford (Out); Bennedict Mathurin (Out); Julian Reese (Day-To-Day); Bradley Beal (Out).

Ventajas del partido (los dos lados): puntos esperados frente a su media de los últimos 10, ajuste por la defensa rival y diferencia de estatura con los rivales de su posición.

| Equipo | Jugador | Puntos esperados | Su media (últ. 10) | Defensa rival en puntos | Rebotes esperados | Altura vs rival |
|---|---|---|---|---|---|---|
| NO | Saddiq Bey | 19.0 | 16.0 | -2% | 5.4 | +0.5" |
| NO | Jeremiah Fears | 19.4 | 17.4 | +2% | 5.3 | -1.2" |
| NO | Zion Williamson | 21.9 | 22.3 | -1% | 5.7 | -1.5" |
| NO | Trey Murphy III | 20.2 | 15.5 | -2% | 5.6 | +0.5" |
| LAC | Darius Garland | 20.1 | 21.1 | +4% | 2.2 | -3.1" |
| LAC | Rui Hachimura | 14.8 | 14.8 | +0% | 6.2 | +0.4" |
| LAC | Brandon Ingram | 16.2 | 17.3 | +0% | 5.1 | +0.4" |
| NO | Herbert Jones | 8.3 | 7.4 | -2% | 3.0 | -0.5" |
| LAC | Derrick Jones Jr. | 9.9 | 8.6 | +1% | 4.1 | -1.6" |
| LAC | Max Strus | 9.9 | 7.9 | +3% | 3.7 | +0.9" |

Las 8 más probables (máximo 2 por jugador: las de un mismo jugador suelen ganar o perder juntas).

| Prop | Prob. final | Modelo | Casa | Esperado | Últ. 10 | Temporada | vs este rival | Cuota (implícita) |
|---|---|---|---|---|---|---|---|---|
| **Trey Murphy III: más de 0.5 robos** | **68%** | 72% | 65% | 1.2 ± 1.1 | 9/10 | 9/11 | 1, 1, 3, 2, 2 | 1.47 (68%) |
| **Derik Queen: menos de 0.5 triples** ⚠️ suplente | **68%** | 68% | 69% | 0.5 ± 1.0 | 7/10 | 13/19 | 0, 1, 1, 0, 0 | 1.37 (73%) |
| **Derrick Jones Jr.: más de 0.5 triples** | **68%** | 70% | 64% | 1.3 ± 1.2 | 6/10 | 12/16 | 0, 1, 0, 3, 2 | 1.46 (68%) |
| **Herbert Jones: menos de 1.5 robos** | **67%** | 68% | 65% | 1.2 ± 1.3 | 6/10 | 13/19 | 0, 2, 5, 0, 1 | 1.44 (69%) |
| **Herbert Jones: menos de 1.5 triples** | **64%** | 64% | 63% | 1.2 ± 1.2 | 5/10 | 13/19 | 0, 3, 1, 0, 3 | 1.50 (67%) |
| **Derrick Jones Jr.: menos de 1.5 asistencias** | **63%** | 63% | 65% | 1.4 ± 1.2 | 8/10 | 13/16 | 3, 3, 3, 0, 1 | 1.45 (69%) |
| **Brook Lopez: más de 0.5 tapones** | **63%** | 64% | 61% | 1.1 ± 1.1 | 6/10 | 11/17 | 0, 1, 0, 0, 1 | 1.50 (67%) |
| **Kris Dunn: más de 4.5 puntos** ⚠️ suplente | **63%** | 70% | 53% | 7.1 ± 4.0 | 6/10 | 13/17 | 14, 8, 6, 9, 6 | 1.79 (56%) |

### Fichas de los jugadores destacados

#### Trey Murphy III (aleros/ala-pívots) vs LA Clippers

- Minutos esperados: **33.3** (± 3.5); 77 partidos en la base.
- sin Dejounte Murray (61 partidos): 35.2 min vs 34.5 con él; pts +17%/min, ast +11%/min
- Su prop más probable hoy: **Trey Murphy III: más de 0.5 robos** (68%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de LA Clippers contra aleros/ala-pívots en robos: -6% respecto a la media; ajuste por su historial contra defensas similares: +2%.

**¿Por qué 1.2 robos?** (línea 0.5; 33.3 minutos esperados)

En corto:

- La pasó en 9 de 11 esta temporada (falló con 0, 0)
- Con 29+ minutos (hoy se esperan 33): 10 de 13 en sus últimos 15
- Contra las ~10 mejores defensas en robos a aleros/ala-pívots: 14 de 17 (últimos 40 partidos)
- Contra defensas fuertes como la de hoy y con 29+ minutos: 15 de 20, con 1.4 de media (últimos 60 partidos)
- El rival es #25 de 30 en robos que concede a aleros/ala-pívots por minuto (#1 = el que más concede; -6% frente a la media)
- Oportunidades de robo (últimos 10): el rival perdió 10.1 balones por partido con él en pista y robó el 13%
- El rival es #13 de 30 en balones que pierde (#1 = el que más; 14.3 por partido)
- Minutos: 33 esperados (titular, ±3)

Razonamiento (5 factores a favor, 1 en contra):

- ✅ Minutos: 33.3 esperados (titular, ±3.5).
- ✅ Forma: 1.4 en sus últimos 5, 1.2 esta temporada (11 partidos), 1.5 la temporada pasada (línea 0.5).
- ➖ Cómo produce robos: roba el 12.7% de las pérdidas del rival en pista × 14.3 pérdidas esperadas del rival.
- ❌ Defensa: el rival concede -6% de robos por minuto a aleros/ala-pívots (defensa fuerte); ajuste aplicado -6%.
- ✅ Ritmo del partido: +2% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 1, 1, 3, 2, 2 (5 de 5 a favor).
- ✅ Últimos 10: la habría pasado 9 de 10.
- ⚠️ sin Dejounte Murray (61 partidos): 35.2 min vs 34.5 con él; pts +17%/min, ast +11%/min.

- Robos **1.2** (por componentes 1.3 · por tasa por minuto y defensa rival 1.2): roba el 12.7% de las pérdidas del rival en pista × 14.3 pérdidas esperadas del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 33.6 | 32.7 | 32.6 | 35.5 | 34.0 |
| Robos | 1.4 | 1.3 | 1.2 | 1.5 | 1.8 |
| % de las pérdidas del rival que roba | 16.7% | 12.9% | 12.3% | 14.2% | 20.0% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -0%, vs defensa media +3%, vs defensa débil -2%; rebotes: vs defensa fuerte -8%, vs defensa media +11%, vs defensa débil +1%; asistencias: vs defensa fuerte -6%, vs defensa media -1%, vs defensa débil +9%; triples: vs defensa fuerte -3%, vs defensa media -13%, vs defensa débil +18%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 49% | 36% | 35% | 36% |
| bajo el aro | 25% | 74% | 67% | 70% |
| pintura | 17% | 39% | 45% | 45% |
| triple de esquina | 5% | 43% | 38% | 39% |
| media distancia | 5% | 40% | 41% | 40% |

#### Derik Queen (pívots) vs LA Clippers

- Minutos esperados: **22.9** (± 6.1); 100 partidos en la base.
- Dejounte Murray ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Su prop más probable hoy: **Derik Queen: menos de 0.5 triples** (68%). Con 80% de probabilidad: más de - / menos de 1.5.
- Defensa de LA Clippers contra pívots en triples: +4% respecto a la media; ajuste por su historial contra defensas similares: -6%.

**¿Por qué 0.5 triples?** (línea 0.5; 22.9 minutos esperados)

En corto:

- La pasó en 13 de 19 esta temporada (falló con 4, 2, 1, 1)
- Con 19+ minutos (hoy se esperan 23): 8 de 12 en sus últimos 15
- Contra las ~10 mejores defensas en triples a pívots: 10 de 15 (últimos 40 partidos)
- Contra defensas débiles como la de hoy y con 19+ minutos: 5 de 11, con 0.5 de media (últimos 60 partidos)
- El rival es #8 de 30 en triples que concede a pívots por minuto (#1 = el que más concede; +6% frente a la media)
- Su zona principal es triple frontal (10% de sus tiros, 33% de acierto); el rival es #9 de 30 en acierto que deja ahí (36%, liga 35%)
- Cómo tira (últimos 15): penetración 39% (48% de acierto), recibe y tira 17% (43% de acierto), creado 14% (28% de acierto); en penetración el rival es #6 de 30 en lo que deja (#1 = el que más; 1.13 puntos por tiro frente a 1.08 de media)
- Oportunidades: 1.5 triples intentados esperados al 34%
- Minutos: 23 esperados (suplente, ±6)

Razonamiento (3 factores a favor, 4 en contra):

- ❌ Minutos: 22.9 esperados (suplente, ±6.1).
- ❌ Forma: 0.8 en sus últimos 5, 0.5 esta temporada (19 partidos), 0.3 la temporada pasada (línea 0.5).
- ➖ Cómo produce triples: 1.5 triples intentados (su ritmo 2.3 por 36'; el rival concede -1% de triples en su reparto) × 34% esperado.
- ❌ Defensa: el rival concede +6% de triples por minuto a pívots (defensa débil); ajuste aplicado +4%; en su zona principal (triple) el rival concede 36% (liga 35%).
- ✅ Altura: mide 6'9", 3.7 pulgadas menos que los pívots del rival (-1.3% en esta estadística).
- ❌ Ritmo del partido: +2% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 0, 1, 1, 0, 0 (3 de 5 a favor).
- ✅ Últimos 10: la habría pasado 7 de 10.
- ⚠️ Dejounte Murray ya no jugó en sus últimos partidos: la baja ya está en sus minutos.

- ⚠️ Alertas: suplente, minutos inestables.
- Triples **0.5** (por componentes 0.5 · por tasa por minuto y defensa rival 0.5): 1.5 triples intentados (su ritmo 2.3 por 36'; el rival concede -1% de triples en su reparto) × 34% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 22.8 | 21.8 | 22.2 | 25.0 | 19.6 |
| Triples anotados | 0.8 | 0.7 | 0.5 | 0.3 | 0.4 |
| Triples intentados | 2.2 | 1.8 | 1.4 | 1.1 | 0.8 |
| % triples | 36.4% | 38.9% | 37.0% | 26.1% | 50.0% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -8%, vs defensa media +10%, vs defensa débil -3%; rebotes: vs defensa fuerte -6%, vs defensa media +2%, vs defensa débil +5%; asistencias: vs defensa fuerte -8%, vs defensa media -7%, vs defensa débil +12%; triples: vs defensa fuerte -16%, vs defensa media +26%, vs defensa débil -13%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 45% | 62% | 67% | 70% |
| pintura | 31% | 40% | 45% | 45% |
| media distancia | 10% | 37% | 41% | 40% |
| triple frontal | 10% | 33% | 35% | 36% |
| triple de esquina | 4% | 33% | 38% | 39% |

#### Derrick Jones Jr. (aleros/ala-pívots) vs New Orleans Pelicans

- Minutos esperados: **25.6** (± 3.0); 67 partidos en la base.
- Jordan Miller ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Bradley Beal ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Su prop más probable hoy: **Derrick Jones Jr.: más de 0.5 triples** (68%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de New Orleans Pelicans contra aleros/ala-pívots en triples: -0% respecto a la media; ajuste por su historial contra defensas similares: -3%.

**¿Por qué 1.3 triples?** (línea 0.5; 25.6 minutos esperados)

En corto:

- La pasó en 12 de 16 esta temporada (falló con 0, 0, 0, 0)
- Contra las ~10 mejores defensas en triples a aleros/ala-pívots: 7 de 13 (últimos 40 partidos)
- Contra defensas medias como la de hoy y con 22+ minutos: 13 de 20, con 1.2 de media (últimos 60 partidos)
- El rival es #16 de 30 en triples que concede a aleros/ala-pívots por minuto (#1 = el que más concede; +1% frente a la media)
- Su zona principal es triple frontal (26% de sus tiros, 37% de acierto); el rival es #25 de 30 en acierto que deja ahí (34%, liga 35%)
- Cómo tira (últimos 15): recibe y tira 44% (38% de acierto), penetración 19% (48% de acierto), creado 12% (57% de acierto); en recibe y tira el rival es #16 de 30 en lo que deja (#1 = el que más; 1.07 puntos por tiro frente a 1.07 de media)
- Oportunidades: 3.7 triples intentados esperados al 38%
- Minutos: 26 esperados (titular, ±3)

Razonamiento (3 factores a favor, 2 en contra):

- ✅ Minutos: 25.6 esperados (titular, ±3.0).
- ❌ Forma: 0.4 en sus últimos 5, 1.6 esta temporada (16 partidos), 1.1 la temporada pasada (línea 0.5).
- ➖ Cómo produce triples: 3.7 triples intentados (su ritmo 4.8 por 36'; el rival concede +6% de triples en su reparto) × 38% esperado.
- ➖ Defensa: el rival concede +1% de triples por minuto a aleros/ala-pívots (defensa media); ajuste aplicado -0%; en su zona principal (triple) el rival concede 34% (liga 35%).
- ❌ Altura: mide 6'6", 1.6 pulgadas menos que los aleros/ala-pívots del rival (-0.6% en esta estadística).
- ✅ Ritmo del partido: +2% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 0, 1, 0, 3, 2 (3 de 5 a favor).
- ➖ Últimos 10: la habría pasado 6 de 10.
- ⚠️ Jordan Miller ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ Bradley Beal ya no jugó en sus últimos partidos: la baja ya está en sus minutos.

- Triples **1.3** (por componentes 1.4 · por tasa por minuto y defensa rival 1.3): 3.7 triples intentados (su ritmo 4.8 por 36'; el rival concede +6% de triples en su reparto) × 38% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 25.4 | 27.2 | 27.8 | 26.9 | 29.8 |
| Triples anotados | 0.4 | 1.3 | 1.6 | 1.1 | 1.2 |
| Triples intentados | 3.0 | 3.6 | 3.8 | 3.1 | 3.0 |
| % triples | 13.3% | 36.1% | 42.6% | 35.7% | 40.0% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -2%, vs defensa media +5%, vs defensa débil -3%; rebotes: vs defensa fuerte -7%, vs defensa media +13%, vs defensa débil -2%; asistencias: vs defensa fuerte -6%, vs defensa media -6%, vs defensa débil +10%; triples: vs defensa fuerte -7%, vs defensa media -10%, vs defensa débil +23%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 35% | 69% | 67% | 69% |
| triple frontal | 26% | 37% | 35% | 34% |
| triple de esquina | 19% | 40% | 38% | 38% |
| pintura | 18% | 42% | 45% | 48% |
| media distancia | 2% | 36% | 41% | 41% |

#### Herbert Jones (aleros/ala-pívots) vs LA Clippers

- Minutos esperados: **26.3** (± 4.5); 75 partidos en la base.
- Dejounte Murray ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Su prop más probable hoy: **Herbert Jones: menos de 1.5 robos** (67%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de LA Clippers contra aleros/ala-pívots en robos: -6% respecto a la media; ajuste por su historial contra defensas similares: +1%.

**¿Por qué 1.2 robos?** (línea 1.5; 26.3 minutos esperados)

En corto:

- La pasó en 13 de 19 esta temporada (falló con 3, 3, 3, 3)
- Con 22+ minutos (hoy se esperan 26): 8 de 12 en sus últimos 15
- Contra las ~10 mejores defensas en robos a aleros/ala-pívots: 9 de 14 (últimos 40 partidos)
- Contra defensas fuertes como la de hoy y con 22+ minutos: 9 de 16, con 1.6 de media (últimos 60 partidos)
- El rival es #25 de 30 en robos que concede a aleros/ala-pívots por minuto (#1 = el que más concede; -6% frente a la media)
- Oportunidades de robo (últimos 10): el rival perdió 8.4 balones por partido con él en pista y robó el 17%
- El rival es #13 de 30 en balones que pierde (#1 = el que más; 14.3 por partido)
- Minutos: 26 esperados (titular, ±5)

Razonamiento (3 factores a favor, 2 en contra):

- ✅ Minutos: 26.3 esperados (titular, ±4.5).
- ❌ Forma: 2.0 en sus últimos 5, 1.2 esta temporada (19 partidos), 1.6 la temporada pasada (línea 1.5).
- ➖ Cómo produce robos: roba el 13.8% de las pérdidas del rival en pista × 14.3 pérdidas esperadas del rival.
- ✅ Defensa: el rival concede -6% de robos por minuto a aleros/ala-pívots (defensa fuerte); ajuste aplicado -6%.
- ❌ Ritmo del partido: +2% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 0, 2, 5, 0, 1 (3 de 5 a favor).
- ➖ Últimos 10: la habría pasado 6 de 10.
- ⚠️ Dejounte Murray ya no jugó en sus últimos partidos: la baja ya está en sus minutos.

- Robos **1.2** (por componentes 1.1 · por tasa por minuto y defensa rival 1.2): roba el 13.8% de las pérdidas del rival en pista × 14.3 pérdidas esperadas del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 27.0 | 26.3 | 24.7 | 28.4 | 25.4 |
| Robos | 2.0 | 1.4 | 1.2 | 1.6 | 1.6 |
| % de las pérdidas del rival que roba | 19.6% | 16.7% | 12.6% | 18.1% | 23.5% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +2%, vs defensa media -4%, vs defensa débil +2%; rebotes: vs defensa fuerte +5%, vs defensa media +3%, vs defensa débil -9%; asistencias: vs defensa fuerte -6%, vs defensa media +13%, vs defensa débil -10%; triples: vs defensa fuerte +1%, vs defensa media -22%, vs defensa débil +20%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 33% | 32% | 35% | 36% |
| bajo el aro | 27% | 56% | 67% | 70% |
| triple de esquina | 18% | 32% | 38% | 39% |
| pintura | 17% | 36% | 45% | 45% |
| media distancia | 5% | 37% | 41% | 40% |

#### Brook Lopez (pívots) vs New Orleans Pelicans

- Minutos esperados: **23.5** (± 4.5); 93 partidos en la base.
- Jordan Miller ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Bradley Beal ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Su prop más probable hoy: **Brook Lopez: más de 0.5 tapones** (63%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de New Orleans Pelicans contra pívots en tapones: +27% respecto a la media; ajuste por su historial contra defensas similares: +0%.

**¿Por qué 1.1 tapones?** (línea 0.5; 23.5 minutos esperados)

En corto:

- La pasó en 11 de 17 esta temporada (falló con 0, 0, 0, 0)
- Con 19+ minutos (hoy se esperan 23): 8 de 12 en sus últimos 15
- Contra las ~10 mejores defensas en tapones a pívots: 10 de 15 (últimos 40 partidos)
- Contra defensas débiles como la de hoy y con 19+ minutos: 10 de 15, con 1.3 de media (últimos 60 partidos)
- El rival es #1 de 30 en tapones que concede a pívots por minuto (#1 = el que más concede; +27% frente a la media)
- Oportunidades de tapón (últimos 9): 31.0 tiros de 2 del rival por partido con él en pista; taponó el 2.2%
- El rival es #1 de 30 en tiros de 2 por partido (#1 = el que más; 57.4)
- El 55% de los tiros del rival son cerca del aro (penetración, corte, poste, palmeo): #1 de 30
- Minutos: 23 esperados (titular, ±5)

Razonamiento (5 factores a favor, 0 en contra):

- ✅ Minutos: 23.5 esperados (titular, ±4.5).
- ✅ Forma: 0.6 en sus últimos 5, 0.8 esta temporada (17 partidos), 1.2 la temporada pasada (línea 0.5).
- ➖ Cómo produce tapones: tapona el 3.4% de los tiros de 2 del rival en pista × 57.3 tiros de 2 esperados del rival.
- ✅ Defensa: el rival concede +27% de tapones por minuto a pívots (defensa débil); ajuste aplicado +27%.
- ✅ Altura: mide 7'1", 3.1 pulgadas más que los pívots del rival (+2.3% en esta estadística).
- ✅ Ritmo del partido: +2% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ➖ Contra este rival: 0, 1, 0, 0, 1 (2 de 5 a favor).
- ➖ Últimos 10: la habría pasado 6 de 10.
- ⚠️ Jordan Miller ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ Bradley Beal ya no jugó en sus últimos partidos: la baja ya está en sus minutos.

- Tapones **1.1** (por componentes 0.9 · por tasa por minuto y defensa rival 1.1): tapona el 3.4% de los tiros de 2 del rival en pista × 57.3 tiros de 2 esperados del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 22.8 | 25.4 | 24.0 | 22.0 | 25.2 |
| Tapones | 0.6 | 0.7 | 0.8 | 1.2 | 0.4 |
| % de los tiros de 2 del rival que tapona | 2.2% | 2.3% | 2.9% | 5.1% | 1.6% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -1%, vs defensa media -14%, vs defensa débil +11%; rebotes: vs defensa fuerte -15%, vs defensa media +1%, vs defensa débil +13%; asistencias: vs defensa fuerte -2%, vs defensa media +18%, vs defensa débil -13%; triples: vs defensa fuerte -27%, vs defensa media +7%, vs defensa débil +36%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 44% | 36% | 35% | 34% |
| pintura | 23% | 50% | 45% | 48% |
| bajo el aro | 19% | 72% | 67% | 69% |
| media distancia | 8% | 38% | 41% | 41% |
| triple de esquina | 7% | 42% | 38% | 38% |

## Golden State Warriors @ Portland Trail Blazers

Diferencia esperada: Portland Trail Blazers por 7.5.

Parte de lesiones: Kristaps Porzingis (Out); Stephen Curry (Out); Ja Morant (Out); Moses Moody (Out); Vit Krejci (Out); Chris Youngblood (Out); Shaedon Sharpe (Out); Jimmy Butler III (Out); Damian Lillard (Out).

Ventajas del partido (los dos lados): puntos esperados frente a su media de los últimos 10, ajuste por la defensa rival y diferencia de estatura con los rivales de su posición.

| Equipo | Jugador | Puntos esperados | Su media (últ. 10) | Defensa rival en puntos | Rebotes esperados | Altura vs rival |
|---|---|---|---|---|---|---|
| POR | Deni Avdija | 25.5 | 25.5 | +0% | 6.9 | +0.6" |
| GS | Brandin Podziemski | 17.8 | 15.0 | +0% | 4.9 | -0.1" |
| POR | Toumani Camara | 13.2 | 9.4 | -0% | 4.6 | -0.4" |
| GS | Yaxel Lendeborg | 19.7 | 17.0 | -3% | 7.4 | +1.6" |
| POR | Jrue Holiday | 16.3 | 14.4 | +1% | 4.3 | +1.5" |
| POR | Sidy Cissoko | 10.2 | 9.9 | +2% | 4.0 | +3.5" |
| POR | Donovan Clingan | 12.4 | 10.2 | +0% | 11.5 | +4.9" |
| GS | Draymond Green | 7.4 | 4.1 | -3% | 4.3 | -1.4" |
| GS | De'Anthony Melton | 11.3 | 8.7 | +0% | 3.7 | -2.1" |
| GS | Will Richard | 6.5 | 8.8 | -0% | 2.3 | -1.1" |

Las 8 más probables (máximo 2 por jugador: las de un mismo jugador suelen ganar o perder juntas).

| Prop | Prob. final | Modelo | Casa | Esperado | Últ. 10 | Temporada | vs este rival | Cuota (implícita) |
|---|---|---|---|---|---|---|---|---|
| **Scoot Henderson: menos de 3.5 asistencias** ⚠️ suplente | **72%** | 81% | 58% | 2.1 ± 1.5 | 9/10 | 17/18 | - | 1.61 (62%) |
| **Sidy Cissoko: menos de 1.5 robos** | **71%** | 76% | 63% | 1.0 ± 1.0 | 8/10 | 16/18 | 0, 1, 1 | 1.45 (69%) |
| **Yaxel Lendeborg: más de 0.5 robos** | **71%** | 73% | 67% | 1.4 ± 1.2 | 7/10 | 12/18 | - | 1.42 (71%) |
| **Brandin Podziemski: más de 0.5 robos** | **67%** | 68% | 65% | 1.2 ± 1.1 | 7/10 | 11/16 | 2, 1, 3, 2 | 1.47 (68%) |
| **Charles Bassey: menos de 1.5 asistencias** | **66%** | 68% | 62% | 1.2 ± 1.1 | 8/10 | 13/16 | - | 1.51 (66%) |
| **Deni Avdija: más de 0.5 robos** | **65%** | 64% | 66% | 1.0 ± 1.0 | 7/10 | 11/16 | 1, 0, 0 | 1.41 (71%) |
| **Deni Avdija: más de 1.5 triples** | **64%** | 66% | 61% | 2.3 ± 1.5 | 8/10 | 12/16 | 2, 2, 4 | 1.55 (65%) |
| **Toumani Camara: más de 0.5 robos** | **63%** | 62% | 65% | 1.0 ± 1.0 | 6/10 | 10/18 | 0, 2, 0, 3 | 1.42 (71%) |

### Fichas de los jugadores destacados

#### Scoot Henderson (bases/escoltas) vs Golden State Warriors

- Minutos esperados: **24.6** (± 4.1); 54 partidos en la base.
- Ja Morant ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- sin Damian Lillard, la estrella de su equipo (0 partidos suyos sin él): más tiros y balón para él por minuto (puntos +7%, triples +4%, asistencias +6%)
- Su prop más probable hoy: **Scoot Henderson: menos de 3.5 asistencias** (72%). Con 80% de probabilidad: más de 0.5 / menos de 3.5.
- Defensa de Golden State Warriors contra bases/escoltas en asistencias: +2% respecto a la media; ajuste por su historial contra defensas similares: +2%.

**¿Por qué 2.1 asistencias?** (línea 3.5; 24.6 minutos esperados)

En corto:

- La pasó en 17 de 18 esta temporada; los fallos, en partidos raros (paliza de 20)
- Con 21+ minutos (hoy se esperan 25): 12 de 13 en sus últimos 15
- Contra las ~10 mejores defensas en asistencias a bases/escoltas: 16 de 17 (últimos 40 partidos)
- Contra defensas medias como la de hoy y con 21+ minutos: 10 de 14, con 3.6 de media (últimos 60 partidos)
- El rival es #15 de 30 en asistencias que concede a bases/escoltas por minuto (#1 = el que más concede; +2% frente a la media)
- Asistencias esperadas: 1.7 por partido si sus compañeros metieran lo normal (tiene 1.7; con él en pista metieron el 102% de lo esperado por tipo de tiro, últimos 10); ajuste aplicado -0.6%
- Oportunidades: asiste el 11% de las canastas de sus compañeros con él en pista
- Su equipo no tiene a Damian Lillard: más tiros y balón para él
- Minutos: 25 esperados (suplente, ±4)

Razonamiento (2 factores a favor, 1 en contra):

- ❌ Minutos: 24.6 esperados (suplente, ±4.1).
- ✅ Forma: 1.8 en sus últimos 5, 1.5 esta temporada (18 partidos), 3.3 la temporada pasada (línea 3.5).
- ➖ Cómo produce asistencias: asiste el 11.4% de las canastas de sus compañeros en pista × 16.4 canastas de compañeros esperadas (su equipo 40.5 por 48' contra esta defensa).
- ➖ Defensa: el rival concede +2% de asistencias por minuto a bases/escoltas (defensa media); ajuste aplicado +2%.
- ➖ Ritmo del partido: -0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Últimos 10: la habría pasado 9 de 10.
- ⚠️ Ja Morant ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ sin Damian Lillard, la estrella de su equipo (0 partidos suyos sin él): más tiros y balón para él por minuto (puntos +7%, triples +4%, asistencias +6%).

- ⚠️ Alertas: suplente, sin Damian Lillard: más tiros para él.
- Asistencias **2.1** (por componentes 2.0 · por tasa por minuto y defensa rival 2.2): asiste el 11.4% de las canastas de sus compañeros en pista × 16.4 canastas de compañeros esperadas (su equipo 40.5 por 48' contra esta defensa).

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 25.6 | 24.0 | 23.2 | 25.2 | - |
| Asistencias | 1.8 | 1.7 | 1.5 | 3.3 | - |
| % de las canastas de compañeros que asiste | 9.6% | 9.8% | 8.6% | 18.0% | - |
| Pérdidas por jugada | 12.8% | 10.6% | 16.0% | 15.6% | - |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -5%, vs defensa media -6%, vs defensa débil +11%; rebotes: vs defensa fuerte -23%, vs defensa media +2%, vs defensa débil +8%; asistencias: vs defensa fuerte -32%, vs defensa media +24%, vs defensa débil +17%; triples: vs defensa fuerte -11%, vs defensa media -8%, vs defensa débil +24%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 36% | 33% | 35% | 34% |
| pintura | 22% | 37% | 45% | 47% |
| bajo el aro | 19% | 62% | 67% | 70% |
| triple de esquina | 12% | 33% | 38% | 39% |
| media distancia | 10% | 44% | 41% | 43% |

#### Sidy Cissoko (bases/escoltas) vs Golden State Warriors

- Minutos esperados: **27.5** (± 3.9); 97 partidos en la base.
- Ja Morant ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- sin Damian Lillard, la estrella de su equipo (0 partidos suyos sin él): más tiros y balón para él por minuto (puntos +7%, triples +4%, asistencias +6%)
- Su prop más probable hoy: **Sidy Cissoko: menos de 1.5 robos** (71%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Golden State Warriors contra bases/escoltas en robos: +11% respecto a la media; ajuste por su historial contra defensas similares: -4%.

**¿Por qué 1.0 robos?** (línea 1.5; 27.5 minutos esperados)

En corto:

- La pasó en 16 de 18 esta temporada (falló con 2, 3)
- Con 23+ minutos (hoy se esperan 27): 6 de 8 en sus últimos 15
- Contra las ~10 mejores defensas en robos a bases/escoltas: 16 de 18 (últimos 40 partidos)
- Contra defensas débiles como la de hoy y con 23+ minutos: 4 de 6, con 0.8 de media (últimos 60 partidos)
- El rival es #4 de 30 en robos que concede a bases/escoltas por minuto (#1 = el que más concede; +11% frente a la media)
- Oportunidades de robo (últimos 10): el rival perdió 8.0 balones por partido con él en pista y robó el 12%
- El rival es #4 de 30 en balones que pierde (#1 = el que más; 15.2 por partido)
- Minutos: 27 esperados (titular, ±4)

Razonamiento (3 factores a favor, 2 en contra):

- ✅ Minutos: 27.5 esperados (titular, ±3.9).
- ❌ Forma: 1.6 en sus últimos 5, 0.7 esta temporada (18 partidos), 0.8 la temporada pasada (línea 1.5).
- ➖ Cómo produce robos: roba el 11.5% de las pérdidas del rival en pista × 15.8 pérdidas esperadas del rival.
- ❌ Defensa: el rival concede +11% de robos por minuto a bases/escoltas (defensa débil); ajuste aplicado +11%.
- ➖ Ritmo del partido: -0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 0, 1, 1 (3 de 3 a favor).
- ✅ Últimos 10: la habría pasado 8 de 10.
- ⚠️ Ja Morant ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ sin Damian Lillard, la estrella de su equipo (0 partidos suyos sin él): más tiros y balón para él por minuto (puntos +7%, triples +4%, asistencias +6%).

- Robos **1.0** (por componentes 1.0 · por tasa por minuto y defensa rival 1.0): roba el 11.5% de las pérdidas del rival en pista × 15.8 pérdidas esperadas del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 28.0 | 27.2 | 24.8 | 18.5 | 25.7 |
| Robos | 1.6 | 1.0 | 0.7 | 0.7 | 0.7 |
| % de las pérdidas del rival que roba | 17.4% | 12.5% | 10.4% | 11.3% | 8.7% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +11%, vs defensa media -1%, vs defensa débil -11%; rebotes: vs defensa fuerte -19%, vs defensa media -4%, vs defensa débil +23%; asistencias: vs defensa fuerte +12%, vs defensa media -21%, vs defensa débil +1%; triples: vs defensa fuerte +5%, vs defensa media -22%, vs defensa débil +14%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 33% | 31% | 35% | 34% |
| triple de esquina | 30% | 38% | 38% | 39% |
| bajo el aro | 25% | 69% | 67% | 70% |
| pintura | 11% | 35% | 45% | 47% |
| media distancia | 2% | 40% | 41% | 43% |

#### Yaxel Lendeborg (aleros/ala-pívots) vs Portland Trail Blazers

- Minutos esperados: **31.7** (± 3.1); 18 partidos en la base.
- Kristaps Porzingis ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Stephen Curry ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Moses Moody ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- sin Jimmy Butler III, la estrella de su equipo (0 partidos suyos sin él): más tiros y balón para él por minuto (puntos +7%, triples +4%, asistencias +6%)
- Jimmy Butler III ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Su prop más probable hoy: **Yaxel Lendeborg: más de 0.5 robos** (71%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Portland Trail Blazers contra aleros/ala-pívots en robos: +21% respecto a la media; ajuste por su historial contra defensas similares: +4%.

**¿Por qué 1.4 robos?** (línea 0.5; 31.7 minutos esperados)

En corto:

- La pasó en 12 de 18 esta temporada (falló con 0, 0, 0, 0)
- Con 28+ minutos (hoy se esperan 32): 9 de 12 en sus últimos 15
- Contra las ~10 mejores defensas en robos a aleros/ala-pívots: 2 de 5 (últimos 40 partidos)
- Contra defensas débiles como la de hoy y con 28+ minutos: 4 de 4, con 1.8 de media (últimos 60 partidos)
- El rival es #1 de 30 en robos que concede a aleros/ala-pívots por minuto (#1 = el que más concede; +21% frente a la media)
- Oportunidades de robo (últimos 10): el rival perdió 8.6 balones por partido con él en pista y robó el 15%
- El rival es #1 de 30 en balones que pierde (#1 = el que más; 15.8 por partido)
- El rival no tiene a Damian Lillard (0.6 robos por partido)
- Minutos: 32 esperados (titular, ±3)

Razonamiento (4 factores a favor, 0 en contra):

- ✅ Minutos: 31.7 esperados (titular, ±3.1).
- ✅ Forma: 1.4 en sus últimos 5, 1.1 esta temporada (18 partidos) (línea 0.5).
- ➖ Cómo produce robos: roba el 11.8% de las pérdidas del rival en pista × 17.4 pérdidas esperadas del rival.
- ✅ Defensa: el rival concede +21% de robos por minuto a aleros/ala-pívots (defensa débil); ajuste aplicado +21%.
- ➖ Ritmo del partido: -0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Últimos 10: la habría pasado 7 de 10.
- ⚠️ Kristaps Porzingis ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ Stephen Curry ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ Moses Moody ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ sin Jimmy Butler III, la estrella de su equipo (0 partidos suyos sin él): más tiros y balón para él por minuto (puntos +7%, triples +4%, asistencias +6%).
- ⚠️ Jimmy Butler III ya no jugó en sus últimos partidos: la baja ya está en sus minutos.

- Robos **1.4** (por componentes 1.4 · por tasa por minuto y defensa rival 1.4): roba el 11.8% de las pérdidas del rival en pista × 17.4 pérdidas esperadas del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 32.2 | 31.5 | 31.7 | - | - |
| Robos | 1.4 | 1.3 | 1.1 | - | - |
| % de las pérdidas del rival que roba | 14.3% | 15.1% | 11.5% | - | - |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +6%, vs defensa media -8%, vs defensa débil +7%; rebotes: vs defensa fuerte -3%, vs defensa media -16%, vs defensa débil +18%; asistencias: vs defensa fuerte -59%, vs defensa media +36%, vs defensa débil +23%; triples: vs defensa fuerte +50%, vs defensa media -22%, vs defensa débil -64%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 30% | 35% | 35% | 35% |
| pintura | 30% | 46% | 45% | 45% |
| bajo el aro | 25% | 67% | 67% | 66% |
| media distancia | 9% | 33% | 41% | 42% |
| triple de esquina | 6% | 39% | 38% | 38% |

#### Brandin Podziemski (bases/escoltas) vs Portland Trail Blazers

- Minutos esperados: **32.1** (± 4.5); 100 partidos en la base.
- Kristaps Porzingis ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Stephen Curry ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Moses Moody ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- sin Jimmy Butler III, la estrella de su equipo (20 partidos suyos sin él): más tiros y balón para él por minuto (puntos +13%, triples -2%, asistencias -2%)
- Jimmy Butler III ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Su prop más probable hoy: **Brandin Podziemski: más de 0.5 robos** (67%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Portland Trail Blazers contra bases/escoltas en robos: +18% respecto a la media; ajuste por su historial contra defensas similares: -3%.

**¿Por qué 1.2 robos?** (línea 0.5; 32.1 minutos esperados)

En corto:

- La pasó en 11 de 16 esta temporada (falló con 0, 0, 0, 0)
- Con 28+ minutos (hoy se esperan 32): 9 de 13 en sus últimos 15
- Contra las ~10 mejores defensas en robos a bases/escoltas: 11 de 14 (últimos 40 partidos)
- Contra defensas débiles como la de hoy y con 28+ minutos: 12 de 16, con 1.1 de media (últimos 60 partidos)
- El rival es #1 de 30 en robos que concede a bases/escoltas por minuto (#1 = el que más concede; +18% frente a la media)
- Oportunidades de robo (últimos 10): el rival perdió 9.4 balones por partido con él en pista y robó el 10%
- El rival es #1 de 30 en balones que pierde (#1 = el que más; 15.8 por partido)
- El rival no tiene a Damian Lillard (0.6 robos por partido)
- Minutos: 32 esperados (titular, ±4)

Razonamiento (5 factores a favor, 0 en contra):

- ✅ Minutos: 32.1 esperados (titular, ±4.5).
- ✅ Forma: 0.6 en sus últimos 5, 1.0 esta temporada (16 partidos), 1.0 la temporada pasada (línea 0.5).
- ➖ Cómo produce robos: roba el 10.1% de las pérdidas del rival en pista × 17.4 pérdidas esperadas del rival.
- ✅ Defensa: el rival concede +18% de robos por minuto a bases/escoltas (defensa débil); ajuste aplicado +18%.
- ➖ Ritmo del partido: -0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 2, 1, 3, 2 (4 de 4 a favor).
- ✅ Últimos 10: la habría pasado 7 de 10.
- ⚠️ Kristaps Porzingis ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ Stephen Curry ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ Moses Moody ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ sin Jimmy Butler III, la estrella de su equipo (20 partidos suyos sin él): más tiros y balón para él por minuto (puntos +13%, triples -2%, asistencias -2%).
- ⚠️ Jimmy Butler III ya no jugó en sus últimos partidos: la baja ya está en sus minutos.

- Robos **1.2** (por componentes 1.2 · por tasa por minuto y defensa rival 1.2): roba el 10.1% de las pérdidas del rival en pista × 17.4 pérdidas esperadas del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 32.2 | 31.7 | 32.4 | 28.7 | 26.8 |
| Robos | 0.6 | 0.9 | 1.0 | 1.1 | 2.0 |
| % de las pérdidas del rival que roba | 5.8% | 9.6% | 9.5% | 12.2% | 17.0% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -3%, vs defensa media -2%, vs defensa débil +4%; rebotes: vs defensa fuerte +3%, vs defensa media -13%, vs defensa débil +8%; asistencias: vs defensa fuerte -12%, vs defensa media -12%, vs defensa débil +22%; triples: vs defensa fuerte -11%, vs defensa media +2%, vs defensa débil +8%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 41% | 33% | 35% | 35% |
| pintura | 21% | 49% | 45% | 45% |
| bajo el aro | 16% | 70% | 67% | 66% |
| media distancia | 12% | 39% | 41% | 42% |
| triple de esquina | 9% | 52% | 38% | 38% |

#### Charles Bassey (pívots) vs Portland Trail Blazers

- Minutos esperados: **21.1** (± 4.3); 30 partidos en la base.
- Kristaps Porzingis ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Stephen Curry ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Moses Moody ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- sin Jimmy Butler III, la estrella de su equipo (6 partidos suyos sin él): más tiros y balón para él por minuto (puntos +4%, asistencias +5%)
- Jimmy Butler III ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Su prop más probable hoy: **Charles Bassey: menos de 1.5 asistencias** (66%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Portland Trail Blazers contra pívots en asistencias: +5% respecto a la media; ajuste por su historial contra defensas similares: -5%.

**¿Por qué 1.2 asistencias?** (línea 1.5; 21.1 minutos esperados)

En corto:

- La pasó en 13 de 16 esta temporada (falló con 3, 2, 2)
- Con 17+ minutos (hoy se esperan 21): 5 de 8 en sus últimos 15
- Contra las ~10 mejores defensas en asistencias a pívots: 9 de 10 (últimos 40 partidos)
- Contra defensas débiles como la de hoy y con 17+ minutos: 4 de 4, con 0.8 de media (últimos 60 partidos)
- El rival es #7 de 30 en asistencias que concede a pívots por minuto (#1 = el que más concede; +5% frente a la media)
- Asistencias esperadas: 0.9 por partido si sus compañeros metieran lo normal (tiene 0.8; con él en pista metieron el 91% de lo esperado por tipo de tiro, últimos 10); ajuste aplicado +5.7%
- Oportunidades: asiste el 7% de las canastas de sus compañeros con él en pista
- El rival no tiene a Damian Lillard (4.3 asistencias por partido)
- Su equipo no tiene a Jimmy Butler III: más tiros y balón para él
- Minutos: 21 esperados (titular, ±4)

Razonamiento (3 factores a favor, 2 en contra):

- ✅ Minutos: 21.1 esperados (titular, ±4.3).
- ✅ Forma: 1.0 en sus últimos 5, 0.8 esta temporada (16 partidos), 0.5 la temporada pasada (línea 1.5).
- ➖ Cómo produce asistencias: asiste el 7.4% de las canastas de sus compañeros en pista × 13.0 canastas de compañeros esperadas (su equipo 39.6 por 48' contra esta defensa).
- ❌ Defensa: el rival concede +5% de asistencias por minuto a pívots (defensa débil); ajuste aplicado +5%.
- ➖ Ritmo del partido: -0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Últimos 10: la habría pasado 8 de 10.
- ❌ Bajas del rival: sin Damian Lillard (titular); +1.5% en esta estadística.
- ⚠️ Kristaps Porzingis ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ Stephen Curry ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ Moses Moody ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ sin Jimmy Butler III, la estrella de su equipo (6 partidos suyos sin él): más tiros y balón para él por minuto (puntos +4%, asistencias +5%).
- ⚠️ Jimmy Butler III ya no jugó en sus últimos partidos: la baja ya está en sus minutos.

- ⚠️ Alertas: sin Jimmy Butler III: más tiros para él.
- Asistencias **1.2** (por componentes 1.0 · por tasa por minuto y defensa rival 1.1): asiste el 7.4% de las canastas de sus compañeros en pista × 13.0 canastas de compañeros esperadas (su equipo 39.6 por 48' contra esta defensa).

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 22.2 | 18.7 | 16.0 | 11.0 | - |
| Asistencias | 1.0 | 0.8 | 0.8 | 0.5 | - |
| % de las canastas de compañeros que asiste | 6.8% | 6.2% | 6.6% | 6.4% | - |
| Pérdidas por jugada | 18.9% | 18.6% | 16.0% | 9.7% | - |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -15%, vs defensa media +25%, vs defensa débil -3%; rebotes: vs defensa fuerte -4%, vs defensa media +25%, vs defensa débil -8%; asistencias: vs defensa fuerte +5%, vs defensa media +48%, vs defensa débil -49%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 57% | 71% | 67% | 66% |
| pintura | 37% | 56% | 45% | 45% |
| triple frontal | 2% | 34% | 35% | 35% |
| triple de esquina | 2% | 35% | 38% | 38% |
| media distancia | 2% | 44% | 41% | 42% |
