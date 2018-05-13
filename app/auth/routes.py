from flask import render_template, redirect, url_for

from app.auth import auth_bp
from app.auth.forms import LoginForm

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('main.index'))
    return render_template('auth/login.html', title='Login', form=form)