import abc
import datetime


class BaseDateQuery:
  def __init__(self):
    self.query = None
    self.coll = None

  def execute(self):
    self.prepare()
    result = list(self.coll.aggregate(self.query))
    for i in result:
      group = i["_id"]
      date = datetime.datetime(group["year"], group["month"], group["dayOfMonth"], int(group["hour"]),
                               int(group["minute"]))
      i["_id"] = date
    result = sorted(result, key=lambda x: x["_id"])
    return result

  @abc.abstractmethod
  def prepare(self):
    pass
