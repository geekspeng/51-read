# -*- coding: utf-8 -*-
# @Time    : 2018/6/7
# @Author  : geekspeng
# @Email   : geekspeng@icloud.com
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from markupsafe import Markup
from werkzeug.urls import url_parse

from app import db
from app.auth import auth
from app.auth.forms import LoginForm, RegistrationForm, ChangePasswordForm, \
    ResetPasswordRequestForm, ResetPasswordForm, ChangeKindleEmailForm
from app.models.users import Users
from app.utils.email import send_password_reset_email, send_confirmation_email


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint \
                and request.blueprint != 'auth' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/confirm')
@login_required
def resend_confirmation():
    send_confirmation_email(current_user)
    flash(Markup('A new confirmation email has been sent to you by email.'), "info")
    return redirect(url_for('main.index'))


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    user = Users.check_confirmation_token(token)
    if user and current_user.id == user.id:
        user.confirmed = True
        db.session.add(user)
        db.session.commit()
        flash(Markup('You have confirmed your account. Thanks!'), "info")
    else:
        flash(Markup('The confirmation link is invalid or has expired.'), "warning")
    return redirect(url_for('main.index'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(Markup('Invalid email or password'), "warning")
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', title='Sign In', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Users(email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        send_confirmation_email(user)
        flash(Markup('A confirmation email has been sent to you by email.'), "info")
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)


@auth.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.check_password(form.old_password.data):
            current_user.set_password(form.password.data)
            db.session.add(current_user)
            db.session.commit()
            flash(Markup('Your password has been updated.'), "info")
            return redirect(url_for('main.index'))
        else:
            flash(Markup('Invalid password.'), "warning")
    return render_template("auth/change_password.html", title='Change password', form=form)


@auth.route('/change_kindle_email', methods=['GET', 'POST'])
@login_required
def change_kindle_email():
    form = ChangeKindleEmailForm()
    if form.validate_on_submit():
        current_user.kindle_email = form.kindle_email.data
        db.session.add(current_user)
        db.session.commit()
        flash(Markup('Kindle email has been updated.'), "info")
        return redirect(url_for('main.index'))
    form.kindle_email.data = current_user.kindle_email
    return render_template("auth/change_kindle_mail.html", title='Change kindle email', form=form)


@auth.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
            flash(Markup('Check your email for the instructions to reset your password'), "info")
            return redirect(url_for('auth.login'))
        flash(Markup('The email is not registered'), "warning")
    return render_template('auth/reset_password_request.html', title='Reset Password', form=form)


@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = Users.check_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(Markup('Your password has been reset.'), "info")
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)

