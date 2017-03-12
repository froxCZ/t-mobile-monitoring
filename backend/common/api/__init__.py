from functools import wraps

from flask import Blueprint, jsonify
from flask import abort
from flask import make_response
from flask import request

from common import UserManager

common = Blueprint('common', __name__)


def require_root(func):
  @wraps(func)
  def check_token(*args, **kwargs):
    apiKey = request.headers.get("X-API-KEY")
    if apiKey == None:
      apiKey = request.args.get('apiKey')
    user = UserManager.getUserByApiKey(apiKey)
    if user is None:
      abort(make_response(jsonify(message="Unauthorized"), 401))
    if user["role"] != "root":
      abort(make_response(jsonify(message="Not enough permissions"), 403))
    return func(*args, **kwargs)

  return check_token


@common.route('/login', methods=["GET"])
@require_root
def login():
  return jsonify({"a": 1})
