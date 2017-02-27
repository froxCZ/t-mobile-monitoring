import datetime

from flask import Blueprint, jsonify
from flask import request

from api import util
from config import config

lobs = Blueprint('lobs', __name__)


@lobs.route('/configs', methods=["GET"])
def lobsConfig():
  return jsonify(config.getLobsConfig())


@lobs.route('/config/<string:lobName>', methods=["POST"])
def updateLob(lobName):
  setObj = {}
  from config.config import configColl
  for key, value in request.get_json().items():
    setObj["lobs." + lobName + "." + key] = value
  configColl.update_one({"_id": "lobs"}, {"$set": setObj})
  return jsonify({})


@lobs.route('/<string:lobName>/outage', methods=["POST"])
def saveOutage(lobName):
  from mongo import mongo
  outagesColl = mongo.db()["outages"]
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

  res = outagesColl.update_one({"_id": date}, {"$set": {"lobs." + lobName: {"from": fromDate, "to": toDate}}}, upsert=True)

  return jsonify({})


@lobs.route('/<string:lobName>/outages', methods=["GET"])
def getOutages(lobName):
  fromDate = util.jsStringToDate(request.args.get('from'), hoursOffset=10)
  toDate = util.jsStringToDate(request.args.get('to'), hoursOffset=10)
  from outage import OutageQuery
  outages = OutageQuery(lobName).getOutages(fromDate, toDate)
  return jsonify(outages)
