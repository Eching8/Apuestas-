# Apuestas NBA: cómo armar combinadas cuando el usuario las pida

El usuario (Bogotá, apuesta en Betano) pidió el 29 oct 2026 que **cualquier combinada que pida** se arme con
el criterio de las que ganaron el 28 oct (segura A, segura B, seguras de cuota 2+ y 3+, de valor 15+), y no
con el de las que perdieron (combinadas largas con una pata floja, rachas de "menos de triples", 5 patas del
mismo partido). Probabilidad y constancia por encima de la cuota.

## Reglas

1. **Solo jugadores constantes** (`analizador.candidatas_seguras`): titulares con minutos estables, sin alertas
   (ni suplente, ni minutos inestables, ni cambio de rol, ni traspaso, ni lesión), que hayan pasado la línea en
   7+ de sus últimos 10 y en el 60 %+ de esta temporada. Cada pata con 62 %+ de probabilidad final.
2. **Un partido por pata** en las combinadas (como la B y las de cuota objetivo). Los bet builders son la
   excepción, y cada pierna tiene que haberse pasado en 2 de cada 3 partidos de esta temporada
   (`builder.ACIERTO_TEMPORADA_MIN`) y no bajar de la línea mínima de la casa.
3. **Las menos patas posibles** para llegar a la cuota pedida (`combinadas.con_cuota`): 2-3 patas para cuota
   2-3; para cuotas altas, la combinada "de valor" (picks donde el modelo ve más de lo que paga la casa, 6+ de
   10, sin alertas) antes que alargar una segura.
4. **Primero la segura A** (líneas alternativas de estrellas al 85-92 %) cuando se pide algo muy seguro.
5. **Ninguna pata "moneda al aire"**: si una pata queda por debajo de ~60 % o la casa no ofrece la línea,
   cambiarla por la siguiente más segura de la lista, no por la que más paga.
6. Si el usuario pide algo agresivo (cuota 30+), avisar de la probabilidad real y armarlo igual con estas
   reglas, sin meter más de 2 patas del mismo partido.

Antes de recomendar, revisar lesiones del día y el parte (ESPN) y decir la probabilidad conjunta y la cuota
justa. Cada apuesta que comparta va a `apuestas_usuario/AAAA-MM-DD.json` (`apuestas/nba/usuario.py`) para
seguirla; hasta que diga lo contrario son de prueba (empieza con dinero real el 30 oct o el 2 nov).

Estas reglas salen de un solo día de resultados: revisar en el acumulado del informe ("Acumulado de las
combinadas de prueba") si estos tipos siguen cumpliendo lo prometido y decírselo si dejan de hacerlo.

# Apuestas NFL: cómo armar combinadas cuando el usuario las pida

Mismo criterio que la NBA (arriba), traducido a la NFL en `apuestas/nfl/combinadas.py` (`nfl combinadas`,
`nfl seguimiento`). Las apuestas que comparta van a `apuestas_usuario/nfl/AAAA-MM-DD.json`
(`apuestas/nfl/usuario.py`; las patas pueden ser de cualquier partido de esa semana, y "equipo" desempata
homónimos). Son **apuestas fantasma** (no las juega en Betano: el 29 oct pidió seguirlas todas para tener la data
completa antes de empezar de verdad), así que se registran y se liquidan todas, también las que no le gusten.

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
- **El bet builder de Betano recorta mucho las patas del mismo partido**: comparar su cuota con la justa y no
  aceptar la combinada si queda por debajo.
