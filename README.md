# Setup

## .env

1. Log in to https://www.reddit.com before visiting https://old.reddit.com/prefs/apps to generate a Client ID and Secret Key.
2. On the website https://old.reddit.com/prefs/apps, you will find an option to create an application.
3. When you reach that point, please choose the following settings for optimal results:
   1.  Choose a name for your app.
   2.  Select the "Script" option.
   3.  For the Redirect URI, use http://localhost:5000
4. When you click "Create App", you will be provided with two keys: one is the CLIENT_ID and the other is the SECRET_ID.
   1. The CLIENT_ID can be found under the name, with the text "personal use script".
   2. The SECRET_KEY is located after the text "secret".
5. Create a file named .env in the same directory as your main.py and enter the following:

>CLIENT_ID = "STRING_HERE" \
SECRET_KEY = "STRING_HERE" \
username = "STRING_HERE"  # This should be your Reddit username. \
password = "STRING_HERE"  # This should be your Reddit password. \
EB_SECRET = "YOUR_RANDOM_STRING"

## Libraries and Dependencies 

### Tensorflow for M1/M2 (Apple)
   required to use TF on M1/M2
   https://developer.apple.com/metal/tensorflow-plugin/

### Git LFS
   used to pull down large files (git lfs pull)
   https://git-lfs.com

### Python libs
   pip3 install -r requirements.txt

## running the application
   - if inside project directory: python3 -m flask --app __init__.py --debug run
   - if in parent dir: python3 -m flask --app project_dir_name --debug run
