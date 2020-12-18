import flask
import flask.blueprints
import flask_caching

from api.__vars import *

api = flask.blueprints.Blueprint('cla', __name__, url_prefix='/api')
cache = flask_caching.Cache(config=CONFIG)

@cache.cached()
@api.route('/cla')
def cla():
	return flask.jsonify({"success":True,"resp":sorted(list(DB["VLO"]["CLASS"]["ID"].values()))}), 200
