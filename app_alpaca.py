from alpaca import Alpaca
from datetime import datetime
import time

class TrainingBot:
    def __init__(self, profit_per, loss_per, position_size):
        self.api = Alpaca(
            'PK8EKE8VGG6HF218VV69', 'sOvmOYZw7Y4WufN4Uvn3jiMm6ztFgYEsBwSzgW8K',
            '5Min',
        )
        self.period = 5 # Always in minutes for now (1, 5 or 15)
        self.minutes = self.get_minutes()
        self.symbols = ['PINS', 'GSHD', 'SRNE', 'SEM', 'EBS']
        self.profit_per = profit_per
        self.loss_per = loss_per
        self.position_size = position_size
        self.psa()
        self.run()


    def get_minutes(self):
        nb_in_hour = int(60 / self.period)
        return [self.period * i for i in range(1, nb_in_hour)]


    def run(self):
        while True:
            if datetime.now().minute in self.minutes: # Every x minutes
                if self.api.are_markets_open(): # Not on the same line as to not spam the API
                    positions = self.api.positions()

                    for symbol in self.symbols:
                        data = self.api.compute(symbol)
                        self.check_buy(data, positions)

                    for position in positions:
                        data = self.api.compute(position.symbol)
                        self.check_sell(data, position)

                    self.psa()
                    time.sleep(60)


    def psa(self):
        account = self.api.get_account()

        print('----------------------------------------------------------------------------------------')
        print(f"{datetime.now().strftime('%H:%M:%S')} | Portfolio value: {account['capital']}$ | Today P/L: {account['today_pl']}$ | Open positions: {account['nb_positions']}")
        print('----------------------------------------------------------------------------------------')



    def check_buy(self, data, positions):
        if not self.api.in_positions(data['symbol']): # No duplicates
            if data['10_avg'] > data['50_avg'] and data['rsi'] <= 30: # Buy conditions
                max_price = self.position_size * self.api.capital()
                qty = int(round((max_price / data['close']), 0))
                if qty > 0:
                    self.api.buy(
                        data['symbol'],
                        qty,
                        take_profit=dict(
                            limit_price=data['close'] + (data['close'] * self.profit_per),
                        ),
                        stop_loss=dict(
                            stop_price=data['close'] - (data['close'] * self.loss_per),
                            limit_price=data['close'] - (data['close'] * self.loss_per),
                        )
                    )
                    return True
        print(f"{data['timestamp'].time()} |  --  | {data['symbol']: <4} | {data['close']}$ | {round(data['rsi'], 2)} rsi | {round(data['10_avg'], 2)}$ 10MA | {round(data['50_avg'], 2)}$ 50MA")


    def check_sell(self, data, position):
        if data['rsi'] is not None and data['rsi'] > 70:
            self.sell(data['symbol'], data['close'], position.qty)
            return True




TrainingBot(0.06, 0.03, 0.15)
