# -*- coding: utf-8 -*-
# @Time    : 2018/9/8 12:44
# @Author  : geekspeng
# @Email   : geekspeng@icloud.com
import os
from xml import etree

from app import uploads
from app.utils.book_meta import BookMeta


def get_fb2_meta(abs_file_path, file_path, file_name, file_extension):
    ns = {
        'fb': 'http://www.gribuser.ru/xml/fictionbook/2.0',
        'l': 'http://www.w3.org/1999/xlink',
    }

    tree = etree.fromstring(open(abs_file_path).read())

    def get_author(element):
        last_name = element.xpath('fb:last-name/text()', namespaces=ns)
        if len(last_name):
            last_name = last_name[0]
        else:
            last_name = ''
        middle_name = element.xpath('fb:middle-name/text()', namespaces=ns)
        if len(middle_name):
            middle_name = middle_name[0]
        else:
            middle_name = ''
        first_name = element.xpath('fb:first-name/text()', namespaces=ns)
        if len(first_name):
            first_name = first_name[0]
        else:
            first_name = ''
        return first_name + ' ' + middle_name + ' ' + last_name
    authors = tree.xpath('/fb:FictionBook/fb:description/fb:title-info/fb:author', namespaces=ns)
    author = str(", ".join(map(get_author, authors)))

    title = tree.xpath('/fb:FictionBook/fb:description/fb:title-info/fb:book-title/text()', namespaces=ns)
    if len(title):
        title = str(title[0])
    else:
        title = file_name
    description = tree.xpath('/fb:FictionBook/fb:description/fb:publish-info/fb:book-name/text()', namespaces=ns)
    if len(description):
        description = str(description[0])
    else:
        description = ''

    return BookMeta(
        title=title,
        author=author,
        cover_path="",
        description=description,
        tags="",
        series="",
        series_id="",
        languages="",
        file_path=file_path,
        file_name=file_name,
        file_extension=file_extension,
        file_size=os.path.getsize(abs_file_path))
