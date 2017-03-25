from scheduler.AbstractScheduler import AbstractScheduler
from zookeeper.analyzer import AnalyzerExecutor


class ZookeeperScheduler(AbstractScheduler):
  def __init__(self):
    executors = {
      5: [AnalyzerExecutor()],
    }
    super().__init__(executors)
