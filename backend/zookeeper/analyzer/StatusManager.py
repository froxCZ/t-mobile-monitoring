from mongo import zookeeperMongo

statusColl = zookeeperMongo.statuses()

DEFAULT_CLUSTER_STATUS = {"nodes": {}, "status": None}


class StatusManager:
  """
  Saves or retrieves status of ZooKeeper cluster and its nodes
  """
  @staticmethod
  def getClusterStatus():
    res = statusColl.find_one({"_id": "zookeeper"}, {"_id": 0})
    if res is None:
      res = {}
    return {**DEFAULT_CLUSTER_STATUS, **res}

  @staticmethod
  def saveClusterStatus(clusterStatus, time):
    clusterStatus["time"] = time
    res = statusColl.update_one({"_id": "zookeeper"}, {"$set": clusterStatus}, upsert=True)
