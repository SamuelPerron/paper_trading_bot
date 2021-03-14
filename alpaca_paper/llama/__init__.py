from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import os
import redis
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

CORS(app)

redis_obj = redis.StrictRedis(host='redis', port=6379, db=0)

db = SQLAlchemy(app)
db.init_app(app)
migrate = Migrate(app, db)

# --- ENV variables --- #
ACCOUNT_ID = os.getenv('ACCOUNT_ID')
ALPACA_UID = os.getenv('ALPACA_UID')
ALPACA_SECRET = os.getenv('ALPACA_SECRET')


# --- App imports --- #
from .account import accounts_blueprint, Account
app.register_blueprint(accounts_blueprint, url_prefix='/account')

from .position import positions_blueprint, Position
app.register_blueprint(positions_blueprint, url_prefix='/positions')