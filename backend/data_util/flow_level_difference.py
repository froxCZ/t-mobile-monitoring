def calculateFlowLevelDifference(flowValue, expected, dayAverage):
  """
  calculates relative and scaled difference between flow value and expected value
  :param flowValue:
  :param expected:
  :param dayAverage:
  :return:
  """
  relativeDifference = 1
  scaledDifference = 1
  if flowValue != expected:
    diff = flowValue - expected
    relativeDifference = min(flowValue / max(expected, 0.1), 3)
    if dayAverage != 0:
      if relativeDifference >= 0.1:
        scaledDiff = min((diff / dayAverage) + 1, 3)
        if scaledDiff >= 1 and relativeDifference >= 1:
          scaledDifference = min(scaledDiff, relativeDifference)
        else:
          scaledDifference = max(scaledDiff, relativeDifference)
      else:
        scaledDifference = relativeDifference
    else:
      scaledDifference = 1
  scaledDifference = round(scaledDifference, 3)
  relativeDifference = round(relativeDifference, 3)
  resultTick = {}
  resultTick["relativeDifference"] = relativeDifference
  resultTick["scaledDifference"] = scaledDifference
  return resultTick
