from flask_login import UserMixin
from . import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    firstname = db.Column(db.String(200))
    lastname = db.Column(db.String(200))


class Query(db.Model):
    handle = db.Column(db.String(280), primary_key=True)
    time = db.Column(db.DateTime)


class Predictions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fk = db.Column(db.String(280))
    comment = db.Column(db.Text(65535))
    prediction = db.Column(db.Float)
