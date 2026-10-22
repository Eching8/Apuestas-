# Cómo usar el analizador de apuestas desde un chat normal

## La respuesta corta

**Sí se puede, pero tiene que ser un chat de Claude Code (claude.ai/code), no un chat corriente de claude.ai.**

- Los accesos a los dominios (ESPN, sports.bzzoiro.com, api.sportsgameodds.com, football-data.co.uk) y tus claves **no pertenecen a este proyecto**: están guardados en tu **entorno en la nube "Apuestas 2.0"**. Cualquier sesión de Claude Code que abras con ese entorno tiene exactamente los mismos accesos, sin que tengas que pegar ninguna clave.
- El código está en GitHub (repositorio `Eching8/Apuestas-`), así que cualquier sesión de Claude Code puede descargarlo y ejecutarlo.
- Un **chat corriente de claude.ai** (la pestaña de chat normal) **no sirve**: su ordenador interno no puede conectarse a esas webs ni usar tus claves guardadas. Podría leer el código, pero no ejecutar el análisis con datos reales. Y nunca pegues tus claves en un chat.

## Pasos (una sola vez por chat)

1. Abre **https://claude.ai/code** (o la pestaña "Code" en la app de Claude del móvil).
2. Elige el repositorio **Eching8/Apuestas-**.
3. En el selector de entorno, elige **"Apuestas 2.0"** (es el que tiene los permisos y las claves). Si eliges "Predeterminado", Bzzoiro y SportsGameOdds no funcionarán.
4. Pega el prompt de abajo y envíalo.

## Prompt listo para pegar

```
Responde siempre en español, de forma breve y clara; no soy técnico.

Quiero que ejecutes mi analizador de apuestas de fútbol de este repositorio (Eching8/Apuestas-).
Sigue la guía del repositorio .claude/skills/apuestas-diario/SKILL.md y respeta sus límites
(nunca --forzar, diario solo una vez al día, nada de llamadas a las APIs por tu cuenta).

1. Prepara el código y los datos:
   bash scripts/preparar.sh
   bash scripts/datos.sh restaurar
2. Comprueba las fuentes: python3 -m apuestas fuentes
   Dime cuáles funcionan (ESPN, Bzzoiro, SportsGameOdds, football-data.co.uk). Si alguna falla,
   dime el mensaje exacto y sigue con las demás. No me pidas claves por el chat.
3. Analiza los partidos de hoy: python3 -m apuestas diario
   (si ya se ejecutó hoy, usa en su lugar python3 -m apuestas analizar --sin-descarga)
   Si quiero solo una liga te lo diré (por ejemplo, APUESTAS_LIGAS=3 para Europa League).
4. python3 -m apuestas rendimiento
5. Resúmeme en el chat, leyendo reportes/AAAA-MM-DD.md: las mejores selecciones sueltas (máx. 8)
   con probabilidad, cuota y valor, y las combinadas (alta probabilidad, valor, lotería y
   "crea tu apuesta"). Avisa de que son provisionales hasta ver las alineaciones.
6. Dime a qué horas conviene hacer el chequeo de alineaciones (python3 -m apuestas agenda) y
   prográmalos si puedes; en cada chequeo ejecuta python3 -m apuestas chequeo y dime qué apuestas
   quedan confirmadas, anuladas o nuevas.
7. Al terminar cada paso que use datos: bash scripts/datos.sh guardar

No inventes ningún dato: si algo falla, dime el error tal cual. Recuérdame que son estimaciones
y que el backtest muestra que el modelo no le gana a las casas.
```

### Variantes cortas (para pegar después, en el mismo chat)

- Solo chequeo de alineaciones: `Haz ahora el chequeo de alineaciones (paso 2 de la guía apuestas-diario) y dime las apuestas finales.`
- Predicción sin gastar peticiones: `Ejecuta python3 -m apuestas predecir --dias 3 y resúmeme las probabilidades y la combinada lotería.`
- Remates: `Ejecuta python3 -m apuestas remates --ligas 3 --mixta --alta-prob y resúmeme las mejores combinadas.`

## Cosas a tener en cuenta

- **Los datos se guardan en GitHub** (rama `datos`): la base de partidos y los contadores de peticiones viajan entre chats. Por eso el prompt siempre restaura al empezar y guarda al terminar; si dos chats analizan a la vez, pueden gastar el doble de peticiones o pisarse los datos. Usa un chat cada vez.
- **Límites de las fuentes**: Bzzoiro hasta 1.000 peticiones al día y SportsGameOdds hasta 2.000 objetos al mes (el plan gratis de SportsGameOdds no incluye Europa League). El programa ya los controla.
- **Si cambias una clave o un permiso**, hazlo en el entorno "Apuestas 2.0" (claude.ai/code → selector de entorno → engranaje). Los chats nuevos lo recogen solos.
- **Lo que no pasa al otro chat**: las conversaciones y los avisos programados de este proyecto. El otro chat empieza sin memoria; todo lo que necesita está en el repositorio y en la rama `datos`.
