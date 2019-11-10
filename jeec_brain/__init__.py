import os
from config import config, Config
from flask import Flask, redirect, url_for, request, jsonify
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from flask_cors import CORS

from jeec_brain.database import db, create_tables
from jeec_brain.finders.users_finder import UsersFinder

from applicationinsights.flask.ext import AppInsights

csrf = CSRFProtect()
login_manager = LoginManager()


def initialize_admin_api_blueprint(app):
    from jeec_brain.apps.admin_api  import bp as admin_api_bp
    app.register_blueprint(admin_api_bp, url_prefix='/admin')
    csrf.exempt(admin_api_bp)

def initialize_companies_api_blueprint(app):
    from jeec_brain.apps.companies_api import bp as companies_api_bp
    app.register_blueprint(companies_api_bp, url_prefix='/companies')
    csrf.exempt(companies_api_bp)

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

    # enable Cross-Origin Resource Sharing
    CORS(app)
    
    app.config['UPLOAD_FOLDER'] = os.path.join(app.instance_path, 'storage')

    initialize_admin_api_blueprint(app)
    initialize_companies_api_blueprint(app)
    initialize_website_api_blueprint(app)

    # add health-check route
    @app.route('/health', methods=['GET'])
    def health():
        return jsonify(success=True)

    # set up index route
    @app.route('/', methods=['GET'])
    def index():
        return redirect(url_for('companies_api.get_company_login_form'))

    # enable azure insights integration
    appinsights = AppInsights(app)
    @app.after_request
    def after_request(response):
        appinsights.flush()
        return response

    # force https access by redirecting the client 
    @app.before_request
    def before_request():
        if request.url.startswith('http://'):
            url = request.url.replace('http://', 'https://', 1)
            code = 301
            return redirect(url, code=code)

    app.app_context().push()
    return app


@login_manager.user_loader
def load_user(username):
    return UsersFinder.get_user_from_username(username=username)
