import datetime

import data_query
from mediation.flow_analyzer import status
from mediation.flow_analyzer.OutlierDetector import OutlierDetector


class OutageDetector():
  def __init__(self, flow):
    super().__init__()
    self.flow = flow
    self.outlierDetector = OutlierDetector(self.flow)
    self.precomputedData = {}

  def getStatus(self, ticTime):
    ticTraffic = self.getticTraffic(ticTime)
    outlierType = self.outlierDetector.getOutlierType(ticTraffic)
    self.difference = self.outlierDetector.difference
    if outlierType == status.OK:
      return status.OK
    if outlierType == status.OUTAGE:
      return status.OUTAGE

    ticTime = ticTraffic["_id"]
    previousticTime = ticTime - datetime.timedelta(minutes=self.flow["options"]["granularity"])
    previousticTraffic = self.getticTraffic(previousticTime)
    previousOutlierType = self.outlierDetector.getOutlierType(previousticTraffic)
    if previousOutlierType == status.OK:
      return status.WARNING
    else:
      return status.OUTAGE

  def getticTraffic(self, ticTime):
    if ticTime in self.precomputedData:
      return self.precomputedData[ticTime]
    else:
      return data_query.TicTrafficQuery(ticTime, self.flow).execute()

  def setPrecomputedData(self, precomputedData):
    self.precomputedData = precomputedData
