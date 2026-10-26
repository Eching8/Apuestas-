# Props NBA 2026-10-26

> **Aviso:** las apuestas implican riesgo de perder dinero. Estas probabilidades son estimaciones estadísticas, no garantías: ningún modelo acierta siempre y las combinadas multiplican el riesgo. Apuesta solo lo que puedas permitirte perder. Si el juego deja de ser un entretenimiento, busca ayuda.

**Modelo** = minutos, tasa por minuto, bajas, defensa rival por posición, zonas de tiro y tipo de defensa, mezclado con el acierto real del jugador sobre esa línea. **Casa** = probabilidad implícita en las cuotas sin el margen. **Prob. final** = mezcla de ambas. Si modelo y casa discrepan mucho, la casa suele saber algo (rol, rotación, una baja): revísalo antes de apostar.

Cada media se construye desde las estadísticas que la producen (tiros × acierto por zona, % de los rebotes disponibles que captura, % de las canastas de sus compañeros que asiste...) y se muestra con esas estadísticas en sus últimos 5 y 10 partidos, la temporada y contra este rival. Todo queda guardado en la tabla `nba_analisis` de la base.

## Las más probables del día

| Partido | Prop | Prob. final | Modelo | Casa | Esperado | Últ. 10 | Temporada | vs este rival | Cuota (implícita) |
|---|---|---|---|---|---|---|---|---|---|
| Phoenix Suns @ Oklahoma City Thunder | **Ajay Mitchell: menos de 0.5 tapones** | **72%** | 80% | 68% | 0.2 ± 0.4 | 8/10 | 2/3 | 0, 0, 0, 0, 0 | 1.36 (73%) |
| Indiana Pacers @ Milwaukee Bucks | **Jaime Jaquez Jr.: más de 0.5 triples** | **69%** | 74% | 65% | 1.3 ± 1.2 | 9/10 | 3/3 | 2, 0, 1 | 1.43 (70%) |
| Washington Wizards @ Charlotte Hornets | **Kyshawn George: menos de 1.5 robos** | **68%** | 74% | 65% | 1.0 ± 1.0 | 9/10 | 2/3 | 1, 2, 0, 0 | 1.41 (71%) |
| Minnesota Timberwolves @ Cleveland Cavaliers | **Ayo Dosunmu: más de 0.5 triples** | **68%** | 75% | 63% | 1.5 ± 1.2 | 8/10 | 3/3 | 2, 1 | 1.48 (68%) |
| Phoenix Suns @ Oklahoma City Thunder | **Ajay Mitchell: menos de 1.5 triples** | **66%** | 70% | 65% | 1.1 ± 1.1 | 9/10 | 3/3 | 4, 1, 1, 3, 1 | 1.44 (69%) |
| Chicago Bulls @ Boston Celtics | **Baylor Scheierman: menos de 9.5 puntos** | **66%** | 82% | 58% | 5.4 ± 3.9 | 9/10 | 2/2 | 10, 2, 3 | 2.00 (50%) |
| Dallas Mavericks @ Miami Heat | **Giannis Antetokounmpo: más de 0.5 robos** | **66%** | 66% | 66% | 1.1 ± 1.0 | 7/10 | 3/3 | 1 | 1.40 (71%) |
| Minnesota Timberwolves @ Cleveland Cavaliers | **Peyton Watson: más de 1.5 asistencias** | **66%** | 74% | 62% | 2.7 ± 1.7 | 9/10 | 2/2 | 0, 0, 1 | 1.48 (68%) |
| Chicago Bulls @ Boston Celtics | **Payton Pritchard: menos de 1.5 robos+tapones** | **66%** | 80% | 58% | 0.8 ± 0.9 | 10/10 | 2/2 | 2, 0, 1 | 2.00 (50%) |
| Washington Wizards @ Charlotte Hornets | **Anthony Davis: menos de 1.5 robos** | **66%** | 68% | 64% | 1.1 ± 1.1 | 8/10 | 2/3 | - | 1.44 (69%) |
| Golden State Warriors @ Denver Nuggets | **Gui Santos: más de 1.5 asistencias** | **66%** | 68% | 64% | 2.5 ± 1.8 | 8/10 | 2/3 | 3, 7, 0 | 1.44 (69%) |
| Minnesota Timberwolves @ Cleveland Cavaliers | **Evan Mobley: menos de 1.5 triples** | **66%** | 66% | 65% | 1.1 ± 1.0 | 5/10 | 1/2 | 0, 3 | 1.44 (70%) |
| Memphis Grizzlies @ Utah Jazz | **Keyonte George: más de 0.5 robos** | **65%** | 67% | 65% | 1.1 ± 1.1 | 7/10 | 3/3 | 1, 1, 2 | 1.43 (70%) |
| Golden State Warriors @ Denver Nuggets | **Gui Santos: más de 0.5 triples** | **65%** | 67% | 64% | 1.1 ± 1.1 | 8/10 | 3/3 | 1, 2, 0 | 1.45 (69%) |

**Si haces combinada:** cada selección que añades multiplica el riesgo. Probabilidad de acertar todas con las más probables de partidos distintos:

- 2 selecciones: **50%**
- 3 selecciones: **34%**
- 4 selecciones: **23%**
- 5 selecciones: **15%**
- 6 selecciones: **10%**

Dentro de un mismo partido (bet builder) las selecciones no son independientes y el cálculo es aún menos fiable. Con 12 selecciones al 65 % la probabilidad de acertar todas es menor del 1 %.

### En qué se basan las 10 más probables

#### Ajay Mitchell: menos de 0.5 tapones (72%) — Phoenix Suns @ Oklahoma City Thunder

**¿Por qué 0.2 tapones?** (línea 0.5; 27.4 minutos esperados)

- Tapones **0.2** (por componentes 0.2 · por tasa por minuto y defensa rival 0.2): tapona el 1.1% de los tiros de 2 del rival en pista × 46.3 tiros de 2 esperados del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 23.8 | 27.4 | 24.7 | 26.3 | 28.8 |
| Tapones | 0.4 | 0.2 | 0.3 | 0.3 | 0.0 |
| % de los tiros de 2 del rival que tapona | 1.7% | 0.7% | 1.3% | 1.1% | 0.0% |

#### Jaime Jaquez Jr.: más de 0.5 triples (69%) — Indiana Pacers @ Milwaukee Bucks

**¿Por qué 1.3 triples?** (línea 0.5; 30.8 minutos esperados)

- Triples **1.3** (por componentes 1.1 · por tasa por minuto y defensa rival 1.4): 3.3 triples intentados (su ritmo 4.2 por 36'; el rival concede -9% de triples en su reparto) × 34% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 32.0 | 30.8 | 31.0 | 28.5 | 26.7 |
| Triples anotados | 1.6 | 1.7 | 1.7 | 0.8 | 1.0 |
| Triples intentados | 3.6 | 3.8 | 3.0 | 2.5 | 2.0 |
| % triples | 44.4% | 44.7% | 55.6% | 31.7% | 50.0% |

#### Kyshawn George: menos de 1.5 robos (68%) — Washington Wizards @ Charlotte Hornets

**¿Por qué 1.0 robos?** (línea 1.5; 29.6 minutos esperados)

- Robos **1.0** (por componentes 1.0 · por tasa por minuto y defensa rival 0.9): roba el 11.8% de las pérdidas del rival en pista × 14.0 pérdidas esperadas del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 25.6 | 22.9 | 30.3 | 28.9 | 24.8 |
| Robos | 0.8 | 0.6 | 1.0 | 1.0 | 0.8 |
| % de las pérdidas del rival que roba | 10.2% | 8.1% | 11.0% | 13.3% | 12.6% |

#### Ayo Dosunmu: más de 0.5 triples (68%) — Minnesota Timberwolves @ Cleveland Cavaliers

**¿Por qué 1.5 triples?** (línea 0.5; 26.2 minutos esperados)

- Triples **1.5** (por componentes 1.6 · por tasa por minuto y defensa rival 1.5): 3.6 triples intentados (su ritmo 4.9 por 36'; el rival concede +1% de triples en su reparto) × 43% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 27.0 | 28.7 | 26.3 | 27.5 | 18.5 |
| Triples anotados | 0.8 | 1.6 | 1.0 | 1.8 | 1.5 |
| Triples intentados | 2.4 | 3.5 | 2.3 | 4.1 | 3.5 |
| % triples | 33.3% | 45.7% | 42.9% | 43.8% | 42.9% |

#### Ajay Mitchell: menos de 1.5 triples (66%) — Phoenix Suns @ Oklahoma City Thunder

**¿Por qué 1.1 triples?** (línea 1.5; 27.4 minutos esperados)

- Triples **1.1** (por componentes 1.4 · por tasa por minuto y defensa rival 1.0): 4.1 triples intentados (su ritmo 4.7 por 36'; el rival concede +0% de triples en su reparto) × 33% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 23.8 | 27.4 | 24.7 | 26.3 | 28.8 |
| Triples anotados | 0.2 | 0.5 | 0.3 | 1.1 | 2.0 |
| Triples intentados | 2.0 | 2.7 | 2.3 | 3.2 | 4.6 |
| % triples | 10.0% | 18.5% | 14.3% | 34.3% | 43.5% |

#### Baylor Scheierman: menos de 9.5 puntos (66%) — Chicago Bulls @ Boston Celtics

**¿Por qué 5.4 puntos?** (línea 9.5; 14.5 minutos esperados)

- Puntos **5.4** (por componentes 5.8 · por tasa por minuto y defensa rival 5.3): 4.6 tiros de campo (su ritmo 9.3 por 36'; el rival concede +6% de tiros) × 1.15 puntos por tiro [triple frontal 48% de sus tiros al 36% (rival concede 37%, liga 35%); triple de esquina 24% de sus tiros al 44% (rival concede 37%, liga 38%); pintura 13% de sus tiros al 49% (rival concede 43%, liga 45%)] + 0.6 tiros libres × 79%.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 15.0 | 16.6 | 14.5 | 18.2 | 13.7 |
| Puntos | 3.6 | 7.0 | 5.0 | 5.4 | 5.0 |
| Tiros de campo intentados | 3.6 | 5.4 | 4.0 | 4.3 | 4.0 |
| % tiros de campo | 38.9% | 42.6% | 50.0% | 45.1% | 50.0% |
| Triples intentados | 2.4 | 3.9 | 2.0 | 3.1 | 2.7 |
| % triples | 33.3% | 41.0% | 50.0% | 39.8% | 37.5% |
| Tiros libres intentados | 0.0 | 0.8 | 0.0 | 0.4 | 0.0 |
| % tiros libres | - | 100.0% | - | 90.3% | - |
| Jugadas que usa por 36 min | 10.6 | 14.0 | 12.4 | 9.9 | 10.5 |

#### Giannis Antetokounmpo: más de 0.5 robos (66%) — Dallas Mavericks @ Miami Heat

**¿Por qué 1.1 robos?** (línea 0.5; 28.7 minutos esperados)

- Robos **1.1** (por componentes 1.1 · por tasa por minuto y defensa rival 1.0): roba el 12.9% de las pérdidas del rival en pista × 14.6 pérdidas esperadas del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 28.0 | 28.2 | 29.3 | 28.9 | 37.0 |
| Robos | 1.0 | 1.1 | 1.3 | 0.9 | 1.0 |
| % de las pérdidas del rival que roba | 11.0% | 14.7% | 13.3% | 12.8% | 9.3% |

#### Peyton Watson: más de 1.5 asistencias (66%) — Minnesota Timberwolves @ Cleveland Cavaliers

**¿Por qué 2.7 asistencias?** (línea 1.5; 28.9 minutos esperados)

- Asistencias **2.7** (por componentes 2.6 · por tasa por minuto y defensa rival 2.7): asiste el 13.2% de las canastas de sus compañeros en pista × 19.9 canastas de compañeros esperadas (su equipo 41.4 por 48' contra esta defensa).

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 22.6 | 26.4 | 30.5 | 29.6 | 33.7 |
| Asistencias | 3.0 | 2.8 | 3.0 | 2.1 | 0.3 |
| % de las canastas de compañeros que asiste | 16.4% | 13.9% | 12.9% | 9.1% | 1.2% |
| Pérdidas por jugada | 22.3% | 15.1% | 25.3% | 12.3% | 13.6% |

#### Payton Pritchard: menos de 1.5 robos+tapones (66%) — Chicago Bulls @ Boston Celtics

**¿Por qué 0.8 robos+tapones?** (línea 1.5; 29.9 minutos esperados)

- Robos **0.6** (por componentes 0.6 · por tasa por minuto y defensa rival 0.6): roba el 7.9% de las pérdidas del rival en pista × 12.7 pérdidas esperadas del rival.
- Tapones **0.2** (por componentes 0.2 · por tasa por minuto y defensa rival 0.1): tapona el 0.6% de los tiros de 2 del rival en pista × 46.3 tiros de 2 esperados del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 31.8 | 31.8 | 29.0 | 32.5 | 31.7 |
| Robos | 0.2 | 0.4 | 0.0 | 0.7 | 1.0 |
| % de las pérdidas del rival que roba | 2.5% | 5.3% | 0.0% | 9.0% | 11.7% |
| Tapones | 0.0 | 0.0 | 0.0 | 0.1 | 0.0 |
| % de los tiros de 2 del rival que tapona | 0.0% | 0.0% | 0.0% | 0.4% | 0.0% |

#### Anthony Davis: menos de 1.5 robos (66%) — Washington Wizards @ Charlotte Hornets

**¿Por qué 1.1 robos?** (línea 1.5; 32.3 minutos esperados)

- Robos **1.1** (por componentes 1.2 · por tasa por minuto y defensa rival 1.1): roba el 13.0% de las pérdidas del rival en pista × 14.0 pérdidas esperadas del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 33.6 | 32.6 | 32.3 | 31.2 | - |
| Robos | 1.0 | 1.1 | 1.3 | 1.1 | - |
| % de las pérdidas del rival que roba | 11.1% | 13.2% | 13.5% | 14.2% | - |


## Washington Wizards @ Charlotte Hornets

Parte de lesiones: Grant Williams (Out); Coby White (Out); Naz Reid (Day-To-Day); Jamir Watkins (Out); Kylan Boswell (Out); Tristan Vukcevic (Out); Kon Knueppel (Out); AJ Dybantsa (Out).

Las 8 más probables (máximo 2 por jugador: las de un mismo jugador suelen ganar o perder juntas).

| Prop | Prob. final | Modelo | Casa | Esperado | Últ. 10 | Temporada | vs este rival | Cuota (implícita) |
|---|---|---|---|---|---|---|---|---|
| **Kyshawn George: menos de 1.5 robos** | **68%** | 74% | 65% | 1.0 ± 1.0 | 9/10 | 2/3 | 1, 2, 0, 0 | 1.41 (71%) |
| **Anthony Davis: menos de 1.5 robos** | **66%** | 68% | 64% | 1.1 ± 1.1 | 8/10 | 2/3 | - | 1.44 (69%) |
| **Alex Sarr: menos de 1.5 tapones** | **64%** | 66% | 64% | 1.2 ± 1.5 | 6/10 | 2/3 | 1, 4, 3 | 1.45 (69%) |
| **Bilal Coulibaly: más de 0.5 triples** | **64%** | 64% | 64% | 1.1 ± 1.1 | 5/10 | 2/3 | 3, 3 | 1.45 (69%) |
| **Moussa Diabate: más de 0.5 robos** | **64%** | 64% | 64% | 1.5 ± 1.6 | 6/10 | 3/3 | 1, 0, 0 | 1.45 (69%) |
| **Naz Reid: menos de 3.5 asistencias** | **63%** | 70% | 60% | 2.7 ± 2.4 | 7/10 | 2/3 | 3, 1 | 1.56 (64%) |
| **Justin Champagnie: más de 0.5 triples** | **62%** | 62% | 62% | 1.0 ± 1.0 | 8/10 | 2/3 | 1, 0, 0 | 1.50 (67%) |
| **Anthony Davis: menos de 1.5 tapones** | **62%** | 67% | 59% | 1.1 ± 1.1 | 6/10 | 2/3 | - | 1.58 (63%) |

### Fichas de los jugadores destacados

#### Kyshawn George (aleros/ala-pívots) vs Charlotte Hornets

- Minutos esperados: **29.6** (± 5.6); 51 partidos en la base.
- Jamir Watkins ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- cambio de rol esta temporada (por minuto): tpm -69%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Kyshawn George: menos de 1.5 robos** (68%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Charlotte Hornets contra aleros/ala-pívots en robos: -8% respecto a la media; ajuste por su historial contra defensas similares: +3%.

**¿Por qué 1.0 robos?** (línea 1.5; 29.6 minutos esperados)

- Robos **1.0** (por componentes 1.0 · por tasa por minuto y defensa rival 0.9): roba el 11.8% de las pérdidas del rival en pista × 14.0 pérdidas esperadas del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 25.6 | 22.9 | 30.3 | 28.9 | 24.8 |
| Robos | 0.8 | 0.6 | 1.0 | 1.0 | 0.8 |
| % de las pérdidas del rival que roba | 10.2% | 8.1% | 11.0% | 13.3% | 12.6% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -6%, vs defensa media -5%, vs defensa débil +17%; rebotes: vs defensa fuerte -16%, vs defensa media +3%, vs defensa débil +21%; asistencias: vs defensa fuerte +2%, vs defensa media -3%, vs defensa débil +1%; triples: vs defensa fuerte -3%, vs defensa media +37%, vs defensa débil -26%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 35% | 35% | 35% | 35% |
| pintura | 21% | 40% | 45% | 44% |
| bajo el aro | 20% | 69% | 68% | 68% |
| media distancia | 15% | 42% | 41% | 39% |
| triple de esquina | 9% | 39% | 38% | 39% |

#### Anthony Davis (aleros/ala-pívots) vs Charlotte Hornets

- Minutos esperados: **32.3** (± 3.0); 23 partidos en la base.
- Jamir Watkins ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Su prop más probable hoy: **Anthony Davis: menos de 1.5 robos** (66%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Charlotte Hornets contra aleros/ala-pívots en robos: -8% respecto a la media; ajuste por su historial contra defensas similares: -1%.

**¿Por qué 1.1 robos?** (línea 1.5; 32.3 minutos esperados)

- Robos **1.1** (por componentes 1.2 · por tasa por minuto y defensa rival 1.1): roba el 13.0% de las pérdidas del rival en pista × 14.0 pérdidas esperadas del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 33.6 | 32.6 | 32.3 | 31.2 | - |
| Robos | 1.0 | 1.1 | 1.3 | 1.1 | - |
| % de las pérdidas del rival que roba | 11.1% | 13.2% | 13.5% | 14.2% | - |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -9%, vs defensa media +1%, vs defensa débil +8%; rebotes: vs defensa fuerte -2%, vs defensa media -4%, vs defensa débil +4%; asistencias: vs defensa fuerte -7%, vs defensa débil +1%; triples: vs defensa fuerte -40%, vs defensa media +51%, vs defensa débil -34%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 40% | 69% | 68% | 68% |
| pintura | 29% | 42% | 45% | 44% |
| media distancia | 20% | 36% | 41% | 39% |
| triple frontal | 10% | 30% | 35% | 35% |
| triple de esquina | 2% | 37% | 38% | 39% |

#### Alex Sarr (pívots) vs Charlotte Hornets

- Minutos esperados: **23.7** (± 3.0); 51 partidos en la base.
- Jamir Watkins ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- cambio de rol esta temporada (por minuto): pts -47%, ast +40%, tpm -64%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Alex Sarr: menos de 1.5 tapones** (64%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Charlotte Hornets contra pívots en tapones: -0% respecto a la media; ajuste por su historial contra defensas similares: -2%.

**¿Por qué 1.2 tapones?** (línea 1.5; 23.7 minutos esperados)

- Tapones **1.2** (por componentes 1.1 · por tasa por minuto y defensa rival 1.3): tapona el 4.8% de los tiros de 2 del rival en pista × 47.7 tiros de 2 esperados del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 23.4 | 22.1 | 24.0 | 27.2 | 29.0 |
| Tapones | 1.0 | 1.6 | 1.0 | 2.0 | 2.7 |
| % de los tiros de 2 del rival que tapona | 3.8% | 6.3% | 3.6% | 6.3% | 9.5% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -6%, vs defensa media +3%, vs defensa débil +7%; rebotes: vs defensa fuerte +4%, vs defensa media -8%, vs defensa débil -0%; asistencias: vs defensa fuerte +11%, vs defensa media -11%, vs defensa débil -4%; triples: vs defensa fuerte -9%, vs defensa media -47%, vs defensa débil +49%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| pintura | 34% | 41% | 45% | 44% |
| bajo el aro | 32% | 72% | 68% | 68% |
| triple frontal | 21% | 34% | 35% | 35% |
| media distancia | 10% | 36% | 41% | 39% |
| triple de esquina | 3% | 35% | 38% | 39% |

#### Bilal Coulibaly (bases/escoltas) vs Charlotte Hornets

- Minutos esperados: **25.9** (± 3.0); 59 partidos en la base.
- Jamir Watkins ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- cambio de rol esta temporada (por minuto): ast -87%, tpm -43%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Bilal Coulibaly: más de 0.5 triples** (64%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Charlotte Hornets contra bases/escoltas en triples: -5% respecto a la media; ajuste por su historial contra defensas similares: -0%.

**¿Por qué 1.1 triples?** (línea 0.5; 25.9 minutos esperados)

- Triples **1.1** (por componentes 1.2 · por tasa por minuto y defensa rival 1.1): 3.5 triples intentados (su ritmo 5.1 por 36'; el rival concede -2% de triples en su reparto) × 33% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 25.2 | 23.2 | 26.7 | 26.2 | 20.0 |
| Triples anotados | 1.2 | 1.0 | 0.7 | 1.2 | 3.0 |
| Triples intentados | 2.8 | 3.3 | 2.7 | 3.6 | 6.5 |
| % triples | 42.9% | 30.3% | 25.0% | 31.9% | 46.2% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -0%, vs defensa media -7%, vs defensa débil +5%; rebotes: vs defensa fuerte -7%, vs defensa media +6%, vs defensa débil -0%; asistencias: vs defensa fuerte +3%, vs defensa media -1%, vs defensa débil -2%; triples: vs defensa fuerte -2%, vs defensa media +24%, vs defensa débil -23%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 32% | 69% | 68% | 68% |
| triple frontal | 24% | 29% | 35% | 35% |
| pintura | 23% | 32% | 45% | 44% |
| triple de esquina | 14% | 39% | 38% | 39% |
| media distancia | 7% | 39% | 41% | 39% |

#### Moussa Diabate (aleros/ala-pívots) vs Washington Wizards

- Minutos esperados: **25.0** (± 5.6); 78 partidos en la base.
- Grant Williams ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Kon Knueppel ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Su prop más probable hoy: **Moussa Diabate: más de 0.5 robos** (64%). Con 80% de probabilidad: más de - / menos de 3.5.
- Defensa de Washington Wizards contra aleros/ala-pívots en robos: +14% respecto a la media; ajuste por su historial contra defensas similares: +5%.

**¿Por qué 1.5 robos?** (línea 0.5; 25.0 minutos esperados)

- Robos **1.5** (por componentes 1.2 · por tasa por minuto y defensa rival 1.6): roba el 17.7% de las pérdidas del rival en pista × 13.4 pérdidas esperadas del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 26.2 | 26.4 | 25.7 | 26.1 | 30.3 |
| Robos | 1.6 | 1.1 | 2.7 | 0.7 | 0.3 |
| % de las pérdidas del rival que roba | 21.8% | 15.3% | 30.0% | 11.4% | 4.9% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -19%, vs defensa media +19%, vs defensa débil +3%; rebotes: vs defensa fuerte -14%, vs defensa media +1%, vs defensa débil +14%; asistencias: vs defensa fuerte +34%, vs defensa media -18%, vs defensa débil -22%; triples: vs defensa fuerte -100%, vs defensa media +181%, vs defensa débil -100%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 72% | 72% | 68% | 70% |
| pintura | 24% | 40% | 45% | 42% |
| media distancia | 2% | 41% | 41% | 41% |
| triple frontal | 1% | 34% | 35% | 35% |
| triple de esquina | 0% | 39% | 38% | 40% |

## Minnesota Timberwolves @ Cleveland Cavaliers

Parte de lesiones: Donte DiVincenzo (Out).

Las 8 más probables (máximo 2 por jugador: las de un mismo jugador suelen ganar o perder juntas).

| Prop | Prob. final | Modelo | Casa | Esperado | Últ. 10 | Temporada | vs este rival | Cuota (implícita) |
|---|---|---|---|---|---|---|---|---|
| **Ayo Dosunmu: más de 0.5 triples** | **68%** | 75% | 63% | 1.5 ± 1.2 | 8/10 | 3/3 | 2, 1 | 1.48 (68%) |
| **Peyton Watson: más de 1.5 asistencias** | **66%** | 74% | 62% | 2.7 ± 1.7 | 9/10 | 2/2 | 0, 0, 1 | 1.48 (68%) |
| **Evan Mobley: menos de 1.5 triples** | **66%** | 66% | 65% | 1.1 ± 1.0 | 5/10 | 1/2 | 0, 3 | 1.44 (70%) |
| **Donovan Mitchell: menos de 1.5 robos** | **64%** | 64% | 64% | 1.4 ± 1.2 | 8/10 | 1/2 | 1, 1 | 1.44 (69%) |
| **Anthony Edwards: menos de 1.5 robos** | **63%** | 65% | 62% | 1.3 ± 1.4 | 7/10 | 1/3 | 0, 1 | 1.48 (68%) |
| **Jaylon Tyson: menos de 1.5 triples** | **62%** | 65% | 61% | 1.3 ± 1.3 | 9/10 | 1/2 | 4, 0 | 1.53 (65%) |
| **Jarrett Allen: menos de 1.5 asistencias** | **62%** | 63% | 62% | 1.4 ± 1.2 | 9/10 | 2/2 | 4, 1 | 1.51 (66%) |
| **Jarrett Allen: menos de 1.5 tapones** | **62%** | 56% | 65% | 1.3 ± 1.1 | 4/10 | 0/2 | 1, 0 | 1.45 (69%) |

### Fichas de los jugadores destacados

#### Ayo Dosunmu (bases/escoltas) vs Cleveland Cavaliers

- Minutos esperados: **26.2** (± 3.7); 82 partidos en la base.
- Donte DiVincenzo ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- cambio de rol esta temporada (por minuto): reb +51%, ast +52%, tpm -41%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Ayo Dosunmu: más de 0.5 triples** (68%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Cleveland Cavaliers contra bases/escoltas en triples: +3% respecto a la media; ajuste por su historial contra defensas similares: +0%.

**¿Por qué 1.5 triples?** (línea 0.5; 26.2 minutos esperados)

- Triples **1.5** (por componentes 1.6 · por tasa por minuto y defensa rival 1.5): 3.6 triples intentados (su ritmo 4.9 por 36'; el rival concede +1% de triples en su reparto) × 43% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 27.0 | 28.7 | 26.3 | 27.5 | 18.5 |
| Triples anotados | 0.8 | 1.6 | 1.0 | 1.8 | 1.5 |
| Triples intentados | 2.4 | 3.5 | 2.3 | 4.1 | 3.5 |
| % triples | 33.3% | 45.7% | 42.9% | 43.8% | 42.9% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +4%, vs defensa media -10%, vs defensa débil +2%; rebotes: vs defensa fuerte -17%, vs defensa media +0%, vs defensa débil +17%; asistencias: vs defensa fuerte +6%, vs defensa media -14%, vs defensa débil +7%; triples: vs defensa fuerte -10%, vs defensa media +2%, vs defensa débil +15%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 39% | 65% | 68% | 64% |
| triple frontal | 25% | 42% | 35% | 36% |
| pintura | 21% | 42% | 45% | 44% |
| triple de esquina | 11% | 41% | 38% | 39% |
| media distancia | 4% | 45% | 41% | 42% |

#### Peyton Watson (bases/escoltas) vs Minnesota Timberwolves

- Minutos esperados: **28.9** (± 5.2); 56 partidos en la base.
- cambio de rol esta temporada (por minuto): pts -37%, reb -60%, ast +41%, tpm -35%; se da más peso a la línea de la casa
- solo 2 partidos con su equipo actual: su rol puede haber cambiado, se da más peso a la línea de la casa
- Su prop más probable hoy: **Peyton Watson: más de 1.5 asistencias** (66%). Con 80% de probabilidad: más de 0.5 / menos de 4.5.
- Defensa de Minnesota Timberwolves contra bases/escoltas en asistencias: -2% respecto a la media; ajuste por su historial contra defensas similares: -2%.

**¿Por qué 2.7 asistencias?** (línea 1.5; 28.9 minutos esperados)

- Asistencias **2.7** (por componentes 2.6 · por tasa por minuto y defensa rival 2.7): asiste el 13.2% de las canastas de sus compañeros en pista × 19.9 canastas de compañeros esperadas (su equipo 41.4 por 48' contra esta defensa).

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 22.6 | 26.4 | 30.5 | 29.6 | 33.7 |
| Asistencias | 3.0 | 2.8 | 3.0 | 2.1 | 0.3 |
| % de las canastas de compañeros que asiste | 16.4% | 13.9% | 12.9% | 9.1% | 1.2% |
| Pérdidas por jugada | 22.3% | 15.1% | 25.3% | 12.3% | 13.6% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +3%, vs defensa media -11%, vs defensa débil +8%; rebotes: vs defensa fuerte -5%, vs defensa media +0%, vs defensa débil +4%; asistencias: vs defensa fuerte -26%, vs defensa media -5%, vs defensa débil +22%; triples: vs defensa fuerte -32%, vs defensa media +11%, vs defensa débil +31%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 28% | 67% | 68% | 66% |
| pintura | 27% | 43% | 45% | 43% |
| triple frontal | 20% | 34% | 35% | 33% |
| triple de esquina | 15% | 44% | 38% | 38% |
| media distancia | 10% | 41% | 41% | 40% |

#### Evan Mobley (pívots) vs Minnesota Timberwolves

- Minutos esperados: **34.9** (± 3.0); 82 partidos en la base.
- cambio de rol esta temporada (por minuto): tpm +38%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Evan Mobley: menos de 1.5 triples** (66%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Minnesota Timberwolves contra pívots en triples: +1% respecto a la media; ajuste por su historial contra defensas similares: -1%.

**¿Por qué 1.1 triples?** (línea 1.5; 34.9 minutos esperados)

- Triples **1.1** (por componentes 0.9 · por tasa por minuto y defensa rival 1.1): 2.9 triples intentados (su ritmo 3.3 por 36'; el rival concede -8% de triples en su reparto) × 31% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 35.8 | 36.1 | 34.5 | 32.5 | 35.0 |
| Triples anotados | 1.6 | 1.4 | 1.5 | 1.0 | 1.5 |
| Triples intentados | 4.4 | 4.2 | 3.5 | 3.3 | 4.0 |
| % triples | 36.4% | 33.3% | 42.9% | 30.7% | 37.5% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -8%, vs defensa media -3%, vs defensa débil +16%; rebotes: vs defensa fuerte -3%, vs defensa media -4%, vs defensa débil +9%; asistencias: vs defensa fuerte -7%, vs defensa media -1%, vs defensa débil +13%; triples: vs defensa fuerte -1%, vs defensa media -31%, vs defensa débil +20%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 43% | 76% | 68% | 66% |
| pintura | 26% | 43% | 45% | 43% |
| triple frontal | 22% | 32% | 35% | 33% |
| media distancia | 5% | 43% | 41% | 40% |
| triple de esquina | 4% | 34% | 38% | 38% |

#### Donovan Mitchell (bases/escoltas) vs Minnesota Timberwolves

- Minutos esperados: **35.2** (± 3.0); 90 partidos en la base.
- cambio de rol esta temporada (por minuto): reb +58%, ast -35%, tpm -39%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Donovan Mitchell: menos de 1.5 robos** (64%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Minnesota Timberwolves contra bases/escoltas en robos: -1% respecto a la media; ajuste por su historial contra defensas similares: -1%.

**¿Por qué 1.4 robos?** (línea 1.5; 35.2 minutos esperados)

- Robos **1.4** (por componentes 1.4 · por tasa por minuto y defensa rival 1.3): roba el 13.0% de las pérdidas del rival en pista × 14.5 pérdidas esperadas del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 36.4 | 36.0 | 35.0 | 32.9 | 34.0 |
| Robos | 2.0 | 1.4 | 1.5 | 1.4 | 1.0 |
| % de las pérdidas del rival que roba | 19.4% | 13.0% | 12.1% | 14.1% | 8.8% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -3%, vs defensa media -5%, vs defensa débil +10%; rebotes: vs defensa fuerte -9%, vs defensa media -3%, vs defensa débil +14%; asistencias: vs defensa fuerte -10%, vs defensa media +13%, vs defensa débil +6%; triples: vs defensa fuerte -4%, vs defensa media +12%, vs defensa débil -18%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 37% | 37% | 35% | 33% |
| pintura | 24% | 53% | 45% | 43% |
| bajo el aro | 22% | 65% | 68% | 66% |
| media distancia | 11% | 47% | 41% | 40% |
| triple de esquina | 5% | 36% | 38% | 38% |

#### Anthony Edwards (bases/escoltas) vs Cleveland Cavaliers

- Minutos esperados: **30.4** (± 3.5); 77 partidos en la base.
- Donte DiVincenzo ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- cambio de rol esta temporada (por minuto): tpm +49%; se da más peso a la línea de la casa
- segundo partido en dos noches: -3% de minutos
- Su prop más probable hoy: **Anthony Edwards: menos de 1.5 robos** (63%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Cleveland Cavaliers contra bases/escoltas en robos: -1% respecto a la media; ajuste por su historial contra defensas similares: -1%.

**¿Por qué 1.3 robos?** (línea 1.5; 30.4 minutos esperados)

- Robos **1.3** (por componentes 1.3 · por tasa por minuto y defensa rival 1.3): roba el 14.4% de las pérdidas del rival en pista × 14.2 pérdidas esperadas del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 33.8 | 31.7 | 31.3 | 33.6 | 36.0 |
| Robos | 1.8 | 1.0 | 2.0 | 1.2 | 0.5 |
| % de las pérdidas del rival que roba | 16.0% | 10.7% | 18.4% | 12.7% | 6.3% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -7%, vs defensa media -6%, vs defensa débil +14%; rebotes: vs defensa fuerte -9%, vs defensa media -1%, vs defensa débil +10%; asistencias: vs defensa fuerte -9%, vs defensa media +12%, vs defensa débil +0%; triples: vs defensa fuerte -2%, vs defensa media -15%, vs defensa débil +13%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 37% | 39% | 35% | 36% |
| bajo el aro | 22% | 70% | 68% | 64% |
| media distancia | 19% | 43% | 41% | 42% |
| pintura | 18% | 45% | 45% | 44% |
| triple de esquina | 4% | 41% | 38% | 39% |

## Chicago Bulls @ Boston Celtics

Parte de lesiones: Nic Claxton (Out); Patrick Williams (Day-To-Day); Devin Carter (Out); Noa Essengue (Day-To-Day).

Las 8 más probables (máximo 2 por jugador: las de un mismo jugador suelen ganar o perder juntas).

| Prop | Prob. final | Modelo | Casa | Esperado | Últ. 10 | Temporada | vs este rival | Cuota (implícita) |
|---|---|---|---|---|---|---|---|---|
| **Baylor Scheierman: menos de 9.5 puntos** | **66%** | 82% | 58% | 5.4 ± 3.9 | 9/10 | 2/2 | 10, 2, 3 | 2.00 (50%) |
| **Payton Pritchard: menos de 1.5 robos+tapones** | **66%** | 80% | 58% | 0.8 ± 0.9 | 10/10 | 2/2 | 2, 0, 1 | 2.00 (50%) |
| **Tre Jones: menos de 1.5 robos+tapones** | **65%** | 77% | 58% | 0.7 ± 0.9 | 8/10 | 2/3 | 0 | 2.00 (50%) |
| **Derrick White: más de 0.5 robos** | **64%** | 67% | 63% | 1.2 ± 1.1 | 7/10 | 2/2 | 2, 1, 3 | 1.44 (69%) |
| **Leonard Miller: menos de 1.5 robos+tapones** | **63%** | 74% | 58% | 0.9 ± 1.0 | 7/10 | 3/3 | 0 | 2.00 (50%) |
| **Leonard Miller: menos de 1.5 triples** | **63%** | 60% | 65% | 1.3 ± 1.1 | 5/10 | 2/3 | 0 | 1.43 (70%) |
| **Paul George: menos de 0.5 tapones** | **63%** | 66% | 61% | 0.4 ± 0.6 | 7/10 | 2/2 | 1, 0 | 1.48 (68%) |
| **Jayson Tatum: menos de 1.5 robos** | **62%** | 59% | 63% | 1.4 ± 1.3 | 7/10 | 1/2 | - | 1.44 (70%) |

### Fichas de los jugadores destacados

#### Baylor Scheierman (bases/escoltas) vs Chicago Bulls

- Minutos esperados: **14.5** (± 4.4); 86 partidos en la base.
- cambio de rol esta temporada (por minuto): reb -45%, ast -100%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Baylor Scheierman: menos de 9.5 puntos** (66%). Con 80% de probabilidad: más de 1.5 / menos de 8.5.
- Defensa de Chicago Bulls contra bases/escoltas en puntos: +1% respecto a la media; ajuste por su historial contra defensas similares: -1%.

**¿Por qué 5.4 puntos?** (línea 9.5; 14.5 minutos esperados)

- Puntos **5.4** (por componentes 5.8 · por tasa por minuto y defensa rival 5.3): 4.6 tiros de campo (su ritmo 9.3 por 36'; el rival concede +6% de tiros) × 1.15 puntos por tiro [triple frontal 48% de sus tiros al 36% (rival concede 37%, liga 35%); triple de esquina 24% de sus tiros al 44% (rival concede 37%, liga 38%); pintura 13% de sus tiros al 49% (rival concede 43%, liga 45%)] + 0.6 tiros libres × 79%.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 15.0 | 16.6 | 14.5 | 18.2 | 13.7 |
| Puntos | 3.6 | 7.0 | 5.0 | 5.4 | 5.0 |
| Tiros de campo intentados | 3.6 | 5.4 | 4.0 | 4.3 | 4.0 |
| % tiros de campo | 38.9% | 42.6% | 50.0% | 45.1% | 50.0% |
| Triples intentados | 2.4 | 3.9 | 2.0 | 3.1 | 2.7 |
| % triples | 33.3% | 41.0% | 50.0% | 39.8% | 37.5% |
| Tiros libres intentados | 0.0 | 0.8 | 0.0 | 0.4 | 0.0 |
| % tiros libres | - | 100.0% | - | 90.3% | - |
| Jugadas que usa por 36 min | 10.6 | 14.0 | 12.4 | 9.9 | 10.5 |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +17%, vs defensa media -15%, vs defensa débil -9%; rebotes: vs defensa fuerte -5%, vs defensa media +2%, vs defensa débil +3%; asistencias: vs defensa fuerte -0%, vs defensa media -8%, vs defensa débil +8%; triples: vs defensa fuerte -14%, vs defensa media +13%, vs defensa débil +5%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 48% | 36% | 35% | 37% |
| triple de esquina | 24% | 44% | 38% | 37% |
| pintura | 13% | 49% | 45% | 43% |
| bajo el aro | 8% | 70% | 68% | 67% |
| media distancia | 7% | 45% | 41% | 43% |

#### Payton Pritchard (bases/escoltas) vs Chicago Bulls

- Minutos esperados: **29.9** (± 3.0); 88 partidos en la base.
- cambio de rol esta temporada (por minuto): pts -30%, ast -46%, tpm -37%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Payton Pritchard: menos de 1.5 robos+tapones** (66%). Con 80% de probabilidad: más de - / menos de 1.5.
- Defensa de Chicago Bulls contra bases/escoltas en robos+tapones: +8% respecto a la media; ajuste por su historial contra defensas similares: -1%.

**¿Por qué 0.8 robos+tapones?** (línea 1.5; 29.9 minutos esperados)

- Robos **0.6** (por componentes 0.6 · por tasa por minuto y defensa rival 0.6): roba el 7.9% de las pérdidas del rival en pista × 12.7 pérdidas esperadas del rival.
- Tapones **0.2** (por componentes 0.2 · por tasa por minuto y defensa rival 0.1): tapona el 0.6% de los tiros de 2 del rival en pista × 46.3 tiros de 2 esperados del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 31.8 | 31.8 | 29.0 | 32.5 | 31.7 |
| Robos | 0.2 | 0.4 | 0.0 | 0.7 | 1.0 |
| % de las pérdidas del rival que roba | 2.5% | 5.3% | 0.0% | 9.0% | 11.7% |
| Tapones | 0.0 | 0.0 | 0.0 | 0.1 | 0.0 |
| % de los tiros de 2 del rival que tapona | 0.0% | 0.0% | 0.0% | 0.4% | 0.0% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -2%, vs defensa media -4%, vs defensa débil +6%; rebotes: vs defensa fuerte -7%, vs defensa media +6%, vs defensa débil +3%; asistencias: vs defensa fuerte -11%, vs defensa media -9%, vs defensa débil +20%; triples: vs defensa fuerte -6%, vs defensa media -9%, vs defensa débil +22%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 47% | 37% | 35% | 37% |
| pintura | 23% | 54% | 45% | 43% |
| bajo el aro | 12% | 69% | 68% | 67% |
| media distancia | 12% | 41% | 41% | 43% |
| triple de esquina | 5% | 40% | 38% | 37% |

#### Tre Jones (bases/escoltas) vs Boston Celtics

- Minutos esperados: **19.4** (± 4.7); 68 partidos en la base.
- Su prop más probable hoy: **Tre Jones: menos de 1.5 robos+tapones** (65%). Con 80% de probabilidad: más de - / menos de 1.5.
- Defensa de Boston Celtics contra bases/escoltas en robos+tapones: -22% respecto a la media; ajuste por su historial contra defensas similares: -2%.

**¿Por qué 0.7 robos+tapones?** (línea 1.5; 19.4 minutos esperados)

- Robos **0.6** (por componentes 0.6 · por tasa por minuto y defensa rival 0.6): roba el 15.0% de las pérdidas del rival en pista × 10.3 pérdidas esperadas del rival.
- Tapones **0.1** (por componentes 0.1 · por tasa por minuto y defensa rival 0.1): tapona el 0.6% de los tiros de 2 del rival en pista × 50.9 tiros de 2 esperados del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 20.0 | 23.9 | 18.3 | 27.0 | 23.0 |
| Robos | 0.8 | 0.8 | 1.0 | 1.2 | 0.0 |
| % de las pérdidas del rival que roba | 12.6% | 10.7% | 17.6% | 16.8% | 0.0% |
| Tapones | 0.0 | 0.0 | 0.0 | 0.2 | 0.0 |
| % de los tiros de 2 del rival que tapona | 0.0% | 0.0% | 0.0% | 0.5% | 0.0% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -6%, vs defensa media +9%, vs defensa débil +1%; rebotes: vs defensa fuerte -15%, vs defensa media +10%, vs defensa débil +10%; asistencias: vs defensa fuerte +1%, vs defensa media -12%, vs defensa débil +10%; triples: vs defensa fuerte -12%, vs defensa media +1%, vs defensa débil +15%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 51% | 69% | 68% | 66% |
| pintura | 24% | 44% | 45% | 43% |
| triple frontal | 14% | 31% | 35% | 36% |
| triple de esquina | 7% | 37% | 38% | 37% |
| media distancia | 4% | 44% | 41% | 42% |

#### Derrick White (bases/escoltas) vs Chicago Bulls

- Minutos esperados: **34.6** (± 3.2); 86 partidos en la base.
- cambio de rol esta temporada (por minuto): reb -42%, ast +34%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Derrick White: más de 0.5 robos** (64%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Chicago Bulls contra bases/escoltas en robos: +10% respecto a la media; ajuste por su historial contra defensas similares: +2%.

**¿Por qué 1.2 robos?** (línea 0.5; 34.6 minutos esperados)

- Robos **1.2** (por componentes 1.1 · por tasa por minuto y defensa rival 1.2): roba el 11.8% de las pérdidas del rival en pista × 12.7 pérdidas esperadas del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 36.4 | 33.7 | 34.5 | 34.2 | 35.3 |
| Robos | 1.0 | 0.9 | 1.0 | 1.1 | 2.0 |
| % de las pérdidas del rival que roba | 11.0% | 11.5% | 8.4% | 13.7% | 20.9% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +1%, vs defensa media -4%, vs defensa débil +4%; rebotes: vs defensa fuerte -5%, vs defensa media +12%, vs defensa débil -3%; asistencias: vs defensa fuerte -10%, vs defensa media -11%, vs defensa débil +23%; triples: vs defensa fuerte -6%, vs defensa media +1%, vs defensa débil +7%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 51% | 32% | 35% | 37% |
| pintura | 21% | 43% | 45% | 43% |
| media distancia | 12% | 42% | 41% | 43% |
| bajo el aro | 9% | 72% | 68% | 67% |
| triple de esquina | 7% | 38% | 38% | 37% |

#### Leonard Miller (aleros/ala-pívots) vs Boston Celtics

- Minutos esperados: **24.4** (± 4.2); 49 partidos en la base.
- Su prop más probable hoy: **Leonard Miller: menos de 1.5 robos+tapones** (63%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Boston Celtics contra aleros/ala-pívots en robos+tapones: -23% respecto a la media; ajuste por su historial contra defensas similares: +1%.

**¿Por qué 0.9 robos+tapones?** (línea 1.5; 24.4 minutos esperados)

- Robos **0.5** (por componentes 0.5 · por tasa por minuto y defensa rival 0.5): roba el 9.6% de las pérdidas del rival en pista × 10.3 pérdidas esperadas del rival.
- Tapones **0.4** (por componentes 0.4 · por tasa por minuto y defensa rival 0.4): tapona el 1.7% de los tiros de 2 del rival en pista × 50.9 tiros de 2 esperados del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 29.0 | 29.2 | 23.7 | 15.7 | 7.0 |
| Robos | 1.0 | 0.6 | 0.7 | 0.4 | 0.0 |
| % de las pérdidas del rival que roba | 11.1% | 6.6% | 9.7% | 8.3% | 0.0% |
| Tapones | 0.6 | 0.7 | 0.3 | 0.3 | 0.0 |
| % de los tiros de 2 del rival que tapona | 1.8% | 2.1% | 1.2% | 1.8% | 0.0% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -7%, vs defensa media +11%, vs defensa débil +3%; rebotes: vs defensa fuerte +10%, vs defensa media -20%, vs defensa débil +10%; asistencias: vs defensa fuerte +9%, vs defensa media -13%, vs defensa débil +2%; triples: vs defensa fuerte -12%, vs defensa media -14%, vs defensa débil +39%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 50% | 73% | 68% | 66% |
| triple frontal | 23% | 28% | 35% | 36% |
| triple de esquina | 16% | 39% | 38% | 37% |
| pintura | 8% | 42% | 45% | 43% |
| media distancia | 2% | 41% | 41% | 42% |

## Dallas Mavericks @ Miami Heat

Parte de lesiones: Caleb Martin (Out); Naji Marshall (Out); Santi Aldama (Out); Cooper Flagg (Out); Tarik Biberovic (Out).

Las 8 más probables (máximo 2 por jugador: las de un mismo jugador suelen ganar o perder juntas).

| Prop | Prob. final | Modelo | Casa | Esperado | Últ. 10 | Temporada | vs este rival | Cuota (implícita) |
|---|---|---|---|---|---|---|---|---|
| **Giannis Antetokounmpo: más de 0.5 robos** | **66%** | 66% | 66% | 1.1 ± 1.0 | 7/10 | 3/3 | 1 | 1.40 (71%) |
| **Daniel Gafford: más de 0.5 tapones** | **63%** | 64% | 62% | 1.0 ± 1.0 | 9/10 | 3/3 | 0, 2 | 1.49 (67%) |
| **Tim Hardaway Jr.: más de 1.5 rebotes** | **62%** | 67% | 60% | 2.6 ± 1.8 | 7/10 | 2/3 | 1, 3, 2, 1 | 1.56 (64%) |
| **Giannis Antetokounmpo: menos de 37.5 pts+ast** | **62%** | 80% | 52% | 29.1 ± 8.4 | 8/10 | 2/3 | 36 | 1.80 (56%) |
| **Pelle Larsson: más de 0.5 triples** | **62%** | 60% | 63% | 1.0 ± 1.0 | 6/10 | 2/3 | 0, 1 | 1.50 (67%) |
| **Davion Mitchell: más de 0.5 robos** | **61%** | 57% | 64% | 0.9 ± 1.0 | 3/10 | 1/3 | 0, 2 | 1.44 (70%) |
| **Davion Mitchell: más de 10.5 puntos** | **61%** | 77% | 52% | 15.2 ± 5.1 | 8/10 | 3/3 | 4, 8 | 1.80 (56%) |
| **P.J. Washington: más de 1.5 asistencias** | **61%** | 61% | 61% | 2.3 ± 1.5 | 4/10 | 2/3 | 1 | 1.53 (66%) |

### Fichas de los jugadores destacados

#### Giannis Antetokounmpo (aleros/ala-pívots) vs Dallas Mavericks

- Minutos esperados: **28.7** (± 3.5); 39 partidos en la base.
- cambio de rol esta temporada (por minuto): ast -46%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Giannis Antetokounmpo: más de 0.5 robos** (66%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Dallas Mavericks contra aleros/ala-pívots en robos: -3% respecto a la media; ajuste por su historial contra defensas similares: -1%.

**¿Por qué 1.1 robos?** (línea 0.5; 28.7 minutos esperados)

- Robos **1.1** (por componentes 1.1 · por tasa por minuto y defensa rival 1.0): roba el 12.9% de las pérdidas del rival en pista × 14.6 pérdidas esperadas del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 28.0 | 28.2 | 29.3 | 28.9 | 37.0 |
| Robos | 1.0 | 1.1 | 1.3 | 0.9 | 1.0 |
| % de las pérdidas del rival que roba | 11.0% | 14.7% | 13.3% | 12.8% | 9.3% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -5%, vs defensa media -0%, vs defensa débil +4%; rebotes: vs defensa fuerte -14%, vs defensa media +3%, vs defensa débil +18%; asistencias: vs defensa fuerte -18%, vs defensa media +20%, vs defensa débil -1%; triples: vs defensa fuerte +55%, vs defensa media -6%, vs defensa débil -35%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 60% | 77% | 68% | 69% |
| pintura | 17% | 48% | 45% | 45% |
| media distancia | 14% | 31% | 41% | 42% |
| triple frontal | 8% | 32% | 35% | 35% |
| triple de esquina | 0% | 39% | 38% | 37% |

#### Daniel Gafford (aleros/ala-pívots) vs Miami Heat

- Minutos esperados: **20.9** (± 3.9); 58 partidos en la base.
- sin Naji Marshall (5 partidos): 20.8 min vs 21.7 con él; pts +6%/min, ast +29%/min
- sin Cooper Flagg (10 partidos): 22.4 min vs 21.4 con él; reb -8%/min, ast +7%/min
- cambio de rol esta temporada (por minuto): pts -32%, ast +174%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Daniel Gafford: más de 0.5 tapones** (63%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Miami Heat contra aleros/ala-pívots en tapones: -1% respecto a la media; ajuste por su historial contra defensas similares: +5%.

**¿Por qué 1.0 tapones?** (línea 0.5; 20.9 minutos esperados)

- Tapones **1.0** (por componentes 0.9 · por tasa por minuto y defensa rival 1.0): tapona el 5.0% de los tiros de 2 del rival en pista × 60.2 tiros de 2 esperados del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 20.0 | 21.4 | 20.0 | 21.7 | 21.0 |
| Tapones | 2.0 | 1.4 | 2.0 | 1.3 | 1.0 |
| % de los tiros de 2 del rival que tapona | 8.3% | 5.7% | 8.7% | 4.9% | 3.5% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +10%, vs defensa media -5%, vs defensa débil -10%; rebotes: vs defensa fuerte +0%, vs defensa media +2%, vs defensa débil -2%; asistencias: vs defensa fuerte +22%, vs defensa media -17%, vs defensa débil -18%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 73% | 71% | 68% | 67% |
| pintura | 24% | 44% | 45% | 46% |
| media distancia | 3% | 43% | 41% | 41% |
| triple frontal | 1% | 35% | 35% | 35% |
| triple de esquina | 0% | 38% | 38% | 39% |

#### Tim Hardaway Jr. (bases/escoltas) vs Dallas Mavericks

- Minutos esperados: **20.5** (± 3.0); 88 partidos en la base.
- cambio de rol esta temporada (por minuto): pts -47%, reb +35%, ast -32%, tpm -51%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Tim Hardaway Jr.: más de 1.5 rebotes** (62%). Con 80% de probabilidad: más de 0.5 / menos de 4.5.
- Defensa de Dallas Mavericks contra bases/escoltas en rebotes: +9% respecto a la media; ajuste por su historial contra defensas similares: -1%.

**¿Por qué 2.6 rebotes?** (línea 1.5; 20.5 minutos esperados)

- Rebotes **2.6** (por componentes 2.6 · por tasa por minuto y defensa rival 2.6): defensivos 2.2 = captura el 10.3% de los fallos del rival en pista × 49.8 fallos esperados del rival (liga 47.0) × 43% del partido; ofensivos 0.4 = 1.9% de los fallos de su equipo × 51.2.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 20.0 | 22.6 | 20.0 | 26.5 | 30.8 |
| Rebotes | 2.6 | 2.9 | 2.7 | 2.6 | 1.8 |
| % de los fallos del rival que captura | 10.1% | 10.4% | 11.7% | 9.0% | 5.9% |
| % de los fallos de su equipo que captura | 2.9% | 2.2% | 1.5% | 1.0% | 0.0% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -7%, vs defensa media +1%, vs defensa débil +5%; rebotes: vs defensa fuerte -11%, vs defensa media +14%, vs defensa débil -3%; asistencias: vs defensa fuerte -13%, vs defensa media +18%, vs defensa débil +8%; triples: vs defensa fuerte -8%, vs defensa media +5%, vs defensa débil +8%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 56% | 38% | 35% | 35% |
| triple de esquina | 14% | 40% | 38% | 37% |
| media distancia | 11% | 48% | 41% | 42% |
| pintura | 9% | 45% | 45% | 45% |
| bajo el aro | 9% | 65% | 68% | 69% |

#### Pelle Larsson (bases/escoltas) vs Dallas Mavericks

- Minutos esperados: **30.2** (± 5.0); 74 partidos en la base.
- cambio de rol esta temporada (por minuto): pts -37%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Pelle Larsson: más de 0.5 triples** (62%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Dallas Mavericks contra bases/escoltas en triples: -3% respecto a la media; ajuste por su historial contra defensas similares: -5%.

**¿Por qué 1.0 triples?** (línea 0.5; 30.2 minutos esperados)

- Triples **1.0** (por componentes 1.1 · por tasa por minuto y defensa rival 1.0): 3.5 triples intentados (su ritmo 4.2 por 36'; el rival concede -6% de triples en su reparto) × 32% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 27.6 | 29.4 | 29.7 | 26.4 | 25.5 |
| Triples anotados | 0.6 | 0.8 | 0.7 | 0.9 | 0.5 |
| Triples intentados | 2.4 | 3.1 | 2.7 | 2.7 | 3.5 |
| % triples | 25.0% | 25.8% | 25.0% | 32.1% | 14.3% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -1%, vs defensa media -9%, vs defensa débil +11%; rebotes: vs defensa fuerte -6%, vs defensa media +4%, vs defensa débil +3%; asistencias: vs defensa fuerte -19%, vs defensa media -6%, vs defensa débil +31%; triples: vs defensa fuerte -28%, vs defensa media +24%, vs defensa débil +17%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 37% | 70% | 68% | 69% |
| pintura | 25% | 44% | 45% | 45% |
| triple frontal | 25% | 31% | 35% | 35% |
| triple de esquina | 10% | 38% | 38% | 37% |
| media distancia | 3% | 35% | 41% | 42% |

#### Davion Mitchell (bases/escoltas) vs Dallas Mavericks

- Minutos esperados: **34.6** (± 3.7); 74 partidos en la base.
- cambio de rol esta temporada (por minuto): pts +49%, reb -69%, tpm +48%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Davion Mitchell: más de 0.5 robos** (61%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Dallas Mavericks contra bases/escoltas en robos: +8% respecto a la media; ajuste por su historial contra defensas similares: +2%.

**¿Por qué 0.9 robos?** (línea 0.5; 34.6 minutos esperados)

- Robos **0.9** (por componentes 0.9 · por tasa por minuto y defensa rival 0.9): roba el 8.8% de las pérdidas del rival en pista × 14.6 pérdidas esperadas del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 35.4 | 33.3 | 34.3 | 28.8 | 31.0 |
| Robos | 0.8 | 0.4 | 0.3 | 1.0 | 1.0 |
| % de las pérdidas del rival que roba | 8.2% | 5.4% | 2.9% | 11.8% | 10.6% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +5%, vs defensa media -0%, vs defensa débil -9%; rebotes: vs defensa fuerte -9%, vs defensa media -19%, vs defensa débil +34%; asistencias: vs defensa fuerte +5%, vs defensa media -4%, vs defensa débil -2%; triples: vs defensa fuerte -19%, vs defensa media +11%, vs defensa débil +22%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 37% | 40% | 35% | 35% |
| pintura | 26% | 49% | 45% | 45% |
| bajo el aro | 25% | 66% | 68% | 69% |
| media distancia | 6% | 40% | 41% | 42% |
| triple de esquina | 5% | 37% | 38% | 37% |

## Indiana Pacers @ Milwaukee Bucks

Parte de lesiones: T.J. McConnell (Out); Ivica Zubac (Day-To-Day); Ben Sheppard (Out); Johnny Furphy (Out).

Las 8 más probables (máximo 2 por jugador: las de un mismo jugador suelen ganar o perder juntas).

| Prop | Prob. final | Modelo | Casa | Esperado | Últ. 10 | Temporada | vs este rival | Cuota (implícita) |
|---|---|---|---|---|---|---|---|---|
| **Jaime Jaquez Jr.: más de 0.5 triples** | **69%** | 74% | 65% | 1.3 ± 1.2 | 9/10 | 3/3 | 2, 0, 1 | 1.43 (70%) |
| **Kasparas Jakucionis: menos de 1.5 triples** | **65%** | 64% | 65% | 1.2 ± 1.2 | 6/10 | 3/3 | 1, 0, 0 | 1.44 (70%) |
| **Ryan Rollins: menos de 1.5 robos** | **65%** | 69% | 63% | 1.0 ± 1.0 | 6/10 | 3/3 | 3, 0, 1, 1 | 1.43 (70%) |
| **Kyle Kuzma: menos de 1.5 triples** | **63%** | 61% | 64% | 1.4 ± 1.3 | 7/10 | 2/3 | 2, 1, 1 | 1.46 (68%) |
| **Kel'el Ware: más de 0.5 triples** | **63%** | 65% | 62% | 1.0 ± 1.1 | 9/10 | 2/3 | 1, 0, 1 | 1.50 (67%) |
| **Andrew Nembhard: menos de 1.5 robos** | **62%** | 73% | 55% | 1.0 ± 1.0 | 9/10 | 3/3 | 1, 1 | 2.00 (50%) |
| **Jaime Jaquez Jr.: menos de 1.5 robos+tapones** | **61%** | 81% | 50% | 0.8 ± 1.0 | 10/10 | 3/3 | 0, 1, 1 | 2.00 (50%) |
| **Aaron Nesmith: menos de 1.5 robos+tapones** | **61%** | 82% | 50% | 0.7 ± 0.8 | 10/10 | 2/2 | 1, 2, 1 | 2.00 (50%) |

### Fichas de los jugadores destacados

#### Jaime Jaquez Jr. (aleros/ala-pívots) vs Indiana Pacers

- Minutos esperados: **30.8** (± 3.9); 79 partidos en la base.
- cambio de rol esta temporada (por minuto): reb +59%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Jaime Jaquez Jr.: más de 0.5 triples** (69%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Indiana Pacers contra aleros/ala-pívots en triples: -3% respecto a la media; ajuste por su historial contra defensas similares: -1%.

**¿Por qué 1.3 triples?** (línea 0.5; 30.8 minutos esperados)

- Triples **1.3** (por componentes 1.1 · por tasa por minuto y defensa rival 1.4): 3.3 triples intentados (su ritmo 4.2 por 36'; el rival concede -9% de triples en su reparto) × 34% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 32.0 | 30.8 | 31.0 | 28.5 | 26.7 |
| Triples anotados | 1.6 | 1.7 | 1.7 | 0.8 | 1.0 |
| Triples intentados | 3.6 | 3.8 | 3.0 | 2.5 | 2.0 |
| % triples | 44.4% | 44.7% | 55.6% | 31.7% | 50.0% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -17%, vs defensa media +13%, vs defensa débil +7%; rebotes: vs defensa fuerte -9%, vs defensa media -3%, vs defensa débil +16%; asistencias: vs defensa fuerte -17%, vs defensa media +9%, vs defensa débil +7%; triples: vs defensa fuerte -21%, vs defensa media -12%, vs defensa débil +28%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| pintura | 39% | 44% | 45% | 47% |
| bajo el aro | 32% | 69% | 68% | 68% |
| triple frontal | 14% | 30% | 35% | 34% |
| media distancia | 7% | 50% | 41% | 44% |
| triple de esquina | 7% | 42% | 38% | 40% |

#### Kasparas Jakucionis (bases/escoltas) vs Indiana Pacers

- Minutos esperados: **24.0** (± 3.3); 56 partidos en la base.
- cambio de rol esta temporada (por minuto): pts +33%, tpm -61%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Kasparas Jakucionis: menos de 1.5 triples** (65%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Indiana Pacers contra bases/escoltas en triples: -4% respecto a la media; ajuste por su historial contra defensas similares: +1%.

**¿Por qué 1.2 triples?** (línea 1.5; 24.0 minutos esperados)

- Triples **1.2** (por componentes 1.3 · por tasa por minuto y defensa rival 1.2): 3.3 triples intentados (su ritmo 5.4 por 36'; el rival concede -9% de triples en su reparto) × 38% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 25.0 | 20.6 | 24.7 | 17.9 | 14.7 |
| Triples anotados | 1.4 | 1.2 | 0.7 | 1.2 | 0.3 |
| Triples intentados | 3.0 | 3.0 | 2.7 | 2.9 | 2.0 |
| % triples | 46.7% | 40.0% | 25.0% | 42.3% | 16.7% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +1%, vs defensa media -26%, vs defensa débil +15%; rebotes: vs defensa fuerte -28%, vs defensa media +16%, vs defensa débil +1%; asistencias: vs defensa fuerte -10%, vs defensa media -20%, vs defensa débil +17%; triples: vs defensa fuerte -15%, vs defensa media -4%, vs defensa débil +26%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 42% | 34% | 35% | 34% |
| bajo el aro | 25% | 63% | 68% | 68% |
| triple de esquina | 19% | 48% | 38% | 40% |
| pintura | 11% | 41% | 45% | 47% |
| media distancia | 2% | 38% | 41% | 44% |

#### Ryan Rollins (bases/escoltas) vs Indiana Pacers

- Minutos esperados: **28.1** (± 4.5); 77 partidos en la base.
- cambio de rol esta temporada (por minuto): reb +44%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Ryan Rollins: menos de 1.5 robos** (65%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Indiana Pacers contra bases/escoltas en robos: +1% respecto a la media; ajuste por su historial contra defensas similares: +0%.

**¿Por qué 1.0 robos?** (línea 1.5; 28.1 minutos esperados)

- Robos **1.0** (por componentes 1.0 · por tasa por minuto y defensa rival 1.1): roba el 14.2% de las pérdidas del rival en pista × 12.3 pérdidas esperadas del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 29.6 | 30.0 | 27.7 | 32.1 | 33.0 |
| Robos | 1.0 | 1.4 | 0.7 | 1.5 | 1.2 |
| % de las pérdidas del rival que roba | 12.9% | 17.2% | 9.4% | 18.1% | 14.3% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -3%, vs defensa media +1%, vs defensa débil +3%; rebotes: vs defensa fuerte -10%, vs defensa media +6%, vs defensa débil +6%; asistencias: vs defensa fuerte -5%, vs defensa media +5%, vs defensa débil -0%; triples: vs defensa fuerte -4%, vs defensa media +2%, vs defensa débil +4%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 34% | 40% | 35% | 34% |
| bajo el aro | 22% | 68% | 68% | 68% |
| pintura | 20% | 38% | 45% | 47% |
| media distancia | 14% | 45% | 41% | 44% |
| triple de esquina | 10% | 38% | 38% | 40% |

#### Kyle Kuzma (aleros/ala-pívots) vs Indiana Pacers

- Minutos esperados: **30.2** (± 4.3); 72 partidos en la base.
- cambio de rol esta temporada (por minuto): reb +70%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Kyle Kuzma: menos de 1.5 triples** (63%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Indiana Pacers contra aleros/ala-pívots en triples: -3% respecto a la media; ajuste por su historial contra defensas similares: +2%.

**¿Por qué 1.4 triples?** (línea 1.5; 30.2 minutos esperados)

- Triples **1.4** (por componentes 1.4 · por tasa por minuto y defensa rival 1.4): 4.0 triples intentados (su ritmo 5.1 por 36'; el rival concede -9% de triples en su reparto) × 35% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 27.0 | 24.3 | 30.7 | 26.2 | 29.0 |
| Triples anotados | 0.8 | 1.0 | 1.0 | 1.2 | 1.3 |
| Triples intentados | 2.6 | 3.8 | 4.0 | 3.5 | 4.0 |
| % triples | 30.8% | 26.3% | 25.0% | 34.7% | 33.3% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +13%, vs defensa media -13%, vs defensa débil +3%; rebotes: vs defensa fuerte -11%, vs defensa media -7%, vs defensa débil +13%; asistencias: vs defensa fuerte -38%, vs defensa media -8%, vs defensa débil +37%; triples: vs defensa fuerte +28%, vs defensa media -41%, vs defensa débil +25%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 35% | 69% | 68% | 68% |
| pintura | 23% | 41% | 45% | 47% |
| triple frontal | 23% | 33% | 35% | 34% |
| triple de esquina | 12% | 37% | 38% | 40% |
| media distancia | 7% | 44% | 41% | 44% |

#### Kel'el Ware (pívots) vs Indiana Pacers

- Minutos esperados: **21.2** (± 7.9); 81 partidos en la base.
- Su prop más probable hoy: **Kel'el Ware: más de 0.5 triples** (63%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Indiana Pacers contra pívots en triples: -6% respecto a la media; ajuste por su historial contra defensas similares: -1%.

**¿Por qué 1.0 triples?** (línea 0.5; 21.2 minutos esperados)

- Triples **1.0** (por componentes 0.9 · por tasa por minuto y defensa rival 1.0): 2.5 triples intentados (su ritmo 4.5 por 36'; el rival concede -9% de triples en su reparto) × 38% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 25.8 | 22.8 | 19.3 | 22.4 | 20.3 |
| Triples anotados | 1.8 | 1.8 | 1.0 | 1.2 | 0.7 |
| Triples intentados | 4.2 | 3.8 | 2.7 | 3.1 | 2.0 |
| % triples | 42.9% | 47.4% | 37.5% | 39.0% | 33.3% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -10%, vs defensa media -8%, vs defensa débil +16%; rebotes: vs defensa fuerte -7%, vs defensa media +1%, vs defensa débil +8%; asistencias: vs defensa fuerte -19%, vs defensa media -12%, vs defensa débil +30%; triples: vs defensa fuerte -36%, vs defensa media +36%, vs defensa débil +15%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 47% | 70% | 68% | 68% |
| triple frontal | 27% | 36% | 35% | 34% |
| pintura | 15% | 39% | 45% | 47% |
| triple de esquina | 10% | 42% | 38% | 40% |
| media distancia | 2% | 38% | 41% | 44% |

## Phoenix Suns @ Oklahoma City Thunder

Parte de lesiones: Jaylin Williams (Day-To-Day); Jalen Williams (Out); Oso Ighodaro (Day-To-Day); Cason Wallace (Day-To-Day); Mark Williams (Out); Otega Oweh (Out); Nikola Topic (Out).

Las 8 más probables (máximo 2 por jugador: las de un mismo jugador suelen ganar o perder juntas).

| Prop | Prob. final | Modelo | Casa | Esperado | Últ. 10 | Temporada | vs este rival | Cuota (implícita) |
|---|---|---|---|---|---|---|---|---|
| **Ajay Mitchell: menos de 0.5 tapones** | **72%** | 80% | 68% | 0.2 ± 0.4 | 8/10 | 2/3 | 0, 0, 0, 0, 0 | 1.36 (73%) |
| **Ajay Mitchell: menos de 1.5 triples** | **66%** | 70% | 65% | 1.1 ± 1.1 | 9/10 | 3/3 | 4, 1, 1, 3, 1 | 1.44 (69%) |
| **Collin Gillespie: menos de 2.5 triples** | **64%** | 67% | 62% | 2.0 ± 1.7 | 9/10 | 2/2 | 6, 1, 1, 2, 2 | 1.51 (66%) |
| **Cason Wallace: menos de 0.5 tapones** | **63%** | 72% | 58% | 0.3 ± 0.5 | 8/10 | 3/3 | 1, 1, 0, 0, 0 | 1.57 (64%) |
| **Collin Gillespie: menos de 1.5 robos** | **62%** | 63% | 61% | 1.3 ± 1.3 | 7/10 | 0/2 | 1, 1, 2, 1, 0 | 1.51 (66%) |
| **Khaman Maluach: menos de 0.5 triples** | **61%** | 68% | 58% | 0.4 ± 0.7 | 8/10 | 1/2 | 0, 0, 0, 0, 2 | 1.62 (62%) |
| **Khaman Maluach: menos de 1.5 tapones** | **61%** | 66% | 58% | 1.1 ± 1.1 | 7/10 | 1/2 | 0, 0, 0, 0, 2 | 1.60 (63%) |
| **Luke Kennard: menos de 1.5 triples** | **60%** | 55% | 63% | 1.6 ± 1.5 | 6/10 | 0/1 | 1, 4, 2, 1, 0 | 1.48 (68%) |

### Fichas de los jugadores destacados

#### Ajay Mitchell (bases/escoltas) vs Phoenix Suns

- Minutos esperados: **27.4** (± 3.2); 71 partidos en la base.
- sin Jalen Williams (36 partidos): 27.4 min vs 25.0 con él; pts +20%/min
- cambio de rol esta temporada (por minuto): tpm -67%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Ajay Mitchell: menos de 0.5 tapones** (72%). Con 80% de probabilidad: más de - / menos de 0.5.
- Defensa de Phoenix Suns contra bases/escoltas en tapones: -18% respecto a la media; ajuste por su historial contra defensas similares: -6%.

**¿Por qué 0.2 tapones?** (línea 0.5; 27.4 minutos esperados)

- Tapones **0.2** (por componentes 0.2 · por tasa por minuto y defensa rival 0.2): tapona el 1.1% de los tiros de 2 del rival en pista × 46.3 tiros de 2 esperados del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 23.8 | 27.4 | 24.7 | 26.3 | 28.8 |
| Tapones | 0.4 | 0.2 | 0.3 | 0.3 | 0.0 |
| % de los tiros de 2 del rival que tapona | 1.7% | 0.7% | 1.3% | 1.1% | 0.0% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -19%, vs defensa media +10%, vs defensa débil +4%; rebotes: vs defensa fuerte -3%, vs defensa media +10%, vs defensa débil -11%; asistencias: vs defensa fuerte -5%, vs defensa media +2%, vs defensa débil +4%; triples: vs defensa fuerte -16%, vs defensa media +48%, vs defensa débil -4%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| pintura | 34% | 48% | 45% | 45% |
| bajo el aro | 28% | 67% | 68% | 69% |
| triple frontal | 21% | 32% | 35% | 35% |
| media distancia | 9% | 37% | 41% | 41% |
| triple de esquina | 8% | 39% | 38% | 37% |

#### Collin Gillespie (bases/escoltas) vs Oklahoma City Thunder

- Minutos esperados: **25.2** (± 4.1); 88 partidos en la base.
- Mark Williams ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- cambio de rol esta temporada (por minuto): pts -49%, ast +41%, tpm -59%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Collin Gillespie: menos de 2.5 triples** (64%). Con 80% de probabilidad: más de 0.5 / menos de 3.5.
- Defensa de Oklahoma City Thunder contra bases/escoltas en triples: +2% respecto a la media; ajuste por su historial contra defensas similares: +2%.

**¿Por qué 2.0 triples?** (línea 2.5; 25.2 minutos esperados)

- Triples **2.0** (por componentes 2.3 · por tasa por minuto y defensa rival 1.9): 5.9 triples intentados (su ritmo 8.2 por 36'; el rival concede +5% de triples en su reparto) × 39% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 28.0 | 25.0 | 24.5 | 28.2 | 27.4 |
| Triples anotados | 2.0 | 1.5 | 1.0 | 2.8 | 2.4 |
| Triples intentados | 6.8 | 5.3 | 6.5 | 7.1 | 5.8 |
| % triples | 29.4% | 28.3% | 15.4% | 40.0% | 41.4% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +5%, vs defensa media -1%, vs defensa débil -4%; rebotes: vs defensa fuerte -14%, vs defensa media -2%, vs defensa débil +17%; asistencias: vs defensa fuerte -16%, vs defensa media -11%, vs defensa débil +25%; triples: vs defensa fuerte +4%, vs defensa media -17%, vs defensa débil +9%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 59% | 38% | 35% | 35% |
| pintura | 14% | 47% | 45% | 41% |
| media distancia | 11% | 41% | 41% | 39% |
| triple de esquina | 10% | 41% | 38% | 38% |
| bajo el aro | 7% | 60% | 68% | 62% |

#### Cason Wallace (bases/escoltas) vs Phoenix Suns

- Minutos esperados: **20.3** (± 8.7); 95 partidos en la base.
- en el parte de lesiones: day-to-day
- sin Jalen Williams (55 partidos): 27.6 min vs 23.8 con él; pts +14%/min, reb -21%/min, ast +33%/min
- Su prop más probable hoy: **Cason Wallace: menos de 0.5 tapones** (63%). Con 80% de probabilidad: más de - / menos de 1.5.
- Defensa de Phoenix Suns contra bases/escoltas en tapones: -18% respecto a la media; ajuste por su historial contra defensas similares: +0%.

**¿Por qué 0.3 tapones?** (línea 0.5; 20.3 minutos esperados)

- Tapones **0.3** (por componentes 0.3 · por tasa por minuto y defensa rival 0.3): tapona el 1.2% de los tiros de 2 del rival en pista × 46.3 tiros de 2 esperados del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 21.0 | 23.8 | 16.3 | 26.3 | 23.2 |
| Tapones | 0.2 | 0.3 | 0.0 | 0.4 | 0.4 |
| % de los tiros de 2 del rival que tapona | 0.9% | 1.3% | 0.0% | 1.4% | 1.7% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +9%, vs defensa media -4%, vs defensa débil -8%; rebotes: vs defensa fuerte -10%, vs defensa media +5%, vs defensa débil +9%; asistencias: vs defensa fuerte +2%, vs defensa media -4%, vs defensa débil +1%; triples: vs defensa fuerte -3%, vs defensa media -7%, vs defensa débil +16%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 33% | 36% | 35% | 35% |
| bajo el aro | 31% | 63% | 68% | 69% |
| triple de esquina | 18% | 39% | 38% | 37% |
| pintura | 15% | 35% | 45% | 45% |
| media distancia | 3% | 40% | 41% | 41% |

#### Khaman Maluach (pívots) vs Oklahoma City Thunder

- Minutos esperados: **21.1** (± 7.4); 53 partidos en la base.
- Mark Williams ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Su prop más probable hoy: **Khaman Maluach: menos de 0.5 triples** (61%). Con 80% de probabilidad: más de - / menos de 1.5.
- Defensa de Oklahoma City Thunder contra pívots en triples: +1% respecto a la media; ajuste por su historial contra defensas similares: -1%.

**¿Por qué 0.4 triples?** (línea 0.5; 21.1 minutos esperados)

- Triples **0.4** (por componentes 0.4 · por tasa por minuto y defensa rival 0.4): 1.2 triples intentados (su ritmo 2.1 por 36'; el rival concede +5% de triples en su reparto) × 34% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 15.2 | 16.3 | 22.5 | 9.0 | 15.0 |
| Triples anotados | 0.2 | 0.3 | 0.5 | 0.1 | 0.4 |
| Triples intentados | 0.6 | 1.0 | 1.0 | 0.5 | 1.2 |
| % triples | 33.3% | 30.0% | 50.0% | 21.7% | 33.3% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +6%, vs defensa media +3%, vs defensa débil -10%; rebotes: vs defensa fuerte -14%, vs defensa media +4%, vs defensa débil +17%; asistencias: vs defensa fuerte -18%, vs defensa media +27%, vs defensa débil +1%; triples: vs defensa fuerte +6%, vs defensa media -22%, vs defensa débil +30%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 60% | 67% | 68% | 62% |
| triple frontal | 16% | 32% | 35% | 35% |
| pintura | 14% | 42% | 45% | 41% |
| triple de esquina | 8% | 38% | 38% | 38% |
| media distancia | 2% | 42% | 41% | 39% |

#### Luke Kennard (bases/escoltas) vs Oklahoma City Thunder

- Minutos esperados: **21.8** (± 6.0); 89 partidos en la base.
- Mark Williams ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- solo 1 partidos con su equipo actual: su rol puede haber cambiado, se da más peso a la línea de la casa
- Su prop más probable hoy: **Luke Kennard: menos de 1.5 triples** (60%). Con 80% de probabilidad: más de - / menos de 3.5.
- Defensa de Oklahoma City Thunder contra bases/escoltas en triples: +2% respecto a la media; ajuste por su historial contra defensas similares: -0%.

**¿Por qué 1.6 triples?** (línea 1.5; 21.8 minutos esperados)

- Triples **1.6** (por componentes 1.7 · por tasa por minuto y defensa rival 1.6): 3.6 triples intentados (su ritmo 5.8 por 36'; el rival concede +5% de triples en su reparto) × 46% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 25.2 | 30.5 | 18.0 | 22.8 | 26.2 |
| Triples anotados | 2.2 | 1.6 | 3.0 | 1.5 | 1.6 |
| Triples intentados | 3.8 | 3.8 | 5.0 | 3.2 | 3.2 |
| % triples | 57.9% | 42.1% | 60.0% | 47.7% | 50.0% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -15%, vs defensa media -9%, vs defensa débil +32%; rebotes: vs defensa fuerte -16%, vs defensa media -8%, vs defensa débil +23%; asistencias: vs defensa fuerte -7%, vs defensa media +3%, vs defensa débil +13%; triples: vs defensa fuerte -22%, vs defensa media +1%, vs defensa débil +20%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 38% | 45% | 35% | 35% |
| pintura | 21% | 53% | 45% | 41% |
| triple de esquina | 17% | 46% | 38% | 38% |
| bajo el aro | 13% | 65% | 68% | 62% |
| media distancia | 12% | 50% | 41% | 39% |

## Atlanta Hawks @ Houston Rockets

Parte de lesiones: Marcus Smart (Day-To-Day); Steven Adams (Out); Mouhamed Gueye (Out); Henri Veesaar (Out).

Las 8 más probables (máximo 2 por jugador: las de un mismo jugador suelen ganar o perder juntas).

| Prop | Prob. final | Modelo | Casa | Esperado | Últ. 10 | Temporada | vs este rival | Cuota (implícita) |
|---|---|---|---|---|---|---|---|---|
| **CJ McCollum: menos de 3.5 asistencias** | **63%** | 67% | 60% | 2.7 ± 1.8 | 8/10 | 3/3 | 1, 2, 2, 3 | 1.54 (65%) |
| **Jabari Smith Jr.: más de 1.5 triples** | **63%** | 68% | 60% | 2.3 ± 1.5 | 8/10 | 2/3 | 2, 3, 2 | 1.56 (64%) |
| **Kevin Durant: más de 1.5 triples** | **63%** | 71% | 58% | 2.5 ± 1.6 | 8/10 | 3/3 | 3, 3, 3 | 1.62 (62%) |
| **Kevin Durant: más de 8.5 reb+ast** | **62%** | 75% | 55% | 10.9 ± 3.4 | 8/10 | 2/3 | 6, 9, 9 | 1.69 (59%) |
| **Alperen Sengun: más de 0.5 tapones** | **62%** | 67% | 59% | 1.2 ± 1.1 | 8/10 | 1/3 | 0, 0, 3 | 1.56 (64%) |
| **Onyeka Okongwu: menos de 6.5 rebotes** | **60%** | 69% | 55% | 5.0 ± 2.3 | 7/10 | 3/3 | 6, 8 | 1.70 (59%) |
| **Jalen Johnson: menos de 1.5 robos** | **60%** | 62% | 58% | 1.4 ± 1.2 | 6/10 | 1/3 | 2, 1 | 1.69 (59%) |
| **Luguentz Dort: menos de 1.5 triples** | **60%** | 62% | 58% | 1.4 ± 1.2 | 9/10 | 2/3 | 1, 0, 3, 0 | 1.61 (62%) |

### Fichas de los jugadores destacados

#### CJ McCollum (bases/escoltas) vs Houston Rockets

- Minutos esperados: **26.5** (± 3.8); 85 partidos en la base.
- cambio de rol esta temporada (por minuto): reb -41%, ast -37%; se da más peso a la línea de la casa
- Su prop más probable hoy: **CJ McCollum: menos de 3.5 asistencias** (63%). Con 80% de probabilidad: más de 0.5 / menos de 4.5.
- Defensa de Houston Rockets contra bases/escoltas en asistencias: -7% respecto a la media; ajuste por su historial contra defensas similares: -3%.

**¿Por qué 2.7 asistencias?** (línea 3.5; 26.5 minutos esperados)

- Asistencias **2.7** (por componentes 2.6 · por tasa por minuto y defensa rival 2.7): asiste el 15.1% de las canastas de sus compañeros en pista × 17.5 canastas de compañeros esperadas (su equipo 41.3 por 48' contra esta defensa).

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 26.6 | 29.3 | 25.7 | 29.9 | 28.8 |
| Asistencias | 1.4 | 2.2 | 2.0 | 3.7 | 2.0 |
| % de las canastas de compañeros que asiste | 7.2% | 11.3% | 9.7% | 17.0% | 10.2% |
| Pérdidas por jugada | 14.0% | 14.2% | 10.0% | 10.2% | 10.6% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -1%, vs defensa media +4%, vs defensa débil -2%; rebotes: vs defensa fuerte -6%, vs defensa media +0%, vs defensa débil +5%; asistencias: vs defensa fuerte -19%, vs defensa media +16%, vs defensa débil +14%; triples: vs defensa fuerte +2%, vs defensa media -23%, vs defensa débil +38%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 37% | 37% | 35% | 34% |
| pintura | 23% | 48% | 45% | 46% |
| media distancia | 17% | 46% | 41% | 39% |
| bajo el aro | 16% | 66% | 68% | 67% |
| triple de esquina | 7% | 37% | 38% | 38% |

#### Jabari Smith Jr. (aleros/ala-pívots) vs Atlanta Hawks

- Minutos esperados: **36.8** (± 3.0); 86 partidos en la base.
- sin Steven Adams (54 partidos): 36.3 min vs 34.4 con él; reb -8%/min, ast +8%/min
- Su prop más probable hoy: **Jabari Smith Jr.: más de 1.5 triples** (63%). Con 80% de probabilidad: más de 0.5 / menos de 4.5.
- Defensa de Atlanta Hawks contra aleros/ala-pívots en triples: -1% respecto a la media; ajuste por su historial contra defensas similares: +3%.

**¿Por qué 2.3 triples?** (línea 1.5; 36.8 minutos esperados)

- Triples **2.3** (por componentes 2.2 · por tasa por minuto y defensa rival 2.4): 6.0 triples intentados (su ritmo 6.0 por 36'; el rival concede -2% de triples en su reparto) × 36% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 37.4 | 39.5 | 34.3 | 35.6 | 33.3 |
| Triples anotados | 2.4 | 2.8 | 2.3 | 2.4 | 2.3 |
| Triples intentados | 6.2 | 7.3 | 5.3 | 6.5 | 6.7 |
| % triples | 38.7% | 38.4% | 43.8% | 36.4% | 35.0% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -4%, vs defensa media -2%, vs defensa débil +8%; rebotes: vs defensa fuerte -5%, vs defensa media +7%, vs defensa débil -0%; asistencias: vs defensa fuerte -14%, vs defensa media +19%, vs defensa débil +0%; triples: vs defensa fuerte -10%, vs defensa media +6%, vs defensa débil +5%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 33% | 36% | 35% | 35% |
| pintura | 19% | 48% | 45% | 44% |
| triple de esquina | 18% | 38% | 38% | 37% |
| bajo el aro | 17% | 70% | 68% | 67% |
| media distancia | 14% | 39% | 41% | 42% |

#### Kevin Durant (aleros/ala-pívots) vs Atlanta Hawks

- Minutos esperados: **37.6** (± 3.0); 85 partidos en la base.
- sin Steven Adams (50 partidos): 36.7 min vs 36.2 con él; ast +17%/min
- Su prop más probable hoy: **Kevin Durant: más de 1.5 triples** (63%). Con 80% de probabilidad: más de 0.5 / menos de 4.5.
- Defensa de Atlanta Hawks contra aleros/ala-pívots en triples: -1% respecto a la media; ajuste por su historial contra defensas similares: -1%.

**¿Por qué 2.5 triples?** (línea 1.5; 37.6 minutos esperados)

- Triples **2.5** (por componentes 2.1 · por tasa por minuto y defensa rival 2.7): 5.3 triples intentados (su ritmo 5.2 por 36'; el rival concede -2% de triples en su reparto) × 40% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 38.2 | 37.1 | 37.0 | 35.5 | 33.7 |
| Triples anotados | 1.6 | 2.3 | 2.3 | 2.3 | 3.0 |
| Triples intentados | 3.6 | 4.9 | 4.3 | 5.6 | 6.7 |
| % triples | 44.4% | 46.9% | 53.8% | 40.9% | 45.0% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -3%, vs defensa media +3%, vs defensa débil +0%; rebotes: vs defensa fuerte -6%, vs defensa media -3%, vs defensa débil +10%; asistencias: vs defensa fuerte -19%, vs defensa media +1%, vs defensa débil +19%; triples: vs defensa fuerte -1%, vs defensa media +5%, vs defensa débil -5%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| pintura | 30% | 58% | 45% | 44% |
| triple frontal | 29% | 40% | 35% | 35% |
| media distancia | 29% | 48% | 41% | 42% |
| bajo el aro | 9% | 77% | 68% | 67% |
| triple de esquina | 4% | 43% | 38% | 37% |

#### Alperen Sengun (pívots) vs Atlanta Hawks

- Minutos esperados: **33.8** (± 3.2); 83 partidos en la base.
- sin Steven Adams (54 partidos): 33.0 min vs 35.2 con él; pts -5%/min
- Su prop más probable hoy: **Alperen Sengun: más de 0.5 tapones** (62%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Atlanta Hawks contra pívots en tapones: -9% respecto a la media; ajuste por su historial contra defensas similares: -4%.

**¿Por qué 1.2 tapones?** (línea 0.5; 33.8 minutos esperados)

- Tapones **1.2** (por componentes 1.4 · por tasa por minuto y defensa rival 1.1): tapona el 2.8% de los tiros de 2 del rival en pista × 51.7 tiros de 2 esperados del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 36.0 | 36.0 | 33.0 | 33.0 | 31.0 |
| Tapones | 0.8 | 1.0 | 0.3 | 1.1 | 1.0 |
| % de los tiros de 2 del rival que tapona | 2.1% | 2.7% | 1.0% | 3.0% | 3.1% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -14%, vs defensa media -6%, vs defensa débil +17%; rebotes: vs defensa fuerte -6%, vs defensa media -9%, vs defensa débil +14%; asistencias: vs defensa fuerte -0%, vs defensa media -10%, vs defensa débil +8%; triples: vs defensa fuerte -42%, vs defensa media +14%, vs defensa débil +30%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| pintura | 44% | 44% | 45% | 44% |
| bajo el aro | 36% | 70% | 68% | 67% |
| triple frontal | 11% | 33% | 35% | 35% |
| media distancia | 9% | 37% | 41% | 42% |
| triple de esquina | 1% | 39% | 38% | 37% |

#### Onyeka Okongwu (aleros/ala-pívots) vs Houston Rockets

- Minutos esperados: **26.2** (± 3.5); 83 partidos en la base.
- cambio de rol esta temporada (por minuto): ast +32%, tpm -58%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Onyeka Okongwu: menos de 6.5 rebotes** (60%). Con 80% de probabilidad: más de 2.5 / menos de 7.5.
- Defensa de Houston Rockets contra aleros/ala-pívots en rebotes: -13% respecto a la media; ajuste por su historial contra defensas similares: -1%.

**¿Por qué 5.0 rebotes?** (línea 6.5; 26.2 minutos esperados)

- Rebotes **5.0** (por componentes 5.5 · por tasa por minuto y defensa rival 4.9): defensivos 4.0 = captura el 15.8% de los fallos del rival en pista × 45.9 fallos esperados del rival (liga 47.0) × 55% del partido; ofensivos 1.5 = 5.8% de los fallos de su equipo × 47.6.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 28.6 | 30.2 | 25.7 | 31.2 | 25.0 |
| Rebotes | 5.2 | 6.0 | 5.0 | 7.5 | 7.0 |
| % de los fallos del rival que captura | 13.6% | 16.5% | 12.9% | 18.8% | 22.0% |
| % de los fallos de su equipo que captura | 6.2% | 4.7% | 6.4% | 5.9% | 7.5% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -1%, vs defensa media -6%, vs defensa débil +10%; rebotes: vs defensa fuerte -16%, vs defensa media +7%, vs defensa débil +22%; asistencias: vs defensa fuerte +11%, vs defensa media -24%, vs defensa débil +15%; triples: vs defensa fuerte -8%, vs defensa media -3%, vs defensa débil +9%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 33% | 36% | 35% | 34% |
| pintura | 27% | 47% | 45% | 46% |
| bajo el aro | 27% | 69% | 68% | 67% |
| triple de esquina | 13% | 37% | 38% | 38% |
| media distancia | 1% | 40% | 41% | 39% |

## Memphis Grizzlies @ Utah Jazz

Parte de lesiones: Jusuf Nurkic (Out); Trey Alexander (Out); Zach Edey (Day-To-Day); Karim Lopez (Day-To-Day).

Las 8 más probables (máximo 2 por jugador: las de un mismo jugador suelen ganar o perder juntas).

| Prop | Prob. final | Modelo | Casa | Esperado | Últ. 10 | Temporada | vs este rival | Cuota (implícita) |
|---|---|---|---|---|---|---|---|---|
| **Keyonte George: más de 0.5 robos** | **65%** | 67% | 65% | 1.1 ± 1.1 | 7/10 | 3/3 | 1, 1, 2 | 1.43 (70%) |
| **Jaren Jackson Jr.: menos de 1.5 robos** | **65%** | 72% | 61% | 0.9 ± 1.2 | 6/10 | 3/3 | 1 | 1.64 (61%) |
| **Zach Edey: más de 0.5 asistencias** | **64%** | 65% | 64% | 1.3 ± 1.3 | 6/10 | 1/2 | 0 | 1.43 (70%) |
| **Ty Jerome: más de 0.5 robos+tapones** | **63%** | 76% | 56% | 1.6 ± 1.3 | 7/10 | 3/3 | 1 | 1.57 (64%) |
| **Jaylen Wells: más de 2.5 rebotes** | **62%** | 73% | 56% | 4.3 ± 2.2 | 6/10 | 3/3 | 5, 3, 1, 5 | 1.66 (60%) |
| **Keyonte George: menos de 7.5 asistencias** | **62%** | 73% | 56% | 6.1 ± 2.6 | 8/10 | 1/3 | 5, 4, 8 | 1.67 (60%) |
| **Jaren Jackson Jr.: menos de 2.5 asistencias** | **62%** | 63% | 61% | 2.2 ± 1.5 | 6/10 | 2/3 | 2 | 1.51 (66%) |
| **Lauri Markkanen: menos de 2.5 asistencias** | **60%** | 58% | 61% | 2.4 ± 1.6 | 7/10 | 1/3 | 3, 2 | 1.52 (66%) |

### Fichas de los jugadores destacados

#### Keyonte George (bases/escoltas) vs Memphis Grizzlies

- Minutos esperados: **29.9** (± 3.2); 57 partidos en la base.
- Jusuf Nurkic ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- cambio de rol esta temporada (por minuto): ast +43%; se da más peso a la línea de la casa
- segundo partido en dos noches: -3% de minutos
- Su prop más probable hoy: **Keyonte George: más de 0.5 robos** (65%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Memphis Grizzlies contra bases/escoltas en robos: +9% respecto a la media; ajuste por su historial contra defensas similares: -1%.

**¿Por qué 1.1 robos?** (línea 0.5; 29.9 minutos esperados)

- Robos **1.1** (por componentes 1.2 · por tasa por minuto y defensa rival 1.1): roba el 12.9% de las pérdidas del rival en pista × 14.7 pérdidas esperadas del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 27.6 | 26.3 | 31.3 | 33.1 | 32.3 |
| Robos | 0.8 | 1.0 | 1.0 | 1.1 | 1.3 |
| % de las pérdidas del rival que roba | 12.0% | 14.1% | 12.1% | 12.2% | 15.7% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -1%, vs defensa media +5%, vs defensa débil -5%; rebotes: vs defensa fuerte -0%, vs defensa media +2%, vs defensa débil -3%; asistencias: vs defensa fuerte -6%, vs defensa media +3%, vs defensa débil +4%; triples: vs defensa fuerte +1%, vs defensa media +3%, vs defensa débil -7%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 37% | 37% | 35% | 35% |
| pintura | 29% | 48% | 45% | 46% |
| media distancia | 16% | 44% | 41% | 43% |
| bajo el aro | 14% | 70% | 68% | 70% |
| triple de esquina | 5% | 40% | 38% | 39% |

#### Jaren Jackson Jr. (aleros/ala-pívots) vs Memphis Grizzlies

- Minutos esperados: **30.2** (± 3.0); 51 partidos en la base.
- Jusuf Nurkic ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- segundo partido en dos noches: -3% de minutos
- Su prop más probable hoy: **Jaren Jackson Jr.: menos de 1.5 robos** (65%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Memphis Grizzlies contra aleros/ala-pívots en robos: +0% respecto a la media; ajuste por su historial contra defensas similares: +1%.

**¿Por qué 0.9 robos?** (línea 1.5; 30.2 minutos esperados)

- Robos **0.9** (por componentes 1.0 · por tasa por minuto y defensa rival 0.9): roba el 10.6% de las pérdidas del rival en pista × 14.7 pérdidas esperadas del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 28.2 | 29.6 | 31.3 | 30.3 | 28.0 |
| Robos | 0.8 | 1.6 | 0.3 | 1.1 | 1.0 |
| % de las pérdidas del rival que roba | 10.6% | 19.1% | 4.0% | 12.5% | 13.2% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -7%, vs defensa media +3%, vs defensa débil +7%; rebotes: vs defensa fuerte -23%, vs defensa media +16%, vs defensa débil +21%; asistencias: vs defensa fuerte -16%, vs defensa media +8%, vs defensa débil +15%; triples: vs defensa fuerte -5%, vs defensa media +6%, vs defensa débil -2%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| pintura | 42% | 51% | 45% | 46% |
| triple frontal | 24% | 35% | 35% | 35% |
| bajo el aro | 18% | 64% | 68% | 70% |
| triple de esquina | 8% | 39% | 38% | 39% |
| media distancia | 7% | 41% | 41% | 43% |

#### Zach Edey (pívots) vs Utah Jazz

- Minutos esperados: **22.5** (± 3.5); 13 partidos en la base.
- en el parte de lesiones: day-to-day
- cambio de rol esta temporada (por minuto): pts -38%, ast +65%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Zach Edey: más de 0.5 asistencias** (64%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Utah Jazz contra pívots en asistencias: +4% respecto a la media; ajuste por su historial contra defensas similares: -2%.

**¿Por qué 1.3 asistencias?** (línea 0.5; 22.5 minutos esperados)

- Asistencias **1.3** (por componentes 1.3 · por tasa por minuto y defensa rival 1.4): asiste el 8.1% de las canastas de sus compañeros en pista × 15.9 canastas de compañeros esperadas (su equipo 44.3 por 48' contra esta defensa).

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 24.8 | 25.2 | 21.5 | 25.8 | 21.0 |
| Asistencias | 1.6 | 1.3 | 1.5 | 1.1 | 0.0 |
| % de las canastas de compañeros que asiste | 8.3% | 6.8% | 8.7% | 5.6% | 0.0% |
| Pérdidas por jugada | 17.6% | 18.8% | 0.0% | 18.8% | 0.0% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa media -28%, vs defensa débil +25%; rebotes: vs defensa fuerte +3%, vs defensa media +3%, vs defensa débil -3%; asistencias: vs defensa fuerte -29%, vs defensa media -14%, vs defensa débil +23%; triples: vs defensa media +130%, vs defensa débil -100%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 49% | 70% | 68% | 73% |
| pintura | 43% | 53% | 45% | 50% |
| triple frontal | 6% | 34% | 35% | 37% |
| media distancia | 2% | 41% | 41% | 43% |
| triple de esquina | 1% | 38% | 38% | 39% |

#### Ty Jerome (bases/escoltas) vs Utah Jazz

- Minutos esperados: **30.3** (± 3.0); 18 partidos en la base.
- segundo partido en dos noches: -3% de minutos
- Su prop más probable hoy: **Ty Jerome: más de 0.5 robos+tapones** (63%). Con 80% de probabilidad: más de - / menos de 3.5.
- Defensa de Utah Jazz contra bases/escoltas en robos+tapones: +14% respecto a la media; ajuste por su historial contra defensas similares: +2%.

**¿Por qué 1.6 robos+tapones?** (línea 0.5; 30.3 minutos esperados)

- Robos **1.2** (por componentes 1.1 · por tasa por minuto y defensa rival 1.2): roba el 11.0% de las pérdidas del rival en pista × 16.4 pérdidas esperadas del rival.
- Tapones **0.4** (por componentes 0.4 · por tasa por minuto y defensa rival 0.4): tapona el 1.1% de los tiros de 2 del rival en pista × 54.0 tiros de 2 esperados del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 29.0 | 26.9 | 32.0 | 22.7 | 32.0 |
| Robos | 0.8 | 0.8 | 0.7 | 1.1 | 0.0 |
| % de las pérdidas del rival que roba | 8.7% | 9.3% | 5.9% | 15.2% | 0.0% |
| Tapones | 0.4 | 0.3 | 0.3 | 0.3 | 1.0 |
| % de los tiros de 2 del rival que tapona | 1.4% | 1.0% | 1.0% | 1.1% | 3.5% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -14%, vs defensa media -6%, vs defensa débil +14%; rebotes: vs defensa fuerte -11%, vs defensa media -12%, vs defensa débil +51%; asistencias: vs defensa fuerte -14%, vs defensa media +14%, vs defensa débil -8%; triples: vs defensa fuerte -10%, vs defensa media +15%, vs defensa débil -9%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 37% | 40% | 35% | 37% |
| pintura | 36% | 53% | 45% | 50% |
| bajo el aro | 12% | 67% | 68% | 73% |
| media distancia | 11% | 44% | 41% | 43% |
| triple de esquina | 4% | 41% | 38% | 39% |

#### Jaylen Wells (aleros/ala-pívots) vs Utah Jazz

- Minutos esperados: **27.6** (± 3.9); 72 partidos en la base.
- cambio de rol esta temporada (por minuto): reb +35%; se da más peso a la línea de la casa
- segundo partido en dos noches: -3% de minutos
- Su prop más probable hoy: **Jaylen Wells: más de 2.5 rebotes** (62%). Con 80% de probabilidad: más de 1.5 / menos de 6.5.
- Defensa de Utah Jazz contra aleros/ala-pívots en rebotes: +3% respecto a la media; ajuste por su historial contra defensas similares: +0%.

**¿Por qué 4.3 rebotes?** (línea 2.5; 27.6 minutos esperados)

- Rebotes **4.3** (por componentes 4.3 · por tasa por minuto y defensa rival 4.2): defensivos 2.8 = captura el 10.4% de los fallos del rival en pista × 47.6 fallos esperados del rival (liga 47.0) × 57% del partido; ofensivos 1.4 = 5.2% de los fallos de su equipo × 47.9.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 26.2 | 25.3 | 28.7 | 26.4 | 30.0 |
| Rebotes | 3.2 | 2.9 | 4.7 | 3.2 | 3.5 |
| % de los fallos del rival que captura | 7.4% | 7.1% | 8.4% | 8.8% | 8.2% |
| % de los fallos de su equipo que captura | 5.2% | 4.5% | 7.9% | 3.3% | 3.4% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -9%, vs defensa media +4%, vs defensa débil +6%; rebotes: vs defensa fuerte -4%, vs defensa media +0%, vs defensa débil +4%; asistencias: vs defensa fuerte -12%, vs defensa media -4%, vs defensa débil +13%; triples: vs defensa fuerte -6%, vs defensa media +8%, vs defensa débil -1%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 34% | 35% | 35% | 37% |
| bajo el aro | 18% | 62% | 68% | 73% |
| triple de esquina | 18% | 39% | 38% | 39% |
| pintura | 16% | 48% | 45% | 50% |
| media distancia | 13% | 45% | 41% | 43% |

## Golden State Warriors @ Denver Nuggets

Parte de lesiones: Kristaps Porzingis (Out); Cameron Johnson (Day-To-Day); Alpha Diallo (Day-To-Day); Brandon Williams (Day-To-Day); Charles Bassey (Day-To-Day); Moses Moody (Out); Julian Strawther (Out); Spencer Jones (Out); Gui Santos (Day-To-Day).

Las 8 más probables (máximo 2 por jugador: las de un mismo jugador suelen ganar o perder juntas).

| Prop | Prob. final | Modelo | Casa | Esperado | Últ. 10 | Temporada | vs este rival | Cuota (implícita) |
|---|---|---|---|---|---|---|---|---|
| **Gui Santos: más de 1.5 asistencias** | **66%** | 68% | 64% | 2.5 ± 1.8 | 8/10 | 2/3 | 3, 7, 0 | 1.44 (69%) |
| **Gui Santos: más de 0.5 triples** | **65%** | 67% | 64% | 1.1 ± 1.1 | 8/10 | 3/3 | 1, 2, 0 | 1.45 (69%) |
| **Jamal Murray: menos de 1.5 robos** | **64%** | 70% | 61% | 1.1 ± 1.1 | 9/10 | 2/2 | 2, 1, 2, 3 | 1.62 (62%) |
| **Brandin Podziemski: más de 0.5 robos** | **63%** | 72% | 59% | 1.4 ± 1.2 | 7/10 | 1/1 | 2, 1, 0, 1 | 1.49 (67%) |
| **Draymond Green: menos de 1.5 triples** | **63%** | 62% | 64% | 1.4 ± 1.3 | 8/10 | 2/2 | 2, 5, 2 | 1.47 (68%) |
| **Christian Braun: menos de 1.5 robos** | **62%** | 66% | 61% | 1.2 ± 1.1 | 6/10 | 1/2 | 0, 2, 1, 0 | 1.65 (61%) |
| **Brandin Podziemski: más de 0.5 robos+tapones** | **62%** | 76% | 56% | 1.8 ± 1.4 | 7/10 | 1/1 | 3, 1, 1, 1 | 1.59 (63%) |
| **Christian Braun: más de 1.5 asistencias** | **60%** | 69% | 55% | 3.0 ± 1.8 | 4/10 | 1/2 | 0, 2, 4, 2 | 1.68 (60%) |

### Fichas de los jugadores destacados

#### Gui Santos (aleros/ala-pívots) vs Denver Nuggets

- Minutos esperados: **23.2** (± 3.1); 73 partidos en la base.
- en el parte de lesiones: day-to-day
- Kristaps Porzingis ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Moses Moody ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- cambio de rol esta temporada (por minuto): ast -36%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Gui Santos: más de 1.5 asistencias** (66%). Con 80% de probabilidad: más de 0.5 / menos de 4.5.
- Defensa de Denver Nuggets contra aleros/ala-pívots en asistencias: +15% respecto a la media; ajuste por su historial contra defensas similares: +1%.

**¿Por qué 2.5 asistencias?** (línea 1.5; 23.2 minutos esperados)

- Asistencias **2.5** (por componentes 2.1 · por tasa por minuto y defensa rival 2.7): asiste el 13.4% de las canastas de sus compañeros en pista × 15.9 canastas de compañeros esperadas (su equipo 41.0 por 48' contra esta defensa).

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 26.0 | 27.0 | 22.7 | 20.9 | 22.3 |
| Asistencias | 2.8 | 3.0 | 1.7 | 2.4 | 3.3 |
| % de las canastas de compañeros que asiste | 14.9% | 15.6% | 9.9% | 15.5% | 19.5% |
| Pérdidas por jugada | 15.3% | 15.4% | 4.3% | 16.9% | 22.6% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -10%, vs defensa media +9%, vs defensa débil +3%; rebotes: vs defensa fuerte -4%, vs defensa media -6%, vs defensa débil +10%; asistencias: vs defensa fuerte -13%, vs defensa media +12%, vs defensa débil +2%; triples: vs defensa fuerte -5%, vs defensa media -1%, vs defensa débil +6%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 35% | 71% | 68% | 70% |
| triple frontal | 33% | 32% | 35% | 34% |
| pintura | 17% | 44% | 45% | 45% |
| triple de esquina | 14% | 43% | 38% | 36% |
| media distancia | 1% | 41% | 41% | 40% |

#### Jamal Murray (bases/escoltas) vs Golden State Warriors

- Minutos esperados: **40.2** (± 3.0); 84 partidos en la base.
- cambio de rol esta temporada (por minuto): reb +30%, ast -44%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Jamal Murray: menos de 1.5 robos** (64%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Golden State Warriors contra bases/escoltas en robos: +7% respecto a la media; ajuste por su historial contra defensas similares: -1%.

**¿Por qué 1.1 robos?** (línea 1.5; 40.2 minutos esperados)

- Robos **1.1** (por componentes 1.1 · por tasa por minuto y defensa rival 1.2): roba el 10.5% de las pérdidas del rival en pista × 12.4 pérdidas esperadas del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 39.2 | 39.7 | 40.0 | 35.0 | 34.5 |
| Robos | 1.2 | 0.8 | 1.0 | 0.9 | 2.0 |
| % de las pérdidas del rival que roba | 9.7% | 7.5% | 8.4% | 10.7% | 24.0% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -4%, vs defensa media -2%, vs defensa débil +6%; rebotes: vs defensa fuerte -9%, vs defensa media -10%, vs defensa débil +23%; asistencias: vs defensa fuerte -11%, vs defensa media +3%, vs defensa débil +13%; triples: vs defensa fuerte +5%, vs defensa media -21%, vs defensa débil +9%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 36% | 41% | 35% | 35% |
| pintura | 23% | 44% | 45% | 48% |
| media distancia | 20% | 43% | 41% | 44% |
| bajo el aro | 17% | 65% | 68% | 71% |
| triple de esquina | 4% | 48% | 38% | 41% |

#### Brandin Podziemski (bases/escoltas) vs Denver Nuggets

- Minutos esperados: **32.9** (± 4.6); 85 partidos en la base.
- sin Kristaps Porzingis (67 partidos): 27.7 min vs 32.9 con él; pts -13%/min, ast +13%/min
- Moses Moody ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- Su prop más probable hoy: **Brandin Podziemski: más de 0.5 robos** (63%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Denver Nuggets contra bases/escoltas en robos: -7% respecto a la media; ajuste por su historial contra defensas similares: -1%.

**¿Por qué 1.4 robos?** (línea 0.5; 32.9 minutos esperados)

- Robos **1.4** (por componentes 1.3 · por tasa por minuto y defensa rival 1.5): roba el 13.0% de las pérdidas del rival en pista × 13.6 pérdidas esperadas del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 33.2 | 30.9 | 33.0 | 28.7 | 32.0 |
| Robos | 1.2 | 1.0 | 3.0 | 1.1 | 1.0 |
| % de las pérdidas del rival que roba | 10.6% | 10.0% | 17.3% | 11.7% | 12.2% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +2%, vs defensa media -7%, vs defensa débil +6%; rebotes: vs defensa fuerte -7%, vs defensa media +2%, vs defensa débil +8%; asistencias: vs defensa fuerte -7%, vs defensa media -27%, vs defensa débil +22%; triples: vs defensa fuerte -14%, vs defensa media +6%, vs defensa débil +10%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 40% | 33% | 35% | 34% |
| pintura | 22% | 47% | 45% | 45% |
| bajo el aro | 19% | 70% | 68% | 70% |
| media distancia | 12% | 39% | 41% | 40% |
| triple de esquina | 7% | 49% | 38% | 36% |

#### Draymond Green (aleros/ala-pívots) vs Denver Nuggets

- Minutos esperados: **27.2** (± 5.4); 72 partidos en la base.
- sin Kristaps Porzingis (55 partidos): 26.9 min vs 30.8 con él; pts +21%/min, reb +19%/min, ast -7%/min
- Moses Moody ya no jugó en sus últimos partidos: la baja ya está en sus minutos
- cambio de rol esta temporada (por minuto): pts -55%, ast +34%, tpm -63%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Draymond Green: menos de 1.5 triples** (63%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Denver Nuggets contra aleros/ala-pívots en triples: -1% respecto a la media; ajuste por su historial contra defensas similares: -4%.

**¿Por qué 1.4 triples?** (línea 1.5; 27.2 minutos esperados)

- Triples **1.4** (por componentes 1.5 · por tasa por minuto y defensa rival 1.3): 4.5 triples intentados (su ritmo 4.8 por 36'; el rival concede +2% de triples en su reparto) × 32% esperado.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 29.4 | 28.6 | 26.0 | 27.7 | 30.0 |
| Triples anotados | 0.6 | 1.0 | 0.5 | 1.5 | 3.0 |
| Triples intentados | 2.0 | 2.9 | 1.5 | 4.5 | 7.3 |
| % triples | 30.0% | 34.5% | 33.3% | 32.4% | 40.9% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte +6%, vs defensa media -7%, vs defensa débil -1%; rebotes: vs defensa fuerte -2%, vs defensa media -0%, vs defensa débil +4%; asistencias: vs defensa fuerte -1%, vs defensa media -2%, vs defensa débil +3%; triples: vs defensa fuerte -20%, vs defensa media -1%, vs defensa débil +35%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| triple frontal | 41% | 30% | 35% | 34% |
| bajo el aro | 24% | 68% | 68% | 70% |
| triple de esquina | 21% | 39% | 38% | 36% |
| pintura | 11% | 44% | 45% | 45% |
| media distancia | 3% | 37% | 41% | 40% |

#### Christian Braun (bases/escoltas) vs Golden State Warriors

- Minutos esperados: **36.0** (± 4.2); 51 partidos en la base.
- cambio de rol esta temporada (por minuto): ast -51%; se da más peso a la línea de la casa
- Su prop más probable hoy: **Christian Braun: menos de 1.5 robos** (62%). Con 80% de probabilidad: más de - / menos de 2.5.
- Defensa de Golden State Warriors contra bases/escoltas en robos: +7% respecto a la media; ajuste por su historial contra defensas similares: -1%.

**¿Por qué 1.2 robos?** (línea 1.5; 36.0 minutos esperados)

- Robos **1.2** (por componentes 1.1 · por tasa por minuto y defensa rival 1.2): roba el 12.3% de las pérdidas del rival en pista × 12.4 pérdidas esperadas del rival.

| Estadística | Últ. 5 | Últ. 10 | Temporada | Temp. anterior | vs este rival |
|---|---|---|---|---|---|
| Minutos | 32.4 | 33.9 | 36.5 | 31.8 | 34.5 |
| Robos | 1.4 | 1.3 | 1.5 | 0.7 | 0.8 |
| % de las pérdidas del rival que roba | 13.6% | 14.1% | 13.7% | 9.7% | 8.9% |

- Rendimiento por minuto según la defensa rival (frente a su media): puntos: vs defensa fuerte -17%, vs defensa media -1%, vs defensa débil +17%; rebotes: vs defensa fuerte -15%, vs defensa media +1%, vs defensa débil +17%; asistencias: vs defensa fuerte -9%, vs defensa media -10%, vs defensa débil +21%; triples: vs defensa fuerte -0%, vs defensa media -3%, vs defensa débil +2%.

| Zona | Reparto de sus tiros | Su acierto | Media liga | Concede el rival |
|---|---|---|---|---|
| bajo el aro | 45% | 71% | 68% | 71% |
| triple frontal | 20% | 29% | 35% | 35% |
| triple de esquina | 17% | 35% | 38% | 41% |
| pintura | 13% | 45% | 45% | 48% |
| media distancia | 5% | 41% | 41% | 44% |
