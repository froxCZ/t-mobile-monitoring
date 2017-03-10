import datetime
import logging

import config
import util
from flow_analyzer.OutageDetector import OutageDetector
from flow_analyzer.OutlierDetector import OutlierDetector


class FlowAnalyzer:
  def __init__(self, flow):
    super().__init__()
    self.flow = flow
    self.options = flow["options"]
    self.outlierDetector = OutlierDetector(self.flow)
    self.precomputedData = {}
    self.outageDetector = OutageDetector(self.flow)

  def run(self, time):
    logging.info("analyzing " + self.flow["name"])
    latestCompleteTicTime = self._getLatestCompleteTicTime(time)
    self.status = self.outageDetector.getStatus(latestCompleteTicTime)
    self.difference = self.outageDetector.difference
    self.ticTime = latestCompleteTicTime
    assert self.difference is not None

    return 0

  def _getLatestCompleteTicTime(self, time):
    granularity = self.options["granularity"]
    minuteOfDay = time.hour * 60 + time.minute
    minutesOverInterval = minuteOfDay % granularity
    latestClosedIntervalTime = time - datetime.timedelta(minutes=minutesOverInterval)
    latestClosedIntervalTime = latestClosedIntervalTime.replace(second=0, microsecond=0)
    return latestClosedIntervalTime

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
  gsm = config.getLobConfig("CZ_BVS")
  analyzer = FlowAnalyzer(gsm["flows"]["BVSCTX"])
  analyzer.run(util.stringToTime("01.01.2017 11:00:00"))
  isOutage, traffic = analyzer.getResult()
  print(isOutage)
  print(traffic)
