# Running the application
   If in directory:
   python(3) -m flask --app \_\_init\_\_.py --debug run
   If in parent directory:
   python(3) -m flask --app <dirname> --debug run

# Tensorflow for M1/M2 devices
   https://developer.apple.com/metal/tensorflow-plugin/

# .env
A .env file is used in conjunction with .gitignore to obscure sensitive information. To set up the .env:

# Twitter API
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

4. A .gitignore file has been created as a part of this PR. As of Sprint 1, \_\_pycache\_\_ and .env is ignored.

Feel free to add additional keys, tokens, environment variables, and the associated documentations.

# Reddit API 

## Requirements
1. Ensure you have a Reddit account.

## Steps to set up the reddit API
1. Log in to https://www.reddit.com before visiting https://old.reddit.com/prefs/apps to generate a Client ID and Secret Key.
2. On the website https://old.reddit.com/prefs/apps, you will find an option to create an application.
3. When you reach that point, please choose the following settings for optimal results:
   1.  Choose a name for your app.
   2.  Select the "Script" option.
   3.  For the Redirect URI, use http://localhost:8080
4. When you click "Create App", you will be provided with two keys: one is the CLIENT_ID and the other is the SECRET_ID.
   1. The CLIENT_ID can be found under the name, with the text "personal use script".
   2. The SECRET_KEY is located after the text "secret".
5. Create a file named .env in the same directory as your main.py and enter the following:
   
>CLIENT_ID = "STRING_HERE" \
SECRET_KEY = "STRING_HERE" \
username = "STRING_HERE"  # This should be your Reddit username. \
password = "STRING_HERE"  # This should be your Reddit password. \

# .env file explained
We use the dotenv module to load the .env file. By default, the function looks for the presence of .env under the same directory as your app.py file.
Once the configuration file is loaded, we can access these variables by calling the os.getenv() function.

