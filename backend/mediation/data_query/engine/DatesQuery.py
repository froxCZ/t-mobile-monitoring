import datetime

import pytz

from common import util
from mongo import mongo

utc = pytz.timezone("UTC")


class DatesQuery:
  def __init__(self, dates, flows, granularity=0):
    self.query = None
    self.coll = mongo.traffic()
    self.flow = flows[0]
    self.metrics = []
    self.dates = [util.resetDateTimeMidnight(d) for d in dates]
    self.metric = self.flow["name"]
    self.metrics.append(self.metric)
    self.granularity = int(granularity)
    self.metadata = {}
    self.determinateGranularity()

  def _executeMongoAggregateQuery(self):
    from mediation.data_query.engine import MongoAggregateDateQuery
    return MongoAggregateDateQuery(self.flow, self.dates, self.granularity).execute()

  def _executePythonAggregateQuery(self):
    from mediation.data_query.engine import PythonAggregateDateQuery
    return PythonAggregateDateQuery(self.flow, self.dates, self.granularity).execute()

  def execute(self):
    startTime = util.startTime()
    resultDict = self._executePythonAggregateQuery()
    diff = util.timeDifference(startTime)
    #print(diff, ",")
    nullObject = {self.metric: 0}
    finalResultDict = {}
    for date in self.dates:
      d = date
      until = util.resetDateTimeMidnight(date + datetime.timedelta(days=1))
      while d < until:
        if d not in resultDict:  # TODO: check if some results can have just few of the metrics.
          finalResultDict[d] = {**nullObject, **{"_id": d}}
        else:
          finalResultDict[d] = resultDict[d]
        d = util.getNextTic(d, self.granularity)

    result = sorted(finalResultDict.values(), key=lambda x: x["_id"])
    return result

  def determinateGranularity(self):
    if (self.granularity == 0):
      self.granularity = self.flow["options"]["granularity"]
    self.metadata["granularity"] = self.granularity
