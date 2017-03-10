import data_query
import util


class TickTrafficQuery():
  def __init__(self, dateTime, flow):
    self.dateTime = dateTime
    self.flow = flow

  def execute(self):
    currentQuery = data_query.DatesQuery([self.dateTime], [self.flow])
    currentData = currentQuery.execute()
    currentTick = self._getTick(currentData, self.dateTime)
    if currentTick == None:
      raise Exception("Could not find tick for flow " + self.flow["gName"] + " at " + str(self.dateTime))
    expectedQuery = data_query.ExpectedTrafficQuery(self.dateTime, [self.flow])
    expectedData = expectedQuery.execute()
    metric = expectedQuery.metrics[0]
    dayMinute = util.dateToDayMinutes(self.dateTime)
    if dayMinute not in expectedData:
      raise Exception("Could not find expected tick for flow " + self.flow["gName"] + " at " + str(self.dateTime))
    expectedValue = expectedData[util.dateToDayMinutes(self.dateTime)]
    result = {"value": currentTick[metric],
              "expected": expectedValue,
              "dayAverage": expectedQuery.dayAverage,
              "_id": currentTick["_id"]}
    return result

  def _getTick(self, tickList, datetime):
    for tick in tickList:
      if tick["_id"] == datetime:
        return tick
    return None
