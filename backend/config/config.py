# large files: "FOX",        "RTB",
# deprecated. use __init__
from mediation import MediationConfig
from mongo import mongo

configColl = mongo.config()


#
def setFlowDefaultOptions(obj, parentObj):
  return {**{"enabled": True}, **parentObj, **obj}


# used by new query
def createMergedFlowsObject(country, lobName, flowType):
  flow = {}
  flow["name"] = lobName + "-" + flowType
  flow["type"] = "all_forwards"
  flow["lobName"] = lobName
  flow["dataPath"] = country + "." + lobName + "." + flowType + ".sum"
  flow["gName"] = lobName + "_" + flowType
  flow["country"] = country
  flow["options"] = MediationConfig.getLobWithCountry(country, lobName)["options"]
  return flow
