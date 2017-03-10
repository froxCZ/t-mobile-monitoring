from flask import Blueprint, jsonify

import config
from flow_analyzer import FlowAnalyzer

lobsStatus = Blueprint('status', __name__)


@lobsStatus.route('/', methods=["GET"])
def getStatusList():
  statusList = []
  lobsConfig = config.getLobsConfig()["lobs"]
  for lobName, lob in lobsConfig.items():
    for flowName,flow in lob["flows"].items():
      print(flowName)
      analyzer = FlowAnalyzer(flow)
      runResult = analyzer.run(config.getCurrentTime())
  return jsonify(statusList)