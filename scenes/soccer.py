# each scene is going to showcase different info depending on the sport,
# this is the soccer scene, which will show the score, and clock

from utils.overrides import getDisplayAbbr
from scenes.base_scene import *
import os

class SoccerScene(BaseScene):
    
    def __init__(self, SoccerData, timezone="UTC"):
        super().__init__()
        self.imgSize = 48
        self.retroLogos = False #uses alternate logos if available

        #each part of the soccer data needs to be added to the class
        self.drawings = {
            "team1img": ImgArgs(self._resolve_logo_path(SoccerData.league, SoccerData.team1.abbr), self.imgSize, -12),
            "team2img": ImgArgs(self._resolve_logo_path(SoccerData.league, SoccerData.team2.abbr), self.imgSize, -12, right_image=True),
        }

        if SoccerData.status == "pre":
            self.drawings |= {
                "pre-clock-string": FontArgs(JERSEY20_FONT, SoccerData.displayClock(timezone), 64, 16, white),
            }
        else:
            self.drawings |= {
                'center-dash': FontArgs(JERSEY20_FONT, '-', 64, 16, white),

                "team1score": FontArgs(JERSEY20_FONT, SoccerData.team1.score, 55, 16, white, 'r'),
                "team2score": FontArgs(JERSEY20_FONT, SoccerData.team2.score, 72, 16, white, 'l'),

                "team1abbr": FontArgs(JERSEY20_FONT, getDisplayAbbr(SoccerData.league, SoccerData.team1.abbr), 59, 28, grey, 'r'),
                "team2abbr": FontArgs(JERSEY20_FONT, getDisplayAbbr(SoccerData.league, SoccerData.team2.abbr), 68, 28, grey, 'l'),

                "clock": FontArgs(SMALL_FONT, SoccerData.displayClock(timezone), 66, 4, grey)
            }
