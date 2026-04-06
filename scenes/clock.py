import time
from scenes.base_scene import *

class ClockScene(BaseScene):
    def __init__(self):
        super().__init__()
        self.drawings = {
            "clock" : FontArgs(JERSEY20_FONT, lambda: time.strftime("%I:%M"), 66, 4, white)
        }