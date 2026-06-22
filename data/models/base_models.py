# this file cotains all the classes for the data

from datetime import datetime, timezone
from data.models.importance import ImportanceMixin

# this class will have some data for the team and its score for the game, and will be used in the Game class
class Team(object):
    def __init__(self, teamName, abbreviation, score, deltaScore = 0, ranked = 0):
        self.name = teamName         # i.e Knicks
        self.abbr = abbreviation     # i.e NY or NYK
        self.score = score
        self.deltaScore = deltaScore # this change is measured for animations
        self.home = False            # TODO functionality needs to be added
        self.ranked = ranked         # for college sports

# each sports game will be put into this class for organization
# specific sports will inherit from the class, with info as needed
class Game(ImportanceMixin, object):
    def __init__(self, gameID, sport, league, team1name, team2name, team1abbr, team2abbr, t1score, t2score, status, startTime, playoffs = False):
        self.gameID = gameID                                  # ESPN api assigns a gameID to each event
        self.sport = sport                                    #
        self.league = league                                  #
        self.team1 = Team(team1name, team1abbr, t1score)      #
        self.team2 = Team(team2name, team2abbr, t2score)      #
        self.status = status                                  # pre, in, post
        self.startTime = startTime                            # datetime object
        self.endTime = None                                   # datetime object
        self.playoffs = playoffs                              # TODO functionality needs to added
        self.importance = 0                                   # will be populated to determine which game to display

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

        #ensures stale games are not shown, 
        if self.startTime and (now - self.startTime).days >= 2:
            return False

        if self.status == "in":
            return True

        elif self.status == "pre":
            if self.startTime is None:
                return False
            minutes_until = (self.startTime - now).total_seconds() / 60
            return minutes_until <= lookahead_minutes

        elif self.status == "post":
            return self.minutesSinceEnd() <= lookback_minutes

        return False
    
    def updateFrom(self, event):
        # Updates base fields from a fresh API event. every child class must extend this

        comp = event["competitions"][0]
        newt1score = comp["competitors"][0]["score"]
        newt2score = comp["competitors"][1]["score"]

        self.team1.deltaScore = str(int(newt1score or 0) - int(self.team1.score or 0))
        self.team2.deltaScore = str(int(newt2score or 0) - int(self.team2.score or 0))
        self.team1.score = newt1score
        self.team2.score = newt2score

        newStatus = comp["status"]["type"]["state"]
        if newStatus == "post" and self.endTime is None:
            self.markEnded()
        self.status = newStatus
    
    def __str__(self):
        # debugging string representation
        return f"{self.team1.name} {self.team1.score} ||    || {self.team2.name} {self.team2.score}  || {self.status} | {self.startTime} || importance: {self.importance} generic Game"
