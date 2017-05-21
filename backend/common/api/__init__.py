import hashlib

from flask import Blueprint, jsonify
from flask import request

from common import AppConfig
from common import SystemStatusManager
from common import UserManager
from common import util
from common.api.auth import require_root, require_user
from mediation.flow_analyzer import EventsManager

appAPI = Blueprint('common', __name__)

"""
General API endpoints
"""

class StatusException(Exception):
  def __init__(self, message, status):
    self.message = message
    self.status = status


def _invalidLoginResponse():
  resp = jsonify({"message": "Invalid username or password"})
  resp.status_code = 401
  return resp


def _hashPassword(password):
  return hashlib.sha512(password.encode('utf-8')).hexdigest()

@appAPI.route("/currentTime")
def currentTime():
  return jsonify({"currentTime": util.dateToTimeString(AppConfig.getCurrentTime())})

@appAPI.route('/status', methods=["GET"])
def getSystemStatus():
  return jsonify(SystemStatusManager.getStatus())

@appAPI.route('/login', methods=["POST"])
def login():
  body = request.get_json()
  if body == None:
    return _invalidLoginResponse()
  username = body["username"]
  password = body["password"]
  if username == None or password == None:
    return _invalidLoginResponse()
  passHash = _hashPassword(password)
  user = UserManager.getUserByName(username)
  if user == None or user["passwordHash"].lower() != passHash.lower():
    return _invalidLoginResponse()
  del user["passwordHash"]
  return jsonify(user)


@appAPI.route('/visitorLogin', methods=["POST"])
def visitorLogin():
  username = "visitor"
  password = "visitor"
  passHash = _hashPassword(password)
  user = UserManager.getUserByName(username)
  if user == None or user["passwordHash"].lower() != passHash.lower():
    return _invalidLoginResponse()
  del user["passwordHash"]
  return jsonify(user)


@appAPI.route('/users', methods=["GET"])
@require_root
def usersGET():
  return jsonify(UserManager.getUsers())


@appAPI.route('/users', methods=["POST"])
@require_root
def usersPOST():
  body = request.get_json()
  if "login" not in body or len(body["login"]) == 0:
    raise StatusException("Login is required", 400)
  UserManager.addUser(body)
  return jsonify(UserManager.getUsers())

@appAPI.route('/user/<string:login>', methods=["PUT"])
@require_root
def userPUT(login):
  body = request.get_json()
  body["_id"] = login
  res = UserManager.updateUser(body)
  if res.matched_count != 1:
    raise StatusException("Trying to update user which does not exists", 400)
  return jsonify(UserManager.getUsers())


@appAPI.route('/user/<string:login>', methods=["DELETE"])
@require_root
def userDELETE(login):
  UserManager.deleteUser(login)
  return jsonify(UserManager.getUsers())

@appAPI.route('/events', methods=["GET"])
@require_user
def events():
  offset = int(request.args.get('offset', 0))
  onlyOutage = util.str2bool(request.args.get('onlyOutage', False))
  events = EventsManager.getEvents(offset, onlyOutage)
  return jsonify(events)
