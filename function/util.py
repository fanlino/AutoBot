from datetime import datetime, timedelta
from dateutil import tz


# convert utc time to local time
def utctime_to_localtime(utctime: datetime):
    local_tz = tz.tzlocal()
    utc_tz = tz.gettz('UTC')
    utctime = utctime.replace(tzinfo=utc_tz)
    localtime = utctime.astimezone(local_tz)
    return localtime
    