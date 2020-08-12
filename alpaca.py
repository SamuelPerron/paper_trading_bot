import alpaca_trade_api as tradeapi
from datetime import datetime
from bs4 import BeautifulSoup
import requests


class Alpaca:
    def __init__(self, key, secret, timeframe):
        self.distant = tradeapi.REST(
            key,
            secret,
            base_url='https://paper-api.alpaca.markets'
        )
        self.timeframe = timeframe
        self.max_nb_positions = 5


    def are_markets_open(self):
        is_open = False
        now = datetime.now()
        if now.hour >= 9 and now.hour < 16:
            if now.hour == 9 and now.minutes < 30:
                return False
            is_open = self.distant.get_clock().is_open
        return is_open


    def get(self, symbol):
        return self.distant.get_last_quote(symbol)


    def positions(self):
        return self.distant.list_positions()


    def in_positions(self, symbol):
        return symbol in [p.symbol for p in self.positions()]


    def capital(self):
        return float(self.distant.get_account().buying_power)


    def fetch_pre_market(self):
        symbols = []
        positions = self.positions()

        headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0'}
        r = requests.get('https://thestockmarketwatch.com/markets/pre-market/today.aspx', headers=headers)
        if r.status_code == 200:
            s = BeautifulSoup(r.text, 'html.parser')
            table = s.find('table', {'id': 'tblMoversDesktop'})
            rows = table.find_all('tr')
            rows.pop(0)
            for row in rows:
                if len(symbols) <= self.max_nb_positions - len(positions):
                    volume = int(row.find('td', {'class': 'tdVolume'}).text)
                    if volume >= 10000:
                        symbols.append({
                            's': row.find('a', {'class': 'symbol'}).text, # Symbol
                            'p': row.find('div', {'class': 'lastPrice'}).text, # Last price
                            'c': row.find('div', {'class': 'chgUp'}).text, # Change percentage
                            'v': volume, # Volume
                        })

            for position in positions:
                q = self.get(position.symbol)
                symbols.append({
                    's': position.symbol,
                    'p': f'${q.askprice}',
                    'c': '-',
                    'v': '-',
                })

        return symbols


    def get_account(self):
        account = self.distant.get_account()
        return {
            'capital': account.portfolio_value,
            'cash': account.cash,
            'positions_value': sum([float(p.market_value) for p in self.positions()]),
            'today_pl': round(float(account.equity) - float(account.last_equity), 2),
            'nb_positions': len(self.positions()),
        }


    def buy(self, symbol, qty, take_profit, stop_loss):
        self.distant.submit_order(
            symbol=symbol,
            side='buy',
            type='market',
            qty=qty,
            time_in_force='day',
            order_class='bracket',
            take_profit=take_profit,
            stop_loss=stop_loss
        )
        print(f"{datetime.now().strftime('%H:%M:%S')} | LONG | {symbol} x{qty}")


    def sell(self, symbol, limit_price, qty):
        self.distant.submit_order(
            symbol=symbol,
            side='sell',
            type='limit',
            qty=qty,
            time_in_force='day',
            limit_price=limit_price
        )
        print(f"{datetime.now().strftime('%H:%M:%S')} | SELL | {symbol} x{qty}")


    def compute(self, symbol):
        result = self.distant.get_barset(symbol, self.timeframe, 200)[symbol]
        last = result[-1]
        return {
            'timestamp': last.t,
            'symbol': symbol,
            'open': last.o,
            'close': last.c,
            'volume': last.v,
            '5_avg': self.period_avg(result, 5),
            '10_avg': self.period_avg(result, 10),
            '50_avg': self.period_avg(result, 50),
            '200_avg': self.period_avg(result, 200),
            'rsi': self.rsi(result, last),
        }


    def period_avg(self, data, nb):
        trunc = data[-nb:]
        avg_list = [bar.c for bar in trunc]
        return sum(avg_list) / len(avg_list)


    def rsi(self, data, last):
        period = 14
        diffs = self.closing_diff(period, data)

        avg_pos_list = [n for n in diffs if n >= 0]
        avg_neg_list = [n for n in diffs if n < 0]
        if len(avg_pos_list) == 0:
            return 0
        elif len(avg_neg_list) == 0:
            return 100
        avg_pos = sum(avg_pos_list) / len(avg_pos_list)
        avg_neg = abs(sum(avg_neg_list) / len(avg_neg_list))

        current = self.closing_diff(1, data)[0]
        current_pos = 0
        current_neg = 0
        if current > 0:
            current_pos = current
        else:
            current_neg = current

        calc = 100 - abs(
            100 / (
                1 + (
                    (avg_pos * 13 + current_pos) / (avg_neg * 13 + current_neg)
                )
            )
        )

        return calc


    def closing_diff(self, nb_days, data):
        trunc = data[-nb_days:]
        return [
            ((bar.c - bar.o) / bar.o) * 100
            for bar in trunc
        ]
