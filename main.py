from flask import Blueprint, render_template
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def welcome():
    return render_template("index.html")

@main.route('/profile')
def profile():
    return render_template("profile.html")
    
@main.route('/search')
def search():
    return render_template("search.html")

@main.route('/information')
def information():
    return render_template("information.html")

@main.route('/userTopic')
def userTopic():
    return render_template("userTopic.html")

@main.route('/userSentiment')
def userSentiment():
    return render_template("userSentiment.html")

@main.route('/topicSentiment')
def topicSentiment():
    return render_template("topicSentiment.html")