from models import Portfolio
import time
from datetime import datetime, timedelta
import csv
import sys
import matplotlib.pyplot as plt
import matplotlib.dates as dates
from api import PaperApi


class TrainingBot:
    def __init__(self, profit_per, loss_per, position_size, date_start, date_end):
        self.api = PaperApi()
        self.portfolio = self.get_portfolio(profit_per, loss_per, position_size)
        self.symbols = ['AC.TO', 'ACB.TO', 'CTC-A.TO', 'GBR.V', 'BBD-B.TO', 'FVL.TO', 'RTN.V', 'SJR-B.TO']
        self.date_start = date_start
        self.date_end = date_end

    def get_portfolio(self, profit_per, loss_per, position_size):
        return Portfolio(
            capital=1000.00,
            profit_per=profit_per,
            loss_per=loss_per,
            position_size=position_size,
            withdraw_money=True
        )


    def run(self):
        time_of_day = ['open', 'close']
        oldest_date = datetime.strptime(self.date_start, '%Y-%m-%d')
        nearest_date = datetime.strptime(self.date_end, '%Y-%m-%d')
        for increment in range(0, (nearest_date - oldest_date).days):
            date = (oldest_date + timedelta(days=increment)).strftime('%Y-%m-%d')
            for symbol in self.symbols:
                for time in time_of_day:
                    self.make_action(symbol, date, time)
                    self.portfolio.refresh_market_value(date)
            api = PaperApi()
            if api.are_markets_open(date):
                self.portfolio.snapshot(date)
        print(f'''
            Final portfolio:
            Capital: {round(self.portfolio.capital, 2)}$
            Positions value: {round(self.portfolio.market_value, 2)}$
            Total amount: {round(self.portfolio.capital + self.portfolio.market_value + self.portfolio.withdrawed_capital, 2)}$
            Total trades: {self.portfolio.total_trades}
            Overall win %: {round(self.portfolio.wins * 100 / self.portfolio.total_sells, 2)}%
            Overall difference: {round(((self.portfolio.capital + self.portfolio.market_value + self.portfolio.withdrawed_capital) * 100 / self.portfolio.base_capital) / 100, 2)} %
            Best trade: {round(self.portfolio.best_trade, 2)}$
            Peak: {round(self.portfolio.peak, 2)}$
            Low: {round(self.portfolio.low, 2)}$
        ''')
        self.plot_results()

    def delete_old_data(self):
        self.portfolio.delete_old_data()

    def make_action(self, symbol, date, time):
        data = self.api.get(symbol, date)
        # Buy
        self.portfolio.check_for_buy(data, date, time)
        # Sell
        self.portfolio.check_for_sale(data, date, time)

    def plot_results(self):
        x = []
        y_total_value = []
        y_withdrawed_capital = []
        y_total_market = []

        y_50d_avg = []
        y_200d_avg = []
        y_rsi = []
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


bot = TrainingBot(
    profit_per=0.018,
    loss_per=0.01,
    position_size=0.11,
    date_start='2018-05-08',
    date_end='2020-05-08'
)
bot.delete_old_data()
bot.run()
