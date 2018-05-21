from datetime import datetime

from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)

    registered_on = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {0} ({1})>'.format(self.username, self.email)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    body = db.Column(db.String(1000))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return '<Post "{title}" from {ts} by user id={uid}>'.format(
            title=self.title, ts=self.timestamp, uid=self.user_id)