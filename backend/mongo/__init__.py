import pytz
from bson import CodecOptions
from pymongo import MongoClient

_client = MongoClient("mongodb://localhost/", tz_aware=True)

codec_options = CodecOptions(
  tz_aware=True,
  tzinfo=pytz.timezone('CET')
)


class _Mongo:
  def lobs(self):
    return self.dataDb()["lobs"].with_options(codec_options=CodecOptions(
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

  def dataDb(self):
    return _client["dev_data"]

  def db(self):
    return _client["dev"]


mongo = _Mongo()
