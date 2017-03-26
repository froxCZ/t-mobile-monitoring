from scheduler.AbstractScheduler import AbstractScheduler
from zookeeper.analyzer import ZookeeperAnalyzerExecutor


class ZookeeperScheduler(AbstractScheduler):
  def __init__(self):
    executors = {
      5: [ZookeeperAnalyzerExecutor()],
    }
    super().__init__(executors)
