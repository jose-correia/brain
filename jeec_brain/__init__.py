import os
from config import config, Config
from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from flask_cors import CORS

from jeec_brain.database import db, create_tables

from jeec_brain.finders.users_finder import UsersFinder

csrf = CSRFProtect()
login_manager = LoginManager()


def initialize_auth_api_blueprint(app):
    from jeec_brain.apps.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    csrf.exempt(auth_bp)

def initialize_admin_api_blueprint(app):
    from jeec_brain.apps.admin_api  import bp as admin_api_bp
    app.register_blueprint(admin_api_bp, url_prefix='/admin')
    csrf.exempt(admin_api_bp)

def initialize_cv_platform_api(app):
    from jeec_brain.apps.cv_platform_api import bp as cv_platform_api_bp
    app.register_blueprint(cv_platform_api_bp, url_prefix='/cvplatform')
    csrf.exempt(cv_platform_api_bp)

def initialize_website_api_blueprint(app):
    from jeec_brain.apps.website_api  import bp as website_api_bp
    app.register_blueprint(website_api_bp, url_prefix='/website')
    csrf.exempt(website_api_bp)


def create_app():
    app = Flask(__name__)

    env_config = Config.APP_ENV
    app.config.from_object(config[env_config])
   
   # initialize login manager
    login_manager.login_message = 'First you must sign in.'
    login_manager.login_message_category = 'danger'
    login_manager.init_app(app)

    with app.app_context():
        db.init_app(app)
        create_tables()

    # enable CSRF protection
    csrf.init_app(app)

    CORS(app) # enable Cross-Origin Resource Sharing
    
    app.config['UPLOAD_FOLDER'] = os.path.join(app.instance_path, 'storage')

    initialize_auth_api_blueprint(app)
    initialize_admin_api_blueprint(app)
    initialize_cv_platform_api(app)
    initialize_website_api_blueprint(app)

    app.app_context().push()
    return app


@login_manager.user_loader
def load_user(username):
    return UsersFinder.get_user_from_username(username=username)
