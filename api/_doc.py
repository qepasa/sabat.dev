import flask
import flask.blueprints
import flask_caching

from api.__vars import *

api = flask.blueprints.Blueprint('doc', __name__, url_prefix='/api')
cache = flask_caching.Cache(config=CONFIG)

@cache.cached()
@api.route('/documentation', methods=['GET'])
@api.route('/docs', methods=['GET'])
def docs():
	return flask.redirect('https://github.com/Cloud11665/sabat.dev/tree/master/api')
