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
        self.not_json = {'code': 403, 'error': 'post type must be json'}
        self.field_not_complete = {'code': 403, 'error': 'fields not complete'}
        self.wrong_email = {'code': 403, 'error': "format check of email failed: got today's dinner"}

        user = User.create('xua@wustl.edu', 'strong_password')
        self.user_id = user.user_id
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def login(self):
        response = self.client.post('/api/users/login', json={
            'email': 'xua@wustl.edu', 'password': 'strong_password'
        })
        self.assertEqual(response.json, self.success)

    def test_create_event(self):
        self.login()
        user = User.query.filter_by(user_id=self.user_id).first()
        self.assertEqual(len(Event.query.with_parent(user).all()), 1)
        response = self.client.post('/api/events/create', json={
            'event_name': "having dinner",
            'event_time': str(datetime.now())
        })
        self.assertEqual(response.json, self.success_create)
        user = User.query.filter_by(user_id=self.user_id).first()
        self.assertEqual(len(Event.query.with_parent(user).all()), 2)

    def test_get_events(self):
        self.login()
        user = User.query.filter_by(user_id=self.user_id).first()
        user.events = [
            Event.create('dinner', datetime(2018, 6, 5, 18, 30, 0)),
            Event.create('dinner', datetime(2018, 6, 6, 18, 30, 0)),
            Event.create('dinner', datetime(2018, 6, 7, 18, 30, 0)),
            Event.create('dinner', datetime(2018, 6, 8, 18, 30, 0)),
            Event.create('dinner', datetime(2018, 8, 5, 18, 30, 0)),
            Event.create('dinner', datetime(2018, 7, 6, 18, 30, 0)),
            Event.create('dinner', datetime(2018, 7, 7, 18, 30, 0)),
            Event.create('dinner', datetime(2018, 7, 8, 18, 30, 0))
        ]
        db.session.commit()
        response = self.client.post('/api/events/user', json={
            'year': 2018,
            'month': 7
        })
        self.assertEqual(len(response.json['events']), 3)

    def test_modify_event(self):
        self.login()

    def test_delete_event(self):
        self.login()
        user = User.query.filter_by(user_id=self.user_id).first()
        user.events = [
            Event.create('dinner', datetime(2018, 6, 5, 18, 30, 0)),
            Event.create('dinner', datetime(2018, 6, 6, 18, 30, 0)),
            Event.create('dinner', datetime(2018, 6, 7, 18, 30, 0)),
            Event.create('dinner', datetime(2018, 6, 8, 18, 30, 0)),
        ]
        event_id = user.events[0].event_id
        self.assertEqual(len(Event.query.with_parent(user).all()), 3)
        db.session.commit()

        response = self.client.post('/api/events/create', json={
            'event_id': event_id
        })
        self.assertEqual(response.json, self.success)
        self.assertEqual(len(Event.query.with_parent(user).all()), 3)
