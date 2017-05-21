from zookeeper import ZooUtil
from .Communicator import StatsFetcher
from ..ZookeeperConfig import ZookeeperConfig


class Analyzer():
  """
  Checks status of all nodes in cluster.
  """

  def __init__(self):
    super().__init__()

  def run(self, cluster=None):
    if cluster == None:
      cluster = ZookeeperConfig.getCluster()
    if cluster["enabled"] == False:
      cluster["status"] = "DISABLED"
      return cluster
    numberOfNodes = len(cluster["nodes"])
    onlineNodes = 0
    nodeStatus = {}
    for socketAddress, node in cluster["nodes"].items():
      host, port = ZooUtil.socketAddressToHostAndPort(socketAddress)
      res = StatsFetcher.getStatus(host, port)
      nodeStatus[socketAddress] = res
      if res["status"] == "OK" and res["mode"] is not None:
        onlineNodes += 1
    status = "OUTAGE"
    if onlineNodes == numberOfNodes:
      status = "OK"
    elif onlineNodes > int(numberOfNodes / 2):
      status = "WARNING"

    clusterStatus = {}
    clusterStatus["nodes"] = nodeStatus
    clusterStatus["status"] = status
    return clusterStatus


if __name__ == '__main__':
  res = Analyzer().run()
  print(res)
