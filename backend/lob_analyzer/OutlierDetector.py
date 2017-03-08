# class OutlierDetector:
#   def __init__(self, flow, dateTime):
#     self.flow = flow
#     self.dateTime = dateTime
#
#   def _getExpectedData(self):
#     from data_query import ExpectedTrafficQuery
#     return ExpectedTrafficQuery(self.lobName,self.dateTime).execute()
#
#   def _getCurrentData(self):
#     from data_query import DatesQuery
#     datesQuery = DatesQuery([self.dateTime], self.lobName, resultName="value");
#     data = datesQuery.execute()
#     return util.listToDayMinutes(data)

class OutlierDetector():
  pass