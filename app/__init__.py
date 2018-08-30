# -*- coding: utf-8 -*-
# @Time    : 2018/8/29 17:52
# @Author  : geekspeng
# @Email   : geekspeng@icloud.com
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    from app.errors import errors as errors_blueprint
    app.register_blueprint(errors_blueprint)

    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
