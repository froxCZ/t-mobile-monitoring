import math
import traceback

import simplejson as simplejson
from numpy import sum, arange
from pylab import pcolor, show, colorbar, xticks, yticks
from scipy.stats import linregress

from api.data_query import MongoQueryExecutor
from config import config

CZ_LOBS = config.getLobsConfig()["lobs"]["CZ"]
# CZ_LOBS = ["SMS","GSM","MMS"]


def correlate2Lobs(lobName1, lobName2):
  lobConfig1 = config.getLobConfigByName(lobName1)
  lobConfig2 = config.getLobConfigByName(lobName2)
  if (lobConfig1.granularity < lobConfig2.granularity - 60):
    return -1,0
  granularity = max(lobConfig1.granularity, lobConfig2.granularity)
  import api.util as util
  fromDate = util.jsStringToDate("2016-10-03T10:00:00.000Z")
  toDate = util.jsStringToDate("2016-10-10T10:00:00.000Z")

  lob1Query = MongoQueryExecutor(fromDate, toDate, lobName1, granularity)
  lob2Query = MongoQueryExecutor(fromDate, toDate, lobName2, granularity)
  lob1Data, metricsList = lob1Query.execute()
  lob1Data = util.dateDataListToList(lob1Data, metricsList[0])

  lob2Data, metricsList = lob2Query.execute()
  lob2Data = util.dateDataListToList(lob2Data, metricsList[0])
  lin = linregress(lob1Data, lob2Data)
  # cosineSimilarity = cosine_similarity(lob1Data, lob2Data)
  return lin.rvalue, 0


def cosine_similarity(a, b):
  return sum([i * j for i, j in zip(a, b)]) / (math.sqrt(sum([i * i for i in a])) * math.sqrt(sum([i * i for i in b])))


def getBestCorrelations(lobName):
  mainLobConfig = config.getLobConfigByName(lobName)
  country = mainLobConfig.country
  countryLobs = CZ_LOBS
  resArr = []
  for lob in countryLobs:
    fullLobName = country + "." + lob
    try:
      correlation = correlate2Lobs(lobName, fullLobName)
      resArr.append((fullLobName, correlation[0]))
    except:
      traceback.print_exc()
      pass
  resSorted = sorted(resArr, key=lambda x: x[1], reverse=True)
  return resSorted


#
CZ_LOBS = sorted(CZ_LOBS)
results = []
map = {}
for lob in CZ_LOBS:
  fullName = "CZ." + lob
  result = getBestCorrelations(fullName)
  result = sorted(result, key=lambda x: x[0])
  results.append(result)
  map[fullName] = {}
  for cor in result:
    map[fullName][cor[0]]=cor[1]
  print(fullName + ": " + str(result))

print(simplejson.dumps(map))



# generating some uncorrelated data
# data = rand(10,100) # each row of represents a variable
# print(data)
#
# # creating correlation between the variables
# # variable 2 is correlated with all the other variables
# data[2,:] = sum(data,0)
# # variable 4 is correlated with variable 8
# data[4,:] = log(data[8,:])*0.5

# plotting the correlation matrix
print(results)
data = results
R = data#corrcoef(data)
print(R)
pcolor(R)
colorbar()
yticks(arange(0.5, len(CZ_LOBS)+0.5), CZ_LOBS)
xticks(arange(0.5, len(CZ_LOBS)+0.5), CZ_LOBS)
show()
