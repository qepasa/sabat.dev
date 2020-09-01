import datetime

import flask

app = flask.Flask(__name__)
app.secret_key = 'janpawel2jebalmaledzieci'
app.permanent_session_lifetime = datetime.timedelta(weeks=1)


@app.route('/')
def home():
	return flask.render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
	if flask.request.method == 'POST':
		flask.session.permanent = True
		user = flask.request.form['nm']
		flask.session['user'] = user
		return flask.redirect(flask.url_for('user'))
	else:
		return flask.render_template('login.html')

@app.route('/user')
def user():
	if 'user' in flask.session:
		user = flask.session['user']
		return f"<h1>{user}</h1>"
	else:
		return flask.redirect(flask.url_for('login'))


if __name__ == '__main__':
	app.run(debug=True)