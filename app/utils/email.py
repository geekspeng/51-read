# -*- coding: utf-8 -*-
# @Time    : 2018/9/6 15:35
# @Author  : geekspeng
# @Email   : geekspeng@icloud.com
from threading import Thread
from flask import render_template, current_app
from flask_mail import Message
from app import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body,
               attachments=None, sync=False):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    if attachments:
        for attachment in attachments:
            msg.attach(*attachment)
    if sync:
        mail.send(msg)
    else:
        Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()


def send_confirmation_email(user):
    token = user.generate_confirmation_token()
    send_email(subject='[51read] Confirm Your Account',
               sender=current_app.config['ADMIN'],
               recipients=[user.email],
               text_body=render_template('email/confirm.txt',
                                         user=user, token=token),
               html_body=render_template('email/confirm.html',
                                         user=user, token=token))


def send_password_reset_email(user):
    token = user.generate_reset_password_token()
    send_email('[51read] Reset Your Password',
               sender=current_app.config['ADMIN'],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))


