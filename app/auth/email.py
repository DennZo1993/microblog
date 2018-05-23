from flask import current_app, render_template

from app.email import send_email


def send_user_activation_email(user):
    token = user.generate_security_token(purpose='activation')
    send_email(sender=current_app.config['ADMINS'][0], recipients=[user.email],
               subject='Microblog account activation',
               text_body=render_template('email/activation.txt', user=user, token=token),
               html_body=render_template('email/activation.html', user=user, token=token))
