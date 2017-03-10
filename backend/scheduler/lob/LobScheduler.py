import datetime
import logging

from config import TIMEZONE
from config import config
from flow_analyzer import FlowAnalyzer
from scheduler.AbstractModuleScheduler import AbstractModuleScheduler
from scheduler.lob.LobScheduleHistory import LobScheduleHistory


class LobScheduler(AbstractModuleScheduler):
  name = "LobScheduler"

  def run(self):
    super(LobScheduler, self).run()
    lobsConfig = config.getLobsConfig()["lobs"]
    lobScheduleHistory = LobScheduleHistory()
    self.lastExecutions = lobScheduleHistory.getLastSuccessfullExecutions()
    jobsToSchedule = {}
    for lobName, lob in lobsConfig.items():
      for flow in {**lob["forwards"], **lob["inputs"]}.values():
        if self.shouldSchedule(flow):
          granularity = flow["options"]["granularity"]
          l = jobsToSchedule.get(granularity, [])
          l.append(flow)
          jobsToSchedule[granularity] = l
    if(len(jobsToSchedule)) == 0:
      logging.debug("no jobs to execute")
    for gran, flowList in sorted(jobsToSchedule.items()):
      for flow in flowList:
        time = datetime.datetime.now().replace(tzinfo=TIMEZONE)
        analyzer = FlowAnalyzer(flow,datetime.datetime.now().replace(tzinfo=TIMEZONE))
        runResult = analyzer.run()
        if runResult == 0:
          lobScheduleHistory.saveSuccessfullExecution(flow, time)

  def shouldSchedule(self, flow):
    lastExecutionTime = datetime.datetime.min.replace(tzinfo=TIMEZONE)
    granularity = flow["options"]["granularity"]
    if flow["gName"] in self.lastExecutions:
      lastExecution = self.lastExecutions[flow["gName"]]
      if lastExecution["result"] == 0:
        lastExecutionTime = lastExecution["finishTime"]
    if lastExecutionTime < datetime.datetime.now().replace(tzinfo=TIMEZONE) - datetime.timedelta(minutes=granularity):
      return True
    else:
      return False


if __name__ == "__main__":
  logging.basicConfig(format='%(levelname)s [%(module)s]: %(message)s', level=logging.DEBUG)
  LobScheduler().run()
