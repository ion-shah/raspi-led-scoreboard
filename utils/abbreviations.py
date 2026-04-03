#this is a pretty useless file, but some of the ESPN API abbreviations aren't my favorite, so I manually change them here.

ABBREVIATION_OVERRIDES = {
    "nba": {
        "NY":  "NYK",
        "GS":  "GSW",
        "SA":  "SAS",
        "NO":  "NOP",
        "UTAH": "UTA",
    },
    "nfl": {},
    "mlb": {},
    "nhl": {},
}

def getDisplayAbbr(league, abbr):
    return ABBREVIATION_OVERRIDES.get(league, {}).get(abbr, abbr)