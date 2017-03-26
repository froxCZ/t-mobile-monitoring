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
    myScheduler = schedule.Scheduler()
    for executor in self.executors:
        executor.execute()

    for executor in self.executors:
      myScheduler.every(executor.getInterval()).seconds.do(executor.execute)

    while True:
      myScheduler.run_pending()
      time.sleep(1)
