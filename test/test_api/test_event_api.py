from flask import session
from flask_testing import TestCase
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
        self.not_json = {'code': 400, 'error': 'post type must be json'}
        self.field_not_complete = {'code': 400, 'error': 'fields not complete'}
        self.error_need_login = {'code': 403, 'error': 'need to login'}
        self.error_need_csrf = {'code': 400, 'error': 'needs csrf token'}
        self.error_wrong_csrf = {'code': 400, 'error': 'wrong csrf token'}

        user = User.create('xua@wustl.edu', 'strong_password')
        another_user = User.create('jason@wustl.edu', 'strong_password')
        event = Event.create('dinner', datetime.now())
        another_event = Event.create('lunch', datetime.now())
        self.user_id = user.user_id
        self.event_id = event.event_id
        self.another_user_id = another_user.user_id
        self.another_event_id = another_event.event_id
        db.session.add(user)
        db.session.add(another_user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def login(self, client):
        client.get('/')
        self.csrf_token = session['csrf_token']

        response = client.post('/api/users/login', json={
            'email': 'xua@wustl.edu',
            'password': 'strong_password',
            'csrf_token': self.csrf_token
        })
        self.assertEqual(response.json, self.success)

    def test_create_event(self):
        with self.app.test_client() as client:
            self.login(client)

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

    def test_create_missing_field(self):
        with self.app.test_client() as client:
            self.login(client)

            user = User.query.filter_by(user_id=self.user_id).first()
            self.assertEqual(len(Event.query.with_parent(user).all()), 0)
            response = client.post('/api/events/create', json={
                # 'event_name': "having dinner",
                'event_time': str(datetime.now()),
                'csrf_token': self.csrf_token
            })
            self.assertEqual(response.json, self.field_not_complete)
            user = User.query.filter_by(user_id=self.user_id).first()
            self.assertEqual(len(Event.query.with_parent(user).all()), 0)

            response = client.post('/api/events/create', json={
                'event_name': "having dinner",
                # 'event_time': str(datetime.now()),
                'csrf_token': self.csrf_token
            })
            self.assertEqual(response.json, self.field_not_complete)
            user = User.query.filter_by(user_id=self.user_id).first()
            self.assertEqual(len(Event.query.with_parent(user).all()), 0)

    def test_create_invalid_value_type(self):
        with self.app.test_client() as client:
            self.login(client)

            user = User.query.filter_by(user_id=self.user_id).first()
            self.assertEqual(len(Event.query.with_parent(user).all()), 0)
            response = client.post('/api/events/create', json={
                'event_name': 1235,
                'event_time': str(datetime.now()),
                'csrf_token': self.csrf_token
            })
            self.assertEqual(response.json, {
                'code': 400,
                'error': "error type of event_name: expect <class 'str'> but get <class 'int'>"
            })
            user = User.query.filter_by(user_id=self.user_id).first()
            self.assertEqual(len(Event.query.with_parent(user).all()), 0)

            response = client.post('/api/events/create', json={
                'event_name': "having dinner",
                'event_time': 21354,
                'csrf_token': self.csrf_token
            })
            self.assertEqual(response.json, {
                'code': 400,
                'error': "error type of event_time: expect <class 'str'> but get <class 'int'>"
            })
            user = User.query.filter_by(user_id=self.user_id).first()
            self.assertEqual(len(Event.query.with_parent(user).all()), 0)

    def test_create_without_login(self):
        with self.app.test_client() as client:
            client.get('/')
            self.csrf_token = session['csrf_token']

            user = User.query.filter_by(user_id=self.user_id).first()
            self.assertEqual(len(Event.query.with_parent(user).all()), 0)
            response = client.post('/api/events/create', json={
                'event_name': "having dinner",
                'event_time': str(datetime.now()),
                'csrf_token': self.csrf_token
            })
            self.assertEqual(response.json, self.error_need_login)
            user = User.query.filter_by(user_id=self.user_id).first()
            self.assertEqual(len(Event.query.with_parent(user).all()), 0)

    def test_create_without_csrf(self):
        with self.app.test_client() as client:
            self.login(client)

            user = User.query.filter_by(user_id=self.user_id).first()
            self.assertEqual(len(Event.query.with_parent(user).all()), 0)
            response = client.post('/api/events/create', json={
                'event_name': "having dinner",
                'event_time': str(datetime.now()),
                # 'csrf_token': self.csrf_token
            })
            self.assertEqual(response.json, self.error_need_csrf)
            user = User.query.filter_by(user_id=self.user_id).first()
            self.assertEqual(len(Event.query.with_parent(user).all()), 0)

            # csrf check is before the field check
            # so it will return need csrf error
            user = User.query.filter_by(user_id=self.user_id).first()
            self.assertEqual(len(Event.query.with_parent(user).all()), 0)
            response = client.post('/api/events/create', json={
                'event_name': "having dinner",
                # 'event_time': str(datetime.now()),
                # 'csrf_token': self.csrf_token
            })
            self.assertEqual(response.json, self.error_need_csrf)
            user = User.query.filter_by(user_id=self.user_id).first()
            self.assertEqual(len(Event.query.with_parent(user).all()), 0)

    def test_create_wrong_csrf(self):
        with self.app.test_client() as client:
            self.login(client)

            user = User.query.filter_by(user_id=self.user_id).first()
            self.assertEqual(len(Event.query.with_parent(user).all()), 0)
            response = client.post('/api/events/create', json={
                'event_name': "having dinner",
                'event_time': str(datetime.now()),
                'csrf_token': 'not csrf'
            })
            self.assertEqual(response.json, self.error_wrong_csrf)
            user = User.query.filter_by(user_id=self.user_id).first()
            self.assertEqual(len(Event.query.with_parent(user).all()), 0)

            # csrf check is before the field check
            # so it will return wrong csrf error
            user = User.query.filter_by(user_id=self.user_id).first()
            self.assertEqual(len(Event.query.with_parent(user).all()), 0)
            response = client.post('/api/events/create', json={
                'event_name': "having dinner",
                # 'event_time': str(datetime.now()),
                'csrf_token': 'not csrf'
            })
            self.assertEqual(response.json, self.error_wrong_csrf)
            user = User.query.filter_by(user_id=self.user_id).first()
            self.assertEqual(len(Event.query.with_parent(user).all()), 0)

    def test_get_events(self):
        with self.app.test_client() as client:
            self.login(client)

            user = User.query.filter_by(user_id=self.user_id).first()
            user.events = [
                Event.create('dinner', datetime(2018, 6, 5, 18, 30, 0)),
                Event.create('dinner', datetime(2018, 6, 6, 18, 30, 0)),
                Event.create('dinner', datetime(2018, 6, 7, 18, 30, 0)),
                Event.create('dinner', datetime(2018, 6, 8, 18, 30, 0)),

                Event.create('dinner', datetime(2018, 7, 6, 18, 30, 0)),
                Event.create('dinner', datetime(2018, 7, 7, 18, 30, 0)),
                Event.create('dinner', datetime(2018, 7, 8, 18, 30, 0))
            ]
            event = Event.create('dinner', datetime(2018, 8, 5, 18, 30, 0))
            event.tags = [
                Tag(tag_name='important', activated=True),
                Tag(tag_name='finished', activated=False)
            ]
            user.events.append(event)
            db.session.commit()
            response = client.post('/api/events/user', json={
                'year': 2018,
                'month': 7,
                'csrf_token': self.csrf_token
            })
            self.assertEqual(len(response.json['events']), 3)
            response = client.post('/api/events/user', json={
                'year': 2018,
                'month': 8,
                'csrf_token': self.csrf_token
            })
            self.assertEqual(len(response.json['events']), 1)
            tags = [
                {'tag_name': 'finished', 'activated': False},
                {'tag_name': 'important', 'activated': True},
            ]
            self.assertEqual(response.json['events'][0]['tags'], tags)

    def test_modify_event_name(self):
        with self.app.test_client() as client:
            self.login(client)

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
            self.login(client)

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
            self.login(client)

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
            self.login(client)

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
