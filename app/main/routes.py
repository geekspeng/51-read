# -*- coding: utf-8 -*-
# @Time    : 2018/6/7
# @Author  : geekspeng
# @Email   : geekspeng@icloud.com
from flask import render_template
from . import main


@main.route('/')
def index():
    return render_template('main/index.html', title="Index")


@main.route('/search')
def search():
    return 'search!'
