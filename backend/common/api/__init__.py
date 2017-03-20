import hashlib

from flask import Blueprint, jsonify
from flask import request

from common import UserManager

common = Blueprint('common', __name__)


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


@common.route('/login', methods=["POST"])
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


@common.route('/users', methods=["GET"])
def usersGET():
  return jsonify(UserManager.getUsers())


@common.route('/users', methods=["POST"])
def usersPOST():
  body = request.get_json()
  if "login" not in body or len(body["login"]) == 0:
    raise StatusException("Login is required", 400)
  UserManager.addUser(body)
  return jsonify(UserManager.getUsers())


@common.route('/user/<string:login>', methods=["PUT"])
def userPUT(login):
  body = request.get_json()
  body["_id"] = login
  res = UserManager.updateUser(body)
  if res.matched_count != 1:
    raise StatusException("Trying to update user which does not exists", 400)
  return jsonify(UserManager.getUsers())


@common.route('/user/<string:login>', methods=["DELETE"])
def userDELETE(login):
  UserManager.deleteUser(login)
  return jsonify(UserManager.getUsers())
