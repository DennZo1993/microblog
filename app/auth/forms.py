from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField
from wtforms.validators import (
    DataRequired, EqualTo, Email, Length,
    ValidationError
)

from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    sign_in = SubmitField('Sign in')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField(
        'Password', validators=[DataRequired(), Length(min=8)])
    repeat_password = PasswordField(
        'Repeat password', validators=[DataRequired(), EqualTo('password')])
    register = SubmitField('Register')

    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first() is not None:
            raise ValidationError('This username is already in use')

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first() is not None:
            raise ValidationError('This email address is already in use')