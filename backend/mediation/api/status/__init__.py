from flask import Blueprint, jsonify

from mediation.flow_analyzer import FlowStatusManager

lobsStatus = Blueprint('status', __name__)


@lobsStatus.route('/', methods=["GET"])
def getLobsOverview():
  lobsOverview = FlowStatusManager().getLobsOverview()
  return jsonify(lobsOverview)

@lobsStatus.route('/lob/<string:lobName>', methods=["GET"])
def getLobStatusDetail(lobName):
  lobStatusDetail = FlowStatusManager().getLobDetail(lobName)
  return jsonify(lobStatusDetail)

@lobsStatus.route('/countries', methods=["GET"])
def getCountriesOverview():
  countries = FlowStatusManager().getCountriesOverview()
  return jsonify(countries)
