# -*- coding: utf-8 -*-
# @Time    : 2018/9/8 22:20
# @Author  : geekspeng
# @Email   : geekspeng@icloud.com
import os
from datetime import datetime

from iso639 import languages as isoLanguages
from markupsafe import Markup

from app import db, uploads
from app.utils import helper

books_authors_link = db.Table(
    'books_authors_link',
    db.Column('book', db.Integer, db.ForeignKey('books.id'), primary_key=True),
    db.Column('author', db.Integer, db.ForeignKey('authors.id'), primary_key=True)
)

books_tags_link = db.Table(
    'books_tags_link',
    db.Column('book', db.Integer, db.ForeignKey('books.id'), primary_key=True),
    db.Column('tag', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)

books_series_link = db.Table(
    'books_series_link',
    db.Column('book', db.Integer, db.ForeignKey('books.id'), primary_key=True),
    db.Column('series', db.Integer, db.ForeignKey('series.id'), primary_key=True)
)

books_ratings_link = db.Table(
    'books_ratings_link',
    db.Column('book', db.Integer, db.ForeignKey('books.id'), primary_key=True),
    db.Column('rating', db.Integer, db.ForeignKey('ratings.id'), primary_key=True)
)

books_languages_link = db.Table(
    'books_languages_link',
    db.Column('book', db.Integer, db.ForeignKey('books.id'), primary_key=True),
    db.Column('lang_code', db.Integer, db.ForeignKey('languages.id'), primary_key=True)
)

books_publishers_link = db.Table(
    'books_publishers_link',
    db.Column('book', db.Integer, db.ForeignKey('books.id'), primary_key=True),
    db.Column('publisher', db.Integer, db.ForeignKey('publishers.id'), primary_key=True)
)


class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book = db.Column(db.Integer, db.ForeignKey('books.id'))
    text = db.Column(db.String(64))

    def __repr__(self):
        return "<Comments({0})>".format(self.text)


class Authors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    sort = db.Column(db.String(128))
    link = db.Column(db.String(128), default='')

    def __repr__(self):
        return "<Authors('{0},{1}{2}')>".format(self.name, self.sort, self.link)

    @staticmethod
    def get_author_by_name(name):
        return Authors.query.filter_by(name=name).first()

    @staticmethod
    def add_author(name):
        db_author = Authors.get_author_by_name(name)
        if not db_author:
            db_author = Authors(name=name, sort=helper.get_sorted_author(name))
            db.session.add(db_author)
            db.session.commit()


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book = db.Column(db.Integer, db.ForeignKey('books.id'))
    format = db.Column(db.String(20))
    uncompressed_size = db.Column(db.Integer)
    name = db.Column(db.String(128))

    def __repr__(self):
        return "<Data('{0},{1}{2}{3}')>".format(self.book, self.format, self.uncompressed_size, self.name)

    @staticmethod
    def get_data_by_format(file_format):
        return Data.query.filter_by(format=file_format).first()


class Identifiers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(128))
    val = db.Column(db.String(128))
    book = db.Column(db.Integer, db.ForeignKey('books.id'))

    def format_type(self):
        if self.type == "amazon":
            return "Amazon"
        elif self.type == "isbn":
            return "ISBN"
        elif self.type == "doi":
            return "DOI"
        elif self.type == "goodreads":
            return "Goodreads"
        elif self.type == "google":
            return "Google Books"
        elif self.type == "kobo":
            return "Kobo"
        else:
            return self.type

    def __repr__(self):
        if self.type == "amazon":
            return "https://amzn.com/{0}".format(self.val)
        elif self.type == "isbn":
            return "http://www.worldcat.org/isbn/{0}".format(self.val)
        elif self.type == "doi":
            return "http://dx.doi.org/{0}".format(self.val)
        elif self.type == "goodreads":
            return "http://www.goodreads.com/book/show/{0}".format(self.val)
        elif self.type == "douban":
            return "https://book.douban.com/subject/{0}".format(self.val)
        elif self.type == "google":
            return "https://books.google.com/books?id={0}".format(self.val)
        elif self.type == "kobo":
            return "https://www.kobo.com/ebook/{0}".format(self.val)
        else:
            return ""


class Languages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lang_code = db.Column(db.String(20))

    def __repr__(self):
        return "<Languages('{0}')>".format(self.lang_code)

    @staticmethod
    def get_language_by_code(lang_code):
        return Languages.query.filter_by(lang_code=lang_code).first()

    @staticmethod
    def add_language(lang_code):
        db_language = Languages.get_language_by_code(lang_code)
        if not db_language:
            db_language = Languages(lang_code=lang_code)
            db.session.add(db_language)
            db.session.commit()


class Publishers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    sort = db.Column(db.String(128))

    def __repr__(self):
        return "<Publishers('{0},{1}')>".format(self.name, self.sort)


class Ratings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)

    def __repr__(self):
        return "<Ratings('{0}')>".format(self.rating)


class Series(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    sort = db.Column(db.String(128), default='')

    def __repr__(self):
        return u"<Series('{0},{1}')>".format(self.name, self.sort)

    @staticmethod
    def get_series_by_name(name):
        return Series.query.filter_by(name=name).first()

    @staticmethod
    def add_series(name):
        db_series = Series.get_series_by_name(name)
        if not db_series:
            db_series = Series(name=name)
            db.session.add(db_series)
            db.session.commit()


class Tags(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32))

    def __repr__(self):
        return "<Tags('{0})>".format(self.name)

    @staticmethod
    def get_tag_by_name(name):
        return Tags.query.filter_by(name=name).first()

    @staticmethod
    def add_tag(name):
        db_tag = Tags.get_tag_by_name(name=name)
        if not db_tag:
            db_tag = Tags(name)
            db.session.add(db_tag)
            db.session.commit()


class Books(db.Model):
    DEFAULT_PUBDATE = "0101-01-01 00:00:00+00:00"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    sort = db.Column(db.String(128), default='')
    author_sort = db.Column(db.String(128))
    timestamp = db.Column(db.String(128), default=datetime.utcnow)
    pubdate = db.Column(db.String(128), default=datetime(101, 1, 1))
    series_index = db.Column(db.String(128))
    last_modified = db.Column(db.String(128), default=datetime.utcnow)
    path = db.Column(db.String(128))
    has_cover = db.Column(db.Boolean,  default=False)
    uuid = db.Column(db.String(128))

    authors = db.relationship('Authors', secondary=books_authors_link, backref='books')
    tags = db.relationship('Tags', secondary=books_tags_link, backref='books')
    comments = db.relationship('Comments', backref='books')
    data = db.relationship('Data', backref='books')
    series = db.relationship('Series', secondary=books_series_link, backref='books')
    ratings = db.relationship('Ratings', secondary=books_ratings_link, backref='books')
    languages = db.relationship('Languages', secondary=books_languages_link, backref='books')
    publishers = db.relationship('Publishers', secondary=books_publishers_link, backref='books')
    identifiers = db.relationship('Identifiers', backref='books')

    def __repr__(self):
        return "<Books('{0},{1}{2}{3}{4}{5}{6}{7}{8}')>".format(self.title, self.sort, self.author_sort,
                                                                self.timestamp, self.pubdate, self.series_index,
                                                                self.last_modified, self.path, self.cover_path)

    @property
    def atom_timestamp(self):
        return (self.timestamp or '').replace(' ', 'T')

    @staticmethod
    def delete_book(book_id):
        db_book = Books.query.filter_by(id=book_id).first()
        if db_book:
            file_path = uploads.path(db_book.path)
            # delete readbook
            ReadBook.query.filter_by(book_id=book_id).delete()
            # delete author
            for author in db_book.authors:
                db_book.authors.remove(author)
                if len(author.books) == 0:
                    db.session.delete(author)
            # delete tag
            for tag in db_book.tags:
                db_book.tags.remove(tag)
                if len(tag.books) == 0:
                    db.session.delete(tag)
            # delete series
            for series in db_book.series:
                db_book.series.remove(series)
                if len(series.books) == 0:
                    db.session.delete(series)
            # delete language
            for language in db_book.languages:
                db_book.languages.remove(language)
                if len(language.books) == 0:
                    db.session.delete(language)
            # delete publisher
            for publisher in db_book.publishers:
                db_book.publishers.remove(publisher)
                if len(publisher.books) == 0:
                    db.session.delete(publisher)
            # delete data
            for data in db_book.data:
                db_book.data.remove(data)
                if data.books is None:
                    db.session.delete(data)
            # delete comment
            for comment in db_book.comments:
                db_book.comments.remove(comment)
                if comment.books is None:
                    db.session.delete(comment)
            db.session.delete(db_book)
            db.session.commit()
            helper.delete_book(file_path)

    @staticmethod
    def add_book(meta):
        # add book
        has_cover = True if meta.cover_path else False
        db_book = Books(title=meta.title, author_sort=helper.get_sorted_author(meta.author),
                        series_index=meta.series_id, path=meta.file_path, has_cover=has_cover)
        # add author
        if meta.author != "":
            db_author = Authors.get_author_by_name(meta.author)
            if not db_author:
                db_author = Authors(name=meta.author, sort=helper.get_sorted_author(meta.author))
                db.session.add(db_author)
            db_book.authors.append(db_author)
        # add series
        if meta.series != "":
            db_series = Series.get_series_by_name(meta.series)
            if not db_series:
                db_series = Series(name=meta.series)
                db.session.add(db_series)
            db_book.series.append(db_series)
        # add language
        if meta.languages != "":
            lang_code = isoLanguages.get(name=meta.languages).part3
            db_language = Languages.get_language_by_code(lang_code)
            if not db_language:
                db_language = Languages(lang_code=lang_code)
                db.session.add(db_language)
            db_book.languages.append(db_language)
        # add tag
        if meta.tags != "":
            for tag in meta.tags.split(','):
                db_tag = Tags.get_tag_by_name(name=tag.strip())
                if not db_tag:
                    db_tag = Tags(name=tag.strip())
                    db.session.add(db_tag)
                db_book.tags.append(db_tag)
        # add data
        db_data = Data(books=db_book, format=meta.file_extension,
                       uncompressed_size=meta.file_size, name=meta.title)
        db.session.add(db_data)
        db_book.data.append(db_data)
        # add comment
        upload_comment = Markup(meta.description).unescape()
        if upload_comment != "":
            db_comment = Comments(books=db_book, text=upload_comment)
            db.session.add(db_comment)
            db_book.comments.append(db_comment)
        db.session.add(db_book)
        db.session.commit()
        return db_book

    @staticmethod
    def search_book(term):
        return db.session.query(Books).filter(
            db.or_(Books.tags.any(Tags.name.ilike("%" + term + "%")),
                   Books.series.any(Series.name.ilike("%" + term + "%")),
                   Books.authors.any(Authors.name.ilike("%" + term + "%")),
                   Books.publishers.any(Publishers.name.ilike("%" + term + "%")),
                   Books.title.ilike("%" + term + "%"))).all()

    @staticmethod
    # get the pagination of books from database
    def get_books_pagination(page, per_page, db_filter, order):
        pagination = Books.query.filter(db_filter).order_by(order).paginate(
            page, per_page=per_page, error_out=False)
        return pagination

    # Convert existing book entry to new format
    @staticmethod
    def convert_book_format(book_id, convert_tool_path, old_book_format, new_book_format):
        db_book = Books.query.get(book_id)
        db_data = Data.query.filter_by(book=book_id, format=old_book_format).first()
        if db_book is None or db_data is None:
            return "{format} format not found for this book".format(format=old_book_format)
        old_file_name = db_data.name + '.' + old_book_format.lower()
        new_file_name = db_data.name + '.' + new_book_format.lower()
        old_file_path = uploads.path(old_file_name, db_book.path)
        new_file_path = uploads.path(new_file_name, db_book.path)
        if os.path.isfile(old_file_path):
            if not os.path.isfile(new_file_name):
                result = helper.convert_book(convert_tool_path, old_file_path, new_file_path)
                if result is None:
                    new_format = Data(book=db_book.id, name=db_book.data[0].name, format=new_book_format,
                                      uncompressed_size=os.path.getsize(new_file_path))
                    db_book.data.append(new_format)
                    db.session.commit()
                return result
            else:
                return "{format} format already exists".format(format=new_file_name)
        else:
            return "{format} not found: {fn}".format(format=old_book_format, fn=db_book.title + "." + old_book_format.lower())


class ReadBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), unique=False)
    is_read = db.Column(db.Boolean, unique=False)


class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),  unique=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'),  unique=False)
    format = db.Column(db.String(20))
    bookmark_key = db.Column(db.String(128))
