import requests
import json
import os
from dotenv import load_dotenv
import time
import unicodedata

load_dotenv()


def get_access_token():
    """
    Retrieves the access token from the Reddit API.

    Returns:
    str: The access token string or None if there is an error.
    """
    CLIENT_ID = os.getenv("CLIENT_ID")
    SECRET_KEY = os.getenv("SECRET_KEY")
    username = os.getenv("username")
    password = os.getenv("password")
    print(username)
    print(password)

    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)
    data = {
        'grant_type': 'password',
        'username': username,
        'password': password
    }

    headers = {'User-Agent': 'earlybird'}
    try:
        res = requests.post('https://www.reddit.com/api/v1/access_token',
                            auth=auth, data=data, headers=headers)
        print(res.json())
        res.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"Error getting access token: {e}")
        return None

    try:
        d = res.json()
        if 'access_token' not in d:
            print(f"Error: {d['message']}")
            return None

        return f"bearer {d['access_token']}"
    except (json.decoder.JSONDecodeError, KeyError):
        print("Error decoding JSON response from Reddit API")
        return None


def clean_title(title):
    """
    Cleans the given title by removing non-letter characters and extra whitespaces.

    Parameters:
    title (str): The title to clean.

    Returns:
    str: The cleaned title.
    """
    # Remove non-letter characters all of them
    title = ''.join(c for c in title if unicodedata.category(c)
                    [0] == 'L' or c.isspace())
    # Remove extra whitespaces
    title = ' '.join(title.split())
    return title


def get_posts(query, cap=None):
    """
    Retrieves post titles and permalinks based on the given query.

    Parameters:
    query (str): The Reddit username to search for.
    cap (int, optional): The maximum number of posts to return. Defaults to 50.

    Returns:
    tuple: A tuple containing two lists - one with post titles and another with permalinks, or None if there is an error.
    """
    if query is None:
        print("Error: Query parameter is None")
        return

    if cap is None:
        cap = 50

    token = get_access_token()
    if token is None:
        return

    headers = {'Authorization': token, 'User-Agent': 'MyAPI/0.0.1'}
    base_url = 'https://oauth.reddit.com'
    path = f'/user/{query}/overview'
    titles = []
    permalinks = []
    clean_titles = []
    after = None

    while len(titles) < cap:
        params = {'limit': 100}
        if after is not None:
            params['after'] = after

        try:
            res = requests.get(base_url + path, headers=headers, params=params)
            res.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f"Error getting posts: {e}")
            return

        try:
            data = res.json()['data']
            posts = data['children']
        except (json.decoder.JSONDecodeError, KeyError):
            print("Error decoding JSON response from Reddit API")
            return

        for post in posts:
            title = post['data'].get('title')
            permalink = post['data'].get('permalink')

            if title is not None and title not in titles:
                clean = clean_title(title)
                clean_titles.append(clean)
                titles.append(title)
                permalinks.append(permalink)

                if len(titles) >= cap:
                    break

        after = data['after']
        if after is None:
            break

        time.sleep(1)

    if not titles:
        return
    return titles, permalinks


def get_comments(permalink):
    """
    Retrieves comments from a post with the given permalink.

    Parameters:
    permalink (str): The permalink of the post.

    Returns:
    list: A list of comments, or None if there is an error.
    """
    token = get_access_token()
    if token is None:
        return

    headers = {'Authorization': token, 'User-Agent': 'MyAPI/0.0.1'}
    base_url = 'https://oauth.reddit.com/'

    try:
        res = requests.get(base_url + permalink, headers=headers)
        print(permalink)
        res.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"Error getting comments: {e}")
        return

    data = res.json()[1]['data']['children']
    comments = [comment['data'].get('body') for comment in data]
    return comments
