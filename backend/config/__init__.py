from .AppConfig import AppConfig

configColl = AppConfig.getColletion()


def getCurrentTime():
  """
  deprecated, use appconfig directly
  :return:
  """
  return AppConfig.getCurrentTime()
