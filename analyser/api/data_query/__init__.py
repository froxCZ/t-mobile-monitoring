from flask import Blueprint, jsonify
from flask import request

import api.util as util
import smooth
from api.data_query.DateRangeGroupQuery import DateRangeGroupQuery
from api.data_query.DatesQuery import DatesQuery
from api.data_query.DayAverageQuery import DayAverageQuery

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



def smoothData(data, granularity, validMetricName):
  dataList = []
  for row in data:
    dataList.append(row[validMetricName])
  smoothedData = smooth.smoothData(granularity, dataList)
  for index, elem in enumerate(smoothedData):
    data[index]["smoothed"] = elem
