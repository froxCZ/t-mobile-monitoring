from flask import Blueprint, jsonify
from flask import request

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
