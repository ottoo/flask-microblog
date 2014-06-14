from flask.ext.login import unicode
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base
from passlib.apps import custom_app_context

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String(80))
    content = Column(String(65000))
    date = Column(DateTime)

    def __init__(self, title, content, date=None):
        self.title = title
        self.content = content
        if date is None:
            date = datetime.utcnow()
        self.date = date

    def __repr__(self):
        return '<Post %r>' % self.title

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    email = Column(String(120), unique=True)
    password = Column(String(128))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = custom_app_context.encrypt(password)

    def verify_password(self, password):
        return custom_app_context.verify(password, self.password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % self.username