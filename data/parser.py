# this file contains functions that parse the JSON data from the API and return Game objects

from datetime import datetime, timezone
from data.models import Game

def parseDate(dateStr):
    # this function takes in a date string from the API and returns a datetime object

    return datetime.strptime(dateStr, "%Y-%m-%dT%H:%MZ").replace(tzinfo=timezone.utc)
    
def buildGame(event, sport, league):
    # returns a Game object from a provided JSON
    # expects data from ["events"]

    gameID = event["id"]
    team1 = event["competitions"][0]["competitors"][0]["team"]["abbreviation"]
    team2 = event["competitions"][0]["competitors"][1]["team"]["abbreviation"]
    t1score = event["competitions"][0]["competitors"][0]["score"]
    t2score = event["competitions"][0]["competitors"][1]["score"]
    status = event["competitions"][0]["status"]["type"]["state"] # pre, in, or post
    startTime = parseDate(event["date"])

    #TODO add checking for playoffs 

    return Game(gameID, sport, league, team1, team2, t1score, t2score, status, startTime)
    
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