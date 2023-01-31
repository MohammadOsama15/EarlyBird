from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('login.html')


# grab user login details and submit via http POST
@auth.route('/login', methods=['POST'])
def login_post():

    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check whether email exists and hash matches, short circuit user back to login page if credentials do not match
    if not user or not check_password_hash(user.password, password):
        flash("Please check your login details and try again.")
        return redirect(url_for("auth.login"))

    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')


# function for submitting user registration info via http POST
@auth.route('/signup', methods=['POST'])
def signup_post():

    email = request.form.get('email')
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    password = request.form.get('password')

    # checks whether email is already in use
    user = User.query.filter_by(email=email).first()
    print(user)

    # if record exists, force signup again
    if user:
        return redirect(url_for('auth.signup'))

    # if execution reaches this line (e.g. doesn't get short-circuited), create new user and hash password entry.
    new_user = User(email=email, firstname=firstname, lastname=lastname,
                    password=generate_password_hash(password, method='sha256'))

    # add the user
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


# log out user via flask_login function and return to index
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    print(url_for('main.index'))
    return redirect(url_for('main.index'))
