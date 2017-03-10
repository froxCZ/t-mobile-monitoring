import datetime
import logging

import config
from config import TIMEZONE
from flow_analyzer import FlowAnalyzer
from flow_analyzer.FlowAnalyzerRunnerHistory import FlowAnalyzerRunnerHistory
from scheduler.AbstractModuleScheduler import AbstractModuleScheduler


class FlowAnalyzerRunner(AbstractModuleScheduler):
  name = "FlowAnalyzerRunner"

  def __init__(self):
    super().__init__()
    self.runHistory = FlowAnalyzerRunnerHistory()
    self.runHistory.removeAllExecutions()
    #delete status history

  def run(self):
    super(FlowAnalyzerRunner, self).run()
    lobsConfig = config.getLobsConfig()["lobs"]

    self.lastExecutions = self.runHistory.getLastSuccessfullExecutions()
    jobsToSchedule = {}
    for lobName, lob in lobsConfig.items():
      for flow in {**lob["forwards"], **lob["inputs"]}.values():
        if self.shouldSchedule(flow):
          granularity = flow["options"]["granularity"]
          l = jobsToSchedule.get(granularity, [])
          l.append(flow)
          jobsToSchedule[granularity] = l
    if (len(jobsToSchedule)) == 0:
      logging.debug("no jobs to execute")
    for gran, flowList in sorted(jobsToSchedule.items()):
      for flow in flowList:
        time = config.getCurrentTime()
        analyzer = FlowAnalyzer(flow)
        runResult = analyzer.run(config.getCurrentTime().replace(tzinfo=TIMEZONE))
        if runResult == 0:
          self.runHistory.saveSuccessfullExecution(flow, time)

  def shouldSchedule(self, flow):
    lastExecutionTime = datetime.datetime.min.replace(tzinfo=TIMEZONE)
    granularity = flow["options"]["granularity"]
    if flow["gName"] in self.lastExecutions:
      lastExecution = self.lastExecutions[flow["gName"]]
      if lastExecution["result"] == 0:
        lastExecutionTime = lastExecution["finishTime"]
    if lastExecutionTime < config.getCurrentTime() - datetime.timedelta(minutes=granularity):
      return True
    else:
      return False


if __name__ == "__main__":
  logging.basicConfig(format='%(levelname)s [%(module)s]: %(message)s', level=logging.DEBUG)
  FlowAnalyzerRunner().run()
