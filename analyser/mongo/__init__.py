from pymongo import MongoClient

_client = MongoClient("mongodb://localhost/")

class _Mongo:
  def dataDb(self):
    return _client["dev_data"]
  def db(self):
    return _client["dev"]
mongo = _Mongo()