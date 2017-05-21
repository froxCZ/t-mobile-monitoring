import logging

from common import util
from mediation import data_query


class TicTrafficQuery():
  """
  Calculates expected and flow level traffic for given tick only
  """

  def __init__(self, dateTime, flow, granularity=0):
    self.dateTime = dateTime
    self.flow = flow
    self.granularity = granularity

  def execute(self):
    currentQuery = data_query.DatesQuery([self.dateTime], [self.flow], granularity=self.granularity)
    currentData = currentQuery.execute()
    currenttic = self._gettic(currentData, self.dateTime)
    if currenttic == None:
      logging.error("Could not find tic for flow " + self.flow["gName"] + " at " + str(self.dateTime))
      raise Exception("Could not find tic for flow " + self.flow["gName"] + " at " + str(self.dateTime))
    expectedQuery = data_query.ExpectedTrafficQuery(self.dateTime, [self.flow], granularity=self.granularity)
    expectedData = expectedQuery.execute()
    metric = expectedQuery.metrics[0]
    dayMinute = util.dateToDayMinutes(self.dateTime)
    if dayMinute not in expectedData:
      raise Exception("Could not find expected tic for flow " + self.flow["gName"] + " at " + str(self.dateTime))
    expectedValue = expectedData[util.dateToDayMinutes(self.dateTime)]
    result = {"value": currenttic[metric],
              "expected": expectedValue,
              "dayAverage": expectedQuery.dayAverage,
              "_id": currenttic["_id"]}
    return result

  def _gettic(self, ticList, d):
    for tic in ticList:
      if tic["_id"] == d:
        return tic
    for tic in ticList:
      if util.getTicTime(tic["_id"], self.granularity) == util.getTicTime(d, self.granularity):
        return tic
    return None
