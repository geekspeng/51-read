# -*- coding: utf-8 -*-
# @Time    : 2018/8/30 16:00
# @Author  : geekspeng
# @Email   : geekspeng@icloud.com
import unittest
from app import create_app, db
from app.models.users import Users
from config import TestingConfig


class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_check_password(self):
        u = Users(email='your-email@example.com')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))
