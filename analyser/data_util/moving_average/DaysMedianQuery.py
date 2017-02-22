from statistics import median


class DaysMedianQuery:
  def __init__(self, dates, lobName):
    self.dates = dates
    self.lobName = lobName

  def execute(self):
    from api.data_query import DatesQuery
    data = DatesQuery(self.dates, self.lobName, "value").execute()[0]
    return _createMeans(data,"value")


def _createMeans(data, valueName):
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
