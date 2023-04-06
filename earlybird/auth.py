from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Profile
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.search'))
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash("Please check your login details and try again.")
        return redirect(url_for("auth.login"))

    login_user(user, remember=remember)
    return redirect(url_for('main.search'))


@auth.route('/signup')
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.search'))
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user:
        flash("This email address has already been taken.")
        return redirect(url_for('auth.signup'))

    new_user = User(email=email,
                    password=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.flush()
    new_user_profile = Profile(firstname=firstname,
                               lastname=lastname,
                               user_id=new_user.id)
    db.session.add(new_user_profile)
    db.session.commit()
    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
