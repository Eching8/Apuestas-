---
name: apuestas-diario
description: Rutina diaria automática del analizador de apuestas de fútbol - análisis de la mañana, chequeos de alineación antes de cada partido y apuestas finales en el chat. Úsala cuando una tarea programada o un aviso pidan la rutina diaria o un chequeo de alineaciones.
---

# Rutina diaria de apuestas

Esta sesión la abre cada día una tarea programada y el usuario sigue el hilo desde aquí. Todo lo
que tenga que ver lo escribes **en el chat**, en español, breve y claro. Nunca apuestas por él: solo
informas. Recuerda siempre que son estimaciones, que el backtest muestra que el modelo no le gana a
las casas y que la combinada lotería tiene valor esperado negativo.

No cambies código del repositorio ni la tarea programada. Los únicos commits son los de
`scripts/datos.sh guardar`.

## Herramientas que necesitas

`add_repo` y `send_later` (servidor `claude-code-remote`) se cargan bajo demanda. Antes de nada:
`ToolSearch` con `select:mcp__claude-code-remote__add_repo,mcp__claude-code-remote__send_later`.
Sin `add_repo` no hay permiso para guardar en la rama `datos`; sin `send_later` no hay chequeos.

## Paso 1: mañana (al abrirse la sesión)

1. Llama a `add_repo` con owner `eching8`, repo `apuestas-` y `access: "push"`, y clona con el
   comando que te devuelva (si ya está clonado, no hace falta). Después:
   ```bash
   bash scripts/preparar.sh
   bash scripts/datos.sh restaurar
   ```
2. Comprueba la clave con `python3 -m apuestas api` (no gasta peticiones). La clave puede llegar
   como variable `API_FOOTBALL_KEY` o como *network secret* que añade el proxy sin que la veas.
   - **Si dice NO DISPONIBLE**: ejecuta `python3 -m apuestas predecir --dias 1`, resume en el chat las
     probabilidades de los partidos del día y la combinada lotería del informe
     `reportes/predicciones-AAAA-MM-DD.md`, y explica que sin `API_FOOTBALL_KEY` en el entorno no hay
     cuotas reales de córners/tarjetas ni chequeo de alineaciones. Se añade en la configuración del
     entorno en la nube → Network secrets → Add secret: sitio `v3.football.api-sports.io`, cabecera
     `x-apisports-key` sin prefijo y la clave como valor (que nunca la pegue en el chat). Después
     `bash scripts/datos.sh guardar` y termina.
3. Ejecuta `python3 -m apuestas diario` (guarda resultados de ayer, liquida y analiza hoy).
   Si falla por la API (plan, límite, clave inválida), dilo en el chat con el mensaje exacto y
   recurre a `python3 -m apuestas predecir --dias 1`.
4. Ejecuta `python3 -m apuestas rendimiento` para el acierto acumulado.
5. Escribe en el chat el **resumen de la mañana**, leyendo `reportes/AAAA-MM-DD.md`:
   - rendimiento de ayer y acumulado (una o dos líneas);
   - selecciones sueltas destacadas (máx. 8) con probabilidad, cuota y valor;
   - combinadas: alta probabilidad, valor, **lotería (cuota ≥ 100)** y las mejores
     **"crea tu apuesta"** (con su cuota justa);
   - aviso: "son provisionales hasta el chequeo de alineaciones".
6. Programa los chequeos (solo si `diario` funcionó con la API): `python3 -m apuestas agenda --json`
   devuelve una lista con `chequeo_utc`.
   Para cada momento llama a `send_later` (servidor `claude-code-remote`) con `at` = `chequeo_utc`
   (formato RFC3339, añade `:00Z` si hace falta), `name` = "Chequeo de alineaciones HH:MM" y
   `message` = "Chequeo de alineaciones: sigue el paso 2 de .claude/skills/apuestas-diario/SKILL.md".
   Si algún momento ya pasó, ejecuta el paso 2 ahora. Di en el chat a qué horas (hora local de
   `APUESTAS_TZ`, por defecto Ciudad de México) habrá chequeos.
7. `bash scripts/datos.sh guardar`.

## Paso 2: chequeo de alineaciones (cada aviso)

1. Si no existe `data/apuestas.db` (el contenedor se reinició), repite `bash scripts/preparar.sh` y
   `bash scripts/datos.sh restaurar`.
2. `python3 -m apuestas chequeo` (descarga alineaciones y cuotas del momento de los partidos que
   empiezan en la próxima hora).
3. Escribe en el chat las **apuestas finales** de esos partidos, a partir de la salida y de
   `reportes/AAAA-MM-DD-chequeo.md`:
   - ✅ confirmadas (probabilidad y cuota actual), ❌ anuladas con su motivo, 🆕 nuevas;
   - ausencias importantes detectadas;
   - estado de cada combinada (confirmada / rota / pendiente). Si una combinada mezcla partidos de
     horarios distintos, avisa de qué piernas quedan sin chequear.
4. Si la salida contiene `PENDIENTE` (alineaciones sin publicar), programa otro `send_later` dentro
   de 12 minutos con el mismo mensaje.
5. `bash scripts/datos.sh guardar`.
6. Si era el último chequeo del día (`python3 -m apuestas agenda` no devuelve más momentos), cierra
   con una línea: "Último chequeo del día. Mañana a primera hora, resultados y nuevo análisis."

## Límites

- Plan gratuito de API-Football: 100 peticiones al día. `diario` usa como mucho
  `APUESTAS_PRESUPUESTO` (60) y cada chequeo 2 por partido (`APUESTAS_PRESUPUESTO_CHEQUEO`, 30). Si
  aparece "presupuesto agotado", dilo y no insistas hasta el día siguiente.
- Si algo falla, informa del error concreto en el chat; no inventes resultados.
