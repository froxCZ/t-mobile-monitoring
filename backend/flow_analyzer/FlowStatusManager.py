import datetime

import config
from flow_analyzer import status
from mongo import mongo


class FlowStatusManager:
  def __init__(self):
    pass

  def getLobDetail(self, lobName):
    lob = config.getLobConfig(lobName)
    allStatuses = self.getAll()
    lobFlowStatuses = {}
    for flowName, flow in lob["flows"].items():
      lobFlowStatuses[flowName] = allStatuses[flow["gName"]]

    return lobFlowStatuses

  def getLobsOverview(self):
    allStatuses = self.getAll()
    lobStatusDict = {}
    for lobName, lob in config.getLobs().items():
      ok = 0
      warning = 0
      outage = 0
      expired = 0
      disabled = 0
      for flow in lob["flows"].values():
        gName = flow["gName"]
        if flow["options"]["enabled"] is False:
          disabled += 1
          continue
        flowStatus = allStatuses.get(gName, {"status": status.NA})["status"]
        if flowStatus == status.NA:
          expired += 1
        elif flowStatus == status.OK:
          ok += 1
        elif flowStatus == status.WARNING:
          warning += 1
        elif flowStatus == status.OUTAGE:
          outage += 1
      lobStatusDict[lobName] = {
        status.OK: ok,
        status.WARNING: warning,
        status.OUTAGE: outage,
        status.NA: expired,
        status.DISABLED: disabled
      }
    return lobStatusDict

  def getAll(self):
    lobs = config.getLobsConfig()["lobs"]
    res = mongo.statuses().find_one({"_id": "lobs"}, {"_id": 0})
    if res is None:
      return {}
    statuses = {}
    for lobName, lob in lobs.items():
      for flowName, flow in lob["flows"].items():
        gName = flow["gName"]
        if gName in res:
          statuses[gName] = self._setStatusMetadata(res[gName], flow)
        else:
          statuses[gName] = {"status": "N_A"}
    return statuses

  def _setStatusMetadata(self, status, flow):
    ticTime = status["ticTime"]
    granDelta = datetime.timedelta(minutes=flow["options"]["granularity"])
    if ticTime + 2 * granDelta < config.getCurrentTime():
      return {"status": "N_A"}
    return status

  def getStatusForFlow(self, flow):
    gName = flow["gName"]
    res = mongo.statuses().find_one({"_id": "lobs"}, {gName: 1})
    if gName not in res:
      return {"validity": "expired"}
    return self._setStatusMetadata(res[gName], flow)

  def saveStatus(self, flow, status, difference, ticTime):
    statusDict = {"status": status,
                  "ticTime": ticTime,
                  "difference": difference}
    setObj = {"$set": {flow["gName"]: statusDict}}
    mongo.statuses().update_one({"_id": "lobs"}, setObj, upsert=True)
    pass

  def removeAll(self):
    mongo.statuses().delete_one({"_id": "lobs"})
