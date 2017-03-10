import traceback
from datetime import datetime

from flask import Flask, jsonify
from flask.ext.cors import CORS
from flask.json import JSONEncoder

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


@app.errorhandler(Exception)
def handle_invalid_usage(error):
  response = jsonify({"message": str(error)})
  response.status_code = 500
  traceback.print_exc()
  return response


from api.data_query import api_data_query
from api.config import lobsConfig

app.register_blueprint(api_data_query, url_prefix="/data_query")
app.register_blueprint(lobsConfig, url_prefix="/lobs/config")
app.run(debug=True)
