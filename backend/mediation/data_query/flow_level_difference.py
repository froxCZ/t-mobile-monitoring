def calculateFlowLevelDifference(flowValue, expected, dayAverage):
  """
  calculates relative and scaled difference between flow value and expected value
  :param flowValue:
  :param expected:
  :param dayAverage:
  :return:
  """
  ticDifference = 1
  dayDifference = 1
  if flowValue != expected:
    diff = flowValue - expected
    ticDifference = min(flowValue / max(expected, 0.1), 3)
    if dayAverage != 0:
      if ticDifference >= 0.1:
        scaledDiff = min((diff / dayAverage) + 1, 3)
        if scaledDiff >= 1 and ticDifference >= 1:
          dayDifference = min(scaledDiff, ticDifference)
        else:
          dayDifference = max(scaledDiff, ticDifference)
      else:
        dayDifference = ticDifference
    else:
      dayDifference = 1
  dayDifference = round(dayDifference, 3)
  ticDifference = round(ticDifference, 3)
  resulttic = {}
  resulttic["ticDifference"] = ticDifference
  resulttic["dayDifference"] = dayDifference
  return resulttic
