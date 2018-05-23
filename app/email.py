from threading import Thread

from flask import current_app
from flask_mail import Message

from app import mail


def send_email_async(app, message):
    with app.app_context():
        mail.send(message)


def send_email(sender, recipients, subject, text_body, html_body, attachments=None, sync_mode=False):
    msg = Message(subject=subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    if attachments:
        for attachment in attachments:
            msg.attach(*attachment)
    if sync_mode:
        mail.send(msg)
    else:
        Thread(target=send_email_async, args=(current_app._get_current_object(), msg)).start()
