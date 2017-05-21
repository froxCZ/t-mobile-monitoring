import re
import socket


class StatusFetcher():
  """
  Fetches data from zookeeper node.
  """
  offline = {"status": "OFFLINE", "mode":None}
  notServing = {"status": "OK","mode":None}

  @staticmethod
  def getStatus(host, port):
    try:
      statResult = send_cmd(host, port, b"stat")
    except Exception:
      return StatusFetcher.offline
    return parseStatResult(statResult)


modeFinder = {"regexp": r"Mode: (.*)", "group": 1}
zookeeperVersion = {"regexp": r"Zookeeper version: (.*),", "group": 1}
latencyFinder = {"regexp": r"Latency min/avg/max: (.*)", "group": 1}
zxidFinder = {"regexp": r"Zxid: (.*)", "group": 1}
outstandingFinder = {"regexp": r"Outstanding: (.*)", "group": 1}
nodeCountFinder = {"regexp": r"Node count: (.*)", "group": 1}
connectionsFinder = {"regexp": r"Connections: (.*)", "group": 1}


def parseStatResult(statCmdResult):
  stat = {}
  stat["status"] = "OK"
  if "This ZooKeeper instance is not currently serving requests" in statCmdResult:
    return StatusFetcher.notServing
  stat["mode"] = getFinderValue(modeFinder, statCmdResult)
  stat["latency"] = getFinderValue(latencyFinder, statCmdResult)
  stat["latency"] = getFinderValue(latencyFinder, statCmdResult)
  stat["outstanding"] = getFinderValue(outstandingFinder, statCmdResult)
  stat["zxid"] = getFinderValue(zxidFinder, statCmdResult)
  stat["nodeCount"] = getFinderValue(nodeCountFinder, statCmdResult)
  stat["zookeeperVersion"] = getFinderValue(zookeeperVersion, statCmdResult)
  stat["connections"] = getFinderValue(connectionsFinder, statCmdResult)
  return stat


def getFinderValue(finder, str):
  matches = re.finditer(finder["regexp"], str)
  for matchNum, match in enumerate(matches):
    return match.group(finder["group"])


def send_cmd(host, port, cmd):
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.settimeout(0.5)
  s.connect((host, port))
  result = []
  try:
    s.sendall(cmd)

    s.shutdown(socket.SHUT_WR)

    while True:
      data = s.recv(4096)
      if not data:
        break
      data = data.decode()
      result.append(data)
  finally:
    s.close()

  return "".join(result)
