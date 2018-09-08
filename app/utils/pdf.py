# -*- coding: utf-8 -*-
# @Time    : 2018/9/8 14:48
# @Author  : geekspeng
# @Email   : geekspeng@icloud.com
import os

from PyPDF2 import PdfFileReader

from app.utils.book_meta import BookMeta


def get_pdf_meta(abs_file_path, file_path, file_name, file_extension):
    pdf = PdfFileReader(open(abs_file_path, 'rb'))
    doc_info = pdf.getDocumentInfo()

    if doc_info is not None:
        author = doc_info.author if doc_info.author else "Unknown"
        title = doc_info.title if doc_info.title else file_name
        subject = doc_info.subject
    else:
        author = "Unknown"
        title = file_name
        subject = ""

    return BookMeta(
        title=title,
        author=author,
        cover_path="",
        description=subject,
        tags="",
        series="",
        series_id="",
        languages="",
        file_path=file_path,
        file_name=file_name,
        file_extension=file_extension,
        file_size=os.path.getsize(abs_file_path))

