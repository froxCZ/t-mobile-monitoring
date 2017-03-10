import logging
import time

import schedule

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
from flow_analyzer import FlowAnalyzerRunner

# FlowAnalyzerRunner().run()
#
MODULE_SCHEDULERS = {
  5*60: [FlowAnalyzerRunner()],

}

for seconds, schedulers in MODULE_SCHEDULERS.items():
  for scheduler in schedulers:
    scheduler.run()
    schedule.every(seconds).seconds.do(scheduler.run)

while True:
  schedule.run_pending()
  time.sleep(1)
