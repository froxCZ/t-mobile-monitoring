from . import outageColl


class OutageQuery:
  def __init__(self, lobName, ):
    self.lobName = lobName

  def getOutages(self, fromDate, toDate):
    """

    :return: list of datetime objects, when this lob name had outage
    """
    lobMongoPath = "lobs." + self.lobName
    res = list(outageColl.find(
      {"_id": {"$gte": fromDate, "$lt": toDate},
       lobMongoPath: {"$exists": True}},
      {"_id": 1}
    ).sort("_id", 1))

    return list(map(lambda x: x["_id"], res))
