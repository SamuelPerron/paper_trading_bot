from models import Portfolio
import time
from datetime import datetime, timedelta
import csv
import sys
import matplotlib.pyplot as plt
import matplotlib.dates as dates
from api import PaperApi


class TrainingBot:
    def __init__(self):
        self.api = PaperApi()
        self.portfolio = self.get_portfolio()
        self.symbols = ['AC.TO', 'ACB.TO', 'CTC-A.TO', 'GBR.V', 'BBD-B.TO', 'FVL.TO', 'RTN.V', 'SJR-B.TO']

    def get_portfolio(self):
        return Portfolio(
            capital=1000.00,
            profit_per=0.0101,
            loss_per=0.01,
            position_size=0.11,
            withdraw_money=True
        )

    def run(self):
        oldest_date = datetime.strptime('2018-05-08', '%Y-%m-%d')
        nearest_date = datetime.strptime('2020-05-08', '%Y-%m-%d')
        for increment in range(0, (nearest_date - oldest_date).days):
            date = (oldest_date + timedelta(days=increment)).strftime('%Y-%m-%d')
            for symbol in self.symbols:
                self.make_action(symbol, date)
                self.portfolio.refresh_market_value(date)
            self.portfolio.snapshot(date)
        print(f'''
            Final portfolio:
            Capital: {round(self.portfolio.capital, 2)}$
            Positions value: {round(self.portfolio.market_value, 2)}$
            Total amount: {round(self.portfolio.capital + self.portfolio.market_value + self.portfolio.withdrawed_capital, 2)}$
            Total trades: {self.portfolio.total_trades}
            Overall win %: {round(self.portfolio.wins * 100 / self.portfolio.total_trades, 2)}%
            Best trade: {round(self.portfolio.best_trade)}$
            Worst trade: -{round(self.portfolio.worst_trade)}$
        ''')
        self.plot_results()

    def delete_old_data(self):
        self.portfolio.delete_old_data()

    def make_action(self, symbol, date):
        data = self.api.get(symbol, date)
        # Buy
        self.portfolio.check_for_buy(data, date)
        # Sell
        self.portfolio.check_for_sale(data, date)

    def plot_results(self):
        x = []
        y_total_value = []
        y_withdrawed_capital = []
        y_total_market = []
        with open('data/portfolio.csv', 'r') as csv_file:
            plots = csv.reader(csv_file, delimiter=',')
            i = 0
            for row in plots:
                if i % 7 == 0:
                    x.append(datetime.strptime(row[0], '%Y-%m-%d').date())
                    y_total_value.append(float(row[3]))
                    y_total_market.append(float(row[1]) + float(row[2]))
                    y_withdrawed_capital.append(float(row[4]))
                i = i + 1
        fig, ax = plt.subplots()
        ax.plot(x, y_total_value, label='Total value')
        ax.plot(x, y_total_market, label='Total money in portfolio')
        ax.plot(x, y_withdrawed_capital, label='Withdrawed money')
        ax.set(xlabel='Date', ylabel='$CAD', title='Trading bot')
        fig.autofmt_xdate()
        ax.legend(loc=0)
        ax.grid()
        fig.savefig('results.png')


bot = TrainingBot()
bot.delete_old_data()
bot.run()
