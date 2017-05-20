import matplotlib.pyplot as plt

import util
from mediation import MediationConfig
from mediation import data_query

fromDate = util.stringToDate("21.12.2016")
toDate = util.stringToDate("30.12.2016")
lobName = "GSM"
flowName = "MSSBRN1A"
lob = MediationConfig.getLobWithCountry("CZ", lobName)
flow = lob["flows"][flowName]
flows = [flow]
granularity = 60

response = {}
mongoQuery = data_query.DateRangeGroupQuery(fromDate, toDate, flows, granularity=granularity)
data = mongoQuery.execute()
metrics = {}
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
dayDifference = util.dateDataListToList(data, "dayDifference")
tickDifference = util.dateDataListToList(data, "tickDifference")
dataTicks = []
dataTickPos = []
for i in range(0, len(dates)):
  if i % 12 == 0:
    dataTicks.append(dates[i])
    dataTickPos.append(i)

plt.figure(figsize=(12, 9))

plt.subplot(211)
plt.xticks(dataTickPos, dataTicks, rotation=25)
plt.plot(data1, color="red", linewidth=2, label="actual")
plt.plot(expected, color="blue", label="expected")
plt.plot(util.dateDataListToList(data, "dayAverage"), color="orange", label="day average")
plt.title(lobName + "-" + flowName + " traffic")
plt.legend(loc='upper right')

plt.subplot(212)
plt.xticks(dataTickPos, dataTicks, rotation=25)
plt.title(lobName + "-" + flowName + " difference")
plt.plot(dayDifference, '#ff009f', linewidth=2, label="day difference")
plt.plot(tickDifference, 'gray', label="tick difference")
plt.plot([1 for x in range(0, len(dayDifference))], 'black')
plt.plot([0.8 for x in range(0, len(dayDifference))], 'orange')
plt.plot([0.5 for x in range(0, len(dayDifference))], 'red')
plt.tight_layout()
plt.legend(loc='lower left')
plt.show()
