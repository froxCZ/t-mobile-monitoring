from mongo import zookeeperMongo

statusColl = zookeeperMongo.statuses()

class StatusManager:

  @staticmethod
  def getClusterStatus():
    res = statusColl.find_one({"_id": "zookeeper"}, {"_id": 0})
    if res is None:
      res = {}
