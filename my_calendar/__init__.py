from flask import Flask, render_template
from flask.ext.restful import Api
from .api import User, Event, EventByID


app = Flask(__name__)
api = Api(api)


@app.route('/')
def index():
    return render_template('home.html', username='jason')


api.add_resource(User, '/user/')
api.add_resource(Event, '/event/')
api.add_resource(EventByID, '/event/<string:event_id>')
