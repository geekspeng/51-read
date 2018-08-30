# -*- coding: utf-8 -*-
# @Time    : 2018/6/7
# @Author  : geekspeng
# @Email   : geekspeng@icloud.com
from . import auth


@auth.route('/')
def hello_world():
    return 'auth!'
