# -*- coding: utf-8 -*-
# @Time    : 2018/6/7
# @Author  : geekspeng 
# @Email   : geekspeng@icloud.com
import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'you-will-never-guess')

    # recaptcha
    # RECAPTCHA_PUBLIC_KEY = '6LeYIbsSAAAAACRPIllxA7wvXjIE411PfdB2gt2J'
    # RECAPTCHA_PRIVATE_KEY = '6LeYIbsSAAAAAJezaIq3Ft_hSTo0YtyeFG-JgRtu'
    # RECAPTCHA_OPTIONS = dict(theme='custom')

    # SQLAlchemy config
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL',
                                             'sqlite:///' + os.path.join(basedir, 'app.db'))

    # mail config
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    # admin config
    ADMIN = os.environ.get('ADMIN')

    # log to stdout
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')


class TestingConfig(Config):
    TESTING = True

    # SQLAlchemy config
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

