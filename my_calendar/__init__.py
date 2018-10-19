from flask import Flask, render_template
from .db import db_session
from .api import bp_api


app = Flask(__name__)
app.register_blueprint(bp_api)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'memcached'


@app.route('/')
def index():
    return render_template('home.html', username='jason')


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
