#TODO import espn module

from data import espn

# TEST 1
# this test is to see if I am properly getting the data for a single sport
testSport = "basketball"
testLeague = "womens-college-basketball"

games = espn.getScoreboard(testSport, testLeague)
for game in games:
    print(game)