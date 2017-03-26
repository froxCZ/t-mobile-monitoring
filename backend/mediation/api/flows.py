from flask import Blueprint, jsonify
from flask import request

from common.api import StatusException
from mediation import MediationConfig
from mediation.MediationConfig import MEDIATION_DOCUMENT
from mediation.flow_analyzer import FlowStatusManager

flowsAPI = Blueprint('flows', __name__)

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


@flowsAPI.route('/<string:country>', methods=["GET"])
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


@flowsAPI.route('/<string:country>/enable', methods=["GET"])
def getEnabledCountry(country):
  return jsonify({"enabled": MediationConfig.getCountryByName(country)["enabled"]})


@flowsAPI.route('/<string:country>/enable', methods=["PUT"])
def enableCountry(country):
  body = request.get_json()
  enable = body["enable"]
  MediationConfig.configColl.update_one(
    MEDIATION_DOCUMENT, {"$set": {"countries." + country + ".enabled": enable}})
  return getEnabledCountry(country)


@flowsAPI.route('/<string:country>/<string:lobName>', methods=["GET"])
def getLob(country, lobName):
  res = MediationConfig.getLobWithCountry(country, lobName)
  if shouldIncludeStatus():
    status = FlowStatusManager().getLobDetailWithCountry(country, lobName)
    for k, v in status.items():
      type = res["flows"][k]["type"]
      res[type][k]["status"] = v
  del res["flows"]
  return jsonify(res)


@flowsAPI.route(
  '/<string:country>/<string:lobName>/<string:flowName>', methods=["GET"])
def flowGET(country, lobName, flowName):
  flow = MediationConfig.getLobWithCountry(country, lobName)["flows"][flowName]
  if shouldIncludeStatus():
    status = FlowStatusManager().getLobDetailWithCountry(country, lobName)[flowName]
    flow["status"] = status
  return jsonify(flow)


@flowsAPI.route('', methods=["GET"])
def getCountriesOverview():
  countries = FlowStatusManager().getCountriesOverview()
  return jsonify(countries)


@flowsAPI.route('/<string:country>/<string:lobName>/<string:flowName>/enable', methods=["PUT"])
def enableFlow(country, lobName, flowName):
  body = request.get_json()
  enable = body["enable"]
  flow = MediationConfig.getLobWithCountry(country, lobName)["flows"][flowName]
  MediationConfig.configColl.update_one(
    MEDIATION_DOCUMENT, {"$set": {"lobs." + flow["dataPath"] + ".enabled": enable}})
  return jsonify(MediationConfig.getLobWithCountry(country, lobName)["flows"][flowName]["options"])


@flowsAPI.route('/<string:country>/<string:lobName>/options', methods=["PUT"])
def lobOptionsPUT(country, lobName):
  body = request.get_json()
  optionsPath = "lobs." + country + "." + lobName + ".options"
  MediationConfig.configColl.update_one(MEDIATION_DOCUMENT, {"$set": {optionsPath: body}})
  return jsonify(MediationConfig.getLobWithCountry(country, lobName)["options"])


@flowsAPI.route('/<string:country>/<string:lobName>/enable', methods=["PUT"])
def enableLob(country, lobName):
  enable = request.get_json()["enable"]
  optionsPath = "lobs." + country + "." + lobName + ".options.enabled"
  MediationConfig.configColl.update_one(MEDIATION_DOCUMENT, {"$set": {optionsPath: enable}})
  return jsonify(MediationConfig.getLobWithCountry(country, lobName)["options"])


@flowsAPI.route('/<string:country>/<string:lobName>/<string:flowName>/options', methods=["GET"])
def getFlowOptions(country, lobName, flowName):
  lobConfig = MediationConfig.getLobWithCountry(country, lobName)
  flowConfig = lobConfig["flows"][flowName]
  return jsonify(flowConfig)


@flowsAPI.route('/<string:country>/<string:lobName>/<string:flowName>/options', methods=["PUT"])
def putFlowOptions(country, lobName, flowName):
  body = request.get_json()
  flow = MediationConfig.getLobWithCountry(country, lobName)["flows"][flowName]
  res = MediationConfig.configColl.update_one(MEDIATION_DOCUMENT, {"$set": {"lobs." + flow["dataPath"]: body}})
  return jsonify(MediationConfig.getLobWithCountry(country, lobName)["flows"][flowName]["options"])


@flowsAPI.route('/', methods=["POST"])
def addLob():
  """put under /lobs"""
  addLobRequest = request.get_json()
  country = addLobRequest["country"]
  lobName = addLobRequest["lobName"]
  if MediationConfig.getLobWithCountry(country, lobName) is not None:
    raise StatusException("Lob already exists", 400)
  MediationConfig.addLob(country, lobName)
  return getCountry(country)


@flowsAPI.route('/<string:country>/<string:lobName>', methods=["DELETE"])
def deleteLob(country, lobName):
  lob = MediationConfig.getLobWithCountry(country, lobName)
  if lob is not None:
    MediationConfig.deleteLob(lob)
  else:
    raise StatusException("lob does not exists", 400)
  return getCountry(country)


@flowsAPI.route('/<string:country>/<string:lobName>', methods=["POST"])
def addFlow(country, lobName):
  lob = MediationConfig.getLobWithCountry(country, lobName)
  addFlowRequest = request.get_json()
  name = addFlowRequest["name"]
  type = addFlowRequest["type"]
  if name in lob["flows"]:
    raise StatusException("Flow already exists", 400)
  flow = {"country": country, "lobName": lobName, "type": type, "name": name}
  MediationConfig.addFlow(flow)
  return getLob(country, lobName)


@flowsAPI.route('/<string:country>/<string:lobName>/<string:flowName>', methods=["DELETE"])
def deleteFlow(country, lobName, flowName):
  lob = MediationConfig.getLobWithCountry(country, lobName)
  if flowName in lob["flows"]:
    MediationConfig.deleteFlow(lob["flows"][flowName])
  return getLob(country, lobName)
