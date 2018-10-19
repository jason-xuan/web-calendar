from sqlalchemy import Column, String, Integer, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from passlib.hash import sha256_crypt


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    user_id = Column(Integer(), primary_key=True, autoincrement=True)
    email = Column(String(50), unique=True)
    password = Column(String(100))

    def __init__(self, email: str, password: str):
        self.email = email
        self.password = sha256_crypt.hash(password)

    def verify(self, password):
        return sha256_crypt.verify(password, self.password)


class Event(Base):
    __tablename__ = 'event'
    event_id = Column(Integer(), primary_key=True, autoincrement=True)
    event_name = Column(String(50))
    event_time = Column(DateTime())


class Tag(Base):
    __tablename__ = 'tag'
    tag_id = Column(Integer(), primary_key=True, autoincrement=True)
    tag_name = Column(String(50))
    is_activated = Column(Boolean())
