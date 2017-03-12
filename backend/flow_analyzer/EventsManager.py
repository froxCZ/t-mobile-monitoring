import logging

import config
from mongo import mongo


class EventsManager:
  @staticmethod
  def logEvent(flow, message, ticTime=None):
    flowObj = {flow["lobName"]: {flow["name"]: 1}}
    obj = {"flow": flowObj, "time": config.getCurrentTime(), "message": message, "ticTime": ticTime}
    logging.debug("flow: " + flow["gName"] + " message:" + message)
    mongo.events().insert_one(obj)
