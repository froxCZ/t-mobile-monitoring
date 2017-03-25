import pytz
from bson import CodecOptions
from pymongo import MongoClient

from config import AppConfig

_client = MongoClient("mongodb://localhost/", tz_aware=True)

codec_options = CodecOptions(
  tz_aware=True,
  tzinfo=pytz.timezone('CET')
)
mongoConfig = AppConfig.getMongoConfig()
_client.admin.authenticate(mongoConfig["user"], mongoConfig["password"], mechanism='SCRAM-SHA-1')
dataDb = _client["mediation_data"]
db = _client["mediation"]


class _Mongo:
  def users(self):
    return self.db()["users"].with_options(codec_options=CodecOptions(
      tz_aware=True,
      tzinfo=pytz.timezone('CET')
    ))

  def lobs(self):
    return self.dataDb()["lobs"].with_options(codec_options=CodecOptions(
      tz_aware=True,
      tzinfo=pytz.timezone('CET')
    ))

  def statuses(self):
    return self.db()["statuses"].with_options(codec_options=CodecOptions(
      tz_aware=True,
      tzinfo=pytz.timezone('CET')
    ))

  def events(self):
    return self.db()["events"].with_options(codec_options=CodecOptions(
      tz_aware=True,
      tzinfo=pytz.timezone('CET')
    ))

  def config(self):
    return self.db()["config"].with_options(codec_options=CodecOptions(
      tz_aware=True,
      tzinfo=pytz.timezone('CET')
    ))

  def outages(self):
    return self.db()["outages"].with_options(codec_options=CodecOptions(
      tz_aware=True,
      tzinfo=pytz.timezone('CET')
    ))

  def status(self):
    return self.db()["status"].with_options(codec_options=CodecOptions(
      tz_aware=True,
      tzinfo=pytz.timezone('CET')
    ))

  def dataDb(self):
    return dataDb

  def db(self):
    return db


class _ZookeeperMongo:
  def config(self):
    return self.db()["zookeeper_config"].with_options(codec_options=CodecOptions(
      tz_aware=True,
      tzinfo=pytz.timezone('CET')
    ))

  def statuses(self):
    return self.db()["statuses"].with_options(codec_options=CodecOptions(
      tz_aware=True,
      tzinfo=pytz.timezone('CET')
    ))

  def dataDb(self):
    return dataDb

  def db(self):
    return db


mongo = _Mongo()

zookeeperMongo = _ZookeeperMongo()
