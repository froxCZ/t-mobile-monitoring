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
