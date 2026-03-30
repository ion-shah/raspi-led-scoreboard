# this file works to get the data from the ESPN API
# the API is unofficial, but info regarding the API is sourced from https://github.com/pseudo-r/Public-ESPN-API/

import requests
from datetime import datetime, timezone, timedelta
import json
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
    
def getGameDict(data, sport):
    # for a provided JSON this function will return a dictionary of type Game
    # expects data from the scoreboard endpoint

    gameDict = {}
    league = data["leagues"][0]["slug"]
    for event in data["events"]:
        currGame = buildGame(event, sport, league)
        #TODO add checking for playoffs 

        gameDict[currGame.gameID] = currGame
    return gameDict

def getScoreboardList(sport, league):
    #This function ties everything together and returns a list of games for a given sport

    endpoint = apiEndpoint(sport, league)
    data = getJSON(endpoint)

    return getGameDict(data, sport)


def refreshGameList(oldGames, freshData, sport, lookahead_minutes=20, lookback_minutes=20):
    # this function takes in a list of games and new data, and updates the list of games with the new data
    # this is used to update the scores and status of games that are already in the list, and add new games that have started since the last refresh

    league = freshData["leagues"][0]["slug"]
    freshIDs = set() # keeps track of unique gameIDs

    for newEvent in freshData["events"]:
        gameID = newEvent["id"]
        freshIDs.add(gameID)

        newStatus = newEvent["competitions"][0]["status"]["type"]["state"]
        newT1score = newEvent["competitions"][0]["competitors"][0]["score"]
        newT2score = newEvent["competitions"][0]["competitors"][1]["score"]

        if gameID in oldGames:
            oldGames[gameID].team1.deltaScore = str( int(newT1score or 0) - int(oldGames[gameID].team1.score or 0) )
            oldGames[gameID].team2.deltaScore = str( int(newT2score or 0) - int(oldGames[gameID].team2.score or 0) )
            oldGames[gameID].team1.score = str(newT1score)
            oldGames[gameID].team2.score = str(newT2score)

            # check if game has ended
            if newStatus == "post" and oldGames[gameID].status != "post":
                oldGames[gameID].markEnded()
            oldGames[gameID].status = newStatus
                  
        else:
            #creates new game object
            oldGames[gameID] = buildGame(newEvent, sport, league)
        
    # this second pass removes any games that are irrelevant
    for gameID in list(oldGames.keys()):
        if gameID not in freshIDs or not oldGames[gameID].isRelevant(lookahead_minutes, lookback_minutes):
            del oldGames[gameID]

    return oldGames    

# this class will have some data for the team and its score for the game, and will be used in the Game class
class Team(object):
    def __init__(self, abbreviation, score, deltaScore = 0, ranked = 0):
        self.name = abbreviation
        self.score = score
        self.deltaScore = deltaScore # this change is measured for animations
        self.ranked = ranked         # for college sports

# each sports game will be put into this class for organization
# specific sports will inherit from the class, with info as needed
class Game(object):
    def __init__(self, gameID, sport, league, team1, team2, t1score, t2score, status, startTime, playoffs = False):
        self.gameID = gameID                   # ESPN api assigns a gameID to each event
        self.sport = sport                     #
        self.league = league                   #
        self.team1 = Team(team1, t1score)      #
        self.team2 = Team(team2, t2score)      #
        self.status = status                   # pre, in, post
        self.startTime = startTime             # datetime object
        self.endTime = None                    # datetime object
        self.playoffs = playoffs               # TODO functionality needs to added
        self.importance = 0                    # will be populated to determine which game to display

    def markEnded(self):
        # marks the time when the game ends 
        if self.endTime == None:
            self.endTime = datetime.now(timezone.utc)

    def minutesSinceEnd(self):
        # returns minutes since game ended, or 0 if not ended yet.
        if self.endTime is None:
            return 0
        delta = datetime.now(timezone.utc) - self.endTime
        return delta.total_seconds() / 60

        
    def isRelevant(self, lookahead_minutes=20, lookback_minutes=20):
        # this function checks if we care about the game based on the time
        # helps ignore games that are too far in the future or past, and helps determine which games to show on the scoreboard

        now = datetime.now(timezone.utc) 

        if self.status == "in":
            return True

        elif self.status == "pre":
            if self.startTime is None:
                return False
            minutes_until = (self.startTime - now).total_seconds() / 60
            return 0 <= minutes_until <= lookahead_minutes

        elif self.status == "post":
            return self.minutesSinceEnd() <= lookback_minutes

        return False
    
    def __str__(self):
        return f"{self.team1.name} {self.team1.score} ||    || {self.team2.name} {self.team2.score}  || {self.status} | {self.startTime}"

    
    #TODO add child classes for baseball, football, hockey, and basketball, and NCAA
    #TODO add soccer functionality
    #TODO add type hinting
