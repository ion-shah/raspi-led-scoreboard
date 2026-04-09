#this file has abbreviations I like better and has the retro logos to use instead
ABBREVIATION_OVERRIDES = {
    "nba": {
        "NY":  "NYK",
        "GS":  "GSW",
        "SA":  "SAS",
        "NO":  "NOP",
        "WSH": "WAS"
    },
    "nfl": {},
    "mlb": {},
    "nhl": {},
}

LOGO_OVERRIDES = {
    "nba": {
        "UTAH": "2004",
        "TOR": "1995",
        "DET": "1996",
        "BKN": "2003",
        "CLE": "2016",
        "MEM": "2001"

    },
    "nfl": {},
    "mlb": {},
    "nhl": {},
}

def getDisplayAbbr(league, abbr):
    return ABBREVIATION_OVERRIDES.get(league, {}).get(abbr, abbr)