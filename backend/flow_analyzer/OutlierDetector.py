import data_util


class OutlierDetector():
  NO_OUTLIER = 0
  SOFT_OUTLIER = 1
  HARD_OUTLIER = 2

  def __init__(self, flow):
    super().__init__()
    self.flow = flow

  def getOutlierType(self, tickTraffic):
    flowLevel = data_util.calculateFlowLevelDifference(tickTraffic["value"],
                                                       tickTraffic["expected"],
                                                       tickTraffic["dayAverage"])
    ##todo use relative or scaled, based on config
    # todo use lazy days to lower alarm based on config
    hardLevel = self.flow["options"]["hardAlarmLevel"]
    softLevel = self.flow["options"]["softAlarmLevel"]
    flowLevelDifference = flowLevel["normalizedDifference"]
    if flowLevelDifference < hardLevel:
      return self.HARD_OUTLIER
    elif flowLevelDifference < softLevel:
      return self.SOFT_OUTLIER
    else:
      return self.NO_OUTLIER
