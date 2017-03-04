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
          discovered[lobName] = {"inputs": {}, "forwards": {}}
        if "inputs" in lob:
          for neid in lob["inputs"]:
            if neid == "sum" or neid == "updatesCnt":
              continue
            if neid not in lobsConfig[lobName]["inputs"] and neid not in discovered[lobName]["inputs"]:
              discovered[lobName]["inputs"][neid] = {"granularity": 0}
        if "forwards" in lob:
          for forward in lob["forwards"]:
            if forward == "sum" or forward == "updatesCnt":
              continue
            if forward not in lobsConfig[lobName]["forwards"] and forward not in discovered[lobName]["forwards"]:
              discovered[lobName]["forwards"][forward] = {"granularity": 0}

    return discovered