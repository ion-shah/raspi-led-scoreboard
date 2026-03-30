#TODO import espn module

from data import espn

# TEST 1
# this test is to see if I am properly getting the data for a single sport
testSport = "basketball"
testLeague = "nba"
api = espn.getJSON(espn.apiEndpoint(testSport, testLeague))

games = espn.getScoreboardList(testSport, testLeague)

freshGames = espn.refreshGameList(games, espn.getJSON(espn.apiEndpoint(testSport, testLeague)), testSport)

for game in freshGames.values():
    print(game)

print("done")