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

def getDisplayAbbr(league, abbr):
    return ABBREVIATION_OVERRIDES.get(league, {}).get(abbr, abbr)