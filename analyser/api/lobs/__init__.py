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


@lobs.route('/config/<string:lobName>/outage', methods=["POST"])
def saveOutage(lobName):
  from mongo import mongo
  outagesColl = mongo.db()["outages"]
  date = util.jsStringToDate(request.get_json()["date"])  # might need timezone?
  date = util.resetDateTimeMidnight(date)
  outagesColl.update_one({"_id": date}, {"$set": {"lobs." + lobName: 1}}, upsert=True)
  return jsonify({})


@lobs.route('/config/<string:lobName>/outages', methods=["GET"])
def getOutages(lobName):
  fromDate = util.jsStringToDate(request.args.get('from'))
  toDate = util.jsStringToDate(request.args.get('to'))
  from outage import OutageQuery
  outages = OutageQuery(lobName).getOutages(fromDate, toDate)
  return jsonify(outages)
