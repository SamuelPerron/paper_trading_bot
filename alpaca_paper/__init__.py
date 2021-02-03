from alpaca_paper.dotenv import API_KEY, API_SECRET
import requests

class Alpaca:
    base_url = 'https://paper-api.alpaca.markets/v2'
    market_base_url = 'https://data.alpaca.markets/v1'


    def api(self, method, url, params={}, data={}):
        headers = {
            'APCA-API-KEY-ID': API_KEY,
            'APCA-API-SECRET-KEY': API_SECRET
        }
        base_url = self.base_url
        if 'bars' in url:
            base_url = self.market_base_url
        request = f'requests.{method}("{base_url}/{url}", headers={headers}, params={params}, json={data},)'
        return eval(request)


    def clock(self):
        return self.api('get', 'clock').json()


    def account(self):
        return self.api('get', 'account').json()


    def orders(self, id=None, filters={}, cancel=False):
        possible_filters = (
            'status', 'limit', 'after', 
            'until', 'direction', 'nested', 'symbols'
        )
        for ftr in filters:
            if ftr not in possible_filters:
                raise ValueError(f'`{ftr}` is not an acceptable filter.')
        
        if id and filters != {}:
            raise ValueError('Can\'t filter when getting a specific order.')

        url = 'orders'
        if id:
            url += f'/{id}'

        method = 'get'
        if cancel:
            method = 'delete'

        return self.api(method, url, filters).json()


    def new_order(self, details):
        details.update({'time_in_force': 'day'})
        required_fields = ('symbol', 'qty', 'side', 'type')

        type = details.get('type')
        if type in ('limit', 'stop_limit'):
            required_fields.append('limit_price')
        if type in ('stop', 'stop_limit', 'trailing_stop'):
            required_fields.append('stop_price')

        for field in required_fields:
            if not details.get(field):
                raise ValueError(f'`{field}` is required.')

        return self.api('post', 'orders', data=details).json()


    def positions(self, symbol=None, close=False):
        method = 'get'
        if close:
            method = 'DELETE'
        
        url = 'positions'
        if symbol:
            url += f'/{symbol}'

        return self.api(method, url).json()


    def bars(self, symbols, limit, timeframe='5Min'):
        params = {
            'symbols': ','.join(symbols),
            'limit': limit,
        }
        return self.api('get', f'bars/{timeframe}', params=params).json()


    def __str__(self):
        id = self.account()['id']
        return f'Alpaca <id: {id}>'
