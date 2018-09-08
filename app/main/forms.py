# -*- coding: utf-8 -*-
# @Time    : 2018/8/29 17:52
# @Author  : geekspeng
# @Email   : geekspeng@icloud.com
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired, ValidationError


class ConvertBookForm(FlaskForm):
    convert_from = SelectField('Convert from', validators=[DataRequired()], coerce=str)
    convert_to = SelectField('Convert to', validators=[DataRequired()], coerce=str)
    submit = SubmitField('Convert Book')

    def __init__(self, book, *args, **kwargs):
        super(ConvertBookForm, self).__init__(*args, **kwargs)
        self.convert_from.choices = [(data.format.lower(), data.format.lower()) for data in book.data]
        self.convert_to.choices = [('azw3', 'azw3'), ('mobi', 'mobi'), ('epub', 'epub'), ('fb2', 'fb2'), ('pdf', 'pdf'),
                                   ('docx', 'docx'), ('txt', 'txt')]

    def validate_convert_to(self, field):
        if self.convert_from.data == field.data:
            raise ValidationError('Book format cannot be the same')
