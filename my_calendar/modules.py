from passlib.hash import sha256_crypt
from datetime import datetime


class User:

    @staticmethod
    def create(email: str, password: str):
        return User(email, sha256_crypt.hash(password))

    def __init__(self, email: str, password: str, user_id: int=None):
        self.user_id = user_id
        self.email = email
        self.password = password

    def verify(self, password):
        return sha256_crypt.verify(password, self.password)

    def __repr__(self):
        return f'{self.user_id}:{self.email}'


class Event:

    def __init__(self, event_name: str, event_time: datetime, event_id: int=None):
        self.event_id = event_id
        self.event_name = event_name
        self.event_time = event_time

    def __repr__(self):
        return f'{self.event_name}:{self.event_time}'


class Tag:
    def __init__(self, tag_name: str, is_activated: bool=False, tag_id: int=None):
        self.tag_id = tag_id
        self.tag_name = tag_name
        self.is_activated = is_activated

    def __repr__(self):
        return f'{self.tag_name}:{"activated" if self.is_activated else "not activated"}'
