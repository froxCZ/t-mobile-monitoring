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
  mongoQuery = data_query.DateRangeGroupQuery(fromDate, toDate, flows, granularity=granularity)
  data = mongoQuery.execute()
  metrics = {}
  metricsList = mongoQuery.metrics
  metadata = mongoQuery.metadata
  if len(flows) == 1:
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
  #
  # if (len(data) > 10):
  #   validMetricName = metricsList[0]
  #   smoothData(data, metadata["granularity"], validMetricName)
  #   metricsList.append(validMetricName + "_smoothed")

  for metric in metricsList:
    # maxx = 0
    # minn = float('inf')
    # for row in data:
    #   if metric in row:
    #     maxx = max(row[metric], maxx)
    #     minn = min(row[metric], minn)
    metrics[metric] = {}
  response["data"] = data
  response["metadata"] = {**{"metrics": metrics}, **metadata}
  return jsonify(response)


@dataAPI.route('/insert', methods=["POST"])
def insertData():
  f = request.files['file']
  stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
  insertor = DataInsertor(stream)
  insertor.run()
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
  dataList = data_query.dateDictToList(data_query.minuteDictToDateDict(requestDate, medians, "median"))
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
