from statistics import median

import api.util as util
from mediation.api.data_query import DatesQuery


def getDayAverages(lobName):
  weekends = [util.jsStringToDate("2016-10-08T00:00:00.000Z"),
              util.jsStringToDate("2016-10-09T00:00:00.000Z"),
              util.jsStringToDate("2016-10-15T00:00:00.000Z"),
              util.jsStringToDate("2016-10-16T00:00:00.000Z"),
              util.jsStringToDate("2016-11-05T00:00:00.000Z"),
              util.jsStringToDate("2016-11-06T00:00:00.000Z")
              ]
  holidays = [util.jsStringToDate("2016-09-28T00:00:00.000Z"),
              util.jsStringToDate("2016-10-28T00:00:00.000Z"),
              util.jsStringToDate("2016-11-17T00:00:00.000Z")]
  workDays = [
    #util.jsStringToDate("2016-10-21T00:00:00.000Z"),
    util.jsStringToDate("2016-10-24T00:00:00.000Z"),
    util.jsStringToDate("2016-10-25T00:00:00.000Z"),
    util.jsStringToDate("2016-10-26T00:00:00.000Z"),
    util.jsStringToDate("2016-10-27T00:00:00.000Z"),
    util.jsStringToDate("2016-10-31T00:00:00.000Z"),
    util.jsStringToDate("2016-11-01T00:00:00.000Z"),
    util.jsStringToDate("2016-11-02T00:00:00.000Z"),
    util.jsStringToDate("2016-11-03T00:00:00.000Z"),
    #util.jsStringToDate("2016-11-04T00:00:00.000Z"),
  ]
  lazyDays = [util.jsStringToDate("2016-11-18-T00:00:00.000Z"), ]
  workdayData, workdayMetrics = DatesQuery(workDays, lobName, "value").execute()
  finalData, finalMetrics = DatesQuery(weekends, lobName, "value").execute()
  holidaysData, holidayMetrics = DatesQuery(holidays, lobName, "value").execute()
  lazyDaysData, lazyMetrics = DatesQuery(lazyDays, lobName, "value").execute()
  dayMedians = {}
  for minute, median in _createMeans(workdayData, "value").items():
    dayMedians[minute] = {"_id": minute}
    dayMedians[minute]["workDays"] = median

  for minute, median in _createMeans(finalData, "value").items():
    dayMedians[minute]["weekends"] = median

  for minute, median in _createMeans(holidaysData, "value").items():
    dayMedians[minute]["holidays"] = median
  for minute, median in _createMeans(lazyDaysData, "value").items():
    dayMedians[minute]["lazyDays"] = median

  finalMetrics.extend(workdayMetrics)
  finalMetrics.extend(holidayMetrics)
  response = {}
  response["data"] = sorted(dayMedians.values(), key=lambda x: x["_id"])
  response["metrics"] = ["weekends", "workDays", "holidays", "lazyDays"]
  return response


def _createMeans(data, valueName):
  day = {}
  for row in data:
    dateTime = row["_id"]
    minutesOfDay = dateTime.hour * 60 + dateTime.minute
    if minutesOfDay in day:
      valueList = day[minutesOfDay]
    else:
      valueList = []
      day[minutesOfDay] = valueList
    valueList.append(row[valueName])
  dayMedians = {}
  totalRelativeDeviation = 0
  cnt = 0
  max = 0
  for minute, valueList in day.items():
    if len(data) == 0:
      continue
    dayMedians[minute] = median(valueList)
    perctDeviation = medianDeviation(valueList)
    totalRelativeDeviation += perctDeviation
    if perctDeviation > 0.10:
      print(str(perctDeviation) + " at time: " + str(minute))
      max = perctDeviation
    cnt += 1
  avgRelativeDeviation = totalRelativeDeviation / cnt
  print("relative deviation: " + str(avgRelativeDeviation * 100))
  return dayMedians


def medianDeviation(data):
  data = sorted(data)
  data = data[:int(len(data)/4)]
  med = median(data)
  mads = []
  if med == 0:
    return 1
  for b in data:
    devPerc = b / med
    mads.append((1 - devPerc))
  return max(mads)


  # a = [15,10,10,2]
  # print(medianDeviation(a))

