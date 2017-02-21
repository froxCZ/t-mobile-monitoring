import traceback

from scipy.stats import linregress

from api.data_query import MongoQueryExecutor
from config import config


def _correlate2Lobs(lobName1, lobName2, granularity=0):
  lobConfig1 = config.getLobConfigByName(lobName1)
  lobConfig2 = config.getLobConfigByName(lobName2)
  if granularity is 0:
    if (lobConfig1.granularity < lobConfig2.granularity - 60):
      return -1
    granularity = max(lobConfig1.granularity, lobConfig2.granularity)
  import api.util as util
  fromDate = util.jsStringToDate("2016-10-24T10:00:00.000Z")
  toDate = util.jsStringToDate("2016-10-31T10:00:00.000Z")

  lob1Query = MongoQueryExecutor(fromDate, toDate, [lobName1], granularity)
  lob2Query = MongoQueryExecutor(fromDate, toDate, [lobName2], granularity)
  lob1Data, metricsList = lob1Query.execute()
  lob1Data = util.dateDataListToList(lob1Data, metricsList[0])

  lob2Data, metricsList = lob2Query.execute()
  lob2Data = util.dateDataListToList(lob2Data, metricsList[0])
  lin = linregress(lob1Data, lob2Data)
  return lin.rvalue


def getBestCorrelations(lobName, correlationThreshold=0.9, granularity=0):
  lobConfig = config.getLobConfigByName(lobName)
  otherLobs = config.getLobsConfig()["lobs"][lobConfig.country]
  resArr = []
  for lob in otherLobs:
    fullLobName = lobConfig.country + "." + lob
    if lobName == fullLobName:
      continue
    try:
      correlation = _correlate2Lobs(lobName, fullLobName, granularity)
      dayCorrelation = _correlate2Lobs(lobName, fullLobName, 1440) #lobs show have same workday/weekend changes
      resArr.append((fullLobName, correlation,dayCorrelation))
    except:
      traceback.print_exc()
      pass
  resArr = [x for x in resArr if x[1] >= correlationThreshold and x[2]>=correlationThreshold]
  resSorted = sorted(resArr, key=lambda x: x[1], reverse=True)
  return map(lambda x: {"lobName": x[0], "correlation": (x[1]+x[2])/2}, resSorted)
