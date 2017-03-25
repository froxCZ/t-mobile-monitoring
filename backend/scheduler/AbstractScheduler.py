import abc
import threading
import time

import schedule


class AbstractScheduler(threading.Thread):
  name = ""

  def __init__(self, executors):
    super().__init__()
    self.executors = executors

  def run(self):
    self.startScheduling()

  @abc.abstractmethod
  def startScheduling(self):
    for seconds, schedulers in self.executors.items():
      for scheduler in schedulers:
        schedule.every(seconds).seconds.do(scheduler.execute)

    while True:
      schedule.run_pending()
      time.sleep(1)
