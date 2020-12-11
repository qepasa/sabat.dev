import json

import flask
import flask.blueprints


api = flask.blueprints.Blueprint('cla', __name__, url_prefix='/api')


@api.route('/cla')
def test():
	return 'asd2'
