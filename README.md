# Apuestas: analizador diario de partidos, combinadas y props de la NBA

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
- **Tasa por minuto** de cada estadística, con toda su historia (la temporada anterior pesa la mitad).
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

Qué aporta cada factor (Brier, menor es mejor; base 0.2270): sin defensa por posición 0.2277, sin el
acierto real 0.2279. Las zonas de tiro y el tipo de defensa apenas cambian el resultado global (±0.0001):
se quedan sobre todo como explicación en las fichas. Limitaciones: el backtest no tiene partes de lesiones
históricos ni líneas reales de las casas, que son más difíciles de batir que la mediana. `nba rendimiento`
es la medida honesta con apuestas reales. No hay datos de quién defendió a quién (eso solo está en
stats.nba.com); el "tipo de jugador" se aproxima con la defensa del rival por posición y por zona.

## Pruebas

```bash
python -m unittest -v
```

Las pruebas usan una API simulada con datos sintéticos (`tests/fake_api.py`), solo para
comprobar el código; nunca se usan en los informes.
