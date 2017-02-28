import datetime

from mongo import mongo


class DayAverageQuery:
  def __init__(self, dates, lobName, granularity,resultName=None):
    self.dates = dates
    self.lobName = lobName
    self.granularity = granularity
    self.metadata = {}
    self.metrics = []
    self.resultName = resultName
    if self.resultName is None:
      self.resultName = lobName
    self.coll = mongo.lobs()

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

  def createMatchObject(self):
    orMatches = []
    for date in self.dates:
      orMatches.append({"_id": {"$gte": date, "$lt": date + datetime.timedelta(days=1)}})
    return {"$match": {"$or": orMatches}}

  def createTimeGroupAndProjection(self):
    groupCount = self.granularity
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
    project = {"_id": {"$add": [{"$multiply": [60, "$_id.hour"]}, "$_id.interval"]}}
    return groupObject, project

  def createHourGrouping(self, groupByHours):
    groupObject = {
      "_id": {
        "interval": {
          "$subtract": [
            {"$hour": "$_id"},
            {"$mod": [{"$hour": "$_id"}, groupByHours]}
          ]
        }
      },
      "anyDate": {"$first": "$_id"},
    }
    project = {"_id": {"$multiply": [60, "$_id.interval"]}}
    return groupObject, project

  def createDayGrouping(self, groupByDays):
    groupObject = {
      "_id": 0,
      "anyDate": {"$first": "$_id"},
    }
    project = {"_id": 1}
    return groupObject, project

  def createDataGroupAndProjection(self):
    group = {}
    project = {}
    validName = validMongoAttribute(self.lobName)
    validResultName = validMongoAttribute(self.resultName)
    group[validName] = {"$sum": "$data." + self.lobName + ".sum"}
    project[validResultName] = {"$divide": ["$" + validName, len(self.dates)]}
    self.metrics.append(validResultName)
    return group, project

  def execute(self):
    self.prepare()
    result = self.coll.aggregate(self.query)
    return list(result), self.metrics


def validMongoAttribute(string):
  return string.replace(".", "_")
