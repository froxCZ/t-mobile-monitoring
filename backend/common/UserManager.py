import hashlib
import random
import string

from mongo import mongo

"""
Classes for managing users.
"""

def modifyUsers(x):
  if "passwordHash" in x:
    del x["passwordHash"]
  if x["accountType"] == "user":
    del x["apiKey"]
  x["login"] = x["_id"]
  del x["_id"]
  return x


def _hashPassword(password):
  return hashlib.sha512(password.encode('utf-8')).hexdigest()


def _generateApiKey():
  return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

DEFAULT_USER = {
  "login": "root",
  "password": "root",
  "name": "root",
  "accountType": "user",
  "permission": "root",
}

VISITOR_USER = {
  "login": "visitor",
  "password": "visitor",
  "name": "visitor",
  "accountType": "user",
  "permission": "readOnly",
}


class UserManager():
  @staticmethod
  def getUserByApiKey(apiKey):
    if apiKey is None:
      return None
    return mongo.users().find_one({"apiKey": apiKey})

  @staticmethod
  def getUserByName(username):
    if username is None:
      return None
    return mongo.users().find_one({"_id": username})

  @staticmethod
  def getUsers():
    return list(map(modifyUsers, list(mongo.users().find())))

  @staticmethod
  def addUser(body):
    body["_id"] = body["login"]
    del body["login"]
    if body["accountType"] == "user":
      body["passwordHash"] = _hashPassword(body["password"])
      del body["password"]
    body["apiKey"] = _generateApiKey()
    return mongo.users().insert_one(body)

  @staticmethod
  def updateUser(body):
    if "password" in body:
      body["passwordHash"] = _hashPassword(body["password"])
      del body["password"]
    if body.get("generateNewApiKey",False):
      body["apiKey"] = _generateApiKey()
      del body["generateNewApiKey"]
    return mongo.users().update_one({"_id": body["_id"]}, {"$set": body})

  @staticmethod
  def deleteUser(login):
    return mongo.users().delete_one({"_id": login})


# if len(UserManager.getUsers()) == 0:#if there is no user in db, insert root/root and visitor
#   UserManager.addUser(DEFAULT_USER)
#   UserManager.addUser(VISITOR_USER)