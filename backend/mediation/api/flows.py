from flask import Blueprint, jsonify
from flask import request

from mediation import MediationConfig
from mediation.flow_analyzer import FlowStatusManager

flowsApi = Blueprint('flows', __name__)

DEFAULT_EXPAND = {"config": True, "status": True}


def shouldIncludeStatus():
  includeStatus = request.args.get('includeStatus')
  if includeStatus == None:
    return True
  else:
    return includeStatus


def addStatus(res, status):
  for k, v in status.items():
    res[k]["status"] = v


@flowsApi.route('/<string:country>', methods=["GET"])
def getCountry(country):
  res = MediationConfig.getLobs(country)
  for lob in res.values():
    del lob["flows"]
    del lob["inputs"]
    del lob["forwards"]
  if shouldIncludeStatus():
    status = FlowStatusManager().getLobsOverview(country)
    addStatus(res, status)
  return jsonify(res)


@flowsApi.route('/<string:country>/<string:lobName>', methods=["GET"])
def getLob(country, lobName):
  res = MediationConfig.getLobWithCountry(country, lobName)
  if shouldIncludeStatus():
    status = FlowStatusManager().getLobDetailWithCountry(country, lobName)
    for k, v in status.items():
      type = res["flows"][k]["type"]
      res[type][k]["status"] = v
  del res["flows"]
  return jsonify(res)


@flowsApi.route(
  '/<string:country>/<string:lobName>/<string:flowName>', methods=["GET"])
def getFlow(country, lobName, flowName):
  flow = MediationConfig.getLobWithCountry(country, lobName)["flows"][flowName]
  if shouldIncludeStatus():
    status = FlowStatusManager().getLobDetailWithCountry(country, lobName)[flowName]
    flow["status"] = status
  return jsonify(flow)


@flowsApi.route('/countries', methods=["GET"])
def getCountriesOverview():
  countries = FlowStatusManager().getCountriesOverview()
  return jsonify(countries)
