import datetime

import util
from flow_analyzer import FlowAnalyzer


class OutageDateRangeQuery():
  def __init__(self, fromDate, toDate, flow, granularity):
    super().__init__()
    self.fromDate = util.resetDateTimeMidnight(fromDate)
    self.toDate = util.resetDateTimeMidnight(toDate)
    self.flow = flow
    self.granularity = granularity
    self.metric = "outage"
    self.tickDict = {}
    self.flowAnalyzer = FlowAnalyzer(self.flow)

  def setPrecomputedData(self, precomputedData, valueKey):
    for tick in precomputedData:
      id = tick["_id"]
      self.tickDict[id] = {"_id": id,
                           "value": tick[valueKey],
                           "expected": tick["expected"],
                           "dayAverage": tick["dayAverage"]
                           }
    self.flowAnalyzer.setPrecomputedData(self.tickDict)

  def execute(self):
    granularityDelta = datetime.timedelta(minutes=self.granularity)
    d = self.fromDate
    outageList = []
    while d < self.toDate:
      self.flowAnalyzer.run(d)
      outage = self.flowAnalyzer.isOutage
      outageList.append({"_id": d, "outage": outage})
      d += granularityDelta
    return outageList
