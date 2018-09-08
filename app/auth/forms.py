# -*- coding: utf-8 -*-
# @Time    : 2018/8/29 17:52
# @Author  : geekspeng
# @Email   : geekspeng@icloud.com
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models.users import Users


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(6, 24)])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), Length(6, 24), EqualTo('password')])
    # recaptcha = RecaptchaField()
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('The email is registered, please use a different email address.')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old password', validators=[DataRequired(), Length(6, 24)])
    password = PasswordField('New Password', validators=[DataRequired(), Length(6, 24)])
    password2 = PasswordField('Confirm new password', validators=[DataRequired(), Length(6, 24), EqualTo('password')])
    submit = SubmitField('Update Password')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    # recaptcha = RecaptchaField()
    submit = SubmitField('Confirm')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('The email is not registered, please use a different email address.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')