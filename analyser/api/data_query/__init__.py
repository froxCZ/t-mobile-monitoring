from flask import Blueprint, jsonify
from flask import request

import api.util as util
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
  for metric in metricsList:
    maxx = 0
    minn = float('inf')
    for row in data:
      if metric in row:
        maxx = max(row[metric], maxx)
        minn = min(row[metric], minn)
    print(maxx)
    metrics[metric] = {"max": maxx, "min": minn}
  response["data"] = data
  response["metadata"] = {**{"metrics": metrics}, **mongoQuery.metadata}
  return jsonify(response)



