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

    # Email
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['d.zobnin.teststuff@gmail.com']
