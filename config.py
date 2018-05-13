import os

class Config(object):
    LOG_TO_STDERR = False
    LOG_DIRECTORY = 'logs'
    LOG_MAIN_FILE = 'microblog.log'

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'my-secret-key'