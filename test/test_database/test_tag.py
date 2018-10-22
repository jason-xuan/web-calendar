from flask_testing import TestCase
from datetime import datetime
from sqlalchemy import and_, extract
from my_calendar import create_app
from my_calendar.database import db
from my_calendar.modules import User, Event, Tag


class TestTag(TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite:///db_for_test.db"
    TESTING = True

    def create_app(self):
        return create_app(self)

    def setUp(self):
        db.create_all()

        user = User.create('xua@wustl.edu', 'strong_password')
        event = Event.create('dinner', datetime(2018, 7, 5, 18, 30, 0))
        user.events.append(event)
        self.user_id = user.user_id
        self.event_id = event.event_id
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_add_tag(self):
        user = User.query.filter_by(user_id=self.user_id).first()
        event = Event.query.with_parent(user).filter_by(event_id=self.event_id).first()
        tag = Tag(tag_name='important', activated=False)
        event.tags.append(tag)
        db.session.commit()

        user = User.query.filter_by(user_id=self.user_id).first()
        event = Event.query.with_parent(user).filter_by(event_id=self.event_id).first()
        tags = Tag.query.with_parent(event).all()

        self.assertEqual(len(tags), 1)
        self.assertEqual(tags[0].event_id, self.event_id)
        self.assertEqual(tags[0].tag_name, 'important')

