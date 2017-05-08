from integration import MediationStatusProducer
from mediation.flow_analyzer import EventsManager


class StatusChangeNotificator:
  def __init__(self):
    self.statusProducer = MediationStatusProducer.instance()
    pass

  def statusChanged(self, flow, previousStatus, newStatus, ticTime):
    msg = "Changed from " + previousStatus + " to " + newStatus
    EventsManager.logStatusChangeEvent(flow, msg, ticTime, newStatus)
    msgDict = {
      "system": "mediation",
      "lobName": flow["lobName"],
      "ticTime": ticTime,
      "newStatus": newStatus,
      "previousStatus": previousStatus,
      "country": flow["country"]
    }
    self.statusProducer.send(msgDict)
