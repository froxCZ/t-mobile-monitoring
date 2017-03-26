import logging

import config
from integration import StatusProducer
from scheduler.AbstractExecutor import AbstractExecutor
from zookeeper.analyzer.Analyzer import Analyzer
from zookeeper.analyzer.StatusManager import StatusManager


class ZookeeperAnalyzerExecutor(AbstractExecutor):
  name = "ZookeeperAnalyzerExecutor"
  def __init__(self):
    super().__init__(ZookeeperAnalyzerExecutor.name)
    self.analyzer = Analyzer()

  def _executeInternal(self):
    clusterStatus = self.analyzer.run()
    self.checkStatusChange(StatusManager.getClusterStatus(), clusterStatus)
    StatusManager.saveClusterStatus(clusterStatus, config.getCurrentTime())

  def checkStatusChange(self, oldClusterStatus, newClusterStatus):
    statusChange = {"nodes": {}, "system": "zookeeper"}
    change = False
    try:
      if newClusterStatus["status"] == "DISABLED":
        return
      for nodeName, node in newClusterStatus["nodes"].items():
        oldNode = oldClusterStatus["nodes"].get(nodeName, None)
        if oldNode is None:
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
        StatusProducer.instance().send(statusChange)
    except Exception as e:
      logging.exception("Exception while checking zookeeper status change.")


if __name__ == '__main__':
  ZookeeperAnalyzerExecutor().execute()
