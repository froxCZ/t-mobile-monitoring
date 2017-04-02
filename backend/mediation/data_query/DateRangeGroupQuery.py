import datetime

import util
from .DatesQuery import DatesQuery


class DateRangeGroupQuery(DatesQuery):
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
    result = super(DateRangeGroupQuery, self).execute()
    timeSequenceResult = []
    lastDate = self.fromDate
    timeDelta = datetime.timedelta(minutes=self.metadata["granularity"])
    i = 0
    nullMetrics = {}
    for metric in self.metrics:
      nullMetrics[metric] = 0
    # while lastDate < self.toDate:
    #   if i < len(result) and lastDate == result[i]["_id"]:
    #     timeSequenceResult.append({**nullMetrics, **result[i]})
    #     i += 1
    #   else:
    #     timeSequenceResult.append({**{"_id": lastDate}, **nullMetrics})
    #     raise Exception("DOUBLE FILLING - SHOULD NEVER HAPPEN")
    #   lastDate += timeDelta

    return result
