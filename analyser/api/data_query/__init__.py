import datetime

from flask import Blueprint, jsonify
from flask import request

import api.util as util
import smooth
from data_query import DateRangeGroupQuery
from data_query import SimilarDaysMedianQuery

data_query = Blueprint('data_query', __name__)


@data_query.route('/', methods=["POST"])
def dataQuery():
  searchParam = request.get_json()
  fromDate = util.jsStringToDate(searchParam["from"], hoursOffset=10).replace(hour=0, minute=0, second=0)
  toDate = util.jsStringToDate(searchParam["to"], hoursOffset=10).replace(hour=0, minute=0, second=0)
  lobNames = searchParam["aggregation"]["sum"]
  response = {}
  mongoQuery = DateRangeGroupQuery(fromDate, toDate, lobNames, searchParam["granularity"])
  data = mongoQuery.execute()
  metrics = {}
  metricsList = mongoQuery.metrics
  metadata = mongoQuery.metadata
  date = fromDate
  dayDelta = datetime.timedelta(days=1)
  medianList = []
  while date < toDate:
    l = minuteDictToDateDict(date,
                             SimilarDaysMedianQuery(lobNames[0], date, granularity=metadata["granularity"])
                             .execute(),
                             "median")
    for d, v in l.items():
      medianList.append(v)
    date += dayDelta
  if len(medianList) > 0:
    data = merge2DateLists(medianList, ["median"], data, metricsList)
    metricsList.append("median")

  if (len(data) > 10):
    validMetricName = metricsList[0]
    smoothData(data, metadata["granularity"], validMetricName)
    metricsList.append("smoothed")

  for metric in metricsList:
    maxx = 0
    minn = float('inf')
    for row in data:
      if metric in row:
        maxx = max(row[metric], maxx)
        minn = min(row[metric], minn)
    metrics[metric] = {"max": maxx, "min": minn}
  response["data"] = data
  response["metadata"] = {**{"metrics": metrics}, **metadata}
  return jsonify(response)


@data_query.route('/best_correlations', methods=["GET"])
def bestCorrelations():
  lobName = request.args.get('lobName')
  granularity = int(request.args.get('granularity'))
  from data_util import correlation
  bestCorrelations = correlation.getBestCorrelations(lobName, granularity=granularity)
  return jsonify(bestCorrelations)


@data_query.route('/averages', methods=["GET"])
def getDayAverages():
  lobName = request.args.get('lobName')
  from data_util.moving_average import DayAverageExecutor
  return jsonify(DayAverageExecutor.getDayAverages(lobName))


@data_query.route('/day_medians', methods=["GET"])
def getDayMedians():
  lobName = request.args.get('lobName')
  requestDate = request.args.get('date')
  if requestDate is None:
    requestDate = datetime.datetime.now()
  else:
    requestDate = util.jsStringToDate(requestDate)
  requestDate = util.resetDateTimeMidnight(requestDate)
  medianQuery = SimilarDaysMedianQuery(lobName, requestDate)
  medians = medianQuery.execute()
  dataList = dateDictToList(minuteDictToDateDict(requestDate, medians, "median"))
  response = {}
  response["data"] = dataList
  response["granularity"] = medianQuery.metadata["granularity"]
  response["metrics"] = ["median"]
  return jsonify(response)


def minuteDictToDateDict(baseDate, dict, valueName):
  dateDict = {}
  baseDate = baseDate.replace(tzinfo=None)
  for minute, x in dict.items():
    id = baseDate + datetime.timedelta(minutes=minute)
    dateDict[id] = {"_id": id, valueName: x}
  return dateDict


def dateDictToList(dateDict):
  sortedKeys = sorted(dateDict.keys())
  sortedList = []
  for key in sortedKeys:
    sortedList.append(dateDict[key])
  return sortedList


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


def listToDateDict(l):
  dateDict = {}
  for i in l:
    dateDict[i["_id"]] = i
  return dateDict


def smoothData(data, granularity, validMetricName):
  dataList = []
  for row in data:
    dataList.append(row[validMetricName])
  smoothedData = smooth.smoothData(granularity, dataList)
  for index, elem in enumerate(smoothedData):
    data[index]["smoothed"] = elem
