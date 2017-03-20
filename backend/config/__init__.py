from .AppConfig import AppConfig

configColl = AppConfig.getColletion()

AppConfig.loadConfigFile()

def getCurrentTime():
  """
  deprecated, use appconfig directly
  :return:
  """
  return AppConfig.getCurrentTime()
