# Apuestas NBA: cómo armar combinadas cuando el usuario las pida

El usuario (Bogotá, apuesta en Betano) pidió el 29 oct 2026 que **cualquier combinada que pida** se arme con
el criterio de las que ganaron el 28 oct (segura A, segura B, seguras de cuota 2+ y 3+), y no
con el de las que perdieron (combinadas largas con una pata floja, rachas de "menos de triples", 5 patas del
mismo partido). Probabilidad y constancia por encima de la cuota.

**Lo que busca el usuario (3 nov 2026): ganar sus apuestas, no sacarle valor a la casa.** Cada pata y cada
combinada se elige por la probabilidad más alta de acertar, respaldada por los datos de esta temporada y la lógica
del partido. El valor (lo que paga la casa frente a lo que vale) nunca es criterio para meter una pata ni para
elegir entre dos; la cuota solo sirve para llegar a la que pide con las patas más seguras. Vale para la NBA y la NFL.

## Reglas

1. **Solo jugadores constantes** (`analizador.candidatas_seguras`): titulares con minutos estables, sin alertas
   (ni suplente, ni minutos inestables, ni cambio de rol, ni traspaso, ni lesión), que hayan pasado la línea en
   7+ de sus últimos 10 y en el 60 %+ de esta temporada. Cada pata con 62 %+ de probabilidad final.
2. **Un partido por pata** en las combinadas (como la B y las de cuota objetivo). Los bet builders son la
   excepción, y cada pierna tiene que haberse pasado en 2 de cada 3 partidos de esta temporada
   (`builder.ACIERTO_TEMPORADA_MIN`) y no bajar de la línea mínima de la casa.
3. **Las menos patas posibles** para llegar a la cuota pedida (`combinadas.con_cuota`, máximo 5): 2-3 patas
   para cuota 2-3. **Nada de combinadas "de valor"** (lo pidió el 3 nov 2026: buscarle valor a la casa metía
   "menos" de estrellas y patas flojas, 0 de 5). Una cuota alta tiene que tener lógica de partido (minutos, rol,
   bajas, guion del partido) y patas probables; si no se llega, se dice y se propone una cuota menor.
4. **Primero la segura A** (líneas alternativas de estrellas al 85-92 %) cuando se pide algo muy seguro.
5. **Ninguna pata "moneda al aire"**: si una pata queda por debajo de ~60 % o la casa no ofrece la línea,
   cambiarla por la siguiente más segura de la lista, no por la que más paga.
6. Si el usuario pide algo agresivo (cuota 30+), avisar de la probabilidad real y armarlo igual con estas
   reglas, sin meter más de 2 patas del mismo partido. **Agresivas (6 nov 2026):** no tenerle miedo a líneas más
   altas que la mínima de Betano si el análisis las respalda (lo pidió él: "si me explicas bien que se le espera
   tanto, le apuesto aunque tenga desventaja"). Ahí valen patas del 60 %+ (no monedas al aire, nunca bajo ~58 %),
   cada una explicada al estilo de "En corto" (esperado frente a la línea, acierto con sus minutos y contra defensas
   como la de hoy, puesto del rival, zona/tipo de tiro, oportunidades, bajas). Él manda la combinada con las líneas
   de Betano y se le cambian las patas flojas por otras agresivas bien respaldadas, no por la que más paga. Las
   reglas 7-9 (dinero real) siguen igual.

- **"Menos" de anotación** (puntos, triples, PRA, P+R, P+A) solo con 75 %+ y 8+ de 10, y nunca de un compañero
  de una estrella ausente (`analizador.menos_aceptable`, alerta "sin X: más tiros para él"). Los "menos" de
  rebotes, asistencias y defensa de titulares sí rinden (75 % frente a 65 % prometido, 25 oct-1 nov).

- **Props vetadas por el usuario** (`modelo.VETADOS`): no se proponen nunca, por ningún lado. Isaiah Jackson
  rebotes (2 nov 2026: menos de 7.5, hizo 8 y tumbó las dos apuestas reales). Si pide vetar otra, se agrega ahí.

## Con dinero real (desde el 30 oct 2026)

7. **Sin excepciones a la regla 1**: una pata que no cumple la constancia de esta temporada no entra aunque
   tenga valor. El 30 oct, Garland menos 23.5 pts (2 de 4 esta temporada) hizo 24 y tumbó una de 13.64.
8. **No alargar ni subir líneas para llegar a una cuota.** Si la casa no paga la cuota que se busca con patas
   del 70 %+, decirlo y proponer menos patas o otra combinada; no meter patas del 55-65 % para llegar. El 30
   oct, Hart 7+ rebotes (64 %, puesta para llegar a cuota 10) hizo 6 y tumbó la de 8.49.
9. **Máximo 4-5 patas** en lo que se juega con dinero: con patas del ~70 %, ocho o nueve patas solo aciertan
   ~6-10 % aunque cada pata esté bien calibrada (30 oct: las patas acertaron 10 de 13, 77 % frente a 72 %
   prometido, y aun así perdieron las dos combinadas).

Antes de recomendar, revisar lesiones del día y el parte (ESPN) y decir la probabilidad conjunta y la cuota
justa. **Cada pata se presenta con sus argumentos concretos** (`modelo.argumentos`, "En corto" en el informe; lo
pidió el 4 nov 2026 con el ejemplo de un analista): cuántas veces la pasó esta temporada y por qué falló las que
falló, con minutos normales, contra las mejores defensas, el puesto del rival (#N de 30) concediendo esa
estadística a su posición y en su zona de tiro, las oportunidades (tiros, rebotes disponibles) y las bajas.
Los datos de pbpstats.com (`nba/pbpstats.py`: % de rebotes disponibles que se queda, transición tras robos) se bajan
cada día; stats.nba.com no responde desde la nube. **Un "menos" que el jugador ya falló esta temporada en partidos
normales** (30 %+ de sus partidos, sin pocos minutos, faltas ni paliza) lleva la alerta "falla en partidos normales"
y no entra (backtest 2025-26: 63.8 % frente a 66 % prometido; PRA 59.8 %). **Jugada a jugada de ESPN**
(`nba/jugadas.py`, `nba jugadas`): oportunidades de rebote reales con el jugador en pista y puntos al contraataque
por jugador y partido (equipos ajustados a los "fast break points" oficiales). Los puntos se ajustan por el
contraataque que concede el rival (`modelo.TRANSICION_*`), y un "menos" de puntos contra un rival que concede 12 %+
más contraataque que la media lleva la alerta "el rival concede mucho contraataque" y no entra (2025-26: 58.9 %
frente a 66.3 % prometido). Si el rival jugó anoche y él no, +1.5 % de puntos y +2 % de asistencias
(`modelo.RIVAL_CANSADO`). "En corto" también da el acierto con los minutos de hoy contando la temporada pasada
(cuando le suben los minutos por bajas), el acierto con defensa como la de hoy y sus minutos a la vez, y el puesto
del rival en rebotes y rebotes ofensivos que concede en total, y **cómo tira** (tipos de tiro de ESPN agrupados como
los "play types": recibe y tira, creado, penetración, corte, poste, palmeo, aro; `jugadas.parse_tipos`) con el puesto
del rival en lo que deja en su tipo principal. Esto último solo explica: en 2025-26 no movió los puntos ni los triples
frente a lo que ya preveía el modelo. Las asistencias potenciales solo están en stats.nba.com (no responde desde la nube); en su lugar, **asistencias
esperadas** (`modelo.SUERTE_*`): con la jugada a jugada se sabe cuántos tiros metieron sus compañeros con él en pista
frente a los esperados por tipo de tiro; si vienen fríos, sus asistencias suben (+6 % en 2025-26; los "menos" de
asistencias con compañeros fríos acertaban 59.3 % prometiendo 67.6 %, ahora 64.2 % frente a 66.6 %). En corto también
da su segunda zona de tiro y el puesto del rival en tiros libres que concede a su posición. **Su propia puntería**
(`modelo.PUNTERIA_*`): canastas en sus últimos 10 frente a las esperadas por sus tipos de tiro; corrige los puntos
(±3 %) y un "menos" de puntos de un jugador que viene frío (0.95 o menos) lleva la alerta "viene fallando tiros que
suele meter" y no entra (2025-26: 55.5 % frente a 65 % prometido). Probado y descartado: árbitros (no cambian tiros
libres ni puntos) y peso defensivo de cada baja del rival (demasiado ruidoso). **Robos, tapones, robos+tapones y
pérdidas** tienen su propio análisis: oportunidades reales con él en pista (pérdidas y tiros de 2 del rival), puesto
del rival en balones que pierde, tiros de 2 y tiros cerca del aro, y pérdidas que provoca; su calibración es propia
(`modelo.CALIBRACION_STAT`: con 0.9 salían conservadoras). Sus líneas de la casa solo llegan con SportsGameOdds o con
The Odds API si `ODDS_API_DEFENSIVAS=1` (cuesta más créditos). **El usuario sigue con el plan gratuito de The Odds
API** (5 nov 2026): los créditos se racionan solos (`theodds.partidos_hoy`: los que quedan entre los días que faltan
del mes) y, si no alcanzan, se piden primero los partidos más parejos. Los partidos sin líneas siguen teniendo picks
seguros (líneas alternativas) y bet builders, que no necesitan la línea de la casa; cuando arme combinadas de líneas
principales de esos partidos, pedirle al usuario las cuotas de Betano. **Líneas mínimas de Betano** (6 nov 2026: Betano
solo abre sus alternativas ~2 por debajo de la principal en puntos y 1 en asistencias y rebotes; las patas del bet
builder a 8+ o 23+ no existían): picks seguros y bet builders nunca proponen una línea por debajo de la mínima que
ofrecería la casa (`modelo.piso_casa`, estimada si no hay línea); el bet builder puede ir con 3 patas, y si a esa
mínima no hay pick al 85 %, sale la mínima con su probabilidad real si pasa del 75 %. Cuando el usuario mande las
líneas de Betano, evaluar esas exactas y cambiar las que bajen del 70 %, no forzarlas. Cada apuesta que comparta va a `apuestas_usuario/AAAA-MM-DD.json` (`apuestas/nba/usuario.py`) para
seguirla; hasta que diga lo contrario son de prueba (empieza con dinero real el 30 oct o el 2 nov).

Estas reglas salen de un solo día de resultados: revisar en el acumulado del informe ("Acumulado de las
combinadas de prueba") si estos tipos siguen cumpliendo lo prometido y decírselo si dejan de hacerlo.

# Apuestas NFL: cómo armar combinadas cuando el usuario las pida

Mismo criterio que la NBA (arriba), traducido a la NFL en `apuestas/nfl/combinadas.py` (`nfl combinadas`,
`nfl seguimiento`). Las apuestas que comparta van a `apuestas_usuario/nfl/AAAA-MM-DD.json`
(`apuestas/nfl/usuario.py`; las patas pueden ser de cualquier partido de esa semana, y "equipo" desempata
homónimos). Son **apuestas fantasma** (no las juega en Betano: el 29 oct pidió seguirlas todas para tener la data
completa antes de empezar de verdad), así que se registran y se liquidan todas, también las que no le gusten.
**La primera con dinero real** fue el 1 nov 2026: la combinada de 7 de Betano a 51.89 con 10.000 COP
("Betano 51.89 (real)", `"real": true`); las reales llevan `apostado` y `moneda` y se siguen aparte en el acumulado.

## Reglas

1. **Solo jugadores constantes** (`combinadas.constante`): sin alertas (`combinadas.alertas`: papel menor por
   snaps, vuelve de lesión, cambio de rol, traspaso reciente, en el parte de lesiones, muy lejos de la casa), que
   pasaron la línea en 7+ de sus últimos 10 y en el 60 %+ de esta temporada. Cada pata con 62 %+ de probabilidad.
2. **Un partido por pata** cuando hay varios partidos. Con uno solo (jueves, lunes) hay que sacar los mejores props
   de ese partido (lo pidió el 29 oct): **sin tope por equipo**, una pata por jugador, y **todas con el mismo guion**
   (`combinadas.coherente`: ningún par con correlación en contra). La probabilidad conjunta usa las correlaciones medidas en 2024-2026
   (`combinadas.CORRELACIONES`): yardas del QB ↔ yardas de sus receptores +0.37, ↔ recepciones +0.26, ↔ su RB
   −0.13; QB rivales +0.11; RB rivales −0.17; receptores entre sí ~0. Por eso el bet builder de la casa paga
   mucho menos que el producto de las cuotas: no alargarlo con patas de relleno.
3. **Las menos patas posibles** para la cuota pedida (`combinadas.con_cuota`); para cuotas altas, la de valor
   antes que alargar una segura.
4. **Primero la segura A** (líneas alternativas al 85 %+ de jugadores sin alertas, 8+ de 10) si piden algo seguro.
5. **Ninguna pata moneda al aire** ni con valor negativo a la cuota de la casa del usuario: si su casa no ofrece
   la línea o paga menos que la cuota mínima (justa × 1.04), cambiarla por la siguiente más segura.
6. Para cuotas de 30+, avisar de la probabilidad real y armarla igual con estas reglas.
7. Betano no tiene "no anota": no usarlo en las combinadas (el sistema ya no lo propone).

## Lecciones de los partidos jugados (actualizar con el seguimiento)

- **Solo props de partido completo**: de 153 selecciones liquidadas, las de cuarto y mitad pierden dinero.
- **Las patas de una combinada tienen que ganar con el mismo guion** (26 oct, DAL 38-21 PHI: el under de acarreos
  del RB del favorito y el under de recepciones del receptor del que pierde se cayeron juntos en la paliza).
- **Nada de unders de acarreos de RB titulares en partidos parejos o de no favoritos**: en 2025 el modelo los
  proyectaba 1.3 acarreos por debajo de lo real. **Tampoco cuando la línea de la casa parece desfasada** (29 oct:
  Hubbard menos de 17.5 con la línea de EE. UU. en 16.5; Carolina perdió por 14 casi todo el partido y aun así le
  dieron 22 acarreos: tumbó la sencilla, la de valor, la agresiva y el bet builder de 17.50).
- **Revisar los inactivos ~90 minutos antes del partido y cambiar las patas de quien no juegue** (29 oct: Jonnu
  Smith salió como baja a las 23:03 UTC, una hora antes; la pata queda anulada y en un bet builder la casa puede
  anular o recalcular toda la apuesta).
- **Si el modelo va contra la casa en todo un equipo a la vez, es un sesgo del modelo**, no valor (29 oct, Green
  Bay: Jacobs volvía de lesión y Lloyd había sido el titular): revisar el historial antes de recomendar.
- **El RB titular que vuelve de lesión tiene prioridad sobre sus suplentes** (Saquon contra Dallas; 29 oct, Jacobs
  14 acarreos y 2 TD contra 2 acarreos y nada de Lloyd). El modelo lo diluía con las cuotas que habían inflado los
  suplentes; ahora conserva el 80 % de su papel (`modelo.PRIORIDAD_REGRESO`). No apostar a los suplentes de un
  titular que vuelve (ni a su "anota" ni a sus acarreos), aunque hayan sido los titulares mientras él no estaba.
- **Comprobar el historial de cada pata con la línea exacta de la casa del usuario** (el pateador de Carolina:
  el modelo daba 60 % al menos de 6.5 puntos y lo había pasado en 5 de 6).
- **Combinadas de 2+ TD: las patas entran en el orden de probabilidad del modelo** (`nfl td`, "Candidatos a 2 o más
  touchdowns"), sin saltarse a nadie por uno que esté más abajo en la lista. El 1 nov se metió a Jeanty (14 %) y se
  dejó fuera a Derrick Henry (21 %), que anotó en el primer cuarto. Aun bien elegidas, 4 patas de 2+ TD dan ~0.2 %:
  con dinero real, solo montos pequeños y avisando de la probabilidad (van contra las reglas 1 y 8 de la NBA, patas
  del 70 %+). Comparar su cuota de Betano con las de EE. UU. (`nfl verificar`): el 1 nov Betano pagaba 15-25 % menos
  por pata (248 frente a ~547 la combinada).
- **El bet builder de Betano recorta mucho las patas del mismo partido**: comparar su cuota con la justa y no
  aceptar la combinada si queda por debajo.

# Apuestas NHL: cómo armar combinadas cuando el usuario las pida

Mismo criterio que la NBA (arriba: ganar sus apuestas, no sacarle valor a la casa; probabilidad y constancia por
encima de la cuota), traducido al hockey en `apuestas/nhl/` (`nhl analizar`, informe en la rama `nhl-informes`).
Las apuestas que comparta van a `apuestas_usuario/nhl/AAAA-MM-DD.json` (`apuestas/nhl/usuario.py`; stat: shots,
points, goals, assists, blocked, hits, saves) y se liquidan solas.

## Reglas

1. **Solo jugadores constantes** (`analizador.candidatas_seguras`): papel principal por tiempo en hielo (top 9 de
   delanteros, 14+ min; top 4 de defensas, 17+ min), tiempo en hielo estable, sin alertas (`modelo.alertas`: papel
   menor, tiempo en hielo inestable, cambio de unidad de PP, cambio de línea o de rol, traspaso reciente, vuelve de
   lesión, en el parte de lesiones; porteros: portero no confirmado), que pasaron la línea en 7+ de sus últimos 10 y en
   el 60 %+ de esta temporada. Cada pata con 62 %+. ESPN no da las líneas (quién juega con quién): el cambio de línea
   se detecta por el tiempo en igualdad (±20 % en sus últimos 3).
2. **Un partido por pata** en las combinadas. Bet builders (`nhl/builder.py`) como excepción: 2-3 "más de" del mismo
   partido con el mismo guion, cada pierna pasada en 2 de cada 3 partidos de esta temporada y sin bajar de la línea
   mínima de Betano.
3. **Las menos patas posibles** para la cuota pedida (`combinadas.con_cuota`, máximo 5). Nada de combinadas "de valor".
4. **Primero la segura A** (líneas alternativas al 85 %+) si pide algo muy seguro.
5. **Ninguna pata moneda al aire**: bajo ~60 % o sin línea en Betano, se cambia por la siguiente más segura.
6. **Agresivas**: valen líneas más altas que la mínima de Betano si el análisis las respalda (60 %+, nunca bajo ~58 %),
   cada pata explicada con su "En corto".
7. **Con dinero real**: patas del 70 %+, máximo 4-5 patas, no alargar ni subir líneas para llegar a una cuota.

- **"Menos" de producción** (tiros a puerta, puntos, goles, asistencias) solo con 75 %+ y 8+ de 10, y nunca si falta
  un compañero importante de su equipo (alerta "sin X: más hielo para él") ni si ya la falló en partidos normales
  (alerta "falla en partidos normales"), hasta medirlos con líneas reales de la NHL.
- **Portero**: las paradas solo con el portero probable de ESPN confirmado (`nhl_games.home_goalie_id`); el flujo corre
  otra vez a las 16:47 de Bogotá para ver los porteros confirmados y las lesiones de última hora.
- **"En corto"** (`modelo.argumentos`): acierto esta temporada y por qué falló las que falló (poco hielo, paliza), con
  su tiempo en hielo normal, contra las mejores defensas y contra defensas como la de hoy, puesto del rival (#N de 32)
  concediendo esa estadística a su posición, oportunidades (intentos de tiro, % a puerta, tiempo y puntos en power
  play), portero rival (% de paradas, #N), penaltis del rival, bajas y diferencia esperada.
- **Líneas mínimas de Betano** (`modelo.linea_minima_casa`, estimadas): puntos, goles y asistencias 0.5; tiros a puerta,
  bloqueados y hits, una por debajo de la principal; paradas, ~4 por debajo. Cuando el usuario mande las líneas de
  Betano, evaluar esas exactas, corregir estas estimaciones y cambiar las patas que bajen del 70 %.

**Líneas de la casa**: The Odds API es el plan gratuito que comparte con la NBA. La NHL solo pide líneas con
`ODDS_API_NHL=1` (variable del repositorio) y se queda con `ODDS_API_NHL_PARTE` (0.3) de la ración diaria; la NBA, con
el resto (`nba.theodds.partidos_hoy`). Sin líneas, el informe sale con líneas y cuotas estimadas (la justa menos el
margen de Betano, `analizador.MARGEN_CASA`): pedirle al usuario las cuotas de Betano antes de armar algo con dinero.
