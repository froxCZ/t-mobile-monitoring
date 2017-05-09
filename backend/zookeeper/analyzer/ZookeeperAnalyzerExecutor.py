import logging

from config import AppConfig
from integration import MediationStatusProducer
from scheduler.AbstractExecutor import AbstractExecutor
from zookeeper.analyzer.Analyzer import Analyzer
from zookeeper.analyzer.StatusManager import StatusManager


class ZookeeperAnalyzerExecutor(AbstractExecutor):
  name = "ZookeeperAnalyzerExecutor"
  interval = 5
  maxRunningTime = 5

  def __init__(self):
    super().__init__(ZookeeperAnalyzerExecutor.name, ZookeeperAnalyzerExecutor.interval)
    self.analyzer = Analyzer()

  def _executeInternal(self):
    clusterStatus = self.analyzer.run()
    self.checkStatusChange(StatusManager.getClusterStatus(), clusterStatus)
    StatusManager.saveClusterStatus(clusterStatus, AppConfig.getCurrentTime())

  def checkStatusChange(self, oldClusterStatus, newClusterStatus):
    statusChange = {"nodes": {}, "system": "zookeeper"}
    change = False
    try:
      if newClusterStatus["status"] == "DISABLED":
        return
      for nodeName, node in newClusterStatus["nodes"].items():
        oldNode = oldClusterStatus["nodes"].get(nodeName, None)
        if oldNode is None or "status" not in oldNode:
          statusChange["nodes"][nodeName] = {"previousStatus": None, "newStatus": node["status"]}
          change = True
        else:
          if oldNode["status"] != node["status"]:
            statusChange["nodes"][nodeName] = {"previousStatus": oldNode["status"], "newStatus": node["status"]}
            change = True
      if oldClusterStatus["status"] != newClusterStatus["status"]:
        statusChange["status"] = {"previousStatus": oldClusterStatus["status"], "newStatus": newClusterStatus["status"]}
        change = True
      if change:
        MediationStatusProducer.instance().send(statusChange)
    except Exception as e:
      logging.exception("Exception while checking zookeeper status change.")


if __name__ == '__main__':
  ZookeeperAnalyzerExecutor().execute()
