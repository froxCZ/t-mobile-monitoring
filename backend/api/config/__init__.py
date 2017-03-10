import datetime

from flask import Blueprint, jsonify
from flask import request

from api import util
from config import config
from data_query import DiscoverQuery
from mongo import mongo

lobsConfig = Blueprint('lobs', __name__)


@lobsConfig.route('/', methods=["GET"])
def lobsList():
  fullConfig = request.args.get('fullConfig')
  if fullConfig is None:
    fullConfig = False
  lobConfigs = config.getLobsConfig()
  if fullConfig == False:
    for lob in lobConfigs["lobs"].values():
      del lob["flows"]
      del lob["inputs"]
      del lob["forwards"]

  return jsonify(lobConfigs)

@lobsConfig.route('/discover', methods=["POST"])
def discover():
  """
  find new inputs and forwards for the past 14 days and adds them to the config
  :return:
  """
  now = datetime.datetime.now()
  fromDate = now - datetime.timedelta(days=14)
  newLobNeids = DiscoverQuery(fromDate, now).execute()
  setObj = {}
  addedCnt = 0
  for lobName, newConfig in newLobNeids.items():
    for neidName, neid in newConfig["neids"].items():
      setObj["lobs." + lobName + ".neids." + neidName] = neid
      addedCnt += 1
    for forwardName, forward in newConfig["forwards"].items():
      setObj["lobs." + lobName + ".forwards." + forwardName] = forward
      addedCnt += 1
  res = mongo.config().update_many({"_id": "lobs"}, {"$set": setObj})
  return jsonify({"added": res.modified_count * addedCnt})

@lobsConfig.route('/<string:lobName>', methods=["GET"])
def getLobConfig(lobName):
  return jsonify(config.getLobConfig(lobName))


@lobsConfig.route('/<string:lobName>/flow/<string:flowName>', methods=["PUT"])
def putLobFlowOptions(lobName, flowName):
  body = request.get_json()
  from config import config
  flow = config.getLobConfig(lobName)["flows"][flowName]
  config.configColl.update_one({"_id": "lobs"}, {"$set": {"lobs." + flow["dataPath"]: body}})
  return jsonify(config.getLobConfig(lobName)["flows"][flowName]["options"])


@lobsConfig.route('/<string:lobName>/options', methods=["PUT"])
def putLobOptions(lobName):
  from config import config
  body = request.get_json()
  optionsPath = "lobs." + lobName + ".options"
  config.configColl.update_one({"_id": "lobs"}, {"$set": {optionsPath: body}})
  return jsonify(config.getLobConfig(lobName)["options"])


@lobsConfig.route('/<string:lobName>', methods=["POST"])
def updateLob(lobName):
  setObj = {}
  unsetObj = {}
  body = request.get_json()
  from config.config import configColl
  for key, value in body.items():
    if value == None:
      unsetObj["lobs." + lobName + "." + key] = value
    else:
      setObj["lobs." + lobName + "." + key] = value
  updateObj = {}
  if (len(setObj)):
    updateObj["$set"] = setObj
  if (len(unsetObj)):
    updateObj["$unset"] = unsetObj
  configColl.update_one({"_id": "lobs"}, updateObj)
  return jsonify({})


@lobsConfig.route('/<string:lobName>/outage', methods=["POST"])
def saveOutage(lobName):
  from mongo import mongo
  outagesColl = mongo.outages()
  json = request.get_json()
  fromDate = util.jsStringToDate(json["from"])  # might need timezone?
  toDate = util.jsStringToDate(json["to"])  # might need timezone?
  # todo create record for each date in range!
  date = util.resetDateTimeMidnight(fromDate)

  dayDelta = datetime.timedelta(days=1)
  while date != util.resetDateTimeMidnight(toDate):
    outagesColl.update_one({"_id": date},
                           {"$set": {"lobs." + lobName: {"from": fromDate, "to": date + dayDelta}}}, upsert=True)
    date = date + dayDelta
    fromDate = date

  res = outagesColl.update_one({"_id": date}, {"$set": {"lobs." + lobName: {"from": fromDate, "to": toDate}}},
                               upsert=True)

  return jsonify({})


@lobsConfig.route('/<string:lobName>/outages', methods=["GET"])
def getOutages(lobName):
  fromDate = util.jsStringToDate(request.args.get('from'))
  toDate = util.jsStringToDate(request.args.get('to'))
  from outage import OutageQuery
  outages = OutageQuery(lobName).getOutages(fromDate, toDate)
  return jsonify(outages)
