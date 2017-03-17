from flask import Blueprint, jsonify
from flask import request

from common.api import StatusException
from mediation import MediationConfig
from mediation.MediationConfig import MEDIATION_DOCUMENT
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
def countryGET(country):
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
def lobGET(country, lobName):
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
def flowGET(country, lobName, flowName):
  flow = MediationConfig.getLobWithCountry(country, lobName)["flows"][flowName]
  if shouldIncludeStatus():
    status = FlowStatusManager().getLobDetailWithCountry(country, lobName)[flowName]
    flow["status"] = status
  return jsonify(flow)


@flowsApi.route('/countries', methods=["GET"])
def countriesOverviewGET():
  countries = FlowStatusManager().getCountriesOverview()
  return jsonify(countries)


@flowsApi.route('/<string:country>/<string:lobName>/<string:flowName>/enable', methods=["PUT"])
def flowEnablePUT(country, lobName, flowName):
  body = request.get_json()
  enable = body["enable"]
  flow = MediationConfig.getLobWithCountry(country, lobName)["flows"][flowName]
  MediationConfig.configColl.update_one(
    MEDIATION_DOCUMENT, {"$set": {"lobs." + flow["dataPath"] + ".enabled": enable}})
  return jsonify(MediationConfig.getLob(lobName)["flows"][flowName]["options"])


@flowsApi.route('/<string:country>/<string:lobName>/options', methods=["PUT"])
def lobOptionsPUT(country, lobName):
  body = request.get_json()
  optionsPath = "lobs." + country + "." + lobName + ".options"
  MediationConfig.configColl.update_one(MEDIATION_DOCUMENT, {"$set": {optionsPath: body}})
  return jsonify(MediationConfig.getLob(lobName)["options"])


@flowsApi.route('/<string:country>/<string:lobName>/<string:flowName>/options', methods=["GET"])
def flowOptionsGET(country, lobName, flowName):
  lobConfig = MediationConfig.getLobWithCountry(country, lobName)
  flowConfig = lobConfig["flows"][flowName]
  return jsonify(flowConfig)


@flowsApi.route('/<string:country>/<string:lobName>/<string:flowName>/options', methods=["PUT"])
def flowOptionsPUT(country, lobName, flowName):
  body = request.get_json()
  flow = MediationConfig.getLobWithCountry(country, lobName)["flows"][flowName]
  res = MediationConfig.configColl.update_one(MEDIATION_DOCUMENT, {"$set": {"lobs." + flow["dataPath"]: body}})
  return jsonify(MediationConfig.getLobWithCountry(country, lobName)["flows"][flowName]["options"])


@flowsApi.route('/', methods=["POST"])
def addLobPOST():
  """put under /lobs"""
  addLobRequest = request.get_json()
  country = addLobRequest["country"]
  lobName = addLobRequest["lobName"]
  if MediationConfig.getLob(lobName) is not None:
    raise StatusException("Lob already exists", 400)
  MediationConfig.addLob(country, lobName)
  return countryGET(country)
