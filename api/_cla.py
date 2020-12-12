import flask
import flask.blueprints

from api.__vars import *

api = flask.blueprints.Blueprint('cla', __name__, url_prefix='/api')

@api.route('/cla')
def klasslist():
	return flask.jsonify({"success":True,"resp":CLASS_KEY.keys()})
	#There is no good way to do this,
	#since its all dependent on a lookup table.
