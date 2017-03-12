from flask import Blueprint, jsonify
from flask import request

import util
from mediation.flow_analyzer import EventsManager

mediation = Blueprint('mediation', __name__)


@mediation.route('/events', methods=["GET"])
def events():
  offset = int(request.args.get('offset', 0))
  omitOK = util.str2bool(request.args.get('omitOK', False))
  events = EventsManager.getEvents(offset, omitOK)
  return jsonify(events)
