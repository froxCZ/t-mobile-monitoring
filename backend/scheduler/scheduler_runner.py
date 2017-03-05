import logging
import time

import schedule

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
from scheduler.lob.LobScheduler import LobScheduler

# LobScheduler().run()
#
MODULE_SCHEDULERS = {
  5: [LobScheduler()],

}

for seconds, schedulers in MODULE_SCHEDULERS.items():
  for scheduler in schedulers:
    schedule.every(seconds).seconds.do(scheduler.run)

while True:
  schedule.run_pending()
  time.sleep(1)
