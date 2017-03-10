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
      for tic in l.values():
        tic["dayAverage"] = similarDaysQuery.dayAverage
      valueKey = similarDaysQuery.metrics[0]
      for d, v in l.items():
        medianList.append(v)
      date += dayDelta
    resultData = []
    mergedMedianListData = util.merge2DateLists(medianList, ["expected", "dayAverage"], self.data, [valueKey])
    for tic in mergedMedianListData:
      resulttic = calculateFlowLevelDifference(tic[valueKey], tic["expected"], tic["dayAverage"])
      resulttic["_id"] = tic["_id"]
      resulttic["expected"] = tic["expected"]
      resulttic["dayAverage"] = tic["dayAverage"]
      resultData.append(resulttic)
    self.metrics = ["flowDifference", "normalizedDifference", "expected", "dayAverage"]
    return resultData
