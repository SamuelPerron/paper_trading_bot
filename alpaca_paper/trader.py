from alpaca_paper import Alpaca
from datetime import datetime
import csv
import os
import time


class Trader:
    CSV_FILE = 'current_symbols.csv'

    def __init__(self, strategy):
        self.alpaca = Alpaca()
        self.strategy = strategy
        self.timeframe = '5Min'
        self.symbols = []

        self.trade()


    def trade(self):
        clock = self.alpaca.clock()
        next_open = datetime.strptime(clock['next_open'][:-6], '%Y-%m-%dT%H:%M:%S')
        time.sleep(2)
        now = datetime.now()
        if clock['is_open']:
            print(f'{now.strftime("%Y-%m-%d %H:%M:%S")}')
            if not os.path.exists(Trader.CSV_FILE):
                self.find_next_symbols()
            
            self.fetch_symbols()

            bars = self.alpaca.bars(self.symbols, big_brain=True)
            for bar in bars:
                if self.strategy.check_for_entry_signal(bar.df):
                    self.buy(bar.symbol, bar.df['c'])

        elif (next_open - now).total_seconds() <= 300:
            self.find_next_symbols()
            print(f'--- NEW SYMBOLS | {now.strftime("%Y-%m-%d")} ---\n{", ".join(self.symbols)}')

        else:
            next_open_minutes = round((next_open - now).total_seconds() / 60, 2)
            if next_open_minutes < 60:
                print(f'Markets open in {next_open_minutes} minutes.')
            else:
                print('Markets closed.')
            self.remove_symbols()


    def buy(self, symbol, price):
        price = price.iloc[-1]
        stop_loss = self.strategy.find_stop_loss(price)
        buying_power = float(self.alpaca.account()['buying_power'])
        qty = self.strategy.find_qty(price, buying_power)
        if qty > 0:
            order = {
                'symbol': symbol,
                'side': 'buy',
                'type': 'market',
                'qty': qty,
                'order_class': 'bracket',
                'take_profit': {
                    'limit_price': str(self.strategy.find_take_profit(price))
                },
                'stop_loss': {
                    'stop_price': str(stop_loss),
                    'limit_price': str(stop_loss - 0.5)
                }
            }
            self.alpaca.new_order(order)
            print(f'--- BUY ORDER ---\n    {symbol} x{qty}')


    def find_next_symbols(self):
        strategy_symbols = self.strategy.find_next_symbols()
        positions_symbols = [position['symbol'] for position in self.alpaca.positions()]
        symbols = strategy_symbols + positions_symbols

        self.create_symbols_file()
        with open(Trader.CSV_FILE, mode='w') as file:
            writer = csv.writer(file)
            for symbol in symbols:
                writer.writerow([symbol,])
        

    def remove_symbols(self):
        if os.path.exists(Trader.CSV_FILE):
            os.remove(Trader.CSV_FILE)


    def fetch_symbols(self):
        with open(Trader.CSV_FILE, mode='r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                self.symbols.append(row[0])
            

    def create_symbols_file(self):
        open(Trader.CSV_FILE, 'w')

        