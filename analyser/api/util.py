import datetime

import dateutil.parser


def jsStringToDate(string):
  return dateutil.parser.parse(string) \
         - datetime.timedelta(hours=10)  # hack while dates in mongo are at 00:00Z instead of 00:00CET
def dateDataListToList(dateDataList,metricName):
  dataList = []
  for row in dateDataList:
    dataList.append(row[metricName])
  return dataList
