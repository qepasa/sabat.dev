import flask
import flask.blueprints
import flask_caching

from api.__vars import *

api = flask.blueprints.Blueprint('cla', __name__, url_prefix='/api')
cache = flask_caching.Cache(config=CONFIG)

@api.route('/cla')
@cache.cached(timeout=3600)
def cla():
	return flask.jsonify({"success":True,"resp":sorted(list(DB["VLO"]["CLASS"]["ID"].values()))}), 200
