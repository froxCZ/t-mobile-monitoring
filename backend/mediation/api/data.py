import datetime
import io

from flask import Blueprint, jsonify
from flask import request

import util
from mediation import MediationConfig
from mediation import data_query
from mediation.data_receiver import DataInsertor

dataAPI = Blueprint('data_api', __name__)


@dataAPI.route('/query', methods=["POST"])
def dataQueryV2():
  """
Endpoint for getting traffic data.
POST body:
{
  "from":"01.02.2017",
  "to":"15.02.2017",
  "lob":{"country":"CZ","name":"ACI"},
  "neids":["GSM"],
  "forwards":[],
  "granularity":0
}

Response:
{
  "data": [
    {
      "GSM": 188385532,
      "_id": "2017-02-01T00:00:00+01:00",
      "dayAverage": 1162595297.6666667,
      "dayDifference": 1.023,
      "expected": 161627916,
      "status": "OK",
      "ticDifference": 1.166
    },
    ...
  ],
   "metadata": {
    "flowName": "GSM",
    "granularity": 480,
    "metrics": {
      "GSM": {
        "type": "traffic"
      },
      "dayAverage": {
        "type": "traffic"
      },
      "dayDifference": {
        "type": "difference"
      },
      "expected": {
        "type": "traffic"
      },
      "status": {
        "type": "other"
      },
      "ticDifference": {
        "type": "difference"
      }
    }
  }
"""
  searchParam = request.get_json()
  fromDate = util.stringToDate(searchParam["from"])
  toDate = util.stringToDate(searchParam["to"])
  lobRequest = searchParam["lob"]
  country = lobRequest["country"]
  lobName = lobRequest["name"]
  lobConfig = MediationConfig.getLobWithCountry(country, lobName)
  flows = []
  granularity = searchParam.get("granularity", 0)
  if "neids" in searchParam:
    for neid in searchParam["neids"]:
      if neid == "*":
        flows.append(createMergedFlowsObject(country, lobName, "inputs"))
        break
      flows.append(lobConfig["flows"][neid])
  if "forwards" in searchParam:
    for forward in searchParam["forwards"]:
      if forward == "*":
        flows.append(createMergedFlowsObject(country, lobName, "forwards"))
        break
      flows.append(lobConfig["flows"][forward])
  response = {}

  # Query the traffic data and add to metric list
  mongoQuery = data_query.DateRangeGroupQuery(fromDate, toDate, flows, granularity=granularity)
  data = mongoQuery.execute()
  metrics = {}
  metricsList = []
  flowName = mongoQuery.metrics[0]
  metricsList.append(flowName)

  metadata = mongoQuery.metadata
  if len(flows) == 1:
    # Run outage detection analysis
    metric = metricsList[0]
    flowLevelQuery = data_query.FlowLevelDateRangeQuery(fromDate, toDate, flows, metadata["granularity"], data)
    flowLevelData = flowLevelQuery.execute()
    data = util.merge2DateLists(flowLevelData, None, data, None)
    metricsList.extend(flowLevelQuery.metrics)
    outageQuery = data_query.OutageDateRangeQuery(fromDate, toDate, flows[0], metadata["granularity"])
    outageQuery.setPrecomputedData(data, metric)
    outageList = outageQuery.execute()
    data = util.merge2DateLists(outageList, [outageQuery.metric], data, None)
    metricsList.append(outageQuery.metric)

  # Create metadata infor
  for metric in metricsList:
    if metric == flowName or metric == "dayAverage" or metric == "expected":
      type = "traffic"
    elif "Difference" in metric:
      type = "difference"
    else:
      type = "other"
    metrics[metric] = {"type": type}
  response["data"] = data
  response["metadata"] = {**{"metrics": metrics}, **metadata, "flowName": flowName}
  return jsonify(response)


@dataAPI.route('/insert', methods=["POST"])
def insertData():
  f = request.files['file']
  stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
  insertor = DataInsertor()
  insertor.run(stream)
  return jsonify({})


@dataAPI.route('/best_correlations', methods=["GET"])
def bestCorrelations():
  lobName = request.args.get('lobName')
  granularity = int(request.args.get('granularity'))
  from past.data_util import correlation
  bestCorrelations = correlation.getBestCorrelations(lobName, granularity=granularity)
  return jsonify(bestCorrelations)


@dataAPI.route('/averages', methods=["GET"])
def getDayAverages():
  lobName = request.args.get('lobName')
  from past.data_util.moving_average import DayAverageExecutor
  return jsonify(DayAverageExecutor.getDayAverages(lobName))


@dataAPI.route('/day_medians', methods=["GET"])
def getDayMedians():
  """deprecated"""
  lobName = request.args.get('lobName')
  requestDate = request.args.get('date')
  if requestDate is None:
    requestDate = datetime.datetime.now()
  else:
    requestDate = util.jsStringToDate(requestDate)
  requestDate = util.resetDateTimeMidnight(requestDate)
  medianQuery = data_query.ExpectedTrafficQuery(lobName, requestDate)
  medians = medianQuery.execute()
  dataList = util.dateDictToList(data_query.minuteDictToDateDict(requestDate, medians, "median"))
  response = {}
  response["data"] = dataList
  response["granularity"] = medianQuery.metadata["granularity"]
  response["metrics"] = ["median"]
  return jsonify(response)

def createMergedFlowsObject(country, lobName, flowType):
  flow = {}
  flow["name"] = lobName + "-" + flowType
  flow["type"] = "all_forwards"
  flow["lobName"] = lobName
  flow["dataPath"] = country + "." + lobName + "." + flowType + ".sum"
  flow["gName"] = lobName + "_" + flowType
  flow["country"] = country
  flow["options"] = MediationConfig.getLobWithCountry(country, lobName)["options"]
  return flow
# def smoothData(data, granularity, validMetricName):
#   dataList = []
#   for row in data:
#     dataList.append(row[validMetricName])
#   smoothedData = smooth.smoothData(granularity, dataList)
#   for index, elem in enumerate(smoothedData):
#     data[index][validMetricName + "_smoothed"] = elem
