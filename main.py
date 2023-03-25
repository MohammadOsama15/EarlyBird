from flask_login import login_required, current_user
from flask import Blueprint, render_template, redirect, url_for, request
from . import cache
from .redditAPI import get_posts
from .inference import model, tokenize_sequence
from .db_functions import get_timestamp, store_timestamp, delete_timestamp
from .db_functions import get_predictions, store_prediction, delete_predictions
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


@main.route('/profile')
@login_required
def profile():
    return render_template("profile.html", name=current_user.firstname)


@main.route('/search')
@login_required
def search():
    queried = False
    data = None
    case = None
    query = request.args.get("searchTerm")
    if query:
        queried = True
        timestamp_from_db = get_timestamp(search_term=query)
        print(timestamp_from_db and 0)
        predictions_from_db = get_predictions(fk=query)
        print(predictions_from_db and 0)
        if not timestamp_from_db or predictions_from_db:
            print("not in db")
            case = "not_in_db"
        elif (timestamp_from_db + timedelta(hours=24)) < datetime.datetime.utcnow():
            case = "expired"
            print("expired")
        else:
            case = "valid"
        print(case)
        match case:
            case "not_in_db":
                data = submit_query(query, cap=50)
            case "expired":
                delete_timestamp(search_term=query)
                delete_predictions(fk=query)
                data = submit_query(query, cap=50)
            case "valid":
                data = predictions_from_db
    template = render_template("search.html", data=data, queried=queried)
    if case == "not_in_db" or case == "expired":
        store_timestamp(search_term=query)
        store_prediction(fk=query, predictions=data)
    return template


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
        return
    except Exception as e:
        logger.error(
            f"Error querying user {current_user}: {str(e)}")
