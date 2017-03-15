import hashlib

from flask import Blueprint, jsonify
from flask import request

from common import UserManager

common = Blueprint('common', __name__)


def _invalidLoginResponse():
  resp = jsonify({"message": "Invalid username or password"})
  resp.status_code = 401
  return resp

@common.route('/login', methods=["POST"])
def login():
  body = request.get_json()
  if body == None:
    return _invalidLoginResponse()
  username = body["username"]
  password = body["password"]
  if username == None or password == None:
    return _invalidLoginResponse()
  passHash = hashlib.sha512(password.encode('utf-8')).hexdigest()
  user = UserManager.getUserByName(username)
  if user == None or user["passwordHash"].lower() != passHash.lower():
    return _invalidLoginResponse()
  del user["passwordHash"]
  return jsonify(user)

@common.route('/users', methods=["GET"])
def usersGET():
  return jsonify(UserManager.getUsers())