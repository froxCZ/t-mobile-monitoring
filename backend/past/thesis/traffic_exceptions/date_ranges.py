import matplotlib.pyplot as plt

import util
from mediation import MediationConfig
from mediation import data_query

# fromDate1 = util.stringToTime("28.10.2016 00:00:00")
# toDate1 = util.stringToTime("29.10.2016 00:00:00")
# fromDate2 = util.stringToTime("21.10.2016 00:00:00")
# toDate2 = util.stringToTime("22.10.2016 00:00:00")
# fromDate3 = util.stringToTime("17.10.2016 00:00:00")
# toDate3 = util.stringToTime("18.10.2016 00:00:00")
# granularity = 60
# lob = MediationConfig.getLobWithCountry("CZ", "SMS")
# flowName = "SMSCCTX"
# flow = lob["flows"][flowName]
#
# q1 = DateRangeGroupQuery(fromDate1, toDate1, [flow], granularity)
# q2 = DateRangeGroupQuery(fromDate2, toDate2, [flow], granularity)
# q3 = DateRangeGroupQuery(fromDate3, toDate3, [flow], granularity)
# lob1Data = util.dateDataListToList(q1.execute(), flowName)
# lob2Data = util.dateDataListToList(q2.execute(), flowName)
# lob3Data = util.dateDataListToList(q3.execute(), flowName)
#
# ticks = util.dateDataListToList(q1.execute(), "_id")
# plt.figure(figsize=(12, 6))
# plt.plot(lob2Data, color="blue", label="21.10")
# plt.plot(lob1Data, color="red", label="27.10")
# plt.plot(lob3Data, color="green", label="17.11")
#
# #plt.xticks(ticks, rotation='vertical')
# plt.title(flowName)
# plt.legend(loc='upper left')
# plt.show()


fromDate = util.stringToDate("30.01.2017")
toDate = util.stringToDate("12.02.2017")
lobName = "GGS"
flowName = "BIEL5"
lob = MediationConfig.getLobWithCountry("DE", lobName)
flow = lob["flows"][flowName]
flows = [flow]
granularity = 240

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
dataTicks = []
dataTickPos = []
for i in range(0, len(dates)):
  if i % 7 == 0:
    dataTicks.append(dates[i])
    dataTickPos.append(i)

plt.figure(figsize=(12, 6))
plt.plot(data1, color="red", label=lobName+"-" +flowName)
plt.plot(expected, color="blue", label="expected")
plt.xticks(dataTickPos, dataTicks, rotation=25)
plt.title(lobName+"-" +flowName+"")
plt.legend(loc='lower right')
plt.show()