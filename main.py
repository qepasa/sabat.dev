import toml
import flask
import flask_cors
import flask_caching

import api

with open('./config.toml', 'r', encoding='utf-8') as cfg:
	CONFIG = toml.load(cfg)

app = flask.Flask(__name__)
flask_cors.CORS(app)
app.config.from_mapping(CONFIG)

cache = flask_caching.Cache(app)

#! API
app.register_blueprint(api.cla)
app.register_blueprint(api.doc)
app.register_blueprint(api.sub)
app.register_blueprint(api.tta)

#! Views

@app.route('/')
def home():
	return flask.render_template('home.html')

@app.route('/projects')
def projects():
	return flask.render_template('projects.html')


@app.route('/contact')
def contact():
	return flask.render_template('contact.html')

if __name__ == '__main__':
	app.run(debug=True)

