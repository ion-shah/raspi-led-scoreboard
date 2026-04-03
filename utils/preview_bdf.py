"""
Shows all printable glyphs from a .bdf font directly on the matrix.
Uses the hzeller graphics module which natively supports .bdf files.

Usage:
    sudo venv/bin/python utils/preview_bdf.py assets/fonts/6x10.bdf
"""

import sys
import os
import time

from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

if len(sys.argv) < 2:
    print("Usage: sudo venv/bin/python utils/preview_bdf.py assets/fonts/6x10.bdf")
    sys.exit(1)

FONT_PATH = os.path.abspath(sys.argv[1])

if not os.path.exists(FONT_PATH):
    print(f"Font not found: {FONT_PATH}")
    sys.exit(1)

print(f"Loading font: {FONT_PATH}")

# ── Matrix setup ──────────────────────────────────────────────────────────────

def make_matrix():
    opts = RGBMatrixOptions()
    opts.rows             = 32
    opts.cols             = 64
    opts.chain_length     = 2
    opts.hardware_mapping = 'adafruit-hat-pwm'
    opts.brightness       = 80
    return RGBMatrix(options=opts)

# ── Load font ─────────────────────────────────────────────────────────────────

font = graphics.Font()
font.LoadFont(FONT_PATH)

# ── Build glyph string ────────────────────────────────────────────────────────
# Printable ASCII: space through ~
GLYPHS = ''.join(chr(c) for c in range(32, 127))

# Split into rows that fit the 128px wide canvas
# graphics.DrawText returns the advance width — we use a fixed estimate to
# chunk characters into rows, then let DrawText handle exact placement
CHARS_PER_ROW = 20
rows = [GLYPHS[i:i+CHARS_PER_ROW] for i in range(0, len(GLYPHS), CHARS_PER_ROW)]

print(f"Glyph rows: {len(rows)}")
print(f"Hold: Ctrl+C to exit\n")

matrix  = make_matrix()
canvas  = matrix.CreateFrameCanvas()
color   = graphics.Color(255, 255, 255)
row_h   = font.height + 2   # a little breathing room between rows

try:
    while True:
        # Scroll vertically if all rows don't fit on one screen
        total_h = len(rows) * row_h
        frames  = max(1, total_h)   # one scroll step per pixel

        for offset in range(frames):
            canvas.Clear()
            for i, row_text in enumerate(rows):
                y = i * row_h - offset + font.height
                if y < 0 or y > 32 + row_h:
                    continue        # skip off-screen rows
                graphics.DrawText(canvas, font, 1, y, color, row_text)
            canvas = matrix.SwapOnVSync(canvas)
            time.sleep(0.04)        # ~25fps scroll

        # Pause one second at the end before looping
        time.sleep(1)

except KeyboardInterrupt:
    matrix.Clear()
    print("Done.")