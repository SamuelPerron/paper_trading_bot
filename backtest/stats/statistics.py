import pandas as pd
from datetime import datetime
import csv
import matplotlib.pyplot as plt

class RunData:
    def __init__(self):
        self.entries = pd.DataFrame({ 'date': [], 'price': [], 'qty': [] })
        self.exits = pd.DataFrame({ 'date': [], 'price': [], 'qty': [], 'profit': [] })
        self.capital = pd.DataFrame({ 'date': [], 'capital': [] })
        self.nb_wins = 0
        self.nb_loss = 0


    def get_final_stats(self):
        try:
            winrate = self.nb_wins / (self.nb_wins + self.nb_loss)
        except ZeroDivisionError:
            winrate = 0

        return [
            len(self.entries), len(self.exits), float(self.capital.head(n=1)['capital']),
            float(self.exits['profit'].loc[self.exits['profit'] > 0].mean()),
            float(self.exits['profit'].loc[self.exits['profit'] < 0].mean()),
            float(self.exits['profit'].loc[self.exits['profit'] > 0].max()),
            float(self.exits['profit'].loc[self.exits['profit'] < 0].min()),
            float(self.exits['profit'].mean()), float(self.capital.tail(n=1)['capital']),
            float(self.capital.max()['capital']), float(self.capital.min()['capital']),
            float(self.capital.mean()['capital']), float(self.capital.median()['capital']),
            float(self.capital.tail(n=1)['capital']) - float(self.capital.head(n=1)['capital']),
            (float(self.capital.tail(n=1)['capital']) - float(self.capital.head(n=1)['capital'])) / float(self.capital.head(n=1)['capital']),
            self.nb_loss, self.nb_wins, winrate, self.nb_wins + self.nb_loss
        ]


    def save_run(self, symbol, strategy_id, df):
        stats = self.get_final_stats()
        stats.insert(0, symbol)
        stats.insert(0, strategy_id)
        stats.insert(0, datetime.now())

        with open(f'results.csv', 'a') as results_file:
            writer = csv.writer(results_file)
            writer.writerow(stats)

        self.plot(symbol, strategy_id, df)


    def find_loc(self, dates, df):
        marks = []
        for date in dates:
            marks.append(df.index.get_loc(date))
        return marks


    def plot(self, symbol, strategy_id, df):
        fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(20, 10))
        self.capital.index = self.capital['date']

        df['Adj Close'].plot(ax=axes[0], label='Adj. close price')
        axes[0].legend(loc='upper right')

        self.capital['capital'].plot(ax=axes[1])

        df['Adj Close'].plot( # Plot entry markers
            markevery=self.find_loc(self.entries['date'], df),
            marker='o',
            markerfacecolor='green',
            color='green',
            linestyle='',
            ax=axes[0]
        )
        df['Adj Close'].plot( # Plot exit markers
            markevery=self.find_loc(self.exits['date'], df),
            marker='o',
            markerfacecolor='red',
            color='red',
            linestyle='',
            ax=axes[0]
        )

        axes[0].set_title(f'{symbol} stock price')
        axes[1].set_title('Capital over time')
        plt.savefig(f'results/{symbol}-{strategy_id}.png')
