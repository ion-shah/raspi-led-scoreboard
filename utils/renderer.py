# this file has the renderer object, that the main file will use to draw the scoreboard
from utils.layout import drawFont, drawImage
from scenes.base_scene import *

class Renderer:
    def __init__(self, canvas, timezone):
        self.canvas = canvas
        self.timezone = timezone
        self._last_key = None
    def render(self, scene, cache_key=None):
        if cache_key is not None and cache_key == self._last_key:
            #if same scene, do not redraw or clear
            return
        self._last_key = cache_key

        self.canvas.Clear()
        for drawing in scene.drawings.values():
            if isinstance(drawing, ImgArgs):
                drawImage(**drawing.__dict__, canvas=self.canvas)
            elif isinstance(drawing, FontArgs):
                drawFont(**drawing.__dict__, canvas=self.canvas)
    def swap(self, matrix):
        self.canvas = matrix.SwapOnVSync(self.canvas)
        return self.canvas
