import datetime
import logging

import config
import data_query
import util
from lob_analyzer.OutageDetector import OutageDetector
from lob_analyzer.OutlierDetector import OutlierDetector


class LobAnalyzer:
  def __init__(self, flow, time):
    super().__init__()
    self.flow = flow
    self.options = flow["options"]
    self.outlierDetector = OutlierDetector(self.flow)
    self.time = time

  def run(self):
    logging.info("analyzing " + self.flow["name"])
    latestCompleteIntervalTime = self._getLatestCompleteIntervalTime(self.time)
    tickTraffic = data_query.TickTrafficQuery(latestCompleteIntervalTime, self.flow).execute()
    outageDetector = OutageDetector(self.flow)
    self.isOutage = outageDetector.isOutage(tickTraffic)
    self.tickTraffic = tickTraffic

    return 0

  def _getLatestCompleteIntervalTime(self, time):
    granularity = self.options["granularity"]
    minuteOfDay = time.hour * 60 + time.minute
    minutesOverInterval = minuteOfDay % granularity
    latestClosedIntervalTime = time - datetime.timedelta(minutes=minutesOverInterval + granularity)
    latestClosedIntervalTime = latestClosedIntervalTime.replace(second=0, microsecond=0)
    return latestClosedIntervalTime

  def getResult(self):
    """
    returns result. It's up to caller to save it to db!
    :return:
    """
    return self.isOutage, self.tickTraffic


if __name__ == "__main__":
  logging.basicConfig(format='%(levelname)s [%(module)s]: %(message)s', level=logging.DEBUG)
  gsm = config.getLobConfig("CZ_BVS")
  analyzer = LobAnalyzer(gsm["flows"]["BVSCTX"], util.stringToTime("27.12.2016 11:00:00"))
  analyzer.run()
  isOutage, traffic = analyzer.getResult()
  print(isOutage)
  print(traffic)
