import datetime

import data_query
from flow_analyzer.OutlierDetector import OutlierDetector


class OutageDetector():
  def __init__(self, flow):
    super().__init__()
    self.flow = flow
    self.outlierDetector = OutlierDetector(self.flow)
    self.precomputedData = {}

  def isOutage(self, tickTime):
    tickTraffic = self.getTickTraffic(tickTime)
    outlierType = self.outlierDetector.getOutlierType(tickTraffic)
    if outlierType == OutlierDetector.NO_OUTLIER:
      return False
    if outlierType == OutlierDetector.HARD_OUTLIER:
      return True

    tickTime = tickTraffic["_id"]
    previousTickTime = tickTime - datetime.timedelta(minutes=self.flow["options"]["granularity"])
    previousTickTraffic = self.getTickTraffic(previousTickTime)
    previousOutlierType = self.outlierDetector.getOutlierType(previousTickTraffic)
    if previousOutlierType == OutlierDetector.NO_OUTLIER:
      return False
    else:
      return True

  def getTickTraffic(self, tickTime):
    if tickTime in self.precomputedData:
      return self.precomputedData[tickTime]
    else:
      return data_query.TickTrafficQuery(tickTime, self.flow).execute()

  def setPrecomputedData(self, precomputedData):
    self.precomputedData = precomputedData
