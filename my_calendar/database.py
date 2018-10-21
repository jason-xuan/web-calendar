from flask_sqlalchemy import SQLAlchemy
from flask import current_app


db = SQLAlchemy()


def init_app():
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    db.init_app(current_app)
