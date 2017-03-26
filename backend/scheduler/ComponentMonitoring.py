
from config import AppConfig
from integration import MediationDataConsumer
from integration import StatusProducer
from scheduler.AbstractExecutor import AbstractExecutor
from scheduler.AbstractScheduler import AbstractScheduler


class ComponentMonitoring(AbstractExecutor):
  name = "ComponentMonitoring"
  interval = 10
  maxRunningTime = 5
  def __init__(self):
    super().__init__(ComponentMonitoring.name,ComponentMonitoring.interval)

  def _executeInternal(self):
    from common import SystemStatusManager
    SystemStatusManager.setKafkaComponentStatus(StatusProducer.name,
                                                StatusProducer.instance().status,
                                                AppConfig.getCurrentTime())
    SystemStatusManager.setKafkaComponentStatus(MediationDataConsumer.name,
                                                MediationDataConsumer.instance().status,
                                                AppConfig.getCurrentTime())


class ComponentMonitoringScheduler(AbstractScheduler):
  def __init__(self):
    super().__init__([ComponentMonitoring()])
