from config import AppConfig
from mongo import mongo

configColl = mongo.config()

MEDIATION_DOCUMENT = {"_id": "mediation"}


class MediationConfig():
  configColl = configColl

  @staticmethod
  def getLob(lobName):
    lobs = MediationConfig.getLobs(_getCountryFromLob(lobName))
    if lobName in lobs:
      return lobs[lobName]
    else:
      return None

  @staticmethod
  def getCountries():
    defaultParam = {"lazyDays": [], "holidays": []}
    res = configColl.find_one(MEDIATION_DOCUMENT)["countries"]
    countries = {}
    for countryName, country in res.items():
      countries[countryName] = {**defaultParam, **country}
    return countries

  @staticmethod
  def getCountryByName(countryName):
    return MediationConfig.getCountries()[countryName]

  @staticmethod
  def getCountryList():
    return ["CZ", "AT", "NL", "DE"]

  @staticmethod
  def getLobs(country, enabledOnly=False):
    """
    returns config for all inputs and forwards. Config is derived from parent object.
    :return:
    """
    res = configColl.find_one(MEDIATION_DOCUMENT)
    defaultConfig = {
      "granularity": 240,
      "hardAlarmLevel": 0.5,
      "softAlarmLevel": 0.75,
      "difference": "day",
    }
    if country not in res["lobs"]:
      return {}
    for lobName, config in res["lobs"][country].items():
      config["country"] = country
      config["name"] = lobName
      if "options" not in config:
        config["options"] = {}
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
        flow["dataPath"] = country + "." + lobName + ".inputs." + flowName
        flow["gName"] = country + "_" + lobName + "_" + flowName
        flow["country"] = country
        inputs[flowName] = flow
        config["flows"][flowName] = flow
      config["inputs"] = inputs
      forwards = {}
      for flowName, flowOptions in config["forwards"].items():
        inputName = flowName.split(":")[0]
        if inputName in config["inputs"]:
          flow = {"options": setFlowDefaultOptions(flowOptions, parentObj=config["inputs"][inputName]["options"])}
        else:
          flow = {"options": setFlowDefaultOptions(flowOptions, parentObj=config["options"])}
        flow["name"] = flowName
        flow["type"] = "forwards"
        flow["lobName"] = lobName
        flow["country"] = country
        flow["dataPath"] = country + "." + lobName + ".forwards." + flowName
        flow["gName"] = country + "_" + lobName + "_" + flowName
        forwards[flowName] = flow
        config["flows"][flowName] = flow
      config["forwards"] = forwards
    lobs = res["lobs"][country]
    if enabledOnly:
      for lobName, lob in lobs.items():
        for flowName, flow in lob["flows"].copy().items():
          if flow["options"]["enabled"] == False:
            del lob["flows"][flowName]
            del lob[flow["type"]][flowName]
    return lobs

  @staticmethod
  def addFlow(flow):
    dataPath = "lobs." + flow["country"] + "." + flow["lobName"] + "." + flow["type"] + "." + flow["name"]
    configColl.update_one(MEDIATION_DOCUMENT, {"$set": {dataPath: {}}})
    pass

  @staticmethod
  def deleteFlow(flow):
    dataPath = "lobs." + flow["country"] + "." + flow["lobName"] + "." + flow["type"] + "." + flow["name"]
    return configColl.update_one(MEDIATION_DOCUMENT, {"$unset": {dataPath: {}}})

  @staticmethod
  def addLob(country, name):
    dataPath = "lobs." + country + "." + name
    return configColl.update_one(MEDIATION_DOCUMENT, {"$set": {dataPath: {}}})

  @staticmethod
  def deleteLob(lob):
    dataPath = "lobs." + lob["country"] + "." + lob["name"]
    return configColl.update_one(MEDIATION_DOCUMENT, {"$unset": {dataPath: {}}})

  @staticmethod
  def getLobWithCountry(country, lobName):
    lobs = MediationConfig.getLobs(country)
    if lobName in lobs:
      return lobs[lobName]
    else:
      return None

  @staticmethod
  def threadsCount():
    return AppConfig.getMediationConfig().get("threadsCount", 1)


def _getCountryFromLob(lobName):
  return lobName.split("_")[0]


def setFlowDefaultOptions(obj, parentObj):
  return {**{"enabled": True}, **parentObj, **obj}
