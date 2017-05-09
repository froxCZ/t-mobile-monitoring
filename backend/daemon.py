import logging

from integration import MediationDataConsumer
from integration import MediationStatusProducer
from mediation import MediationScheduler
from scheduler.ComponentMonitoring import ComponentMonitoringScheduler
from zookeeper import ZookeeperScheduler

MediationDataConsumer.instance().start()
MediationStatusProducer.instance()
MediationScheduler().start()
ZookeeperScheduler().start()
ComponentMonitoringScheduler().start()
logging.getLogger('kafka').setLevel(logging.CRITICAL)
logging.getLogger('schedule').setLevel(logging.CRITICAL)