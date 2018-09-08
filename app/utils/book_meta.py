# -*- coding: utf-8 -*-
# @Time    : 2018/9/8 14:19
# @Author  : geekspeng
# @Email   : geekspeng@icloud.com
from collections import namedtuple

BookMeta = namedtuple('BookMeta',
                      ['title', 'author', 'cover_path', 'description', 'tags',
                       'series', 'series_id', 'languages', 'file_path', 'file_name', 'file_extension', 'file_size'])


def default_meta(title, file_path, file_name, file_extension, file_size):
    return BookMeta(
        title=title,
        author="Unknown",
        cover_path="",
        description="",
        tags="",
        series="",
        series_id="",
        languages="",
        file_path=file_path,
        file_name=file_name,
        file_extension=file_extension,
        file_size=file_size)
