from flask import render_template, flash
from flask import redirect, url_for
from flask import request
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse

from app import db
from app.data_access import UserDAO
from app.auth import auth_bp
from app.auth.forms import LoginForm, RegistrationForm


@auth_bp.route('/login', methods=['GET', 'POST'])
@auth_bp.route('/register', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    return render_template(
        'auth/login.html', title='Login',
        login_form=LoginForm(), register_form=RegistrationForm())


@auth_bp.route('/login_user', methods=['GET', 'POST'])
def do_login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = UserDAO.get_by_credentials(username=login_form.username.data, password=login_form.password.data)
        if not user:
            flash('Invalid username or password', category='danger')
            return redirect(url_for('.login'))
        if not user.is_active:
            flash('Your account is not active yet. Please check your mailbox for activation link', category='warning')
            return redirect(url_for('.login'))

        login_user(user, remember=login_form.remember_me.data)
        # Redirect to the next page if it's given and valid, '/index' otherwise
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)

    return render_template(
        'auth/login.html', title='Login',
        login_form=login_form, register_form=RegistrationForm())


@auth_bp.route('/register_user', methods=['GET', 'POST'])
def do_register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    register_form = RegistrationForm()
    if register_form.validate_on_submit():
        user = UserDAO.create(username=register_form.username.data,
                              password=register_form.password.data,
                              email=register_form.email.data)

        flash('You are now a registered user!', category='success')
        return redirect(url_for('.login'))

    return render_template(
        'auth/login.html', title='Login',
        login_form=LoginForm(), register_form=register_form)


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
