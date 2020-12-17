import flask
import flask.blueprints
import flask_caching

from api.__vars import *

api = flask.blueprints.Blueprint('tim', __name__, url_prefix='/api')
cache = flask_caching.Cache(config=CONFIG)

@cache.cached()
@api.route('/tim')
def tim():
	return flask.jsonify({"success":True,"resp":DB["VLO"]["TIME"]["DATA"]}), 200
