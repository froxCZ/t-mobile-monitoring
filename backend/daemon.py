from mediation import MediationScheduler
from scheduler.ComponentMonitoring import ComponentMonitoringScheduler
from zookeeper import ZookeeperScheduler

MediationScheduler().start()
ZookeeperScheduler().start()
ComponentMonitoringScheduler().start()
