import time
from scenes.base_scene import *

class ClockScene(BaseScene):
    def __init__(self):
        super().__init__()
        self.drawings = {
            "clock" : FontArgs(JERSEY20_FONT, time.strftime("%I:%M %p").lstrip("0"), 64, 16, white)
        }