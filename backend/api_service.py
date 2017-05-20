import traceback
from datetime import datetime

from flask import Flask, jsonify
from flask.json import JSONEncoder
from flask_cors import CORS

from config import AppConfig

app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 40 * 1024 * 1024


class CustomJSONEncoder(JSONEncoder):
  """
  JSON encoder to send datetime in iso format
  """
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

@app.errorhandler(Exception)
def handle_invalid_usage(error):
  """
  Exceptions handler which returns json with message and status code.
  """
  if (type(error) == StatusException):
    response = jsonify({"message": error.message})
    response.status_code = error.status
  else:
    response = jsonify({"message": str(error)})
    response.status_code = 500
  traceback.print_exc()
  return response


from mediation.api.data import dataAPI
from mediation.api.config import configAPI
from mediation.api.status import lobsStatus
from mediation.api.flows import flowsAPI
from common.api import appAPI, StatusException
from zookeeper.api import zookeeperAPI

#Registration of all endpoints
app.register_blueprint(dataAPI, url_prefix="/mediation/data")
app.register_blueprint(configAPI, url_prefix="/mediation/config")
app.register_blueprint(lobsStatus, url_prefix="/mediation/status")
app.register_blueprint(flowsAPI, url_prefix="/mediation/flows")
app.register_blueprint(appAPI, url_prefix="/app")
app.register_blueprint(zookeeperAPI, url_prefix="/zookeeper")

app.run(debug=AppConfig.getFlaskConfig().get("debug",False), host="0.0.0.0", port=5000, threaded=True)
