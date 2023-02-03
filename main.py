from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from . import db

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template("index.html")


# log in required to view private details
@main.route('/profile')
@login_required
def profile():

    # pass firstname for greet message
    return render_template("profile.html", name=current_user.firstname)


# log in required to use search feature???
@main.route('/search')
@login_required
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
