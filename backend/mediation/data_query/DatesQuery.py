import datetime

import util
from mongo import mongo


class DatesQuery:
  def __init__(self, dates, flows, granularity=0):
    self.query = None
    self.coll = mongo.lobs()
    self.metrics = []
    self.dataPaths = []
    self.dates = [util.resetDateTimeMidnight(d) for d in dates]
    self.flows = flows
    self.granularity = int(granularity)
    self.createDataPathAndOutputs2()
    self.metadata = {}

  def execute(self):
    self.prepare()
    result = list(self.coll.aggregate(self.query))
    resultDict = {}
    for i in result:
      group = i["_id"]
      date = datetime.datetime(group["year"], group["month"], group["dayOfMonth"], int(group["hour"]),
                               int(group["minute"]))
      from config import AppConfig
      date = date.replace(tzinfo=AppConfig.getTimezone())
      i["_id"] = date
      resultDict[date] = i
    granularityDelta = datetime.timedelta(minutes=self.granularity)
    nullObject = {}
    for metric in self.metrics:
      nullObject[metric] = 0
    for date in self.dates:
      d = date
      while d < date + datetime.timedelta(days=1):
        if d not in resultDict:  # TODO: check if some results can have just few of the metrics.
          resultDict[d] = {**nullObject, **{"_id": d}}
        d += granularityDelta

    result = sorted(resultDict.values(), key=lambda x: x["_id"])
    return result

  def createDataPathAndOutputs2(self):
    maxGran = 0
    for flow in self.flows:
      self.dataPaths.append(("$data." + flow["dataPath"], flow["name"]))
      maxGran = max(maxGran, flow["options"]["granularity"])
    if (self.granularity == 0):
      self.granularity = maxGran

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
    elif groupCount <= 24*60:
      days = 1
      minuteRange = days * 24 * 60
      grouping = self.createDayGrouping(days)
    else:
      raise NotImplemented("")
    self.metadata["granularity"] = minuteRange
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
    project = {"_id": "$_id"}
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
    project = {"_id": "$_id"}
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
      "_id": "$_id"
    }
    return groupObject, project

  def createDataGroupAndProjection(self):
    group = {}
    project = {}
    for dataPath in self.dataPaths:
      validName = dataPath[1]
      group[validName] = {"$sum": dataPath[0]}
      project[validName] = "$" + validName
      self.metrics.append(validName)
    return group, project

  def _idTimezoneFix(self):
    return {"$add": ["$_id", 60 * 60 * 1000]}

  def createMatchObject(self):
    orMatches = []
    for date in self.dates:
      orMatches.append({"_id": {"$gte": date, "$lt": date + datetime.timedelta(days=1)}})
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
        "_id": 1
      }
    }
    self.query = [match, group, project, sort]
