from alpaca_paper.dotenv import API_KEY, API_SECRET
from alpaca_paper.big_brain import BigBrain
import requests


class API:
    def __init__(self):
        """
        This should implement a base_url for trading calls
        and data_url for market data.
        """
        raise NotImplementedError()

    def api(self):
        """
        This should implement the basic API calls that will
        be used throughout the implementations of the API.

        Params
            method => str
            url    => str
            params => { param: str(VALUE) }
            data   => { }
        """
        raise NotImplementedError()

    def clock(self):
        """ 
        This should primarily return if the markets are opened.

        Expected return format
            {
                "is_open": bool,
                "next_open": datetime(%Y-%m-%dT%H:%M:%S),
                "next_close": datetime(%Y-%m-%dT%H:%M:%S)
            }
        """
        raise NotImplementedError()

    def account(self):
        """ 
        This should return the current account information.

        Expected return format
            {
                "id": int or str,
                "buying_power": float or str,
                "equity": float or str
            }
        """
        raise NotImplementedError()

    def positions_as_symbols(self):
        """ 
        This should return a list of all the symbols currently held.

        Expected return format
            [
                str(SYMBOL)
            ]
        """
        raise NotImplementedError()

    def orders(self):
        """ 
        This should return the orders linked to the current portfolio.
        This can return a specific order by passing the order id.
        This can return filtered orders by passing filters.
        This can cancel an order by passing cancel to True.

        Params
            id      => int 
            filters => { filter_name: str(VALUE) } 
            cancel  => bool

        Expected return format
            [
                Order()
            ]
        """
        raise NotImplementedError()

    def new_order(self):
        """ 
        This should be used to send new orders to the distant API.

        Params
            details => { }

        Expected return format
            Order()
        """
        raise NotImplementedError()
    
    def positions(self):
        """ 
        This should return all currently held positions.
        By passing close to True, it is expected to liquidate all positions.
        By passing close to True and a symbol, it is expected to close
        this particular position.

        Params
            symbol => str
            close  => bool

        Expected return format
            [
                Position()
            ]
        """
        raise NotImplementedError()

    def bars(self):
        """ 
        This should return market data. Symbols should always be passed
        to fetch the relevent information. 
        The timeframe is the period by which the data should be split. 
        (1Min, 5Min, day, week, ...)
        The limit is how many periods should be retreived.
        big_brain should be set to True if we want to have the data computed
        with metrics like (RSI, MACS, EMA, ...).

        Params
            symbols   => [ str ]
            timeframe => str
            limit     => int
            big_brain => bool

        Expected return format
            {
                str(SYMBOL): [
                    {
                        "o": float(OPEN PRICE),
                        "h": float(HIGH PRICE),
                        "l": float(LOW PRICE),
                        "c": float(CLOSE PRICE),
                        "v": float(VOLUME)
                    }
                ]
            }
        """
        raise NotImplementedError()

    def __str__(self):
        """ 
        This should return a good identifier for the API.

        Expected return format
            '{Name} <{account_id}>'
        """
        raise NotImplementedError()


class Alpaca(API):
    def __init__(self):
        self.base_url = 'https://paper-api.alpaca.markets/v2'
        self.data_base_url = 'https://data.alpaca.markets/v1'


    def api(self, method, url, params={}, data={}):
        headers = {
            'APCA-API-KEY-ID': API_KEY,
            'APCA-API-SECRET-KEY': API_SECRET
        }
        base_url = self.base_url
        if 'bars' in url:
            base_url = self.data_base_url
        request = f'requests.{method}("{base_url}/{url}", headers={headers}, params={params}, json={data},)'
        executed_request = eval(request)

        if str(executed_request.status_code)[0] != '2':
            print(f'ERROR --- {executed_request.json()}')
            # TODO: Log complete error w/ context in file
        return executed_request


    def clock(self):
        return self.api('get', 'clock').json()


    def account(self):
        return self.api('get', 'account').json()

    
    def positions_as_symbols(self):
        return [position['symbol'] for position in self.positions()]


    def orders(self, id=None, filters={}, cancel=False):
        possible_filters = (
            'status', 'limit', 'after', 
            'until', 'direction', 'nested', 'symbols'
        )
        for ftr in filters.keys():
            if ftr not in possible_filters:
                print(f'ERROR --- `{ftr}` is not an acceptable filter.')
        
        if id and filters != {}:
            print(f'ERROR --- Can\'t filter when getting a specific order.')

        url = 'orders'
        if id:
            url += f'/{id}'

        method = 'get'
        if cancel:
            method = 'delete'

        return self.api(method, url, filters).json()


    def new_order(self, details):
        details.update({'time_in_force': 'gtc'})
        required_fields = ('symbol', 'qty', 'side', 'type')

        type = details.get('type')
        if type in ('limit', 'stop_limit'):
            required_fields.append('limit_price')
        if type in ('stop', 'stop_limit', 'trailing_stop'):
            required_fields.append('stop_price')

        for field in required_fields:
            if not details.get(field):
                print(f'ERROR --- `{field}` is required.')

        return self.api('post', 'orders', data=details).json()


    def positions(self, symbol=None, close=False):
        method = 'get'
        if close:
            method = 'delete'
        
        url = 'positions'
        if symbol:
            url += f'/{symbol}'

        return self.api(method, url).json()


    def bars(self, symbols, timeframe, limit=200, big_brain=False):
        params = {
            'symbols': ','.join(symbols),
            'limit': limit,
        }

        response = self.api('get', f'bars/{timeframe}', params=params)
        if big_brain and response.status_code == 200:
            data = response.json()
            return [BigBrain(symbol=symbol, data=data[symbol]) for symbol in data.keys()]
        return response.json()


    def __str__(self):
        id = self.account()['id']
        return f'Alpaca <id: {id}>'
