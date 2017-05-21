import copy
import datetime
import logging
import random
import string
import time

import dateutil.parser
import pytz

"""
General util file for all application modules.
"""
utc = pytz.timezone("UTC")
from config.AppConfig import TIMEZONE, AppConfig


def jsStringToDate(string):
  return TIMEZONE.localize(dateutil.parser.parse(string))


def stringToDate(dateString):
  return TIMEZONE.localize(datetime.datetime.strptime(dateString, "%d.%m.%Y"))


def stringToTime(dateTimeString):
  return TIMEZONE.localize(datetime.datetime.strptime(dateTimeString, "%d.%m.%Y %H:%M:%S"))


def dateToTimeString(date):
  return date.replace(microsecond=0).isoformat()  # .strftime("%d.%m.%Y %H:%M:%S")


def dateDataListToList(dateDataList, metricName):
  dataList = []
  for row in dateDataList:
    dataList.append(row[metricName])
  return dataList


def dateToDayMinutes(date):
  return date.hour * 60 + date.minute


def listToDayMinutes(dataList, value="value"):
  day = {}
  for i in dataList:
    day[dateToDayMinutes(i["_id"])] = i[value]
  return day


def resetDateTimeMidnight(dateTime):
  # return dateTime.replace(hour=0, minute=0, second=0, microsecond=0)
  return TIMEZONE.localize(datetime.datetime.combine(dateTime.date(), datetime.datetime.min.time()))


def str2bool(value):
  return {"True": True, "true": True}.get(value, False)


def minuteDictToDateDict(baseDate, dict, valueName):
  """
  from dict having minutes in a day as attribute creates a dict with attributes basedate+minute
  :param baseDate:
  :param dict:
  :param valueName:
  :return:
  """
  dateDict = {}
  baseDate = baseDate
  if (len(dict.values()) == 0):
    return dateDict
  if (len(dict.values()) == 1):
    granularity = 1440
  else:
    keys = sorted(dict.keys())
    granularity = int(keys[1] - keys[0])

  d = resetDateTimeMidnight(baseDate)
  until = resetDateTimeMidnight(baseDate + datetime.timedelta(days=1))
  while d < until:
    minuteOfDay = d.hour * 60 + d.minute
    if minuteOfDay in dict:
      minuteVal = dict[minuteOfDay]
    else:
      minuteVal = 0
    dateDict[d] = {"_id": d, valueName: minuteVal}
    d = getNextTic(d, granularity)
  return dateDict


def merge2DateLists(list1, val1, list2, val2):
  """
  merges two dicts into one by _id. If value is missing, it sets it to 0
  :param list1:
  :param val1: list of values in list 1
  :param list2:
  :param val2: list of values in list 2
  :return:
  """
  d = {}
  if len(list1) != len(list2):
    logging.error("lists are different! %s,%s", len(list1), len(list2))
  assert len(list1) == len(list2)
  list1NullObject = None
  list2NullObject = None
  if val1 is not None:
    list1NullObject = {}
    for i in val1:
      list1NullObject[i] = 0
  if val2 is not None:
    list2NullObject = {}
    for i in val2:
      list2NullObject[i] = 0

  for i in list1:
    iCopy = copy.copy(i)
    key = iCopy["_id"]
    if list2NullObject is not None:
      iCopy.update(list2NullObject)
    d[key] = iCopy
  for i in list2:
    key = i["_id"]
    if key in d:
      d[key].update(i)
    else:
      if list1NullObject is not None:
        i.update(list1NullObject)
      d[key] = i
  return dictToSortedList(d)


def dictToSortedList(dateDict):
  """
  converts dict with date attributes to a list
  :param dateDict:
  :return:
  """
  sortedKeys = sorted(dateDict.keys())
  sortedList = []
  for key in sortedKeys:
    sortedList.append(dateDict[key])
  return sortedList


def listToDateDict(l):
  """
  takes list of {_id, ..} and creates a dict
  :param l:
  :return:
  """
  dateDict = {}
  for i in l:
    dateDict[i["_id"]] = i
  return dateDict


def randomHash(size):
  return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))


def getNextTic(d, granularity):
  """
  returns next tick
  :param d:
  :param granularity:
  :return:
  """
  prevOffsetSeconds = d.tzinfo._utcoffset.total_seconds()
  from config import AppConfig
  newTic = (d + datetime.timedelta(minutes=granularity)).astimezone(AppConfig.getTimezone())
  newOffsetSeconds = newTic.tzinfo._utcoffset.total_seconds()
  if prevOffsetSeconds != newOffsetSeconds:
    if prevOffsetSeconds < newOffsetSeconds:
      newTic = getTicTime(newTic, granularity)
    else:
      newTic = roundToNextTicTime(newTic, granularity)
  return getTicTime(newTic, granularity)


def roundToNextTicTime(time, granularity):
  minuteOfDay = time.hour * 60 + time.minute
  minutesOverInterval = minuteOfDay % granularity
  naiveTime = time.replace(tzinfo=None)
  latestClosedIntervalNaiveTime = naiveTime + datetime.timedelta(minutes=granularity - minutesOverInterval)
  latestClosedIntervalNaiveTime = latestClosedIntervalNaiveTime.replace(second=0, microsecond=0)
  return AppConfig.getTimezone().localize(latestClosedIntervalNaiveTime)


def getTicTime(time, granularity):
  minuteOfDay = time.hour * 60 + time.minute
  minutesOverInterval = minuteOfDay % granularity
  naiveTime = time.replace(tzinfo=None)
  latestClosedIntervalNaiveTime = naiveTime - datetime.timedelta(minutes=minutesOverInterval)
  latestClosedIntervalNaiveTime = latestClosedIntervalNaiveTime.replace(second=0, microsecond=0)
  return AppConfig.getTimezone().localize(latestClosedIntervalNaiveTime)


def getNextDay(d):
  dayDelta = datetime.timedelta(days=1)
  return AppConfig.getTimezone().localize(d.replace(tzinfo=None) + dayDelta)


def startTime():
  return time.time()


def timeDifference(startTime):
  return (time.time() - startTime)


if __name__ == "__main__":
  t = stringToTime("29.10.2017 00:00:00")
  gran = 120
  t1 = getNextTic(t, gran)
  t2 = getNextTic(t1, gran)
  t3 = getNextTic(t2, gran)
  t4 = getNextTic(t3, gran)
  t5 = getNextTic(t4, gran)
