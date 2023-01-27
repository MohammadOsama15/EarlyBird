# .env
A .env file is used in conjunction with .gitignore to obscure sensitive information. To set up the .env:

1. Create a Twitter Developer account at:
   https://developer.twitter.com/en/portal
   
   Note: a valid phone number is required for registration.
  
2. Create a project and generate your API keys.
3. Create a file named .env in the same directory as your app.py and fill in the blank:

>API_KEY = YOUR_TWITTER_API_KEY = "STRING_HERE" \
API_SECRET_KEY = "STRING_HERE" \
BEARER_TOKEN = "STRING_HERE" \
ACCESS_TOKEN = "STRING_HERE" \
ACCESS_TOKEN_SECRET = "STRING_HERE"

4. A .gitnore file has been created as a part of this PR. As of Sprint 1, **pycache** and .**env** is ignored.

Feel free to add additional keys, tokens, environment variables, and the associated documentations.

## .env file explained
We use the dotenv module to load the .env file. By default, the function looks for the presence of .env under the same directory as your app.py file.

Once the configuration file is loaded, we can access these variables by calling the os.getenv() function.

