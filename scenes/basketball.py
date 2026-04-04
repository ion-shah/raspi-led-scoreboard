# each scene is going to showcase different info depending on the sport,
# this is the basketball scene, which will show the score, quarter, and cloc
# k
from PIL import Image, ImageDraw, ImageFont
import time

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


size = 48

def draw_text_spaced(canvas, font, font_path, x, y, color, text, spacing=2, double=False):
    """
    Draw BDF text onto canvas with custom letter spacing.
    double=True renders at 2x size using nearest-neighbor scaling.
    """
    fill = (color.red, color.green, color.blue)

    # ── Normal size: draw directly onto canvas ────────────────────────────────
    if not double:
        cursor = x
        for char in text:
            if hasattr(font, 'DrawGlyph'):
                advance = font.DrawGlyph(canvas, cursor, y, color, ord(char))
            else:
                advance = graphics.DrawText(canvas, font, cursor, y, color, char)
            cursor += advance + spacing
        return cursor

    # ── Double size: render to Pillow via bdfparser, scale 2x, push to canvas ─
    from bdfparser import Font as BdfFont

    bdf    = BdfFont(font_path)
    g = bdf.glyph('0')

    native_h = font.height

    # Measure native width
    native_w = 0
    for char in text:
        glyph = bdf.glyph(char)
        if glyph:
            native_w += glyph.meta['dwx0'] + spacing
    native_w = max(native_w - spacing, 1)

    # Render glyphs into native-size Pillow image
    staging = Image.new('RGB', (native_w, native_h), (0, 0, 0))
    pixels  = staging.load()
    cursor  = 0

    for char in text:
        glyph = bdf.glyph(char)
        if glyph is None:
            cursor += 6 + spacing
            continue
        bitmap = glyph.draw().todata(2)
        rows   = len(bitmap)
        for row_idx, row in enumerate(bitmap):
            for col_idx, bit in enumerate(row):
                if not bit:
                    continue
                px = cursor + col_idx + glyph.meta['bbxoff']
                py = native_h - glyph.meta['bbyoff'] - rows + row_idx
                if 0 <= px < native_w and 0 <= py < native_h:
                    pixels[px, py] = fill
        cursor += glyph.meta['dwx0'] + spacing

    # Scale 2x and paste onto full panel image
    scaled  = staging.resize((native_w * 2, native_h * 2), Image.NEAREST)
    panel   = Image.new('RGB', (canvas.width, canvas.height), (0, 0, 0))
    paste_y = y - (font.baseline * 2)
    panel.paste(scaled, (x, max(paste_y, 0)))
    canvas.SetImage(panel)

    return x + native_w * 2

matrix = RGBMatrix(options=options)
canvas = matrix.CreateFrameCanvas()  # ← fix: create canvas first

img1 = Image.open('assets/imgs/logos/nba/teams/NYK.png').convert('RGB')
img1 = img1.resize((size, size), Image.LANCZOS)

img2 = Image.open('assets/imgs/logos/nba/teams/BOS.png').convert('RGB')
img2 = img2.resize((size, size), Image.LANCZOS)

font = graphics.Font()
font.LoadFont('assets/fonts/Jersey20-custom.bdf')

canvas.SetImage(img1, offset_x=-15, offset_y=-7)          # draw onto canvas, not matrix directly
canvas.SetImage(img2, offset_x=90, offset_y=-7)          # draw onto canvas, not matrix directly

# DrawText(core.Canvas c, Font f, int x, int y, Color color, text):
color = graphics.Color(255, 255, 255)
#graphics.DrawText(canvas, font, 30, 20, color, '100')
time.sleep(2)  # pause to show logos before drawing text
# DrawGlyph(self, core.Canvas c, int x, int y, Color color, uint32_t char):
draw_text_spaced(canvas, font, 'assets/fonts/Jersey20-custom.bdf', 10, 20, color, '    @ 7:30 ET', spacing=1, double=False)



matrix.SwapOnVSync(canvas)    # push canvas to panel

input('press enter to exit')