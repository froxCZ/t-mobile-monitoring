def calculateFlowLevelDifference(flowValue, expected, dayAverage):
  """
  calculates relative and scaled difference between flow value and expected value
  :param flowValue:
  :param expected:
  :param dayAverage:
  :return:
  """
  tickDifference = 1
  dayDifference = 1
  if flowValue != expected:
    diff = flowValue - expected
    tickDifference = min(flowValue / max(expected, 0.1), 3)
    if dayAverage != 0:
      if tickDifference >= 0.1:
        scaledDiff = min((diff / dayAverage) + 1, 3)
        if scaledDiff >= 1 and tickDifference >= 1:
          dayDifference = min(scaledDiff, tickDifference)
        else:
          dayDifference = max(scaledDiff, tickDifference)
      else:
        dayDifference = tickDifference
    else:
      dayDifference = 1
  dayDifference = round(dayDifference, 3)
  tickDifference = round(tickDifference, 3)
  resulttic = {}
  resulttic["tickDifference"] = tickDifference
  resulttic["dayDifference"] = dayDifference
  return resulttic


if __name__ == "__main__":
  result = calculateFlowLevelDifference(13545666,11267818,140230789)
  print(result)
