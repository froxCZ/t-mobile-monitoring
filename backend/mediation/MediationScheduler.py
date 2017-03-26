from mediation.flow_analyzer import DiscoverFlowsExecutor
from mediation.flow_analyzer import MediationAnalyzerExecutor
from scheduler.AbstractScheduler import AbstractScheduler


class MediationScheduler(AbstractScheduler):
  def __init__(self):
    executors = {
      15: [MediationAnalyzerExecutor()],
      60 * 60: [DiscoverFlowsExecutor()]
    }
    super().__init__(executors)
