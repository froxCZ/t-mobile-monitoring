from pymongo import MongoClient

from config import AppConfig
"""
Classes for accessing MongoDB collections.
"""

_client = MongoClient("mongodb://localhost/", tz_aware=True)

mongoConfig = AppConfig.getMongoConfig()
_client.admin.authenticate(mongoConfig["user"], mongoConfig["password"], mechanism='SCRAM-SHA-1')
dataDb = _client["mediation_data"]
db = _client["mediation"]


class _Mongo:
  def users(self):
    return self.db()["users"]

  def traffic(self):
    return self.dataDb()["traffic"]

  def statuses(self):
    return self.db()["statuses"]

  def events(self):
    return self.db()["events"]

  def config(self):
    return self.db()["config"]

  def outages(self):
    return self.db()["outages"]

  def dataDb(self):
    return dataDb

  def db(self):
    return db


class _ZookeeperMongo:
  def config(self):
    return self.db()["zookeeper_config"]

  def statuses(self):
    return self.db()["statuses"]

  def dataDb(self):
    return dataDb

  def db(self):
    return db


mongo = _Mongo()

zookeeperMongo = _ZookeeperMongo()
