from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from . import cache
from .redditAPI import get_posts
from .inference import model, tokenize_sequence
from .db_functions import check_presence, store_query, delete_query, store_prediction, fetch_results  
from datetime import timedelta
import datetime
import logging

main = Blueprint('main', __name__)

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
file_handler = logging.FileHandler('errors.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


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
    expired = False
    # the data being requested below is from the search form on the search page.
    query = request.args.get("searchTerm")
    if query is not None:
        queried = True
        try:
            #if between server cache and ceiling, pull db entries, else, query api
            record_exists = check_presence(query)
            if record_exists:
                time = record_exists + timedelta(hours=24)
                now = datetime.datetime.utcnow()
                if time < now:
                    expired = True
                    delete_query(handle=query)
                    data = submit_query(query, cap=50)
                else:
                    data = fetch_results(fk=query)
            else:

                data = submit_query(query, cap=50)
            if data:
                if expired:
                    store_query(handle=query)
                return render_template("search.html", data=data)
        except Exception as e:
            logger.error(f"An error occurred while processing search query for user {current_user}: {str(e)}")
            return render_template("error.html", message="An error occurred while processing your search request. Please try again later.")
    return render_template("search.html", queried=queried)


@main.route('/information')
def information():
    return render_template("information.html")


@cache.memoize(timeout=3600)
def submit_query(query: str, cap: int):
    try:
        results = get_posts(query=query, cap=cap)
        if results:
            tokenized_sequence = tokenize_sequence(results)
            predictions = model.predict(tokenized_sequence)
            data = zip(predictions, results)
            return data
    except Exception as e:
        logger.error(f"An error occurred while submitting a search query for user {current_user}: {str(e)}")
        return render_template("error.html", message="An error occurred while processing your search request. Please try again later.")
    return

