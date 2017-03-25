import datetime
import logging
import threading
from queue import Queue, Empty

import config
from config import AppConfig
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
    runResult = analyzer.run(config.getCurrentTime().replace(tzinfo=AppConfig.getTimezone()))
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
          logging.error("Error while analyzing flow. " + str(e))
    except Empty as e:
      pass


class FlowAnalyzerExecutor(AbstractExecutor):

  def __init__(self):
    super().__init__("MediationAnalyzerExecutor")
    self.statusManager = FlowStatusManager()

  def _executeInternal(self):
    flowQueue = Queue()
    for country in MediationConfig.getCountryList():
      self._enqueFlowsToAnalyze(flowQueue, country)
    if not flowQueue.empty():
      workers = [Worker(flowQueue, self.statusManager) for i in range(0, MediationConfig.threadsCount())]
      for worker in workers:
        worker.start()
      for worker in workers:
        worker.join()

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
    if lastTicTime < config.getCurrentTime() - datetime.timedelta(minutes=2 * granularity):
      return True
    else:
      return False


if __name__ == "__main__":
  logging.basicConfig(format='%(levelname)s [%(module)s]: %(message)s', level=logging.DEBUG)
  FlowAnalyzerExecutor().execute()
  print("x")