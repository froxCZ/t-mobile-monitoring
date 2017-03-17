from flask import Blueprint, jsonify
from flask import request

from mediation import MediationConfig

lobsConfig = Blueprint('lobs', __name__)

@lobsConfig.route('/countries', methods=["GET"])
def coutriesGET():
  return jsonify(MediationConfig.getCountries())


@lobsConfig.route('/countries', methods=["PUT"])
def coutriesPUT():
  body = request.get_json()
  MediationConfig.configColl.update_one({"_id": "lobs"}, {"$set": {"countries": body}})
  return jsonify(MediationConfig.getCountries())

# @lobsConfig.route('/lobs/<string:countryName>', methods=["GET"])
# def lobsListGET(countryName):
#   lobConfigs = MediationConfig.getLobs(countryName)
#   for lob in lobConfigs.values():
#     del lob["flows"]
#     del lob["inputs"]
#     del lob["forwards"]
#   return jsonify(lobConfigs)

#
#
# @lobsConfig.route('/', methods=["POST"])
# def addLob():
#   """put under /lobs"""
#   addLobRequest = request.get_json()
#   country = addLobRequest["country"]
#   lobName = addLobRequest["lobName"]
#   if MediationConfig.getLob(lobName) is not None:
#     raise StatusException("Lob already exists", 400)
#   MediationConfig.addLob(country, lobName)
#   return lobsListGET(country)
#
#
# @lobsConfig.route('/<string:lobName>', methods=["DELETE"])
# def deleteLob(lobName):
#   lob = MediationConfig.getLob(lobName)
#   if lob is not None:
#     MediationConfig.deleteLob(lob)
#   else:
#     raise StatusException("lob does not exists", 400)
#   return jsonify(MediationConfig.getLobs(lob["country"]))
#
#
# @lobsConfig.route('/<string:lobName>/flow', methods=["POST"])
# def addFlow(lobName):
#   lob = MediationConfig.getLob(lobName)
#   addFlowRequest = request.get_json()
#   country = lob["country"]
#   flowName = addFlowRequest["flowName"]
#   if flowName in lob["flows"]:
#     raise StatusException("Flow already exists", 400)
#   if ":" in flowName:
#     type = "forwards"
#   else:
#     type = "inputs"
#   flow = {"country": country, "lobName": lobName, "type": type, "name": flowName}
#   MediationConfig.addFlow(flow)
#   return getLobConfig(lobName)
#
#
# @lobsConfig.route('/<string:lobName>/flow/<string:flowName>', methods=["DELETE"])
# def deleteFlow(lobName, flowName):
#   lob = MediationConfig.getLob(lobName)
#   if flowName in lob["flows"]:
#     MediationConfig.deleteFlow(lob["flows"][flowName])
#   return getLobConfig(lobName)
#
#
# @lobsConfig.route('/<string:lobName>', methods=["GET"])
# def getLobConfig(lobName):
#   lobConfig = MediationConfig.getLob(lobName)
#   del lobConfig["flows"]
#   return jsonify(lobConfig)
#
#
# @lobsConfig.route('/<string:lobName>/flow/<string:flowName>', methods=["GET"])
# def getFlowConfig(lobName, flowName):
#   lobConfig = MediationConfig.getLob(lobName)
#   flowConfig = lobConfig["flows"][flowName]
#   return jsonify(flowConfig)
#
#
# @lobsConfig.route('/<string:lobName>/flow/<string:flowName>/options', methods=["PUT"])
# def putLobFlowOptions(lobName, flowName):
#   body = request.get_json()
#   flow = MediationConfig.getLob(lobName)["flows"][flowName]
#   res = MediationConfig.configColl.update_one({"_id": "lobs"}, {"$set": {"lobs." + flow["dataPath"]: body}})
#   return jsonify(MediationConfig.getLob(lobName)["flows"][flowName]["options"])
#
#
# @lobsConfig.route('/<string:lobName>/options', methods=["PUT"])
# def putLobOptions(lobName):
#   body = request.get_json()
#   optionsPath = "lobs." + lobName + ".options"
#   MediationConfig.configColl.update_one({"_id": "lobs"}, {"$set": {optionsPath: body}})
#   return jsonify(MediationConfig.getLob(lobName)["options"])
#
#
# @lobsConfig.route('/<string:lobName>/flow/<string:flowName>/enable', methods=["PUT"])
# def lobFlowActivation(lobName, flowName):
#   body = request.get_json()
#   enable = body["enable"]
#   flow = MediationConfig.getLob(lobName)["flows"][flowName]
#   MediationConfig.configColl.update_one({"_id": "lobs"}, {"$set": {"lobs." + flow["dataPath"] + ".enabled": enable}})
#   return jsonify(MediationConfig.getLob(lobName)["flows"][flowName]["options"])
#
#
# @lobsConfig.route('/<string:lobName>', methods=["POST"])
# def updateLob(lobName):
#   setObj = {}
#   unsetObj = {}
#   body = request.get_json()
#   for key, value in body.items():
#     if value == None:
#       unsetObj["lobs." + lobName + "." + key] = value
#     else:
#       setObj["lobs." + lobName + "." + key] = value
#   updateObj = {}
#   if (len(setObj)):
#     updateObj["$set"] = setObj
#   if (len(unsetObj)):
#     updateObj["$unset"] = unsetObj
#   MediationConfig.configColl.update_one({"_id": "lobs"}, updateObj)
#   return jsonify({})
#
#
# @lobsConfig.route('/<string:lobName>/outage', methods=["POST"])
# def saveOutage(lobName):
#   from mongo import mongo
#   outagesColl = mongo.outages()
#   json = request.get_json()
#   fromDate = util.jsStringToDate(json["from"])  # might need timezone?
#   toDate = util.jsStringToDate(json["to"])  # might need timezone?
#   # todo create record for each date in range!
#   date = util.resetDateTimeMidnight(fromDate)
#
#   dayDelta = datetime.timedelta(days=1)
#   while date != util.resetDateTimeMidnight(toDate):
#     outagesColl.update_one({"_id": date},
#                            {"$set": {"lobs." + lobName: {"from": fromDate, "to": date + dayDelta}}}, upsert=True)
#     date = date + dayDelta
#     fromDate = date
#
#   res = outagesColl.update_one({"_id": date}, {"$set": {"lobs." + lobName: {"from": fromDate, "to": toDate}}},
#                                upsert=True)
#
#   return jsonify({})
#
#
# @lobsConfig.route('/<string:lobName>/outages', methods=["GET"])
# def getOutages(lobName):
#   fromDate = util.jsStringToDate(request.args.get('from'))
#   toDate = util.jsStringToDate(request.args.get('to'))
#   from past.outage import OutageQuery
#   outages = OutageQuery(lobName).getOutages(fromDate, toDate)
#   return jsonify(outages)

#
# @lobsConfig.route('/discover', methods=["POST"])
# def discover():
#   """
#   find new inputs and forwards for the past 14 days and adds them to the config
#   :return:
#   """
#   now = datetime.datetime.now()
#   fromDate = now - datetime.timedelta(days=14)
#   newLobNeids = DiscoverQuery(fromDate, now).execute()
#   setObj = {}
#   addedCnt = 0
#   for lobName, newConfig in newLobNeids.items():
#     for neidName, neid in newConfig["neids"].items():
#       setObj["lobs." + lobName + ".neids." + neidName] = neid
#       addedCnt += 1
#     for forwardName, forward in newConfig["forwards"].items():
#       setObj["lobs." + lobName + ".forwards." + forwardName] = forward
#       addedCnt += 1
#   res = mongo.config().update_many({"_id": "lobs"}, {"$set": setObj})
#   return jsonify({"added": res.modified_count * addedCnt})
