import os
from os.path import join, dirname
from dotenv import load_dotenv

#TODO get the dotenv environment to work
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

class Config(object):
    # Default configuration
    APP_ENV = os.environ.get('APP_ENV', 'development')

    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    DEBUG = True
    TESTING = False

    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL'] + os.environ['APP_DB'] + "?client_encoding=utf8"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024 #16Mb

    ALLOWED_IMAGES = ['png', 'svg', 'jpg']
    MAX_IMG_SIZE = 200000
    ALLOWED_EXTENSIONS = ['pdf']

    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER')

    APPINSIGHTS_INSTRUMENTATIONKEY = os.environ.get('APPINSIGHTS_INSTRUMENTATIONKEY')

    SEND_FILE_MAX_AGE_DEFAULT = 0

    CV_SUBMISSION_OPEN = os.environ.get('CV_SUBMISSION_OPEN')

    ACTIVITIES = ['Workshops', 'Speakers', 'Tech Talks', 'Panel Discussions', 'Job Fair', 'Matchmaking']

    STUDENT_APP_URL = os.environ.get('STUDENT_APP_URL')

    ROCKET_CHAT_APP_URL = os.environ.get('ROCKET_CHAT_APP_URL')
    ROCKET_CHAT_ADMIN_USERNAME = os.environ.get('ROCKET_CHAT_ADMIN_USERNAME')
    ROCKET_CHAT_ADMIN_PASSWORD = os.environ.get('ROCKET_CHAT_ADMIN_PASSWORD')

class DevelopmentConfig(Config):
    """Development configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY')

    DEBUG = True
    TESTING = True

    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL'] + os.environ['APP_DB'] + "?client_encoding=utf8"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    ALLOWED_EXTENSIONS = ['pdf']
    

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    APP_DB = os.environ.get('APP_DB')
    # SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL'] + APP_DB
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class StagingConfig(Config):
    """ Staging configuration"""
    DEBUG = True
    SESSION_COOKIE_SECURE = True
    DEVELOPMENT = True


class ProductionConfig(Config):
    """Production configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG = False
    SESSION_COOKIE_SECURE = True

    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL'] + os.environ['APP_DB'] + "?client_encoding=utf8"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    ALLOWED_EXTENSIONS = ['pdf']


config = {
    'development': DevelopmentConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}

__all__ = ['config']
