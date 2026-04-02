#TODO import espn module

from data import fetchScoreboard, getScoreboardList, refreshGameList, buildGameDict
from utils import config_loader as loader

import pprint

config = loader.loadConfig("config.yaml")

# TEST 1
# this test is to see if I am properly getting the data for a single sport
testSport = "basketball"
testLeague = "nba"
api = fetchScoreboard(testSport, testLeague)

games = buildGameDict(api, testSport)

for game in games.values():
    print(game)

print("--fetch test done--")

freshGames = refreshGameList(games, fetchScoreboard(testSport, testLeague), testSport, config=config)

for game in freshGames.values():
    print(game)

print("--filtered games test done--")
