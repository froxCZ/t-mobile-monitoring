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

logging.getLogger('kafka').setLevel(logging.CRITICAL)


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
  daemon = True

  def __init__(self):
    super().__init__()
    if IntegrationConfig.outputTopic() is not None:
      self.q = Queue()
      self.emailSender = EmailSender.instance()
      self.start()
      self.sendingSuccess = None
      self.kafkaProducer = None

  def _startProducer(self):
    try:
      assert IntegrationConfig.kafkaServers() is not None
      self.kafkaProducer = KafkaProducer(
        bootstrap_servers=IntegrationConfig.kafkaServers(),
        value_serializer=jsonDictSerializer,
        request_timeout_ms=3000
      )
    except Exception as e:
      logging.exception("Failed to connect to kafka.")
      time.sleep(120)
      raise e

  def run(self):
    while True:
      dictMsg = None
      try:
        dictMsg = self.q.get()
        if self.kafkaProducer is None:
          self._startProducer()
        self.kafkaProducer.send(IntegrationConfig.outputTopic(), dictMsg).get(3)
        self.sendingSuccess = True
      except Exception as e:
        if self.sendingSuccess:
          self.emailSender.sendEmail("kafka", "Failed to send message " + str(dictMsg))
          self.sendingSuccess = False
        if dictMsg is not None and self.q.qsize() < 10000:
          self.q.put(dictMsg)

  def send(self, dictMsg):
    if IntegrationConfig.outputTopic() is not None:
      dictMsg["messageId"] = util.randomHash(10)
      dictMsg["time"] = AppConfig.getCurrentTime()
      self.q.put(dictMsg)

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
