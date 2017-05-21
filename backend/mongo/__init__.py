from pymongo import MongoClient

from config import AppConfig
"""
Classes for accessing MongoDB collections.
The mongo client is created in lazy way, so some parts of the app (tests) can be executed without mongo database running.
"""
db = None
dataDb = None
_client = None

def init():
  global db, dataDb, _client
  _client = MongoClient("mongodb://localhost/", tz_aware=True)
  mongoConfig = AppConfig.getMongoConfig()
  _client.admin.authenticate(mongoConfig["user"], mongoConfig["password"], mechanism='SCRAM-SHA-1')
  dataDb = _client["mediation_data"]
  db = _client["mediation"]


def getDb():
  if db is None:
    init()
  return db


def getDataDb():
  if dataDb is None:
    init()
  return dataDb


class _Mongo:
  def users(self):
    return getDb()["users"]

  def traffic(self):
    return getDataDb()["traffic"]

  def statuses(self):
    return getDb()["statuses"]

  def events(self):
    return getDb()["events"]

  def config(self):
    return getDb()["config"]

  def outages(self):
    return getDb()["outages"]

  def dataDb(self):
    return getDataDb()


class _ZookeeperMongo:
  def config(self):
    return getDb()["zookeeper_config"]

  def statuses(self):
    return getDb()["statuses"]

  def dataDb(self):
    return getDataDb()


mongo = _Mongo()

zookeeperMongo = _ZookeeperMongo()
