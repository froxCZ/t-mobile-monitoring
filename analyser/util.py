import datetime

import dateutil.parser

from config import TIMEZONE


def jsStringToDate(string):
  return dateutil.parser.parse(string).replace(tzinfo=TIMEZONE)


def dateToString(date):
  return date.strftime("%Y-%m-%dT%H:%M:%S.000Z")


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
  dayAverage = sum(dict.values()) / len(dict.values())
  for minute, x in dict.items():
    id = baseDate + datetime.timedelta(minutes=minute)
    dateDict[id] = {"_id": id, valueName: x, "dayAverage": dayAverage}
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
  list1NullObject = {}
  for i in val1:
    list1NullObject[i] = 0
  list2NullObject = {}
  for i in val2:
    list2NullObject[i] = 0

  for i in list1:
    key = i["_id"]
    i.update(list2NullObject)
    d[key] = i
  for i in list2:
    key = i["_id"]
    if key in d:
      d[key].update(i)
    else:
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
