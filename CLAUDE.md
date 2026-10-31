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
justa. Cada apuesta que comparta va a `apuestas_usuario/AAAA-MM-DD.json` (`apuestas/nba/usuario.py`) para
seguirla; hasta que diga lo contrario son de prueba (empieza con dinero real el 30 oct o el 2 nov).

Estas reglas salen de un solo día de resultados: revisar en el acumulado del informe ("Acumulado de las
combinadas de prueba") si estos tipos siguen cumpliendo lo prometido y decírselo si dejan de hacerlo.
