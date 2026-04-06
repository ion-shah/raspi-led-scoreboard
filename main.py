import time
from datetime import datetime, timezone
from utils.config_loader import loadConfig, getEnabledSports
from data import fetchScoreboard, refreshGameList, getDisplayList, fetchAndRefresh, buildGameDict, getPollInterval
from utils import Renderer
from scenes import *
try:
    from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
except ImportError:
    print("RGBMatrix library not found, using emulator.")
    from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions, graphics

LIVE_POLL_INTERVAL = 5   # seconds between API polls when games are live
IDLE_POLL_INTERVAL = 30  # seconds between API polls when no games are live

# ====== initialization ======
print( "\n===============================\n"
      +"===     LED SCOREBOARD      ===\n"
      +"===============================\n")

print("Loading config.yaml...")
config = loadConfig()
print("config.yaml loaded and verified.\n")

DISPLAY_INTERVAL = config["display"]["scene_duration"]   # seconds each game is shown before rotating

#========== matrix setup ==============
print("Setting up matrix")
hardware = config["hardware"]

options = RGBMatrixOptions()
options.rows = hardware["rows"]
options.cols = hardware["cols"]
options.chain_length = hardware["chained"]
options.hardware_mapping = hardware["gpio_mapping"]
options.led_rgb_sequence = hardware["rgb_mapping"]

matrix = RGBMatrix(options=options)
canvas = matrix.CreateFrameCanvas() 
tz = config["display"]["timezone"]

renderer = Renderer(canvas, tz)

enabled = getEnabledSports(config)  # [("basketball", "nba"), ...]
print(f"Enabled sports: {enabled}\n")

game_cache = {}  # {gameID: Game object} — this will be updated on each API poll and used to build the display list
for sport, league in enabled:
    print(f"Fetching initial data for {sport} {league}...")
    data = fetchScoreboard(sport, league)
    if data is not None:
        game_cache.update(buildGameDict(data, sport))



# ============= main loop =============

print("\n\nEntering main loop...\n")

rotation_index   = 0
last_poll_time   = time.time()
last_switch_time = time.time()

try:
    while True:
        now = time.time()

        # -- Poll always runs first, every cycle if interval elapsed --
        if now - last_poll_time >= getPollInterval(game_cache, live_interval=LIVE_POLL_INTERVAL, idle_interval=IDLE_POLL_INTERVAL):
            #print(f"[POLL] fetching...")
            for sport, league in enabled:
                game_cache = fetchAndRefresh(game_cache, sport, league, config)
            last_poll_time = now
            #print(f"[POLL] cache has {len(game_cache)} games")

        # -- Build display list --
        display_list = getDisplayList(game_cache, config)

        # -- Render --
        if not display_list:
            #print(f"No relevant games — showing clock")
            renderer.render(ClockScene())
        else:
            # pinned game overrides rotation
            if display_list[0].isPinned(config):
                current_game = display_list[0]
            else:
                rotation_index = rotation_index % len(display_list)
                current_game = display_list[rotation_index]

                if now - last_switch_time >= DISPLAY_INTERVAL:
                    rotation_index = (rotation_index + 1) % len(display_list)
                    last_switch_time = now
                    #print(f"[ROTATE] switched to next game in rotation")

            #debug statements
            #print(current_game)
            #print(f"  clock:      {current_game.displayClock(config['display']['timezone'])}")
            #print(f"  period:     {current_game.periodLabel()}")
            #print(f"  importance: {current_game.importance}")
            #print(f"  pinned:     {current_game.isPinned(config)}")

            renderer.render(getScene(current_game, tz))

        matrix.SwapOnVSync(canvas)
        time.sleep(0.05)

except KeyboardInterrupt:
    print("Program stopped by user")