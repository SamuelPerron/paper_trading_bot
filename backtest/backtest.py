import json
import matplotlib.pyplot as plt
import pandas as pd
from os import walk
from api_pandas import ApiPandas

INITIAL_CAPITAL = 1000

class Backtest():
    def __init__(self, symbol, strategy, intraday=False):
        self.symbol = symbol
        self.api = ApiPandas(self.symbol, intraday)
        self.entries = pd.DataFrame({ 'date': [], 'price': [] })
        self.exits = pd.DataFrame({ 'date': [], 'price': [] })
        self.capital = pd.DataFrame({ 'date': [], 'capital': [] })
        self.current_capital = INITIAL_CAPITAL
        self.nb_positions = 0
        self.strategy_id = strategy
        self.current_stop_loss = None
        self.current_take_gain = None
        self.current_trailing = None
        self.current_entry_price = None
        self.nb_wins = 0
        self.nb_loss = 0

        self.strategy = strategy

        self.run()


    def find_loc(self, dates):
        marks = []
        for date in dates:
            marks.append(self.api.df.index.get_loc(date))
        return marks


    def check_entry(self, data):
        return self.strategy.check_for_entry_signal(data) and\
            (self.current_capital > 0 and self.nb_positions == 0)


    def check_exit(self, data):
        return self.nb_positions > 0 and\
            self.strategy.check_for_exit_signal(
                data, self.strategy.get_stop_loss(data['Adj Close'], self.current_entry_price))


    def update_capital(self, date, move):
        self.capital = self.capital.append({ 'date': date, 'capital': self.current_capital + move }, ignore_index=True)


    def run(self):
        for date, row in self.api.df.iterrows():
            if self.nb_positions < 0 or self.current_capital < 0:
                raise ValueError(f'Problem with state. \nnb_positions: {self.nb_positions}\ncurrent_capital: {self.current_capital}')

            stats = {'date': date, 'price': row['Adj Close']}

            if self.check_entry(row):
                perc_capital = self.current_capital * self.strategy.position_size
                qty = int(round(perc_capital / row['Adj Close'], 0))
                if qty > 0:
                    self.entries = self.entries.append(stats, ignore_index=True)
                    price = qty * row['Adj Close']
                    self.current_capital -= price
                    self.nb_positions = qty
                    self.current_entry_price = row['Adj Close']

            elif self.check_exit(row):
                self.exits = self.exits.append(stats, ignore_index=True)
                self.current_capital += row['Adj Close'] * self.nb_positions
                if row['Adj Close'] < self.current_entry_price:
                    self.nb_loss += 1
                else:
                    self.nb_wins += 1
                self.nb_positions = 0
                self.current_entry_price = None

            self.update_capital(date, self.nb_positions * row['Adj Close'])
            print(f'{self.symbol} | {date} | {round(self.current_capital, 2)}')

        self.plot()
        self.save_results()


    def plot(self):
        fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(20, 10))
        self.capital.index = self.capital['date']

        self.api.df['Adj Close'].plot(ax=axes[0], label='Adj. close price')
        self.api.df['50d_ma'].plot(ax=axes[0], label='50 periods MA')
        self.api.df['200d_ma'].plot(ax=axes[0], label='200 periods MA')
        axes[0].legend(loc='upper right')

        self.capital['capital'].plot(ax=axes[1])

        self.api.df['Adj Close'].plot( # Plot entry markers
            markevery=self.find_loc(self.entries['date']),
            marker='o',
            markerfacecolor='green',
            color='green',
            linestyle='',
            ax=axes[0]
        )
        self.api.df['Adj Close'].plot( # Plot exit markers
            markevery=self.find_loc(self.exits['date']),
            marker='o',
            markerfacecolor='red',
            color='red',
            linestyle='',
            ax=axes[0]
        )

        axes[0].set_title(f'{self.symbol} stock price')
        axes[1].set_title('Capital over time')
        plt.savefig(f'results/{self.symbol}-{self.strategy.name}.png')


    def save_results(self):
        try:
            winrate = self.nb_wins / (self.nb_wins + self.nb_loss)
        except ZeroDivisionError:
            winrate = 0
        to_save = {
            'strategy_id': self.strategy.name,
            'symbol': self.symbol,
            'nb_entries': len(self.entries),
            'nb_exits': len(self.exits),
            'starting_capital': INITIAL_CAPITAL,
            'ending_capital': float(self.capital.tail(n=1)['capital']),
            'highest_capital': float(self.capital.max()['capital']),
            'lowest_capital': float(self.capital.min()['capital']),
            'avg_capital': float(self.capital.mean()['capital']),
            'median_capital': float(self.capital.median()['capital']),
            'true_change': float(self.capital.tail(n=1)['capital']) - float(self.capital.head(n=1)['capital']),
            'pct_change': (float(self.capital.tail(n=1)['capital']) - float(self.capital.head(n=1)['capital'])) / float(self.capital.head(n=1)['capital']),
            'loss': self.nb_loss,
            'wins': self.nb_wins,
            'winrate': winrate
        }

        with open('results.json', 'r') as results_file:
            read_results = results_file.read()
            old = json.loads(read_results)
            already_exists = [True for i in old if i['strategy_id'] == self.strategy_id and i['symbol'] == self.symbol]
            if len(already_exists) == 0:
                old.append(to_save)

        with open('results.json', 'w') as results_file:
            json.dump(old, results_file, indent=4)



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
