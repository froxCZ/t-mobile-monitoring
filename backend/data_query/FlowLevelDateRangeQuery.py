import datetime

import util
from data_query import ExpectedTrafficQuery
from data_util import calculateFlowLevelDifference


class FlowLevelDateRangeQuery:
  def __init__(self, fromDate, toDate, flows, granularity, data):
    super().__init__()
    self.fromDate = util.resetDateTimeMidnight(fromDate)
    self.toDate = util.resetDateTimeMidnight(toDate)
    self.flows = flows
    self.granularity = granularity
    self.data = data
    self.metrics = []

  def execute(self):
    date = self.fromDate
    dayDelta = datetime.timedelta(days=1)
    medianList = []
    while date < self.toDate:
      similarDaysQuery = ExpectedTrafficQuery(date, self.flows, granularity=self.granularity)
      similarDatesData = similarDaysQuery.execute()
      l = util.minuteDictToDateDict(date, similarDatesData, "expected")
      dayTotal = 0
      for tick in l.values():
        dayTotal += tick["expected"]
      if len(l.values()) != 0:
        dayAverage = dayTotal / len(l.values())
      else:
        dayAverage = 0
      for tick in l.values():
        tick["dayAverage"] = dayAverage
      valueKey = similarDaysQuery.metrics[0]
      for d, v in l.items():
        medianList.append(v)
      date += dayDelta
    resultData = []
    mergedMedianListData = util.merge2DateLists(medianList, ["expected", "dayAverage"], self.data, [valueKey])
    for tick in mergedMedianListData:
      resultTick = calculateFlowLevelDifference(tick[valueKey], tick["expected"], tick["dayAverage"])
      resultTick["_id"] = tick["_id"]
      resultTick["expected"] = tick["expected"]
      resultTick["dayAverage"] = tick["dayAverage"]
      resultData.append(resultTick)
    self.metrics = ["relativeDifference", "scaledDifference", "expected", "dayAverage"]
    return resultData
