import traceback

from scipy.stats import linregress

from api.data_query import DateRangeGroupQuery
from config import config



def _correlate2Lobs(lobName1, lobName2,granularity=0):
  lobConfig1 = config.getLobConfigByName(lobName1)
  lobConfig2 = config.getLobConfigByName(lobName2)
  if granularity is 0:
    if (lobConfig1.granularity < lobConfig2.granularity - 60):
      return -1
    granularity = max(lobConfig1.granularity, lobConfig2.granularity)
  import api.util as util

  fromDate = util.jsStringToDate("2016-10-28T10:00:00.000Z")
  toDate = util.jsStringToDate("2016-10-29T10:00:00.000Z")
  lob1Query = DateRangeGroupQuery(fromDate, toDate, [lobName1], granularity)
  lob2Query = DateRangeGroupQuery(fromDate, toDate, [lobName2], granularity)
  lob1Data = lob1Query.execute()[0]
  lob2Data = lob2Query.execute()[0]

  fromDate = util.jsStringToDate("2016-10-25T10:00:00.000Z")
  toDate = util.jsStringToDate("2016-10-26T10:00:00.000Z")
  lob1Query = DateRangeGroupQuery(fromDate, toDate, [lobName1], granularity)
  lob2Query = DateRangeGroupQuery(fromDate, toDate, [lobName2], granularity)
  lob1Data.extend(lob1Query.execute()[0])
  lob2Data.extend(lob2Query.execute()[0])

  lob1Data = util.dateDataListToList(lob1Data,lobName1.replace(".", "_"))
  lob2Data = util.dateDataListToList(lob2Data,lobName2.replace(".", "_"))

  lin = linregress(lob1Data, lob2Data)
  return lin.rvalue

def getBestCorrelations(lobName, correlationThreshold=0.9,granularity=0):
  lobConfig = config.getLobConfigByName(lobName)
  otherLobs = config.getLobsConfig()["lobs"][lobConfig.country]
  resArr = []
  for lob in otherLobs:
    fullLobName = lobConfig.country + "." + lob
    if lobName == fullLobName:
      continue
    try:
      correlation = _correlate2Lobs(lobName, fullLobName,granularity)
      resArr.append((fullLobName, correlation))
    except:
      traceback.print_exc()
      pass
  resArr = [x for x in resArr if x[1] >= correlationThreshold]
  resSorted = sorted(resArr, key=lambda x: x[1], reverse=True)
  return list(map(lambda x:{"lobName":x[0],"correlation":x[1]},resSorted))


x = getBestCorrelations("CZ.MMS")
print(x)