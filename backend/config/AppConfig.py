import datetime

import pytz

TIMEZONE = pytz.timezone('CET')
_BASE_DATE_DIFF = datetime.timedelta(days=60)

from mongo import mongo

configColl = mongo.config()


class AppConfig:
  @staticmethod
  def getCurrentTime():
    # return datetime.datetime.now().replace(tzinfo=TIMEZONE)
    return datetime.datetime.now().replace(tzinfo=TIMEZONE) - _BASE_DATE_DIFF

  @staticmethod
  def getColletion():
    return configColl

  @staticmethod
  def getTimezone():
    return TIMEZONE

  @staticmethod
  def kafkaServers():
    return "127.0.0.2:9092"

