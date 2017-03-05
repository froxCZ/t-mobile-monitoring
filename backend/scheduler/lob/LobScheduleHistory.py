from mongo import mongo


class LobScheduleHistory:
  def __init__(self):
    pass

  def getLastSuccessfullExecutions(self):
    res = mongo.scheduleHistory().find_one({"_id": "lobs"})
    if res == None:
      res = {}
    return res

  def saveSuccessfullExecution(self, flow, time):
    setObj = {"$set": {flow["gName"]: {"finishTime": time, "result": 0}}}
    mongo.scheduleHistory().update_one({"_id": "lobs"}, setObj, upsert=True)
    pass
