import datetime

import dateutil.parser


def jsStringToDate(string, hoursOffset=0):
  return dateutil.parser.parse(string) \
         - datetime.timedelta(hours=hoursOffset)  # hack while dates in mongo are at 00:00Z instead of 00:00CET


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
  return dateTime.replace(minute=0, second=0, microsecond=0)
