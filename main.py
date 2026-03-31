#TODO import espn module

from data import fetchScoreboard, getScoreboardList, refreshGameList, buildGameDict

# TEST 1
# this test is to see if I am properly getting the data for a single sport
testSport = "basketball"
testLeague = "nba"
api = fetchScoreboard(testSport, testLeague)

games = buildGameDict(api, testSport)

freshGames = refreshGameList(games, fetchScoreboard(testSport, testLeague), testSport)

for game in freshGames.values():
    print(game)

print("done")