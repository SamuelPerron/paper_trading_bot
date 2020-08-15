import json
import matplotlib.pyplot as plt
import pandas as pd
from api_pandas import ApiPandas

INITIAL_CAPITAL = 1000

class Backtest():
    def __init__(self, symbol, strategy):
        with open('strategies.json', 'r') as strategies_file:
            strategies = strategies_file.read()
        strategies_obj = json.loads(strategies)

        self.symbol = symbol
        self.api = ApiPandas(self.symbol)
        self.entries = pd.DataFrame({ 'date': [], 'price': [] })
        self.exits = pd.DataFrame({ 'date': [], 'price': [] })
        self.capital = pd.DataFrame({ 'date': [], 'capital': [] })
        self.current_capital = INITIAL_CAPITAL
        self.nb_positions = 0
        self.strategy_id = strategy
        self.current_stop_loss = None
        self.current_take_gain = None

        try:
            self.strategy = strategies_obj[strategy - 1]
            self.position_size = self.strategy['position_size']
            self.stop_loss = self.strategy['stop_loss']
            self.take_gain = self.strategy['take_gain']
        except IndexError:
            raise ValueError(f'This strategy ({strategy}) does not exist.')

        self.run()


    def find_loc(self, dates):
        marks = []
        for date in dates:
            marks.append(self.api.df.index.get_loc(date))
        return marks


    def check_entry(self, date):
        data = self.api.df.loc[date]
        return data['RSI'] <= 30 and\
            (self.current_capital > 0 and self.nb_positions == 0)


    def check_exit(self, date):
        data = self.api.df.loc[date]
        return (data['RSI'] >= 70 or\
            data['Adj Close'] <= self.current_stop_loss or data['Adj Close'] >= self.current_take_gain) and\
            (self.nb_positions >= 1)


    def update_capital(self, date, move):
        self.capital = self.capital.append({ 'date': date, 'capital': self.current_capital + move }, ignore_index=True)


    def run(self):
        for date, row in self.api.df.iterrows():
            stats = {'date': date, 'price': row['Adj Close']}

            if self.check_entry(date):
                perc_capital = self.current_capital * self.position_size
                qty = int(round(perc_capital / row['Adj Close'], 0))
                if qty > 0:
                    self.entries = self.entries.append(stats, ignore_index=True)
                    self.current_capital -= qty * row['Adj Close']
                    self.nb_positions += qty
                    self.current_stop_loss = row['Adj Close'] - (row['Adj Close'] * self.stop_loss)
                    self.current_take_gain = row['Adj Close'] + (row['Adj Close'] * self.take_gain)
                    print(f'Buy {qty}')

            elif self.nb_positions > 0 and self.check_exit(date):
                self.exits = self.exits.append(stats, ignore_index=True)
                self.current_capital += row['Adj Close'] * self.nb_positions
                self.nb_positions -= self.nb_positions
                self.current_stop_loss = None
                self.current_take_gain = None

            self.update_capital(date, self.nb_positions * row['Adj Close'])

        self.plot()
        self.save_results()


    def plot(self):
        fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(20, 10))
        self.capital.index = self.capital['date']

        self.api.df['Adj Close'].plot(ax=axes[0], label='Adj. close price')
        self.api.df['50d_ma'].plot(ax=axes[0], label='50 days MA')
        self.api.df['200d_ma'].plot(ax=axes[0], label='200 days MA')
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
        plt.savefig('backtest.png')


    def save_results(self):
        to_save = {
            'strategy_id': self.strategy_id,
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
            'pct_change': (float(self.capital.tail(n=1)['capital']) - float(self.capital.head(n=1)['capital'])) / float(self.capital.head(n=1)['capital'])
        }

        with open('results.json', 'r') as results_file:
            read_results = results_file.read()
            old = json.loads(read_results)
            already_exists = [True for i in old if i['strategy_id'] == self.strategy_id and i['symbol'] == self.symbol]
            if len(already_exists) == 0:
                old.append(to_save)

        with open('results.json', 'w') as results_file:
            json.dump(old, results_file, indent=4)



Backtest('CTC-A.TO', 1)
