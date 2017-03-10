import data_util
import flow_analyzer.status as status

class OutlierDetector():

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
      return status.OUTAGE
    elif flowLevelDifference < softLevel:
      return status.WARNING
    else:
      return status.OK
