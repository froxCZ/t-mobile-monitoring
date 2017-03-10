import datetime

import data_query
from flow_analyzer.OutlierDetector import OutlierDetector


class OutageDetector():
  def __init__(self, flow):
    super().__init__()
    self.flow = flow
    self.outlierDetector = OutlierDetector(self.flow)
    self.precomputedData = {}

  def isOutage(self, ticTime):
    ticTraffic = self.getticTraffic(ticTime)
    outlierType = self.outlierDetector.getOutlierType(ticTraffic)
    if outlierType == OutlierDetector.NO_OUTLIER:
      return False
    if outlierType == OutlierDetector.HARD_OUTLIER:
      return True

    ticTime = ticTraffic["_id"]
    previousticTime = ticTime - datetime.timedelta(minutes=self.flow["options"]["granularity"])
    previousticTraffic = self.getticTraffic(previousticTime)
    previousOutlierType = self.outlierDetector.getOutlierType(previousticTraffic)
    if previousOutlierType == OutlierDetector.NO_OUTLIER:
      return False
    else:
      return True

  def getticTraffic(self, ticTime):
    if ticTime in self.precomputedData:
      return self.precomputedData[ticTime]
    else:
      return data_query.TicTrafficQuery(ticTime, self.flow).execute()

  def setPrecomputedData(self, precomputedData):
    self.precomputedData = precomputedData
