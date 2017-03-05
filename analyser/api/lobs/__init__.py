import datetime

from flask import Blueprint, jsonify
from flask import request

from api import util
from config import config
from data_query import DiscoverQuery
from mongo import mongo

lobs = Blueprint('lobs', __name__)


@lobs.route('/', methods=["GET"])
def lobsList():
  return jsonify(config.getLobsConfig())


@lobs.route('/discover', methods=["POST"])
def discover():
  """
  find new neids and forwards for the past 14 days and adds them to the config
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


@lobs.route('/configs', methods=["GET"])
def lobsConfig():
  return jsonify(config.getLobsConfig())


@lobs.route('/<string:lobName>', methods=["GET"])
def getLobConfig(lobName):
  return jsonify(config.getLobConfig(lobName))


@lobs.route('/<string:lobName>/options', methods=["PUT"])
def putOptions(lobName):
  body = request.get_json()
  from config.config import configColl
  fullFlowName = lobName
  flowType = request.args.get('flowType')
  if flowType is not None:
    flowName = request.args.get('flowName')
    if flowName is None:
      raise Exception("flow name not specified")
    fullFlowName += "." + flowType + "." + flowName
  optionsPath = "lobs." + fullFlowName + ".options"
  configColl.update_one({"_id": "lobs"}, {"$set": {optionsPath: body}})
  return jsonify(config.getOptionsByFullFlowName(fullFlowName))


@lobs.route('/<string:lobName>', methods=["POST"])
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


@lobs.route('/<string:lobName>/outage', methods=["POST"])
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


@lobs.route('/<string:lobName>/outages', methods=["GET"])
def getOutages(lobName):
  fromDate = util.jsStringToDate(request.args.get('from'))
  toDate = util.jsStringToDate(request.args.get('to'))
  from outage import OutageQuery
  outages = OutageQuery(lobName).getOutages(fromDate, toDate)
  return jsonify(outages)
