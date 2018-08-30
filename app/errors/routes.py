# -*- coding: utf-8 -*-
# @Time    : 2018/8/29 18:00
# @Author  : geekspeng
# @Email   : geekspeng@icloud.com
from . import errors


@errors.route('/errors')
def hello_world():
    return 'errors!'
