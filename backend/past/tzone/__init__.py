import pytz

import util

tz = pytz.timezone('Europe/Prague')
t = util.stringToTime("01.01.2017 01:00:00")
print(t)