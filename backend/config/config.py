# large files: "FOX",        "RTB",
# deprecated. use __init__
from mongo import mongo

configColl = mongo.config()


class Lob:
  def __init__(self, country, name, granularity=None, smooth=True):
    self.country = country;
    self.name = name
    self.granularity = granularity
    self.smooth = smooth


CZ_LOBS = {"SIS": Lob("CZ", "SIS", 180),
           "DWA": Lob("CZ", "DWA", 10),
           "MWB": Lob("CZ", "MWB", 60),
           "DAR": Lob("CZ", "DAR", 15),
           "SMS": Lob("CZ", "SMS", 60),
           "PCF": Lob("CZ", "PCF", 15),
           "PPC": Lob("CZ", "PPC", 15),
           "TCF": Lob("CZ", "TCF", 30),
           "GSM": Lob("CZ", "GSM", 15),
           "TPP": Lob("CZ", "TPP", 60),
           "XTC": Lob("CZ", "XTC", 15),
           "PST": Lob("CZ", "PST", 60),
           "WHS": Lob("CZ", "WHS", 10),
           "TAP": Lob("CZ", "TAP", 120),
           "SBC": Lob("CZ", "SBC", 90),
           "SCF": Lob("CZ", "SCF", 180),
           "LAS": Lob("CZ", "LAS", 15),
           "MMS": Lob("CZ", "MMS", 15),
           "ATS": Lob("CZ", "ATS", 15),
           "RRA": Lob("CZ", "RRA", 60),
           "VMS": Lob("CZ", "VMS", 60),
           "MTS": Lob("CZ", "MTS", 15),
           "OTA": Lob("CZ", "OTA", 30),
           "BVS": Lob("CZ", "BVS", 15),
           "VOP": Lob("CZ", "VOP", 20),
           "WEL": Lob("CZ", "WEL", 60),
           "CIR": Lob("CZ", "CIR", 60),
           "SMG": Lob("CZ", "SMG", 60),
           "LTP": Lob("CZ", "LTP", 1440),
           "M2M": Lob("CZ", "M2M", 1440),
           "EWG": Lob("CZ", "EWG", 180),
           "TIT": Lob("CZ", "TIT", 120),
           "RES": Lob("CZ", "RES", 1440),
           "KPI": Lob("CZ", "KPI", 1440),
           "EPC": Lob("CZ", "EPC", 120),
           "MNT": Lob("CZ", "MNT", 10),
           "TOC": Lob("CZ", "TOC", 1440),
           "EWH": Lob("CZ", "EWH", 60),
           "ACI": Lob("CZ", "ACI", 10),
           "ICG": Lob("CZ", "ICG", 60)}
LOBS = {"CZ": CZ_LOBS}


def getLobConfigByName(fullName):
  res = configColl.find_one({"_id": "lobs"}, {"lobs." + fullName: 1})
  tmp = fullName.split("_")
  country = tmp[0]
  granularity = res["lobs"][fullName]["options"]["granularity"]
  return Lob(country, fullName, granularity)


def getLobConfigByNameDict(fullName):
  return getLobsConfig()["lobs"][fullName]


def getLobsConfig():
  """
  returns config for all inputs and forwards. Config is derived from parent object.
  :return:
  """
  res = configColl.find_one({"_id": "lobs"})
  defaultConfig = {
    "granularity": 240,
    "hardAlarmLevel": 0.5,
    "softAlarmLevel": 0.75,
    "difference": "day",
  }
  flowDefaultConfig = {"enabled": True}
  for lobName, config in res["lobs"].items():
    config["options"] = {**defaultConfig, **config["options"]}
    if "inputs" not in config:
      config["inputs"] = {}
    if "forwards" not in config:
      config["forwards"] = {}
    config["flows"] = {}
    inputs = {}
    for flowName, flowOptions in config["inputs"].items():
      flow = {"options": setFlowDefaultOptions(flowOptions, parentObj=config["options"])}
      flow["name"] = flowName
      flow["type"] = "inputs"
      flow["lobName"] = lobName
      flow["dataPath"] = lobName + ".inputs." + flowName
      flow["gName"] = lobName + "_" + flowName
      inputs[flowName] = flow
      config["flows"][flowName] = flow
    config["inputs"] = inputs
    forwards = {}
    for flowName, flowOptions in config["forwards"].items():
      inputName = flowName.split(":")[0]
      if inputName in config["inputs"]:
        flow = {"options": setFlowDefaultOptions(flowOptions, parentObj=config["options"])}
        flow["name"] = flowName
        flow["type"] = "forwards"
        flow["lobName"] = lobName
        flow["dataPath"] = lobName + ".forwards." + flowName
        flow["gName"] = lobName + "_" + flowName
        forwards[flowName] = flow
        config["flows"][flowName] = flow
    config["forwards"] = forwards
  return res


def setFlowDefaultOptions(obj, parentObj):
  return {**{"enabled": True}, **parentObj, **obj}


def createMergedFlowsObject(lobName, flowType):
  flow = {}
  flow["name"] = lobName + "-" + flowType
  flow["type"] = "all_forwards"
  flow["lobName"] = lobName
  flow["dataPath"] = lobName + "." + flowType + ".sum"
  flow["gName"] = lobName + "_" + flowType
  flow["options"] = getLobConfig(lobName)["options"]
  return flow


def getLobConfig(lobName):
  return getLobsConfig()["lobs"][lobName]


def getOptionsByFullFlowName(fullFlowName):
  if fullFlowName.count(".") > 0:
    lob, type, flow = fullFlowName.split(".")
    return getLobConfig(lob)[type][flow]["options"]
  else:
    return getLobConfig(fullFlowName)["options"]


def getOptions(lobName, input=None, forward=None):
  lobConfig = getLobConfig(lobName)
  if (input == None and forward == None) or input == "*" or forward == "*":
    return lobConfig["options"]
  elif forward == None:
    return lobConfig["inputs"][input]["options"]
  else:
    return lobConfig["forwards"][forward]["options"]


def updateLob(lobName, lobUpdate):
  return configColl.update_one({"_id": "lobs"}, lobUpdate)
