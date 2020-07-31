import alpaca_trade_api as tradeapi
from datetime import datetime


class Alpaca:
    def __init__(self, key, secret, timeframe):
        self.distant = tradeapi.REST(
            key,
            secret,
            base_url='https://paper-api.alpaca.markets'
        )
        self.timeframe = timeframe


    def are_markets_open(self):
        return self.distant.get_clock().is_open


    def get(self, symbol):
        return self.distant.get_last_quote(symbol)


    def positions(self):
        return self.distant.list_positions()


    def in_positions(self, symbol):
        return symbol in [p.symbol for p in self.positions()]


    def capital(self):
        return float(self.distant.get_account().buying_power)


    def get_account(self):
        account = self.distant.get_account()
        return {
            'capital': account.portfolio_value,
            'cash': account.cash,
            'positions_value': sum([float(p.market_value) for p in self.positions()]),
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
