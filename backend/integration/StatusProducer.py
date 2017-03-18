import json
import threading
import time
from datetime import datetime
from queue import Queue

from kafka import KafkaProducer

import util
from config import AppConfig
from integration import EmailSender


def jsonDictSerializer(dictToSend):
  baseTypeDict = {}
  for k, v in dictToSend.items():
    if type(v) == datetime:
      baseTypeDict[k] = util.dateToTimeString(v)
    else:
      baseTypeDict[k] = v
  serialized = json.dumps(baseTypeDict)
  return bytes(serialized, encoding='utf-8')


class StatusProducer(threading.Thread):
  _instance = None

  def __init__(self):
    super().__init__()
    self.q = Queue()
    self.kafkaProducer = KafkaProducer(
      bootstrap_servers=AppConfig.kafkaServers(),
      value_serializer=jsonDictSerializer,
      request_timeout_ms=3000

    )
    self.emailSender = EmailSender.instance()
    self.start()
    self.sendingSuccess = None

  def run(self):
    while True:
      dictMsg = None
      try:
        dictMsg = self.q.get()
        x = self.kafkaProducer.send('mediationMonitoringStatus', dictMsg).get(3)
        print("sent " + str(dictMsg))
        self.sendingSuccess = True
      except Exception as e:
        if self.sendingSuccess:
          self.emailSender.sendEmail("kafka", "Failed to send message " + str(dictMsg))
          self.sendingSuccess = False
        if dictMsg is not None and self.q.qsize() < 100000:
          self.q.put(dictMsg)

  def send(self, dictMsg):
    dictMsg["messageId"] = util.randomHash(10)
    dictMsg["time"] = AppConfig.getCurrentTime()
    self.q.put(dictMsg)
    print("queued " + str(dictMsg))

  @staticmethod
  def instance():
    if StatusProducer._instance is None:
      StatusProducer._instance = StatusProducer()
    return StatusProducer._instance


if __name__ == "__main__":
  # logging.basicConfig(
  #   format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
  #   level=logging.INFO
  # )
  msg = {
    "system": "mediation",
    "country": "CZ",
    "lobName": "ACI",
    "flowName": "GSM",
    "ticTime": AppConfig.getCurrentTime(),
    "time": AppConfig.getCurrentTime(),
    "newStatus": "OK",
    "previousStatus": "N_A"
  }
  i = 0
  while True:
    StatusProducer.instance().send({"c": i})
    time.sleep(3)
    i += 1
