import datetime
import logging
import time

from common import AppConfig
from mediation import MediationConfig
from mongo import mongo
from scheduler.AbstractExecutor import AbstractExecutor

SEPARATOR = "-+-"

"""
This class discovers flows used in past day and adds them to database.
"""

def createGlobalName(country, lob, flow, type):
  strArr = [country, lob, flow, type]
  for s in strArr:
    if len(s) == 0:
      raise Exception("cant create global name for " + str(strArr))
  return SEPARATOR.join(strArr)


def globalNameToFlow(globalName):
  country, lobName, name, type = globalName.split(SEPARATOR)
  return {"country": country, "lobName": lobName, "name": name, "type": type}


class DiscoverFlowsExecutor(AbstractExecutor):
  name = "DiscoverFlowsExecutor"
  interval = 60 * 60
  maxRunningTime = 5 * 60

  def __init__(self):
    super().__init__(DiscoverFlowsExecutor.name, DiscoverFlowsExecutor.interval)
    self.toDate = AppConfig.getCurrentTime()
    self.fromDate = self.toDate - datetime.timedelta(days=7)

  def _executeInternal(self):
    start = time.time()
    cursor = mongo.traffic().find({"$and": [
      {"_id": {"$gte": self.fromDate}},
      {"_id": {"$lt": self.toDate}}
    ]})
    allFlows = dict((countryName, {}) for countryName in MediationConfig.getCountries())
    currentConfig = dict(
      (countryName, MediationConfig.getLobs(countryName)) for countryName in MediationConfig.getCountries())
    newFlows = {}
    newLobs = dict((countryName, {}) for countryName in MediationConfig.getCountries())
    for doc in cursor:
      for countryName, country in doc["data"].items():
        for lobName, lob in country.items():
          if lobName == "FOX":
            continue
          if currentConfig[countryName].get(lobName, None) == None:
            newLobs[countryName][lobName] = True
          for flowName, flow in lob.get("inputs", {}).items():
            if flowName == "updatesCnt" or flowName == "sum":
              continue
            if flowName not in currentConfig[countryName].get(lobName, {}).get("inputs", {}):
              newFlows[createGlobalName(countryName, lobName, flowName, "inputs")] = True
          for flowName, flow in lob.get("forwards", {}).items():
            if flowName == "updatesCnt" or flowName == "sum":
              continue
            if flowName not in currentConfig[countryName].get(lobName, {}).get("forwards", {}):
              newFlows[createGlobalName(countryName, lobName, flowName, "forwards")] = True
              # print(flowName)
    insertedLobs = 0
    for countryName, lobs in newLobs.items():
      for lobName in lobs.keys():
        insertedLobs += 1
        MediationConfig.addLob(countryName, lobName)
    for globalFlowName in newFlows.keys():
      flow = globalNameToFlow(globalFlowName)
      MediationConfig.addFlow(flow)
    if insertedLobs > 0 or len(newFlows) > 0:
      logging.info("inserted " + str(insertedLobs) + " lobs and " + str(len(newFlows)) +
                   " flows in " + str(int(time.time() - start)) + " seconds")
