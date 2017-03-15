from mongo import zookeeperMongo

configColl = zookeeperMongo.config()


class ZookeeperConfig():
  @staticmethod
  def getCluster():
    default = {"enabled": False, "nodes": {}}
    res = configColl.find_one({"_id": "cluster"}, {"_id": 0})
    if res is None:
      res = default
    else:
      res = {**default, **res}
    return res

  @staticmethod
  def upsertNode(socketAddress, body):
    configColl.update_one({"_id": "cluster"}, {"$set": {"nodes." + socketAddress: body}}, upsert=True)

  @staticmethod
  def deleteNode(socketAddress):
    configColl.update_one({"_id": "cluster"}, {"$unset": {"nodes." + socketAddress: ""}})

  @staticmethod
  def enableMonitoring(enable=True):
    configColl.update_one({"_id": "cluster"}, {"$set": {"enabled": enable}}, upsert=True)

  @staticmethod
  def isMonitoringEnabled():
    return ZookeeperConfig.getCluster()["enabled"]


if __name__ == '__main__':
  servers = {}
  servers["a"] = {"ip": "127.0.0.1"}
  ZookeeperConfig.upsertNode(servers)
  print(ZookeeperConfig.getCluster())
