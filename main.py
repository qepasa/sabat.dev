import flask

app = flask.Flask(__name__)


@app.route('/')
def home():
    return flask.render_template('home.html')


@app.route('/projects')
def projects():
    return flask.render_template('projects.html')


@app.route('/contact')
def contact():
    return flask.render_template('contact.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    return flask.render_template('login.html')


if __name__ == '__main__':
    app.run()
