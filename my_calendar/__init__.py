from flask import Flask

from .database import init_app
from datetime import timedelta

<<<<<<< HEAD
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds = 1)
=======

def create_app():
    app = Flask(__name__)
>>>>>>> 90c303a9546b9d11a1bd47711576280ce4fe219c

    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'memcached'
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'mysql+mysqlconnector://wustl_inst:wustl_pass@ec2-52-14-93-16.us-east-2.compute.amazonaws.com:3306/orm_calendar'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    from my_calendar.home import bp_home
    from my_calendar.api import bp_api
    app.register_blueprint(bp_home)
    app.register_blueprint(bp_api)

    from .modules import User, Event, Tag
    with app.app_context():
        database.init_app()

    return app
