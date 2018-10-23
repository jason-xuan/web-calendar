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
        self.user_id = user.user_id
        db.session.add(user)
        db.session.commit()

        with self.app.test_client() as client:
            client.get('/')
            self.csrf_token = session['csrf_token']

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_event(self):
        with self.app.test_client() as client:
            client.get('/')
            self.csrf_token = session['csrf_token']
            response = client.post('/api/users/login', json={
                'email': 'xua@wustl.edu',
                'password': 'strong_password',
                'csrf_token': self.csrf_token
            })
            self.assertEqual(response.json, self.success)

            user = User.query.filter_by(user_id=self.user_id).first()
            self.assertEqual(len(Event.query.with_parent(user).all()), 0)
            response = client.post('/api/events/create', json={
                'event_name': "having dinner",
                'event_time': str(datetime.now()),
                'csrf_token': self.csrf_token
            })
            self.assertEqual(response.json, self.success_create)
            user = User.query.filter_by(user_id=self.user_id).first()
            self.assertEqual(len(Event.query.with_parent(user).all()), 1)

    def test_get_events(self):
        with self.app.test_client() as client:
            client.get('/')
            self.csrf_token = session['csrf_token']
            response = client.post('/api/users/login', json={
                'email': 'xua@wustl.edu',
                'password': 'strong_password',
                'csrf_token': self.csrf_token
            })
            self.assertEqual(response.json, self.success)

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
            response = client.post('/api/events/user', json={
                'year': 2018,
                'month': 7,
                'csrf_token': self.csrf_token
            })
            self.assertEqual(len(response.json['events']), 3)

    def test_modify_event_name(self):
        with self.app.test_client() as client:
            client.get('/')
            self.csrf_token = session['csrf_token']
            response = client.post('/api/users/login', json={
                'email': 'xua@wustl.edu',
                'password': 'strong_password',
                'csrf_token': self.csrf_token
            })
            self.assertEqual(response.json, self.success)

            user = User.query.filter_by(user_id=self.user_id).first()
            event = Event.create('dinner', datetime(2018, 6, 5, 18, 30, 0))
            event_id = event.event_id
            user.events.append(event)
            db.session.commit()
            response = client.post('/api/events/update', json={
                'event_id': event_id,
                'update_fields': {
                    'event_name': 'lunch'
                },
                'csrf_token': self.csrf_token
            })
            self.assertEqual(response.json, self.success)
            event = Event.query.filter_by(event_id=event_id).first()
            self.assertEqual(event.event_name, 'lunch')

    def test_modify_event_time(self):
        with self.app.test_client() as client:
            client.get('/')
            self.csrf_token = session['csrf_token']
            response = client.post('/api/users/login', json={
                'email': 'xua@wustl.edu',
                'password': 'strong_password',
                'csrf_token': self.csrf_token
            })
            self.assertEqual(response.json, self.success)

            user = User.query.filter_by(user_id=self.user_id).first()
            event = Event.create('dinner', datetime(2018, 6, 5, 18, 30, 0))
            event_id = event.event_id
            user.events.append(event)
            db.session.commit()
            now = datetime.now()
            response = client.post('/api/events/update', json={
                'event_id': event_id,
                'update_fields': {
                    'event_time': str(now)
                },
                'csrf_token': self.csrf_token
            })
            self.assertEqual(response.json, self.success)
            event = Event.query.filter_by(event_id=event_id).first()
            self.assertEqual(event.event_time, now)

    def test_modify_event_name_and_time(self):
        with self.app.test_client() as client:
            client.get('/')
            self.csrf_token = session['csrf_token']
            response = client.post('/api/users/login', json={
                'email': 'xua@wustl.edu',
                'password': 'strong_password',
                'csrf_token': self.csrf_token
            })
            self.assertEqual(response.json, self.success)

            user = User.query.filter_by(user_id=self.user_id).first()
            event = Event.create('dinner', datetime(2018, 6, 5, 18, 30, 0))
            event_id = event.event_id
            user.events.append(event)
            db.session.commit()
            now = datetime.now()
            response = client.post('/api/events/update', json={
                'event_id': event_id,
                'update_fields': {
                    'event_name': 'lunch',
                    'event_time': str(now)
                },
                'csrf_token': self.csrf_token
            })
            self.assertEqual(response.json, self.success)
            event = Event.query.filter_by(event_id=event_id).first()
            self.assertEqual(event.event_time, now)
            self.assertEqual(event.event_name, 'lunch')

    def test_delete_event(self):
        with self.app.test_client() as client:
            client.get('/')
            self.csrf_token = session['csrf_token']
            response = client.post('/api/users/login', json={
                'email': 'xua@wustl.edu',
                'password': 'strong_password',
                'csrf_token': self.csrf_token
            })
            self.assertEqual(response.json, self.success)

            user = User.query.filter_by(user_id=self.user_id).first()
            user.events = [
                Event.create('dinner', datetime(2018, 6, 5, 18, 30, 0)),
                Event.create('dinner', datetime(2018, 6, 6, 18, 30, 0)),
                Event.create('dinner', datetime(2018, 6, 7, 18, 30, 0)),
                Event.create('dinner', datetime(2018, 6, 8, 18, 30, 0)),
            ]
            event_id = user.events[0].event_id
            self.assertEqual(len(Event.query.with_parent(user).all()), 4)
            db.session.commit()

            response = client.post('/api/events/delete', json={
                'event_id': event_id,
                'csrf_token': self.csrf_token
            })
            user = User.query.filter_by(user_id=self.user_id).first()
            self.assertEqual(response.json, self.success)
            self.assertEqual(len(Event.query.with_parent(user).all()), 3)
