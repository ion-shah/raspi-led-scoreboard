# this file has some relevant functions for handling time

from datetime import datetime, timezone
import pytz

def parseDate(dateStr):
    # this function takes in a date string from the API and returns a datetime object
    return datetime.strptime(dateStr, "%Y-%m-%dT%H:%MZ").replace(tzinfo=timezone.utc)

def formatLocalTime(dt, timezone_str):
    # this function takes in a datetime object and a timezone string, and returns a formatted time string in that timezone
    local_tz = pytz.timezone(timezone_str)
    local_time = dt.astimezone(local_tz)
    return local_time.strftime("%I:%M %p").lstrip("0")