import json
import logging
import threading

from kafka import KafkaConsumer

import util
from config import AppConfig
from mongo import mongo


class MediationDataConsumer(threading.Thread):
  daemon = False

  def run(self):
    consumer = KafkaConsumer(bootstrap_servers=AppConfig.kafkaServers(),
                             auto_offset_reset='latest',
                             enable_auto_commit=True,
                             group_id="mediationMonitoring")
    consumer.subscribe(['mediationData'])

    for message in consumer:
      try:
        self.processMessage(message)
      except Exception as e:
        logging.warning(str(e))

  def processMessage(self, message):
    try:
      value = message.value.decode('utf-8')
      row = json.loads(value)
      return self.saveMediationData(row)
    except Exception as e:
      logging.error("Error while processing mediation data " + str(e))
      return True

  def saveMediationData(self, row):
    """
    :param data:
    dict{"country":"CZ",
    "lob":"ACI",
    "type":"inputs",
    "flowName":"GSM",
    "dataSize":497464,
    "time":"01.01.2017 00:00:24"}
    :return:
    """
    time = util.stringToTime(row["time"]).replace(second=0)
    updatePath = "data." + row["country"] + "." + row["lob"] + "." + row["type"] + "."
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
      mongo.lobs().update({'_id': time}, updateObj, upsert=True)
      logging.info(
        "Inserted row for " + row["lob"] + " " + row["flowName"] + " at " + str(time) + " of size " + str(dataSize))
      return True
    except Exception as e:
      logging.error("Error while persisting data " + str(row) + " exception: " + str(e))
      return False


def main():
  threads = [
    MediationDataConsumer()
  ]

  for t in threads:
    t.start()


if __name__ == "__main__":
  logging.basicConfig(
    format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
    level=logging.INFO
  )
  main()
  """
  data = {"country": "CZ",
          "lob": "ACI",
          "type": "inputs",
          "flowName": "GSM",
          "dataSize": 497464,
          "time": "05.05.2017 15:03:24"}
  MediationDataConsumer().saveMediationData(data)
  """
