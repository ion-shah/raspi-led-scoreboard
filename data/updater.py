# this file contains functions that update the scoreboard that is in memory

from data.espn import fetchScoreboard
from data.parser import buildGame, buildGameDict

def refreshGameList(oldGames, freshData, sport, config):
    # this function takes in a list of games and new data, and updates the list of games with the new data
    # this is used to update the scores and status of games that are already in the list, and add new games that have started since the last refresh

    league = freshData["leagues"][0]["slug"]
    freshIDs = set() # keeps track of unique gameIDs

    lookahead_minutes = config.get("scheduling", {}).get("pregame_lookahead_minutes", 20)
    lookback_minutes = config.get("scheduling", {}).get("postgame_lookback_minutes", 20)

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

            oldGames[gameID].calculateImportance(config) # recalculate importance based on new status
                  
        else:
            #creates new game object
            oldGames[gameID] = buildGame(newEvent, sport, league)
            oldGames[gameID].calculateImportance(config) 

    # this second pass removes any games that are irrelevant
    for gameID in list(oldGames.keys()):
        if gameID not in freshIDs or not oldGames[gameID].isRelevant(lookahead_minutes, lookback_minutes):
            del oldGames[gameID]

    return oldGames    

def getScoreboardList(sport, league, lookahead_minutes=20, lookback_minutes=20):
    #this function returns a list of valid Game objects for display

    data = fetchScoreboard(sport, league)
    if data is None:
        return []
    games = buildGameDict(data, sport)
    return [g for g in games.values() if g.isRelevant(lookahead_minutes, lookback_minutes)]