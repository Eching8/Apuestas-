# Props NBA 2026-11-20

> **Aviso:** las apuestas implican riesgo de perder dinero. Estas probabilidades son estimaciones estadísticas, no garantías: ningún modelo acierta siempre y las combinadas multiplican el riesgo. Apuesta solo lo que puedas permitirte perder. Si el juego deja de ser un entretenimiento, busca ayuda.

**Modelo** = minutos, tasa por minuto, bajas, defensa rival por posición, zonas de tiro y tipo de defensa, mezclado con el acierto real del jugador sobre esa línea. **Casa** = probabilidad implícita en las cuotas sin el margen. **Prob. final** = mezcla de ambas. Si modelo y casa discrepan mucho, la casa suele saber algo (rol, rotación, una baja): revísalo antes de apostar.

Cada media se construye desde las estadísticas que la producen (tiros × acierto por zona, % de los rebotes disponibles que captura, % de las canastas de sus compañeros que asiste...) y se muestra con esas estadísticas en sus últimos 5 y 10 partidos, la temporada y contra este rival. Todo queda guardado en la tabla `nba_analisis` de la base.

## Estado de calibración

**Listo para dinero real.** 8 de 8 criterios cumplidos:

- ✅ Días con picks liquidados: 23 de 21
- ✅ Props de línea principal: muestra: 279 de 150
- ✅ Props de línea principal: aciertan lo prometido: acierto 71.3% vs prometido 67.3%
- ✅ Picks seguros: muestra: 822 de 150
- ✅ Picks seguros: aciertan lo prometido: acierto 89.2% vs prometido 86.8%
- ✅ Props con cuota: beneficio positivo: +14.00 u en 279
- ✅ Combinadas: muestra: 188 de 30
- ✅ Combinadas: ganan lo prometido: ganadas 37.2% vs prometido 32.6%

## Seguimiento: combinadas de prueba del 2026-11-19

Ganadas 3 de 5 liquidadas.

**Combinada segura B (principales)** — ✅ GANADA (prob. 44%, cuota 2.32)
  - ✅ Rudy Gobert: menos de 1.5 tapones → 0
  - ✅ Derrick Jones Jr.: menos de 1.5 asistencias → 1

**Segura cuota 2+** — ✅ GANADA (prob. 44%, cuota 2.32)
  - ✅ Rudy Gobert: menos de 1.5 tapones → 0
  - ✅ Derrick Jones Jr.: menos de 1.5 asistencias → 1

**Bet builder (New York Knicks @ Minnesota Timberwolves)** — ✅ GANADA (prob. 51%)
  - ✅ Karl-Anthony Towns: más de 2.5 asistencias → 4
  - ✅ Ayo Dosunmu: más de 0.5 triples → 2
  - ✅ OG Anunoby: más de 0.5 triples → 1

**Bet builder (LA Clippers @ San Antonio Spurs)** — ❌ perdida (prob. 46%)
  - ❌ Brook Lopez: más de 3.5 rebotes → 3
  - ❌ Derrick Jones Jr.: más de 0.5 triples → 0
  - ✅ Rui Hachimura: más de 0.5 triples → 2

**Doble de bet builders** — ❌ perdida (prob. 24%)
  - ✅ Karl-Anthony Towns: más de 2.5 asistencias → 4
  - ✅ Ayo Dosunmu: más de 0.5 triples → 2
  - ✅ OG Anunoby: más de 0.5 triples → 1
  - ❌ Brook Lopez: más de 3.5 rebotes → 3
  - ❌ Derrick Jones Jr.: más de 0.5 triples → 0
  - ✅ Rui Hachimura: más de 0.5 triples → 2

### Acumulado de las combinadas de prueba

| Tipo | Jugadas | Ganadas | % ganadas | Prob. prometida | Beneficio (1 u, con cuota) |
|---|---|---|---|---|---|
| Combinada segura A (alternas) | 13 | 9 | 69% | 66% | - |
| Bet builder | 65 | 30 | 46% | 39% | - |
| Segura cuota 10+ | 4 | 0 | 0% | 11% | -4.00 u en 4 |
| Segura cuota 15+ | 2 | 0 | 0% | 7% | -2.00 u en 2 |
| Segura cuota 2+ | 18 | 11 | 61% | 46% | +5.29 u en 18 |
| Segura cuota 3+ | 16 | 8 | 50% | 32% | +9.25 u en 16 |
| Segura cuota 5+ | 13 | 2 | 15% | 20% | -3.64 u en 13 |
| Doble de bet builders | 16 | 3 | 19% | 19% | - |
| Combinada segura B (principales) | 18 | 6 | 33% | 25% | +1.72 u en 18 |
| Rachas de temporada (4 patas) | 5 | 0 | 0% | 16% | -5.00 u en 5 |
| Rachas de temporada (8 patas) | 3 | 0 | 0% | 3% | -3.00 u en 3 |
| Tus apuestas | 39 | 3 | 8% | 12% | -31.28 u en 38 |
| De valor cuota 10+ | 4 | 0 | 0% | 13% | -4.00 u en 4 |
| De valor cuota 15+ | 3 | 1 | 33% | 9% | +12.17 u en 3 |
| De valor cuota 30+ | 2 | 0 | 0% | 5% | -2.00 u en 2 |
| De valor cuota 5+ | 6 | 0 | 0% | 22% | -6.00 u en 6 |

## Bet builders del día

Por partido, 4 "más de" de titulares estables sin alertas, en líneas un poco por debajo de su nivel (cada pierna ~72 %+). La probabilidad de acertar todas tiene en cuenta que los jugadores de un mismo partido se mueven algo juntos. **Cuota justa** = 1 / probabilidad (solo para saber cuánto debería pagar; se elige por probabilidad). Backtest 2025-26: prometían ~32 % y acertaron 38-40 % (conservador).

### Doble: Toronto Raptors @ Detroit Pistons + Houston Rockets @ Denver Nuggets

Probabilidad de acertar los dos bet builders: **20%** (1 de cada 5); cuota justa **5.02**.

**Toronto Raptors @ Detroit Pistons** — acertar las 4: **45%**, cuota justa 2.22

- Immanuel Quickley 5+ asistencias (72%; esperado 6.4; últ. 10: 8/10)
- Scottie Barnes 4+ asistencias (73%; esperado 5.2; últ. 10: 8/10)
- Daniss Jenkins 1+ triples (85%; esperado 2.4; últ. 10: 9/10)

**Houston Rockets @ Denver Nuggets** — acertar las 4: **44%**, cuota justa 2.26

- Kevin Durant 3+ asistencias (77%; esperado 4.3; últ. 10: 9/10)
- Fred VanVleet 2+ triples (74%; esperado 2.7; últ. 10: 10/10)
- Cameron Johnson 1+ triples (76%; esperado 1.6; últ. 10: 8/10)

**Phoenix Suns @ Utah Jazz** — acertar las 4: **38%**, cuota justa 2.61

- Miles Bridges 2+ asistencias (74%; esperado 2.8; últ. 10: 9/10)
- Oso Ighodaro 2+ asistencias (77%; esperado 3.1; últ. 10: 9/10)
- Devin Booker 1+ triples (82%; esperado 2.0; últ. 10: 9/10)
- Dillon Brooks 1+ triples (82%; esperado 2.2; últ. 10: 7/10)

**Orlando Magic @ Brooklyn Nets** — acertar las 4: **38%**, cuota justa 2.65

- Desmond Bane 2+ asistencias (84%; esperado 4.1; últ. 10: 8/10)
- Nolan Traore 1+ triples (73%; esperado 1.5; últ. 10: 8/10)
- Michael Porter Jr. 2+ triples (75%; esperado 2.9; últ. 10: 9/10)
- Anthony Black 1+ triples (81%; esperado 1.9; últ. 10: 9/10)

## Combinada segura del día

**Opción A, líneas alternativas (la más segura):** el pick seguro más probable de cada partido, de titulares estables. Búscalas en las líneas alternativas de tu casa ("15+", "20+"...): cada una vale la pena si paga al menos su cuota mínima.

| Partido | Selección | Prob. | Cuota mínima | Esperado | Últ. 10 |
|---|---|---|---|---|---|
| Charlotte Hornets @ Atlanta Hawks | **Naz Reid: más de 6.5 rebotes** | **79%** | 1.27 | 10.8 | 5/10 |
| Indiana Pacers @ Cleveland Cavaliers | **Andrew Nembhard: más de 22.5 pts+reb+ast** | **78%** | 1.28 | 28.4 | 7/10 |

| Selecciones | Probabilidad de acertar todas |
|---|---|
| 2 | **61%** |

**Opción B, líneas principales con cuota real:**

Se elige por **probabilidad**, no por valor: la más probable de cada partido entre jugadores constantes (titulares con minutos estables, sin cambio de rol, traspaso ni lesión, que la habrían pasado en 7+ de sus últimos 10 y en el 60 %+ de esta temporada) y con cuota real de la casa. Si tu casa no ofrece esa línea, usa la siguiente de la lista "Las más seguras con cuota".

| Partido | Selección | Prob. | Cuota | Últ. 10 | Temporada |
|---|---|---|---|---|---|
| Houston Rockets @ Denver Nuggets | **Amen Thompson: menos de 1.5 robos**<br>el rival concede -7% de robos por minuto a bases/escoltas (defensa fuerte); ajuste aplicado -7% | **70%** | 1.46 | 9/10 | 13/15 |
| Charlotte Hornets @ Atlanta Hawks | **Dyson Daniels: menos de 0.5 tapones**<br>el rival concede -10% de tapones por minuto a bases/escoltas (defensa fuerte); ajuste aplicado -10% | **67%** | 1.44 | 8/10 | 11/15 |
| Orlando Magic @ Brooklyn Nets | **Nolan Traore: menos de 2.5 rebotes**<br>el rival concede +2% de rebotes por minuto a bases/escoltas (defensa media); ajuste aplicado +2% | **64%** | 1.55 | 8/10 | 11/13 |
| New Orleans Pelicans @ Oklahoma City Thunder | **Jared McCain: más de 0.5 robos**<br>el rival concede -6% de robos por minuto a bases/escoltas (defensa fuerte); ajuste aplicado -6% | **62%** | 1.50 | 7/10 | 10/15 |

| Selecciones | Probabilidad de acertar todas | Cuota |
|---|---|---|
| 2 | **47%** | 2.09 |
| 3 | **30%** | 3.23 |
| 4 | **19%** | 4.86 |

**Amen Thompson: menos de 1.5 robos** (70%):

- La pasó en 13 de 15 esta temporada (falló con 4, 2)
- Con 29+ minutos (hoy se esperan 33): 10 de 12 en sus últimos 15
- Contra las ~10 mejores defensas en robos a bases/escoltas: 10 de 14 (últimos 40 partidos)
- Contra defensas fuertes como la de hoy y con 29+ minutos: 11 de 18, con 1.6 de media (últimos 60 partidos)
- El rival es #23 de 30 en robos que concede a bases/escoltas por minuto (#1 = el que más concede; -7% frente a la media)
- Oportunidades de robo (últimos 10): el rival perdió 8.9 balones por partido con él en pista y robó el 12%
- El rival es #28 de 30 en balones que pierde (#1 = el que más; 12.3 por partido)
- Minutos: 33 esperados (titular, ±5)

**Dyson Daniels: menos de 0.5 tapones** (67%):

- La pasó en 11 de 15 esta temporada (falló con 1, 1, 1, 1)
- Con 32+ minutos (hoy se esperan 36): 6 de 6 en sus últimos 15
- Hoy juega más que de costumbre (36 min frente a 32): con 32+ minutos, esta temporada y la pasada, la pasó 35 de 49 (71%)
- Contra las ~10 mejores defensas en tapones a bases/escoltas: 10 de 13 (últimos 40 partidos)
- Contra defensas fuertes como la de hoy y con 32+ minutos: 6 de 10, con 0.4 de media (últimos 60 partidos)
- El rival es #23 de 30 en tapones que concede a bases/escoltas por minuto (#1 = el que más concede; -10% frente a la media)
- Oportunidades de tapón (últimos 10): 32.3 tiros de 2 del rival por partido con él en pista; taponó el 0.6%
- El rival es #30 de 30 en tiros de 2 por partido (#1 = el que más; 44.4)
- El 43% de los tiros del rival son cerca del aro (penetración, corte, poste, palmeo): #25 de 30
- El rival no tiene a Grayson Allen (0.4 tapones por partido)
- Minutos: 36 esperados (titular, ±4)

**Nolan Traore: menos de 2.5 rebotes** (64%):

- La pasó en 11 de 13 esta temporada (falló con 4, 3)
- Con 20+ minutos (hoy se esperan 24): 8 de 10 en sus últimos 15
- Contra las ~10 mejores defensas en rebotes a bases/escoltas: 10 de 14 (últimos 40 partidos)
- Contra defensas medias como la de hoy y con 20+ minutos: 9 de 13, con 1.8 de media (últimos 60 partidos)
- El rival es #11 de 30 en rebotes que concede a bases/escoltas por minuto (#1 = el que más concede; +2% frente a la media)
- El rival es #22 de 30 en rebotes que concede en total (#1 = el que más)
- El rival es #28 de 30 en rebotes ofensivos que concede en total (#1 = el que más)
- Rebotes disponibles con él en pista (últimos 10): 23.1 tiros fallados del rival y 23.6 de su equipo por partido; se queda el 6% y el 1%; el rival falla 46.9 tiros por partido (#21 de 30, #1 = el que más falla)
- Minutos: 24 esperados (titular, ±4)

**Jared McCain: más de 0.5 robos** (62%):

- La pasó en 10 de 15 esta temporada (falló con 0, 0, 0, 0)
- Con 25+ minutos (hoy se esperan 29): 6 de 10 en sus últimos 15
- Contra las ~10 mejores defensas en robos a bases/escoltas: 7 de 20 (últimos 40 partidos)
- Contra defensas fuertes como la de hoy y con 25+ minutos: 3 de 6, con 0.8 de media (últimos 60 partidos)
- El rival es #21 de 30 en robos que concede a bases/escoltas por minuto (#1 = el que más concede; -6% frente a la media)
- Oportunidades de robo (últimos 10): el rival perdió 7.0 balones por partido con él en pista y robó el 16%
- El rival es #18 de 30 en balones que pierde (#1 = el que más; 13.8 por partido)
- El rival no tiene a Dejounte Murray (1.6 robos por partido)
- Minutos: 29 esperados (titular, ±3)

### Las más seguras con cuota

| Partido | Prop | Prob. final | Modelo | Casa | Esperado | Últ. 10 | Temporada | vs este rival | Cuota (implícita) |
|---|---|---|---|---|---|---|---|---|---|
| Houston Rockets @ Denver Nuggets | **Amen Thompson: menos de 1.5 robos** | **70%** | 75% | 64% | 1.0 ± 1.0 | 9/10 | 13/15 | 1, 1, 2, 0, 2 | 1.46 (69%) |
| Charlotte Hornets @ Atlanta Hawks | **Dyson Daniels: menos de 0.5 tapones** | **67%** | 68% | 65% | 0.4 ± 0.6 | 8/10 | 11/15 | 1, 0, 0, 0, 0 | 1.44 (70%) |
| Houston Rockets @ Denver Nuggets | **Cameron Johnson: más de 0.5 robos** | **64%** | 70% | 59% | 1.1 ± 1.1 | 9/10 | 9/10 | 2, 2, 1, 0, 1 | 1.62 (62%) |
| Orlando Magic @ Brooklyn Nets | **Nolan Traore: menos de 2.5 rebotes** | **64%** | 67% | 60% | 2.0 ± 1.5 | 8/10 | 11/13 | 3, 3 | 1.55 (65%) |
| Charlotte Hornets @ Atlanta Hawks | **Onyeka Okongwu: más de 1.5 triples** | **64%** | 67% | 60% | 2.4 ± 1.6 | 9/10 | 10/15 | 2, 3, 4, 0, 2 | 1.56 (64%) |
| Charlotte Hornets @ Atlanta Hawks | **Moussa Diabate: menos de 2.5 asistencias** | **63%** | 66% | 60% | 2.1 ± 1.5 | 8/10 | 9/12 | 1, 2, 2, 1 | 1.55 (65%) |
| Orlando Magic @ Brooklyn Nets | **Day'Ron Sharpe: más de 0.5 tapones** | **63%** | 64% | 62% | 1.2 ± 1.3 | 7/10 | 9/14 | 0, 0, 0 | 1.53 (65%) |
| Charlotte Hornets @ Atlanta Hawks | **Moussa Diabate: más de 0.5 tapones** | **63%** | 63% | 62% | 1.0 ± 1.1 | 7/10 | 8/12 | 1, 0, 0, 0 | 1.49 (67%) |
| New Orleans Pelicans @ Oklahoma City Thunder | **Jared McCain: más de 0.5 robos** | **62%** | 62% | 63% | 1.0 ± 1.0 | 7/10 | 10/15 | 0 | 1.50 (67%) |
| Charlotte Hornets @ Atlanta Hawks | **Coby White: menos de 4.5 asistencias** | **62%** | 67% | 58% | 3.9 ± 2.6 | 9/10 | 6/7 | 4, 5 | 1.62 (62%) |

## Combinadas con cuota objetivo

La combinación de jugadores constantes (mismos filtros que la opción B, partidos distintos) con más probabilidad de acertar todas cuya cuota llega al objetivo. Se registran como picks de prueba y se liquidan solas: `nba rendimiento` dice cuándo el sistema está listo para dinero real. Una cuota alta nunca es segura: cuota 15 justa acierta 1 de cada 15. Lo que la data puede hacer es acercarse o superar esa probabilidad. Se eligen solo por probabilidad de acertar (nunca por valor): como mucho 5 patas, sin "menos" de anotación dudosos.

**Segura, cuota 2+ (2 patas):** cuota 2.09, probabilidad de acertar todas **47%** (1 de cada 2)

- Amen Thompson: menos de 1.5 robos (70%, cuota 1.46) — Houston Rockets @ Denver Nuggets — 6 factores a favor, 0 en contra
  - La pasó en 13 de 15 esta temporada (falló con 4, 2)
  - Con 29+ minutos (hoy se esperan 33): 10 de 12 en sus últimos 15
  - Contra las ~10 mejores defensas en robos a bases/escoltas: 10 de 14 (últimos 40 partidos)
  - Contra defensas fuertes como la de hoy y con 29+ minutos: 11 de 18, con 1.6 de media (últimos 60 partidos)
  - El rival es #23 de 30 en robos que concede a bases/escoltas por minuto (#1 = el que más concede; -7% frente a la media)
  - Oportunidades de robo (últimos 10): el rival perdió 8.9 balones por partido con él en pista y robó el 12%
  - El rival es #28 de 30 en balones que pierde (#1 = el que más; 12.3 por partido)
  - Minutos: 33 esperados (titular, ±5)
- Dyson Daniels: menos de 0.5 tapones (67%, cuota 1.44) — Charlotte Hornets @ Atlanta Hawks — 5 factores a favor, 1 en contra
  - La pasó en 11 de 15 esta temporada (falló con 1, 1, 1, 1)
  - Con 32+ minutos (hoy se esperan 36): 6 de 6 en sus últimos 15
  - Hoy juega más que de costumbre (36 min frente a 32): con 32+ minutos, esta temporada y la pasada, la pasó 35 de 49 (71%)
  - Contra las ~10 mejores defensas en tapones a bases/escoltas: 10 de 13 (últimos 40 partidos)
  - Contra defensas fuertes como la de hoy y con 32+ minutos: 6 de 10, con 0.4 de media (últimos 60 partidos)
  - El rival es #23 de 30 en tapones que concede a bases/escoltas por minuto (#1 = el que más concede; -10% frente a la media)
  - Oportunidades de tapón (últimos 10): 32.3 tiros de 2 del rival por partido con él en pista; taponó el 0.6%
  - El rival es #30 de 30 en tiros de 2 por partido (#1 = el que más; 44.4)
  - El 43% de los tiros del rival son cerca del aro (penetración, corte, poste, palmeo): #25 de 30
  - El rival no tiene a Grayson Allen (0.4 tapones por partido)
  - Minutos: 36 esperados (titular, ±4)

**Segura, cuota 3+ (3 patas):** cuota 3.23, probabilidad de acertar todas **30%** (1 de cada 3)

- Amen Thompson: menos de 1.5 robos (70%, cuota 1.46) — Houston Rockets @ Denver Nuggets — 6 factores a favor, 0 en contra
  - La pasó en 13 de 15 esta temporada (falló con 4, 2)
  - Con 29+ minutos (hoy se esperan 33): 10 de 12 en sus últimos 15
  - Contra las ~10 mejores defensas en robos a bases/escoltas: 10 de 14 (últimos 40 partidos)
  - Contra defensas fuertes como la de hoy y con 29+ minutos: 11 de 18, con 1.6 de media (últimos 60 partidos)
  - El rival es #23 de 30 en robos que concede a bases/escoltas por minuto (#1 = el que más concede; -7% frente a la media)
  - Oportunidades de robo (últimos 10): el rival perdió 8.9 balones por partido con él en pista y robó el 12%
  - El rival es #28 de 30 en balones que pierde (#1 = el que más; 12.3 por partido)
  - Minutos: 33 esperados (titular, ±5)
- Dyson Daniels: menos de 0.5 tapones (67%, cuota 1.44) — Charlotte Hornets @ Atlanta Hawks — 5 factores a favor, 1 en contra
  - La pasó en 11 de 15 esta temporada (falló con 1, 1, 1, 1)
  - Con 32+ minutos (hoy se esperan 36): 6 de 6 en sus últimos 15
  - Hoy juega más que de costumbre (36 min frente a 32): con 32+ minutos, esta temporada y la pasada, la pasó 35 de 49 (71%)
  - Contra las ~10 mejores defensas en tapones a bases/escoltas: 10 de 13 (últimos 40 partidos)
  - Contra defensas fuertes como la de hoy y con 32+ minutos: 6 de 10, con 0.4 de media (últimos 60 partidos)
  - El rival es #23 de 30 en tapones que concede a bases/escoltas por minuto (#1 = el que más concede; -10% frente a la media)
  - Oportunidades de tapón (últimos 10): 32.3 tiros de 2 del rival por partido con él en pista; taponó el 0.6%
  - El rival es #30 de 30 en tiros de 2 por partido (#1 = el que más; 44.4)
  - El 43% de los tiros del rival son cerca del aro (penetración, corte, poste, palmeo): #25 de 30
  - El rival no tiene a Grayson Allen (0.4 tapones por partido)
  - Minutos: 36 esperados (titular, ±4)
- Nolan Traore: menos de 2.5 rebotes (64%, cuota 1.55) — Orlando Magic @ Brooklyn Nets — 4 factores a favor, 2 en contra
  - La pasó en 11 de 13 esta temporada (falló con 4, 3)
  - Con 20+ minutos (hoy se esperan 24): 8 de 10 en sus últimos 15
  - Contra las ~10 mejores defensas en rebotes a bases/escoltas: 10 de 14 (últimos 40 partidos)
  - Contra defensas medias como la de hoy y con 20+ minutos: 9 de 13, con 1.8 de media (últimos 60 partidos)
  - El rival es #11 de 30 en rebotes que concede a bases/escoltas por minuto (#1 = el que más concede; +2% frente a la media)
  - El rival es #22 de 30 en rebotes que concede en total (#1 = el que más)
  - El rival es #28 de 30 en rebotes ofensivos que concede en total (#1 = el que más)
  - Rebotes disponibles con él en pista (últimos 10): 23.1 tiros fallados del rival y 23.6 de su equipo por partido; se queda el 6% y el 1%; el rival falla 46.9 tiros por partido (#21 de 30, #1 = el que más falla)
  - Minutos: 24 esperados (titular, ±4)

**Segura, cuota 5+ (4 patas):** cuota 5.28, probabilidad de acertar todas **18%** (1 de cada 6)

- Amen Thompson: menos de 1.5 robos (70%, cuota 1.46) — Houston Rockets @ Denver Nuggets — 6 factores a favor, 0 en contra
  - La pasó en 13 de 15 esta temporada (falló con 4, 2)
  - Con 29+ minutos (hoy se esperan 33): 10 de 12 en sus últimos 15
  - Contra las ~10 mejores defensas en robos a bases/escoltas: 10 de 14 (últimos 40 partidos)
  - Contra defensas fuertes como la de hoy y con 29+ minutos: 11 de 18, con 1.6 de media (últimos 60 partidos)
  - El rival es #23 de 30 en robos que concede a bases/escoltas por minuto (#1 = el que más concede; -7% frente a la media)
  - Oportunidades de robo (últimos 10): el rival perdió 8.9 balones por partido con él en pista y robó el 12%
  - El rival es #28 de 30 en balones que pierde (#1 = el que más; 12.3 por partido)
  - Minutos: 33 esperados (titular, ±5)
- Nolan Traore: menos de 2.5 rebotes (64%, cuota 1.55) — Orlando Magic @ Brooklyn Nets — 4 factores a favor, 2 en contra
  - La pasó en 11 de 13 esta temporada (falló con 4, 3)
  - Con 20+ minutos (hoy se esperan 24): 8 de 10 en sus últimos 15
  - Contra las ~10 mejores defensas en rebotes a bases/escoltas: 10 de 14 (últimos 40 partidos)
  - Contra defensas medias como la de hoy y con 20+ minutos: 9 de 13, con 1.8 de media (últimos 60 partidos)
  - El rival es #11 de 30 en rebotes que concede a bases/escoltas por minuto (#1 = el que más concede; +2% frente a la media)
  - El rival es #22 de 30 en rebotes que concede en total (#1 = el que más)
  - El rival es #28 de 30 en rebotes ofensivos que concede en total (#1 = el que más)
  - Rebotes disponibles con él en pista (últimos 10): 23.1 tiros fallados del rival y 23.6 de su equipo por partido; se queda el 6% y el 1%; el rival falla 46.9 tiros por partido (#21 de 30, #1 = el que más falla)
  - Minutos: 24 esperados (titular, ±4)
- Onyeka Okongwu: más de 1.5 triples (64%, cuota 1.56) — Charlotte Hornets @ Atlanta Hawks — 7 factores a favor, 0 en contra
  - La pasó en 10 de 15 esta temporada; los fallos, en partidos raros (jugó 28 min, 5 faltas, jugó 29 min, jugó 26 min, jugó 29 min)
  - Con 31+ minutos (hoy se esperan 35): 6 de 6 en sus últimos 15
  - Contra las ~10 mejores defensas en triples a aleros/ala-pívots: 7 de 12 (últimos 40 partidos)
  - Contra defensas débiles como la de hoy y con 31+ minutos: 10 de 14, con 2.3 de media (últimos 60 partidos)
  - El rival es #7 de 30 en triples que concede a aleros/ala-pívots por minuto (#1 = el que más concede; +6% frente a la media)
  - Su zona principal es triple frontal (35% de sus tiros, 37% de acierto); el rival es #2 de 30 en acierto que deja ahí (37%, liga 35%)
  - Cómo tira (últimos 15): recibe y tira 49% (33% de acierto), penetración 22% (65% de acierto), corte 9% (80% de acierto); en recibe y tira el rival es #1 de 30 en lo que deja (#1 = el que más; 1.15 puntos por tiro frente a 1.07 de media)
  - Oportunidades: 5.9 triples intentados esperados al 38%
  - El rival no tiene a Grayson Allen (3.2 triples por partido)
  - Minutos: 35 esperados (titular, ±3)
- Jared McCain: más de 0.5 robos (62%, cuota 1.50) — New Orleans Pelicans @ Oklahoma City Thunder — 3 factores a favor, 2 en contra
  - La pasó en 10 de 15 esta temporada (falló con 0, 0, 0, 0)
  - Con 25+ minutos (hoy se esperan 29): 6 de 10 en sus últimos 15
  - Contra las ~10 mejores defensas en robos a bases/escoltas: 7 de 20 (últimos 40 partidos)
  - Contra defensas fuertes como la de hoy y con 25+ minutos: 3 de 6, con 0.8 de media (últimos 60 partidos)
  - El rival es #21 de 30 en robos que concede a bases/escoltas por minuto (#1 = el que más concede; -6% frente a la media)
  - Oportunidades de robo (últimos 10): el rival perdió 7.0 balones por partido con él en pista y robó el 16%
  - El rival es #18 de 30 en balones que pierde (#1 = el que más; 13.8 por partido)
  - El rival no tiene a Dejounte Murray (1.6 robos por partido)
  - Minutos: 29 esperados (titular, ±3)

## Picks seguros de titulares estables

Líneas bajas (alternativas) de titulares con 30+ minutos: mejor un "15+ puntos" casi seguro de una estrella que la línea normal de un suplente. En el backtest, elegidas al 85 % acertaron el 89-96 %. **Cuota mínima** = la que hace falta para que valga la pena (1 / probabilidad); búscala en las líneas alternativas de tu casa.

| Partido | Jugador | Pick seguro | Prob. | Cuota mínima | Esperado | Últ. 10 |
|---|---|---|---|---|---|---|
| Charlotte Hornets @ Atlanta Hawks | Naz Reid | **más de 6.5 rebotes** | **79%** | 1.27 | 10.8 | 5/10 |
| Indiana Pacers @ Cleveland Cavaliers | Andrew Nembhard | **más de 22.5 pts+reb+ast** | **78%** | 1.28 | 28.4 | 7/10 |

## Las más probables del día

| Partido | Prop | Prob. final | Modelo | Casa | Esperado | Últ. 10 | Temporada | vs este rival | Cuota (implícita) |
|---|---|---|---|---|---|---|---|---|---|
| Orlando Magic @ Brooklyn Nets | **Day'Ron Sharpe: menos de 0.5 triples** | **72%** | 70% | 74% | 0.3 ± 0.6 | 8/10 | 10/14 | 0, 0, 0 | 1.23 (81%) |
| Houston Rockets @ Denver Nuggets | **Amen Thompson: menos de 1.5 robos** | **70%** | 75% | 64% | 1.0 ± 1.0 | 9/10 | 13/15 | 1, 1, 2, 0, 2 | 1.46 (69%) |
| Sacramento Kings @ Los Angeles Lakers | **Ziaire Williams: más de 0.5 triples** ⚠️ suplente | **70%** | 75% | 63% | 1.4 ± 1.2 | 8/10 | 11/13 | 1, 2 | 1.48 (68%) |
| Orlando Magic @ Brooklyn Nets | **Moritz Wagner: más de 0.5 asistencias** ⚠️ suplente | **70%** | 71% | 67% | 1.5 ± 1.3 | 7/10 | 11/14 | - | 1.42 (71%) |
| Houston Rockets @ Denver Nuggets | **Amen Thompson: menos de 0.5 triples** | **69%** | 67% | 73% | 0.5 ± 0.8 | 9/10 | 12/15 | 0, 0, 0, 0, 1 | 1.29 (78%) |
| Charlotte Hornets @ Atlanta Hawks | **Dyson Daniels: menos de 0.5 triples** | **69%** | 71% | 66% | 0.3 ± 0.6 | 9/10 | 13/15 | 0, 0, 0, 0, 1 | 1.40 (71%) |
| New Orleans Pelicans @ Oklahoma City Thunder | **Ajay Mitchell: menos de 1.5 triples** | **68%** | 71% | 65% | 1.1 ± 1.2 | 8/10 | 11/13 | 0, 0 | 1.44 (70%) |
| Toronto Raptors @ Detroit Pistons | **Jamison Battle: menos de 1.5 asistencias** ⚠️ suplente | **67%** | 68% | 66% | 1.2 ± 1.2 | 9/10 | 13/15 | 0 | 1.41 (71%) |
| Toronto Raptors @ Detroit Pistons | **Cade Cunningham: más de 0.5 robos** | **67%** | 68% | 66% | 1.3 ± 1.3 | 7/10 | 10/13 | 2, 3 | 1.44 (69%) |
| Charlotte Hornets @ Atlanta Hawks | **Dyson Daniels: menos de 0.5 tapones** | **67%** | 68% | 65% | 0.4 ± 0.6 | 8/10 | 11/15 | 1, 0, 0, 0, 0 | 1.44 (70%) |
| New Orleans Pelicans @ Oklahoma City Thunder | **Jaylin Williams: menos de 1.5 triples** ⚠️ suplente | **67%** | 68% | 65% | 1.2 ± 1.1 | 9/10 | 7/8 | 0, 0, 4 | 1.43 (70%) |
| Washington Wizards @ Chicago Bulls | **Alex Sarr: más de 1.5 robos+tapones** | **66%** | 69% | 63% | 2.5 ± 1.8 | 7/10 | 11/15 | 3, 0 | 1.52 (66%) |
| Washington Wizards @ Chicago Bulls | **AJ Dybantsa: menos de 1.5 triples** | **66%** | 70% | 62% | 1.2 ± 1.1 | 9/10 | 11/12 | - | 1.51 (66%) |
| Phoenix Suns @ Utah Jazz | **Collin Gillespie: menos de 3.5 rebotes** ⚠️ suplente | **66%** | 71% | 59% | 2.8 ± 1.7 | 9/10 | 12/14 | 3, 3, 3 | 1.56 (64%) |
| New Orleans Pelicans @ Oklahoma City Thunder | **Zion Williamson: más de 0.5 robos** | **66%** | 65% | 66% | 1.2 ± 1.3 | 5/10 | 10/15 | 0, 1 | 1.44 (69%) |
| Charlotte Hornets @ Atlanta Hawks | **Brandon Miller: menos de 3.5 asistencias** | **65%** | 71% | 58% | 2.4 ± 1.7 | 5/10 | 7/12 | 0, 2, 4, 8 | 1.61 (62%) |
| Toronto Raptors @ Detroit Pistons | **Jamal Shead: más de 0.5 triples** ⚠️ suplente | **65%** | 66% | 64% | 1.2 ± 1.1 | 8/10 | 9/15 | 1, 0, 0 | 1.46 (69%) |
| Toronto Raptors @ Detroit Pistons | **Jamison Battle: menos de 2.5 triples** ⚠️ suplente | **65%** | 69% | 58% | 1.8 ± 1.6 | 5/10 | 10/15 | 0 | 1.61 (62%) |

**Si haces combinada:** cada selección que añades multiplica el riesgo. Probabilidad de acertar todas con las más probables de partidos distintos:

- 2 selecciones: **51%**
- 3 selecciones: **35%**
- 4 selecciones: **24%**
- 5 selecciones: **17%**
- 6 selecciones: **11%**

Dentro de un mismo partido (bet builder) las selecciones no son independientes y el cálculo es aún menos fiable. Con 12 selecciones al 65 % la probabilidad de acertar todas es menor del 1 %.

### En qué se basan las 10 más probables

#### Day'Ron Sharpe: menos de 0.5 triples (72%) — Orlando Magic @ Brooklyn Nets

**¿Por qué 0.3 triples?** (línea 0.5; 24.1 minutos esperados)

En corto:

- La pasó en 10 de 14 esta temporada (falló con 2, 1, 1, 1)
- Con 20+ minutos (hoy se esperan 24): 8 de 10 en sus últimos 15
- Contra las ~10 mejores defensas en triples a pívots: 8 de 11 (últimos 40 partidos)
- Contra defensas fuertes como la de hoy y con 20+ minutos: 7 de 9, con 0.2 de media (últimos 60 partidos)
- El rival es #30 de 30 en triples que concede a pívots por minuto (#1 = el que más concede; -28% frente a la media)
- Su zona principal es triple frontal (8% de sus tiros, 31% de acierto); el rival es #16 de 30 en acierto que deja ahí (35%, liga 35%)
- Cómo tira (últimos 15): palmeo 26% (56% de acierto), corte 23% (59% de acierto), recibe y tira 17% (31% de acierto); en palmeo el rival es #30 de 30 en lo que deja (#1 = el que más; 1.09 puntos por tiro frente a 1.17 de media)
- Oportunidades: 1.1 triples intentados esperados al 33%
- Minutos: 24 esperados (titular, ±4)

Razonamiento (5 factores a favor, 0 en contra):

- ✅ Minutos: 24.1 esperados (titular, ±3.6).
- ✅ Forma: 0.4 en sus últimos 5, 0.4 esta temporada (14 partidos), 0.1 la temporada pasada (línea 0.5).
- ➖ Cómo produce triples: 1.1 triples intentados (su ritmo 1.8 por 36'; el rival concede -4% de triples en su reparto) × 33% esperado.
- ✅ Defensa: el rival concede -28% de triples por minuto a pívots (defensa fuerte); ajuste aplicado -15%; en su zona principal (triple) el rival concede 35% (liga 35%).
- ➖ Ritmo del partido: -1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 0, 0, 0 (3 de 3 a favor).
- ✅ Últimos 10: la habría pasado 8 de 10.

- Triples **0.3** (por componentes 0.4 · por tasa por minuto y defensa rival 0.3): 1.1 triples intentados (su ritmo 1.8 por 36'; el rival concede -4% de triples en su reparto) × 33% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 22.8 | 24.5 | 23.6 | 18.7 | 19.0 |
| Triples anotados | 0.4 | 0.3 | 0.4 | 0.1 | 0.0 |
| Triples intentados | 1.2 | 1.2 | 1.1 | 0.6 | 0.3 |
| % triples | 33.3% | 25.0% | 31.2% | 23.1% | 0.0% |

#### Amen Thompson: menos de 1.5 robos (70%) — Houston Rockets @ Denver Nuggets

**¿Por qué 1.0 robos?** (línea 1.5; 32.7 minutos esperados)

En corto:

- La pasó en 13 de 15 esta temporada (falló con 4, 2)
- Con 29+ minutos (hoy se esperan 33): 10 de 12 en sus últimos 15
- Contra las ~10 mejores defensas en robos a bases/escoltas: 10 de 14 (últimos 40 partidos)
- Contra defensas fuertes como la de hoy y con 29+ minutos: 11 de 18, con 1.6 de media (últimos 60 partidos)
- El rival es #23 de 30 en robos que concede a bases/escoltas por minuto (#1 = el que más concede; -7% frente a la media)
- Oportunidades de robo (últimos 10): el rival perdió 8.9 balones por partido con él en pista y robó el 12%
- El rival es #28 de 30 en balones que pierde (#1 = el que más; 12.3 por partido)
- Minutos: 33 esperados (titular, ±5)

Razonamiento (6 factores a favor, 0 en contra):

- ✅ Minutos: 32.7 esperados (titular, ±4.8).
- ✅ Forma: 0.8 en sus últimos 5, 1.1 esta temporada (15 partidos), 1.6 la temporada pasada (línea 1.5).
- ➖ Cómo produce robos: roba el 12.1% de las pérdidas del rival en pista × 11.5 pérdidas esperadas del rival.
- ✅ Defensa: el rival concede -7% de robos por minuto a bases/escoltas (defensa fuerte); ajuste aplicado -7%.
- ✅ Ritmo del partido: -2% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 1, 1, 2, 0, 2 (3 de 5 a favor).
- ✅ Últimos 10: la habría pasado 9 de 10.

- Robos **1.0** (por componentes 1.0 · por tasa por minuto y defensa rival 1.1): roba el 12.1% de las pérdidas del rival en pista × 11.5 pérdidas esperadas del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 33.0 | 32.8 | 33.1 | 37.9 | 38.0 |
| Robos | 0.8 | 1.1 | 1.1 | 1.5 | 1.2 |
| % de las pérdidas del rival que roba | 10.5% | 12.4% | 10.8% | 14.9% | 15.4% |

#### Ziaire Williams: más de 0.5 triples (70%) — Sacramento Kings @ Los Angeles Lakers

**¿Por qué 1.4 triples?** (línea 0.5; 22.0 minutos esperados)

En corto:

- La pasó en 11 de 13 esta temporada (falló con 0, 0)
- Con 18+ minutos (hoy se esperan 22): 11 de 13 en sus últimos 15
- Contra las ~10 mejores defensas en triples a aleros/ala-pívots: 10 de 14 (últimos 40 partidos)
- Contra defensas medias como la de hoy y con 18+ minutos: 14 de 17, con 1.3 de media (últimos 60 partidos)
- El rival es #11 de 30 en triples que concede a aleros/ala-pívots por minuto (#1 = el que más concede; +3% frente a la media)
- Su zona principal es triple frontal (36% de sus tiros, 36% de acierto); el rival es #1 de 30 en acierto que deja ahí (37%, liga 35%)
- Su segunda zona es triple de esquina (22% de sus tiros, 39% de acierto); el rival es #2 de 30 en acierto que deja ahí (40%, liga 38%)
- Cómo tira (últimos 15): recibe y tira 49% (46% de acierto), penetración 28% (56% de acierto), creado 12% (33% de acierto); en recibe y tira el rival es #12 de 30 en lo que deja (#1 = el que más; 1.10 puntos por tiro frente a 1.07 de media)
- Oportunidades: 3.3 triples intentados esperados al 39%
- Su equipo no tiene a Austin Reaves: más tiros y balón para él
- Minutos: 22 esperados (suplente, ±4)

Razonamiento (4 factores a favor, 1 en contra):

- ❌ Minutos: 22.0 esperados (suplente, ±3.5).
- ✅ Forma: 0.8 en sus últimos 5, 1.6 esta temporada (13 partidos), 1.5 la temporada pasada (línea 0.5).
- ➖ Cómo produce triples: 3.3 triples intentados (su ritmo 5.7 por 36'; el rival concede -1% de triples en su reparto) × 39% esperado.
- ✅ Defensa: el rival concede +3% de triples por minuto a aleros/ala-pívots (defensa media); ajuste aplicado +4%; en su zona principal (triple) el rival concede 37% (liga 35%).
- ➖ Ritmo del partido: +1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 1, 2 (2 de 2 a favor).
- ✅ Últimos 10: la habría pasado 8 de 10.
- ⚠️ sin Austin Reaves, la estrella de su equipo (4 partidos suyos sin él): más tiros y balón para él por minuto (puntos +1%, triples -3%, asistencias +3%).
- ⚠️ Austin Reaves ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ partido desigual (favorito por 14.5): los suplentes suelen jugar +4% de minutos si se rompe.

- ⚠️ Alertas: suplente, riesgo de paliza.
- Triples **1.4** (por componentes 1.3 · por tasa por minuto y defensa rival 1.5): 3.3 triples intentados (su ritmo 5.7 por 36'; el rival concede -1% de triples en su reparto) × 39% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 21.8 | 21.7 | 23.2 | 22.9 | 22.5 |
| Triples anotados | 0.8 | 1.6 | 1.6 | 1.5 | 1.5 |
| Triples intentados | 2.0 | 3.5 | 3.6 | 4.5 | 3.5 |
| % triples | 40.0% | 45.7% | 44.7% | 34.3% | 42.9% |

#### Moritz Wagner: más de 0.5 asistencias (70%) — Orlando Magic @ Brooklyn Nets

**¿Por qué 1.5 asistencias?** (línea 0.5; 17.3 minutos esperados)

En corto:

- La pasó en 11 de 14 esta temporada (falló con 0, 0, 0)
- Con 13+ minutos (hoy se esperan 17): 10 de 13 en sus últimos 15
- Contra las ~10 mejores defensas en asistencias a pívots: 7 de 14 (últimos 40 partidos)
- Contra defensas medias como la de hoy y con 13+ minutos: 5 de 7, con 1.0 de media (últimos 60 partidos)
- El rival es #16 de 30 en asistencias que concede a pívots por minuto (#1 = el que más concede; -2% frente a la media)
- Asistencias esperadas: 1.8 por partido si sus compañeros metieran lo normal (tiene 1.6; con él en pista metieron el 89% de lo esperado por tipo de tiro, últimos 10); ajuste aplicado +6.4%
- Oportunidades: asiste el 12% de las canastas de sus compañeros con él en pista
- Minutos: 17 esperados (suplente, ±4)

Razonamiento (2 factores a favor, 1 en contra):

- ❌ Minutos: 17.3 esperados (suplente, ±3.8).
- ✅ Forma: 2.6 en sus últimos 5, 1.6 esta temporada (14 partidos), 0.7 la temporada pasada (línea 0.5).
- ➖ Cómo produce asistencias: asiste el 12.0% de las canastas de sus compañeros en pista × 10.2 canastas de compañeros esperadas (su equipo 36.7 por 48' contra esta defensa).
- ➖ Defensa: el rival concede -2% de asistencias por minuto a pívots (defensa media); ajuste aplicado -2%.
- ➖ Ritmo del partido: -1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Últimos 10: la habría pasado 7 de 10.

- ⚠️ Alertas: suplente.
- Asistencias **1.5** (por componentes 1.2 · por tasa por minuto y defensa rival 1.4): asiste el 12.0% de las canastas de sus compañeros en pista × 10.2 canastas de compañeros esperadas (su equipo 36.7 por 48' contra esta defensa).

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 16.6 | 18.3 | 17.9 | 11.4 | - |
| Asistencias | 2.6 | 1.6 | 1.6 | 0.7 | - |
| % de las canastas de compañeros que asiste | 20.9% | 12.8% | 12.7% | 7.9% | - |
| Pérdidas por jugada | 14.2% | 10.4% | 11.5% | 7.9% | - |

#### Amen Thompson: menos de 0.5 triples (69%) — Houston Rockets @ Denver Nuggets

**¿Por qué 0.5 triples?** (línea 0.5; 32.7 minutos esperados)

En corto:

- La pasó en 12 de 15 esta temporada (falló con 3, 1, 1)
- Con 29+ minutos (hoy se esperan 33): 9 de 12 en sus últimos 15
- Contra las ~10 mejores defensas en triples a bases/escoltas: 10 de 13 (últimos 40 partidos)
- Contra defensas medias como la de hoy y con 29+ minutos: 16 de 20, con 0.2 de media (últimos 60 partidos)
- El rival es #16 de 30 en triples que concede a bases/escoltas por minuto (#1 = el que más concede; -1% frente a la media)
- Su zona principal es triple de esquina (7% de sus tiros, 29% de acierto); el rival es #27 de 30 en acierto que deja ahí (37%, liga 38%)
- Cómo tira (últimos 15): penetración 41% (56% de acierto), corte 17% (83% de acierto), recibe y tira 13% (33% de acierto); en penetración el rival es #15 de 30 en lo que deja (#1 = el que más; 1.09 puntos por tiro frente a 1.08 de media)
- Oportunidades: 1.8 triples intentados esperados al 28%
- Minutos: 33 esperados (titular, ±5)

Razonamiento (4 factores a favor, 2 en contra):

- ✅ Minutos: 32.7 esperados (titular, ±4.8).
- ❌ Forma: 0.6 en sus últimos 5, 0.3 esta temporada (15 partidos), 0.3 la temporada pasada (línea 0.5).
- ➖ Cómo produce triples: 1.8 triples intentados (su ritmo 1.9 por 36'; el rival concede +2% de triples en su reparto) × 28% esperado.
- ➖ Defensa: el rival concede -1% de triples por minuto a bases/escoltas (defensa media); ajuste aplicado -2%; en su zona principal (esquina3) el rival concede 37% (liga 38%).
- ❌ Altura: mide 6'7", 2.4 pulgadas más que los bases/escoltas del rival (+0.8% en esta estadística).
- ✅ Ritmo del partido: -2% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 0, 0, 0, 0, 1 (4 de 5 a favor).
- ✅ Últimos 10: la habría pasado 9 de 10.

- Triples **0.5** (por componentes 0.5 · por tasa por minuto y defensa rival 0.4): 1.8 triples intentados (su ritmo 1.9 por 36'; el rival concede +2% de triples en su reparto) × 28% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 33.0 | 32.8 | 33.1 | 37.9 | 38.0 |
| Triples anotados | 0.6 | 0.3 | 0.3 | 0.3 | 0.2 |
| Triples intentados | 1.2 | 0.9 | 1.0 | 1.5 | 1.2 |
| % triples | 50.0% | 33.3% | 33.3% | 21.8% | 16.7% |

#### Dyson Daniels: menos de 0.5 triples (69%) — Charlotte Hornets @ Atlanta Hawks

**¿Por qué 0.3 triples?** (línea 0.5; 35.7 minutos esperados)

En corto:

- La pasó en 13 de 15 esta temporada (falló con 1, 1)
- Con 32+ minutos (hoy se esperan 36): 6 de 6 en sus últimos 15
- Hoy juega más que de costumbre (36 min frente a 32): con 32+ minutos, esta temporada y la pasada, la pasó 35 de 49 (71%)
- Contra las ~10 mejores defensas en triples a bases/escoltas: 10 de 13 (últimos 40 partidos)
- Contra defensas fuertes como la de hoy y con 32+ minutos: 9 de 12, con 0.2 de media (últimos 60 partidos)
- El rival es #27 de 30 en triples que concede a bases/escoltas por minuto (#1 = el que más concede; -7% frente a la media)
- Su zona principal es triple frontal (11% de sus tiros, 23% de acierto); el rival es #2 de 30 en acierto que deja ahí (37%, liga 35%)
- Cómo tira (últimos 15): penetración 52% (54% de acierto), recibe y tira 15% (20% de acierto), palmeo 11% (47% de acierto); en penetración el rival es #14 de 30 en lo que deja (#1 = el que más; 1.09 puntos por tiro frente a 1.08 de media)
- Oportunidades: 1.7 triples intentados esperados al 25%
- El rival no tiene a Grayson Allen (3.2 triples por partido)
- Minutos: 36 esperados (titular, ±4)

Razonamiento (5 factores a favor, 2 en contra):

- ✅ Minutos: 35.7 esperados (titular, ±3.7).
- ✅ Forma: 0.2 en sus últimos 5, 0.1 esta temporada (15 partidos), 0.3 la temporada pasada (línea 0.5).
- ➖ Cómo produce triples: 1.7 triples intentados (su ritmo 2.4 por 36'; el rival concede -2% de triples en su reparto) × 25% esperado.
- ✅ Defensa: el rival concede -7% de triples por minuto a bases/escoltas (defensa fuerte); ajuste aplicado -2%; en su zona principal (triple) el rival concede 37% (liga 35%).
- ❌ Altura: mide 6'7", 3.6 pulgadas más que los bases/escoltas del rival (+1.3% en esta estadística).
- ➖ Ritmo del partido: +1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 0, 0, 0, 0, 1 (4 de 5 a favor).
- ✅ Últimos 10: la habría pasado 9 de 10.
- ❌ Bajas del rival: sin Grayson Allen (titular); +1.7% en esta estadística.
- ⚠️ sin CJ McCollum (38 partidos): 34.5 min vs 31.2 con él; reb -13%/min.

- Triples **0.3** (por componentes 0.4 · por tasa por minuto y defensa rival 0.3): 1.7 triples intentados (su ritmo 2.4 por 36'; el rival concede -2% de triples en su reparto) × 25% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 32.4 | 32.1 | 30.9 | 32.8 | 29.4 |
| Triples anotados | 0.2 | 0.1 | 0.1 | 0.3 | 0.2 |
| Triples intentados | 0.8 | 1.3 | 1.3 | 1.6 | 1.8 |
| % triples | 25.0% | 7.7% | 10.5% | 19.8% | 11.1% |

#### Ajay Mitchell: menos de 1.5 triples (68%) — New Orleans Pelicans @ Oklahoma City Thunder

**¿Por qué 1.1 triples?** (línea 1.5; 28.5 minutos esperados)

En corto:

- La pasó en 11 de 13 esta temporada; los fallos, en partidos raros (paliza de 31, paliza de 24)
- Con 24+ minutos (hoy se esperan 28): 9 de 11 en sus últimos 15
- Contra las ~10 mejores defensas en triples a bases/escoltas: 10 de 12 (últimos 40 partidos)
- Contra defensas débiles como la de hoy y con 24+ minutos: 9 de 13, con 1.2 de media (últimos 60 partidos)
- El rival es #4 de 30 en triples que concede a bases/escoltas por minuto (#1 = el que más concede; +9% frente a la media)
- Su zona principal es triple frontal (20% de sus tiros, 31% de acierto); el rival es #26 de 30 en acierto que deja ahí (34%, liga 35%)
- Cómo tira (últimos 15): penetración 53% (56% de acierto), creado 22% (51% de acierto), recibe y tira 18% (26% de acierto); en penetración el rival es #2 de 30 en lo que deja (#1 = el que más; 1.19 puntos por tiro frente a 1.08 de media)
- Oportunidades: 3.8 triples intentados esperados al 32%
- El rival no tiene a Dejounte Murray (0.8 triples por partido)
- Minutos: 28 esperados (titular, ±4)

Razonamiento (4 factores a favor, 2 en contra):

- ✅ Minutos: 28.5 esperados (titular, ±4.0).
- ✅ Forma: 1.0 en sus últimos 5, 0.8 esta temporada (13 partidos), 1.1 la temporada pasada (línea 1.5).
- ➖ Cómo produce triples: 3.8 triples intentados (su ritmo 4.5 por 36'; el rival concede +5% de triples en su reparto) × 32% esperado.
- ❌ Defensa: el rival concede +9% de triples por minuto a bases/escoltas (defensa débil); ajuste aplicado +3%; en su zona principal (triple) el rival concede 34% (liga 35%).
- ➖ Ritmo del partido: +1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 0, 0 (2 de 2 a favor).
- ✅ Últimos 10: la habría pasado 8 de 10.
- ❌ Bajas del rival: sin Dejounte Murray (titular); +1.7% en esta estadística.
- ⚠️ Chet Holmgren ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ Jalen Williams ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ Cason Wallace ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ partido desigual (favorito por 11.5): los titulares suelen jugar -3% de minutos si se rompe.

- Triples **1.1** (por componentes 1.2 · por tasa por minuto y defensa rival 1.1): 3.8 triples intentados (su ritmo 4.5 por 36'; el rival concede +5% de triples en su reparto) × 32% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 28.2 | 28.7 | 27.8 | 26.3 | 28.0 |
| Triples anotados | 1.0 | 0.9 | 0.8 | 1.1 | 0.0 |
| Triples intentados | 3.2 | 3.3 | 3.1 | 3.2 | 3.5 |
| % triples | 31.2% | 27.3% | 25.0% | 34.3% | 0.0% |

#### Jamison Battle: menos de 1.5 asistencias (67%) — Toronto Raptors @ Detroit Pistons

**¿Por qué 1.2 asistencias?** (línea 1.5; 21.7 minutos esperados)

En corto:

- La pasó en 13 de 15 esta temporada (falló con 2, 2)
- Con 18+ minutos (hoy se esperan 22): 8 de 9 en sus últimos 15
- Contra las ~10 mejores defensas en asistencias a aleros/ala-pívots: 11 de 12 (últimos 40 partidos)
- El rival es #26 de 30 en asistencias que concede a aleros/ala-pívots por minuto (#1 = el que más concede; -6% frente a la media)
- Asistencias esperadas: 0.3 por partido si sus compañeros metieran lo normal (tiene 0.3; con él en pista metieron el 90% de lo esperado por tipo de tiro, últimos 10); ajuste aplicado +5.8%
- Oportunidades: asiste el 4% de las canastas de sus compañeros con él en pista
- Su equipo no tiene a RJ Barrett: más tiros y balón para él
- Minutos: 22 esperados (suplente, ±10)

Razonamiento (4 factores a favor, 1 en contra):

- ❌ Minutos: 21.7 esperados (suplente, ±10.0).
- ✅ Forma: 0.2 en sus últimos 5, 0.4 esta temporada (15 partidos), 0.4 la temporada pasada (línea 1.5).
- ➖ Cómo produce asistencias: asiste el 4.4% de las canastas de sus compañeros en pista × 14.4 canastas de compañeros esperadas (su equipo 37.9 por 48' contra esta defensa).
- ✅ Defensa: el rival concede -6% de asistencias por minuto a aleros/ala-pívots (defensa fuerte); ajuste aplicado -6%.
- ➖ Ritmo del partido: -1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 0 (1 de 1 a favor).
- ✅ Últimos 10: la habría pasado 9 de 10.
- ⚠️ sin RJ Barrett, la estrella de su equipo (20 partidos suyos sin él): más tiros y balón para él por minuto (puntos -10%, triples -15%, asistencias +40%).
- ⚠️ sin RJ Barrett (20 partidos): 11.8 min vs 10.4 con él.
- ⚠️ sin Collin Murray-Boyles (23 partidos): 9.5 min vs 11.3 con él; pts -8%/min, ast +35%/min.
- ⚠️ Kawhi Leonard ya no jugó en sus últimos partidos: la baja ya está en sus minutos.

- ⚠️ Alertas: suplente, minutos inestables, sin RJ Barrett: más tiros para él.
- Asistencias **1.2** (por componentes 1.2 · por tasa por minuto y defensa rival 1.2): asiste el 4.4% de las canastas de sus compañeros en pista × 14.4 canastas de compañeros esperadas (su equipo 37.9 por 48' contra esta defensa).

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 19.6 | 20.5 | 18.7 | 9.0 | 4.0 |
| Asistencias | 0.2 | 0.3 | 0.4 | 0.4 | 0.0 |
| % de las canastas de compañeros que asiste | 1.5% | 2.0% | 2.8% | 5.0% | 0.0% |
| Pérdidas por jugada | 2.6% | 4.5% | 5.3% | 10.5% | - |

#### Cade Cunningham: más de 0.5 robos (67%) — Toronto Raptors @ Detroit Pistons

**¿Por qué 1.3 robos?** (línea 0.5; 36.8 minutos esperados)

En corto:

- La pasó en 10 de 13 esta temporada (falló con 0, 0, 0)
- Con 33+ minutos (hoy se esperan 37): 8 de 11 en sus últimos 15
- Contra las ~10 mejores defensas en robos a bases/escoltas: 15 de 20 (últimos 40 partidos)
- Contra defensas fuertes como la de hoy y con 33+ minutos: 17 de 24, con 1.2 de media (últimos 60 partidos)
- El rival es #24 de 30 en robos que concede a bases/escoltas por minuto (#1 = el que más concede; -7% frente a la media)
- Oportunidades de robo (últimos 10): el rival perdió 12.3 balones por partido con él en pista y robó el 11%
- El rival es #24 de 30 en balones que pierde (#1 = el que más; 12.9 por partido)
- El rival no tiene a RJ Barrett (0.2 robos por partido)
- Minutos: 37 esperados (titular, ±6)

Razonamiento (3 factores a favor, 2 en contra):

- ❌ Minutos: 36.8 esperados (titular, ±6.3).
- ✅ Forma: 1.0 en sus últimos 5, 1.4 esta temporada (13 partidos), 1.3 la temporada pasada (línea 0.5).
- ➖ Cómo produce robos: roba el 12.1% de las pérdidas del rival en pista × 14.5 pérdidas esperadas del rival.
- ❌ Defensa: el rival concede -7% de robos por minuto a bases/escoltas (defensa fuerte); ajuste aplicado -7%.
- ➖ Ritmo del partido: -1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 2, 3 (2 de 2 a favor).
- ✅ Últimos 10: la habría pasado 7 de 10.
- ⚠️ en el parte de lesiones: day-to-day.

- ⚠️ Alertas: minutos inestables, en el parte de lesiones.
- Robos **1.3** (por componentes 1.3 · por tasa por minuto y defensa rival 1.2): roba el 12.1% de las pérdidas del rival en pista × 14.5 pérdidas esperadas del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 37.4 | 35.7 | 35.0 | 33.9 | 33.5 |
| Robos | 1.0 | 1.4 | 1.4 | 1.4 | 2.5 |
| % de las pérdidas del rival que roba | 8.8% | 11.4% | 12.2% | 12.4% | 26.3% |

#### Dyson Daniels: menos de 0.5 tapones (67%) — Charlotte Hornets @ Atlanta Hawks

**¿Por qué 0.4 tapones?** (línea 0.5; 35.7 minutos esperados)

En corto:

- La pasó en 11 de 15 esta temporada (falló con 1, 1, 1, 1)
- Con 32+ minutos (hoy se esperan 36): 6 de 6 en sus últimos 15
- Hoy juega más que de costumbre (36 min frente a 32): con 32+ minutos, esta temporada y la pasada, la pasó 35 de 49 (71%)
- Contra las ~10 mejores defensas en tapones a bases/escoltas: 10 de 13 (últimos 40 partidos)
- Contra defensas fuertes como la de hoy y con 32+ minutos: 6 de 10, con 0.4 de media (últimos 60 partidos)
- El rival es #23 de 30 en tapones que concede a bases/escoltas por minuto (#1 = el que más concede; -10% frente a la media)
- Oportunidades de tapón (últimos 10): 32.3 tiros de 2 del rival por partido con él en pista; taponó el 0.6%
- El rival es #30 de 30 en tiros de 2 por partido (#1 = el que más; 44.4)
- El 43% de los tiros del rival son cerca del aro (penetración, corte, poste, palmeo): #25 de 30
- El rival no tiene a Grayson Allen (0.4 tapones por partido)
- Minutos: 36 esperados (titular, ±4)

Razonamiento (5 factores a favor, 1 en contra):

- ✅ Minutos: 35.7 esperados (titular, ±3.7).
- ✅ Forma: 0.2 en sus últimos 5, 0.3 esta temporada (15 partidos), 0.4 la temporada pasada (línea 0.5).
- ➖ Cómo produce tapones: tapona el 0.9% de los tiros de 2 del rival en pista × 45.5 tiros de 2 esperados del rival.
- ✅ Defensa: el rival concede -10% de tapones por minuto a bases/escoltas (defensa fuerte); ajuste aplicado -10%.
- ❌ Altura: mide 6'7", 3.6 pulgadas más que los bases/escoltas del rival (+2.7% en esta estadística).
- ➖ Ritmo del partido: +1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 1, 0, 0, 0, 0 (4 de 5 a favor).
- ✅ Últimos 10: la habría pasado 8 de 10.
- ⚠️ sin CJ McCollum (38 partidos): 34.5 min vs 31.2 con él; reb -13%/min.

- Tapones **0.4** (por componentes 0.4 · por tasa por minuto y defensa rival 0.4): tapona el 0.9% de los tiros de 2 del rival en pista × 45.5 tiros de 2 esperados del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 32.4 | 32.1 | 30.9 | 32.8 | 29.4 |
| Tapones | 0.2 | 0.2 | 0.3 | 0.4 | 0.2 |
| % de los tiros de 2 del rival que tapona | 0.6% | 0.6% | 0.9% | 1.1% | 0.8% |


## Charlotte Hornets @ Atlanta Hawks

Diferencia esperada: Atlanta Hawks por 6.5.

Parte de lesiones: CJ McCollum (Out); Dennis Schroder (Out); Grayson Allen (Out); Jock Landale (Out); Grant Williams (Out); Mouhamed Gueye (Out); Asa Newell (Out); Kon Knueppel (Out); Kingston Flemings (Day-To-Day).

Ventajas del partido (los dos lados): puntos esperados frente a su media de los últimos 10, ajuste por la defensa rival y diferencia de estatura con los rivales de su posición.

| Equipo | Jugador | Puntos esperados | Su media (últ. 10) | Defensa rival en puntos | Rebotes esperados | Altura vs rival |
|---|---|---|---|---|---|---|
| ATL | Jalen Johnson | 23.0 | 19.1 | -0% | 9.2 | -0.1" |
| ATL | Dyson Daniels | 12.3 | 8.3 | -2% | 7.0 | +3.6" |
| ATL | Onyeka Okongwu | 18.2 | 17.7 | +0% | 8.4 | +1.9" |
| ATL | Nickeil Alexander-Walker | 21.8 | 22.0 | -1% | 4.1 | +1.6" |
| CHA | Sion James | 10.2 | 6.7 | -1% | 3.9 | +0.3" |
| CHA | Naz Reid | 19.6 | 16.9 | +1% | 10.8 | -2.0" |
| CHA | Moussa Diabate | 11.2 | 8.2 | +1% | 9.9 | +1.2" |
| CHA | Brandon Miller | 18.3 | 21.5 | +1% | 4.1 | -1.8" |
| ATL | Aaron Wiggins | 13.1 | 13.6 | -1% | 3.5 | +1.6" |
| CHA | Royce O'Neale | 7.3 | 6.6 | +1% | 4.5 | -2.8" |

Picks seguros de titulares estables:

| Jugador | Pick seguro | Prob. | Cuota mínima | Esperado | Últ. 10 |
|---|---|---|---|---|---|
| Naz Reid | **más de 6.5 rebotes** | **79%** | 1.27 | 10.8 | 5/10 |

Las 8 más probables (máximo 2 por jugador: las de un mismo jugador suelen ganar o perder juntas).

| Prop | Prob. final | Modelo | Casa | Esperado | Últ. 10 | Temporada | vs este rival | Cuota (implícita) |
|---|---|---|---|---|---|---|---|---|
| **Dyson Daniels: menos de 0.5 triples** | **69%** | 71% | 66% | 0.3 ± 0.6 | 9/10 | 13/15 | 0, 0, 0, 0, 1 | 1.40 (71%) |
| **Dyson Daniels: menos de 0.5 tapones** | **67%** | 68% | 65% | 0.4 ± 0.6 | 8/10 | 11/15 | 1, 0, 0, 0, 0 | 1.44 (70%) |
| **Brandon Miller: menos de 3.5 asistencias** | **65%** | 71% | 58% | 2.4 ± 1.7 | 5/10 | 7/12 | 0, 2, 4, 8 | 1.61 (62%) |
| **Onyeka Okongwu: más de 1.5 triples** | **64%** | 67% | 60% | 2.4 ± 1.6 | 9/10 | 10/15 | 2, 3, 4, 0, 2 | 1.56 (64%) |
| **Coby White: menos de 21.5 pts+ast** | **64%** | 79% | 52% | 15.1 ± 6.0 | 6/10 | 4/7 | 28, 26 | 1.80 (56%) |
| **Naz Reid: más de 7.5 rebotes** | **64%** | 72% | 52% | 10.8 ± 4.0 | 5/10 | 8/14 | 6, 6, 7 | 1.80 (56%) |
| **Nickeil Alexander-Walker: menos de 1.5 robos** | **63%** | 66% | 59% | 1.2 ± 1.1 | 6/10 | 9/15 | 2, 1, 1, 0, 1 | 1.57 (63%) |
| **Moussa Diabate: menos de 2.5 asistencias** | **63%** | 66% | 60% | 2.1 ± 1.5 | 8/10 | 9/12 | 1, 2, 2, 1 | 1.55 (65%) |

### Fichas de los jugadores destacados

#### Dyson Daniels (bases/escoltas) vs Charlotte Hornets

- Minutos esperados: **35.7** (± 3.7); 97 partidos en la base.
- sin CJ McCollum (38 partidos): 34.5 min vs 31.2 con él; reb -13%/min
- Su prop más probable hoy: **Dyson Daniels: menos de 0.5 triples** (69%). Con 80% de probabilidad: más de - / menos de 1.5.
- Defensa de Charlotte Hornets contra bases/escoltas en triples: -2% respecto a la media; ajuste por su historial contra defensas similares: -13%.

**¿Por qué 0.3 triples?** (línea 0.5; 35.7 minutos esperados)

En corto:

- La pasó en 13 de 15 esta temporada (falló con 1, 1)
- Con 32+ minutos (hoy se esperan 36): 6 de 6 en sus últimos 15
- Hoy juega más que de costumbre (36 min frente a 32): con 32+ minutos, esta temporada y la pasada, la pasó 35 de 49 (71%)
- Contra las ~10 mejores defensas en triples a bases/escoltas: 10 de 13 (últimos 40 partidos)
- Contra defensas fuertes como la de hoy y con 32+ minutos: 9 de 12, con 0.2 de media (últimos 60 partidos)
- El rival es #27 de 30 en triples que concede a bases/escoltas por minuto (#1 = el que más concede; -7% frente a la media)
- Su zona principal es triple frontal (11% de sus tiros, 23% de acierto); el rival es #2 de 30 en acierto que deja ahí (37%, liga 35%)
- Cómo tira (últimos 15): penetración 52% (54% de acierto), recibe y tira 15% (20% de acierto), palmeo 11% (47% de acierto); en penetración el rival es #14 de 30 en lo que deja (#1 = el que más; 1.09 puntos por tiro frente a 1.08 de media)
- Oportunidades: 1.7 triples intentados esperados al 25%
- El rival no tiene a Grayson Allen (3.2 triples por partido)
- Minutos: 36 esperados (titular, ±4)

Razonamiento (5 factores a favor, 2 en contra):

- ✅ Minutos: 35.7 esperados (titular, ±3.7).
- ✅ Forma: 0.2 en sus últimos 5, 0.1 esta temporada (15 partidos), 0.3 la temporada pasada (línea 0.5).
- ➖ Cómo produce triples: 1.7 triples intentados (su ritmo 2.4 por 36'; el rival concede -2% de triples en su reparto) × 25% esperado.
- ✅ Defensa: el rival concede -7% de triples por minuto a bases/escoltas (defensa fuerte); ajuste aplicado -2%; en su zona principal (triple) el rival concede 37% (liga 35%).
- ❌ Altura: mide 6'7", 3.6 pulgadas más que los bases/escoltas del rival (+1.3% en esta estadística).
- ➖ Ritmo del partido: +1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 0, 0, 0, 0, 1 (4 de 5 a favor).
- ✅ Últimos 10: la habría pasado 9 de 10.
- ❌ Bajas del rival: sin Grayson Allen (titular); +1.7% en esta estadística.
- ⚠️ sin CJ McCollum (38 partidos): 34.5 min vs 31.2 con él; reb -13%/min.

- Triples **0.3** (por componentes 0.4 · por tasa por minuto y defensa rival 0.3): 1.7 triples intentados (su ritmo 2.4 por 36'; el rival concede -2% de triples en su reparto) × 25% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 32.4 | 32.1 | 30.9 | 32.8 | 29.4 |
| Triples anotados | 0.2 | 0.1 | 0.1 | 0.3 | 0.2 |
| Triples intentados | 0.8 | 1.3 | 1.3 | 1.6 | 1.8 |
| % triples | 25.0% | 7.7% | 10.5% | 19.8% | 11.1% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +5%, vs defensa media +9%, vs defensa débil -14%; rebotes: vs defensa fuerte -6%, vs defensa media +1%, vs defensa débil +7%; asistencias: vs defensa fuerte -10%, vs defensa media +2%, vs defensa débil +11%; triples: vs defensa fuerte -22%, vs defensa media +44%, vs defensa débil -31%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 45% | 67% | 68% | 68% |
| pintura | 37% | 45% | 45% | 44% |
| triple frontal | 11% | 23% | 35% | 37% |
| triple de esquina | 5% | 27% | 38% | 38% |
| media distancia | 2% | 39% | 41% | 38% |

#### Brandon Miller (aleros/ala-pívots) vs Atlanta Hawks

- Minutos esperados: **28.1** (± 7.2); 79 partidos en la base.
- Dennis Schroder ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- sin Grayson Allen: muestra insuficiente (1 partidos sin él)
- sin Grant Williams (39 partidos): 29.9 min vs 30.9 con él; reb -10%/min, ast -8%/min
- Kon Knueppel ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Su prop más probable hoy: **Brandon Miller: menos de 3.5 asistencias** (65%). Con 80% de probabilidad: más de 0.5 / menos de 4.5.
- Defensa de Atlanta Hawks contra aleros/ala-pívots en asistencias: +0% respecto a la media; ajuste por su historial contra defensas similares: +3%.

**¿Por qué 2.4 asistencias?** (línea 3.5; 28.1 minutos esperados)

En corto:

- La pasó en 7 de 12 esta temporada (falló con 4, 4, 4, 5)
- Con 24+ minutos (hoy se esperan 28): 7 de 12 en sus últimos 15
- Contra las ~10 mejores defensas en asistencias a aleros/ala-pívots: 10 de 14 (últimos 40 partidos)
- Contra defensas medias como la de hoy y con 24+ minutos: 10 de 16, con 3.0 de media (últimos 60 partidos)
- El rival es #13 de 30 en asistencias que concede a aleros/ala-pívots por minuto (#1 = el que más concede; +0% frente a la media)
- Asistencias esperadas: 3.0 por partido si sus compañeros metieran lo normal (tiene 2.9; con él en pista metieron el 97% de lo esperado por tipo de tiro, últimos 10); ajuste aplicado +1.7%
- Oportunidades: asiste el 14% de las canastas de sus compañeros con él en pista
- El rival no tiene a CJ McCollum (4.6 asistencias por partido)
- Minutos: 28 esperados (titular, ±7)

Razonamiento (1 factores a favor, 2 en contra):

- ❌ Minutos: 28.1 esperados (titular, ±7.2).
- ✅ Forma: 2.8 en sus últimos 5, 2.5 esta temporada (12 partidos), 3.4 la temporada pasada (línea 3.5).
- ➖ Cómo produce asistencias: asiste el 14.5% de las canastas de sus compañeros en pista × 17.0 canastas de compañeros esperadas (su equipo 40.0 por 48' contra esta defensa).
- ➖ Defensa: el rival concede +0% de asistencias por minuto a aleros/ala-pívots (defensa media); ajuste aplicado +0%.
- ➖ Ritmo del partido: +1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ➖ Contra este rival: 0, 2, 4, 8 (2 de 4 a favor).
- ➖ Últimos 10: la habría pasado 5 de 10.
- ❌ Bajas del rival: sin CJ McCollum (titular); +1.5% en esta estadística.
- ⚠️ Dennis Schroder ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ sin Grayson Allen: muestra insuficiente (1 partidos sin él).
- ⚠️ sin Grant Williams (39 partidos): 29.9 min vs 30.9 con él; reb -10%/min, ast -8%/min.
- ⚠️ Kon Knueppel ya no jugó en sus últimos partidos: la baja ya está en sus minutos.

- ⚠️ Alertas: minutos inestables, falla en partidos normales (4 de 12 esta temporada).
- Asistencias **2.4** (por componentes 2.3 · por tasa por minuto y defensa rival 2.4): asiste el 14.5% de las canastas de sus compañeros en pista × 17.0 canastas de compañeros esperadas (su equipo 40.0 por 48' contra esta defensa).

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 25.4 | 30.7 | 30.5 | 30.4 | 32.2 |
| Asistencias | 2.8 | 2.9 | 2.5 | 3.3 | 3.5 |
| % de las canastas de compañeros que asiste | 18.9% | 17.2% | 14.5% | 15.5% | 15.6% |
| Pérdidas por jugada | 11.4% | 10.0% | 10.3% | 12.6% | 13.0% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -14%, vs defensa media +5%, vs defensa débil +7%; rebotes: vs defensa fuerte -17%, vs defensa media -8%, vs defensa débil +20%; asistencias: vs defensa fuerte -15%, vs defensa media +6%, vs defensa débil +9%; triples: vs defensa fuerte -21%, vs defensa media +12%, vs defensa débil +14%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 44% | 34% | 35% | 35% |
| pintura | 25% | 42% | 45% | 44% |
| bajo el aro | 13% | 69% | 68% | 67% |
| media distancia | 10% | 38% | 41% | 43% |
| triple de esquina | 8% | 42% | 38% | 37% |

#### Onyeka Okongwu (aleros/ala-pívots) vs Charlotte Hornets

- Minutos esperados: **35.1** (± 3.0); 95 partidos en la base.
- sin CJ McCollum (37 partidos): 32.2 min vs 30.5 con él; pts +8%/min, ast +10%/min
- Su prop más probable hoy: **Onyeka Okongwu: más de 1.5 triples** (64%). Con 80% de probabilidad: más de 0.5 / menos de 4.5.
- Defensa de Charlotte Hornets contra aleros/ala-pívots en triples: +5% respecto a la media; ajuste por su historial contra defensas similares: +5%.

**¿Por qué 2.4 triples?** (línea 1.5; 35.1 minutos esperados)

En corto:

- La pasó en 10 de 15 esta temporada; los fallos, en partidos raros (jugó 28 min, 5 faltas, jugó 29 min, jugó 26 min, jugó 29 min)
- Con 31+ minutos (hoy se esperan 35): 6 de 6 en sus últimos 15
- Contra las ~10 mejores defensas en triples a aleros/ala-pívots: 7 de 12 (últimos 40 partidos)
- Contra defensas débiles como la de hoy y con 31+ minutos: 10 de 14, con 2.3 de media (últimos 60 partidos)
- El rival es #7 de 30 en triples que concede a aleros/ala-pívots por minuto (#1 = el que más concede; +6% frente a la media)
- Su zona principal es triple frontal (35% de sus tiros, 37% de acierto); el rival es #2 de 30 en acierto que deja ahí (37%, liga 35%)
- Cómo tira (últimos 15): recibe y tira 49% (33% de acierto), penetración 22% (65% de acierto), corte 9% (80% de acierto); en recibe y tira el rival es #1 de 30 en lo que deja (#1 = el que más; 1.15 puntos por tiro frente a 1.07 de media)
- Oportunidades: 5.9 triples intentados esperados al 38%
- El rival no tiene a Grayson Allen (3.2 triples por partido)
- Minutos: 35 esperados (titular, ±3)

Razonamiento (7 factores a favor, 0 en contra):

- ✅ Minutos: 35.1 esperados (titular, ±3.0).
- ✅ Forma: 2.8 en sus últimos 5, 1.9 esta temporada (15 partidos), 1.9 la temporada pasada (línea 1.5).
- ➖ Cómo produce triples: 5.9 triples intentados (su ritmo 6.2 por 36'; el rival concede -2% de triples en su reparto) × 38% esperado.
- ✅ Defensa: el rival concede +6% de triples por minuto a aleros/ala-pívots (defensa débil); ajuste aplicado +5%; en su zona principal (triple) el rival concede 37% (liga 35%).
- ✅ Altura: mide 6'10", 1.9 pulgadas más que los aleros/ala-pívots del rival (+0.7% en esta estadística).
- ➖ Ritmo del partido: +1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 2, 3, 4, 0, 2 (4 de 5 a favor).
- ✅ Últimos 10: la habría pasado 9 de 10.
- ✅ Bajas del rival: sin Grayson Allen (titular); +1.7% en esta estadística.
- ⚠️ sin CJ McCollum (37 partidos): 32.2 min vs 30.5 con él; pts +8%/min, ast +10%/min.

- Triples **2.4** (por componentes 2.3 · por tasa por minuto y defensa rival 2.4): 5.9 triples intentados (su ritmo 6.2 por 36'; el rival concede -2% de triples en su reparto) × 38% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 33.4 | 32.5 | 30.8 | 31.2 | 30.6 |
| Triples anotados | 2.8 | 2.4 | 1.9 | 1.9 | 2.2 |
| Triples intentados | 7.8 | 6.3 | 5.5 | 5.1 | 5.2 |
| % triples | 35.9% | 38.1% | 33.7% | 38.0% | 42.3% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +1%, vs defensa media -5%, vs defensa débil +5%; rebotes: vs defensa fuerte -11%, vs defensa media -4%, vs defensa débil +17%; asistencias: vs defensa fuerte -6%, vs defensa media +4%, vs defensa débil +7%; triples: vs defensa fuerte -5%, vs defensa media -19%, vs defensa débil +15%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 35% | 37% | 35% | 37% |
| bajo el aro | 28% | 70% | 68% | 68% |
| pintura | 26% | 48% | 45% | 44% |
| triple de esquina | 11% | 36% | 38% | 38% |
| media distancia | 1% | 40% | 41% | 38% |

#### Coby White (bases/escoltas) vs Atlanta Hawks

- Minutos esperados: **20.7** (± 3.4); 59 partidos en la base.
- Dennis Schroder ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- sin Grayson Allen: muestra insuficiente (1 partidos sin él)
- sin Grant Williams (8 partidos): 18.0 min vs 20.0 con él; pts -18%/min, reb -6%/min, ast +16%/min
- Kon Knueppel ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- cambio de rol esta temporada (por minuto): tpm -37%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Coby White: menos de 21.5 pts+ast** (64%). Con 80% de probabilidad: más de 9.5 / menos de 20.5.
- Defensa de Atlanta Hawks contra bases/escoltas en pts+ast: -1% respecto a la media; ajuste por su historial contra defensas similares: +2%.

**¿Por qué 15.1 pts+ast?** (línea 21.5; 20.7 minutos esperados)

En corto:

- La pasó en 4 de 7 esta temporada (falló con 23, 22, 24)
- Con 17+ minutos (hoy se esperan 21): 5 de 10 en sus últimos 15
- Contra las ~10 mejores defensas en puntos a bases/escoltas: 12 de 16 (últimos 40 partidos)
- Contra defensas medias como la de hoy y con 17+ minutos: 5 de 16, con 22.4 de media (últimos 60 partidos)
- El rival es #18 de 30 en puntos que concede a bases/escoltas por minuto (#1 = el que más concede; -1% frente a la media)
- Su zona principal es triple frontal (45% de sus tiros, 34% de acierto); el rival es #15 de 30 en acierto que deja ahí (35%, liga 35%)
- Su segunda zona es bajo el aro (25% de sus tiros, 65% de acierto); el rival es #18 de 30 en acierto que deja ahí (67%, liga 68%)
- El rival es #22 de 30 en tiros libres que concede a bases/escoltas (#1 = el que más; -7% frente a la media)
- Puntería: en sus últimos 10 metió el 94% de las canastas esperadas por sus tipos de tiro (viene frío: suele volver a su nivel)
- Cómo tira (últimos 15): creado 40% (33% de acierto), penetración 29% (62% de acierto), recibe y tira 27% (35% de acierto); en creado el rival es #26 de 30 en lo que deja (#1 = el que más; 0.89 puntos por tiro frente a 0.94 de media)
- Oportunidades: 8.7 tiros de campo y 2.8 libres esperados (1.04 puntos por tiro)
- Transición: el rival concede 12.9 puntos por partido al contraataque (#25 de 30, #1 = el que más); él anota 1.6 así por partido (ajuste aplicado -1.3%)
- El rival no tiene a CJ McCollum (18.0 pts+ast por partido)
- Minutos: 21 esperados (titular, ±3)

Razonamiento (2 factores a favor, 2 en contra):

- ✅ Minutos: 20.7 esperados (titular, ±3.4).
- ✅ Forma: 19.2 en sus últimos 5, 16.0 esta temporada (7 partidos), 21.0 la temporada pasada (línea 21.5).
- ➖ Cómo produce puntos: 8.7 tiros de campo (su ritmo 19.8 por 36'; el rival concede +0% de tiros) × 1.04 puntos por tiro [triple frontal 45% de sus tiros al 34% (rival concede 35%, liga 35%); bajo el aro 25% de sus tiros al 65% (rival concede 67%, liga 68%); pintura 16% de sus tiros al 46% (rival concede 44%, liga 45%)] + 2.8 tiros libres × 83%.
- ➖ Cómo produce asistencias: asiste el 22.1% de las canastas de sus compañeros en pista × 13.4 canastas de compañeros esperadas (su equipo 40.0 por 48' contra esta defensa).
- ➖ Defensa: el rival concede -1% de puntos por minuto a bases/escoltas (defensa media); ajuste aplicado -1%; en su zona principal (triple) el rival concede 35% (liga 35%).
- ➖ Ritmo del partido: +1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ❌ Contra este rival: 28, 26 (0 de 2 a favor).
- ➖ Últimos 10: la habría pasado 6 de 10.
- ❌ Bajas del rival: sin CJ McCollum (titular); +1.6% en esta estadística.
- ⚠️ Dennis Schroder ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ sin Grayson Allen: muestra insuficiente (1 partidos sin él).
- ⚠️ sin Grant Williams (8 partidos): 18.0 min vs 20.0 con él; pts -18%/min, reb -6%/min, ast +16%/min.
- ⚠️ Kon Knueppel ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ cambio de rol esta temporada (por minuto): tpm -37%; se da más peso a la línea de la casa.

- ⚠️ Alertas: muy lejos de la casa, falla en partidos normales (3 de 7 esta temporada), viene fallando tiros que suele meter.
- Puntos **11.3** (por componentes 11.4 · por tasa por minuto y defensa rival 11.1): 8.7 tiros de campo (su ritmo 19.8 por 36'; el rival concede +0% de tiros) × 1.04 puntos por tiro [triple frontal 45% de sus tiros al 34% (rival concede 35%, liga 35%); bajo el aro 25% de sus tiros al 65% (rival concede 67%, liga 68%); pintura 16% de sus tiros al 46% (rival concede 44%, liga 45%)] + 2.8 tiros libres × 83%.
- Asistencias **3.9** (por componentes 3.4 · por tasa por minuto y defensa rival 3.8): asiste el 22.1% de las canastas de sus compañeros en pista × 13.4 canastas de compañeros esperadas (su equipo 40.0 por 48' contra esta defensa).

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 20.4 | 19.5 | 19.4 | 24.8 | 31.0 |
| Puntos | 15.6 | 13.1 | 12.7 | 17.1 | 22.5 |
| Tiros de campo intentados | 12.2 | 10.9 | 11.3 | 12.4 | 13.0 |
| % tiros de campo | 41.0% | 40.4% | 38.0% | 44.5% | 50.0% |
| Triples intentados | 6.0 | 5.5 | 5.7 | 6.3 | 8.5 |
| % triples | 23.3% | 29.1% | 20.0% | 36.7% | 47.1% |
| Tiros libres intentados | 4.8 | 3.2 | 3.4 | 4.7 | 8.0 |
| % tiros libres | 87.5% | 84.4% | 87.5% | 81.9% | 68.8% |
| Jugadas que usa por 36 min | 30.9 | 27.3 | 29.3 | 24.5 | 25.0 |
| Asistencias | 3.6 | 2.8 | 3.3 | 3.9 | 4.5 |
| % de las canastas de compañeros que asiste | 27.9% | 22.1% | 27.0% | 20.5% | 16.2% |
| Pérdidas por jugada | 18.3% | 16.9% | 19.0% | 14.8% | 23.2% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -6%, vs defensa media +6%, vs defensa débil +0%; rebotes: vs defensa fuerte -12%, vs defensa media -6%, vs defensa débil +15%; asistencias: vs defensa fuerte -12%, vs defensa media +15%, vs defensa débil -3%; triples: vs defensa fuerte -8%, vs defensa media +6%, vs defensa débil +4%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 45% | 34% | 35% | 35% |
| bajo el aro | 25% | 65% | 68% | 67% |
| pintura | 16% | 46% | 45% | 44% |
| media distancia | 8% | 36% | 41% | 43% |
| triple de esquina | 6% | 35% | 38% | 37% |

#### Naz Reid (pívots) vs Atlanta Hawks

- Minutos esperados: **32.7** (± 6.7); 102 partidos en la base.
- Dennis Schroder ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- sin Grayson Allen: muestra insuficiente (1 partidos sin él)
- sin Grant Williams (11 partidos): 29.5 min vs 34.3 con él; reb +17%/min, ast -16%/min
- Kon Knueppel ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Su prop más probable hoy: **Naz Reid: más de 7.5 rebotes** (64%). Con 80% de probabilidad: más de 6.5 / menos de 14.5.
- Defensa de Atlanta Hawks contra pívots en rebotes: +4% respecto a la media; ajuste por su historial contra defensas similares: +2%.

**¿Por qué 10.8 rebotes?** (línea 7.5; 32.7 minutos esperados)

En corto:

- La pasó en 8 de 14 esta temporada (falló con 4, 6, 6, 5)
- Con 29+ minutos (hoy se esperan 33): 8 de 10 en sus últimos 15
- Contra las ~10 mejores defensas en rebotes a pívots: 7 de 21 (últimos 40 partidos)
- Contra defensas débiles como la de hoy y con 29+ minutos: 5 de 7, con 9.4 de media (últimos 60 partidos)
- El rival es #7 de 30 en rebotes que concede a pívots por minuto (#1 = el que más concede; +4% frente a la media)
- El rival es #7 de 30 en rebotes que concede en total (#1 = el que más)
- El rival es #23 de 30 en rebotes ofensivos que concede en total (#1 = el que más)
- Rebotes disponibles con él en pista (últimos 10): 27.9 tiros fallados del rival y 34.1 de su equipo por partido; se queda el 25% y el 3%; el rival falla 53.5 tiros por partido (#1 de 30, #1 = el que más falla)
- El rival no tiene a CJ McCollum (3.7 rebotes por partido)
- Minutos: 33 esperados (titular, ±7)

Razonamiento (2 factores a favor, 3 en contra):

- ❌ Minutos: 32.7 esperados (titular, ±6.7).
- ✅ Forma: 8.4 en sus últimos 5, 8.4 esta temporada (14 partidos), 6.4 la temporada pasada (línea 7.5).
- ➖ Cómo produce rebotes: defensivos 9.0 = captura el 23.3% de los fallos del rival en pista × 48.2 fallos esperados del rival (liga 46.9) × 68% del partido; ofensivos 1.7 = 4.5% de los fallos de su equipo × 48.0.
- ✅ Defensa: el rival concede +4% de rebotes por minuto a pívots (defensa débil); ajuste aplicado +4%.
- ❌ Altura: mide 6'9", 2.0 pulgadas menos que los pívots del rival (-0.7% en esta estadística).
- ➖ Ritmo del partido: +1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ❌ Contra este rival: 6, 6, 7 (0 de 3 a favor).
- ➖ Últimos 10: la habría pasado 5 de 10.
- ⚠️ Dennis Schroder ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ sin Grayson Allen: muestra insuficiente (1 partidos sin él).
- ⚠️ sin Grant Williams (11 partidos): 29.5 min vs 34.3 con él; reb +17%/min, ast -16%/min.
- ⚠️ Kon Knueppel ya no jugó en sus últimos partidos: la baja ya está en sus minutos.

- ⚠️ Alertas: minutos inestables.
- Rebotes **10.8** (por componentes 10.7 · por tasa por minuto y defensa rival 11.0): defensivos 9.0 = captura el 23.3% de los fallos del rival en pista × 48.2 fallos esperados del rival (liga 46.9) × 68% del partido; ofensivos 1.7 = 4.5% de los fallos de su equipo × 48.0.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 32.2 | 30.4 | 30.6 | 26.1 | 22.7 |
| Rebotes | 8.4 | 7.9 | 8.4 | 6.3 | 6.3 |
| % de los fallos del rival que captura | 23.9% | 25.1% | 24.9% | 20.3% | 19.5% |
| % de los fallos de su equipo que captura | 2.2% | 2.6% | 3.3% | 4.4% | 2.9% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -8%, vs defensa media -3%, vs defensa débil +10%; rebotes: vs defensa fuerte -0%, vs defensa media -7%, vs defensa débil +5%; asistencias: vs defensa fuerte -10%, vs defensa media +5%, vs defensa débil +7%; triples: vs defensa fuerte +4%, vs defensa media -14%, vs defensa débil +12%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 34% | 34% | 35% | 35% |
| pintura | 27% | 45% | 45% | 44% |
| bajo el aro | 18% | 67% | 68% | 67% |
| triple de esquina | 14% | 41% | 38% | 37% |
| media distancia | 7% | 38% | 41% | 43% |

## Orlando Magic @ Brooklyn Nets

Diferencia esperada: Orlando Magic por 5.5.

Parte de lesiones: Jonathan Isaac (Out); Paolo Banchero (Out); Grant Nelson (Out); Izaiyah Nelson (Out); Noah Penda (Out).

Ventajas del partido (los dos lados): puntos esperados frente a su media de los últimos 10, ajuste por la defensa rival y diferencia de estatura con los rivales de su posición.

| Equipo | Jugador | Puntos esperados | Su media (últ. 10) | Defensa rival en puntos | Rebotes esperados | Altura vs rival |
|---|---|---|---|---|---|---|
| ORL | Franz Wagner | 26.0 | 26.3 | +3% | 7.0 | +0.4" |
| ORL | Desmond Bane | 20.9 | 19.5 | +0% | 4.8 | +1.2" |
| ORL | Anthony Black | 18.4 | 16.4 | +1% | 5.0 | +2.2" |
| BKN | Michael Porter Jr. | 20.5 | 20.3 | +1% | 6.7 | +1.2" |
| ORL | Wendell Carter Jr. | 13.7 | 13.3 | +5% | 8.1 | -0.4" |
| BKN | Julius Randle | 18.7 | 19.9 | +1% | 5.5 | +0.2" |
| ORL | Tristan da Silva | 13.4 | 15.4 | +3% | 4.6 | -1.6" |
| BKN | Egor Demin | 11.8 | 10.6 | +0% | 2.8 | +3.2" |
| BKN | Nolan Traore | 12.8 | 15.3 | +0% | 2.0 | -1.8" |
| BKN | Day'Ron Sharpe | 9.3 | 8.9 | -4% | 7.2 | -0.1" |

Las 8 más probables (máximo 2 por jugador: las de un mismo jugador suelen ganar o perder juntas).

| Prop | Prob. final | Modelo | Casa | Esperado | Últ. 10 | Temporada | vs este rival | Cuota (implícita) |
|---|---|---|---|---|---|---|---|---|
| **Day'Ron Sharpe: menos de 0.5 triples** | **72%** | 70% | 74% | 0.3 ± 0.6 | 8/10 | 10/14 | 0, 0, 0 | 1.23 (81%) |
| **Moritz Wagner: más de 0.5 asistencias** ⚠️ suplente | **70%** | 71% | 67% | 1.5 ± 1.3 | 7/10 | 11/14 | - | 1.42 (71%) |
| **Mikel Brown Jr.: menos de 2.5 rebotes** ⚠️ suplente | **64%** | 68% | 61% | 2.0 ± 1.4 | 8/10 | 8/10 | - | 1.53 (66%) |
| **Nolan Traore: menos de 2.5 rebotes** | **64%** | 67% | 60% | 2.0 ± 1.5 | 8/10 | 11/13 | 3, 3 | 1.55 (65%) |
| **Desmond Bane: más de 2.5 asistencias** | **64%** | 70% | 56% | 4.1 ± 2.0 | 7/10 | 7/13 | 4, 3, 2 | 1.67 (60%) |
| **Day'Ron Sharpe: más de 0.5 tapones** | **63%** | 64% | 62% | 1.2 ± 1.3 | 7/10 | 9/14 | 0, 0, 0 | 1.53 (65%) |
| **Julius Randle: más de 0.5 robos** | **61%** | 62% | 59% | 1.0 ± 1.0 | 7/10 | 9/14 | 2 | 1.61 (62%) |
| **Egor Demin: menos de 2.5 triples** | **61%** | 63% | 59% | 2.1 ± 1.6 | 6/10 | 4/8 | 6, 5, 1 | 1.59 (63%) |

### Fichas de los jugadores destacados

#### Day'Ron Sharpe (pívots) vs Orlando Magic

- Minutos esperados: **24.1** (± 3.6); 76 partidos en la base.
- Su prop más probable hoy: **Day'Ron Sharpe: menos de 0.5 triples** (72%). Con 80% de probabilidad: más de - / menos de 1.5.
- Defensa de Orlando Magic contra pívots en triples: -15% respecto a la media; ajuste por su historial contra defensas similares: -1%.

**¿Por qué 0.3 triples?** (línea 0.5; 24.1 minutos esperados)

En corto:

- La pasó en 10 de 14 esta temporada (falló con 2, 1, 1, 1)
- Con 20+ minutos (hoy se esperan 24): 8 de 10 en sus últimos 15
- Contra las ~10 mejores defensas en triples a pívots: 8 de 11 (últimos 40 partidos)
- Contra defensas fuertes como la de hoy y con 20+ minutos: 7 de 9, con 0.2 de media (últimos 60 partidos)
- El rival es #30 de 30 en triples que concede a pívots por minuto (#1 = el que más concede; -28% frente a la media)
- Su zona principal es triple frontal (8% de sus tiros, 31% de acierto); el rival es #16 de 30 en acierto que deja ahí (35%, liga 35%)
- Cómo tira (últimos 15): palmeo 26% (56% de acierto), corte 23% (59% de acierto), recibe y tira 17% (31% de acierto); en palmeo el rival es #30 de 30 en lo que deja (#1 = el que más; 1.09 puntos por tiro frente a 1.17 de media)
- Oportunidades: 1.1 triples intentados esperados al 33%
- Minutos: 24 esperados (titular, ±4)

Razonamiento (5 factores a favor, 0 en contra):

- ✅ Minutos: 24.1 esperados (titular, ±3.6).
- ✅ Forma: 0.4 en sus últimos 5, 0.4 esta temporada (14 partidos), 0.1 la temporada pasada (línea 0.5).
- ➖ Cómo produce triples: 1.1 triples intentados (su ritmo 1.8 por 36'; el rival concede -4% de triples en su reparto) × 33% esperado.
- ✅ Defensa: el rival concede -28% de triples por minuto a pívots (defensa fuerte); ajuste aplicado -15%; en su zona principal (triple) el rival concede 35% (liga 35%).
- ➖ Ritmo del partido: -1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 0, 0, 0 (3 de 3 a favor).
- ✅ Últimos 10: la habría pasado 8 de 10.

- Triples **0.3** (por componentes 0.4 · por tasa por minuto y defensa rival 0.3): 1.1 triples intentados (su ritmo 1.8 por 36'; el rival concede -4% de triples en su reparto) × 33% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 22.8 | 24.5 | 23.6 | 18.7 | 19.0 |
| Triples anotados | 0.4 | 0.3 | 0.4 | 0.1 | 0.0 |
| Triples intentados | 1.2 | 1.2 | 1.1 | 0.6 | 0.3 |
| % triples | 33.3% | 25.0% | 31.2% | 23.1% | 0.0% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -10%, vs defensa media -9%, vs defensa débil +19%; rebotes: vs defensa fuerte -4%, vs defensa media +8%, vs defensa débil -0%; asistencias: vs defensa fuerte -7%, vs defensa media -9%, vs defensa débil +12%; triples: vs defensa fuerte +5%, vs defensa media +25%, vs defensa débil -23%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 64% | 68% | 68% | 69% |
| pintura | 22% | 47% | 45% | 45% |
| triple frontal | 8% | 31% | 35% | 35% |
| triple de esquina | 6% | 35% | 38% | 38% |
| media distancia | 1% | 38% | 41% | 43% |

#### Moritz Wagner (pívots) vs Orlando Magic

- Minutos esperados: **17.3** (± 3.8); 53 partidos en la base.
- Su prop más probable hoy: **Moritz Wagner: más de 0.5 asistencias** (70%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Orlando Magic contra pívots en asistencias: -2% respecto a la media; ajuste por su historial contra defensas similares: -2%.

**¿Por qué 1.5 asistencias?** (línea 0.5; 17.3 minutos esperados)

En corto:

- La pasó en 11 de 14 esta temporada (falló con 0, 0, 0)
- Con 13+ minutos (hoy se esperan 17): 10 de 13 en sus últimos 15
- Contra las ~10 mejores defensas en asistencias a pívots: 7 de 14 (últimos 40 partidos)
- Contra defensas medias como la de hoy y con 13+ minutos: 5 de 7, con 1.0 de media (últimos 60 partidos)
- El rival es #16 de 30 en asistencias que concede a pívots por minuto (#1 = el que más concede; -2% frente a la media)
- Asistencias esperadas: 1.8 por partido si sus compañeros metieran lo normal (tiene 1.6; con él en pista metieron el 89% de lo esperado por tipo de tiro, últimos 10); ajuste aplicado +6.4%
- Oportunidades: asiste el 12% de las canastas de sus compañeros con él en pista
- Minutos: 17 esperados (suplente, ±4)

Razonamiento (2 factores a favor, 1 en contra):

- ❌ Minutos: 17.3 esperados (suplente, ±3.8).
- ✅ Forma: 2.6 en sus últimos 5, 1.6 esta temporada (14 partidos), 0.7 la temporada pasada (línea 0.5).
- ➖ Cómo produce asistencias: asiste el 12.0% de las canastas de sus compañeros en pista × 10.2 canastas de compañeros esperadas (su equipo 36.7 por 48' contra esta defensa).
- ➖ Defensa: el rival concede -2% de asistencias por minuto a pívots (defensa media); ajuste aplicado -2%.
- ➖ Ritmo del partido: -1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Últimos 10: la habría pasado 7 de 10.

- ⚠️ Alertas: suplente.
- Asistencias **1.5** (por componentes 1.2 · por tasa por minuto y defensa rival 1.4): asiste el 12.0% de las canastas de sus compañeros en pista × 10.2 canastas de compañeros esperadas (su equipo 36.7 por 48' contra esta defensa).

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 16.6 | 18.3 | 17.9 | 11.4 | - |
| Asistencias | 2.6 | 1.6 | 1.6 | 0.7 | - |
| % de las canastas de compañeros que asiste | 20.9% | 12.8% | 12.7% | 7.9% | - |
| Pérdidas por jugada | 14.2% | 10.4% | 11.5% | 7.9% | - |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -16%, vs defensa media -1%, vs defensa débil +18%; rebotes: vs defensa fuerte -19%, vs defensa media +40%, vs defensa débil +1%; asistencias: vs defensa fuerte -12%, vs defensa media -26%, vs defensa débil +31%; triples: vs defensa fuerte -12%, vs defensa media +10%, vs defensa débil +3%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 43% | 66% | 68% | 69% |
| triple frontal | 27% | 42% | 35% | 35% |
| pintura | 22% | 36% | 45% | 45% |
| triple de esquina | 7% | 39% | 38% | 38% |
| media distancia | 1% | 40% | 41% | 43% |

#### Mikel Brown Jr. (bases/escoltas) vs Orlando Magic

- Minutos esperados: **22.8** (± 3.7); 10 partidos en la base.
- Su prop más probable hoy: **Mikel Brown Jr.: menos de 2.5 rebotes** (64%). Con 80% de probabilidad: más de 0.5 / menos de 3.5.
- Defensa de Orlando Magic contra bases/escoltas en rebotes: +2% respecto a la media; ajuste por su historial contra defensas similares: +0%.

**¿Por qué 2.0 rebotes?** (línea 2.5; 22.8 minutos esperados)

En corto:

- La pasó en 8 de 10 esta temporada (falló con 5, 3)
- Con 19+ minutos (hoy se esperan 23): 7 de 9 en sus últimos 15
- Contra las ~10 mejores defensas en rebotes a bases/escoltas: 4 de 5 (últimos 40 partidos)
- El rival es #11 de 30 en rebotes que concede a bases/escoltas por minuto (#1 = el que más concede; +2% frente a la media)
- El rival es #22 de 30 en rebotes que concede en total (#1 = el que más)
- El rival es #28 de 30 en rebotes ofensivos que concede en total (#1 = el que más)
- Rebotes disponibles con él en pista (últimos 10): 22.2 tiros fallados del rival y 23.4 de su equipo por partido; se queda el 7% y el 1%; el rival falla 46.9 tiros por partido (#21 de 30, #1 = el que más falla)
- Minutos: 23 esperados (suplente, ±4)

Razonamiento (2 factores a favor, 2 en contra):

- ❌ Minutos: 22.8 esperados (suplente, ±3.7).
- ✅ Forma: 1.2 en sus últimos 5, 1.8 esta temporada (10 partidos) (línea 2.5).
- ➖ Cómo produce rebotes: defensivos 1.6 = captura el 7.8% de los fallos del rival en pista × 42.9 fallos esperados del rival (liga 46.9) × 48% del partido; ofensivos 0.3 = 1.4% de los fallos de su equipo × 45.3.
- ❌ Defensa: el rival concede +2% de rebotes por minuto a bases/escoltas (defensa media); ajuste aplicado +2%.
- ➖ Ritmo del partido: -1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Últimos 10: la habría pasado 8 de 10.

- ⚠️ Alertas: suplente.
- Rebotes **2.0** (por componentes 1.9 · por tasa por minuto y defensa rival 2.0): defensivos 1.6 = captura el 7.8% de los fallos del rival en pista × 42.9 fallos esperados del rival (liga 46.9) × 48% del partido; ofensivos 0.3 = 1.4% de los fallos de su equipo × 45.3.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 22.0 | 22.8 | 22.8 | - | - |
| Rebotes | 1.2 | 1.8 | 1.8 | - | - |
| % de los fallos del rival que captura | 4.5% | 7.2% | 7.2% | - | - |
| % de los fallos de su equipo que captura | 1.0% | 0.9% | 0.9% | - | - |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -1%; rebotes: vs defensa fuerte +4%, vs defensa media +21%; asistencias: vs defensa fuerte -8%, vs defensa media +7%; triples: vs defensa fuerte -9%, vs defensa media +2%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 50% | 33% | 35% | 35% |
| bajo el aro | 19% | 54% | 68% | 69% |
| pintura | 17% | 39% | 45% | 45% |
| media distancia | 10% | 41% | 41% | 43% |
| triple de esquina | 5% | 38% | 38% | 38% |

#### Nolan Traore (bases/escoltas) vs Orlando Magic

- Minutos esperados: **24.4** (± 3.5); 69 partidos en la base.
- Su prop más probable hoy: **Nolan Traore: menos de 2.5 rebotes** (64%). Con 80% de probabilidad: más de 0.5 / menos de 3.5.
- Defensa de Orlando Magic contra bases/escoltas en rebotes: +2% respecto a la media; ajuste por su historial contra defensas similares: -3%.

**¿Por qué 2.0 rebotes?** (línea 2.5; 24.4 minutos esperados)

En corto:

- La pasó en 11 de 13 esta temporada (falló con 4, 3)
- Con 20+ minutos (hoy se esperan 24): 8 de 10 en sus últimos 15
- Contra las ~10 mejores defensas en rebotes a bases/escoltas: 10 de 14 (últimos 40 partidos)
- Contra defensas medias como la de hoy y con 20+ minutos: 9 de 13, con 1.8 de media (últimos 60 partidos)
- El rival es #11 de 30 en rebotes que concede a bases/escoltas por minuto (#1 = el que más concede; +2% frente a la media)
- El rival es #22 de 30 en rebotes que concede en total (#1 = el que más)
- El rival es #28 de 30 en rebotes ofensivos que concede en total (#1 = el que más)
- Rebotes disponibles con él en pista (últimos 10): 23.1 tiros fallados del rival y 23.6 de su equipo por partido; se queda el 6% y el 1%; el rival falla 46.9 tiros por partido (#21 de 30, #1 = el que más falla)
- Minutos: 24 esperados (titular, ±4)

Razonamiento (4 factores a favor, 2 en contra):

- ✅ Minutos: 24.4 esperados (titular, ±3.5).
- ✅ Forma: 1.0 en sus últimos 5, 1.8 esta temporada (13 partidos), 1.8 la temporada pasada (línea 2.5).
- ➖ Cómo produce rebotes: defensivos 1.6 = captura el 7.4% de los fallos del rival en pista × 42.9 fallos esperados del rival (liga 46.9) × 51% del partido; ofensivos 0.4 = 1.9% de los fallos de su equipo × 45.3.
- ❌ Defensa: el rival concede +2% de rebotes por minuto a bases/escoltas (defensa media); ajuste aplicado +2%.
- ✅ Altura: mide 6'3", 1.8 pulgadas menos que los bases/escoltas del rival (-0.6% en esta estadística).
- ➖ Ritmo del partido: -1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ❌ Contra este rival: 3, 3 (0 de 2 a favor).
- ✅ Últimos 10: la habría pasado 8 de 10.

- Rebotes **2.0** (por componentes 2.1 · por tasa por minuto y defensa rival 2.0): defensivos 1.6 = captura el 7.4% de los fallos del rival en pista × 42.9 fallos esperados del rival (liga 46.9) × 51% del partido; ofensivos 0.4 = 1.9% de los fallos de su equipo × 45.3.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 23.4 | 24.8 | 22.6 | 22.2 | 29.0 |
| Rebotes | 1.0 | 1.7 | 1.8 | 1.8 | 3.0 |
| % de los fallos del rival que captura | 3.9% | 6.5% | 6.2% | 7.7% | 9.1% |
| % de los fallos de su equipo que captura | 0.8% | 0.8% | 2.1% | 1.1% | 1.8% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -10%, vs defensa media -9%, vs defensa débil +17%; rebotes: vs defensa fuerte +18%, vs defensa media -20%, vs defensa débil -1%; asistencias: vs defensa fuerte -10%, vs defensa media -10%, vs defensa débil +21%; triples: vs defensa fuerte -1%, vs defensa media +4%, vs defensa débil -3%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| pintura | 30% | 45% | 45% | 45% |
| triple frontal | 29% | 36% | 35% | 35% |
| bajo el aro | 24% | 57% | 68% | 69% |
| triple de esquina | 11% | 34% | 38% | 38% |
| media distancia | 6% | 40% | 41% | 43% |

#### Desmond Bane (bases/escoltas) vs Brooklyn Nets

- Minutos esperados: **36.6** (± 3.0); 104 partidos en la base.
- sin Paolo Banchero, la estrella de su equipo (20 partidos suyos sin él): más tiros y balón para él por minuto (puntos +10%, triples -15%, asistencias +21%)
- Paolo Banchero ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Su prop más probable hoy: **Desmond Bane: más de 2.5 asistencias** (64%). Con 80% de probabilidad: más de 1.5 / menos de 6.5.
- Defensa de Brooklyn Nets contra bases/escoltas en asistencias: +5% respecto a la media; ajuste por su historial contra defensas similares: +1%.

**¿Por qué 4.1 asistencias?** (línea 2.5; 36.6 minutos esperados)

En corto:

- La pasó en 7 de 13 esta temporada (falló con 2, 0, 1, 2)
- Con 33+ minutos (hoy se esperan 37): 8 de 13 en sus últimos 15
- Contra las ~10 mejores defensas en asistencias a bases/escoltas: 7 de 20 (últimos 40 partidos)
- Contra defensas débiles como la de hoy y con 33+ minutos: 14 de 16, con 4.2 de media (últimos 60 partidos)
- El rival es #10 de 30 en asistencias que concede a bases/escoltas por minuto (#1 = el que más concede; +5% frente a la media)
- Asistencias esperadas: 3.1 por partido si sus compañeros metieran lo normal (tiene 3.1; con él en pista metieron el 99% de lo esperado por tipo de tiro, últimos 10); ajuste aplicado +0.6%
- Oportunidades: asiste el 13% de las canastas de sus compañeros con él en pista
- Su equipo no tiene a Paolo Banchero: más tiros y balón para él
- Minutos: 37 esperados (titular, ±3)

Razonamiento (5 factores a favor, 0 en contra):

- ✅ Minutos: 36.6 esperados (titular, ±3.0).
- ✅ Forma: 3.4 en sus últimos 5, 2.7 esta temporada (13 partidos), 3.5 la temporada pasada (línea 2.5).
- ➖ Cómo produce asistencias: asiste el 13.2% de las canastas de sus compañeros en pista × 23.3 canastas de compañeros esperadas (su equipo 40.1 por 48' contra esta defensa).
- ✅ Defensa: el rival concede +5% de asistencias por minuto a bases/escoltas (defensa débil); ajuste aplicado +5%.
- ➖ Ritmo del partido: -1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 4, 3, 2 (2 de 3 a favor).
- ✅ Últimos 10: la habría pasado 7 de 10.
- ⚠️ sin Paolo Banchero, la estrella de su equipo (20 partidos suyos sin él): más tiros y balón para él por minuto (puntos +10%, triples -15%, asistencias +21%).
- ⚠️ Paolo Banchero ya no jugó en sus últimos partidos: la baja ya está en sus minutos.

- Asistencias **4.1** (por componentes 3.7 · por tasa por minuto y defensa rival 4.2): asiste el 13.2% de las canastas de sus compañeros en pista × 23.3 canastas de compañeros esperadas (su equipo 40.1 por 48' contra esta defensa).

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 36.4 | 36.3 | 35.2 | 33.9 | 35.7 |
| Asistencias | 3.4 | 3.1 | 2.7 | 3.9 | 3.0 |
| % de las canastas de compañeros que asiste | 13.1% | 12.8% | 11.3% | 16.8% | 12.3% |
| Pérdidas por jugada | 7.5% | 11.0% | 11.9% | 10.7% | 15.0% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -6%, vs defensa media +1%, vs defensa débil +7%; rebotes: vs defensa fuerte +10%, vs defensa media -1%, vs defensa débil -12%; asistencias: vs defensa fuerte -7%, vs defensa media +5%, vs defensa débil +4%; triples: vs defensa fuerte -11%, vs defensa media -3%, vs defensa débil +21%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 35% | 39% | 35% | 36% |
| bajo el aro | 23% | 62% | 68% | 69% |
| pintura | 21% | 44% | 45% | 46% |
| media distancia | 12% | 45% | 41% | 40% |
| triple de esquina | 9% | 41% | 38% | 41% |

## Indiana Pacers @ Cleveland Cavaliers

Diferencia esperada: Cleveland Cavaliers por 6.5.

Parte de lesiones: T.J. McConnell (Day-To-Day); Andrew Nembhard (Day-To-Day); Tyrese Haliburton (Out); Evan Mobley (Out); Peyton Watson (Day-To-Day); Jaylon Tyson (Out); Braden Smith (Day-To-Day); Nae'Qwan Tomlin (Out); Johnny Furphy (Out).

Ventajas del partido (los dos lados): puntos esperados frente a su media de los últimos 10, ajuste por la defensa rival y diferencia de estatura con los rivales de su posición.

| Equipo | Jugador | Puntos esperados | Su media (últ. 10) | Defensa rival en puntos | Rebotes esperados | Altura vs rival |
|---|---|---|---|---|---|---|
| IND | Andrew Nembhard | 17.8 | 16.5 | -1% | 2.8 | +0.1" |
| CLE | Donovan Mitchell | 24.0 | 25.1 | +3% | 4.7 | -2.3" |
| CLE | James Harden | 14.9 | 15.6 | +2% | 4.8 | +0.7" |
| IND | Pascal Siakam | 23.5 | 23.0 | +0% | 6.0 | +0.2" |
| CLE | Tyrese Proctor | 13.0 | 12.3 | +2% | 4.6 | -0.3" |
| IND | Aaron Nesmith | 15.1 | 11.4 | -1% | 3.5 | +1.1" |
| CLE | Jarrett Allen | 15.1 | 12.5 | +4% | 9.9 | -3.5" |
| CLE | Meleek Thomas | 12.9 | 13.5 | +3% | 3.3 | -1.3" |
| IND | Kelly Oubre Jr. | 12.4 | 12.4 | -1% | 3.6 | +4.1" |
| IND | Ivica Zubac | 10.9 | 9.8 | -2% | 8.6 | +2.6" |

Picks seguros de titulares estables:

| Jugador | Pick seguro | Prob. | Cuota mínima | Esperado | Últ. 10 |
|---|---|---|---|---|---|
| Andrew Nembhard | **más de 22.5 pts+reb+ast** | **78%** | 1.28 | 28.4 | 7/10 |

Las 8 más probables (máximo 2 por jugador: las de un mismo jugador suelen ganar o perder juntas).

| Prop | Prob. final | Modelo | Casa | Esperado | Últ. 10 | Temporada | vs este rival | Cuota (implícita) |
|---|---|---|---|---|---|---|---|---|
| **Peyton Watson: más de 1.5 asistencias** | **64%** | 67% | 60% | 2.4 ± 1.6 | 7/10 | 9/12 | 0, 1 | 1.56 (64%) |
| **Aaron Nesmith: menos de 2.5 triples** | **62%** | 63% | 60% | 2.2 ± 1.7 | 8/10 | 10/13 | 3 | 1.55 (65%) |
| **Kelly Oubre Jr.: menos de 1.5 triples** | **61%** | 63% | 59% | 1.3 ± 1.2 | 7/10 | 10/13 | 0, 2, 2, 4 | 1.57 (64%) |
| **James Harden: menos de 24.5 pts+ast** | **61%** | 69% | 50% | 21.2 ± 6.1 | 7/10 | 10/15 | 35 | 1.89 (53%) |
| **Aaron Nesmith: más de 1.5 asistencias** | **61%** | 63% | 59% | 2.3 ± 1.6 | 6/10 | 7/13 | 4 | 1.57 (64%) |
| **Tyrese Proctor: menos de 3.5 asistencias** | **60%** | 62% | 57% | 3.3 ± 2.3 | 8/10 | 12/15 | 1, 0, 0 | 1.63 (61%) |
| **James Harden: menos de 17.5 puntos** | **60%** | 67% | 50% | 14.9 ± 6.0 | 7/10 | 10/15 | 28 | 1.89 (53%) |
| **Andrew Nembhard: más de 24.5 pts+reb+ast** | **60%** | 69% | 51% | 28.4 ± 6.5 | 6/10 | 7/11 | 27, 31, 41 | 1.83 (55%) |

### Fichas de los jugadores destacados

#### Peyton Watson (bases/escoltas) vs Indiana Pacers

- Minutos esperados: **26.2** (± 4.3); 66 partidos en la base.
- en el parte de lesiones: day-to-day
- sin Evan Mobley: muestra insuficiente (2 partidos sin él)
- sin Jaylon Tyson (5 partidos): 24.4 min vs 29.7 con él; pts +14%/min, reb +10%/min, ast +5%/min
- Su prop más probable hoy: **Peyton Watson: más de 1.5 asistencias** (64%). Con 80% de probabilidad: más de 0.5 / menos de 4.5.
- Defensa de Indiana Pacers contra bases/escoltas en asistencias: +1% respecto a la media; ajuste por su historial contra defensas similares: -1%.

**¿Por qué 2.4 asistencias?** (línea 1.5; 26.2 minutos esperados)

En corto:

- La pasó en 9 de 12 esta temporada (falló con 0, 1, 1)
- Con 22+ minutos (hoy se esperan 26): 7 de 8 en sus últimos 15
- Contra las ~10 mejores defensas en asistencias a bases/escoltas: 8 de 12 (últimos 40 partidos)
- Contra defensas medias como la de hoy y con 22+ minutos: 8 de 13, con 2.0 de media (últimos 60 partidos)
- El rival es #16 de 30 en asistencias que concede a bases/escoltas por minuto (#1 = el que más concede; +1% frente a la media)
- Asistencias esperadas: 2.2 por partido si sus compañeros metieran lo normal (tiene 2.4; con él en pista metieron el 109% de lo esperado por tipo de tiro, últimos 10); ajuste aplicado -2.2%
- Oportunidades: asiste el 12% de las canastas de sus compañeros con él en pista
- Minutos: 26 esperados (titular, ±4)

Razonamiento (3 factores a favor, 1 en contra):

- ✅ Minutos: 26.2 esperados (titular, ±4.3).
- ✅ Forma: 2.0 en sus últimos 5, 2.5 esta temporada (12 partidos), 2.1 la temporada pasada (línea 1.5).
- ➖ Cómo produce asistencias: asiste el 12.2% de las canastas de sus compañeros en pista × 18.6 canastas de compañeros esperadas (su equipo 44.3 por 48' contra esta defensa).
- ➖ Defensa: el rival concede +1% de asistencias por minuto a bases/escoltas (defensa media); ajuste aplicado +1%.
- ➖ Ritmo del partido: +0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ❌ Contra este rival: 0, 1 (0 de 2 a favor).
- ✅ Últimos 10: la habría pasado 7 de 10.
- ⚠️ en el parte de lesiones: day-to-day.
- ⚠️ sin Evan Mobley: muestra insuficiente (2 partidos sin él).
- ⚠️ sin Jaylon Tyson (5 partidos): 24.4 min vs 29.7 con él; pts +14%/min, reb +10%/min, ast +5%/min.

- ⚠️ Alertas: en el parte de lesiones.
- Asistencias **2.4** (por componentes 2.4 · por tasa por minuto y defensa rival 2.5): asiste el 12.2% de las canastas de sus compañeros en pista × 18.6 canastas de compañeros esperadas (su equipo 44.3 por 48' contra esta defensa).

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 26.4 | 26.9 | 27.5 | 29.6 | 31.5 |
| Asistencias | 2.0 | 2.4 | 2.5 | 2.1 | 0.5 |
| % de las canastas de compañeros que asiste | 9.6% | 11.3% | 11.6% | 9.1% | 1.8% |
| Pérdidas por jugada | 11.0% | 10.4% | 12.9% | 12.3% | 4.1% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -6%, vs defensa media +0%, vs defensa débil +6%; rebotes: vs defensa fuerte +4%, vs defensa media -5%, vs defensa débil -0%; asistencias: vs defensa fuerte -22%, vs defensa media -3%, vs defensa débil +19%; triples: vs defensa fuerte -26%, vs defensa media +15%, vs defensa débil +27%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 30% | 64% | 68% | 67% |
| pintura | 24% | 43% | 45% | 47% |
| triple frontal | 20% | 32% | 35% | 35% |
| triple de esquina | 16% | 39% | 38% | 39% |
| media distancia | 10% | 39% | 41% | 44% |

#### Aaron Nesmith (bases/escoltas) vs Cleveland Cavaliers

- Minutos esperados: **30.1** (± 4.6); 58 partidos en la base.
- sin Tyrese Haliburton, la estrella de su equipo (10 partidos suyos sin él): más tiros y balón para él por minuto (puntos +7%, triples +8%, asistencias +1%)
- Tyrese Haliburton ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Johnny Furphy ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Su prop más probable hoy: **Aaron Nesmith: menos de 2.5 triples** (62%). Con 80% de probabilidad: más de 0.5 / menos de 4.5.
- Defensa de Cleveland Cavaliers contra bases/escoltas en triples: +3% respecto a la media; ajuste por su historial contra defensas similares: +4%.

**¿Por qué 2.2 triples?** (línea 2.5; 30.1 minutos esperados)

En corto:

- La pasó en 10 de 13 esta temporada (falló con 4, 3, 3)
- Con 26+ minutos (hoy se esperan 30): 7 de 10 en sus últimos 15
- Contra las ~10 mejores defensas en triples a bases/escoltas: 8 de 13 (últimos 40 partidos)
- Contra defensas débiles como la de hoy y con 26+ minutos: 7 de 13, con 2.8 de media (últimos 60 partidos)
- El rival es #8 de 30 en triples que concede a bases/escoltas por minuto (#1 = el que más concede; +4% frente a la media)
- Su zona principal es triple frontal (36% de sus tiros, 34% de acierto); el rival es #6 de 30 en acierto que deja ahí (36%, liga 35%)
- Cómo tira (últimos 15): recibe y tira 42% (36% de acierto), penetración 32% (59% de acierto), creado 21% (21% de acierto); en recibe y tira el rival es #17 de 30 en lo que deja (#1 = el que más; 1.07 puntos por tiro frente a 1.07 de media)
- Oportunidades: 6.5 triples intentados esperados al 36%
- El rival no tiene a Evan Mobley (2.0 triples por partido)
- Su equipo no tiene a Tyrese Haliburton: más tiros y balón para él
- Minutos: 30 esperados (titular, ±5)

Razonamiento (3 factores a favor, 3 en contra):

- ✅ Minutos: 30.1 esperados (titular, ±4.6).
- ✅ Forma: 1.2 en sus últimos 5, 1.5 esta temporada (13 partidos), 2.3 la temporada pasada (línea 2.5).
- ➖ Cómo produce triples: 6.5 triples intentados (su ritmo 7.0 por 36'; el rival concede +1% de triples en su reparto) × 36% esperado.
- ❌ Defensa: el rival concede +4% de triples por minuto a bases/escoltas (defensa débil); ajuste aplicado +3%; en su zona principal (triple) el rival concede 36% (liga 35%).
- ➖ Ritmo del partido: +0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ❌ Contra este rival: 3 (0 de 1 a favor).
- ✅ Últimos 10: la habría pasado 8 de 10.
- ❌ Bajas del rival: sin Evan Mobley (titular); +1.7% en esta estadística.
- ⚠️ sin Tyrese Haliburton, la estrella de su equipo (10 partidos suyos sin él): más tiros y balón para él por minuto (puntos +7%, triples +8%, asistencias +1%).
- ⚠️ Tyrese Haliburton ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ Johnny Furphy ya no jugó en sus últimos partidos: la baja ya está en sus minutos.

- ⚠️ Alertas: sin Tyrese Haliburton: más tiros para él.
- Triples **2.2** (por componentes 2.3 · por tasa por minuto y defensa rival 2.1): 6.5 triples intentados (su ritmo 7.0 por 36'; el rival concede +1% de triples en su reparto) × 36% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 30.8 | 28.9 | 26.8 | 29.6 | 33.0 |
| Triples anotados | 1.2 | 1.4 | 1.5 | 2.3 | 3.0 |
| Triples intentados | 5.0 | 5.4 | 5.5 | 6.2 | 7.0 |
| % triples | 24.0% | 25.9% | 28.2% | 37.9% | 42.9% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -12%, vs defensa media +4%, vs defensa débil +13%; rebotes: vs defensa fuerte +2%, vs defensa media -6%, vs defensa débil +4%; asistencias: vs defensa fuerte +2%, vs defensa media -10%, vs defensa débil +5%; triples: vs defensa fuerte -6%, vs defensa media -11%, vs defensa débil +21%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 36% | 34% | 35% | 36% |
| bajo el aro | 18% | 59% | 68% | 64% |
| triple de esquina | 17% | 37% | 38% | 38% |
| pintura | 17% | 44% | 45% | 44% |
| media distancia | 11% | 38% | 41% | 41% |

#### Kelly Oubre Jr. (bases/escoltas) vs Cleveland Cavaliers

- Minutos esperados: **25.9** (± 5.0); 75 partidos en la base.
- sin Tyrese Haliburton, la estrella de su equipo (9 partidos suyos sin él): más tiros y balón para él por minuto (puntos +3%, triples +1%, asistencias +4%)
- Tyrese Haliburton ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Johnny Furphy ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Su prop más probable hoy: **Kelly Oubre Jr.: menos de 1.5 triples** (61%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Cleveland Cavaliers contra bases/escoltas en triples: +3% respecto a la media; ajuste por su historial contra defensas similares: -2%.

**¿Por qué 1.3 triples?** (línea 1.5; 25.9 minutos esperados)

En corto:

- La pasó en 10 de 13 esta temporada (falló con 2, 2, 2)
- Con 22+ minutos (hoy se esperan 26): 8 de 11 en sus últimos 15
- Contra las ~10 mejores defensas en triples a bases/escoltas: 8 de 14 (últimos 40 partidos)
- Contra defensas débiles como la de hoy y con 22+ minutos: 8 de 14, con 1.5 de media (últimos 60 partidos)
- El rival es #8 de 30 en triples que concede a bases/escoltas por minuto (#1 = el que más concede; +4% frente a la media)
- Su zona principal es triple frontal (25% de sus tiros, 29% de acierto); el rival es #6 de 30 en acierto que deja ahí (36%, liga 35%)
- Cómo tira (últimos 15): recibe y tira 38% (28% de acierto), penetración 28% (70% de acierto), creado 12% (29% de acierto); en recibe y tira el rival es #17 de 30 en lo que deja (#1 = el que más; 1.07 puntos por tiro frente a 1.07 de media)
- Oportunidades: 4.3 triples intentados esperados al 34%
- El rival no tiene a Evan Mobley (2.0 triples por partido)
- Su equipo no tiene a Tyrese Haliburton: más tiros y balón para él
- Minutos: 26 esperados (titular, ±5)

Razonamiento (3 factores a favor, 4 en contra):

- ✅ Minutos: 25.9 esperados (titular, ±5.0).
- ✅ Forma: 1.2 en sus últimos 5, 1.0 esta temporada (13 partidos), 1.6 la temporada pasada (línea 1.5).
- ➖ Cómo produce triples: 4.3 triples intentados (su ritmo 5.7 por 36'; el rival concede +1% de triples en su reparto) × 34% esperado.
- ❌ Defensa: el rival concede +4% de triples por minuto a bases/escoltas (defensa débil); ajuste aplicado +3%; en su zona principal (triple) el rival concede 36% (liga 35%).
- ❌ Altura: mide 6'8", 4.1 pulgadas más que los bases/escoltas del rival (+1.4% en esta estadística).
- ➖ Ritmo del partido: +0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ❌ Contra este rival: 0, 2, 2, 4 (1 de 4 a favor).
- ✅ Últimos 10: la habría pasado 7 de 10.
- ❌ Bajas del rival: sin Evan Mobley (titular); +1.7% en esta estadística.
- ⚠️ sin Tyrese Haliburton, la estrella de su equipo (9 partidos suyos sin él): más tiros y balón para él por minuto (puntos +3%, triples +1%, asistencias +4%).
- ⚠️ Tyrese Haliburton ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ Johnny Furphy ya no jugó en sus últimos partidos: la baja ya está en sus minutos.

- ⚠️ Alertas: sin Tyrese Haliburton: más tiros para él.
- Triples **1.3** (por componentes 1.4 · por tasa por minuto y defensa rival 1.2): 4.3 triples intentados (su ritmo 5.7 por 36'; el rival concede +1% de triples en su reparto) × 34% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 27.8 | 25.0 | 24.5 | 31.9 | 26.0 |
| Triples anotados | 1.2 | 1.1 | 1.0 | 1.6 | 2.0 |
| Triples intentados | 4.4 | 3.9 | 4.0 | 4.6 | 5.2 |
| % triples | 27.3% | 28.2% | 25.0% | 35.1% | 38.1% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -4%, vs defensa media +3%, vs defensa débil +5%; rebotes: vs defensa fuerte -12%, vs defensa media +6%, vs defensa débil +10%; asistencias: vs defensa fuerte -20%, vs defensa media +21%, vs defensa débil +21%; triples: vs defensa fuerte +7%, vs defensa media -9%, vs defensa débil +9%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 29% | 68% | 68% | 64% |
| triple frontal | 25% | 29% | 35% | 36% |
| pintura | 23% | 48% | 45% | 44% |
| triple de esquina | 19% | 39% | 38% | 38% |
| media distancia | 5% | 41% | 41% | 41% |

#### James Harden (bases/escoltas) vs Indiana Pacers

- Minutos esperados: **33.2** (± 3.3); 100 partidos en la base.
- Evan Mobley ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- sin Jaylon Tyson (19 partidos): 34.3 min vs 34.5 con él; pts -13%/min
- Su prop más probable hoy: **James Harden: menos de 24.5 pts+ast** (61%). Con 80% de probabilidad: más de 15.5 / menos de 26.5.
- Defensa de Indiana Pacers contra bases/escoltas en pts+ast: +2% respecto a la media; ajuste por su historial contra defensas similares: -1%.

**¿Por qué 21.2 pts+ast?** (línea 24.5; 33.2 minutos esperados)

En corto:

- La pasó en 10 de 15 esta temporada (falló con 28, 36, 25, 28)
- Con 29+ minutos (hoy se esperan 33): 8 de 13 en sus últimos 15
- Contra las ~10 mejores defensas en puntos a bases/escoltas: 10 de 17 (últimos 40 partidos)
- Contra defensas débiles como la de hoy y con 29+ minutos: 3 de 13, con 28.8 de media (últimos 60 partidos)
- El rival es #7 de 30 en puntos que concede a bases/escoltas por minuto (#1 = el que más concede; +4% frente a la media)
- Su zona principal es triple frontal (49% de sus tiros, 36% de acierto); el rival es #12 de 30 en acierto que deja ahí (35%, liga 35%)
- Su segunda zona es pintura (23% de sus tiros, 41% de acierto); el rival es #6 de 30 en acierto que deja ahí (47%, liga 45%)
- El rival es #15 de 30 en tiros libres que concede a bases/escoltas (#1 = el que más; +2% frente a la media)
- Puntería: en sus últimos 10 metió el 96% de las canastas esperadas por sus tipos de tiro
- Cómo tira (últimos 15): creado 36% (43% de acierto), recibe y tira 32% (33% de acierto), penetración 29% (40% de acierto); en creado el rival es #23 de 30 en lo que deja (#1 = el que más; 0.91 puntos por tiro frente a 0.94 de media)
- Oportunidades: 10.9 tiros de campo y 4.6 libres esperados (1.05 puntos por tiro)
- Transición: el rival concede 11.6 puntos por partido al contraataque (#28 de 30, #1 = el que más); él anota 1.2 así por partido (ajuste aplicado -1.5%)
- Minutos: 33 esperados (titular, ±3)

Razonamiento (2 factores a favor, 1 en contra):

- ✅ Minutos: 33.2 esperados (titular, ±3.3).
- ➖ Forma: 24.4 en sus últimos 5, 22.5 esta temporada (15 partidos), 28.8 la temporada pasada (línea 24.5).
- ➖ Cómo produce puntos: 10.9 tiros de campo (su ritmo 13.4 por 36'; el rival concede +2% de tiros) × 1.05 puntos por tiro [triple frontal 49% de sus tiros al 36% (rival concede 35%, liga 35%); pintura 23% de sus tiros al 41% (rival concede 47%, liga 45%); bajo el aro 17% de sus tiros al 61% (rival concede 67%, liga 68%)] + 4.6 tiros libres × 85%.
- ➖ Cómo produce asistencias: asiste el 24.2% de las canastas de sus compañeros en pista × 26.0 canastas de compañeros esperadas (su equipo 44.3 por 48' contra esta defensa).
- ➖ Defensa: el rival concede +4% de puntos por minuto a bases/escoltas (defensa débil); ajuste aplicado +2%; en su zona principal (triple) el rival concede 35% (liga 35%).
- ➖ Ritmo del partido: +0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ❌ Contra este rival: 35 (0 de 1 a favor).
- ✅ Últimos 10: la habría pasado 7 de 10.
- ⚠️ Evan Mobley ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ sin Jaylon Tyson (19 partidos): 34.3 min vs 34.5 con él; pts -13%/min.

- Puntos **14.9** (por componentes 15.4 · por tasa por minuto y defensa rival 14.8): 10.9 tiros de campo (su ritmo 13.4 por 36'; el rival concede +2% de tiros) × 1.05 puntos por tiro [triple frontal 49% de sus tiros al 36% (rival concede 35%, liga 35%); pintura 23% de sus tiros al 41% (rival concede 47%, liga 45%); bajo el aro 17% de sus tiros al 61% (rival concede 67%, liga 68%)] + 4.6 tiros libres × 85%.
- Asistencias **6.3** (por componentes 6.5 · por tasa por minuto y defensa rival 6.4): asiste el 24.2% de las canastas de sus compañeros en pista × 26.0 canastas de compañeros esperadas (su equipo 44.3 por 48' contra esta defensa).

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 32.6 | 32.1 | 33.1 | 35.2 | 34.0 |
| Puntos | 17.2 | 15.6 | 16.2 | 22.8 | 28.0 |
| Tiros de campo intentados | 11.2 | 11.0 | 11.9 | 15.6 | 17.0 |
| % tiros de campo | 42.9% | 40.0% | 38.5% | 43.1% | 47.1% |
| Triples intentados | 7.0 | 6.5 | 6.9 | 8.0 | 11.0 |
| % triples | 40.0% | 41.5% | 37.5% | 36.7% | 45.5% |
| Tiros libres intentados | 5.4 | 4.7 | 5.1 | 7.4 | 8.0 |
| % tiros libres | 88.9% | 87.2% | 85.7% | 87.6% | 87.5% |
| Jugadas que usa por 36 min | 17.9 | 17.3 | 18.5 | 23.0 | 23.8 |
| Asistencias | 7.2 | 6.3 | 6.3 | 7.6 | 7.0 |
| % de las canastas de compañeros que asiste | 27.1% | 24.8% | 24.5% | 31.2% | 28.2% |
| Pérdidas por jugada | 16.1% | 15.5% | 16.5% | 16.4% | 8.9% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +0%, vs defensa media +4%, vs defensa débil -5%; rebotes: vs defensa fuerte -11%, vs defensa media +2%, vs defensa débil +15%; asistencias: vs defensa fuerte -9%, vs defensa media -10%, vs defensa débil +18%; triples: vs defensa fuerte +2%, vs defensa media -4%, vs defensa débil +3%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 49% | 36% | 35% | 35% |
| pintura | 23% | 41% | 45% | 47% |
| bajo el aro | 17% | 61% | 68% | 67% |
| media distancia | 8% | 43% | 41% | 44% |
| triple de esquina | 4% | 41% | 38% | 39% |

#### Tyrese Proctor (bases/escoltas) vs Indiana Pacers

- Minutos esperados: **30.2** (± 4.1); 68 partidos en la base.
- Evan Mobley ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- sin Jaylon Tyson (18 partidos): 16.1 min vs 11.5 con él; pts -10%/min, reb -9%/min, ast -14%/min
- Su prop más probable hoy: **Tyrese Proctor: menos de 3.5 asistencias** (60%). Con 80% de probabilidad: más de 0.5 / menos de 5.5.
- Defensa de Indiana Pacers contra bases/escoltas en asistencias: +1% respecto a la media; ajuste por su historial contra defensas similares: -2%.

**¿Por qué 3.3 asistencias?** (línea 3.5; 30.2 minutos esperados)

En corto:

- La pasó en 12 de 15 esta temporada (falló con 10, 4, 5)
- Con 26+ minutos (hoy se esperan 30): 2 de 3 en sus últimos 15
- Hoy juega más que de costumbre (30 min frente a 24): con 26+ minutos, esta temporada y la pasada, la pasó 3 de 5 (60%)
- Contra las ~10 mejores defensas en asistencias a bases/escoltas: 13 de 14 (últimos 40 partidos)
- El rival es #16 de 30 en asistencias que concede a bases/escoltas por minuto (#1 = el que más concede; +1% frente a la media)
- Asistencias esperadas: 2.8 por partido si sus compañeros metieran lo normal (tiene 2.9; con él en pista metieron el 105% de lo esperado por tipo de tiro, últimos 10); ajuste aplicado -1.2%
- Oportunidades: asiste el 16% de las canastas de sus compañeros con él en pista
- Minutos: 30 esperados (titular, ±4)

Razonamiento (3 factores a favor, 0 en contra):

- ✅ Minutos: 30.2 esperados (titular, ±4.1).
- ➖ Forma: 3.4 en sus últimos 5, 2.7 esta temporada (15 partidos), 1.4 la temporada pasada (línea 3.5).
- ➖ Cómo produce asistencias: asiste el 16.5% de las canastas de sus compañeros en pista × 23.4 canastas de compañeros esperadas (su equipo 44.3 por 48' contra esta defensa).
- ➖ Defensa: el rival concede +1% de asistencias por minuto a bases/escoltas (defensa media); ajuste aplicado +1%.
- ➖ Ritmo del partido: +0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 1, 0, 0 (3 de 3 a favor).
- ✅ Últimos 10: la habría pasado 8 de 10.
- ⚠️ Evan Mobley ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ sin Jaylon Tyson (18 partidos): 16.1 min vs 11.5 con él; pts -10%/min, reb -9%/min, ast -14%/min.

- Asistencias **3.3** (por componentes 3.3 · por tasa por minuto y defensa rival 3.4): asiste el 16.5% de las canastas de sus compañeros en pista × 23.4 canastas de compañeros esperadas (su equipo 44.3 por 48' contra esta defensa).

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 27.8 | 24.5 | 20.3 | 10.6 | 9.3 |
| Asistencias | 3.4 | 2.9 | 2.7 | 1.4 | 0.3 |
| % de las canastas de compañeros que asiste | 15.1% | 15.0% | 16.3% | 15.9% | 3.7% |
| Pérdidas por jugada | 8.7% | 9.0% | 8.3% | 14.2% | 0.0% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -23%, vs defensa media +16%, vs defensa débil +12%; rebotes: vs defensa fuerte -31%, vs defensa media -29%, vs defensa débil +47%; asistencias: vs defensa fuerte -4%, vs defensa media -17%, vs defensa débil +16%; triples: vs defensa fuerte +10%, vs defensa media -18%, vs defensa débil +11%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 47% | 39% | 35% | 35% |
| bajo el aro | 20% | 68% | 68% | 67% |
| pintura | 13% | 39% | 45% | 47% |
| triple de esquina | 11% | 39% | 38% | 39% |
| media distancia | 10% | 47% | 41% | 44% |

## Toronto Raptors @ Detroit Pistons

Diferencia esperada: Detroit Pistons por 7.5.

Parte de lesiones: Taurean Prince (Out); RJ Barrett (Out); Cade Cunningham (Day-To-Day); Nate Bittle (Out); Ronald Holland II (Out); Ugonna Onyenso (Day-To-Day); Collin Murray-Boyles (Out); Ebuka Okorie (Out); Kawhi Leonard (Out).

Ventajas del partido (los dos lados): puntos esperados frente a su media de los últimos 10, ajuste por la defensa rival y diferencia de estatura con los rivales de su posición.

| Equipo | Jugador | Puntos esperados | Su media (últ. 10) | Defensa rival en puntos | Rebotes esperados | Altura vs rival |
|---|---|---|---|---|---|---|
| DET | Cade Cunningham | 24.5 | 27.1 | +0% | 5.3 | +3.6" |
| TOR | Scottie Barnes | 19.0 | 23.8 | -2% | 7.4 | -0.3" |
| TOR | Immanuel Quickley | 20.0 | 17.7 | -5% | 3.6 | -3.4" |
| DET | Daniss Jenkins | 15.7 | 15.3 | +0% | 4.1 | +1.6" |
| TOR | Ja'Kobe Walter | 14.1 | 12.1 | -4% | 3.6 | -1.4" |
| DET | Kevin Huerter | 12.6 | 11.5 | +0% | 3.6 | +3.6" |
| DET | Duncan Robinson | 14.5 | 17.1 | -3% | 2.6 | -0.1" |
| DET | Ausar Thompson | 10.9 | 10.9 | +1% | 7.7 | +4.6" |
| TOR | Jakob Poeltl | 10.6 | 9.6 | -7% | 7.8 | +4.0" |
| TOR | Jamal Shead | 8.2 | 9.7 | -5% | 2.3 | -4.4" |

Las 8 más probables (máximo 2 por jugador: las de un mismo jugador suelen ganar o perder juntas).

| Prop | Prob. final | Modelo | Casa | Esperado | Últ. 10 | Temporada | vs este rival | Cuota (implícita) |
|---|---|---|---|---|---|---|---|---|
| **Jamison Battle: menos de 1.5 asistencias** ⚠️ suplente | **67%** | 68% | 66% | 1.2 ± 1.2 | 9/10 | 13/15 | 0 | 1.41 (71%) |
| **Cade Cunningham: más de 0.5 robos** | **67%** | 68% | 66% | 1.3 ± 1.3 | 7/10 | 10/13 | 2, 3 | 1.44 (69%) |
| **Jamal Shead: más de 0.5 triples** ⚠️ suplente | **65%** | 66% | 64% | 1.2 ± 1.1 | 8/10 | 9/15 | 1, 0, 0 | 1.46 (69%) |
| **Jamison Battle: menos de 2.5 triples** ⚠️ suplente | **65%** | 69% | 58% | 1.8 ± 1.6 | 5/10 | 10/15 | 0 | 1.61 (62%) |
| **Javonte Green: menos de 1.5 triples** ⚠️ suplente | **63%** | 66% | 58% | 1.3 ± 1.4 | 9/10 | 12/14 | 0, 1, 0 | 1.60 (63%) |
| **Ja'Kobe Walter: menos de 4.5 rebotes** | **63%** | 67% | 57% | 3.6 ± 1.9 | 5/10 | 9/15 | 4, 2, 3 | 1.65 (61%) |
| **Jakob Poeltl: más de 0.5 tapones** | **63%** | 66% | 59% | 1.4 ± 1.3 | 4/10 | 6/13 | 0, 1, 0 | 1.62 (62%) |
| **Paul Reed: más de 0.5 robos** ⚠️ suplente | **62%** | 63% | 61% | 1.1 ± 1.1 | 7/10 | 9/14 | 1, 0, 3 | 1.55 (65%) |

### Fichas de los jugadores destacados

#### Jamison Battle (aleros/ala-pívots) vs Detroit Pistons

- Minutos esperados: **21.7** (± 10.0); 81 partidos en la base.
- sin RJ Barrett, la estrella de su equipo (20 partidos suyos sin él): más tiros y balón para él por minuto (puntos -10%, triples -15%, asistencias +40%)
- sin RJ Barrett (20 partidos): 11.8 min vs 10.4 con él
- sin Collin Murray-Boyles (23 partidos): 9.5 min vs 11.3 con él; pts -8%/min, ast +35%/min
- Kawhi Leonard ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Su prop más probable hoy: **Jamison Battle: menos de 1.5 asistencias** (67%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Detroit Pistons contra aleros/ala-pívots en asistencias: -6% respecto a la media; ajuste por su historial contra defensas similares: -1%.

**¿Por qué 1.2 asistencias?** (línea 1.5; 21.7 minutos esperados)

En corto:

- La pasó en 13 de 15 esta temporada (falló con 2, 2)
- Con 18+ minutos (hoy se esperan 22): 8 de 9 en sus últimos 15
- Contra las ~10 mejores defensas en asistencias a aleros/ala-pívots: 11 de 12 (últimos 40 partidos)
- El rival es #26 de 30 en asistencias que concede a aleros/ala-pívots por minuto (#1 = el que más concede; -6% frente a la media)
- Asistencias esperadas: 0.3 por partido si sus compañeros metieran lo normal (tiene 0.3; con él en pista metieron el 90% de lo esperado por tipo de tiro, últimos 10); ajuste aplicado +5.8%
- Oportunidades: asiste el 4% de las canastas de sus compañeros con él en pista
- Su equipo no tiene a RJ Barrett: más tiros y balón para él
- Minutos: 22 esperados (suplente, ±10)

Razonamiento (4 factores a favor, 1 en contra):

- ❌ Minutos: 21.7 esperados (suplente, ±10.0).
- ✅ Forma: 0.2 en sus últimos 5, 0.4 esta temporada (15 partidos), 0.4 la temporada pasada (línea 1.5).
- ➖ Cómo produce asistencias: asiste el 4.4% de las canastas de sus compañeros en pista × 14.4 canastas de compañeros esperadas (su equipo 37.9 por 48' contra esta defensa).
- ✅ Defensa: el rival concede -6% de asistencias por minuto a aleros/ala-pívots (defensa fuerte); ajuste aplicado -6%.
- ➖ Ritmo del partido: -1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 0 (1 de 1 a favor).
- ✅ Últimos 10: la habría pasado 9 de 10.
- ⚠️ sin RJ Barrett, la estrella de su equipo (20 partidos suyos sin él): más tiros y balón para él por minuto (puntos -10%, triples -15%, asistencias +40%).
- ⚠️ sin RJ Barrett (20 partidos): 11.8 min vs 10.4 con él.
- ⚠️ sin Collin Murray-Boyles (23 partidos): 9.5 min vs 11.3 con él; pts -8%/min, ast +35%/min.
- ⚠️ Kawhi Leonard ya no jugó en sus últimos partidos: la baja ya está en sus minutos.

- ⚠️ Alertas: suplente, minutos inestables, sin RJ Barrett: más tiros para él.
- Asistencias **1.2** (por componentes 1.2 · por tasa por minuto y defensa rival 1.2): asiste el 4.4% de las canastas de sus compañeros en pista × 14.4 canastas de compañeros esperadas (su equipo 37.9 por 48' contra esta defensa).

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 19.6 | 20.5 | 18.7 | 9.0 | 4.0 |
| Asistencias | 0.2 | 0.3 | 0.4 | 0.4 | 0.0 |
| % de las canastas de compañeros que asiste | 1.5% | 2.0% | 2.8% | 5.0% | 0.0% |
| Pérdidas por jugada | 2.6% | 4.5% | 5.3% | 10.5% | - |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -18%, vs defensa media +12%, vs defensa débil -2%; rebotes: vs defensa fuerte -1%, vs defensa media -0%, vs defensa débil +1%; asistencias: vs defensa fuerte +17%, vs defensa media -46%, vs defensa débil +31%; triples: vs defensa fuerte -34%, vs defensa media +36%, vs defensa débil -10%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 43% | 42% | 35% | 32% |
| triple de esquina | 22% | 40% | 38% | 39% |
| bajo el aro | 21% | 65% | 68% | 65% |
| pintura | 8% | 54% | 45% | 43% |
| media distancia | 5% | 38% | 41% | 39% |

#### Cade Cunningham (bases/escoltas) vs Toronto Raptors

- Minutos esperados: **36.8** (± 6.3); 92 partidos en la base.
- en el parte de lesiones: day-to-day
- Su prop más probable hoy: **Cade Cunningham: más de 0.5 robos** (67%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Toronto Raptors contra bases/escoltas en robos: -7% respecto a la media; ajuste por su historial contra defensas similares: -5%.

**¿Por qué 1.3 robos?** (línea 0.5; 36.8 minutos esperados)

En corto:

- La pasó en 10 de 13 esta temporada (falló con 0, 0, 0)
- Con 33+ minutos (hoy se esperan 37): 8 de 11 en sus últimos 15
- Contra las ~10 mejores defensas en robos a bases/escoltas: 15 de 20 (últimos 40 partidos)
- Contra defensas fuertes como la de hoy y con 33+ minutos: 17 de 24, con 1.2 de media (últimos 60 partidos)
- El rival es #24 de 30 en robos que concede a bases/escoltas por minuto (#1 = el que más concede; -7% frente a la media)
- Oportunidades de robo (últimos 10): el rival perdió 12.3 balones por partido con él en pista y robó el 11%
- El rival es #24 de 30 en balones que pierde (#1 = el que más; 12.9 por partido)
- El rival no tiene a RJ Barrett (0.2 robos por partido)
- Minutos: 37 esperados (titular, ±6)

Razonamiento (3 factores a favor, 2 en contra):

- ❌ Minutos: 36.8 esperados (titular, ±6.3).
- ✅ Forma: 1.0 en sus últimos 5, 1.4 esta temporada (13 partidos), 1.3 la temporada pasada (línea 0.5).
- ➖ Cómo produce robos: roba el 12.1% de las pérdidas del rival en pista × 14.5 pérdidas esperadas del rival.
- ❌ Defensa: el rival concede -7% de robos por minuto a bases/escoltas (defensa fuerte); ajuste aplicado -7%.
- ➖ Ritmo del partido: -1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 2, 3 (2 de 2 a favor).
- ✅ Últimos 10: la habría pasado 7 de 10.
- ⚠️ en el parte de lesiones: day-to-day.

- ⚠️ Alertas: minutos inestables, en el parte de lesiones.
- Robos **1.3** (por componentes 1.3 · por tasa por minuto y defensa rival 1.2): roba el 12.1% de las pérdidas del rival en pista × 14.5 pérdidas esperadas del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 37.4 | 35.7 | 35.0 | 33.9 | 33.5 |
| Robos | 1.0 | 1.4 | 1.4 | 1.4 | 2.5 |
| % de las pérdidas del rival que roba | 8.8% | 11.4% | 12.2% | 12.4% | 26.3% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +0%, vs defensa media -5%, vs defensa débil +7%; rebotes: vs defensa fuerte -4%, vs defensa media -7%, vs defensa débil +11%; asistencias: vs defensa fuerte -8%, vs defensa media -5%, vs defensa débil +14%; triples: vs defensa fuerte -9%, vs defensa media +8%, vs defensa débil +5%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 29% | 34% | 35% | 34% |
| pintura | 29% | 45% | 45% | 44% |
| bajo el aro | 23% | 62% | 68% | 68% |
| media distancia | 17% | 48% | 41% | 39% |
| triple de esquina | 3% | 33% | 38% | 38% |

#### Jamal Shead (bases/escoltas) vs Detroit Pistons

- Minutos esperados: **26.5** (± 4.7); 104 partidos en la base.
- sin RJ Barrett, la estrella de su equipo (20 partidos suyos sin él): más tiros y balón para él por minuto (puntos +5%, triples +26%, asistencias -10%)
- sin RJ Barrett (26 partidos): 25.3 min vs 22.7 con él
- sin Collin Murray-Boyles (26 partidos): 22.3 min vs 23.7 con él; pts -12%/min
- Kawhi Leonard ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Su prop más probable hoy: **Jamal Shead: más de 0.5 triples** (65%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Detroit Pistons contra bases/escoltas en triples: -6% respecto a la media; ajuste por su historial contra defensas similares: -6%.

**¿Por qué 1.2 triples?** (línea 0.5; 26.5 minutos esperados)

En corto:

- La pasó en 9 de 15 esta temporada (falló con 0, 0, 0, 0)
- Con 23+ minutos (hoy se esperan 27): 6 de 8 en sus últimos 15
- Contra las ~10 mejores defensas en triples a bases/escoltas: 4 de 9 (últimos 40 partidos)
- Contra defensas fuertes como la de hoy y con 23+ minutos: 3 de 8, con 0.4 de media (últimos 60 partidos)
- El rival es #28 de 30 en triples que concede a bases/escoltas por minuto (#1 = el que más concede; -7% frente a la media)
- Su zona principal es triple frontal (42% de sus tiros, 32% de acierto); el rival es #30 de 30 en acierto que deja ahí (32%, liga 35%)
- Cómo tira (últimos 15): recibe y tira 34% (27% de acierto), penetración 32% (51% de acierto), creado 28% (35% de acierto); en recibe y tira el rival es #19 de 30 en lo que deja (#1 = el que más; 1.06 puntos por tiro frente a 1.07 de media)
- Oportunidades: 4.4 triples intentados esperados al 30%
- Su equipo no tiene a RJ Barrett: más tiros y balón para él
- Minutos: 27 esperados (suplente, ±5)

Razonamiento (2 factores a favor, 4 en contra):

- ❌ Minutos: 26.5 esperados (suplente, ±4.7).
- ✅ Forma: 1.2 en sus últimos 5, 1.0 esta temporada (15 partidos), 1.1 la temporada pasada (línea 0.5).
- ➖ Cómo produce triples: 4.4 triples intentados (su ritmo 5.6 por 36'; el rival concede +2% de triples en su reparto) × 30% esperado.
- ❌ Defensa: el rival concede -7% de triples por minuto a bases/escoltas (defensa fuerte); ajuste aplicado -6%; en su zona principal (triple) el rival concede 32% (liga 35%).
- ❌ Altura: mide 6'1", 4.4 pulgadas menos que los bases/escoltas del rival (-1.6% en esta estadística).
- ➖ Ritmo del partido: -1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ❌ Contra este rival: 1, 0, 0 (1 de 3 a favor).
- ✅ Últimos 10: la habría pasado 8 de 10.
- ⚠️ sin RJ Barrett, la estrella de su equipo (20 partidos suyos sin él): más tiros y balón para él por minuto (puntos +5%, triples +26%, asistencias -10%).
- ⚠️ sin RJ Barrett (26 partidos): 25.3 min vs 22.7 con él.
- ⚠️ sin Collin Murray-Boyles (26 partidos): 22.3 min vs 23.7 con él; pts -12%/min.
- ⚠️ Kawhi Leonard ya no jugó en sus últimos partidos: la baja ya está en sus minutos.

- ⚠️ Alertas: suplente.
- Triples **1.2** (por componentes 1.3 · por tasa por minuto y defensa rival 1.2): 4.4 triples intentados (su ritmo 5.6 por 36'; el rival concede +2% de triples en su reparto) × 30% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 22.8 | 24.9 | 23.7 | 23.3 | 25.7 |
| Triples anotados | 1.2 | 1.4 | 1.0 | 1.1 | 0.3 |
| Triples intentados | 4.0 | 4.5 | 3.5 | 3.4 | 3.0 |
| % triples | 30.0% | 31.1% | 28.3% | 32.2% | 11.1% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -6%, vs defensa media -1%, vs defensa débil +8%; rebotes: vs defensa fuerte -5%, vs defensa media +2%, vs defensa débil +4%; asistencias: vs defensa fuerte -12%, vs defensa media -10%, vs defensa débil +25%; triples: vs defensa fuerte -23%, vs defensa media -13%, vs defensa débil +34%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 42% | 32% | 35% | 32% |
| pintura | 22% | 38% | 45% | 43% |
| bajo el aro | 19% | 59% | 68% | 65% |
| triple de esquina | 10% | 33% | 38% | 39% |
| media distancia | 7% | 36% | 41% | 39% |

#### Javonte Green (bases/escoltas) vs Toronto Raptors

- Minutos esperados: **20.9** (± 8.5); 106 partidos en la base.
- Su prop más probable hoy: **Javonte Green: menos de 1.5 triples** (63%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Toronto Raptors contra bases/escoltas en triples: -1% respecto a la media; ajuste por su historial contra defensas similares: +4%.

**¿Por qué 1.3 triples?** (línea 1.5; 20.9 minutos esperados)

En corto:

- La pasó en 12 de 14 esta temporada (falló con 3, 5)
- Con 17+ minutos (hoy se esperan 21): 7 de 9 en sus últimos 15
- Contra las ~10 mejores defensas en triples a bases/escoltas: 18 de 23 (últimos 40 partidos)
- Contra defensas medias como la de hoy y con 17+ minutos: 8 de 10, con 1.4 de media (últimos 60 partidos)
- El rival es #14 de 30 en triples que concede a bases/escoltas por minuto (#1 = el que más concede; -0% frente a la media)
- Su zona principal es triple frontal (39% de sus tiros, 28% de acierto); el rival es #23 de 30 en acierto que deja ahí (34%, liga 35%)
- Su segunda zona es triple de esquina (25% de sus tiros, 45% de acierto); el rival es #15 de 30 en acierto que deja ahí (38%, liga 38%)
- Cómo tira (últimos 15): recibe y tira 70% (30% de acierto), penetración 13% (78% de acierto), aro 7% (60% de acierto); en recibe y tira el rival es #15 de 30 en lo que deja (#1 = el que más; 1.07 puntos por tiro frente a 1.07 de media)
- Oportunidades: 3.8 triples intentados esperados al 35%
- El rival no tiene a RJ Barrett (1.7 triples por partido)
- Minutos: 21 esperados (suplente, ±9)

Razonamiento (3 factores a favor, 3 en contra):

- ❌ Minutos: 20.9 esperados (suplente, ±8.5).
- ✅ Forma: 0.8 en sus últimos 5, 1.1 esta temporada (14 partidos), 1.2 la temporada pasada (línea 1.5).
- ➖ Cómo produce triples: 3.8 triples intentados (su ritmo 6.8 por 36'; el rival concede +1% de triples en su reparto) × 35% esperado.
- ➖ Defensa: el rival concede -0% de triples por minuto a bases/escoltas (defensa media); ajuste aplicado -1%; en su zona principal (triple) el rival concede 34% (liga 35%).
- ❌ Altura: mide 6'5", 2.6 pulgadas más que los bases/escoltas del rival (+0.9% en esta estadística).
- ➖ Ritmo del partido: -1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 0, 1, 0 (3 de 3 a favor).
- ✅ Últimos 10: la habría pasado 9 de 10.
- ❌ Bajas del rival: sin RJ Barrett (titular); +1.7% en esta estadística.

- ⚠️ Alertas: suplente, minutos inestables.
- Triples **1.3** (por componentes 1.3 · por tasa por minuto y defensa rival 1.3): 3.8 triples intentados (su ritmo 6.8 por 36'; el rival concede +1% de triples en su reparto) × 35% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 19.2 | 19.1 | 18.6 | 17.1 | 12.3 |
| Triples anotados | 0.8 | 0.8 | 1.1 | 1.1 | 0.3 |
| Triples intentados | 3.2 | 3.2 | 3.6 | 3.0 | 1.3 |
| % triples | 25.0% | 25.0% | 29.4% | 36.9% | 25.0% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +3%, vs defensa media -16%, vs defensa débil +11%; rebotes: vs defensa fuerte -2%, vs defensa media +2%, vs defensa débil -0%; asistencias: vs defensa fuerte -6%, vs defensa media +7%, vs defensa débil -1%; triples: vs defensa fuerte -11%, vs defensa media -6%, vs defensa débil +24%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 39% | 28% | 35% | 34% |
| triple de esquina | 25% | 45% | 38% | 38% |
| bajo el aro | 25% | 69% | 68% | 68% |
| pintura | 9% | 39% | 45% | 44% |
| media distancia | 3% | 40% | 41% | 39% |

#### Ja'Kobe Walter (bases/escoltas) vs Detroit Pistons

- Minutos esperados: **34.3** (± 3.0); 94 partidos en la base.
- sin RJ Barrett, la estrella de su equipo (20 partidos suyos sin él): más tiros y balón para él por minuto (puntos -1%, triples -15%, asistencias -10%)
- sin RJ Barrett (20 partidos): 21.9 min vs 23.4 con él
- sin Collin Murray-Boyles (21 partidos): 22.0 min vs 23.3 con él; pts +8%/min, reb -8%/min
- Kawhi Leonard ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Su prop más probable hoy: **Ja'Kobe Walter: menos de 4.5 rebotes** (63%). Con 80% de probabilidad: más de 1.5 / menos de 5.5.
- Defensa de Detroit Pistons contra bases/escoltas en rebotes: -12% respecto a la media; ajuste por su historial contra defensas similares: -5%.

**¿Por qué 3.6 rebotes?** (línea 4.5; 34.3 minutos esperados)

En corto:

- La pasó en 9 de 15 esta temporada (falló con 7, 5, 6, 6)
- Con 30+ minutos (hoy se esperan 34): 6 de 10 en sus últimos 15
- Contra las ~10 mejores defensas en rebotes a bases/escoltas: 16 de 19 (últimos 40 partidos)
- Contra defensas fuertes como la de hoy y con 30+ minutos: 6 de 8, con 3.0 de media (últimos 60 partidos)
- El rival es #30 de 30 en rebotes que concede a bases/escoltas por minuto (#1 = el que más concede; -12% frente a la media)
- El rival es #26 de 30 en rebotes que concede en total (#1 = el que más)
- El rival es #14 de 30 en rebotes ofensivos que concede en total (#1 = el que más)
- Rebotes disponibles con él en pista (últimos 10): 28.5 tiros fallados del rival y 33.8 de su equipo por partido; se queda el 9% y el 4%; el rival falla 46.9 tiros por partido (#20 de 30, #1 = el que más falla)
- Minutos: 34 esperados (titular, ±3)

Razonamiento (4 factores a favor, 0 en contra):

- ✅ Minutos: 34.3 esperados (titular, ±3.0).
- ✅ Forma: 3.6 en sus últimos 5, 4.0 esta temporada (15 partidos), 2.8 la temporada pasada (línea 4.5).
- ➖ Cómo produce rebotes: defensivos 2.9 = captura el 10.1% de los fallos del rival en pista × 43.5 fallos esperados del rival (liga 46.9) × 71% del partido; ofensivos 1.1 = 3.6% de los fallos de su equipo × 46.8.
- ✅ Defensa: el rival concede -12% de rebotes por minuto a bases/escoltas (defensa fuerte); ajuste aplicado -12%.
- ➖ Ritmo del partido: -1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 4, 2, 3 (3 de 3 a favor).
- ➖ Últimos 10: la habría pasado 5 de 10.
- ⚠️ sin RJ Barrett, la estrella de su equipo (20 partidos suyos sin él): más tiros y balón para él por minuto (puntos -1%, triples -15%, asistencias -10%).
- ⚠️ sin RJ Barrett (20 partidos): 21.9 min vs 23.4 con él.
- ⚠️ sin Collin Murray-Boyles (21 partidos): 22.0 min vs 23.3 con él; pts +8%/min, reb -8%/min.
- ⚠️ Kawhi Leonard ya no jugó en sus últimos partidos: la baja ya está en sus minutos.

- Rebotes **3.6** (por componentes 4.0 · por tasa por minuto y defensa rival 3.4): defensivos 2.9 = captura el 10.1% de los fallos del rival en pista × 43.5 fallos esperados del rival (liga 46.9) × 71% del partido; ofensivos 1.1 = 3.6% de los fallos de su equipo × 46.8.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 34.8 | 33.2 | 31.3 | 21.5 | 19.3 |
| Rebotes | 3.6 | 4.1 | 4.0 | 2.6 | 3.0 |
| % de los fallos del rival que captura | 8.7% | 9.5% | 10.2% | 9.2% | 12.1% |
| % de los fallos de su equipo que captura | 3.0% | 4.1% | 3.8% | 3.5% | 3.6% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -2%, vs defensa media +4%, vs defensa débil -2%; rebotes: vs defensa fuerte -13%, vs defensa media +5%, vs defensa débil +12%; asistencias: vs defensa fuerte -15%, vs defensa media -19%, vs defensa débil +36%; triples: vs defensa fuerte -15%, vs defensa media +26%, vs defensa débil -12%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 39% | 36% | 35% | 32% |
| triple de esquina | 30% | 40% | 38% | 39% |
| bajo el aro | 18% | 65% | 68% | 65% |
| pintura | 10% | 37% | 45% | 43% |
| media distancia | 3% | 41% | 41% | 39% |

## Washington Wizards @ Chicago Bulls

Diferencia esperada: Chicago Bulls por 2.5.

Parte de lesiones: Reece Beekman (Out); Justin Champagnie (Out); Jamir Watkins (Out); Tristan Vukcevic (Out); Caleb Wilson (Out); Tobe Awaka (Out); Felix Okpara (Day-To-Day); Noa Essengue (Day-To-Day).

Ventajas del partido (los dos lados): puntos esperados frente a su media de los últimos 10, ajuste por la defensa rival y diferencia de estatura con los rivales de su posición.

| Equipo | Jugador | Puntos esperados | Su media (últ. 10) | Defensa rival en puntos | Rebotes esperados | Altura vs rival |
|---|---|---|---|---|---|---|
| WSH | Kyshawn George | 20.1 | 19.4 | +5% | 5.4 | +0.4" |
| WSH | AJ Dybantsa | 19.7 | 15.9 | +5% | 7.3 | +1.4" |
| WSH | Anthony Davis | 24.8 | 25.3 | +5% | 10.9 | +2.4" |
| WSH | Trae Young | 19.2 | 15.6 | +1% | 2.9 | -2.4" |
| CHI | Matas Buzelis | 18.3 | 15.6 | +5% | 6.0 | -0.8" |
| CHI | Norman Powell | 22.1 | 21.5 | +1% | 3.3 | -0.6" |
| CHI | Josh Giddey | 12.8 | 11.9 | +1% | 6.6 | +2.4" |
| WSH | Alex Sarr | 14.0 | 12.5 | +4% | 7.6 | +1.0" |
| CHI | Isaac Okoro | 11.3 | 8.4 | +5% | 3.4 | -4.8" |
| CHI | Jalen Smith | 14.7 | 13.1 | +5% | 8.6 | -0.8" |

Las 8 más probables (máximo 2 por jugador: las de un mismo jugador suelen ganar o perder juntas).

| Prop | Prob. final | Modelo | Casa | Esperado | Últ. 10 | Temporada | vs este rival | Cuota (implícita) |
|---|---|---|---|---|---|---|---|---|
| **Alex Sarr: más de 1.5 robos+tapones** | **66%** | 69% | 63% | 2.5 ± 1.8 | 7/10 | 11/15 | 3, 0 | 1.52 (66%) |
| **AJ Dybantsa: menos de 1.5 triples** | **66%** | 70% | 62% | 1.2 ± 1.1 | 9/10 | 11/12 | - | 1.51 (66%) |
| **Bilal Coulibaly: más de 0.5 robos** ⚠️ suplente | **64%** | 65% | 64% | 1.1 ± 1.1 | 5/10 | 9/15 | 2, 0, 0 | 1.48 (67%) |
| **Trae Young: menos de 2.5 triples** | **63%** | 63% | 62% | 2.1 ± 1.5 | 6/10 | 10/16 | 4, 1, 7, 1 | 1.51 (66%) |
| **Isaac Okoro: menos de 1.5 triples** | **62%** | 67% | 56% | 1.3 ± 1.3 | 7/10 | 11/14 | 0, 1 | 1.69 (59%) |
| **Alex Sarr: menos de 1.5 triples** | **61%** | 63% | 59% | 1.3 ± 1.2 | 7/10 | 11/15 | 0, 2 | 1.58 (63%) |
| **Isaac Okoro: más de 0.5 robos** | **61%** | 57% | 66% | 1.0 ± 1.2 | 6/10 | 7/14 | 0, 1 | 1.44 (69%) |
| **Kyshawn George: más de 20.5 pts+reb** | **61%** | 67% | 51% | 25.4 ± 8.1 | 7/10 | 10/16 | 31, 29 | 1.82 (55%) |

### Fichas de los jugadores destacados

#### Alex Sarr (pívots) vs Chicago Bulls

- Minutos esperados: **28.3** (± 6.5); 63 partidos en la base.
- Justin Champagnie ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Jamir Watkins ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Su prop más probable hoy: **Alex Sarr: más de 1.5 robos+tapones** (66%). Con 80% de probabilidad: más de 0.5 / menos de 4.5.
- Defensa de Chicago Bulls contra pívots en robos+tapones: +13% respecto a la media; ajuste por su historial contra defensas similares: -1%.

**¿Por qué 2.5 robos+tapones?** (línea 1.5; 28.3 minutos esperados)

En corto:

- La pasó en 11 de 15 esta temporada (falló con 0, 0, 0, 0)
- Con 24+ minutos (hoy se esperan 28): 8 de 11 en sus últimos 15
- Contra las ~10 mejores defensas en robos a pívots: 10 de 17 (últimos 40 partidos)
- Contra defensas medias como la de hoy y con 24+ minutos: 6 de 11, con 2.6 de media (últimos 60 partidos)
- El rival es #13 de 30 en robos que concede a pívots por minuto (#1 = el que más concede; +4% frente a la media)
- Oportunidades de robo (últimos 10): el rival perdió 7.0 balones por partido con él en pista y robó el 10%
- El rival es #6 de 30 en balones que pierde (#1 = el que más; 15.1 por partido)
- El rival no tiene a Caleb Wilson (2.7 robos+tapones por partido)
- Minutos: 28 esperados (titular, ±6)

Razonamiento (4 factores a favor, 1 en contra):

- ❌ Minutos: 28.3 esperados (titular, ±6.5).
- ✅ Forma: 2.2 en sus últimos 5, 2.1 esta temporada (15 partidos), 2.8 la temporada pasada (línea 1.5).
- ➖ Cómo produce robos: roba el 11.2% de las pérdidas del rival en pista × 14.1 pérdidas esperadas del rival.
- ➖ Cómo produce tapones: tapona el 4.5% de los tiros de 2 del rival en pista × 53.3 tiros de 2 esperados del rival.
- ✅ Defensa: el rival concede +4% de robos por minuto a pívots (defensa media); ajuste aplicado +13%.
- ✅ Ritmo del partido: +2% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ➖ Contra este rival: 3, 0 (1 de 2 a favor).
- ✅ Últimos 10: la habría pasado 7 de 10.
- ⚠️ Justin Champagnie ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ Jamir Watkins ya no jugó en sus últimos partidos: la baja ya está en sus minutos.

- ⚠️ Alertas: minutos inestables.
- Robos **0.8** (por componentes 0.9 · por tasa por minuto y defensa rival 0.8): roba el 11.2% de las pérdidas del rival en pista × 14.1 pérdidas esperadas del rival.
- Tapones **1.7** (por componentes 1.4 · por tasa por minuto y defensa rival 1.8): tapona el 4.5% de los tiros de 2 del rival en pista × 53.3 tiros de 2 esperados del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 29.8 | 28.4 | 27.2 | 27.2 | 25.5 |
| Robos | 0.4 | 0.7 | 0.9 | 0.8 | 0.0 |
| % de las pérdidas del rival que roba | 6.1% | 10.0% | 11.6% | 11.2% | 0.0% |
| Tapones | 1.8 | 1.3 | 1.3 | 2.0 | 1.5 |
| % de los tiros de 2 del rival que tapona | 4.9% | 3.9% | 4.0% | 6.2% | 5.3% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -4%, vs defensa media +4%, vs defensa débil +3%; rebotes: vs defensa fuerte -5%, vs defensa media +14%, vs defensa débil -4%; asistencias: vs defensa fuerte +15%, vs defensa media -19%, vs defensa débil -5%; triples: vs defensa fuerte -8%, vs defensa media -20%, vs defensa débil +35%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 33% | 75% | 68% | 66% |
| pintura | 30% | 41% | 45% | 44% |
| triple frontal | 23% | 34% | 35% | 36% |
| media distancia | 8% | 37% | 41% | 42% |
| triple de esquina | 6% | 34% | 38% | 37% |

#### AJ Dybantsa (aleros/ala-pívots) vs Chicago Bulls

- Minutos esperados: **35.1** (± 4.3); 12 partidos en la base.
- Justin Champagnie ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Jamir Watkins ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Su prop más probable hoy: **AJ Dybantsa: menos de 1.5 triples** (66%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Chicago Bulls contra aleros/ala-pívots en triples: +3% respecto a la media; ajuste por su historial contra defensas similares: +1%.

**¿Por qué 1.2 triples?** (línea 1.5; 35.1 minutos esperados)

En corto:

- La pasó en 11 de 12 esta temporada; los fallos, en partidos raros (paliza de 28)
- Con 31+ minutos (hoy se esperan 35): 8 de 8 en sus últimos 15
- Contra las ~10 mejores defensas en triples a aleros/ala-pívots: 5 de 6 (últimos 40 partidos)
- El rival es #6 de 30 en triples que concede a aleros/ala-pívots por minuto (#1 = el que más concede; +6% frente a la media)
- Su zona principal es triple de esquina (14% de sus tiros, 29% de acierto); el rival es #22 de 30 en acierto que deja ahí (37%, liga 38%)
- Cómo tira (últimos 15): penetración 37% (45% de acierto), recibe y tira 23% (25% de acierto), creado 22% (42% de acierto); en penetración el rival es #10 de 30 en lo que deja (#1 = el que más; 1.10 puntos por tiro frente a 1.08 de media)
- Oportunidades: 4.5 triples intentados esperados al 29%
- El rival no tiene a Caleb Wilson (2.3 triples por partido)
- Minutos: 35 esperados (titular, ±4)

Razonamiento (3 factores a favor, 3 en contra):

- ✅ Minutos: 35.1 esperados (titular, ±4.3).
- ✅ Forma: 0.8 en sus últimos 5, 0.8 esta temporada (12 partidos) (línea 1.5).
- ➖ Cómo produce triples: 4.5 triples intentados (su ritmo 4.5 por 36'; el rival concede -3% de triples en su reparto) × 29% esperado.
- ❌ Defensa: el rival concede +6% de triples por minuto a aleros/ala-pívots (defensa débil); ajuste aplicado +3%; en su zona principal (esquina3) el rival concede 37% (liga 38%).
- ❌ Ritmo del partido: +2% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Últimos 10: la habría pasado 9 de 10.
- ❌ Bajas del rival: sin Caleb Wilson (titular); +1.7% en esta estadística.
- ⚠️ Justin Champagnie ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ Jamir Watkins ya no jugó en sus últimos partidos: la baja ya está en sus minutos.

- Triples **1.2** (por componentes 1.3 · por tasa por minuto y defensa rival 1.1): 4.5 triples intentados (su ritmo 4.5 por 36'; el rival concede -3% de triples en su reparto) × 29% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 35.6 | 34.7 | 33.7 | - | - |
| Triples anotados | 0.8 | 0.8 | 0.8 | - | - |
| Triples intentados | 5.0 | 4.0 | 3.9 | - | - |
| % triples | 16.0% | 20.0% | 21.3% | - | - |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +21%, vs defensa media +2%, vs defensa débil -39%; rebotes: vs defensa fuerte -7%, vs defensa media +19%, vs defensa débil -8%; asistencias: vs defensa fuerte -14%, vs defensa media +21%; triples: vs defensa fuerte -6%, vs defensa media -5%, vs defensa débil +32%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 32% | 66% | 68% | 66% |
| pintura | 27% | 38% | 45% | 44% |
| triple de esquina | 14% | 29% | 38% | 37% |
| media distancia | 14% | 41% | 41% | 42% |
| triple frontal | 13% | 29% | 35% | 36% |

#### Bilal Coulibaly (bases/escoltas) vs Chicago Bulls

- Minutos esperados: **23.2** (± 4.5); 71 partidos en la base.
- Justin Champagnie ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Jamir Watkins ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Su prop más probable hoy: **Bilal Coulibaly: más de 0.5 robos** (64%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Chicago Bulls contra bases/escoltas en robos: +15% respecto a la media; ajuste por su historial contra defensas similares: +5%.

**¿Por qué 1.1 robos?** (línea 0.5; 23.2 minutos esperados)

En corto:

- La pasó en 9 de 15 esta temporada (falló con 0, 0, 0, 0)
- Con 19+ minutos (hoy se esperan 23): 9 de 14 en sus últimos 15
- Contra las ~10 mejores defensas en robos a bases/escoltas: 11 de 15 (últimos 40 partidos)
- Contra defensas débiles como la de hoy y con 19+ minutos: 9 de 14, con 1.4 de media (últimos 60 partidos)
- El rival es #3 de 30 en robos que concede a bases/escoltas por minuto (#1 = el que más concede; +15% frente a la media)
- Oportunidades de robo (últimos 10): el rival perdió 6.4 balones por partido con él en pista y robó el 9%
- El rival es #6 de 30 en balones que pierde (#1 = el que más; 15.1 por partido)
- El rival no tiene a Caleb Wilson (1.8 robos por partido)
- Minutos: 23 esperados (suplente, ±5)

Razonamiento (3 factores a favor, 2 en contra):

- ❌ Minutos: 23.2 esperados (suplente, ±4.5).
- ✅ Forma: 0.6 en sus últimos 5, 1.0 esta temporada (15 partidos), 1.3 la temporada pasada (línea 0.5).
- ➖ Cómo produce robos: roba el 15.0% de las pérdidas del rival en pista × 14.1 pérdidas esperadas del rival.
- ✅ Defensa: el rival concede +15% de robos por minuto a bases/escoltas (defensa débil); ajuste aplicado +15%.
- ✅ Ritmo del partido: +2% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ❌ Contra este rival: 2, 0, 0 (1 de 3 a favor).
- ➖ Últimos 10: la habría pasado 5 de 10.
- ⚠️ Justin Champagnie ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ Jamir Watkins ya no jugó en sus últimos partidos: la baja ya está en sus minutos.

- ⚠️ Alertas: suplente.
- Robos **1.1** (por componentes 1.0 · por tasa por minuto y defensa rival 1.1): roba el 15.0% de las pérdidas del rival en pista × 14.1 pérdidas esperadas del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 23.4 | 23.9 | 25.0 | 26.2 | 24.7 |
| Robos | 0.6 | 0.6 | 1.0 | 1.3 | 0.7 |
| % de las pérdidas del rival que roba | 11.1% | 9.4% | 15.5% | 18.3% | 12.5% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -7%, vs defensa media +5%, vs defensa débil +2%; rebotes: vs defensa fuerte +0%, vs defensa media +10%, vs defensa débil -11%; asistencias: vs defensa fuerte +1%, vs defensa media -12%, vs defensa débil +10%; triples: vs defensa fuerte -20%, vs defensa media +40%, vs defensa débil -14%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 35% | 69% | 68% | 66% |
| triple frontal | 21% | 29% | 35% | 36% |
| pintura | 20% | 33% | 45% | 44% |
| triple de esquina | 18% | 32% | 38% | 37% |
| media distancia | 6% | 38% | 41% | 42% |

#### Trae Young (bases/escoltas) vs Chicago Bulls

- Minutos esperados: **33.6** (± 5.3); 31 partidos en la base.
- Justin Champagnie ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Jamir Watkins ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Su prop más probable hoy: **Trae Young: menos de 2.5 triples** (63%). Con 80% de probabilidad: más de 0.5 / menos de 3.5.
- Defensa de Chicago Bulls contra bases/escoltas en triples: +2% respecto a la media; ajuste por su historial contra defensas similares: +1%.

**¿Por qué 2.1 triples?** (línea 2.5; 33.6 minutos esperados)

En corto:

- La pasó en 10 de 16 esta temporada (falló con 4, 3, 3, 3)
- Con 30+ minutos (hoy se esperan 34): 7 de 13 en sus últimos 15
- Contra las ~10 mejores defensas en triples a bases/escoltas: 7 de 11 (últimos 40 partidos)
- Contra defensas medias como la de hoy y con 30+ minutos: 5 de 7, con 1.7 de media (últimos 60 partidos)
- El rival es #11 de 30 en triples que concede a bases/escoltas por minuto (#1 = el que más concede; +2% frente a la media)
- Su zona principal es triple frontal (44% de sus tiros, 32% de acierto); el rival es #4 de 30 en acierto que deja ahí (36%, liga 35%)
- Cómo tira (últimos 15): creado 46% (31% de acierto), penetración 40% (48% de acierto), recibe y tira 14% (30% de acierto); en creado el rival es #11 de 30 en lo que deja (#1 = el que más; 0.96 puntos por tiro frente a 0.94 de media)
- Oportunidades: 6.3 triples intentados esperados al 33%
- El rival no tiene a Caleb Wilson (2.3 triples por partido)
- Minutos: 34 esperados (titular, ±5)

Razonamiento (3 factores a favor, 3 en contra):

- ✅ Minutos: 33.6 esperados (titular, ±5.3).
- ✅ Forma: 2.0 en sus últimos 5, 1.9 esta temporada (16 partidos), 1.8 la temporada pasada (línea 2.5).
- ➖ Cómo produce triples: 6.3 triples intentados (su ritmo 6.6 por 36'; el rival concede -3% de triples en su reparto) × 33% esperado.
- ❌ Defensa: el rival concede +2% de triples por minuto a bases/escoltas (defensa media); ajuste aplicado +2%; en su zona principal (triple) el rival concede 36% (liga 35%).
- ✅ Altura: mide 6'2", 2.4 pulgadas menos que los bases/escoltas del rival (-0.9% en esta estadística).
- ❌ Ritmo del partido: +2% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ➖ Contra este rival: 4, 1, 7, 1 (2 de 4 a favor).
- ➖ Últimos 10: la habría pasado 6 de 10.
- ❌ Bajas del rival: sin Caleb Wilson (titular); +1.7% en esta estadística.
- ⚠️ Justin Champagnie ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ Jamir Watkins ya no jugó en sus últimos partidos: la baja ya está en sus minutos.

- ⚠️ Alertas: falla en partidos normales (6 de 16 esta temporada).
- Triples **2.1** (por componentes 2.1 · por tasa por minuto y defensa rival 2.0): 6.3 triples intentados (su ritmo 6.6 por 36'; el rival concede -3% de triples en su reparto) × 33% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 34.0 | 34.1 | 35.0 | 25.5 | 31.2 |
| Triples anotados | 2.0 | 2.0 | 1.9 | 1.8 | 3.2 |
| Triples intentados | 5.8 | 6.0 | 6.4 | 5.3 | 9.0 |
| % triples | 34.5% | 33.3% | 30.4% | 33.8% | 36.1% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -19%, vs defensa media +0%, vs defensa débil +21%; rebotes: vs defensa fuerte -4%, vs defensa media +20%, vs defensa débil -19%; asistencias: vs defensa fuerte -10%, vs defensa media -8%, vs defensa débil +26%; triples: vs defensa fuerte -4%, vs defensa media +6%, vs defensa débil -2%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 44% | 32% | 35% | 36% |
| pintura | 24% | 44% | 45% | 44% |
| media distancia | 14% | 41% | 41% | 42% |
| bajo el aro | 13% | 64% | 68% | 66% |
| triple de esquina | 5% | 38% | 38% | 37% |

#### Isaac Okoro (aleros/ala-pívots) vs Washington Wizards

- Minutos esperados: **27.5** (± 6.9); 77 partidos en la base.
- sin Caleb Wilson, la estrella de su equipo (4 partidos suyos sin él): más tiros y balón para él por minuto (puntos +5%, triples +6%, asistencias +5%)
- Caleb Wilson ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Su prop más probable hoy: **Isaac Okoro: menos de 1.5 triples** (62%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Washington Wizards contra aleros/ala-pívots en triples: +4% respecto a la media; ajuste por su historial contra defensas similares: -3%.

**¿Por qué 1.3 triples?** (línea 1.5; 27.5 minutos esperados)

En corto:

- La pasó en 11 de 14 esta temporada (falló con 4, 3, 2)
- Con 24+ minutos (hoy se esperan 28): 3 de 6 en sus últimos 15
- Contra las ~10 mejores defensas en triples a aleros/ala-pívots: 10 de 14 (últimos 40 partidos)
- Contra defensas débiles como la de hoy y con 24+ minutos: 9 de 13, con 1.2 de media (últimos 60 partidos)
- El rival es #5 de 30 en triples que concede a aleros/ala-pívots por minuto (#1 = el que más concede; +6% frente a la media)
- Su zona principal es triple de esquina (29% de sus tiros, 34% de acierto); el rival es #4 de 30 en acierto que deja ahí (39%, liga 38%)
- Su segunda zona es triple frontal (20% de sus tiros, 32% de acierto); el rival es #19 de 30 en acierto que deja ahí (35%, liga 35%)
- Cómo tira (últimos 15): recibe y tira 49% (29% de acierto), penetración 31% (58% de acierto), corte 7% (67% de acierto); en recibe y tira el rival es #23 de 30 en lo que deja (#1 = el que más; 1.04 puntos por tiro frente a 1.07 de media)
- Oportunidades: 4.0 triples intentados esperados al 34%
- Su equipo no tiene a Caleb Wilson: más tiros y balón para él
- Minutos: 28 esperados (titular, ±7)

Razonamiento (3 factores a favor, 4 en contra):

- ❌ Minutos: 27.5 esperados (titular, ±6.9).
- ❌ Forma: 1.8 en sus últimos 5, 0.9 esta temporada (14 partidos), 1.2 la temporada pasada (línea 1.5).
- ➖ Cómo produce triples: 4.0 triples intentados (su ritmo 4.9 por 36'; el rival concede -4% de triples en su reparto) × 34% esperado.
- ❌ Defensa: el rival concede +6% de triples por minuto a aleros/ala-pívots (defensa débil); ajuste aplicado +4%; en su zona principal (esquina3) el rival concede 39% (liga 38%).
- ✅ Altura: mide 6'4", 4.8 pulgadas menos que los aleros/ala-pívots del rival (-1.7% en esta estadística).
- ❌ Ritmo del partido: +2% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 0, 1 (2 de 2 a favor).
- ✅ Últimos 10: la habría pasado 7 de 10.
- ⚠️ sin Caleb Wilson, la estrella de su equipo (4 partidos suyos sin él): más tiros y balón para él por minuto (puntos +5%, triples +6%, asistencias +5%).
- ⚠️ Caleb Wilson ya no jugó en sus últimos partidos: la baja ya está en sus minutos.

- ⚠️ Alertas: minutos inestables, sin Caleb Wilson: más tiros para él.
- Triples **1.3** (por componentes 1.3 · por tasa por minuto y defensa rival 1.3): 4.0 triples intentados (su ritmo 4.9 por 36'; el rival concede -4% de triples en su reparto) × 34% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 30.4 | 24.9 | 22.9 | 26.9 | 15.0 |
| Triples anotados | 1.8 | 1.1 | 0.9 | 1.2 | 0.5 |
| Triples intentados | 4.6 | 3.5 | 3.0 | 3.5 | 1.5 |
| % triples | 39.1% | 31.4% | 28.6% | 33.0% | 33.3% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -8%, vs defensa media +1%, vs defensa débil +8%; rebotes: vs defensa fuerte -8%, vs defensa media +23%, vs defensa débil -8%; asistencias: vs defensa fuerte -2%, vs defensa media -12%, vs defensa débil +14%; triples: vs defensa fuerte -19%, vs defensa media +33%, vs defensa débil -11%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 42% | 63% | 68% | 69% |
| triple de esquina | 29% | 34% | 38% | 39% |
| triple frontal | 20% | 32% | 35% | 35% |
| pintura | 8% | 38% | 45% | 43% |
| media distancia | 0% | 40% | 41% | 43% |

## New Orleans Pelicans @ Oklahoma City Thunder

Diferencia esperada: Oklahoma City Thunder por 11.5 — algo desigual: titulares hasta -1.5% de minutos.

Parte de lesiones: Alex Caruso (Day-To-Day); Dejounte Murray (Out); Trey Murphy III (Out); Trendon Watford (Out); Chet Holmgren (Out); Bryce McGowens (Out); Jalen Williams (Out); Bennedict Mathurin (Out); Cason Wallace (Out); Thomas Sorber (Out).

Ventajas del partido (los dos lados): puntos esperados frente a su media de los últimos 10, ajuste por la defensa rival y diferencia de estatura con los rivales de su posición.

| Equipo | Jugador | Puntos esperados | Su media (últ. 10) | Defensa rival en puntos | Rebotes esperados | Altura vs rival |
|---|---|---|---|---|---|---|
| NO | Saddiq Bey | 17.7 | 17.3 | -4% | 5.8 | -0.1" |
| OKC | Shai Gilgeous-Alexander | 31.0 | 33.7 | +4% | 3.8 | +2.0" |
| NO | Jeremiah Fears | 14.9 | 17.1 | -5% | 4.9 | -2.1" |
| NO | Zion Williamson | 18.1 | 21.6 | -6% | 5.6 | -2.1" |
| OKC | Jared McCain | 16.0 | 15.0 | +3% | 3.5 | -1.0" |
| OKC | Ajay Mitchell | 17.9 | 19.6 | +4% | 3.7 | -0.0" |
| NO | Herbert Jones | 8.0 | 6.2 | -4% | 3.3 | -1.1" |
| OKC | Aday Mara | 11.8 | 11.0 | +6% | 8.1 | +5.3" |
| OKC | Isaiah Hartenstein | 10.3 | 7.9 | +6% | 11.4 | +2.3" |
| NO | Jordan Poole | 12.4 | 10.5 | -4% | 2.2 | -1.1" |

Las 8 más probables (máximo 2 por jugador: las de un mismo jugador suelen ganar o perder juntas).

| Prop | Prob. final | Modelo | Casa | Esperado | Últ. 10 | Temporada | vs este rival | Cuota (implícita) |
|---|---|---|---|---|---|---|---|---|
| **Ajay Mitchell: menos de 1.5 triples** | **68%** | 71% | 65% | 1.1 ± 1.2 | 8/10 | 11/13 | 0, 0 | 1.44 (70%) |
| **Jaylin Williams: menos de 1.5 triples** ⚠️ suplente | **67%** | 68% | 65% | 1.2 ± 1.1 | 9/10 | 7/8 | 0, 0, 4 | 1.43 (70%) |
| **Zion Williamson: más de 0.5 robos** | **66%** | 65% | 66% | 1.2 ± 1.3 | 5/10 | 10/15 | 0, 1 | 1.44 (69%) |
| **Shai Gilgeous-Alexander: más de 0.5 robos** | **64%** | 63% | 65% | 1.0 ± 1.0 | 6/10 | 9/15 | 0, 3, 1 | 1.46 (69%) |
| **Herbert Jones: menos de 1.5 triples** | **62%** | 64% | 61% | 1.3 ± 1.2 | 5/10 | 11/16 | 1, 1, 3 | 1.54 (65%) |
| **Jared McCain: más de 0.5 robos** | **62%** | 62% | 63% | 1.0 ± 1.0 | 7/10 | 10/15 | 0 | 1.50 (67%) |
| **Shai Gilgeous-Alexander: más de 1.5 triples** | **62%** | 63% | 61% | 2.3 ± 1.5 | 7/10 | 9/15 | 0, 3, 1 | 1.54 (65%) |
| **Jared McCain: menos de 2.5 asistencias** | **62%** | 62% | 61% | 2.2 ± 1.5 | 8/10 | 11/15 | 1 | 1.51 (66%) |

### Fichas de los jugadores destacados

#### Ajay Mitchell (bases/escoltas) vs New Orleans Pelicans

- Minutos esperados: **28.5** (± 4.0); 81 partidos en la base.
- Chet Holmgren ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Jalen Williams ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Cason Wallace ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- partido desigual (favorito por 11.5): los titulares suelen jugar -3% de minutos si se rompe
- Su prop más probable hoy: **Ajay Mitchell: menos de 1.5 triples** (68%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de New Orleans Pelicans contra bases/escoltas en triples: +3% respecto a la media; ajuste por su historial contra defensas similares: +4%.

**¿Por qué 1.1 triples?** (línea 1.5; 28.5 minutos esperados)

En corto:

- La pasó en 11 de 13 esta temporada; los fallos, en partidos raros (paliza de 31, paliza de 24)
- Con 24+ minutos (hoy se esperan 28): 9 de 11 en sus últimos 15
- Contra las ~10 mejores defensas en triples a bases/escoltas: 10 de 12 (últimos 40 partidos)
- Contra defensas débiles como la de hoy y con 24+ minutos: 9 de 13, con 1.2 de media (últimos 60 partidos)
- El rival es #4 de 30 en triples que concede a bases/escoltas por minuto (#1 = el que más concede; +9% frente a la media)
- Su zona principal es triple frontal (20% de sus tiros, 31% de acierto); el rival es #26 de 30 en acierto que deja ahí (34%, liga 35%)
- Cómo tira (últimos 15): penetración 53% (56% de acierto), creado 22% (51% de acierto), recibe y tira 18% (26% de acierto); en penetración el rival es #2 de 30 en lo que deja (#1 = el que más; 1.19 puntos por tiro frente a 1.08 de media)
- Oportunidades: 3.8 triples intentados esperados al 32%
- El rival no tiene a Dejounte Murray (0.8 triples por partido)
- Minutos: 28 esperados (titular, ±4)

Razonamiento (4 factores a favor, 2 en contra):

- ✅ Minutos: 28.5 esperados (titular, ±4.0).
- ✅ Forma: 1.0 en sus últimos 5, 0.8 esta temporada (13 partidos), 1.1 la temporada pasada (línea 1.5).
- ➖ Cómo produce triples: 3.8 triples intentados (su ritmo 4.5 por 36'; el rival concede +5% de triples en su reparto) × 32% esperado.
- ❌ Defensa: el rival concede +9% de triples por minuto a bases/escoltas (defensa débil); ajuste aplicado +3%; en su zona principal (triple) el rival concede 34% (liga 35%).
- ➖ Ritmo del partido: +1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 0, 0 (2 de 2 a favor).
- ✅ Últimos 10: la habría pasado 8 de 10.
- ❌ Bajas del rival: sin Dejounte Murray (titular); +1.7% en esta estadística.
- ⚠️ Chet Holmgren ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ Jalen Williams ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ Cason Wallace ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ partido desigual (favorito por 11.5): los titulares suelen jugar -3% de minutos si se rompe.

- Triples **1.1** (por componentes 1.2 · por tasa por minuto y defensa rival 1.1): 3.8 triples intentados (su ritmo 4.5 por 36'; el rival concede +5% de triples en su reparto) × 32% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 28.2 | 28.7 | 27.8 | 26.3 | 28.0 |
| Triples anotados | 1.0 | 0.9 | 0.8 | 1.1 | 0.0 |
| Triples intentados | 3.2 | 3.3 | 3.1 | 3.2 | 3.5 |
| % triples | 31.2% | 27.3% | 25.0% | 34.3% | 0.0% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -19%, vs defensa media +8%, vs defensa débil +6%; rebotes: vs defensa fuerte +2%, vs defensa media +3%, vs defensa débil -6%; asistencias: vs defensa fuerte -2%, vs defensa media -1%, vs defensa débil +3%; triples: vs defensa fuerte -30%, vs defensa media +30%, vs defensa débil +3%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| pintura | 35% | 52% | 45% | 48% |
| bajo el aro | 28% | 65% | 68% | 69% |
| triple frontal | 20% | 31% | 35% | 34% |
| media distancia | 9% | 39% | 41% | 40% |
| triple de esquina | 7% | 38% | 38% | 38% |

#### Jaylin Williams (aleros/ala-pívots) vs New Orleans Pelicans

- Minutos esperados: **19.6** (± 5.6); 88 partidos en la base.
- Chet Holmgren ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Jalen Williams ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Cason Wallace ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- cambio de rol esta temporada (por minuto): pts -56%, ast -30%, tpm -46%; se da más peso a la línea de la casa
- partido desigual (favorito por 11.5): los suplentes suelen jugar +3% de minutos si se rompe
- Su prop más probable hoy: **Jaylin Williams: menos de 1.5 triples** (67%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de New Orleans Pelicans contra aleros/ala-pívots en triples: -1% respecto a la media; ajuste por su historial contra defensas similares: -1%.

**¿Por qué 1.2 triples?** (línea 1.5; 19.6 minutos esperados)

En corto:

- La pasó en 7 de 8 esta temporada (falló con 2)
- Con 16+ minutos (hoy se esperan 20): 9 de 11 en sus últimos 15
- Contra las ~10 mejores defensas en triples a aleros/ala-pívots: 14 de 20 (últimos 40 partidos)
- Contra defensas medias como la de hoy y con 16+ minutos: 7 de 11, con 1.5 de media (últimos 60 partidos)
- El rival es #18 de 30 en triples que concede a aleros/ala-pívots por minuto (#1 = el que más concede; -1% frente a la media)
- Su zona principal es triple frontal (54% de sus tiros, 37% de acierto); el rival es #26 de 30 en acierto que deja ahí (34%, liga 35%)
- Cómo tira (últimos 15): recibe y tira 79% (30% de acierto), penetración 11% (38% de acierto), creado 6% (25% de acierto); en recibe y tira el rival es #18 de 30 en lo que deja (#1 = el que más; 1.06 puntos por tiro frente a 1.07 de media)
- Oportunidades: 3.7 triples intentados esperados al 35%
- El rival no tiene a Dejounte Murray (0.8 triples por partido)
- Minutos: 20 esperados (suplente, ±6)

Razonamiento (3 factores a favor, 2 en contra):

- ❌ Minutos: 19.6 esperados (suplente, ±5.6).
- ✅ Forma: 0.8 en sus últimos 5, 0.8 esta temporada (8 partidos), 1.5 la temporada pasada (línea 1.5).
- ➖ Cómo produce triples: 3.7 triples intentados (su ritmo 6.4 por 36'; el rival concede +5% de triples en su reparto) × 35% esperado.
- ➖ Defensa: el rival concede -1% de triples por minuto a aleros/ala-pívots (defensa media); ajuste aplicado -1%; en su zona principal (triple) el rival concede 34% (liga 35%).
- ➖ Ritmo del partido: +1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 0, 0, 4 (2 de 3 a favor).
- ✅ Últimos 10: la habría pasado 9 de 10.
- ❌ Bajas del rival: sin Dejounte Murray (titular); +1.7% en esta estadística.
- ⚠️ Chet Holmgren ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ Jalen Williams ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ Cason Wallace ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ cambio de rol esta temporada (por minuto): pts -56%, ast -30%, tpm -46%; se da más peso a la línea de la casa.
- ⚠️ partido desigual (favorito por 11.5): los suplentes suelen jugar +3% de minutos si se rompe.

- ⚠️ Alertas: suplente, cambio de rol.
- Triples **1.2** (por componentes 1.3 · por tasa por minuto y defensa rival 1.0): 3.7 triples intentados (su ritmo 6.4 por 36'; el rival concede +5% de triples en su reparto) × 35% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 21.6 | 19.7 | 18.1 | 19.0 | 22.7 |
| Triples anotados | 0.8 | 0.7 | 0.8 | 1.4 | 1.3 |
| Triples intentados | 3.2 | 3.3 | 3.2 | 3.8 | 4.3 |
| % triples | 25.0% | 21.2% | 23.1% | 37.9% | 30.8% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -5%, vs defensa media -5%, vs defensa débil +13%; rebotes: vs defensa fuerte -9%, vs defensa media +12%, vs defensa débil +2%; asistencias: vs defensa fuerte -16%, vs defensa media -3%, vs defensa débil +23%; triples: vs defensa fuerte -14%, vs defensa media -7%, vs defensa débil +46%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 54% | 37% | 35% | 34% |
| triple de esquina | 19% | 34% | 38% | 38% |
| bajo el aro | 12% | 60% | 68% | 69% |
| pintura | 9% | 45% | 45% | 48% |
| media distancia | 5% | 42% | 41% | 40% |

#### Zion Williamson (aleros/ala-pívots) vs Oklahoma City Thunder

- Minutos esperados: **30.3** (± 3.4); 77 partidos en la base.
- Dejounte Murray ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Trey Murphy III ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- partido desigual (no favorito por 11.5): los titulares suelen jugar -3% de minutos si se rompe
- Su prop más probable hoy: **Zion Williamson: más de 0.5 robos** (66%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Oklahoma City Thunder contra aleros/ala-pívots en robos: -8% respecto a la media; ajuste por su historial contra defensas similares: -2%.

**¿Por qué 1.2 robos?** (línea 0.5; 30.3 minutos esperados)

En corto:

- La pasó en 10 de 15 esta temporada (falló con 0, 0, 0, 0)
- Con 26+ minutos (hoy se esperan 30): 9 de 14 en sus últimos 15
- Contra las ~10 mejores defensas en robos a aleros/ala-pívots: 7 de 12 (últimos 40 partidos)
- Contra defensas fuertes como la de hoy y con 26+ minutos: 10 de 19, con 1.1 de media (últimos 60 partidos)
- El rival es #27 de 30 en robos que concede a aleros/ala-pívots por minuto (#1 = el que más concede; -8% frente a la media)
- Oportunidades de robo (últimos 10): el rival perdió 9.7 balones por partido con él en pista y robó el 12%
- El rival es #30 de 30 en balones que pierde (#1 = el que más; 11.9 por partido)
- Minutos: 30 esperados (titular, ±3)

Razonamiento (2 factores a favor, 1 en contra):

- ✅ Minutos: 30.3 esperados (titular, ±3.4).
- ✅ Forma: 1.0 en sus últimos 5, 1.9 esta temporada (15 partidos), 0.9 la temporada pasada (línea 0.5).
- ➖ Cómo produce robos: roba el 15.1% de las pérdidas del rival en pista × 11.9 pérdidas esperadas del rival.
- ❌ Defensa: el rival concede -8% de robos por minuto a aleros/ala-pívots (defensa fuerte); ajuste aplicado -8%.
- ➖ Ritmo del partido: +1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ➖ Contra este rival: 0, 1 (1 de 2 a favor).
- ➖ Últimos 10: la habría pasado 5 de 10.
- ⚠️ Dejounte Murray ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ Trey Murphy III ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ partido desigual (no favorito por 11.5): los titulares suelen jugar -3% de minutos si se rompe.

- Robos **1.2** (por componentes 1.1 · por tasa por minuto y defensa rival 1.3): roba el 15.1% de las pérdidas del rival en pista × 11.9 pérdidas esperadas del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 30.2 | 32.1 | 32.1 | 29.7 | 31.0 |
| Robos | 1.0 | 1.2 | 1.9 | 1.0 | 0.5 |
| % de las pérdidas del rival que roba | 11.4% | 12.4% | 18.4% | 11.4% | 5.3% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -1%, vs defensa media +1%, vs defensa débil +0%; rebotes: vs defensa fuerte +5%, vs defensa media -5%, vs defensa débil -0%; asistencias: vs defensa fuerte -4%, vs defensa media +8%, vs defensa débil -5%; triples: vs defensa fuerte +14%, vs defensa media -58%, vs defensa débil +51%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 65% | 68% | 68% | 62% |
| pintura | 30% | 44% | 45% | 41% |
| triple frontal | 2% | 39% | 35% | 35% |
| media distancia | 2% | 49% | 41% | 40% |
| triple de esquina | 1% | 37% | 38% | 39% |

#### Shai Gilgeous-Alexander (bases/escoltas) vs New Orleans Pelicans

- Minutos esperados: **32.9** (± 3.8); 98 partidos en la base.
- Chet Holmgren ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Jalen Williams ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Cason Wallace ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- partido desigual (favorito por 11.5): los titulares suelen jugar -3% de minutos si se rompe
- Su prop más probable hoy: **Shai Gilgeous-Alexander: más de 0.5 robos** (64%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de New Orleans Pelicans contra bases/escoltas en robos: -6% respecto a la media; ajuste por su historial contra defensas similares: -0%.

**¿Por qué 1.0 robos?** (línea 0.5; 32.9 minutos esperados)

En corto:

- La pasó en 9 de 15 esta temporada (falló con 0, 0, 0, 0)
- Con 29+ minutos (hoy se esperan 33): 8 de 14 en sus últimos 15
- Contra las ~10 mejores defensas en robos a bases/escoltas: 12 de 19 (últimos 40 partidos)
- Contra defensas fuertes como la de hoy y con 29+ minutos: 20 de 28, con 1.2 de media (últimos 60 partidos)
- El rival es #21 de 30 en robos que concede a bases/escoltas por minuto (#1 = el que más concede; -6% frente a la media)
- Oportunidades de robo (últimos 10): el rival perdió 9.3 balones por partido con él en pista y robó el 9%
- El rival es #18 de 30 en balones que pierde (#1 = el que más; 13.8 por partido)
- El rival no tiene a Dejounte Murray (1.6 robos por partido)
- Minutos: 33 esperados (titular, ±4)

Razonamiento (3 factores a favor, 1 en contra):

- ✅ Minutos: 32.9 esperados (titular, ±3.8).
- ✅ Forma: 0.8 en sus últimos 5, 0.9 esta temporada (15 partidos), 1.4 la temporada pasada (línea 0.5).
- ➖ Cómo produce robos: roba el 10.7% de las pérdidas del rival en pista × 15.2 pérdidas esperadas del rival.
- ❌ Defensa: el rival concede -6% de robos por minuto a bases/escoltas (defensa fuerte); ajuste aplicado -6%.
- ➖ Ritmo del partido: +1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 0, 3, 1 (2 de 3 a favor).
- ➖ Últimos 10: la habría pasado 6 de 10.
- ⚠️ Chet Holmgren ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ Jalen Williams ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ Cason Wallace ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ partido desigual (favorito por 11.5): los titulares suelen jugar -3% de minutos si se rompe.

- Robos **1.0** (por componentes 1.1 · por tasa por minuto y defensa rival 1.0): roba el 10.7% de las pérdidas del rival en pista × 15.2 pérdidas esperadas del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 34.0 | 33.4 | 33.3 | 33.8 | 31.7 |
| Robos | 0.8 | 0.8 | 0.9 | 1.4 | 1.3 |
| % de las pérdidas del rival que roba | 7.7% | 8.6% | 9.9% | 12.0% | 11.8% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -10%, vs defensa media +1%, vs defensa débil +11%; rebotes: vs defensa fuerte -4%, vs defensa media +5%, vs defensa débil +0%; asistencias: vs defensa fuerte -5%, vs defensa media +5%, vs defensa débil +2%; triples: vs defensa fuerte -16%, vs defensa media -4%, vs defensa débil +34%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| media distancia | 28% | 50% | 41% | 40% |
| pintura | 25% | 51% | 45% | 48% |
| triple frontal | 23% | 37% | 35% | 34% |
| bajo el aro | 22% | 70% | 68% | 69% |
| triple de esquina | 1% | 35% | 38% | 38% |

#### Herbert Jones (aleros/ala-pívots) vs Oklahoma City Thunder

- Minutos esperados: **27.1** (± 5.1); 72 partidos en la base.
- Dejounte Murray ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Trey Murphy III ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Su prop más probable hoy: **Herbert Jones: menos de 1.5 triples** (62%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Oklahoma City Thunder contra aleros/ala-pívots en triples: +4% respecto a la media; ajuste por su historial contra defensas similares: -3%.

**¿Por qué 1.3 triples?** (línea 1.5; 27.1 minutos esperados)

En corto:

- La pasó en 11 de 16 esta temporada (falló con 3, 2, 2, 2)
- Con 23+ minutos (hoy se esperan 27): 5 de 10 en sus últimos 15
- Contra las ~10 mejores defensas en triples a aleros/ala-pívots: 9 de 16 (últimos 40 partidos)
- Contra defensas débiles como la de hoy y con 23+ minutos: 7 de 11, con 1.5 de media (últimos 60 partidos)
- El rival es #3 de 30 en triples que concede a aleros/ala-pívots por minuto (#1 = el que más concede; +8% frente a la media)
- Su zona principal es triple frontal (34% de sus tiros, 32% de acierto); el rival es #14 de 30 en acierto que deja ahí (35%, liga 35%)
- Cómo tira (últimos 15): recibe y tira 42% (31% de acierto), penetración 33% (36% de acierto), creado 18% (37% de acierto); en recibe y tira el rival es #24 de 30 en lo que deja (#1 = el que más; 1.04 puntos por tiro frente a 1.07 de media)
- Oportunidades: 4.2 triples intentados esperados al 32%
- Minutos: 27 esperados (titular, ±5)

Razonamiento (3 factores a favor, 1 en contra):

- ✅ Minutos: 27.1 esperados (titular, ±5.1).
- ✅ Forma: 1.4 en sus últimos 5, 0.9 esta temporada (16 partidos), 1.4 la temporada pasada (línea 1.5).
- ➖ Cómo produce triples: 4.2 triples intentados (su ritmo 5.2 por 36'; el rival concede +8% de triples en su reparto) × 32% esperado.
- ❌ Defensa: el rival concede +8% de triples por minuto a aleros/ala-pívots (defensa débil); ajuste aplicado +4%; en su zona principal (triple) el rival concede 35% (liga 35%).
- ➖ Ritmo del partido: +1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 1, 1, 3 (2 de 3 a favor).
- ➖ Últimos 10: la habría pasado 5 de 10.
- ⚠️ Dejounte Murray ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ Trey Murphy III ya no jugó en sus últimos partidos: la baja ya está en sus minutos.

- Triples **1.3** (por componentes 1.3 · por tasa por minuto y defensa rival 1.2): 4.2 triples intentados (su ritmo 5.2 por 36'; el rival concede +8% de triples en su reparto) × 32% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 28.0 | 26.3 | 24.4 | 28.4 | 25.7 |
| Triples anotados | 1.4 | 1.2 | 0.9 | 1.4 | 1.7 |
| Triples intentados | 4.6 | 3.9 | 3.2 | 4.6 | 5.3 |
| % triples | 30.4% | 30.8% | 29.4% | 30.9% | 31.2% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +2%, vs defensa media -5%, vs defensa débil +1%; rebotes: vs defensa fuerte +8%, vs defensa media -5%, vs defensa débil -7%; asistencias: vs defensa fuerte -2%, vs defensa media +10%, vs defensa débil -9%; triples: vs defensa fuerte +6%, vs defensa media -12%, vs defensa débil +7%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 34% | 32% | 35% | 35% |
| bajo el aro | 27% | 57% | 68% | 62% |
| triple de esquina | 18% | 32% | 38% | 39% |
| pintura | 17% | 38% | 45% | 41% |
| media distancia | 5% | 38% | 41% | 40% |

## Phoenix Suns @ Utah Jazz

Diferencia esperada: Phoenix Suns por 4.5.

Parte de lesiones: Jusuf Nurkic (Out); Lauri Markkanen (Out); Jaren Jackson Jr. (Out); Mark Williams (Out).

Ventajas del partido (los dos lados): puntos esperados frente a su media de los últimos 10, ajuste por la defensa rival y diferencia de estatura con los rivales de su posición.

| Equipo | Jugador | Puntos esperados | Su media (últ. 10) | Defensa rival en puntos | Rebotes esperados | Altura vs rival |
|---|---|---|---|---|---|---|
| UTAH | Keyonte George | 24.9 | 20.2 | +0% | 3.7 | +0.3" |
| PHX | Devin Booker | 24.9 | 25.8 | +6% | 3.2 | -0.7" |
| UTAH | Darryn Peterson | 16.2 | 18.4 | +0% | 4.1 | +1.3" |
| UTAH | Ace Bailey | 15.9 | 13.2 | +0% | 5.4 | +5.3" |
| PHX | Dillon Brooks | 16.4 | 14.3 | +4% | 3.9 | -1.8" |
| PHX | Miles Bridges | 14.2 | 13.9 | +4% | 6.0 | -1.8" |
| PHX | Jalen Green | 14.9 | 12.9 | +6% | 3.7 | -1.7" |
| PHX | Oso Ighodaro | 7.8 | 6.3 | +5% | 5.6 | +2.2" |
| UTAH | Mo Bamba | 10.6 | 9.2 | +1% | 9.0 | -1.6" |
| UTAH | Jaxson Hayes | 9.3 | 8.1 | +1% | 6.1 | -1.6" |

Las 8 más probables (máximo 2 por jugador: las de un mismo jugador suelen ganar o perder juntas).

| Prop | Prob. final | Modelo | Casa | Esperado | Últ. 10 | Temporada | vs este rival | Cuota (implícita) |
|---|---|---|---|---|---|---|---|---|
| **Collin Gillespie: menos de 3.5 rebotes** ⚠️ suplente | **66%** | 71% | 59% | 2.8 ± 1.7 | 9/10 | 12/14 | 3, 3, 3 | 1.56 (64%) |
| **Keyonte George: menos de 7.5 asistencias** | **64%** | 70% | 56% | 5.7 ± 2.5 | 4/10 | 7/15 | 9, 10 | 1.68 (60%) |
| **Darryn Peterson: menos de 4.5 asistencias** | **64%** | 70% | 55% | 3.5 ± 2.0 | 6/10 | 12/16 | - | 1.69 (59%) |
| **Keyonte George: menos de 4.5 rebotes** | **63%** | 66% | 58% | 3.7 ± 2.4 | 6/10 | 10/15 | 8, 5 | 1.61 (62%) |
| **Darryn Peterson: menos de 27.5 pts+reb+ast** | **61%** | 68% | 51% | 23.9 ± 7.8 | 5/10 | 11/16 | - | 1.85 (54%) |
| **Devin Booker: más de 1.5 triples** | **60%** | 60% | 61% | 2.0 ± 1.4 | 8/10 | 10/14 | 1, 6, 5 | 1.54 (65%) |
| **Ace Bailey: menos de 2.5 asistencias** | **60%** | 61% | 59% | 2.2 ± 1.5 | 6/10 | 9/16 | 2, 3, 1 | 1.59 (63%) |
| **Jalen Green: menos de 3.5 asistencias** | **59%** | 60% | 59% | 3.2 ± 2.0 | 6/10 | 9/14 | 3 | 1.59 (63%) |

### Fichas de los jugadores destacados

#### Collin Gillespie (bases/escoltas) vs Utah Jazz

- Minutos esperados: **23.3** (± 4.0); 100 partidos en la base.
- Mark Williams ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Su prop más probable hoy: **Collin Gillespie: menos de 3.5 rebotes** (66%). Con 80% de probabilidad: más de 0.5 / menos de 4.5.
- Defensa de Utah Jazz contra bases/escoltas en rebotes: +4% respecto a la media; ajuste por su historial contra defensas similares: +0%.

**¿Por qué 2.8 rebotes?** (línea 3.5; 23.3 minutos esperados)

En corto:

- La pasó en 12 de 14 esta temporada (falló con 4, 4)
- Con 19+ minutos (hoy se esperan 23): 12 de 14 en sus últimos 15
- Contra las ~10 mejores defensas en rebotes a bases/escoltas: 11 de 17 (últimos 40 partidos)
- Contra defensas débiles como la de hoy y con 19+ minutos: 6 de 15, con 4.3 de media (últimos 60 partidos)
- El rival es #6 de 30 en rebotes que concede a bases/escoltas por minuto (#1 = el que más concede; +4% frente a la media)
- El rival es #8 de 30 en rebotes que concede en total (#1 = el que más)
- El rival es #16 de 30 en rebotes ofensivos que concede en total (#1 = el que más)
- Rebotes disponibles con él en pista (últimos 10): 22.7 tiros fallados del rival y 25.8 de su equipo por partido; se queda el 8% y el 2%; el rival falla 48.6 tiros por partido (#9 de 30, #1 = el que más falla)
- Minutos: 23 esperados (suplente, ±4)

Razonamiento (4 factores a favor, 2 en contra):

- ❌ Minutos: 23.3 esperados (suplente, ±4.0).
- ✅ Forma: 2.8 en sus últimos 5, 2.4 esta temporada (14 partidos), 4.2 la temporada pasada (línea 3.5).
- ➖ Cómo produce rebotes: defensivos 2.1 = captura el 9.2% de los fallos del rival en pista × 46.2 fallos esperados del rival (liga 46.9) × 48% del partido; ofensivos 0.7 = 3.0% de los fallos de su equipo × 47.4.
- ❌ Defensa: el rival concede +4% de rebotes por minuto a bases/escoltas (defensa débil); ajuste aplicado +4%.
- ✅ Altura: mide 6'1", 4.7 pulgadas menos que los bases/escoltas del rival (-1.7% en esta estadística).
- ➖ Ritmo del partido: -1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 3, 3, 3 (3 de 3 a favor).
- ✅ Últimos 10: la habría pasado 9 de 10.
- ⚠️ Mark Williams ya no jugó en sus últimos partidos: la baja ya está en sus minutos.

- ⚠️ Alertas: suplente.
- Rebotes **2.8** (por componentes 2.7 · por tasa por minuto y defensa rival 2.8): defensivos 2.1 = captura el 9.2% de los fallos del rival en pista × 46.2 fallos esperados del rival (liga 46.9) × 48% del partido; ofensivos 0.7 = 3.0% de los fallos de su equipo × 47.4.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 24.0 | 23.5 | 24.3 | 28.2 | 28.7 |
| Rebotes | 2.8 | 2.5 | 2.4 | 4.1 | 3.0 |
| % de los fallos del rival que captura | 10.7% | 8.4% | 7.8% | 11.4% | 9.5% |
| % de los fallos de su equipo que captura | 1.6% | 2.3% | 2.5% | 3.9% | 0.0% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +0%, vs defensa media +3%, vs defensa débil -4%; rebotes: vs defensa fuerte -9%, vs defensa media +3%, vs defensa débil +9%; asistencias: vs defensa fuerte -16%, vs defensa media -3%, vs defensa débil +23%; triples: vs defensa fuerte -8%, vs defensa media -4%, vs defensa débil +11%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 59% | 38% | 35% | 36% |
| pintura | 13% | 45% | 45% | 48% |
| media distancia | 11% | 42% | 41% | 42% |
| triple de esquina | 11% | 41% | 38% | 37% |
| bajo el aro | 7% | 61% | 68% | 71% |

#### Keyonte George (bases/escoltas) vs Phoenix Suns

- Minutos esperados: **35.1** (± 4.3); 69 partidos en la base.
- Jusuf Nurkic ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- sin Lauri Markkanen, la estrella de su equipo (20 partidos suyos sin él): más tiros y balón para él por minuto (puntos +10%, triples +9%, asistencias -12%)
- Lauri Markkanen ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Jaren Jackson Jr. ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Su prop más probable hoy: **Keyonte George: menos de 7.5 asistencias** (64%). Con 80% de probabilidad: más de 3.5 / menos de 8.5.
- Defensa de Phoenix Suns contra bases/escoltas en asistencias: -8% respecto a la media; ajuste por su historial contra defensas similares: -3%.

**¿Por qué 5.7 asistencias?** (línea 7.5; 35.1 minutos esperados)

En corto:

- La pasó en 7 de 15 esta temporada (falló con 10, 11, 8, 8)
- Con 31+ minutos (hoy se esperan 35): 4 de 11 en sus últimos 15
- Contra las ~10 mejores defensas en asistencias a bases/escoltas: 13 de 17 (últimos 40 partidos)
- Contra defensas fuertes como la de hoy y con 31+ minutos: 10 de 15, con 6.5 de media (últimos 60 partidos)
- El rival es #28 de 30 en asistencias que concede a bases/escoltas por minuto (#1 = el que más concede; -8% frente a la media)
- Asistencias esperadas: 7.7 por partido si sus compañeros metieran lo normal (tiene 7.3; con él en pista metieron el 95% de lo esperado por tipo de tiro, últimos 10); ajuste aplicado +3.2%
- Oportunidades: asiste el 29% de las canastas de sus compañeros con él en pista
- Su equipo no tiene a Lauri Markkanen: más tiros y balón para él
- Minutos: 35 esperados (titular, ±4)

Razonamiento (2 factores a favor, 3 en contra):

- ✅ Minutos: 35.1 esperados (titular, ±4.3).
- ❌ Forma: 8.6 en sus últimos 5, 7.1 esta temporada (15 partidos), 6.1 la temporada pasada (línea 7.5).
- ➖ Cómo produce asistencias: asiste el 29.0% de las canastas de sus compañeros en pista × 21.4 canastas de compañeros esperadas (su equipo 40.1 por 48' contra esta defensa).
- ✅ Defensa: el rival concede -8% de asistencias por minuto a bases/escoltas (defensa fuerte); ajuste aplicado -8%.
- ➖ Ritmo del partido: -1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ❌ Contra este rival: 9, 10 (0 de 2 a favor).
- ❌ Últimos 10: la habría pasado 4 de 10.
- ⚠️ Jusuf Nurkic ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ sin Lauri Markkanen, la estrella de su equipo (20 partidos suyos sin él): más tiros y balón para él por minuto (puntos +10%, triples +9%, asistencias -12%).
- ⚠️ Lauri Markkanen ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ Jaren Jackson Jr. ya no jugó en sus últimos partidos: la baja ya está en sus minutos.

- ⚠️ Alertas: sin Lauri Markkanen: más tiros para él, falla en partidos normales (7 de 15 esta temporada).
- Asistencias **5.7** (por componentes 5.5 · por tasa por minuto y defensa rival 5.6): asiste el 29.0% de las canastas de sus compañeros en pista × 21.4 canastas de compañeros esperadas (su equipo 40.1 por 48' contra esta defensa).

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 35.8 | 33.6 | 33.3 | 33.1 | 38.0 |
| Asistencias | 8.6 | 7.3 | 7.1 | 6.1 | 9.5 |
| % de las canastas de compañeros que asiste | 34.8% | 33.7% | 33.1% | 26.2% | 39.9% |
| Pérdidas por jugada | 14.4% | 14.9% | 15.9% | 13.7% | 16.1% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +2%, vs defensa media -6%, vs defensa débil +4%; rebotes: vs defensa fuerte -13%, vs defensa media +16%, vs defensa débil -3%; asistencias: vs defensa fuerte -8%, vs defensa media +3%, vs defensa débil +8%; triples: vs defensa fuerte -5%, vs defensa media +12%, vs defensa débil -8%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 36% | 37% | 35% | 35% |
| pintura | 30% | 47% | 45% | 46% |
| media distancia | 16% | 44% | 41% | 41% |
| bajo el aro | 13% | 69% | 68% | 69% |
| triple de esquina | 5% | 34% | 38% | 37% |

#### Darryn Peterson (bases/escoltas) vs Phoenix Suns

- Minutos esperados: **29.5** (± 5.8); 16 partidos en la base.
- Jusuf Nurkic ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- sin Lauri Markkanen, la estrella de su equipo (8 partidos suyos sin él): más tiros y balón para él por minuto (puntos +2%, triples -0%, asistencias +4%)
- Lauri Markkanen ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Jaren Jackson Jr. ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Su prop más probable hoy: **Darryn Peterson: menos de 4.5 asistencias** (64%). Con 80% de probabilidad: más de 1.5 / menos de 5.5.
- Defensa de Phoenix Suns contra bases/escoltas en asistencias: -8% respecto a la media; ajuste por su historial contra defensas similares: -0%.

**¿Por qué 3.5 asistencias?** (línea 4.5; 29.5 minutos esperados)

En corto:

- La pasó en 12 de 16 esta temporada (falló con 5, 5, 7, 6)
- Con 25+ minutos (hoy se esperan 29): 10 de 14 en sus últimos 15
- Contra las ~10 mejores defensas en asistencias a bases/escoltas: 5 de 7 (últimos 40 partidos)
- Contra defensas fuertes como la de hoy y con 25+ minutos: 5 de 7, con 4.0 de media (últimos 60 partidos)
- El rival es #28 de 30 en asistencias que concede a bases/escoltas por minuto (#1 = el que más concede; -8% frente a la media)
- Asistencias esperadas: 4.3 por partido si sus compañeros metieran lo normal (tiene 4.2; con él en pista metieron el 98% de lo esperado por tipo de tiro, últimos 10); ajuste aplicado +1.0%
- Oportunidades: asiste el 18% de las canastas de sus compañeros con él en pista
- Su equipo no tiene a Lauri Markkanen: más tiros y balón para él
- Minutos: 29 esperados (titular, ±6)

Razonamiento (3 factores a favor, 0 en contra):

- ✅ Minutos: 29.5 esperados (titular, ±5.8).
- ✅ Forma: 3.2 en sus últimos 5, 3.7 esta temporada (16 partidos) (línea 4.5).
- ➖ Cómo produce asistencias: asiste el 17.9% de las canastas de sus compañeros en pista × 19.2 canastas de compañeros esperadas (su equipo 40.1 por 48' contra esta defensa).
- ✅ Defensa: el rival concede -8% de asistencias por minuto a bases/escoltas (defensa fuerte); ajuste aplicado -8%.
- ➖ Ritmo del partido: -1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ➖ Últimos 10: la habría pasado 6 de 10.
- ⚠️ Jusuf Nurkic ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ sin Lauri Markkanen, la estrella de su equipo (8 partidos suyos sin él): más tiros y balón para él por minuto (puntos +2%, triples -0%, asistencias +4%).
- ⚠️ Lauri Markkanen ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ Jaren Jackson Jr. ya no jugó en sus últimos partidos: la baja ya está en sus minutos.

- ⚠️ Alertas: sin Lauri Markkanen: más tiros para él.
- Asistencias **3.5** (por componentes 3.6 · por tasa por minuto y defensa rival 3.5): asiste el 17.9% de las canastas de sus compañeros en pista × 19.2 canastas de compañeros esperadas (su equipo 40.1 por 48' contra esta defensa).

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 30.2 | 31.0 | 30.6 | - | - |
| Asistencias | 3.2 | 4.2 | 3.7 | - | - |
| % de las canastas de compañeros que asiste | 14.8% | 20.2% | 17.9% | - | - |
| Pérdidas por jugada | 10.5% | 12.3% | 10.7% | - | - |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +18%, vs defensa media -2%, vs defensa débil -14%; rebotes: vs defensa fuerte -12%, vs defensa media +23%, vs defensa débil +2%; asistencias: vs defensa fuerte +0%, vs defensa media -15%, vs defensa débil +7%; triples: vs defensa fuerte +23%, vs defensa media -16%, vs defensa débil -22%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 36% | 35% | 35% | 35% |
| pintura | 36% | 45% | 45% | 46% |
| media distancia | 12% | 33% | 41% | 41% |
| bajo el aro | 9% | 68% | 68% | 69% |
| triple de esquina | 7% | 39% | 38% | 37% |

#### Devin Booker (bases/escoltas) vs Utah Jazz

- Minutos esperados: **33.1** (± 3.4); 87 partidos en la base.
- Mark Williams ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Su prop más probable hoy: **Devin Booker: más de 1.5 triples** (60%). Con 80% de probabilidad: más de 0.5 / menos de 3.5.
- Defensa de Utah Jazz contra bases/escoltas en triples: +7% respecto a la media; ajuste por su historial contra defensas similares: -2%.

**¿Por qué 2.0 triples?** (línea 1.5; 33.1 minutos esperados)

En corto:

- La pasó en 10 de 14 esta temporada (falló con 1, 0, 0, 0)
- Con 29+ minutos (hoy se esperan 33): 8 de 11 en sus últimos 15
- Contra las ~10 mejores defensas en triples a bases/escoltas: 8 de 13 (últimos 40 partidos)
- Contra defensas débiles como la de hoy y con 29+ minutos: 9 de 15, con 2.0 de media (últimos 60 partidos)
- El rival es #2 de 30 en triples que concede a bases/escoltas por minuto (#1 = el que más concede; +11% frente a la media)
- Su zona principal es triple frontal (29% de sus tiros, 33% de acierto); el rival es #3 de 30 en acierto que deja ahí (36%, liga 35%)
- Cómo tira (últimos 15): creado 61% (49% de acierto), penetración 18% (64% de acierto), recibe y tira 14% (19% de acierto); en creado el rival es #10 de 30 en lo que deja (#1 = el que más; 0.97 puntos por tiro frente a 0.94 de media)
- Oportunidades: 6.0 triples intentados esperados al 35%
- Minutos: 33 esperados (titular, ±3)

Razonamiento (5 factores a favor, 0 en contra):

- ✅ Minutos: 33.1 esperados (titular, ±3.4).
- ✅ Forma: 1.8 en sus últimos 5, 1.9 esta temporada (14 partidos), 1.7 la temporada pasada (línea 1.5).
- ➖ Cómo produce triples: 6.0 triples intentados (su ritmo 6.1 por 36'; el rival concede +5% de triples en su reparto) × 35% esperado.
- ✅ Defensa: el rival concede +11% de triples por minuto a bases/escoltas (defensa débil); ajuste aplicado +7%; en su zona principal (triple) el rival concede 36% (liga 35%).
- ➖ Ritmo del partido: -1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 1, 6, 5 (2 de 3 a favor).
- ✅ Últimos 10: la habría pasado 8 de 10.
- ⚠️ Mark Williams ya no jugó en sus últimos partidos: la baja ya está en sus minutos.

- Triples **2.0** (por componentes 2.1 · por tasa por minuto y defensa rival 2.0): 6.0 triples intentados (su ritmo 6.1 por 36'; el rival concede +5% de triples en su reparto) × 35% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 32.4 | 33.3 | 33.6 | 33.0 | 36.7 |
| Triples anotados | 1.8 | 2.2 | 1.9 | 1.8 | 4.0 |
| Triples intentados | 5.8 | 6.3 | 5.6 | 5.5 | 8.7 |
| % triples | 31.0% | 34.9% | 34.2% | 32.2% | 46.2% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -10%, vs defensa media +11%, vs defensa débil +2%; rebotes: vs defensa fuerte -8%, vs defensa media -6%, vs defensa débil +17%; asistencias: vs defensa fuerte -12%, vs defensa media +4%, vs defensa débil +9%; triples: vs defensa fuerte +0%, vs defensa media -14%, vs defensa débil +12%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 29% | 33% | 35% | 36% |
| pintura | 27% | 48% | 45% | 48% |
| media distancia | 27% | 47% | 41% | 42% |
| bajo el aro | 15% | 68% | 68% | 71% |
| triple de esquina | 2% | 33% | 38% | 37% |

#### Ace Bailey (bases/escoltas) vs Phoenix Suns

- Minutos esperados: **29.2** (± 4.2); 88 partidos en la base.
- Jusuf Nurkic ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- sin Lauri Markkanen, la estrella de su equipo (20 partidos suyos sin él): más tiros y balón para él por minuto (puntos +15%, triples +17%, asistencias +4%)
- Lauri Markkanen ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Jaren Jackson Jr. ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Su prop más probable hoy: **Ace Bailey: menos de 2.5 asistencias** (60%). Con 80% de probabilidad: más de 0.5 / menos de 3.5.
- Defensa de Phoenix Suns contra bases/escoltas en asistencias: -8% respecto a la media; ajuste por su historial contra defensas similares: -4%.

**¿Por qué 2.2 asistencias?** (línea 2.5; 29.2 minutos esperados)

En corto:

- La pasó en 9 de 16 esta temporada (falló con 3, 4, 4, 3)
- Con 25+ minutos (hoy se esperan 29): 7 de 12 en sus últimos 15
- Contra las ~10 mejores defensas en asistencias a bases/escoltas: 12 de 16 (últimos 40 partidos)
- Contra defensas fuertes como la de hoy y con 25+ minutos: 12 de 18, con 2.0 de media (últimos 60 partidos)
- El rival es #28 de 30 en asistencias que concede a bases/escoltas por minuto (#1 = el que más concede; -8% frente a la media)
- Asistencias esperadas: 2.3 por partido si sus compañeros metieran lo normal (tiene 2.2; con él en pista metieron el 94% de lo esperado por tipo de tiro, últimos 10); ajuste aplicado +3.4%
- Oportunidades: asiste el 11% de las canastas de sus compañeros con él en pista
- Su equipo no tiene a Lauri Markkanen: más tiros y balón para él
- Minutos: 29 esperados (titular, ±4)

Razonamiento (3 factores a favor, 1 en contra):

- ✅ Minutos: 29.2 esperados (titular, ±4.2).
- ❌ Forma: 2.8 en sus últimos 5, 2.2 esta temporada (16 partidos), 1.9 la temporada pasada (línea 2.5).
- ➖ Cómo produce asistencias: asiste el 11.3% de las canastas de sus compañeros en pista × 18.4 canastas de compañeros esperadas (su equipo 40.1 por 48' contra esta defensa).
- ✅ Defensa: el rival concede -8% de asistencias por minuto a bases/escoltas (defensa fuerte); ajuste aplicado -8%.
- ➖ Ritmo del partido: -1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 2, 3, 1 (2 de 3 a favor).
- ➖ Últimos 10: la habría pasado 6 de 10.
- ⚠️ Jusuf Nurkic ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ sin Lauri Markkanen, la estrella de su equipo (20 partidos suyos sin él): más tiros y balón para él por minuto (puntos +15%, triples +17%, asistencias +4%).
- ⚠️ Lauri Markkanen ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ Jaren Jackson Jr. ya no jugó en sus últimos partidos: la baja ya está en sus minutos.

- ⚠️ Alertas: sin Lauri Markkanen: más tiros para él, falla en partidos normales (5 de 16 esta temporada).
- Asistencias **2.2** (por componentes 2.2 · por tasa por minuto y defensa rival 2.1): asiste el 11.3% de las canastas de sus compañeros en pista × 18.4 canastas de compañeros esperadas (su equipo 40.1 por 48' contra esta defensa).

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 29.2 | 30.1 | 30.4 | 27.6 | 23.7 |
| Asistencias | 2.8 | 2.2 | 2.2 | 1.8 | 2.0 |
| % de las canastas de compañeros que asiste | 13.3% | 10.6% | 10.7% | 8.7% | 11.7% |
| Pérdidas por jugada | 9.2% | 11.6% | 12.3% | 10.3% | 17.0% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -7%, vs defensa media +3%, vs defensa débil +6%; rebotes: vs defensa fuerte +1%, vs defensa media -2%, vs defensa débil +1%; asistencias: vs defensa fuerte +3%, vs defensa media -0%, vs defensa débil -3%; triples: vs defensa fuerte -4%, vs defensa media -1%, vs defensa débil +5%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 32% | 33% | 35% | 35% |
| bajo el aro | 19% | 68% | 68% | 69% |
| media distancia | 19% | 38% | 41% | 41% |
| pintura | 16% | 57% | 45% | 46% |
| triple de esquina | 14% | 32% | 38% | 37% |

## Houston Rockets @ Denver Nuggets

Diferencia esperada: Denver Nuggets por 1.5.

Parte de lesiones: Steven Adams (Day-To-Day); Clint Capela (Out); Julian Strawther (Out); Alperen Sengun (Day-To-Day).

Ventajas del partido (los dos lados): puntos esperados frente a su media de los últimos 10, ajuste por la defensa rival y diferencia de estatura con los rivales de su posición.

| Equipo | Jugador | Puntos esperados | Su media (últ. 10) | Defensa rival en puntos | Rebotes esperados | Altura vs rival |
|---|---|---|---|---|---|---|
| DEN | Nikola Jokic | 23.5 | 24.6 | -3% | 10.9 | +0.4" |
| DEN | Jamal Murray | 22.9 | 26.7 | -2% | 4.5 | +0.6" |
| DEN | Christian Braun | 12.7 | 13.5 | -2% | 4.1 | +2.6" |
| HOU | Amen Thompson | 15.6 | 14.5 | -1% | 6.4 | +2.4" |
| HOU | Kevin Durant | 21.0 | 20.1 | +3% | 5.0 | +2.6" |
| HOU | Jabari Smith Jr. | 14.2 | 14.2 | +3% | 5.7 | +2.6" |
| HOU | Fred VanVleet | 13.0 | 15.2 | -2% | 3.0 | -4.6" |
| HOU | Alperen Sengun | 17.2 | 20.5 | -2% | 8.1 | +0.0" |
| DEN | Aaron Gordon | 12.2 | 11.1 | -3% | 4.7 | -1.8" |
| DEN | Cameron Johnson | 11.4 | 11.4 | -3% | 3.6 | -1.8" |

Las 8 más probables (máximo 2 por jugador: las de un mismo jugador suelen ganar o perder juntas).

| Prop | Prob. final | Modelo | Casa | Esperado | Últ. 10 | Temporada | vs este rival | Cuota (implícita) |
|---|---|---|---|---|---|---|---|---|
| **Amen Thompson: menos de 1.5 robos** | **70%** | 75% | 64% | 1.0 ± 1.0 | 9/10 | 13/15 | 1, 1, 2, 0, 2 | 1.46 (69%) |
| **Amen Thompson: menos de 0.5 triples** | **69%** | 67% | 73% | 0.5 ± 0.8 | 9/10 | 12/15 | 0, 0, 0, 0, 1 | 1.29 (78%) |
| **Aaron Gordon: menos de 1.5 triples** | **65%** | 68% | 62% | 1.1 ± 1.1 | 7/10 | 9/13 | 0, 0, 0 | 1.51 (66%) |
| **Cameron Johnson: más de 0.5 robos** | **64%** | 70% | 59% | 1.1 ± 1.1 | 9/10 | 9/10 | 2, 2, 1, 0, 1 | 1.62 (62%) |
| **Jamal Murray: más de 0.5 robos** | **63%** | 61% | 66% | 1.0 ± 1.1 | 6/10 | 9/13 | 1, 1, 2, 0, 1 | 1.44 (69%) |
| **Nikola Jokic: más de 0.5 tapones** | **62%** | 68% | 55% | 1.1 ± 1.1 | 6/10 | 9/13 | 2, 1, 0, 1, 2 | 1.65 (61%) |
| **Marcus Smart: menos de 1.5 triples** ⚠️ suplente | **62%** | 63% | 61% | 1.3 ± 1.4 | 6/10 | 6/10 | 1, 5, 3, 3 | 1.53 (66%) |
| **Tari Eason: menos de 1.5 triples** ⚠️ suplente | **62%** | 62% | 62% | 1.3 ± 1.2 | 5/10 | 11/16 | 2, 0 | 1.51 (66%) |

### Fichas de los jugadores destacados

#### Amen Thompson (bases/escoltas) vs Denver Nuggets

- Minutos esperados: **32.7** (± 4.8); 100 partidos en la base.
- Su prop más probable hoy: **Amen Thompson: menos de 1.5 robos** (70%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Denver Nuggets contra bases/escoltas en robos: -7% respecto a la media; ajuste por su historial contra defensas similares: +1%.

**¿Por qué 1.0 robos?** (línea 1.5; 32.7 minutos esperados)

En corto:

- La pasó en 13 de 15 esta temporada (falló con 4, 2)
- Con 29+ minutos (hoy se esperan 33): 10 de 12 en sus últimos 15
- Contra las ~10 mejores defensas en robos a bases/escoltas: 10 de 14 (últimos 40 partidos)
- Contra defensas fuertes como la de hoy y con 29+ minutos: 11 de 18, con 1.6 de media (últimos 60 partidos)
- El rival es #23 de 30 en robos que concede a bases/escoltas por minuto (#1 = el que más concede; -7% frente a la media)
- Oportunidades de robo (últimos 10): el rival perdió 8.9 balones por partido con él en pista y robó el 12%
- El rival es #28 de 30 en balones que pierde (#1 = el que más; 12.3 por partido)
- Minutos: 33 esperados (titular, ±5)

Razonamiento (6 factores a favor, 0 en contra):

- ✅ Minutos: 32.7 esperados (titular, ±4.8).
- ✅ Forma: 0.8 en sus últimos 5, 1.1 esta temporada (15 partidos), 1.6 la temporada pasada (línea 1.5).
- ➖ Cómo produce robos: roba el 12.1% de las pérdidas del rival en pista × 11.5 pérdidas esperadas del rival.
- ✅ Defensa: el rival concede -7% de robos por minuto a bases/escoltas (defensa fuerte); ajuste aplicado -7%.
- ✅ Ritmo del partido: -2% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 1, 1, 2, 0, 2 (3 de 5 a favor).
- ✅ Últimos 10: la habría pasado 9 de 10.

- Robos **1.0** (por componentes 1.0 · por tasa por minuto y defensa rival 1.1): roba el 12.1% de las pérdidas del rival en pista × 11.5 pérdidas esperadas del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 33.0 | 32.8 | 33.1 | 37.9 | 38.0 |
| Robos | 0.8 | 1.1 | 1.1 | 1.5 | 1.2 |
| % de las pérdidas del rival que roba | 10.5% | 12.4% | 10.8% | 14.9% | 15.4% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -10%, vs defensa media +2%, vs defensa débil +6%; rebotes: vs defensa fuerte -5%, vs defensa media +2%, vs defensa débil +4%; asistencias: vs defensa fuerte -3%, vs defensa media +1%, vs defensa débil +1%; triples: vs defensa fuerte +4%, vs defensa media +9%, vs defensa débil -15%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 47% | 72% | 68% | 70% |
| pintura | 32% | 43% | 45% | 45% |
| media distancia | 10% | 32% | 41% | 40% |
| triple de esquina | 7% | 29% | 38% | 37% |
| triple frontal | 4% | 29% | 35% | 35% |

#### Aaron Gordon (aleros/ala-pívots) vs Houston Rockets

- Minutos esperados: **28.7** (± 3.1); 52 partidos en la base.
- Su prop más probable hoy: **Aaron Gordon: menos de 1.5 triples** (65%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Houston Rockets contra aleros/ala-pívots en triples: -8% respecto a la media; ajuste por su historial contra defensas similares: -1%.

**¿Por qué 1.1 triples?** (línea 1.5; 28.7 minutos esperados)

En corto:

- La pasó en 9 de 13 esta temporada (falló con 2, 2, 2, 3)
- Con 25+ minutos (hoy se esperan 29): 10 de 13 en sus últimos 15
- Contra las ~10 mejores defensas en triples a aleros/ala-pívots: 13 de 17 (últimos 40 partidos)
- Contra defensas fuertes como la de hoy y con 25+ minutos: 12 de 17, con 1.3 de media (últimos 60 partidos)
- El rival es #30 de 30 en triples que concede a aleros/ala-pívots por minuto (#1 = el que más concede; -14% frente a la media)
- Su zona principal es triple frontal (29% de sus tiros, 33% de acierto); el rival es #29 de 30 en acierto que deja ahí (34%, liga 35%)
- Cómo tira (últimos 15): recibe y tira 36% (38% de acierto), creado 19% (16% de acierto), penetración 17% (48% de acierto); en recibe y tira el rival es #30 de 30 en lo que deja (#1 = el que más; 0.98 puntos por tiro frente a 1.07 de media)
- Oportunidades: 3.8 triples intentados esperados al 34%
- Minutos: 29 esperados (titular, ±3)

Razonamiento (7 factores a favor, 0 en contra):

- ✅ Minutos: 28.7 esperados (titular, ±3.1).
- ✅ Forma: 0.8 en sus últimos 5, 1.1 esta temporada (13 partidos), 1.6 la temporada pasada (línea 1.5).
- ➖ Cómo produce triples: 3.8 triples intentados (su ritmo 4.9 por 36'; el rival concede -2% de triples en su reparto) × 34% esperado.
- ✅ Defensa: el rival concede -14% de triples por minuto a aleros/ala-pívots (defensa fuerte); ajuste aplicado -8%; en su zona principal (triple) el rival concede 34% (liga 35%).
- ✅ Altura: mide 6'8", 1.8 pulgadas menos que los aleros/ala-pívots del rival (-0.6% en esta estadística).
- ✅ Ritmo del partido: -2% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 0, 0, 0 (3 de 3 a favor).
- ✅ Últimos 10: la habría pasado 7 de 10.

- ⚠️ Alertas: falla en partidos normales (4 de 13 esta temporada).
- Triples **1.1** (por componentes 1.3 · por tasa por minuto y defensa rival 1.1): 3.8 triples intentados (su ritmo 4.9 por 36'; el rival concede -2% de triples en su reparto) × 34% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 29.0 | 28.7 | 29.1 | 28.0 | 18.3 |
| Triples anotados | 0.8 | 1.0 | 1.1 | 1.6 | 0.0 |
| Triples intentados | 3.0 | 3.7 | 3.8 | 4.4 | 1.7 |
| % triples | 26.7% | 27.0% | 28.6% | 37.4% | 0.0% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -3%, vs defensa media -2%, vs defensa débil +10%; rebotes: vs defensa fuerte -12%, vs defensa media -8%, vs defensa débil +16%; asistencias: vs defensa fuerte -14%, vs defensa media +13%, vs defensa débil +3%; triples: vs defensa fuerte -23%, vs defensa media +41%, vs defensa débil -21%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 32% | 72% | 68% | 67% |
| triple frontal | 29% | 33% | 35% | 34% |
| pintura | 16% | 34% | 45% | 46% |
| triple de esquina | 12% | 38% | 38% | 38% |
| media distancia | 11% | 42% | 41% | 40% |

#### Cameron Johnson (aleros/ala-pívots) vs Houston Rockets

- Minutos esperados: **28.5** (± 3.9); 69 partidos en la base.
- Su prop más probable hoy: **Cameron Johnson: más de 0.5 robos** (64%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Houston Rockets contra aleros/ala-pívots en robos: +13% respecto a la media; ajuste por su historial contra defensas similares: +4%.

**¿Por qué 1.1 robos?** (línea 0.5; 28.5 minutos esperados)

En corto:

- La pasó en 9 de 10 esta temporada; los fallos, en partidos raros (jugó 11 min)
- Con 24+ minutos (hoy se esperan 28): 12 de 13 en sus últimos 15
- Contra las ~10 mejores defensas en robos a aleros/ala-pívots: 9 de 16 (últimos 40 partidos)
- Contra defensas débiles como la de hoy y con 24+ minutos: 13 de 16, con 1.4 de media (últimos 60 partidos)
- El rival es #2 de 30 en robos que concede a aleros/ala-pívots por minuto (#1 = el que más concede; +13% frente a la media)
- Oportunidades de robo (últimos 10): el rival perdió 8.4 balones por partido con él en pista y robó el 13%
- El rival es #17 de 30 en balones que pierde (#1 = el que más; 14.0 por partido)
- Minutos: 28 esperados (titular, ±4)

Razonamiento (5 factores a favor, 1 en contra):

- ✅ Minutos: 28.5 esperados (titular, ±3.9).
- ✅ Forma: 1.2 en sus últimos 5, 1.1 esta temporada (10 partidos), 0.8 la temporada pasada (línea 0.5).
- ➖ Cómo produce robos: roba el 12.4% de las pérdidas del rival en pista × 11.9 pérdidas esperadas del rival.
- ✅ Defensa: el rival concede +13% de robos por minuto a aleros/ala-pívots (defensa débil); ajuste aplicado +13%.
- ❌ Ritmo del partido: -2% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 2, 2, 1, 0, 1 (4 de 5 a favor).
- ✅ Últimos 10: la habría pasado 9 de 10.

- Robos **1.1** (por componentes 0.9 · por tasa por minuto y defensa rival 1.2): roba el 12.4% de las pérdidas del rival en pista × 11.9 pérdidas esperadas del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 29.0 | 28.3 | 28.3 | 30.4 | 32.6 |
| Robos | 1.2 | 1.1 | 1.1 | 0.8 | 1.2 |
| % de las pérdidas del rival que roba | 13.0% | 13.1% | 13.1% | 10.5% | 11.1% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -10%, vs defensa media +8%, vs defensa débil +18%; rebotes: vs defensa fuerte +10%, vs defensa media -22%, vs defensa débil +9%; asistencias: vs defensa fuerte -10%, vs defensa media +3%, vs defensa débil +11%; triples: vs defensa fuerte -10%, vs defensa media +1%, vs defensa débil +25%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 35% | 38% | 35% | 34% |
| bajo el aro | 23% | 70% | 68% | 67% |
| triple de esquina | 19% | 39% | 38% | 38% |
| pintura | 14% | 45% | 45% | 46% |
| media distancia | 9% | 40% | 41% | 40% |

#### Jamal Murray (bases/escoltas) vs Houston Rockets

- Minutos esperados: **36.0** (± 3.0); 95 partidos en la base.
- Su prop más probable hoy: **Jamal Murray: más de 0.5 robos** (63%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Houston Rockets contra bases/escoltas en robos: +2% respecto a la media; ajuste por su historial contra defensas similares: -8%.

**¿Por qué 1.0 robos?** (línea 0.5; 36.0 minutos esperados)

En corto:

- La pasó en 9 de 13 esta temporada (falló con 0, 0, 0, 0)
- Con 32+ minutos (hoy se esperan 36): 9 de 14 en sus últimos 15
- Contra las ~10 mejores defensas en robos a bases/escoltas: 10 de 17 (últimos 40 partidos)
- Contra defensas medias como la de hoy y con 32+ minutos: 4 de 15, con 0.5 de media (últimos 60 partidos)
- El rival es #15 de 30 en robos que concede a bases/escoltas por minuto (#1 = el que más concede; +2% frente a la media)
- Oportunidades de robo (últimos 10): el rival perdió 10.9 balones por partido con él en pista y robó el 9%
- El rival es #17 de 30 en balones que pierde (#1 = el que más; 14.0 por partido)
- Minutos: 36 esperados (titular, ±3)

Razonamiento (3 factores a favor, 1 en contra):

- ✅ Minutos: 36.0 esperados (titular, ±3.0).
- ✅ Forma: 1.4 en sus últimos 5, 1.2 esta temporada (13 partidos), 0.8 la temporada pasada (línea 0.5).
- ➖ Cómo produce robos: roba el 10.9% de las pérdidas del rival en pista × 11.9 pérdidas esperadas del rival.
- ➖ Defensa: el rival concede +2% de robos por minuto a bases/escoltas (defensa media); ajuste aplicado +2%.
- ❌ Ritmo del partido: -2% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 1, 1, 2, 0, 1 (4 de 5 a favor).
- ➖ Últimos 10: la habría pasado 6 de 10.

- Robos **1.0** (por componentes 1.0 · por tasa por minuto y defensa rival 1.0): roba el 10.9% de las pérdidas del rival en pista × 11.9 pérdidas esperadas del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 36.4 | 35.8 | 36.5 | 35.0 | 37.8 |
| Robos | 1.4 | 1.0 | 1.2 | 0.9 | 1.0 |
| % de las pérdidas del rival que roba | 13.0% | 9.2% | 10.5% | 11.0% | 8.8% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -2%, vs defensa media -2%, vs defensa débil +4%; rebotes: vs defensa fuerte -17%, vs defensa media +12%, vs defensa débil +6%; asistencias: vs defensa fuerte -13%, vs defensa media +8%, vs defensa débil +15%; triples: vs defensa fuerte +2%, vs defensa media -11%, vs defensa débil +8%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 36% | 41% | 35% | 34% |
| pintura | 22% | 45% | 45% | 46% |
| media distancia | 20% | 46% | 41% | 40% |
| bajo el aro | 17% | 66% | 68% | 67% |
| triple de esquina | 5% | 49% | 38% | 38% |

#### Nikola Jokic (pívots) vs Houston Rockets

- Minutos esperados: **37.2** (± 3.0); 84 partidos en la base.
- Su prop más probable hoy: **Nikola Jokic: más de 0.5 tapones** (62%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Houston Rockets contra pívots en tapones: -1% respecto a la media; ajuste por su historial contra defensas similares: +0%.

**¿Por qué 1.1 tapones?** (línea 0.5; 37.2 minutos esperados)

En corto:

- La pasó en 9 de 13 esta temporada (falló con 0, 0, 0, 0)
- Con 33+ minutos (hoy se esperan 37): 11 de 14 en sus últimos 15
- Contra las ~10 mejores defensas en tapones a pívots: 9 de 11 (últimos 40 partidos)
- Contra defensas medias como la de hoy y con 33+ minutos: 11 de 17, con 1.1 de media (últimos 60 partidos)
- El rival es #16 de 30 en tapones que concede a pívots por minuto (#1 = el que más concede; -1% frente a la media)
- Oportunidades de tapón (últimos 10): 38.0 tiros de 2 del rival por partido con él en pista; taponó el 1.8%
- El rival es #3 de 30 en tiros de 2 por partido (#1 = el que más; 56.1)
- El 47% de los tiros del rival son cerca del aro (penetración, corte, poste, palmeo): #17 de 30
- Minutos: 37 esperados (titular, ±3)

Razonamiento (3 factores a favor, 1 en contra):

- ✅ Minutos: 37.2 esperados (titular, ±3.0).
- ✅ Forma: 1.0 en sus últimos 5, 1.1 esta temporada (13 partidos), 0.8 la temporada pasada (línea 0.5).
- ➖ Cómo produce tapones: tapona el 2.8% de los tiros de 2 del rival en pista × 56.5 tiros de 2 esperados del rival.
- ➖ Defensa: el rival concede -1% de tapones por minuto a pívots (defensa media); ajuste aplicado -1%.
- ❌ Ritmo del partido: -2% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 2, 1, 0, 1, 2 (4 de 5 a favor).
- ➖ Últimos 10: la habría pasado 6 de 10.

- Tapones **1.1** (por componentes 1.2 · por tasa por minuto y defensa rival 1.1): tapona el 2.8% de los tiros de 2 del rival en pista × 56.5 tiros de 2 esperados del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 38.0 | 36.3 | 36.7 | 34.7 | 35.8 |
| Tapones | 1.0 | 0.7 | 1.1 | 0.8 | 1.2 |
| % de los tiros de 2 del rival que tapona | 2.6% | 1.8% | 2.8% | 2.1% | 2.9% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -2%, vs defensa media -8%, vs defensa débil +8%; rebotes: vs defensa fuerte -2%, vs defensa media -2%, vs defensa débil +3%; asistencias: vs defensa fuerte -7%, vs defensa media -3%, vs defensa débil +5%; triples: vs defensa fuerte -2%, vs defensa media -5%, vs defensa débil +14%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| pintura | 38% | 57% | 45% | 46% |
| bajo el aro | 25% | 72% | 68% | 67% |
| triple frontal | 24% | 33% | 35% | 34% |
| media distancia | 12% | 49% | 41% | 40% |
| triple de esquina | 2% | 42% | 38% | 38% |

## Sacramento Kings @ Los Angeles Lakers

Diferencia esperada: Los Angeles Lakers por 14.5 — puede romperse: titulares -3% de minutos, suplentes +4%.

Parte de lesiones: Ben Simmons (Out); De'Andre Hunter (Day-To-Day); Austin Reaves (Out); Precious Achiuwa (Day-To-Day); Maxime Raynaud (Out).

Ventajas del partido (los dos lados): puntos esperados frente a su media de los últimos 10, ajuste por la defensa rival y diferencia de estatura con los rivales de su posición.

| Equipo | Jugador | Puntos esperados | Su media (últ. 10) | Defensa rival en puntos | Rebotes esperados | Altura vs rival |
|---|---|---|---|---|---|---|
| LAL | Luka Doncic | 35.6 | 38.9 | +5% | 7.1 | +4.6" |
| SAC | Darius Acuff Jr. | 24.2 | 28.1 | +1% | 3.3 | -3.2" |
| SAC | De'Andre Hunter | 15.5 | 15.4 | -1% | 4.5 | -1.2" |
| LAL | Quentin Grimes | 17.4 | 14.9 | +4% | 3.9 | +0.6" |
| SAC | Zach LaVine | 18.6 | 18.8 | +1% | 2.9 | -0.2" |
| LAL | Walker Kessler | 15.9 | 13.9 | +6% | 10.9 | +3.9" |
| SAC | Domantas Sabonis | 13.0 | 12.2 | +0% | 10.2 | +1.8" |
| SAC | Keegan Murray | 11.0 | 9.8 | -1% | 3.9 | -0.2" |
| LAL | Jake LaRavia | 8.7 | 6.0 | +6% | 4.3 | -0.9" |
| LAL | Matisse Thybulle | 9.3 | 5.6 | +5% | 2.9 | +1.6" |

Las 8 más probables (máximo 2 por jugador: las de un mismo jugador suelen ganar o perder juntas).

| Prop | Prob. final | Modelo | Casa | Esperado | Últ. 10 | Temporada | vs este rival | Cuota (implícita) |
|---|---|---|---|---|---|---|---|---|
| **Ziaire Williams: más de 0.5 triples** ⚠️ suplente | **70%** | 75% | 63% | 1.4 ± 1.2 | 8/10 | 11/13 | 1, 2 | 1.48 (68%) |
| **Domantas Sabonis: menos de 5.5 asistencias** | **64%** | 68% | 58% | 4.3 ± 2.3 | 6/10 | 7/13 | 1, 3 | 1.61 (62%) |
| **Keegan Murray: más de 0.5 robos** | **63%** | 58% | 66% | 1.0 ± 1.0 | 6/10 | 5/7 | - | 1.44 (70%) |
| **Malik Monk: menos de 4.5 asistencias** ⚠️ suplente | **62%** | 65% | 58% | 3.9 ± 2.7 | 7/10 | 9/13 | 3, 2, 8, 2, 2 | 1.61 (62%) |
| **Ziaire Williams: más de 7.5 puntos** ⚠️ suplente | **61%** | 70% | 51% | 10.4 ± 4.8 | 7/10 | 10/13 | 10, 18 | 1.87 (53%) |
| **Zach LaVine: menos de 3.5 rebotes** | **61%** | 62% | 59% | 2.9 ± 1.8 | 5/10 | 6/13 | 4, 4, 4 | 1.59 (63%) |
| **Sandro Mamukelashvili: menos de 1.5 triples** ⚠️ suplente | **60%** | 60% | 61% | 1.5 ± 1.6 | 6/10 | 11/16 | 0, 3, 3 | 1.56 (64%) |
| **Domantas Sabonis: menos de 17.5 reb+ast** | **60%** | 66% | 53% | 14.6 ± 4.8 | 5/10 | 5/13 | 18, 17 | 1.78 (56%) |

### Fichas de los jugadores destacados

#### Ziaire Williams (aleros/ala-pívots) vs Sacramento Kings

- Minutos esperados: **22.0** (± 3.5); 69 partidos en la base.
- sin Austin Reaves, la estrella de su equipo (4 partidos suyos sin él): más tiros y balón para él por minuto (puntos +1%, triples -3%, asistencias +3%)
- Austin Reaves ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- partido desigual (favorito por 14.5): los suplentes suelen jugar +4% de minutos si se rompe
- Su prop más probable hoy: **Ziaire Williams: más de 0.5 triples** (70%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Sacramento Kings contra aleros/ala-pívots en triples: +4% respecto a la media; ajuste por su historial contra defensas similares: +1%.

**¿Por qué 1.4 triples?** (línea 0.5; 22.0 minutos esperados)

En corto:

- La pasó en 11 de 13 esta temporada (falló con 0, 0)
- Con 18+ minutos (hoy se esperan 22): 11 de 13 en sus últimos 15
- Contra las ~10 mejores defensas en triples a aleros/ala-pívots: 10 de 14 (últimos 40 partidos)
- Contra defensas medias como la de hoy y con 18+ minutos: 14 de 17, con 1.3 de media (últimos 60 partidos)
- El rival es #11 de 30 en triples que concede a aleros/ala-pívots por minuto (#1 = el que más concede; +3% frente a la media)
- Su zona principal es triple frontal (36% de sus tiros, 36% de acierto); el rival es #1 de 30 en acierto que deja ahí (37%, liga 35%)
- Su segunda zona es triple de esquina (22% de sus tiros, 39% de acierto); el rival es #2 de 30 en acierto que deja ahí (40%, liga 38%)
- Cómo tira (últimos 15): recibe y tira 49% (46% de acierto), penetración 28% (56% de acierto), creado 12% (33% de acierto); en recibe y tira el rival es #12 de 30 en lo que deja (#1 = el que más; 1.10 puntos por tiro frente a 1.07 de media)
- Oportunidades: 3.3 triples intentados esperados al 39%
- Su equipo no tiene a Austin Reaves: más tiros y balón para él
- Minutos: 22 esperados (suplente, ±4)

Razonamiento (4 factores a favor, 1 en contra):

- ❌ Minutos: 22.0 esperados (suplente, ±3.5).
- ✅ Forma: 0.8 en sus últimos 5, 1.6 esta temporada (13 partidos), 1.5 la temporada pasada (línea 0.5).
- ➖ Cómo produce triples: 3.3 triples intentados (su ritmo 5.7 por 36'; el rival concede -1% de triples en su reparto) × 39% esperado.
- ✅ Defensa: el rival concede +3% de triples por minuto a aleros/ala-pívots (defensa media); ajuste aplicado +4%; en su zona principal (triple) el rival concede 37% (liga 35%).
- ➖ Ritmo del partido: +1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 1, 2 (2 de 2 a favor).
- ✅ Últimos 10: la habría pasado 8 de 10.
- ⚠️ sin Austin Reaves, la estrella de su equipo (4 partidos suyos sin él): más tiros y balón para él por minuto (puntos +1%, triples -3%, asistencias +3%).
- ⚠️ Austin Reaves ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ partido desigual (favorito por 14.5): los suplentes suelen jugar +4% de minutos si se rompe.

- ⚠️ Alertas: suplente, riesgo de paliza.
- Triples **1.4** (por componentes 1.3 · por tasa por minuto y defensa rival 1.5): 3.3 triples intentados (su ritmo 5.7 por 36'; el rival concede -1% de triples en su reparto) × 39% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 21.8 | 21.7 | 23.2 | 22.9 | 22.5 |
| Triples anotados | 0.8 | 1.6 | 1.6 | 1.5 | 1.5 |
| Triples intentados | 2.0 | 3.5 | 3.6 | 4.5 | 3.5 |
| % triples | 40.0% | 45.7% | 44.7% | 34.3% | 42.9% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -4%, vs defensa media -1%, vs defensa débil +7%; rebotes: vs defensa fuerte -5%, vs defensa media +5%, vs defensa débil +3%; asistencias: vs defensa fuerte -50%, vs defensa media +27%, vs defensa débil +34%; triples: vs defensa fuerte +4%, vs defensa media +0%, vs defensa débil -5%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 36% | 36% | 35% | 37% |
| bajo el aro | 27% | 70% | 68% | 72% |
| triple de esquina | 22% | 39% | 38% | 40% |
| pintura | 11% | 40% | 45% | 51% |
| media distancia | 4% | 41% | 41% | 42% |

#### Domantas Sabonis (aleros/ala-pívots) vs Los Angeles Lakers

- Minutos esperados: **29.1** (± 5.1); 32 partidos en la base.
- Maxime Raynaud ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- partido desigual (no favorito por 14.5): los titulares suelen jugar -3% de minutos si se rompe
- Su prop más probable hoy: **Domantas Sabonis: menos de 5.5 asistencias** (64%). Con 80% de probabilidad: más de 1.5 / menos de 6.5.
- Defensa de Los Angeles Lakers contra aleros/ala-pívots en asistencias: -4% respecto a la media; ajuste por su historial contra defensas similares: -1%.

**¿Por qué 4.3 asistencias?** (línea 5.5; 29.1 minutos esperados)

En corto:

- La pasó en 7 de 13 esta temporada (falló con 8, 8, 7, 8)
- Con 25+ minutos (hoy se esperan 29): 7 de 12 en sus últimos 15
- Contra las ~10 mejores defensas en asistencias a aleros/ala-pívots: 9 de 12 (últimos 40 partidos)
- Contra defensas fuertes como la de hoy y con 25+ minutos: 8 de 10, con 4.1 de media (últimos 60 partidos)
- El rival es #23 de 30 en asistencias que concede a aleros/ala-pívots por minuto (#1 = el que más concede; -4% frente a la media)
- Asistencias esperadas: 5.4 por partido si sus compañeros metieran lo normal (tiene 5.4; con él en pista metieron el 100% de lo esperado por tipo de tiro, últimos 10); ajuste aplicado +0.3%
- Oportunidades: asiste el 21% de las canastas de sus compañeros con él en pista
- El rival no tiene a Austin Reaves (4.1 asistencias por partido)
- Minutos: 29 esperados (titular, ±5)

Razonamiento (4 factores a favor, 1 en contra):

- ✅ Minutos: 29.1 esperados (titular, ±5.1).
- ✅ Forma: 5.2 en sus últimos 5, 5.8 esta temporada (13 partidos), 4.1 la temporada pasada (línea 5.5).
- ➖ Cómo produce asistencias: asiste el 21.4% de las canastas de sus compañeros en pista × 19.5 canastas de compañeros esperadas (su equipo 40.8 por 48' contra esta defensa).
- ✅ Defensa: el rival concede -4% de asistencias por minuto a aleros/ala-pívots (defensa fuerte); ajuste aplicado -4%.
- ➖ Ritmo del partido: +1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 1, 3 (2 de 2 a favor).
- ➖ Últimos 10: la habría pasado 6 de 10.
- ❌ Bajas del rival: sin Austin Reaves (titular); +1.5% en esta estadística.
- ⚠️ Maxime Raynaud ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ partido desigual (no favorito por 14.5): los titulares suelen jugar -3% de minutos si se rompe.

- Asistencias **4.3** (por componentes 4.2 · por tasa por minuto y defensa rival 4.3): asiste el 21.4% de las canastas de sus compañeros en pista × 19.5 canastas de compañeros esperadas (su equipo 40.8 por 48' contra esta defensa).

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 28.6 | 32.4 | 33.2 | 29.7 | 33.0 |
| Asistencias | 5.2 | 5.4 | 5.8 | 4.1 | 2.0 |
| % de las canastas de compañeros que asiste | 26.5% | 23.6% | 24.6% | 18.9% | 8.3% |
| Pérdidas por jugada | 15.8% | 20.9% | 22.5% | 16.7% | 14.9% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +8%, vs defensa media -7%, vs defensa débil -4%; rebotes: vs defensa fuerte +7%, vs defensa media -7%, vs defensa débil -1%; asistencias: vs defensa fuerte -9%, vs defensa media +11%, vs defensa débil -2%; triples: vs defensa fuerte +33%, vs defensa media -26%, vs defensa débil -13%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 48% | 71% | 68% | 72% |
| pintura | 36% | 52% | 45% | 44% |
| triple frontal | 10% | 30% | 35% | 35% |
| media distancia | 4% | 46% | 41% | 42% |
| triple de esquina | 2% | 36% | 38% | 38% |

#### Keegan Murray (aleros/ala-pívots) vs Los Angeles Lakers

- Minutos esperados: **27.2** (± 6.6); 30 partidos en la base.
- Maxime Raynaud ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- partido desigual (no favorito por 14.5): los titulares suelen jugar -3% de minutos si se rompe
- Su prop más probable hoy: **Keegan Murray: más de 0.5 robos** (63%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Los Angeles Lakers contra aleros/ala-pívots en robos: +5% respecto a la media; ajuste por su historial contra defensas similares: +4%.

**¿Por qué 1.0 robos?** (línea 0.5; 27.2 minutos esperados)

En corto:

- La pasó en 5 de 7 esta temporada (falló con 0, 0)
- Con 23+ minutos (hoy se esperan 27): 6 de 12 en sus últimos 15
- Contra las ~10 mejores defensas en robos a aleros/ala-pívots: 7 de 11 (últimos 40 partidos)
- Contra defensas débiles como la de hoy y con 23+ minutos: 7 de 10, con 1.0 de media (últimos 60 partidos)
- El rival es #8 de 30 en robos que concede a aleros/ala-pívots por minuto (#1 = el que más concede; +5% frente a la media)
- Oportunidades de robo (últimos 9): el rival perdió 7.9 balones por partido con él en pista y robó el 11%
- El rival es #10 de 30 en balones que pierde (#1 = el que más; 14.5 por partido)
- El rival no tiene a Austin Reaves (1.0 robos por partido)
- Minutos: 27 esperados (titular, ±7)

Razonamiento (2 factores a favor, 1 en contra):

- ❌ Minutos: 27.2 esperados (titular, ±6.6).
- ✅ Forma: 1.0 en sus últimos 5, 1.0 esta temporada (7 partidos), 1.0 la temporada pasada (línea 0.5).
- ➖ Cómo produce robos: roba el 12.0% de las pérdidas del rival en pista × 13.9 pérdidas esperadas del rival.
- ✅ Defensa: el rival concede +5% de robos por minuto a aleros/ala-pívots (defensa débil); ajuste aplicado +5%.
- ➖ Ritmo del partido: +1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ➖ Últimos 10: la habría pasado 6 de 10.
- ⚠️ Maxime Raynaud ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ partido desigual (no favorito por 14.5): los titulares suelen jugar -3% de minutos si se rompe.

- ⚠️ Alertas: minutos inestables.
- Robos **1.0** (por componentes 0.9 · por tasa por minuto y defensa rival 1.0): roba el 12.0% de las pérdidas del rival en pista × 13.9 pérdidas esperadas del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 27.8 | 27.2 | 27.6 | 34.6 | - |
| Robos | 1.0 | 0.8 | 1.0 | 1.0 | - |
| % de las pérdidas del rival que roba | 14.7% | 10.9% | 14.6% | 10.5% | - |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +0%, vs defensa media -12%, vs defensa débil +31%; rebotes: vs defensa fuerte +6%, vs defensa media +4%, vs defensa débil -12%; asistencias: vs defensa fuerte -19%, vs defensa media +21%, vs defensa débil -16%; triples: vs defensa fuerte +5%, vs defensa media -32%, vs defensa débil +9%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| pintura | 36% | 49% | 45% | 44% |
| triple frontal | 29% | 31% | 35% | 35% |
| media distancia | 15% | 37% | 41% | 42% |
| bajo el aro | 11% | 71% | 68% | 72% |
| triple de esquina | 9% | 28% | 38% | 38% |

#### Malik Monk (bases/escoltas) vs Los Angeles Lakers

- Minutos esperados: **20.2** (± 7.7); 75 partidos en la base.
- Maxime Raynaud ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- partido desigual (no favorito por 14.5): los suplentes suelen jugar +4% de minutos si se rompe
- Su prop más probable hoy: **Malik Monk: menos de 4.5 asistencias** (62%). Con 80% de probabilidad: más de 1.5 / menos de 6.5.
- Defensa de Los Angeles Lakers contra bases/escoltas en asistencias: +6% respecto a la media; ajuste por su historial contra defensas similares: -1%.

**¿Por qué 3.9 asistencias?** (línea 4.5; 20.2 minutos esperados)

En corto:

- La pasó en 9 de 13 esta temporada (falló con 10, 7, 7, 6)
- Con 16+ minutos (hoy se esperan 20): 4 de 7 en sus últimos 15
- Contra las ~10 mejores defensas en asistencias a bases/escoltas: 9 de 16 (últimos 40 partidos)
- Contra defensas débiles como la de hoy y con 16+ minutos: 10 de 14, con 3.6 de media (últimos 60 partidos)
- El rival es #7 de 30 en asistencias que concede a bases/escoltas por minuto (#1 = el que más concede; +6% frente a la media)
- Asistencias esperadas: 3.9 por partido si sus compañeros metieran lo normal (tiene 3.9; con él en pista metieron el 101% de lo esperado por tipo de tiro, últimos 10); ajuste aplicado -0.3%
- Oportunidades: asiste el 25% de las canastas de sus compañeros con él en pista
- El rival no tiene a Austin Reaves (4.1 asistencias por partido)
- Minutos: 20 esperados (suplente, ±8)

Razonamiento (3 factores a favor, 3 en contra):

- ❌ Minutos: 20.2 esperados (suplente, ±7.7).
- ✅ Forma: 3.6 en sus últimos 5, 3.8 esta temporada (13 partidos), 3.0 la temporada pasada (línea 4.5).
- ➖ Cómo produce asistencias: asiste el 25.0% de las canastas de sus compañeros en pista × 13.5 canastas de compañeros esperadas (su equipo 40.8 por 48' contra esta defensa).
- ❌ Defensa: el rival concede +6% de asistencias por minuto a bases/escoltas (defensa débil); ajuste aplicado +6%.
- ➖ Ritmo del partido: +1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 3, 2, 8, 2, 2 (4 de 5 a favor).
- ✅ Últimos 10: la habría pasado 7 de 10.
- ❌ Bajas del rival: sin Austin Reaves (titular); +1.5% en esta estadística.
- ⚠️ Maxime Raynaud ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ partido desigual (no favorito por 14.5): los suplentes suelen jugar +4% de minutos si se rompe.

- ⚠️ Alertas: suplente, minutos inestables.
- Asistencias **3.9** (por componentes 3.4 · por tasa por minuto y defensa rival 4.0): asiste el 25.0% de las canastas de sus compañeros en pista × 13.5 canastas de compañeros esperadas (su equipo 40.8 por 48' contra esta defensa).

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 18.2 | 18.5 | 17.1 | 22.0 | 23.0 |
| Asistencias | 3.6 | 3.9 | 3.8 | 3.0 | 3.4 |
| % de las canastas de compañeros que asiste | 27.3% | 29.2% | 29.7% | 17.7% | 19.2% |
| Pérdidas por jugada | 19.4% | 18.3% | 17.2% | 11.8% | 11.9% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -3%, vs defensa media +7%, vs defensa débil -5%; rebotes: vs defensa fuerte +9%, vs defensa media -4%, vs defensa débil -6%; asistencias: vs defensa fuerte -1%, vs defensa media +8%, vs defensa débil -6%; triples: vs defensa fuerte -22%, vs defensa media +24%, vs defensa débil -7%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 42% | 38% | 35% | 35% |
| pintura | 28% | 40% | 45% | 44% |
| bajo el aro | 13% | 69% | 68% | 72% |
| media distancia | 9% | 42% | 41% | 42% |
| triple de esquina | 7% | 36% | 38% | 38% |

#### Zach LaVine (bases/escoltas) vs Los Angeles Lakers

- Minutos esperados: **31.1** (± 4.3); 52 partidos en la base.
- Maxime Raynaud ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- partido desigual (no favorito por 14.5): los titulares suelen jugar -3% de minutos si se rompe
- Su prop más probable hoy: **Zach LaVine: menos de 3.5 rebotes** (61%). Con 80% de probabilidad: más de 0.5 / menos de 4.5.
- Defensa de Los Angeles Lakers contra bases/escoltas en rebotes: -8% respecto a la media; ajuste por su historial contra defensas similares: -1%.

**¿Por qué 2.9 rebotes?** (línea 3.5; 31.1 minutos esperados)

En corto:

- La pasó en 6 de 13 esta temporada (falló con 5, 4, 4, 4)
- Con 27+ minutos (hoy se esperan 31): 5 de 11 en sus últimos 15
- Contra las ~10 mejores defensas en rebotes a bases/escoltas: 9 de 14 (últimos 40 partidos)
- Contra defensas fuertes como la de hoy y con 27+ minutos: 6 de 14, con 3.3 de media (últimos 60 partidos)
- El rival es #28 de 30 en rebotes que concede a bases/escoltas por minuto (#1 = el que más concede; -8% frente a la media)
- El rival es #27 de 30 en rebotes que concede en total (#1 = el que más)
- El rival es #18 de 30 en rebotes ofensivos que concede en total (#1 = el que más)
- Rebotes disponibles con él en pista (últimos 10): 27.4 tiros fallados del rival y 30.1 de su equipo por partido; se queda el 11% y el 1%; el rival falla 43.9 tiros por partido (#30 de 30, #1 = el que más falla)
- El rival no tiene a Austin Reaves (3.4 rebotes por partido)
- Minutos: 31 esperados (titular, ±4)

Razonamiento (2 factores a favor, 2 en contra):

- ✅ Minutos: 31.1 esperados (titular, ±4.3).
- ❌ Forma: 3.8 en sus últimos 5, 3.4 esta temporada (13 partidos), 2.8 la temporada pasada (línea 3.5).
- ➖ Cómo produce rebotes: defensivos 2.5 = captura el 9.9% de los fallos del rival en pista × 39.5 fallos esperados del rival (liga 46.9) × 65% del partido; ofensivos 0.4 = 1.4% de los fallos de su equipo × 45.9.
- ✅ Defensa: el rival concede -8% de rebotes por minuto a bases/escoltas (defensa fuerte); ajuste aplicado -8%.
- ➖ Ritmo del partido: +1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ❌ Contra este rival: 4, 4, 4 (0 de 3 a favor).
- ➖ Últimos 10: la habría pasado 5 de 10.
- ⚠️ Maxime Raynaud ya no jugó en sus últimos partidos: la baja ya está en sus minutos.
- ⚠️ partido desigual (no favorito por 14.5): los titulares suelen jugar -3% de minutos si se rompe.

- Rebotes **2.9** (por componentes 2.9 · por tasa por minuto y defensa rival 2.9): defensivos 2.5 = captura el 9.9% de los fallos del rival en pista × 39.5 fallos esperados del rival (liga 46.9) × 65% del partido; ofensivos 0.4 = 1.4% de los fallos de su equipo × 45.9.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 32.2 | 31.5 | 32.9 | 31.4 | 35.7 |
| Rebotes | 3.8 | 3.3 | 3.4 | 2.8 | 4.0 |
| % de los fallos del rival que captura | 13.7% | 10.6% | 10.0% | 8.8% | 10.5% |
| % de los fallos de su equipo que captura | 0.0% | 1.3% | 1.2% | 0.7% | 1.7% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -19%, vs defensa media -2%, vs defensa débil +18%; rebotes: vs defensa fuerte -4%, vs defensa media -5%, vs defensa débil +6%; asistencias: vs defensa fuerte -8%, vs defensa media +19%, vs defensa débil -4%; triples: vs defensa fuerte +13%, vs defensa media -23%, vs defensa débil +8%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 38% | 38% | 35% | 35% |
| bajo el aro | 19% | 73% | 68% | 72% |
| media distancia | 18% | 45% | 41% | 42% |
| pintura | 15% | 51% | 45% | 44% |
| triple de esquina | 10% | 42% | 38% | 38% |
