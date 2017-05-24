from mongo import zookeeperMongo

class ZookeeperConfig():
  """
  Config related to ZooKeeper
  """

  @staticmethod
  def getCollection():
    return zookeeperMongo.config()

  @staticmethod
  def getCluster():
    default = {"enabled": False, "nodes": {}}
    res = ZookeeperConfig.getCollection().find_one({"_id": "cluster"}, {"_id": 0})
    if res is None:
      res = default
    else:
      res = {**default, **res}
    return res

  @staticmethod
  def upsertNode(socketAddress, body):
    ZookeeperConfig.getCollection().update_one({"_id": "cluster"}, {"$set": {"nodes." + socketAddress: body}}, upsert=True)

  @staticmethod
  def deleteNode(socketAddress):
    ZookeeperConfig.getCollection().update_one({"_id": "cluster"}, {"$unset": {"nodes." + socketAddress: ""}})

  @staticmethod
  def enableMonitoring(enable=True):
    ZookeeperConfig.getCollection().update_one({"_id": "cluster"}, {"$set": {"enabled": enable}}, upsert=True)

  @staticmethod
  def isMonitoringEnabled():
    return ZookeeperConfig.getCluster()["enabled"]

