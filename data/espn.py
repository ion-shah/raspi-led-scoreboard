# this file works to get the data from the ESPN API
# the API is unofficial, but info regarding the API is sourced from https://github.com/pseudo-r/Public-ESPN-API/

import requests
import json
BASE_URL = "https://site.api.espn.com/apis/site/v2/sports/"

# https://site.api.espn.com/apis/site/v2/sports/{sport}/{league}/{resource}
# this function returns the endpoint of the scoreboard in a provided league and sport
# for example, apiSite("basketball", "nba") provides the endpoint for live nba scores

def apiEndpoint(sport, league, resource="scoreboard", gameID = None):
    if resource == "summary": 
        # set the resource parameter to summary to get a summary of a given game instead
        return f"{BASE_URL}/{sport}/{league}/{resource}?event={gameID}"
        
    else:
        return f"{BASE_URL}/{sport}/{league}/{resource}"

def getJSON(endpoint):
    response = requests.get(endpoint)
    if response.status_code == 404:
        return "404 error, invalid endpoint"
    elif response.status_code == 200:
        return response.json()
    else:
        return None
    
# for a provided JSON this function will return a list of type Game
# expects data from the scoreboard endpoint
def getGameList(data, sport):
    gameList = []
    league = data["leagues"][0]["slug"]
    for event in data["events"]:
        gameID = event["id"]
        team1 = event["competitions"][0]["competitors"][0]["team"]["abbreviation"]
        team2 = event["competitions"][0]["competitors"][1]["team"]["abbreviation"]
        t1score = event["competitions"][0]["competitors"][0]["score"]
        t2score = event["competitions"][0]["competitors"][1]["score"]

        #TODO add checking for playoffs
        #TODO add 

        gameList.append(Game(gameID, sport, league, team1, team2, t1score, t2score))
    return gameList

#This function ties everything together and returns list of games for a given sport
def getScoreboard(sport, league):
    endpoint = apiEndpoint(sport, league)
    data = getJSON(endpoint)

    return getGameList(data, sport)

# each sports game will be put into this class for organization
# specific sports will inherit from the class, with info as needed
class Game(object):
    def __init__(self, gameID, sport, league, team1, team2, t1score, t2score, playoffs = False):
        self.gameID = gameID
        self.sport = sport
        self.league = league
        self.team1 = team1
        self.team2 = team2
        self.t1score = t1score
        self.t2score = t2score
        self.playoffs = playoffs
        self.importance = 0

    def __str__(self):
        return f"{self.team1} {self.t1score} ||    || {self.t2score} {self.team2}"

    
    #TODO add child classes for baseball, football, hockey, and basketball, and NCAA
    #TODO add soccer functionality
    #TODO add type hinting
