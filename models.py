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


# table for search box input and time associated with query
class Query(db.Model):
    handle = db.Column(db.String(280), primary_key=True)
    time = db.Column(db.DateTime)

# table for strings and predictions associated with them
class Predictions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fk = db.Column(db.String(280))
    comment = db.Column(db.Text(65535))
    prediction = db.Column(db.Float)

# error handling
try:
    db.create_all()
except Exception as e:
    print("Error creating database: ", str(e))
