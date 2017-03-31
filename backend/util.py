import copy
import datetime
import random
import string

import dateutil.parser

from config.AppConfig import TIMEZONE


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
  return dateTime.replace(hour=0, minute=0, second=0, microsecond=0)


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
  for minute, x in dict.items():
    id = baseDate + datetime.timedelta(minutes=minute)
    dateDict[id] = {"_id": id, valueName: x}
  return dateDict


def merge2DateLists(list1, val1, list2, val2):
  """
  merges two dicts into one by _id. If value is missing, it sets it to 0
  :param list1:
  :param val1:
  :param list2:
  :param val2:
  :return:
  """
  d = {}
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
  return dateDictToList(d)


def dateDictToList(dateDict):
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
