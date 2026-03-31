# this file works to get the data from the ESPN API
# the API is unofficial, but info regarding the API is sourced from https://github.com/pseudo-r/Public-ESPN-API/

import requests

from data.parser import buildGameDict
BASE_URL = "https://site.api.espn.com/apis/site/v2/sports/"


def apiEndpoint(sport, league, resource="scoreboard", gameID = None):
    # https://site.api.espn.com/apis/site/v2/sports/{sport}/{league}/{resource}
    # this function returns the endpoint of the scoreboard in a provided league and sport
    # for example, apiSite("basketball", "nba") provides the endpoint for live nba scores

    if resource == "summary": 
        # set the resource parameter to summary to get a summary of a given game instead
        return f"{BASE_URL}/{sport}/{league}/{resource}?event={gameID}"
        
    else:
        return f"{BASE_URL}/{sport}/{league}/{resource}"

def getJSON(endpoint):
    response = requests.get(endpoint)
    if response.status_code == 404:
        print("404 ERROR, invalid endpoint")
        return None
    elif response.status_code == 200:
        return response.json()
    else:
        print(f"ERROR Unexpected status code: {response.status_code}")
        return None
    
def fetchScoreboard(sport, league):
    # this function fetches the scoreboard data for a given sport and league, and returns it as a JSON object
    return getJSON(apiEndpoint(sport, league))

def getScoreboardList(sport, league):
    #This function ties everything together and returns a list of games for a given sport

    endpoint = apiEndpoint(sport, league)
    data = getJSON(endpoint)

    return buildGameDict(data, sport)

#TODO add child classes for baseball, football, hockey, and basketball, and NCAA
#TODO add soccer functionality
#TODO add type hinting
