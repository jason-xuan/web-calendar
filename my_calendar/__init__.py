from flask import Flask

from .database import init_app, rebuild_db


config = {
    'SESSION_TYPE': 'memcached',
    'SQLALCHEMY_DATABASE_URI':
        'mysql+mysqlconnector://wustl_inst:wustl_pass@ec2-52-14-93-16.us-east-2.compute.amazonaws.com:3306/orm_calendar',
    'SQLALCHEMY_TRACK_MODIFICATIONS': True,
    'SESSION_COOKIE_HTTPONLY': True,
}


def create_app(test_config=None):
    app = Flask(__name__)

    app.secret_key = 'super secret key'
    app.config.from_mapping(config)
    if test_config is not None:
        app.config.from_object(test_config)

    from my_calendar.home import bp_home
    from my_calendar.api import bp_api
    app.register_blueprint(bp_home)
    app.register_blueprint(bp_api)

    from .modules import User, Event, Tag
    with app.app_context():
        database.init_app()

    return app