# this mixin assigns an importance score to each game for display prioritization.
# Higher score = shown first. Games above pin_threshold pause rotation entirely.

STATUS_SCORES = {
    "in":   50,
    "pre":  10,
    "post":  5,
}

class ImportanceMixin:

    # the following __Score functions assign an importance based on an attribute
    def _favoriteScore(self, favorites, base=40, step=5, floor=5):
        score = 0
        for team in [self.team1, self.team2]:
            for i, abbr in enumerate(favorites):
                if team.name == abbr:
                    score += max(base - (i * step), floor)
        return score

    def _leagueScore(self, favorite_leagues, base=50, step=20, floor=20):
        for i, league in enumerate(favorite_leagues):
            if self.league == league:
                return max(base - (i * step), floor)
        return 0

    def _collegeRankScore(self): # ranked college teams get increased importance
        score = 0
        for team in [self.team1, self.team2]:
            if team.ranked and team.ranked > 0:
                score += max(26 - team.ranked, 0)
        return score

    def calculateImportance(self, config):
        # Calculates and sets self.importance based on config
        # Call this after each refresh cycle
        
        sports_config = config["sports"].get(self.league, {})
        favorites = sports_config.get("favorites", [])
        favorite_leagues = config.get("priority", {}).get("favorite_leagues", [])

        self.importance = (
            STATUS_SCORES.get(self.status, 0)
            + self._leagueScore(favorite_leagues)
            + self._favoriteScore(favorites)
            + self._collegeRankScore()
        )

    def isPinned(self, config):
        # Returns True if this game should pause the display rotation. 
        threshold = config.get("priority", {}).get("pin_threshold", 150)
        return self.importance >= threshold