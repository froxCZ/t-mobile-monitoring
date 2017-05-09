import datetime

import pytz

import util
from config import AppConfig
from mediation.data_query import ExpectedTrafficQuery
from .flow_level_difference import calculateFlowLevelDifference

utc = pytz.timezone("UTC")


class FlowLevelDateRangeQuery:
  """
  Calls ExpectedTrafficQuery and calculates current level of traffic compared to expectations
  """

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
      date = util.getNextDay(date)
    resultData = []
    mergedMedianListData = util.merge2DateLists(medianList, ["expected", "dayAverage"], self.data, [valueKey])
    for tic in mergedMedianListData:
      resulttic = calculateFlowLevelDifference(tic[valueKey], tic["expected"], tic["dayAverage"])
      resulttic["_id"] = tic["_id"]
      resulttic["expected"] = tic["expected"]
      resulttic["dayAverage"] = tic["dayAverage"]
      resultData.append(resulttic)
    self.metrics = ["tickDifference", "dayDifference", "expected", "dayAverage"]
    return resultData

if __name__ == "__main__":
  gran = 120
  flow = {'lobName': 'ACI', 'dataPath': 'CZ.ACI.inputs.GSM', 'country': 'CZ', 'gName': 'CZ_ACI_GSM', 'name': 'GSM',
          'options': {'softAlarmLevel': 0.75, 'hardAlarmLevel': 0.51, 'minimalExpectation': 1, 'enabled': True,
                      'difference': 'day', 'granularity': 480}, 'type': 'inputs'}
  dates = [AppConfig.getTimezone().localize(datetime.datetime(2017, 3, 26, 0, 0))]
  FlowLevelDateRangeQuery(flow, dates, gran).execute()