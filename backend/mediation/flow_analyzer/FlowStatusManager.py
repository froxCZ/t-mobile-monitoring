import datetime

import config
from mediation import MediationConfig
from mediation.flow_analyzer import status
from mongo import mongo


class FlowStatusManager:
  def __init__(self):
    pass

  def getLobDetailWithCountry(self, country, lobName):
    lob = MediationConfig.getLobWithCountry(country, lobName)
    allStatuses = self.getAll(lob["country"])
    lobFlowStatuses = {}
    for flowName, flow in lob["flows"].items():
      lobFlowStatuses[flowName] = allStatuses[flow["gName"]]

    return lobFlowStatuses

  def getLobDetail(self, lobName):
    lob = MediationConfig.getLob(lobName)
    allStatuses = self.getAll(lob["country"])
    lobFlowStatuses = {}
    for flowName, flow in lob["flows"].items():
      lobFlowStatuses[flowName] = allStatuses[flow["gName"]]

    return lobFlowStatuses

  def getLobsOverview(self, country):
    allStatuses = self.getAll(country)
    lobStatusDict = {}
    for lobName, lob in MediationConfig.getLobs(country).items():
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

  def getAll(self, country):
    lobs = MediationConfig.getLobs(country)
    res = mongo.statuses().find_one({"_id": "lobs"}, {"_id": 0})
    if res is None:
      res = {}
    statuses = {}
    for lobName, lob in lobs.items():
      for flowName, flow in lob["flows"].items():
        gName = flow["gName"]
        if gName in res:
          statuses[gName] = self._setStatusMetadata(res[gName], flow)
        else:
          statuses[gName] = {"status": "N_A"}
    return statuses

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

  def _setStatusMetadata(self, flowStatus, flow):
    ticTime = flowStatus["ticTime"]
    granDelta = datetime.timedelta(minutes=flow["options"]["granularity"])
    if not flow["options"]["enabled"]:
      return {"status": status.DISABLED}
    if ticTime + 2 * granDelta < config.getCurrentTime():
      return {"status": status.NA}
    return flowStatus

  def removeAll(self):
    mongo.statuses().delete_one({"_id": "lobs"})

  def getCountriesOverview(self):
    countries = {}
    for country in MediationConfig.getCountryList():
      allStatuses = self.getAll(country)
      ok = 0
      warning = 0
      outage = 0
      expired = 0
      disabled = 0
      for lobName, lob in MediationConfig.getLobs(country).items():
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
      countries[country] = {
        status.OK: ok,
        status.WARNING: warning,
        status.OUTAGE: outage,
        status.NA: expired,
        status.DISABLED: disabled
      }

    return countries
