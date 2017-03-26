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

  def startScheduling(self):
    for seconds, executors in self.executors.items():
      for executor in executors:
        schedule.every(seconds).seconds.do(executor.execute)

    while True:
      schedule.run_pending()
      time.sleep(1)
