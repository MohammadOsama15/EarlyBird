from flask_login import login_required, current_user
from flask import Blueprint, render_template, redirect, url_for, request
from . import cache
from .redditAPI import get_posts
from .inference import model, tokenize_sequence
from .db_functions import check_presence, store_query
from .db_functions import delete_query, fetch_results
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
    query = request.args.get("searchTerm")
    if query is not None:
        queried = True
        try:
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
            logger.error(
                f"Error querying user {current_user}: {str(e)}")
            return render_template("error.html", message="Search error.")
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
            data = zip(results, predictions)
            return data
    except Exception as e:
        logger.error(
            f"Error querying user {current_user}: {str(e)}")
        return render_template("error.html", message="Search error.")
    return
