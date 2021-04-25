from flask_testing import TestCase
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

from ..import create_app, db


class BaseTestCase(TestCase):
    def create_app(self):
        app = create_app('testing')
        self.db = db
        
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()