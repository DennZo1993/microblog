from flask import render_template

from app.auth import auth_bp
from app.auth.forms import LoginForm

@auth_bp.route('/login')
def login():
    form = LoginForm()
    return render_template('auth/login.html', title='Login', form=form)