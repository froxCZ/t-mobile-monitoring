from mongo import zookeeperMongo

statusColl = zookeeperMongo.statuses()


class StatusManager:
  @staticmethod
  def getClusterStatus():
    res = statusColl.find_one({"_id": "zookeeper"}, {"_id": 0})
    if res is None:
      res = {}
    return res

  @staticmethod
  def saveClusterStatus(clusterStatus, time):
    clusterStatus["time"] = time
    res = statusColl.update_one({"_id": "zookeeper"}, {"$set": clusterStatus}, upsert=True)
    print(res)
