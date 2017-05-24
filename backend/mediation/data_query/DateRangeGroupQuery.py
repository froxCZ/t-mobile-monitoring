from common import util
from mediation.data_query.engine.DatesQuery import DatesQuery


class DateRangeGroupQuery(DatesQuery):
  """
  Returns traffic of dates in the range.
  """
  def __init__(self, fromDate, toDate, flows, granularity=0):
    self.fromDate = fromDate
    self.toDate = toDate
    lastDate = self.fromDate
    dates = []
    while lastDate < self.toDate:
      dates.append(lastDate)
      lastDate = util.getNextDay(lastDate)
    super().__init__(dates, flows, granularity)

  def execute(self):
    return super(DateRangeGroupQuery, self).execute()
