from datetime import datetime, timedelta
import jwt

from flask import current_app
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)

    registered_on = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    activated_on = db.Column(db.DateTime, nullable=True)

    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {0} ({1})>'.format(self.username, self.email)

    ''' Flask-Login requirements
    '''

    @property
    def is_active(self):
        return self.activated_on is not None

    ''' Common functions
    '''

    def activate(self, activation_time=None):
        self.activated_on = activation_time if activation_time else datetime.utcnow()

    def deactivate(self):
        self.activated_on = None

    def set_email(self, email_addr):
        self.email = email_addr.lower()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_security_token(self, purpose):
        exp_delta = timedelta(hours=current_app.config['TOKEN_EXPIRATION_HOURS'])
        payload = {
            'user_id': self.id,
            'purpose': purpose,
            'exp': datetime.utcnow() + exp_delta,
        }
        token = jwt.encode(payload, current_app.config['SECRET_KEY'], 'HS256')
        return token.decode('utf-8')

    @staticmethod
    def validate_security_token(token, purpose):
        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], 'HS256')
            if payload['purpose'] != purpose:
                return None
            user_id = payload['user_id']
        except:
            return None
        return User.query.get(user_id)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    body = db.Column(db.String(1000))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return '<Post "{title}" from {ts} by user id={uid}>'.format(
            title=self.title, ts=self.timestamp, uid=self.user_id)
