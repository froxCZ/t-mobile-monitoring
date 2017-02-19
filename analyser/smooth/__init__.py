from smooth.smooth_fnc import savitzky


def smoothData(granularity, data):
  windowSize, order = _granularityToWindowSizeAndOrder(granularity)
  smoothed = savitzky(data, window_size=windowSize, order=order)
  smoothed[smoothed < 0] = 0 #negative values replace with 0
  return smoothed

def _granularityToWindowSizeAndOrder(granularity):
  if granularity <= 15:
    return (51, 9)
  if granularity <= 30:
    return (29, 9)
  if granularity <= 60:
    return (13, 9)
  if granularity <= 120:
    return (11, 9)
  if granularity <= 240:
    return (9, 7)
  return (5, 3)
