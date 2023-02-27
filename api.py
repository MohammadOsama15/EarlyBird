from dotenv import load_dotenv
import os
import requests
# Load environmental variables. By default, dotenv searches current directory for .env file
# A custom filepath to the .env file can be supplied as the argument
load_dotenv()

# Fetch bearer token required for https authentication
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

# https header
headers = {"Authorization": "Bearer {}".format(BEARER_TOKEN)}

# this function converts a Twitter handle into user ID.
# method = GET, url = query string, headers = security token declared above.
def getID(handle):
    url = "https://api.twitter.com/2/users/by/username/{}".format(handle)
    response = requests.request("GET", url, headers=headers)
    return response

# grab Tweets posted by an user ID:
def getTweets(id):
    url = "https://api.twitter.com/2/users/{}/tweets".format(id)
    response = requests.request("GET", url, headers=headers)
    return response