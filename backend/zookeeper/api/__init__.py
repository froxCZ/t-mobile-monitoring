from flask import Blueprint, jsonify
from flask import request

from zookeeper.config import ZookeeperConfig
from ..analyzer import StatusManager

zookeeperApi = Blueprint('zookeeper', __name__)


@zookeeperApi.route('/cluster', methods=["GET"])
def configGET():
  return jsonify(ZookeeperConfig.getCluster())


@zookeeperApi.route('/node/<string:socketAddress>', methods=["DELETE"])
def nodeDELETE(socketAddress):
  ZookeeperConfig.deleteNode(socketAddress)
  return jsonify(ZookeeperConfig.getCluster())


@zookeeperApi.route('/node/<string:socketAddress>', methods=["POST"])
def nodePOST(socketAddress):
  ZookeeperConfig.upsertNode(socketAddress, request.get_json())
  return jsonify(ZookeeperConfig.getCluster())


@zookeeperApi.route('/cluster/enable', methods=["POST"])
def monitoringEnable():
  ZookeeperConfig.enableMonitoring(True)
  return jsonify(ZookeeperConfig.getCluster())


@zookeeperApi.route('/cluster/disable', methods=["POST"])
def monitoringDisable():
  ZookeeperConfig.enableMonitoring(False)
  return jsonify(ZookeeperConfig.getCluster())


@zookeeperApi.route('/status', methods=["GET"])
def status():
  if ZookeeperConfig.isMonitoringEnabled() is False:
    return jsonify({"enabled": False})
    pass
  return jsonify(StatusManager.getClusterStatus())
