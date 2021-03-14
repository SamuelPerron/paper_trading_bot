from .. import ACCOUNT_ID, ALPACA_UID, ALPACA_SECRET, ACOUNT_BASE_CASH


def get_current_account():
    from ..account import Account

    account = Account.query.filter_by(id=ACCOUNT_ID).first()
    if not account:
        account = Account(cash=ACOUNT_BASE_CASH)
        account.save_to_db()

    return account


def alpaca(method, url, params={}, data={}):
    base_url = 'https://paper-api.alpaca.markets/v2'
    if 'bars' in url:
        base_url = 'https://data.alpaca.markets/v1'
    
    headers = {
        'APCA-API-KEY-ID': ALPACA_UID,
        'APCA-API-SECRET-KEY': ALPACA_SECRET
    }

    request = f'requests.{method}("{base_url}/{url}", headers={headers}, params={params}, json={data},)'
    executed_request = eval(request)

    if str(executed_request.status_code)[0] != '2':
        print(f'ERROR --- {executed_request.json()}')
        # TODO: Log complete error w/ context in file
    return executed_request


def bars(symbols, timeframe, limit=200):
    params = {
            'symbols': ','.join(symbols),
            'limit': limit,
        }

    response = alpaca('get', f'bars/{timeframe}', params=params)
    return response.json()