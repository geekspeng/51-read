# -*- coding: utf-8 -*-
# @Time    : 2018/6/7
# @Author  : geekspeng
# @Email   : geekspeng@icloud.com
import os
from shutil import move

from flask import render_template, url_for, redirect, request, flash, current_app, send_from_directory
from flask_login import login_required, current_user
from flask_uploads import extension
from markupsafe import Markup

from app import uploads
from app.main import main
from app.main.forms import ConvertBookForm
from app.models.books import Books, Data
from app.utils import book_format, helper
from app.utils.email import send_book


@main.route("/", defaults={'page': 1})
@main.route('/page/<int:page>')
@login_required
def index(page):
    pagination = Books.get_books_pagination(page=page, per_page=current_app.config['BOOKS_PER_PAGE'], db_filter=True,
                                            order=Books.timestamp.desc())
    books = pagination.items
    return render_template('main/index.html', books=books, pagination=pagination, title="Home")


@main.route("/search", methods=["GET"])
@login_required
def search():
    term = request.args.get("query").strip().lower()
    books = []
    if term:
        books = Books.search_book(term)
    return render_template('main/index.html', books=books, pagination=None, title="Results")


@main.route("/upload", methods=["POST"])
@login_required
def upload():
    for file in request.files.getlist('btn-upload'):
        if not uploads.extension_allowed(extension(file.filename)):
            flash(Markup('File extension "%s" is not allowed to be uploaded to this server' % extension(file.filename)),
                  "warning")
            return redirect(url_for('main.index'))

        # save file
        file_name, file_extension = os.path.splitext(file.filename)
        folder = os.path.join(current_user.email, file_name)
        file_path = helper.resolve_folder_conflict(current_app.config['UPLOAD_FOLDER'], folder)
        saved_file_name = uploads.save(file, folder=file_path, name=file.filename)

        # get book meta
        meta = book_format.process(uploads.path(saved_file_name), file_path, file_name, file_extension[1:])

        # move file
        if meta.title != meta.file_name:
            new_file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file_path,
                                         meta.title + file_extension)
            move(uploads.path(saved_file_name), new_file_path)
            if meta.cover_path:
                new_cover_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file_path,
                                              meta.title + '.jpg')
                move(meta.cover_path, new_cover_path)

        # add book
        Books.add_book(meta)
    flash(Markup('File upload completed.'), "info")
    return redirect(url_for('main.index'))


@main.route("/delete/<int:book_id>/")
@login_required
def delete_book(book_id):
    Books.delete_book(book_id)
    flash(Markup('Book successfully deleted'), "info")
    return redirect(url_for('main.index'))


@main.route('/send/<int:book_id>')
@login_required
def send_to_kindle(book_id):
    if current_user.kindle_email:
        book = Books.query.get_or_404(book_id)
        res = send_book(current_user, book)
        if res:
            flash(Markup(res), "warning")
        else:
            flash(Markup("Book successfully queued for sending to %s" % current_user.kindle_mail), "success")
    else:
        flash(Markup("Please configure your kindle e-mail address first..."), "error")
        return redirect(url_for('auth.change_kindle_email'))
    return redirect(url_for('main.index'))


@main.route("/book/convert/<int:book_id>", methods=['GET', 'POST'])
@login_required
def convert_book(book_id):
    book = Books.query.get_or_404(book_id)
    form = ConvertBookForm(book)
    if form.validate_on_submit():
        book_format_from = form.convert_from.data
        book_format_to = form.convert_to.data
        if current_app.config['CONVERT_TOOL_PATH'] is None:
            flash(Markup("ebook-converter failed, there is no conversion tool"), "success")
            return redirect(url_for('main.index'))
        result = Books.convert_book_format(book_id, current_app.config['CONVERT_TOOL_PATH'], book_format_from.upper(),
                                           book_format_to.upper())
        if result is None:
            flash(Markup("Book successfully converted"), "success")
            return redirect(url_for('main.index'))
        else:
            flash(Markup("There was an error converting this book: %s" % result), "error")
    return render_template('main/convert_book.html', title='Convert Book', book=book, form=form)


@main.route("/read/<file_format>/<int:book_id>")
@login_required
def read_book(file_format, book_id):
    book = Books.query.get_or_404(book_id)
    file_name = book.title + '.' + file_format.lower()
    if file_format.lower() == "pdf":
        return render_template('main/readpdf.html', book_id=book_id, file_name=file_name)
    elif file_format.lower() == "txt":
        return render_template('main/readtxt.html', book_id=book_id, file_name=file_name)
    elif file_format.lower() == "epub":
        return render_template('main/readepub.html', book_id=book_id, file_name=file_name)


@main.route("/book/<int:book_id>/<file_name>")
@login_required
def get_book(book_id, file_name):
    book = Books.query.get_or_404(book_id)
    file_path = os.path.join(book.path, file_name)
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], file_path)


@main.route("/cover/<int:book_id>")
@login_required
def get_cover(book_id):
    book = Books.query.get_or_404(book_id)
    cover_path = os.path.join(book.path, book.title + '.jpg')
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], cover_path)