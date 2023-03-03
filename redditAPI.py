import requests
import json
import os
from dotenv import load_dotenv
import time
import unicodedata

load_dotenv()


def get_access_token():
    CLIENT_ID = os.getenv("CLIENT_ID")
    SECRET_KEY = os.getenv("SECRET_KEY")
    username = os.getenv("username")
    password = os.getenv("password")

    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)
    data = {
        'grant_type': 'password',
        'username': username,
        'password': password
    }

    headers = {'User-Agent': 'MyAPI/0.0.1'}
    try:
        res = requests.post('https://www.reddit.com/api/v1/access_token',
                            auth=auth, data=data, headers=headers)
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
        print(f"Error decoding JSON response from Reddit API")
        return None


def clean_title(title):
    # Remove non-letter characters all of them
    title = ''.join(c for c in title if unicodedata.category(c)
                    [0] == 'L' or c.isspace())
    # Remove extra whitespaces
    title = ' '.join(title.split())
    return title


def get_posts(query, cap=None):
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
    try:
        response = requests.get(base_url + '/api/v1/me', headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"Error getting user info: {e}")
        return

    path = f'/user/{query}/overview'
    titles = []
    clean_titles = []  # to save all the cleaned up titles
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
            print(f"Error decoding JSON response from Reddit API")
            return

        for post in posts:
            title = post['data'].get('title')
            if title is not None and title not in titles:
                clean = clean_title(title)
                # saving it in the array clean_titles
                clean_titles.append(clean)
                titles.append(title)  # displaying normal titles to front end
                if len(titles) >= cap:
                    break

        after = data['after']
        if after is None:
            break

        time.sleep(1)

    if not titles:
        return
    return titles
