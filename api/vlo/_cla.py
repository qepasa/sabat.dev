import flask
import flask.blueprints
import flask_caching

from api.__vars import *

api = flask.blueprints.Blueprint('cla', __name__, url_prefix='/api')
cache = flask_caching.Cache(config=CONFIG)

@cache.cached()
@api.route('/cla')
def cla():
	return flask.jsonify({"success":True,"resp":list(CLASS_KEY.keys())}), 200
	#There is no good way to do this,
	#since its all dependent on a lookup table.
