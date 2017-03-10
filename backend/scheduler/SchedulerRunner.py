from scheduler.Scheduler import Scheduler
class SchedulerRunner():
  def __init__(self):
    super().__init__()

  def start(self):
    threads = [Scheduler()]
    for t in threads:
      t.start()
