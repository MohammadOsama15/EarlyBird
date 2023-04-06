from flask_login import UserMixin
from . import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    profile = db.relationship('Profile', backref='user', lazy=True)


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    biography = db.Column(db.Text())
    phone = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Timestamp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    search_term = db.Column(db.String(280))
    time = db.Column(db.DateTime)
    titles = db.relationship('Title', backref='timestamp', lazy=True)


class Title(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text())
    prediction = db.Column(db.Float)
    permalink = db.Column(db.Text())
    timestamp_id = db.Column(db.Integer, db.ForeignKey('timestamp.id'))
    comments = db.relationship('Comment', backref='title', lazy=True)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text())
    prediction = db.Column(db.Float)
    title_id = db.Column(db.Integer, db.ForeignKey('title.id'))
