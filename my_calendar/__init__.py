from flask import Flask
from my_calendar.home import bp_home
from my_calendar.api import bp_api
from .database import init_app

app = Flask(__name__)


app.register_blueprint(bp_home)
app.register_blueprint(bp_api)

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'memcached'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://wustl_inst:wustl_pass@ec2-52-14-93-16.us-east-2.compute.amazonaws.com:3306/calendar'

database.init_app(app)

