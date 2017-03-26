import util
from mediation import data_query


class TicTrafficQuery():
  """
  Calculates expected and flow level traffic for given tick only
  """

  def __init__(self, dateTime, flow):
    self.dateTime = dateTime
    self.flow = flow

  def execute(self):
    currentQuery = data_query.DatesQuery([self.dateTime], [self.flow])
    currentData = currentQuery.execute()
    currenttic = self._gettic(currentData, self.dateTime)
    if currenttic == None:
      raise Exception("Could not find tic for flow " + self.flow["gName"] + " at " + str(self.dateTime))
    expectedQuery = data_query.ExpectedTrafficQuery(self.dateTime, [self.flow])
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

  def _gettic(self, ticList, datetime):
    for tic in ticList:
      if tic["_id"] == datetime:
        return tic
    return None
