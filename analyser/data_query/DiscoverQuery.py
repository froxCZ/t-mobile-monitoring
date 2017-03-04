import util
from config import config
from mongo import mongo


class DiscoverQuery():
  def __init__(self, fromDate, toDate):
    self.fromDate = fromDate
    self.toDate = toDate

  def execute(self):
    lobsConfig = config.getLobsConfig()["lobs"]
    discovered = {}
    cursor = mongo.lobs().find({"$and": [
      {"_id": {"$gte": self.fromDate}},
      {"_id": {"$lt": self.toDate}}
    ]})
    for doc in cursor:
      for lobName, lob in doc["data"].items():
        if lobName not in lobsConfig:
          continue
        if lobName not in discovered:
          discovered[lobName] = {"neids": {}, "forwards": {}}
        if "inputs" in lob:
          for neid in lob["inputs"]:
            if neid == "sum" or neid == "updatesCnt":
              continue
            if neid not in lobsConfig[lobName]["neids"] and neid not in discovered[lobName]["neids"]:
              discovered[lobName]["neids"][neid] = {"granulity": 0}
        if "forwards" in lob:
          for forward in lob["forwards"]:
            if forward == "sum" or forward == "updatesCnt":
              continue
            if forward not in lobsConfig[lobName]["forwards"] and forward not in discovered[lobName]["forwards"]:
              discovered[lobName]["forwards"][forward] = {"granulity": 0}

    return discovered


f = util.stringToDate("01.01.2017")
t = util.stringToDate("10.01.2017")

res = DiscoverQuery(f, t).execute()
print(res)
