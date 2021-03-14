from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import os
import redis
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:example@db:5432/llama'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

CORS(app)

redis_obj = redis.StrictRedis(host='redis', port=6379, db=0)

db = SQLAlchemy(app)
db.init_app(app)
migrate = Migrate(app, db)

ACCOUNT_ID = 1


# --- Base models --- #
class BaseDBModel():
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    soft_deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def json(self):
        return {
            'id': self.id
        }

    def delete(self):
        self.soft_deleted = True
        db.session.commit()

    def save_to_db(self):
        now = datetime.now()
        if not self.id:
            self.created_at = now
        
        self.updated_at = now
        db.session.add(self)
        db.session.commit()


# --- App imports --- #
from .account import accounts_blueprint, Account
app.register_blueprint(accounts_blueprint, url_prefix='/account')

from .position import positions_blueprint, Position
app.register_blueprint(positions_blueprint, url_prefix='/positions')