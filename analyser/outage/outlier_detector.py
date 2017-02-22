from api import util
from config import config


class OutlierDetector:
  def __init__(self, lobName, dateTime):
    self.lobName = lobName
    self.lobConfig = config.getLobConfigByName(lobName)
    self.granularity = self.lobConfig.granularity
    self.dateTime = dateTime

  def _getMedians(self):
    from data_util.moving_average import DayGenerator
    pastDays = DayGenerator.getPastSimilarDays(self.lobName, self.dateTime)
    from data_util.moving_average import DaysMedianQuery
    return DaysMedianQuery(pastDays, self.lobName).execute()

  def _getCurrentData(self):
    from api.data_query import DatesQuery
    data = DatesQuery([self.dateTime], self.lobName, resultName="value").execute()[0]
    return util.listToDayMinutes(data)

  def getOutageStatus(self):
    currentData = self._getCurrentData()
    medianData = self._getMedians()
    currentMinute = util.dateToDayMinutes(self.dateTime)
    roundedMinute = int(currentMinute / self.granularity) \
                    * self.granularity  # rounded by granularity on last completed interval
    # roundedDate = self.dateTime.replace(hour=int(roundedMinute/60), minute=roundedMinute%60)
    percentageLevel0 = currentData[roundedMinute] / medianData[roundedMinute]
    percentageLevel1 = currentData[roundedMinute - self.granularity] / medianData[roundedMinute - self.granularity]

    print(percentageLevel0)
    print(percentageLevel1)
