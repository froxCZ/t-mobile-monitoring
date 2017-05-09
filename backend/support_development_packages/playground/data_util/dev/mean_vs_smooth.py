import statistics as s

import matplotlib.pyplot as plt
import numpy
from support_development_packages.smooth import smoothData

import util
from mediation import MediationConfig
from mediation.data_query import DateRangeGroupQuery


def running_mean(l, N):
  sum = 0
  result = list(0 for x in l)

  for i in range(0, N):
    sum = sum + l[i]
    result[i] = sum / (i + 1)

  for i in range(N, len(l)):
    sum = sum - l[i - N] + l[i]
    result[i] = sum / N

  return result


def movingAverage(interval, window_size):
  window = numpy.ones(int(window_size)) / float(window_size)
  return numpy.convolve(interval, window, 'same')

def cumulativeRunningMedian(data, window_size):
  output = []
  for i in range(0,len(data)):
    start = max(0,i-window_size)
    windowData = data[start:i+1]
    mean = s.median(windowData)
    output.append(mean)
  return output

def cumulativeRunningMean(data, window_size):
  output = []
  for i in range(0,len(data)):
    start = max(0,i-window_size)
    windowData = data[start:i+1]
    average = sum(windowData)/len(windowData)
    output.append(average)
  return output

def cumulativeWeightedRunningMean(data, window_size):
  output = []
  for i in range(0,len(data)):
    start = max(0,i-window_size)
    windowData = data[start:i+1]
    weights = [1+x*x for x in range(0,len(windowData))]
    s = 0
    for x, y in zip(windowData, weights):
      s += x * y
    average = s / sum(weights)
    output.append(average)
  return output

fromDate = util.stringToTime("02.03.2017 00:00:00")
toDate = util.stringToTime("03.03.2017 00:00:00")
granularity = 15
q = DateRangeGroupQuery(fromDate, toDate, [MediationConfig.getLobWithCountry("CZ", "GSM")["flows"]["MSSBRN1A"]],
                        granularity)
# q = DateRangeGroupQuery(fromDate, toDate, [MediationConfig.getLobWithCountry("CZ","ACI")["flows"]["GSM"]], granularity)
lob1Data = util.dateDataListToList(q.execute(), "MSSBRN1A")
lob1Data.append(0)
lob1Data.append(0)
lob1Data.append(0)
lob1Data.append(0)
dates = list(
  map(lambda x: util.dateToTimeString(x).split("+")[0].split("T")[1].split(":")[0], util.dateDataListToList(q.execute(), "_id")))
dataTicks = []
dataTickPos = []
for i in range(0, len(dates)):
  if i % 4 == 0:
    dataTicks.append(dates[i])
    dataTickPos.append(i)

# lob1Data=[100,0,0,100,0,0,100,0,0,100,0,0,100,0,0,100,0,0,100,0,0,100,0,0]
plt.figure(figsize=(12, 6))
plt.plot(lob1Data, linewidth=0.3, color="#ff009f", label="actual data")

# Running mean lines
# plt.plot(cumulativeRunningMedian(lob1Data, 9), label='Cumulative median (9)', color="red")
# plt.plot(cumulativeRunningMedian(lob1Data, 7), label='Cumulative median (7)', color="green")
# plt.plot(cumulativeRunningMedian(lob1Data, 3), label='Cumulative median (3)', color="blue")



# plt.plot(cumulativeRunningMean(lob1Data, 10), label='Cumulative mean (10)', color="red")
plt.plot(cumulativeRunningMean(lob1Data, 7), label='Cumulative mean (7)', color="blue")
# plt.plot(cumulativeRunningMean(lob1Data, 4), label='Cumulative mean (4)', color="green")
# plt.plot(cumulativeWeightedRunningMean(lob1Data, 7), label='Weighted cumulative mean (7)', color="black")
# plt.plot(movingAverage(lob1Data, 10), label='Simple Running mean (10)', color="orange")

# plt.plot(smoothData(granularity,lob1Data[:-20]))
plt.plot(smoothData(granularity, lob1Data),color="brown",label="Savitzky–Golay filter",linewidth=2)
plt.xticks(dataTickPos, dataTicks, rotation='vertical')
plt.title('CZ - GSM - MSSBRN1A')
plt.legend(loc='upper left')
plt.show()
