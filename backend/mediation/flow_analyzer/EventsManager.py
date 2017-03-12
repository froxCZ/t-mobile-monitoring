import logging

import config
from mongo import mongo


class EventsManager:
  @staticmethod
  def logStatusChangeEvent(flow, message, ticTime, newStatus):
    currentTime = config.getCurrentTime()
    obj = {"_id": currentTime,
           "flowName": flow["name"],
           "lobName": flow["lobName"],
           "country": flow["country"],
           "time": currentTime,
           "message": message,
           "newStatus": newStatus,
           "ticTime": ticTime}
    logging.debug("flow: " + flow["gName"] + " message:" + message)
    mongo.events().insert_one(obj)

  @staticmethod
  def getEvents(skip=0, limit=30):
    events = list(mongo.events().find({}, {"_id": 0}).limit(limit).skip(skip).sort("_id", -1))
    return events
