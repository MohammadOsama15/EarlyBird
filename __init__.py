# this module instantiates the app and ties Flask blueprints separated by functionality
import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_caching import Cache


# load environmental variables from .env file
load_dotenv()

# this is used to encrypt our cookie
SECRET_KEY = os.getenv("EB_SECRET")

db = SQLAlchemy()
cache = Cache(config={'CACHE_TYPE': 'simple'})


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['DEBUG'] = True

    try:
        db.init_app(app)
    except Exception as e:
        print(f"Error initializing database: {str(e)}")

    try:
        cache.init_app(app)
    except Exception as e:
        print(f"Error initializing cache: {str(e)}")

    # login_manager is used to keep track of user session state
    login_manager = LoginManager()
    login_manager_login_view = 'auth.login'
    login_manager.init_app(app)

    # import python module used for authentication
    from .auth import auth as auth_blueprint    
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # grab our database model
    from .models import User

    # grab primary key associated with current user
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # create db if one is not already present
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print(f"Error creating database: {str(e)}")

    return app
