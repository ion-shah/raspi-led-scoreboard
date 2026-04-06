# this file has the renderer object, that the main file will use to draw the scoreboard
from utils.layout import drawFont, drawImage
from scenes.base_scene import *

class Renderer:
    def __init__(self, canvas, timezone):
        self.canvas = canvas
        self.timezone = timezone
    def render(self, scene):
        self.canvas.Clear()
        for drawing in scene.drawings.values():
            if isinstance(drawing, ImgArgs):
                drawImage(**drawing.__dict__, canvas=self.canvas)
            elif isinstance(drawing, FontArgs):
                drawFont(**drawing.__dict__, canvas=self.canvas)
