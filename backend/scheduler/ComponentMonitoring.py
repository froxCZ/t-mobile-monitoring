
from common import AppConfig
from integration import MediationDataConsumer
from integration import MediationStatusProducer
from scheduler.AbstractExecutor import AbstractExecutor
from scheduler.AbstractScheduler import AbstractScheduler


class ComponentMonitoring(AbstractExecutor):
  """
  Executor which saves status of kafka consumer and producer to the database.
  """
  name = "ComponentMonitoring"
  interval = 10
  maxRunningTime = 5
  def __init__(self):
    super().__init__(ComponentMonitoring.name,ComponentMonitoring.interval)

  def _executeInternal(self):
    from common import SystemStatusManager
    SystemStatusManager.setKafkaComponentStatus(MediationStatusProducer.name,
                                                MediationStatusProducer.instance().status,
                                                AppConfig.getCurrentTime())
    SystemStatusManager.setKafkaComponentStatus(MediationDataConsumer.name,
                                                MediationDataConsumer.instance().status,
                                                AppConfig.getCurrentTime())


class ComponentMonitoringScheduler(AbstractScheduler):
  def __init__(self):
    super().__init__([ComponentMonitoring()])
