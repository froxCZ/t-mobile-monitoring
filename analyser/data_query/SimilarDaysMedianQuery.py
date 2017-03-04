from statistics import median


class SimilarDaysMedianQuery:
  def __init__(self, lobNames, date, granularity=0, neids=[], forwards=[]):
    from data_util.moving_average import DayGenerator
    self.lobNames = lobNames
    self.neids = neids
    self.forwards = forwards
    self.date = date
    self.granularity = granularity
    self.dates = DayGenerator.getPastSimilarDays(self.lobNames, date)
    if len(lobNames) > 1:
      raise Exception("only one lob name can be specified")
    if len(neids) + len(forwards) > 1:
      raise Exception("only one neid or forward can be specified")

  def execute(self):
    from data_query.DatesQuery import DatesQuery
    datesQuery = DatesQuery(self.dates, self.lobNames,
                            granularity=self.granularity,
                            neids=self.neids,
                            forwards=self.forwards)
    data = datesQuery.execute()
    self.metadata = datesQuery.metadata
    self.metrics = datesQuery.metrics
    # _createWeightedMeans(data,"value")
    return _createMedians(data, datesQuery.metrics[0])


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
