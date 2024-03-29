from mediation import data_query
from mediation.flow_analyzer import status


class OutlierDetector():
  """
  Detects whether the traffic is significantly lower than expected value.
  """
  def __init__(self, flow, granularity=0):
    super().__init__()
    self.flow = flow
    self.granularity = granularity

  def getOutlierType(self, ticTraffic):
    flowLevel = data_query.calculateFlowLevelDifference(ticTraffic["value"],
                                                        ticTraffic["expected"],
                                                        ticTraffic["dayAverage"])
    options = self.flow["options"]
    differenceType = options["difference"] + "Difference"  # use relative or scaled, based on config
    # todo use lazy days to lower alarm based on config
    hardLevel = self.flow["options"]["hardAlarmLevel"]
    softLevel = self.flow["options"]["softAlarmLevel"]
    self.difference = flowLevel[differenceType]
    if self.difference < hardLevel:
      return status.OUTAGE
    elif self.difference < softLevel:
      return status.WARNING
    else:
      return status.OK
