from scheduler.AbstractScheduler import AbstractScheduler
from zookeeper.analyzer import ZookeeperAnalyzerExecutor


class ZookeeperScheduler(AbstractScheduler):
  def __init__(self):
    super().__init__([ZookeeperAnalyzerExecutor()])

