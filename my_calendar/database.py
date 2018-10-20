"""
some code from
https://github.com/pallets/flask/blob/master/examples/tutorial/flaskr
"""
from flask import g
import mysql.connector
from .modules import User, Event, Tag


db_config = {
  'user': 'wustl_inst',
  'password': 'wustl_pass',
  'host': 'ec2-52-14-93-16.us-east-2.compute.amazonaws.com',
  'database': 'calendar',
}


def connect_db():
    cnx = mysql.connector.connect(**db_config)
    return cnx


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'db'):
        g.db = connect_db()
    return g.db


def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)


def insert_user(user):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO `users`(`email`, `password`) VALUES (%s, %s)', (user.email, user.password))
    db.commit()
    cursor.close()


def search_user_by_id(user_id):
    cursor = get_db().cursor()
    cursor.execute('SELECT `email`, `password` FROM `users` WHERE `user_id`=%s', (user_id, ))
    result = cursor.fetchall()
    if len(result) == 0:
        return None
    email, password = result[0]
    user = User(email, password, user_id)
    cursor.close()
    return user


def search_user_by_email(email):
    cursor = get_db().cursor()
    cursor.execute('SELECT `user_id`, `password` FROM `users` WHERE `email`=%s', (email, ))
    result = cursor.fetchall()
    if len(result) == 0:
        return None
    user_id, password = result[0]
    user = User(email, password, int(user_id))
    cursor.close()
    return user

# from my_calendar.database import get_db, insert_user, search_user_by_email, search_user_by_id
# from my_calendar.modules import User, Event, Tag