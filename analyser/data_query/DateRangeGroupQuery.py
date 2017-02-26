import datetime

from config import config
from data_query.BaseDateQuery import BaseDateQuery
from mongo import mongo


class DateRangeGroupQuery(BaseDateQuery):
  def __init__(self, fromDate, toDate, lobNames, granularity, dates=None):
    super().__init__()
    self.fromDate = fromDate
    self.toDate = toDate
    self.lobNames = lobNames
    self.granularity = int(granularity)
    self.query = []
    self.coll = mongo.dataDb()["lobs"]
    self.metrics = []
    self.maxTicks = 500
    self.dates = dates
    if (int(self.granularity) == 0):
      for lobName in lobNames:
        self.granularity = max(self.granularity, config.getLobConfigByName(lobName).granularity)
    else:
      self.maxTicks = 2000
    self.metadata = {}

  def prepare(self):
    if (self.dates == None):
      match = {"$match": {"_id": {"$gte": self.fromDate, "$lt": self.toDate}}}
    else:
      match = self.createMatchObject()
    group, project = self.createTimeGroupAndProjection(abs(self.fromDate.timestamp() - self.toDate.timestamp()))
    group2, project2 = self.createDataGroupAndProjection(self.lobNames)
    group.update(group2)
    project.update(project2)
    group = {"$group": group}
    project = {"$project": project}
    sort = {
      "$sort": {
        "anyDate": 1
      }
    }
    self.query = [match, group, project]

  def createMatchObject(self):
    orMatches = []
    for date in self.dates:
      orMatches.append({"_id": {"$gte": date, "$lt": date + datetime.timedelta(days=1)}})
    return {"$match": {"$or": orMatches}}

  def createTimeGroupAndProjection(self, timeDiff):
    timeDiff /= 60
    minutes = max(timeDiff, 60)
    granularity = self.granularity
    groupCount = max(minutes / self.maxTicks, granularity)
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
      minuteGroups = [60, 2 * 60,3*60, 4 * 60, 8 * 60,12*60]
      for minuteGroup in minuteGroups:
        if (groupCount <= minuteGroup):
          minuteRange = minuteGroup
          grouping = self.createHourGrouping(minuteGroup / 60)
          break
    else:
      days = 1
      minuteRange = days * 24 * 60
      grouping = self.createDayGrouping(days)
    self.metadata["granularity"] = minuteRange
    return grouping

  def createMinuteGrouping(self, groupByMinutes):

    groupObject = {
      "_id": {
        "year": {"$year": "$_id"},
        "month": {"$month": "$_id"},
        "dayOfMonth": {"$dayOfMonth": "$_id"},
        "hour": {"$hour": "$_id"},
        "minute": {
          "$subtract": [
            {"$minute": "$_id"},
            {"$mod": [{"$minute": "$_id"}, groupByMinutes]}
          ]
        }
      },
      "anyDate": {"$first": "$_id"},
    }
    project = {"_id": "$_id"}
    return groupObject, project

  def createHourGrouping(self, groupByHours):
    groupObject = {
      "_id": {
        "year": {"$year": "$_id"},
        "month": {"$month": "$_id"},
        "dayOfMonth": {"$dayOfMonth": "$_id"},
        "hour": {
          "$subtract": [
            {"$hour": "$_id"},
            {"$mod": [{"$hour": "$_id"}, groupByHours]}
          ]
        },
        "minute": "0"
      },
      "anyDate": {"$first": "$_id"},
    }
    project = {"_id": "$_id"}
    return groupObject, project

  def createDayGrouping(self, groupByDays):
    groupObject = {
      "_id": {
        "year": {"$year": "$_id"},
        "month": {"$month": "$_id"},
        "dayOfMonth": {"$dayOfMonth": "$_id"},
        "hour": "0",
        "minute": "0",
      },
      "anyDate": {"$first": "$_id"},
    }
    project = {"_id": "$_id"}
    return groupObject, project

  def createDataGroupAndProjection(self, lobs):
    group = {}
    project = {}
    for dataPath in lobs:
      validName = validMongoAttribute(dataPath)
      group[validName] = {"$sum": "$data." + dataPath + ".sum"}
      project[validName] = "$" + validName
      self.metrics.append(dataPath)
    return group, project

  def execute(self):
    result = super(DateRangeGroupQuery, self).execute()
    timeSequenceResult = []
    lastDate = self.fromDate.replace(hour=0, minute=0, second=0, tzinfo=None)
    timeDelta = datetime.timedelta(minutes=self.metadata["granularity"])
    i = 0
    nullMetrics = {}
    for metric in self.metrics:
      nullMetrics[metric] = 0
    while lastDate <= self.toDate.replace(tzinfo=None):
      if i < len(result) and lastDate == result[i]["_id"]:
        timeSequenceResult.append({**nullMetrics, **result[i]})
        i += 1
      else:
        timeSequenceResult.append({**{"_id": lastDate}, **nullMetrics})
      lastDate += timeDelta

    return timeSequenceResult


def validMongoAttribute(string):
  return string.replace(".", "_")
