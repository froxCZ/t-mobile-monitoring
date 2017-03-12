import traceback
from datetime import datetime

from flask import Flask, jsonify
from flask.ext.cors import CORS
from flask.json import JSONEncoder

import config
import util

app = Flask(__name__)
CORS(app)


class CustomJSONEncoder(JSONEncoder):
  def default(self, obj):
    try:
      if isinstance(obj, datetime):
        return obj.isoformat()
      iterable = iter(obj)
    except TypeError:
      pass
    else:
      return list(iterable)
    return JSONEncoder.default(self, obj)


app.json_encoder = CustomJSONEncoder


@app.route("/")
def hello():
  return "Helasdlo xWorld!"


@app.route("/currentTime")
def currentTime():
  return jsonify({"currentTime": util.dateToTimeString(config.getCurrentTime())})


@app.errorhandler(Exception)
def handle_invalid_usage(error):
  response = jsonify({"message": str(error)})
  response.status_code = 500
  traceback.print_exc()
  return response


from mediation.api.data_query import api_data_query
from mediation.api.config import lobsConfig
from mediation.api.status import lobsStatus
from mediation.api.mediation import mediation

app.register_blueprint(api_data_query, url_prefix="/mediation/data_query")
app.register_blueprint(lobsConfig, url_prefix="/mediation/config")
app.register_blueprint(lobsStatus, url_prefix="/mediation/status")
app.register_blueprint(mediation, url_prefix="/mediation")
# SchedulerRunner().start()
app.run(debug=True)
