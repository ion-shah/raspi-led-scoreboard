# utils/brightness.py
from datetime import datetime
import pytz

def getBrightness(config):
    # Returns brightness based on schedule in config.yaml.
    # Falls back to hardware.brightness if schedule is disabled.
    base      = config["hardware"]["brightness"]
    schedule  = config["display"]["brightness_schedule"]

    if not schedule.get("enabled", False):
        return base

    tz  = pytz.timezone(config["display"]["timezone"])
    now = datetime.now(tz).strftime("%H:%M")

    day_start   = schedule["day_start"]
    night_start = schedule["night_start"]

    if day_start <= now < night_start:
        return schedule["day_brightness"]
    else:
        return schedule["night_brightness"]