from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base

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
    password = Column(String(30))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username