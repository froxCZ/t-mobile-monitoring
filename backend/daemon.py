from integration import MediationDataConsumer
from mediation import MediationScheduler
from scheduler.ComponentMonitoring import ComponentMonitoringScheduler
from zookeeper import ZookeeperScheduler
MediationDataConsumer.instance().start()
MediationScheduler().start()
ZookeeperScheduler().start()
ComponentMonitoringScheduler().start()
