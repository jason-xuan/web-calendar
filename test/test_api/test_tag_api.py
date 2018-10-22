from flask import session
from flask_testing import TestCase
from contextlib import contextmanager
from flask import appcontext_pushed, g
from datetime import datetime
from dateutil import parser
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
        event = Event.create('dinner', datetime.now())
        self.user_id = user.user_id
        self.event_id = event.event_id
        user.events.append(event)
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

    def test_create_tag(self):
        self.login()
        event = Event.query.filter_by(event_id=self.event_id).first()
        self.assertEqual(len(Tag.query.with_parent(event).all()), 0)
        response = self.client.post('/api/tags/create', json={
            'event_id': self.event_id,
            'tag_name': 'important'
        })
        self.assertEqual(response.json, self.success_create)
        event = Event.query.filter_by(event_id=self.event_id).first()
        self.assertEqual(len(Tag.query.with_parent(event).all()), 1)
