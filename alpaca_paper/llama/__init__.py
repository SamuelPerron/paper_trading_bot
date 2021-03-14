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


# --- App imports --- #
from .account import accounts_blueprint, Account
app.register_blueprint(accounts_blueprint, url_prefix='/account')

from .position import positions_blueprint, Position
app.register_blueprint(positions_blueprint, url_prefix='/positions')