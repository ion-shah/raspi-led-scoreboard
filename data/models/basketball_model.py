# each sport has its own data, so that will be included in this file for each child class of Game
from data.models.base_models import Game
from utils.time_utils import parseDate

class BasketballGame(Game):
    def __init__(self, gameID, sport, league, team1, team2,
                 t1score, t2score, status, startTime,
                 period=0, clock="", timeDesc="", playoffs=False):
        
        super().__init__(gameID, sport, league, team1, team2,
                         t1score, t2score, status, startTime, playoffs)
        
        self.period = period        # int, 1-4 for regulation, 5+ for OT
        self.clock = clock          # string, displayClock field from ESPN API
        self.timeDesc = timeDesc   # string, time description like "1st Quarter", "Halftime", etc.

    def periodLabel(self):
        # Returns a display-friendly period string.
        # 1-4 → Q1-Q4, 5 → OT, 6 → 2OT, 7 → 3OT etc.
        
        if self.period <= 0:
            return ""
        elif self.period <= 4:
            return f"Q{self.period}"
        elif self.period == 5:
            return "OT"
        else:
            return f"{self.period - 4}OT"

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
            if self.period > 4:
                return f"FINAL/{self.periodLabel()}"  # "FINAL/OT", "FINAL/2OT"
            return "FINAL"

        elif self.status == "in":
            return self._liveClockString()

        return ""

    def _liveClockString(self):
        # Handles all the edge cases for in-progress games.
        # Uses self.description (from ESPN status.type.description) as the
        # most reliable signal for between-quarter and halftime states.

        if self.description:
            desc = self.description.lower()
            if "halftime" in desc:
                return "HALF"
            if "end of" in desc:
                # "End of 1st Quarter" → "END Q1"
                return f"END {self.periodLabel()}"
            if "overtime" in desc and not self.clock:
                return f"{self.periodLabel()}"

        # clock is empty or zero with no useful description
        clock_is_empty = not self.clock or self.clock in ("0:00", "00:00", '0.0' "")
        if clock_is_empty:
            if self.period == 2:
                return "HALF"
            elif self.period > 0:
                return f"END {self.periodLabel()}"
            return "LIVE"

        # normal in-progress state — just show the clock
        return self.clock
    
    def updateFrom(self, event):
        super().updateFrom(event)

        comp = event["competitions"][0]
        status_block = comp["status"]
        self.period    = status_block.get("period", self.period)
        self.clock     = status_block.get("displayClock", self.clock)
        self.timeDesc = status_block.get("type", {}).get("description", self.timeDesc)

    def __str__(self):
        return f"{self.team1.name} {self.team1.score} ||    || {self.team2.name} {self.team2.score}  || {self.displayClock()} || {self.status} | {self.startTime} || importance: {self.importance}"