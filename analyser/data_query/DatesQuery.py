import datetime

from config import config
from data_query.BaseDateQuery import BaseDateQuery
from mongo import mongo


class DatesQuery(BaseDateQuery):
  def __init__(self, dates, lobName, resultName=None, granularity=0):
    super().__init__()
    roundedDates = []
    for date in dates:
      roundedDates.append(date.replace(hour=0, minute=0, second=0, microsecond=0))
    self.dates = roundedDates
    self.lobName = lobName
    self.query = []
    self.coll = mongo.dataDb()["lobs"]
    self.metrics = []
    self.maxTicks = 10000
    self.resultName = resultName
    if self.resultName is None:
      self.resultName = lobName
    if granularity == 0:
      self.granularity = config.getLobConfigByName(lobName).granularity
    else:
      self.granularity = granularity

    self.metadata = {}

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
    project = {
      "_id": "$_id"
    }
    return groupObject, project

  def createDataGroupAndProjection(self):
    group = {}
    project = {}
    validResultName = validMongoAttribute(self.resultName)
    validName = validMongoAttribute(self.lobName)
    group[validName] = {"$sum": "$data." + self.lobName + ".sum"}
    project[validResultName] = "$" + validName
    self.metrics.append(self.resultName)
    return group, project

  def execute(self):
    if(len(self.dates)) == 0:
      return []
    """
    some time ticks might be missing
    :return:
    """
    return super(DatesQuery, self).execute()


def validMongoAttribute(string):
  return string.replace(".", "_")
