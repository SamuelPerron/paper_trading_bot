from alpaca_paper.strategies import Strategy
from alpaca_paper.screeners import MarketWatch


class MACD(Strategy):
    def __init__(self):
        self.name = 'MACD'
        self.position_size = 0.15
        self.stop_loss = 0.025
        self.take_profit = 0.02


    def check_for_entry_signal(self, data, *args, **kwargs):
        return data['MACD'] > data['MACD Signal']


    def find_next_symbols(self):
        mw = MarketWatch()
        return [symbol['symbol'] for symbol in mw.pre_market()['most_actives']]


    def find_qty(self, price, buying_power):
        perc_capital = buying_power * self.position_size
        return int(round(perc_capital / price, 0))


    def find_take_profit(self, price):
        return price * (1 + self.take_profit)


    def find_stop_loss(self, price):
        return price * (1 - self.stop_loss)


strategy = MACD()
        