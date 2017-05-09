import logging

from config import AppConfig
from mongo import mongo
from .status import OK


class EventsManager:
  @staticmethod
  def logStatusChangeEvent(flow, message, ticTime, newStatus):
    currentTime = AppConfig.getCurrentTime()
    obj = {"flowName": flow["name"],
           "lobName": flow["lobName"],
           "country": flow["country"],
           "time": currentTime,
           "message": message,
           "newStatus": newStatus,
           "ticTime": ticTime}
    logging.debug("flow: " + flow["gName"] + " message:" + message)
    mongo.events().insert_one(obj)

  @staticmethod
  def getEvents(offset=0, omitOK=False, limit=30):
    filter = {}
    if omitOK is True:
      filter["newStatus"] = {"$ne": OK}
    events = list(mongo.events().find(filter, {"_id": 0}).limit(limit).skip(offset).sort("_id", -1))
    return events
