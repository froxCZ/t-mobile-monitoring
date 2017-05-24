import datetime

from common import AppConfig
from common import util
from mongo import mongo


class PythonAggregateDateQuery:
  """
  Aggregate query that works across dates with different timezones (DST time change). Max aggregation in Mongo is
  60 minutes, rest is aggregated in Python in this class.
  """
  def __init__(self, flow, dates, granularity):
    super().__init__()
    self.flow = flow
    self.coll = mongo.traffic()
    self.dates = dates
    self.granularity = granularity
    self.dataPath = "data." + self.flow["dataPath"]
    self.metric = self.flow["name"]

  def createMatchObject(self):
    orMatches = []
    for date in self.dates:
      orMatches.append({"_id": {"$gte": date, "$lt": util.resetDateTimeMidnight(date + datetime.timedelta(days=1))}})
    return {"$match": {"$and": [{"$or": orMatches}, {self.dataPath: {"$exists": True}}]}}

  def createMinuteGrouping(self):
    if self.granularity >= 60:
      groupByMinutes = 60
    else:
      groupByMinutes = self.granularity

    groupObject = {
      "_id": {
        "year": {"$year": "$_id"},
        "month": {"$month": "$_id"},
        "dayOfMonth": {"$dayOfMonth": "$_id"},
        "hour": {"$hour": "$_id"},
        "minute": {
          "$subtract": [
            {"$minute": "$_id"},
            {"$mod": [{"$minute": "$_id"}, groupByMinutes]}
          ]
        }
      },
      self.metric: {"$sum": "$" + self.dataPath},
      "anyDate": {"$first": "$_id"},
    }
    return {"$group": groupObject}

  def _executeQuery(self):
    query = [self.createMatchObject(), self.createMinuteGrouping()]
    return self.coll.aggregate(query)

  def execute(self):
    timezone = AppConfig.getTimezone()

    def convertToTimezone(x):
      x["_id"] = x["anyDate"].astimezone(timezone)
      return x

    res = list(map(convertToTimezone, list(self._executeQuery())))
    resultDict = self.aggregate(res)
    return resultDict

  def aggregate(self, res):
    bucket = {}
    for row in res:
      roundedDate = util.getTicTime(row["_id"], self.granularity)
      bucket[roundedDate] = bucket.get(roundedDate, 0) + row[self.metric]
    resultDict = {}
    for d in bucket.keys():
      resultDict[d] = {"_id": d, self.metric: bucket[d]}
    return resultDict


if __name__ == "__main__":
  gran = 120
  flow = {'lobName': 'ACI', 'dataPath': 'CZ.ACI.inputs.GSM', 'country': 'CZ', 'gName': 'CZ_ACI_GSM', 'name': 'GSM',
          'options': {'softAlarmLevel': 0.75, 'hardAlarmLevel': 0.51, 'minimalExpectation': 1, 'enabled': True,
                      'difference': 'day', 'granularity': 480}, 'type': 'inputs'}
  dates = [AppConfig.getTimezone().localize(datetime.datetime(2017, 3, 26, 0, 0))]
  PythonAggregateDateQuery(flow, dates, gran).execute()
