import datetime

import data_query
from lob_analyzer.OutlierDetector import OutlierDetector


class OutageDetector():
  def __init__(self, flow):
    super().__init__()
    self.flow = flow
    self.outlierDetector = OutlierDetector(self.flow)

  def isOutage(self, tickTraffic):
    outlierType = self.outlierDetector.getOutlierType(tickTraffic)
    if outlierType == OutlierDetector.NO_OUTLIER:
      return False
    if outlierType == OutlierDetector.HARD_OUTLIER:
      return True

    tickTime = tickTraffic["_id"]
    previousTickTime = tickTime - datetime.timedelta(minutes=self.flow["options"]["granularity"])
    previousTickTraffic = data_query.TickTrafficQuery(previousTickTime, self.flow).execute()
    previousOutlierType = self.outlierDetector.getOutlierType(previousTickTraffic)
    if previousOutlierType == OutlierDetector.NO_OUTLIER:
      return False
    else:
      return True
