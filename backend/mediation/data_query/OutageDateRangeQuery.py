import datetime

import util

class OutageDateRangeQuery():
  def __init__(self, fromDate, toDate, flow, granularity):
    super().__init__()
    self.fromDate = util.resetDateTimeMidnight(fromDate)
    self.toDate = util.resetDateTimeMidnight(toDate)
    self.flow = flow
    self.granularity = granularity
    self.metric = "status"
    self.ticDict = {}
    from mediation.flow_analyzer import FlowAnalyzer
    self.flowAnalyzer = FlowAnalyzer(self.flow,self.granularity)

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
    d = self.fromDate + granularityDelta
    statusList = []
    while d < self.toDate + granularityDelta:
      self.flowAnalyzer.run(d)
      status = self.flowAnalyzer.status
      statusList.append({"_id": self.flowAnalyzer.ticTime, "status": status})
      d += granularityDelta
    return statusList


if __name__ == "__main__":
  OutageDateRangeQuery(util.stringToTime("17.01.2017 15:00:00"),util.stringToTime("20.01.2017 15:00:00"),{},0)