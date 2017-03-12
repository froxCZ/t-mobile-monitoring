import logging


class StatusChangeNotificator:
  def __init__(self):
    pass

  def statusChanged(self, flow, previousStatus, newStatus, ticTime):
    logging.info("status change notification: " +
                 flow["gName"] + " from " + previousStatus + " to " + newStatus + " tic: " + str(ticTime))
