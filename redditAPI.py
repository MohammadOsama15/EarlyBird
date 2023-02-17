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
    res = requests.post('https://www.reddit.com/api/v1/access_token',
                        auth=auth, data=data, headers=headers)
    try:
        d = res.json()
        if 'access_token' not in d:
            print(f"Error: {d['message']}")
            return None

        return f"bearer {d['access_token']}"
    except json.decoder.JSONDecodeError:
        print(f"Error: Could not decode JSON response from Reddit API")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


def clean_title(title):
    # Remove non-letter characters all of them
    title = ''.join(c for c in title if unicodedata.category(c)[0] == 'L' or c.isspace())
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
    response = requests.get(base_url + '/api/v1/me', headers=headers)

    if response.status_code != 200:
        print(f"Error: {response.json()['message']}")
        return

    path = f'/user/{query}/overview'
    titles = []
    clean_titles =[] # to save all the cleaned up titles
    after = None
    while len(titles) < cap:
        params = {'limit': 100}
        if after is not None:
            params['after'] = after

        res = requests.get(base_url + path, headers=headers, params=params)
        if res.status_code != 200:
            print(f"Error: {res.json()['message']}")
            return

        data = res.json()['data']
        posts = data['children']
        for post in posts:
            title = post['data'].get('title')
            if title is not None and title not in titles:
                clean = clean_title(title)
                clean_titles.append(clean) #saving it in the array clean_titles 
                titles.append(title) #displaying normal titles to front end
                if len(titles) >= cap:
                    break

        after = data['after']
        if after is None:
            break

        time.sleep(1)

    if not titles:
        return "Reddit user has no posts."
    return titles

def search_posts(query, cap=None):
    titles = get_posts(query, cap)
    if titles is None:
        return None

    # Perform additional processing on the returned titles, if needed.
    return titles
