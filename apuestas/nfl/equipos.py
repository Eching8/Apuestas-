"""Los 32 equipos con las abreviaturas de nflverse y las variantes de ESPN y SportsGameOdds."""
from __future__ import annotations

from ..nba.sgo import clave_nombre

# abreviatura nflverse -> (nombre completo, apodo, ciudad)
EQUIPOS = {
    "ARI": ("Arizona Cardinals", "Cardinals", "Arizona"),
    "ATL": ("Atlanta Falcons", "Falcons", "Atlanta"),
    "BAL": ("Baltimore Ravens", "Ravens", "Baltimore"),
    "BUF": ("Buffalo Bills", "Bills", "Buffalo"),
    "CAR": ("Carolina Panthers", "Panthers", "Carolina"),
    "CHI": ("Chicago Bears", "Bears", "Chicago"),
    "CIN": ("Cincinnati Bengals", "Bengals", "Cincinnati"),
    "CLE": ("Cleveland Browns", "Browns", "Cleveland"),
    "DAL": ("Dallas Cowboys", "Cowboys", "Dallas"),
    "DEN": ("Denver Broncos", "Broncos", "Denver"),
    "DET": ("Detroit Lions", "Lions", "Detroit"),
    "GB": ("Green Bay Packers", "Packers", "Green Bay"),
    "HOU": ("Houston Texans", "Texans", "Houston"),
    "IND": ("Indianapolis Colts", "Colts", "Indianapolis"),
    "JAX": ("Jacksonville Jaguars", "Jaguars", "Jacksonville"),
    "KC": ("Kansas City Chiefs", "Chiefs", "Kansas City"),
    "LA": ("Los Angeles Rams", "Rams", ""),
    "LAC": ("Los Angeles Chargers", "Chargers", ""),
    "LV": ("Las Vegas Raiders", "Raiders", "Las Vegas"),
    "MIA": ("Miami Dolphins", "Dolphins", "Miami"),
    "MIN": ("Minnesota Vikings", "Vikings", "Minnesota"),
    "NE": ("New England Patriots", "Patriots", "New England"),
    "NO": ("New Orleans Saints", "Saints", "New Orleans"),
    "NYG": ("New York Giants", "Giants", ""),
    "NYJ": ("New York Jets", "Jets", ""),
    "PHI": ("Philadelphia Eagles", "Eagles", "Philadelphia"),
    "PIT": ("Pittsburgh Steelers", "Steelers", "Pittsburgh"),
    "SEA": ("Seattle Seahawks", "Seahawks", "Seattle"),
    "SF": ("San Francisco 49ers", "49ers", "San Francisco"),
    "TB": ("Tampa Bay Buccaneers", "Buccaneers", "Tampa Bay"),
    "TEN": ("Tennessee Titans", "Titans", "Tennessee"),
    "WAS": ("Washington Commanders", "Commanders", "Washington"),
}
# Abreviaturas de ESPN y antiguas que no coinciden con las de nflverse.
ALIAS = {"LAR": "LA", "WSH": "WAS", "JAC": "JAX", "OAK": "LV", "SD": "LAC", "STL": "LA"}

# Nombres con los que se escribe un equipo en texto libre (apodo, ciudad, en español).
_POR_TEXTO: dict[str, str] = {}
for _abbr, (_nombre, _apodo, _ciudad) in EQUIPOS.items():
    for _t in (_abbr, _nombre, _apodo, _ciudad):
        if _t:
            _POR_TEXTO[clave_nombre(_t)] = _abbr
_POR_TEXTO.update({clave_nombre(k): v for k, v in {
    "Niners": "SF", "Bucs": "TB", "Pats": "NE", "Commies": "WAS", "Jags": "JAX", "Cards": "ARI",
    "Halcones": "ATL", "Cuervos": "BAL", "Osos": "CHI", "Leones": "DET", "Empacadores": "GB", "Potros": "IND",
    "Jefes": "KC", "Carneros": "LA", "Cargadores": "LAC", "Delfines": "MIA", "Vikingos": "MIN", "Patriotas": "NE",
    "Santos": "NO", "Gigantes": "NYG", "Aguilas": "PHI", "Acereros": "PIT", "Halcones Marinos": "SEA",
    "Bucaneros": "TB", "Titanes": "TEN", "Vaqueros": "DAL", "Texanos": "HOU", "Jaguares": "JAX", "Panteras": "CAR",
    "Cafes": "CLE", "Bengalies": "CIN", "Bucaneros De Tampa": "TB", "Comandantes": "WAS", "Cardenales": "ARI",
    "Rams": "LA", "LAR": "LA", "WSH": "WAS",
}.items()})


def normalizar(abbr: str | None) -> str | None:
    if not abbr:
        return None
    a = abbr.upper().strip()
    return ALIAS.get(a, a) if ALIAS.get(a, a) in EQUIPOS else None


def nombre(abbr: str) -> str:
    return EQUIPOS.get(abbr, (abbr,))[0]


def apodo(abbr: str) -> str:
    return EQUIPOS.get(abbr, (abbr, abbr))[1]


def por_texto(texto: str) -> str | None:
    """'chargers', 'Los Angeles Chargers', 'LAC', 'cargadores' -> 'LAC'."""
    return _POR_TEXTO.get(clave_nombre(texto))


def por_nombre_largo(texto: str) -> str | None:
    """'Philadelphia Eagles' o 'PHILADELPHIA_EAGLES_NFL' (SportsGameOdds) -> 'PHI'."""
    k = clave_nombre(texto)
    if k.endswith("_NFL"):
        k = k[:-4]
    return _POR_TEXTO.get(k)
