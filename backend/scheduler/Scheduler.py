import logging
import threading
import time

import schedule

from zookeeper.analyzer import ZookeeperAnalyzerRunner


class Scheduler(threading.Thread):
  def __init__(self):
    super().__init__()

  def run(self):
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    from mediation.flow_analyzer import FlowAnalyzerRunner
    MODULE_SCHEDULERS = {
      5:[ZookeeperAnalyzerRunner()],
      5*60: [FlowAnalyzerRunner()],

    }

    for seconds, schedulers in MODULE_SCHEDULERS.items():
      for scheduler in schedulers:
        scheduler.run()
        schedule.every(seconds).seconds.do(scheduler.run)

    while True:
      schedule.run_pending()
      time.sleep(1)