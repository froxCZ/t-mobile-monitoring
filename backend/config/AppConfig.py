import datetime
import json
import logging
import os

import pytz

TIMEZONE = pytz.timezone('Europe/Prague')

configColl = None



class AppConfig:
  configDict = None
  DATE_DIFF = None

  @staticmethod
  def getCurrentTime():
    # return datetime.datetime.now().replace(tzinfo=TIMEZONE)
    return datetime.datetime.now(tz=TIMEZONE) + AppConfig.DATE_DIFF

  @staticmethod
  def getColletion():
    return configColl

  @staticmethod
  def getTimezone():
    return TIMEZONE

  @staticmethod
  def getFlaskConfig():
    return AppConfig.configDict.get("flask", {})

  @staticmethod
  def getSystemConfig():
    return AppConfig.configDict.get("system", {})

  @staticmethod
  def getMediationConfig():
    return AppConfig.configDict.get("mediation", {})

  @staticmethod
  def getMongoConfig():
    return AppConfig.configDict.get("mongo")

  @staticmethod
  def getIntegrationConfig():
    return AppConfig.configDict.get("integration", {})

  @staticmethod
  def loadConfigFile():
    for configFile in ["/config/backend.json", os.path.join(os.path.dirname(__file__), "..", "config.json")]:
      if os.path.exists(configFile):
        with open(configFile) as json_data_file:
          AppConfig.configDict = json.load(json_data_file)
        assert AppConfig.configDict is not None
        logLevel = logging._nameToLevel[AppConfig.getSystemConfig().get("logLevel", "INFO")]
        logging.basicConfig(format='%(levelname)s %(asctime)s [%(module)s]: %(message)s', level=logLevel)
        AppConfig.DATE_DIFF = datetime.timedelta(days=AppConfig.configDict.get("system", {}).get("daysOffset", 0))
        logging.info("Loaded config: " + str(AppConfig.configDict))
        logging.info("App time: " + str(AppConfig.getCurrentTime()))
        break
    from mongo import mongo
    global configColl
    configColl = mongo.config()
