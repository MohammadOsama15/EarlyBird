from flask_login import login_required, current_user
from flask import Blueprint
from flask import flash
from flask import jsonify
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from flask import Response, make_response
from . import cache
from .api import get_posts, get_comments, get_user_comments, clean_title
from .inference import model, tokenize_sequence
from .db_functions import *
from .models import Timestamp, Comment
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import json
import logging
import os
import pandas as pd
import plotly.express as px

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

@main.route('/search_history')
@login_required
def search_history():
    search_history_data = Timestamp.query.order_by(Timestamp.time.desc()).all()
    unique_search_history_data = []
    seen_search_terms = set()

    for search in search_history_data:
        if search.search_term not in seen_search_terms:
            unique_search_history_data.append(search)
            seen_search_terms.add(search.search_term)

    return render_template("search_history.html", search_history=unique_search_history_data)

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
                update_password(current_user.id, user_payload['newpassword'])
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
    CAP = 100
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
            delete_timestamp(search_term=query)
            delete_titles(fk=stored_query_id)
        case "yes":
            data = titles_from_db
    if data:
        if is_in_db != "yes":
            store_timestamp(search_term=query)
            _, timestamp_id = get_timestamp(search_term=query)
            store_titles(fk=timestamp_id, data=data)
    user_comments_url = url_for('main.user_comments', searchTerm=query)
    return render_template("search.html", query=query, data=data, queried=queried, user_comments_url=user_comments_url)


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
    res = infer_comments(permalink)
    data=None
    if res:
        data, df_json = res
        delete_comments(query=permalink)
        store_comments(permalink, df_json)
    return render_template("comments.html", data=data, query=permalink)

@main.route('/store-labeled-data', methods=['POST'])
@login_required
def add_training_data():
    comment = request.json
    store_labeled_data(comment['corpus'], comment['prediction'])
    return jsonify({'message': 'Data stored successfully.'})

@main.route('/download-inference', methods=['POST'])
@login_required
def download_inference():
    data = request.json
    query = data['query']
    json_string = retrieve_comments(query)
    response = make_response(json_string)
    response.headers['Content-Type'] = 'application/json'
    response.headers['Content-Disposition'] = 'attachment; filename=inference.json'
    return response

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
            cleaned = []
            titles, permalinks = results
            for title in titles:
                cleaned.append(clean_title(title))
            tokenized_sequence = tokenize_sequence(titles)
            predictions = model.predict(tokenized_sequence)
            data = [{'title': t, 'prediction': p, 'permalink': l, 'cleaned_title': c}
                    for t, p, l, c in zip(titles, predictions, permalinks, cleaned)]
            for item in data:
                print(item['cleaned_title'])
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
            cleaned = []
            for comment in comments:
                cleaned.append(clean_title(comment))
            tokenized_sequence = tokenize_sequence(comments)
            predictions = model.predict(tokenized_sequence)
            data = [{'comment': c, 'prediction': p, 'cleaned_corpus': cleaned}
                    for c, p, cleaned in zip(comments, predictions, cleaned)]
            flattened_predictions = [val for sublist in predictions for val in sublist]
            df = pd.DataFrame({'comment': comments, 'prediction': flattened_predictions})
            df_json = df.to_json(orient='records')
            return data, df_json
    except Exception as e:
        logger.error(
            f"Could not fetch comments: {str(e)}")
        return None
    
@main.route('/user_comments')
@login_required
def user_comments():
    """
    The user_comments route, which requires user to be logged in.
    Returns:
    The rendered user_comments.html template with the user's comments.
    """
    query = request.args.get("searchTerm")
    if query:
        comments, comment_timestamps = get_user_comments(query, cap=200)
        tokenized_sequence = tokenize_sequence(comments)
        predictions = model.predict(tokenized_sequence)
        flattened_predictions = [val for sublist in predictions for val in sublist]

        df = pd.DataFrame({'comment': comments, 'timestamp': comment_timestamps, 'prediction': flattened_predictions})
        df_json = df.to_json(orient='records')
        delete_comments(query=query)
        store_comments(query, df_json)

        # Scatter plot
        scatter_fig = px.scatter(df, x='timestamp', y='prediction', title='Sentiment Heat Map')
        scatter_fig.write_html(os.path.dirname(__file__)+"/static/scatter_plot.html", include_plotlyjs='cdn', full_html=False)

        # Line graph
        line_fig = px.line(df, x='timestamp', y='prediction', title='Sentiment Over Time')
        line_fig.write_html(os.path.dirname(__file__)+"/static/line_plot.html", include_plotlyjs='cdn', full_html=False)

        # Count positive and negative sentiments
        positive_count = sum(1 for p in flattened_predictions if p >= 0.5)
        negative_count = sum(1 for p in flattened_predictions if p < 0.5)

        # Pie chart
        pie_fig = px.pie(names=['Positive', 'Negative'],
                         values=[positive_count, negative_count],
                         title='Sentiment Distribution')
        pie_fig.write_html(os.path.dirname(__file__)+"/static/pie_chart.html", include_plotlyjs='cdn', full_html=False)


        data = zip(comments, comment_timestamps, flattened_predictions)
        data = [{'comment': c, 'timestamp': t, 'predictions': p} for c, t, p in data]
    else:
        data = []


    return render_template("user_comments.html", data=data, query=query)
