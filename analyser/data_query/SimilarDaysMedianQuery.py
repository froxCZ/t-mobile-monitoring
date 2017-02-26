from statistics import median


class SimilarDaysMedianQuery:
  def __init__(self, lobName, date, granularity=0):
    from data_util.moving_average import DayGenerator
    self.lobName = lobName
    self.date = date
    self.granularity = granularity
    self.dates = DayGenerator.getPastSimilarDays(self.lobName, date)

  def execute(self):
    from data_query.DatesQuery import DatesQuery
    print(self.date)
    datesQuery = DatesQuery(self.dates, self.lobName, resultName="value", granularity=self.granularity)
    data = datesQuery.execute()
    self.metadata = datesQuery.metadata
    self.metrics = datesQuery.metrics
    return _createMedians(data, "value")


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
    print(str(len(valueList)))
    n = 2
    valueList = valueList[n:-n]
    print(str(len(valueList)))
    print()
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
    dayMedians[minute] = median(valueList)
  return dayMedians


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
