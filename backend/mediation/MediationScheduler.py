from mediation.flow_analyzer import DiscoverFlowsExecutor
from mediation.flow_analyzer import MediationAnalyzerExecutor
from scheduler.AbstractScheduler import AbstractScheduler


class MediationScheduler(AbstractScheduler):
  """
  Scheduler started by monitoring daemon on background. This class periodically runs other mediation executors.
  """
  def __init__(self):
    executors = [MediationAnalyzerExecutor(),DiscoverFlowsExecutor()]
    super().__init__(executors)
