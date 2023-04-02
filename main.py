from flask_login import login_required, current_user
from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from . import cache
from .redditAPI import get_posts, get_comments
from .inference import model, tokenize_sequence
from .db_functions import get_timestamp
from .db_functions import store_timestamp
from .db_functions import delete_timestamp
from .db_functions import get_predictions
from .db_functions import store_prediction
from .db_functions import delete_predictions
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
    """
    The index route, which redirects to the search route if the user is authenticated.

    Returns:
    The rendered index.html template or a redirect to the search route.
    """

    if current_user.is_authenticated:
        return redirect(url_for('main.search'))
    return render_template("index.html")


@main.route('/profile')
@login_required
def profile():
    """
    The profile route, which requires user logged in.

    Returns:
    The rendered profile.html template with the user's first name.
    """
    return render_template("profile.html", name=current_user.firstname)


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
    data = submit_query(query, cap= 50)
    # if query:
    #     queried = True
    #     timestamp_from_db = get_timestamp(search_term=query)
    #     predictions_from_db = get_predictions(fk=query)
    #     if timestamp_from_db and predictions_from_db:
    #         is_in_db = "yes"
    #         now = datetime.datetime.utcnow()
    #         if (timestamp_from_db + timedelta(hours=24)) < now:
    #             is_in_db = "expired"
    # match is_in_db:
    #     case "no":
    #         data = submit_query(query, cap=50)
    #     case "expired":
    #         data = submit_query(query, cap=50)
    #         delete_timestamp(search_term=query)
    #         delete_predictions(fk=query)
    #     case "yes":
    #         data = predictions_from_db
    # if data:
    #     if is_in_db != "yes":
    #         store_timestamp(search_term=query)
    #         store_prediction(fk=query, predictions=data)
    # Assuming 'titles', 'predictions', and 'permalinks' are the lists containing the data
  
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
def comments(permalink):
    """
    The comments route, which requires user logged in.

    Parameters:
    permalink (str): The permalink of the post.

    Returns:
    The rendered comments.html template with the comments for the post.
    """
    comments = get_comments(permalink)
    return render_template("comments.html", comments=comments)

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
            data = zip(results, predictions,permalinks)
            data = [{'title': t, 'prediction': p, 'permalink': l} for t, p, l in zip(titles, predictions, permalinks)]
            return data
        return
    except Exception as e:
        logger.error(
            f"Error querying user {current_user}: {str(e)}")
        return None