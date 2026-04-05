# this file has functions that help with the spacing of text on the scoreboard
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PIL import Image, ImageDraw, ImageFont
import time, math
from scenes.base_scene import FontData, jersey20_font, small_bdf_font

try:
    from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
except ImportError:
    print("RGBMatrix library not found, using emulator.")
    from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions, graphics

def draw_text_spaced(canvas, font_data, x, y, color, text, double=False):


    """
    Draw BDF text onto canvas with custom letter spacing.
    double=True renders at 2x size using nearest-neighbor scaling.
    """
    fill = (color.red, color.green, color.blue)
    font = font_data.font
    font_path = font_data.font_path
    spacing = font_data.glyphSpacing

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
    #from bdfparser import Font as BdfFont

    bdf    = font_data.bdf
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

def get_text_width(font_data, text, double=False):
    spacing = font_data.glyphSpacing
    native_w = 0
    for char in text:
        glyph = font_data.bdf.glyph(char)
        if glyph:
            native_w += glyph.meta['dwx0'] + spacing
    native_w = max(native_w - spacing, 1)
    return native_w * 2 if double else native_w


def image_y_offset(canvas_height, image_height):
    """
    Returns the offset_y to vertically center an image on the canvas.
    Pass this to canvas.SetImage(img, offset_x, offset_y).
    
    canvas_height : canvas.height  (32)
    image_height  : the height of the PIL image after resizing
    """
    return (canvas_height - image_height) // 2


def image_x_offsets(canvas_width, image_width, padding=2):
    """
    Returns (left_x, right_x) offsets to place two images on opposite sides.
    Pass these to canvas.SetImage(img, offset_x, offset_y).

    canvas_width : canvas.width  (128)
    image_width  : width of the image (assumes both images same width)
    padding      : pixels between image edge and canvas edge
    """
    left_x  = padding
    right_x = canvas_width - image_width - padding
    return left_x, right_x


def text_coords_center(font_data, text, center_x, center_y, double=False):
    """
    Given a center point on the canvas, returns the (x, y) to pass to
    draw_text_spaced so the text is visually centered on that point.

    The returned y accounts for the BDF baseline offset — you should pass
    it directly to draw_text_spaced without any further adjustment.

    center_x : horizontal center you want the text to appear at
    center_y : vertical center you want the text to appear at
    double   : set True if you're calling draw_text_spaced with double=True
    """

    scale    = 2 if double else 1
    baseline = font_data.font.baseline * scale
    height   = font_data.font.height   * scale
    width    = get_text_width(font_data, text, double=double)

    x = center_x - round(width / 2) -1
    y = center_y + height // 2 - (height - baseline)

    return x, y

def text_coords_right(font_data, text, right_x, y, double=False):
    """
    Returns (x, y) to pass to draw_text_spaced so the text's right edge
    lands at right_x.

    right_x : the x coordinate you want the text to end at
    y       : vertical position (same meaning as in text_coords)
    """
    scale    = 2 if double else 1 
    baseline = font_data.font.baseline * scale
    height   = font_data.font.height   * scale
    width    = get_text_width(font_data, text, double=double)

    x = right_x - width
    y = y + height // 2 - (height - baseline)

    return x, y

def text_coords_left(font_data, text, left_x, y, double=False):
    """
    Returns (x, y) to pass to draw_text_spaced so the text's left edge
    starts at left_x.

    left_x : the x coordinate you want the text to start at
    y      : vertical position (same meaning as in text_coords)
    """
    scale    = 2 if double else 1
    baseline = font_data.font.baseline * scale
    height   = font_data.font.height   * scale

    x = left_x
    y = y + height // 2 - (height - baseline)

    return x, y

def draw_font(canvas, font_data, text, x, y, color, alignment="centered", double=False):
    a = alignment.lower()
    if a in ["left", 'l']:
        location = text_coords_left(font_data, text, x, y, double=double)
    elif a in ["right", "r"]:
        location = text_coords_right(font_data, text, x, y, double=double)
    else:
        location = text_coords_center(font_data, text, x, y, double=double)

    newx, newy = location

    draw_text_spaced(canvas, font_data, newx, newy, color, text, double=double)