from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table, Boolean, DateTime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(50), unique=True)
    name = Column(String(50))
    password = Column(String(100))
    join_date = Column(Date)
    description = Column(String(500))
    questions = relationship("Question")
    answers = relationship("Answer")
    votes = relationship("Vote")


class Category(db.Model):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    description = Column(String(500))
    questions = relationship("Question")


class Post(db.Model):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('users.id'))
    content = Column(String(1000))
    votes = relationship("Vote", lazy='dynamic')
    author = relationship("User")
    date = Column(DateTime)

    __mapper_args__ = {'polymorphic_identity':'posts'}


class Question(Post):
    __tablename__ = "questions"
    id = Column(Integer, ForeignKey('posts.id'), primary_key=True)
    title = Column(String(50))
    category_id = Column(Integer, ForeignKey('categories.id'))
    # answers = relationship("Answer", foreign_keys=[id])

    __mapper_args__ = {'polymorphic_identity':'questions'}


class Answer(Post):
    __tablename__ = "answers"
    id = Column(Integer, ForeignKey('posts.id'), primary_key=True)
    question_id = Column(Integer, ForeignKey('questions.id'))
    is_best = Column(Boolean)

    __mapper_args__ = {'polymorphic_identity':'answers'}


class Vote(db.Model):
    __tablename__ = "votes"
    id = Column(Integer, primary_key=True)
    post_id =  Column(Integer, ForeignKey('posts.id'))
    author_id = Column(Integer, ForeignKey('users.id'))
    is_up = Column(Boolean)