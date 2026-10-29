# Apuestas

Este repositorio contiene dos cosas:

1. **`nbaev/` — sistema de props NBA con valor esperado** (en construcción por fases, ver abajo). Estima la
   probabilidad de cada prop de jugador con una simulación del partido, la compara con las cuotas sin margen y
   solo señala apuestas con EV positivo en mercados que hayan superado el backtest.
2. **`apuestas/` — analizador** de fútbol, props NBA y **NFL** (props de todos los mercados, touchdowns, zona roja, hojas de picks y combinadas; documentado más abajo, en "Sistema anterior" y "NFL").

> Las apuestas implican riesgo de perder dinero. Ningún modelo garantiza ganancias: las casas tienen margen,
> información y límites. Este sistema está pensado para medir con honestidad si existe ventaja y desactivar
> lo que no la tenga.

## nbaev: props NBA con valor esperado

### Uso rápido (cada día)

```bash
pip install -r requirements.txt
python -m nbaev datos historial            # solo la primera vez (~40 min): histórico desde 2021-22
python -m nbaev diario                     # datos, lesiones, cuotas, simulación y picks de hoy
python -m nbaev props --n 8                # las 8 mejores props del día, con su estado de validación
python -m nbaev datos importar-csv b365.csv && python -m nbaev diario --sin-actualizar   # con cuotas de bet365
streamlit run nbaev/app/dashboard.py       # tabla completa con filtros
```

Repite `python -m nbaev diario` cerca del inicio de los partidos (lesiones y cuotas más recientes). **Estado actual:
ningún mercado está validado** (ver fases 4 y 6): las props salen con monto 0 y son informativas.

### Plan por fases

| Fase | Contenido | Estado |
|---|---|---|
| 1 | Datos: box scores, jugada a jugada, cuartos, quintetos, primer anotador, contexto, lesiones, cuotas | **hecha** |
| 2 | Proyección de minutos | **hecha** |
| 3 | Modelo de puntos (distribución completa + Monte Carlo) | **hecha** |
| 4 | Validación walk-forward y backtest con cuotas reales | **hecha** (puntos: desactivado) |
| 5 | Comparación con cuotas sin margen, filtros y banca (Kelly fraccional) | **hecha** |
| 6 | Resto de mercados, validados uno a uno, y combinadas | **hecha** (ninguno validado) |

### Resultados de la fase 1 (26/10/2026)

- **Partidos**: 6.676 terminados, de 2021-22 a la temporada actual (regular, play-in y playoffs), con box score y
  jugada a jugada. Faltan 4 de playoffs de 2026 que ESPN no tiene (devuelve 404).
- **Jugada a jugada frente al box score** (fracción de jugadores cuya suma por cuartos cuadra exactamente):
  puntos 99,9 %, triples 100 %, libres 100 %, asistencias 99,7 %, rebotes 99,5-99,8 %, tapones 99,7 %,
  robos 99,5 %, pérdidas 98,2 %. Minutos reconstruidos con los cambios: error medio de 0,25 min (el box de ESPN
  redondea al entero).
- **Primer anotador**: salto inicial identificado en el 99,7 % de los partidos, titulares en el 99,9 %, primera
  canasta en el 100 %. El equipo que gana el salto anota primero el 63-65 % de las veces.
- **Spread y total previos**: 100 % de los partidos (pickcenter de ESPN, API core de ESPN y cierre de SportsGameOdds).
  Control: el total implícito de cada equipo tiene correlación 0,55 con sus puntos reales y sesgo de +0,2 puntos.
- **Cuotas históricas reales** (SportsGameOdds, consenso de casas de EE. UU.), 2025-26: 1.320 partidos con cierre
  (desde octubre de 2025) y 710 con apertura (desde el 17/01/2026); 1,24 millones de cuotas. Jugador emparejado
  con ESPN en el 99,95 %. El resultado que guarda la fuente coincide con el box de ESPN en el 96-99,9 % de los casos;
  para liquidar se usará siempre el box de ESPN.
- **Margen de la casa en el cierre** (overround medio over+under): ~6,5 % en puntos, 6,7-7,3 % en rebotes,
  asistencias y combinados, ~7 % en triples, robos y tapones. Es el listón que el modelo tiene que superar.
- **Catálogo de mercados**: 40 combinaciones vistas, todas "sin validar". En el histórico solo hay mercados de
  partido completo: SportsGameOdds no conserva apertura/cierre de 1.er cuarto, 1.ª mitad ni primera canasta, así
  que esos mercados solo se podrán validar con las capturas diarias que se acumulen desde ahora.

### Fase 2: proyección de minutos (`nbaev/features/minutos.py`, `nbaev/models/minutos.py`)

```bash
python -m nbaev minutos validar      # walk-forward mensual -> reportes/fase2_minutos.md
python -m nbaev minutos entrenar     # entrena con todo el histórico (data/modelos/minutos.joblib)
python -m nbaev minutos proyectar    # minutos de los partidos de hoy (tabla proj_minutos)
```

- **Población**: jugadores vestidos (jugaron o DNP técnico). Los lesionados no se proyectan: el parte de lesiones
  dice antes del partido que no juegan. En partidos futuros la plantilla probable son los que aparecieron en los
  últimos 5 partidos del equipo esta temporada (sin traspasados) más los del parte de lesiones, cada uno con una
  probabilidad de jugar según su estado (`minutos.prob_juega` en la configuración: Out 0, Doubtful 0,25,
  Questionable 0,5, Day-To-Day 0,65; es una heurística sin calibrar porque no hay partes históricos).
- **Bajas de compañeros**: ESPN casi nunca lista a los lesionados, así que no se cuentan uno a uno. Se mide cuántos
  minutos habituales hay disponibles en el equipo frente a lo normal (`libres`, también por posición) y se reparte
  la base de cada jugador para que el equipo sume 240 (`min_norm`).
- **Modelo**: LightGBM con 34 variables (historial del jugador, rol, minutos liberados, descanso, viaje, spread y
  total). Da la media con riesgo de no jugar, la media y los cuantiles 10/50/90 **si juega** (las props se anulan si
  no juega) y la P(DNP técnico). Las medias de cada equipo se reparten para sumar los minutos de un partido.
- **Resultado** (walk-forward mensual, oct-2023 a oct-2026, 102.378 filas fuera de muestra; informe completo en
  `docs/resultados/fase2_minutos.md`): error medio de **4,49 min** frente a 5,24 del mejor baseline (−14 %; bootstrap
  por partido: −0,75 min, IC 95 % [−0,78, −0,71]). En jugadores con prop: 4,53 frente a 5,10. Mejora en todos los
  segmentos (bajas de compañeros 5,15 frente a 6,26; vuelta de lesión 5,06 frente a 6,03; playoffs 4,04 frente a
  5,11). Cuantiles si juega: cobertura real 9,7 / 49,6 / 89,0 % (nominal 10 / 50 / 90). P(DNP) calibrada: Brier
  0,079 frente a 0,093 de la tasa reciente del jugador.
- **Limitaciones**: en jugadores con prop y proyección baja (< 15 min) el modelo se queda 3 min corto: la casa saca
  prop cuando espera más rol (sabe de bajas o cambios que el modelo no ve). No se usa el quinteto titular confirmado
  (no hay histórico fiable antes del salto); usarlo cuando se publique mejoraría la proyección.

### Fase 3: modelo de puntos (`nbaev/features/produccion.py`, `nbaev/models/simulacion.py`, `nbaev/models/puntos.py`)

```bash
python -m nbaev puntos validar      # walk-forward con minutos fuera de muestra y líneas reales -> reportes/fase3_puntos.md
python -m nbaev puntos proyectar    # distribución de puntos de hoy (10.000 simulaciones; tabla proj_puntos)
```

- **Tasas** por minuto de cada jugador (media exponencial con regresión bayesiana hacia su posición) y porcentajes
  de 2, 3 y libres encogidos; defensa rival por posición, rating defensivo, ritmo esperado y total implícito.
- **LightGBM** predice los puntos por minuto con ese contexto; la simulación escala los volúmenes de tiro del
  jugador para reproducir esa media sin cambiar su perfil (reparto 2/3, libres, acierto).
- **Simulación Monte Carlo** por componentes: minutos (fase 2, con efecto paliza según el margen sorteado) ->
  intentos (binomial negativa) -> aciertos (beta-binomial), con ritmo del partido y acierto de cada equipo
  compartidos. Puntos, triples, tiros de campo y libres salen de la misma simulación: todas las líneas son
  coherentes (P(25+) ≤ P(20+) siempre). La varianza de cada componente se estima con datos (método de momentos).
- **Resultados** (walk-forward mensual oct-2023 a oct-2026, 85.732 actuaciones con minutos también fuera de
  muestra; informe completo en `docs/resultados/fase3_puntos.md`):
  - Error medio de la media: **4,40 puntos** frente a 4,57 del baseline (estable en las 3 temporadas). En jugadores
    con prop: 4,90 frente a **4,78 de la línea de cierre de la casa**: la casa estima mejor la media.
  - Distribución calibrada: PIT aleatorizado casi uniforme (deciles 0,095-0,12).
  - Contra las líneas reales (consenso de casas de EE. UU., 2025-26), **el modelo solo no supera al mercado**:
    log loss 0,6966 frente a 0,6918 en apertura y 0,7060 frente a 0,6921 en cierre. Cuando discrepa mucho de la
    línea suele equivocarse él.
  - Mezclado con el mercado (pesos ajustados solo con meses anteriores) mejora un poco el log loss de la apertura
    (−0,0027, IC 95 % [−0,0057, +0,0001]: en el límite de la significación) y nada el del cierre. La fase 4 explica
    de dónde sale esa mejora a la apertura (información que llega tarde).
  - Valores recalculados tras descartar las cuotas sin margen (ver fase 6); la primera versión, con ellas, daba
    −0,0030 (IC [−0,0053, −0,0008]).
  - El modelo cuantílico directo es marginalmente mejor en P(over) (−0,002 de log loss) y el promedio de ambos no
    mejora al cuantílico: se mantiene la simulación como fuente única porque garantiza la coherencia entre líneas,
    mercados y jugadores.
- **Calidad de datos**: los "cierres" de SportsGameOdds de oct-2025 a mediados de enero de 2026 tienen ~10 % de líneas
  tomadas con el partido empezado. Solo se usa un cierre si hay apertura y no se aleja más de 3 puntos.

### Fase 4: backtest con cuotas reales (`nbaev/backtest/apuestas.py`, `nbaev/betting/`)

```bash
python -m nbaev backtest puntos     # -> reportes/fase4_backtest_puntos.md y estado del mercado en el catálogo
```

- Motor genérico para mercados de dos lados: elige el lado con más EV si edge ≥ umbral; máx. 1 apuesta por
  jugador y 3 por partido; liquida con el resultado real; ROI, drawdown, CLV (por precio y **ajustado por línea**:
  la probabilidad justa del cierre trasladada a la línea apostada), % de veces que se bate el cierre, bootstrap por
  partido y p-valores de Holm por probar varias estrategias. Banca simulada con 1/4 Kelly, tope 2 % por apuesta y
  10 % por día. Quitar margen: multiplicativo, power y Shin (`nbaev/betting/margen.py`).
- **Resultado del mercado de puntos (feb-jun 2026): DESACTIVADO.** Informe completo en
  `docs/resultados/fase4_backtest_puntos.md` (recalculado sin las cuotas de relleno; primera versión entre paréntesis).
  - A la cuota de apertura parecía haber ventaja: 1.529 apuestas, ROI +6,2 % (IC 95 % [+1,6 %, +10,8 %]), CLV
    ajustado +1,8 %, bate el cierre el 75 % de las veces (antes: 1.694 apuestas, ROI +8,9 %).
  - Pero el diagnóstico muestra de dónde sale: ROI +20,7 % cuando la línea se movió después hacia la apuesta,
    −3,9 % (el margen) cuando no se movió; +11,9 % con bajas de compañeros, +1,2 % sin ellas. El modelo usa
    información que solo se conoce cerca del salto (quién se viste, spread y total de cierre) y que la apertura no
    tenía. No es una ventaja alcanzable: quien tiene esa información ve ya cuotas cercanas al cierre.
  - Prueba realista, apostando a la cuota de cierre: ROI **−7,2 %** (IC 95 % [−16,0 %, +1,6 %]; antes −13,4 %). El
    modelo no supera al mercado cuando ambos saben lo mismo.
- Regla de validación (aplicada a cada mercado): ≥ 300 apuestas, CLV ajustado > 0, batir el cierre > 50 % y ROI con
  IC 95 % > 0 apostando cuando se conoce la información que usa el modelo. Se guarda en `market_validation` y en el
  estado del `market_catalog`.
- Qué haría falta para medir la ventaja real a la apertura: partes de lesiones y cuotas con hora, para ejecutar el
  modelo con lo que se sabía en cada momento. Las capturas diarias (`datos diario` + `datos cuotas`) ya los guardan;
  con 2-3 meses de capturas se podrá repetir este backtest "en el momento".

### Fase 5: comparación con cuotas, picks y banca (`nbaev/diario.py`, `nbaev/betting/`)

```bash
python -m nbaev diario                       # datos + lesiones + cuotas + proyección + picks -> reportes/diario/AAAA-MM-DD.{md,csv,json}
python -m nbaev diario --sin-actualizar      # solo proyecta y compara con lo ya descargado
python -m nbaev apuestas ver                 # registro de apuestas, rendimiento y banca
python -m nbaev apuestas confirmar 12 --cuota 1.87 --monto 20   # la hice (con mi cuota y monto reales)
python -m nbaev apuestas descartar 13
streamlit run nbaev/app/dashboard.py         # dashboard con filtros por mercado, partido y jugador
```

Para cada línea capturada (cada casa y cada línea alternativa) el flujo diario:

1. Simula el partido (10.000 veces) y calcula P(over), P(under) y P(empate) del jugador.
2. Quita el margen de la casa (multiplicativo, power o Shin; si la casa solo da un lado, se usa el consenso).
3. Probabilidad final = **mezcla modelo + mercado** (regresión logística ajustada con las líneas reales fuera de muestra
   de la validación; con el cierre, el modelo pesa poco, que es lo honesto según la fase 4).
4. EV = p_gana × cuota + p_empate − 1; edge = p_final − p_justa. Ordena por EV, no por probabilidad.
5. Filtros: EV > 0; edge ≥ 4 % (más en mercados exóticos: primera canasta 10 %, triple-doble 8 %, 1.er cuarto 7 %...);
   ≥ 15 minutos proyectados; fuera Questionable/Doubtful/Day-To-Day; **Benjamini-Hochberg** sobre todas las líneas del
   día (10 % de falsos descubrimientos) para que no pasen EV+ por azar; máximo 1 apuesta por jugador y 3 por partido.
6. Monto con 1/4 Kelly, tope 2 % por apuesta y 10 % por día, **solo en mercados validados**; en mercados sin validar o
   desactivados el pick aparece con monto 0.
7. Exporta la tabla (jugador, partido, mercado, línea, proyección, P(over), P(under), cuota y casa, prob. justa,
   prob. final, edge, EV, monto, estado del mercado y las 3 razones SHAP en puntos), registra **cada línea evaluada con
   la hora** (`predicciones`: permite medir el CLV real a futuro) y las apuestas sugeridas (`apuestas`), y liquida las
   pendientes con el resultado real y la cuota de cierre (CLV).

bet365: si se cargan sus cuotas por CSV (`datos importar-csv`), es la casa preferida aunque otra pague más.
Las demás casas vienen de SportsGameOdds.

### Fase 6: todos los mercados (`nbaev/models/estadisticas.py`, `proyeccion.py`, `primer_anotador.py`, `betting/combinadas.py`)

```bash
python -m nbaev mercados validar          # walk-forward de todos los mercados (temporada 2025-26)
python -m nbaev backtest mercados         # backtest por mercado, estados y docs/resultados/fase6_mercados.md
python -m nbaev combinada --sel "Jayson Tatum|pts|24.5|over|1.87|0.5" --sel "Jayson Tatum|pra|38.5|over|1.87|0.5"
python -m nbaev comparar duelo "Jayson Tatum" "Paul George" --mercado pts
python -m nbaev comparar maximo "Jayson Tatum" [--equipo]
```

- **Una sola simulación por partido** para todo: minutos -> tiros (puntos, triples, tiros de campo, libres) y rebotes
  ofensivos/defensivos, asistencias, robos, tapones y pérdidas (cada uno con su LightGBM de tasa, su defensa rival por
  posición y su binomial negativa con varianza estimada). Combinados (PR, PA, RA, PRA, robos+tapones), doble-doble y
  triple-doble salen de esas simulaciones; las líneas alternativas son simplemente otras líneas sobre la misma
  distribución (coherencia garantizada). Periodos: reparto beta-binomial con la fracción de cada jugador en el 1.er
  cuarto y la 1.ª mitad (1.er cuarto ≤ 1.ª mitad ≤ partido). Primer anotador: salto inicial (Bradley-Terry con el
  historial de cada saltador), probabilidad de anotar primero tras ganar el salto (63 %) y reparto entre titulares.
  Duelos y máximo anotador: comparaciones dentro de cada simulación (empates repartidos).
- **Combinadas**: probabilidad conjunta contando simulaciones (las selecciones del mismo partido están correlacionadas)
  y margen acumulado frente a las simples. Ojo: las casas ponen precio propio a las combinadas del mismo partido
  (no multiplican cuotas) precisamente por esa correlación.
- **Calibración** (PIT, temporada 2025-26, ~29.500 actuaciones): todas las estadísticas con desviación máxima por decil
  ≤ 0,02; 1.er cuarto y 1.ª mitad ≤ 0,024. Máximo anotador: log loss 0,121 frente a 0,187 del uniforme, bien calibrado.
  Primera canasta (2.680 partidos): log loss 2,291 frente a 2,381 (volumen de tiro) y 2,398 (uniforme).
- **Datos**: una parte de las cuotas de consenso de SportsGameOdds son valores de relleno (2,00 / 2,00, sin margen):
  casi todas las de pérdidas, todas las de 1.ª mitad capturadas hoy y un 15-25 % del resto. Se descartan siempre
  (margen < 1 %), también en el flujo diario. Los mercados "sí/no" por estadística (p. ej. "anota un triple") no traen
  el umbral en la fuente y no se modelan.
- **Resultado del backtest por mercado** (feb-jun 2026; informe en `docs/resultados/fase6_mercados.md`): **ningún
  mercado queda validado.** Todos parecen rentables a la apertura por la misma razón que puntos (información tardía);
  apostando al cierre ninguno tiene ROI con IC 95 % > 0 **y** CLV positivo. Candidatos a seguir en tiempo real:
  **robos** (ROI al cierre +7,6 %, IC [+2,2 %, +13,1 %]; aporta ~5 puntos sobre "todo al under") y **robos + tapones**
  (+5,8 %, IC [+0,4 %, +11,0 %]), pero con CLV ajustado negativo a la apertura, así que no cumplen la regla.
  Pérdidas: sin cuotas reales suficientes. Triple-doble, 1.er cuarto, 1.ª mitad, primera canasta, duelos y máximo
  anotador: sin cuotas históricas → "sin validar" hasta acumular capturas.

### Limitaciones (léelas antes de apostar)

- **No hay evidencia de ventaja explotable** en ningún mercado con los datos disponibles. El sistema no sugiere montos
  mientras ningún mercado esté validado. Apostar con él hoy es apostar contra el margen de la casa.
- La aparente ventaja a la apertura es un artefacto: el modelo usa información que se conoce cerca del salto. Para
  medir la ventaja real hacen falta partes de lesiones y cuotas con hora; el flujo diario ya los guarda
  (`predicciones`, `injuries`, `prop_odds`). Con 2-3 meses de capturas (dos al día) se puede repetir el backtest con
  la información de cada momento.
- Solo hay una temporada parcial de cuotas reales (feb-jun 2026) y de consenso de casas de EE. UU.; **no hay cuotas
  de bet365** (se cargan a mano por CSV). Las cuotas de una casa concreta y sus límites pueden ser peores.
- stats.nba.com (tracking) no responde desde la nube; ESPN no da partes de lesiones históricos; los minutos a
  principio de temporada y los cambios de rol son la mayor fuente de error.
- Las probabilidades de jugar según el parte (Questionable, Day-To-Day...) son heurísticas sin calibrar.

### Instalación

```bash
python3 -m venv .venv && source .venv/bin/activate   # Python 3.11 o superior
pip install -r requirements.txt
```

Configuración en `config/config.yaml`. Para cambios propios crea `config/local.yaml` (no se versiona) con solo
las claves que quieras sobrescribir. Para SportsGameOdds exporta `SPORTSGAMEODDS_KEY` (gratis en
sportsgameodds.com; en el entorno de Claude Code el proxy ya la inyecta).

### Paso a paso (fase 1: datos)

```bash
# 1. Histórico desde 2021-22 (una vez; ~7.000 partidos, 1-2 horas). Se puede cortar y reanudar.
python -m nbaev datos historial

# 2. Cuotas históricas reales (apertura y cierre de consenso) para el backtest. Cada partido gasta
#    una "entidad" del plan de SportsGameOdds (2.500/mes en el plan amateur); se respeta una reserva.
python -m nbaev datos cuotas-historicas --desde 2025-10-21 --hasta 2026-06-30

# 3. Cada día (antes de los partidos): partidos de ayer, lesiones, cierres de ayer, cuotas de hoy.
python -m nbaev datos diario

# 4. Cuotas de bet365 cargadas a mano (ver plantillas/cuotas_manual.csv).
python -m nbaev datos importar-csv mis_cuotas_bet365.csv

# 5. Cobertura y calidad de la base.
python -m nbaev datos estado
```

Programarlo cada día (Linux/macOS, `crontab -e`), por ejemplo a las 11:00 y a las 17:30 para tener dos capturas
de cuotas (la diferencia entre ambas y el cierre es lo que mide el CLV):

```
0 11 * * *  cd /ruta/al/repo && .venv/bin/python -m nbaev datos diario >> logs/cron.log 2>&1
30 17 * * * cd /ruta/al/repo && .venv/bin/python -m nbaev datos cuotas >> logs/cron.log 2>&1
```

### Fuentes de datos

| Fuente | Qué aporta | Notas |
|---|---|---|
| ESPN (API pública) | Calendario, box score, jugada a jugada con coordenadas, líneas de cierre (spread/total), parte de lesiones | Fuente principal: responde desde cualquier red |
| stats.nba.com (`nba_api`) | Métricas avanzadas y tracking: potential assists, rebound chances, touches | **Bloquea servidores en la nube**. Funciona desde casa: `python -m nbaev datos nba-api --temporada 2025` |
| SportsGameOdds | Props de ~8 casas de EE. UU. (FanDuel, DraftKings, Caesars, BetMGM...), apertura y cierre de consenso, resultados | No incluye bet365. Plan amateur: 10 peticiones/min, 2.500 partidos/mes |
| CSV manual | Cuotas de bet365 (o cualquier casa) | Plantilla en `plantillas/cuotas_manual.csv` |

`nba_api` es la librería pedida para los box scores, pero stats.nba.com no responde desde servidores en la nube
(probado: la conexión se queda colgada; cdn.nba.com devuelve 403). Por eso los box scores y el jugada a jugada
salen de ESPN, que trae lo mismo (y además coordenadas de tiro y líneas de cierre), y `nba_api` queda para lo
que solo tiene la NBA (tracking). En modo `auto` se prueba una vez y, si no responde, se sigue sin esos datos.

### Base de datos (`data/nbaev.duckdb`)

| Tabla | Contenido |
|---|---|
| `games`, `teams` | Partidos (regular, play-in y playoffs) y equipos. `season` = año de inicio (2021 = 2021-22) |
| `player_games` | Box score por jugador y partido |
| `player_absences` | Convocados que no jugaron y motivo (lesión / decisión técnica): parte de bajas histórico |
| `team_games` | Totales de equipo y puntos por cuarto |
| `plays` | Jugada a jugada normalizado |
| `player_periods` | Producción y segundos en pista de cada jugador por cuarto (props de 1.er cuarto y 1.ª mitad) |
| `stints` | Tramos con el mismo quinteto en pista |
| `shots` | Tiros de campo con zona (aro, pintura, media, triple de esquina, triple frontal) |
| `game_starts` | Salto inicial (quién saltó y quién ganó), titulares, primera canasta y primeros puntos del partido y de cada equipo |
| `game_lines` | Spread, total y moneyline (cierre de ESPN; apertura, cierre y capturas de SportsGameOdds) |
| `team_context` | Local/visitante, días de descanso, back-to-back, partidos en 4 y 7 días, km de viaje, cambio de huso, total implícito de cada equipo |
| `injuries`, `lineups` | Parte de lesiones y titulares con la hora de cada captura |
| `prop_odds` | Cuotas de props: fuente, tipo (apertura/cierre/captura), hora, casa, jugador, mercado, periodo, línea, lado, cuota y resultado |
| `market_catalog` | Cada mercado visto en las fuentes. Los nuevos entran como **sin validar** |
| `player_map`, `event_map` | Correspondencia de ids de otras fuentes con los de ESPN |
| `nba_stats` | Métricas de stats.nba.com acumuladas hasta `date_to` |
| `pbp_quality` | Control de cada partido: cuánto cuadra el jugada a jugada con el box score |
| Vistas `v_team_adv`, `v_player_adv` | Posesiones, pace, rating ofensivo/defensivo, usage y true shooting |

Las respuestas originales de ESPN se guardan comprimidas en `data/crudos/`: si se mejora un parser,
`python -m nbaev datos reprocesar` reconstruye las tablas sin volver a descargar.

### Cero fuga de información (`nbaev/data/asof.py`)

Toda feature y toda evaluación deben leer los datos a través de `asof`, que aplica estas reglas:

- Las estadísticas de un partido solo existen desde su inicio + 3,5 h.
- Lesiones, alineaciones y cuotas solo desde la hora de su captura (`snapshot_at`).
- Las cuotas de **cierre** y el **resultado** de las props nunca son entrada del modelo: solo sirven para medir CLV y aciertos.
- stats.nba.com: solo fotos acumuladas hasta el día anterior al partido.

Limitaciones conocidas: para partidos pasados no existe el parte de lesiones de esa hora, así que las bajas se
toman de quién no jugó según el box score (incluye bajas de última hora que quizá no se sabían al apostar). Y las
líneas de spread/total históricas son de cierre (en directo se usará la captura disponible a la hora de la predicción).

### Pruebas

```bash
python -m pytest tests/nbaev -q
```

---

# Sistema anterior (`apuestas/`): fútbol, NBA y NFL

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

### Picks seguros de titulares estables

Para titulares con 30+ minutos esperados (titular en al menos 3 de sus últimos 5), el informe busca la
línea de "más de" más alta que pasa con al menos 85 % (`APUESTAS_NBA_PROB_SEGURA`) en puntos, rebotes,
asistencias y PRA: un "15+ puntos" casi seguro de una estrella en lugar de la línea normal de un suplente.
Se muestra con su **cuota mínima** (1 / probabilidad) para buscarla en las líneas alternativas de la casa.
Backtest (22 oct-25 nov 2025 y 20 feb-10 mar 2026): elegidas al 85 % acertaron el 89-96 %; al 90 %, el
93-99 %. Las props de suplentes llevan la marca "⚠️ suplente": dependen de los minutos que les dé el técnico.

### Combinada segura del día

Elige por **probabilidad**, no por valor:

- **Opción A, líneas alternativas:** el pick seguro más probable de cada partido (ver arriba), con la
  probabilidad de acertar 2, 3 y 4 juntos (con 4 picks al ~90 %, ~65 %).
- **Opción B, líneas principales con cuota real:** la más probable de cada partido entre jugadores
  constantes: titulares con minutos estables, sin cambio de rol, traspaso ni lesión, que la habrían pasado
  en 7+ de sus últimos 10 y en el 60 %+ de esta temporada, con cuota de al menos 1.30
  (`APUESTAS_NBA_CUOTA_MIN`). Si la casa no ofrece una línea, se usa la siguiente de la lista.

### Combinadas con cuota objetivo y calibración

Cada día se arman y registran (tabla `nba_combinadas`) la combinada de alternas, la de principales y las
de cuota objetivo 2, 3, 5, 10 y 15: la combinación de jugadores constantes, en partidos distintos, con más
probabilidad de acertar todas cuya cuota llega al objetivo, con su valor (probabilidad × cuota − 1): una
cuota alta nunca es segura (cuota 15 justa = 1 de cada 15) y si el valor es negativo no conviene ese día.
Las piernas con alertas no entran: suplente (riesgo de minutos), minutos inestables, cambio de rol,
traspaso, lesión y "muy lejos de la casa" (el modelo la ve más de 25 puntos más probable que la casa: la
casa suele saber algo que el modelo no) y "menos de una estrella al inicio de temporada": en el arranque
de 2025-26, los "menos de" en puntos de anotadores de 20+ prometían 67 % y acertaron 60 % (las estrellas
arrancan fuertes); su probabilidad se acerca a 50 % hasta los 15 partidos. Son picks de prueba: se liquidan solos con
los resultados reales. `nba rendimiento` y el inicio del informe muestran si el sistema está listo para
dinero real: 21+ días con picks liquidados, 150+ props y 150+ picks seguros que aciertan al menos lo
prometido (−2 puntos), beneficio positivo en las props con cuota y 30+ combinadas que ganan lo prometido.

### Seguimiento de las combinadas de prueba

El informe empieza con cómo terminaron las combinadas del día anterior, pierna por pierna (✅/❌, con el
valor real), y el acumulado por tipo (jugadas, ganadas, % frente a la probabilidad prometida y beneficio).
Una pierna perdida decide la combinada aunque falten partidos por terminar. Para lanzar el informe de una
fecha concreta: *Actions → NBA diario → Run workflow* con la fecha.

Las apuestas que armas tú en la casa (de prueba o reales) van en `apuestas_usuario/AAAA-MM-DD.json` (formato
en `apuestas/nba/usuario.py`): el flujo diario las registra como "Tu apuesta: ...", las liquida con las demás y
salen en el seguimiento y en el acumulado como "Tus apuestas" (no cuentan para los criterios de calibración
del sistema).

### Bet builders y dobles (`apuestas/nba/builder.py`)

Por partido, 4 "más de" de titulares estables sin alertas, en líneas un poco por debajo de su nivel
(cada pierna ~72 %+, prioridad a puntos y asistencias), y la doble de los dos bet builders más probables.
La probabilidad de acertar todas usa la correlación entre jugadores del mismo partido (desvíos frente a su
media, 2025-26: puntos +0.08 entre compañeros y +0.04 entre rivales; asistencias, rebotes y triples casi
nada), con una simulación de cópula normal. Se da la cuota justa para compararla con la del bet builder de
la casa. Backtest (22 oct-25 nov 2025 y 1 feb-10 mar 2026, 461 bet builders): prometían ~32 % y acertaron
38-40 %; las piernas, 75 % y 78-79 %. Se registran como prueba (tipos `builder` y `doble_builder`). Cuando la casa tiene línea principal de esa
estadística, solo se usan líneas que suele ofrecer como alternativa: la principal menos ~10 % (al menos 1),
como las mínimas de Betano el 27 oct (Cade 8.5 asistencias → 8+, Brunson 25.5 puntos → 24+).

### Razonamiento de cada pick, altura y ventajas del partido

- Cada prop lleva su razonamiento factor por factor, marcado a favor (✅), en contra (❌) o neutro (➖):
  minutos y titularidad, forma (últimos 5, esta temporada y la anterior frente a la línea), cómo produce
  la estadística (tiros por zona, % de rebotes, % de canastas asistidas...), defensa rival por posición
  y por zona, altura, ritmo del partido, historial contra el rival, acierto en sus últimos 10 y notas
  (bajas, cambio de rol...). Las combinadas muestran cuántos factores tiene cada pierna a favor y en contra.
- **Altura** (plantillas de ESPN, se actualizan cada día): diferencia de estatura con los rivales de su
  posición. En los residuos del modelo (nov 2025-mar 2026) explica rebotes (+0.67 % por pulgada, t = 2.9),
  tapones, triples y puntos; se usa la mitad de cada efecto y como mucho ±6 %. Fuera de muestra (oct 2025
  y abr 2026) mejora el Brier en ambos periodos (0.21688 → 0.21681 y 0.22456 → 0.22452).
- **Ventajas del partido:** para los dos equipos, puntos y rebotes esperados de sus jugadores frente a su
  media, ajuste por la defensa rival y diferencia de estatura.

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

Corre en los servidores de GitHub cada día hacia las 9:00 de Bogotá (programado a las 8:13: GitHub retrasa los horarios hasta casi una hora): guarda los resultados de ayer, liquida
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
python -m apuestas nfl hoja --equipo BUF               # hoja de picks del partido: los dos lados, listos para elegir
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

### Combinadas del día y su seguimiento (`nfl combinadas`, `nfl seguimiento`)

Las mismas reglas que las combinadas de la NBA (ver `CLAUDE.md`), traducidas a la NFL en `apuestas/nfl/combinadas.py`:
segura A (líneas alternativas al 85 %+), segura B (la principal más probable de cada partido), seguras de cuota
2, 3, 5 y 10 y de valor 5, 10 y 15 (con las menos patas posibles), rachas de temporada y un bet builder por
partido (más la doble). Solo entran jugadores constantes: sin alertas (papel menor, vuelve de lesión, cambio de
rol, traspaso reciente, en el parte de lesiones, muy lejos de la casa), 7+ de sus últimos 10 y 60 %+ de esta
temporada. Con varios partidos, una pata por partido; con uno solo, como mucho dos por equipo, y la probabilidad
conjunta usa las correlaciones medidas en 2024-2026 (yardas del QB ↔ yardas de sus receptores +0.37, ↔ su RB
−0.13; RB rivales −0.17...), que es también por qué el bet builder de la casa paga menos que el producto.

Todas se guardan en `nfl_combinadas` y se liquidan solas con los resultados; las apuestas que hace el usuario
en su casa se escriben en `apuestas_usuario/nfl/AAAA-MM-DD.json` y se siguen igual. `nfl seguimiento --fecha
AAAA-MM-DD` muestra cada pierna con su valor real y el acumulado por tipo, y el informe diario las incluye.

### La hoja de picks de cada partido (`nfl hoja`, y al principio del informe)

Los dos lados de cada partido, ya analizados para elegir: por cada equipo, sus ventajas sobre la defensa rival
(métrica a métrica, el punto débil del rival en la zona roja y si juega un QB suplente), sus candidatos a TD de
cualquier posición (anota y 2+ con probabilidad, mejor cuota, valor y qué apuesta tiene sentido o desde qué cuota),
sus props con valor y las más probables, y sus defensores (tacleadas y sacks). Al final, los picks recomendados del
partido de los dos lados, por valor esperado.

**Conversión de los QB.** Un acarreo de QB en la zona roja termina en TD el 25 % de las veces (sneaks, carreras
diseñadas) y uno de RB el 16 %: repartir los TD por tierra solo por acarreos subestimaba a los QB corredores. Su
cuota de TD por tierra se pondera por su conversión en la zona roja (contraída hacia la de los QB). Backtest de
2025: los QB mejoran (Brier 0.1355 → 0.1338) y el total queda igual; hacerlo con todas las posiciones empeora (en
los RB la conversión individual es ruido), así que solo se aplica a los QB.

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
