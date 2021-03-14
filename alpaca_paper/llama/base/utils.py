from .. import ACCOUNT_ID


def get_current_account():
    from ..account import Account

    return Account.query.filter_by(id=ACCOUNT_ID).first()