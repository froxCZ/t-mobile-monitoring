import datetime

import util
from .DateRangeGroupQuery import DateRangeGroupQuery
from .DatesQuery import DatesQuery
from .DatesQueryV1 import DatesQueryV1
from .DiscoverQuery import DiscoverQuery
from .ExpectedTrafficQuery import ExpectedTrafficQuery


def medianDateRange(fromDate, toDate, flows, granularity, data):
  fromDate = fromDate.replace(hour=0, minute=0, second=0)
  toDate = toDate.replace(hour=0, minute=0, second=0)
  dayDelta = datetime.timedelta(days=1)
  medianList = []
  date = fromDate
  while date < toDate:
    similarDaysQuery = ExpectedTrafficQuery(date, flows, granularity=granularity)
    similarDatesData = similarDaysQuery.execute()
    l = util.minuteDictToDateDict(date, similarDatesData, "expected")
    valueKey = similarDaysQuery.metrics[0]
    for d, v in l.items():
      medianList.append(v)
    date += dayDelta
  # valueKey = "smoothed"
  if True:
    data = util.merge2DateLists(medianList, ["expected", "dayAverage"], data, [valueKey])
    for tick in data:
      if tick[valueKey] == tick["expected"]:
        tick["relativeDifference"] = 1
        tick["scaledDifference"] = 1
      else:
        diff = tick[valueKey] - tick["expected"]
        tick["relativeDifference"] = min(tick[valueKey] / max(tick["expected"], 0.1), 3)
        if tick["dayAverage"] != 0:
          if tick["relativeDifference"] >= 0.1:
            scaledDiff = min((diff / tick["dayAverage"]) + 1, 3)
            if scaledDiff >= 1 and tick["relativeDifference"] >= 1:
              tick["scaledDifference"] = min(scaledDiff, tick["relativeDifference"])
            else:
              tick["scaledDifference"] = max(scaledDiff, tick["relativeDifference"])
              # tick["scaledDifference"] = min((diff / tick["dayAverage"]) + 1, 3)
          else:
            tick["scaledDifference"] = tick["relativeDifference"]
        else:
          tick["scaledDifference"] = 1
      tick["scaledDifference"] = round(tick["scaledDifference"], 3)
      tick["relativeDifference"] = round(tick["relativeDifference"], 3)
  else:
    print("SHOULD NOT HAPPEN X")
  return data
