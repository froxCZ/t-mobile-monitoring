import datetime
import logging

import pytz

from common import AppConfig
from common import util
from mediation import MediationConfig
from mediation.flow_analyzer.OutageDetector import OutageDetector
from mediation.flow_analyzer.OutlierDetector import OutlierDetector

utc = pytz.timezone("UTC")


class FlowAnalyzer:
  def __init__(self, flow, granularity=None):
    super().__init__()
    self.flow = flow
    self.options = flow["options"]
    if granularity is None:
      self.granularity = self.options["granularity"]
    else:
      self.granularity = granularity
    self.outlierDetector = OutlierDetector(self.flow, self.granularity)
    self.precomputedData = {}
    self.outageDetector = OutageDetector(self.flow, self.granularity)

  def run(self, time):
    latestCompleteTicTime = self._getLatestCompleteTicTime(time)
    self.status = self.outageDetector.getStatus(latestCompleteTicTime)
    self.difference = self.outageDetector.difference
    self.ticTime = latestCompleteTicTime
    assert self.difference is not None

    return 0

  def _getLatestCompleteTicTime(self, time):
    granularity = self.granularity
    minuteOfDay = time.hour * 60 + time.minute
    minutesOverInterval = minuteOfDay % granularity
    if granularity == 60:
      latestClosedIntervalTime = time - datetime.timedelta(minutes=minutesOverInterval + granularity)
      latestClosedIntervalTime = latestClosedIntervalTime.replace(second=0, microsecond=0)
      return util.getTicTime(latestClosedIntervalTime.astimezone(AppConfig.getTimezone()), granularity)
    else:
      naiveTime = time.replace(tzinfo=None)
      latestClosedIntervalNaiveTime = naiveTime - datetime.timedelta(minutes=minutesOverInterval + granularity)
      latestClosedIntervalNaiveTime = latestClosedIntervalNaiveTime.replace(second=0, microsecond=0)
      localized = AppConfig.getTimezone().localize(latestClosedIntervalNaiveTime).astimezone(AppConfig.getTimezone())
      return util.getTicTime(localized, granularity)

  def getResult(self):
    """
    returns result. It's up to caller to save it to db!
    :return:
    """
    return self.status, self.difference

  def setPrecomputedData(self, precomputedData):
    self.precomputedData = precomputedData
    self.outageDetector.setPrecomputedData(self.precomputedData)


if __name__ == "__main__":
  logging.basicConfig(format='%(levelname)s [%(module)s]: %(message)s', level=logging.DEBUG)
  gsm = MediationConfig.getLobWithCountry("CZ", "TIT")
  analyzer = FlowAnalyzer(gsm["flows"]["CLH"])
  analyzer.run(util.stringToTime("17.01.2017 15:00:00"))
  isOutage, traffic = analyzer.getResult()
  print(isOutage)
  print(traffic)
