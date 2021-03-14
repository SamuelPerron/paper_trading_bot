from flask import Blueprint, abort
from .. import app
from ..base.utils import get_current_account
from .models import Account

accounts_blueprint = Blueprint('account', __name__)

@accounts_blueprint.route('/')
def account():
    account = get_current_account()

    if account:
        return account.json()

    return abort(404)