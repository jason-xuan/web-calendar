from passlib.hash import sha256_crypt
from datetime import datetime
from .utils import new_uuid


class User:

    @staticmethod
    def create(email: str, password: str):
        return User(new_uuid(), email, sha256_crypt.hash(password))

    def __init__(self, user_id: str, email: str, password: str):
        self.user_id = user_id
        self.email = email
        self.password = password

    def verify(self, password):
        return sha256_crypt.verify(password, self.password)

    def __repr__(self):
        return f'{self.user_id}:{self.email}'


class Event:

    @staticmethod
    def create(event_name: str, event_time: datetime):
        return Event(new_uuid(), event_name, event_time)

    def __init__(self, event_id: str, event_name: str, event_time: datetime):
        self.event_id = event_id
        self.event_name = event_name
        self.event_time = event_time

    def __repr__(self):
        return f'{self.event_name}:{self.event_time}'


class Tag:

    @staticmethod
    def create(tag_name: str, activated: bool=False):
        return Tag(new_uuid(), tag_name, activated)

    def __init__(self, tag_id: str, tag_name: str, is_activated: bool=False):
        self.tag_id = tag_id
        self.tag_name = tag_name
        self.is_activated = is_activated

    def __repr__(self):
        return f'{self.tag_name}:{"activated" if self.activated else "not activated"}'
