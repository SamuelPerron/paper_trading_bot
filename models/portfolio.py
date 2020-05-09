import csv
from api import PaperApi

class Portfolio:
    def __init__(self, capital, profit_per, loss_per, position_size, withdraw_money):
        self.base_capital = capital
        self.capital = capital
        self.market_value = 0
        self.profit_per = profit_per
        self.loss_per = loss_per
        self.position_size = position_size
        self.positions = []
        self.total_value = capital
        self.withdrawed_capital = 0
        self.withdraw_money = withdraw_money
        self.total_trades = 0
        self.wins = 0
        self.best_trade = 0
        self.worst_trade = 99999
        self.peak = 0
        self.low = 99999
        print('New portfolio with 1000$ of base capital')

    def snapshot(self, date):
        with open('data/portfolio.csv', mode='a') as csv_file:
            writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([date, self.capital, self.market_value, self.total_value, self.withdrawed_capital])

    def delete_old_data(self):
        with open('data/portfolio.csv', mode='w') as csv_file:
            csv_file.write('')

    def refresh_market_value(self, date):
        self.market_value = 0
        api = PaperApi()
        for position in self.positions:
            market_price = api.get(position['symbol'], date)
            if market_price is not None:
                self.market_value += float(market_price['close']) * int(position['nb'])
        if self.capital > self.base_capital and self.withdraw_money:
            diff = self.capital - self.base_capital
            self.capital = self.base_capital
            self.withdrawed_capital += diff
        self.total_value = self.market_value + self.capital + self.withdrawed_capital
        if self.total_value > self.peak:
            self.peak = self.total_value
        if self.total_value < self.low:
            self.low = self.total_value


    def remove_position(self, symbol, new_value, date):
        new_positions = [position for position in self.positions if position['symbol'] != symbol]
        self.positions = new_positions
        self.capital += new_value
        if self.best_trade < new_value:
            self.best_trade = new_value
        if self.worst_trade > new_value:
            self.worst_trade = new_value
        self.total_trades += 1
        self.refresh_market_value(date)

    def print_sell(self, date, data, info_positions, result):
        print(f"{date} | SELL | {data['symbol']} x{info_positions['total_nb']} | {result}")

    def check_for_sale(self, data, date):
        if data is not None:
            info_positions = {'total_nb': 0, 'total_value': 0}
            for position in self.positions:
                if position['symbol'] == data['symbol']:
                    info_positions['total_nb'] += position['nb']
                    info_positions['total_value'] += position['bought_price']

            market_value = float(data['close']) * info_positions['total_nb']
            # Profit
            if info_positions['total_nb'] > 0 and \
                (market_value > info_positions['total_value'] + (info_positions['total_value'] * self.profit_per) or (data['rsi'] is not None and data['rsi'] > 70)):
                self.remove_position(data['symbol'], market_value, date)
                self.print_sell(date, data, info_positions, 'PROFIT')
                self.wins += 1
                return True

            # # Loss
            if info_positions['total_nb'] > 0 and \
                (market_value < info_positions['total_value'] - (info_positions['total_value'] * self.loss_per) or (data['rsi'] is not None and data['rsi'] > 70)):
                self.remove_position(data['symbol'], market_value, date)
                self.print_sell(date, data, info_positions, 'LOSS')
                return True
        return False

    def add_position(self, symbol, nb, bought_price, avg_price, date):
        if nb > 0:
            self.positions.append({
                'symbol': symbol,
                'nb': nb,
                'bought_price': bought_price,
                'avg_price': avg_price,
                'date': date,
            })
            self.capital =  self.capital - bought_price
            self.refresh_market_value(date)
            self.total_trades += 1
            print(f'{date} | BUY | {symbol} x{nb}')

    def check_for_buy(self, data, date):
        if data is not None:
            if (data['50d_avg'] > 0 and data['200d_avg'] > 0) and\
                data['50d_avg'] > data['200d_avg'] and\
                data['rsi'] < 70:
                max_price = self.position_size * self.capital
                nb_actions = int(round((max_price / float(data['close'])), 0))
                self.add_position(
                    data['symbol'],
                    nb_actions,
                    nb_actions * float(data['close']),
                    float(data['close']),
                    date
                )
                return True
        return False
