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

    #
    # test create tag
    #
    def test_create_tag(self):
        with self.app.test_client() as client:
            client.get('/')
            self.csrf_token = session['csrf_token']

            response = client.post('/api/users/login', json={
                'email': 'xua@wustl.edu',
                'password': 'strong_password',
                'csrf_token': self.csrf_token
            })
            self.assertEqual(response.json, self.success)

            event = Event.query.filter_by(event_id=self.event_id).first()
            self.assertEqual(len(Tag.query.with_parent(event).all()), 0)
            response = client.post('/api/tags/create', json={
                'event_id': self.event_id,
                'tag_name': 'important',
                'csrf_token': self.csrf_token
            })
            self.assertEqual(response.json, self.success_create)

            event = Event.query.filter_by(event_id=self.event_id).first()
            self.assertEqual(len(Tag.query.with_parent(event).all()), 1)
            response = client.post('/api/tags/create', json={
                'event_id': self.event_id,
                'tag_name': 'driving',
                'csrf_token': self.csrf_token
            })
            self.assertEqual(response.json, self.success_create)
            event = Event.query.filter_by(event_id=self.event_id).first()
            self.assertEqual(len(Tag.query.with_parent(event).all()), 2)

    def test_create_duplicate_tag(self):
        with self.app.test_client() as client:
            client.get('/')
            self.csrf_token = session['csrf_token']

            response = client.post('/api/users/login', json={
                'email': 'xua@wustl.edu',
                'password': 'strong_password',
                'csrf_token': self.csrf_token
            })
            self.assertEqual(response.json, self.success)

            event = Event.query.filter_by(event_id=self.event_id).first()
            self.assertEqual(len(Tag.query.with_parent(event).all()), 0)
            response = client.post('/api/tags/create', json={
                'event_id': self.event_id,
                'tag_name': 'important',
                'csrf_token': self.csrf_token
            })
            self.assertEqual(response.json, self.success_create)

            event = Event.query.filter_by(event_id=self.event_id).first()
            self.assertEqual(len(Tag.query.with_parent(event).all()), 1)
            response = client.post('/api/tags/create', json={
                'event_id': self.event_id,
                'tag_name': 'important',
                'csrf_token': self.csrf_token
            })
            self.assertEqual(response.json, {'code': 400, 'error': 'tag already exist'})
            event = Event.query.filter_by(event_id=self.event_id).first()
            self.assertEqual(len(Tag.query.with_parent(event).all()), 1)

    def test_create_with_missing_event_id(self):
        with self.app.test_client() as client:
            client.get('/')
            self.csrf_token = session['csrf_token']

            response = client.post('/api/users/login', json={
                'email': 'xua@wustl.edu',
                'password': 'strong_password',
                'csrf_token': self.csrf_token
            })
            self.assertEqual(response.json, self.success)

            response = client.post('/api/tags/create', json={
                'tag_name': 'important',
                'csrf_token': self.csrf_token
            })
            self.assertEqual(response.json, {'code': 400, 'error': 'fields not complete'})

    def test_create_with_missing_tag_name(self):
        with self.app.test_client() as client:
            client.get('/')
            self.csrf_token = session['csrf_token']

            response = client.post('/api/users/login', json={
                'email': 'xua@wustl.edu',
                'password': 'strong_password',
                'csrf_token': self.csrf_token
            })
            self.assertEqual(response.json, self.success)

            response = client.post('/api/tags/create', json={
                'event_id': self.event_id,
                'csrf_token': self.csrf_token
            })
            self.assertEqual(response.json, {'code': 400, 'error': 'fields not complete'})

    def test_create_with_missing_csrf(self):
        with self.app.test_client() as client:
            client.get('/')
            self.csrf_token = session['csrf_token']

            response = client.post('/api/users/login', json={
                'email': 'xua@wustl.edu',
                'password': 'strong_password',
                'csrf_token': self.csrf_token
            })
            self.assertEqual(response.json, self.success)

            response = client.post('/api/tags/create', json={
                'event_id': self.event_id,
                'tag_name': 'important',
            })
            self.assertEqual(response.json, {'code': 400, 'error': 'needs csrf token'})

    #
    # test get tags
    #
    def test_get_tags(self):
        with self.app.test_client() as client:
            client.get('/')
            self.csrf_token = session['csrf_token']

            response = client.post('/api/users/login', json={
                'email': 'xua@wustl.edu',
                'password': 'strong_password',
                'csrf_token': self.csrf_token
            })
            self.assertEqual(response.json, self.success)

            event = Event.query.filter_by(event_id=self.event_id).first()
            event.tags = [
                Tag(tag_name='important', activated=False),
                Tag(tag_name='personal', activated=False)
            ]
            db.session.commit()
            response = client.post('/api/tags/event', json={
                'event_id': self.event_id,
                'csrf_token': self.csrf_token
            })
            self.assert200(response)
            self.assertEqual(len(response.json['tags']), 2)

    #
    # test update tags
    #
    def test_update_tag(self):
        with self.app.test_client() as client:
            client.get('/')
            self.csrf_token = session['csrf_token']

            response = client.post('/api/users/login', json={
                'email': 'xua@wustl.edu',
                'password': 'strong_password',
                'csrf_token': self.csrf_token
            })
            self.assertEqual(response.json, self.success)

            event = Event.query.filter_by(event_id=self.event_id).first()
            self.assertEqual(len(Tag.query.with_parent(event).all()), 0)
            event.tags = [
                Tag(tag_name='important', activated=False),
                Tag(tag_name='personal', activated=False)
            ]
            db.session.commit()
            response = client.post('/api/tags/update', json={
                'event_id': self.event_id,
                'tag_name': 'important',
                'activated': True,
                'csrf_token': self.csrf_token
            })
            event = Event.query.filter_by(event_id=self.event_id).first()
            tag = Tag.query.with_parent(event).filter_by(tag_name='important').first()
            self.assertEqual(response.json, self.success)
            self.assertTrue(tag.activated)

    def test_update_not_exist(self):
        with self.app.test_client() as client:
            client.get('/')
            self.csrf_token = session['csrf_token']

            response = client.post('/api/users/login', json={
                'email': 'xua@wustl.edu',
                'password': 'strong_password',
                'csrf_token': self.csrf_token
            })
            self.assertEqual(response.json, self.success)

            response = client.post('/api/tags/update', json={
                'event_id': 'not event id',
                'tag_name': 'important',
                'activated': True,
                'csrf_token': self.csrf_token
            })
            self.assertEqual(response.json, {'code': 404, 'error': 'event not exist'})

            response = client.post('/api/tags/update', json={
                'event_id': self.event_id,
                'tag_name': 'tag name not exist',
                'activated': True,
                'csrf_token': self.csrf_token
            })
            self.assertEqual(response.json, {'code': 404, 'error': 'tag not exist'})

    #
    # test delete tags
    #
    def test_delete_tags(self):
        with self.app.test_client() as client:
            client.get('/')
            self.csrf_token = session['csrf_token']

            response = client.post('/api/users/login', json={
                'email': 'xua@wustl.edu',
                'password': 'strong_password',
                'csrf_token': self.csrf_token
            })
            self.assertEqual(response.json, self.success)

            event = Event.query.filter_by(event_id=self.event_id).first()
            self.assertEqual(len(Tag.query.with_parent(event).all()), 0)
            event.tags = [
                Tag(tag_name='important', activated=False),
                Tag(tag_name='personal', activated=False)
            ]
            db.session.commit()

            event = Event.query.filter_by(event_id=self.event_id).first()
            self.assertEqual(len(Tag.query.with_parent(event).all()), 2)

            response = client.post('/api/tags/delete', json={
                'event_id': self.event_id,
                'tag_name': 'important',
                'csrf_token': self.csrf_token
            })
            self.assert200(response)
            self.assertEqual(response.json, self.success)
            event = Event.query.filter_by(event_id=self.event_id).first()
            # assert number and if the tag is still exist
            self.assertEqual(len(Tag.query.with_parent(event).all()), 1)
            self.assertIsNone(Tag.query.with_parent(event).filter_by(tag_name='important').first())

    def test_delete_not_exist(self):
        with self.app.test_client() as client:
            client.get('/')
            self.csrf_token = session['csrf_token']

            response = client.post('/api/users/login', json={
                'email': 'xua@wustl.edu',
                'password': 'strong_password',
                'csrf_token': self.csrf_token
            })
            self.assertEqual(response.json, self.success)

            response = client.post('/api/tags/delete', json={
                'event_id': 'not event id',
                'tag_name': 'important',
                'csrf_token': self.csrf_token
            })
            self.assertEqual(response.json, {'code': 404, 'error': 'event not exist'})

            response = client.post('/api/tags/delete', json={
                'event_id': self.event_id,
                'tag_name': 'tag name not exist',
                'csrf_token': self.csrf_token
            })
            self.assertEqual(response.json, {'code': 404, 'error': 'tag not exist'})
