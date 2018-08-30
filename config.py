# -*- coding: utf-8 -*-
# @Time    : 2018/6/7
# @Author  : geekspeng 
# @Email   : geekspeng@icloud.com
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    # SQLAlchemy config
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL',
                                             'sqlite:///' + os.path.join(basedir, 'app.db'))


class TestingConfig(Config):
    TESTING = True

    # SQLAlchemy config
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

