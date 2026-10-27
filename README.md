# Apuestas: analizador diario de partidos, combinadas y props de la NBA y la NFL

Busca los partidos de fútbol del día (desde el 21 de octubre de 2026 en adelante), descarga
estadísticas reales de cada equipo y jugador, las guarda en una base de datos local que crece
cada día, calcula probabilidades por mercado, las cruza con las cuotas reales de las casas y
arma combinadas de **alta probabilidad** y de **alto valor**.

> Las apuestas implican riesgo de perder dinero. Las probabilidades son estimaciones, no
> garantías. Apuesta solo lo que puedas permitirte perder.

## Fuentes de datos

| Fuente | Para qué | Clave |
|---|---|---|
| [API-Football](https://www.api-football.com) (api-sports.io) | Partidos del día, estadísticas por partido (córners, tarjetas, goles, tiros a puerta, remates), estadísticas de jugadores, cuotas de varias casas | Obligatoria. Plan gratuito: 100 peticiones/día |
| [football-data.org](https://www.football-data.org) | Segunda fuente independiente para validar horarios y marcadores | Opcional, gratuita |

No se inventa ningún dato: si falta la clave o la API no tiene cobertura de un partido, el
programa lo dice y lo deja fuera del análisis.

## Instalación

```bash
python3 -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env      # y pon tu API_FOOTBALL_KEY
```

Requiere Python 3.10 o superior.

## Uso

```bash
python -m apuestas analizar                    # partidos de hoy
python -m apuestas analizar --fecha 2026-10-22
python -m apuestas actualizar                  # guarda resultados de ayer y liquida las selecciones
python -m apuestas diario                      # actualizar (ayer) + analizar (hoy)
python -m apuestas validar --fecha 2026-10-21  # contrasta con football-data.org
python -m apuestas rendimiento                 # acierto real del modelo hasta ahora
```

Opciones útiles de `analizar`:

- `--sin-jugadores`: no descarga estadísticas de jugadores (la mitad de peticiones).
- `--incluir-sin-cuota`: incluye mercados para los que la API no da cuota (p. ej. tiros de
  jugador). En ese caso el informe muestra la **cuota justa**: solo tiene valor si tu casa paga más.
- `--sin-descarga`: re-analiza con lo que ya está en la base, sin gastar peticiones.

Cada ejecución genera `reportes/AAAA-MM-DD.md` (legible) y `reportes/AAAA-MM-DD.json`.

### Programarlo cada día

Linux/macOS (`crontab -e`), todos los días a las 9:00:

```
0 9 * * * cd /ruta/a/apuestas && .venv/bin/python -m apuestas diario >> reportes/cron.log 2>&1
```

Windows: Programador de tareas → acción `python -m apuestas diario` con "Iniciar en" la carpeta del proyecto.

## Cómo funciona

1. **Recolección** (`collector.py`). Pide los partidos del día, filtra por las ligas de
   `APUESTAS_LIGAS` y, para cada equipo, descarga sus últimos partidos con estadísticas de
   equipo y jugadores. Un partido ya guardado nunca se vuelve a pedir, así que con los días
   cada análisis gasta menos peticiones. Si se alcanza el presupuesto, se detiene sin perder
   lo descargado.
2. **Base de datos** (`data/apuestas.db`, SQLite). Tablas `teams`, `fixtures`, `team_stats`
   (goles, córners, amarillas, rojas, tiros a puerta, remates, faltas, posesión, xG por equipo
   y partido), `player_stats`, `odds`, `picks`, `combos` y `validations`.
3. **Modelo** (`model.py`). Para cada estadística: ataque del equipo × lo que concede el rival
   ÷ media de la liga, con más peso a los partidos recientes, ventaja de local y contracción
   hacia la media cuando hay pocos datos. Goles con Poisson; córners, tarjetas y tiros con
   binomial negativa (más varianza, como en la realidad). Jugadores: tasa por 90 minutos ×
   minutos esperados × debilidad del rival.
4. **Valor** (`odds.py`). Cuota mediana entre casas, probabilidad implícita del mercado sin
   margen, y probabilidad final = mezcla modelo/mercado (`APUESTAS_PESO_MODELO`). Valor =
   probabilidad final × cuota − 1.
5. **Combinadas** (`combinadas.py`). Máximo una selección por partido (las del mismo partido
   están correlacionadas). Perfil *alta probabilidad*: la mayor probabilidad conjunta con
   cuota ≥ 2.00. Perfil *valor*: el mayor EV con probabilidad conjunta ≥ 35 %. Se sugiere un
   stake de ¼ de Kelly con tope del 2 % del bankroll.
6. **Seguimiento** (`settle.py`). `actualizar` liquida cada selección con el resultado real y
   `rendimiento` muestra acierto y beneficio por mercado: la única forma honesta de saber si
   el modelo funciona. Si el acierto real queda por debajo de la probabilidad media
   estimada, sube `APUESTAS_PROB_MIN` o baja `APUESTAS_PESO_MODELO`.

## Límites a tener en cuenta

- El plan gratuito de API-Football solo da partidos de ayer, hoy y mañana (y temporadas
  2022-2024), 100 peticiones al día y 10 por minuto. No permite descargar el historial de esta
  temporada, así que la base se llena día a día con `actualizar` y el modelo propio se activa
  cuando cada equipo tiene al menos 4 partidos guardados. Mientras tanto, el análisis usa solo
  las probabilidades implícitas de las casas (sin margen), que no sirven para encontrar valor.
  Con un plan de pago el historial se descarga al momento.
- Revisa en tu panel de API-Football que tu plan incluye la temporada actual y las cuotas.
- Las casas no siempre publican cuotas de córners, tarjetas o tiros en la API; sin cuota no
  hay forma de medir el valor, solo la cuota justa.
- El modelo no conoce lesiones, rotaciones ni alineaciones. Revísalas antes de apostar.

## NBA: player props por probabilidad

Calcula la probabilidad de que cada prop del día pase (puntos, rebotes, asistencias, triples, robos,
tapones, pérdidas, PRA y sus combinaciones, tiros de campo y tiros libres) y ordena las más probables.

| Fuente | Para qué | Clave |
|---|---|---|
| ESPN (API pública) | Calendario, box score de cada jugador, **cada tiro con sus coordenadas** (zonas), posiciones y parte de lesiones | No necesita |
| [SportsGameOdds](https://sportsgameodds.com) | Líneas y cuotas de props de varias casas (FanDuel, DraftKings, Caesars, BetMGM...) | `SPORTSGAMEODDS_KEY`. Plan gratuito: 2.500 partidos/mes, se piden solo los del día |

```bash
python -m apuestas nba historial --desde 2025-10-21     # una vez: temporada pasada + actual (~1.400 partidos, ~15 min)
python -m apuestas nba analizar                         # props de hoy -> reportes/nba/AAAA-MM-DD.md y .json
python -m apuestas nba actualizar                       # resultados de ayer + liquidación (analizar ya lo hace)
python -m apuestas nba rendimiento                      # acierto real por tramo de probabilidad y estadística
python -m apuestas nba backtest --desde 2026-02-01 --hasta 2026-03-31
```

### Qué tiene en cuenta (`apuestas/nba/modelo.py`)

- **Minutos esperados**: últimos 10 partidos con más peso a los recientes; en cuanto empieza la
  temporada, los minutos de la anterior casi no cuentan (los roles cambian). Back-to-back: -3 %.
- **Tasa por minuto** de cada estadística, con toda su historia (la temporada anterior pesa la mitad y,
  en cuanto hay partidos de la nueva, como mucho lo que 4 partidos). Si un jugador cambia de rol (tasa
  ±30 % con menos de 10 partidos), la línea de la casa pesa más (60 %): conoce el rol nuevo.
- **Bajas**: si un compañero importante está fuera, compara al jugador con y sin él (minutos y tasas).
  Si ese compañero ya faltaba en los últimos partidos, la baja ya está en sus minutos y no se suma.
- **Defensa rival por posición**: lo que concede el rival por minuto a bases, aleros o pívots.
- **Zonas de tiro**: dónde tira el jugador (aro, pintura, media distancia, triple de esquina y frontal),
  su acierto en cada zona y lo que concede el rival ahí. Ajusta puntos y triples.
- **Tipo de defensa**: cómo le fue contra defensas fuertes, medias y débiles en esa estadística.
- **Acierto real** sobre esa misma línea en sus últimos 15 partidos.
- **La casa**: su probabilidad sin margen se mezcla con la del modelo (`APUESTAS_NBA_PESO_MERCADO`,
  0.4 por defecto). Cuando modelo y casa discrepan mucho, la casa suele saber algo (rol, rotación, una baja).

### Cada prop, desde las estadísticas que la producen (`apuestas/nba/desglose.py`)

La media de cada prop se construye también desde sus componentes, y el informe explica de dónde sale.
Por ejemplo, "¿por qué 30 PRA?":

- **Puntos** = tiros de campo esperados (su ritmo × minutos × cuántos tiros concede el rival) × puntos
  por tiro (su reparto por zonas × su acierto en cada zona, ajustado por lo que concede el rival ahí)
  + tiros libres × su % de libres.
- **Rebotes** = % de los fallos del rival que captura mientras está en pista × fallos esperados del
  rival + % de los fallos de su equipo que captura en ataque × fallos esperados de su equipo.
- **Asistencias** = % de las canastas de sus compañeros que asiste con él en pista × canastas esperadas.
- **Triples** = triples intentados × % esperado (esquina y frontal). **Robos** = % de las pérdidas del
  rival que roba × pérdidas esperadas. **Tapones** = % de los tiros de 2 del rival que tapona × tiros de
  2 esperados. **Pérdidas** = pérdidas por jugada × jugadas que usa × presión del rival.

Lo "esperado" del partido cruza el ataque de un equipo con la defensa del otro (por 48 minutos). Junto a
cada prop se muestran sus estadísticas relacionadas (minutos, tiros, porcentajes, % de rebotes...) en
los últimos 5 y 10 partidos, la temporada, la anterior y contra este rival. Todo queda guardado en la
base: la tabla `nba_analisis` tiene cada prop evaluada con su desglose y sus métricas (JSON), y la vista
`nba_team_games` los totales de cada equipo por partido.

La proyección final mezcla 30 % de este desglose y 70 % de tasa por minuto × defensa rival por posición:
en el backtest ambas aciertan casi igual (Brier 0.2270 frente a 0.2282 usando solo el desglose), así que
el desglose sirve sobre todo para explicar cada número y detectar cuándo algo no cuadra.

La distribución es binomial negativa con la dispersión propia del jugador más la incertidumbre de sus
minutos. El informe muestra, por partido, las props más probables y una ficha de los jugadores
destacados: minutos, notas de bajas, su prop más probable, la línea que pasaría con 80 % de
probabilidad (útil para líneas alternativas), su rendimiento según el tipo de defensa y la tabla de zonas.

### Quién lo defiende: stats.nba.com (`nba enfrentamientos`)

`python -m apuestas nba enfrentamientos` descarga de stats.nba.com, partido a partido, **quién defendió a
quién** (posesiones y puntos de cada atacante contra cada defensor) y estadísticas avanzadas de temporada
(uso, % de rebotes y asistencias). Con eso, para cada jugador (`apuestas/nba/marcajes.py`):

- qué defensores del rival suelen marcar a su posición y qué parte de las posesiones se lleva cada uno
  (sin los que están fuera hoy);
- qué tan buenos son: puntos que permiten por 100 posesiones (élite / medio / débil);
- cómo le va a él contra cada nivel de defensor y contra cada defensor concreto.

El ajuste se aplica a puntos, tiros anotados y triples (máximo ±12 %) y aparece en el "¿por qué?" de cada
prop. Aún no está validado con backtest: hace falta descargar primero los datos; después,
`nba backtest` lo incluye automáticamente.

**stats.nba.com bloquea los servidores en la nube**, incluidos los de GitHub Actions (probado: la consulta
se queda colgada). Funciona desde una conexión de casa, así que hay dos formas de ejecutarlo:

1. En tu computadora: `python -m apuestas nba enfrentamientos` (la primera vez, unas 1.400 consultas, ~30 min).
2. Con un proxy residencial o un runner autohospedado de GitHub Actions en una computadora de casa.

### Automático cada día en GitHub (`.github/workflows/nba-diario.yml`)

Corre en los servidores de GitHub a las 10:47 (Ciudad de México): guarda los resultados de ayer, liquida
las props, baja lesiones y líneas de hoy y publica el informe en la rama `nba-informes`
(`ultimo.md` y `nba/AAAA-MM-DD.md`). Necesita el secreto `SPORTSGAMEODDS_KEY` (*Settings → Secrets and
variables → Actions*) y que el flujo esté en `main` para el horario y el botón *Run workflow*. La base se
conserva con la caché de Actions; si se pierde, se reconstruye sola desde ESPN.

### ¿Está calibrado?

Backtest del 20 de febrero al 10 de marzo de 2026 (19.700 props, línea de referencia = mediana de los
últimos 10 partidos del jugador, sin cuotas):

| El modelo dice | Pasó |
|---|---|
| 65-70 % (media 67.4 %) | 67.3 % |
| 70-75 % (media 72.2 %) | 71.6 % |
| 75-80 % (media 77.2 %) | 78.8 % |
| 80-85 % (media 82.2 %) | 85.4 % |
| 85 %+ (media 88.4 %) | 91.0 % |

Arranque de temporada (22 oct-25 nov de 2025, con 2024-25 como temporada anterior): en jugadores con
cambio de rol, limitar la temporada anterior a 4 partidos baja el Brier de 0.2274 a 0.2256; en el resto
no cambia.

Qué aporta cada factor (Brier, menor es mejor; base 0.2270): sin defensa por posición 0.2277, sin el
acierto real 0.2279. Las zonas de tiro y el tipo de defensa apenas cambian el resultado global (±0.0001):
se quedan sobre todo como explicación en las fichas. Limitaciones: el backtest no tiene partes de lesiones
históricos ni líneas reales de las casas, que son más difíciles de batir que la mediana. `nba rendimiento`
es la medida honesta con apuestas reales. No hay datos de quién defendió a quién (eso solo está en
stats.nba.com); el "tipo de jugador" se aproxima con la defensa del rival por posición y por zona.

## NFL: props, touchdowns y enfrentamientos (`apuestas/nfl/`)

Evalúa **todos los mercados** que publican las casas para cada partido (unos 150-500 por partido), calcula quién
tiene más probabilidad de **anotar un TD**, de **anotar 2 o más** y de anotar el **primer TD**, lee el
enfrentamiento métrica a métrica y cruza todo con las líneas de las casas para encontrar las mejores:

| Familia | Mercados |
|---|---|
| Props de jugador | yardas de pase, por tierra y por recepción; recepciones, envíos, acarreos, pases completos e intentados; TD de pase, intercepciones; combinadas (carrera + recepción, pase + carrera); recepción, carrera y pase completo más largos; yardas por acarreo; puntos de fantasy |
| Touchdowns | anota (sí/no), 2+ y 3+ TD, primer y último TD del partido, primer TD de la 2.ª mitad, anota en la 1.ª/2.ª mitad o en un cuarto |
| Props por periodo | las mismas props de jugador en el 1.er, 2.º, 3.er y 4.º cuarto y en cada mitad |
| Defensa | sacks, tacleadas (combinadas, en solitario y asistidas), intercepciones del defensor |
| Pateador | goles de campo, puntos extra, puntos del pateador |
| Partido y equipo | moneyline, spread, total y total por equipo (partido, mitades y cada cuarto); par/impar; resultado a 3 vías; si un equipo anota en el periodo; quién anota primero y último; si anotan los dos en un cuarto; número de TD y de goles de campo (total, por equipo y por periodo); gol de campo más largo; mayor ventaja; safety; pérdidas de balón; punts; sacks de equipo |

| Fuente | Para qué | Clave |
|---|---|---|
| [nflverse](https://github.com/nflverse/nflverse-data) | Estadísticas por jugador y partido (150 columnas: EPA, CPOE, air yards, target share, WOPR...), **jugada a jugada** (zona roja, dentro de la 10 y la 5, envíos a la zona de anotación, scrambles frente a carreras diseñadas), calendario con líneas de cierre y clima, plantillas semana a semana, parte oficial de lesiones y snaps | No necesita. Se actualiza cada noche |
| ESPN (API pública) | Parte de lesiones al momento (con comentarios) y movimientos de plantilla (traspasos) | No necesita |
| [SportsGameOdds](https://sportsgameodds.com) | Línea de cada casa (FanDuel, DraftKings, Caesars, BetMGM, ESPN BET, Bovada...), consenso, cuota justa sin margen y línea de apertura | `SPORTSGAMEODDS_KEY` (la misma de la NBA) |

```bash
python -m apuestas nfl actualizar                      # la primera vez descarga 3 temporadas (~1 min); luego solo lo que cambió
python -m apuestas nfl analizar                        # próximos 7 días -> reportes/nfl/AAAA-MM-DD.md y .json
python -m apuestas nfl td --multiples                  # ranking de TD (ordenado por 2+ TD)
python -m apuestas nfl td --razonar 5                  # y el razonamiento paso a paso de los 5 primeros
python -m apuestas nfl mercados --tipo partido         # todos los mercados evaluados (jugador, periodos, td,
python -m apuestas nfl mercados --texto "1.er cuarto"  #   defensa, pateador, partido), ordenados por valor
python -m apuestas nfl validar "Bills -3.5"            # también spread, ML, totales, periodos, quién anota primero
python -m apuestas nfl validar "más de 47.5 puntos Packers Panthers 1.ª mitad"
python -m apuestas nfl validar "Zack Baun más de 7.5 tacleadas"
python -m apuestas nfl matchup bills ravens            # ataque contra defensa, métrica a métrica
python -m apuestas nfl validar "Derrick Henry +2 TD"   # ¿es buena? ¿por qué la juega la gente?
python -m apuestas nfl validar "Josh Allen 2 touchdowns contra los Chargers"
python -m apuestas nfl validar "Saquon más de 69.5 yardas por tierra @ -110"
python -m apuestas nfl jugador "Josh Allen"            # ficha: rol, últimos partidos, tendencias, contra quién anota
python -m apuestas nfl rendimiento                     # acierto real de lo recomendado y lo validado
python -m apuestas nfl backtest --desde 2025-10-01 --hasta 2026-01-05
```

### La base de datos se mantiene sola

`nfl actualizar` (y `nfl analizar`, que lo llama antes) pide cada archivo de nflverse con su ETag: si no cambió, no
lo descarga, así que se puede ejecutar varias veces al día. Guarda:

- `nfl_games`: calendario, marcador, spread y total de cierre, techo, superficie, temperatura, viento, QB titular.
- `nfl_player_games` + `nfl_player_pbp` + `nfl_snaps`: todo lo que hizo cada jugador en cada partido.
- `nfl_team_games`: cada partido de cada equipo (jugadas, dropbacks, EPA por jugada / pase / carrera, % de éxito,
  jugadas explosivas, visitas y TD en zona roja, terceras, sacks, pérdidas, pase sobre lo esperado, carreras del QB).
  Lo que concede una defensa es la fila de su rival; la vista `nfl_def_pos` lo desglosa por posición.
- `nfl_rosters` y `nfl_movimientos`: equipo actual de cada jugador y **traspasos** (semana a semana de nflverse y,
  más rápido, los "Traded ... to ..." de ESPN).
- `nfl_injuries`: parte oficial de la semana y el de ESPN al momento (manda el más reciente).
- `nfl_lineas`: cada línea de cada casa cada vez que se descarga (histórico para ver cómo se mueve el mercado).
- `nfl_picks`: lo recomendado y lo validado, con sus razones, liquidado con el resultado real.

### Cómo proyecta (`apuestas/nfl/modelo.py`)

1. **Entorno del partido**: puntos esperados del equipo (el total del equipo de las casas; si no hay, total y spread;
   si no, ataque × defensa rival), dropbacks y carreras (ritmo propio, del rival y **guion**: el favorito corre más),
   TD de ataque = puntos × TD por punto, repartidos entre pase y carrera según el equipo y lo que concede el rival.
   Viento fuerte (15+ mph) recorta el juego aéreo.
2. **Reparto**: cuota de acarreos, envíos y pases de cada jugador con más peso a lo reciente, sin contar los partidos
   que dejó a medias (menos de la mitad de sus snaps habituales). **Bajas**: quien está fuera (Out, IR, Doubtful,
   suspendido, cortado) no se proyecta y su volumen se reparte entre el resto; si el QB titular no juega, el suplente
   pasa a lanzar. "Questionable": volumen ×0.92. **Traspasos**: tras un cambio de equipo cuentan los partidos con el
   equipo nuevo (si hay pocos, la casa pesa más).
3. **Eficiencia contra el rival por posición**: yardas por acarreo, por envío, % de recepción, yardas por pase,
   intercepciones; las del jugador contraídas hacia su posición y ajustadas por lo que el rival concede **a esa
   posición** (no es lo mismo una defensa que sufre contra los TE que contra los WR). Los QB corredores se miden contra
   las yardas y TD por tierra que la defensa concede a los QB.
4. **Touchdowns**: TD por tierra del equipo × su cuota de oportunidades cerca de la meta (dentro de la 10 pesa más que
   la zona roja y que los acarreos totales) + TD por aire del equipo × su cuota de envíos en zona roja y a la zona de
   anotación, ajustado por el % de TD que el rival concede a su posición. P(1+), P(2+) y P(3+) con binomial negativa;
   el primer TD reparte la probabilidad de que haya alguno según los TD esperados de cada jugador.

### La lectura del tipster (`razones.lectura_td`, `nfl td --razonar N`, `nfl validar`)

Para cada candidato a TD, el razonamiento paso a paso: el partido (puntos y TD esperados, guion), el QB (si juega
un suplente y qué cambia), el rival en la zona roja (% de TD por visita y visitas que concede, con su puesto), lo
que concede a su posición, su papel cerca de la meta (acarreos dentro de la 10, zona roja, envíos a la zona de
anotación), su eficiencia convirtiendo frente a la media de su posición, su temporada, y la conclusión: si la
apuesta con valor es "anota" o "2+ TD" y a qué cuota mínima. Aparece en el informe ("La lectura de los mejores
candidatos"), en `nfl td --razonar 5` y en `nfl validar` para cualquier apuesta de TD.

**QB suplente.** Se detecta solo (el QB con más titularidades de la temporada no juega). Comparando a 33
equipos-temporada consigo mismos (2024-2026), con suplente: TD de pase -28 %, TD de carrera -7 %, puntos -13 %,
visitas a la zona roja -15 %, y el RB1 recibe un 9 % más de los acarreos dentro de la 10 (22 de 33 equipos). Es
decir, la lógica de "se la van a dar al RB" se cumple en el reparto, pero el equipo llega menos a la zona roja. En el
backtest de 2025, convertir eso en multiplicadores no mejora las predicciones (Brier de TD 0.1502 frente a 0.1500):
la línea de la casa ya descuenta al suplente. Por eso entra como razonamiento con sus datos, no como ajuste.

**Titular que vuelve de lesión.** Si un jugador que ya era parte del equipo vuelve tras faltar, a quienes lo
sustituyeron se les descuenta (a mitad de fuerza) el volumen que ganaron en su ausencia. Caso Saquon Barkley y
Dameon Pierce (26-10-2026): sin corrección el modelo daba 6.9 y 14 acarreos; con ella, 10.9 y 9.2; en el partido
se repartieron 7 y 7 al empezar el 3.er cuarto. Efecto neutro en el backtest.

### Mercados de partido: un simulador posesión a posesión (`apuestas/nfl/modelo_partido.py`)

Cada partido se simula 4.000 veces. Las posesiones de cada equipo (ritmo propio y del rival) se reparten por cuartos;
cada posesión termina en TD, gol de campo o nada (y, rara vez, en safety o TD de la defensa), con probabilidades que
salen del **modelo propio, sin la línea de la casa** (TD esperados de ataque × defensa rival, goles de campo
esperados) y con más anotación en el 2.º y 4.º cuarto, como en los datos. Cada equipo lleva un factor de forma
aleatorio en cada simulación y los empates van a prórroga. De las mismas simulaciones salen, de forma coherente
entre sí, moneyline, spread, totales, periodos, par/impar, 3 vías, quién anota primero y último, ambos anotan, TD y
FG, FG más largo (con las distancias reales de la liga), mayor ventaja, safety y las props de los pateadores.

Las props por periodo de cada jugador usan la parte del partido que suele pasar en ese periodo (calculada de las
estadísticas por cuarto de toda la liga) con más dispersión cuanto más corto es el periodo. Las defensivas, la media
del defensor × las jugadas esperadas del rival y su tipo (más carreras: más tacleadas de LB y línea) × lo que su ataque
deja capturar a su QB o pierde el balón. Todo se liquida solo con el resultado real (`nfl_anotaciones` guarda cada
cambio del marcador; `nfl_player_quarter`, las estadísticas por cuarto).

Medido en el backtest de 2025 (semanas 5-18, `nfl backtest --partidos`): el simulador acierta al **ganador** mejor que
el azar (Brier 0.222 frente a 0.250), pero **no le gana al spread ni al total de cierre** (0.257 y 0.262): esas líneas
son muy eficientes. Por eso en spread y totales la casa pesa 85 % en la probabilidad final, en el resto de mercados
de partido 60 %, y conviene tratarlos como referencia, no como fuente de valor.

### Pensar como un tipster (`analizador.py`, `mercado.py`, `razones.py`, `validar.py`)

- **Mejor línea**: para cada apuesta se busca la casa que mejor paga (o la línea alternativa más barata).
- **Probabilidad final** = 65 % modelo + 35 % casa sin margen (`APUESTAS_NFL_PESO_MERCADO`). Si el jugador acaba de
  llegar, tiene poca muestra o está en duda, la casa pesa 60 %; si modelo y casa discrepan más de 15 puntos, 60 %, y
  más de 25, 75 %: casi siempre la casa sabe algo (un rol nuevo, quién vuelve de lesión).
- **Con valor** = EV ≥ 4 % (`APUESTAS_NFL_VALOR_MIN`), el modelo ve al menos 3 puntos más que la casa, y no es un
  "chollo imposible" (el modelo no ve más de 1.6 veces lo que ve la casa ni difiere en más de 25 puntos, y la cuota
  no es más de 1.5 veces la de consenso, que suele ser una línea caducada).
- **Movimiento de línea**: de la apertura a ahora. Si la cuota baja o la línea sube en un lado, entra dinero ahí; se
  marca como razón a favor o en contra.
- **"¿Por qué la gente apuesta esto?"**: el validador busca la narrativa en los datos (el último partido, la racha,
  su volumen de TD, su historial contra el rival, el movimiento de la línea, el atractivo de las cuotas altas) y
  después la contrasta con el modelo: veredicto, cuota justa y cuota mínima a la que vale la pena.
- **El "¿por qué?" de cada apuesta**: volumen esperado, entorno del partido, lo que concede el rival a su posición
  (con su puesto en la liga), su acierto sobre esa misma línea (últimos 5, 10 y temporada), rachas, contra este rival,
  contra defensas fuertes / medias / débiles en lo que mide la apuesta, local o visitante, bajas y traspasos.
- **El enfrentamiento** (`nfl matchup` y cada partido del informe): EPA por jugada, por acarreo y por dropback, yardas
  por acarreo y por pase, explosivas, zona roja, TD por partido, terceras, sacks, QB corredor, identidad del ataque
  (pase sobre lo esperado) y lo que la defensa concede a RB, WR y TE, con veredicto: ventaja del ataque, de la defensa,
  fuerza contra fuerza o debilidad contra debilidad.

Ejemplo con los datos del 26 de octubre de 2026 (`nfl validar "Josh Allen 2 touchdowns contra los Chargers"`): *"LAC concede 0.25 TD por tierra por partido a los QB (liga
0.19; 8º que más de 32) (+29%)"*, *"Zona roja: Bills 68% (3º de 32) contra Chargers que concede 50%"*, y la
advertencia de que las apuestas de múltiples TD atraen por el premio y las casas cobran más margen en ellas.

### ¿Está calibrado?

Backtest de la temporada 2025, semanas 5 a 18 (cada partido predicho solo con datos anteriores; líneas de cierre de
nflverse para el entorno; los jugadores que no jugaron cuentan como bajas conocidas):

| Anotar 1+ TD: el modelo dice | Pasó |
|---|---|
| 0-10 % (media 6.2 %) | 6.7 % |
| 10-20 % (media 14.9 %) | 15.2 % |
| 20-30 % (media 24.7 %) | 26.0 % |
| 30-40 % (media 34.2 %) | 34.4 % |
| 40-50 % (media 44.4 %) | 42.5 % |
| 50-60 % (media 53.7 %) | 55.4 % |

Brier de anotar 1+ TD 0.1466 frente a 0.1532 de su propia frecuencia histórica; 2+ TD: dice 3.3 % de media y pasó
3.8 %. En yardas y conteos (línea de referencia = mediana de sus últimos 8 partidos) el modelo gana a la referencia
en todas las estadísticas (p. ej. yardas de pase 0.2227 frente a 0.2546, acarreos 0.2155 frente a 0.2358), pero por
encima del 70 % es optimista (dice 74-86 %, pasa 61-77 %): por eso la casa pesa en la probabilidad final y las
selecciones exigen valor, no solo probabilidad. La calibración (logit × 0.75 en yardas y conteos; TD esperados
comprimidos con exponente 0.85) sale de este mismo backtest. `nfl rendimiento` es la medida honesta con líneas reales.

La puntuación de fantasy es la de las líneas de las casas tipo PrizePicks (yardas de pase /25, TD de pase 4,
intercepción -1, yardas /10, recepción 1, TD 6, balón perdido -1); si tu casa puntúa distinto, la línea no es
comparable.

Limitaciones: nflverse publica las estadísticas la noche del partido (los datos de la jornada en curso llegan al día
siguiente); no hay porcentajes de apuestas del público (se usa el movimiento de la línea como señal de dónde entra el
dinero); no hay datos de coberturas (hombre/zona) ni de presión por jugada; las líneas históricas de las casas no
están en el backtest.

### Automático cada día en GitHub (`.github/workflows/nfl-diario.yml`)

Igual que el de la NBA: actualiza la base, analiza los próximos 7 días y publica el informe en la rama `nfl-informes`
(`ultimo.md` y `nfl/AAAA-MM-DD.md`). Usa el mismo secreto `SPORTSGAMEODDS_KEY` y necesita estar en `main`.

## Pruebas

```bash
python -m unittest -v
```

Las pruebas usan una API simulada con datos sintéticos (`tests/fake_api.py`), solo para
comprobar el código; nunca se usan en los informes.
