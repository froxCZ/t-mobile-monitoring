from mongo import mongo


class MongoQueryExecutor:
  def __init__(self, searchParam):
    self.searchParam = searchParam
    self.query = []
    self.coll = mongo.dataDb()["lobs"]
    self.metrics = []

    self.prepare()

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
    self.query = [match, group, project,sort]

  def createTimeGroupAndProjection(self, timeDiff):
    timeDiff /= 60
    minutes = max(timeDiff, 60)
    groupCount = minutes / 400  # CONSTANT
    if groupCount < 60:
      minuteGroups = [1, 5, 15, 30]
      for minuteGroup in minuteGroups:
        if (groupCount < minuteGroup):
          return self.createMinuteGrouping(minuteGroup)
    raise Exception('too large range')

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
    result = self.coll.aggregate(self.query)
    return list(result),self.metrics


def validMongoAttribute(string):
  return string.replace(".", "")
