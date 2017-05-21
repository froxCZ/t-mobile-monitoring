import datetime
import logging
import threading
import time
from queue import Queue, Empty

from common import AppConfig
from mediation import MediationConfig
from mediation.flow_analyzer import FlowAnalyzer
from mediation.flow_analyzer import status
from mediation.flow_analyzer.FlowStatusManager import FlowStatusManager
from scheduler.AbstractExecutor import AbstractExecutor


class Worker(threading.Thread):
  def __init__(self, queue, statusManager):
    super().__init__()
    self.queue = queue
    self.statusManager = statusManager

  def _analyzeFlow(self, flow, lastExecution):
    analyzer = FlowAnalyzer(flow)
    analyzer.run(AppConfig.getCurrentTime())
    previousStatus = lastExecution["status"]
    newStatus = analyzer.status
    self.statusManager.saveStatus(flow, previousStatus, newStatus, analyzer.difference, analyzer.ticTime)

  def run(self):
    try:
      while True:
        try:
          job = self.queue.get_nowait()
          self._analyzeFlow(job["flow"], job["lastExecution"])
        except Exception as e:
          if type(e) is Empty:
            raise Empty
          logging.exception("Error while analyzing flow.")
    except Empty as e:
      pass


class MediationAnalyzerExecutor(AbstractExecutor):
  name = "MediationAnalyzerExecutor"
  interval = 15
  maxRunningTime = 5 * 60

  def __init__(self):
    super().__init__(MediationAnalyzerExecutor.name, MediationAnalyzerExecutor.interval)
    self.statusManager = FlowStatusManager()

  def _executeInternal(self):
    flowQueue = Queue()
    for country in MediationConfig.getCountryList():
      self._enqueFlowsToAnalyze(flowQueue, country)
    if not flowQueue.empty():
      start = time.time()
      flowsToAnalyzeCnt = flowQueue.unfinished_tasks
      logging.info("Going to analyze " + str(flowsToAnalyzeCnt)+" flows")
      workers = [Worker(flowQueue, self.statusManager) for i in range(0, MediationConfig.threadsCount())]
      for worker in workers:
        worker.start()
      for worker in workers:
        worker.join()
      logging.info("Finished analyzing " + str(flowsToAnalyzeCnt) +
                   " flows. Time: " + str(int(time.time() - start)) + " seconds.")

  def _enqueFlowsToAnalyze(self, flowQueue, country):
    self.lastExecutions = self.statusManager.getAll(country)
    countryLobs = MediationConfig.getLobs(country, enabledOnly=True)
    for lobName, lob in countryLobs.items():
      for flow in lob["flows"].values():
        if self.shouldSchedule(flow):
          job = {"flow": flow, "lastExecution": self.lastExecutions[flow["gName"]]}
          flowQueue.put(job)

  def _getFlowsToAnalyze(self, country):
    flowsToAnalyze = []
    lobsConfig = MediationConfig.getLobs(country, enabledOnly=True)
    for lobName, lob in lobsConfig.items():
      for flow in lob["flows"].values():
        if self.shouldSchedule(flow):
          flowsToAnalyze.append(flow)
    return flowsToAnalyze

  def shouldSchedule(self, flow):
    granularity = flow["options"]["granularity"]
    lastExecution = self.lastExecutions[flow["gName"]]
    if lastExecution["status"] == status.NA:
      return True
    lastTicTime = lastExecution["ticTime"]
    if lastTicTime < AppConfig.getCurrentTime() - datetime.timedelta(minutes=2 * granularity):
      return True
    else:
      return False


if __name__ == "__main__":
  logging.basicConfig(format='%(levelname)s [%(module)s]: %(message)s', level=logging.DEBUG)
  MediationAnalyzerExecutor().execute()
  print("x")
