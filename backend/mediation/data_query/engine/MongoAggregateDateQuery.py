import datetime

import pytz

import util
from mongo import mongo

utc = pytz.timezone("UTC")
cet = pytz.timezone("CET")


class MongoAggregateDateQuery:
  def __init__(self, flow, dates, granularity):
    super().__init__()
    self.flow = flow
    self.coll = mongo.lobs()
    self.dates = dates
    self.granularity = granularity
    self.dataPath = "data." + self.flow["dataPath"]
    self.metric = self.flow["name"]

  def _executeMongoAggregateQuery(self):
    result = list(self.coll.aggregate(self.query))
    resultDict = {}
    from config import AppConfig
    appTimezone = AppConfig.getTimezone()
    for i in result:
      group = i["_id"]
      utcDate = datetime.datetime(group["year"], group["month"], group["dayOfMonth"], int(group["hour"]),
                                  int(group["minute"]), 0, 0, utc)
      date = utcDate.astimezone(appTimezone)
      anyDate = i["anyDate"].astimezone(appTimezone)
      i["_id"] = date
      resultDict[date] = i
    return resultDict

  def execute(self):
    self.prepare()
    result = list(self.coll.aggregate(self.query))
    resultDict = {}
    from config import AppConfig
    appTimezone = AppConfig.getTimezone()
    for i in result:
      group = i["_id"]
      cetDate = datetime.datetime(group["year"], group["month"], group["dayOfMonth"], int(group["hour"]),
                                  int(group["minute"]), 0, 0, cet)
      date = cetDate.astimezone(appTimezone)
      anyDate = i["anyDate"].astimezone(appTimezone)
      i["_id"] = date
      resultDict[date] = i
    return resultDict

  def createTimeGroupAndProjection(self):
    groupCount = self.granularity
    minuteRange = 0
    grouping = None
    if groupCount <= 30:
      minuteGroups = [1, 5, 10, 15, 30]
      for minuteGroup in minuteGroups:
        if (groupCount <= minuteGroup):
          minuteRange = minuteGroup
          grouping = self.createMinuteGrouping(minuteGroup)
          break
    elif groupCount <= 12 * 60:
      minuteGroups = [60, 2 * 60, 3 * 60, 4 * 60, 6 * 60, 8 * 60, 12 * 60]
      for minuteGroup in minuteGroups:
        if (groupCount <= minuteGroup):
          minuteRange = minuteGroup
          grouping = self.createHourGrouping(minuteGroup / 60)
          break
    elif groupCount <= 24 * 60:
      days = 1
      minuteRange = days * 24 * 60
      grouping = self.createDayGrouping(days)
    else:
      raise NotImplemented("")
    return grouping

  def createMinuteGrouping(self, groupByMinutes):
    groupObject = {
      "_id": {
        "year": {"$year": self._idTimezoneFix()},
        "month": {"$month": self._idTimezoneFix()},
        "dayOfMonth": {"$dayOfMonth": self._idTimezoneFix()},
        "hour": {"$hour": self._idTimezoneFix()},
        "minute": {
          "$subtract": [
            {"$minute": self._idTimezoneFix()},
            {"$mod": [{"$minute": self._idTimezoneFix()}, groupByMinutes]}
          ]
        }
      },
      "anyDate": {"$first": self._idTimezoneFix()},
    }
    project = {
      "_id": "$_id",
      "anyDate": "$anyDate",
    }
    return groupObject, project

  def createHourGrouping(self, groupByHours):
    groupObject = {
      "_id": {
        "year": {"$year": self._idTimezoneFix()},
        "month": {"$month": self._idTimezoneFix()},
        "dayOfMonth": {"$dayOfMonth": self._idTimezoneFix()},
        "hour": {
          "$subtract": [
            {"$hour": self._idTimezoneFix()},
            {"$mod": [{"$hour": self._idTimezoneFix()}, groupByHours]}
          ]
        },
        "minute": "0"
      },
      "anyDate": {"$first": self._idTimezoneFix()},
    }
    project = {
      "_id": "$_id",
      "anyDate": "$anyDate",
    }
    return groupObject, project

  def createDayGrouping(self, groupByDays):
    groupObject = {
      "_id": {
        "year": {"$year": self._idTimezoneFix()},
        "month": {"$month": self._idTimezoneFix()},
        "dayOfMonth": {"$dayOfMonth": self._idTimezoneFix()},
        "hour": "0",
        "minute": "0",
      },
      "anyDate": {"$first": self._idTimezoneFix()},
    }
    project = {
      "_id": "$_id",
      "anyDate": "$anyDate",
    }
    return groupObject, project

  def createDataGroupAndProjection(self):
    group = {}
    project = {}
    group[self.metric] = {"$sum": "$"+self.dataPath}
    project[self.metric] = "$" + self.metric
    return group, project

  def _idTimezoneFix(self):
    return {"$add": ["$_id", 60*60*1000]}#uses utc timezone!

  def createMatchObject(self):
    orMatches = []
    for date in self.dates:
      orMatches.append({"_id": {"$gte": date, "$lt": util.resetDateTimeMidnight(date + datetime.timedelta(days=1))}})
    return {"$match": {"$or": orMatches}}

  def prepare(self):
    match = self.createMatchObject()
    group, project = self.createTimeGroupAndProjection()
    group2, project2 = self.createDataGroupAndProjection()
    group.update(group2)
    project.update(project2)
    group = {"$group": group}
    project = {"$project": project}
    sort = {
      "$sort": {
        "anyDate": 1
      }
    }
    self.query = [match, group, project, sort]
