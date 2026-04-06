
try:
    from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
    BdfFont = None
except ImportError:
    print("RGBMatrix library not found, using emulator.")
    from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions, graphics
    from bdfparser import Font as BdfFont

__all__ = [
    "BaseScene",
    "FontArgs", "ImgArgs",
    "JERSEY20_FONT", "SMALL_FONT",
    "white", "grey",
]

class FontData:
    def __init__(self, font_name, font_path, glyphSpacing):
        self.font_name    = font_name
        self.font_path    = font_path
        self.glyphSpacing = glyphSpacing

        font = graphics.Font()
        font.LoadFont(font_path)
        self.font = font

        self.bdf = BdfFont(font_path) if BdfFont is not None else None
#this font is used for the large score displays
JERSEY20_FONT = FontData(
    font_name = "Jersey20-custom",
    font_path = "assets/fonts/Jersey20-custom.bdf",
    glyphSpacing = 1
)
#this font is for small auxillary text like team abbreviations and clock
SMALL_FONT = FontData(
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

class FontArgs:
    def __init__(self, font_data, text, x, y, color, alignment="centered", double=False):
        self.font_data = font_data
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.alignment = alignment
        self.double = double

class ImgArgs:
    def __init__(self, img_path, img_size, padding=None, right_image=False):
        self.img_path = img_path
        self.img_size = img_size
        self.padding = padding
        self.right_image = right_image


# each class is essentially a list of FontArgs and ImgArgs classes but with cleaner constructors

#the base scene has the data that corresponds to the Game class
class BaseScene:
    def __init__(self):
        # drawings is a dict in the form of 
        # {'short_desc' : Args}
        # each subclass will populate it
        self.drawings = {}
