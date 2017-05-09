from mediation.flow_analyzer import DiscoverFlowsExecutor
from mediation.flow_analyzer import MediationAnalyzerExecutor
from scheduler.AbstractScheduler import AbstractScheduler

"""
Scheduler started by monitoring daemon on background. This class periodically runs other mediation executors.
"""
class MediationScheduler(AbstractScheduler):
  def __init__(self):
    executors = [MediationAnalyzerExecutor(),DiscoverFlowsExecutor()]
    super().__init__(executors)
