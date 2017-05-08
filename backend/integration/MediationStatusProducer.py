import json
import logging
import threading
import time
from datetime import datetime
from queue import Queue

from kafka import KafkaProducer

import util
from config import AppConfig
from integration import EmailSender
from integration import IntegrationConfig


def jsonDictSerializer(dictToSend):
  baseTypeDict = {}
  for k, v in dictToSend.items():
    if type(v) == datetime:
      baseTypeDict[k] = util.dateToTimeString(v)
    else:
      baseTypeDict[k] = v
  serialized = json.dumps(baseTypeDict)
  return bytes(serialized, encoding='utf-8')


class MediationStatusProducer(threading.Thread):
  name = "MediationStatusProducer"
  _instance = None
  daemon = True

  def __init__(self):
    super().__init__()
    self.status = "DISCONNECTED"
    self.q = Queue()
    self.emailSender = EmailSender.instance()
    self.start()
    self.sendingSuccess = None
    self.kafkaProducer = None

  def _startProducer(self):
    if IntegrationConfig.outputTopic() is not None and IntegrationConfig.kafkaServers() is not None:
      while True:
        try:
          kafkaProducer = KafkaProducer(
            bootstrap_servers=IntegrationConfig.kafkaServers(),
            value_serializer=jsonDictSerializer,
            request_timeout_ms=3000
          )
          self.status = "CONNECTED"
          self.kafkaProducer = kafkaProducer
          return True
        except Exception as e:
          logging.exception("Failed to connect to kafka.")
          time.sleep(120)
    else:
      self.status = "NOT_CONFIGURED"
      return False

  def run(self):
    if self._startProducer():
      while True:
        dictMsg = None
        try:
          dictMsg = self.q.get()
          self.kafkaProducer.send(IntegrationConfig.outputTopic(), dictMsg).get(3)
          self.status = "CONNECTED"
          self.sendingSuccess = True
        except Exception as e:
          self.status = "DISCONNECTED"
          if self.sendingSuccess:
            self.emailSender.sendEmail("kafka", "Failed to send message " + str(dictMsg))
            self.sendingSuccess = False
          if dictMsg is not None and self.q.qsize() < 10000:
            self.q.put(dictMsg)

  def send(self, dictMsg):
    if self.status != "NOT_CONFIGURED":
      dictMsg["messageId"] = util.randomHash(10)
      dictMsg["time"] = AppConfig.getCurrentTime()
      self.q.put(dictMsg)

  @staticmethod
  def instance():
    if MediationStatusProducer._instance is None:
      MediationStatusProducer._instance = MediationStatusProducer()
    return MediationStatusProducer._instance


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
    MediationStatusProducer.instance().send({"c": i})
    time.sleep(3)
    i += 1
