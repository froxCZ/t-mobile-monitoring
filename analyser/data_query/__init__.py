import datetime

from .DateRangeGroupQuery import DateRangeGroupQuery
from .DatesQuery import DatesQuery
from .SimilarDaysMedianQuery import SimilarDaysMedianQuery


def medianDateRange(fromDate, toDate, lobName, granularity, data):
  fromDate = fromDate.replace(hour=0, minute=0, second=0)
  toDate = toDate.replace(hour=0, minute=0, second=0)
  dayDelta = datetime.timedelta(days=1)
  medianList = []
  date = fromDate
  while date < toDate:
    l = minuteDictToDateDict(date, SimilarDaysMedianQuery(lobName, date, granularity=granularity).execute(), "median")
    for d, v in l.items():
      medianList.append(v)
    date += dayDelta
  valueKey = lobName
  # valueKey = "smoothed"
  if True:
    data = merge2DateLists(medianList, ["median", "dayAverage"], data, [valueKey])
    for tick in data:
      if tick[valueKey] == tick["median"]:
        tick["relativeDifference"] = 1
        tick["scaledDifference"] = 1
      else:
        diff = tick[valueKey] - tick["median"]
        tick["relativeDifference"] = min(tick[valueKey] / max(tick["median"], 0.1), 3)
        if tick["dayAverage"] != 0:
          scaledDiff = min((diff / tick["dayAverage"]) + 1, 3)
          if scaledDiff >= 1 and tick["relativeDifference"] >= 1:
            tick["scaledDifference"] = min(scaledDiff, tick["relativeDifference"])
          else:
            tick["scaledDifference"] = max(scaledDiff, tick["relativeDifference"])
            # tick["scaledDifference"] = min((diff / tick["dayAverage"]) + 1, 3)
        else:
          tick["scaledDifference"] = 1


  else:
    print("SHOULD NOT HAPPEN X")
  return data


def minuteDictToDateDict(baseDate, dict, valueName):
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
  sortedKeys = sorted(dateDict.keys())
  sortedList = []
  for key in sortedKeys:
    sortedList.append(dateDict[key])
  return sortedList


def listToDateDict(l):
  dateDict = {}
  for i in l:
    dateDict[i["_id"]] = i
  return dateDict
