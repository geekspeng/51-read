# -*- coding: utf-8 -*-
# @Time    : 2018/8/29 18:00
# @Author  : geekspeng
# @Email   : geekspeng@icloud.com
from flask import render_template
from . import errors


@errors.app_errorhandler(403)
def forbidden(e):
    return render_template('errors/403.html'), 403


@errors.app_errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@errors.app_errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500
