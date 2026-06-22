# this file contains functions that parse the JSON data from the API and return Game objects

from data.models.base_models import Game
from data.models.basketball_model import BasketballGame
from data.models.soccer_model import SoccerGame
from utils.time_utils import parseDate

LEAGUE_SPORT_MAP = {
    "basketball" : ["nba", "mens-college-basketball"],
    "soccer": ["fifa.world"]
    # add more sports as functionality expands
}
                
def buildGame(event, sport, league):
    # returns a Game object from a provided JSON
    # expects data from ["events"]

    comp = event["competitions"][0]
    status = comp["status"]["type"]["state"]
    
    base_args = dict(
        gameID    = event["id"],
        sport     = sport,
        league    = league,
        team1abbr     = comp["competitors"][0]["team"]["abbreviation"],
        team2abbr     = comp["competitors"][1]["team"]["abbreviation"],
        team1name = comp["competitors"][0]["team"]["name"],
        team2name = comp["competitors"][1]["team"]["name"],
        t1score   = comp["competitors"][0]["score"],
        t2score   = comp["competitors"][1]["score"],
        status    = status,
        startTime = parseDate(event["date"]),
        #TODO add checking for playoffs 
    )

    if league in LEAGUE_SPORT_MAP.get("basketball", []):
        return _buildBasketballGame(comp, base_args)
    
    if league in LEAGUE_SPORT_MAP.get("soccer", []):
        return _buildSoccerGame(comp, base_args)
    

    return Game(**base_args) #return generic Game if no sport-specific class exists


#=====CHILD CLASS BUILDERS=====
def _buildBasketballGame(comp, base_args):
    status_block = comp["status"]
    period   = status_block.get("period", 0)
    clock    = status_block.get("displayClock", "")
    timeDesc = status_block.get("type", {}).get("description", "")

    return BasketballGame(
        **base_args,
        period    = period,
        clock     = clock,
        timeDesc = timeDesc
    )

def _buildSoccerGame(comp, base_args):
    status_block = comp["status"]
    period   = status_block.get("period", 0)
    clock    = status_block.get("displayClock", "")
    timeDesc = status_block.get("type", {}).get("description", "")

    return SoccerGame(
        **base_args,
        period    = period,
        clock     = clock,
        timeDesc = timeDesc
    )

# ==============================
    
def buildGameDict(data, sport):
    # for a provided JSON this function will return a dictionary of type Game
    # expects data from the scoreboard endpoint

    gameDict = {}
    league = data["leagues"][0]["slug"]
    for event in data["events"]:
        currGame = buildGame(event, sport, league)
        #TODO add checking for playoffs 

        gameDict[currGame.gameID] = currGame
    return gameDict