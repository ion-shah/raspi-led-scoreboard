# each scene is going to showcase different info depending on the sport,
# this is the basketball scene, which will show the score, quarter, and cloc

from utils.abbreviations import getDisplayAbbr
from scenes.base_scene import *

class BasketballScene(BaseScene):
    
    def __init__(self, BasketballData, timezone="UTC"):
        super().__init__()
        self.imgSize = 48

        #each part of the basketball data needs to be added to the class
        self.drawings = {
            "team1img": ImgArgs(self.getLogoPath(BasketballData.league, BasketballData.team1), self.imgSize, -12),
            "team2img": ImgArgs(self.getLogoPath(BasketballData.league, BasketballData.team2), self.imgSize, -12, right_image=True),
        }

        if BasketballData.status == "pre":
            self.drawings |= {
                "pre-clock-string": FontArgs(JERSEY20_FONT, BasketballData.displayClock(timezone), 64, 16, white),
            }
        else:
            self.drawings |= {
                'center-dash': FontArgs(JERSEY20_FONT, '-', 64, 16, white),

                "team1score": FontArgs(JERSEY20_FONT, BasketballData.team1.score, 55, 16, white, 'r'),
                "team2score": FontArgs(JERSEY20_FONT, BasketballData.team2.score, 68, 16, white, 'l'),

                "team1abbr": FontArgs(JERSEY20_FONT, getDisplayAbbr(BasketballData.league, BasketballData.team1.abbr), 59, 28, grey, 'r'),
                "team2abbr": FontArgs(JERSEY20_FONT, getDisplayAbbr(BasketballData.league, BasketballData.team2.abbr), 66, 28, grey, 'l'),

                "clock": FontArgs(SMALL_FONT), BasketballData.displayClock(timezone), 66, 4, grey)
            }


    def getLogoPath(self, league, TeamData):
        return f"assets/imgs/logos/nba/teams/{getDisplayAbbr(league, TeamData.abbr)}.png"
    