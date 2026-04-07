import time
from scenes.base_scene import *

class ClockScene(BaseScene):
    def __init__(self):
        super().__init__()
        self.drawings = {
            "clock" : FontArgs(JERSEY20_FONT, str(time.strftime("%I:%M")), 64, 16, white)
        }