from datetime import datetime

from flask import Flask
from flask.json import JSONEncoder

app = Flask(__name__)

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

from api.data_query import data_query
app.register_blueprint(data_query,url_prefix="/data_query")
app.run(debug=True)