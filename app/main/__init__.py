# -*- coding: utf-8 -*-
# @Time    : 2018/6/7
# @Author  : geekspeng
# @Email   : geekspeng@icloud.com
from flask import Blueprint

main = Blueprint('main', __name__)

from . import routes
