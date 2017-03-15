import config
from scheduler.AbstractModuleScheduler import AbstractModuleScheduler
from zookeeper.analyzer import StatusManager
from zookeeper.analyzer.Analyzer import Analyzer


class ZookeeperAnalyzerRunner(AbstractModuleScheduler):
  name = "ZookeeperAnalyzerRunner"

  def __init__(self):
    super().__init__()
    self.analyzer = Analyzer()

  def run(self):
    super().run()
    clusterStatus = self.analyzer.run()
    StatusManager.saveClusterStatus(clusterStatus,config.getCurrentTime())


if __name__ == '__main__':
  ZookeeperAnalyzerRunner().run()