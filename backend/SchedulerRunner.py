import logging

from scheduler.Scheduler import Scheduler
class SchedulerRunner():
  def __init__(self):
    super().__init__()

  def start(self):
    threads = [Scheduler()]
    for t in threads:
      t.start()

if __name__ == "__main__":
  logging.basicConfig(format='%(levelname)s [%(module)s]: %(message)s', level=logging.DEBUG)
  SchedulerRunner().start()
