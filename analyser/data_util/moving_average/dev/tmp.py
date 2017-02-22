import matplotlib.pyplot as plt

from api import util
from config import config


holidays = [util.jsStringToDate("2016-09-28T00:00:00.000Z"),
            util.jsStringToDate("2016-10-28T00:00:00.000Z"),
            util.jsStringToDate("2016-11-17T00:00:00.000Z")]
from api.data_query import DayAverageQuery


class MovingAverageQuery:
  def __init__(self, lobName):
    self.lobName = lobName
    self.lobConfig = config.getLobConfigByName(lobName)

  def execute(self):
    mongoQuery = DayAverageQuery(holidays, self.lobName, self.lobConfig.granularity)
    data, metric = mongoQuery.execute()
    dayData = {}
    print(data)
    for tick in data:
      key = tick["_id"]
      val = tick[metric[0]]
      if key in dayData:
        val += dayData[key]
      dayData[key] = val
    list = []
    for key,val in dayData.items():
      list.append((key,val))
    list = sorted(list,key=lambda x:x[0])
    return list


# query = MovingAverageQuery("CZ.SMS")
# averages = query.execute()
# print(averages)
# x,y=zip(*averages)
from data_util.moving_average import DayAverageExecutor
response = DayAverageExecutor.getDayAverages("CZ.DWA")
workDays = util.dateDataListToList(response["data"],"workDays")
plt.plot(workDays,label='workDays')

# holidays = util.dateDataListToList(response["data"],"holidays")
# plt.plot(holidays,label='holidays')
#
# weekends = util.dateDataListToList(response["data"],"weekends")
# plt.plot(weekends,label='weekends')

plt.legend()
plt.show()

