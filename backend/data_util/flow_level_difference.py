def calculateFlowLevelDifference(flowValue, expected, dayAverage):
  """
  calculates relative and scaled difference between flow value and expected value
  :param flowValue:
  :param expected:
  :param dayAverage:
  :return:
  """
  flowDifference = 1
  normalizedDifference = 1
  if flowValue != expected:
    diff = flowValue - expected
    flowDifference = min(flowValue / max(expected, 0.1), 3)
    if dayAverage != 0:
      if flowDifference >= 0.1:
        scaledDiff = min((diff / dayAverage) + 1, 3)
        if scaledDiff >= 1 and flowDifference >= 1:
          normalizedDifference = min(scaledDiff, flowDifference)
        else:
          normalizedDifference = max(scaledDiff, flowDifference)
      else:
        normalizedDifference = flowDifference
    else:
      normalizedDifference = 1
  normalizedDifference = round(normalizedDifference, 3)
  flowDifference = round(flowDifference, 3)
  resultTick = {}
  resultTick["flowDifference"] = flowDifference
  resultTick["normalizedDifference"] = normalizedDifference
  return resultTick
