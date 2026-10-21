# Apuestas: analizador diario de partidos y combinadas

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
| [football-data.co.uk](https://www.football-data.co.uk) | Historial de muchas temporadas (resultados, remates, tiros a puerta, córners, tarjetas y cuotas previas y de cierre) para el **modelo histórico**, y próximos partidos con cuotas | No necesita clave |

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

# Modelo histórico (no necesita clave de API)
python -m apuestas historico                   # descarga/actualiza el historial
python -m apuestas backtest                    # ¿le gana el modelo a las casas? (desde 2024-07-01)
python -m apuestas predecir --dias 3           # próximos partidos con probabilidades y valor
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

## Modelo histórico (Dixon-Coles)

`modelo_historico.py` aprende de varias temporadas de football-data.co.uk, así que funciona desde
el primer día (no hace falta esperar a que la base de API-Football se llene):

- **Fuerzas por equipo.** Cada equipo tiene ataque y defensa por estadística:
  `goles del local = exp(media + ventaja local + ataque local + defensa visitante)`. Se ajustan por
  máxima verosimilitud de Poisson con **decaimiento temporal** (un partido de hace un año pesa la
  mitad), **regularización** hacia el equipo medio y un ajuste propio para los **recién ascendidos**.
- **Tiros a puerta.** El objetivo de goles mezcla los goles reales con los tiros a puerta convertidos
  a goles con la tasa de la liga (`PESO_TIROS_DEFECTO`): los goles tienen mucho azar, los tiros a
  puerta miden mejor lo que genera y concede cada equipo.
- **Corrección Dixon-Coles** (`rho`) para 0-0, 1-0, 0-1 y 1-1, y una matriz de marcadores de la
  que salen 1X2, doble oportunidad, ambos marcan y totales.
- Córners, tarjetas y tiros: el mismo ajuste con binomial negativa (sobredispersión estimada).

`analizar` usa este modelo en cuanto la liga está cubierta (`APUESTAS_LIGAS_HISTORICO`) y los dos
equipos se emparejan por nombre con los de football-data.co.uk (`puente.py`); si no, recurre al
modelo de forma reciente y, sin historial, solo a las cuotas. Los mercados de jugador siguen
saliendo de la base de API-Football.

### Backtest: la prueba de fuego

`python -m apuestas backtest` recorre las temporadas de prueba semana a semana, re-entrenando el
modelo solo con lo jugado hasta ese lunes, y compara sus probabilidades con las de las casas
(sin margen) antes del partido y al cierre. Además simula apuestas de 1 unidad cuando hay valor y mide el
**CLV** (valor según la cuota de cierre), el indicador más fiable de si un modelo encuentra valor
real: el beneficio de unos cientos de apuestas es casi todo ruido.

Resultado con los valores por defecto (8 ligas europeas, 6.461 partidos de las temporadas
2024/25, 2025/26 y lo jugado de 2026/27; `reportes/backtest-AAAA-MM-DD.md` tiene el detalle por liga):

| Log-loss (más bajo = mejor) | Modelo | Mezcla 20 % modelo | Cuotas previas | Cuotas de cierre |
|---|---|---|---|---|
| 1X2 | 0.9889 | 0.9788 | 0.9778 | 0.9747 |
| Más/menos de 2.5 goles | 0.6743 | 0.6714 | 0.6712 | 0.6682 |

| Apuestas simuladas (cuota media previa) | Apuestas | ROI | CLV |
|---|---|---|---|
| Solo modelo, valor ≥ 5 % | 4.331 | −9.8 % | −7.2 % |
| Mezcla 50 %, valor ≥ 3 % (configuración anterior) | 2.081 | −10.0 % | −7.6 % |
| Mezcla 20 %, valor ≥ 5 % (configuración actual) | 106 | −13.9 % | −6.7 % |

Cómo leerlo, sin adornos:

- El modelo está **bien calibrado** (cuando dice 45 %, ocurre ~46 % de las veces), pero las casas
  predicen mejor: ninguna mezcla mejora a sus cuotas. Así ocurre con casi cualquier modelo hecho
  con datos públicos.
- Por eso el "valor" que encuentra el modelo frente a la cuota media es, en promedio, **falso**: un
  CLV de −7 % equivale a apostar al azar pagando el margen de la casa. Por este backtest
  `APUESTAS_PESO_MODELO` pasó de 0.5 a 0.2 y `APUESTAS_VALOR_MIN` de 0.03 a 0.05: así salen muchas
  menos selecciones "de valor", y es lo correcto.
- Lo que sí aporta: probabilidades razonables y la cuota justa de mercados que no tienen cuota en
  los datos (córners, tarjetas, tiros), predicciones desde el primer día y una forma objetiva de
  medir cualquier mejora futura (xG, alineaciones, lesiones…). Una mejora solo es real si baja el
  log-loss y deja el CLV en positivo en este backtest.
- Las ligas extra (MEX…) no traen cuotas previas, solo de cierre, así que no entran en esta comparación.

Ligas disponibles (`--ligas`): E0 Premier, E1 Championship, SP1 LaLiga, SP2 Segunda, I1 Serie A,
I2 Serie B, D1 Bundesliga, D2 2. Bundesliga, F1 Ligue 1, F2 Ligue 2, N1 Eredivisie, P1 Portugal,
B1 Bélgica, T1 Turquía, SC0 Escocia, G1 Grecia; y solo con resultados y cuotas de cierre: MEX Liga
MX, ARG Argentina, BRA Brasil, USA MLS, JPN Japón, SWE, NOR, DNK, AUT, SWZ, POL, CHN.

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
  temporada, así que la base se llena día a día con `actualizar`. Para las ligas cubiertas por
  football-data.co.uk eso ya no importa: el modelo histórico funciona desde el primer día. En el
  resto (Champions, Europa League...) el modelo propio se activa cuando cada equipo tiene al menos 4
  partidos guardados y, mientras tanto, el análisis usa solo las probabilidades implícitas de las
  casas (sin margen), que no sirven para encontrar valor.
- Revisa en tu panel de API-Football que tu plan incluye la temporada actual y las cuotas.
- Las casas no siempre publican cuotas de córners, tarjetas o tiros en la API; sin cuota no
  hay forma de medir el valor, solo la cuota justa.
- El modelo no conoce lesiones, rotaciones ni alineaciones. Revísalas antes de apostar.

## Pruebas

```bash
python -m unittest -v
```

Las pruebas usan una API simulada con datos sintéticos (`tests/fake_api.py`), solo para
comprobar el código; nunca se usan en los informes.
