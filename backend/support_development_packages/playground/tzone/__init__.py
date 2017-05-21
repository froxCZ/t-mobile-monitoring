import datetime

import pytz
from dateutil import tz

from common import util
prg = pytz.timezone('Europe/Prague')
dateutilPrg = tz.gettz('Europe/Prague')
utc = pytz.timezone('UTC')
cet = pytz.timezone('CET')
# t = util.stringToTime("01.01.2017 01:00:00")
# print(t)
day = util.resetDateTimeMidnight(util.stringToTime("26.03.2017 07:00:00"))
day2 = util.resetDateTimeMidnight(util.stringToTime("26.03.2017 00:00:00")+datetime.timedelta(days=1))
print(day.astimezone(utc))
print(util.resetDateTimeMidnight(day+datetime.timedelta(days=1)).astimezone(utc))
x = (util.stringToTime("27.03.2017 00:00:00")+datetime.timedelta(days=1)).astimezone(utc)

# print(prg.localize(datetime.datetime(2017, 3, 26, 1, 0, 0, 0)))
# print(prg.localize(datetime.datetime(2017, 3, 26, 2, 0, 0, 0)))
# print(prg.localize(datetime.datetime(2017, 3, 26, 3, 0, 0, 0)))
# print(prg.localize(datetime.datetime(2017, 3, 26, 2, 0, 0, 0)) == prg.localize(datetime.datetime(2017, 3, 26, 3, 0, 0, 0)))
# print("--")
# print(datetime.datetime(2017, 3, 26, 0, 0, 0, 0,cet).astimezone(prg))
# print(datetime.datetime(2017, 3, 26, 1, 0, 0, 0,cet).astimezone(prg))
# print(datetime.datetime(2017, 3, 26, 2, 0, 0, 0,cet).astimezone(prg))
# print(datetime.datetime(2017, 3, 26, 3, 0, 0, 0,cet).astimezone(prg))
# #BUG!
# print("----")
# arr = datetime.datetime(2017, 3, 26, 2,0,0,0,dateutilPrg)
# print(arr)

util.stringToTime("27.03.2017 15:35:03")
