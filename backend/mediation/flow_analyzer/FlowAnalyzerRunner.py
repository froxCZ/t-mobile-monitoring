import datetime
import logging

import config
from config import AppConfig
from mediation import MediationConfig
from mediation.flow_analyzer import status
from mediation.flow_analyzer.FlowAnalyzer import FlowAnalyzer
from mediation.flow_analyzer.FlowStatusManager import FlowStatusManager
from mediation.flow_analyzer.StatusChangeNotificator import StatusChangeNotificator
from scheduler.AbstractAnalyzerRunner import AbstractAnalyzerRunner


class FlowAnalyzerRunner(AbstractAnalyzerRunner):
  name = "FlowAnalyzerRunner"

  def __init__(self):
    super().__init__()
    self.manager = FlowStatusManager()
    self.notificator = StatusChangeNotificator()

  def _runInternal(self):
    for country in MediationConfig.getCountryList():
      self._analyzeContry(country)

  def _analyzeContry(self, country):
    self.lastExecutions = self.manager.getAll(country)

    flowsToAnalyze = self._getFlowsToAnalyze(country)
    if (len(flowsToAnalyze)) == 0:
      logging.debug("no flows to analyze")

    for flow in flowsToAnalyze:
      self._analyzeFlow(flow)

  def _analyzeFlow(self, flow):
    analyzer = FlowAnalyzer(flow)
    runResult = analyzer.run(config.getCurrentTime().replace(tzinfo=AppConfig.getTimezone()))
    previousStatus = self.lastExecutions[flow["gName"]]["status"]
    newStatus = analyzer.status
    if previousStatus != newStatus:
      self.notificator.statusChanged(flow, previousStatus, newStatus, analyzer.ticTime)
    self.manager.saveStatus(flow, newStatus, analyzer.difference, analyzer.ticTime)

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
  FlowAnalyzerRunner().run()
