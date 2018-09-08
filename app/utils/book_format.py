# -*- coding: utf-8 -*-
# @Time    : 2018/9/8 12:44
# @Author  : geekspeng
# @Email   : geekspeng@icloud.com
import logging
import os

from app import uploads
from app.utils import pdf, epub, fb2
from app.utils.book_meta import default_meta

logger = logging.getLogger("book_format")


def process(abs_file_path, file_path, file_name, file_extension):
    meta = None
    try:
        if "PDF" == file_extension.upper():
            meta = pdf.get_pdf_meta(abs_file_path, file_path, file_name, file_extension.upper())
        elif "EPUB" == file_extension.upper():
            meta = epub.get_epub_meta(abs_file_path, file_path, file_name, file_extension.upper())
        elif "FB2" == file_extension.upper():
            meta = fb2.get_fb2_meta(abs_file_path, file_path, file_name, file_extension.upper())
    except Exception as ex:
        logger.warning('cannot parse metadata, using default: %s', ex)

    if meta:
        return meta
    else:
        return default_meta(file_name, file_path, file_name, file_extension.upper(),
                            os.path.getsize(uploads.path(abs_file_path)))
