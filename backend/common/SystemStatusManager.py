import datetime

from config import AppConfig
from integration import MediationDataConsumer
from integration import StatusProducer
from mediation.flow_analyzer import MediationAnalyzerExecutor
from mongo import mongo
from zookeeper.analyzer import ZookeeperAnalyzerExecutor

statusColl = mongo.statuses()


def _statusIsExpired(time, maxMinutes=5):
  return AppConfig.getCurrentTime() - time > datetime.timedelta(minutes=maxMinutes)


class SystemStatusManager:
  @staticmethod
  def getStatus():
    from scheduler.ComponentMonitoring import ComponentMonitoring
    executors = [ComponentMonitoring.name, ZookeeperAnalyzerExecutor.name, MediationAnalyzerExecutor.name]
    kafkaComponents = [StatusProducer.name,MediationDataConsumer.name]
    systemStatus = {"executors": {}, "kafka": {}}
    res = statusColl.find_one({"_id": "system"}, {"_id": 0})
    if res == None:
      res = {}
    for executorName in executors:
      executorStatus = res.get("executors", {}).get(executorName, None)
      if executorStatus is None or _statusIsExpired(executorStatus["time"]):
        systemStatus["executors"][executorName] = "FAIL"
      else:
        systemStatus["executors"][executorName] = executorStatus["status"]

    for componentName in kafkaComponents:
      componentStatus = res.get("kafka", {}).get(componentName, None)
      if componentStatus is None or _statusIsExpired(componentStatus["time"]):
        systemStatus["kafka"][componentName] = "FAIL"
      else:
        systemStatus["kafka"][componentName] = componentStatus["status"]
    hasFail = False
    for executorStatus in systemStatus["executors"].values():
      if executorStatus == "FAIL":
        hasFail = True
    for kafkaStatus in systemStatus["kafka"].values():
      if kafkaStatus == "FAIL" or kafkaStatus == "DISCONNECTED":
        hasFail = True
    if hasFail:
      systemStatus["status"] = "FAIL"
    else:
      systemStatus["status"] = "OK"
    return systemStatus

  @staticmethod
  def setKafkaComponentStatus(name, status, time):
    statusColl.update_one({"_id": "system"},
                          {"$set": {"kafka." + name: {"time": time, "status": status}}}, upsert=True)

  @staticmethod
  def saveExecutorSuccessfulExecution(executorName, time):
    statusColl.update_one({"_id": "system"},
                          {"$set": {"executors." + executorName: {"time": time, "status": "OK"}}}, upsert=True)
