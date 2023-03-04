from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from . import cache
from .redditAPI import get_posts
from .inference import model, tokenize_sequence


main = Blueprint('main', __name__)


@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.search'))
    return render_template("index.html")


# log in required to view private details
@main.route('/profile')
@login_required
def profile():

    # pass firstname for greet message
    return render_template("profile.html", name=current_user.firstname)


@main.route('/search')
@login_required
def search():
    queried = False
    # the data being requested below is from the search form on the search page.
    query = request.args.get("searchTerm")
    if query is not None:
        queried = True
        data = submit_query(query, cap=50)
        if data:
            return render_template("search.html", data=data)
    return render_template("search.html", queried=queried)


@main.route('/information')
def information():
    return render_template("information.html")


@cache.memoize(timeout=3600)
def submit_query(query: str, cap: int):
    results = get_posts(query=query, cap=cap)
    if results:
        tokenized_sequence = tokenize_sequence(results)
        predictions = model.predict(tokenized_sequence)
        data = zip(predictions, results)
        return data
    return
