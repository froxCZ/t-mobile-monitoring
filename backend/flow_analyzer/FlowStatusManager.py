from mongo import mongo


class FlowStatusManager:
  def __init__(self):
    pass

  def getAll(self):
    res = mongo.statuses().find_one({"_id": "lobs"},{"_id":0})
    if res == None:
      res = {}
    return res

  def saveStatus(self, flow, status, difference, ticTime):
    statusDict = {"status": status,
                  "ticTime": ticTime,
                  "difference": difference}
    setObj = {"$set": {flow["gName"]: statusDict}}
    mongo.statuses().update_one({"_id": "lobs"}, setObj, upsert=True)
    pass

  def getStatusForFlow(self, flow):
    gName = flow["gName"]
    res = mongo.statuses().find_one({"_id": "lobs"}, {gName: 1})
    if gName not in res:
      return None
    return res[gName]

  def removeAll(self):
    mongo.statuses().delete_one({"_id": "lobs"})
    pass