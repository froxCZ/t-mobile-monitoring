import datetime

import util
from mediation.flow_analyzer import FlowAnalyzer


class OutageDateRangeQuery():
  def __init__(self, fromDate, toDate, flow, granularity):
    super().__init__()
    self.fromDate = util.resetDateTimeMidnight(fromDate)
    self.toDate = util.resetDateTimeMidnight(toDate)
    self.flow = flow
    self.granularity = granularity
    self.metric = "status"
    self.ticDict = {}
    self.flowAnalyzer = FlowAnalyzer(self.flow)

  def setPrecomputedData(self, precomputedData, valueKey):
    for tic in precomputedData:
      id = tic["_id"]
      self.ticDict[id] = {"_id": id,
                           "value": tic[valueKey],
                           "expected": tic["expected"],
                           "dayAverage": tic["dayAverage"]
                           }
    self.flowAnalyzer.setPrecomputedData(self.ticDict)

  def execute(self):
    granularityDelta = datetime.timedelta(minutes=self.granularity)
    d = self.fromDate
    statusList = []
    while d < self.toDate:
      self.flowAnalyzer.run(d)
      status = self.flowAnalyzer.status
      statusList.append({"_id": d, "status": status})
      d += granularityDelta
    return statusList
