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
    BOOKS_PER_PAGE = 20

    # mail config
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    # admin config
    ADMIN = os.environ.get('ADMIN')

    # file upload
    UPLOADS_DEFAULT_DEST = os.environ.get('UPLOAD_FOLDER', basedir)
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads')

    # qiniu
    QINIU_ACCESS_KEY = os.environ.get('QINIU_ACCESS_KEY')
    QINIU_SECRET_KEY = os.environ.get('QINIU_SECRET_KEY')
    QINIU_BUCKET_NAME = os.environ.get('QINIU_BUCKET_NAME')
    QINIU_DOMAIN = os.environ.get('QINIU_DOMAIN')

    CONVERT_TOOL_PATH = os.environ.get('CONVERT_TOOL_PATH', None)

    # log to stdout
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')


class TestingConfig(Config):
    TESTING = True

    # SQLAlchemy config
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

