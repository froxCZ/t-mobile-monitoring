import logging

from common import AppConfig
from mongo import mongo
from .status import OUTAGE


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
  def getEvents(offset=0, onlyOutage=False, limit=30):
    filter = {}
    if onlyOutage is True:
      filter["newStatus"] = {"$eq": OUTAGE}
    events = list(mongo.events().find(filter, {"_id": 0}).limit(limit).skip(offset).sort("_id", -1))
    return events
