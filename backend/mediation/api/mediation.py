from flask import Blueprint, jsonify
from flask import request

from mediation.flow_analyzer import EventsManager

mediation = Blueprint('mediation', __name__)


@mediation.route('/events', methods=["GET"])
def events():
  skip = int(request.args.get('skip', 0))
  events = EventsManager.getEvents(skip)
  return jsonify(events)
