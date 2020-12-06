import json
import pandas as pd
from os import walk
from api_pandas import ApiPandas
from stats.statistics import RunData

INITIAL_CAPITAL = 1000

class Backtest():
    def __init__(self, symbol, strategy, intraday=False):
        self.symbol = symbol
        self.api = ApiPandas(self.symbol, intraday)
        self.strategy = strategy
        self.stats = RunData()

        self.current_capital = INITIAL_CAPITAL
        self.nb_positions = 0
        self.current_stop_loss = None
        self.current_take_gain = None
        self.current_trailing = None
        self.current_entry_price = None

        self.run()


    def check_entry(self, data):
        return self.strategy.check_for_entry_signal(data) and\
            (self.current_capital > 0 and self.nb_positions == 0)


    def check_exit(self, data):
        return self.nb_positions > 0 and\
            self.strategy.check_for_exit_signal(
                data, self.strategy.get_stop_loss(data['Adj Close'], self.current_entry_price))


    def update_capital(self, date, move):
        self.stats.capital = self.stats.capital.append({ 'date': date, 'capital': self.current_capital + move }, ignore_index=True)


    def run(self):
        for date, row in self.api.df.iterrows():
            if self.nb_positions < 0 or self.current_capital < 0:
                raise ValueError(f'Problem with state. \nnb_positions: {self.nb_positions}\ncurrent_capital: {self.current_capital}')

            stats = {'date': date, 'price': row['Adj Close']}

            if self.check_entry(row):
                perc_capital = self.current_capital * self.strategy.position_size
                qty = int(round(perc_capital / row['Adj Close'], 0))
                if qty > 0:
                    self.stats.entries = self.stats.entries.append(stats, ignore_index=True)
                    price = qty * row['Adj Close']
                    self.current_capital -= price
                    self.nb_positions = qty
                    self.current_entry_price = row['Adj Close']

            elif self.check_exit(row):
                stats['profit'] = row['Adj Close'] * self.nb_positions - self.current_entry_price - self.nb_positions
                self.stats.exits = self.stats.exits.append(stats, ignore_index=True)
                self.current_capital += row['Adj Close'] * self.nb_positions
                if row['Adj Close'] < self.current_entry_price:
                    self.stats.nb_loss += 1
                else:
                    self.stats.nb_wins += 1
                self.nb_positions = 0
                self.current_entry_price = None

            self.update_capital(date, self.nb_positions * row['Adj Close'])
            print(f'{self.symbol} | {date} | {round(self.current_capital, 2)}')

        self.stats.save_run(self.symbol, self.strategy.id, self.api.df)



class Launcher:
    def __init__(self, strategy=None, symbol=None, intraday=False):
        self.intraday = intraday
        if strategy and symbol:
            Backtest(symbol, strategy, self.intraday)
        else:

            if strategy:
                self.strategy = strategy
                self.symbols = self.get_all_symbols()
                self.test_all_symbols()

            elif symbol:
                print(symbol)
                self.symbol = symbol
                self.strategies = self.get_all_strategies()
                self.test_all_strategies()

            else:
                self.symbols = self.get_all_symbols()
                self.strategies = self.get_all_strategies()
                self.test_all()


    def get_all_strategies(self):
        with open('strategies.json', 'r') as strategies_file:
            strategies = strategies_file.read()
        strategies_obj = json.loads(strategies)
        return [strategy['id'] for strategy in strategies_obj]


    def get_all_symbols(self):
        f = []
        for (dirpath, dirnames, filenames) in walk('data'):
            f.extend(filenames)
            break
        return [symbol[:-4] for symbol in f]


    def test_all_strategies(self):
        for id in self.strategies:
            Backtest(self.symbol, id, self.intraday)


    def test_all_symbols(self):
        for symbol in self.symbols:
            Backtest(symbol, self.strategy, self.intraday)


    def test_all(self):
        for symbol in self.symbols:
            for strategy in self.strategies:
                Backtest(symbol, strategy, self.intraday)
