# Analizador diario de fútbol ⚽

Encuentra los partidos del día (desde el **21-10-2026** en adelante) y estima córners, tarjetas, goles,
tiros al arco y remates (por equipo y por jugador). Valida los datos contra una segunda fuente,
compara las probabilidades con las cuotas para encontrar mercados con valor y arma combinadas. Cada
día guarda en una base de datos SQLite las estadísticas de los equipos que analiza.

## Fuentes de datos

| Fuente | Uso | Clave |
|---|---|---|
| [API-Football](https://www.api-football.com/) (api-sports.io) | Partidos, estadísticas por partido (córners, tarjetas, tiros, remates, posesión, xG), estadísticas por jugador y cuotas (Bet365 por defecto) | Sí. El plan gratis da 100 peticiones al día; el plan Pro, 7.500 |
| [football-data.co.uk](https://www.football-data.co.uk) (CSV) | Segunda fuente gratuita: valida marcador, córners, tarjetas, remates y tiros al arco de las 7 ligas europeas configuradas y el marcador de Liga MX, MLS, Argentina y Brasil. Añade xG, árbitro (Premier) y cuotas de Bet365 (1X2 y más/menos 2.5) | No |
| ESPN (API pública) | Validación cruzada de marcadores, córners, tarjetas y tiros. **Modo alternativo completo** si no hay clave de API-Football: partidos, historial de cada equipo en todas sus competiciones, estadísticas de equipo y jugador, y cuotas de DraftKings (1X2, doble oportunidad y total de goles) | No |

### Modos de fuente (`--source`)

| Modo | Cuándo | Qué hace |
|---|---|---|
| `hybrid` (lo elige `auto` si la clave es válida) | Plan gratis de API-Football | ESPN para el historial y las estadísticas (sin límite). API-Football para las cuotas de Bet365 (córners, tarjetas, tiros, remates, ambos marcan, remates por jugador), el árbitro y la validación cruzada de los partidos terminados. Unas 40–60 peticiones al día. |
| `api-football` | Plan de pago | Todo desde API-Football y validación con ESPN. |
| `espn` (lo elige `auto` si no hay clave válida) | Sin clave | ESPN para todo y football-data.co.uk para validar y para las cuotas de Bet365. Completa con DraftKings (1X2, doble oportunidad y goles). |

Límites del plan gratis de API-Football: 100 peticiones al día, 10 por minuto (el programa espera 6.5 s entre
peticiones) y acceso solo a ayer, hoy y mañana.

`--source auto` (por defecto) usa el modo híbrido si la clave es válida y, si no, solo ESPN. La base de datos de cada
fuente va en un archivo distinto (`futbol.db` para `api-football`; `futbol_espn.db` para `hybrid` y `espn`). En modo ESPN la validación cruzada la hace football-data.co.uk. En una prueba con 224 partidos,
1,636 de 1,642 estadísticas coincidieron con ESPN. Copas europeas, copas nacionales y Liga BetPlay quedan sin segunda
fuente. ESPN no publica el árbitro (football-data solo lo trae en la Premier) y los minutos de los jugadores se aproximan a partir
de la titularidad y los cambios.

Los partidos en los que las dos fuentes no coinciden quedan marcados (`matches.validated = -1`, con el detalle en
`validation_notes` y la comparación de cada estadística en la tabla `validations`).

## Instalación

```bash
pip install -r requirements.txt
cp .env.example .env        # y pon tu API_FOOTBALL_KEY
```

## Uso

```bash
python -m futbol_analyzer run                       # analiza hoy
python -m futbol_analyzer run --date 2026-10-22     # una fecha concreta (>= 2026-10-21)
python -m futbol_analyzer results --date 2026-10-21 # solo guarda resultados y estadísticas, valida y liquida picks
python -m futbol_analyzer team 541                  # ratings guardados de un equipo
python -m futbol_analyzer performance               # aciertos, ROI y Brier históricos
python -m unittest discover tests                   # pruebas sin red
```

El reporte se guarda en `reports/analisis_AAAA-MM-DD.md` y en un `.json` con el mismo nombre.

### Ejecutarlo automáticamente cada día (cron)

```cron
# 09:00 todos los días
0 9 * * * cd /ruta/futbol_analyzer && /usr/bin/python3 -m futbol_analyzer run >> logs.txt 2>&1
```

## Qué hace `run`

1. **Pone al día los resultados** de los 2 días anteriores: guarda marcador, estadísticas de equipo y de jugadores.
2. **Valida** cada partido terminado contra ESPN.
3. **Liquida** las predicciones y combinadas pendientes para medir aciertos y ROI.
4. **Descarga los partidos del día** de las ligas que tengas en `config.LEAGUES`. Si un equipo tiene menos de 6 partidos
   en la base, descarga sus últimos 15 con todas las estadísticas. Además guarda un *snapshot* diario del equipo en
   `team_ratings`: índices de ataque y defensa, promedios y forma.
5. **Modelo**:
   - Para goles, córners, tarjetas, remates y tiros al arco calcula índices de ataque y defensa relativos a la liga,
     con más peso a los partidos recientes y un ajuste hacia la media cuando hay pocos datos (encogimiento bayesiano).
   - Goles: Poisson con corrección Dixon-Coles para los marcadores bajos.
   - Córners, tarjetas y remates: binomial negativa, con la dispersión estimada a partir de la propia liga.
   - Tarjetas: ajustadas por el historial del árbitro.
   - Jugadores: remates y tiros al arco por cada 90 minutos × minutos esperados × ritmo de remates esperado del equipo
     × probabilidad de ser titular.
6. **Mercados óptimos**:
   - Los goles esperados se mezclan al 50 % con los que implican las cuotas de 1X2 y del total de goles.
   - Con cuota real: mezcla la probabilidad del modelo (65 %) con la de la casa sin margen (35 %), calcula el
     valor esperado (EV) y el stake con Kelly ¼. Filtros por defecto: probabilidad ≥ 62 %, EV ≥ 3 % y cuota ≤ 2.60.
   - Sin cuota real (córners, tarjetas, remates, jugadores): una línea por mercado con probabilidad entre 68 % y 84 %,
     y una **cuota mínima** (cuota justa + 5 %). Apuesta solo si tu casa paga al menos esa cuota.
7. **Combinadas** (como mucho una selección por partido, para evitar correlaciones):
   - *Valor*: solo patas con cuota real y EV positivo. Elige las de mayor EV conjunto con probabilidad conjunta ≥ 40 %.
   - *Alta probabilidad*: las de mayor probabilidad conjunta con cuota total ≥ 1.70.

Todos los umbrales están en `futbol_analyzer/config.py`.

## Base de datos (`futbol.db`)

`teams`, `matches`, `team_match_stats`, `player_match_stats`, `team_ratings`, `validations`, `predictions`, `combos`, `api_cache`.

## Notas

- Con el plan gratis (100 peticiones al día), la primera ejecución gasta mucho en completar el historial de los equipos.
  Limita las ligas en `LEAGUES` o sube `FUTBOL_REQUEST_BUDGET` si tienes un plan de pago. Lo ya descargado se guarda
  en caché y no se vuelve a pedir.
- Las probabilidades son estimaciones de un modelo. Revisa `performance` (Brier y ROI) antes de confiar en ellas.
  Ningún modelo garantiza ganancias: apuesta con responsabilidad.
