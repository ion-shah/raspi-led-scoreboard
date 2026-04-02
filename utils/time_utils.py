# this file has some relevant functions for handling time

from datetime import datetime, timezone
import pytz

def parseDate(dateStr):
    # this function takes in a date string from the API and returns a datetime object
    return datetime.strptime(dateStr, "%Y-%m-%dT%H:%MZ").replace(tzinfo=timezone.utc)