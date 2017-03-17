from statistics import median

import util
from mediation import MediationConfig
from .SimilarPastDaysFinder import SimilarPastDaysFinder


class ExpectedTrafficQuery:
  def __init__(self, date, flows, granularity=0):
    self.flows = flows
    self.flow = flows[0]
    self.date = date
    self.granularity = granularity
    self.dates = SimilarPastDaysFinder(self.flow).findSimilarPastDays(date)
    country = MediationConfig.getCountryByName(self.flow["country"])
    options = self.flow["options"]
    self.adjustment = None
    lazyDayDifference = self.flow["options"].get("lazyDayDifference", 1)
    if lazyDayDifference != 1:
      for lazyDayStr in country["lazyDays"]:
        lazyDay = util.stringToDate(lazyDayStr)
        if lazyDay.date() == date.date():
          self.adjustment = lazyDayDifference
          break

  def execute(self):
    from mediation.data_query import DatesQuery
    datesQuery = DatesQuery(self.dates, self.flows, self.granularity)
    data = datesQuery.execute()
    self.metadata = datesQuery.metadata
    self.metrics = datesQuery.metrics
    metric = datesQuery.metrics[0]
    if self.adjustment is not None:
      for tick in data:
        tick[metric] = tick[metric] * self.adjustment
    dayMedians = _createMedians(data, metric)
    self.dayAverage = 0
    if len(dayMedians.values()) != 0:
      self.dayAverage = sum(dayMedians.values()) / len(dayMedians.values())
    return dayMedians


def _createMedians(data, valueName):
  day = {}
  for row in data:
    dateTime = row["_id"]
    minutesOfDay = dateTime.hour * 60 + dateTime.minute
    if minutesOfDay in day:
      valueList = day[minutesOfDay]
    else:
      valueList = []
      day[minutesOfDay] = valueList
    valueList.append(row[valueName])
  dayMedians = {}
  for minute, valueList in day.items():
    valueList = sorted(valueList)
    if len(valueList) > 5:
      n = 2
      valueList = valueList[n:-n]
    if len(valueList) == 0:
      dayMedians[minute] = 0
      continue
    med = median(valueList)
    dayMedians[minute] = med
  return dayMedians


def _createWeightedMeans(data, valueName):
  day = {}
  for row in data:
    dateTime = row["_id"]
    minutesOfDay = dateTime.hour * 60 + dateTime.minute
    if minutesOfDay in day:
      valueList = day[minutesOfDay]
    else:
      valueList = []
      day[minutesOfDay] = valueList
    valueList.append(row[valueName])
  dayMedians = {}
  for minute, valueList in day.items():
    if len(data) == 0:
      continue
    dayMedians[minute] = _weightedMean(valueList)
  return dayMedians


def _weightedMean(values):
  weights = [(i + 1) * (i + 1) for i in range(0, len(values))]

  s = 0
  for x, y in zip(values, weights):
    s += x * y

  average = s / sum(weights)
  return average


def medianDeviation(data):
  data = sorted(data)
  data = data[:int(len(data) / 4)]
  med = median(data)
  mads = []
  if med == 0:
    return 1
  for b in data:
    devPerc = b / med
    mads.append((1 - devPerc))
  return max(mads)
