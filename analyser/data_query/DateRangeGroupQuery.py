import datetime

from data_query.DatesQuery import  DatesQuery


class DateRangeGroupQuery(DatesQuery):
  def __init__(self, fromDate, toDate, lobNames, granularity, neids=None, forwards=None):
    self.fromDate = fromDate
    self.toDate = toDate
    lastDate = self.fromDate
    dates = []
    timeDelta = datetime.timedelta(days=1)
    while lastDate < self.toDate:
      dates.append(lastDate)
      lastDate += timeDelta
    super().__init__(dates,lobNames, granularity, neids, forwards)


  def execute(self):
    result = super(DateRangeGroupQuery, self).execute()
    timeSequenceResult = []
    lastDate = self.fromDate
    timeDelta = datetime.timedelta(minutes=self.metadata["granularity"])
    i = 0
    nullMetrics = {}
    for metric in self.metrics:
      nullMetrics[metric] = 0
    while lastDate < self.toDate:
      if i < len(result) and lastDate == result[i]["_id"]:
        timeSequenceResult.append({**nullMetrics, **result[i]})
        i += 1
      else:
        timeSequenceResult.append({**{"_id": lastDate}, **nullMetrics})
      lastDate += timeDelta

    return timeSequenceResult
