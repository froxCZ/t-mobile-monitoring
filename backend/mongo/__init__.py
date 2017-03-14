import pytz
from bson import CodecOptions
from pymongo import MongoClient

_client = MongoClient("mongodb://localhost/", tz_aware=True)

codec_options = CodecOptions(
  tz_aware=True,
  tzinfo=pytz.timezone('CET')
)


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
    return _client["mediation_data"]

  def db(self):
    return _client["mediation"]


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
    return _client["mediation_data"]

  def db(self):
    return _client["mediation"]


mongo = _Mongo()

zookeeperMongo = _ZookeeperMongo()
