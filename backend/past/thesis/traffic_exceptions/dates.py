import matplotlib.pyplot as plt

import util
from mediation import MediationConfig
from mediation import data_query


def getData(flows, fromDate, toDate):
  flow = flows[0]
  flowName = flow["name"]
  mongoQuery = data_query.DateRangeGroupQuery(fromDate, toDate, flows, granularity=granularity)
  data = mongoQuery.execute()
  metricsList = mongoQuery.metrics
  metadata = mongoQuery.metadata
  if len(flows) == 1:
    metric = metricsList[0]
    flowLevelQuery = data_query.FlowLevelDateRangeQuery(fromDate, toDate, flows, metadata["granularity"], data)
    flowLevelData = flowLevelQuery.execute()
    data = util.merge2DateLists(flowLevelData, None, data, None)
    metricsList.extend(flowLevelQuery.metrics)
    outageQuery = data_query.OutageDateRangeQuery(fromDate, toDate, flows[0], metadata["granularity"])
    outageQuery.setPrecomputedData(data, metric)
    outageList = outageQuery.execute()
    data = util.merge2DateLists(outageList, [outageQuery.metric], data, None)
    metricsList.append(outageQuery.metric)

  dates = list(
    map(lambda x: x.strftime("%d.%m %H:%M"), util.dateDataListToList(data, "_id")))
  data1 = util.dateDataListToList(data, flowName)
  expected = util.dateDataListToList(data, "expected")
  dataTicks = []
  dataTickPos = []
  for i in range(0, len(dates)):
    if True:
      dataTicks.append(dates[i])
      dataTickPos.append(i)
  return data1, expected, dataTicks, dataTickPos


fromDate = util.stringToDate("30.01.2017")
toDate = util.stringToDate("12.02.2017")
# lobName = "ICG"
# flowName = "CENTREX01"
lobName = "GSM"
flowName = "MSSBRN1B"
lob = MediationConfig.getLobWithCountry("CZ", lobName)
flow = lob["flows"][flowName]
flows = [flow]
granularity = 240

data = []
expected = []
ticks = []
pos = []
d, e, t, p = getData(flows, util.stringToDate("28.09.2016"), util.stringToDate("29.09.2016"))
data += d
expected += e
ticks += t
posLen = len(pos)
pos += [i + posLen for i in p]
d, e, t, p = getData(flows, util.stringToDate("28.10.2016"), util.stringToDate("29.10.2016"))
data += d
expected += e
ticks += t
posLen = len(pos)
pos += [i + posLen for i in p]
d, e, t, p = getData(flows, util.stringToDate("17.11.2016"), util.stringToDate("18.11.2016"))
data += d
expected += e
ticks += t
posLen = len(pos)
pos += [i + posLen for i in p]
plt.figure(figsize=(12, 6))
plt.plot(data, color="red", label=lobName + "-" + flowName)
plt.plot(expected, color="blue", label="weekend median")
plt.xticks(pos, ticks, rotation=25)
plt.title(lobName + "-" + flowName + "")
plt.legend(loc='lower right')
plt.show()
