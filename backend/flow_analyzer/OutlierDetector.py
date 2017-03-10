import data_util


class OutlierDetector():
  NO_OUTLIER = 0
  SOFT_OUTLIER = 1
  HARD_OUTLIER = 2

  def __init__(self, flow):
    super().__init__()
    self.flow = flow

  def getOutlierType(self, ticTraffic):
    flowLevel = data_util.calculateFlowLevelDifference(ticTraffic["value"],
                                                       ticTraffic["expected"],
                                                       ticTraffic["dayAverage"])
    options = self.flow["options"]
    differenceType = options["difference"] + "Difference"  # use relative or scaled, based on config
    # todo use lazy days to lower alarm based on config
    hardLevel = self.flow["options"]["hardAlarmLevel"]
    softLevel = self.flow["options"]["softAlarmLevel"]
    flowLevelDifference = flowLevel[differenceType]
    if flowLevelDifference < hardLevel:
      return self.HARD_OUTLIER
    elif flowLevelDifference < softLevel:
      return self.SOFT_OUTLIER
    else:
      return self.NO_OUTLIER
