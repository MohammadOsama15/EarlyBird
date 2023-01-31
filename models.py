# create database models in this file
from flask_login import UserMixin
from . import db


# user table structure
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    firstname = db.Column(db.String(200))
    lastname = db.Column(db.String(200))


# Tweet storage data structure
class Tweets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tweet = db.Column(db.String(280))
    time = db.Column(db.DateTime)
    sentiment_score = db.Column(db.Float)
