from common import config
from common import util
from mediation.api


class OutlierDetector:
  def __init__(self, lobName, dateTime):
    self.lobName = lobName
    self.lobConfig = config.getLobConfigByName(lobName)
    self.granularity = self.lobConfig.granularity
    self.dateTime = dateTime

  def _getMedians(self):
    from mediation.data_query import ExpectedTrafficQuery
    return ExpectedTrafficQuery(self.lobName,self.dateTime).execute()

  def _getCurrentData(self):
    from mediation.data_query import DatesQuery
    datesQuery = DatesQuery([self.dateTime], self.lobName, resultName="value");
    data = datesQuery.execute()
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
