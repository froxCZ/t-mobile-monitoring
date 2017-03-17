import traceback
from datetime import datetime

from flask import Flask, jsonify
from flask.json import JSONEncoder
from flask_cors import CORS

import common.api.auth as auth
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
@auth.require_root
def currentTime():
  return jsonify({"currentTime": util.dateToTimeString(config.getCurrentTime())})


@app.errorhandler(Exception)
def handle_invalid_usage(error):
  if (type(error) == StatusException):
    response = jsonify({"message": error.message})
    response.status_code = error.status
  else:
    response = jsonify({"message": str(error)})
    response.status_code = 500
  traceback.print_exc()
  return response


from mediation.api.data_query import api_data_query
from mediation.api.config import lobsConfig
from mediation.api.status import lobsStatus
from mediation.api.flows import flowsApi
from mediation.api.mediation import mediation
from common.api import common, StatusException
from zookeeper.api import zookeeperApi

app.register_blueprint(api_data_query, url_prefix="/mediation/data_query")
app.register_blueprint(lobsConfig, url_prefix="/mediation/config")
app.register_blueprint(lobsStatus, url_prefix="/mediation/status")
app.register_blueprint(flowsApi, url_prefix="/mediation/flows")
app.register_blueprint(mediation, url_prefix="/mediation")
app.register_blueprint(common, url_prefix="/app")
app.register_blueprint(zookeeperApi, url_prefix="/zookeeper")

# SchedulerRunner().start()
app.run(debug=True, host="0.0.0.0", port=5000, threaded=True)
