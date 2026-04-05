# each scene is going to showcase different info depending on the sport,
# this is the basketball scene, which will show the score, quarter, and cloc

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PIL import Image, ImageDraw, ImageFont
import time

from utils.layout import *
from base_scene import *

try:
    from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
except ImportError:
    print("RGBMatrix library not found, using emulator.")
    from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions, graphics

# --- matrix setup ---
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 2
options.hardware_mapping = 'adafruit-hat-pwm'
options.led_rgb_sequence = 'GBR'

matrix = RGBMatrix(options=options)
canvas = matrix.CreateFrameCanvas()  # ← fix: create canvas first

size = 48
score = "38"

imgY = image_y_offset(32, size)
imgXleft, imgXright = image_x_offsets(128, size, -12)



img1 = Image.open('assets/imgs/logos/nba/teams/BOS.png').convert('RGB')
img1 = img1.resize((size, size), Image.LANCZOS)

img2 = Image.open('assets/imgs/logos/nba/teams/NYK.png').convert('RGB')
img2 = img2.resize((size, size), Image.LANCZOS)

canvas.SetImage(img1, imgXleft, imgY)          # draw onto canvas, not matrix directly -15, -7
canvas.SetImage(img2, imgXright, imgY)          # draw onto canvas, not matrix directly


# DrawText(core.Canvas c, Font f, int x, int y, Color color, text):
color = graphics.Color(255, 255, 255)
grey = graphics.Color(100, 100, 100)

center = text_coords_center(jersey20_font, "-", 64, 16)
draw_text_spaced(canvas, jersey20_font, *center, color, '-', double=False)

#clockScoreLocation = text_coords(small_bdf_font, "Q3 4:18", 64, 4)
#draw_text_spaced(canvas, small_bdf_font, *clockScoreLocation, color, "Q3 4:18", double=False)

draw_font(canvas, jersey20_font, score, 55, 16, color, 'r')
draw_font(canvas, jersey20_font, score, 68, 16, color, 'l')

draw_font(canvas, small_bdf_font, "Q3 23:18", 66, 4, grey)

draw_font(canvas, jersey20_font, "BOS", 59, 28, grey, alignment='right')

draw_font(canvas, jersey20_font, "NYK", 66, 28, grey, alignment="left")



matrix.SwapOnVSync(canvas)    # push canvas to panel

input('press enter to exit')


