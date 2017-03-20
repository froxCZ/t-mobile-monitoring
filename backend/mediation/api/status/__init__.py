from flask import Blueprint, jsonify

from mediation.flow_analyzer import FlowStatusManager

lobsStatus = Blueprint('status', __name__)

"""
deprecated endpoint, use /flows
"""
@lobsStatus.route('/lobs/<string:country>', methods=["GET"])
def getLobsOverview(country):
  lobsOverview = FlowStatusManager().getLobsOverview(country)
  return jsonify(lobsOverview)

@lobsStatus.route('/lob/<string:lobName>', methods=["GET"])
def getLobStatusDetail(lobName):
  lobStatusDetail = FlowStatusManager().getLobDetail(lobName)
  return jsonify(lobStatusDetail)

@lobsStatus.route('/countries', methods=["GET"])
def getCountriesOverview():
  countries = FlowStatusManager().getCountriesOverview()
  return jsonify(countries)
