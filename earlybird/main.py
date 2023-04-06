from flask_login import login_required, current_user
from flask import Blueprint
from flask import flash
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from . import cache
from .api import get_posts, get_comments
from .inference import model, tokenize_sequence
from .db_functions import get_timestamp
from .db_functions import store_timestamp
from .db_functions import delete_timestamp
from .db_functions import get_titles
from .db_functions import store_titles
from .db_functions import delete_titles
from .db_functions import get_profile
from .db_functions import update_password
from .db_functions import update_profile
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash
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
    """
    The index route, which redirects to the search route if the user is authenticated.

    Returns:
    The rendered index.html template or a redirect to the search route.
    """

    if current_user.is_authenticated:
        return redirect(url_for('main.search'))
    return render_template("index.html")


@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """
    The profile route, which requires user logged in.

    Returns:
    The rendered profile.html template with the user's first name.
    """
    user_payload = {}
    profile_payload = {}
    if request.method == 'POST':

        user_params = {"password",
                       "newpassword",
                       "confirmpassword"}
        user_payload = {key: value for key,
                        value in request.form.items() if key in user_params and value != ""}
        profile_payload = {key: value for key,
                           value in request.form.items() if key not in user_params and value != ""}
        if profile_payload:
            update_profile(current_user.id, profile_payload)
        if set(["password", "newpassword", "confirmpassword"]).issubset(user_payload.keys()):
            print("all three fields are present")
            if not check_password_hash(current_user.password, user_payload['password']):
                flash("Please check your password and try again.")
            else:
                user_payload['newpassword'] = generate_password_hash(
                    user_payload['newpassword'], method='sha256')
                update_password(current_user.id, user_payload)
                return redirect(url_for('auth.logout'))

    profile = get_profile(current_user.id)
    return render_template("profile.html", profile=profile, user=user_payload)


@main.route('/search')
@login_required
def search():
    """
    The search route, which requires user to be logged in.

    Returns:
    The rendered search.html template with the search results.
    """
    queried, data, is_in_db = False, None, "no"
    query = request.args.get("searchTerm")
    CAP = 50
    if query:
        queried = True
        exists_timestamp = get_timestamp(search_term=query)
        if exists_timestamp:
            timestamp_from_db, stored_query_id = exists_timestamp
            titles_from_db = get_titles(stored_query_id)
            if timestamp_from_db and titles_from_db:
                is_in_db = "yes"
                now = datetime.datetime.utcnow()
                if (timestamp_from_db + timedelta(hours=24)) < now:
                    is_in_db = "expired"
    match is_in_db:
        case "no":
            data = submit_query(query, cap=CAP)
        case "expired":
            data = submit_query(query, cap=CAP)
            delete_timestamp(fk=stored_query_id)
            delete_titles(fk=stored_query_id)
        case "yes":
            data = titles_from_db
    if data:
        if is_in_db != "yes":
            store_timestamp(search_term=query)
            _, timestamp_id = get_timestamp(search_term=query)
            store_titles(fk=timestamp_id, data=data)
    return render_template("search.html", data=data, queried=queried)


@main.route('/information')
def information():
    """
    The information route.

    Returns:
    The rendered information.html template.
    """
    return render_template("information.html")


@main.route('/comments/r/<path:permalink>')
@login_required
def comments(permalink: str):
    """
    The comments route, which requires user logged in.

    Parameters:
    permalink (str): The permalink of the post.

    Returns:
    The rendered comments.html template with the comments for the post.
    """
    data = infer_comments(permalink)
    return render_template("comments.html", data=data)


@cache.memoize(timeout=3600)
def submit_query(query: str, cap: int):
    """
    Submits a query to the Reddit API, tokenizes the results, and makes predictions using a model.

    Parameters:
    query (str): The query to search for in the Reddit API.
    cap (int): The number of results to query.

    Returns:
    list: A list of dictionaries containing the title, prediction, and permalink for each result, or None if there is an error.
    """
    try:
        results = get_posts(query=query, cap=cap)
        if results:
            titles, permalinks = results
            tokenized_sequence = tokenize_sequence(titles)
            predictions = model.predict(tokenized_sequence)
            data = zip(results, predictions, permalinks)
            data = [{'title': t, 'prediction': p, 'permalink': l}
                    for t, p, l in zip(titles, predictions, permalinks)]
            return data
        return
    except Exception as e:
        logger.error(
            f"Error querying user {current_user}: {str(e)}")
        return None


@cache.memoize(timeout=3600)
def infer_comments(permalink: str):
    """
    Submits a query to the Reddit API, tokenizes the results, and makes predictions using a model.

    Parameters:
    fk (int): Title.id
    permalink: permalink of the title

    Returns:
    list: A list of dictionaries containing the comments and the associated predictions.
    """
    try:
        comments = get_comments(permalink)
        if comments:
            tokenized_sequence = tokenize_sequence(comments)
            predictions = model.predict(tokenized_sequence)
            data = zip(comments, predictions)
            data = [{'comment': c, 'prediction': p}
                    for c, p in zip(comments, predictions)]
            return data
    except Exception as e:
        logger.error(
            f"Could not fetch comments: {str(e)}")
        return None
