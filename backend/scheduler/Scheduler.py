import logging
import threading
import time

import schedule

from zookeeper.analyzer import AnalyzerExecutor

"""
deprecated
"""

class Scheduler(threading.Thread):
  def __init__(self):
    super().__init__()

  def run(self):
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
    from mediation.flow_analyzer import MediationAnalyzerExecutor
    MODULE_SCHEDULERS = {
      5:[AnalyzerExecutor()],
      15: [MediationAnalyzerExecutor()],

    }

    for seconds, schedulers in MODULE_SCHEDULERS.items():
      for scheduler in schedulers:
        schedule.every(seconds).seconds.do(scheduler.execute)

    while True:
      schedule.run_pending()
      time.sleep(1)