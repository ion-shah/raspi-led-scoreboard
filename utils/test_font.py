# setup/test_font.py
# this is a file to test out the Jersey 20 font
"""
Run on the Pi to see exactly how Jersey 20 looks on the physical panel.
Before running:
  1. Download Jersey_20-Regular.ttf from Google Fonts
  2. Place it at assets/fonts/Jersey20-Regular.ttf
  3. Copy a few .bdf fonts from rpi-rgb-led-matrix/fonts/ to assets/fonts/

Usage:
  sudo venv/bin/python setup/test_font.py

Controls:
  The display cycles through screens automatically every 3 seconds.
  Press Ctrl+C to exit.
"""

import time
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from PIL import Image, ImageDraw, ImageFont
from rgbmatrix import RGBMatrix, RGBMatrixOptions


# ── Matrix setup ──────────────────────────────────────────────────────────────

def make_matrix():
    opts = RGBMatrixOptions()
    opts.rows = 32
    opts.cols = 64
    opts.chain_length = 2
    opts.hardware_mapping = 'adafruit-hat-pwm'    
    opts.brightness = 80
    opts.disable_hardware_pulsing = True      # needed on Pi Zero / Pi 4 without root PWM access
    # opts.gpio_slowdown = 2                  # uncomment if you see flickering
    return RGBMatrix(options=opts)


# ── Font helpers ───────────────────────────────────────────────────────────────

FONT_DIR = os.path.join(os.path.dirname(__file__), '..', 'assets', 'fonts')

def ttf(size):
    path = os.path.join(FONT_DIR, 'Jersey20-Regular.ttf')
    if not os.path.exists(path):
        raise FileNotFoundError(f"Font not found at: {os.path.abspath(path)}")
    return ImageFont.truetype(path, size)

def bdf(name):
    path = os.path.join(FONT_DIR, name)
    return ImageFont.load(path)


# ── Individual test screens ────────────────────────────────────────────────────

def screen_jersey_sizes():
    """Jersey 20 at multiple sizes so you can pick what fits your panel."""
    img = Image.new('RGB', (128, 32), (0, 0, 0))
    d = ImageDraw.Draw(img)

    # Row 1 — size 8: fits two lines of data easily
    d.text((1, 0),  '76  LAL',  font=ttf(8),  fill=(255, 180, 0))

    # Row 2 — size 10: slightly larger scores
    d.text((1, 10), '102 BOS',  font=ttf(10), fill=(0, 200, 80))

    # Row 3 — size 12: big score, only one row fits
    d.text((1, 20), '88  NYK',  font=ttf(12), fill=(0, 120, 255))

    return img, 'Jersey 20 — sizes 8 / 10 / 12'


def screen_jersey_vs_bdf():
    """Side-by-side: Jersey 20 (left) vs a BDF font (right)."""
    img = Image.new('RGB', (128, 32), (0, 0, 0))
    d = ImageDraw.Draw(img)

    # Left half — Jersey 20 size 10
    d.text((1,  1),  'TTF',       font=ttf(10), fill=(255, 255, 255))
    d.text((1,  12), '108',       font=ttf(10), fill=(255, 180, 0))
    d.text((1,  23), 'LAL',       font=ttf(8),  fill=(150, 150, 150))

    # Divider
    d.line([(32, 0), (32, 31)], fill=(40, 40, 40))

    # Right half — BDF 6x10 (swap filename if you don't have this one)
    try:
        f_bdf = bdf('6x10.bdf')
        d.text((34, 1),  'BDF',  font=f_bdf, fill=(255, 255, 255))
        d.text((34, 12), '108',  font=f_bdf, fill=(255, 180, 0))
        d.text((34, 23), 'LAL',  font=f_bdf, fill=(150, 150, 150))
    except Exception:
        d.text((34, 12), 'no bdf', font=ttf(8), fill=(100, 100, 100))

    return img, 'Jersey TTF vs BDF side-by-side'


def screen_full_scoreboard_mock():
    """Realistic NBA scoreboard layout using Jersey 20."""
    img = Image.new('RGB', (128, 32), (0, 0, 0))
    d = ImageDraw.Draw(img)

    # Team abbreviations — small, top row
    abbr_font = ttf(8)
    d.text((1,  0), 'LAL', font=abbr_font, fill=(180, 140, 60))   # Lakers gold
    d.text((44, 0), 'BOS', font=abbr_font, fill=(0, 160, 60))     # Celtics green

    # Scores — larger, middle
    score_font = ttf(12)
    d.text((1,  10), '108', font=score_font, fill=(255, 255, 255))
    d.text((44, 10), '112', font=score_font, fill=(255, 255, 255))

    # Clock and period — bottom, small
    clock_font = ttf(8)
    d.text((18, 24), '4:32  Q3', font=clock_font, fill=(160, 160, 160))

    return img, 'Full NBA mock — Jersey 20'


def screen_antialiasing_closeup():
    """
    Single large character so you can see antialiasing up close.
    Useful for judging whether gray edge pixels look good or muddy.
    """
    img = Image.new('RGB', (128, 32), (0, 0, 0))
    d = ImageDraw.Draw(img)

    # One huge digit centered — exposes every antialiased edge pixel
    d.text((4, 0), '108', font=ttf(20), fill=(255, 220, 0))

    return img, 'Antialiasing test — size 20'


def screen_color_on_black():
    """Different text colors to see how Jersey 20 reads on the panel."""
    img = Image.new('RGB', (128, 32), (0, 0, 0))
    d = ImageDraw.Draw(img)

    f = ttf(10)
    d.text((1,  0),  'WHITE',  font=f, fill=(255, 255, 255))
    d.text((1,  11), 'YELLOW', font=f, fill=(255, 210, 0))
    d.text((1,  22), 'CYAN',   font=f, fill=(0, 220, 220))

    return img, 'Color test — Jersey 20'


# ── Main loop ─────────────────────────────────────────────────────────────────

SCREENS = [
    screen_jersey_sizes,
    screen_jersey_vs_bdf,
    screen_full_scoreboard_mock,
    screen_antialiasing_closeup,
    screen_color_on_black,
]

HOLD_SECONDS = 3  # how long to show each screen before advancing


def main():
    matrix = make_matrix()
    print('Font test running. Ctrl+C to exit.')
    print(f'Cycling {len(SCREENS)} screens, {HOLD_SECONDS}s each.\n')

    i = 0
    try:
        while True:
            fn = SCREENS[i % len(SCREENS)]
            img, label = fn()
            matrix.SetImage(img.convert('RGB'))
            print(f'  [{i % len(SCREENS) + 1}/{len(SCREENS)}] {label}')
            time.sleep(HOLD_SECONDS)
            i += 1
    except KeyboardInterrupt:
        matrix.Clear()
        print('\nDone.')


if __name__ == '__main__':
    main()