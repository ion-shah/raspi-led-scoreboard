# this file contains functions that update the scoreboard that is in memory

from data.espn import fetchScoreboard
from data.parser import buildGame, buildGameDict

def refreshGameList(oldGames, freshData, sport, config):
    league = freshData["leagues"][0]["slug"]
    freshIDs = set() # keeps track of unique gameIDs in the fresh data

    for event in freshData["events"]:
        gameID = event["id"]
        freshIDs.add(gameID)

        if gameID in oldGames:
            oldGames[gameID].updateFrom(event)   # updates data specific to each sport
        else:
            oldGames[gameID] = buildGame(event, sport, league)

        oldGames[gameID].calculateImportance(config) # calculate importance for all games after refresh

    # prune irrelevant games
    lookahead = config["scheduling"]["pregame_lookahead_minutes"]
    lookback  = config["scheduling"]["postgame_lookback_minutes"]
    for gameID in list(oldGames.keys()):
        if gameID not in freshIDs or not oldGames[gameID].isRelevant(lookahead, lookback):
            del oldGames[gameID]

    return oldGames

def getScoreboardList(sport, league, config):
    #this function returns a list of valid Game objects for display

    lookahead = config["scheduling"]["pregame_lookahead_minutes"]
    lookback  = config["scheduling"]["postgame_lookback_minutes"]

    data = fetchScoreboard(sport, league)
    if data is None:
        return []
    games = buildGameDict(data, sport)
    return [g for g in games.values() if g.isRelevant(lookahead, lookback)]

def getDisplayList(game_cache, config):
    # Returns games sorted by importance, pinned games first.

    games = list(game_cache.values())
    pinned   = [g for g in games if g.isPinned(config)]
    unpinned = [g for g in games if not g.isPinned(config)]
    
    pinned.sort(key=lambda g: g.importance, reverse=True)
    unpinned.sort(key=lambda g: g.importance, reverse=True)

    return pinned + unpinned

def fetchAndRefresh(game_cache, sport, league, config):
    # this function fetches the latest data and updates the game cache in place, then returns the updated cache

    freshData = fetchScoreboard(sport, league)
    if freshData is not None:
        return refreshGameList(game_cache, freshData, sport, config)
    else:
        print(f"Failed to fetch data for {sport} {league}, keeping old data")
        return game_cache

def getPollInterval(game_cache, live_interval=10, idle_interval=30):
    # Returns poll interval in seconds based on whether any games are live.

    any_live = any(g.status == "in" for g in game_cache.values())
    return live_interval if any_live else idle_interval