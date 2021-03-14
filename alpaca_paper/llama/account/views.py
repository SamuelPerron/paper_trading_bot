from flask import Blueprint
from .. import app, ACCOUNT_ID
from .models import Account

accounts_blueprint = Blueprint('account', __name__)

@accounts_blueprint.route('/')
def account():
    account = Account.query.filter_by(id=ACCOUNT_ID).first()
    return account.json()