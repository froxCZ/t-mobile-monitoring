from functools import wraps

from flask import abort
from flask import jsonify
from flask import make_response
from flask import request

from common import UserManager


def _getUserByApiKey():
  apiKey = request.headers.get("X-API-KEY")
  if apiKey == None:
    apiKey = request.args.get('apiKey')
  return UserManager.getUserByApiKey(apiKey)


def require_root(func):
  @wraps(func)
  def check_token(*args, **kwargs):
    user = _getUserByApiKey()
    if user is None:
      abort(make_response(jsonify(message="Unauthorized"), 401))
    if user["permission"] != "root":
      abort(make_response(jsonify(message="Not enough permissions"), 403))
    return func(*args, **kwargs)

  return check_token


def require_user(func):
  @wraps(func)
  def check_token(*args, **kwargs):
    user = _getUserByApiKey()
    if user is None:
      abort(make_response(jsonify(message="Unauthorized"), 401))
    return func(*args, **kwargs)

  return check_token
