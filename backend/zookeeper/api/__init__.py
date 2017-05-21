from flask import Blueprint, jsonify
from flask import request

from common.api import require_root
from common.api import require_user
from zookeeper.analyzer import StatusManager
from ..ZookeeperConfig import ZookeeperConfig

zookeeperAPI = Blueprint('zookeeper', __name__)

"""
API endpoints related to ZooKeeper monitoring
"""


@zookeeperAPI.route('/cluster', methods=["GET"])
@require_user
def configGET():
  return jsonify(ZookeeperConfig.getCluster())


@zookeeperAPI.route('/node/<string:socketAddress>', methods=["DELETE"])
@require_root
def nodeDELETE(socketAddress):
  ZookeeperConfig.deleteNode(socketAddress)
  return jsonify(ZookeeperConfig.getCluster())


@zookeeperAPI.route('/node/<string:socketAddress>', methods=["POST"])
@require_root
def nodePOST(socketAddress):
  ZookeeperConfig.upsertNode(socketAddress, request.get_json())
  return jsonify(ZookeeperConfig.getCluster())


@zookeeperAPI.route('/cluster/enable', methods=["POST"])
@require_root
def monitoringEnable():
  ZookeeperConfig.enableMonitoring(True)
  return jsonify(ZookeeperConfig.getCluster())


@zookeeperAPI.route('/cluster/disable', methods=["POST"])
@require_root
def monitoringDisable():
  ZookeeperConfig.enableMonitoring(False)
  return jsonify(ZookeeperConfig.getCluster())


@zookeeperAPI.route('/status', methods=["GET"])
@require_user
def status():
  if ZookeeperConfig.isMonitoringEnabled() is False:
    return jsonify({"enabled": False})
    pass
  return jsonify(StatusManager.getClusterStatus())
