import json
import logging
import threading
import time

from kafka import KafkaConsumer

import util
from integration import IntegrationConfig
from mongo import mongo


class MediationDataConsumer(threading.Thread):
  name = "MediationDataConsumer"
  _instance = None
  daemon = True

  def __init__(self):
    super().__init__()
    self.status = "DISCONNECTED"

  def _startConsumer(self):
    if IntegrationConfig.inputTopic() is not None and IntegrationConfig.kafkaServers() is not None:
      while True:
        try:
          consumer = KafkaConsumer(bootstrap_servers=IntegrationConfig.kafkaServers(),
                                   auto_offset_reset='latest',
                                   enable_auto_commit=True,
                                   group_id="mediationMonitoring")
          consumer.subscribe([IntegrationConfig.inputTopic()])
          self.status = "CONNECTED"
          self.consumer = consumer
          return
        except Exception as e:
          logging.exception("Failed to connect to kafka.")
          time.sleep(120)
    else:
      self.status = "NOT_CONFIGURED"
      return False

  def run(self):
    if self._startConsumer():
      for message in self.consumer:
        try:
          self.processMessage(message)
        except Exception as e:
          logging.exception("Error while processing mediation data message.")

  def processMessage(self, message):
    value = message.value.decode('utf-8')
    row = json.loads(value)
    return self.saveMediationData(row)

  def saveMediationData(self, row):
    """
    :param data:
    dict{"country":"CZ",
    "lobName":"ACI",
    "type":"inputs",
    "flowName":"GSM",
    "dataSize":497464,
    "time":"01.01.2017 00:00:24"}
    :return:
    """
    time = util.stringToTime(row["time"]).replace(second=0)
    updatePath = "data." + row["country"] + "." + row["lobName"] + "." + row["type"] + "."
    try:
      dataSize = int(row["dataSize"])
    except ValueError:
      print("ValueError: " + row)
      dataSize = 0
    updateObj = {"$inc":
                   {updatePath + row["flowName"]: dataSize,
                    updatePath + "sum": dataSize,
                    updatePath + "updatesCnt": 1
                    }
                 }
    try:
      mongo.traffic().update({'_id': time}, updateObj, upsert=True)
      logging.info(
        "Inserted row for " + row["lobName"] + " " + row["flowName"] + " at " + str(time) + " of size " + str(dataSize))
      return True
    except Exception as e:
      logging.error("Error while persisting data " + str(row) + " exception: " + str(e))
      return False

  @staticmethod
  def instance():
    if MediationDataConsumer._instance is None:
      MediationDataConsumer._instance = MediationDataConsumer()
    return MediationDataConsumer._instance


if __name__ == "__main__":
  logging.basicConfig(
    format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
    level=logging.INFO
  )
  threads = [
    MediationDataConsumer()
  ]

  for t in threads:
    t.start()
  """
  data = {"country": "CZ",
          "lobName": "ACI",
          "type": "inputs",
          "flowName": "GSM",
          "dataSize": 497464,
          "time": "05.05.2017 15:03:24"}
  MediationDataConsumer().saveMediationData(data)
  """
