# def load():
#   import sys
#   paths = ['/home/frox/school/thesis/nodejs/bigmon/backend']
#   for p in paths:
#     sys.path.insert(0, p)
#
#
# load()
import threading
from queue import Queue

from common import AppConfig
from mediation import MediationConfig
from mediation.flow_analyzer import FlowAnalyzer

queue = Queue()


class Worker(threading.Thread):
  def __init__(self, queue):
    super().__init__()
    self.queue = queue

  def run(self):
    try:
      while True:
        job = self.queue.get_nowait()
        FlowAnalyzer(job).run(AppConfig.getCurrentTime())
    except Exception as e:
      pass


for lob in MediationConfig.getLobs("CZ", enabledOnly=True).values():
  for flow in lob["flows"].values():
    queue.put(flow)
workers = [Worker(queue) for i in range(0, 8)]
for worker in workers:
  worker.start()

for worker in workers:
  worker.join()

print("finished")
