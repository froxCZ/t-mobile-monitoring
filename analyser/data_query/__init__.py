import datetime

import util
from .DateRangeGroupQuery import DateRangeGroupQuery
from .DatesQuery import DatesQuery
from .SimilarDaysMedianQuery import SimilarDaysMedianQuery

def medianDateRange(fromDate, toDate, lobName, granularity, data):
  fromDate = fromDate.replace(hour=0, minute=0, second=0)
  toDate = toDate.replace(hour=0, minute=0, second=0)
  dayDelta = datetime.timedelta(days=1)
  medianList = []
  date = fromDate
  while date < toDate:
    l = util.minuteDictToDateDict(date, SimilarDaysMedianQuery(lobName, date, granularity=granularity).execute(), "median")
    for d, v in l.items():
      medianList.append(v)
    date += dayDelta
  valueKey = lobName
  # valueKey = "smoothed"
  if True:
    data = util.merge2DateLists(medianList, ["median", "dayAverage"], data, [valueKey])
    for tick in data:
      if tick[valueKey] == tick["median"]:
        tick["relativeDifference"] = 1
        tick["scaledDifference"] = 1
      else:
        diff = tick[valueKey] - tick["median"]
        tick["relativeDifference"] = min(tick[valueKey] / max(tick["median"], 0.1), 3)
        if tick["dayAverage"] != 0:
          scaledDiff = min((diff / tick["dayAverage"]) + 1, 3)
          if scaledDiff >= 1 and tick["relativeDifference"] >= 1:
            tick["scaledDifference"] = min(scaledDiff, tick["relativeDifference"])
          else:
            tick["scaledDifference"] = max(scaledDiff, tick["relativeDifference"])
            # tick["scaledDifference"] = min((diff / tick["dayAverage"]) + 1, 3)
        else:
          tick["scaledDifference"] = 1
  else:
    print("SHOULD NOT HAPPEN X")
  return data