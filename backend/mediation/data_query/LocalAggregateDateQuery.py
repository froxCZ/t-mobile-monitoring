import datetime

import util
from config import AppConfig
from mongo import mongo


class LocalAggregateDateQuery:
  def __init__(self, flow, dates, granularity):
    super().__init__()
    self.flow = flow
    self.coll = mongo.lobs()
    self.dates = dates
    self.granularity = granularity
    self.dataPath = "data." + self.flow["dataPath"]
    self.metric = self.flow["name"]

  def createMatchObject(self):
    orMatches = []
    for date in self.dates:
      orMatches.append({"_id": {"$gte": date, "$lt": util.resetDateTimeMidnight(date + datetime.timedelta(days=1))}})
    return {"$match": {"$and": [{"$or": orMatches}, {self.dataPath: {"$exists": True}}]}}

  def _execQuery(self):
    project = {"$project": {self.metric: "$" + self.dataPath}}
    query = [self.createMatchObject(), project]
    return self.coll.aggregate(query)

  def execute(self):
    def convertToTimezone(x):
      x["_id"] = x["_id"].astimezone(AppConfig.getTimezone())
      return x

    res = list(map(convertToTimezone, list(self._execQuery())))
    resultDict = self.aggregate(res)
    return resultDict

  def aggregate(self, res):
    bucket = {}
    for row in res:
      roundedDate = util.getTicTime(row["_id"], self.granularity)
      bucket[roundedDate] = bucket.get(roundedDate, 0) + row[self.metric]
    resultDict = {}
    for d in sorted(bucket.keys()):
      resultDict[d] = {"_id": d, self.metric: bucket[d]}
    return resultDict


if __name__ == "__main__":
  gran = 120
  flow = {'lobName': 'ACI', 'dataPath': 'CZ.ACI.inputs.GSM', 'country': 'CZ', 'gName': 'CZ_ACI_GSM', 'name': 'GSM',
          'options': {'softAlarmLevel': 0.75, 'hardAlarmLevel': 0.51, 'minimalExpectation': 1, 'enabled': True,
                      'difference': 'day', 'granularity': 480}, 'type': 'inputs'}
  dates = [AppConfig.getTimezone().localize(datetime.datetime(2017, 3, 26, 0, 0))]
  LocalAggregateDateQuery(flow, dates, gran).execute()
