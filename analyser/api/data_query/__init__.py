import datetime

from flask import Blueprint, jsonify
from flask import request

import api.util as util
import smooth
from data_query import DateRangeGroupQuery
data_query = Blueprint('data_query', __name__)


@data_query.route('/', methods=["POST"])
def dataQuery():
  searchParam = request.get_json()
  fromDate = util.jsStringToDate(searchParam["from"], hoursOffset=10)
  toDate = util.jsStringToDate(searchParam["to"], hoursOffset=10)
  lobNames = searchParam["aggregation"]["sum"]
  response = {}
  mongoQuery = DateRangeGroupQuery(fromDate, toDate, lobNames, searchParam["granularity"])
  data, metricsList = mongoQuery.execute()
  metrics = {}
  print(metricsList)
  metadata = mongoQuery.metadata

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
  from data_query import SimilarDaysMedianQuery
  lobName = request.args.get('lobName')
  requestDate = request.args.get('date')
  if requestDate is None:
    requestDate = datetime.datetime.now()
  else:
    requestDate = util.jsStringToDate(requestDate)
  requestDate = util.resetDateTimeMidnight(requestDate)
  medianQuery = SimilarDaysMedianQuery(lobName, requestDate)
  medians = medianQuery.execute()
  dataList = []
  for minute, median in medians.items():
    dataList.append({"_id": requestDate + datetime.timedelta(minutes=minute), "median": median})
  dataList = sorted(dataList, key=lambda x: x["_id"])
  response = {}
  response["data"] = dataList
  response["granularity"] = medianQuery.metadata["granularity"]
  response["metrics"] = ["median"]
  return jsonify(response)


def smoothData(data, granularity, validMetricName):
  dataList = []
  for row in data:
    dataList.append(row[validMetricName])
  smoothedData = smooth.smoothData(granularity, dataList)
  for index, elem in enumerate(smoothedData):
    data[index]["smoothed"] = elem
