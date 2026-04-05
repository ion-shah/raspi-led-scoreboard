#===create fonts===
try:
    from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
except ImportError:
    print("RGBMatrix library not found, using emulator.")
    from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions, graphics

from bdfparser import Font as BdfFont

class FontData:
    def __init__(self, font_name, font_path, glyphSpacing):
        self.font_name    = font_name
        self.font_path    = font_path
        self.glyphSpacing = glyphSpacing

        font = graphics.Font()
        font.LoadFont(font_path)
        self.font = font

        self.bdf = BdfFont(font_path)   # loaded once, reused everywhere
#this font is used for the large score displays
jersey20_font = FontData(
    font_name = "Jersey20-custom",
    font_path = "assets/fonts/Jersey20-custom.bdf",
    glyphSpacing = 1
)
#this font is for small auxillary text like team abbreviations and clock
small_bdf_font = FontData(
    font_name = "6x10",
    font_path = "assets/fonts/6x10.bdf",
    glyphSpacing = 1
)
#======================

#=====colors======
white = graphics.Color(255, 255, 255)
grey = graphics.Color(100, 100, 100)
#=================

# each scene class contains all the arguments to create the image on the matrix
# the scene is sent to the utils/renderer.py to actually generate the image
