# Props NBA 2026-11-06

> **Aviso:** las apuestas implican riesgo de perder dinero. Estas probabilidades son estimaciones estadísticas, no garantías: ningún modelo acierta siempre y las combinadas multiplican el riesgo. Apuesta solo lo que puedas permitirte perder. Si el juego deja de ser un entretenimiento, busca ayuda.

**Modelo** = minutos, tasa por minuto, bajas, defensa rival por posición, zonas de tiro y tipo de defensa, mezclado con el acierto real del jugador sobre esa línea. **Casa** = probabilidad implícita en las cuotas sin el margen. **Prob. final** = mezcla de ambas. Si modelo y casa discrepan mucho, la casa suele saber algo (rol, rotación, una baja): revísalo antes de apostar.

Cada media se construye desde las estadísticas que la producen (tiros × acierto por zona, % de los rebotes disponibles que captura, % de las canastas de sus compañeros que asiste...) y se muestra con esas estadísticas en sus últimos 5 y 10 partidos, la temporada y contra este rival. Todo queda guardado en la tabla `nba_analisis` de la base.

## Estado de calibración

**En calibración: todos los picks son de prueba.**  6 de 8 criterios cumplidos:

- ⬜ Días con picks liquidados: 10 de 21
- ⬜ Props de línea principal: muestra: 97 de 150
- ✅ Props de línea principal: aciertan lo prometido: acierto 70.1% vs prometido 67.1%
- ✅ Picks seguros: muestra: 713 de 150
- ✅ Picks seguros: aciertan lo prometido: acierto 89.8% vs prometido 86.9%
- ✅ Props con cuota: beneficio positivo: +0.30 u en 97
- ✅ Combinadas: muestra: 85 de 30
- ✅ Combinadas: ganan lo prometido: ganadas 32.9% vs prometido 29.5%

## Seguimiento: combinadas de prueba del 2026-11-05

Ganadas 1 de 3 liquidadas.

**Combinada segura A (alternas)** — ✅ GANADA (prob. 79%)
  - ✅ Dillon Brooks: más de 9.5 puntos → 24
  - ✅ Giannis Antetokounmpo: más de 1.5 asistencias → 4

**Bet builder (Miami Heat @ Golden State Warriors)** — ❌ perdida (prob. 38%)
  - ❌ Brandin Podziemski: más de 15.5 puntos → 9
  - ❌ Andrew Wiggins: más de 0.5 triples → 0
  - ✅ Davion Mitchell: más de 0.5 triples → 4
  - ✅ Yaxel Lendeborg: más de 0.5 triples → 1

**Tu apuesta: Agresiva doble bet builder 7.86** — ❌ perdida (prob. 13%, cuota 7.86)
  - ✅ Bam Adebayo: menos de 1.5 triples → 0
  - ❌ Brandin Podziemski: más de 16.5 puntos → 9
  - ✅ Miles Bridges: más de 1.5 triples → 3
  - ✅ Wendell Carter Jr.: más de 0.5 triples → 2

### Acumulado de las combinadas de prueba

| Tipo | Jugadas | Ganadas | % ganadas | Prob. prometida | Beneficio (1 u, con cuota) |
|---|---|---|---|---|---|
| Combinada segura A (alternas) | 9 | 6 | 67% | 70% | - |
| Bet builder | 20 | 6 | 30% | 36% | - |
| Segura cuota 10+ | 2 | 0 | 0% | 10% | -2.00 u en 2 |
| Segura cuota 15+ | 2 | 0 | 0% | 7% | -2.00 u en 2 |
| Segura cuota 2+ | 7 | 5 | 71% | 45% | +3.49 u en 7 |
| Segura cuota 3+ | 6 | 5 | 83% | 30% | +9.85 u en 6 |
| Segura cuota 5+ | 4 | 1 | 25% | 18% | +1.03 u en 4 |
| Doble de bet builders | 5 | 0 | 0% | 14% | - |
| Combinada segura B (principales) | 7 | 4 | 57% | 26% | +7.56 u en 7 |
| Rachas de temporada (4 patas) | 5 | 0 | 0% | 16% | -5.00 u en 5 |
| Rachas de temporada (8 patas) | 3 | 0 | 0% | 3% | -3.00 u en 3 |
| Tus apuestas | 13 | 0 | 0% | 8% | -13.00 u en 13 |
| De valor cuota 10+ | 4 | 0 | 0% | 13% | -4.00 u en 4 |
| De valor cuota 15+ | 3 | 1 | 33% | 9% | +12.17 u en 3 |
| De valor cuota 30+ | 2 | 0 | 0% | 5% | -2.00 u en 2 |
| De valor cuota 5+ | 6 | 0 | 0% | 22% | -6.00 u en 6 |

## Bet builders del día

Por partido, 4 "más de" de titulares estables sin alertas, en líneas un poco por debajo de su nivel (cada pierna ~72 %+). La probabilidad de acertar todas tiene en cuenta que los jugadores de un mismo partido se mueven algo juntos. **Cuota justa** = 1 / probabilidad (solo para saber cuánto debería pagar; se elige por probabilidad). Backtest 2025-26: prometían ~32 % y acertaron 38-40 % (conservador).

### Doble: Utah Jazz @ Dallas Mavericks + Philadelphia 76ers @ Cleveland Cavaliers

Probabilidad de acertar los dos bet builders: **13%** (1 de cada 8); cuota justa **7.53**.

**Utah Jazz @ Dallas Mavericks** — acertar las 4: **38%**, cuota justa 2.64

- P.J. Washington 12+ puntos (74%; esperado 16.6; últ. 10: 7/10)
- Darryn Peterson 3+ asistencias (76%; esperado 4.4; últ. 10: 6/8)
- Jaxson Hayes 4+ rebotes (78%; esperado 6.3; últ. 10: 8/10)
- Daniel Gafford 4+ rebotes (83%; esperado 6.7; últ. 10: 7/10)

**Philadelphia 76ers @ Cleveland Cavaliers** — acertar las 4: **35%**, cuota justa 2.85

- Jaylen Brown 3+ asistencias (76%; esperado 4.3; últ. 10: 7/10)
- Tyrese Maxey 4+ asistencias (77%; esperado 5.3; últ. 10: 10/10)
- VJ Edgecombe 2+ asistencias (82%; esperado 3.5; últ. 10: 9/10)
- Evan Mobley 1+ triples (73%; esperado 1.6; últ. 10: 9/10)

**Minnesota Timberwolves @ New Orleans Pelicans** — acertar las 4: **35%**, cuota justa 2.86

- Ayo Dosunmu 3+ asistencias (73%; esperado 4.7; últ. 10: 8/10)
- Zion Williamson 17+ puntos (76%; esperado 20.4; últ. 10: 8/10)
- Jeremiah Fears 2+ asistencias (79%; esperado 4.4; últ. 10: 8/10)
- Jaden McDaniels 14+ puntos (79%; esperado 17.9; últ. 10: 8/10)

**Washington Wizards @ Atlanta Hawks** — acertar las 4: **34%**, cuota justa 2.90

- CJ McCollum 2+ asistencias (75%; esperado 4.2; últ. 10: 7/10)
- Trae Young 15+ puntos (77%; esperado 19.5; últ. 10: 8/10)
- Kyshawn George 3+ asistencias (77%; esperado 4.8; últ. 10: 7/10)
- Nickeil Alexander-Walker 14+ puntos (77%; esperado 20.4; últ. 10: 7/10)

**Toronto Raptors @ Milwaukee Bucks** — acertar las 4: **32%**, cuota justa 3.13

- RJ Barrett 3+ asistencias (73%; esperado 3.8; últ. 10: 9/10)
- Ryan Rollins 9+ puntos (74%; esperado 12.0; últ. 10: 9/10)
- Jaime Jaquez Jr. 11+ puntos (75%; esperado 14.5; últ. 10: 8/10)
- Ja'Kobe Walter 8+ puntos (77%; esperado 12.1; últ. 10: 9/10)

**Oklahoma City Thunder @ Memphis Grizzlies** — acertar las 4: **30%**, cuota justa 3.28

- Cameron Boozer 3+ asistencias (73%; esperado 4.3; últ. 10: 8/8)
- Ty Jerome 17+ puntos (73%; esperado 23.0; últ. 10: 7/10)
- Ajay Mitchell 11+ puntos (74%; esperado 17.2; últ. 10: 6/10)
- Shai Gilgeous-Alexander 23+ puntos (74%; esperado 29.0; últ. 10: 7/10)

**San Antonio Spurs @ Sacramento Kings** — acertar las 4: **30%**, cuota justa 3.33

- Dylan Harper 16+ puntos (73%; esperado 19.7; últ. 10: 8/10)
- Domantas Sabonis 11+ puntos (73%; esperado 15.0; últ. 10: 8/10)
- Victor Wembanyama 21+ puntos (73%; esperado 28.3; últ. 10: 7/10)
- Stephon Castle 4+ asistencias (74%; esperado 5.5; últ. 10: 8/10)

**Boston Celtics @ Charlotte Hornets** — acertar las 4: **30%**, cuota justa 3.34

- Jayson Tatum 5+ asistencias (73%; esperado 6.3; últ. 10: 8/10)
- Brandon Miller 17+ puntos (73%; esperado 22.9; últ. 10: 7/10)
- Paul George 14+ puntos (73%; esperado 18.8; últ. 10: 9/10)
- Derrick White 9+ puntos (74%; esperado 13.3; últ. 10: 8/10)

## Combinada segura del día

**Opción A, líneas alternativas (la más segura):** el pick seguro más probable de cada partido, de titulares estables. Búscalas en las líneas alternativas de tu casa ("15+", "20+"...): cada una vale la pena si paga al menos su cuota mínima.

| Partido | Selección | Prob. | Cuota mínima | Esperado | Últ. 10 |
|---|---|---|---|---|---|
| Oklahoma City Thunder @ Memphis Grizzlies | **Cameron Boozer: más de 0.5 asistencias** | **92%** | 1.09 | 4.3 | 8/8 |
| Boston Celtics @ Charlotte Hornets | **Jayson Tatum: más de 2.5 asistencias** | **91%** | 1.10 | 6.3 | 10/10 |
| Utah Jazz @ Dallas Mavericks | **Keyonte George: más de 1.5 asistencias** | **90%** | 1.11 | 6.4 | 9/10 |
| Portland Trail Blazers @ Los Angeles Lakers | **Austin Reaves: más de 1.5 asistencias** | **90%** | 1.11 | 4.8 | 9/10 |

| Selecciones | Probabilidad de acertar todas |
|---|---|
| 2 | **83%** |
| 3 | **75%** |
| 4 | **68%** |

Hoy ninguna línea principal cumple los filtros de jugador constante.

## Picks seguros de titulares estables

Líneas bajas (alternativas) de titulares con 30+ minutos: mejor un "15+ puntos" casi seguro de una estrella que la línea normal de un suplente. En el backtest, elegidas al 85 % acertaron el 89-96 %. **Cuota mínima** = la que hace falta para que valga la pena (1 / probabilidad); búscala en las líneas alternativas de tu casa.

| Partido | Jugador | Pick seguro | Prob. | Cuota mínima | Esperado | Últ. 10 |
|---|---|---|---|---|---|---|
| Oklahoma City Thunder @ Memphis Grizzlies | Cameron Boozer | **más de 0.5 asistencias** | **92%** | 1.09 | 4.3 | 8/8 |
| Oklahoma City Thunder @ Memphis Grizzlies | Ty Jerome | **más de 1.5 asistencias** | **92%** | 1.09 | 5.0 | 10/10 |
| Boston Celtics @ Charlotte Hornets | Jayson Tatum | **más de 2.5 asistencias** | **91%** | 1.10 | 6.3 | 10/10 |
| Utah Jazz @ Dallas Mavericks | Keyonte George | **más de 1.5 asistencias** | **90%** | 1.11 | 6.4 | 9/10 |
| Portland Trail Blazers @ Los Angeles Lakers | Austin Reaves | **más de 1.5 asistencias** | **90%** | 1.11 | 4.8 | 9/10 |
| Washington Wizards @ Atlanta Hawks | Trae Young | **más de 4.5 asistencias** | **90%** | 1.11 | 8.9 | 10/10 |
| Utah Jazz @ Dallas Mavericks | Cooper Flagg | **más de 1.5 asistencias** | **90%** | 1.11 | 5.9 | 9/10 |
| Boston Celtics @ Charlotte Hornets | Naz Reid | **más de 3.5 rebotes** | **90%** | 1.11 | 8.0 | 10/10 |
| Toronto Raptors @ Milwaukee Bucks | Scottie Barnes | **más de 2.5 rebotes** | **90%** | 1.11 | 7.6 | 10/10 |
| Oklahoma City Thunder @ Memphis Grizzlies | Cameron Boozer | **más de 4.5 rebotes** | **90%** | 1.11 | 8.9 | 8/8 |
| Boston Celtics @ Charlotte Hornets | Moussa Diabate | **más de 4.5 rebotes** | **90%** | 1.12 | 8.9 | 10/10 |
| Philadelphia 76ers @ Cleveland Cavaliers | LeBron James | **más de 2.5 rebotes** | **89%** | 1.12 | 6.8 | 8/10 |
| Boston Celtics @ Charlotte Hornets | Jayson Tatum | **más de 2.5 rebotes** | **89%** | 1.12 | 7.0 | 10/10 |
| San Antonio Spurs @ Sacramento Kings | Domantas Sabonis | **más de 1.5 asistencias** | **89%** | 1.12 | 4.9 | 9/10 |
| Utah Jazz @ Dallas Mavericks | P.J. Washington | **más de 3.5 rebotes** | **89%** | 1.12 | 8.0 | 10/10 |

## Las más probables del día

| Partido | Prop | Prob. final | Modelo | Casa | Esperado | Últ. 10 | Temporada | vs este rival | Cuota (implícita) |
|---|---|---|---|---|---|---|---|---|---|
| Philadelphia 76ers @ Cleveland Cavaliers | **Kentavious Caldwell-Pope: menos de 1.5 triples** ⚠️ suplente | **67%** | 68% | 65% | 1.2 ± 1.1 | 8/10 | 7/9 | 1, 0 | 1.44 (70%) |

### En qué se basan las 10 más probables

#### Kentavious Caldwell-Pope: menos de 1.5 triples (67%) — Philadelphia 76ers @ Cleveland Cavaliers

**¿Por qué 1.2 triples?** (línea 1.5; 20.7 minutos esperados)

En corto:

- La pasó en 7 de 9 esta temporada (falló con 4, 2)
- Con 17+ minutos (hoy se esperan 21): 12 de 14 en sus últimos 15
- Contra las ~10 mejores defensas en triples a bases/escoltas: 14 de 17 (últimos 40 partidos)
- Contra defensas débiles como la de hoy y con 17+ minutos: 13 de 19, con 1.4 de media (últimos 60 partidos)
- El rival es #10 de 30 en triples que concede a bases/escoltas por minuto (#1 = el que más concede; +3% frente a la media)
- Su zona principal es triple frontal (38% de sus tiros, 32% de acierto); el rival es #6 de 30 en acierto que deja ahí (36%, liga 35%)
- Cómo tira (últimos 15): recibe y tira 39% (41% de acierto), creado 30% (39% de acierto), penetración 27% (48% de acierto); en recibe y tira el rival es #14 de 30 en lo que deja (#1 = el que más; 1.08 puntos por tiro frente a 1.06 de media)
- Oportunidades: 3.1 triples intentados esperados al 36%
- Minutos: 21 esperados (suplente, ±5)

Razonamiento (3 factores a favor, 2 en contra):

- ❌ Minutos: 20.7 esperados (suplente, ±5.0).
- ✅ Forma: 0.8 en sus últimos 5, 1.3 esta temporada (9 partidos), 1.1 la temporada pasada (línea 1.5).
- ➖ Cómo produce triples: 3.1 triples intentados (su ritmo 5.3 por 36'; el rival concede -0% de triples en su reparto) × 36% esperado.
- ❌ Defensa: el rival concede +3% de triples por minuto a bases/escoltas (defensa débil); ajuste aplicado +3%; en su zona principal (triple) el rival concede 36% (liga 35%).
- ➖ Ritmo del partido: +1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 1, 0 (2 de 2 a favor).
- ✅ Últimos 10: la habría pasado 8 de 10.
- ⚠️ cambio de rol esta temporada (por minuto): pts -35%, ast -54%; se da más peso a la línea de la casa.

- ⚠️ Alertas: suplente.
- Triples **1.2** (por componentes 1.1 · por tasa por minuto y defensa rival 1.2): 3.1 triples intentados (su ritmo 5.3 por 36'; el rival concede -0% de triples en su reparto) × 36% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 18.8 | 23.0 | 22.7 | 21.3 | 24.0 |
| Triples anotados | 0.8 | 1.3 | 1.3 | 1.1 | 0.5 |
| Triples intentados | 2.0 | 3.2 | 3.0 | 3.4 | 0.5 |
| % triples | 40.0% | 40.6% | 44.4% | 31.6% | 100.0% |


## Washington Wizards @ Atlanta Hawks

Diferencia esperada: Atlanta Hawks por 7.5.

Parte de lesiones: Jock Landale (Out); Reece Beekman (Out); Justin Champagnie (Out); Keshon Gilbert (Out); Jamir Watkins (Out); Jalen Johnson (Day-To-Day); Mouhamed Gueye (Out); Asa Newell (Out); Tristan Vukcevic (Out); Anthony Davis (Day-To-Day).

Sin líneas de props para este partido (o sin historial suficiente de los jugadores).

## Boston Celtics @ Charlotte Hornets

Diferencia esperada: Boston Celtics por 8.5.

Parte de lesiones: Dennis Schroder (Day-To-Day); Grant Williams (Out); Payton Pritchard (Day-To-Day); Devin Carter (Out); Moussa Diabate (Day-To-Day); Kon Knueppel (Out).

Sin líneas de props para este partido (o sin historial suficiente de los jugadores).

## Philadelphia 76ers @ Cleveland Cavaliers

Diferencia esperada: Philadelphia 76ers por 2.5.

Parte de lesiones: Jarrett Allen (Day-To-Day); Peyton Watson (Day-To-Day); Jaylon Tyson (Out); Dominick Barlow (Out); Ariel Hukporti (Out); Tyrese Proctor (Day-To-Day); Adem Bona (Day-To-Day).

Ventajas del partido (los dos lados): puntos esperados frente a su media de los últimos 10, ajuste por la defensa rival y diferencia de estatura con los rivales de su posición.

| Equipo | Jugador | Puntos esperados | Su media (últ. 10) | Defensa rival en puntos | Rebotes esperados | Altura vs rival |
|---|---|---|---|---|---|---|
| PHI | Tyrese Maxey | 25.0 | 26.9 | -1% | 3.7 | -2.2" |
| PHI | Jaylen Brown | 22.7 | 22.5 | -1% | 6.3 | +1.8" |
| PHI | VJ Edgecombe | 14.2 | 11.9 | -1% | 6.0 | +0.8" |
| CLE | James Harden | 17.4 | 16.3 | -2% | 5.1 | +0.7" |
| PHI | LeBron James | 18.1 | 17.6 | +1% | 6.8 | +0.9" |
| CLE | Donovan Mitchell | 21.5 | 23.7 | -2% | 4.8 | -2.3" |
| PHI | Joel Embiid | 20.7 | 19.3 | -2% | 9.4 | +1.9" |
| CLE | Evan Mobley | 17.4 | 17.9 | -1% | 8.7 | -0.3" |
| CLE | Peyton Watson | 12.3 | 10.9 | -2% | 4.1 | +3.7" |
| CLE | Sam Merrill | 9.9 | 7.8 | -2% | 3.2 | -0.3" |

Picks seguros de titulares estables:

| Jugador | Pick seguro | Prob. | Cuota mínima | Esperado | Últ. 10 |
|---|---|---|---|---|---|
| LeBron James | **más de 2.5 rebotes** | **89%** | 1.12 | 6.8 | 8/10 |
| Joel Embiid | **más de 4.5 rebotes** | **89%** | 1.13 | 9.4 | 9/10 |
| Evan Mobley | **más de 4.5 rebotes** | **88%** | 1.13 | 8.7 | 9/10 |
| LeBron James | **más de 11.5 puntos** | **88%** | 1.14 | 18.1 | 10/10 |
| James Harden | **más de 2.5 asistencias** | **88%** | 1.14 | 5.9 | 8/10 |
| Donovan Mitchell | **más de 13.5 puntos** | **87%** | 1.14 | 21.5 | 10/10 |

Las 8 más probables (máximo 2 por jugador: las de un mismo jugador suelen ganar o perder juntas).

| Prop | Prob. final | Modelo | Casa | Esperado | Últ. 10 | Temporada | vs este rival | Cuota (implícita) |
|---|---|---|---|---|---|---|---|---|
| **Kentavious Caldwell-Pope: menos de 1.5 triples** ⚠️ suplente | **67%** | 68% | 65% | 1.2 ± 1.1 | 8/10 | 7/9 | 1, 0 | 1.44 (70%) |
| **LeBron James: menos de 1.5 triples** | **65%** | 62% | 67% | 1.2 ± 1.1 | 6/10 | 5/7 | 1, 1, 0 | 1.41 (71%) |
| **Peyton Watson: menos de 1.5 triples** | **65%** | 67% | 63% | 1.1 ± 1.2 | 7/10 | 5/6 | 0, 2 | 1.49 (67%) |
| **Kentavious Caldwell-Pope: más de 1.5 rebotes** ⚠️ suplente | **63%** | 65% | 61% | 2.2 ± 1.6 | 8/10 | 7/9 | 3, 0 | 1.54 (65%) |
| **Peyton Watson: más de 1.5 asistencias** | **62%** | 69% | 58% | 2.5 ± 1.9 | 8/10 | 5/6 | 2, 4 | 1.61 (62%) |
| **Evan Mobley: menos de 1.5 triples** | **60%** | 55% | 64% | 1.6 ± 1.6 | 5/10 | 4/8 | 1, 0, 1, 1, 3 | 1.48 (68%) |
| **Donovan Mitchell: menos de 5.5 asistencias** | **59%** | 63% | 56% | 4.8 ± 2.6 | 6/10 | 4/8 | 3, 6, 12, 9, 8 | 1.68 (60%) |
| **VJ Edgecombe: más de 2.5 asistencias** | **59%** | 64% | 55% | 3.5 ± 2.0 | 6/10 | 4/8 | 6, 4, 2, 4 | 1.71 (58%) |

### Fichas de los jugadores destacados

#### Kentavious Caldwell-Pope (bases/escoltas) vs Cleveland Cavaliers

- Minutos esperados: **20.7** (± 5.0); 60 partidos en la base.
- cambio de rol esta temporada (por minuto): pts -35%, ast -54%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Kentavious Caldwell-Pope: menos de 1.5 triples** (67%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Cleveland Cavaliers contra bases/escoltas en triples: +3% respecto a la media; ajuste por su historial contra defensas similares: +3%.

**¿Por qué 1.2 triples?** (línea 1.5; 20.7 minutos esperados)

En corto:

- La pasó en 7 de 9 esta temporada (falló con 4, 2)
- Con 17+ minutos (hoy se esperan 21): 12 de 14 en sus últimos 15
- Contra las ~10 mejores defensas en triples a bases/escoltas: 14 de 17 (últimos 40 partidos)
- Contra defensas débiles como la de hoy y con 17+ minutos: 13 de 19, con 1.4 de media (últimos 60 partidos)
- El rival es #10 de 30 en triples que concede a bases/escoltas por minuto (#1 = el que más concede; +3% frente a la media)
- Su zona principal es triple frontal (38% de sus tiros, 32% de acierto); el rival es #6 de 30 en acierto que deja ahí (36%, liga 35%)
- Cómo tira (últimos 15): recibe y tira 39% (41% de acierto), creado 30% (39% de acierto), penetración 27% (48% de acierto); en recibe y tira el rival es #14 de 30 en lo que deja (#1 = el que más; 1.08 puntos por tiro frente a 1.06 de media)
- Oportunidades: 3.1 triples intentados esperados al 36%
- Minutos: 21 esperados (suplente, ±5)

Razonamiento (3 factores a favor, 2 en contra):

- ❌ Minutos: 20.7 esperados (suplente, ±5.0).
- ✅ Forma: 0.8 en sus últimos 5, 1.3 esta temporada (9 partidos), 1.1 la temporada pasada (línea 1.5).
- ➖ Cómo produce triples: 3.1 triples intentados (su ritmo 5.3 por 36'; el rival concede -0% de triples en su reparto) × 36% esperado.
- ❌ Defensa: el rival concede +3% de triples por minuto a bases/escoltas (defensa débil); ajuste aplicado +3%; en su zona principal (triple) el rival concede 36% (liga 35%).
- ➖ Ritmo del partido: +1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 1, 0 (2 de 2 a favor).
- ✅ Últimos 10: la habría pasado 8 de 10.
- ⚠️ cambio de rol esta temporada (por minuto): pts -35%, ast -54%; se da más peso a la línea de la casa.

- ⚠️ Alertas: suplente.
- Triples **1.2** (por componentes 1.1 · por tasa por minuto y defensa rival 1.2): 3.1 triples intentados (su ritmo 5.3 por 36'; el rival concede -0% de triples en su reparto) × 36% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 18.8 | 23.0 | 22.7 | 21.3 | 24.0 |
| Triples anotados | 0.8 | 1.3 | 1.3 | 1.1 | 0.5 |
| Triples intentados | 2.0 | 3.2 | 3.0 | 3.4 | 0.5 |
| % triples | 40.0% | 40.6% | 44.4% | 31.6% | 100.0% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -24%, vs defensa media +19%, vs defensa débil +6%; rebotes: vs defensa fuerte -3%, vs defensa media +22%, vs defensa débil -13%; asistencias: vs defensa fuerte -11%, vs defensa media +17%, vs defensa débil +1%; triples: vs defensa fuerte -25%, vs defensa media +15%, vs defensa débil +16%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 38% | 32% | 35% | 36% |
| media distancia | 20% | 45% | 41% | 41% |
| pintura | 17% | 43% | 45% | 43% |
| triple de esquina | 13% | 41% | 38% | 39% |
| bajo el aro | 12% | 64% | 68% | 64% |

#### LeBron James (aleros/ala-pívots) vs Cleveland Cavaliers

- Minutos esperados: **32.9** (± 3.0); 80 partidos en la base.
- cambio de rol esta temporada (por minuto): tpm -36%; se da más peso a la línea de la casa
- Su prop más probable hoy: **LeBron James: menos de 1.5 triples** (65%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Cleveland Cavaliers contra aleros/ala-pívots en triples: +4% respecto a la media; ajuste por su historial contra defensas similares: -3%.

**¿Por qué 1.2 triples?** (línea 1.5; 32.9 minutos esperados)

En corto:

- La pasó en 5 de 7 esta temporada (falló con 2, 2)
- Contra las ~10 mejores defensas en triples a aleros/ala-pívots: 8 de 16 (últimos 40 partidos)
- Contra defensas débiles como la de hoy y con 29+ minutos: 10 de 17, con 1.3 de media (últimos 60 partidos)
- El rival es #8 de 30 en triples que concede a aleros/ala-pívots por minuto (#1 = el que más concede; +5% frente a la media)
- Su zona principal es triple frontal (22% de sus tiros, 33% de acierto); el rival es #6 de 30 en acierto que deja ahí (36%, liga 35%)
- Cómo tira (últimos 15): penetración 36% (59% de acierto), recibe y tira 21% (27% de acierto), creado 20% (41% de acierto); en penetración el rival es #13 de 30 en lo que deja (#1 = el que más; 1.07 puntos por tiro frente a 1.08 de media)
- Oportunidades: 3.9 triples intentados esperados al 34%
- Minutos: 33 esperados (titular, ±3)

Razonamiento (3 factores a favor, 1 en contra):

- ✅ Minutos: 32.9 esperados (titular, ±3.0).
- ✅ Forma: 1.0 en sus últimos 5, 0.9 esta temporada (7 partidos), 1.3 la temporada pasada (línea 1.5).
- ➖ Cómo produce triples: 3.9 triples intentados (su ritmo 4.2 por 36'; el rival concede -0% de triples en su reparto) × 34% esperado.
- ❌ Defensa: el rival concede +5% de triples por minuto a aleros/ala-pívots (defensa débil); ajuste aplicado +4%; en su zona principal (triple) el rival concede 36% (liga 35%).
- ➖ Ritmo del partido: +1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 1, 1, 0 (3 de 3 a favor).
- ➖ Últimos 10: la habría pasado 6 de 10.
- ⚠️ cambio de rol esta temporada (por minuto): tpm -36%; se da más peso a la línea de la casa.

- ⚠️ Alertas: cambio de rol.
- Triples **1.2** (por componentes 1.3 · por tasa por minuto y defensa rival 1.2): 3.9 triples intentados (su ritmo 4.2 por 36'; el rival concede -0% de triples en su reparto) × 34% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 32.8 | 34.6 | 33.0 | 32.8 | 30.3 |
| Triples anotados | 1.0 | 1.1 | 0.9 | 1.3 | 0.7 |
| Triples intentados | 3.2 | 3.9 | 3.3 | 4.1 | 3.3 |
| % triples | 31.2% | 28.2% | 26.1% | 32.1% | 20.0% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -3%, vs defensa media +5%, vs defensa débil +2%; rebotes: vs defensa fuerte -12%, vs defensa media +3%, vs defensa débil +12%; asistencias: vs defensa fuerte -13%, vs defensa media +5%, vs defensa débil +12%; triples: vs defensa fuerte +10%, vs defensa media -11%, vs defensa débil -5%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 35% | 73% | 68% | 64% |
| pintura | 23% | 41% | 45% | 43% |
| triple frontal | 22% | 33% | 35% | 36% |
| media distancia | 16% | 42% | 41% | 41% |
| triple de esquina | 5% | 30% | 38% | 39% |

#### Peyton Watson (bases/escoltas) vs Philadelphia 76ers

- Minutos esperados: **26.5** (± 5.6); 60 partidos en la base.
- en el parte de lesiones: day-to-day
- cambio de rol esta temporada (por minuto): ast +52%, tpm -54%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Peyton Watson: menos de 1.5 triples** (65%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Philadelphia 76ers contra bases/escoltas en triples: -3% respecto a la media; ajuste por su historial contra defensas similares: -9%.

**¿Por qué 1.1 triples?** (línea 1.5; 26.5 minutos esperados)

En corto:

- La pasó en 5 de 6 esta temporada; los fallos, en partidos raros (6 faltas)
- Con 23+ minutos (hoy se esperan 27): 5 de 9 en sus últimos 15
- Contra las ~10 mejores defensas en triples a bases/escoltas: 14 de 18 (últimos 40 partidos)
- Contra defensas fuertes como la de hoy y con 23+ minutos: 17 de 22, con 0.9 de media (últimos 60 partidos)
- El rival es #21 de 30 en triples que concede a bases/escoltas por minuto (#1 = el que más concede; -4% frente a la media)
- Su zona principal es triple frontal (20% de sus tiros, 32% de acierto); el rival es #21 de 30 en acierto que deja ahí (34%, liga 35%)
- Cómo tira (últimos 15): penetración 36% (52% de acierto), recibe y tira 33% (29% de acierto), creado 15% (38% de acierto); en penetración el rival es #9 de 30 en lo que deja (#1 = el que más; 1.11 puntos por tiro frente a 1.08 de media)
- Oportunidades: 4.0 triples intentados esperados al 35%
- Minutos: 27 esperados (titular, ±6)

Razonamiento (4 factores a favor, 1 en contra):

- ✅ Minutos: 26.5 esperados (titular, ±5.6).
- ✅ Forma: 0.8 en sus últimos 5, 0.7 esta temporada (6 partidos), 1.5 la temporada pasada (línea 1.5).
- ➖ Cómo produce triples: 4.0 triples intentados (su ritmo 5.3 por 36'; el rival concede +2% de triples en su reparto) × 35% esperado.
- ✅ Defensa: el rival concede -4% de triples por minuto a bases/escoltas (defensa fuerte); ajuste aplicado -3%; en su zona principal (triple) el rival concede 34% (liga 35%).
- ❌ Altura: mide 6'8", 3.7 pulgadas más que los bases/escoltas del rival (+1.3% en esta estadística).
- ➖ Ritmo del partido: +1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ➖ Contra este rival: 0, 2 (1 de 2 a favor).
- ✅ Últimos 10: la habría pasado 7 de 10.
- ⚠️ en el parte de lesiones: day-to-day.
- ⚠️ cambio de rol esta temporada (por minuto): ast +52%, tpm -54%; se da más peso a la línea de la casa.

- ⚠️ Alertas: cambio de rol, en el parte de lesiones.
- Triples **1.1** (por componentes 1.4 · por tasa por minuto y defensa rival 1.0): 4.0 triples intentados (su ritmo 5.3 por 36'; el rival concede +2% de triples en su reparto) × 35% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 28.0 | 24.5 | 28.3 | 29.6 | 37.0 |
| Triples anotados | 0.8 | 0.9 | 0.7 | 1.5 | 1.0 |
| Triples intentados | 4.2 | 3.6 | 4.0 | 3.6 | 3.0 |
| % triples | 19.0% | 25.0% | 16.7% | 41.1% | 33.3% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -0%, vs defensa media -1%, vs defensa débil +1%; rebotes: vs defensa fuerte +7%, vs defensa media -4%, vs defensa débil -2%; asistencias: vs defensa fuerte -31%, vs defensa media -1%, vs defensa débil +24%; triples: vs defensa fuerte -42%, vs defensa media +32%, vs defensa débil +31%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 30% | 64% | 68% | 68% |
| pintura | 25% | 45% | 45% | 42% |
| triple frontal | 20% | 32% | 35% | 34% |
| triple de esquina | 14% | 42% | 38% | 37% |
| media distancia | 10% | 40% | 41% | 39% |

#### Evan Mobley (pívots) vs Philadelphia 76ers

- Minutos esperados: **32.3** (± 3.4); 88 partidos en la base.
- cambio de rol esta temporada (por minuto): tpm +105%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Evan Mobley: menos de 1.5 triples** (60%). Con 80% de probabilidad: más de - / menos de 3.5.
- Defensa de Philadelphia 76ers contra pívots en triples: +7% respecto a la media; ajuste por su historial contra defensas similares: +8%.

**¿Por qué 1.6 triples?** (línea 1.5; 32.3 minutos esperados)

En corto:

- La pasó en 4 de 8 esta temporada (falló con 3, 5, 4, 2)
- Con 28+ minutos (hoy se esperan 32): 8 de 14 en sus últimos 15
- Contra las ~10 mejores defensas en triples a pívots: 17 de 24 (últimos 40 partidos)
- Contra defensas débiles como la de hoy y con 28+ minutos: 8 de 12, con 1.5 de media (últimos 60 partidos)
- El rival es #5 de 30 en triples que concede a pívots por minuto (#1 = el que más concede; +17% frente a la media)
- Su zona principal es triple frontal (23% de sus tiros, 34% de acierto); el rival es #21 de 30 en acierto que deja ahí (34%, liga 35%)
- Cómo tira (últimos 15): recibe y tira 32% (43% de acierto), penetración 20% (61% de acierto), corte 17% (90% de acierto); en recibe y tira el rival es #26 de 30 en lo que deja (#1 = el que más; 0.98 puntos por tiro frente a 1.06 de media)
- Oportunidades: 3.7 triples intentados esperados al 34%
- Minutos: 32 esperados (titular, ±3)

Razonamiento (2 factores a favor, 2 en contra):

- ✅ Minutos: 32.3 esperados (titular, ±3.4).
- ❌ Forma: 2.0 en sus últimos 5, 2.1 esta temporada (8 partidos), 0.8 la temporada pasada (línea 1.5).
- ➖ Cómo produce triples: 3.7 triples intentados (su ritmo 4.0 por 36'; el rival concede +2% de triples en su reparto) × 34% esperado.
- ❌ Defensa: el rival concede +17% de triples por minuto a pívots (defensa débil); ajuste aplicado +7%; en su zona principal (triple) el rival concede 34% (liga 35%).
- ➖ Ritmo del partido: +1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 1, 0, 1, 1, 3 (4 de 5 a favor).
- ➖ Últimos 10: la habría pasado 5 de 10.
- ⚠️ cambio de rol esta temporada (por minuto): tpm +105%; se da más peso a la línea de la casa.

- ⚠️ Alertas: cambio de rol, falla en partidos normales (3 de 8 esta temporada).
- Triples **1.6** (por componentes 1.2 · por tasa por minuto y defensa rival 1.8): 3.7 triples intentados (su ritmo 4.0 por 36'; el rival concede +2% de triples en su reparto) × 34% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 31.2 | 33.3 | 32.9 | 32.5 | 33.2 |
| Triples anotados | 2.0 | 2.0 | 2.1 | 1.0 | 1.2 |
| Triples intentados | 4.6 | 4.2 | 4.4 | 3.3 | 3.2 |
| % triples | 43.5% | 47.6% | 48.6% | 30.7% | 37.5% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -9%, vs defensa media +6%, vs defensa débil +11%; rebotes: vs defensa fuerte -6%, vs defensa media +1%, vs defensa débil +8%; asistencias: vs defensa fuerte -8%, vs defensa media +2%, vs defensa débil +13%; triples: vs defensa fuerte -11%, vs defensa media -17%, vs defensa débil +35%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 43% | 76% | 68% | 68% |
| pintura | 25% | 42% | 45% | 42% |
| triple frontal | 23% | 34% | 35% | 34% |
| media distancia | 5% | 45% | 41% | 39% |
| triple de esquina | 4% | 37% | 38% | 37% |

#### Donovan Mitchell (bases/escoltas) vs Philadelphia 76ers

- Minutos esperados: **32.6** (± 4.1); 96 partidos en la base.
- Su prop más probable hoy: **Donovan Mitchell: menos de 5.5 asistencias** (59%). Con 80% de probabilidad: más de 2.5 / menos de 7.5.
- Defensa de Philadelphia 76ers contra bases/escoltas en asistencias: +0% respecto a la media; ajuste por su historial contra defensas similares: -2%.

**¿Por qué 4.8 asistencias?** (línea 5.5; 32.6 minutos esperados)

En corto:

- La pasó en 4 de 8 esta temporada (falló con 6, 11, 7, 7)
- Con 29+ minutos (hoy se esperan 33): 9 de 14 en sus últimos 15
- Contra las ~10 mejores defensas en asistencias a bases/escoltas: 19 de 23 (últimos 40 partidos)
- Contra defensas medias como la de hoy y con 29+ minutos: 5 de 12, con 6.2 de media (últimos 60 partidos)
- El rival es #15 de 30 en asistencias que concede a bases/escoltas por minuto (#1 = el que más concede; +0% frente a la media)
- Asistencias esperadas: 4.7 por partido si sus compañeros metieran lo normal (tiene 4.6; con él en pista metieron el 98% de lo esperado por tipo de tiro, últimos 10); ajuste aplicado +1.3%
- Oportunidades: asiste el 22% de las canastas de sus compañeros con él en pista
- Minutos: 33 esperados (titular, ±4)

Razonamiento (1 factores a favor, 2 en contra):

- ✅ Minutos: 32.6 esperados (titular, ±4.1).
- ❌ Forma: 6.0 en sus últimos 5, 5.5 esta temporada (8 partidos), 4.9 la temporada pasada (línea 5.5).
- ➖ Cómo produce asistencias: asiste el 21.7% de las canastas de sus compañeros en pista × 20.8 canastas de compañeros esperadas (su equipo 41.4 por 48' contra esta defensa).
- ➖ Defensa: el rival concede +0% de asistencias por minuto a bases/escoltas (defensa media); ajuste aplicado +0%.
- ➖ Ritmo del partido: +1% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ❌ Contra este rival: 3, 6, 12, 9, 8 (1 de 5 a favor).
- ➖ Últimos 10: la habría pasado 6 de 10.

- ⚠️ Alertas: falla en partidos normales (3 de 8 esta temporada).
- Asistencias **4.8** (por componentes 4.5 · por tasa por minuto y defensa rival 4.9): asiste el 21.7% de las canastas de sus compañeros en pista × 20.8 canastas de compañeros esperadas (su equipo 41.4 por 48' contra esta defensa).

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 31.4 | 33.6 | 33.1 | 32.9 | 34.6 |
| Asistencias | 6.0 | 4.6 | 5.5 | 5.1 | 7.6 |
| % de las canastas de compañeros que asiste | 26.1% | 21.0% | 23.8% | 22.9% | 30.1% |
| Pérdidas por jugada | 12.7% | 13.2% | 14.2% | 10.9% | 11.9% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -4%, vs defensa media +9%, vs defensa débil -2%; rebotes: vs defensa fuerte -6%, vs defensa media -11%, vs defensa débil +16%; asistencias: vs defensa fuerte -8%, vs defensa media +9%, vs defensa débil +5%; triples: vs defensa fuerte -4%, vs defensa media +11%, vs defensa débil -7%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 38% | 37% | 35% | 34% |
| pintura | 24% | 52% | 45% | 42% |
| bajo el aro | 22% | 65% | 68% | 68% |
| media distancia | 11% | 47% | 41% | 39% |
| triple de esquina | 5% | 35% | 38% | 37% |

## Utah Jazz @ Dallas Mavericks

Diferencia esperada: Dallas Mavericks por 7.5.

Parte de lesiones: Jusuf Nurkic (Out); Jaren Jackson Jr. (Out); Max Christie (Day-To-Day); Trey Alexander (Out); Santi Aldama (Out); Dereck Lively II (Out); Tarik Biberovic (Out); Sergio de Larrea (Out).

Sin líneas de props para este partido (o sin historial suficiente de los jugadores).

## Oklahoma City Thunder @ Memphis Grizzlies

Diferencia esperada: Oklahoma City Thunder por 3.5.

Parte de lesiones: Scotty Pippen Jr. (Out); Isaiah Stewart (Out); Jaylin Williams (Out); Chet Holmgren (Out); Cason Wallace (Out); Thomas Sorber (Out); Nikola Topic (Out).

Sin líneas de props para este partido (o sin historial suficiente de los jugadores).

## Toronto Raptors @ Milwaukee Bucks

Diferencia esperada: Toronto Raptors por 6.5.

Parte de lesiones: Nate Bittle (Out); Scottie Barnes (Day-To-Day); Kam Jones (Out); Kawhi Leonard (Out).

Sin líneas de props para este partido (o sin historial suficiente de los jugadores).

## Minnesota Timberwolves @ New Orleans Pelicans

Diferencia esperada: Minnesota Timberwolves por 4.5.

Parte de lesiones: Donte DiVincenzo (Out); Trey Murphy III (Day-To-Day); Terrence Shannon Jr. (Day-To-Day); Anthony Edwards (Out); Yves Missi (Out).

Sin líneas de props para este partido (o sin historial suficiente de los jugadores).

## Portland Trail Blazers @ Los Angeles Lakers

Diferencia esperada: Los Angeles Lakers por 2.5.

Parte de lesiones: Sandro Mamukelashvili (Day-To-Day); Ja Morant (Out); Vit Krejci (Out); Shaedon Sharpe (Out).

Ventajas del partido (los dos lados): puntos esperados frente a su media de los últimos 10, ajuste por la defensa rival y diferencia de estatura con los rivales de su posición.

| Equipo | Jugador | Puntos esperados | Su media (últ. 10) | Defensa rival en puntos | Rebotes esperados | Altura vs rival |
|---|---|---|---|---|---|---|
| LAL | Austin Reaves | 22.1 | 23.7 | +0% | 3.7 | +1.1" |
| LAL | Luka Doncic | 33.6 | 36.2 | +0% | 7.2 | +4.1" |
| POR | Deni Avdija | 22.6 | 23.1 | +0% | 6.1 | -0.3" |
| LAL | Walker Kessler | 14.7 | 13.4 | +4% | 10.3 | +2.2" |
| POR | Toumani Camara | 12.6 | 11.3 | -0% | 3.8 | -1.3" |
| POR | Jrue Holiday | 13.4 | 15.1 | +0% | 3.9 | -1.1" |
| POR | Donovan Clingan | 12.3 | 10.6 | +1% | 9.9 | +0.3" |
| LAL | Quentin Grimes | 9.6 | 8.0 | -0% | 2.9 | +0.1" |
| LAL | Ziaire Williams | 10.7 | 11.7 | -2% | 3.1 | +1.5" |
| POR | Scoot Henderson | 11.0 | 8.7 | +0% | 2.2 | -2.1" |

Picks seguros de titulares estables:

| Jugador | Pick seguro | Prob. | Cuota mínima | Esperado | Últ. 10 |
|---|---|---|---|---|---|
| Austin Reaves | **más de 1.5 asistencias** | **90%** | 1.11 | 4.8 | 9/10 |
| Luka Doncic | **más de 3.5 rebotes** | **88%** | 1.13 | 7.2 | 10/10 |
| Austin Reaves | **más de 14.5 puntos** | **88%** | 1.14 | 22.1 | 10/10 |
| Deni Avdija | **más de 15.5 puntos** | **88%** | 1.14 | 22.6 | 10/10 |
| Deni Avdija | **más de 25.5 pts+reb+ast** | **87%** | 1.15 | 34.4 | 10/10 |
| Austin Reaves | **más de 21.5 pts+reb+ast** | **87%** | 1.15 | 30.7 | 10/10 |

Las 8 más probables (máximo 2 por jugador: las de un mismo jugador suelen ganar o perder juntas).

| Prop | Prob. final | Modelo | Casa | Esperado | Últ. 10 | Temporada | vs este rival | Cuota (implícita) |
|---|---|---|---|---|---|---|---|---|
| **Sandro Mamukelashvili: más de 0.5 triples** ⚠️ suplente | **65%** | 63% | 66% | 1.2 ± 1.1 | 5/10 | 5/9 | 3, 3, 0 | 1.42 (70%) |
| **Jrue Holiday: más de 1.5 triples** ⚠️ suplente | **63%** | 65% | 62% | 2.3 ± 1.5 | 8/10 | 6/7 | 2, 1, 0, 4 | 1.53 (65%) |
| **Donovan Clingan: más de 0.5 triples** | **62%** | 60% | 63% | 0.9 ± 1.0 | 8/10 | 5/7 | 2, 1, 0, 0 | 1.49 (67%) |
| **Quentin Grimes: más de 0.5 triples** ⚠️ suplente | **62%** | 58% | 64% | 1.0 ± 1.1 | 5/10 | 4/9 | 0, 1 | 1.47 (68%) |
| **Matisse Thybulle: menos de 2.5 rebotes** | **61%** | 68% | 57% | 2.0 ± 1.4 | 8/10 | 7/9 | 2 | 1.64 (61%) |
| **Austin Reaves: menos de 2.5 triples** | **61%** | 61% | 61% | 2.2 ± 1.5 | 5/10 | 5/9 | 4, 3 | 1.54 (65%) |
| **Ziaire Williams: más de 7.5 puntos** | **60%** | 75% | 50% | 10.7 ± 4.4 | 10/10 | 6/6 | 11, 16, 7 | 1.90 (53%) |
| **Ziaire Williams: menos de 1.5 triples** | **60%** | 58% | 62% | 1.5 ± 1.3 | 7/10 | 3/6 | 2, 1, 1 | 1.52 (66%) |

### Fichas de los jugadores destacados

#### Sandro Mamukelashvili (aleros/ala-pívots) vs Portland Trail Blazers

- Minutos esperados: **23.4** (± 3.9); 96 partidos en la base.
- en el parte de lesiones: day-to-day
- cambio de rol esta temporada (por minuto): tpm -34%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Sandro Mamukelashvili: más de 0.5 triples** (65%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Portland Trail Blazers contra aleros/ala-pívots en triples: -4% respecto a la media; ajuste por su historial contra defensas similares: -2%.

**¿Por qué 1.2 triples?** (línea 0.5; 23.4 minutos esperados)

En corto:

- La pasó en 5 de 9 esta temporada (falló con 0, 0, 0, 0)
- Con 19+ minutos (hoy se esperan 23): 6 de 9 en sus últimos 15
- Contra las ~10 mejores defensas en triples a aleros/ala-pívots: 9 de 14 (últimos 40 partidos)
- Contra defensas fuertes como la de hoy y con 19+ minutos: 8 de 14, con 1.3 de media (últimos 60 partidos)
- El rival es #25 de 30 en triples que concede a aleros/ala-pívots por minuto (#1 = el que más concede; -7% frente a la media)
- Su zona principal es triple frontal (37% de sus tiros, 37% de acierto); el rival es #14 de 30 en acierto que deja ahí (35%, liga 35%)
- Cómo tira (últimos 15): recibe y tira 38% (28% de acierto), penetración 33% (81% de acierto), creado 8% (25% de acierto); en recibe y tira el rival es #23 de 30 en lo que deja (#1 = el que más; 1.00 puntos por tiro frente a 1.06 de media)
- Oportunidades: 3.3 triples intentados esperados al 37%
- El rival no tiene a Ja Morant (1.3 triples por partido)
- Minutos: 23 esperados (suplente, ±4)

Razonamiento (4 factores a favor, 2 en contra):

- ❌ Minutos: 23.4 esperados (suplente, ±3.9).
- ✅ Forma: 0.8 en sus últimos 5, 1.0 esta temporada (9 partidos), 1.5 la temporada pasada (línea 0.5).
- ➖ Cómo produce triples: 3.3 triples intentados (su ritmo 5.4 por 36'; el rival concede -6% de triples en su reparto) × 37% esperado.
- ❌ Defensa: el rival concede -7% de triples por minuto a aleros/ala-pívots (defensa fuerte); ajuste aplicado -4%; en su zona principal (triple) el rival concede 35% (liga 35%).
- ✅ Altura: mide 6'9", 1.5 pulgadas más que los aleros/ala-pívots del rival (+0.5% en esta estadística).
- ➖ Ritmo del partido: -0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 3, 3, 0 (2 de 3 a favor).
- ➖ Últimos 10: la habría pasado 5 de 10.
- ✅ Bajas del rival: sin Ja Morant (titular); +1.7% en esta estadística.
- ⚠️ en el parte de lesiones: day-to-day.
- ⚠️ cambio de rol esta temporada (por minuto): tpm -34%; se da más peso a la línea de la casa.

- ⚠️ Alertas: suplente, cambio de rol, en el parte de lesiones.
- Triples **1.2** (por componentes 1.2 · por tasa por minuto y defensa rival 1.1): 3.3 triples intentados (su ritmo 5.4 por 36'; el rival concede -6% de triples en su reparto) × 37% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 24.2 | 22.1 | 23.6 | 21.3 | 26.0 |
| Triples anotados | 0.8 | 0.9 | 1.0 | 1.4 | 2.0 |
| Triples intentados | 4.0 | 3.1 | 3.2 | 3.6 | 3.7 |
| % triples | 20.0% | 29.0% | 31.0% | 38.4% | 54.5% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -6%, vs defensa media +1%, vs defensa débil +6%; rebotes: vs defensa fuerte -5%, vs defensa media +7%, vs defensa débil -1%; asistencias: vs defensa fuerte -15%, vs defensa media +24%, vs defensa débil -3%; triples: vs defensa fuerte -17%, vs defensa media +6%, vs defensa débil +10%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 37% | 37% | 35% | 35% |
| bajo el aro | 35% | 69% | 68% | 66% |
| pintura | 17% | 50% | 45% | 46% |
| triple de esquina | 9% | 36% | 38% | 38% |
| media distancia | 2% | 40% | 41% | 42% |

#### Jrue Holiday (bases/escoltas) vs Los Angeles Lakers

- Minutos esperados: **26.9** (± 3.8); 66 partidos en la base.
- Ja Morant ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Su prop más probable hoy: **Jrue Holiday: más de 1.5 triples** (63%). Con 80% de probabilidad: más de 0.5 / menos de 3.5.
- Defensa de Los Angeles Lakers contra bases/escoltas en triples: -1% respecto a la media; ajuste por su historial contra defensas similares: +1%.

**¿Por qué 2.3 triples?** (línea 1.5; 26.9 minutos esperados)

En corto:

- La pasó en 6 de 7 esta temporada; los fallos, en partidos raros (paliza de 41)
- Con 23+ minutos (hoy se esperan 27): 10 de 13 en sus últimos 15
- Contra las ~10 mejores defensas en triples a bases/escoltas: 9 de 15 (últimos 40 partidos)
- Contra defensas medias como la de hoy y con 23+ minutos: 10 de 16, con 2.2 de media (últimos 60 partidos)
- El rival es #17 de 30 en triples que concede a bases/escoltas por minuto (#1 = el que más concede; -1% frente a la media)
- Su zona principal es triple frontal (44% de sus tiros, 36% de acierto); el rival es #16 de 30 en acierto que deja ahí (34%, liga 35%)
- Cómo tira (últimos 15): creado 44% (42% de acierto), penetración 25% (54% de acierto), recibe y tira 21% (38% de acierto); en creado el rival es #20 de 30 en lo que deja (#1 = el que más; 0.90 puntos por tiro frente a 0.91 de media)
- Oportunidades: 5.7 triples intentados esperados al 37%
- Minutos: 27 esperados (suplente, ±4)

Razonamiento (2 factores a favor, 1 en contra):

- ❌ Minutos: 26.9 esperados (suplente, ±3.8).
- ✅ Forma: 2.8 en sus últimos 5, 2.4 esta temporada (7 partidos), 2.6 la temporada pasada (línea 1.5).
- ➖ Cómo produce triples: 5.7 triples intentados (su ritmo 7.7 por 36'; el rival concede +0% de triples en su reparto) × 37% esperado.
- ➖ Defensa: el rival concede -1% de triples por minuto a bases/escoltas (defensa media); ajuste aplicado -1%; en su zona principal (triple) el rival concede 34% (liga 35%).
- ➖ Ritmo del partido: -0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ➖ Contra este rival: 2, 1, 0, 4 (2 de 4 a favor).
- ✅ Últimos 10: la habría pasado 8 de 10.
- ⚠️ Ja Morant ya no jugó en sus últimos partidos: la baja ya está en sus minutos.

- ⚠️ Alertas: suplente.
- Triples **2.3** (por componentes 2.1 · por tasa por minuto y defensa rival 2.3): 5.7 triples intentados (su ritmo 7.7 por 36'; el rival concede +0% de triples en su reparto) × 37% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 27.0 | 30.0 | 26.0 | 30.3 | 29.0 |
| Triples anotados | 2.8 | 2.6 | 2.4 | 2.6 | 1.8 |
| Triples intentados | 5.6 | 6.1 | 5.7 | 6.9 | 6.0 |
| % triples | 50.0% | 42.6% | 42.5% | 37.6% | 29.2% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -14%, vs defensa media -10%, vs defensa débil +23%; rebotes: vs defensa fuerte -19%, vs defensa media +13%, vs defensa débil +5%; asistencias: vs defensa fuerte -8%, vs defensa media +3%, vs defensa débil +7%; triples: vs defensa fuerte -19%, vs defensa media -10%, vs defensa débil +32%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 44% | 36% | 35% | 34% |
| pintura | 24% | 49% | 45% | 44% |
| bajo el aro | 16% | 66% | 68% | 72% |
| triple de esquina | 9% | 44% | 38% | 38% |
| media distancia | 7% | 40% | 41% | 43% |

#### Donovan Clingan (pívots) vs Los Angeles Lakers

- Minutos esperados: **25.7** (± 5.9); 90 partidos en la base.
- Ja Morant ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Su prop más probable hoy: **Donovan Clingan: más de 0.5 triples** (62%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Los Angeles Lakers contra pívots en triples: -12% respecto a la media; ajuste por su historial contra defensas similares: +2%.

**¿Por qué 0.9 triples?** (línea 0.5; 25.7 minutos esperados)

En corto:

- La pasó en 5 de 7 esta temporada (falló con 0, 0)
- Con 22+ minutos (hoy se esperan 26): 8 de 10 en sus últimos 15
- Contra las ~10 mejores defensas en triples a pívots: 5 de 9 (últimos 40 partidos)
- Contra defensas fuertes como la de hoy y con 22+ minutos: 9 de 15, con 0.9 de media (últimos 60 partidos)
- El rival es #29 de 30 en triples que concede a pívots por minuto (#1 = el que más concede; -21% frente a la media)
- Su zona principal es triple frontal (33% de sus tiros, 35% de acierto); el rival es #16 de 30 en acierto que deja ahí (34%, liga 35%)
- Cómo tira (últimos 15): recibe y tira 39% (35% de acierto), corte 22% (68% de acierto), palmeo 15% (53% de acierto); en recibe y tira el rival es #5 de 30 en lo que deja (#1 = el que más; 1.12 puntos por tiro frente a 1.06 de media)
- Oportunidades: 2.5 triples intentados esperados al 34%
- Minutos: 26 esperados (titular, ±6)

Razonamiento (3 factores a favor, 1 en contra):

- ✅ Minutos: 25.7 esperados (titular, ±5.9).
- ✅ Forma: 1.0 en sus últimos 5, 1.0 esta temporada (7 partidos), 1.2 la temporada pasada (línea 0.5).
- ➖ Cómo produce triples: 2.5 triples intentados (su ritmo 3.6 por 36'; el rival concede +0% de triples en su reparto) × 34% esperado.
- ❌ Defensa: el rival concede -21% de triples por minuto a pívots (defensa fuerte); ajuste aplicado -12%; en su zona principal (triple) el rival concede 34% (liga 35%).
- ➖ Ritmo del partido: -0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ➖ Contra este rival: 2, 1, 0, 0 (2 de 4 a favor).
- ✅ Últimos 10: la habría pasado 8 de 10.
- ⚠️ Ja Morant ya no jugó en sus últimos partidos: la baja ya está en sus minutos.

- Triples **0.9** (por componentes 0.9 · por tasa por minuto y defensa rival 0.9): 2.5 triples intentados (su ritmo 3.6 por 36'; el rival concede +0% de triples en su reparto) × 34% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 26.2 | 23.4 | 24.7 | 26.9 | 24.2 |
| Triples anotados | 1.0 | 1.1 | 1.0 | 1.1 | 0.8 |
| Triples intentados | 2.2 | 3.1 | 2.1 | 3.3 | 3.2 |
| % triples | 45.5% | 35.5% | 46.7% | 32.5% | 23.1% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -7%, vs defensa media +4%, vs defensa débil +3%; rebotes: vs defensa fuerte -11%, vs defensa media +4%, vs defensa débil +7%; asistencias: vs defensa fuerte -19%, vs defensa media +6%, vs defensa débil +10%; triples: vs defensa fuerte -20%, vs defensa media +7%, vs defensa débil +12%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 50% | 65% | 68% | 72% |
| triple frontal | 33% | 35% | 35% | 34% |
| pintura | 13% | 45% | 45% | 44% |
| triple de esquina | 3% | 32% | 38% | 38% |
| media distancia | 1% | 43% | 41% | 43% |

#### Quentin Grimes (bases/escoltas) vs Portland Trail Blazers

- Minutos esperados: **25.7** (± 4.8); 96 partidos en la base.
- cambio de rol esta temporada (por minuto): tpm -55%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Quentin Grimes: más de 0.5 triples** (62%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Portland Trail Blazers contra bases/escoltas en triples: -5% respecto a la media; ajuste por su historial contra defensas similares: -0%.

**¿Por qué 1.0 triples?** (línea 0.5; 25.7 minutos esperados)

En corto:

- La pasó en 4 de 9 esta temporada (falló con 0, 0, 0, 0)
- Con 22+ minutos (hoy se esperan 26): 7 de 12 en sus últimos 15
- Contra las ~10 mejores defensas en triples a bases/escoltas: 9 de 14 (últimos 40 partidos)
- Contra defensas fuertes como la de hoy y con 22+ minutos: 11 de 15, con 1.3 de media (últimos 60 partidos)
- El rival es #28 de 30 en triples que concede a bases/escoltas por minuto (#1 = el que más concede; -9% frente a la media)
- Su zona principal es triple frontal (38% de sus tiros, 31% de acierto); el rival es #14 de 30 en acierto que deja ahí (35%, liga 35%)
- Cómo tira (últimos 15): recibe y tira 39% (29% de acierto), penetración 29% (61% de acierto), creado 21% (18% de acierto); en recibe y tira el rival es #23 de 30 en lo que deja (#1 = el que más; 1.00 puntos por tiro frente a 1.06 de media)
- Oportunidades: 3.3 triples intentados esperados al 33%
- El rival no tiene a Ja Morant (1.3 triples por partido)
- Minutos: 26 esperados (suplente, ±5)

Razonamiento (2 factores a favor, 2 en contra):

- ❌ Minutos: 25.7 esperados (suplente, ±4.8).
- ✅ Forma: 0.6 en sus últimos 5, 0.7 esta temporada (9 partidos), 1.4 la temporada pasada (línea 0.5).
- ➖ Cómo produce triples: 3.3 triples intentados (su ritmo 4.9 por 36'; el rival concede -6% de triples en su reparto) × 33% esperado.
- ❌ Defensa: el rival concede -9% de triples por minuto a bases/escoltas (defensa fuerte); ajuste aplicado -5%; en su zona principal (triple) el rival concede 35% (liga 35%).
- ➖ Ritmo del partido: -0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ➖ Contra este rival: 0, 1 (1 de 2 a favor).
- ➖ Últimos 10: la habría pasado 5 de 10.
- ✅ Bajas del rival: sin Ja Morant (titular); +1.7% en esta estadística.
- ⚠️ cambio de rol esta temporada (por minuto): tpm -55%; se da más peso a la línea de la casa.

- ⚠️ Alertas: suplente, cambio de rol.
- Triples **1.0** (por componentes 1.1 · por tasa por minuto y defensa rival 0.9): 3.3 triples intentados (su ritmo 4.9 por 36'; el rival concede -6% de triples en su reparto) × 33% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 27.6 | 25.1 | 26.1 | 28.5 | 29.5 |
| Triples anotados | 0.6 | 0.8 | 0.7 | 1.6 | 0.5 |
| Triples intentados | 3.0 | 3.1 | 2.9 | 4.8 | 3.5 |
| % triples | 20.0% | 25.8% | 23.1% | 33.9% | 14.3% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +0%, vs defensa media -6%, vs defensa débil +4%; rebotes: vs defensa fuerte -8%, vs defensa media +6%, vs defensa débil +3%; asistencias: vs defensa fuerte -5%, vs defensa media -9%, vs defensa débil +17%; triples: vs defensa fuerte +3%, vs defensa media -8%, vs defensa débil +7%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 38% | 31% | 35% | 35% |
| bajo el aro | 29% | 71% | 68% | 66% |
| triple de esquina | 13% | 39% | 38% | 38% |
| pintura | 12% | 41% | 45% | 46% |
| media distancia | 8% | 35% | 41% | 42% |

#### Matisse Thybulle (bases/escoltas) vs Portland Trail Blazers

- Minutos esperados: **23.7** (± 3.0); 44 partidos en la base.
- cambio de rol esta temporada (por minuto): reb -44%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Matisse Thybulle: menos de 2.5 rebotes** (61%). Con 80% de probabilidad: más de 0.5 / menos de 3.5.
- Defensa de Portland Trail Blazers contra bases/escoltas en rebotes: -6% respecto a la media; ajuste por su historial contra defensas similares: -2%.

**¿Por qué 2.0 rebotes?** (línea 2.5; 23.7 minutos esperados)

En corto:

- La pasó en 7 de 9 esta temporada (falló con 3, 3)
- Con 20+ minutos (hoy se esperan 24): 6 de 9 en sus últimos 15
- Contra las ~10 mejores defensas en rebotes a bases/escoltas: 10 de 13 (últimos 40 partidos)
- Contra defensas fuertes como la de hoy y con 20+ minutos: 6 de 8, con 2.1 de media (últimos 60 partidos)
- El rival es #27 de 30 en rebotes que concede a bases/escoltas por minuto (#1 = el que más concede; -6% frente a la media)
- El rival es #23 de 30 en rebotes que concede en total (#1 = el que más)
- El rival es #9 de 30 en rebotes ofensivos que concede en total (#1 = el que más)
- Rebotes disponibles con él en pista (últimos 10): 22.9 tiros fallados del rival y 18.9 de su equipo por partido; se queda el 5% y el 2%; el rival falla 46.0 tiros por partido (#23 de 30, #1 = el que más falla)
- El rival no tiene a Ja Morant (2.6 rebotes por partido)
- Minutos: 24 esperados (titular, ±3)

Razonamiento (5 factores a favor, 0 en contra):

- ✅ Minutos: 23.7 esperados (titular, ±3.0).
- ✅ Forma: 1.6 en sus últimos 5, 1.7 esta temporada (9 partidos), 1.9 la temporada pasada (línea 2.5).
- ➖ Cómo produce rebotes: defensivos 1.6 = captura el 6.9% de los fallos del rival en pista × 47.6 fallos esperados del rival (liga 47.0) × 49% del partido; ofensivos 0.5 = 2.7% de los fallos de su equipo × 41.1.
- ✅ Defensa: el rival concede -6% de rebotes por minuto a bases/escoltas (defensa fuerte); ajuste aplicado -6%.
- ➖ Ritmo del partido: -0% de posesiones frente a la media (ya incluido en lo que concede el rival).
- ✅ Contra este rival: 2 (1 de 1 a favor).
- ✅ Últimos 10: la habría pasado 8 de 10.
- ⚠️ cambio de rol esta temporada (por minuto): reb -44%; se da más peso a la línea de la casa.

- ⚠️ Alertas: cambio de rol.
- Rebotes **2.0** (por componentes 2.2 · por tasa por minuto y defensa rival 1.9): defensivos 1.6 = captura el 6.9% de los fallos del rival en pista × 47.6 fallos esperados del rival (liga 47.0) × 49% del partido; ofensivos 0.5 = 2.7% de los fallos de su equipo × 41.1.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 24.6 | 23.3 | 24.2 | 15.6 | 22.0 |
| Rebotes | 1.6 | 1.6 | 1.7 | 1.9 | 2.0 |
| % de los fallos del rival que captura | 3.8% | 5.2% | 5.0% | 9.5% | 11.8% |
| % de los fallos de su equipo que captura | 2.9% | 2.1% | 2.4% | 3.2% | 0.0% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -20%, vs defensa media +0%, vs defensa débil +9%; rebotes: vs defensa fuerte -17%, vs defensa media -6%, vs defensa débil +31%; asistencias: vs defensa fuerte +7%, vs defensa media -10%, vs defensa débil +8%; triples: vs defensa fuerte -36%, vs defensa media +1%, vs defensa débil +28%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 37% | 37% | 35% | 35% |
| triple de esquina | 35% | 40% | 38% | 38% |
| bajo el aro | 16% | 66% | 68% | 66% |
| pintura | 12% | 39% | 45% | 46% |
| media distancia | 0% | 41% | 41% | 42% |

## San Antonio Spurs @ Sacramento Kings

Diferencia esperada: San Antonio Spurs por 15.5 — puede romperse: titulares -3% de minutos, suplentes +4%.

Parte de lesiones: Ben Simmons (Out); Keegan Murray (Out); Maxime Raynaud (Out); Jayden Quaintance (Out); Tobias Harris (Out).

Sin líneas de props para este partido (o sin historial suficiente de los jugadores).

## Sin emparejar con ESPN

Líneas de The Odds API (SportsGameOdds sin respuesta); para que los créditos lleguen a fin de mes solo se pidieron los 2 partidos más parejos (212 créditos restantes)
