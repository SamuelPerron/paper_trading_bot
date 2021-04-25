from flask import Blueprint, abort
from ..base.utils import get_current_account
from ..base.responses import DetailsHttpResponse
from .models import Account
from .serializers import AccountSerializer

accounts_blueprint = Blueprint('account', __name__)

@accounts_blueprint.route('/')
def account():
    account = get_current_account()
    if account:
        return DetailsHttpResponse(account, AccountSerializer).json()

    return abort(404)