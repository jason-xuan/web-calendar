from flask import session
from flask_testing import TestCase
from contextlib import contextmanager
from flask import appcontext_pushed, g
from datetime import datetime
from my_calendar import create_app
from my_calendar.database import db
from my_calendar.modules import User, Event, Tag


# @contextmanager
# def user_set(app, user):
#     def handler(sender, **kwargs):
#         g.user = user
#     with appcontext_pushed.connected_to(handler, app):
#         yield


class TestUserApi(TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite:///db_for_test.db"
    TESTING = True

    def create_app(self):
        return create_app(self)

    def setUp(self):
        db.drop_all()
        db.create_all()

        self.success = {'code': 200}

        user = User.create('xua@wustl.edu', 'strong_password')
        self.user_id = user.user_id
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_login(self):
        with self.app.test_client() as client:
            response = client.post('/api/users/login', json={
                    'email': 'xua@wustl.edu', 'password': 'strong_password'
                })
            self.assertEqual(response.json, self.success)
            # login check
            self.assertTrue('user_id' in session)
            self.assertEqual(session['user_id'], self.user_id)

    def test_logout(self):
        with self.app.test_client() as client:
            response = client.post('/api/users/login', json={
                    'email': 'xua@wustl.edu', 'password': 'strong_password'
                })
            self.assertEqual(response.json, self.success)
            # login check
            self.assertTrue('user_id' in session)
            self.assertEqual(session['user_id'], self.user_id)

            response = client.get('/api/users/logout')
            self.assertEqual(response.json, self.success)
            # logout check
            self.assertFalse('user_id' in session)

