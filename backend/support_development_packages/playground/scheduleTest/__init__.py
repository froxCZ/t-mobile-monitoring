import logging
import time

import schedule

from scheduler.AbstractExecutor import AbstractExecutor

"""
demonstrates how scheduler behaves when there is some long running task.
"""
class Worker(AbstractExecutor):
  def _executeInternal(self):
    print("asd")
    time.sleep(5)


class Scheduler:
  def __init__(self):
    super().__init__()

  def run(self):
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

    schedule.every(3).seconds.do(Worker().execute)

    while True:
      schedule.run_pending()
      print("finished")
      time.sleep(0.5)

Scheduler().run()