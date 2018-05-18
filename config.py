import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # Logging
    LOG_TO_STDERR = False
    LOG_DIRECTORY = 'logs'
    LOG_MAIN_FILE = 'microblog.log'

    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'my-secret-key'
    TOKEN_EXPIRATION_HOURS = int(os.environ.get('TOKEN_EXPIRATION_HOURS') or '24')

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'microblog.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
