from flask import Blueprint, jsonify
from flask import request

import api.util as util
import smooth
from api.data_query.MongoQueryExecutor import MongoQueryExecutor

data_query = Blueprint('data_query', __name__)


@data_query.route('/', methods=["POST"])
def dataQuery():
  searchParam = request.get_json()
  searchParam["from"] = util.jsStringToDate(searchParam["from"])
  searchParam["to"] = util.jsStringToDate(searchParam["to"])
  response = {}
  mongoQuery = MongoQueryExecutor(searchParam)
  data, metricsList = mongoQuery.execute()
  metrics = {}
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


def smoothData(data, granularity, validMetricName):
  dataList = []
  for row in data:
    dataList.append(row[validMetricName])
  smoothedData = smooth.smoothData(granularity, dataList)
  for index, elem in enumerate(smoothedData):
    data[index]["smoothed"] = elem
