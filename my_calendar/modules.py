from passlib.hash import sha256_crypt
from datetime import datetime
from .database import db
from .utils import new_uuid


class User(db.Model):
    user_id = db.Column(db.String(32), primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(80))
    events = db.relationship('Event', lazy=True, backref='owner')

    @staticmethod
    def create(email: str, password: str):
        return User(user_id=new_uuid(), email=email, password=sha256_crypt.hash(password))

    def verify(self, password):
        return sha256_crypt.verify(password, self.password)

    def __repr__(self):
        return f'{self.user_id}:{self.email}'


class Event(db.Model):
    event_id = db.Column(db.String(32), primary_key=True)
    event_name = db.Column(db.String(100))
    event_time = db.Column(db.DateTime)
    owner_id = db.Column(db.String(32), db.ForeignKey('user.user_id'), nullable=False)
    tags = db.relationship('Tag', backref='event', lazy=False)

    @staticmethod
    def create(event_name: str, event_time: datetime):
        return Event(event_id=new_uuid(), event_name=event_name, event_time=event_time)

    def __repr__(self):
        return f'{self.event_name}:{self.event_time}'

    def to_dict(self):
        return {
            'event_id': self.event_id,
            'owner': self.owner.email,
            'event_name': self.event_name,
            'event_time': str(self.event_time),
        }


class Tag(db.Model):
    event_id = db.Column(db.String(32), db.ForeignKey('event.event_id'), primary_key=False)
    tag_name = db.Column(db.String(100), primary_key=True)
    activated = db.Column(db.Boolean)

    @staticmethod
    def __repr__(self):
        return f'{self.tag_name}:{"activated" if self.activated else "not activated"}'

    def to_dict(self):
        return {
            'tag_id': self.tag_id,
            'tag_name': self.tag_name,
            'activated': self.activated
        }
