import logging
from logging import StreamHandler
from logging.handlers import RotatingFileHandler
import os

from flask import Flask
from flask.logging import default_handler
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail

from config import Config


bootstrap = Bootstrap()
login = LoginManager()
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()

def create_app(config_obj=Config):
    app = Flask(__name__)
    app.config.from_object(config_obj)

    # Register blueprints
    from app.errors import errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.main import main_bp
    app.register_blueprint(main_bp)

    # Init application
    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    login.init_app(app)
    login.login_view = 'auth.login'

    # Init logging
    if not app.debug:
        if app.config['LOG_TO_STDERR']:
            log_handler = StreamHandler()
        else:
            log_dir = app.config['LOG_DIRECTORY']
            if not os.path.exists(log_dir):
                os.mkdir(log_dir)
            log_file = os.path.join(log_dir, app.config['LOG_MAIN_FILE'])
            log_handler = RotatingFileHandler(filename=log_file, maxBytes=10240, backupCount=10)

        formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
        log_handler.setFormatter(formatter)
        log_handler.setLevel(logging.INFO)

        app.logger.removeHandler(default_handler)
        app.logger.addHandler(log_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Microblog startup')

    return app

from app import models