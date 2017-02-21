from config import config
from mongo import mongo


class MongoQueryExecutor:
  def __init__(self, fromDate, toDate, lobNames, granularity):
    self.fromDate = fromDate
    self.toDate = toDate
    self.lobNames = lobNames
    self.granularity = int(granularity)
    self.query = []
    self.coll = mongo.dataDb()["lobs"]
    self.metrics = []
    self.maxTicks = 500
    if (int(self.granularity) == 0):
      for lobName in lobNames:
        self.granularity = max(self.granularity, config.getLobConfigByName(lobName).granularity)
    else:
      self.maxTicks = 1000
    self.metadata = {}

  def prepare(self):
    match = {"$match": {"_id": {"$gt": self.fromDate, "$lt": self.toDate}}}
    group, project = self.createTimeGroupAndProjection(abs(self.fromDate.timestamp() - self.toDate.timestamp()))
    group2, project2 = self.createDataGroupAndProjection(self.lobNames)
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
    elif groupCount <= 8 * 60:
      minuteGroups = [60, 2 * 60, 4 * 60, 8 * 60]
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
        "interval": {
          "$subtract": [
            {"$minute": "$_id"},
            {"$mod": [{"$minute": "$_id"}, groupByMinutes]}
          ]
        }
      },
      "anyDate": {"$first": "$_id"},
    }
    project = {"_id": {
      "$subtract": ["$anyDate", {"$multiply": [1000 * 60, {"$mod": [{"$minute": "$anyDate"}, groupByMinutes]}]}]}}
    return groupObject, project

  def createHourGrouping(self, groupByHours):
    groupObject = {
      "_id": {
        "year": {"$year": "$_id"},
        "month": {"$month": "$_id"},
        "dayOfMonth": {"$dayOfMonth": "$_id"},
        "interval": {
          "$subtract": [
            {"$hour": "$_id"},
            {"$mod": [{"$hour": "$_id"}, groupByHours]}
          ]
        }
      },
      "anyDate": {"$first": "$_id"},
    }
    project = {"_id": {
      "$subtract": ["$anyDate", {"$multiply": [1000 * 60 * 60, {"$mod": [{"$hour": "$anyDate"}, groupByHours]}]}]}}
    return groupObject, project

  def createDayGrouping(self, groupByDays):
    groupObject = {
      "_id": {
        "year": {"$year": "$_id"},
        "month": {"$month": "$_id"},
        "dayOfMonth": {"$dayOfMonth": "$_id"},
        "interval": {
          "$subtract": [
            {"$dayOfMonth": "$_id"},
            {"$mod": [{"$dayOfMonth": "$_id"}, groupByDays]}
          ]
        }
      },
      "anyDate": {"$first": "$_id"},
    }
    project = {"_id": {
      "$subtract": ["$anyDate",
                    {"$multiply": [1000 * 60 * 60 * 24, {"$mod": [{"$dayOfMonth": "$anyDate"}, groupByDays]}]}]}}
    return groupObject, project

  def createDataGroupAndProjection(self, lobs):
    group = {}
    project = {}
    for dataPath in lobs:
      validName = validMongoAttribute(dataPath)
      group[validName] = {"$sum": "$data." + dataPath + ".sum"}
      project[validName] = "$" + validName
      self.metrics.append(validName)
    return group, project

  def execute(self):
    self.prepare();
    result = self.coll.aggregate(self.query)
    return list(result), self.metrics


def validMongoAttribute(string):
  return string.replace(".", "_")
