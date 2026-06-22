# Soccer is to diffrentiate from American football

from data.models.base_models import Game
from utils.time_utils import parseDate

class SoccerGame(Game):
    def __init__(self, gameID, sport, league, 
                 team1name, team2name, team1abbr, team2abbr,
                 t1score, t2score, status, startTime,
                 period=0, clock="", timeDesc="", playoffs=False):
        
        super().__init__(gameID, sport, league, team1name, team2name, team1abbr, team2abbr,
                         t1score, t2score, status, startTime, playoffs)
        
        self.period = period        # int, 
        self.clock = clock          # string, displayClock field from ESPN API
        self.timeDesc = timeDesc   # string, time description like "1st Quarter", "Halftime", etc.

    def displayClock(self, timezone_str="UTC"):
        # Returns a display string for the game clock.
        # timezone_str is only needed for pre-game start time formatting.
        
        if self.status == "pre":
            if timezone_str and self.startTime:
                import pytz
                local_tz = pytz.timezone(timezone_str)
                local_time = self.startTime.astimezone(local_tz)
                return local_time.strftime("%I:%M %p").lstrip("0")
            return "PRE"

        elif self.status == "post":
            return "FT"
            #TODO need to add penalty handling

        elif self.status == "in":
            return self._liveClockString()

        return ""

    def _liveClockString(self):
        # Handles all the edge cases for in-progress games.
        # Uses self.description (from ESPN status.type.description) as the
        # most reliable signal for between-quarter and halftime states.

        # clock is empty or zero with no useful description
        clock_is_empty = not self.clock or self.clock in ("0:00", "00:00", "0.0", "")
        """
        if clock_is_empty:
            if self.period == 1:
                return "HT"
            elif self.period > 0:
                return "FT"
            return "LIVE"
        """

        if self.status == "post":
            return "FT"

        # normal in-progress state — just show the clock
        return self.clock
    
    def updateFrom(self, event):
        super().updateFrom(event)

        comp = event["competitions"][0]
        status_block   = comp["status"]
        self.period    = status_block.get("period", self.period)
        self.clock     = status_block.get("displayClock", self.clock)
        self.timeDesc  = status_block.get("type", {}).get("description", self.timeDesc)
        self.status    = status_block.get("type", {}).get("state", self.status)

    def __str__(self):
        return f"{self.team1.name} {self.team1.score} ||    || {self.team2.name} {self.team2.score}  || {self.displayClock()} || {self.status} | {self.startTime} || importance: {self.importance}"