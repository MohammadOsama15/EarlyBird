import requests
import json
import os
from dotenv import load_dotenv

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
    d = res.json()
    if 'access_token' not in d:
        print(f"Error: {d['message']}")
        exit()

    return 'bearer ' + d['access_token']

def get_posts(query):
    if query is None:
        print("Error: Query parameter is None")
        return None

    token = get_access_token()
    headers = {'Authorization': token, 'User-Agent': 'MyAPI/0.0.1'}
    base_url = 'https://oauth.reddit.com'
    response = requests.get(base_url + '/api/v1/me', headers=headers)

    if response.status_code != 200:
        print(f"Error: {response.json()['message']}")
        return None

    res = requests.get(base_url + '/user/' + query + '/overview', headers=headers)
    if res.status_code != 200:
        print(f"Error: {res.json()['message']}")
        return None

    # already taking care of this above but just a double catch, just in case, so it doesn't break.
    if res.status_code == 404:
        print("Reddit user not found.")
        return None

    posts = res.json()['data']['children']
    titles = set()
    for post in posts[:min(50, len(posts))]:
        data = post['data']
        title = data.get('title', data.get('link_title', None))
        if title is not None and title not in titles:
            titles.add(title)
            print(title)
    if not titles:
        return ("Reddit user has no posts.")
    return titles


def search_posts(query):
    titles = get_posts(query)
    return titles
