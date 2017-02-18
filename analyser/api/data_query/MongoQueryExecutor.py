import config
from mongo import mongo


class MongoQueryExecutor:
  def __init__(self, searchParam):
    self.searchParam = searchParam
    self.query = []
    self.coll = mongo.dataDb()["lobs"]
    self.metrics = []
    self.lobName = searchParam["aggregation"]["sum"][0]
    self.lobConfig = config.getLobByName(self.lobName)
    self.metadata = {}

  def prepare(self):
    fromDate = self.searchParam["from"]
    toDate = self.searchParam["to"]
    match = {"$match": {"_id": {"$gt": fromDate, "$lt": toDate}}}
    group, project = self.createTimeGroupAndProjection(abs(fromDate.timestamp() - toDate.timestamp()))
    group2, project2 = self.createDataGroupAndProjection(self.searchParam["aggregation"])
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
    hours = minutes / 60
    groupCount = max(minutes / 400, self.lobConfig.granularity)  # CONSTANT
    minuteRange = 0
    grouping = None
    if groupCount <= 30:
      minuteGroups = [1, 5, 15, 30]
      for minuteGroup in minuteGroups:
        if (groupCount <= minuteGroup):
          minuteRange = minuteGroup
          grouping = self.createMinuteGrouping(minuteGroup)
          break
    elif hours < 336:
      minuteGroups = [60, 2 * 60, 4 * 60]
      for minuteGroup in minuteGroups:
        if (groupCount <= minuteGroup):
          minuteRange = minuteGroup
          grouping = self.createHourGrouping(minuteGroup / 60)
          break
    else:
      days = 1
      minuteRange = days * 24 * 60
      grouping = self.createDayGrouping(days)
    self.metadata["minuteRange"] = minuteRange
    return grouping

  def createMinuteGrouping(self, groupByMinutes):
    print(groupByMinutes)
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
    print("hours: " + str(groupByHours))
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
    print("days: " + str(groupByDays))
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

  def createDataGroupAndProjection(self, aggregation):
    group = {}
    project = {}
    for dataPath in aggregation["sum"]:
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
  return string.replace(".", "")
