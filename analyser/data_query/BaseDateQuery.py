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
      date.replace(tzinfo=None)
      i["_id"] = date
      for key in i.keys():
        if key == "_id":
          continue
        newKey = key.replace("_", ".")
        if key != newKey:
          i[newKey] = i[key]
          del i[key]

    result = sorted(result, key=lambda x: x["_id"])
    return result

  @abc.abstractmethod
  def prepare(self):
    pass
