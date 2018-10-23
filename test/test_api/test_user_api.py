from flask import session
from flask_testing import TestCase
from contextlib import contextmanager
from flask import appcontext_pushed, g
from datetime import datetime
from my_calendar import create_app
from my_calendar.database import db
from my_calendar.modules import User, Event, Tag


class TestUserApi(TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite:///db_for_test.db"
    TESTING = True

    def create_app(self):
        return create_app(self)

    def setUp(self):
        db.drop_all()
        db.create_all()

        self.success = {'code': 200}
        self.success_create = {'code': 201}
        self.not_json = {'code': 400, 'error': 'post type must be json'}
        self.field_not_complete = {'code': 400, 'error': 'fields not complete'}
        self.wrong_email = {'code': 400, 'error': "format check of email failed: got today's dinner"}

        user = User.create('xua@wustl.edu', 'strong_password')
        self.user_id = user.user_id
        db.session.add(user)
        db.session.commit()

        with self.app.test_client() as client:
            respond = client.get('/')
            self.csrf_token = session['csrf_token']
            # print(self.csrf_token)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_login(self):
        with self.app.test_client() as client:
            response = client.post('/api/users/login', json={
                'email': 'xua@wustl.edu',
                'password': 'strong_password',
                'csrf_token': self.csrf_token
                })
            self.assertEqual(response.json, self.success)
            # login check
            self.assertTrue('user_id' in session)
            self.assertEqual(session['user_id'], self.user_id)

    def test_logout(self):
        with self.app.test_client() as client:
            response = client.post('/api/users/login', json={
                'email': 'xua@wustl.edu',
                'password': 'strong_password',
                'csrf_token': self.csrf_token
                })
            self.assertEqual(response.json, self.success)
            # login check
            self.assertTrue('user_id' in session)
            self.assertEqual(session['user_id'], self.user_id)

            response = client.get('/api/users/logout')
            self.assertEqual(response.json, self.success)
            # logout check
            self.assertFalse('user_id' in session)

    def test_register(self):
        self.assertEqual(len(User.query.all()), 1)
        with self.app.test_client() as client:
            response = client.post('/api/users/register', json={
                'email': 'jason@wustl.edu',
                'password': 'strong_password',
                'csrf_token': self.csrf_token
            })
            self.assertEqual(response.json, self.success_create)
            self.assertEqual(len(User.query.all()), 2)
            user = User.query.filter_by(email='jason@wustl.edu').first()
            self.assertTrue(user.verify('strong_password'))

    def test_without_email(self):
        response = self.client.post('/api/users/register', json={
            'password': 'strong_password',
            'csrf_token': self.csrf_token
        })
        self.assertEqual(response.json, self.field_not_complete)

        response = self.client.post('/api/users/login', json={
            'password': 'strong_password',
            'csrf_token': self.csrf_token
        })
        self.assertEqual(response.json, self.field_not_complete)

    def test_without_password(self):
        response = self.client.post('/api/users/register', json={
            'email': 'jason@wustl.edu',
            'csrf_token': self.csrf_token
        })
        self.assertEqual(response.json, self.field_not_complete)

        response = self.client.post('/api/users/login', json={
            'email': 'jason@wustl.edu',
            'csrf_token': self.csrf_token
        })
        self.assertEqual(response.json, self.field_not_complete)

    def test_wrong_email_type(self):
        response = self.client.post('/api/users/register', json={
            'email': "today's dinner",
            'password': 'strong_password',
            'csrf_token': self.csrf_token
        })
        self.assertEqual(response.json, self.wrong_email)

        response = self.client.post('/api/users/login', json={
            'email': "today's dinner",
            'password': 'strong_password',
            'csrf_token': self.csrf_token
        })
        self.assertEqual(response.json, self.wrong_email)